# Findings & Decisions

## 2026-02-12 用户新指令（Primitive-only）
- 输入是日报，输出应只做一件事：提取“不可再分的原语（名词）”。
- 暂不需要资金/预测/机制分析等扩展层。
- 用户允许激进清理无关文件（仓库由 git 托底）。

## 2026-02-12 当前仓库与新目标冲突点
- 仍存在多条与“只抽原语”无关链路：`data/wiki/*`、`docs/*`、`sync/*`、`scripts/feishu_sync.py`。
- `data/processed/juya_network_seed.csv` 与 `data/processed/entity_relationship_graph.csv` 属于事件/关系层，超出“仅原语”目标。
- 可直接复用 `data/processed/term_lexicon_0211_0209.csv` 作为原语抽取初始基底，再统一为单一 canonical 文件。

## 2026-02-12 原语基底核查
- `data/processed/term_lexicon_0211_0209.csv` 共 87 条，覆盖 `Company/Model/Product/Person/Technique/...` 等原语类别。
- 当前词典已满足“名词原语清单”核心需求，可直接升级为唯一主表。
- 现有术语中未发现必须再拆分的组合项（未出现 `A/B` 合并项），可保留逐项原子形式。

## 2026-02-12 Primitive-only 重构执行结果
- 新增唯一原语主表：`data/processed/primitives.csv`（由历史词典重排为 canonical）。
- 新增模板：`data/templates/primitives_template.csv`。
- 已激进删除无关链路：
  - `data/wiki/` 整目录
  - `docs/` 整目录
  - `sync/` 整目录
  - `.github/workflows/sync-to-feishu.yml`
  - `scripts/feishu_sync.py`
  - `requirements-feishu-sync.txt`
  - 事件/关系中间表（`juya_network_seed.csv`、`entity_relationship_graph.csv` 等）
- 已重写 `AGENTS.md`、`README.md`、`data/raw/wechat/README.md` 为“日报 -> 原语”单流程。

## 2026-02-12 验证结论（Primitive-only）
- 现存工作文件已收敛为：
  - 原文层：`data/raw/wechat/*`
  - 原语层：`data/processed/primitives.csv`
  - 模板层：`data/templates/primitives_template.csv`
  - 记忆层：`task_plan.md`、`findings.md`、`progress.md`
- `primitives.csv` 当前行数：87（含表头）。
- 关键残留检索结果：未发现旧数据链路引用；命中项仅来自原文正文 URL（非流程配置）。
- `check-complete.sh` 结果：`ALL PHASES COMPLETE (10/10)`。

## 2026-02-12 变更轨迹复盘（按提交历史）
- 提交序列（`2026-02-11 -> 2026-02-12`）显示明显三段式演进：
  1) 资产扩张：`7765826` 建立 data/docs 多层研究资产；
  2) 管理/分发增强：`18852d3` 增加 Wiki + 飞书自动同步；
  3) 目标收缩：`122f3a1` 大规模删减到 primitive-only。
- 关键结论：用户稳定偏好是“低过程暴露 + 单一主产物”，对多层分析、验证台账、分发工程的容忍度低。
- 由历史反推的真实需求：日报输入后应直接沉淀“不可再分原语集合”，其余能力应默认关闭，除非用户显式开启。

## 2026-02-12 新方向确认（用户明确）
- 原语仍保留为去噪底座，但目标不止一元词表。
- 新增“类似 Obsidian 图谱延伸”的高维结构层，当前先不引入动词关系。
- 方案确定为：`1元 + N元`，即“原语表 + 同现超边”。

## 2026-02-12 1元 + N元 落地结果
- 新增脚本：`scripts/build_primitive_cooccurrence.py`。
- 新增产物：
  - `data/processed/primitive_occurrences.csv`（按日报条目记录原语出现）
  - `data/processed/primitive_hyperedges.csv`（同条目原语集合，N元超边）
