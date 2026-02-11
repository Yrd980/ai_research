# 去噪事实簇 v0（2026-02-11 → 2026-02-09）

> 原则：同一条信息按“证据性质”分层，不做评分，不做预测。  
> 目标：把“可直接采信事实”与“观察线索”拆开，避免叙事污染。

## 分层定义

- **F1 已证实动作**：有官方博客/文档/GitHub PR 或公司公告可直连验证。
- **F2 平台披露/产品声明**：来自官方账号或产品页，仍需观察后续稳定性。
- **F3 传闻与测试线索**：处于预览、灰测、第三方观察，保留但不当作已落地。

---

## F1 已证实动作（事实核心层）

### 模型与产品发布
- Qwen-Image-2.0 发布（官方博客+chat入口）
- MOSS-TTS 家族发布（GitHub/HuggingFace）
- LLaDA2.1 发布（GitHub/HuggingFace）
- HY-1.8B-2Bit 发布（HF/微信技术文）
- Grok Imagine Image Pro/API 上线（xAI docs）
- Aurora Alpha 上线（OpenRouter 页面）
- Composer 1.5 上线（Cursor blog/docs）
- Sora Extensions 功能上线（官方账号）
- Obsidian CLI 发布（官方帮助文档）

### 协议/生态能力发布
- Responses API 新能力（OpenAI dev）
- gemini-skills 仓库发布（GitHub）
- draw.io MCP server 发布（官方账号）
- ModelScope OpenAPI/OAuth 发布（官方文）
- WebMCP 在 Chrome 146 进入预览文档
- Transformers.js v4 预览发布（HF blog）

### 资本/并购动作
- Entire 完成 6000万美元种子融资（公司博客）
- Runway 完成 3.15亿美元E轮融资（报道）
- Nebius 宣布收购 Tavily（公司新闻稿）

---

## F2 平台披露/产品声明（高相关观测层）

- OpenAI 对高风险 GPT-5.3-Codex 请求路由至 GPT-5.2（平台相关披露）
- OpenAI 向第三方扩展 GPT-5.3-Codex 可用性（开发者渠道披露）
- ChatGPT 广告测试（官方公告，仍在测试范围内）
- Codex 免费层可用策略延续（高管声明）
- Claude Code Desktop 引入 `--dangerously-skip-permissions`（工具更新披露）
- Claude Cowork Windows 版发布（官方账号披露）
- Claude App 交互与语音模式开放（分阶段披露）
- WorkBuddy 开放内测（产品页与介绍）
- CatPaw 全量开放（产品公告）
- Google Stitch Figma 导出功能（官方账号披露）
- 豆包春晚联名活动（活动公告）

---

## F3 传闻与测试线索（保留观察层）

- Qwen 3.5 系列“即将发布”及 PR 支持线索
- Seedream 5.0-Preview（预览版，文中同时提示效果退化）
- Meta AI 内部测试 `Avocado / Avocado Thinking / Sierra / Big Brain`
- Gemini Premium Content 功能开发线索
- GLM-5 参数规模/架构细节外部推测

---

## 噪音隔离规则（本轮已执行）

- 同一事件若同时存在“官方源 + 转述源”，仅将官方源放入 F1/F2，转述作为旁注。
- 含“可能/传闻/测试中/开发中”关键词的条目统一归入 F3。
- 未给出原始链接或仅二手评论的条目，不进入事实核心层。

