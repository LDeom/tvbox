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

## Duplicate-content inventory (Git blob SHA comparison, 2026-11-19)

Identical blob hashes were grouped; this identifies byte-for-byte copies, not necessarily obsolete files.

| Extension | Files | Unique contents | Duplicate groups |
|---|---:|---:|---:|
| JS | 696 | 644 | 46 |
| Python | 62 | 46 | 10 |
| JSON | 257 | 206 | 33 |
| M3U | 5 | 5 | 0 |
| TXT | 32 | 29 | 2 |

Examples include the same JS providers mirrored across `FTY/`, `js/`, and `xiaosa/`; identical Python providers across `py/` and `xiaosa/py/`; and identical JSON provider definitions in `json/`, `XBPQ/`, and `xiaosa/`.

These duplicates may be intentional app-profile copies with different relative-path bases or configuration consumers. No duplicate files were deleted. Before deduplication, each consumer's root/path resolution and app-specific compatibility must be confirmed.

## Ordinary playlist structural audit (2026-11-19)

Seven non-adult playlists were re-read and parsed according to their actual formats (M3U URL lines versus comma-separated TXT entries). Counts below are URL entries; duplicate counts are within each file.

| File | URL entries | Unique URLs | Hosts | Structural finding |
|---|---:|---:|---:|---|
| `ITV.txt` | 636 | 636 | 1 | One malformed channel row fixed in this branch |
| `list.m3u` | 824 | 824 | 136 | 824 EXTINF records paired with 824 URL lines |
| `list.txt` | 202 | 202 | 18 | No malformed URL rows found |
| `tvboxtv.txt` | 1,391 | 1,391 | 110 | No duplicate URL rows found |
| `tvlive.txt` | 1,420 | 1,419 | 110 | One URL reused by two channel labels |
| `radio.m3u` | 1,478 | 1,456 | 111 | 22 repeated URL occurrences |
| `radio.txt` | 1,478 | 1,456 | 111 | Same 1,456 unique URLs as radio.m3u |

### Concrete repair

In `ITV.txt`, line 560 contained `BesTV-16http://...` without the required comma separator. It was corrected to `BesTV-16,http://...` so the channel name and URL are parseable by comma-separated playlist readers.

### Items flagged, not deleted

- `tvlive.txt` contains the same localhost proxy URL (`127.0.0.1:9978`) under two different channel names. A loopback URL is only reachable on the device running the proxy; whether the target app starts that proxy is unknown. This is flagged for runtime verification, not removed.
- `radio.m3u` and `radio.txt` each contain 22 repeated URL occurrences. These may be alternate names/entries; no automatic deletion was made.
- Structural checks do not prove a stream is online, authorized, or playable. HTTP/DNS and playback tests remain outstanding. Earlier rough counts for these files are superseded by the exact format-aware counts in this section.
- Adult-oriented lists were excluded from this public playlist audit and are not candidates for domestic mirroring.

## Localhost service dependency review (2026-11-19)

The primary configs `js.json`, `0825.json`, `dianshi.json`, `xiaosa/api.json`, `9918.json`, and `99188.json` contain loopback references. These are not public source URLs and must not be replaced with public mirrors without understanding the app's local service contract.

Observed endpoints include:
- `127.0.0.1:9978`: proxy, local files, danmaku, wallpaper, cookies, and playlist text files.
- `127.0.0.1:10079`: JSON playback parser endpoints.
- `127.0.0.1:10172`: SOCKS5 proxy.
- `127.0.0.1:10199`: Telegram search/media service.

The repository search did not identify a corresponding server implementation for these ports in the checked tree. They may be provided by the target app, an external companion service, or user-installed local services; this is not proven. Consequently, configs depending on these endpoints may fail when used outside that environment. The references are flagged as runtime prerequisites and were not removed or rewritten.

## Clarification: loopback service ports and VOD API spot checks (2026-11-19)

The previous note grouped all loopback ports as generic "local service" dependencies. This is too broad; the configuration evidence supports the following separation:

- **9978** is used for app-local file/proxy/danmaku endpoints. Documentation for a TVBox implementation describes a local HTTP server that tries ports 9978–9998 and exposes the actual port through `getPort()`. Since this repository's configs hard-code 9978, a port collision may cause those references to miss the active server if the target app uses that dynamic-port behavior. The exact behavior of the user's target player must be confirmed before changing these paths. Reference: https://github.com/digfaq/tvbox/blob/main/docs/%E5%BA%94%E7%94%A8%E5%AE%8C%E6%95%B4%E5%BC%80%E5%8F%91%E6%96%87%E6%A1%A3.md
- **10079** is configured as a local JSON parse/playback helper in the `playUrl` field for several VOD providers. It is not the same thing as the standard 9978 file/proxy service. No corresponding helper implementation was found in this repository.
- **10172** is explicitly configured as a local SOCKS5 proxy for selected providers (for example YouTube/TG and a Duboku source). It requires a SOCKS5 listener on the device; this repository does not provide one.
- **10199** is configured as a local Telegram search/media API for TG provider entries. No matching server implementation was found in this repository.

### Online API endpoint spot checks

Direct requests to the configured public VOD category endpoints returned a structured CatVod-style JSON listing during this check:
- `https://cj.lziapi.com/api.php/provide/vod`
- `http://cj.ffzyapi.com/api.php/provide/vod`
- `https://bfzyapi.com/api.php/provide/vod`
- `https://suoniapi.com/api.php/provide/vod`

The following endpoints could not be retrieved by the web inspection service in this run:
- `https://haiwaikan.com/api.php/provide/vod`
- `https://api.kuaifan.tv/api.php/provide/vod`
- `https://leshiapi.com/api.php/provide/vod`

An inspection-service retrieval failure is not proof that a provider is offline. These results establish only that the first four API endpoints responded with listing-shaped data at inspection time; they do not verify detail queries, playback URL extraction, media reachability, region access, or user authorization. No provider was deleted based on this limited check.

## Additional ordinary VOD API spot checks (2026-11-19)

Additional endpoints found in `dianshi.json` were checked without querying adult-oriented sources.

**Returned listing-shaped JSON during this inspection:**
- `https://api.ukuapi.com/api.php/provide/vod/?ac=list` — redirected to `api.ukuapi88.com` and returned a CatVod-style list.
- `https://api.apibdzy.com/api.php/provide/vod?ac=list` — returned a CatVod-style list.

**Could not be verified by the web inspection service:**
- `http://caiji.dyttzyapi.com/api.php/provide/vod` — HTTP 403 at inspection time.
- `http://tyyszy.com/api.php/provide/vod`
- `https://wolongzyw.com/api.php/provide/vod/?ac=list`
- `https://jszyapi.com/api.php/provide/vod/?ac=list`
- `https://zy.jinchancaiji.com/api.php/provide/vod`
- `https://vs.okcdn100.top/api.php/provide/vod`

403 or inspection-service inaccessibility is not enough to label a source dead; app user-agent, geographic routing, or upstream protection may differ. No source was removed. As with the earlier checks, receiving a listing response is not playback validation.


## 中文补充说明：本轮继续核查（2026-11-19）

### 新发现的普通点播接口

从当前分支的 `dianshi.json`、`0825.json` 和 `js.json` 再次提取接口地址，排除成人内容接口后，对此前尚未覆盖的地址进行了补充请求：

