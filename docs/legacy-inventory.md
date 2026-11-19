# P0 项目盘点与基线报告

## 范围与证据口径

- 本次扫描基于本地 Git 跟踪文件；生成前的工作区干净，分支 `main`，基线 Commit `9b1a27f8f242c4bfceebe81e84a0c5759469b72a`。
- Nginx 配置把 `html/` 挂载为文档根目录；因此 `html/` 下 HTML 文件按旧站路径映射，仓库外该目录的 HTML 会单独标识。
- “已验证”指源文件中直接可见的事实；页面实际运行行为、外部链接可用性、访客视角视觉结果则需浏览器验证。
- 扫描脚本静态解析 HTML 的 `src`/`href`/`srcset`/`poster`/`data`/`background`、内联样式和 CSS `url()`。不执行 JavaScript，也不访问网络；动态路径和外部资源不作为已验证。
- 只读扫描没有修改现有 HTML、CSS、JavaScript、部署配置或静态资源。

## 项目概况

Gem-Web 是澳门理工大学应用科学学院 IMCL（Intelligent Medical Computing Laboratory）实验室的静态网站。首页称实验室提供数字医疗解决方案；自定义域名见 `html/CNAME`。页面主要为独立 HTML，样式为传统 CSS/SCSS，交互使用 jQuery/Bootstrap 资源，内容以静态文件和 JavaScript 数据表为主。

| 指标 | 结果 |
|---|---:|
| Git 跟踪文件（扫描范围） | 1358 |
| HTML 文件（全仓库） | 345 |
| HTML 位于 Nginx `html/` 根目录 | 345 |
| HTML 位于 `html/` 外 | 0 |
| HTML 页面类型 | 16 类 |
| 新闻详情候选 | 75 |
| 资源/其他文件（按扩展名） | 1013 |
| 静态引用异常（missing / 大小写 / 有歧义） | 218 条引用 |
| 非空文件 SHA-256 完全重复组 | 369 组 |
| 零字节跟踪文件 | 16 |

### 根目录文件

``GEM_library.bib`, `default.conf`, `docker-compose.yaml`, `exceltojson.py`, `first test.txt`, `papers_info_2026-01-12_18-47-12.json`, `test.py`。` 重点用途：`docker-compose.yaml`/`default.conf` 提供 Nginx 静态服务配置；`GEM_library.bib` 和根目录 JSON 是出版物数据源/导出数据；`exceltojson.py`、`test.py` 是数据转换脚本。`first test.txt` 名称像临时文件，但仅凭名称无法确认是否可删除。

### HTML 子目录文件分布

| `html/` 一级目录 | Git 跟踪文件数 |
|---|---:|
| `template-mundana-bootstrap-html-master` | 437 |
| `assets` | 300 |
| `(html root)` | 155 |
| `team` | 46 |
| `Research` | 37 |
| `junqiang_research` | 15 |
| `rongsheng_research` | 15 |
| `yqh_research` | 15 |
| `zhangzhuoneng_research` | 15 |
| `xiong_research` | 13 |
| `siyi_research` | 12 |
| `yanghao_research` | 12 |
| `haoming_research` | 11 |
| `zehui_research` | 11 |
| `huangda_research` | 8 |
| `jiaju_junqiang_PETCT` | 8 |
| `jiaju_research_segement` | 8 |
| `kangyang_research` | 8 |
| `news_20231216` | 8 |
| `shaobing_research` | 8 |
| `tianyu_xinye_research` | 8 |
| `.idea` | 7 |
| `jiangmingfu_research` | 7 |
| `news_20240521` | 7 |
| `Xiexinghe_research` | 6 |
| `xiejiefeng_research` | 6 |
| `Demo` | 5 |
| `news_20240520` | 5 |
| `news_20240816` | 5 |
| `news_20241003` | 5 |
| `pujun_DaVinci` | 5 |
| `zelu_research` | 5 |
| `gaojie_research` | 4 |
| `news_20231228` | 4 |
| `news_20240113` | 4 |
| `news_20240229` | 4 |
| `news_20240404` | 4 |
| `news_20240519` | 4 |
| `news_20250303` | 4 |
| `news_20251109` | 4 |
| `news_20260610` | 4 |
| `stanley_research` | 4 |
| `zhengrui_research` | 4 |
| `Chenzhengxuan_research` | 3 |
| `Liyanfeng_research` | 3 |
| `Qiuhui_research` | 3 |
| `Yaofei_research` | 3 |
| `luoxiangmin_research` | 3 |
| `news_20231121` | 3 |
| `news_20231214` | 3 |
| `news_20241201` | 3 |
| `news_20260922_2` | 3 |
| `panxintao_research` | 3 |
| `zhangningyi_research` | 3 |
| `liangzhichao_research` | 2 |

