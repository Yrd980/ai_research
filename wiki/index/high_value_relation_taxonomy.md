# High Value Relation Taxonomy

This file defines normalized relation types for `wiki/index/high_value_relations.csv`.

## Principles

- Keep relation names semantic and stable.
- Prefer directional relations with clear subject/object roles.
- Keep daily-event relations and long-lived structural relations in the same schema, differentiated by `source_type` and `event_date`.
- Keep data layer stateless: do not add workflow state columns such as `status`.
- Handle uncertain candidates in agent conversation/logs, not in `high_value_relations.csv`.

## Normalized Types

- `acquired`
  - Meaning: buyer acquired target.
  - Direction: buyer -> target.
  - Event date: required for `daily_primary` when date can be inferred.

- `owned_by`
  - Meaning: subject is owned/controlled by object (equity/control relation).
  - Direction: company -> owner.
  - Event date: optional for static ownership snapshots.

- `founded_by`
  - Meaning: organization was founded or co-founded by person.
  - Direction: organization -> founder.

- `owns_product`
  - Meaning: organization owns or operates product surface.
  - Direction: organization -> product.

- `develops_model`
  - Meaning: organization develops or releases model family.
  - Direction: organization -> model.

- `maintains_project`
  - Meaning: organization/community maintains project or product line.
  - Direction: maintainer -> project.

- `open_source_repository`
  - Meaning: organization publishes or maintains an open-source repository.
  - Direction: organization -> repository.

## Migration Notes (2026-02-13)

- `open_source_project` rows with `object_term` prefixed by `GH Repo:` are normalized to `open_source_repository`.
- `maintains` is normalized to `maintains_project`.
- Legacy relation names should not be reintroduced.