| 配置接口 | 本轮检查结果 | 处理结论 |
|---|---|---|
| `http://ffzy.tv/api.php/provide/vod/` | 当前检查服务无法访问 | 待目标播放器/网络环境复测，不判定失效 |
| `https://wolongzyw.com/api.php/provide/vod/?ac=list` | 当前检查服务无法访问 | 待复测，不删除 |
| `https://zy.jinchancaiji.com/api.php/provide/vod/?ac=list` | 检查服务返回 502 | 可能是网关或检查链路问题，待复测 |
| `http://154.219.117.232:9981/jacloudapi.php/provide/vod` | 当前检查服务未能解析/请求 | IP 直连接口待设备端验证 |
| `https://api.tyun77.cn/api.php/provide/par` | 当前检查服务无法访问 | 这是配置中出现的解析类接口路径，不能仅按普通 CatVod 列表接口判断 |

以上状态只描述本轮检查工具的结果，不代表源站必然宕机。HTTP 403、502、DNS/请求失败或网页检查工具不可访问，都可能受 UA、网络出口、地区策略、反爬或网关影响。需要在实际 TVBox 客户端网络中继续复测。

### 如何理解“可用”

- **配置存在**：配置文件及本地引用能找到，只能证明静态结构完整。
- **接口有响应**：服务端返回了列表格式数据，说明接口在检查时可访问；不代表详情、搜索、播放地址都正常。
- **播放链路可用**：还需要成功获取详情和播放地址，并实际请求媒体清单/分片或完成播放器播放测试。
- **分发可用且合规**：还需要确认源站授权、内容版权和允许再分发的范围。技术上能访问不等于有权镜像。

因此，本轮没有因检查服务报错就批量删除点播源，也没有把仅返回列表的接口标记成“已播放验证”。成人内容配置继续隔离，不纳入公开镜像候选。

### 当前后续重点

1. 在真实播放器/设备网络中复测标记为“待验证”的接口，记录 HTTP 状态、响应格式和请求时间。
2. 对确认可返回列表的普通接口，继续检查详情接口和播放地址提取；只记录结构与状态，不公开复制媒体地址。
3. 对普通直播列表分批抽样检查 HLS/M3U 响应和媒体分片；遇到鉴权、Referer、UA 或地域限制时单独标记。
4. 在没有明确再分发授权前，不生成国内镜像/CDN 分发链接。


## 中文补充说明：普通直播列表第三轮静态检查（2026-11-19）

### 直播/广播地址协议与特殊依赖

对普通列表 `list.m3u`、`list.txt`、`tvboxtv.txt`、`tvlive.txt`、`radio.m3u`、`radio.txt` 重新抽取 URL 并统计协议和地址类型。这里统计的是 URL 字符串，不把 M3U 的 `tvg-logo` 等元数据字段误算成节目播放地址；此前按文件格式解析得到的节目 URL 数仍以“普通直播/广播列表结构检查”一节为准。

- `list.m3u`：抽取到 860 个 URL 字符串，其中 HTTP 790、HTTPS 70；含较多 IPv4 直连地址。
- `list.txt`：202 个 URL，HTTP 196、HTTPS 6；含 67 个 IPv4 直连地址。
- `tvboxtv.txt`：1,391 个 URL，HTTP 665、HTTPS 726；含 394 个 IPv6 字面量地址。
- `tvlive.txt`：1,420 个 URL，HTTP 698、HTTPS 722；含 394 个 IPv6 字面量地址，并发现 33 条依赖 `127.0.0.1:9978/proxy?do=yt` 的 YouTube 转发配置。
- `radio.m3u` 与 `radio.txt`：各 1,478 个 URL 字符串，HTTP 1,277、HTTPS 201；两种格式的地址集合此前已确认一致。

### 需要特别标记的项目

1. **YouTube 本地代理依赖**：`tvlive.txt` 有 33 条频道配置走 `127.0.0.1:9978/proxy?do=yt`。这些地址不是公网直播 URL，必须由播放器或伴随服务在设备本机提供代理，并且代理本身还要能解析/转发 YouTube 直播。若设备未启动对应服务，这些频道会失败。不能把它们当成源站失效，也不能简单替换成 YouTube 页面 URL。
2. **IPv6 直连地址**：`tvboxtv.txt` 和 `tvlive.txt` 各含 394 条 IPv6 字面量 URL。仅支持 IPv4 或 IPv6 访问受限的网络可能无法连接；应在目标设备的实际网络环境验证，暂不删除。
3. **疑似旧动态参数**：部分 IPv6 中国移动地址包含 `online=1720054946`，该数值对应 2024 年的 Unix 时间。它可能是服务端会话/签名参数，也可能只是客户端标记；目前没有接口文档或成功播放证据，故标记为“疑似过期/需验证”，不据此认定失效。
4. **HTTP 明文链路**：多份列表仍以 HTTP 为主，存在链路被劫持或内容被篡改的风险。若源站支持 HTTPS，建议优先使用官方 HTTPS 地址；不要自行把 HTTP 改成 HTTPS，避免造成错误地址。

### 在线检查限制

本轮尝试直接请求代表性 HLS/广播地址时，当前网页检查环境均未能取得可解析的播放清单（部分返回内部错误或不可访问）。因此本轮没有确认任何一个节目流“可播放”或“失效”。必须在目标设备/播放器网络中做 HLS 清单、分片和实际解码测试。对于带鉴权、Referer、UA、IPv6 或地区限制的源，需记录对应条件后再判定。

本轮只增加风险标记与中文说明，没有删除直播源，也没有改写节目 URL。

## AVBox 订阅适配（2026-11-19）

- 已核对 LDeom/AVBox 当前 main 分支源码：点播站点由 `sites[].key/type/api` 解析；直播 JSON 由 `lives` 解析；直播文本支持 M3U 与 TXT。
- 新增 `avbox/0825-avbox.json`：基于普通配置，保留 135 个站点；全部 149 处相对路径引用均在仓库中找到并转换为 gh-proxy.com 代理 Raw 绝对地址。
- 新增 `avbox/99188-avbox.json`：成人配置，保留 64 个站点；全部 29 处相对路径引用均在仓库中找到并转换为代理绝对地址。
- 新增 `avbox/live.json`：提供 list.txt、list.m3u、ITV.txt、tvboxtv.txt、tvlive.txt 五个普通直播列表入口。
- 新增 `avbox/adult-live.json`：提供 listx.txt、livex.m3u 及两个外部成人直播列表入口。
- 新增 `avbox/README.md` 说明订阅链接与限制。
- 重要限制：结构检查、仓库路径存在性检查不等于第三方站点 API 或直播流真实播放验证；不能将全部站点标记为已可播放。TVBox Spider/JAR/JS 源仍可能依赖外部站点状态、登录态、网络环境或本地代理。
- 本次新增文件位于 `audit/repair-sources-2026-11`，未改 master、未创建 PR、未发布 Release。

## AVBox 点播无内容问题（2026-11-19 追加）

- AVBox 源码确认：点播 `type=1` 走 MacCMS API JSON 分类解析；`type=3` 需要 Spider/JAR/JS 成功加载。
- 原 `avbox/0825-avbox.json` 首个默认站点为 `豆瓣`（type=3、`searchable=0`），而其余 128 个站点中绝大多数也是 type=3 爬虫；配置解析成功不等于 Spider 可用，可能造成首页无分类/影视。
- 新增 `avbox/vod-verified.json` 最小排障配置，仅保留一个 type=1 API 站点。2026-11-19 对其 `?ac=list` 观察到接口返回 JSON、分类及影视记录；未完成 AVBox 真机详情和播放验证。
- 当前仅把这个接口列为「列表接口有响应」，不宣称已验证播放。需要用户在 AVBox 中重新添加该新地址并反馈首页是否出现分类。

## GH-Proxy 域名调整（2026-11-19）

