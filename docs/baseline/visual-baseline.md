# 当前网站视觉与功能基线（源码审阅）

## 验证范围

- 记录基于 HTML、`html/assets/css`、`html/assets/js` 的静态源码，不是浏览器截图或线上访问结果。
- 本运行环境没有 Chromium、Chrome、Firefox、Playwright 或 Selenium；未生成截图，`screenshots/README.md` 说明后续采集办法。
- 建议复测视口：桌面 1440×900、手机 390×844。当前工作未验证实际折行、图片裁切、滚动、键盘操作或外部 CDN 可用性。

## 代表页面

| 页面 | 导航与布局 | 字体/颜色/组件 | 可从源码确认的交互 | 待浏览器验证 |
|---|---|---|---|---|
| 首页 `html/index.html` | 顶部固定 Bootstrap navbar；IMCL 标题/介绍的 jumbotron；两列近期新闻卡片，后续有研究/新闻内容区 | Logo；`main.css`；Google Playfair Display + Source Sans Pro；绿色品牌色（局部 CSS 使用 `#03A87C`）、白色背景、粉/玫红 hover；圆角新闻图卡片 | 移动导航使用 Bootstrap `collapse` data attributes；7 篇最新新闻卡片硬编码在 HTML；页面加载 `history_news.js`，内联脚本消费历史新闻数据并生成列表/分页 | 1440 下 Hero 图片、首屏高度、两列卡片；390 下菜单折叠、新闻卡片堆叠；脚本加载及分页实际表现 |
| 新闻列表 `html/all_news.html` | 固定导航后是静态新闻链接列表；另保留大段注释掉的旧卡片 | 与主站共用 `main.css`；主色绿、Bootstrap link/button | 当前活动新闻项是普通 `<a>` 链接；未引用首页的 `history_news.js` | 视觉呈现、顺序/分页表现、注释内容是否需要保留 |
| 新闻详情 `html/New20260923.html`（如该页不存在则选新闻清单中的首篇） | 标题/日期/主图，正文为中央窄列，分节标题，文章后返回按钮 | Bootstrap jumbotron/container/grid；文章图片有圆角/阴影；文字行高与标题存在局部 `<style>` | 返回首页链接；菜单折叠 | 首图宽度、长标题换行、正文行长、移动端图片和按钮 |
| Research `html/all_research.html` | 固定导航；介绍/卡片式项目列表，主区域按 Bootstrap 网格呈现项目 | 绿色链接及 hover 色，项目缩略图/链接；共享 `main.css` | 项目标题链接到详情 HTML；导航链接 | 卡片数量和高度、长标题溢出、移动端列数和图片比例 |
| Publications `html/Publication2025.html` | 固定导航、年份切换、宽表格按年份筛选 | Bootstrap 主站风格与单页额外表格 CSS；标题/作者/出版物列 | 页面内 `output(jsonData)` 回调 + `output*.json` 脚本注入表格；窄屏媒体规则将表格转成块布局/隐藏表头 | 数据文件脚本加载、窄屏可读性、表头与字段标签、不同年份链接正确性 |
| Team `html/Team.html` | 固定导航；成员卡片/网格布局 | 共用 `main.css`，局部卡片 hover 边框/阴影 | 个人页面或相关链接；导航折叠 | 成员分组、卡片高度、图片比例、手机阅读顺序 |

## 共享视觉特征（源码证据）

- 站点使用 Mundana/Bootstrap 风格：`container`、`row`、`col-*`、`jumbotron`、`navbar`、`card`、`btn` 等类广泛出现。
- 多数主页面引用 `html/assets/css/main.css`，并从 CDN 请求 Google Fonts 与 Font Awesome。
- 品牌识别集中在 IMCL/GEMLab Logo、绿色主色和“智能医学计算实验室”文字；具体 Logo 文件引用各页不完全一致，迁移应保留可验证的原始资产。
- 页内存在内联 CSS 与 inline style（全站合计 `130` 个 `<style>` 块、`2679` 个 `style=` 属性），会使同一组件的间距、宽度及颜色在页面间漂移。
- 静态扫描发现 `191/345` 个 HTML 页面具有 viewport meta；以源代码统计不能替代手机实测。

## 功能基线与可访问性待核验

- 主要导航、文章、卡片和按钮以链接实现；Bootstrap collapse 依赖 jQuery/Bootstrap JS bundle。
- 源码包含首页历史新闻列表/分页的生成逻辑及出版物 JSON 回调；浏览器实际运行、数据文件加载、分页行为、按钮/菜单触屏操作仍需验证。
- 建议检查图片 alt 文本覆盖、键盘焦点、对比度、标题顺序、表格移动端语义及 JavaScript 关闭时的回退行为；本次没有做无障碍自动化或人工浏览器审计。

## 截图索引

本次未创建截图，避免伪造渲染结果。后续安装/提供浏览器截图环境后，按以下名称保存到本目录 `screenshots/`：`home-desktop-1440x900.png`、`home-mobile-390x844.png`、`news-list-desktop-1440x900.png`、`news-detail-desktop-1440x900.png`、`research-desktop-1440x900.png`、`publications-mobile-390x844.png`、`team-desktop-1440x900.png`。使用本地只读静态服务器提供 `html/` 目录；记录浏览器版本、日期、字体网络状态和访问 URL。
