# 更新说明

**日期：** 2026-11-19  
**仓库：** `LDeom/tvbox`  
**更新分支：** `audit/repair-sources-2026-11`  
**基于：** `master`（`641db3307d076547a383841491b17f9280433c5e`）

## 本次已提交的修改

### 1. 修复配置引用

- `0825.json`
  - 将指向不存在的 `./lib/wogg.json`、`./lib/wog.json` 和 `./wogg.json` 的过滤配置引用统一指向仓库内实际存在的 `./json/wogg.json`。
- `js.json`
  - 修复相同的 Wogg 过滤配置路径。
  - 移除启用状态下引用缺失脚本 `./js/西门[V2].js` 的源条目，避免加载不存在的本地脚本。
- `dianshi.json`、`tools/dianshi.json`
  - 将不存在的 `./tv.txt` 直播列表路径改为仓库中存在的 `./list.txt`。

### 2. 配置引用复核

下列配置的本地文件引用均已扫描，未发现缺失目标：

- `0821.json`（36 项）
- `0825.json`（修复后 67 项）
- `0826.json`（1 项）
- `0827.json`（10 项）
- `js.json`（修复后 246 项）
- `jsm.json`（40 项）
- `dianshi.json`（修复后 41 项）
- `tools/dianshi.json`（34 项）
- `9918.json`、`99188.json`（各 21 项）
- `fty.json`（5 项）
- `cat/tjs/open_config.json`（34 项）
- `xiaosa/api.json`（8 项）

补充说明：
- `xiaosa/api.json` 中的 `./spider.jar` 能正确解析到 `xiaosa/spider.jar`，不是缺失文件。
- `XYQ.json` 中指向 `XYQHiker/玩偶妹妹.json` 的引用位于注释掉的源条目中，不属于当前启用的缺失依赖。
- 部分 XBPQ/XYQHiker JSON 文件采用注释或尾随逗号等 JSON5 风格语法。严格 JSON 解析器会报错，但尚未确认客户端实际解析器行为，因此本次没有批量改写。

## 直播与点播列表盘点

已对主要播放列表做静态 URL 统计：

| 文件 | URL 数 | 不同主机数 |
|---|---:|---:|
| `list.m3u` | 860 | 142 |
| `list.txt` | 202 | 18 |
| `tvboxtv.txt` | 1,391 | 110 |
| `tvlive.txt` | 1,420 | 110 |
| `ITV.txt` | 637 | 1 |
| `radio.m3u` | 1,478 | 111 |
| `radio.txt` | 1,478 | 111 |

`tvboxtv.txt` 与 `tvlive.txt` 有 1,387 个 URL 重合；前者另有 4 个独有 URL，后者另有 32 个独有 URL。`radio.m3u` 与 `radio.txt` 包含相同的 1,456 个去重 URL。

这些数据仅代表文件中存在 URL，不代表 DNS、HTTP、鉴权、地域限制或实际媒体播放测试成功。

## 暂不处理的项目

- 仓库包含单独的成人内容播放列表及配置。本次不把它们混入普通电视源，也不生成面向中国大陆的镜像分发地址。
- 仓库 README 对内容合法性、准确性和时效性作出免责声明，并明确提示不要在中国大陆境内使用。国内镜像方案暂缓，待来源授权和分发合规性确认。
- 由于当前执行环境无法可靠完成所有流媒体地址的连通性和播放验证，未把未经实测的源标记为“可用”，也没有按猜测删除源。

## 当前状态

- 所有修改只提交在 `audit/repair-sources-2026-11` 分支。
- 未修改 `master`，未创建 Release。
- 本次为静态配置修复和初步盘点，不等同于全仓库所有源的可播放性认证。

详细审计见 [SOURCE_AUDIT.md](./SOURCE_AUDIT.md)。

## 全仓库 JSON 文件复核补充（2026-11-19）

- 已从 Git tree 盘点并逐个读取检查全部 **257 个 JSON/JSON5 命名文件**。
- 按正确的路径基准检查主配置和子目录依赖；本轮没有确认新的缺失本地文件引用。
- 额外核对了 `cat/js/config_open.json` 的 63 个脚本引用，全部存在。
- `tools/dianshi.json`（34 项）和 `tools/jsm.json`（33 项）使用仓库根目录作为相对路径基准；全部引用均能解析。不能错误地按 `tools/` 子目录拼接。
- `lib/token.json` 的 6 个资源引用均能在 `lib/` 下找到。
- 严格 JSON 解析共发现 43 个文件存在注释、尾逗号或类似 JSON5 语法特征。它们已列入 `SOURCE_AUDIT.md`，但尚未确认客户端/插件的实际解析器，因此没有直接删除或批量重写。
- 这轮是全量 JSON 文件静态盘点，不代表所有站点 URL、API、直播流或点播视频均已完成在线及播放验证。

