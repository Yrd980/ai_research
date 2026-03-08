# AGENTS.md

## Scope

本文件适用于整个仓库。

## Project Purpose

- 主目标：从每日 “AI 早报” 原文中抽取不可再分名词原语。
- 次目标：维护一个与时间解耦的全局名词图谱，支持查询与关联。

## Fixed Entry

- 用户手动写入 `data/raw/wechat/YYYY-MM-DD.md`。
- 这是当前唯一固定输入入口。
- 其余派生文件由 Codex 在同轮维护中直接更新。

## Non-Negotiable Files

以下三份文件是规划记忆，必须保留：
- `task_plan.md`
- `findings.md`
- `progress.md`

## Working Structure

- 原文层：`data/raw/wechat/`
- 提取层：`data/processed/`
- Wiki 图层：`wiki/index/`

## Raw Ingest Rules

- `data/raw/wechat/YYYY-MM-DD.md` 必须保留完整原文。
- 不得用摘要替代原文。
- 必须保留原始链接、数字指标、机制名称、限制条件与 caveat。
- 若正文不完整，必须在 `data/raw/wechat/ingest_manifest.csv` 中设置：
  - `is_full_text=false`
  - `needs_backfill=true`

## Default Workflow

1. 手动写入或更新 `data/raw/wechat/YYYY-MM-DD.md`。
2. 更新 `data/raw/wechat/ingest_manifest.csv`。
3. 维护 `data/processed/primitives.csv`。
4. 维护 `data/processed/primitive_occurrences.csv`。
5. 维护 `data/processed/primitive_hyperedges.csv`。
6. 维护 `wiki/index/terms.csv`、`wiki/index/term_edges.csv`。
7. 按需维护 `wiki/index/high_value_relations.csv`。
8. 仅在必要时补充：
   - `wiki/index/term_aliases.csv`
   - `wiki/index/term_expansion_queue.csv`
   - `wiki/index/term_external_edges.csv`
   - `wiki/index/relation_research_queue.csv`
   - `wiki/entities/*.md`
9. 更新 `task_plan.md`、`findings.md`、`progress.md`。

## Data Rules

- 核心索引 CSV 不引入 `status` 字段。
- 不确定性放在规划与日志文件中，不写入核心索引。
- `wiki/` 是全局名词图层，不复制日报事件叙事。
- 保持输出原子、客观、可追溯。

## Alignment Requirements

- `data/raw/wechat/ingest_manifest.csv` 必须与 `data/raw/wechat/*.md` 一一对应，且按日期倒序。
- 每个原文中带 `#序号` 的日报条目，原则上都应在 `data/processed/primitive_occurrences.csv` 中至少对应 1 行记录。
- `data/processed/primitives.csv` 必须严格由 `primitive_occurrences.csv` 投影得到；不保留没有 occurrence 支撑的原语行。
- `data/processed/primitive_hyperedges.csv` 必须严格由 occurrence 分组派生；仅当同一 `(date,item_no)` 下存在至少 2 个唯一原语时生成。
- `wiki/index/terms.csv` 对已进入 `primitives.csv` 的原语必须存在同名 term，且 `term_type` 对齐。
- `wiki/index/term_edges.csv` 对日报共现产生的 pair 不得缺失或低于日报共现次数；外部扩展可增补，但不能削弱日报主链。
- `wiki/index/high_value_relations.csv` 允许超出日报主链，但 `subject_term_id` / `object_term_id` 必须能在 `terms.csv` 中解析。

## Research Rules

- 优先第一手来源。
- 不把社媒转述当作主证据。
- 默认不新增本地构建脚本。
- 若无长期价值，不新增额外自动化契约层。
- 若未接入主链，不保留独立模板层或可视化快照层。