### 页面分类

| 类型（基于标题、结构和路径内容规则） | 数量 |
|---|---:|
| `template-example` | 92 |
| `news-detail` | 75 |
| `embedded-fragment` | 61 |
| `research-detail` | 61 |
| `team-profile` | 17 |
| `publications` | 13 |
| `news-fragment-or-frame` | 11 |
| `test-or-experiment` | 5 |
| `vacancies` | 2 |
| `research` | 2 |
| `education` | 1 |
| `partners` | 1 |
| `team` | 1 |
| `news-list` | 1 |
| `research-list` | 1 |
| `home` | 1 |

分类规则自动化且可复核；`other/unknown`、frame/fragment、测试和模板页面仍需人工判定。完整来源、旧 URL、标题、站内导航入口、图片/脚本和迁移建议见 `route-map.csv`。

| 路由状态 | 数量 |
|---|---:|
| `manual-review-before-migration` | 169 |
| `proposed` | 156 |
| `route-collision-review` | 20 |

`route-collision-review` 页面虽然已在 CSV 中给出不同的临时建议路径，但它们共享较宽泛的内容分类路由，仍需内容负责人确认最终 URL；frame、template、test 页面则不预设新公开路由。

### 主要页面与系统结构

| 源文件 | 已确认用途/证据 |
|---|---|
| `html/index.html` | `home`；title：IMCL；nav 标签：True；页脚标签：True。 |
| `html/all_news.html` | `news-list`；title：NEWS；nav 标签：True；页脚标签：True。 |
| `html/all_research.html` | `research-list`；title：Research；nav 标签：True；页脚标签：True。 |
| `html/Publication2025.html` | `publications`；title：Research；nav 标签：True；页脚标签：True。 |
| `html/Team.html` | `team`；title：IMCL；nav 标签：True；页脚标签：True。 |

- `docker-compose.yaml` 以 `nginx:alpine` 将主机 `49306` 端口映射到容器 `80`，只读挂载 `default.conf` 和 `html/`。
- `default.conf` 配置 `index.html`/`index.htm`，没有应用后端或 API 代理。
- `html/assets/` 有 300 个跟踪文件；`html/template-mundana-bootstrap-html-master/` 保存模板副本及构建文件。
- Gulpfile 提供 SCSS 编译、watch 和 open 任务；`html/package.json` 仅列 Gulp 开发依赖，未显示 Astro/Vite/TypeScript 应用构建。
- Python 辅助脚本包括根级 Excel 转输出格式脚本、将 JSON 写为 `window.PAPERS_JSON` 的 `test.py`，以及 BibTeX 转 JSON 脚本。脚本的当前路径/工作目录假设应在未来数据流程整理时核实。
- 代码中可见 Bootstrap、jQuery、Popper 和 Font Awesome；Google Fonts/Font Awesome CSS 通过外部 CDN 引用。外网加载与许可证/版本稳定性未做在线验证。

### 文件扩展名分布

