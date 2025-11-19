#!/usr/bin/env python3
"""Normalize JSON formatting for workflow exports."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def format_json_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    formatted = json.dumps(data, indent=2, ensure_ascii=False)
    if not formatted.endswith("\n"):
        formatted += "\n"
    if formatted == text:
        return False
    path.write_text(formatted, encoding="utf-8")
    return True


def main() -> None:
    json_files = sorted(ROOT.rglob("*.json"))
    updated = 0
    for json_file in json_files:
        if json_file.name == "package-lock.json":
            continue
        try:
            changed = format_json_file(json_file)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Failed to parse {json_file}: {exc}")
        if changed:
            updated += 1
    print(f"Formatted {updated} JSON file(s).")


if __name__ == "__main__":
    main()
