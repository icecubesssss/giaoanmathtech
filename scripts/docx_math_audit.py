"""Đổi THỬ toàn bộ công thức của kho seed sang Equation Word, báo công thức hỏng.

    .venv/bin/python -m scripts.docx_math_audit [--show 40]

Chạy trước khi tin bộ đổi (bài học formula-flow: "không báo lỗi ≠ đúng"). Kết quả
in theo nhóm lý do + vài ví dụ + file chứa, để sửa luật tiền xử lý trong
`src/compiler/omml.py` cho tới khi kho sạch.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

from config import settings
from src.compiler.docx_text import formulas_in
from src.compiler.omml import convert_many

SKIP_KEYS = {"tikz", "image", "video", "slug", "id", "source_refs"}


def walk(node, key=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in SKIP_KEYS:
                continue
            yield from walk(v, k)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, key)
    elif isinstance(node, str):
        yield key, node


def collect(root: Path) -> dict[str, set[str]]:
    found: dict[str, set[str]] = collections.defaultdict(set)
    for f in sorted(root.rglob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for key, s in walk(data):
            forms = [s] if key == "latex" else formulas_in(s)
            for fm in forms:
                found[fm].add(str(f.relative_to(settings.ROOT)))
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(settings.ROOT / "inputs" / "seeds"))
    ap.add_argument("--show", type=int, default=25)
    a = ap.parse_args(argv)
    found = collect(Path(a.root))
    print(f"{len(found)} công thức khác nhau")
    res = convert_many(list(found))
    bad = {tex: why for tex, (el, why) in res.items() if el is None}
    print(f"HỎNG: {len(bad)}")
    by = collections.defaultdict(list)
    for tex, why in bad.items():
        by[why.split(" ")[0] if why.startswith("còn sót") is False else why].append(tex)
    for why, items in sorted(by.items(), key=lambda kv: -len(kv[1])):
        print(f"\n== {why}: {len(items)}")
        for tex in items[:a.show]:
            print(f"   {tex[:140]!r}  ← {sorted(found[tex])[0]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
