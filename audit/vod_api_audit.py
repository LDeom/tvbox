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


def playable_url(record):
    raw = str(record.get("vod_play_url") or "").strip()
    if not raw:
        return ""
    # MacCMS commonly uses line separator $$ and episode separator #.
    first_line = raw.split("$$", 1)[0]
    first_item = first_line.split("#", 1)[0]
    if "$" in first_item:
        first_item = first_item.rsplit("$", 1)[-1]
    return first_item.strip()


def probe_media(url):
    if not url.startswith(("http://", "https://")):
        return {"status": "not_http_url", "url_scheme": urlparse(url).scheme}
    try:
        r = SESSION.get(url, headers={"Range": "bytes=0-0"}, stream=True,
                        timeout=TIMEOUT, allow_redirects=True)
        result = {"status_code": r.status_code, "content_type": r.headers.get("Content-Type", ""),
                  "final_host": urlparse(r.url).netloc}
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
        return {"status": "request_error", "error": str(exc)[:240]}


def test_source(name, api):
    result = {"name": name, "api": api, "list": {}, "search": {}, "detail": {},
              "media_probe": {"status": "not_attempted"}}
    base = api.split("?", 1)[0]
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

        try:
            sr, sp = request_json(base, {"ac": "list", "wd": SEARCH_KEYWORD})
            srecords = get_list(sp)
            result["search"] = {"status_code": sr.status_code,
                                "count": len(srecords),
                                "keyword": SEARCH_KEYWORD,
                                "status": "matched" if srecords else "empty"}
        except Exception as exc:
            result["search"] = {"status": "request_or_parse_error", "error": str(exc)[:240]}

        # Check up to five real IDs from the live list; stop after a detail has play URLs.
        detail_errors = []
        for item in records[:5]:
            vid = item.get("vod_id")
            if vid is None:
                continue
            try:
                dr, dp = request_json(base, {"ac": "detail", "ids": str(vid)})
                drecords = get_list(dp)
                chosen = drecords[0] if drecords else {}
                play = str(chosen.get("vod_play_url") or "").strip()
                result["detail"] = {
                    "status_code": dr.status_code, "vod_id": str(vid),
                    "count": len(drecords),
                    "status": "has_play_url" if play else ("detail_without_play_url" if drecords else "empty_detail"),
                    "fields": sorted(chosen.keys()) if chosen else [],
                    "play_from": chosen.get("vod_play_from"),
                    "play_url_present": bool(play),
                    "play_url_length": len(play),
                }
                if play:
                    media = playable_url(chosen)
                    result["media_probe"] = probe_media(media) if media else {"status": "no_extractable_url"}
                    break
            except Exception as exc:
                detail_errors.append({"vod_id": str(vid), "error": str(exc)[:200]})
        if not result["detail"]:
            result["detail"] = {"status": "no_vod_id_in_sample", "errors": detail_errors}
        elif detail_errors:
            result["detail"]["earlier_errors"] = detail_errors
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
            item["search"].get("status"), item["detail"].get("status"),
            item["media_probe"].get("status")))
    print("Report written: vod-api-audit-report.json")
    # The report is useful even if individual providers time out.
    return 0


if __name__ == "__main__":
    sys.exit(main())