## 脚本依赖审查补充（2026-11-19）

- 仓库脚本总量：696 个 JS、62 个 Python。
- 首轮抽查了配置入口和代表性脚本，没有发现已确认的仓库内相对 import 缺失。
- `lib/drpy2.min.js` 依赖的 `lib/drpy-core-lite.min.js`、`lib/uri.min.js` 均存在。
- `FTY/drpy2.js` 的 `./uri.min.js` 存在；另有 `assets://` 运行时资源和远程模板/GBK 资源，需在目标播放器环境继续验证。
- 抽查的 Python 采集源使用 `base.spider`。仓库内没有 `base/spider.py`，但它可能由 TVBox/drpy 执行环境提供；暂列为待确认的外部运行时依赖，不能直接认定脚本失效。
- 工具脚本依赖 `requests`、`demjson3`、`Crypto` 等第三方 Python 包；目前未见依赖锁定/requirements 文件，干净环境运行维护脚本可能需要补齐依赖。
- 本轮未删除或改写任何 JS/Python 脚本，避免把运行时提供的模块误判为缺失文件。
- 这只是脚本依赖首轮抽查，尚未完成全部 758 个脚本的逐项调用链与运行验证。

## Python 62 个脚本静态扫描完成（2026-11-19）

- 已逐个读取仓库全部 62 个 Python 文件，扫描顶层 import、网络库调用迹象和相对文件引用。
- 采集脚本普遍依赖 `base.spider`；仓库中没有该模块，暂视为播放器/采集运行时依赖，不能据此判定失效。
- `xiaosa/py/世界听书.py` 还引用 `t4.base.spider`，运行时是否提供尚未验证。
- 发现第三方依赖包括 `requests`、`Crypto`、`bs4`、`pyquery`、`urllib3`、`cryptography`，当前未验证目标环境是否具备。
- 未确认 Python 脚本存在缺失的仓库内相对文件依赖。
- 本轮为静态扫描，没有执行 Python 编译或运行，也没有验证远程接口和媒体播放。
- 另抽查 FTY、js 目录中的代表性 JS 源，未发现明显 Node 风格 require 或缺失相对文件引用；这不代表 696 个 JS 已全部完成运行验证。

## 重复文件盘点（2026-11-19）

按 Git blob SHA 比对，确认字节完全相同的副本：

| 类型 | 文件数 | 唯一内容数 | 重复组 |
|---|---:|---:|---:|
| JS | 696 | 644 | 46 |
| Python | 62 | 46 | 10 |
| JSON | 257 | 206 | 33 |
| M3U | 5 | 5 | 0 |
| TXT | 32 | 29 | 2 |

常见情况是 FTY、js、xiaosa 目录中的同名脚本副本，以及 py/xiaosa/py 中的采集源副本。它们可能分别服务不同配置根路径或客户端版本，不能仅因内容相同就删除。本轮没有删除重复文件。

## 普通直播/广播列表结构检查（2026-11-19）

按 M3U 和逗号分隔 TXT 的真实格式重新统计：

| 文件 | URL 数 | 去重 URL | Host 数 |
|---|---:|---:|---:|
| `ITV.txt` | 636 | 636 | 1 |
| `list.m3u` | 824 | 824 | 136 |
| `list.txt` | 202 | 202 | 18 |
| `tvboxtv.txt` | 1,391 | 1,391 | 110 |
| `tvlive.txt` | 1,420 | 1,419 | 110 |
| `radio.m3u` | 1,478 | 1,456 | 111 |
| `radio.txt` | 1,478 | 1,456 | 111 |

- 修复了 `ITV.txt` 第 560 行的格式错误：`BesTV-16http://...` 改为 `BesTV-16,http://...`。
- `list.m3u` 的 824 条 EXTINF 均有对应 URL 行。
- `tvlive.txt` 有一个 localhost 代理 URL 被两个频道名复用，是否由目标播放器启动代理尚待验证。
- 广播列表各有 22 次重复 URL，可能是别名或重复收录，没有自动删除。
- 以上仅为格式和静态去重结果，不代表地址在线或能够播放；成人列表不纳入国内镜像。
- 本节精确格式统计覆盖并取代此前的粗略 URL 数量。

