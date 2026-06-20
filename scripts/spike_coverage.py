#!/usr/bin/env python3
"""SPIKE de-risk (Bước 2): bank có đủ câu để 'bốc' cho 1 phiếu tầng không?

Đối chiếu SỐ CÂU MỤC TIÊU (tier_spec) với SỐ CÂU CÓ trong ngân hàng đề
(inputs/refs/de-thi/lop-9/exams/*.json) theo dạng, để thấy GAP → từ đó biết
phần thiếu phải bù bằng scaffold-decompose (Thầy chốt), không bịa.

Chạy:  python scripts/spike_coverage.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # chạy trực tiếp được
from config import settings
from src.schema.tier_spec import load_tier_spec, target_counts, BANDS

EXAMS = settings.ROOT / "inputs/refs/de-thi/lop-9/exams"
# Phiếu [C]tuan10-11 = BPT (chương C2): 2 dạng chính.
BPT_DANG = {"DS-BPT-GIAI", "DS-THUCTE-LAPPT-BPT"}


def load_bank_cau() -> list[dict]:
    cau = []
    for j in sorted(EXAMS.glob("*.json")):
        try:
            data = json.loads(j.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for c in data.get("cau", []):
            c["_exam"] = j.stem
            cau.append(c)
    return cau


def main() -> None:
    spec = load_tier_spec()
    d2b = spec["do_kho_to_band"]

    print("═" * 64)
    print("SPIKE COVERAGE — phiếu BPT lớp C (lop-9/dai-so, tầng C)")
    print("═" * 64)

    tc = target_counts(spec, "lop-9", "dai-so", "C")
    totals = {b: sum(seg.get(b, 0) for seg in tc.values()) for b in BANDS}
    print("\n① SỐ CÂU MỤC TIÊU / phiếu (tier_spec, gồm cả ví dụ+luyện+BTVN):")
    for seg, bands in tc.items():
        print(f"   {seg:<8} " + " · ".join(f"{b} {n}" for b, n in bands.items()))
    print(f"   TỔNG     " + " · ".join(f"{b} {totals[b]}" for b in BANDS if totals[b]))

    cau = load_bank_cau()
    bpt = [c for c in cau if set(c.get("dang", [])) & BPT_DANG]
    by_band = Counter(d2b.get(str(c.get("do_kho", "")), "?") for c in bpt)
    by_dang = Counter(d for c in bpt for d in c.get("dang", []) if d in BPT_DANG)

    print(f"\n② BANK CÓ (dạng BPT, {len(cau)} câu toàn bank → {len(bpt)} câu BPT):")
    for dang, n in by_dang.most_common():
        print(f"   {dang:<22} {n} câu")
    print("   theo band (do_kho→band tạm):  " +
          " · ".join(f"{b} {by_band.get(b, 0)}" for b in BANDS))

    print("\n③ GAP (mục tiêu − bank) — phần thiếu bù bằng SCAFFOLD-DECOMPOSE:")
    for b in BANDS:
        if not totals.get(b):
            continue
        have = by_band.get(b, 0)
        gap = totals[b] - have
        flag = "→ decompose/bù" if gap > 0 else "đủ"
        print(f"   {b:<4} cần {totals[b]:>3} | bank {have:>3} | thiếu {max(gap,0):>3}  {flag}")

    print("\n KẾT LUẬN: bank BPT rất mỏng so với quỹ câu lớp C (đặc biệt NB) →")
    print(" 'bốc thuần' KHÔNG đủ; phải bốc bài giàu rồi CẮT BƯỚC sinh NB/TH (Thầy chốt).")


if __name__ == "__main__":
    main()