| 扩展名 | 数量 |
|---|---:|
| `.scss` | 400 |
| `.html` | 345 |
| `.png` | 216 |
| `.jpg` | 169 |
| `.docx` | 48 |
| `[none]` | 39 |
| `.js` | 37 |
| `.css` | 16 |
| `.svg` | 16 |
| `.doc` | 12 |
| `.txt` | 9 |
| `.json` | 8 |
| `.pdf` | 5 |
| `.xml` | 4 |
| `.map` | 4 |
| `.ico` | 4 |
| `.jpeg` | 4 |
| `.py` | 3 |
| `.md` | 3 |
| `.code-workspace` | 2 |
| `.exe` | 2 |
| `.pptx` | 2 |
| `.yml` | 2 |
| `.bib` | 1 |
| `.conf` | 1 |
| `.yaml` | 1 |
| `.iml` | 1 |
| `.tif` | 1 |
| `.psd` | 1 |
| `.github` | 1 |
| `.gif` | 1 |

### 静态资源与链接检查

- `5244` 个 HTML/CSS 静态引用候选中，`4489` 个能按本地文件解析，`479` 个为外部 URL，`15` 个为仅 fragment、`43` 个为空引用；另有 `218` 次无法精确解析或大小写不匹配。按来源/原文/状态去重后为 `202` 行，见 `asset-inventory.csv` 的 `unresolved local reference`。
- 按文件用途分类：

| 类型 | 跟踪文件数 |
|---|---:|
| `stylesheet` | 416 |
| `image` | 407 |
| `HTML page` | 345 |
| `document` | 67 |
| `other tracked file` | 66 |
| `script` | 37 |
| `data` | 16 |
| `helper/source script` | 3 |
| `deployment/config` | 1 |

- 异常样例（完整来源、原始 URL、解析目标见资产清单）：

| 来源文件 | 原始引用 | 状态 | 候选目标 | 行 |
|---|---|---|---|---:|
| `html/Contact_frame.html` | `head_frame.html` | missing | `` | 8 |
| `html/Demo_Solutions_frame.html` | `head_frame.html` | missing | `` | 9 |
| `html/New20240229.html` | `./about.html` | missing | `` | 54 |
| `html/Partners_frame.html` | `head_frame.html` | missing | `` | 8 |
| `html/Publications_frame.html` | `head_frame.html` | missing | `` | 9 |
| `html/Research/Advanced_U-Net_for_Multi-class_Segmentation_of_Mammography.html` | `../Vacancies.html` | missing | `` | 45 |
| `html/Vancancies _frame.html` | `head_frame.html` | missing | `` | 8 |
| `html/Vancancies.html` | `./Research2024.html` | missing | `` | 33 |
| `html/all_news.html` | `./article.html` | missing | `` | 49 |
| `html/all_research.html` | `./Research/BLENet: a Bio-inspired Lightweight and Efficient Network for Left Ventricle Seg` | missing | `` | 604 |
| `html/haoming_research/paper_info_frame_haoming_research .html` | `../head_frame.html` | missing | `` | 8 |
| `html/huangda_research/paper_info_frame_Huangda_research .html` | `../head_frame.html` | missing | `` | 8 |
| `html/jiaju_junqiang_PETCT/paper_info_frame_jiaju_junqiang_research .html` | `../head_frame.html` | missing | `` | 8 |
| `html/jiaju_research_segement/paper_info_frame_haoming_research .html` | `../head_frame.html` | missing | `` | 8 |
| `html/jiaju_research_segement/paper_info_frame_jiajun_segment_research .html` | `../head_frame.html` | missing | `` | 8 |
| `html/jiaju_research_segement/paper_info_haoming_research.html` | `haoming_research_image.png` | missing | `` | 100 |
| `html/junqiang_research/paper_info_frame_junqiang_research .html` | `../head_frame.html` | missing | `` | 8 |
| `html/kangyang_research/paper_info_frame_kangyang_research .html` | `../head_frame.html` | missing | `` | 8 |
- 检查对空格、中文、百分号编码、查询字符串和 fragment 进行解码/分离；文件名匹配按大小写敏感，另报告唯一的 case-fold 候选。
- SHA-256 完全重复组为 `369`，只统计非空文件的字节完全重复；没有删除或移动资源。
- 未被扫描到的文件只标为“HTML/CSS 静态扫描未发现”，不等价于废弃；JS 拼接/动态资源、模板条件代码和外部网络资源未求值。`history_news.js` 中的字面量 href 单独解析，但不执行脚本。
- 资源完整清单包含路径、类型、字节数、SHA-256、重复路径、引用源和建议归属，详见 `asset-inventory.csv`。