- GH-Proxy 官网公告显示业务域名已统一为 `gh-proxy.org`，因此 AVBox 配置文件及 README 中原 `gh-proxy.com` 的仓库文件代理链接已更新为 `gh-proxy.org`。
- 当前排障订阅地址请使用 `https://gh-proxy.org/https://raw.githubusercontent.com/LDeom/tvbox/audit/repair-sources-2026-11/avbox/vod-verified.json`。
- 这次更新只调整 GitHub 文件代理域名；尚不能替代用户设备上的实际下载验证。

## Whole-repository inventory and AVBox dependency transport repair (2026-11-19)

A recursive Git tree scan of the working branch completed without truncation. It contains 1,108 tracked files: 262 JSON, 696 JavaScript, 62 Python, 32 TXT, 5 M3U, 8 JAR, 9 GZ, 10 MD5, 10 Markdown, plus image/config files. This is a repository inventory, not proof that every provider is active or usable.

The four AVBox entry configurations were then updated to use the jsDelivr URL format already confirmed reachable on the user's device. Only URLs that pointed to files in `LDeom/tvbox` on branch `audit/repair-sources-2026-11` were rewritten; third-party provider URLs, local proxy endpoints, and other external dependencies were preserved.

- `avbox/0825-avbox.json`: 169 repository-file references changed.
- `avbox/99188-avbox.json` (18+): 37 repository-file references changed.
- `avbox/live.json`: 5 repository-file references changed.
- `avbox/adult-live.json` (18+): 2 repository-file references changed.

All four updated files were parsed successfully as JSON after the rewrite. A follow-up read confirmed zero remaining `gh-proxy.org`, `gh-proxy.com`, or `raw.githubusercontent.com/LDeom/tvbox` references in these four AVBox files. They now contain 213 jsDelivr references in total. This validates JSON syntax and URL rewriting only; it does not prove that every linked dependency, third-party API, or media stream loads or plays on the target device.

The full repository still requires per-entry runtime checks and rights-aware classification. No source was deleted based solely on a static or transient network failure. No master-branch changes, pull request, or Release were made.

## Playlist format and runtime-dependency pass (2026-11-19)

The following playlist files were fetched and inspected for line counts, URL counts, duplicate URLs, and representative line structure. These are static counts, not live HTTP or playback checks:

| File | Non-empty lines | URL occurrences | Unique URL strings | Findings |
|---|---:|---:|---:|---|
| `list.txt` | 205 | 202 | 202 | General TXT playlist structure |
| `list.m3u` | 1,649 | 860 | 851 | M3U playlist; duplicate URLs exist |
| `ITV.txt` | 647 | 637 | 637 | TXT channel list |
| `tvboxtv.txt` | 1,400 | 1,391 | 1,391 | Contains IPv6 literal stream URLs |
| `tvlive.txt` | 1,430 | 1,420 | 1,419 | Includes 33 YouTube entries routed through `127.0.0.1:9978/proxy` |
| `listx.txt` | 1,304 | 1,296 | 1,296 | Separate 18+ playlist; keep classified separately |
| `livex.m3u` | 29,303 | 14,651 | 14,651 | Separate 18+ M3U playlist; keep classified separately |
| `radio.m3u` | 2,957 | 1,478 | 1,456 | Duplicate stream URLs exist |
| `radio.txt` | 1,484 | 1,478 | 1,456 | Same unique stream URL set as `radio.m3u` |
| `yo21.txt` | 38 | 38 | 37 | Every URL depends on `127.0.0.1:9978/proxy` and a SOCKS proxy at `127.0.0.1:10172` |

### Confirmed local-service dependencies

- `tvlive.txt` contains 33 YouTube proxy playlist entries using `127.0.0.1:9978/proxy?do=yt`.
- `yo21.txt` contains 38 URL entries, all routed through the local proxy on port 9978 and configured to use the local SOCKS proxy on port 10172.
- These entries will not work as direct remote URLs unless the target player has the required local proxy and SOCKS services running. Replacing these localhost URLs with a CDN URL would be incorrect; the service itself must be installed/configured or the entries excluded from a profile that does not provide it.

### Additional observations

- The `tvboxtv.txt` and `tvlive.txt` samples include IPv6 literal stream addresses. Devices or networks without IPv6 connectivity may fail to play those entries even though the playlist file downloads successfully.
- The 18+ files `listx.txt` and `livex.m3u` remain separate from ordinary playlists. Their URL reachability and age/access controls were not tested in this static pass.
- Playlist URL counts do not imply that the endpoints are live, authorized, region-accessible, or playable. No stream was removed on the basis of this static pass.

## Script/runtime dependency audit (2026-11-19)

A recursive repository tree contains 696 JavaScript files, 62 Python files, and 8 JAR files. The main configuration families were checked for local script/JAR references, resolving normal relative paths and the repository's root-relative `tools/` configuration convention.

### Results

- `cat/js/config_open.json`: 70 local script/config references checked; no missing repository targets.
- `cat/js/config_open99.json`: 91 references checked; `assets://js/...` references are application asset URIs, not repository-relative paths, and were excluded from missing-file checks.
- `cat/js/config_open99_online.json`: no missing local targets found.
- `cat/tjs/open_config.json`, `18_open_config.json`, `tv_config.json`, `18_tv_config.json`: no missing local targets found.
- `xiaosa/api.json`: its local spider JAR and JSON dependencies exist.
- `jsm.json`, `0821.json`, `dianshi.json`, `9918.json`, `99188.json`: no confirmed missing repository-local script/JAR/JSON dependencies found after parsing compound `$$$` and `;` fields.
- `tools/dianshi.json` and `tools/jsm.json`: their references are root-relative by project convention; corresponding root-level `jar/`, `lib/`, `js/`, `py/`, and playlist files exist. They are not missing merely because the config file itself is under `tools/`.

### One confirmed suspicious reference

- `cat/js/config_open_online.json` references `dyxs_openn.js`, but the repository contains `cat/js/dyxs_open.js` and no `cat/js/dyxs_openn.js`. This appears to be a filename typo. It was not silently rewritten because the online config may intentionally target a separately hosted or generated asset; confirm intended behavior before changing it.

### Local runtime dependencies (not missing repository files)

- `js.json` and `0825.json` contain entries that point to `http://127.0.0.1:9978/file/TV/4khdr.txt` and `.../hdhive.txt`. These are runtime-local files, not repository-relative files. They will only resolve if the relevant local proxy/server exposes those paths and the files are provisioned.
- Existing configs also include local proxy endpoints on ports 9978, 10172, and 10199. These require their corresponding runtime services; CDN rewriting cannot satisfy them.

### Validation boundary

This pass checks reference existence and path conventions, not JavaScript execution, Python imports, JAR compatibility, remote website/API availability, or media playback. JAR files are binary and were not modified. No source entries were deleted on this evidence alone.

## Follow-up script syntax spot-check (2026-11-19)

- Reviewed representative configured JavaScript files: `cat/js/dyxs_open.js`, `cat/js/appysv2.js`, `js/drpy.js`, `js/4khdr.js`, `js/678.js`, and `js/茶杯狐.js`; all passed classic-script syntax compilation in the check environment.
- `lib/drpy2.min.js` uses ES module `import` syntax, so it must be checked with a module-aware parser; a classic-script parser rejection is not evidence of invalid syntax.
- Other library samples such as `FTY/cheerio.min.js` and `FTY/gbk.js` expose ES module `export` syntax and likewise require module-aware validation.
- This was a representative spot-check, not a full syntax pass of all 696 JavaScript files. The full repository-wide compile was not completed due to per-file retrieval/tool-call limits.
- Seven Python plugin files were inspected for headers/import structure. No Python compile or dependency-install test was run; imports such as `requests`, `Crypto`, and the host-provided `base.spider` require runtime-specific availability.

