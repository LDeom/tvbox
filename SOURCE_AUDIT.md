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