- 新增模板：
  - `data/templates/primitive_occurrences_template.csv`
  - `data/templates/primitive_hyperedges_template.csv`
- 当前统计（基于 2026-02-09 ~ 2026-02-11 原文）：
  - 原语：86 条（不含表头）
  - 条目块：39
  - 出现记录：74
  - 超边：21（仅保留 `primitive_count >= 2`）
- `check-complete.sh` 结果：`ALL PHASES COMPLETE (11/11)`。

## 2026-02-12 VK 外挂初始化输入盘点
- 当前 `primitives.csv` 可直接提供的实体规模：
  - Company: 22
  - Person: 9
  - Product: 14
  - Model: 26
- 其余可作为延伸词条候选：Technique/Concept/Framework/Platform/Project/Standard/Metric/Campaign/Flag。
- 由此可在不污染日报链路前提下初始化独立 `knowledge/` 目录（实体页 + 索引）。

## 2026-02-12 用户命名修正要求
- 外挂目录名称必须是 `wiki`，不是 `vk` 或 `knowledge`。
- 所有目录名和文件名使用英文命名。

## 2026-02-12 当前命名核查
- 新建外挂目录当前为 `knowledge/`，与用户目标不一致，需要整体重命名为 `wiki/`。
- 当前实体页与索引文件名均为英文 slug 命名，可保留。
- 需同步更新 `AGENTS.md`、`README.md`、`task_plan.md` 和索引中的 `page_path` 路径引用。

## 2026-02-12 命名修正完成情况
- 外挂目录已从 `knowledge/` 重命名为 `wiki/`。
- 索引路径已同步到 `wiki/...`（`wiki/index/entity_registry.csv`）。
- `wiki/README.md` 已去除 VK 表述，改为 wiki 口径。
- 特例文件 `item.md` 已重命名为 `doubao-new-year-campaign.md`，并同步更新实体 ID 为 `cpt_doubao-new-year-campaign`。
- 目录与文件名均为英文命名。
- 验证结果：`AGENTS.md`、`README.md`、`task_plan.md` 与 `wiki/` 索引中已无 `knowledge/`、`VK`、`vk` 命名残留。

## 2026-02-12 用户新增要求（wiki 全时态）
- 日报链路保持倒推用于未来信号，但 `wiki/` 不应按倒推逻辑组织。
- `wiki/` 需要回归“可查询的历史本质库”，将历史信息持续融入。
- 目标是“日报原语 -> wiki 发散延伸”，且继续保持物理隔离。

## 2026-02-12 Wiki 全时态改造结果
- 新增 `wiki/index/history_timeline.csv`，作为历史事件时间线索引。
- `wiki/index/relations.csv` 扩展了基础创始关系（OpenAI/Meta/xAI + 已有 Entire）。
- 公司页与人物页已统一增加 `Historical Timeline` 区块并指向时间线索引。
- `AGENTS.md` 与 `README.md` 已明确：日报链路可倒推，`wiki/` 为全时态可查询库。

## 2026-02-12 客观介绍约束（用户强调）
- 用户要求：即使是介绍（intro）也必须客观。
- 已执行：
  - 全量实体页统一使用 `Objective Intro` 命名。
  - `startup_profiles.csv` 字段改为 `objective_intro`。
  - 当前 intro 默认回退为 `TBD (factual, source-backed only)`，避免主观措辞。
  - 新增并接入 `wiki/index/objective_writing_policy.md` 作为写作约束。

