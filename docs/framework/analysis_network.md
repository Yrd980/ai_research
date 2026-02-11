# 橘鸦 AI 早报「倒序分析网络」v1

## 1) 执行原则（严格倒序）

- 固定顺序：`2026-02-11 -> 2026-02-10 -> ...`
- 不允许跳日补录；只在当前日期完成后进入下一天。
- 每日输出都带 `date`、`issue_seq`（从 1 开始递增）和 `source_url`。

## 2) 数据模型（可扩展）

### 节点类型
- `Issue`：某天早报（例：2026-02-10）
- `Company`：公司实体（OpenAI、Mistral）
- `Product/Model`：产品与模型（Deep Research、Mistral Saba）
- `Project`：开源项目（AnythingLLM）
- `Person`：创始人/核心人物
- `FundingEvent`：融资事件（金额、轮次、投资方）

### 关系类型
- `MENTIONED_IN`：实体被某期早报提及
- `RELEASED`：公司发布产品/模型
- `RAISED`：公司发生融资事件
- `FOUNDED_BY`：公司与创始人关系
- `PARTNERED_WITH`：合作或合资关系

## 3) 当前落地文件

- 倒序索引：`data/indexes/juya_daily_index.md`（已覆盖 30 天：2026-02-11 至 2026-01-13）
- 实体种子：`data/processed/juya_network_seed.csv`（优先录入 2/11 与 2/10）

## 4) 每日处理模板（从下一天开始复用）

1. 读取当天链接（来自 `data/indexes/juya_daily_index.md`）。
2. 抽取 `公司/产品/投融资/创始人` 四类实体。
3. 记录到 `data/processed/juya_network_seed.csv`（或后续扩展表）。
4. 若创始人缺失，标记 `Unknown` 并登记待补来源。
5. 当天完成后再处理下一天（严格倒序）。

## 5) 预测机思路（你说的“反向传播”）

- 将 `Issue(t)` 的事件投影到实体节点，累积实体“热度/频次/融资活跃度/发布节奏”。
- 倒序累积后可形成：
  - `短期趋势`：最近 7 天反复出现的产品线
  - `资本信号`：融资事件密度与金额变化
  - `组织动作`：合作/合资频次变化
- 进一步可做“明日候选事件”打分：
  - 分数 = `近期提及频次` + `跨平台同步强度` + `连续发布间隔特征`

