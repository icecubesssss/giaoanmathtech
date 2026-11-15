#!/usr/bin/env python3
"""Kết quả việc gan-dang-l<lop>-<ky> (Gemini) ⇒ inputs/refs/ngan-hang-sheet/lop-<lop>/<ky>/bo-de.json
cho scripts/phu_dang_gate.py (mỗi đề một danh sách "=Dxx").

    python3 scripts/gemini/lap_bo_de_tu_gan_dang.py --lop 9 --ky ck1
In kèm bảng từng ý để Claude soát mã dạng trước khi tin cổng.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def khoa(ten: str) -> str:
    m = re.search(r"so-(\d+)", ten) or re.search(r"de-(\d+)", ten)
    so = m.group(1) if m else ten
    return ("on" if "on-tap" in ten else "ct") + so


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", type=int, required=True)
    ap.add_argument("--ky", required=True)
    a = ap.parse_args()
    ds = []
    for p in sorted((REPO / "storage/gemini/xong").glob(f"gan-dang-l{a.lop}-{a.ky}-*.json")):
        kq = json.loads(p.read_text())
        kq = kq.get("ket_qua") or kq.get("structured_output") or kq
        ds += kq["de"]
    bo = {}
    for de in ds:
        k = khoa(de["file"])
        bo[k] = [f"={y['dang']}" for y in de["y"]]
        print(f"\n## {k} ({de['file']}) — {len(de['y'])} ý")
        for y in de["y"]:
            print(f"  {y['nhan']:8s} {y['dang']} {y['muc']:3s} {y.get('diem', '')!s:5s} {y['nd'][:60]}"
                  + (f"  ⚠ {y['can_soat']}" if y.get("can_soat") else ""))
    ra = REPO / f"inputs/refs/ngan-hang-sheet/lop-{a.lop}/{a.ky}/bo-de.json"
    ra.parent.mkdir(parents=True, exist_ok=True)
    ra.write_text(json.dumps(bo, ensure_ascii=False, indent=1))
    print(f"\nĐã ghi {ra.relative_to(REPO)}")


if __name__ == "__main__":
    main()
