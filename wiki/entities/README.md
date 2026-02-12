# Entities Layer

Entity pages are reference cards, not the source-of-truth fact table.

## Buckets

- `wiki/entities/company/`
- `wiki/entities/person/`
- `wiki/entities/concept/`

## Editing Rules

1. Keep `Objective Card` fields factual and minimal.
2. Keep `Objective Intro` to one neutral sentence or `TBD`.
3. Put verifiable links in `Sources`.
4. Do not move facts directly from entity pages into downstream views.

## Source of Truth Boundary

- Facts: `wiki/index/assertions.csv`
- Derived views: `wiki/index/relations.csv`, `wiki/index/history_timeline.csv`
- Entity pages: narrative support only.
