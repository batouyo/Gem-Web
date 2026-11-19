# 重复结构与组件盘点

本文件只记录现有 HTML 可复用结构，不创建或迁移任何组件。页面标签计数来自当前 Git 跟踪的 345 个 HTML 文件。注意：有相同 class 不一定代表内容语义、样式和交互相同，应分模板族迁移。

## 观测到的重复结构

| 结构/候选组件 | 源码证据 | 复用建议 |
|---|---|---|
| SiteLayout / Navigation | 189 页含 `<nav>`；`index.html`、`all_research.html`、`Publication2025.html`、`Team.html`、`Contact.html` 都有重复 Bootstrap navbar、Logo、9 个栏目链接 | Astro `BaseLayout` + `SiteHeader`；导航项单一配置，逐个验证旧链接与断点折叠。多个历史页面菜单目标不一致，不能盲目复制单页版本。 |
| SiteFooter | 189 页含 `<footer>` 标签；旧页也可能用非 footer div 实现 | `SiteFooter` 统一实验室名称/学校归属/版权；先盘点旧 footer 文案差异。 |
| PageHero / PageHeader | `index.html` 的 jumbotron 介绍区；新闻详情、Team、Contact 等重复用 Bootstrap `jumbotron`、container/row/col 结构 | 抽取参数化标题、日期、说明和可选封面；首页独特大 Hero 保留为变体。 |
| NewsCard / NewsGrid | 首页硬编码新闻卡片，含缩略图、标题、日期；`all_news.html` 有旧卡片结构；history 脚本以 JS 对象存新闻 | 单一 Markdown collection 驱动首页、归档列表和详情；组件只渲染数据，封面字段需编辑确认。 |
| NewsArticle | 多个 `New*.html` 详情页以标题/日期/图像/正文/返回按钮构成；部分标题、正文、插图和布局写法不同 | Markdown frontmatter + `NewsLayout`；将图注、链接、嵌入内容与中英双语变体作为显式字段/Markdown 内容块。 |
| ResearchCard / ResearchDetail | `all_research.html` 中多个项目卡片链接到 `Research/*.html`，同时有 `_research` 成员目录和 paper-info/frame 页 | 统一 `ResearchCard` 与研究详情 layout；保留成员研究页、项目页、论文说明页的区别。 |
| PublicationTable | `Publication2025.html` 等表格按年/其他年份加载 `output*.json`；旧的 `publications2024.html` 等为另一套硬编码/数据驱动表 | TypeScript publication schema + 一份归一化数据；year filter/list view 用配置控制，确保年份和字段有版本校验。 |
| Pagination | 首页 CSS 声明 `#history-pagination`、`.page-item`，且加载历史新闻 JS；需由页面脚本和浏览器运行确认是否执行 | 新站优先用静态分页或 Astro 生成归档；页码/无 JS 状态需可访问。 |
| Breadcrumb | 本次扫描未发现稳定、广泛使用的 `<nav aria-label="breadcrumb">` / `.breadcrumb` 结构 | 不作为现有必迁组件；新路由如需层级导航再设计。 |
| Button / Return link | 多页复用 Bootstrap `.btn`、`btn-dark/success`，详情页常见 Return | `Button` 可依赖设计 token/链接组件；不要把不同操作和颜色一概合并。 |
| Container / Grid | Bootstrap `.container`、`.row`、`.col-*` 在主要页面重复；具体宽度跟 Bootstrap 栅格及局部 CSS 叠加 | Astro layout 复用容器，SCSS design tokens 控制页面最大宽度、间距和响应断点。 |

## 重复样式与不一致线索

- 当前至少 `130` 个内联 `<style>` 块和 `2679` 个内联 `style` 属性；首页自己覆写新闻卡片、hover、分页和历史条目布局。
- `192` 个 `@media` 声明可在 CSS/SCSS 文本中静态扫描到；`191/345` 页含 viewport meta。尚未运行真实浏览器矩阵，不能由此推断所有页面适配有效。
- 导航文案和 href 存在版本漂移的证据：如首页/主栏目链接 `Publication2025.html`，旧新闻/论文页可能链接 `Publication2024.html` 或小写 `publications2024.html`；`all_news.html` 的合作伙伴链接曾出现 `article.html`。自动链接检查在资产清单中记录实际路径匹配。
- 部分 HTML 使用嵌套 `<p>`、硬编码像素宽度、不同年份文件命名风格；未对 DOM 进行完整规范性校验，迁移前应以模板样例确认。

## 建议复用顺序

1. **共享外壳**：`BaseLayout`、header/nav、footer、响应式容器。
2. **列表内容**：NewsCard / NewsGrid / archive entry、ResearchCard、PublicationTable。
3. **详情布局**：新闻文章与科研项目文章分开建 layout，共用媒体图/图注/元数据组件。
4. **交互控件**：Button、静态分页、导航折叠；先确定 Astro 输出和无 JavaScript 体验。

## 样本页

首页 `html/index.html`；新闻列表 `html/all_news.html` 和 `html/news/history_news.js`；新闻详情 `html/New20260923.html`（若存在，否则按新闻清单首条）；科研列表 `html/all_research.html`；论文页 `html/Publication2025.html`；团队 `html/Team.html`。路由和输入证据见 `route-map.csv`、`news-inventory.csv`。
