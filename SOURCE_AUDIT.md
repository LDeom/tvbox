# TVBox source audit (preliminary)

Audit date: 2026-11-19  
Repository: `LDeom/tvbox`  
Base: `master` at `641db3307d076547a383841491b17f9280433c5e`  
Working branch: `audit/repair-sources-2026-11`

## Repairs made on this branch

1. `0825.json`: repaired missing Wogg-style filter-data references by pointing them to the existing `./json/wogg.json`.
2. `js.json`: repaired the same missing filter-data references. Removed the active `西门[V2]` entry because its referenced `./js/西门[V2].js` script is absent from the repository.
3. `dianshi.json` and `tools/dianshi.json`: replaced the missing `./tv.txt` live-list path with the existing `./list.txt` playlist. The replacement uses the repository's existing channel-name/URL text format.

All four edited JSON files were parsed successfully after the changes. Their scanned local file references resolve against files in the repository.

## Playlist inventory (static parsing only)

URL counts below describe entries found in repository files; they do **not** mean the streams were reachable or playable during this audit.

| File | URL entries | Distinct hosts | Notes |
|---|---:|---:|---|
| `list.m3u` | 860 | 142 | General TV playlist |
| `list.txt` | 202 | 18 | General TV text playlist |
| `tvboxtv.txt` | 1,391 | 110 | General TV text playlist |
| `tvlive.txt` | 1,420 | 110 | General TV text playlist |
| `ITV.txt` | 637 | 1 | Single-provider domain |
| `radio.m3u` | 1,478 | 111 | Radio playlist |
| `radio.txt` | 1,478 | 111 | Same 1,456 unique stream URLs as `radio.m3u`, alternate format |

The two general TV files `tvboxtv.txt` and `tvlive.txt` share 1,387 distinct URLs. `tvlive.txt` has 32 URLs not found in `tvboxtv.txt`; `tvboxtv.txt` has 4 not found in `tvlive.txt`.

The repository also contains separate adult-content playlists/configuration. These have been classified separately and are not included in any proposed public mirror distribution.

## Other findings and cautions

- `listx.m3u` is **not empty**. The Git blob contains about 6.27 MB of data; a normal file-content read returned an empty result for this large file, so the blob was used to verify it.
- The `XYQ.json` reference to `XYQHiker/玩偶妹妹.json` is inside a commented-out entry, so it is not an active missing dependency.
- The percent-encoded path in `fty.json` resolves to the existing `FTY/兔小贝.js`.
- Some nested XBPQ/XYQHiker source files contain comments or trailing commas. A strict JSON parser rejects those forms, but that alone does not prove they are unusable; their expected parser behavior must be confirmed before rewriting them.
- Static URL parsing and local-reference checks do not validate DNS, HTTP responses, authentication, geo-restrictions, expiry, or media playback. Network probes from the audit environment failed at DNS resolution, so no stream is marked as playback-tested.
- The repository README disclaims accuracy/legality and explicitly warns against use within mainland China. No mainland mirror/CDN links are being generated until the rights and distribution constraints are resolved.

## Status

This is a preliminary static audit, not a certification that every source works. No changes have been made to `master`; all repairs are isolated on the working branch for review.

## Follow-up checks (2026-11-19)

Additional configuration files checked after the first report:

- `jsm.json`: 40 local file references scanned; no missing local targets found.
- `0821.json`: 36 references; no missing local targets found.
- `0826.json`: 1 reference; no missing local targets found.
- `0827.json`: 10 references; no missing local targets found.
- `9918.json` and `99188.json`: 21 references each; no missing local targets found.
- `fty.json`: 5 references; no missing local targets found. Its percent-encoded path resolves to the existing FTY script.
- `cat/tjs/open_config.json`: 34 references; no missing local targets found.
- `xiaosa/api.json`: 8 references; no missing local targets found. Its `./spider.jar` correctly resolves to `xiaosa/spider.jar`.
- `XYQ.json`: the missing-looking `玩偶妹妹.json` reference is in a commented-out source entry, not an active dependency.

These checks cover the principal top-level configurations and selected nested configuration groups, not every one of the repository's JSON files. Strict JSON parsing also rejects some source files that use comments/trailing commas (JSON5-like syntax); those were not rewritten because the consuming parser's exact behavior must be confirmed first.

## Full JSON inventory pass (2026-11-19)

A repository-tree inventory identified **257 JSON/JSON5-named files**. All 257 were retrieved and checked with a strict JSON parser after stripping an optional UTF-8 BOM. This is a syntax screening, not proof that each provider/plugin can load the file.

- The main configuration files and nested config references were checked with their applicable path bases. No confirmed missing local dependency was found in the checked configurations.
- Important path-base cases:
  - `tools/dianshi.json` and `tools/jsm.json` resolve their `./...` references from the repository root, not from `tools/`; their 34 and 33 references respectively resolve.
  - `lib/token.json` resolves its six `./...` resource references from `lib/`; all six targets exist.
  - `cat/js/config_open.json` has 63 script references; all 63 targets exist under `cat/js/`.
  - `cat/tjs/open_config.json`, `18_open_config.json`, `18_tv_config.json`, and `tv_config.json` have 34, 10, 10, and 28 local references respectively; all targets exist.
  - `xiaosa/api.json` has eight local references, all present, including `xiaosa/spider.jar`.

