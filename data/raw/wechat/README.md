# WeChat 原文层

该目录仅存放日报原文，不做结构化加工。

## 文件规范

- 每日一个文件：`YYYY-MM-DD.md`
- 示例：`2026-02-12.md`

## 维护要求

1. 原文必须完整落盘（含原始链接、数字细节、机制描述、限制条件）；禁止摘要压缩替代原文。
2. 当日文件写入后，必须同步更新 `ingest_manifest.csv`。
3. 如果原文不完整，`ingest_manifest.csv` 必须设置 `is_full_text=false` 且 `needs_backfill=true`。
4. 不在原文文件中写推断性字段。

## 与下游关系

- 原语与共现：`data/processed/*`
- wiki 名词图谱索引：`wiki/index/*`

以上下游文件在同一次 agentic 维护中同步更新。
