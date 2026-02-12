# Wiki Layer

独立于日报抽取链路的客观知识层。

## 作用

- 承接日报原语，形成可查询的断言索引。
- 不反向污染 `data/processed/*`。

## 关键索引

- `wiki/index/assertions.csv`：唯一事实源（authoritative）
- `wiki/index/assertions_candidates.csv`：日报筛出的候选断言
- `wiki/index/assertions_review_queue.csv`：候选审阅排序队列
- `wiki/index/entity_registry.csv`：实体注册表
- `wiki/index/relations.csv`：派生关系视图
- `wiki/index/history_timeline.csv`：派生时间线视图

## 实体页

- `wiki/entities/company/`
- `wiki/entities/person/`
- `wiki/entities/concept/`

实体页用于客观介绍，不作为事实主账本。

## Agentic 维护顺序

1. 先更新 `assertions_candidates.csv` 与 `assertions_review_queue.csv`。
2. 人工审核后写入 `assertions.csv`。
3. 在同一次编辑中同步 `relations.csv` 与 `history_timeline.csv`。
4. 必要时补充实体页与 `Sources`。

## 写作规则

- `wiki/index/objective_writing_policy.md`
- `wiki/index/primary_source_filter.md`
