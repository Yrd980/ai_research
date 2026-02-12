# AI Research Workspace

面向每日 "AI 早报" 的 agentic 维护仓库。

## 目标

- 主目标：抽取不可再分名词原语。
- 次目标：生成 wiki 候选断言并人工晋升。

## 核心目录

- `data/raw/wechat/`：日报原文
- `data/processed/`：原语与共现结果
- `data/templates/`：CSV 模板
- `wiki/index/`：wiki 索引与断言层

## 必须维护的产物

- `data/raw/wechat/ingest_manifest.csv`
- `data/processed/primitives.csv`
- `data/processed/primitive_occurrences.csv`
- `data/processed/primitive_hyperedges.csv`
- `wiki/index/assertions.csv`
- `wiki/index/assertions_candidates.csv`
- `wiki/index/assertions_review_queue.csv`
- `wiki/index/relations.csv`
- `wiki/index/history_timeline.csv`

## Agentic 日常流程

1. 新增或更新 `data/raw/wechat/YYYY-MM-DD.md`。
2. 更新 `data/raw/wechat/ingest_manifest.csv`。
3. 维护 `data/processed/primitives.csv`（只保留名词原语）。
4. 同步更新 `primitive_occurrences.csv` 与 `primitive_hyperedges.csv`。
5. 同步更新 `assertions_candidates.csv` 与 `assertions_review_queue.csv`。
6. 人工审核后将通过项写入 `wiki/index/assertions.csv`。
7. 同步 `wiki/index/relations.csv` 与 `wiki/index/history_timeline.csv`。

## 约束

- 全程客观、原子化、可追溯。
- 优先第一手链接；去除社媒转述噪声。
- 默认不新增本地构建脚本；直接在 agentic 编辑中维护结果。
- 详细规则以 `AGENTS.md` 为准。
