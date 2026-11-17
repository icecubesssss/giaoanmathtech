#!/usr/bin/env python3
"""Cắt phiếu 8.2 (phiếu B ch.VIII 9C) về 135′ để nhường 45′ kiểm tra gộp VII+VIII (15/11/2026).

Thao tác CƠ HỌC (không viết chữ nội dung — phần chữ giao Gemini ở viec_cat_phieu_8b_9c.py):
  - khai `kiem_tra_phut: 45`, `btvn_phieu_rieng: true` (ngay sau `so_ca`);
  - bỏ Bài 5 (NB, BTVN Bài 22 cùng dạng), Bài 14 (TH ghép số, BTVN Bài 31 cùng dạng),
    Bài 17 (VD lấy đồng thời — trùng nguyên văn Ví dụ 8; BTVN Bài 34 cùng dạng);
  - Luyện tập 1 chia 3 mạch (para heading, chữ tạm "(chờ Gemini)"), Bài 10 (điền khuyết) lên trước Bài 9;
  - BTVN: Bài 27 (điền khuyết) lên đầu BTVN (cổng chọn → điền → trình bày);
  - đánh số lại nhãn "Bài N.".
Chạy MỘT lần trên seed gốc:  python3 scripts/gemini/cat_phieu_8b_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = REPO / ("inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/"
               "phieu-b-phep-thu-hai-hanh-dong-va-luyen-tap-chung.json")
BO = {"Bài 5.", "Bài 14.", "Bài 17."}


def heading(n):
    return {"type": "para", "variant": "heading", "text": f"Mạch {n}. (chờ Gemini)"}


def main():
    d = json.loads(SEED.read_text())
    assert "kiem_tra_phut" not in d, "seed đã cắt rồi — không chạy lại"
    d2 = {}
    for k, v in d.items():
        d2[k] = v
        if k == "so_ca":
            d2["kiem_tra_phut"] = 45
            d2["btvn_phieu_rieng"] = True
    d = d2
    st = d["stages"]
    for s in st:
        s["blocks"] = [b for b in s["blocks"] if b.get("label") not in BO]

    def tim(blocks, nhan=None, vidu=None):
        for i, b in enumerate(blocks):
            if nhan and b.get("label") == nhan:
                return i
            if vidu and b.get("type") == "noted" and b.get("text", "").startswith(r"\textbf{Ví dụ %d." % vidu):
                return i
        raise KeyError(nhan or vidu)

    # Luyện tập 1: mạch 1 trước Ví dụ 1, mạch 2 trước Ví dụ 3, mạch 3 = Bài 10, Bài 9, Bài 11
    lt1 = st[2]["blocks"]
    b10 = lt1.pop(tim(lt1, "Bài 10."))
    lt1.insert(tim(lt1, "Bài 9."), b10)
    lt1.insert(tim(lt1, "Bài 10."), heading(3))
    lt1.insert(tim(lt1, vidu=3), heading(2))
    lt1.insert(tim(lt1, vidu=1), heading(1))

    # BTVN: Bài 27 lên đầu
    tk = st[4]["blocks"]
    b27 = tk.pop(tim(tk, "Bài 27."))
    tk.insert(tim(tk, "Bài 18."), b27)

    # Đánh số lại
    n = 0
    doi = {}
    for s in st:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                n += 1
                doi[b["label"]] = f"Bài {n}."
                b["label"] = f"Bài {n}."
    for cu, moi in doi.items():
        if cu != moi:
            print(f"  {cu:9s} → {moi}")
    print("Tổng bài:", n)
    if "--ghi" in sys.argv:
        SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2))
        print("Đã ghi", SEED.relative_to(REPO))


if __name__ == "__main__":
    main()
