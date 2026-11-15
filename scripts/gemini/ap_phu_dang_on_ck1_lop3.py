#!/usr/bin/env python3
"""Áp kết quả việc Gemini pd3-on1..3 vào scripts/de_ck1_lop3.py + bản ghi đề trung tâm.

    .venv/bin/python scripts/gemini/ap_phu_dang_on_ck1_lop3.py          # xem diff
    .venv/bin/python scripts/gemini/ap_phu_dang_on_ck1_lop3.py --ghi    # ghi
"""
import difflib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/de_ck1_lop3.py"
XONG = REPO / "storage/gemini/xong"
BG = REPO / "inputs/refs/ngan-hang-sheet/tieu-hoc/lop-3/ban-ghi"
TEN_TT = {"tt-kntt01": "T3 - HKI - KNTT - 01.pdf", "tt-kntt02": "T3 - HKI - KNTT - 02.pdf"}


def khoi(src, k):
    """(đầu, cuối) của khối DE["k"]: từ dòng DE["k"] = tới trước dòng chú thích/DE kế tiếp ở đầu dòng."""
    m = re.search(rf'^DE\["{k}"\] = ', src, re.M)
    n = re.search(r'^(# -{10,}|# ={10,}|DE\[)', src[m.end():], re.M)
    return m.start(), m.end() + n.start()


def main():
    ghi = "--ghi" in sys.argv
    src = SCRIPT.read_text()
    moi = src
    tt = {}
    for k in ("on1", "on2", "on3"):
        f = XONG / f"pd3-{k}.json"
        if not f.exists():
            print(f"thiếu {f.name}")
            continue
        kq = json.loads(f.read_text())["ket_qua"]
        a, b = khoi(moi, k)
        moi = moi[:a] + kq["code"].strip() + "\n\n" + moi[b:]
        for c in kq["tt_cau"]:
            tt.setdefault(c["de"], {})[c["cau"]] = {x: c[x] for x in ("cau", "nd", "ht", "diem", "dap_an", "muc", "cd", "bai", "dang")}
        print(f"── {k} ghi_chu: {kq['ghi_chu']}")
    sys.stdout.writelines(difflib.unified_diff(src.splitlines(True), moi.splitlines(True), "cu", "moi", n=0))
    for de, cs in tt.items():
        p = BG / f"l3-{de}.json"
        cu = json.loads(p.read_text())["cau"] if p.exists() else []
        gop = {c["cau"]: c for c in cu} | cs
        d = {"de": f"l3-{de}", "file": f"inputs/refs/de-thi/lop-3/de-trung-tam/{TEN_TT[de]}", "da_soi_anh": True,
             "ghi_chu_de": "Đề trung tâm MathTech (không phải đề trường) — chỉ bóc các câu đề ôn dùng tới; không tính vào % đề trường.",
             "cau": sorted(gop.values(), key=lambda c: c["cau"])}
        print(f"bản ghi {p.name}: {json.dumps(d['cau'], ensure_ascii=False)[:600]}")
        if ghi:
            p.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    if ghi:
        SCRIPT.write_text(moi)
        print("ĐÃ GHI")


if __name__ == "__main__":
    main()