## Corrected online configuration reference

- `cat/js/config_open_online.json` line 68 used `dyxs_openn.js`, while the repository contains `cat/js/dyxs_open.js` and the site key is `dyxs_open`. Updated the API filename to `dyxs_open.js` and verified the target exists in the branch tree.

## Python dependency and automation workflow review (2026-11-19)

- Inspected the repository's `.github/workflows/run.yml` and representative Python plugins/tooling. The workflow installs `demjson3`, `pycryptodome`, and `requests` for its `tools/` jobs; these cover the explicit third-party imports seen in `tools/tvbox.py` and `tools/build_local.py`.
- The Python plugins also import host-provided modules such as `base.spider` and `t4.base.spider`; these are TVBox/runtime APIs, not ordinary pip packages, so their availability must be tested inside the target application/runtime.
- Additional third-party imports found in sampled plugins include `pyquery` (`py/网络直播.py`) and `cryptography` (`py/红果短剧.py`). They are not installed by the repository's automation workflow. This is a potential runtime dependency gap, not yet a confirmed failure: the target app may bundle them.
- Standard-library imports such as `urllib`, `json`, `hashlib`, `concurrent.futures`, and `http.server` do not require pip installation.
- The workflow is configured to trigger on pushes to `master` affecting `tools/**` (as well as manual/scheduled runs). Its final `git-push` job executes `git push -f origin master`. This force-push behavior can overwrite concurrent master history; it is an operational risk worth reviewing. I did not alter the workflow or run it.
- This remains a dependency spot-check of selected Python files, not a full compile/import test of all 62 Python files. No plugin execution or network endpoint health was claimed.



## 自动更新工作流安全性复核与修复（2026-11-19）

- 复核 `.github/workflows/run.yml`：原 `git-push` job 在生成文件后执行 `git push -f origin master`，会对 master 执行强制推送；若远端 master 在工作流 checkout 后出现新提交，强推可能覆盖远端历史。
- 已改为 `git push origin "HEAD:${GITHUB_REF_NAME}"`：推送当前工作流触发分支，不再硬编码 master，也不再使用 force push。普通非快进冲突会安全失败，不会覆盖远端历史。
- 工作流本身未运行；没有触发源抓取、没有生成新源文件，也没有对 master 执行推送。

## Python 静态依赖审计边界补充（2026-11-19）

- 仓库树中共 62 个 Python 文件；此前完整静态 import 扫描记录已列于上文。当前可确认的第三方依赖类别包括 `requests`、`Crypto`（PyCryptodome）、`bs4`、`pyquery`、`urllib3` 和 `cryptography`。
- 工作流工具任务明确安装 `demjson3`、`pycryptodome`、`requests`；插件脚本中的 `pyquery` 和 `cryptography` 是否由目标播放器运行时提供，仍需在目标环境验证，不在此处擅自加入全局依赖安装。
- 本次未执行 62 个脚本的 Python 编译或运行，也未对外部 API 做全量探测；静态 import 结果不能替代运行时兼容性测试。


## 工作流分支隔离补充修复（2026-11-19）

- 进一步复核发现：仅将推送目标改为 `GITHUB_REF_NAME` 仍不足以隔离 master，因为 GitHub 的定时 schedule 事件始终在默认分支运行，`workflow_dispatch` 也可能从 master 手动触发。
- 已将 push 触发分支限定为 `audit/repair-sources-2026-11`，并给 `xiaosa`、`fty`、`git-push` 三个 job 增加 `github.ref_name != 'master'` 条件。
- 因此从 master 触发的 schedule 或手动运行会跳过源抓取和推送；从审计分支触发时才执行，并将提交推回当前分支。推送仍为非强制模式。
- 本次仅修改工作流配置并复核文件内容；未实际运行工作流，未触发外部源抓取。后续仍需在 GitHub Actions 对该分支做一次受控验证，确认 runner 环境和 artifact 步骤正常。


## JavaScript 文件重复内容盘点（2026-11-19）

- 从完整 Git tree（未截断）读取到 696 个 `.js` 文件，对象 blob SHA 分组后有 644 个不同内容对象；发现 46 组字节级完全相同的文件，共涉及 98 个路径。
- 完全相同的内容不等于可删除的冗余：多个目录（例如 `FTY/`、`js/`、`xiaosa/js/`、`lib/`）可能分别由不同配置或运行时按固定路径加载；本轮没有删除或合并任何副本。
- 示例：`FTY/88看球.js`、`js/88看球.js`、`xiaosa/js/88看球.js` 内容相同；`lib/drpy2.min.js` 与 `xiaosa/js/drpy2.min.js` 内容相同。另有部分不同文件名但内容相同，需结合配置引用判断用途。
- 本轮已确认仓库当前仍有 696 个 JS、62 个 Python 文件。受 GitHub connector 单次工具调用预算限制，本轮未完成 696 个 JS 的逐文件语法解析；不得将重复 blob 盘点或少量样本语法检查表述为全量语法通过。
- 配置引用应按各配置格式的字段语义解析，不能用简单的正则匹配推断缺失文件；此前记录的 `cat/js/config_open_online.json` 中 `dyxs_openn.js` 拼写问题已修复为 `dyxs_open.js`。


## 19 个主配置的本地 JS 引用复核（2026-11-19）

- 对 19 个主要配置文件按 JSON 结构递归提取 `api`、`script`、`spider` 等字段，并结合配置所在目录和仓库路径规则解析本地 `.js` 引用。
- 覆盖：`cat/js/` 下四份普通/18+配置、`cat/tjs/` 下四份普通/18+配置，以及 `xiaosa/api.json`、`jsm.json`、`js.json`、`0825.json`、`0821.json`、`dianshi.json`、`tools/dianshi.json`、`tools/jsm.json`、`99188.json`、`9918.json`、`fty.json`。
- 按上述规则解析到的本地 JS 引用均能在仓库文件树中找到；本轮未发现缺失的本地 JS 目标。配置内的 `assets://`、HTTP(S) URL、`csp_*` 等播放器资产 URI、远程或运行时标识不作为仓库本地文件缺失处理。
- 这是一项配置到文件路径的静态存在性检查，不验证远程 API 是否在线、不验证播放器运行时能否加载，也不代表 696 个 JS 文件都被引用。未引用脚本需要结合插件入口、动态加载、外部配置及运行时约定继续判定，不能直接删除。


## 主配置外部主机与本地服务依赖盘点（2026-11-19）

- 对 19 份主要配置提取 URL，识别到 309 个不同主机名，累计 1,124 次 HTTP(S) URL 出现；其中 HTTPS 845 次、HTTP 279 次。出现次数是配置字符串统计，不代表独立服务数或可用率。
- 共识别 71 次指向 `127.0.0.1` 的本地服务 URL，涉及 9 份配置。主要依赖如下：
  - `127.0.0.1:9978/proxy?do=wallpaper`、`...danmaku...`：壁纸/弹幕代理。
  - `127.0.0.1:9978/file/TVBox/bili_cookie.txt`：B站 Cookie 文件。
  - `127.0.0.1:9978/file/TV/4khdr.txt`、`hdhive.txt`、`quark.txt`：本地扩展源文件。
  - `127.0.0.1:10079/parse/...`：本地解析服务，含普通及 proxy 参数模式。
