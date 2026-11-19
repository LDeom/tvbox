# AVBox 订阅配置

本目录提供 AVBox 可读取的 TVBox 系列 JSON 配置与直播订阅入口。所有仓库内文件引用均改为你指定的 gh-proxy.com + raw.githubusercontent.com 形式。

## 订阅地址

- 普通点播配置：[0825-avbox.json](https://gh-proxy.com/https://raw.githubusercontent.com/LDeom/tvbox/audit/repair-sources-2026-11/avbox/0825-avbox.json)
- 普通直播配置：[live.json](https://gh-proxy.com/https://raw.githubusercontent.com/LDeom/tvbox/audit/repair-sources-2026-11/avbox/live.json)
- 成人点播配置：[99188-avbox.json](https://gh-proxy.com/https://raw.githubusercontent.com/LDeom/tvbox/audit/repair-sources-2026-11/avbox/99188-avbox.json)
- 成人直播配置：[adult-live.json](https://gh-proxy.com/https://raw.githubusercontent.com/LDeom/tvbox/audit/repair-sources-2026-11/avbox/adult-live.json)

## 兼容性说明

- 点播 JSON 保留原配置的 sites 字段与 type/api/ext/jar 等站点参数；AVBox 的 ConfigParser 按 sites[].key/type/api 解析站点。
- 直播 JSON 使用 lives 数组；AVBox 支持 lives 配置，也支持直接读取 M3U、TXT。
- 原配置中仓库相对路径（例如 ./jar、./json、./js、./lib、./list.txt）已改成绝对 gh-proxy 代理 Raw 地址，避免代理域名下相对路径解析到错误位置。
- 订阅中只列出结构正常且仓库内存在的直播列表文件；这不等于每个直播 URL 都已完成真实播放验证。
- TVBox 的 type=3 Spider / JS / JAR 站点依赖对应脚本或运行环境。AVBox 具备相关 CatVod 运行代码，但个别站点仍可能因第三方站点改版、登录态、网络地区、脚本兼容性或本地代理依赖而不可用。
- 未验证成功的 API 不标注为“已可播放”；建议在 AVBox 中逐个测试。
- 成人内容订阅与普通订阅完全分离，请按需自行添加。
- 本次仅在审计分支新增文件，不修改 master、不创建 PR、不发布 Release。
