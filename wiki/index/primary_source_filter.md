# Primary Source Filter (AI Daily Only)

This rule applies when generating wiki assertion candidates from `data/raw/wechat/*.md`.

## Inclusion Rules

1. Keep only records where `source_type = primary`.
2. `source_url` must come from the item's original link list.
3. `quote_span` must be a minimal text span copied from the same item block.
4. One row must represent one atomic fact only.

## Exclusion Rules

Drop rows if the selected URL is from social/media repost domains:
- `x.com`, `twitter.com`
- `mp.weixin.qq.com`
- `linux.do`
- `zhihu.com`, `reddit.com`
- `bilibili.com`, `youtube.com`

## Current Workflow

1. Daily ingest stays in `data/raw/wechat/` unchanged.
2. Primitive extraction stays in `data/processed/` unchanged.
3. Build candidates via:

```bash
python3 scripts/build_wiki_assertion_candidates.py
```

4. Review `wiki/index/assertions_candidates.csv` manually before moving rows into `wiki/index/assertions.csv`.

No confidence/evidence scoring is used.
