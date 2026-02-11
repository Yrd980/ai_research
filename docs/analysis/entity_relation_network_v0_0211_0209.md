# 实体关系网 v0（2026-02-11 → 2026-02-09）

> 目标：给出“公司 → 产品/模型 → 协议/入口 → 融资并购 → 关键人物”的关联骨架。  
> 全量术语索引见：`data/processed/term_lexicon_0211_0209.csv`（用于不漏名词追踪）。

## 1) 关系主干（跨层）

### A. 模型与产品链
- `Qwen Team` → `Qwen-Image-2.0` / `Qwen 3.5`（PR线索）
- `xAI` → `Grok Imagine Image Pro` / `Grok Imagine Image`
- `MOSI.AI + OpenMOSS` → `MOSS-TTS` 家族
- `Ant Group` → `LLaDA2.1 (Mini/Flash)`
- `Tencent Hunyuan` → `HY-1.8B-2Bit`
- `OpenRouter` → `Aurora Alpha`
- `Cursor` → `Composer 1.5`
- `ByteDance` → `Seedream 5.0-Preview`
- `Meta AI` → `Avocado / Avocado Thinking / Sierra`
- `Sora` → `Extensions`
- `WorkBuddy`（CodeBuddy线）→ 桌面AI工作台

### B. 协议与生态链
- `OpenAI` → `Responses API` → `Agent Skills` / 容器网络访问 / 长任务
- `draw.io` → `MCP Server (@drawio/mcp)`
- `Google Gemini` → `gemini-skills`
- `ModelScope` → `OpenAPI + OAuth`
- `Google Chrome` → `WebMCP (preview)`
- `Warp` → `Oz`（Agent 编排与审计）

### C. 入口与分发链
- `OpenAI` → `ChatGPT`（广告测试）/ `Deep Research`（升级）/ `GPT-5.3-Codex`（第三方扩展）
- `OpenAI` → `Cursor / VS Code / GitHub Copilot`（Codex分发入口）
- `Anthropic` → `Claude Cowork (Windows)` / `Claude App` / `Claude Code Desktop`
- `Meituan CatPaw` → IDE内 Agent 工作流开放
- `Obsidian` → `Obsidian CLI`（命令行入口）

### D. 资本与并购链
- `Entire` → 种子轮融资（6000万美元）→ 创始人 `Thomas Dohmke`
- `Runway` → E轮融资（3.15亿美元）
- `Nebius` → 收购 `Tavily`（金额未披露）

---

## 2) 实体主档（31个核心实体）

| 实体 | 角色 | 关联产品/协议/动作 | 融资并购 | 关键人物 |
|---|---|---|---|---|
| OpenAI | 平台公司 | GPT-5.3-Codex 路由/开放、Responses API、Deep Research、广告测试 | - | Sam Altman |
| Anthropic | 平台公司 | Claude Cowork、Claude App、Claude Code Desktop、趋势报告 | - | Dario Amodei / Daniela Amodei |
| Google Gemini | 模型线/生态线 | gemini-skills、Premium Content（开发线索） | - | Larry Page / Sergey Brin（公司层） |
| Google Stitch | 产品线 | Figma 导出能力 | - | 同 Google 体系 |
| Google Chrome | 浏览器平台 | WebMCP 预览 | - | 同 Google 体系 |
| Qwen Team | 模型团队 | Qwen-Image-2.0、Qwen 3.5（PR线索） | - | Unknown |
| xAI | 模型公司 | Grok Imagine Image Pro/API | - | Elon Musk |
| MOSI.AI | 模型团队 | MOSS-TTS 家族联合发布 | - | Unknown |
| OpenMOSS | 开源社区 | MOSS-TTS 家族 | - | Unknown |
| Ant Group | 公司 | LLaDA2.1 扩散大模型 | - | Unknown |
| Tencent Hunyuan | 公司/模型线 | HY-1.8B-2Bit 端侧量化 | - | Unknown |
| Cursor | 开发工具公司 | Composer 1.5 | - | Unknown（当前表） |
| OpenRouter | 模型分发平台 | Aurora Alpha | - | Unknown |
| Warp | Agent基础设施 | Oz 编排平台 | - | Unknown |
| ModelScope | 平台 | OpenAPI / OAuth | - | Unknown |
| draw.io | 工具平台 | 官方 MCP server | - | Unknown |
| Meituan CatPaw | 工具线 | CatPaw 全量开放 | - | Wang Xing（公司层） |
| Sora | 视频产品 | Extensions 续写功能 | - | 与 OpenAI 关联 |
| WorkBuddy | 桌面产品 | AI 桌面工作台 | - | Unknown |
| Obsidian | 工具公司 | Obsidian CLI | - | Shida Li / Erica Xu（当前表） |
| Doubao | 产品 | 春晚联名活动 | - | Zhang Yiming（公司层） |
| Entire | 初创公司 | Checkpoints / CLI / Git工作流会话管理 | 种子轮 6000万美元 | Thomas Dohmke |
| Runway | 公司 | 视频生成产品线扩展 | E轮 3.15亿美元 | Cristobal Valenzuela 等 |
| Nebius | AI云平台 | 并购 Tavily | 收购 Tavily | Arkady Volozh |
| Tavily | 被并购方 | agentic search 与实时验证能力 | 被 Nebius 收购 | Unknown |
| Hugging Face | 平台/社区 | Transformers.js v4（预览） | - | Clement Delangue 等 |
| Zhipu AI | 模型公司 | GLM-5 架构线索 | - | Unknown |
| Antigravity | 产品入口 | 提供 Claude Opus 4.6 可用 | - | Unknown |
| ByteDance | 公司 | Seedream 5.0-Preview、豆包活动 | - | Zhang Yiming |
| Meta AI | 公司线 | Avocado 测试、Sierra/Big Brain 概念 | - | Mark Zuckerberg |
| Unsloth | 技术团队 | MoE 训练优化 | - | Unknown |

---

## 3) 人物关联骨架（当前已识别）

- `Sam Altman` ↔ OpenAI（模型路由、API、分发、商业化同日多动作）
- `Thomas Dohmke` ↔ Entire（初创+融资+开发工作流切入）
- `Cristobal Valenzuela` 等 ↔ Runway（融资推进世界模型路线）
- `Arkady Volozh` ↔ Nebius（并购整合 agentic search）
- `Dario/Daniela Amodei` ↔ Anthropic（产品线+开发者工具+研究报告）

> 备注：`Unknown` 人物会在后续日期回填中持续补齐，不覆盖原始事实层。

