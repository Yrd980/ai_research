# AI Research Workspace

## Directory Layout

- `data/raw/wechat/`：公众号原文归档（按日期）
- `data/processed/`：原语主表 + 出现记录 + 超边
- `data/templates/`：原语模板
- `wiki/`：independent objective extension wiki（entity pages + indexes）
- `task_plan.md` / `findings.md` / `progress.md`：skills `planning-with-files` 的长期演化记录（必须保留）
- `AGENTS.md`：仓库级协作规范与执行流程

## Current Canonical Files

- Raw ingest manifest: `data/raw/wechat/ingest_manifest.csv`
- Primitive table: `data/processed/primitives.csv`
- Primitive occurrences (1元): `data/processed/primitive_occurrences.csv`
- Primitive hyperedges (N元): `data/processed/primitive_hyperedges.csv`
- Primitive template: `data/templates/primitives_template.csv`
- Occurrences template: `data/templates/primitive_occurrences_template.csv`
- Hyperedges template: `data/templates/primitive_hyperedges_template.csv`
- Wiki registry: `wiki/index/entity_registry.csv`
- Wiki relations: `wiki/index/relations.csv`
- Startup profiles: `wiki/index/startup_profiles.csv`

## Rebuild Command

```bash
python3 scripts/build_primitive_cooccurrence.py
```
