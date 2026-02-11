# Findings & Decisions

## Requirements
- 用户希望定位截图中的公众号，并获取其 AI 早报内容（至少 2026-02-11 与 2026-02-10）。
- 研究维度：公司、产品、被投信息、创始人信息等。
- 方法偏好：按“今天到昨天”倒序，逐步完善成分析网络。
- 若公众号页面抓取失败，用户可提供复制文本继续。
- 用户新增要求：必须真实按日期顺序执行，从 2026-02-11 开始逐日倒推。
- 用户已提供 `2026-02-11` 与 `2026-02-10` 两天公众号正文（可直接高精度抽取）。

## Research Findings
- 待开始：先验证截图账号名与给定两篇微信链接可访问性。
- 公开搜索可定位到「橘鸦Juya」在 B 站的 AI 早报内容频道（侧证账号存在）。
- 通过网页工具直开两篇微信链接均失败（non-retryable error），需改用替代抓取方案（如 `curl` 抓取原始 HTML 或第三方镜像）。
- 通过 B 站检索可确认账号名为「橘鸦Juya」，频道描述与截图高度一致（“记录人类完蛋全过程”）。
- B 站检索结果显示该账号持续更新「AI 早报」系列，说明公众号内容可能有同步/改编分发路径，可用于交叉补全实体信息。
- 直接检索微信短链 ID（`ZWc2EsB4jcGbPeCf7gRZSA` / `gHmH90xZ-CuNuSyy2avAng`）未返回可直接复原原文的公开镜像结果。
- 检索到的“AI 早报”多为第三方聚合源（如新浪 AI 速递、DataPipe），可作事件交叉校验，但不等同于目标公众号原文。
- 通过 `r.jina.ai/http://mp.weixin.qq.com/s/...` 抓取两篇目标链接，均超时（30 秒）且无正文返回。
- 当前可行路线：搜集“日期-链接索引”与 B 站同日内容先行抽取，待用户补充微信原文后进行精确对齐。
- B 站视频检索结果可直接返回每期 `Intro` 结构化文本，包含逐条新闻标题与外链（X/GitHub/博客/论文）；
  这些字段可直接用于“公司/产品/开源项目/融资事件”抽取。
- 已验证该账号在 2026-01-03 仍有 AI 早报更新，说明可通过其发布时间序列向上追溯到 2026-02-11/02-10。
- 直接调用 B 站视频搜索 API（`x/web-interface/search/type`）返回风控错误页，当前环境无法稳定走官方 API。
- 新策略：继续使用搜索引擎可见索引页，逐条打开视频页抽取 `Intro` 与发布日期，实现按日期倒序回填。
- 已定位倒序起点并确认视频页可读（严格顺序）：
  - `2026-02-11`：https://www.bilibili.com/video/BV1jSA8eUEpq/
  - `2026-02-10`：https://www.bilibili.com/video/BV1gtA8e3E6B/
- `2026-02-11` 期已抽取到的核心条目（来自视频页 Intro）：
  - OpenAI 发布 `Deep Research`
  - 脑机相关研究（论文链接指向 OpenReview）
  - 私有化部署/开源工具：`AnythingLLM`（GitHub）
- `2026-02-10` 期已抽取到的核心条目：
  - OpenAI 与软银建立合资项目（`SB OpenAI Japan`）
  - Perplexity 推出 Deep Research
  - Mistral 发布轻量模型 `Mistral Saba`
  - 融资：`Helicone` 完成约 `7500 万美元` 融资
  - 语音产品：`Sesame` 与 Maya/Miles demo 相关进展
- 直接 `curl` B 站视频页可返回 HTML，但主体为“视频不见了/错误页”壳，难以稳定抽取作者与完整正文；
  因此当前可靠信息以“搜索索引 + web.open 提取的 Intro 文本”为主。
- 已确认账号主页 URL：`https://space.bilibili.com/285286947`（来自公开搜索索引）。
- 账号空间 API 在当前环境不可用：
  - `x/space/arc/search` 返回 `-799`（请求频繁）
  - `x/space/wbi/arc/search` 返回 `-403`（权限不足）
- 因此“几十天倒推”采用稳妥路径：按日期检索 `“我的 AI 实践：橘鸦 AI 早报 YYYY-MM-DD”` 并逐条抽取 Intro。
- 已完成首轮“几十天倒推”索引构建：从 `2026-02-11` 到 `2026-01-13` 共 `30` 天，均为严格倒序。
- 索引结果已落盘：`data/indexes/juya_daily_index.md`（包含每天对应 B 站 URL）。
- 已创建结构化产物：
  - `data/processed/juya_network_seed.csv`：2/11 与 2/10 的公司/产品/融资/创始人种子数据
  - `docs/framework/analysis_network.md`：可持续倒序分析网络（节点、关系、处理模板、预测思路）
- 创始人信息可核实补充（用于 2/10 种子数据）：
  - Perplexity：Aravind Srinivas、Denis Yarats、Johnny Ho、Andy Konwinski
  - Mistral AI：Arthur Mensch、Timothée Lacroix、Guillaume Lample
  - Helicone（来自其 docs 搜索索引）：Shashank Reddy、Sree Harsha
- 已基于你粘贴的原文完成两天高精度结构化：
  - `2026-02-11`：24 条全部入库
  - `2026-02-10`：10 条全部入库
  - 合计 `34/34` 条
- `data/processed/juya_network_seed.csv` 已扩展字段（增加 `item_no`）并按两天条目逐条写入。
- 新增覆盖报告 `docs/reports/juya_0211_0209_coverage.md`，明确字段完整度与待补创始人列表。
- 已继续按顺序完成 `2026-02-09`：
  - `2026-02-09`：5 条全部入库
  - 当前累计：`39/39` 条
