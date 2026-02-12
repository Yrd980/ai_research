#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

DETAIL_START_RE = re.compile(r"^##\s+详细条目")
ITEM_HEADING_RE = re.compile(r"^#{2,4}\s+#(\d+)\s+(.+?)\s*$")
URL_RE = re.compile(r"https?://\S+")

NON_PRIMARY_DOMAINS = {
    "x.com",
    "twitter.com",
    "linux.do",
    "mp.weixin.qq.com",
    "weibo.com",
    "zhihu.com",
    "reddit.com",
    "bilibili.com",
    "youtube.com",
    "youtu.be",
}

NOISY_MARKERS = (
    "rumor",
    "rumors",
    "speculative",
    "speculation",
    "unconfirmed",
    "alleged",
    "possibly",
    "possible",
    "reportedly",
    "might",
    "may",
    "could",
)


@dataclass
class ItemBlock:
    date: str
    item_no: int
    item_title: str
    raw_file: str
    lines: list[str]


def load_occurrences(path: Path) -> dict[tuple[str, int], list[dict[str, str]]]:
    grouped: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            day = (row.get("date") or "").strip()
            item_no_s = (row.get("item_no") or "").strip()
            if not day or not item_no_s.isdigit():
                continue
            grouped[(day, int(item_no_s))].append(row)
    return grouped


def load_entity_map(path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            name = (row.get("entity_name") or "").strip().lower()
            entity_id = (row.get("entity_id") or "").strip()
            if name and entity_id:
                mapping[name] = entity_id
    return mapping


def parse_item_blocks(raw_dir: Path) -> list[ItemBlock]:
    blocks: list[ItemBlock] = []
    for path in sorted(raw_dir.glob("*.md")):
        if not re.match(r"\d{4}-\d{2}-\d{2}\.md$", path.name):
            continue

        day = path.stem
        lines = path.read_text(encoding="utf-8").splitlines()
        in_detail = False

        current_no: int | None = None
        current_title = ""
        current_lines: list[str] = []

        def flush() -> None:
            nonlocal current_no, current_title, current_lines
            if current_no is None:
                return
            blocks.append(
                ItemBlock(
                    date=day,
                    item_no=current_no,
                    item_title=current_title,
                    raw_file=str(path),
                    lines=current_lines[:],
                )
            )
            current_no = None
            current_title = ""
            current_lines = []

        for line in lines:
            stripped = line.strip()
            if not in_detail:
                if DETAIL_START_RE.match(stripped):
                    in_detail = True
                continue

            heading = ITEM_HEADING_RE.match(stripped)
            if heading:
                flush()
                current_no = int(heading.group(1))
                current_title = heading.group(2).strip()
                current_lines = []
                continue

            if current_no is not None:
                current_lines.append(line)

        flush()

    return blocks


def normalize_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def is_primary_url(url: str) -> bool:
    host = normalize_domain(url)
    if host in NON_PRIMARY_DOMAINS:
        return False
    if host.endswith(".x.com") or host.endswith(".twitter.com"):
        return False
    if host.endswith(".weixin.qq.com"):
        return False
    return bool(host)


def pick_primary_url(lines: list[str]) -> str:
    seen: set[str] = set()
    for line in lines:
        for raw_url in URL_RE.findall(line):
            url = raw_url.rstrip(").,;]")
            if url in seen:
                continue
            seen.add(url)
            if is_primary_url(url):
                return url
    return ""


def extract_quote_span(lines: list[str]) -> str:
    for line in lines:
        text = line.strip()
        if not text:
            continue
        if text.startswith("链接"):
            continue
        if text.startswith("-") and "http" in text:
            continue
        if "http://" in text or "https://" in text:
            continue
        return text[:220]
    return ""

def is_noisy_item(title: str, quote_span: str) -> bool:
    text = f"{title} {quote_span}".lower()
    for marker in NOISY_MARKERS:
        if marker.lower() in text:
            return True
    return False


def write_candidates(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "candidate_id",
        "subject_entity_id",
        "subject_text",
        "predicate",
        "object_type",
        "object_value",
        "event_date",
        "event_title",
        "event_summary",
        "source_url",
        "source_type",
        "status",
        "last_updated",
        "quote_span",
        "raw_file",
        "item_no",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build primary-only wiki assertion candidates from AI daily raw files + primitive occurrences."
    )
    parser.add_argument("--raw-dir", default="data/raw/wechat")
    parser.add_argument("--occurrences", default="data/processed/primitive_occurrences.csv")
    parser.add_argument("--entity-registry", default="wiki/index/entity_registry.csv")
    parser.add_argument("--out", default="wiki/index/assertions_candidates.csv")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    occurrence_map = load_occurrences(Path(args.occurrences))
    entity_map = load_entity_map(Path(args.entity_registry))
    blocks = parse_item_blocks(raw_dir)

    rows: list[dict[str, str]] = []
    skipped_no_occ = 0
    skipped_no_primary = 0
    skipped_noisy = 0
    today = str(date.today())
    idx = 1

    for block in blocks:
        occurrences = occurrence_map.get((block.date, block.item_no), [])
        if not occurrences:
            skipped_no_occ += 1
            continue

        source_url = pick_primary_url(block.lines)
        if not source_url:
            skipped_no_primary += 1
            continue

        quote_span = extract_quote_span(block.lines)
        if is_noisy_item(block.item_title, quote_span):
            skipped_noisy += 1
            continue
        seen_primitives: set[str] = set()

        for occ in occurrences:
            primitive = (occ.get("primitive") or "").strip()
            if not primitive or primitive in seen_primitives:
                continue
            seen_primitives.add(primitive)
            rows.append(
                {
                    "candidate_id": f"C{idx:05d}",
                    "subject_entity_id": entity_map.get(primitive.lower(), ""),
                    "subject_text": primitive,
                    "predicate": "daily_report_fact",
                    "object_type": "text",
                    "object_value": block.item_title,
                    "event_date": block.date,
                    "event_title": block.item_title,
                    "event_summary": quote_span,
                    "source_url": source_url,
                    "source_type": "primary",
                    "status": "candidate",
                    "last_updated": today,
                    "quote_span": quote_span,
                    "raw_file": block.raw_file,
                    "item_no": str(block.item_no),
                    "notes": "from_ai_daily_primary_link",
                }
            )
            idx += 1

    write_candidates(Path(args.out), rows)

    print(f"blocks={len(blocks)}")
    print(f"candidate_rows={len(rows)}")
    print(f"skipped_no_occurrences={skipped_no_occ}")
    print(f"skipped_no_primary_link={skipped_no_primary}")
    print(f"skipped_noisy_item={skipped_noisy}")


if __name__ == "__main__":
    main()
