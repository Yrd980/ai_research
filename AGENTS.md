# AGENTS.md

## Scope

This file applies to the entire repository.

## Project Purpose

Build a primitive-only knowledge base from daily "AI 早报" sources.

Primary output target:
- extract irreducible noun primitives from daily input.

Secondary wiki extension target:
- maintain a noun-only global graph for query and association.

## Non-Negotiable Files

The following files are the `planning-with-files` evolution memory and must be preserved:
- `task_plan.md`
- `findings.md`
- `progress.md`

Do not delete these three files during cleanup/refactor.

## Working Structure

- Raw ingest (event stream): `data/raw/wechat/`
- Primitive tables (event-derived): `data/processed/primitives.csv`, `data/processed/primitive_occurrences.csv`, `data/processed/primitive_hyperedges.csv`
- Templates: `data/templates/`
- Wiki global graph (time-agnostic): `wiki/index/`

## Default Workflow For New Daily Input

1. Ingest raw text into `data/raw/wechat/YYYY-MM-DD.md`.
2. Update `data/raw/wechat/ingest_manifest.csv`.
3. Extract irreducible noun primitives into `data/processed/primitives.csv`.
4. Build primitive occurrences (`1元`) and co-occurrence hyperedges (`N元`) from raw daily items.
5. Keep no-verb graph structure only; no assertion/event reasoning layer.
6. Sync wiki global graph indexes (time-agnostic core):
   - `wiki/index/terms.csv`
   - `wiki/index/term_aliases.csv`
   - `wiki/index/term_edges.csv`
   - `wiki/index/term_external_edges.csv` (optional expansion layer)
   - `wiki/index/high_value_relations.csv` (high-quality relation layer)
7. Keep entity pages in `wiki/entities/` as on-demand notes only (do not pre-create in bulk).
8. (Optional) Run multi-agent expansion queue and append external edges from official sources.
9. Maintain `high_value_relations.csv` for M&A/founder/open-source/product ownership.
10. Update `task_plan.md`, `findings.md`, and `progress.md`.

## Research Principles

- Prioritize first-hand/primary evidence over reposted summaries.
- No `evidence_level` scoring; enforce hard include/exclude rules only.
- No funding/forecast/mechanism fields in core data.
- Keep output minimal and atomic.
- Keep `wiki/` physically independent from daily extraction files.
- Daily pipeline is an event stream; wiki is a global noun graph.
- Wiki is noun index only, not daily assertion duplication.
- Prefer one-step agentic edits and keep pipeline outputs updated directly.
- Do not add local build scripts by default.