- 这些地址是客户端本机服务依赖，不是公共服务器地址；如果 AVBox/盒子运行环境没有启动对应端口和文件，相关功能会失败。不能将其替换成仓库 CDN，因为服务行为和用户私有 Cookie/文件不同。
- 另发现 `0821.json` 中有 10 次 `gh-proxy.net` 外部 GitHub 资源引用，`fty.json` 有 1 次 `ghproxy.net` 外部播放列表引用。它们不指向本仓库，且本轮未对其目标内容、授权及国内网络连通性作实测；不自动改写或宣称可用。
- 本轮不对 309 个外部主机做批量删除或替换。域名出现次数、HTTP/HTTPS 协议及静态字符串都不能证明源失效；需要逐接口检测响应结构、地区可达性和播放器兼容性后再作结论。


## 凭据字段暴露风险审计（2026-11-19，敏感值已脱敏）

- 在公开配置中发现疑似真实会话凭据：
  - `cat/js/config_open.json` 与 `cat/js/config_open_online.json`：哔哩、哔哩直播两个条目含非占位 Cookie。
  - `cat/tjs/open_config.json` 与 `cat/tjs/tv_config.json`：gitcafe、changzhang、aliyunpanshare、alipansou、pan_search、wogg 条目含非占位 `aliToken` / `quarkCookie`；bilibili 条目含非占位 Cookie。
- `xiaosa/api.json`、`jsm.json`、`dianshi.json` 中另有固定 `sign` / `buildSignature` 字段。本轮仅标记为凭据样式值，尚未确认是否为个人秘密、公共接口签名或静态协议常量，不擅自删除。
- 配置中的敏感值没有复制进审计报告或更新日志。上述值已进入公开仓库历史，单纯改当前文件不能清除 Git 历史；建议凭据所有者撤销/轮换旧会话与 Token，并评估清理公开 Git 历史及 CDN 缓存。
- 本轮尚未改写这些配置字段，避免未经确认就清空用户 Cookie/Token 导致源功能失效。待确认后可将公开配置改为用户自行填写的占位值；不能替用户撤销第三方账号会话。


## 凭据脱敏修复（2026-11-19）

- 经确认，将 `cat/js/config_open.json`、`cat/js/config_open_online.json` 中哔哩及哔哩直播的 4 处 Cookie 替换为用户自行填写占位值。
- 将 `cat/tjs/open_config.json`、`cat/tjs/tv_config.json` 中 12 处阿里云盘 Token、12 处夸克 Cookie、2 处 B站 Cookie 替换为用户自行填写占位值（两份配置内容存在重复）。
- 保留字段结构和源条目，不删除源；相关需要个人登录态的功能须由用户重新填写自己的凭据后使用。
- 重新读取四份文件并解析 JSON；检查上述目标字段均无残留的非占位长凭据。
- 此修改只影响当前分支最新文件，不会自动清除 Git 历史、fork、已下载副本或 CDN 缓存中的旧值。建议凭据所有者撤销/轮换旧会话与 Token，并另行评估历史清理。


## 点播采集 API 在线响应抽测（2026-11-19）

- 本轮从普通点播配置（含 `0825.json`、`0821.json`、`jsm.json`、`dianshi.json`、`cat/js/config_open*.json`）与成人点播配置（`99188.json`、`9918.json`）抽取直接采集 API 和 `caiji.js` 外部接口进行在线响应检查。
- 截至本轮，以下 5 个普通点播 API 在检查端返回了可解析的非空 MacCMS 风格 JSON 列表，且 `code=1`、`list` 非空，并包含影视名称、分类、更新时间或播放源字段：
  - 量子：`https://cj.lziapi.com/api.php/provide/vod/?ac=list`，响应声明总记录 164,440。
  - 暴风：`https://bfzyapi.com/api.php/provide/vod/?ac=list`，响应声明总记录 173,045。
  - 尤酷：配置域名 `api.ukuapi.com` 跳转至 `api.ukuapi88.com`；最终响应声明总记录 60,844，列表非空。
  - 光速：`https://api.guangsuapi.com/api.php/provide/vod/from/gsm3u8`，响应声明总记录 118,691。
  - 红牛：`https://www.hongniuzy2.com/api.php/provide/vod/from/hnm3u8/`，响应声明总记录 117,937。
- 另有部分接口在本轮检查端返回无法访问、抓取错误或非 JSON 页面；例如索尼接口返回 HTML 类型结果，金蝉接口返回 502。此类结果只说明当前检测端未取得有效 JSON，不能直接判定源永久失效，可能涉及反爬、地区限制、TLS、CDN 或检测端限制。
- 成人点播配置中的直接 API 本轮均未能通过当前检查端取得可解析的非空数据响应；多数请求被检测端报告为 URL 不可访问。该结果标记为“未验证/检测端不可达”，不标记为失效，也未删除或修改任何成人源。
- 重要边界：本轮验证的是采集接口的列表响应，不是播放器端完整搜索、详情、播放地址解析和媒体流播放。对量子、暴风、尤酷、光速、红牛的详情查询 URL，本检测端无法抓取，因此尚不能宣称这些源已经可播放；后续需在 AVBox/TVBox 兼容环境中验证搜索、详情、播放地址和实际媒体请求。
- 接口返回的 `total` 是服务端自报记录数，不是仓库内独立可用影视数；未据此计算可用源总数。没有因单次网络错误而删除任何源。


## 点播搜索与详情接口复核（2026-11-19，检测端受限）

- 对上一轮确认有非空列表的量子、暴风、尤酷、光速、红牛接口，继续尝试使用 MacCMS 常见查询参数 `ac=list&wd=<关键词>` 和 `ac=detail&ids=<vod_id>` 验证搜索及详情。
- 当前可用的网页检测通道拒绝访问这些带查询参数的请求，返回 URL inaccessible / Internal Error；因此本轮没有拿到搜索结果或详情 JSON。不能据此判定 API 不支持搜索/详情，也不能把这五个源升级为“完整点播可用”。
- 量子列表接口本轮再次成功返回 JSON：`code=1`、`list` 非空，包含 `vod_id`、`vod_name`、`vod_play_from` 等字段，响应声明 `total=164473`。这仅确认列表接口仍有数据；本轮拿到的列表字段未包含 `vod_play_url`，播放地址必须通过详情接口获取。
- 本轮未能验证搜索命中、详情 `vod_play_url`、播放源URL响应或媒体分片，因此完整链路状态仍为“未验证”。下一步需使用可直接发起任意 HTTP GET 的受控客户端，或在 AVBox/TVBox 运行环境中执行相同查询；对播放地址只做安全的响应头/首段检查，不下载整部媒体。
- 本轮未修改源配置、未删除任何源、未构建 APK、未触及 master。


## 点播 API 有效影视数据复测（2026-11-19）

本轮使用可读取公开 HTTP 响应的检测通道，对配置中直接提供采集数据的 API 进行复测。判定标准为响应体中存在可解析的采集 JSON、成功标志（如 `code=1`）、非空 `list`，且记录包含影视名称/ID/播放来源等字段；仅 HTTP 成功或站点可打开不算有效。

### 本轮确认返回非空影视列表

| API | 当前响应 | 数据情况 | 结论 |
|---|---|---|---|
| 量子 `cj.lziapi.com` | JSON | `code=1`，`total=164473`，列表非空；记录含 `vod_id`、`vod_name`、`vod_play_from` | 列表接口有效 |
| 暴风 `bfzyapi.com` | JSON | `code=1`，`total=173048`，列表非空；记录含影视名称、ID和播放来源 | 列表接口有效 |
| 索尼 `suoniapi.com` | 响应头标为 text/html，但响应体实际为 JSON | `code=1`，`total=149351`，列表非空 | 内容有效；响应 Content-Type 不规范，播放器兼容性需验证 |

