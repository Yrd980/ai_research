#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import subprocess
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set

import requests


LOGGER = logging.getLogger("feishu_sync")
DEFAULT_BASE_URL = "https://open.feishu.cn"
TOKEN_PATH = "/open-apis/auth/v3/tenant_access_token/internal"


class FeishuApiError(RuntimeError):
    pass


def chunked(items: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def build_row_key(raw_row: Dict[str, str], fields: Sequence[str]) -> str:
    values = [str(raw_row.get(field, "")).strip() for field in fields]
    return "|".join(values)


@dataclass
class MarkdownTarget:
    source: str
    document_id: str
    title: str = ""
    sync_header: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class CsvTarget:
    source: str
    app_token: str
    table_id: str
    upsert_key: str
    field_map: Dict[str, str] = field(default_factory=dict)
    row_key_from: List[str] = field(default_factory=list)
    enabled: bool = True


@dataclass
class SyncConfig:
    markdown_targets: List[MarkdownTarget]
    csv_targets: List[CsvTarget]


class FeishuClient:
    def __init__(self, app_id: str, app_secret: str, base_url: str, timeout: int = 30) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._token: Optional[str] = None

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
        auth: bool = True,
    ) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if auth:
            headers["Authorization"] = f"Bearer {self.get_tenant_access_token()}"

        url = f"{self.base_url}{path}"
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=payload,
            timeout=self.timeout,
        )
        data: Dict[str, Any]
        try:
            data = response.json()
        except ValueError:
            data = {}
        if response.status_code >= 400:
            if data:
                raise FeishuApiError(
                    f"Feishu HTTP error ({method} {path}): "
                    f"http={response.status_code}, code={data.get('code')}, msg={data.get('msg')}, body={data}"
                )
            response.raise_for_status()
        code = data.get("code")
        if code not in (0, "0", None):
            raise FeishuApiError(
                f"Feishu API error ({method} {path}): code={code}, msg={data.get('msg')}, body={data}"
            )
        return data

    def get_tenant_access_token(self) -> str:
        if self._token:
            return self._token
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        data = self._request("POST", TOKEN_PATH, payload=payload, auth=False)
        token = data.get("tenant_access_token")
        if not token:
            token = (data.get("data") or {}).get("tenant_access_token")
        if not token:
            raise FeishuApiError(f"Missing tenant_access_token in response: {data}")
        self._token = token
        return token

    def list_bitable_records(self, app_token: str, table_id: str, page_size: int = 500) -> List[Dict[str, Any]]:
        path = f"/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        page_token = ""
        results: List[Dict[str, Any]] = []
        while True:
            params: Dict[str, Any] = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            response = self._request("GET", path, params=params)
            data = response.get("data", {})
            items = data.get("items") or []
            results.extend(items)
            has_more = bool(data.get("has_more"))
            page_token = data.get("page_token") or ""
            if not has_more:
                break
        return results

    def bitable_batch_create_records(
        self, app_token: str, table_id: str, records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        path = f"/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
        payload = {"records": records}
        return self._request("POST", path, payload=payload)

    def bitable_batch_update_records(
        self, app_token: str, table_id: str, records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        path = f"/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
        payload = {"records": records}
        return self._request("POST", path, payload=payload)

    def list_bitable_fields(self, app_token: str, table_id: str, page_size: int = 200) -> List[Dict[str, Any]]:
        path = f"/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        page_token = ""
        results: List[Dict[str, Any]] = []
        while True:
            params: Dict[str, Any] = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            response = self._request("GET", path, params=params)
            data = response.get("data", {})
            items = data.get("items") or []
            results.extend(items)
            has_more = bool(data.get("has_more"))
            page_token = data.get("page_token") or ""
            if not has_more:
                break
        return results

    def create_bitable_text_field(self, app_token: str, table_id: str, field_name: str) -> Dict[str, Any]:
        path = f"/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        payload = {"field_name": field_name, "type": 1}
        return self._request("POST", path, payload=payload)

    def list_doc_blocks(self, document_id: str, page_size: int = 100) -> List[Dict[str, Any]]:
        path = f"/open-apis/docx/v1/documents/{document_id}/blocks"
        page_token = ""
        items: List[Dict[str, Any]] = []
        while True:
            params: Dict[str, Any] = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            response = self._request("GET", path, params=params)
            data = response.get("data", {})
            current = data.get("items") or []
            if isinstance(current, dict):
                current = list(current.values())
            items.extend(current)
            if not data.get("has_more"):
                break
            page_token = data.get("page_token") or ""
            if not page_token:
                break
        return items

    def delete_doc_children(self, document_id: str, block_id: str, start_index: int, end_index: int) -> None:
        path = f"/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children/batch_delete"
        payload = {"start_index": start_index, "end_index": end_index}
        params = {"document_revision_id": -1}
        self._request("DELETE", path, params=params, payload=payload)

    def append_doc_children(
        self,
        document_id: str,
        block_id: str,
        blocks: List[Dict[str, Any]],
        *,
        index: Optional[int] = None,
    ) -> None:
        path = f"/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"
        payload = {
            "children": blocks,
            "client_token": str(uuid.uuid4()),
        }
        if index is not None:
            payload["index"] = index
        params = {"document_revision_id": -1}
        self._request("POST", path, params=params, payload=payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync Markdown and CSV files from GitHub repo to Feishu.")
    parser.add_argument("--config", default="sync/feishu_sync_targets.json", help="Path to sync config json.")
    parser.add_argument("--mode", choices=["all", "changed"], default="changed", help="Sync mode.")
    parser.add_argument("--base-sha", default="", help="Base git SHA for changed mode.")
    parser.add_argument("--head-sha", default="HEAD", help="Head git SHA for changed mode.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing to Feishu.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logs.")
    return parser.parse_args()


def load_config(path: Path) -> SyncConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    markdown_targets = [MarkdownTarget(**item) for item in raw.get("markdown_targets", [])]
    csv_targets = [CsvTarget(**item) for item in raw.get("csv_targets", [])]
    return SyncConfig(markdown_targets=markdown_targets, csv_targets=csv_targets)


def normalize_repo_path(path: str) -> str:
    return Path(path).as_posix().lstrip("./")


def list_changed_files(base_sha: str, head_sha: str) -> Optional[Set[str]]:
    zero_sha = "0" * 40
    if not base_sha or base_sha == zero_sha:
        return None
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only", base_sha, head_sha],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as error:
        LOGGER.warning("git diff failed (%s). fallback to full sync.", error.output.strip())
        return None
    changed = {normalize_repo_path(line.strip()) for line in output.splitlines() if line.strip()}
    return changed


def select_targets(
    config: SyncConfig,
    changed_paths: Optional[Set[str]],
    config_path: str,
) -> SyncConfig:
    if changed_paths is None:
        return config

    config_changed = normalize_repo_path(config_path) in changed_paths
    if config_changed:
        LOGGER.info("Config changed, forcing full sync.")
        return config

    markdown_targets = [
        target
        for target in config.markdown_targets
        if target.enabled and normalize_repo_path(target.source) in changed_paths
    ]
    csv_targets = [
        target for target in config.csv_targets if target.enabled and normalize_repo_path(target.source) in changed_paths
    ]
    return SyncConfig(markdown_targets=markdown_targets, csv_targets=csv_targets)


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def build_doc_blocks(content: str) -> List[Dict[str, Any]]:
    lines = content.splitlines()
    if not lines:
        lines = ["(empty)"]
    blocks: List[Dict[str, Any]] = []
    for raw_line in lines:
        line = raw_line if raw_line else " "
        blocks.append(
            {
                "block_type": 2,
                "text": {
                    "elements": [
                        {
                            "text_run": {
                                "content": line[:1800],
                            }
                        }
                    ]
                },
            }
        )
    return blocks


def build_sync_header(target: MarkdownTarget) -> str:
    sync_header = target.sync_header or {}
    if not sync_header.get("enabled"):
        return ""

    title = str(sync_header.get("title", "")).strip() or "AI Research 导航"
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# {title}", ""]

    doc_url = str(sync_header.get("doc_url", "")).strip()
    bitable_url = str(sync_header.get("bitable_url", "")).strip()
    if doc_url:
        lines.append(f"- 文档链接: {doc_url}")
    if bitable_url:
        lines.append(f"- 数据表链接: {bitable_url}")
    lines.append(f"- 最近同步: {now_utc}")

    notes = sync_header.get("notes", [])
    if isinstance(notes, list):
        for note in notes:
            note_text = str(note).strip()
            if not note_text:
                continue
            if note_text.startswith("- "):
                lines.append(note_text)
            else:
                lines.append(f"- {note_text}")

    lines.extend(["", "---", ""])
    return "\n".join(lines)


def render_markdown_content(target: MarkdownTarget, source_content: str) -> str:
    sync_header = build_sync_header(target)
    if not sync_header:
        return source_content
    body = source_content.lstrip("\n")
    return f"{sync_header}{body}"


def find_root_block_id(blocks: Sequence[Dict[str, Any]]) -> Optional[str]:
    for block in blocks:
        if block.get("block_type") == 1 and not block.get("parent_id"):
            return block.get("block_id")
    for block in blocks:
        if not block.get("parent_id"):
            return block.get("block_id")
    return None


def sync_markdown_target(client: FeishuClient, target: MarkdownTarget, dry_run: bool) -> None:
    source = Path(target.source)
    if not source.exists():
        LOGGER.warning("Markdown source missing, skipped: %s", target.source)
        return
    source_content = source.read_text(encoding="utf-8")
    content = render_markdown_content(target, source_content)
    blocks = build_doc_blocks(content)
    LOGGER.info("Markdown target: %s -> doc %s (%s lines)", target.source, target.document_id, len(blocks))
    if dry_run:
        return

    existing_blocks = client.list_doc_blocks(target.document_id)
    root_block_id = find_root_block_id(existing_blocks)
    if not root_block_id:
        raise FeishuApiError(f"Cannot locate root block for document {target.document_id}")

    root_block = next((item for item in existing_blocks if item.get("block_id") == root_block_id), {})
    children = root_block.get("children") or []
    base_index = 0
    if children:
        try:
            client.delete_doc_children(target.document_id, root_block_id, 0, len(children))
            LOGGER.info("Cleared %s old doc blocks.", len(children))
        except Exception as error:
            LOGGER.warning("Clear doc blocks failed, append mode fallback: %s", error)
            base_index = len(children)

    current_index = base_index
    for batch in chunked(blocks, 20):
        current_batch = list(batch)
        client.append_doc_children(
            target.document_id,
            root_block_id,
            current_batch,
            index=current_index,
        )
        current_index += len(current_batch)
    LOGGER.info("Markdown synced: %s", target.source)


def map_csv_fields(row: Dict[str, str], field_map: Dict[str, str]) -> Dict[str, Any]:
    mapped: Dict[str, Any] = {}
    for key, value in row.items():
        target_key = field_map.get(key, key)
        mapped[target_key] = value
    return mapped


def sync_csv_target(client: FeishuClient, target: CsvTarget, dry_run: bool) -> None:
    source = Path(target.source)
    if not source.exists():
        LOGGER.warning("CSV source missing, skipped: %s", target.source)
        return
    rows = read_csv_rows(source)
    LOGGER.info("CSV target: %s -> %s/%s (%s rows)", target.source, target.app_token, target.table_id, len(rows))

    payload_rows: List[Dict[str, Any]] = []
    for raw_row in rows:
        fields = map_csv_fields(raw_row, target.field_map)
        if target.row_key_from:
            generated_key = build_row_key(raw_row, target.row_key_from)
            if generated_key:
                fields[target.upsert_key] = generated_key
        key_value = str(fields.get(target.upsert_key, "")).strip()
        if not key_value:
            LOGGER.warning("Skip CSV row missing upsert key '%s': %s", target.upsert_key, raw_row)
            continue
        payload_rows.append(fields)

    if not payload_rows:
        LOGGER.warning("No valid rows for csv target: %s", target.source)
        return

    if dry_run:
        LOGGER.info("CSV dry-run rows prepared: %s", len(payload_rows))
        return

    required_field_names: Set[str] = set()
    for row in payload_rows:
        required_field_names.update(str(key).strip() for key in row.keys() if str(key).strip())

    existing_fields = client.list_bitable_fields(target.app_token, target.table_id)
    existing_field_names = {str(item.get("field_name", "")).strip() for item in existing_fields if item.get("field_name")}
    missing_fields = sorted(name for name in required_field_names if name not in existing_field_names)
    if missing_fields:
        LOGGER.info("CSV target missing fields, auto-creating text fields: %s", ", ".join(missing_fields))
        for field_name in missing_fields:
            client.create_bitable_text_field(target.app_token, target.table_id, field_name)

    existing_records = client.list_bitable_records(target.app_token, target.table_id)
    existing_map: Dict[str, str] = {}
    for item in existing_records:
        record_id = item.get("record_id")
        key = str((item.get("fields") or {}).get(target.upsert_key, "")).strip()
        if record_id and key:
            existing_map[key] = record_id

    to_create: List[Dict[str, Any]] = []
    to_update: List[Dict[str, Any]] = []
    for fields in payload_rows:
        key = str(fields[target.upsert_key]).strip()
        if key in existing_map:
            to_update.append({"record_id": existing_map[key], "fields": fields})
        else:
            to_create.append({"fields": fields})

    LOGGER.info(
        "CSV upsert plan for %s: create=%s, update=%s",
        target.source,
        len(to_create),
        len(to_update),
    )

    for batch in chunked(to_create, 100):
        client.bitable_batch_create_records(target.app_token, target.table_id, list(batch))
    for batch in chunked(to_update, 100):
        client.bitable_batch_update_records(target.app_token, target.table_id, list(batch))
    LOGGER.info("CSV synced: %s", target.source)


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Sync config not found: {config_path}")

    app_id = os.getenv("FEISHU_APP_ID", "").strip()
    app_secret = os.getenv("FEISHU_APP_SECRET", "").strip()
    if not app_id or not app_secret:
        raise RuntimeError("Missing FEISHU_APP_ID or FEISHU_APP_SECRET environment variables.")

    config = load_config(config_path)
    changed_paths: Optional[Set[str]] = None
    if args.mode == "changed":
        changed_paths = list_changed_files(args.base_sha, args.head_sha)
        if changed_paths is not None:
            LOGGER.info("Changed files detected: %s", len(changed_paths))
    selected = select_targets(config, changed_paths, str(config_path))

    if not selected.markdown_targets and not selected.csv_targets:
        LOGGER.info("No matching targets to sync. exit.")
        return 0

    client = FeishuClient(
        app_id=app_id,
        app_secret=app_secret,
        base_url=os.getenv("FEISHU_BASE_URL", DEFAULT_BASE_URL),
    )

    for target in selected.markdown_targets:
        if not target.enabled:
            continue
        sync_markdown_target(client, target, args.dry_run)

    for target in selected.csv_targets:
        if not target.enabled:
            continue
        sync_csv_target(client, target, args.dry_run)

    LOGGER.info("Feishu sync completed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        LOGGER.error("sync failed: %s", error)
        raise