## 2026-02-12 用户结构重置要求（本轮）
- `data/indexes/` 的 B 站公开索引应移除（用户当前走手动输入，不再需要公开索引页）。
- `data/raw/wechat/ingest_manifest.csv` 的 `source_url` 需要从旧微信链接模式调整为手动粘贴来源语义。
- `data/wiki/` 应回归“百科式客观名词页”：只保留公司/产品/创始人等客观信息，不承载去噪过程材料。
- 用户不希望在仓库文件中出现显式过程字段与过程文件：如 `evidence`、`verified`、`confidence` 等。
- 关系网络（类似 Obsidian 光联图）应放在 Wiki 之外，作为独立且持续演进的关系层。
- 公司结构倾向层级归属（例如阿里下挂团队/模型），避免过散拆分；复杂关系可单独文件维护。
- `data/processed/juya_network_seed.csv` 字段需瘦身：`entity_category`、`funding_amount_usd`、`founder_info`、`confidence` 被点名不需要。
- `recursive_mechanism_map`、`startup_watchlist` 偏预测/过程，不符合当前“最本质、最小化”目标。
- `term_lexicon` 用户认可，应保留并继续使用。

## 2026-02-12 当前结构核查结果（待改造）
- `data/indexes/juya_daily_index.md` 当前是完整 B 站日期索引页，符合用户“应删”的对象。
- `data/raw/wechat/ingest_manifest.csv` 当前 `source_url` 仍包含旧微信链接（2/11、2/10），与“手动粘贴”现状不一致。
- `data/wiki/` 当前仍是“证据台账式”结构：包含 `evidence_registry.csv`、`pending_verification.csv`、以及多处 `verified/evidence` 字段。
- `data/wiki/company_wiki.csv` 包含 `founder_verified/founder_evidence_id/key_verified_events` 等过程导向字段。
- `data/wiki/product_model_wiki.csv`、`funding_ma_wiki.csv`、`person_wiki.csv` 都带有 `evidence_id` 字段。
- `data/processed/juya_network_seed.csv` 表头确实含用户不需要字段：`entity_category`、`funding_amount_usd`、`founder_info`、`confidence`。
- `data/processed/recursive_mechanism_map_0211_0209.csv` 与 `data/processed/startup_watchlist_v1.csv` 均偏“机制分析/预测跟踪”，可从核心事实层移除。
- `AGENTS.md` 与 `README.md` 仍写有旧结构：`data/indexes/`、`evidence_registry.csv`、`fact_wiki.csv`、`verified/pending` 分流，需同步重写。

## 2026-02-12 结构重置输入数据盘点
- `data/processed/juya_network_seed.csv` 共 41 条事件，当前是最完整的事件主表，但字段偏重（11 列）。
- `data/wiki/company_wiki.csv` 25 行，存在 `founder_verified/founder_evidence_id/key_verified_events/evidence_count` 过程字段。
- `data/wiki/product_model_wiki.csv` 24 行，存在 `evidence_id`，且含 `entity_category`（与主表冗余）。
- `data/wiki/person_wiki.csv` 目前仅 1 行，字段含 `evidence_id`。
- `data/wiki/funding_ma_wiki.csv` 3 行，字段含 `evidence_id`，可保留为客观事件子页但需去过程字段。
- `data/wiki/evidence_registry.csv`、`data/wiki/pending_verification.csv`、`data/wiki/fact_wiki.csv` 可判定为过程层文件，不符合本轮目标。

## 2026-02-12 连带依赖盘点
- `sync/feishu_sync_targets.json` 的 `field_map` 仍绑定旧字段（`entity_category/funding_amount_usd/founder_info/confidence`），需同步精简。
- `data/templates/rolling_ingestion_template.csv` 仍包含 `entity_category/funding_amount_usd/founder_info/evidence_link/confidence`，与新最小事件表不一致。
- `docs/framework/analysis_network.md`、`docs/framework/utilization_strategy.md`、`docs/framework/world_model_v1_spec.md`、`docs/analysis/world_model_v1_0211_0209.md` 仍引用已淘汰文件或字段，需修订引用路径与口径。

## 2026-02-12 词典与关系层可复用信息
- `term_lexicon` 已覆盖 `Company/Product/Model/Person/Platform`，可直接作为新版 `wiki` 的名词补全来源。
- 关系层建议与 `wiki` 分离：独立维护 `entity_relationship_graph`（层级归属 + 协作/并购/发布关系）。
- 飞书同步文档当前“多维表字段要求”仍列旧字段，若不更新会持续把旧结构带回外部系统。