证据 URL：
- `https://cj.lziapi.com/api.php/provide/vod/?ac=list`
- `https://bfzyapi.com/api.php/provide/vod/?ac=list`
- `https://suoniapi.com/api.php/provide/vod/?ac=list`

### 其他观察与限制

- 尤酷 API 曾在此前检测中通过旧域名跳转至 `api.ukuapi88.com` 并返回数据；本轮重定向目标响应未呈现可解析 JSON，故记为“历史通过、本轮未复核通过”，不直接判死。
- 155、jkun、森林、滴滴等成人配置中的采集 API，本轮检测通道返回不可访问/内部错误；这属于检测通道无法取数，不作为源失效证据。
- 对量子详情（`ac=detail&ids=...`）及关键词搜索（`wd=...`）的请求被检测通道拦截，尚未拿到详情 JSON、`vod_play_url` 或播放地址。当前仅能确认列表接口，不可标记为完整可播放。
- 列表数据里的 `vod_play_from` 只是播放线路标识，不是实际媒体地址。尚未验证播放地址、解析器及本地 `127.0.0.1:10079` 服务。
- 同一 API 在多份配置中重复出现，统计可用源时应按 API URL 去重，不能把配置条目数当成独立源数。

本轮没有删除或改写源条目，没有更改 master，没有构建 APK。检测结果属于 2026-11-19 的时间点快照，源状态可能变化。


### 18+ 点播 API 抽样补测

对成人配置中的 `lbapi9.com`、`apilj.com`、`api.maozyapi.com`、`apittzy.com`、`kkzy.me` 列表端点尝试读取公开响应，检测通道均返回不可访问/内部错误，未取得响应体。此结果仅代表本检测通道无法读取，不能据此判定 API 失效或无影视数据；需用真实客户端/可执行 HTTP 请求环境复测。


## 普通点播 API 扩展复测（2026-11-19）

本轮按普通点播配置中的唯一 API 端点继续抽测，不包含任何 18+ 配置。新增确认：

| API | 响应内容 | 结论 |
|---|---|---|
| 百度 `api.apibdzy.com` | JSON，`code=1`，`total=49763`，`list` 非空；记录含 `vod_id`、`vod_name`、`vod_time`、`vod_play_from`，并返回分类列表 | 列表接口有效 |

证据：`https://api.apibdzy.com/api.php/provide/vod/?ac=list`。本次响应头为 `text/html`，但正文为合法 JSON；应进一步确认目标播放器是否按正文解析而非依赖 Content-Type。

此前检测已确认量子、暴风、索尼列表接口返回非空影视数据。本轮其余普通候选（海外看、快帆、乐视、电影天堂、天涯、卧龙、极速、金蝉、小绵阳等）在当前检测通道中无法取得响应正文或返回 502，均保持“未验证/检测通道不可达”，不判定失效。

### 搜索/详情链路状态

目前新增百度也只确认列表接口。尚未取得搜索响应和详情中的 `vod_play_url`，故普通点播当前累计至少 4 个 API 的列表端点已确认有数据（量子、暴风、索尼、百度）；完整搜索、详情、媒体播放仍未验证。尤酷为历史曾通过但本轮未复核，不计入本轮当前确认数。

本轮只处理普通点播；没有更改源配置、没有删除源、没有修改 master、没有构建 APK。


## 普通点播搜索/详情链路继续检测（2026-11-19）

- 百度列表 API 复测仍返回有效非空 JSON：`code=1`、`total=49769`、20 条当前页记录及分类数组。记录包含 `vod_id`、`vod_name`、`vod_play_from`。这是动态总数快照，不应与上一轮 49763 相加。
- 量子列表 API 仍返回有效非空 JSON：`code=1`、`total=164473`，记录含影视 ID、名称和播放线路标识。
- 暴风与索尼的列表 URL 当前可打开，但本轮工具未能提取可审阅的正文，因此沿用此前通过结果，不新增计数。
- 本轮未能取得搜索/详情查询的有效正文。不得将 `vod_play_from` 当成播放 URL；详情中的 `vod_play_url` 与媒体流仍待验证。
- 百度和量子列表响应可证明采集 API 在当前时间点提供影视目录数据，但不能证明播放器完整链路或所有条目都可播放。
- 本轮只检查普通点播；未更改配置、未删除源、未修改 master、未构建 APK。


## 普通点播 API 复测补充：尤酷重新确认（2026-11-19）

- 尤酷配置 API `https://api.ukuapi.com/api.php/provide/vod/?ac=list` 重定向至 `https://api.ukuapi88.com/api.php/provide/vod/?ac=list`，本轮重新取得合法 JSON：`code=1`、`total=60854`、`list` 非空，记录含 `vod_id`、`vod_name`、`type_name`、`vod_play_from`。
- 本轮返回的列表样本中 `vod_play_url` 为空；列表接口只证明目录数据可取，不能证明详情/播放。
- 索尼 `https://suoniapi.com/api.php/provide/vod/?ac=list` 本轮再次取得合法 JSON：`code=1`、`total=149351`、非空列表。响应头为 text/html，但正文可解析为 JSON，播放器对 Content-Type 的兼容性仍需验证。
- 对尤酷详情 `ac=detail&ids=75947`、索尼详情 `ac=detail&ids=155832` 及尤酷关键词搜索请求，当前网页检测通道均拒绝带查询参数 URL，未取得响应正文。此为检测通道限制，不可判定接口失效或不支持查询。
- 当前已确认返回非空列表的普通点播 API 去重计数仍为 5 个：量子、暴风、索尼、百度、尤酷（尤酷为本轮恢复确认）。详情、播放地址与媒体流仍未验证。
- 本轮未修改配置、未删除源、未修改 master、未构建 APK。


## 普通点播详情链路自动化检测工具（2026-11-19）

- 新增只读脚本 `audit/vod_api_audit.py`，仅检测量子、暴风、索尼、百度、尤酷五个普通点播 API，不读取或请求 18+ 源。
- 脚本按顺序请求列表、关键词搜索（`流浪地球`）、从实时列表选取最多 5 个真实 `vod_id` 请求详情；如详情返回 `vod_play_url`，仅提取首条媒体地址并发送 Range 0-0 请求检查响应，不下载完整媒体。
- 新增 GitHub Actions 工作流 `.github/workflows/vod-api-audit.yml`，支持手动触发，运行后上传 `ordinary-vod-api-audit` JSON 报告（保留 14 天）。工作流权限仅 `contents: read`，不会写回仓库或修改源配置。
- 本环境没有外部 DNS/HTTP 访问能力，GitHub 连接器也没有 workflow_dispatch 写操作；工作流文件已提交，但本轮尚未实际运行，故尚无搜索/详情/媒体结果。需在 GitHub Actions 页面手动运行后读取报告，不能把“已创建检测工作流”表述成“已通过检测”。
- 脚本和工作流仅位于 `audit/repair-sources-2026-11` 分支；未构建 APK、未改 master、未删除或改写源配置。


## 普通点播 API 自动化链路抽测结果（2026-11-19，Actions run #1）

GitHub Actions run `44536222364` 已完成，job 和报告上传均为 success。JSON artifact：`ordinary-vod-api-audit`。本次仅检查普通点播五个 API，不改动源配置。

