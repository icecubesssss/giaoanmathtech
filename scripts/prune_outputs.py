#!/usr/bin/env python3
"""prune_outputs — soi thư mục `outputs/` mồ côi (bản in cũ của phiếu đã đổi tên/xoá).

Vì sao cần: `build` ghi PDF ra `outputs/<đường dẫn seed>/<slug>/`. Đổi tên folder tuần
hay đổi `slug` là engine đẻ thư mục MỚI, thư mục cũ nằm lại nguyên vẹn — mở nhầm bản cũ
lúc nào không hay (AGENTS.md §"Sửa chữ xong phải build lại ĐỦ 3 bản").

    python -m scripts.prune_outputs            # CHỈ liệt kê, không xoá gì
    python -m scripts.prune_outputs --delete   # xoá thật
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEEDS = ROOT / "inputs" / "seeds"
OUTPUTS = ROOT / "outputs"


def expected_dirs() -> dict[str, set[Path]]:
    """slug → các thư mục output hợp lệ (mirror cây seeds, xem src/main.py::_out_root)."""
    exp: dict[str, set[Path]] = {}
    for p in SEEDS.rglob("*.json"):
        try:
            slug = json.loads(p.read_text(encoding="utf-8")).get("slug")
        except Exception:  # noqa: BLE001 — JSON hỏng là việc của validate
            continue
        if isinstance(slug, str) and slug:
            exp.setdefault(slug, set()).add(OUTPUTS / p.parent.relative_to(SEEDS) / slug)
    return exp


def scan() -> tuple[list[Path], list[Path]]:
    """(lạc chỗ — seed còn nhưng đã chuyển folder, mất gốc — không seed nào khớp)."""
    exp = expected_dirs()
    misplaced, gone = [], []
    for d in sorted(OUTPUTS.rglob("*")):
        if not d.is_dir() or not any(d.glob("*.pdf")):
            continue
        if d.name in exp:
            if d not in exp[d.name]:
                misplaced.append(d)
        else:
            gone.append(d)
    return misplaced, gone


def _mb(d: Path) -> float:
    return sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) / 1e6


def main(argv: list[str]) -> int:
    delete = "--delete" in argv
    misplaced, gone = scan()
    exp = expected_dirs()

    if not misplaced and not gone:
        print("✓ outputs/ sạch — không có thư mục mồ côi.")
        return 0

    if misplaced:
        print(f"▲ LẠC CHỖ ({len(misplaced)}) — seed vẫn còn nhưng đã chuyển folder; "
              "build lại ở chỗ mới rồi mới xoá bản cũ:")
        for d in misplaced:
            dest = sorted(exp[d.name])[0]
            print(f"   {_mb(d):6.1f} MB  {d.relative_to(ROOT)}")
            print(f"            → seed nay ở: {dest.relative_to(ROOT)}")
    if gone:
        print(f"\n▲ MẤT GỐC ({len(gone)}) — không seed nào mang slug này nữa:")
        for d in gone:
            print(f"   {_mb(d):6.1f} MB  {d.relative_to(ROOT)}")

    total = sum(_mb(d) for d in misplaced + gone)
    print(f"\nTổng: {len(misplaced) + len(gone)} thư mục · {total:.0f} MB")

    if not delete:
        print("\n(chỉ liệt kê — thêm --delete để xoá thật)")
        return 0

    # Xoá thư mục SÂU TRƯỚC: có trường hợp cả cha lẫn con cùng mồ côi (vd folder tuần
    # chứa PDF lạc + các thư mục phiếu bên trong) — xoá cha trước là con nổ FileNotFound.
    da_xoa = 0
    for d in sorted(misplaced + gone, key=lambda p: len(p.parts), reverse=True):
        if d.exists():
            shutil.rmtree(d)
            da_xoa += 1
    print(f"\n✓ Đã xoá {da_xoa} thư mục.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