## 2026-02-12 已执行的数据层重构
- 已将 `data/processed/juya_network_seed.csv` 精简为 7 列：`issue_seq/date/item_no/source_url/entity_name/event_type/event_summary`。
- 已将 `data/raw/wechat/ingest_manifest.csv` 改为手动输入语义：`input_method/input_reference`，不再保留旧微信 `source_url` 列。
- 已重建 `data/wiki/` 四个名词页为无过程字段结构：`company_wiki/product_model_wiki/person_wiki/funding_ma_wiki`。
- 已新增独立关系图主文件：`data/processed/entity_relationship_graph.csv`（Wiki 外部，持续演进）。
- 已删除用户点名残留：
  - `data/indexes/juya_daily_index.md`
  - `data/wiki/evidence_registry.csv`
  - `data/wiki/fact_wiki.csv`
  - `data/wiki/pending_verification.csv`
  - `data/processed/recursive_mechanism_map_0211_0209.csv`
  - `data/processed/startup_watchlist_v1.csv`

## 2026-02-12 待收尾项（规范与文档）
- `AGENTS.md` 已改新流程，但编号出现重复（`7` 两次），需修正为连续编号。
- 仍有文档引用旧对象：
  - `docs/framework/analysis_network.md` 仍引用 `data/indexes/juya_daily_index.md`
  - `docs/framework/utilization_strategy.md` 仍出现 `confidence` 与 `startup_watchlist`
  - `docs/framework/world_model_v1_spec.md` 与 `docs/analysis/world_model_v1_0211_0209.md` 仍引用 `fact_wiki/pending_verification`
- `docs/framework/github_to_feishu_sync.md` 仍列旧 CSV 字段清单

## 2026-02-12 文档与配置收尾结果
- 已修正 `AGENTS.md` 流程编号并完成新口径对齐。
- 已重写 `docs/framework/analysis_network.md` 与 `docs/framework/utilization_strategy.md`，去除索引依赖与 `confidence/watchlist` 残留。
- 已重写 `docs/framework/world_model_v1_spec.md` 与 `docs/analysis/world_model_v1_0211_0209.md`，数据绑定切换到 `juya_network_seed + wiki + entity_relationship_graph`。
- 已更新 `docs/framework/github_to_feishu_sync.md` 字段清单，移除旧字段。
- 检索确认（排除 planning 文件）已无旧残留引用，仅保留“禁止过程字段”的规则说明文字。

## 2026-02-12 验证结果
- `python3 -m compileall scripts/feishu_sync.py` 通过。
- `python3 scripts/feishu_sync.py --config sync/feishu_sync_targets.json --mode all --dry-run --verbose` 通过（Markdown 67 行、CSV 41 行）。
- 命令误用记录：`--mode csv` 非脚本支持参数，已记录并切换到 `--mode all`，未重复失败路径。
- `check-complete.sh` 结果：`ALL PHASES COMPLETE (9/9)`。

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
- 已落地“零猜测 Wiki 模式”（用户要求 100% 准确）：
  - 新增 `data/wiki/evidence_registry.csv`（来源证据台账）
  - 新增 `data/wiki/fact_wiki.csv`（仅 verified 事实）
  - 新增 `data/wiki/company_wiki.csv` / `product_model_wiki.csv` / `funding_ma_wiki.csv` / `person_wiki.csv`
  - 新增 `data/wiki/pending_verification.csv`（未核验条目隔离）
- 三天回填结果（2/11→2/09）：
  - verified facts: `34`
  - pending verification: `7`
  - objective companies: `25`
- 已完成“第一性原理递归”升级：
  - `docs/framework/world_model_v1_spec.md`
  - `docs/analysis/world_model_v1_0211_0209.md`
  - `data/processed/recursive_mechanism_map_0211_0209.csv`

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

