# P1–P5 重构风险清单

等级含义：高 = 会造成页面/内容/外部入口明显丢失或大面积返工；中 = 影响一组页面或需要人工修订；低 = 局部、可在常规验收中消化。建议阶段是处理窗口，不代表本 P0 已执行修复。

| 风险 | 等级 | 证据/影响 | 建议阶段 | 验证方法 |
|---|---|---|---|---|
| 独立 HTML 与重复模板导致迁移面大 | 高 | `route-map.csv` 覆盖全部 HTML；共享 nav/footer/Bootstrap 网格在多个页面重复，且局部差异并存 | P1 定模板族；P2 建公共 Layout；P3 分批迁移 | 按页面类型抽样比对导航、Hero、页脚、卡片和详情正文；迁移前后路由数量对照 |
| 新闻在详情、首页、列表和 JS 数组多处维护 | 高 | 首页卡片硬编码；`html/all_news.html` 有静态/注释内容（21 个链接指向 20 篇新闻，其中 1 篇重复）；`html/news/history_news.js` 另有 `HISTORY_NEWS` 数据；清单显示 10 篇出现在多个入口 | P2 建 Markdown collection；P3 批量迁移 | 以 `news-inventory.csv` 对照源条目；标题/日期/图/旧 URL 覆盖率须 100% 或逐项解释 |
| 新闻元数据/图片异常，自动迁移可能错配 | 高 | 日期格式不一、日期可能只在正文、首图只是启发式封面；部分列表链接可能大小写漂移 | P2 内容 schema；P3 迁移时人工复核 | 逐篇核对标题、日期、语言、封面、正文插图和 slug；按截图验收页面 |
| 旧 URL 变更造成外链与搜索流量损失 | 高 | `New*.html`、大小写混用、空格/中文路径和多个年份页面；新路由均为建议 | P1 定 route contract；P3 重定向/别名 | route-map 检查一对一/显式例外；自动生成 redirect 表；抽查旧链接 HTTP 状态及搜索索引 |
| 本地资源路径无效/大小写敏感 | 高 | 静态扫描产生的异常及大小写候选见 `asset-inventory.csv`；Linux Nginx 对大小写敏感 | P1 先修/登记已知路径；每个迁移阶段持续扫描 | Linux 环境解析所有本地 `src`/`href`/`srcset`/CSS URL，检查编码空格、中文路径；生成 404 清单 |
| JavaScript 动态引用未静态求值 | 中 | 审计只解析 HTML/CSS；JS 拼接路径、回调数据、iframe 动态加载可能未发现 | P2/P3 迁移数据交互时 | 搜索 `src=`, `location`, `fetch`, `document.write`, `innerHTML` 等动态代码；浏览器网络面板逐页确认 |
| Bootstrap/jQuery 组件与旧脚本依赖 | 中 | HTML 依赖 Bootstrap data attributes/jQuery/Popper；页面脚本顺序和插件行为可能脆弱 | P2 设计 Astro 交互策略；P4 收敛依赖 | 桌面/移动测试 nav collapse、分页、表格数据注入；禁用 JS 检查回退 |
| 出版物的数据格式与版本并存 | 高 | `.bib`、JSON、`output([...])` JS callback、年份 HTML 同时存在，字段大小写/命名不同 | P2 定 schema/importer；P3 统一迁移 | schema 校验记录数、年份、作者、标题、期刊和 DOI；与旧表逐年比较 |
| 模板/字体/图标及附件许可链不清 | 中 | Mundana README 称 MIT，而 `html/package.json` 提及 WowThemesNet License；CDN 字体/图标及 Office 文件各有来源 | P1/P2 内容和设计冻结前 | 对照实际许可证文件、外部字体/图标许可和每类图片来源；保留必要 attribution |
| Docker/Nginx 当前直接服务 `html/`，与 Astro 输出目录不匹配 | 高 | Compose bind mount `./html:/usr/share/nginx/html`；Nginx root 写死 | P4 静态构建切换 | 构建输出 smoke test、容器路径映射验证、404/资产路径检查；生产切换前在临时 compose 验证 |
| 外部 Google Fonts/Font Awesome CDN 可用性与隐私/稳定性 | 中 | 主页面直接引用 Google Fonts 和 Font Awesome CDN，网络失败会改变字体/图标表现 | P1 视觉基线；P2/P4 资源策略 | 离线/拦截 CDN 比较；审查缓存、版本、许可和隐私要求 |
| 没有浏览器截图/行为测试基线 | 中 | 当前执行环境无浏览器自动化工具；源码只能确认布局声明，不能确认实际渲染 | P1 | 在标准 Chromium 环境采集指定 desktop/mobile 截图并人工评审；建立每次迁移的视觉回归流程 |
| 疑似旧页/测试页被误删或遗漏 | 中 | `test*`、`_frame`、重复年份页和模板副本仍可能被外部链接或 iframe 使用；本任务不判废 | P1 内容 owner review；P3 route decision | 查全站 inbound link、服务日志/搜索引擎入口（若可得）、人工确认后才标“不迁移” |
| 语言混杂、HTML 结构/编码差异 | 中 | 英文页面与中文新闻/附件并存，标题日期和字符集/文件名格式不统一 | P2 schema 与 markdown 约定 | 检查 UTF-8、语言 frontmatter、中文 URL 编码、标题与摘要抽取；随机人工校对 |

## 验收门槛建议

- P1：页面/路由清单由内容负责人确认；桌面与手机视觉方向有可比较截图；保留品牌资产与字体策略确认。
- P2：Astro layout/components 有代表性原页对照；内容 schema 和资源命名约定确定。
- P3：页面、新闻、研究与出版物迁移均保留旧 URL 映射；无未解释资源 404；所有内容缺失有清单。
- P4：Docker/Nginx 使用构建输出的临时/预发布验收通过，回滚方案存在。
- P5：桌面/移动视觉回归、路由/链接检查、内容数量核对通过后再决定发布。
