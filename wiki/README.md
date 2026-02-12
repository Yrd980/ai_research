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
