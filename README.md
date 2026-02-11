# AI Research Workspace

## Directory Layout

- `data/raw/wechat/`：公众号原文归档（按日期）
- `data/processed/`：结构化事件、词典、观察清单
- `data/indexes/`：日期与来源索引
- `data/templates/`：后续滚动采集模板
- `docs/analysis/`：世界模型、关系网、去噪事实簇
- `docs/framework/`：方法论与研究框架
- `docs/reports/`：不确定项与待补字段
- `task_plan.md` / `findings.md` / `progress.md`：skills `planning-with-files` 的长期演化记录（必须保留）
- `AGENTS.md`：仓库级协作规范与执行流程

## Current Canonical Files

- Raw ingest manifest: `data/raw/wechat/ingest_manifest.csv`
- Event table: `data/processed/juya_network_seed.csv`
- Term lexicon: `data/processed/term_lexicon_0211_0209.csv`
- World model (v0): `docs/analysis/world_model_v0_0211_0209.md`
- Entity network (v0): `docs/analysis/entity_relation_network_v0_0211_0209.md`
- Denoised clusters (v0): `docs/analysis/denoised_fact_clusters_v0_0211_0209.md`
- Framework: `docs/framework/analysis_network.md`
- Utilization strategy: `docs/framework/utilization_strategy.md`
- Uncertainties: `docs/reports/uncertainties.md`
