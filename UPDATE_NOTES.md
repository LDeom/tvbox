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
