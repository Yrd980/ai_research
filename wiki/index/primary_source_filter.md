# Primary Source Filter

用于从日报条目筛选可进入 wiki 候选层的来源。

## 目标

- 只保留一手来源（primary）。
- 降低社媒转述、聚合转载、话题帖噪声。

## 入选规则

1. `source_url` 来自当条日报原始链接列表。
2. 链接可稳定定位到原始发布方内容。
3. `quote_span` 来自同一条目正文，且为最小必要片段。
4. 一行候选只对应一个原子事实。

## 排除规则

以下域名默认排除（除非后续明确调整）：

- `x.com`, `twitter.com`
- `mp.weixin.qq.com`
- `linux.do`
- `zhihu.com`, `reddit.com`
- `bilibili.com`, `youtube.com`

## Agentic 执行约定

- 在更新日报原文后，同步维护：
  - `wiki/index/assertions_candidates.csv`
  - `wiki/index/assertions_review_queue.csv`
- 再由人工将通过项晋升到 `wiki/index/assertions.csv`。
