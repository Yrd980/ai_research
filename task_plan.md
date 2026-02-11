# Task Plan: 橘鸦 AI 早报倒序研究（2/11 起倒推几十天）

## Goal
定位公众号与对应早报内容，连续倒推几十天抽取公司/产品/投融资/创始人信息，并构建可持续更新的分析网络框架。

## Current Phase
Phase 6

## Phases

### Phase 1: Requirements & Discovery
- [x] 理解用户目标与范围（由 2 天扩展到几十天）
- [x] 激活 planning-with-files 工作流
- [x] 完成公众号与可持续数据源可访问性确认
- **Status:** complete

### Phase 2: Long-Horizon Data Collection
- [x] 建立“日期索引→文章链接”列表（至少数十天）
- [x] 优先抓取最近 10 天做样本验证
- [x] 记录每篇是否可直接抓取或需用户粘贴
- **Status:** complete

### Phase 3: Entity Extraction
- [x] 从文章中提取实体（公司、产品、创始人、投资方、金额）
- [x] 对每条信息标注来源、日期、置信度
- [x] 记录缺失字段与待补证据
- **Status:** complete

### Phase 4: Analysis Network Build
- [x] 设计“日报→实体→关系→趋势”网络结构
- [x] 输出初版节点类型与关系类型
- [x] 形成可持续迭代的补全机制
- **Status:** complete

### Phase 5: Verification & Delivery
- [x] 核对日期与来源链接一致性
- [x] 交付结构化结果与后续滚动模板
- [x] 标注全部不确定项与待补字段
- **Status:** complete

### Phase 6: Continuous Research Loop
- [x] 严格按倒序继续接收并结构化新日期正文
- [x] 每轮补齐公司/产品/融资/创始人缺口字段
- [x] 每轮更新覆盖报告、不确定项与趋势洞察
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 先确认公众号与文章可抓取性，再做深度分析 | 避免在数据不可得时做无效建模 |
| 采用倒序（2/11→2/10）并强制按日期引用 | 符合用户“反向传播”研究方式 |
| 将任务扩展为“2/11 起倒推几十天” | 用户明确希望形成长期研究网络 |

## Errors Encountered
| Error | Resolution |
|-------|------------|
| `web.open` 无法直接打开 `mp.weixin.qq.com` 文章页面 | 改用 shell 抓取与第三方可访问源 |
| `r.jina.ai` 代理抓取微信短链连续超时（30s） | 不再重复同路径，改搜狗微信索引 + B 站同日交叉 |
| B 站公开视频搜索 API 返回风控页面（captcha） | 停止直接 API 枚举，改用搜索索引与单页抓取 |
| B 站空间 API 返回 `-799/-403`（频率限制/权限不足） | 不再依赖空间 API，改用按日期搜索索引逐条回填 |