## 2026-02-11 Feishu Sync Task Findings
- 新需求：为仓库 `/home/yrd/projects/ai_research` 搭建 `GitHub -> 飞书` 的自动同步能力，覆盖 Markdown 与 CSV。
- 仓库当前不存在 `.github/` 目录，尚未配置 GitHub Actions。
- 目录内已存在 `task_plan.md`、`findings.md`、`progress.md`，且根据 `AGENTS.md` 必须保留。
- 命令错误记录：使用 `rg -E` 时触发 `unknown encoding`；后续改为使用 `rg` 基础匹配或管道 `grep -E`，不重复同样写法。
- 仓库当前以 `data/` 和 `docs/` 为核心目录，存在大量 `.md` 与 `.csv` 文件，适合用“按路径前缀过滤”的同步策略（如 `docs/**/*.md`、`data/**/*.csv`）。
- `README.md` 未定义任何现有自动化脚本或部署流程，新增 GitHub Actions 不会与既有 CI 冲突。
- 飞书认证接口可用路径确认：`POST /open-apis/auth/v3/tenant_access_token/internal`。
- 多维表格记录同步可用路径确认：
  - `GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records`
  - `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create`
  - `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update`
- 文档同步可用路径确认：
  - `GET /open-apis/docx/v1/documents/{document_id}/blocks`
  - `DELETE /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children/batch_delete`
  - `POST /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children`
- 工具限制记录：`web.open` 对部分 open.feishu.cn 页面触发 safe-url 限制，已改为搜索聚合结果与可访问 API 索引交叉确认，不重复原路径调用。
- 设计决策：Markdown 先采用“保留 Markdown 原文行 + Docx 段落块写入”的稳妥模式，优先保证自动化稳定性；后续可再升级为富文本块映射。
- `data/processed/juya_network_seed.csv` 表头已确认为：`issue_seq,date,item_no,source_url,entity_category,entity_name,event_type,event_summary,funding_amount_usd,founder_info,confidence`。
- CSV 同步默认可使用复合业务键策略：`issue_seq + date + item_no` 组合生成 `row_key` 用于多维表格 upsert（避免依赖飞书自动记录 ID）。
- 已完成首版落地文件：
  - `scripts/feishu_sync.py`（统一处理 Markdown/CSV 同步）
  - `.github/workflows/sync-to-feishu.yml`（push + 手动触发）
  - `sync/feishu_sync_targets.json`（目标映射模板，默认 `enabled=false` 防误触）
  - `docs/framework/github_to_feishu_sync.md`（配置说明）
  - `requirements-feishu-sync.txt`
- 同步策略关键点：
  - Markdown：按行写入 Docx 文档块；优先清空旧块，失败则降级追加。
  - CSV：按 `upsert_key` 做 create/update 分流，支持 `row_key_from` 自动生成业务键。
- 本地验证通过：`python -m compileall scripts/feishu_sync.py` 与 `--dry-run`。
- 清理动作：移除同步脚本未使用的 `sys` 导入后再次编译与 dry-run，结果仍通过。
- 规划检查：`check-complete.sh` 返回 `ALL PHASES COMPLETE (8/8)`。
- 使用用户提供的真实参数联调后，Docx 接口返回 `code=99991672`，根因是应用未开通文档权限：
  - `docx:document` 或
  - `docx:document:readonly`
- 这不是 ID 填写错误，而是飞书开放平台权限（scope）未授权；需在应用权限页开通并发布后重试。
- 多维表格接口联调结果：
  - `records/list` 成功（说明 `app_token/table_id` 正确且具备读取权限）。
  - 目标表当前仅有一个默认字段 `Text`，没有业务字段（如 `row_key/date/entity_name`）。
  - 自动创建字段调用 `POST /fields` 返回 `code=91403 Forbidden`，说明当前应用/身份对该表无“结构编辑（建字段）”权限。
