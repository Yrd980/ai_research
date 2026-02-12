# Progress Log

## Session: 2026-02-11

### Current Status
- **Phase:** 1 - Requirements & Discovery
- **Started:** 2026-02-11

### Actions Taken
- 读取 `planning-with-files` 技能说明并确认流程要求。
- 运行会话恢复脚本（无历史恢复输出）。
- 初始化 `task_plan.md`、`findings.md`、`progress.md`。
- 将任务目标、阶段、决策写入计划文件。
- 使用网络检索验证账号线索与文章可访问性。
- 发现 `web.open` 无法直接打开微信文章，准备切换抓取方式。
- 用户将需求扩展并确认执行顺序：必须从 2026-02-11 开始严格倒推。
- 追加检索微信短链 ID 与第三方镜像可用性，结果尚未找到直接可用正文源。
- 尝试通过 `r.jina.ai` 代理抓取两篇微信文章，均超时失败。
- 决定切换到“索引检索 + 替代发布源 + 用户补充原文”策略。
- 尝试调用 B 站公开视频搜索 API 获取日期序列，触发风控页面失败。
- 将采集方式调整为：搜索索引定位视频，再做逐日倒序抽取。
- 通过搜索索引定位到账号主页 `space.bilibili.com/285286947`。
- 验证空间 API 仍不可用（`-799`/`-403`），最终确定“按日期检索并回填”的主流程。
- 按日期查询连续抓取 `2026-02-11` 到 `2026-01-13` 共 30 天视频条目。
- 新增 `data/indexes/juya_daily_index.md`，完成严格倒序索引落盘。
- 新增 `data/processed/juya_network_seed.csv`，写入 2/11 与 2/10 的实体与关系种子数据。
- 新增 `docs/framework/analysis_network.md`，定义倒序研究网络与“预测机”计算思路。
- 补充 Perplexity/Mistral/Helicone 的创始人线索来源。
- 新增 `data/templates/rolling_ingestion_template.csv`（后续滚动回填模板）。
- 新增 `docs/reports/uncertainties.md`（待补字段与证据缺口清单）。
- 运行 `check-complete.sh`，确认计划阶段完成度 `5/5`。
- 接收用户提供的 `2026-02-11` 与 `2026-02-10` 公众号正文。
- 将两天内容按条目编号完整结构化入 `data/processed/juya_network_seed.csv`（34 条）。
- 新增 `docs/reports/juya_0211_0209_coverage.md`，输出“是否完整”的覆盖度结论。
- 接收并处理用户提供的 `2026-02-09` 公众号正文（5 条）。
- 继续按顺序回填 `data/processed/juya_network_seed.csv`，累计完成 `39` 条结构化事件。
- 更新覆盖报告至 `2026-02-11 → 2026-02-09`。
- 覆盖报告文件重命名为 `docs/reports/juya_0211_0209_coverage.md`。
- 追加完成度复检，结果仍为 `ALL PHASES COMPLETE (5/5)`。
- 进入“水上数据发掘水下事物”创新打样阶段。
- 新增 `docs/analysis/underwater_insights_0211_0209.md`，输出隐含结构、暗线竞争与预测清单。
- 新增 `data/processed/startup_watchlist_v1.csv`，输出初创/高势能标的优先级与跟踪点。
- 新增 `data/processed/term_lexicon_0211_0209.csv`，沉淀三天“全量名词词典（打样版）”。
- 运行 `check-complete.sh`，当前阶段完成度为 `6/6`。
- 新建 `data/raw/wechat/` 原文入库目录与规范文档。
- 新建 `data/raw/wechat/ingest_manifest.csv` 追踪每日原文落盘状态。
- 新增 `data/raw/wechat/2026-02-09.md` 原文文件，并为 2/11 与 2/10 建立占位文件。
- 完成 `data/raw/wechat/2026-02-11.md` 与 `data/raw/wechat/2026-02-10.md` 原文归档。
- 更新 `ingest_manifest.csv`，2/11 与 2/10 状态改为 `captured`。
- 新增 `docs/framework/utilization_strategy.md`，输出“如何利用数据”的执行框架。
- 新增 `docs/analysis/world_model_v0_0211_0209.md`，完成五层世界模型主线梳理。
- 新增 `docs/analysis/entity_relation_network_v0_0211_0209.md`，完成全量实体关系网打样。
- 新增 `docs/analysis/denoised_fact_clusters_v0_0211_0209.md`，完成去噪事实簇分层。
- 完成项目目录重构：数据迁移至 `data/`，分析迁移至 `docs/`，减少根目录噪音。
- 新增根目录 `README.md` 说明标准结构与核心入口文件。
- 根据用户反馈恢复并保留 `task_plan.md`、`findings.md`、`progress.md`。
- 新增根目录 `AGENTS.md`，固化协作规范与必须保留文件规则。
- 按“100%准确”要求新增 `data/wiki/` 客观事实层（zero-guess）。
- 从 `data/processed/juya_network_seed.csv` 回填三天 Wiki：verified 34 条，pending 7 条。
- 新增 `docs/framework/world_model_v1_spec.md` 与 `docs/analysis/world_model_v1_0211_0209.md`。
- 新增 `data/processed/recursive_mechanism_map_0211_0209.csv`，打通第一性变量与证据引用。
- 接收新需求：在当前仓库落地 GitHub 到飞书的 Markdown/CSV 自动同步方案。
- 检查仓库自动化入口时发现 `.github/` 目录尚不存在，需从零创建 workflow。
- 记录并修正命令错误：`rg -E` 在当前环境会被解析为编码参数，后续改用 `rg` + `grep -E` 组合。
- 新增 `scripts/feishu_sync.py`，实现统一的飞书认证、Docx 同步与 Bitable upsert。
- 新增 `.github/workflows/sync-to-feishu.yml`，支持 push 自动触发与手动全量触发。
- 新增 `sync/feishu_sync_targets.json` 配置模板（默认 `enabled=false` 防误写）。
- 新增 `requirements-feishu-sync.txt` 与 `docs/framework/github_to_feishu_sync.md`。
- 更新 `README.md`，加入同步文档入口。
- 完成本地语法与干跑验证：`compileall`、`--dry-run`、JSON 格式检查。
- 运行 `check-complete.sh`，当前阶段完成度为 `8/8`。
- 移除同步脚本未使用导入并复检：语法与 dry-run 仍通过。
- 使用用户提供的文档/多维表格 ID 与应用凭据进行真实联调。
- 文档读取接口返回 `99991672`，已定位为应用缺失 docx 权限 scope（非 ID 错误）。
- 多维表格读取接口成功，确认 `app_token/table_id` 可用且 API 鉴权正常。
- 同步脚本新增“自动补齐缺失文本字段”能力后联调，字段创建接口返回 `91403 Forbidden`（表结构编辑权限不足）。
- 追加写入探针：`records/batch_create` 仅写 `Text` 也返回 `91403`，确认当前表对应用不具备写权限。
- 已将用户提供的文档/表格真实 ID 写入 `sync/feishu_sync_targets.json` 并启用对应目标。
- 工作流调整为 `FEISHU_APP_ID` 支持 `vars` 或 `secrets` 双来源。
- 更新同步说明文档，补充权限 scope、资源授权与手工字段清单。
- 再次通过脚本编译与全量 dry-run 验证。
- 用户提供新的文档链接后，已切换 `document_id=V3XfdCr4go4nXqxzddfcOXYmnpd`。
- 真实联调：文档读取成功，但文档写入接口返回 `1770032 forBidden`（仅可读）。
- 真实联调：CSV 目标完全打通，自动建字段 + 批量写入 41 条记录成功。
- 复核目标表记录总数：`46`（原有 5 + 新增 41）。
- 隔离验证：同 token 创建新文档 `AQkhdBPAVoyIknxfoNdcpBrmnkM` 并写入 blocks 成功。
- 使用临时配置指向该文档后，Markdown+CSV 全链路实跑成功（CSV `create=0/update=41`）。
- 按用户确认，将正式配置中的文档目标切换到 `AQkhdBPAVoyIknxfoNdcpBrmnkM`。
- 真实全量同步复跑通过：Markdown 覆盖写入成功，CSV 幂等更新 41 条成功。
- 用户提供 Wiki 链接后，完成 API 探针：确认该 wiki token 可作为 docx 文档节点写入。
- 将正式配置文档目标更新为 `D5mVwTynAih2KNkjFy2cN0nLnkf` 并全量实跑成功。
- 新增 Markdown `sync_header` 动态导航头能力（脚本 + 配置）。
- 更新同步说明文档，补充 `sync_header` 字段与行为说明。
- 真实联调复跑：主文档成功清空并写入（71 行），CSV 幂等更新 41 条成功。
- 用户反馈“看不到文档更新”后，排查发现分批写入索引逻辑导致显示顺序异常。
- 修复 `docx children` 写入索引为递增模式并实跑通过。
- 复核文档前 12 行已正确显示导航头与分隔线，正文紧随其后。
- 用户请求提交代码时，`git add -A` 被环境策略拦截；已改为逐文件暂存方案。
- 接收用户新反馈：清理历史残留并回归“最小化客观名词 Wiki”。
- 删除索引与过程残留文件：`data/indexes/juya_daily_index.md`、`data/wiki/evidence_registry.csv`、`data/wiki/fact_wiki.csv`、`data/wiki/pending_verification.csv`、`data/processed/recursive_mechanism_map_0211_0209.csv`、`data/processed/startup_watchlist_v1.csv`。
- 将 `data/raw/wechat/ingest_manifest.csv` 改为手动输入语义字段（`input_method/input_reference`）。
- 将 `data/processed/juya_network_seed.csv` 精简到 7 列最小事件表。
- 重建 `data/wiki/` 四类客观名词页，移除过程字段。
- 新增 `data/processed/entity_relationship_graph.csv`，将关系图放在 Wiki 外部持续演进。
- 同步更新 `AGENTS.md`、`README.md`、`data/templates/rolling_ingestion_template.csv`、`sync/feishu_sync_targets.json` 与框架文档，清除旧字段引用。
- 复检同步脚本干跑：`python3 scripts/feishu_sync.py --mode all --dry-run --verbose` 通过（41 行 CSV）。
- 运行 `check-complete.sh`，当前阶段完成度为 `9/9`。
- 接收用户新要求：仅保留“日报 -> 不可再分原语”单目标。
- 基于 `term_lexicon_0211_0209.csv` 生成 canonical 原语主表 `data/processed/primitives.csv`（87 条）。
- 新增 `data/templates/primitives_template.csv`，用于后续追加原语。
- 激进删除无关目录与文件：`data/wiki/`、`docs/`、`sync/`、`.github/workflows/sync-to-feishu.yml`、`scripts/feishu_sync.py`、`requirements-feishu-sync.txt` 及历史事件/关系表。
- 重写 `AGENTS.md`、`README.md`、`data/raw/wechat/README.md` 到 primitive-only 流程。
- 残留检查确认（排除 planning 文件）不再存在旧数据链路引用。
- 运行 `check-complete.sh`，当前阶段完成度为 `10/10`。

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| 会话恢复脚本 | 输出历史上下文或空 | 空输出（无恢复项） | ✅ |
| 计划文件初始化 | 3 个文件创建 | 已创建并填充 | ✅ |
| 微信链接网页直开 | 成功读取正文 | 失败（non-retryable） | ⚠️ |
| 倒序索引完整性 | 从 2/11 连续回填 | 已回填到 1/13（30 天） | ✅ |
| 计划完成检查 | 阶段全部完成 | ALL PHASES COMPLETE (5/5) | ✅ |
| 三日原文覆盖率 | 2/11→2/09 全量结构化 | 39/39 条已入库 | ✅ |
| Objective Wiki 回填 | verified/pending 分流可复核 | verified=34, pending=7 | ✅ |
| `scripts/feishu_sync.py` 语法检查 | 可编译 | `python -m compileall` 通过 | ✅ |
| 同步脚本干跑 | 无网络写入、流程可执行 | `--mode all --dry-run` 通过 | ✅ |
| 同步配置 JSON | 结构合法 | `python -m json.tool` 通过 | ✅ |
| 新结构残留检查 | 不再引用已删除文件/旧字段 | 排除 planning 文件后无残留引用 | ✅ |
| 新结构同步干跑 | 新字段映射可正常执行 | `--mode all --dry-run` 通过 | ✅ |
| Primitive 主表生成 | 成功生成原语 canonical 文件 | `data/processed/primitives.csv` 共 87 条 | ✅ |
| Primitive-only 残留检查 | 无旧链路配置引用 | 仅原文内容里的普通 URL 命中（非配置引用） | ✅ |

### Errors
| Error | Resolution |
|-------|------------|
| `web.open` 访问微信文章失败 | 切换到 shell 抓取与替代来源 |
| `r.jina.ai` 代理抓取超时 | 不重复该方法，切换搜狗索引与外部同步源 |
| B 站 API 风控拦截 | 放弃 API 端点，改用搜索索引/页面抓取 |
| 空间 API `-799`/`-403` | 放弃空间 API，按日期索引回填 |
| `feishu_sync.py --mode csv` 参数错误（invalid choice） | 改为脚本支持的 `--mode all --dry-run`，验证通过 |