## 配置中的本机服务依赖排查（2026-11-19）

在 `js.json`、`0825.json`、`dianshi.json`、`xiaosa/api.json`、`9918.json`、`99188.json` 中发现多组 127.0.0.1 回环地址：
- 9978：代理、本地文件、弹幕、壁纸、Cookie、列表文件。
- 10079：JSON 播放解析服务。
- 10172：SOCKS5 代理。
- 10199：Telegram 搜索/媒体服务。

这些不是公网地址，依赖目标设备本机运行相应服务。仓库检索没有定位到对应端口的服务端实现；它们可能由播放器、伴随服务或用户本地服务提供，但尚未证实。若在不具备这些服务的环境使用，对应功能可能失败。本轮只标记运行时前置条件，没有删除或改写这些配置。

## 本机端口分类修正及点播 API 在线抽查（2026-11-19）

之前把所有回环端口笼统归为“本机服务”不够准确，现细分如下：

- **9978**：配置用于本地文件、代理、弹幕等。一个 TVBox 实现的开发文档说明本地 HTTP 服务会在 9978–9998 间尝试端口，并可通过 `getPort()` 获取实际端口。因此配置写死 9978 时，如果端口被占用，可能与动态端口不一致。该行为需在目标播放器确认后才能修改。参考：https://github.com/digfaq/tvbox/blob/main/docs/应用完整开发文档.md
- **10079**：在多个点播源的 `playUrl` 中作为本地 JSON 解析/播放辅助服务，不等同于 9978 文件服务；仓库内未找到服务端实现。
- **10172**：配置为本地 SOCKS5 代理，需要设备上实际有代理监听程序；仓库没有提供。
- **10199**：配置为 Telegram 搜索/媒体 API，本仓库未找到对应服务端实现。

### 点播 API 在线抽查

本轮检查时，下列公开 API 地址返回了结构化的 CatVod 风格列表数据：
- `cj.lziapi.com`
- `cj.ffzyapi.com`
- `bfzyapi.com`
- `suoniapi.com`

以下地址未能通过当前网页检查服务取得响应：`haiwaikan.com`、`api.kuaifan.tv`、`leshiapi.com`。这只表示当前检查工具未取到数据，不能直接判定源站失效。

本次只确认前四个 API 在检查时返回了列表格式数据；没有验证详情接口、播放地址提取、视频流可达性、地区限制或授权状态。因此没有据此删除任何点播源。

## 普通点播接口第二批抽查（2026-11-19）

从 `dianshi.json` 继续抽查普通点播 API（不查询成人类接口）：

**成功返回列表格式 JSON：**
- `api.ukuapi.com` 跳转到 `api.ukuapi88.com`，返回 CatVod 列表。
- `api.apibdzy.com` 返回 CatVod 列表。

**当前网页检查工具无法验证：**
- `caiji.dyttzyapi.com` 返回 403。
- `tyyszy.com`、`wolongzyw.com`、`jszyapi.com`、`zy.jinchancaiji.com`、`vs.okcdn100.top` 未能取得响应。

403 或检查工具无法访问不能直接证明源站失效，可能与 UA、地区线路或上游防护有关。没有删除源。返回列表数据也不等于实际播放验证。


## 中文更新记录：第三批点播接口复核（2026-11-19）

本轮继续从 `dianshi.json`、`0825.json`、`js.json` 提取普通点播接口，并对此前没有明确结论的地址补充检查：

- `ffzy.tv`、`wolongzyw.com`、`api.tyun77.cn`：当前检查服务无法取得响应。
- `zy.jinchancaiji.com`：当前检查服务返回 502。
- `154.219.117.232:9981`：当前检查服务未能完成 IP 直连请求。

**这些结果都不能直接证明源站失效。** 需要在真实播放器所在网络中复测，可能存在 UA、地区线路、反爬、网关或协议差异。没有因本轮网页检查失败而删除任何源。

### 重要说明：源的状态分级

1. **静态正常**：配置语法和本地文件引用正常。
2. **接口响应**：API 能返回列表数据，但尚未验证详情和播放。
3. **播放验证**：需要拿到播放地址并由播放器实际播放成功。
4. **可公开分发**：还必须有明确授权，允许复制/镜像/再分发。

目前部分接口仅达到第 2 级；直播列表和点播源尚未全部完成真实播放测试。不能把“接口能打开”当作“节目都能播放”，也不能把“检查工具打不开”直接当作“源已失效”。