### Strict-parser exceptions requiring runtime-parser confirmation

Strict JSON parsing reports errors in the following files. Most observed errors are consistent with comments or trailing commas/JSON5-like syntax; these are **not automatically classified as unusable** until the parser used by the consuming app/plugin is confirmed.

- Root: `XYQ.json`
- `XBPQ/`: `bttt.json`, `养生堂.json`
- `XYQHiker/`: `996影视.json`, `七新影视.json`, `剧圈影视.json`, `可可影视.json`, `哔嘀影视.json`, `巴士动漫.json`, `播视童趣.json`, `来看影视.json`, `河马短剧.json`, `爱你短剧.json`, `玩偶哥哥.json`, `电影港.json`, `短剧屋.json`
- `xiaosa/XBPQ/`: `养生堂.json`
- `xiaosa/XYQHiker/`: `BT天堂.json`, `七新影视.json`, `九八影视.json`, `八号影视.json`, `剧圈影视.json`, `巴士动漫.json`, `来看影视.json`, `电影港.json`, `盒子影视.json`, `看看影视.json`, `短剧屋.json`, `骚火影视.json`
- `xiaosa/json/`: `BSDM.json`, `DYG.json`, `JQYS.json`
- `json/`: `BSDM.json`, `DYG.json`, `JQYS.json`, `api黑木耳.json`, `dj看球.json`, `dmw.json`, `nmys.json`, `企鹅直播.json`, `厂长影视.json`
- `FTY/`: `nmys.json`
- `XYQBiu/`: `网易CC直播.json`

The inventory found **43 strict-parser exceptions**. They are recorded for follow-up; no speculative mass-rewrite or deletion was performed.

## Script dependency audit — first pass (2026-11-19)

Repository inventory: 696 JavaScript files and 62 Python files. This pass focused on primary configuration entry points and representative runtime/build scripts; it is not yet a line-by-line validation of all 758 scripts.

### JavaScript entry points checked

- `lib/drpy2.min.js` imports `./drpy-core-lite.min.js` and `./uri.min.js`; both files exist under `lib/`.
- `FTY/drpy2.js` imports `./uri.min.js`, which exists under `FTY/`. It also uses `assets://js/lib/cheerio.min.js` and `assets://js/lib/crypto-js.js` (runtime asset-scheme dependencies) and remote template/GBK resources. These are not ordinary repository-relative paths and require validation in the target app/runtime.
- `js/drpy.js`, `js/cilixiong.js`, `js/678.js`, `js/茶杯狐.js`, `FTY/模板.js`, `FTY/斗鱼.js`, and `cat/js/douban_open.js` were inspected for obvious relative imports; none were detected by the first-pass import scan.
- Configuration strings were parsed as structured JSON for `js.json`, `0825.json`, `dianshi.json`, `tools/dianshi.json`, and `xiaosa/api.json`. No confirmed missing local references were found after applying the correct path base and stripping metadata suffixes. In particular, `tools/dianshi.json` references are rooted at the repository root, not at `tools/`.

### Python and build-script observations

- Eight Python providers referenced by configs were sampled. They import `base.spider`; no `base/` package or `spider.py` module exists in this repository tree. This may be supplied by the target TVBox/drpy runtime, but that runtime contract has not yet been verified. Treat it as an external runtime dependency, not a confirmed broken import.
- Build/helper scripts `tools/build_local.py`, `copy_xbpq.py`, `fty.py`, `hebing.py`, `tvbox.py`, and `xiao.py` were inspected. Their Python imports include third-party packages such as `requests`, `demjson3`, and `Crypto`; the repository does not currently provide a dependency lock/requirements file in the inspected tree. This can affect running maintenance scripts in a clean Python environment, but does not prove the playback sources are broken.
- No scripts were changed or deleted in this pass. The full 696-JS/62-Python set still needs systematic call-graph and runtime testing.

## Python script inventory — complete static import pass (2026-11-19)

All 62 repository `.py` files were read and scanned for top-level import statements, obvious network-library use, and relative file references.

- The provider scripts predominantly import `base.spider`; this module is not present in the repository tree and is treated as a host-runtime dependency, not a confirmed missing repository file.
- `xiaosa/py/世界听书.py` additionally references `t4.base.spider`; availability of that runtime module remains unverified.
- Third-party modules observed include `requests`, `Crypto` (PyCryptodome), `bs4` (BeautifulSoup), `pyquery`, `urllib3`, and `cryptography`. Presence in the app/runtime environment was not tested.
- Most provider scripts contain hard-coded remote service endpoints. Static presence of those endpoints does not establish current DNS/HTTP availability, API compatibility, or playable media.
- No missing repository-relative file dependency was confirmed in this Python scan.
- The scan is static; it does not compile or execute the Python sources and cannot establish service availability or runtime compatibility.

## JavaScript sampling update

Additional representative live/provider scripts under `FTY/` and `js/` were inspected. The sampled scripts did not expose obvious Node-style `require()` imports or relative file references. Several use runtime-provided networking APIs (for example `fetch`); compatibility depends on the target TVBox JavaScript engine. This remains a sample, not a full 696-file runtime audit.
