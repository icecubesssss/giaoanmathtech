#!/usr/bin/env python3
"""Cập nhật toàn bộ Ví dụ mẫu và Khám phá cho Chương V Toán 9C theo yêu cầu của Thầy:
1. Phóng to hình Khám phá Phiếu 3 (bồn hoa) để HS dùng thước và đo góc trực tiếp.
2. Tách câu và gắn nhãn [NB] ★, [TH] ★★, [VD] ★★★ cho mọi ý a), b), c) trong Ví dụ mẫu.
3. Đồng bộ hoàn chỉnh giữa đề và lời giải mẫu.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH5_DIR = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"


def update_phieu_1():
    fpath = CH5_DIR / "phieu-1-do-dai-cung-dien-tich-quat-vanh-khuyen.json"
    d = json.loads(fpath.read_text(encoding="utf-8"))
    
    # Ví dụ 1 (S3 B2)
    b2 = d["stages"][2]["blocks"][1]
    b2["text"] = b2["text"].replace(
        "a) Tính số đo cung nhỏ $AB$.[[br]]b) Tính số đo cung lớn $AB$.",
        "a) [NB] ★ Tính số đo cung nhỏ $AB$.[[br]]b) [NB] ★ Tính số đo cung lớn $AB$."
    )
    
    # Ví dụ 3 (S3 B9)
    b9 = d["stages"][2]["blocks"][8]
    b9["text"] = b9["text"].replace(
        "a) Tính độ dài cung của hình quạt.[[br]]b) Tính diện tích của hình quạt.",
        "a) [NB] ★ Tính độ dài cung của hình quạt.[[br]]b) [NB] ★ Tính diện tích của hình quạt."
    )
    
    fpath.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-1 examples")


def update_phieu_2():
    fpath = CH5_DIR / "phieu-2-bon-diem-cung-thuoc-duong-tron-tiep-tuyen.json"
    d = json.loads(fpath.read_text(encoding="utf-8"))
    
    # Ví dụ 1 (S3 B5)
    v1 = d["stages"][2]["blocks"][4]
    v1["text"] = v1["text"].replace(
        "a) Chứng minh tam giác $BEC$ và tam giác $BFC$ là các tam giác vuông.[[br]]b) Chứng minh bốn điểm $B$, $C$, $E$, $F$ cùng thuộc một đường tròn.",
        "a) [NB] ★ Chứng minh tam giác $BEC$ và tam giác $BFC$ là các tam giác vuông.[[br]]b) [NB] ★ Chứng minh bốn điểm $B$, $C$, $E$, $F$ cùng thuộc một đường tròn."
    )
    
    # Ví dụ 2 (S3 B8)
    v2 = d["stages"][2]["blocks"][7]
    v2["text"] = v2["text"].replace(
        "a) Chứng minh $OC$ là đường trung trực của đoạn thẳng $AB$.[[br]]b) Chứng minh $\\triangle OAC = \\triangle OBC$.[[br]]c) Chứng minh rằng $CB$ là tiếp tuyến của $(O)$.",
        "a) [TH] ★★ Chứng minh $OC$ là đường trung trực của đoạn thẳng $AB$.[[br]]b) [TH] ★★ Chứng minh $\\triangle OAC = \\triangle OBC$.[[br]]c) [TH] ★★ Chứng minh rằng $CB$ là tiếp tuyến của $(O)$."
    )
    
    fpath.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-2 examples")


def update_phieu_3():
    fpath = CH5_DIR / "phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json"
    d = json.loads(fpath.read_text(encoding="utf-8"))
    
    # 1. Phóng to hình Khám phá (S1 B2)
    kp = d["stages"][0]["blocks"][1]
    kp["figure"]["width"] = "0.82"
    kp["figure"]["tikz"] = (
        r"\begin{tikzpicture}[line width=0.9pt, font=\normalsize, scale=1.15]" + "\n"
        r"  \draw[ink, thick] (0,0) circle (2.4);" + "\n"
        r"  \draw[ink, thick] (5.6,0) -- (1.0286, 2.1684);" + "\n"
        r"  \draw[ink, thick] (5.6,0) -- (1.0286, -2.1684);" + "\n"
        r"  \draw[ink] (0,0) -- (1.0286, 2.1684);" + "\n"
        r"  \draw[ink] (0,0) -- (1.0286, -2.1684);" + "\n"
        r"  \draw[ink, dashed] (0,0) -- (5.6,0);" + "\n"
        r"  \fill[ink] (0,0) circle (1.8pt);" + "\n"
        r"  \fill[ink] (5.6,0) circle (1.8pt);" + "\n"
        r"  \fill[ink] (1.0286, 2.1684) circle (1.8pt);" + "\n"
        r"  \fill[ink] (1.0286, -2.1684) circle (1.8pt);" + "\n"
        r"  \node[left=3pt] at (0,0) {$O$};" + "\n"
        r"  \node[right=3pt] at (5.6,0) {$A$};" + "\n"
        r"  \node[above=4pt] at (1.0286, 2.1684) {$B$};" + "\n"
        r"  \node[below=4pt] at (1.0286, -2.1684) {$C$};" + "\n"
        r"  \path (-2.8, -2.8) rectangle (6.2, 2.8);" + "\n"
        r"\end{tikzpicture}"
    )
    
    # 2. Ví dụ 1 (S3 B5)
    v1 = d["stages"][2]["blocks"][4]
    v1["text"] = v1["text"].replace(
        "a) Chứng minh $OM$ là đường trung trực của đoạn thẳng $AB$.[[br]]b) Chứng minh rằng $OM \\perp AB$.",
        "a) [TH] ★★ Chứng minh $OM$ là đường trung trực của đoạn thẳng $AB$.[[br]]b) [TH] ★★ Chứng minh rằng $OM \\perp AB$."
    )
    
    # 3. Ví dụ 2 (S3 B8)
    v2 = d["stages"][2]["blocks"][7]
    v2["text"] = v2["text"].replace(
        "a) Chứng minh $OC \\perp AD$.[[br]]b) Chứng minh $BD \\perp AD$.[[br]]c) Chứng minh $OC \\parallel BD$.",
        "a) [TH] ★★ Chứng minh $OC \\perp AD$.[[br]]b) [TH] ★★ Chứng minh $BD \\perp AD$.[[br]]c) [TH] ★★ Chứng minh $OC \\parallel BD$."
    )
    
    fpath.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-3 khampha & examples")


def update_phieu_4():
    fpath = CH5_DIR / "phieu-4-chung-minh-he-thuc-tich-bang-dong-dang.json"
    d = json.loads(fpath.read_text(encoding="utf-8"))
    
    # Ví dụ 1 (S3 B9)
    v1 = d["stages"][2]["blocks"][8]
    v1["text"] = v1["text"].replace(
        "a) Chứng minh $\\triangle BEH \\backsim \\triangle BDA$.[[br]]b) Chứng minh $BE \\cdot BA = BH \\cdot BD$.",
        "a) [TH] ★★ Chứng minh $\\triangle BEH \\backsim \\triangle BDA$.[[br]]b) [TH] ★★ Chứng minh $BE \\cdot BA = BH \\cdot BD$."
    )
    
    # Ví dụ 2 (S3 B12)
    v2 = d["stages"][2]["blocks"][11]
    v2["text"] = v2["text"].replace(
        "a) Chứng minh $OA \\perp BC$ tại $H$.[[br]]b) Chứng minh $OH \\cdot OA = R^2$.",
        "a) [TH] ★★ Chứng minh $OA \\perp BC$ tại $H$.[[br]]b) [TH] ★★ Chứng minh $OH \\cdot OA = R^2$."
    )
    
    fpath.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-4 examples")


def update_phieu_5():
    fpath = CH5_DIR / "phieu-5-luyen-tap-chung.json"
    d = json.loads(fpath.read_text(encoding="utf-8"))
    
    # Ví dụ 1 (S3 B6)
    v1 = d["stages"][2]["blocks"][5]
    v1["text"] = v1["text"].replace(
        "a) Chứng minh $MA = MP$ và $NB = NP$.[[br]]b) Chứng minh rằng $MN = MA + NB$.",
        "a) [NB] ★ Chứng minh $MA = MP$ và $NB = NP$.[[br]]b) [TH] ★★ Chứng minh rằng $MN = MA + NB$."
    )
    
    # Ví dụ 2 (S3 B9)
    v2 = d["stages"][2]["blocks"][8]
    v2["text"] = v2["text"].replace(
        "a) Chứng minh tam giác $COD$ vuông tại $O$.[[br]]b) Chứng minh $MC \\cdot MD = OM^2$.",
        "a) [TH] ★★ Chứng minh tam giác $COD$ vuông tại $O$.[[br]]b) [TH] ★★ Chứng minh $MC \\cdot MD = OM^2$."
    )
    
    fpath.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-5 examples")


def update_phieu_6():
    fpath = CH5_DIR / "phieu-6-bai-tap-cuoi-chuong-v.json"
    d = json.loads(fpath.read_text(encoding="utf-8"))
    
    # Ví dụ 1 (S3 B5)
    v1 = d["stages"][2]["blocks"][4]
    v1["text"] = v1["text"].replace(
        "a) Chứng minh rằng bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn. Hãy chỉ rõ tâm $O$ của đường tròn này.[[br]]b) Chứng minh $AB \\cdot AE = AC \\cdot AD$.",
        "a) [TH] ★★ Chứng minh rằng bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn. Hãy chỉ rõ tâm $O$ của đường tròn này.[[br]]b) [TH] ★★ Chứng minh $AB \\cdot AE = AC \\cdot AD$."
    )
    
    fpath.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-6 examples")


if __name__ == "__main__":
    update_phieu_1()
    update_phieu_2()
    update_phieu_3()
    update_phieu_4()
    update_phieu_5()
    update_phieu_6()
    print("ALL WORKSHEETS UPDATED SUCCESSFULLY!")
