# AVBox 订阅配置

本目录提供 AVBox 配置结构示例及订阅入口。仓库文件的 CDN 访问测试以 jsDelivr 为准；用户设备已确认能够打开下方的 jsDelivr 测试文件。该结果只证明配置文件下载链路可达，不代表其中第三方站点或媒体流可播放，也不代表拥有内容再分发授权。

## 普通配置入口（jsDelivr）

- 普通点播配置：[0825-avbox.json](https://cdn.jsdelivr.net/gh/LDeom/tvbox@audit/repair-sources-2026-11/avbox/0825-avbox.json)
- 最小点播排障配置：[vod-verified.json](https://cdn.jsdelivr.net/gh/LDeom/tvbox@audit/repair-sources-2026-11/avbox/vod-verified.json)
- 普通直播配置：[live.json](https://cdn.jsdelivr.net/gh/LDeom/tvbox@audit/repair-sources-2026-11/avbox/live.json)

## 成人内容文件标识

以下文件属于成人内容配置，统一按 **18+** 标识，必须与普通点播、普通直播配置分开管理，不应在普通入口中混合展示：

- `99188-avbox.json` — **18+ 成人点播配置**
- `adult-live.json` — **18+ 成人直播配置**

18+ 是内容分级标识，不是年龄验证机制，也不代表内容来源已经获得授权。使用者应遵守所在地法律、平台规则及内容提供方的年龄与访问限制。

## 兼容性说明

- 点播 JSON 使用 `sites` 字段及站点参数；AVBox 按其支持的站点类型解析。
- 直播 JSON 使用 AVBox 所需的 `lives` 结构；实际兼容性仍应在目标版本中测试。
- 配置文件可通过 jsDelivr 下载，不代表文件内的 API、脚本、图片、播放地址或其他外部依赖也能访问。
- 第三方站点可能受站点改版、登录态、网络地区、脚本兼容性、鉴权或本地代理依赖影响。
- **状态分级：** 文件可下载、JSON 可解析、API 有响应、实际播放成功，是不同验证阶段，不可混为一谈。
- 未完成目标设备实际播放验证的站点，不标记为“已可播放”。
- 成人配置与普通配置分离；文件名及文档均明确标记 **18+**。

## 点播无内容问题的排查版本（2026-11-19）

- `vod-verified.json` 是用于隔离 Spider/JAR/JS 依赖的最小点播排障配置。
- 此前检查曾观察到其 API 列表端点返回结构化 JSON；这不是 AVBox 真机详情或播放成功的证明。
- 如果导入成功但没有分类/影视，应进一步区分配置下载、JSON 解析、分类接口、详情接口及播放地址提取阶段。

## CDN 验证记录（2026-11-19）

- 用户设备已确认可以通过 jsDelivr 打开以下文件：`avbox/vod-verified.json`。
- 已验证的 URL 格式：`https://cdn.jsdelivr.net/gh/LDeom/tvbox@audit/repair-sources-2026-11/...`
- 该验证仅针对上述文件的下载访问；其他文件、配置内嵌资源和第三方媒体源仍需分别验证。
- GH-Proxy 链路此前在用户设备上无法访问，因此不再将其作为首选订阅下载入口。

## 维护边界

- 本次维护只记录 CDN 下载链路与配置分类，不代表第三方源已获授权或可公开再分发。
- 不因单次网络检查失败就擅自删除源；也不把仅能下载配置或返回列表的源标记为播放成功。
- 所有改动仅位于 `audit/repair-sources-2026-11` 分支；不修改 `master`、不创建 PR、不发布 Release。
