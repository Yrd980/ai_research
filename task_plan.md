# Task Plan: 橘鸦 AI 早报倒序研究（2/11 起倒推几十天）

## Goal
定位公众号与对应早报内容，连续倒推几十天抽取公司/产品/投融资/创始人信息，并构建可持续更新的分析网络框架。

## Current Phase
Phase 8

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
- [x] 固化项目协作规范（AGENTS.md）
- **Status:** complete

### Phase 7: Objective Wiki + World Model v1
- [x] 建立零猜测 Wiki 层（verified/pending 分流）
- [x] 将 2/11→2/09 回填为证据驱动事实库
- [x] 输出第一性原理递归框架 v1
- **Status:** complete

### Phase 8: GitHub → 飞书自动同步落地
- [x] 设计并创建同步配置模板（Markdown/CSV 目标映射）
- [x] 实现统一同步脚本（Docx + Bitable）
- [x] 新增 GitHub Actions 自动触发与手动触发
- [x] 输出配置文档与本地 dry-run 验证步骤
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 先确认公众号与文章可抓取性，再做深度分析 | 避免在数据不可得时做无效建模 |
| 采用倒序（2/11→2/10）并强制按日期引用 | 符合用户“反向传播”研究方式 |
| 将任务扩展为“2/11 起倒推几十天” | 用户明确希望形成长期研究网络 |
| 明确保留 `task_plan.md`/`findings.md`/`progress.md` | 这是 planning-with-files 的演化记忆主链 |
| 采用“零猜测 Wiki”替代“可信度打分” | 用户要求 100% 准确：无原始证据不入主库 |
| 推广分发采用“GitHub 为源，飞书为发布页” | 满足用户“不建网站、直接给飞书链接”的目标 |
| 导航信息通过同步时动态注入（`sync_header`）实现 | 保持源 Markdown 干净，同时让对外文档具备运营友好首屏 |

## Errors Encountered
| Error | Resolution |
|-------|------------|
| `web.open` 无法直接打开 `mp.weixin.qq.com` 文章页面 | 改用 shell 抓取与第三方可访问源 |
| `r.jina.ai` 代理抓取微信短链连续超时（30s） | 不再重复同路径，改搜狗微信索引 + B 站同日交叉 |
| B 站公开视频搜索 API 返回风控页面（captcha） | 停止直接 API 枚举，改用搜索索引与单页抓取 |
| B 站空间 API 返回 `-799/-403`（频率限制/权限不足） | 不再依赖空间 API，改用按日期搜索索引逐条回填 |
| `rg -E '...'` 在当前环境被解释为编码参数并报错 `unknown encoding` | 后续改用 `rg` 基础匹配或 `grep -E` 管道，不重复该命令格式 |
| 飞书 Docx API 返回 `99991672` (`Access denied`) | 确认应用缺失 `docx:document`/`docx:document:readonly` scope，需先在飞书开放平台开通权限 |
| 飞书 Bitable 字段创建接口返回 `91403 Forbidden` | 当前应用对目标表缺少结构编辑权限；需手动授予权限或先手工建好字段 |
| 飞书 Bitable 记录写入接口 `batch_create` 返回 `91403 Forbidden` | 当前应用对目标表缺少写入权限（非字段映射问题）；需先授权可写 |
| 飞书 Docx 写入接口返回 `1770032 forBidden` | 文档当前对应用仅可读不可写；需给应用文档编辑权限后重试 |
| 同 app/token 对“新建文档”写入成功，而目标文档仍 `1770032` | 证明 API 与 scope 正常，问题收敛为特定目标文档授权上下文 |
| Docx 分批写入后文档显示顺序异常（导航头不在首屏） | 修复为递增 `index` 写入，避免每批都插入顶部造成逆序错位 |
| `git add -A` 在当前环境被策略拦截（blocked by policy） | 改为显式逐文件 `git add <path>`，避免重复执行被拦截命令 |