- `2026-02-09` 新增关键信号：Qwen 3.5、Seedream 5.0、Meta Avocado 以“预发布/测试”形态集中出现。
- `docs/reports/juya_0211_0209_coverage.md` 已更新覆盖范围到 `2026-02-11 → 2026-02-09`。
- 进入“行研打样”阶段：从三天结构化事件中去重得到 `31` 个核心实体（公司/产品/平台混合）。
- 下一步将输出：实体主档（含初创标记、创始人、赛道）+ 全量名词索引（逐条不漏）。
- 已完成“水上→水下”打样报告：`docs/analysis/underwater_insights_0211_0209.md`
  - 输出了 5 条底层结构判断（入口控制、Agent 基建、多模态工程化、资本同频、预热窗口）
  - 给出未来 7~21 天可执行预测与验证方向
- 已完成初创/高势能观察清单：`data/processed/startup_watchlist_v1.csv`
  - A 级：Entire、Warp、Tavily（被收购验证）
  - B 级：OpenRouter、WorkBuddy、MOSI.AI/OpenMOSS
- 已新增“全量名词词典（打样版）”：`data/processed/term_lexicon_0211_0209.csv`
  - 覆盖公司、产品、模型、技术、指标、人物等多类别术语
  - 可作为后续“不漏词”抽取的统一主键表
- 已建立原文入库目录：`data/raw/wechat/`
  - 新增 `README.md`（命名规范与入库原则）
  - 新增 `ingest_manifest.csv`（按日期追踪入库状态）
  - 已落盘 `2026-02-09.md` 原文，`2026-02-11.md`/`2026-02-10.md` 先建占位待完整同步
- 已完成 2/11 与 2/10 原文归档：
  - `data/raw/wechat/2026-02-11.md`：24 条完整条目+来源链接
  - `data/raw/wechat/2026-02-10.md`：10 条完整条目+来源链接
  - `ingest_manifest.csv` 对应状态更新为 `captured`
- 已新增可执行利用路线图：`docs/framework/utilization_strategy.md`
  - 将项目分为 L0~L3 四层资产（原文、事实、语义、洞察）
  - 给出传闻兑现率、公司动作强度、赛道温度、创始人图谱四类用法
- 已完成“现有数据世界模型 v0”三件套（仅基于 2/11→2/09，不做预测）：
  - `docs/analysis/world_model_v0_0211_0209.md`：技术/协议/入口/资本/组织五层内在关联
  - `docs/analysis/entity_relation_network_v0_0211_0209.md`：公司→产品→协议→资本→人物关系主干
  - `docs/analysis/denoised_fact_clusters_v0_0211_0209.md`：F1/F2/F3 去噪事实簇分层
- 已完成目录重构（降噪整理）：
  - 根目录仅保留 `task_plan.md`、`findings.md`、`progress.md` 与 `README.md`
  - 数据统一归档至 `data/raw|processed|indexes|templates`
  - 分析文档统一归档至 `docs/analysis|framework|reports`
- 已新增项目级 `AGENTS.md`：
  - 固化仓库范围工作规范与目录约定
  - 明确 `task_plan.md` / `findings.md` / `progress.md` 为必须保留文件
  - 固化“原文入库→结构化→词典→分析→计划文件更新”的默认流水线

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 采用“实体抽取 + 关系建模”双层结构 | 兼顾信息收集和后续预测推演 |
| 强制使用“单向倒序队列”处理日期 | 保证严格遵循 2/11→2/10→… 的研究顺序 |
| 先构建 30 天日期索引，再做实体深抽 | 在来源受限时先保证时序完整性 |
| 以用户粘贴的公众号正文作为“高可信主源” | 比跨平台转述更完整可追溯 |
| 将“前瞻/传闻/测试”统一结构化标记 | 后续可计算传闻落地率与兑现周期 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| `web.open` 无法打开 `mp.weixin.qq.com` 链接 | 改用命令行抓取与多源检索，不重复同一失败动作 |
| `r.jina.ai` 抓取微信短链超时 | 停用该路径，转用索引/替代源/用户粘贴并行 |
| B 站 API 返回风控页面 | 停止 API 方式，改用搜索索引抓取 |
| B 站空间 API `-799/-403` | 放弃空间 API，改按日期搜索 |

## Resources
- 用户提供链接 1: https://mp.weixin.qq.com/s/ZWc2EsB4jcGbPeCf7gRZSA （2026-02-11）
- 用户提供链接 2: https://mp.weixin.qq.com/s/gHmH90xZ-CuNuSyy2avAng （2026-02-10）
- B 站账号线索: https://www.bilibili.com/video/BV1Z2UqBxEhM/ （结果页含“橘鸦Juya”与“AI 早报”）
- B 站样例: https://www.bilibili.com/video/BV1zRihBCEK9/ （2026-01-03 AI 早报）
- B 站样例: https://www.bilibili.com/video/BV1tPyRBLEZY/ （2025-11-02 AI 早报，含 Intro 链接清单）
- 2/11 倒序起点: https://www.bilibili.com/video/BV1jSA8eUEpq/
- 2/10 倒序次日: https://www.bilibili.com/video/BV1gtA8e3E6B/
- 2/09 倒序第三日: https://www.bilibili.com/video/BV1SAAcehEbA/
- Perplexity 创始团队线索: https://en.wikipedia.org/wiki/Perplexity_AI
- Mistral 创始团队线索: https://en.wikipedia.org/wiki/Mistral_AI
- Helicone 团队线索: https://docs.helicone.ai/helicone-enterprise/our-team
