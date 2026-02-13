# Wiki Layer

独立于日报抽取链路的全局名词图层（time-agnostic）。

## 作用

- 承接日报原语，形成可查询的名词节点与关联边。
- 作为过去到现在累计的总和，不维护按日事件语义。
- 不反向污染 `data/processed/*`。

## 核心索引

- `wiki/index/terms.csv`：名词节点
- `wiki/index/term_aliases.csv`：别名归一
- `wiki/index/term_edges.csv`：名词关联边（权重）

## 非核心

- `term_occurrences` 属于日报事件流中间层，不作为 wiki 核心索引。

## 实体页策略

- `wiki/entities/` 仅作为按需补充说明页。
- 默认不预建 company/person/concept 全量文件。
- 只有在需要长期注释某个重点名词时才新增页面。


## 多-Agent扩展层

- `wiki/index/term_expansion_queue.csv`：扩展任务队列（按 agent lane 分工）。
- `wiki/index/term_external_edges.csv`：外部一手来源扩展边（官方链接，待审核/可回写）。

执行原则：
- 日报主链不变；扩展层只增补全局图。
- 优先官方站点、官方文档、官方公告。
- 审核通过后可将外部边回写到 `term_edges.csv`。


## 高价值关系层

- `wiki/index/high_value_relations.csv`：高价值关系主表（如 `acquired` / `owned_by` / `founded_by` / `owns_product` / `develops_model` / `maintains_project` / `open_source_repository`）。
- `wiki/index/high_value_relation_taxonomy.md`：关系类型字典与归一化规则。
- `wiki/index/relation_research_queue.csv`：关系研究队列（多-agent lane）。

质量规则：
- 主图只保留高质量实体与关系。
- 低质量噪声词不进入主图，不作为可视化默认节点。
- 索引 CSV 不使用 `status` 字段；状态判断留在对话与项目日志层。