| 源 | 列表 | 搜索“流浪地球” | 详情 `vod_play_url` | 首条媒体 URL Range 探测 |
|---|---|---|---|---|
| 量子 | HTTP 200，20 条 | 命中 20 条 | 有，ID 167147 | HTTP 404，目标媒体地址未找到 |
| 暴风 | HTTP 200，20 条 | 命中 20 条 | 有，ID 169055 | HTTP 206，返回 `application/vnd.apple.mpegurl`，本次探测通过 |
| 索尼 | HTTP 200，20 条 | JSON 解析异常 | 有，ID 157785 | HTTP 403，可能有防盗链/访问限制，不能判死 |
| 百度 | HTTP 200，20 条 | 命中 2 条 | 有，ID 50164 | HTTP 403，可能有防盗链/访问限制，不能判死 |
| 尤酷 | HTTP 200，20 条 | 命中 5 条 | 有，ID 75948 | HTTP 403，可能有防盗链/访问限制，不能判死 |

### 结果解释与限制

- 五个 API 的列表、详情均取得非空数据；四个搜索请求返回命中，索尼搜索请求在解析响应时失败。索尼详情成功说明不能把单次搜索解析异常扩大为整个 API 失效。
- 五个详情响应均含非空 `vod_play_url`。但脚本只抽取每个详情的第一条播放地址进行轻量 Range 请求，不等于完整播放或全部线路验证。
- 暴风返回 HTTP 206，且 Content-Type 为 HLS 播放列表类型，是本轮最强的媒体可达证据；仍未在 TVBox/AVBox 播放器内实播。
- 量子首条媒体地址返回 404，应继续检查该条线路/剧目或重新抽样其他详情，不据单条地址删除量子 API。
- 索尼、百度、尤酷返回 403，可能与 Referer、Cookie、UA、IP/地区策略或防盗链有关；当前结果是“受限/未确认”，不是“源失效”。
- 列表的 `total` 是服务端目录总数，不是有效影视数或可播放数。
- 本次 GitHub Actions job success 代表检测程序成功执行并上传报告，不代表所有源播放成功。
- 此次工作流为 push 事件触发；后续工作流也支持手动 `workflow_dispatch`。未修改 master、未删除源、未构建 APK、未发布 Release。


### 自动检测脚本分类修订后的复跑（Actions run #2）

- run `44536747205` 已完成，conclusion 为 success，报告 artifact 已上传并读取。
- 五个源的列表、详情与搜索结果分类和首轮一致：量子/暴风/百度/尤酷搜索命中，索尼搜索仍解析失败；五个详情均有播放地址。
- 媒体探测状态现按 HTTP 码细分：量子 `not_found`（404）、暴风 `partial_content`（206）、索尼/百度/尤酷 `forbidden_or_hotlink_protected`（403）。这次复跑确认了新分类逻辑正常产出；没有把 403 归为源失效。
- 工作流 run success 只证明自动检测和报告上传完成。播放器内实播仍未验证。


## 第三轮点播多详情/播放线路抽测（Actions run #3）

- run `44537173678` 成功完成，报告 artifact 已生成。
- 五个 API 各抽取 5 个详情，详情接口均成功返回且 `vod_play_url` 非空（每个源 5/5）。
- 量子：5 个详情均有播放地址；多线路媒体探测出现 HTTP 200/206 与 HTTP 404 混合，说明同一源内存在可响应线路和失效抽样地址，不能按源整体判死。
- 暴风：本轮抽取的 5 个详情均有播放地址，但抽样媒体 URL 均返回 HTTP 404；与早先单次 206 结果不同，说明线路/样本动态变化，需扩大样本并在客户端实播。
- 索尼、百度、尤酷：本轮抽取的详情均有播放地址，媒体 URL 多次返回 403；使用 API 根域作为 Referer 重试仍为 403。当前只能标记“媒体访问受限/未确认”，不能判 API 失效。
- 此轮验证覆盖 25 个详情记录；媒体 URL 轻量 Range 探测并非完整下载或播放器实播。

## 仓库其他源文件扫描任务

- 已枚举修复分支当前树中的 299 个 JSON/TXT/M3U/M3U8 文件（静态文件清单统计）。
- 新增 `audit/repository_source_audit.py`，对非成人配置文件进行 JSON 结构/文本可读性检查，提取网址并抽样 HTTP Range 探测；上限 400 个文件、每文件 3 个 URL、全局最多 250 次请求。
- 跳过成人路径及代码库/打包产物目录（如 `cat/js`、`cat/dist`）；本任务只读，不修改源文件。
- 扫描工作流已启动，结果待报告 artifact 完成后再记录。HTTP 403、404、超时均按单条网址结果记录，不直接删除源。


## 第四轮：仓库配置/播放列表文件抽查（Actions run #44539613860）

