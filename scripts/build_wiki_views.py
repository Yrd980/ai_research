#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
from pathlib import Path

RELATION_PREDICATES = {
    "founder_of", "acquired", "acquires", "belongs_to", "part_of", "ceo_of", "invested_in", "partner_of"
}

def read_assertions(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def build_relations(assertions):
    rows = []
    n = 1
    for a in assertions:
        if a.get("predicate", "") not in RELATION_PREDICATES:
            continue
        if a.get("object_type") != "entity_id":
            continue
        rows.append({
            "relation_id": f"R{n:04d}",
            "subject_entity_id": a.get("subject_entity_id", ""),
            "relation_type": a.get("predicate", ""),
            "object_entity_id": a.get("object_value", ""),
            "start_date": a.get("event_date", ""),
            "source_basis": a.get("source_url", ""),
            "status": a.get("status", "seeded") or "seeded",
            "last_updated": a.get("last_updated", ""),
            "notes": a.get("notes", ""),
        })
        n += 1
    return rows

def build_timeline(assertions):
    rows = []
    n = 1
    for a in assertions:
        event_date = a.get("event_date", "")
        if not event_date:
            continue
        title = a.get("event_title", "") or a.get("object_value", "") or a.get("predicate", "")
        summary = a.get("event_summary", "")
        rows.append({
            "timeline_id": f"T{n:04d}",
            "entity_id": a.get("subject_entity_id", ""),
            "event_date": event_date,
            "event_type": a.get("predicate", ""),
            "event_title": title,
            "event_summary": summary,
            "source_url": a.get("source_url", ""),
            "source_type": a.get("source_type", "reference") or "reference",
            "status": a.get("status", "seeded") or "seeded",
            "last_updated": a.get("last_updated", ""),
        })
        n += 1
    return rows

def write_csv(path: Path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="Build wiki relation/timeline views from assertions")
    parser.add_argument("--assertions", default="wiki/index/assertions.csv")
    parser.add_argument("--relations-out", default="wiki/index/relations.csv")
    parser.add_argument("--timeline-out", default="wiki/index/history_timeline.csv")
    args = parser.parse_args()

    assertions = read_assertions(Path(args.assertions))
    rel_rows = build_relations(assertions)
    tl_rows = build_timeline(assertions)

    write_csv(Path(args.relations_out), [
        "relation_id","subject_entity_id","relation_type","object_entity_id","start_date","source_basis","status","last_updated","notes"
    ], rel_rows)
    write_csv(Path(args.timeline_out), [
        "timeline_id","entity_id","event_date","event_type","event_title","event_summary","source_url","source_type","status","last_updated"
    ], tl_rows)

    print(f"assertions={len(assertions)}")
    print(f"relations={len(rel_rows)}")
    print(f"timeline={len(tl_rows)}")

if __name__ == "__main__":
    main()
