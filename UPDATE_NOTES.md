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