- 进一步探针：`records/batch_create`（仅写默认 `Text`）同样返回 `91403 Forbidden`，说明当前应用对该表是“只读或未授权写入”状态。
- 因此当前阻塞点有两个：Docx scope 未开通 + Bitable 字段创建权限不足。
- 已将用户提供的真实资源 ID 写入 `sync/feishu_sync_targets.json` 并启用：
  - `document_id = V3XfdCr4go4nXqxzddfcOXYmnpd`
  - `app_token = VUvcb1eOoaErFhsSdXGcgDt2nnf`
  - `table_id = tbldhAn3lLo4sG5w`
- 工作流已支持 `FEISHU_APP_ID` 从 GitHub Variables 或 Secrets 读取，便于最小化配置摩擦。
- 最新联调结果：
  - Docx：`GET /blocks` 已成功（说明文档可读权限已具备）。
  - Docx：`POST /children` 与 `DELETE /children/batch_delete` 返回 `1770032 forBidden`（仍缺文档写权限）。
  - Bitable：字段自动创建 + `records/batch_create` 均成功；`juya_network_seed.csv` 41 行已写入目标表。
  - Bitable 当前总记录数为 `46`（原有 5 行 + 新增 41 行）。
- 额外验证结果：
  - 可通过同一应用 token 成功 `create document` 并成功 `create blocks`（文档 `AQkhdBPAVoyIknxfoNdcpBrmnkM`）。
  - 使用该可写文档跑全量同步（Markdown + CSV）完全成功，CSV 由 `create=0/update=41` 正常幂等更新。
  - 因此可确认：API 实现和应用 scope 均可用，阻塞点仅在目标文档 `V3XfdCr4go4nXqxzddfcOXYmnpd` 的写入授权上下文。
- 已按用户要求将同步文档正式切换为 `AQkhdBPAVoyIknxfoNdcpBrmnkM`（不再使用原云盘文档）。
- 最新实跑结果：Markdown 清空并重写 `61` 行成功；CSV 保持启用并完成 `41` 条更新（`create=0, update=41`）。
- 用户提供 `wiki` 链接 `D5mVwTynAih2KNkjFy2cN0nLnkf` 后，已验证：
  - 该 token 可直接作为 `docx` 文档 ID 使用；
  - `wiki/v2/spaces/get_node` 返回 `obj_type=docx`、`obj_token=QFIAdgtqgoEzcKxVX66cTjOUn0f`；
  - 应用在该节点可写（create blocks 成功）。
- 正式同步目标已切换到 `D5mVwTynAih2KNkjFy2cN0nLnkf` 并全量实跑成功（Markdown + CSV）。

## 2026-02-11 Wiki 导航头增强
- 用户确认希望在 Wiki 文档首屏自动加入导航头（数据更新时间、表格链接、说明）。
- 当前源文档 `docs/analysis/world_model_v1_0211_0209.md` 保持纯研究正文，不含导航区块。
- 当前脚本 `scripts/feishu_sync.py` 中 `sync_markdown_target` 直接同步原文内容，尚无“同步时动态前置头部”的能力。
- 已实现 `sync_header` 配置能力：在同步时动态拼接导航头（文档链接、表格链接、说明、UTC 同步时间），不改动原始 Markdown 文件。
- 当前 `sync/feishu_sync_targets.json` 已为主目标启用 `sync_header`，并写入 wiki + 多维表格链接。
- 实跑验证通过：同步行数由 `61` 增加到 `71`（新增 10 行导航头），Markdown 与 CSV 均成功。
- 用户反馈“看不到更新”后排查：
  - API 返回 `revision_id=12`，且能读到 `# AI Research 总览导航` 与 `最近同步` 文本，说明写入已发生。
  - 发现文档块顺序异常：分批写入时固定 `index=0` 导致每批插入最前，产生“内容顺序错位”体验。
  - 修复策略：按批次递增写入索引，确保最终显示顺序与源文档一致。