### 本轮处理结果

- 未删除仅因网页检查工具不可访问的源。
- 成人内容配置仍与普通电视/广播源隔离，不生成公开镜像链接。
- 在来源授权和再分发范围未确认前，暂不发布国内 CDN/镜像地址。
- 下一步继续做详情接口、播放链路和普通直播流抽样验证，并把每项结果按上述状态分级记录。

详细技术记录见 [SOURCE_AUDIT.md](./SOURCE_AUDIT.md) 的“中文补充说明：本轮继续核查”章节。


## 中文更新记录：普通直播列表第三轮检查（2026-11-19）

继续检查了六份普通直播/广播列表的协议分布、IP 直连地址及本机代理依赖：

- `tvlive.txt` 发现 33 条 YouTube 频道使用 `127.0.0.1:9978/proxy?do=yt`，必须依赖设备本机代理服务；不具备该服务时这些条目无法按普通公网 URL 播放。
- `tvboxtv.txt`、`tvlive.txt` 各有 394 条 IPv6 字面量地址，目标网络需要具备 IPv6 连通性。
- 部分中国移动 IPv6 地址带有 `online=1720054946` 参数，对应 2024 年时间值，存在动态参数过旧的可能，但含义未证实，因此只标记待验证。
- 多份列表仍大量使用 HTTP，建议在源站确实提供 HTTPS 时优先采用官方 HTTPS 地址，不做猜测式协议替换。

本轮尝试请求代表性 HLS/广播地址，网页检查环境无法取得可用播放清单。因此**没有把任何频道标记为已播放，也没有因检查工具失败而删除频道**。下一步需要在目标设备上测试 IPv4/IPv6 连通性、本机 9978 代理、HLS 清单和分片。

详细记录见 [SOURCE_AUDIT.md](./SOURCE_AUDIT.md) 的“普通直播列表第三轮静态检查”章节。

## 2026-11-19 AVBox 订阅适配

- 新增 `avbox/0825-avbox.json`（普通点播，135 个站点）。
- 新增 `avbox/live.json`（普通直播，5 组列表）。
- 新增 `avbox/99188-avbox.json`（成人点播，64 个站点）。
- 新增 `avbox/adult-live.json`（成人直播，4 组列表）。
- 新增 `avbox/README.md`。
- 仓库内相对资源引用已替换为 `https://gh-proxy.org/https://raw.githubusercontent.com/LDeom/tvbox/audit/repair-sources-2026-11/...`。
- 尚未完成所有第三方 API 与频道流的真实播放测试；订阅可解析不代表每条源均可播放。 

## 2026-11-19 点播空内容排查补充

- 新增 `avbox/vod-verified.json`：最小 type=1 MacCMS API 配置，用于隔离 Spider 依赖。
- README 已说明重新添加该订阅的步骤与验证边界。


## jsDelivr 下载链路与 18+ 文件标识（2026-11-19）

- 用户在手机浏览器确认可访问修复分支中的 `avbox/vod-verified.json` jsDelivr 地址。
- AVBox 文档中的普通配置入口改用 jsDelivr URL 格式；不再把用户已测试失败的 GH-Proxy 作为首选下载入口。
- `avbox/README.md` 已更新，明确普通配置入口与成人配置文件的分类。
- `avbox/99188-avbox.json` 和 `avbox/adult-live.json` 在说明中统一标记为 **18+**，并与普通配置分开。
- 本次只确认了一个配置文件在用户设备浏览器中的下载可达性；尚未逐个验证其他文件、内嵌依赖、API、直播流或实际播放。
- 18+ 仅为内容分级提示，不构成年龄验证或来源授权证明。
- 未批量改写第三方源地址、未删除源、未将未经确认授权的内容制作成公开镜像；所有文档修改仅在 `audit/repair-sources-2026-11` 分支。

## 2026-11-19 — AVBox 全部入口依赖切换到已验证的 jsDelivr 格式

- 普通点播 `avbox/0825-avbox.json`：替换 169 个仓库内依赖链接。
- 18+ 成人点播 `avbox/99188-avbox.json`：替换 37 个仓库内依赖链接。
- 普通直播 `avbox/live.json`：替换 5 个仓库内播放列表链接。
- 18+ 成人直播 `avbox/adult-live.json`：替换 2 个仓库内播放列表链接。
- 只替换指向本仓库当前维护分支的旧代理地址；外部第三方地址和本地代理地址不变。
- 四个文件均通过 JSON 解析检查；复查确认旧 GH-Proxy 和仓库 raw.githubusercontent 地址在这四个 AVBox 文件中均为 0。
- 这项检查仅覆盖配置语法和仓库内依赖 URL 格式，不代表 API 或媒体实际可播放。

