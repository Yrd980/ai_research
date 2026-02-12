# AI Research Workspace

面向每日 "AI 早报" 的 agentic 维护仓库。

## 目标

- 主目标：抽取不可再分名词原语。
- 次目标：构建无时间语义的全局名词图谱（节点/边/别名）。

## 分层边界

- 日报层（event stream）：记录每日输入与时序上下文。
- wiki 层（global graph）：累计名词节点与关联，不复刻日报事件。

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

## Agentic 日常流程

1. 新增或更新 `data/raw/wechat/YYYY-MM-DD.md`。
2. 更新 `data/raw/wechat/ingest_manifest.csv`。
3. 维护 `data/processed/primitives.csv`（只保留名词原语）。
4. 同步更新 `primitive_occurrences.csv` 与 `primitive_hyperedges.csv`。
5. 同步更新 `wiki/index/terms.csv`、`wiki/index/term_aliases.csv`、`wiki/index/term_edges.csv`。
6. 仅在必要时补充 `wiki/entities/*.md`（不全量预建）。

## 约束

- 全程客观、原子化、可追溯。
- 优先第一手链接；去除社媒转述噪声。
- 默认不新增本地构建脚本；直接在 agentic 编辑中维护结果。
- 详细规则以 `AGENTS.md` 为准。
