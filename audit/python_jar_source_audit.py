#!/usr/bin/env python3
"""Read-only Python source syntax, JAR integrity and checksum-reference audit."""
import hashlib
import json
import os
import re
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path.cwd()
PY_DIRS = ("py", "xiaosa/py", "tools", "json", "audit")
ADULT_RE = re.compile(r"(^|/)(adult[^/]*|[^/]*18[^/]*|missav[^/]*|jable[^/]*|sehuatang[^/]*|asianx[^/]*)(/|$)", re.I)
URL_RE = re.compile(r"https?://[^\s\"'<>\\]+", re.I)
JAR_REF_RE = re.compile(r"(?:\./)?jar/([^;\"']+\.jar);md5;([a-fA-F0-9]{32})", re.I)
TIMEOUT = (3, 5)
MAX_PROBES = 50
HEADERS = {"User-Agent": "Mozilla/5.0", "Range": "bytes=0-0"}


def excluded(rel):
    rel = rel.replace("\\", "/")
    return bool(ADULT_RE.search(rel))


def scan_python():
    results = []
    urls = []
    for root in PY_DIRS:
        base = ROOT / root
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if excluded(rel):
                continue
            try:
                source = path.read_text(encoding="utf-8-sig")
                compile(source, rel, "exec")
                syntax, error = "ok", ""
            except UnicodeDecodeError:
                syntax, error = "decode_error", "not UTF-8 source"
                source = ""
            except SyntaxError as exc:
                syntax, error = "syntax_error", f"line {exc.lineno}: {exc.msg}"
                try:
                    source = path.read_text(encoding="utf-8-sig", errors="replace")
                except Exception:
                    source = ""
            results.append({"path": rel, "bytes": path.stat().st_size, "syntax": syntax, "error": error})
            for u in URL_RE.findall(source):
                u = u.rstrip("),];}")
                if u not in urls and not any(x in u for x in ("{", "}")):
                    urls.append(u)
    return results, urls


def scan_jars():
    results = []
    jar_dir = ROOT / "jar"
    if jar_dir.exists():
        for path in sorted(jar_dir.glob("*.jar")):
            md5 = hashlib.md5(path.read_bytes()).hexdigest()
            sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
            valid_zip = zipfile.is_zipfile(path)
            bad_member = None
            if valid_zip:
                try:
                    with zipfile.ZipFile(path) as z:
                        bad_member = z.testzip()
                except Exception as exc:
                    bad_member = str(exc)[:200]
            results.append({
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "md5": md5,
                "sha256": sha256,
                "zip_valid": valid_zip,
                "bad_member": bad_member,
                "integrity": "ok" if valid_zip and bad_member is None else "invalid_or_corrupt"
            })
    return results


def scan_jar_refs(jars):
    jar_by_name = {Path(x["path"]).name: x for x in jars}
    refs = []
    for ext in (".json", ".txt", ".js"):
        for path in ROOT.rglob("*" + ext):
            rel = path.relative_to(ROOT).as_posix()
            if excluded(rel) or any(part in rel.split("/") for part in (".git", "node_modules", "dist", "18_dist")):
                continue
            try:
                text = path.read_text(encoding="utf-8-sig", errors="replace")
            except Exception:
                continue
            for match in JAR_REF_RE.finditer(text):
                name, expected = match.group(1), match.group(2).lower()
                actual = jar_by_name.get(Path(name).name)
                refs.append({
                    "source_file": rel,
                    "jar": name,
                    "expected_md5": expected,
                    "actual_md5": actual["md5"] if actual else None,
                    "status": "missing_jar" if not actual else ("md5_match" if actual["md5"] == expected else "md5_mismatch")
                })
    return refs


def probe(url):
    try:
        r = requests.get(url, headers=HEADERS, stream=True, allow_redirects=True, timeout=TIMEOUT)
        item = {"url": url, "status_code": r.status_code, "final_host": urlparse(r.url).netloc}
        r.close()
        if r.status_code in (200, 206):
            item["status"] = "http_ok"
        elif r.status_code == 403:
            item["status"] = "access_restricted"
        elif r.status_code == 404:
            item["status"] = "not_found"
        else:
            item["status"] = "http_error"
        return item
    except Exception as exc:
        return {"url": url, "status": "request_error", "error": str(exc)[:160]}


def main():
    py, urls = scan_python()
    jars = scan_jars()
    refs = scan_jar_refs(jars)
    probes = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(probe, u) for u in urls[:MAX_PROBES]]
        for f in as_completed(futures):
            probes.append(f.result())
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "non-adult Python source syntax, JAR archive integrity and configured MD5 references",
        "python_file_count": len(py),
        "python_summary": {
            "ok": sum(x["syntax"] == "ok" for x in py),
            "syntax_error": sum(x["syntax"] == "syntax_error" for x in py),
            "decode_error": sum(x["syntax"] == "decode_error" for x in py)
        },
        "jar_count": len(jars),
        "jar_summary": {
            "valid": sum(x["integrity"] == "ok" for x in jars),
            "invalid": sum(x["integrity"] != "ok" for x in jars)
        },
        "jar_reference_count": len(refs),
        "jar_reference_summary": {
            "md5_match": sum(x["status"] == "md5_match" for x in refs),
            "md5_mismatch": sum(x["status"] == "md5_mismatch" for x in refs),
            "missing_jar": sum(x["status"] == "missing_jar" for x in refs)
        },
        "url_probe_count": len(probes),
        "url_probe_summary": {
            "http_ok": sum(x["status"] == "http_ok" for x in probes),
            "restricted": sum(x["status"] == "access_restricted" for x in probes),
            "not_found": sum(x["status"] == "not_found" for x in probes),
            "request_errors": sum(x["status"] == "request_error" for x in probes),
            "other_http": sum(x["status"] == "http_error" for x in probes)
        },
        "python_results": py,
        "jars": jars,
        "jar_references": refs,
        "url_probes": probes
    }
    with open("python-jar-source-audit-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps({
        "python_files": len(py), "python": report["python_summary"],
        "jars": len(jars), "jar": report["jar_summary"],
        "jar_references": len(refs), "references": report["jar_reference_summary"],
        "url_probes": len(probes), "urls": report["url_probe_summary"]
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
