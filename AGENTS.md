# AGENTS.md

## Scope

This file applies to the entire repository.

## Project Purpose

Build a long-horizon AI research knowledge base from daily "AI 早报" sources, with:
- raw-source preservation,
- structured event extraction,
- world-model style synthesis (internal relationships, not noise).

## Non-Negotiable Files

The following files are the `planning-with-files` evolution memory and must be preserved:
- `task_plan.md`
- `findings.md`
- `progress.md`

Do not delete these three files during cleanup/refactor.

## Working Structure

- Raw ingest: `data/raw/wechat/`
- Objective wiki: `data/wiki/`
- Structured data: `data/processed/`
- Date/link indexes: `data/indexes/`
- Templates: `data/templates/`
- Analysis outputs: `docs/analysis/`
- Method/framework docs: `docs/framework/`
- Uncertainty/backlog: `docs/reports/`

## Default Workflow For New Daily Input

1. Ingest raw text into `data/raw/wechat/YYYY-MM-DD.md`.
2. Update `data/raw/wechat/ingest_manifest.csv`.
3. Extract structured events into `data/processed/juya_network_seed.csv`.
4. Sync objective facts to `data/wiki/` (verified facts + pending verification split).
5. Update term lexicon (`data/processed/term_lexicon_*.csv`) with no missing named entities.
6. Refresh analysis artifacts in `docs/analysis/` using current evidence only.
7. Update `task_plan.md`, `findings.md`, and `progress.md`.

## Research Principles

- Prioritize first-hand/primary evidence over reposted summaries.
- Separate facts from rumors/tests/previews.
- Preserve source links for every extracted event.
- Focus on structural relationships (tech layer, protocol layer, distribution layer, capital layer, organization layer).
- Avoid premature forecasting unless explicitly requested.
- For objective wiki: no evidence => no fact entry.
