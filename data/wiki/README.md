# Objective Wiki Layer (Zero-Guess Mode)

This folder stores only verifiable facts derived from ingested daily reports.

## Rules

- No inference without evidence.
- No “confidence score”; entries are either:
  - included in verified wiki tables, or
  - moved to `pending_verification.csv`.
- Every verified fact must link to `evidence_id` in `evidence_registry.csv`.

## Files

- `evidence_registry.csv`: source ledger and verification basis.
- `fact_wiki.csv`: atomic facts (who/when/did-what/evidence).
- `company_wiki.csv`: company-level objective profile (verified only).
- `product_model_wiki.csv`: product/model objective records.
- `funding_ma_wiki.csv`: funding and M&A facts (verified only).
- `person_wiki.csv`: person relationships with explicit evidence.
- `pending_verification.csv`: unresolved facts waiting for official sources.

## Current Snapshot (2026-02-11 → 2026-02-09)

- Verified facts: 34
- Pending verification items: 7
- Companies in objective wiki: 25