## 2026-11-19 — 直播/广播列表静态结构复核

- 复核普通列表：`list.txt` 202 条 URL、`list.m3u` 860 条、`ITV.txt` 637 条、`tvboxtv.txt` 1,391 条、`tvlive.txt` 1,420 条。
- 复核 18+ 列表：`listx.txt` 1,296 条 URL、`livex.m3u` 14,651 条 URL；继续与普通内容分开。
- 广播列表：`radio.m3u` 和 `radio.txt` 各有 1,478 条 URL，去重后均为 1,456 条。
- 已识别 `tvlive.txt` 中 33 条本地 YouTube 代理地址，以及 `yo21.txt` 中 38 条全部依赖本地 9978/10172 代理的地址。没有本地代理服务时，这些条目无法作为普通远程链接播放。
- 部分直播地址使用 IPv6 字面地址，网络不支持 IPv6 的设备可能无法播放。
- 本次仅静态检查，不代表媒体实际可播放；没有仅凭静态结果删除源。

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



## 2026-11-19 — 自动更新工作流推送安全修复

- `.github/workflows/run.yml` 原先使用 `git push -f origin master`，存在强制覆盖 master 历史的风险。
- 已改为 `git push origin "HEAD:${GITHUB_REF_NAME}"`，推送当前触发分支并取消强制推送；发生非快进冲突时会失败而不是覆盖远端历史。
- 未运行工作流，未触发外部源抓取，未构建 APK，未发布 Release，也未修改 master。
- Python 全量静态 import 盘点此前覆盖 62 个文件；`pyquery`、`cryptography` 是否由目标播放器内置仍待设备端验证，没有擅自增加 pip 安装步骤。


## 2026-11-19 — 自动更新工作流进一步隔离审计分支

- 修正此前仅使用 `GITHUB_REF_NAME` 作为推送目标仍可能触及 master 的问题：GitHub schedule 默认在仓库默认分支运行，手动 dispatch 也可能从 master 发起。
- push 触发器现限定为 `audit/repair-sources-2026-11`；三个 job 均跳过 master 上的运行；审计分支触发时只向当前分支进行普通（非 force）推送。
- 未执行工作流、未抓取外部源、未修改 master。需要后续受控验证 Actions runner 的实际执行结果。


## 2026-11-19 — JavaScript 重复内容盘点

- 完整仓库树统计 696 个 JS 文件，按 Git blob SHA 得到 644 个不同内容对象；46 组文件内容字节级相同，涉及 98 个路径。
- 重复副本可能被不同配置按路径引用，因此本轮只登记、不删除、不合并。
- 尚未完成 696 个 JS 文件逐文件语法解析；少量样本检查不能代表全量通过。


## 2026-11-19 — 主配置本地 JS 引用复核

- 静态检查 19 个主要配置文件中的本地 JS 路径，按配置目录规则解析后未发现缺失目标。
- `assets://`、远程 URL、播放器内置标识与本地文件路径分开统计，避免误报。
- 结果只证明仓库内目标文件存在，不代表外部服务可用或实际播放成功；未引用 JS 也不自动视为废弃。


## 2026-11-19 — 外部主机与本地服务依赖盘点

- 19 份主配置中识别到 309 个不同主机名、1,124 次 HTTP(S) URL 字符串出现（HTTPS 845、HTTP 279）。
- 识别到 71 次 localhost/127.0.0.1 服务引用：9978 端口承担壁纸、弹幕、Cookie 和本地扩展文件；10079 端口承担本地解析服务。
- `0821.json` 有 10 次 `gh-proxy.net` 引用，`fty.json` 有 1 次 `ghproxy.net` 引用；均为第三方资源，本轮未验证可达性或授权，未改写。
- 未将静态主机清单当作在线检测结果，不因协议为 HTTP 或暂时不可访问而删除源。


## 2026-11-19 — 凭据暴露风险提示（值已脱敏）

- 在公开配置中发现非占位 B站 Cookie、阿里云盘 Token、夸克 Cookie，涉及 `cat/js/` 与 `cat/tjs/` 的普通配置及 TV 配置。
- `xiaosa/api.json`、`jsm.json`、`dianshi.json` 还包含固定签名样式字段，尚未确认是否属于个人凭据，暂不改动。
- 敏感值未写入本日志。本轮未清空配置字段，以免破坏用户依赖；建议所有者撤销/轮换凭据。修改当前文件无法自动清除 Git 历史或外部缓存。