- 仅扫描非成人配置；排除成人配置路径/文件名，并排除疑似成人直播列表 \`livex.m3u\`。本轮纳入 287 个 JSON/TXT/M3U/M3U8 文件。
- 结构检查：208 个严格 JSON 有效，42 个 JSON5/JSONC 风格文件可解析，1 个文件确认为 JSON5 配置体后附带 HTML，1 个文件无法按文本编码读取。
- 唯一确认的格式异常：\`json/dj看球.json\` 的 JSON5 配置体在第 70 行闭合，HTML 从第 72 行开始追加，导致整个文件不能作为完整 JSON/JSON5 解析。暂不删除/截断，需先确认它是否仍被其他配置引用。
- \`jar/fan.txt\` 无法按 UTF-8、GB18030、GBK 或 UTF-16 解码，暂按二进制/未知编码附件处理，不判为源失效。
- \`live/辽宁联通.txt\` 可按 UTF-16 解码；此前单一 GB18030 检查造成的误报已消除。
- 播放列表静态网址数量：\`ITV.txt\` 637；\`list.m3u\` 851；\`listx.m3u\` 25,814；\`radio.m3u\` 1,456；\`live/山东联通.txt\` 177；\`live/广东联通内网.txt\` 190；\`live/河南联通单播.txt\` 105；\`live/辽宁移动华为.txt\` 390；\`live/辽宁移动烽火.txt\` 390；\`live/辽宁联通.txt\` 150。以上是提取到的 URL 数，不等于去重后的频道数或实播数。
- 河南/辽宁联通列表含 RTSP 私网地址（如 10.253.76.35、10.15.250.13），属于运营商/局域网资源，不能从 GitHub runner 公网环境判定失效。
- 本轮抽样 120 个 URL：43 个 HTTP 200/206，7 个 403，17 个 404，43 个请求异常，5 个本地/私网端点被主动跳过。请求异常、403/404 均只代表抽样 URL 的响应，不代表整份列表不可用。
- 脚本已增加 JSON5 解析、UTF-16 文本读取、RTSP/RTMP/RTP/UDP 识别、私网地址跳过和成人列表排除。

## 第五轮：JavaScript 采集规则静态检查（Actions run #44539178933）

- 检查非成人 \`js/\`、\`FTY/\`、\`cat/js/\`、\`cat/tjs/js/\`、\`xiaosa/js/\` 目录中的 569 个 JS 源文件。
- 569/569 通过 Node.js 语法检查；5 个原先看似语法错误的文件实际是 Base64 或 gzip+Base64 封装，解码后语法均正常。
- 抽样 100 个脚本中的字面 URL：45 个 HTTP 200/206，3 个 403，5 个 404，6 个其他 HTTP 状态，41 个请求异常。该项是静态字面 URL 抽样，不执行 TVBox 专用运行时，也不等于采集源搜索/详情/播放全部可用。
- 未修改采集规则代码；成人脚本名/路径排除。

## 第六轮：Python 规则与 JAR 完整性（Actions run #44539853105）

- 非成人 Python 文件 65 个，全部通过 Python 语法编译检查（65/65）。
- \`jar/\` 下 7 个 JAR 全部通过 ZIP 完整性测试（7/7）。
- 配置中发现 39 处本地 JAR MD5 引用：37 处与仓库 JAR 实际 MD5 一致；另 2 处不一致都位于 \`tools/dianshi.json\`、\`tools/jsm.json\` 这两个构建模板，均引用旧的 \`spider.jar\` MD5。仓库当前 \`jar/spider.jar\` 的 MD5 为 \`decb609b673019e18512dc3a96b6a252\`；\`tools/build_local.py\` 会在生成配置时重新计算并写入下载后 JAR 的 MD5，因此这两处先记为模板旧值，不判运行配置故障。
- Python 源码中抽样 50 个字面 URL：31 个 HTTP 200/206，4 个 403，6 个 404，8 个请求异常，1 个其他 HTTP 状态；仅为端点抽样。
- 没有修改 JAR、Python 源或配置中的 MD5。

## 当前综合判断

- 静态配置文件、JS 语法、Python 语法、JAR 压缩包和 MD5 引用已分层检查。
- \`json/dj看球.json\` 是当前唯一确认的 JSON/JSON5 格式异常；\`jar/fan.txt\` 是未知编码/二进制文件，待确认用途。
- 直播播放列表包含大量运营商私网 RTSP URL，必须在对应网络/设备上实播；公网 HTTP 探测不能替代运营商网络验证。
- 仍未执行 AVBox/TVBox 客户端内的逐源搜索、详情、解析和实播回归；因此未把任何源标记为“实播完全通过”。
- 本轮没有删除源、没有修改原采集规则/播放列表、没有触碰 master、没有构建 APK、没有发布 Release。


## 第七轮：其他 MacCMS 点播 API 端点抽测（Actions run #44541153691）

- 从非成人配置和 JS 规则中额外发现并抽测 25 个 MacCMS 风格 API，排除了此前已测的五个 API，以及带成人指示的域名。
- 10/25 个 API 的列表接口返回非空影视记录；6/25 搜索“流浪地球”命中；10/25 详情接口返回非空播放地址。
- 直接媒体地址抽测：3 个返回 HTTP 206（\`fhapi9.com\`、\`madouse.la\`、\`lbapi9.com\`）；6 个返回 403（包括 \`caiji.dyttzyapi.com\`、\`cj.ffzyapi.com\`、\`ffzy.tv\` 的抽样播放地址）；另有 2 个详情返回爱奇艺/优酷网页链接而非直接媒体流。
- 其余端点包含 DNS 失败、连接/读取超时、SSL 证书错误或 API 返回非 JSON。均标记为“未确认/访问异常”，不据此删除源。
- 搜索未命中不等于 API 不可用；详情有播放地址也不代表媒体一定能播放。需要客户端解析器/播放器实播确认。

## 配置修复：\`json/dj看球.json\`

- 已确认原文件 JSON5 配置对象在第 70 行结束，第 72 行开始误追加了整段 HTML 页面，导致配置整体无法解析。
- 已在审计分支删除 JSON 对象之后的 HTML 尾部，保留原有配置字段和注释；等待仓库扫描工作流重新验证。
- 未删除文件，也未更改其中的源站地址或规则字段。


## 第八轮：格式修复后的回归验证（Actions run #44541512779）

- \`json/dj看球.json\` 尾随 HTML 已移除，回归扫描确认可按 JSON5 解析；文件内原配置字段与注释保留。
- 287 个非成人配置/播放列表文件的最终解析统计：208 个严格 JSON、43 个 JSON5/JSONC、0 个 JSON/JSON5 解析失败；另有 35 个文本列表可读。
- 唯一无法按文本读取的文件仍为 \`jar/fan.txt\`，编码/内容可能是二进制或专用格式，未改动。
- 最终抽样 120 个去重 URL：42 个 HTTP 200/206、10 个 403、17 个 404、5 个其他 HTTP 状态、42 个请求异常、4 个本地/私网地址跳过。均是单条 URL 的结果，不是源文件级失效结论。
- 扫描改为并发并对 URL 去重；成人配置与 \`livex.m3u\` 仍排除。

## 其他 API 扩展抽测最终结论（Actions run #44541153691）

- 额外发现并测试 25 个非成人 MacCMS 风格 API：10 个列表非空、6 个搜索命中、10 个详情含播放地址。
- 直接媒体 URL 抽样：3 个 HTTP 206；6 个 403；2 个为爱奇艺/优酷网页链接，不是直链媒体。403、超时、DNS/SSL 异常都保留为未确认状态。
- 本轮强证据的媒体地址可达样本来自 \`fhapi9.com\`、\`madouse.la\`、\`lbapi9.com\`；其他返回播放地址但媒体请求失败/受限的 API 仍需客户端验证。
- 带成人指示的域名已加入排除规则，后续扩展扫描不再测试。


## 第九轮：主配置本地引用关系核对（2026-11-19）

- 对主配置 `0821.json`、`0825.json`、`0826.json`、`0827.json`、`367.json`、`9918.json`、`99188.json`、`XYQ.json` 提取相对路径文件引用，并与当前分支 Git tree 文件清单逐项比对。
- 引用计数（按配置内出现的不同路径）：`0821.json` 36、`0825.json` 66、`0826.json` 1、`0827.json` 10、`367.json` 0、`9918.json` 19、`99188.json` 19、`XYQ.json` 34。
- `0821.json`、`0825.json`、`0826.json`、`0827.json`、`9918.json`、`99188.json` 提取到的本地引用均在仓库中存在；`367.json` 未提取到本地相对路径引用。
- `XYQ.json` 的 `./XYQHiker/玩偶妹妹.json` 是唯一未在仓库找到的路径，但对应整条站点配置在文件中以注释形式禁用（`//{...}`），不是当前启用的源引用；已存在的启用项 `./XYQHiker/玩偶哥哥.json` 可在仓库找到。因此本轮未发现上述主配置中启用的本地文件引用缺失。
- `0821.json` 引用 `./jar/fan.txt`，该文件仍是上一轮标记的未知编码/接口无法读取内容项；路径存在，但文件格式/用途尚未确认，不能把“存在”解释为 JAR 可加载或功能可用。
- 本轮仅做路径存在性核对，不代表对应 JS/JAR 运行成功、API 可访问或播放器实播通过；未改动任何源配置或删除文件。


### 第九轮补充：不带 ./ 前缀的扩展文件依赖

- 复核发现部分源将本地依赖写在对象字段 ext.Cloud-drive 中，路径为 tvfan/Cloud-drive.txt，不带 ./，因此不在上一节基于 ./ 相对路径的提取计数内。
- 0821.json 中该路径出现 11 次，0826.json 中出现 11 次；当前分支 Git tree 中不存在 tvfan/Cloud-drive.txt，仓库内也没有其他大小写/目录变体。对应上游公开配置同样引用此路径，但其对应提交的文件树中也未发现该文件。
- 这 22 处是启用站点配置中的扩展依赖引用，不能简单归为无效源：它可能由 TVBox/影视仓运行环境或外部数据目录提供，也可能是仓库缺少的配套文件。当前没有证据确认该文件的格式、内容或加载机制，因此记录为“未解析的运行时依赖”，不擅自创建空文件、不删除引用、不判源失效。
- 修正上一节结论的适用范围：以 ./ 或 ../ 明确标记的本地文件引用核对结果仍成立；但不能据此宣称所有运行时扩展依赖均已闭合。后续需结合对应播放器对 Cloud-drive 字段的读取方式及实际运行环境继续确认。
