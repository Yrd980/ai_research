# AI Research Workspace

面向每日 "AI 早报" 的 agentic 维护仓库。

## 目标

- 主目标：抽取不可再分名词原语。
- 次目标：构建无时间语义的全局名词图谱（节点/边/别名）。

## 分层边界

- 日报层（event stream）：记录每日输入与时序上下文。
- wiki 层（global graph）：累计名词节点与关联，不复刻日报事件。

## 原文保真要求

- `data/raw/wechat/YYYY-MM-DD.md` 必须保存完整原文，不允许用摘要替代。
- 原文中的数值指标、机制名称、限制条件与来源链接必须保留。
- 若当天仅有部分正文，`ingest_manifest.csv` 必须设置 `is_full_text=false` 且 `needs_backfill=true`，待全文补齐后改为 `is_full_text=true` 与 `needs_backfill=false`。

## 核心目录

- `data/raw/wechat/`：日报原文
- `data/processed/`：原语与共现结果
- `data/templates/`：CSV 模板
- `wiki/index/`：全局名词图谱索引
- `wiki/entities/`：按需创建的名词笔记页

## 必须维护的产物

- `data/raw/wechat/ingest_manifest.csv`
- `data/processed/primitives.csv`
- `data/processed/primitive_occurrences.csv`
- `data/processed/primitive_hyperedges.csv`
- `wiki/index/terms.csv`
- `wiki/index/term_aliases.csv`
- `wiki/index/term_edges.csv`
- `wiki/index/term_expansion_queue.csv`
- `wiki/index/term_external_edges.csv`
- `wiki/index/high_value_relations.csv`
- `wiki/index/relation_research_queue.csv`

## Agentic 日常流程

1. 新增或更新 `data/raw/wechat/YYYY-MM-DD.md`。
2. 更新 `data/raw/wechat/ingest_manifest.csv`。
3. 维护 `data/processed/primitives.csv`（只保留名词原语）。
4. 同步更新 `primitive_occurrences.csv` 与 `primitive_hyperedges.csv`。
5. 同步更新 `wiki/index/terms.csv`、`wiki/index/term_aliases.csv`、`wiki/index/term_edges.csv`。
6. 维护高价值关系表：`wiki/index/high_value_relations.csv`（收购/创始人/开源/产品归属）。
6. 仅在必要时补充 `wiki/entities/*.md`（不全量预建）。

## 约束

- 全程客观、原子化、可追溯。
- 优先第一手链接；去除社媒转述噪声。
- 默认不新增本地构建脚本；直接在 agentic 编辑中维护结果。
- 数据层索引 CSV 不引入 `status` 字段与候选状态门（如 `candidate/verified/in_progress`）。
- 不确定性留在对话与日志（`task_plan.md`、`findings.md`、`progress.md`），不写入核心索引表。
- 详细规则以 `AGENTS.md` 为准。
