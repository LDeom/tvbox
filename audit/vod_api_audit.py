#!/usr/bin/env python3
"""Read-only smoke test for ordinary MacCMS VOD APIs; writes JSON report only."""
import json
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests

SOURCES = [
    ("量子", "https://cj.lziapi.com/api.php/provide/vod/"),
    ("暴风", "https://bfzyapi.com/api.php/provide/vod/"),
    ("索尼", "https://suoniapi.com/api.php/provide/vod/"),
    ("百度", "https://api.apibdzy.com/api.php/provide/vod/"),
    ("尤酷", "https://api.ukuapi.com/api.php/provide/vod/"),
]
SEARCH_KEYWORD = "流浪地球"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "application/json,text/plain,*/*",
}
TIMEOUT = (10, 25)
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def request_json(url, params):
    response = SESSION.get(url, params=params, timeout=TIMEOUT, allow_redirects=True)
    response.raise_for_status()
    body = response.text.lstrip("\ufeff \r\n\t")
    try:
        payload = response.json()
    except Exception:
        payload = json.loads(body)
    return response, payload


def get_list(payload):
    if isinstance(payload, dict):
        data = payload.get("list")
        if isinstance(data, list):
            return data
        nested = payload.get("data")
        if isinstance(nested, dict) and isinstance(nested.get("list"), list):
            return nested["list"]
    return []


def playable_urls(record):
    """Return up to two distinct HTTP(S) episode URLs across all MacCMS play lines."""
    raw = str(record.get("vod_play_url") or "").strip()
    found = []
    for source_line in raw.split("$$$"):
        for episode in source_line.split("#"):
            item = episode.strip()
            if "$" in item:
                item = item.rsplit("$", 1)[-1].strip()
            if item.startswith(("http://", "https://")) and item not in found:
                found.append(item)
            if len(found) >= 2:
                return found
    return found


def probe_media(url, referer=""):
    if not url.startswith(("http://", "https://")):
        return {"status": "not_http_url", "url_scheme": urlparse(url).scheme}
    headers = {"Range": "bytes=0-0"}
    if referer:
        headers["Referer"] = referer
    try:
        r = SESSION.get(url, headers=headers, stream=True,
                        timeout=TIMEOUT, allow_redirects=True)
        result = {"status_code": r.status_code, "content_type": r.headers.get("Content-Type", ""),
                  "final_host": urlparse(r.url).netloc,
                  "referer_tested": bool(referer)}
        r.close()
        if r.status_code == 206:
            result["status"] = "partial_content"
        elif r.status_code == 200:
            result["status"] = "http_ok"
        elif r.status_code in (301, 302, 307, 308):
            result["status"] = "redirect_response"
        elif r.status_code == 403:
            result["status"] = "forbidden_or_hotlink_protected"
        elif r.status_code == 404:
            result["status"] = "not_found"
        elif r.status_code == 416:
            result["status"] = "range_not_supported_or_invalid"
        else:
            result["status"] = "http_error"
        return result
    except Exception as exc:
        return {"status": "request_error", "error": str(exc)[:240],
                "referer_tested": bool(referer)}


def test_source(name, api):
    result = {"name": name, "api": api, "list": {}, "search": {}, "detail": {},
              "media_probes": []}
    base = api.split("?", 1)[0]
    api_origin = "{0}://{1}/".format(urlparse(base).scheme, urlparse(base).netloc)
    try:
        r, payload = request_json(base, {"ac": "list"})
        records = get_list(payload)
        result["list"] = {
            "status_code": r.status_code, "final_url": r.url,
            "content_type": r.headers.get("Content-Type", ""),
            "code": payload.get("code") if isinstance(payload, dict) else None,
            "total": payload.get("total") if isinstance(payload, dict) else None,
            "count": len(records),
            "sample_fields": sorted(records[0].keys()) if records else [],
        }
        if not records:
            result["list"]["status"] = "empty_or_unrecognized"
            return result
        result["list"]["status"] = "nonempty"

        search_records = []
        try:
            sr, sp = request_json(base, {"ac": "list", "wd": SEARCH_KEYWORD})
            search_records = get_list(sp)
            result["search"] = {"status_code": sr.status_code,
                                "count": len(search_records),
                                "keyword": SEARCH_KEYWORD,
                                "status": "matched" if search_records else "empty"}
        except Exception as exc:
            result["search"] = {"status": "request_or_parse_error", "error": str(exc)[:240]}

        # Try several real IDs, preferring keyword hits, rather than stopping at one detail.
        detail_records = []
        seen_ids = set()
        candidates = search_records + records
        for item in candidates:
            vid = item.get("vod_id")
            if vid is None or str(vid) in seen_ids:
                continue
            seen_ids.add(str(vid))
            if len(seen_ids) >= 5:
                break
        for vid in seen_ids:
            try:
                dr, dp = request_json(base, {"ac": "detail", "ids": vid})
                drecords = get_list(dp)
                chosen = drecords[0] if drecords else {}
                urls = playable_urls(chosen) if chosen else []
                detail_records.append({
                    "vod_id": vid, "status_code": dr.status_code,
                    "count": len(drecords),
                    "status": "has_play_url" if urls else ("detail_without_play_url" if drecords else "empty_detail"),
                    "play_from": chosen.get("vod_play_from"),
                    "play_url_present": bool(urls),
                    "candidate_url_count": len(urls),
                })
                for media_url in urls:
                    if len(result["media_probes"]) >= 10:
                        break
                    probe = probe_media(media_url)
                    probe["vod_id"] = vid
                    if probe.get("status") == "forbidden_or_hotlink_protected":
                        retry = probe_media(media_url, api_origin)
                        retry["vod_id"] = vid
                        retry["referer_retry"] = True
                        result["media_probes"].append({"initial": probe, "referer_retry": retry})
                    else:
                        result["media_probes"].append(probe)
            except Exception as exc:
                detail_records.append({"vod_id": vid, "status": "request_or_parse_error",
                                       "error": str(exc)[:200]})
        result["detail"] = {
            "attempted": len(detail_records),
            "has_play_url": sum(1 for d in detail_records if d.get("play_url_present")),
            "records": detail_records,
        }
    except Exception as exc:
        result["list"] = {"status": "request_or_parse_error", "error": str(exc)[:300]}
    return result

def main():
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "ordinary VOD APIs only; read-only; no source config changes",
        "search_keyword": SEARCH_KEYWORD,
        "results": [],
    }
    for name, api in SOURCES:
        report["results"].append(test_source(name, api))
        time.sleep(1)
    with open("vod-api-audit-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    for item in report["results"]:
        print("{} | list={} | search={} | detail={} | media={}".format(
            item["name"], item["list"].get("status"),
            item["search"].get("status"), item["detail"].get("has_play_url"),
            len(item["media_probes"])))
    print("Report written: vod-api-audit-report.json")
    # The report is useful even if individual providers time out.
    return 0


if __name__ == "__main__":
    sys.exit(main())
