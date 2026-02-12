# AGENTS.md

## Scope

This file applies to the entire repository.

## Project Purpose

Build a primitive-only knowledge base from daily "AI 早报" sources.

Primary output target:
- extract irreducible noun primitives from daily input.

Secondary wiki extension target:
- derive primary-only assertion candidates from daily items for manual promotion into wiki assertions.

## Non-Negotiable Files

The following files are the `planning-with-files` evolution memory and must be preserved:
- `task_plan.md`
- `findings.md`
- `progress.md`

Do not delete these three files during cleanup/refactor.

## Working Structure

- Raw ingest: `data/raw/wechat/`
- Primitive table: `data/processed/primitives.csv`
- Primitive occurrences: `data/processed/primitive_occurrences.csv`
- Primitive hyperedges: `data/processed/primitive_hyperedges.csv`
- Templates: `data/templates/`
- Extension wiki (independent): `wiki/`

## Default Workflow For New Daily Input

1. Ingest raw text into `data/raw/wechat/YYYY-MM-DD.md`.
2. Update `data/raw/wechat/ingest_manifest.csv`.
3. Extract irreducible noun primitives into `data/processed/primitives.csv`.
4. Build primitive occurrences (`1元`) and co-occurrence hyperedges (`N元`) from raw daily items.
5. Keep no-verb graph structure only; no event reasoning layer.
6. Build wiki assertion candidates from daily items with primary-link filtering only.
7. Manually review candidates, then maintain accepted facts in `wiki/index/assertions.csv` (single source of truth).
8. Rebuild wiki views (`relations`/`history_timeline`) from assertions.
9. Optionally extend objective entity pages in `wiki/` (company/person/concept + indexes).
10. Update `task_plan.md`, `findings.md`, and `progress.md`.

## Research Principles

- Prioritize first-hand/primary evidence over reposted summaries.
- No `evidence_level` scoring; enforce hard include/exclude rules only.
- Preserve source date scope for every primitive.
- No funding/forecast/mechanism fields in core data.
- Keep output minimal and atomic.
- Keep `wiki/` physically independent from daily extraction files.
- Daily pipeline can be reverse-chronological; `wiki/` is full-history and query-oriented.
- In wiki layer, `assertions.csv` is authoritative; other index tables are derived views.
- Prefer one-step agentic edits for one-off tasks; promote to scripts/SOP only after repeated use (about 3-5 times).
