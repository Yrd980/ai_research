# GitHub → 飞书自动同步（Markdown + CSV）

## 目标

- 仓库作为唯一内容源（AI 可持续编辑）。
- `GitHub Actions` 自动同步到飞书：
  - Markdown → 飞书文档（Docx）
  - CSV → 飞书多维表格（Bitable）
- 对外只分发飞书链接，不单独建网站。

## 已新增文件

- Workflow: `.github/workflows/sync-to-feishu.yml`
- 同步脚本: `scripts/feishu_sync.py`
- 目标配置: `sync/feishu_sync_targets.json`
- 依赖: `requirements-feishu-sync.txt`

## 你需要准备的配置

### 1) GitHub Secrets

在仓库 Settings → Secrets and variables → Actions → Secrets 新建：

- `FEISHU_APP_SECRET`

### 2) GitHub Variables（可选）

- `FEISHU_APP_ID`（推荐放这里；你当前值：`cli_a906328fc078dbcb`）
- `FEISHU_BASE_URL`  
  默认可不配；如果你有私有代理域名才配置。

### 3) `sync/feishu_sync_targets.json`

把占位值替换成你的真实飞书资源 ID，并把对应 `enabled` 改为 `true`：

- Markdown 目标项需要：
  - `source`: 仓库中的 `.md` 文件路径
  - `document_id`: 飞书文档 ID（`doxcn...`）
  - `sync_header`（可选）：同步时自动前置导航头（不改动原 `.md` 文件）
    - `enabled`: 是否启用自动导航头
    - `title`: 导航头标题
    - `doc_url`: 对外文档链接
    - `bitable_url`: 对外数据表链接
    - `notes`: 导航说明列表（会自动渲染为项目符号）
- CSV 目标项需要：
  - `source`: 仓库中的 `.csv` 文件路径
  - `app_token`: 多维表格 App Token（`bascn...`）
  - `table_id`: 数据表 ID（`tbl...`）
  - `upsert_key`: 用于幂等更新的字段名（建议保留 `row_key`）
  - `row_key_from`: 用来拼 `row_key` 的 CSV 字段数组（示例已配置）
  - `field_map`: CSV 列名到多维表格字段名映射

## 执行方式

- `push` 到 `main` 且命中路径（`docs/**/*.md`、`data/**/*.csv` 等）会自动触发。
- 你也可以在 Actions 里手动运行 `workflow_dispatch`（会全量同步）。

## 飞书侧必开权限（非常关键）

如果不先开权限，脚本会直接报错。当前联调已验证：

- 文档接口报错：`99991672 Access denied`（缺 Docx scope）
- 文档写入报错：`1770032 forBidden`（文档对应用仅可读、无编辑权限）
- 多维表格写入/建字段报错：`91403 Forbidden`（表级写权限不足）

请在飞书开放平台按下列最小集开通并发布：

- 文档相关（至少一个）：
  - `docx:document`（推荐，可读写）
  - 或 `docx:document:readonly`（只读，不满足写入）
- 多维表格相关：
  - 多维表格记录读写权限（用于 `records/batch_create` / `batch_update`）
  - 多维表格字段管理权限（用于自动建字段；若不开就手动建字段）

此外要在飞书里把目标资源授权给该应用：

- 文档 `D5mVwTynAih2KNkjFy2cN0nLnkf`：授权应用可编辑
- 多维表格 `VUvcb1eOoaErFhsSdXGcgDt2nnf` / 表 `tbldhAn3lLo4sG5w`：授权应用可编辑（非只读）

## 多维表格字段要求

如果你暂时不给应用“建字段权限”，请先手动建好这些文本列（与配置一致）：

- `row_key`
- `issue_seq`
- `date`
- `item_no`
- `source_url`
- `entity_category`
- `entity_name`
- `event_type`
- `event_summary`
- `funding_amount_usd`
- `founder_info`
- `confidence`

## 同步逻辑说明

- Markdown：
  - 读取 `.md` 文件内容
  - 可按 `sync_header` 动态插入“导航头 + 最近同步时间（UTC）”
  - 写入飞书 Docx 文档段落块（默认按行写入）
  - 尝试先清空旧块，若清空失败则降级为追加模式（不中断同步）
- CSV：
  - 读取 CSV 行
  - 可按 `row_key_from` 生成 `row_key`
  - 先拉取目标表已有记录，用 `upsert_key` 做 `create/update` 分流
  - 批量写入，避免重复造记录

## 本地调试（可选）

```bash
cd /home/yrd/projects/ai_research
pip install -r requirements-feishu-sync.txt
export FEISHU_APP_ID=xxx
export FEISHU_APP_SECRET=yyy
python scripts/feishu_sync.py --config sync/feishu_sync_targets.json --mode all --dry-run --verbose
```

## 常见排错

- 报 `Missing FEISHU_APP_ID or FEISHU_APP_SECRET`：检查 GitHub Secrets 或本地环境变量。
- 报文档/表格权限错误：给自建应用授予对应文档与多维表格访问权限。
- CSV 全是 create 不 update：检查 `upsert_key` 字段是否真的写入到飞书表里。
- Markdown 出现重复段落：说明清空旧块失败，先看 Action 日志中的 docx 删除接口报错，再按你的文档权限调整。
