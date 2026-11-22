# Google Scholar 论文采集报告

- 作者：檀韬（Tao Tan）
- Google Scholar ID：`lLg3WRkAAAAJ`
- 数据获取时间：2026-11-22T09:41:13Z
- 报告生成时间：2026-11-22T10:14:11Z
- 采集轮次：`20261122T094058.988533Z-a52546c2`
- 原始 API 条目数：416
- 清洗后保留论文数（2021 年及之后）：330
- 排除的早期论文数（年份早于 2021）：73
- 排除的年份缺失或无效论文数：13
- CSV 审核行数：330
- 疑似重复记录数：8
- 与上次快照中符合年份条件的记录比较：330 篇

## 分页完整性与年份清洗

共获取 5 页原始响应；每页最多 100 条。原始响应保留所有年份，审核数据仅保留发表年份为 2021 或之后的论文。缺失或无法识别年份的记录不进入清洗后文件，年份字段不推测、不补造。采集在下一页不存在时结束。

| start | API 条数 | 数据获取时间 |
|---:|---:|---|
| 0 | 100 | 2026-11-22T09:41:07Z |
| 100 | 100 | 2026-11-22T09:41:08Z |
| 200 | 100 | 2026-11-22T09:41:10Z |
| 300 | 100 | 2026-11-22T09:41:12Z |
| 400 | 16 | 2026-11-22T09:41:13Z |

## 各年份论文数量

| 年份 | 篇数 |
|---|---:|
| 2021 | 10 |
| 2022 | 13 |
| 2023 | 51 |
| 2024 | 71 |
| 2025 | 102 |
| 2026 | 83 |

## 字段缺失情况

统计口径为清洗后去重的 330 条论文；缺失字段保持为空，没有推测或补造。

| 字段 | 缺失数 / 论文总数 |
|---|---:|
| `title` | 0 / 330 |
| `authors` | 0 / 330 |
| `year` | 0 / 330 |
| `publication` | 7 / 330 |
| `citation_count` | 86 / 330 |
| `link` | 0 / 330 |
| `citation_id` | 0 / 330 |

## 重复记录供人工核验

按 `citation_id` 去重；相同标题和年份但不同 `citation_id` 的记录仍保留，并标记为疑似重复。CSV 保留清洗后所有论文条目，JSON 的 `publications` 为去重结果，`duplicate_records` 保留疑似重复条目。

| 原因 | 标题 | 年份 | citation_id | 对照 citation_id |
|---|---|---:|---|---|
| possible_title_year_duplicate | Generative Artificial Intelligence in Medical Imaging: Foundations, Progress, and Clinical Translation | 2025 | lLg3WRkAAAAJ:EPG8bYD4jVwC | lLg3WRkAAAAJ:qe6vwMD2xtsC |
| possible_title_year_duplicate | VLA: Prior-Guided Vision-Language-Action Models via World Knowledge Variation | 2026 | lLg3WRkAAAAJ:MIg0yeAD4ggC | lLg3WRkAAAAJ:SxCCDk4iOpsC |
| possible_title_year_duplicate | BioVFM-21M: Benchmarking and Scaling Self-supervised Vision Foundation Models for Biomedical Image Analysis | 2025 | lLg3WRkAAAAJ:Xl6nMSl579sC | lLg3WRkAAAAJ:w1MjKQ0l0TYC |
| possible_title_year_duplicate | Multimodality image processing techniques for training image data generation and usage thereof for developing mono-modality image inferencing models | 2025 | lLg3WRkAAAAJ:r_AWSJRzSzQC | lLg3WRkAAAAJ:wvYxNZNCP7wC |
| possible_title_year_duplicate | Multi-layer image registration | 2024 | lLg3WRkAAAAJ:6ZxmRoH8BuwC | lLg3WRkAAAAJ:-mN3Mh-tlDkC |
| possible_title_year_duplicate | Combining machine and deep transfer learning for mediastinal lymph node evaluation in patients with lung cancer. | 2024 | lLg3WRkAAAAJ:JP7YXuLIOvAC | lLg3WRkAAAAJ:jgBuDB5drN8C |
| possible_title_year_duplicate | Is There a Difference between Paper and Electronic Chinese Signatures? | 2023 | lLg3WRkAAAAJ:ZzlSgRqYykMC | lLg3WRkAAAAJ:OcBU2YAGkTUC |
| possible_title_year_duplicate | Comprehensive deep learning-based framework for automatic organs-at-risk segmentation in head-and-neck and pelvis for MR-guided radiation therapy planning | 2023 | lLg3WRkAAAAJ:yFnVuubrUp4C | lLg3WRkAAAAJ:yqoGN6RLRZoC |

## 与前一完整快照比较

### 新增论文（0）

| 标题 | 年份 | citation_id |
|---|---:|---|
| — | — | — |

### 引用量变化（0）

| 标题 | citation_id | 上次 | 本次 |
|---|---|---:|---:|
| — | — | — | — |

### 本次未见的旧论文（0）

| 标题 | 年份 | citation_id |
|---|---:|---|
| — | — |

## API 请求与额度估算

- HTTP API 请求尝试次数（含重试）：5
- 额度消耗保守估算：5 次搜索请求
- 已完成分页的本地缓存命中不发起 API 请求，因而不增加本轮请求数。
- SerpApi 服务端缓存命中可能免费；本报告按每次 HTTP 尝试一次搜索请求估算，实际扣额以账户面板为准。

报告生成时间：2026-11-22T10:14:11Z
