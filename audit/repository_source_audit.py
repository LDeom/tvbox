#!/usr/bin/env python3
"""Read-only repository source inventory and lightweight endpoint smoke tests."""
import json
import os
import re
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
import json5

ROOT = os.getcwd()
SKIP_PARTS = {".git", ".github", "node_modules", "cat/js", "cat/dist", "cat/18_dist"}
SKIP_RE = re.compile(r"(^|/)(adult|18\+|18_dist|adult-live|18_open_config|18_tv_config|pikpakclass18|9918|99188)(/|\.|-|$)", re.I)
EXTS = {".json", ".txt", ".m3u", ".m3u8"}
URL_RE = re.compile(r"https?://[^\s\"'<>\\]+", re.I)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
}
TIMEOUT = (3, 5)
SESSION = requests.Session()
SESSION.headers.update(HEADERS)
MAX_FILES = 400
MAX_URLS_PER_FILE = 3
MAX_PROBES = 120


def skipped(path):
    p = path.replace("\\", "/")
    if SKIP_RE.search(p):
        return True
    return any(p == part or p.startswith(part + "/") for part in SKIP_PARTS)


def urls_in(value, out):
    if isinstance(value, dict):
        for k, v in value.items():
            urls_in(v, out)
    elif isinstance(value, list):
        for v in value:
            urls_in(v, out)
    elif isinstance(value, str):
        for u in URL_RE.findall(value):
            u = u.rstrip("),];}")
            if u not in out:
                out.append(u)


def inspect_file(path):
    ext = os.path.splitext(path)[1].lower()
    result = {"path": path, "type": ext, "bytes": os.path.getsize(path),
              "parse": "not_applicable", "url_count": 0, "probes": []}
    text = ""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            text = f.read()
    except UnicodeDecodeError:
        decoded = False
        for encoding in ("gb18030", "gbk", "utf-16"):
            try:
                with open(path, "r", encoding=encoding) as f:
                    text = f.read()
                result["encoding"] = encoding
                decoded = True
                break
            except Exception:
                pass
        if not decoded:
            result["parse"] = "decode_error"
            result["error"] = "unsupported or binary text encoding"
            return result
    except Exception as exc:
        result["parse"] = "read_error"
        result["error"] = str(exc)[:180]
        return result

    found = []
    if ext == ".json":
        try:
            data = json.loads(text)
            result["parse"] = "valid_json"
            urls_in(data, found)
        except Exception as strict_exc:
            try:
                data = json5.loads(text)
                result["parse"] = "valid_json5"
                urls_in(data, found)
            except Exception as relaxed_exc:
                result["parse"] = "invalid_json_or_json5"
                result["error"] = str(relaxed_exc)[:180]
                result["strict_json_error"] = str(strict_exc)[:120]
                found = URL_RE.findall(text)
    else:
        result["parse"] = "readable_text"
        # Prefer actual playlist/line URLs; exclude URLs embedded in comments.
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") and not line.startswith("#EXTINF"):
                continue
            for u in URL_RE.findall(line):
                u = u.rstrip("),];}")
                if u not in found:
                    found.append(u)
    result["url_count"] = len(found)
    result["hosts"] = sorted({urlparse(u).netloc for u in found if urlparse(u).netloc})[:30]
    result["sampled_urls"] = found[:MAX_URLS_PER_FILE]
    return result


def probe(url):
    try:
        r = SESSION.get(url, headers={"Range": "bytes=0-0"}, stream=True,
                        timeout=TIMEOUT, allow_redirects=True)
        out = {"status_code": r.status_code, "final_host": urlparse(r.url).netloc,
               "content_type": r.headers.get("Content-Type", "")}
        r.close()
        if r.status_code in (200, 206):
            out["status"] = "http_ok"
        elif r.status_code == 403:
            out["status"] = "access_restricted"
        elif r.status_code == 404:
            out["status"] = "not_found"
        elif r.status_code in (301, 302, 307, 308):
            out["status"] = "redirect"
        else:
            out["status"] = "http_error"
        return out
    except Exception as exc:
        return {"status": "request_error", "error": str(exc)[:180]}


def main():
    paths = []
    for base, dirs, files in os.walk(ROOT):
        relbase = os.path.relpath(base, ROOT).replace("\\", "/")
        dirs[:] = [d for d in dirs if not skipped((relbase + "/" + d).lstrip("./"))]
        for name in files:
            path = os.path.join(base, name)
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            if os.path.splitext(name)[1].lower() in EXTS and not skipped(rel):
                paths.append(rel)
    paths = sorted(paths)[:MAX_FILES]
    report = {"generated_at": datetime.now(timezone.utc).isoformat(),
              "scope": "non-adult JSON/TXT/M3U source/config files; read-only",
              "file_count": len(paths), "max_files": MAX_FILES,
              "max_urls_per_file": MAX_URLS_PER_FILE, "max_probes": MAX_PROBES,
              "results": []}
    total = 0
    for path in paths:
        item = inspect_file(os.path.join(ROOT, path))
        for url in item.pop("sampled_urls", []):
            if total >= MAX_PROBES:
                break
            item["probes"].append({"url": url, **probe(url)})
            total += 1
            time.sleep(0.15)
        report["results"].append(item)
    report["probe_count"] = total
    report["summary"] = {
        "valid_json": sum(1 for x in report["results"] if x["parse"] == "valid_json"),
        "valid_json5": sum(1 for x in report["results"] if x["parse"] == "valid_json5"),
        "invalid_json_or_json5": sum(1 for x in report["results"] if x["parse"] == "invalid_json_or_json5"),
        "decode_or_read_errors": sum(1 for x in report["results"] if x["parse"] in ("decode_error", "read_error")),
        "files_with_urls": sum(1 for x in report["results"] if x["url_count"]),
        "http_ok": sum(1 for x in report["results"] for p in x["probes"] if p["status"] == "http_ok"),
        "restricted": sum(1 for x in report["results"] for p in x["probes"] if p["status"] == "access_restricted"),
        "not_found": sum(1 for x in report["results"] for p in x["probes"] if p["status"] == "not_found"),
        "request_errors": sum(1 for x in report["results"] for p in x["probes"] if p["status"] == "request_error"),
    }
    with open("repository-source-audit-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report["summary"], ensure_ascii=False))
    print("Files scanned: {} | URL probes: {}".format(len(paths), total))


if __name__ == "__main__":
    main()
