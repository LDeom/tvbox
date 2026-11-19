#!/usr/bin/env python3
"""Discover and smoke-test additional non-adult MacCMS-style VOD API endpoints."""
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse

import requests

ROOT = os.getcwd()
EXTS = {".json", ".txt", ".js"}
SKIP_DIRS = {".git", ".github", "node_modules", "cat/18_dist", "cat/dist", "cat/js/lib", "cat/tjs/lib"}
ADULT_RE = re.compile(r"(^|/)(adult[^/]*|[^/]*18[^/]*|missav[^/]*|jable[^/]*|sehuatang[^/]*|asianx[^/]*)(/|$)", re.I)
ADULT_HOST_RE = re.compile(r"(sexnguon|91md|missav|jable|sehuatang|asianx|porn|adult)", re.I)
URL_RE = re.compile(r"https?://[^\s\"'<>\\]+", re.I)
API_RE = re.compile(r"/(?:api\.php/)?provide/vod/?$", re.I)
KNOWN_TESTED = {
    "https://cj.lziapi.com/api.php/provide/vod/",
    "https://bfzyapi.com/api.php/provide/vod/",
    "https://suoniapi.com/api.php/provide/vod/",
    "https://api.apibdzy.com/api.php/provide/vod/",
    "https://api.ukuapi.com/api.php/provide/vod/",
}
MAX_APIS = 25
TIMEOUT = (5, 8)
HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120 Safari/537.36", "Accept": "application/json,*/*"}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def excluded(rel):
    rel = rel.replace("\\", "/")
    if ADULT_RE.search(rel):
        return True
    return any(rel == d or rel.startswith(d + "/") for d in SKIP_DIRS)


def discover():
    found = {}
    for base, dirs, files in os.walk(ROOT):
        relbase = os.path.relpath(base, ROOT).replace("\\", "/")
        dirs[:] = [d for d in dirs if not excluded((relbase + "/" + d).lstrip("./"))]
        for name in files:
            rel = os.path.relpath(os.path.join(base, name), ROOT).replace("\\", "/")
            if os.path.splitext(name)[1].lower() not in EXTS or excluded(rel):
                continue
            try:
                text = open(os.path.join(ROOT, rel), "r", encoding="utf-8-sig", errors="replace").read()
            except Exception:
                continue
            for raw in URL_RE.findall(text):
                url = raw.rstrip("),];}")
                p = urlparse(url)
                if not p.netloc or ADULT_HOST_RE.search(p.netloc) or not API_RE.search(p.path):
                    continue
                base_url = urlunparse((p.scheme, p.netloc, p.path.rstrip("/") + "/", "", "", ""))
                if base_url not in KNOWN_TESTED:
                    found.setdefault(base_url, set()).add(rel)
    return [{"endpoint": k, "files": sorted(v)} for k, v in sorted(found.items())][:MAX_APIS]


def get_json(url, params):
    try:
        r = SESSION.get(url, params=params, timeout=TIMEOUT)
        code = r.status_code
        final = r.url
        ctype = r.headers.get("Content-Type", "")
        data = r.json() if code == 200 else None
        return {"status_code": code, "final_url": final, "content_type": ctype, "data": data}
    except Exception as exc:
        return {"status": "request_or_parse_error", "error": str(exc)[:220]}


def records(payload):
    if not isinstance(payload, dict):
        return []
    data = payload.get("data", payload)
    if isinstance(data, dict):
        rows = data.get("list") or data.get("vod_list") or []
        return rows if isinstance(rows, list) else []
    if isinstance(data, list):
        return data
    return []


def playable_urls(play):
    found = []
    if not isinstance(play, str):
        return found
    for line in play.split("$$$"):
        for episode in line.split("#"):
            candidate = episode.split("$", 1)[1] if "$" in episode else episode
            for url in URL_RE.findall(candidate):
                url = url.rstrip("),];}")
                if url not in found:
                    found.append(url)
    return found


def probe_media(url):
    parsed = urlparse(url)
    if parsed.path.lower().endswith((".html", ".htm")) or parsed.netloc.lower().endswith(("iqiyi.com", "youku.com", "mgtv.com", "qq.com")):
        return {"status": "external_video_page_not_direct_media", "host": parsed.netloc}
    try:
        r = SESSION.get(url, headers={"Range": "bytes=0-0"}, stream=True, timeout=TIMEOUT, allow_redirects=True)
        out = {"status_code": r.status_code, "final_host": urlparse(r.url).netloc, "content_type": r.headers.get("Content-Type", "")}
        r.close()
        if r.status_code in (200, 206):
            out["status"] = "http_ok"
        elif r.status_code == 403:
            out["status"] = "access_restricted"
        elif r.status_code == 404:
            out["status"] = "not_found"
        else:
            out["status"] = "http_error"
        return out
    except Exception as exc:
        return {"status": "request_error", "error": str(exc)[:180]}


def test_one(item):
    endpoint = item["endpoint"]
    out = {"endpoint": endpoint, "referenced_by": item["files"]}
    listing = get_json(endpoint, {"ac": "list", "pg": 1})
    if "data" not in listing or not isinstance(listing.get("data"), dict):
        out["list"] = {k: v for k, v in listing.items() if k != "data"}
        return out
    rows = records(listing["data"])
    out["list"] = {
        "status_code": listing["status_code"],
        "final_url": listing["final_url"],
        "content_type": listing["content_type"],
        "count": len(rows),
        "total": listing["data"].get("total"),
        "status": "nonempty" if rows else "empty"
    }
    search = get_json(endpoint, {"ac": "list", "wd": "流浪地球", "pg": 1})
    srows = records(search.get("data")) if isinstance(search.get("data"), dict) else []
    out["search"] = {
        "status": "matched" if srows else ("no_match" if isinstance(search.get("data"), dict) else "request_or_parse_error"),
        "count": len(srows),
        "error": search.get("error")
    }
    candidate = (srows or rows)
    if not candidate or not isinstance(candidate[0], dict):
        out["detail"] = {"status": "no_record_id"}
        return out
    vid = candidate[0].get("vod_id") or candidate[0].get("id")
    if vid is None:
        out["detail"] = {"status": "no_record_id"}
        return out
    detail = get_json(endpoint, {"ac": "detail", "ids": str(vid)})
    drows = records(detail.get("data")) if isinstance(detail.get("data"), dict) else []
    record = drows[0] if drows and isinstance(drows[0], dict) else {}
    media = playable_urls(record.get("vod_play_url", ""))
    out["detail"] = {
        "status_code": detail.get("status_code"),
        "status": "has_play_url" if media else ("empty_play_url" if record else "request_or_parse_error"),
        "vod_id": str(vid),
        "play_from": record.get("vod_play_from"),
        "candidate_media_urls": len(media)
    }
    out["media_probes"] = [{"url": u, **probe_media(u)} for u in media[:2]]
    return out


def main():
    found = discover()
    results = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(test_one, x) for x in found]
        for f in as_completed(futures):
            results.append(f.result())
    results.sort(key=lambda x: x["endpoint"])
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "additional non-adult MacCMS-style APIs; excludes previously tested five APIs and adult-indicator hosts",
        "discovered_count": len(found),
        "tested_count": len(results),
        "results": results,
        "summary": {
            "list_nonempty": sum(x.get("list", {}).get("status") == "nonempty" for x in results),
            "search_matched": sum(x.get("search", {}).get("status") == "matched" for x in results),
            "detail_has_play_url": sum(x.get("detail", {}).get("status") == "has_play_url" for x in results),
            "media_http_ok": sum(p.get("status") == "http_ok" for x in results for p in x.get("media_probes", [])),
            "media_restricted": sum(p.get("status") == "access_restricted" for x in results for p in x.get("media_probes", [])),
            "media_not_found": sum(p.get("status") == "not_found" for x in results for p in x.get("media_probes", [])),
            "external_video_pages": sum(p.get("status") == "external_video_page_not_direct_media" for x in results for p in x.get("media_probes", []))
        }
    }
    with open("additional-vod-api-audit-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