### 部署与历史文件

- `html/CNAME` 写有 `www.gemlab.site`；仓库是否由 GitHub Pages 直接发布，以及当前线上部署链路，不由这份文件单独证明。
- `html/template-mundana-bootstrap-html-master/README.md` 把模板描述为 MIT；同目录 `package.json` 另列 WowThemesNet License URL。使用/重分发资产前应核对实际许可证文件和具体资源来源，不按模板副本整体推定许可。
- 文件名含 `test`、旧式 `_frame`、多份年份出版物页和模板示例均作为候选待审，不自动判废。页面分类和证据在路由表中。

## 功能与内容维护方式

- 首页 `html/index.html` 将 7 篇最新新闻卡片直接写在 HTML 中；此外页面含 `#history-list`/分页容器，加载 `html/news/history_news.js` 并通过内联脚本读取 `window.HISTORY_NEWS` 生成历史列表。两部分的链接、日期、标题和缩略图分别维护。
- `html/all_news.html` 是独立静态新闻列表，当前有 `21` 个活动详情链接、指向 `20` 篇不同新闻；文件中另保留注释掉的旧卡片，不加载 `history_news.js`。其中 `1` 篇在活动列表重复出现。
- `html/news/history_news.js` 暴露 `43` 个可解析 href；扫描还发现首页 `7` 个静态新闻详情链接。`10` 篇新闻出现在两个或以上维护入口；标题、日期和图片可能不一致。
- 新闻详情多数是单独 HTML，图片通常放在 `html/news_YYYYMMDD.../` 或成员/研究项目目录。标题、日期和封面提取规则各异；完整逐篇记录见 `news-inventory.csv`。
- `10` 篇新闻未能从正文 `<img>` 稳定识别封面（可能使用背景图、frame 或无图），封面字段保留为空；文件路径见 `news-inventory.csv`。日期均由页面文本或文件名规则提取，仍建议编辑复核。
- 标题识别结果为 English/Latin `69` 篇、mixed `4` 篇、Chinese `2` 篇；日期有 `70` 篇从可见页面文本提取、`5` 篇回退到文件名规则，仍建议人工复核。
- 出版物以 BibTeX、不同 `output*.json`（包含 `output([...])` JavaScript 回调格式）和手写年份 HTML 并存；不同年份页面及主导航可能未同步。

## 组件化发现

详见 `component-inventory.md`。扫描到 `189` 个页面有 `<nav>`、`189` 个页面有 `<footer>`，`130` 个内联 `<style>` 块、`2679` 个 HTML `style` 属性；191/345 个 HTML 带 viewport meta。页面容器/Bootstrap 卡片/nav/footer 是 Astro Layout 与组件的主要候选，但类名重复不代表语义一致，迁移时要按模板族归并。

## 视觉/交互基线

源码层面的页面基线与不能实测的项目见 `baseline/visual-baseline.md`。当前环境未安装 Chromium/Chrome/Firefox 或 Playwright/Selenium，因而未生成桌面/手机截图，也没有声称实际浏览器渲染已通过。

## 后续工作建议

1. 先把页面路由和新闻元数据定成唯一数据源，优先处理首页新闻、新闻列表和详情页。
2. P1 先锁定保留 Logo/绿色品牌调性、信息层级、桌面与移动断点；以首页、新闻列表、详情、研究列表为设计样板。
3. P2 建公共站点 Layout、导航、页脚、Hero、新闻卡、文章正文、Research 卡和 publications table，再逐类迁移。
4. 在迁移任何资源前使用本清单中的引用和哈希信息；对所有旧 URL 生成重定向/别名策略，并把当前静态引用异常列入逐项修复验收。

## 可重复执行

运行 `python3 scripts/audit_site_p0.py` 可基于 Git 跟踪的站点源码重新生成三个 CSV 与本文中的统计。当前脚本检查 CSV 结构、HTML 路由唯一性并报告未解析静态引用；人工内容判断和截图仍需单独验收。
