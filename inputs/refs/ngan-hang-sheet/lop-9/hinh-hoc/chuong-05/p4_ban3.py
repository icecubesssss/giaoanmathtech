#!/usr/bin/env python3
"""Phiếu 4 ch.V 9C — bản đổi đích, Thầy 05/11/2026.

Thầy: lấy góc vuông từ đường kính dễ lẫn với góc nội tiếp chắn nửa đường tròn (SGK 9 tập 2 tr.69, chương IX),
và cảm nhận khuôn đề Tạ Quang Bửu không hay ra. Đọc từng ý đẳng thức tích ở 66 đề Kì I (bảng KY_THUAT):
hai tiếp tuyến, tam giác vuông có sẵn 16 đề (24%); có đường kính 10 đề (15%); hai cát tuyến bắc cầu 4 đề (6%).
Luật bước 2a: dạng < 20% không làm đích ⇒ đích đổi sang OH·OM = R² (đề phường Ba Đình), bỏ phần có đường kính.

Đề soi từ ẢNH: phường Ba Đình 2025 IV.2 a, b · Ngô Gia Tự 2025 IV.2 ý b · Nghĩa Tân GK1 2025 Bài IV ý 2, phần
BE.BA = BH.BD · Cụm 14 2025 Bài 4.2 phần OH.OD = R² của ý b · Chương Mỹ 2024 4.2 ý b ·
Lương Thế Vinh GK1 2025 4.2 phần AE.AB = AD² của ý b · Đống Đa minh hoạ 2025 Đề 03 IV.2 phần OI.OM = R² của ý 2 · Gia Lâm 2024 4.2 a, b · đề lớp 8 Đa Tốn CK2 2023 Câu 9, Tam Hưng CK2 2025 Câu 6.

Dùng lại thư viện hình, sơ đồ ở p4_ban2.py. Chạy lại được:
    .venv/bin/python inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-05/p4_ban3.py
Sau đó chạy scripts/phut_so_do.py <phiếu> --ghi rồi chạy lại script này để chép phút vào thuyết minh.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import p4_ban2 as b2  # noqa: E402
from p3_ban2 import R, h_nen_diem_ngoai, h_nen_duong_kinh_ngang, nen  # noqa: E402
from p3_ban3 import bai, giai_bon_diem, giai_trung_truc, gon_hinh, hai_tt, h_nen_tron_ngang, theo_so_do  # noqa: E402
from p4_ban2 import BR, LG, cao, d, foot, giao, goc, h_cau_giay, h_chuong_my, h_kham_pha, h_mai_dich, h_nen_chuong_my, h_nen_nghia_tan, h_nen_tron, h_nghia_tan, nghia_tan, cau_giay, chuong_my, rong, so_do, xet  # noqa: E402,F401
from scripts.tikz_geo import Fig, polar, tangent_points  # noqa: E402

D_ = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"
PHIEU = D_ / "phieu-4-chung-minh-he-thuc-tich-bang-dong-dang.json"
TM = D_ / "thuyet-minh.json"
R_THE = 1.2

# Đọc từng ý đẳng thức tích ở 66 đề Kì I (GK1 + CK1, đã gộp trùng). Một đề có thể ở hai nhóm.
KY_THUAT = {
    "A. Hai tiếp tuyến, tam giác vuông có sẵn (OH·OA = R², AB² = AH·AO)": [
        "ck1-giang-bien-2025-de01-4.2", "ck1-giang-bien-2025-de02-4.2", "ck1-phuong-ba-dinh-2025-IV2", "ck1-ban-mai-2024-3",
        "ck1-gia-lam-2024-4.2", "ck1-ha-dong-2024-4.2", "ck1-phan-dinh-giot-2024-IV2", "ck1-marie-curie-2025-4",
        "ck1-nguyen-truong-to-2025-IV", "ck1-nhat-tan-2024-4.2", "ck1-ly-thanh-tong-7", "ck1-cum-14-2025-4.2",
        "ck1-hoang-liet-2025-4.2", "ck1-nhat-tan-2025-IV2", "ck1-quoc-oai-2024-4.2", "ck1-duc-giang-2025-IV2"],
    "B. Có đường kính, phải lấy góc vuông từ đường kính": [
        "ck1-giang-vo-2025-IV2", "ck1-xuan-la-2024-4.2", "ck1-ta-quang-buu-2025-IV2", "ck1-nhat-tan-2024-4.2",
        "ck1-nguyen-binh-khiem-2025-4.2", "ck1-dich-vong-42", "ck1-thanh-tri-2024-IV2", "ck1-long-bien-2024-IV2",
        "ck1-cau-dien-42", "ck1-ngo-si-lien-2025-5"],
    "B1 (trong B). Hai cát tuyến, bắc cầu, khuôn đề Tạ Quang Bửu": [
        "ck1-giang-vo-2025-IV2", "ck1-xuan-la-2024-4.2", "ck1-ta-quang-buu-2025-IV2", "ck1-nhat-tan-2024-4.2"],
    "C. Tam giác có đường cao, đường vuông góc đề cho sẵn": [
        "gk1-nghia-tan-2025-IV", "ck1-chuong-my-2024-4.2", "gk1-thanh-quan-2024-IV", "ck1-hoai-duc-2024-4.2",
        "gk1-luong-the-vinh-2025-4.2", "gk1-ai-mo-2025-IV1", "ck1-phuong-ha-dong-42", "ck1-cau-giay-2024-IV2",
        "gk1-luong-the-vinh-2024-4.2"],
    "D. AM·AN = AH·AO, cát tuyến qua tâm": ["ck1-ngoc-thuy-III2", "ck1-nguyen-truong-to-2025-IV"],
    "E. Ý cuối khó": ["ck1-ai-mo-2", "ck1-ly-son-2025-IV2", "ck1-phuc-tho-2024-5", "ck1-nguyen-du-2025-4.2"],
}

PHUT = {"Bài 8": 0, "BTVN 8": 0, "BTVN 9": 0}
if PHIEU.exists():
    for _st in json.loads(PHIEU.read_text("utf-8"))["stages"]:
        for _b in _st["blocks"]:
            if _b.get("phut_so_do"):
                PHUT[_b["label"].rstrip(".")] = _b["phut_so_do"]

GHI_CHU_LT1 = (
    "Hai ví dụ: GV vẽ trên bảng, HS vẽ cùng vào hình nền trên phiếu (Ví dụ 1: hai đường cao $BD$, $CE$; Ví dụ 2: hai tiếp tuyến, các đoạn $OA$, $BC$, $OB$). "
    "Khoảng 52 phút với lớp C theo định mức: Bài 1 đến Bài 4 đổi tích ra tỉ lệ thức rồi đọc ra hai tam giác (tử số cùng một tam giác, mẫu số cùng một tam giác) ~10′, "
    "Bài 5 đến Bài 7 trắc nghiệm đồng dạng ~8′, 2 ví dụ GV giảng và cùng HS điền sơ đồ ngược ~22′ (gồm 5′ vẽ), Bài 8 HS vẽ tiếp, đọc sơ đồ ngược rồi trình bày vào vở ~12′."
)
GHI_CHU_LT2 = (
    "Khoảng 21 phút với lớp C theo định mức: HS tự vẽ hình đề phường Ba Đình (~5′), tự trình bày ý b (~16′): phần vuông góc như Phiếu 3, "
    "$OH \\cdot OM = R^2$ như Ví dụ 2, Bài 8. Ý a đã học ở Phiếu 2, GV chữa ở phần chữa bài cuối buổi."
)
GHI_CHU_BTVN = (
    "BTVN khoảng 80 phút với lớp C, dày hơn quỹ 40 phút để HS có thêm bài: BTVN 1 đến BTVN 4 đổi tích ra tỉ lệ thức, đọc ra hai tam giác (~9′), BTVN 5, BTVN 6 trắc nghiệm đồng dạng (~4′), "
    "BTVN 7 vẽ tiếp hình rồi điền khung (~9′), BTVN 8 tự vẽ hình, đọc sơ đồ ngược rồi trình bày vào vở (~16′), BTVN 9 cùng cách (~15′), BTVN 10 tự vẽ hình, tự trình bày như Bài 9 (~28′)."
)


# ── Hình ───────────────────────────────────────────────────────────────────────
def h_the_mot_cap():
    """Thẻ Dạng 1: tam giác có hai đường cao BD, CE."""
    a, b, c = (1.0, 2.0), (0.0, 0.0), (3.4, 0.0)
    dd, e = foot(b, a, c), foot(c, a, b)
    f = Fig()
    f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("D", dd); f.pt("E", e)
    for u, v in [("A", "B"), ("B", "C"), ("A", "C"), ("B", "D"), ("C", "E")]:
        f.seg(u, v)
    f.right("D", a, b); f.right("E", a, c)
    return f.tikz()


def cum_14():
    a, b, m = (-R, 0.0), (R, 0.0), polar(115, R)
    c = (-R, (R * R + R * m[0]) / m[1])
    dd = (R, (R * R - R * m[0]) / m[1])
    return a, b, m, c, dd, foot((0.0, 0.0), m, b)


def h_cum_14():
    a, b, m, c, dd, h = cum_14()
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("B", b); f.pt("M", m); f.pt("C", c); f.pt("D", dd); f.pt("H", h)
    for u, v in [("A", "B"), ("A", "C"), ("C", "D"), ("O", "M"), ("M", "B"), ("O", "D")]:
        f.seg(u, v)
    f.right("A", (0, 0), c); f.right("M", (0, 0), dd); f.right(h, m, dd)
    return f.tikz()


def h_dong_da_03():
    r = R
    O, A, B, C = (0.0, 0.0), (-r, 0.0), (r, 0.0), polar(60, r)
    M = (-r, (r * r + r * C[0]) / C[1])
    I = giao(A, C, O, M)
    f = Fig()
    f.arc(O, r, 0, 180)
    f.pt("O", O); f.pt("A", A); f.pt("B", B); f.pt("C", C); f.pt("M", M); f.pt("I", I)
    f.pt("x", (-r, M[1] + 0.6), dot=False)
    for u, v in [("A", "B"), ("A", "x"), ("M", "C"), ("O", "M"), ("A", "C"), ("O", "C")]:
        f.seg(u, v)
    f.right("A", O, M); f.right("C", O, M); f.right(I, A, O)
    return f.tikz()


def h_nen_tron_tron(day_du):
    """Đề bắt đầu "Từ điểm M nằm ngoài đường tròn (O; R)": chưa in tên điểm nào, chỉ có đường tròn và tâm."""
    f = Fig()
    f.circle((0, 0), R)
    f.fill_raw("  \\fill[ink] (0,0) circle (1.3pt);\n")
    return nen(f, day_du)


def luong_the_vinh():
    a, b, c = (1.1, 2.3), (0.0, 0.0), (4.0, 0.0)
    dd = foot(a, b, c)
    return a, b, c, dd, foot(dd, a, b), foot(dd, a, c)


def h_luong_the_vinh():
    a, b, c, dd, e, g = luong_the_vinh()
    f = Fig()
    f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("D", dd); f.pt("E", e); f.pt("F", g)
    for u, v in [("A", "B"), ("B", "C"), ("A", "C"), ("A", "D"), ("D", "E"), ("D", "F")]:
        f.seg(u, v)
    f.right("D", a, c); f.right("E", b, dd); f.right("F", c, dd)
    return f.tikz()


def h_nen_tam_giac(ham, day_du):
    a, b, c, *_ = ham()
    f = Fig()
    f.pt("A", a); f.pt("B", b); f.pt("C", c)
    f.seg("A", "B"); f.seg("B", "C"); f.seg("A", "C")
    return nen(f, day_du)


def kiem_toan_do():
    """Kết luận của đề phải đúng trên chính hình vẽ."""
    O = (0.0, 0.0)
    a, b, c, dd, e, h = nghia_tan()
    assert abs(d(b, e) * d(b, a) - d(b, h) * d(b, dd)) < 1e-9
    a, b, m, c, dd, h = cum_14()
    assert abs(d(O, h) * d(O, dd) - R * R) < 1e-9
    assert abs((dd[0] - m[0]) * m[0] + (dd[1] - m[1]) * m[1]) < 1e-9 and abs((dd[0] - O[0]) * (b[0] - m[0]) + (dd[1] - O[1]) * (b[1] - m[1])) < 1e-9
    a, b, c, dd, e, g = luong_the_vinh()
    assert abs(d(a, e) * d(a, b) - d(a, dd) ** 2) < 1e-9
    a, b, c, dd, h = cau_giay()
    assert abs(d(c, h) * d(c, a) - 2 * R * R) < 1e-9


# ── Sơ đồ, lời giải khuôn hai tiếp tuyến ───────────────────────────────────────
def sd_hai_tt(o_tich, cap, trung_truc, vuong, xam, goc_vuong, goc_chung, ten_r):
    return so_do(
        o_tich, [cap[0], cap[1]],
        [vuong, f"{trung_truc}:\\\\{xam}"],
        [f"{goc_vuong} (tiếp tuyến);\\\\{goc_chung} chung"], ben=f"$R = {ten_r}$ (bán kính)")


def lesson() -> dict:
    goc_ = b2.lesson()
    # Giữ nguyên: chặng Khám phá, thẻ A1, Bài 1–7.
    kham_pha = goc_["stages"][0]
    the_a1 = next(x for x in goc_["stages"][1]["blocks"] if x.get("title", "").startswith("1."))
    the_a1["figure"]["pos"] = "below"
    tn = {x["label"]: x for x in goc_["stages"][2]["blocks"] if x.get("label")}
    # Ví dụ 1 đứng ngay trước Bài 7 (đi cùng bài cùng dạng) nên Bài 7 mang Hình 3.
    tn["Bài 7."]["statement"] = tn["Bài 7."]["statement"].replace("Hình 2", "Hình 3")
    tn["Bài 7."]["figure"]["caption"] = "Hình 3"

    the_a2 = {
        "type": "noted", "variant": "theory", "title": "2. KIẾN THỨC ĐÃ HỌC THƯỜNG DÙNG",
        "text": "\\nhanly{Tiếp tuyến (Bài 16):} Tiếp tuyến vuông góc với bán kính đi qua tiếp điểm.[[br]]"
                "\\nhanly{Hai tiếp tuyến (Phiếu 3):} $AB = AC$, $OB = OC$ $\\Rightarrow OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$.",
        "figure": {"tikz": hai_tt("A", "B", "C", "H", r=R_THE, xa=2.8), "caption": "$OA \\perp BC$ tại $H$, $AB \\perp OB$ tại $B$", "pos": "below"},
    }
    the_dang_1 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 1. MỘT CẶP TAM GIÁC VUÔNG CHUNG GÓC NHỌN",
        "text": "\\nhanly{Phương pháp.} đưa về hai tam giác đồng dạng.[[br]]"
                "\\nhanly{Bước 1 (nháp):} Đổi tích thành tỉ số $\\dfrac{AE}{AD} = \\dfrac{AC}{AB}$, đọc ra $\\triangle AEC$ và $\\triangle ADB$.[[br]]"
                "\\nhanly{Bước 2:} Chỉ ra góc vuông và góc nhọn chung (g.g).[[br]]"
                "\\nhanly{Bước 3:} Viết tỉ số cạnh tương ứng $\\Rightarrow$ đẳng thức tích.",
        "figure": {"tikz": h_the_mot_cap(), "caption": "$\\triangle AEC$ và $\\triangle ADB$ vuông, chung góc $A$", "pos": "right"},
        "so_do_nguoc": so_do(
            "$AE \\cdot AB = AD \\cdot AC$", ["$\\triangle AEC \\backsim \\triangle ADB$ (g.g)"],
            [f"${goc('AEC')} = {goc('ADB')} = 90^\\circ$\\\\($CE \\perp AB$, $BD \\perp AC$)"],
            [f"${goc('BAC')}$ chung"], rong=2.2),
    }
    the_dang_2 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 2. HAI TIẾP TUYẾN: VUÔNG GÓC RỒI ĐẲNG THỨC TÍCH",
        "text": "\\nhanly{Phương pháp.} lấy góc vuông từ $OA \\perp BC$ và từ tiếp tuyến.[[br]]"
                "\\nhanly{Bước 1:} Chứng minh $OA \\perp BC$ tại $H$ (Phiếu 3).[[br]]"
                "\\nhanly{Bước 2:} $\\triangle OHB \\backsim \\triangle OBA$ (g.g, chung góc $O$).[[br]]"
                "\\nhanly{Bước 3:} Viết tỉ số $\\Rightarrow OH \\cdot OA = OB^2 = R^2$.",
        "figure": {"tikz": hai_tt("A", "B", "C", "H", r=R_THE, xa=2.8), "caption": "$\\triangle OHB$ và $\\triangle OBA$ vuông, chung góc $O$", "pos": "right"},
        "so_do_nguoc": sd_hai_tt("$OH \\cdot OA = R^2$", ("$OH \\cdot OA = OB^2$", "$\\triangle OHB \\backsim \\triangle OBA$ (g.g)"),
                                 "$OA$ là đường trung trực của $BC$", "$OA \\perp BC$ tại $H$", "$AB = AC$; $OB = OC = R$",
                                 f"${goc('OBA')} = 90^\\circ$", f"${goc('AOB')}$", "OB"),
    }

    # ── Ví dụ 1: Nghĩa Tân GK1, phần BE.BA = BH.BD ─────────────────────────────
    nt = h_nghia_tan()
    vi_du_1 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 1.} Cho $\\triangle ABC$ nhọn có ba đỉnh nằm trên $(O)$ và $AB < AC$. Các đường cao $BD$, $CE$ cắt nhau tại $H$ (Hình 2). "
                "Vẽ tiếp vào Hình 2 các yếu tố còn thiếu theo đề. Chứng minh $BE \\cdot BA = BH \\cdot BD$."
                f"{BR}{LG}{BR}"
                f"Xét $\\triangle BEH$ và $\\triangle BDA$ có:{BR}"
                f"${goc('BEH')} = {goc('BDA')} = [[fill:90^\\circ]]$ ($CE \\perp AB$, $BD \\perp AC$){BR}"
                f"$[[fill:\\widehat{{ABD}}]]$ chung{BR}"
                f"$\\Rightarrow \\triangle BEH \\backsim \\triangle [[fill:BDA]]$ (g.g){BR}"
                f"$\\Rightarrow \\dfrac{{BE}}{{BD}} = [[fill:\\dfrac{{BH}}{{BA}}|1.3cm]]$.{BR}"
                "Vậy $BE \\cdot BA = BH \\cdot BD$ (nhân [[fill:chéo]] hai vế).",
        "figure": {"tikz": h_nen_nghia_tan(nt), "tikz_gv": nt, "caption": "Hình 2", "pos": "right"},
        "so_do_nguoc": so_do(
            "$BE \\cdot BA = BH \\cdot BD$", ["$\\triangle BEH \\backsim \\triangle [[fill:BDA]]$ (g.g)"],
            [f"${goc('BEH')} = {goc('BDA')} = [[fill:90^\\circ]]$\\\\($CE \\perp AB$, $BD \\perp AC$)"],
            ["$[[fill:\\widehat{ABD}]]$ chung"], rong=2.2),
    }

    # ── Ví dụ 2: Ngô Gia Tự ý b ────────────────────────────────────────────────
    ngt = hai_tt("A", "B", "C", "H")
    vi_du_2 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 2.} Cho đường tròn $(O; R)$. Từ điểm $A$ nằm ngoài đường tròn kẻ các tiếp tuyến $AB$, $AC$ với đường tròn ($B$, $C$ là các tiếp điểm). "
                "Gọi $H$ là giao điểm của $OA$ và $BC$ (Hình 4). Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề. Chứng minh $OA \\perp BC$ và $OH \\cdot OA = R^2$."
                f"{BR}{LG}{BR}"
                f"$AB$, $AC$ là hai tiếp tuyến của $(O)$ cắt nhau tại $A$ $\\Rightarrow AB = [[fill:AC]]$.{BR}"
                f"$OB = OC$ ([[fill:bán kính]] của $(O)$){BR}"
                f"$\\Rightarrow OA$ là [[fill:đường trung trực]] của đoạn thẳng $BC${BR}"
                f"$\\Rightarrow OA \\perp BC$ tại $H$.{BR}"
                f"Xét $\\triangle OHB$ và $\\triangle OBA$ có:{BR}"
                f"${goc('OHB')} = {goc('OBA')} = 90^\\circ$ ($OA \\perp BC$ tại $H$, $AB$ là [[fill:tiếp tuyến]] của $(O)$ tại $B$){BR}"
                f"$[[fill:\\widehat{{AOB}}]]$ chung{BR}"
                f"$\\Rightarrow \\triangle OHB \\backsim \\triangle [[fill:OBA]]$ (g.g){BR}"
                f"$\\Rightarrow \\dfrac{{OH}}{{OB}} = [[fill:\\dfrac{{OB}}{{OA}}|1.3cm]]${BR}"
                f"$\\Rightarrow OH \\cdot OA = [[fill:OB^2]]$.{BR}"
                "Vậy $OA \\perp BC$ và $OH \\cdot OA = R^2$ (vì $OB = [[fill:R]]$).",
        "figure": {"tikz": h_nen_tron(ngt), "tikz_gv": ngt, "caption": "Hình 4", "pos": "right"},
        "so_do_nguoc": sd_hai_tt("$OH \\cdot OA = R^2$",
                                 ("$OH \\cdot OA = [[fill:OB^2|1.1cm]]$", "$\\triangle OHB \\backsim \\triangle [[fill:OBA]]$ (g.g)"),
                                 "$OA$ là [[fill:đường trung trực|2.6cm]]", "$OA \\perp BC$ tại $H$", "$AB = [[fill:AC]]$; $OB = OC$",
                                 f"${goc('OBA')} = 90^\\circ$", "$[[fill:\\widehat{AOB}]]$", "OB").replace("$R = OB$ (bán kính)", "$R = [[fill:OB]]$ (bán kính)"),
    }

    # ── Bài 8: Cụm 14, phần OH.OD = R² ─────────────────────────────────────────
    c14 = h_cum_14()
    bai_8 = bai(
        "Bài 8.", 2, "onclass", "TH3",
        "[TH] Cho đường tròn $(O; R)$ đường kính $AB$, lấy điểm $M$ bất kì trên đường tròn ($M \\ne A$, $M \\ne B$), tiếp tuyến tại $A$ và $M$ cắt nhau tại $C$. "
        "Qua $O$ kẻ đường thẳng vuông góc với dây cung $MB$ cắt tia $CM$ tại $D$, $OD$ cắt $MB$ tại $H$ (Hình 5). "
        f"Chứng minh $OH \\cdot OD = R^2$. {theo_so_do(5)}",
        xet("OHM", "OMD", f"{goc('OHM')} = {goc('OMD')}", "$OD \\perp MB$ tại $H$, $CD$ là tiếp tuyến của $(O)$ tại $M$", goc("MOD"),
            "\\dfrac{OH}{OM} = \\dfrac{OM}{OD}", "OH \\cdot OD = OM^2") + f".{BR}"
        + "Vậy $OH \\cdot OD = R^2$ (vì $OM = R$).",
        figure={"tikz": h_nen_tron_ngang("A", "B", c14), "tikz_gv": c14, "caption": "Hình 5", "pos": "right"},
        so_do_nguoc=so_do(
            "$OH \\cdot OD = R^2$", ["$OH \\cdot OD = OM^2$", "$\\triangle OHM \\backsim \\triangle OMD$ (g.g)"],
            [f"${goc('OHM')} = 90^\\circ$ ($OD \\perp MB$ tại $H$)"],
            [f"${goc('OMD')} = 90^\\circ$ ($CD$ là tiếp tuyến);\\\\${goc('MOD')}$ chung"], rong=3.0, ben="$R = OM$ (bán kính)"),
        phut_so_do=PHUT["Bài 8"], ve_tiep=3,
    )

    # ── Bài 9: đích phường Ba Đình a, b ───────────────────────────────────────
    bd = hai_tt("M", "A", "B", "H")
    bai_9 = bai(
        "Bài 9.", 3, "onclass", "TH1+VD1",
        "Cho đường tròn $(O; R)$ và một điểm $M$ cố định nằm ngoài đường tròn $(O)$. Từ $M$ kẻ các tiếp tuyến $MA$, $MB$ tới đường tròn $(O)$ ($A$, $B$ là các tiếp điểm).[[br]]"
        "a) [TH] Chứng minh bốn điểm $M$, $A$, $O$, $B$ cùng thuộc một đường tròn.[[br]]"
        "b) [VD] Gọi giao điểm của $MO$ và $AB$ là $H$. Chứng minh $MO \\perp AB$ và $OH \\cdot OM = R^2$.",
        "a) " + giai_bon_diem("M", "A", "B")
        + f"Vậy bốn điểm $M, A, O, B$ cùng thuộc đường tròn đường kính $MO$.{BR}"
        + "b) " + giai_trung_truc("M", "A", "B", ket=f"{BR}$\\Rightarrow MO \\perp AB$ tại $H$.{BR}", duong="MO")
        + xet("OHA", "OAM", f"{goc('OHA')} = {goc('OAM')}", "$MO \\perp AB$ tại $H$, $MA$ là tiếp tuyến của $(O)$ tại $A$", goc("AOM"),
              "\\dfrac{OH}{OA} = \\dfrac{OA}{OM}", "OH \\cdot OM = OA^2") + f".{BR}"
        + "Vậy $MO \\perp AB$ và $OH \\cdot OM = R^2$ (vì $OA = R$).",
        figure_given=False, draw=True,
        figure={"tikz": h_nen_diem_ngoai("M", bd), "tikz_gv": bd, "caption": "Hình 6", "pos": "right"},
        hints=["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
               "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $AB$?",
               "Đẳng thức $OH \\cdot OM = OA^2$ có được từ tỉ lệ thức nào? Tỉ lệ thức đó đọc ra hai tam giác nào?"],
        quy_trinh=["Vẽ tiếp hình: hai tiếp tuyến $MA$, $MB$; đoạn $OM$, $AB$ cắt nhau tại $H$; đánh dấu các góc vuông",
                   "Ý a: hai tiếp tuyến $\\Rightarrow$ hai tam giác vuông chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $MO$",
                   "Ý b: $MA = MB$, $OA = OB = R$ $\\Rightarrow MO$ là đường trung trực của $AB$ $\\Rightarrow MO \\perp AB$ tại $H$",
                   "$\\triangle OHA \\backsim \\triangle OAM$ (g.g) $\\Rightarrow OH \\cdot OM = OA^2 = R^2$ (như Ví dụ 2, Bài 8)"],
    )

    # ── BTVN ───────────────────────────────────────────────────────────────────
    # BTVN 1–4 gương Bài 1–4: đẳng thức tách từ đề BTVN 10 (Gia Lâm), BTVN 8 (Lương Thế Vinh). BTVN 5, 6: đề lớp 8.
    btvn_1 = bai(
        "BTVN 1.", 1, "btvn", "NB1",
        "[NB] Đẳng thức $OA^2 = OH \\cdot OM$ có được từ tỉ lệ thức nào?",
        "C",
        options=["$\\dfrac{OH}{OM} = \\dfrac{OM}{OA}$.", "$\\dfrac{OH}{OA} = \\dfrac{OM}{OA}$.",
                 "$\\dfrac{OH}{OA} = \\dfrac{OA}{OM}$.", "$\\dfrac{OA}{OM} = \\dfrac{OM}{OH}$."],
        figure_given=True,
    )
    btvn_2 = bai(
        "BTVN 2.", 1, "btvn", "NB1",
        "[NB] Để có tỉ lệ thức $\\dfrac{OH}{OA} = \\dfrac{OA}{OM}$, cần chứng minh hai tam giác nào đồng dạng?",
        "A",
        options=["$\\triangle OHA \\backsim \\triangle OAM$.\\phantom{xxxxx}", "$\\triangle OHA \\backsim \\triangle OMA$.",
                 "$\\triangle HOA \\backsim \\triangle OAM$.", "$\\triangle OHA \\backsim \\triangle AOM$."],
        figure_given=True,
    )
    btvn_3 = bai(
        "BTVN 3.", 1, "btvn", "NB1",
        "[NB] Đẳng thức $AE \\cdot AB = AD^2$ có được từ tỉ lệ thức nào?",
        "B",
        options=["$\\dfrac{AE}{AB} = \\dfrac{AB}{AD}$.", "$\\dfrac{AE}{AD} = \\dfrac{AD}{AB}$.",
                 "$\\dfrac{AE}{AD} = \\dfrac{AB}{AD}$.", "$\\dfrac{AD}{AB} = \\dfrac{AB}{AE}$."],
        figure_given=True,
    )
    btvn_4 = bai(
        "BTVN 4.", 1, "btvn", "NB1",
        "[NB] Để có tỉ lệ thức $\\dfrac{AE}{AD} = \\dfrac{AD}{AB}$, cần chứng minh hai tam giác nào đồng dạng?",
        "D",
        options=["$\\triangle AED \\backsim \\triangle ABD$.\\phantom{xxxxx}", "$\\triangle EAD \\backsim \\triangle ADB$.",
                 "$\\triangle AED \\backsim \\triangle DBA$.", "$\\triangle AED \\backsim \\triangle ADB$."],
        figure_given=True,
    )
    btvn_5 = bai(
        "BTVN 5.", 1, "btvn", "NB2",
        "[NB] Cho $\\triangle DEF \\backsim \\triangle HKI$. Tỉ số nào sau đây là đúng?",
        "C",
        options=["$\\dfrac{DE}{HK} = \\dfrac{DF}{KI}$.", "$\\dfrac{DE}{HK} = \\dfrac{EF}{HI}$.",
                 "$\\dfrac{EF}{KI} = \\dfrac{DF}{HI}$.", "$\\dfrac{DF}{HI} = \\dfrac{EF}{HK}$."],
        figure_given=True,
    )
    btvn_6 = bai(
        "BTVN 6.", 1, "btvn", "NB2",
        "[NB] Nếu $\\triangle ABC$ và $\\triangle FED$ có $\\widehat{A} = \\widehat{F}$, cần thêm điều kiện gì dưới đây để $\\triangle ABC \\backsim \\triangle FED$?",
        "A",
        options=["$\\widehat{B} = \\widehat{E}$.", "$\\widehat{C} = \\widehat{E}$.", "$\\widehat{B} = \\widehat{D}$.", "$\\widehat{C} = \\widehat{F}$."],
        figure_given=True,
    )

    cm = h_chuong_my()
    khung = (
        "Xét $\\triangle ADH$ và $\\triangle AHB$ có:[[br]]"
        "$\\widehat{ADH} = \\widehat{AHB} = [[blank:1.1cm]]$ ($HD \\perp AB$, $AH \\perp BC$)[[br]]"
        "$[[blank:1.6cm]]$ chung[[br]]"
        "$\\Rightarrow \\triangle ADH \\backsim \\triangle [[blank:1.6cm]]$ (g.g)[[br]]"
        "$\\Rightarrow \\dfrac{AD}{AH} = [[blank:1.6cm]]$[[br]]"
        "Vậy $AH^2 = AD \\cdot AB$.[[br]]"
        "b) [NB] Chứng minh $AD \\cdot AB = AE \\cdot AC$:[[br]]"
        "Tương tự, $\\triangle AEH \\backsim \\triangle [[blank:1.6cm]]$ (g.g)[[br]]"
        "$\\Rightarrow AH^2 = [[blank:2.4cm]]$.[[br]]"
        "Vậy $AD \\cdot AB = AE \\cdot AC$ (cùng bằng $[[blank:1.6cm]]$)."
    )
    btvn_7 = bai(
        "BTVN 7.", 1, "btvn", "NB3",
        "Cho $\\triangle ABC$ có $3$ góc nhọn, đường cao $AH$, kẻ $HE \\perp AC$ tại $E$, $HD \\perp AB$ tại $D$ (Hình 7).[[br]]"
        "Vẽ tiếp vào Hình 7 các yếu tố còn thiếu theo đề, đánh dấu các góc vuông, rồi điền vào chỗ chấm để hoàn thành bài giải:[[br]]"
        "a) [NB] Chứng minh $AH^2 = AD \\cdot AB$:[[br]]" + khung,
        "a) $90^\\circ$; $\\widehat{BAH}$; $AHB$; $\\dfrac{AH}{AB}$.[[br]]b) $AHC$; $AE \\cdot AC$; $AH^2$.",
        statement_slide="Cho $\\triangle ABC$ có $3$ góc nhọn, đường cao $AH$, kẻ $HE \\perp AC$ tại $E$, $HD \\perp AB$ tại $D$ (Hình 7).[[br]]"
                        "a) [NB] Chứng minh $AH^2 = AD \\cdot AB$.[[br]]b) [NB] Chứng minh $AD \\cdot AB = AE \\cdot AC$.",
        figure_given=True, ve_tiep=3,
        figure={"tikz": h_nen_chuong_my(cm), "tikz_gv": cm, "caption": "Hình 7", "pos": "right"},
    )

    ltv = h_luong_the_vinh()
    btvn_8 = bai(
        "BTVN 8.", 2, "btvn", "TH2",
        "[TH] Cho tam giác $ABC$ nhọn ($AB < AC$), đường cao $AD$ ($D \\in BC$). Gọi $E$, $F$ lần lượt là hình chiếu vuông góc của $D$ lên $AB$ và $AC$ (Hình 8). "
        f"Chứng minh $AE \\cdot AB = AD^2$. {theo_so_do(8)}",
        xet("AED", "ADB", f"{goc('AED')} = {goc('ADB')}", "$DE \\perp AB$ tại $E$, $AD \\perp BC$", goc("BAD"),
            "\\dfrac{AE}{AD} = \\dfrac{AD}{AB}", "AE \\cdot AB = AD^2") + f".{BR}"
        + "Vậy $AE \\cdot AB = AD^2$.",
        draw=True, phut_so_do=PHUT["BTVN 8"],
        figure={"tikz": h_nen_tam_giac(luong_the_vinh, ltv), "tikz_gv": ltv, "caption": "Hình 8", "pos": "right"},
        so_do_nguoc=so_do(
            "$AE \\cdot AB = AD^2$", ["$\\triangle AED \\backsim \\triangle ADB$ (g.g)"],
            [f"${goc('AED')} = {goc('ADB')} = 90^\\circ$\\\\($DE \\perp AB$, $AD \\perp BC$)"],
            [f"${goc('BAD')}$ chung"], rong=2.2),
    )

    dd3 = h_dong_da_03()
    btvn_9 = bai(
        "BTVN 9.", 2, "btvn", "TH3",
        "[TH] Cho nửa đường tròn $(O; R)$, đường kính $AB$. Từ điểm $M$ bất kì trên tiếp tuyến $Ax$ của nửa đường tròn $(O)$ vẽ tiếp tuyến thứ hai $MC$ ($C$ là tiếp điểm). "
        f"Gọi $I$ là giao điểm của $OM$ và $AC$ (Hình 9). Chứng minh $OI \\cdot OM = R^2$. {theo_so_do(9)}",
        giai_trung_truc("M", "A", "C", ket=f"{BR}$\\Rightarrow OM \\perp AC$ tại $I$.{BR}")
        + xet("OIA", "OAM", f"{goc('OIA')} = {goc('OAM')}", "$OM \\perp AC$ tại $I$, $MA$ là tiếp tuyến của $(O)$ tại $A$", goc("AOM"),
              "\\dfrac{OI}{OA} = \\dfrac{OA}{OM}", "OI \\cdot OM = OA^2") + f".{BR}"
        + "Vậy $OI \\cdot OM = R^2$ (vì $OA = R$).",
        draw=True, phut_so_do=PHUT["BTVN 9"],
        figure={"tikz": h_nen_duong_kinh_ngang("A", "B", dd3), "tikz_gv": dd3, "caption": "Hình 9", "pos": "right"},
        so_do_nguoc=sd_hai_tt("$OI \\cdot OM = R^2$", ("$OI \\cdot OM = OA^2$", "$\\triangle OIA \\backsim \\triangle OAM$ (g.g)"),
                              "$OM$ là đường trung trực của $AC$", "$OM \\perp AC$ tại $I$", "$MA = MC$; $OA = OC = R$",
                              f"${goc('OAM')} = 90^\\circ$", f"${goc('AOM')}$", "OA"),
    )

    gl = hai_tt("M", "A", "B", "H")
    btvn_10 = bai(
        "BTVN 10.", 3, "btvn", "TH1+VD1",
        "Từ điểm $M$ nằm ngoài đường tròn $(O; R)$ với $OM > 2R$, kẻ các tiếp tuyến $MA$, $MB$ của đường tròn $(O)$ ($A$, $B$ là các tiếp điểm). "
        "Gọi $H$ là giao điểm của $AB$ và $OM$.[[br]]"
        "a) [TH] Chứng minh bốn điểm $O$, $A$, $M$, $B$ cùng nằm trên một đường tròn.[[br]]"
        "b) [VD] Chứng minh $AB \\perp OM$ tại $H$ và $OA^2 = OH \\cdot OM$.",
        "a) " + giai_bon_diem("M", "A", "B")
        + f"Vậy bốn điểm $O, A, M, B$ cùng nằm trên đường tròn đường kính $MO$.{BR}"
        + "b) " + giai_trung_truc("M", "A", "B", ket=f"{BR}$\\Rightarrow AB \\perp OM$ tại $H$.{BR}")
        + xet("OHA", "OAM", f"{goc('OHA')} = {goc('OAM')}", "$AB \\perp OM$ tại $H$, $MA$ là tiếp tuyến của $(O)$ tại $A$", goc("AOM"),
              "\\dfrac{OH}{OA} = \\dfrac{OA}{OM}", "OA^2 = OH \\cdot OM") + f".{BR}"
        + "Vậy $AB \\perp OM$ tại $H$ và $OA^2 = OH \\cdot OM$.",
        figure_given=False, draw=True,
        figure={"tikz": h_nen_tron_tron(gl), "tikz_gv": gl, "caption": "Hình 10", "pos": "right"},
        hints=["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
               "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $AB$?",
               "Đẳng thức $OA^2 = OH \\cdot OM$ có được từ tỉ lệ thức nào? Tỉ lệ thức đó đọc ra hai tam giác nào?"],
    )

    return {
        "slug": PHIEU.stem,
        "title": "Chứng minh đẳng thức tích bằng tam giác đồng dạng",
        "eyebrow": "PHIẾU 4 • HÌNH HỌC 9 · CHƯƠNG V — BÀI 16 (LUYỆN TẬP)",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "btvn_phieu_rieng": True,
        "stages": [
            kham_pha,
            {"kind": "concept", "number": 2, "title": "Kiến thức trọng tâm",
             "teacher_note": "Phần A đọc đúng lời SGK Toán 8 tập 2 (Bài 36, Định lí 1, tr.98). Phần B là phương pháp cho vế tích của ý b Câu IV.2: đọc từng ý ở 66 đề Kì I, "
                             "khuôn hai tiếp tuyến $OH \\cdot OA = R^2$ có ở 24\\% đề, có đường kính 15\\%, hai cát tuyến bắc cầu 6\\%. "
                             "Hệ thức lượng đã giảm tải nên mọi đẳng thức tích phải đi qua tam giác đồng dạng.",
             "blocks": [
                 {"type": "para", "variant": "part", "text": "A. Lý thuyết"},
                 the_a1, the_a2,
                 {"type": "para", "variant": "part", "text": "B. Phương pháp chứng minh — các dạng quen thuộc"},
                 the_dang_1, the_dang_2,
             ]},
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "teacher_note": GHI_CHU_LT1,
             "blocks": [
                 {"type": "para", "text": "\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề phường Ba Đình) ở Bài 9: ý a chứng minh bốn điểm cùng thuộc một đường "
                                          "tròn (đã học ở Phiếu 2), ý b chứng minh vuông góc (đã học ở Phiếu 3) và đẳng thức tích."},
                 {"type": "para", "variant": "heading", "text": "Mạch 1. Ý b — Từ đẳng thức tích đến hai tam giác vuông chung góc nhọn"},
                 tn["Bài 1."], tn["Bài 2."], tn["Bài 3."], tn["Bài 4."], tn["Bài 5."], tn["Bài 6."],
                 vi_du_1, tn["Bài 7."],
                 {"type": "para", "variant": "heading", "text": "Mạch 2. Ý b — Hai tiếp tuyến: vuông góc rồi đẳng thức tích"},
                 vi_du_2, bai_8,
             ]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "teacher_note": GHI_CHU_LT2,
             "blocks": [
                 {"type": "para", "variant": "heading", "text": "Đề thi Học kì I — phường Ba Đình"},
                 bai_9,
             ]},
            {"kind": "reflection", "number": 5, "title": "Sơ đồ tư duy",
             "teacher_note": GHI_CHU_BTVN,
             "blocks": [
                 {"type": "mindmap", "caption": "Sơ đồ tư duy: Chứng minh đẳng thức tích bằng tam giác đồng dạng",
                  "root": "ĐẲNG THỨC TÍCH",
                  "branches": [
                      {"label": "CÔNG CỤ", "children": [{"label": "Hai tam giác vuông có một góc nhọn bằng nhau thì đồng dạng"},
                                                         {"label": "Tỉ số cạnh tương ứng $\\Rightarrow$ tích"}]},
                      {"label": "CÁCH NGHĨ", "children": [{"label": "Đổi tích thành tỉ lệ thức"},
                                                           {"label": "Đọc ra hai tam giác từ tử số, mẫu số"}]},
                      {"label": "HAI TIẾP TUYẾN", "children": [{"label": "$OA \\perp BC$ tại $H$"},
                                                                {"label": "$\\triangle OHB \\backsim \\triangle OBA$ $\\Rightarrow OH \\cdot OA = R^2$"}]},
                  ]},
                 btvn_1, btvn_2, btvn_3, btvn_4, btvn_5, btvn_6, btvn_7, btvn_8, btvn_9, btvn_10,
             ]},
        ],
    }


# ── Thuyết minh ────────────────────────────────────────────────────────────────
GIO_THUC_TM = [
    "\\quad Giờ thực lớp C (05/11/2026): Khám phá $+$ Kiến thức 12′ · Luyện tập 1 khoảng 52′ (7 câu trắc nghiệm, 2 ví dụ HS vẽ cùng GV và điền sơ đồ ngược, "
    "1 bài theo sơ đồ ngược HS trình bày vào vở $+$ vẽ tiếp hình)",
    "\\quad Luyện tập 2 khoảng 21′ (đề đích phường Ba Đình ý b, HS tự vẽ) · chữa bài (có ý a đề đích), chốt khoảng 5′ · BTVN khoảng 80′ (quỹ 40′, cố ý dày hơn)",
]
DANG_VD_4 = ("Buổi 4 — Câu IV.2 hai ý (đề phường Ba Đình): bốn điểm $M$, $A$, $O$, $B$; $MO \\perp AB$ và $OH \\cdot OM = R^2$ "
             "(đường trung trực rồi một cặp tam giác vuông chung góc nhọn). BTVN: đề Gia Lâm.")
VIDU_4 = ("Buổi 4: Đề mẫu (Nghĩa Tân): tam giác có hai đường cao — $BE \\cdot BA = BH \\cdot BD$. "
          "Đề mẫu (Ngô Gia Tự): hai tiếp tuyến — $OA \\perp BC$ và $OH \\cdot OA = R^2$.")


def dong_tm(phut) -> list[dict]:
    quy = ["Ý a: hai góc vuông tại hai tiếp điểm có chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $MO$",
           "Ý b: $MA = MB$, $OA = OB$ $\\Rightarrow MO$ là đường trung trực của $AB$ $\\Rightarrow MO \\perp AB$ tại $H$",
           "$\\triangle OHA \\backsim \\triangle OAM$ (g.g) $\\Rightarrow OH \\cdot OM = OA^2 = R^2$ (như Ví dụ 2, Bài 8)"]
    return [
        {"band": "NB", "loai": "NB tách TH", "dang": "Trắc nghiệm: đổi đẳng thức tích thành tỉ lệ thức, từ tỉ lệ thức đọc ra hai tam giác cần chứng minh đồng dạng. Trên lớp: $OH \\cdot OA = OB^2$ (tách từ đề Ngô Gia Tự ý b), $CH \\cdot CA = CO \\cdot CB$ (đề Cầu Giấy ý b). BTVN: $OA^2 = OH \\cdot OM$ (đề Gia Lâm ý b), $AE \\cdot AB = AD^2$ (đề Lương Thế Vinh ý b)",
         "source_refs": ["ck1-ngo-gia-tu-2025-IV2.b", "ck1-cau-giay-2024-IV2.b", "ck1-gia-lam-2024-4.2.b", "gk1-luong-the-vinh-2025-4.2.b"], "vidu": 0, "onclass": 4, "btvn": 4, "lythuyet": 0, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB kiến thức cũ", "dang": "Chứng minh hai tam giác đồng dạng (Lớp 8), trắc nghiệm. Trên lớp: thêm điều kiện góc cho g.g (đề Thanh Trì); viết đúng thứ tự đỉnh (đề Đan Phượng); các cặp đồng dạng trong tam giác vuông có đường cao (đề Mai Dịch). BTVN: tỉ số cạnh tương ứng (đề Đa Tốn); thêm điều kiện góc (đề Tam Hưng)",
         "source_refs": ["l8-ck2-2023-thanh-tri-c6", "l8-ck2-x-2023-2024-de-thi-hk2-gddt-dan-phuong-hn-c8", "l8-gk2-2025-thcs-mai-dich-c8", "l8-ck2-2023-thcs-da-ton-c9", "l8-ck2-2025-thcs-tam-hung-c6"], "vidu": 0, "onclass": 3, "btvn": 2, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB ghép bài", "dang": "Vẽ tiếp hình nền, điền khung bài giải: $\\triangle ADH \\backsim \\triangle AHB$ rồi $AD \\cdot AB = AE \\cdot AC$ (BTVN đề Chương Mỹ ý b)",
         "source_refs": ["ck1-chuong-my-2024-4.2.b"], "vidu": 0, "onclass": 0, "btvn": 2, "lythuyet": 0, "decompose": "none",
         "hinh_san": True, "gian_giao": "dien-khuyet", "khung": True, "ve_tiep": {"btvn": 3}},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Ý a của đề thi: bốn điểm cùng thuộc một đường tròn, HS tự vẽ hình, tự trình bày (đề đích phường Ba Đình ý a; BTVN đề Gia Lâm ý a)",
         "source_refs": ["ck1-phuong-ba-dinh-2025-IV2.a", "ck1-gia-lam-2024-4.2.a"], "vidu": 0, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_hinh": {"onclass": 1, "btvn": 1}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Một cặp tam giác vuông chung góc nhọn, đường vuông góc đề cho sẵn. Ví dụ mẫu đề Nghĩa Tân ($BE \\cdot BA = BH \\cdot BD$); HS tự vẽ hình, đọc sơ đồ ngược rồi tự trình bày vào vở (BTVN đề Lương Thế Vinh, phần $AE \\cdot AB = AD^2$ của ý b)",
         "source_refs": ["gk1-nghia-tan-2025-IV.b", "gk1-luong-the-vinh-2025-4.2.b"], "vidu": 1, "onclass": 0, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"vidu": 2}, "ve_hinh": {"btvn": 1},
         "phut_so_do": {"btvn": phut["BTVN 8"]}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Hai tiếp tuyến: tam giác vuông từ tiếp tuyến $+$ đường vuông góc rồi đẳng thức tích với $R^2$. HS vẽ tiếp hình nền, đọc sơ đồ ngược rồi tự trình bày vào vở (trên lớp đề Cụm 14, phần $OH \\cdot OD = R^2$ của ý b; BTVN đề Đống Đa minh hoạ 03, phần $OI \\cdot OM = R^2$ của ý 2). Ví dụ mẫu ở dòng VD",
         "source_refs": ["ck1-cum-14-2025-4.2.b", "v10-dong-da-de03-IV2.b"], "vidu": 0, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"onclass": 3}, "ve_hinh": {"btvn": 1},
         "phut_so_do": {"onclass": phut["Bài 8"], "btvn": phut["BTVN 9"]}},
        {"band": "VD", "loai": "VD lẻ", "dang": "Ý b của đề thi (đề phường Ba Đình, đích của buổi): $MO \\perp AB$ và $OH \\cdot OM = R^2$. Ví dụ mẫu đề Ngô Gia Tự ý b; BTVN đề Gia Lâm ý b",
         "source_refs": ["ck1-phuong-ba-dinh-2025-IV2.b", "ck1-ngo-gia-tu-2025-IV2.b", "ck1-gia-lam-2024-4.2.b"], "vidu": 1, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "vd",
         "hinh_san": False, "gian_giao": "ve-hinh", "ve_tiep": {"vidu": 3}, "quy_trinh": quy},
    ]


def main():
    kiem_toan_do()
    les = gon_hinh(lesson())
    PHIEU.write_text(json.dumps(les, ensure_ascii=False, indent=2) + "\n", "utf-8")
    tm = json.loads(TM.read_text("utf-8"))
    p4 = next(p for p in tm["phieu"] if p["code"] == "4")
    p4["rows"] = dong_tm(PHUT)
    i = next(i for i, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 4"))
    j = next(j for j, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 5"))
    tm["thoiluong"][i + 1:j] = GIO_THUC_TM
    tm["dang_vd"] = [DANG_VD_4 if x.startswith("Buổi 4") else x for x in tm["dang_vd"]]
    tm["vidu"] = [VIDU_4 if x.startswith("Buổi 4") else x for x in tm["vidu"]]
    TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2), "utf-8")
    print("ghi xong", PHIEU.name)
    for k, v in KY_THUAT.items():
        print(f"{len(v):3d}/66 = {round(len(v) / 66 * 100):3d}%  {k}")


if __name__ == "__main__":
    main()
