#!/usr/bin/env python3
"""Phiếu D ch.VI 9C (13/11/2026) — bù giờ: chèn bài TH mới, đánh lại số bài.

Trên lớp 72′/120 ⇒ chèn "Bài 9." (TH, 5 ý đề thật) sau Bài 8, đẩy Bài 9→10, 10→11.
BTVN 78′/90  ⇒ chèn "Bài 20." (TH, 2 ý) sau Bài 18 cũ, đẩy 11..18 → 12..19, 19→21, 20→22.
Khối mới chỉ là chỗ giữ (statement "(chờ Gemini)") — nội dung do viec_bu_gio_phieu_d_9c.py giao Gemini.
Script CHẠY MỘT LẦN: dừng nếu thấy đã có nhãn "Bài 22.".

    python3 scripts/gemini/doi_so_phieu_d_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = REPO / ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
               "phieu-d-tinh-gia-tri-bieu-thuc-chua-hai-nghiem.json")

MAP = {9: 10, 10: 11, **{n: n + 1 for n in range(11, 19)}, 19: 21, 20: 22}

# (kind stage, trường, chuỗi cũ, chuỗi mới) — chỉ những chỗ nhắc số bài CỦA PHIẾU (không đụng "Bài 20" SGK)
DOI_CHU = [
    ("review", "teacher_note", "để dành cho Bài 10.", "để dành cho Bài 11."),
    ("review", "opener", "Đây là Bài 10 — bài cuối", "Đây là Bài 11 — bài cuối"),
    ("practice1", "para0", "\\textbf{Đích của buổi học:} Bài 10 —", "\\textbf{Đích của buổi học:} Bài 11 —"),
    ("practice1", "para0", "Mạch 4 dùng cho Bài 9.", "Mạch 4 dùng cho Bài 10."),
    ("practice2", "teacher_note",
     "Khoảng 60 phút, Bài 7 và Bài 8 mỗi ý khoảng 6 phút. Bài 9 và Bài 10 là hai đề thật (THCS Tự Lập, đề Hà Nội 2026), làm cá nhân rồi gọi lên bảng. Bài 10 là đích của buổi học.",
     "Khoảng 95 phút, Bài 7, Bài 8 và Bài 9 mỗi ý khoảng 6 phút (Bài 9 gồm các đề thật, chữa theo cặp). Bài 10 và Bài 11 là hai đề thật (THCS Tự Lập, đề Hà Nội 2026), làm cá nhân rồi gọi lên bảng. Bài 11 là đích của buổi học."),
    ("reflection", "teacher_note",
     "Bài tập về nhà gồm Bài 11 đến Bài 20, in thành phiếu riêng, khoảng 85 phút. Buổi sau chữa Bài 19 và Bài 20 trước.",
     "Bài tập về nhà gồm Bài 12 đến Bài 22, in thành phiếu riêng, khoảng 90 phút. Buổi sau chữa Bài 21 và Bài 22 trước."),
]


def cho(label, tier):
    return {"type": "problem", "label": label, "level": 2, "tier": tier,
            "statement": "(chờ Gemini)", "solution": "", "hints": [], "writelines": 0}


def main():
    d = json.loads(SEED.read_text())
    nhan = [b.get("label") for s in d["stages"] for b in s["blocks"] if b.get("type") == "problem"]
    if "Bài 22." in nhan:
        sys.exit("Đã đánh số lại rồi — dừng.")
    st = {s["kind"]: s for s in d["stages"]}
    for s in d["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                n = int(b["label"][4:-1])
                if n in MAP:
                    b["label"] = f"Bài {MAP[n]}."
    # chèn chỗ giữ
    p2 = st["practice2"]["blocks"]
    i = next(k for k, b in enumerate(p2) if b.get("label") == "Bài 8.")
    p2.insert(i + 1, cho("Bài 9.", "onclass"))
    rf = st["reflection"]["blocks"]
    i = next(k for k, b in enumerate(rf) if b.get("label") == "Bài 19.")
    rf.insert(i + 1, cho("Bài 20.", "btvn"))
    # chữ
    for kind, truong, cu, moi in DOI_CHU:
        if truong == "teacher_note":
            obj, key = st[kind], "teacher_note"
        elif truong == "opener":
            obj, key = st[kind]["blocks"][0], "text"
        else:
            obj, key = st[kind]["blocks"][0], "text"
        assert obj[key].count(cu) == 1, (kind, truong, cu[:40])
        obj[key] = obj[key].replace(cu, moi)
    moi = [b.get("label") for s in d["stages"] for b in s["blocks"] if b.get("type") == "problem"]
    assert moi == [f"Bài {n}." for n in range(1, 23)], moi
    print("Thứ tự mới:", " ".join(x[4:-1] for x in moi))
    if "--ghi" in sys.argv:
        SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        print("Đã ghi", SEED.relative_to(REPO))


if __name__ == "__main__":
    main()