## 2026-11-19 — 公开配置凭据脱敏

- 经用户确认，四份普通配置中的个人 Cookie / 网盘 Token 已替换为“请填写自己的…”占位值，字段结构与源条目保留。
- 需要个人登录态的功能需由用户自行填写凭据；旧凭据仍可能存在于 Git 历史、fork、下载副本或 CDN 缓存，建议撤销/轮换。


## 2026-11-19 — 点播采集 API 在线响应抽测

- 对普通点播配置中的直接采集 API 和脚本采集 API 做有限在线抽测；5 个接口（量子、暴风、尤酷、光速、红牛）返回 `code=1` 且包含非空影视记录列表。
- 尤酷配置域名发生跳转：`api.ukuapi.com` → `api.ukuapi88.com`，最终响应有非空列表。
- 索尼结果为 HTML 类型；金蝉返回 502；若干其他普通接口以及本轮成人 API 被检测端报告不可访问。这些仅记为未验证/当前检测端不可达，不据此判定永久失效。
- 尚未完成详情查询、搜索查询、播放地址解析及媒体流实播。列表 API 有数据不等于 AVBox/TVBox 中一定能播放；没有删除源，也没有构建 APK 或修改 master。


## 2026-11-19 — 点播搜索/详情请求受检测通道限制

- 对 5 个列表接口已返回数据的点播源，尝试以 `ac=list&wd=关键词` 查询搜索结果、以 `ac=detail&ids=vod_id` 查询详情；当前网页检测通道对带查询参数的 API 请求返回 URL inaccessible / Internal Error，未获得可解析响应。
- 量子列表 API 本轮复测仍返回非空 JSON，`code=1`、`list` 有记录且包含 `vod_id`、`vod_name`、`vod_play_from`；`total=164473` 为服务端自报总数，不代表可播放数。
- 未取得详情中的 `vod_play_url`，也未验证搜索、播放地址和媒体分片。5 个源保持“列表有数据、完整播放链路未验证”，不宣称可播放。
- 没有修改或删除源，没有构建 APK，也没有修改 master。


## 点播 API 在线复测补充（2026-11-19）

- 量子、暴风、索尼三个采集 API 的列表端点当前返回成功标志和非空影视列表。
- 量子列表总数 164473；暴风 173048；索尼 149351。索尼响应头标记为 text/html，但响应体为有效 JSON，需注意客户端兼容性。
- 尤酷为此前曾通过、本轮未重新确认；其他被检测通道拦截的接口不判定为失效。
- 搜索与详情请求仍受检测通道限制，尚未验证 `vod_play_url` 和真实媒体播放，因此这三个接口只标记“列表数据有效”，不标记“完整可播放”。
- 未删除源、未修改 master、未构建 APK。


- 成人点播抽样补测：lbapi9、apilj、maozyapi、apittzy、kkzy 五个 API 的网页检测请求均未取得响应体，全部保持“未验证”，不标记失效。


## 普通点播 API 扩展复测（2026-11-19）

- 新增确认百度采集 API `api.apibdzy.com` 列表端点返回 `code=1`、非空影视列表及分类数据，服务端自报总数 49763；响应头为 text/html、正文为 JSON，需留意播放器兼容性。
- 普通点播累计 4 个 API 列表端点确认有数据：量子、暴风、索尼、百度。该数量按 API 端点去重，不是配置出现次数，也不代表完整可播放。
- 海外看、快帆、乐视、电影天堂、天涯、卧龙、极速、金蝉、小绵阳等当前检测通道未能取得响应正文/返回 502，均列为未验证，不判死。
- 18+ 点播不在本轮范围。未修改源配置、未删除源、未修改 master、未构建 APK。


## 普通点播列表接口复测补充（2026-11-19）

- 百度 API 本轮返回 code=1、非空 list（20 条当前页）、分类数组，服务端 total=49769。上轮 total=49763 为动态数据快照，不累计统计。
- 量子 API 本轮返回 code=1、非空 list，total=164473。
- 搜索和详情请求仍未取得可验证正文；vod_play_url 与真实媒体播放未确认。
- 暴风、索尼沿用此前已确认列表数据的状态，本轮不增加新确认项。
- 本轮仅普通点播；不改配置、不删除源、不改 master、不构建 APK。
