# Wiki Knowledge Extension

This folder is an objective extension layer outside the daily-report pipeline.

## Purpose

- Extend nouns from daily primitives into broader entity knowledge cards.
- Keep this layer independent from `data/processed/*` daily extraction outputs.
- Support expansion links (company, founder, product/model, techniques) without polluting daily edges.

## Structure

- `wiki/entities/company/`: one file per company.
- `wiki/entities/person/`: one file per person/founder.
- `wiki/entities/concept/`: one file per extended noun (model/product/tech/etc.).
- `wiki/index/assertions.csv`: single source of truth for objective facts.
- `wiki/index/entity_registry.csv`: all entities index.
- `wiki/index/relations.csv`: derived relation view from assertions.
- `wiki/index/history_timeline.csv`: derived timeline view from assertions.
- `wiki/index/startup_profiles.csv`: startup introduction index for unfamiliar companies.

## Rules

- Objective only, source-backed updates only.
- Daily extraction files remain unchanged by wiki edits.
- Prefer one-entity-one-file + CSV indexes for both readability and computability.
- Follow `wiki/index/objective_writing_policy.md` for intro and wording standards.
- Edit `assertions.csv` first, then rebuild views via `python3 scripts/build_wiki_views.py`.
