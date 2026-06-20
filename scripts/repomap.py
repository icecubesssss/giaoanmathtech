#!/usr/bin/env python3
"""Sinh PROJECT_MAP.md — bản đồ codebase TIẾT KIỆM TOKEN cho agent/người.

Quét `src/` bằng `ast` (stdlib, không cần cài gói), trích mỗi module:
dòng docstring đầu + danh sách class/hàm cấp cao kèm CHỮ KÝ. Agent đọc 1 file
map nhỏ thay vì mở từng file → đỡ token mỗi lần điều hướng.

Chạy:  python scripts/repomap.py   (hoặc `make map`)
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["src", "config", "scripts"]
OUT = ROOT / "PROJECT_MAP.md"


def _sig(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    a = node.args
    parts = [arg.arg for arg in a.posonlyargs + a.args]
    if a.vararg:
        parts.append("*" + a.vararg.arg)
    if a.kwonlyargs:
        parts.extend(kw.arg for kw in a.kwonlyargs)
    if a.kwarg:
        parts.append("**" + a.kwarg.arg)
    return f"{node.name}({', '.join(parts)})"


def _first_doc_line(node) -> str:
    doc = ast.get_docstring(node) or ""
    return doc.strip().splitlines()[0].strip() if doc else ""


def _module_entry(py: Path) -> str:
    rel = py.relative_to(ROOT)
    try:
        tree = ast.parse(py.read_text(encoding="utf-8"))
    except SyntaxError:
        return f"### `{rel}`\n_(không parse được)_\n"
    lines = [f"### `{rel}`"]
    doc = _first_doc_line(tree)
    if doc:
        lines.append(f"_{doc}_")
    syms = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            syms.append(f"- **class {node.name}** — {_first_doc_line(node)}".rstrip(" —"))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            d = _first_doc_line(node)
            syms.append(f"- `{_sig(node)}`" + (f" — {d}" if d else ""))
    lines.extend(syms or ["- _(không có symbol công khai)_"])
    return "\n".join(lines) + "\n"


def main() -> None:
    out = ["# PROJECT_MAP — bản đồ codebase (tự sinh bởi `make map`)",
           "> Đọc file này TRƯỚC để biết module nào làm gì, khỏi mở từng file. "
           "Sinh từ `scripts/repomap.py`; KHÔNG sửa tay.\n"]
    for d in SCAN_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        pys = sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts)
        if not pys:
            continue
        out.append(f"\n## {d}/\n")
        out.extend(_module_entry(p) for p in pys)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"✓ {OUT.relative_to(ROOT)} ({len(out)} khối)")


if __name__ == "__main__":
    main()
