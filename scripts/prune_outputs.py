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

# Windows: console mặc định cp1252, in "✓ ⚠ ′ ▶" là nổ UnicodeEncodeError giữa chừng.
# Ép UTF-8 cho stdout/stderr; máy nào không hỗ trợ thì bỏ qua, không được làm chết chương trình.
for _luong in (sys.stdout, sys.stderr):
    try:
        _luong.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001 — không có reconfigure (bị bọc lại) thì thôi
        pass

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


def scan_obsolete_files() -> list[Path]:
    """Các file ca-*.pdf và sidecar cũ nằm trong folder ĐÃ CÓ bản in tên mô tả (*-Phieu-HS.pdf...)."""
    from src.exporters.ten_file import BAN_IN
    obsolete = []
    for d in sorted(OUTPUTS.rglob("*")):
        if not d.is_dir():
            continue
        pdfs = list(d.glob("*.pdf"))
        has_new = {kind: any(p.stem.endswith("-" + hau_to) for p in pdfs) for kind, hau_to in BAN_IN.items()}
        for p in pdfs:
            if p.name.startswith("ca-"):
                duoi = p.stem.rsplit("-", 1)[-1]
                if has_new.get(duoi, False):
                    obsolete.append(p)
                    for ext in (".tex", ".tex.sha256", ".log", ".aux"):
                        sidecar = d / f"{p.stem}{ext}"
        # Thuyết minh cũ: thuyet-minh.pdf khi đã có thuyet-minh-<khối>-...pdf
        if any(p.name != "thuyet-minh.pdf" and p.name.startswith("thuyet-minh-") for p in pdfs):
            old_tm = d / "thuyet-minh.pdf"
            if old_tm.exists():
                obsolete.append(old_tm)
                for ext in (".tex", ".tex.sha256", ".log", ".aux"):
                    sidecar = d / f"thuyet-minh{ext}"
                    if sidecar.exists():
                        obsolete.append(sidecar)
    return sorted(set(obsolete))


def main(argv: list[str]) -> int:
    delete = "--delete" in argv
    misplaced, gone = scan()
    obsolete_files = scan_obsolete_files()
    exp = expected_dirs()

    if not misplaced and not gone and not obsolete_files:
        print("✓ outputs/ sạch — không có thư mục mồ côi hoặc file trùng lặp cũ.")
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

    if obsolete_files:
        obs_pdf_count = sum(1 for f in obsolete_files if f.suffix == ".pdf")
        obs_mb = sum(f.stat().st_size for f in obsolete_files) / 1e6
        print(f"\n▲ FILE CŨ TRÙNG LẶP ({obs_pdf_count} PDF, {len(obsolete_files)} files, {obs_mb:.1f} MB) — đã có bản in tên mô tả mới (*-Phieu-HS...):")
        for f in obsolete_files[:10]:
            print(f"   {f.relative_to(ROOT)}")
        if len(obsolete_files) > 10:
            print(f"   ... và {len(obsolete_files) - 10} files khác")

    total = sum(_mb(d) for d in misplaced + gone)
    if obsolete_files:
        total += sum(f.stat().st_size for f in obsolete_files) / 1e6
    print(f"\nTổng: {len(misplaced) + len(gone)} thư mục + {len(obsolete_files)} file thừa · {total:.0f} MB")

    if not delete:
        print("\n(chỉ liệt kê — thêm --delete để xoá thật)")
        return 0

    # Xoá file cũ thừa
    da_xoa_files = 0
    for f in obsolete_files:
        if f.exists():
            f.unlink()
            da_xoa_files += 1

    # Xoá thư mục SÂU TRƯỚC: có trường hợp cả cha lẫn con cùng mồ côi (vd folder tuần
    # chứa PDF lạc + các thư mục phiếu bên trong) — xoá cha trước là con nổ FileNotFound.
    da_xoa = 0
    for d in sorted(misplaced + gone, key=lambda p: len(p.parts), reverse=True):
        if d.exists():
            shutil.rmtree(d)
            da_xoa += 1
    print(f"\n✓ Đã xoá {da_xoa} thư mục và {da_xoa_files} file thừa.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
