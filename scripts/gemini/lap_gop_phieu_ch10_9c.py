#!/usr/bin/env python3
"""Ráp 2 kết quả Gemini (gop-9c-ch10-p1-tren-lop + gop-9c-ch10-p1-btvn) thành seed phiếu A gộp ch.X 9C.

    python3 scripts/gemini/lap_gop_phieu_ch10_9c.py

Chuẩn hoá máy móc sau khi ráp: bỏ writelines, ép tier theo chặng, đánh số Hình 1..N theo thứ tự
xuất hiện, báo khối nào còn minipage/adjustbox (Gemini quên tách hình).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien"
OUT = REPO / D / "phieu-a-hinh-tru-hinh-non-hinh-cau.json"


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    data = kq.get("ket_qua") or kq
    if data.get("ghi_chu"):
        print(f"[{vid}] ghi_chu Gemini: {data['ghi_chu']}")
    return data["stages"]


def main():
    st = lay("gop-9c-ch10-p1-tren-lop") + lay("gop-9c-ch10-p1-btvn")
    assert [s["number"] for s in st] == [1, 2, 3, 4, 5], [s["number"] for s in st]
    canh_bao = 0
    hinh = 0
    for s in st:
        s["blocks"] = [b for b in s["blocks"] if b.get("type") != "writelines"]
        for b in s["blocks"]:
            if b.get("type") == "problem":
                b["tier"] = "btvn" if s["kind"] == "reflection" else "onclass"
                b.pop("writelines", None)
            fig = b.get("figure")
            if isinstance(fig, dict) and (fig.get("tikz") or fig.get("image")):
                hinh += 1
                cu = fig.get("caption", "")
                fig["caption"] = f"Hình {hinh}"
                for k in ("statement", "text", "solution"):
                    if cu and cu != fig["caption"] and isinstance(b.get(k), str):
                        b[k] = re.sub(rf"\b{re.escape(cu)}\b(?!\d)", f"Hình {hinh}", b[k])
            for k in ("statement", "text"):
                v = b.get(k, "")
                if isinstance(v, str) and re.search(r"\\begin\{minipage\}|\\adjustbox|\\parbox", v):
                    canh_bao += 1
                    print("⚠ còn minipage/adjustbox/parbox:", b.get("label") or v[:40])
    lesson = {
        "slug": "phieu-a-hinh-tru-hinh-non-hinh-cau",
        "title": "Buổi 1 — Bài 31 $+$ Bài 32: Hình trụ, hình nón, hình cầu",
        "eyebrow": "PHIẾU A • HÌNH HỌC 9 · CHƯƠNG X — BÀI 31 + BÀI 32 (GỘP)",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "so_ca": 1,
        "btvn_phieu_rieng": True,
        "stages": st,
    }
    OUT.write_text(json.dumps(lesson, ensure_ascii=False, indent=2) + "\n")
    print(f"Đã ghi {OUT.relative_to(REPO)} — {hinh} hình, {canh_bao} cảnh báo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
