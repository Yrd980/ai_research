#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

ITEM_HEADING_RE = re.compile(r"^#{2,4}\s+#(\d+)\s+(.+?)\s*$")
URL_RE = re.compile(r"https?://\S+")
ASCII_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._+\-/]*$")


@dataclass
class Primitive:
    name: str
    ptype: str
    regex: re.Pattern[str] | None = None


@dataclass
class ItemBlock:
    date: str
    item_no: int
    item_title: str
    raw_file: str
    text: str


def load_primitives(path: Path) -> List[Primitive]:
    rows: List[Primitive] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            name = (r.get("primitive") or "").strip()
            ptype = (r.get("primitive_type") or "").strip()
            if not name:
                continue
            regex = None
            if ASCII_TOKEN_RE.match(name):
                pattern = r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])"
                regex = re.compile(pattern, flags=re.IGNORECASE)
            rows.append(Primitive(name=name, ptype=ptype, regex=regex))
    rows.sort(key=lambda p: len(p.name), reverse=True)
    return rows


def normalize_text(lines: Sequence[str]) -> str:
    text = "\n".join(lines)
    text = URL_RE.sub(" ", text)
    return text


def parse_item_blocks(raw_files: Iterable[Path]) -> List[ItemBlock]:
    blocks: List[ItemBlock] = []
    for path in sorted(raw_files):
        if path.name == "README.md":
            continue
        if not re.match(r"\d{4}-\d{2}-\d{2}\.md$", path.name):
            continue
        date = path.stem
        lines = path.read_text(encoding="utf-8").splitlines()

        current_no: int | None = None
        current_title = ""
        current_lines: List[str] = []

        def flush() -> None:
            nonlocal current_no, current_title, current_lines
            if current_no is None:
                return
            text = normalize_text(current_lines)
            blocks.append(
                ItemBlock(
                    date=date,
                    item_no=current_no,
                    item_title=current_title,
                    raw_file=str(path),
                    text=text,
                )
            )
            current_no = None
            current_title = ""
            current_lines = []

        for line in lines:
            m = ITEM_HEADING_RE.match(line.strip())
            if m:
                flush()
                current_no = int(m.group(1))
                current_title = m.group(2).strip()
                current_lines = [current_title]
                continue
            if current_no is not None:
                current_lines.append(line)

        flush()
    return blocks


def match_primitives(text: str, primitives: Sequence[Primitive]) -> List[Primitive]:
    matched: List[Primitive] = []
    text_lower = text.lower()
    seen = set()
    for p in primitives:
        if p.regex is not None:
            hit = p.regex.search(text) is not None
        else:
            hit = p.name.lower() in text_lower
        if hit and p.name not in seen:
            matched.append(p)
            seen.add(p.name)
    return matched


def write_occurrences(path: Path, rows: List[dict]) -> None:
    fields = [
        "occurrence_id",
        "date",
        "item_no",
        "item_title",
        "primitive",
        "primitive_type",
        "raw_file",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_hyperedges(path: Path, rows: List[dict]) -> None:
    fields = [
        "hyperedge_id",
        "date",
        "item_no",
        "item_title",
        "primitive_count",
        "primitives",
        "raw_file",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build primitive occurrences and hyperedges from daily raw markdown.")
    parser.add_argument("--primitives", default="data/processed/primitives.csv")
    parser.add_argument("--raw-dir", default="data/raw/wechat")
    parser.add_argument("--occurrences-out", default="data/processed/primitive_occurrences.csv")
    parser.add_argument("--hyperedges-out", default="data/processed/primitive_hyperedges.csv")
    args = parser.parse_args()

    primitive_path = Path(args.primitives)
    raw_dir = Path(args.raw_dir)
    occurrences_out = Path(args.occurrences_out)
    hyperedges_out = Path(args.hyperedges_out)

    primitives = load_primitives(primitive_path)
    blocks = parse_item_blocks(raw_dir.glob("*.md"))

    occurrence_rows: List[dict] = []
    hyperedge_rows: List[dict] = []

    occurrence_index = 1
    hyperedge_index = 1

    for block in blocks:
        matched = match_primitives(block.text, primitives)
        matched_sorted = sorted(matched, key=lambda p: p.name.lower())

        for p in matched_sorted:
            occurrence_rows.append(
                {
                    "occurrence_id": f"O{occurrence_index:05d}",
                    "date": block.date,
                    "item_no": block.item_no,
                    "item_title": block.item_title,
                    "primitive": p.name,
                    "primitive_type": p.ptype,
                    "raw_file": block.raw_file,
                }
            )
            occurrence_index += 1

        if len(matched_sorted) >= 2:
            hyperedge_rows.append(
                {
                    "hyperedge_id": f"H{hyperedge_index:05d}",
                    "date": block.date,
                    "item_no": block.item_no,
                    "item_title": block.item_title,
                    "primitive_count": len(matched_sorted),
                    "primitives": "; ".join(p.name for p in matched_sorted),
                    "raw_file": block.raw_file,
                }
            )
            hyperedge_index += 1

    write_occurrences(occurrences_out, occurrence_rows)
    write_hyperedges(hyperedges_out, hyperedge_rows)

    print(f"primitives={len(primitives)}")
    print(f"item_blocks={len(blocks)}")
    print(f"occurrences={len(occurrence_rows)}")
    print(f"hyperedges={len(hyperedge_rows)}")


if __name__ == "__main__":
    main()
