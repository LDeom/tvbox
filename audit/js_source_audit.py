#!/usr/bin/env python3
"""Read-only JS source syntax and literal endpoint smoke audit."""
import base64
import gzip
import json
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

ROOT = os.getcwd()
SOURCE_DIRS = ("js", "FTY", "cat/js", "cat/tjs/js", "xiaosa/js")
SKIP_DIRS = (".git", "cat/js/lib", "cat/tjs/lib")
SKIP_NAMES = {
    "cheerio.min.js", "crypto-js.js", "crypto-hiker.js", "drpy2.js",
    "drpy2.min.js", "drpy-core-lite.min.js", "gbk.js", "json5.js",
    "node-rsa.js", "pako.min.js", "sortName.js", "uri.min.js",
    "jinja.js", "jinja.min.js", "mod.js", "app.js", "build.js",
}
ADULT_RE = re.compile(
    r"(^|/)(adult[^/]*|[^/]*18[^/]*|missav[^/]*|jable[^/]*|sehuatang[^/]*|asianx[^/]*)(/|$)",
    re.I,
)
URL_RE = re.compile(r"https?://[^\s\"'<>\\]+", re.I)
TIMEOUT = (3, 5)
MAX_PROBES = 100
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Range": "bytes=0-0",
}


def excluded(rel):
    rel = rel.replace("\\", "/")
    if ADULT_RE.search(rel):
        return True
    if any(rel == p or rel.startswith(p + "/") for p in SKIP_DIRS):
        return True
    name = os.path.basename(rel).lower()
    return name in SKIP_NAMES or name.endswith(".min.js")


def read_source(path):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8-sig", errors="replace").strip()
    if text.startswith("H4sIA"):
        try:
            decoded = gzip.decompress(base64.b64decode(text)).decode("utf-8", errors="replace")
            return decoded, "gzip_base64"
        except Exception:
            pass
    if text.startswith("**"):
        try:
            decoded = base64.b64decode(text[2:]).decode("utf-8", errors="replace")
            return decoded, "base64"
        except Exception:
            pass
    return text, "plain"


def check_js(path):
    source, encoding = read_source(path)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
            f.write(source)
            temp_path = f.name
        p = subprocess.run(
            ["node", "--check", temp_path],
            capture_output=True, text=True, timeout=12
        )
        return {
            "syntax": "ok" if p.returncode == 0 else "syntax_error",
            "encoding": encoding,
            "error": (p.stderr or p.stdout).strip()[:500] if p.returncode else ""
        }
    except FileNotFoundError:
        return {"syntax": "node_unavailable", "encoding": encoding, "error": "node executable not found"}
    except subprocess.TimeoutExpired:
        return {"syntax": "check_timeout", "encoding": encoding, "error": "node --check exceeded 12 seconds"}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


def extract_urls(path):
    try:
        data, _ = read_source(path)
    except Exception:
        return []
    found = []
    for raw in URL_RE.findall(data):
        url = raw.rstrip("),];}")
        if any(x in url for x in ("{", "}", "&&")):
            continue
        host = urlparse(url).netloc
        if host and url not in found:
            found.append(url)
    return found


def probe(url):
    try:
        r = requests.get(
            url, headers=HEADERS, stream=True, allow_redirects=True,
            timeout=TIMEOUT
        )
        item = {
            "url": url,
            "status_code": r.status_code,
            "final_host": urlparse(r.url).netloc,
            "content_type": r.headers.get("Content-Type", "")
        }
        r.close()
        if r.status_code in (200, 206):
            item["status"] = "http_ok"
        elif r.status_code == 403:
            item["status"] = "access_restricted"
        elif r.status_code == 404:
            item["status"] = "not_found"
        elif r.status_code in (301, 302, 307, 308):
            item["status"] = "redirect"
        else:
            item["status"] = "http_error"
        return item
    except Exception as exc:
        return {"url": url, "status": "request_error", "error": str(exc)[:180]}


def main():
    files = []
    for root in SOURCE_DIRS:
        if not os.path.isdir(root):
            continue
        for base, dirs, names in os.walk(root):
            relbase = os.path.relpath(base, ROOT).replace("\\", "/")
            dirs[:] = [d for d in dirs if not excluded((relbase + "/" + d).lstrip("./"))]
            for name in names:
                rel = os.path.relpath(os.path.join(base, name), ROOT).replace("\\", "/")
                if name.lower().endswith(".js") and not excluded(rel):
                    files.append(rel)
    files = sorted(set(files))
    results = []
    all_urls = []
    for rel in files:
        check = check_js(os.path.join(ROOT, rel))
        urls = extract_urls(os.path.join(ROOT, rel))
        results.append({
            "path": rel,
            "bytes": os.path.getsize(os.path.join(ROOT, rel)),
            **check,
            "literal_url_count": len(urls),
            "sample_urls": urls[:5]
        })
        for u in urls:
            if u not in all_urls:
                all_urls.append(u)
    probes = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(probe, u) for u in all_urls[:MAX_PROBES]]
        for f in as_completed(futures):
            probes.append(f.result())
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "non-adult JS source files; static syntax check and literal URL smoke probes",
        "source_dirs": list(SOURCE_DIRS),
        "file_count": len(files),
        "probe_count": len(probes),
        "syntax_summary": {
            "ok": sum(x["syntax"] == "ok" for x in results),
            "syntax_error": sum(x["syntax"] == "syntax_error" for x in results),
            "check_timeout": sum(x["syntax"] == "check_timeout" for x in results),
            "node_unavailable": sum(x["syntax"] == "node_unavailable" for x in results)
        },
        "probe_summary": {
            "http_ok": sum(x["status"] == "http_ok" for x in probes),
            "restricted": sum(x["status"] == "access_restricted" for x in probes),
            "not_found": sum(x["status"] == "not_found" for x in probes),
            "request_errors": sum(x["status"] == "request_error" for x in probes),
            "other_http": sum(x["status"] == "http_error" for x in probes)
        },
        "results": results,
        "probes": probes
    }
    with open("js-source-audit-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps({
        "files": len(files),
        "syntax": report["syntax_summary"],
        "probes": len(probes),
        "probe_summary": report["probe_summary"]
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
