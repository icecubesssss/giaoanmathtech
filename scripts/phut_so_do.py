#!/usr/bin/env python3
"""PHÚT HS C LÀM BÀI CÓ SƠ ĐỒ NGƯỢC, tính từ chính bài đó (Thầy 05/11/2026).

Thầy: "dựa vào bài toán đó bình thường HS mất bao nhiêu phút, xong trừ đi vì được hướng dẫn và có ý
tưởng sẵn … dùng công thức trung bình chứ không dùng cảm nhận".

    bình thường = đọc đề + vẽ hình + Σ ý [nghĩ(mức ý) + số dòng lời giải(dạng ý) × phút/dòng]   (scripts/phut_chuan_bc.py)
    có sơ đồ    = đọc đề + đọc sơ đồ (số kí tự / tốc độ đọc) + Σ ý [số dòng × phút/dòng]
Bỏ phần nghĩ vì sơ đồ đã cho ý tưởng, thêm phần đọc sơ đồ. Vẽ hình tính riêng (`ve_tiep`, `draw`), không
cộng ở đây. Mọi tham số lấy ở config/phut_thuc.json.

Dùng:
    .venv/bin/python scripts/phut_so_do.py <phiếu.json>          # in bảng
    .venv/bin/python scripts/phut_so_do.py <phiếu.json> --ghi    # ghi `phut_so_do` vào các bài
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from phut_chuan_bc import P, phut_bai  # noqa: E402
from src.compiler.jinja_renderer import plainlen  # noqa: E402

_NUT = re.compile(r"\\node\[[^\]]*\]\s*\(\w+\)\s*at\s*\([^)]*\)\s*\{(.*)\};")
_THE = re.compile(r"\[(?:NB|TH|VD|VDC)\]\s*")


def so_ki_tu_so_do(tikz: str) -> int:
    """Số kí tự HS phải đọc trong các ô của sơ đồ."""
    return sum(plainlen(m.group(1).replace(r"\\", " ")) for m in _NUT.finditer(tikz))


def phut_co_so_do(statement: str, tikz: str, muc: str, luat: list[dict], tang: str = "C") -> dict:
    # Luật dạng ý (config/khung-phan-dang) dò kí hiệu ∥, đề phiếu viết bằng mã LaTeX.
    de = _THE.sub("", statement).split(" Vẽ tiếp")[0].replace(r"\parallel", "∥")
    thuong = phut_bai({"de": de, "muc_y": "", "band": muc, "fmt": "Tự luận"}, tang, luat)
    t = P["tang"][tang]
    nghi = t["nghi"][muc] * len(thuong["y"])
    viet = sum(thuong["y"]) - nghi
    doc_so_do = so_ki_tu_so_do(tikz) / t["doc_ky_tu_phut"]
    return {"binh_thuong": round(thuong["doc"] + thuong["ve"] + sum(thuong["y"]), 1), "doc": thuong["doc"],
            "ve": thuong["ve"], "nghi": nghi, "doc_so_do": round(doc_so_do, 1), "viet": round(viet, 1),
            "phut": round(thuong["doc"] + doc_so_do + viet, 1)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("phieu")
    ap.add_argument("--khung", default="config/khung-phan-dang/lop-9-hinh-hoc-chuong-05.json")
    ap.add_argument("--ghi", action="store_true")
    a = ap.parse_args()
    luat = json.loads((ROOT / a.khung).read_text("utf-8"))["dang_y"]
    f = Path(a.phieu)
    raw = f.read_text("utf-8")
    d = json.loads(raw)
    muc_cua = {1: "NB", 2: "TH", 3: "VD", 4: "VDC"}
    for st in d["stages"]:
        for b in st["blocks"]:
            if b.get("type") != "problem" or not b.get("so_do_nguoc"):
                continue
            k = phut_co_so_do(b["statement"], b["so_do_nguoc"], muc_cua[b.get("level", 2)], luat)
            print(f"{b['label']:9s} bình thường {k['binh_thuong']}′ (đọc {k['doc']} + vẽ {k['ve']} + nghĩ {k['nghi']} + viết {k['viet']})"
                  f" → có sơ đồ {k['phut']}′ (đọc {k['doc']} + đọc sơ đồ {k['doc_so_do']} + viết {k['viet']}), chưa gồm vẽ")
            if a.ghi:
                b["phut_so_do"] = k["phut"]
    if a.ghi:
        f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""), "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
