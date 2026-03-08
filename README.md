# AI Research Workspace

围绕每日“AI 早报”维护的名词化知识库仓库。

## 仓库目标

- 主目标：从每日输入中抽取不可再分名词原语。
- 次目标：维护一个与日历解耦的全局名词图谱，支持查询、关联与后续扩展。

## 固定入口

- 用户手动写入 `data/raw/wechat/YYYY-MM-DD.md`。
- 这是当前唯一固定工作流；其余派生文件都由 Codex 直接维护。

## 当前架构

### 1. 原文层（source of truth）

- `data/raw/wechat/YYYY-MM-DD.md`：保存每日原文，必须全文保真。
- `data/raw/wechat/ingest_manifest.csv`：登记每日输入，按日期倒序维护。

### 2. 提取层（event-derived）

- `data/processed/primitives.csv`：原语主表。
- `data/processed/primitive_occurrences.csv`：原语在每日条目中的出现。
- `data/processed/primitive_hyperedges.csv`：同条目原语共现的 N 元关系。

### 3. Wiki 层（time-agnostic noun graph）

- `wiki/index/terms.csv`：全局名词节点。
- `wiki/index/term_aliases.csv`：别名归一。
- `wiki/index/term_edges.csv`：名词之间的核心关联。
- `wiki/index/term_expansion_queue.csv`、`wiki/index/term_external_edges.csv`：外部扩展层。
- `wiki/index/high_value_relations.csv`、`wiki/index/relation_research_queue.csv`：高价值关系层。
- `wiki/entities/`：按需创建的长期实体说明页。

仓库默认不再保留额外的模板层、机器契约层或独立可视化层；只保留主链需要的最小结构。

## 维护边界

### 核心必维护

- `data/raw/wechat/ingest_manifest.csv`
- `data/processed/primitives.csv`
- `data/processed/primitive_occurrences.csv`
- `data/processed/primitive_hyperedges.csv`
- `wiki/index/terms.csv`
- `wiki/index/term_edges.csv`
- `wiki/index/high_value_relations.csv`

### 按需维护
- `wiki/index/term_aliases.csv`
- `wiki/index/term_expansion_queue.csv`
- `wiki/index/term_external_edges.csv`
- `wiki/index/relation_research_queue.csv`
- `wiki/entities/*.md`

## 数据对齐要求

- `ingest_manifest.csv` 与 `data/raw/wechat/*.md` 必须一一对应，并保持日期倒序。
- 原文中每个带 `#序号` 的日报条目，原则上都应在 `primitive_occurrences.csv` 中留下至少一条对应记录。
- `primitives.csv` 应当是 `primitive_occurrences.csv` 的唯一原语投影，不保留无 occurrence 支撑的孤立行。
- `primitive_hyperedges.csv` 应当由同一 `(date, item_no)` 下的 occurrence 自动推导；少于 2 个唯一原语则不生成。
- `terms.csv` 对所有 primitives 必须有同名 term，且类型一致。
- `term_edges.csv` 至少覆盖日报 hyperedge 产生的全部 pair，且共现计数不能低于日报主链。
- `high_value_relations.csv` 可以扩展到日报之外，但其 term 引用必须能回到 `terms.csv`。

## 推荐工作流

### Manual-first

1. 新增或更新 `data/raw/wechat/YYYY-MM-DD.md`。
2. 更新 `data/raw/wechat/ingest_manifest.csv`。
3. 由 Codex 在同一轮会话内直接更新 `data/processed/*.csv`。
4. 再直接回写 `wiki/index/terms.csv`、`wiki/index/term_edges.csv` 与必要的高价值关系。
5. 只有在确有长期价值时，才补充 alias、external edge、research queue 与实体页。

## 原文保真规则

- 原文中的链接、数字、机制名、基准值、限制条件必须保留。
- 若仅有部分正文，必须在 `ingest_manifest.csv` 中设置 `is_full_text=false` 与 `needs_backfill=true`。
- 不在原文文件中写入推断性字段。

## 维护约束

- 数据层索引 CSV 不引入 `status` 字段。
- 不确定性只留在 `task_plan.md`、`findings.md`、`progress.md`。
- 优先一手来源，不把社媒转述当主证据。
- `wiki/` 保持为全局名词层，不复制日报事件叙事。
- 不再保留机器 JSON 入参/回执契约层；派生表直接由 Codex 修改。
- 详细规则以 `AGENTS.md` 为准。
