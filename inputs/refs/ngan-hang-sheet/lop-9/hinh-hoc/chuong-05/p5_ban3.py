#!/usr/bin/env python3
"""Phiếu 5 ch.V 9C — Luyện tập chung, dựng lại theo bản mẫu phiếu 2 (sơ đồ ngược), 05/11/2026.

Thầy chốt 05/11: BỎ phần song song (MB ∥ OC) vì phải lấy góc vuông từ đường kính. Đích Ngô Sĩ Liên: ý a + phần MB ⊥ OD của ý b.
Phiếu luyện CD = AC + BD, góc COD = 90°, MC·MD = R² trên hình ba tiếp tuyến. Phiếu này không dùng trung tuyến chiều ngược.

Đề soi từ ẢNH: Ngô Sĩ Liên 2024 Bài 7 ý a, phần MB ⊥ OD của ý b (bỏ "Gọi I là trung điểm", khuôn bốn điểm duy nhất) ·
SGK KNTT 9 tập 1 Bài 5.30 ý a · Cầu Diễn 2025 Câu 4.2 ý a · tài liệu "4. Tiếp tuyến" Dạng 3 Bài 10 ý a ·
Quốc Oai 2024 Bài 4.2 phần MC.MD = R² của ý b (thêm "Biết ba điểm C, M, D thẳng hàng", đề gốc bắt chứng minh) ·
Hai Bà Trưng 2024 IV.1 · Nam Từ Liêm GK2 2025 IV.1 ·
BTVN: Ban Mai 2024 Bài 6a · Ngôi Sao 2024 4.1 · STK Trương Ngọc Vỹ C31 ý a, b tr.239, Bài 12 ý a tr.229 · Thọ Lộc lần 3 2025 IV.1 · Lý Sơn 2025 IV.2 ý a · Giang Biên Đề 01 2025 Câu 4.2 a, b.
Các đề ba tiếp tuyến có lời gần như nhau nên `check_khong_trung_de` chặn: Marie Curie 2024, STK Bài 10, Bài 15 không dùng được cùng Ví dụ 2.

Chạy lại được:
    .venv/bin/python inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-05/p5_ban3.py
Sau đó chạy scripts/phut_so_do.py <phiếu> --ghi rồi chạy lại script này để chép phút vào thuyết minh.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from p3_ban2 import R, h_nen_diem_ngoai, h_nen_duong_kinh_ngang, nen  # noqa: E402
from p3_ban3 import bai, giai_bon_diem, giai_trung_truc, gon_hinh, h_nen_tron_ngang, theo_so_do  # noqa: E402
from p4_ban2 import BR, LG, HEAD, END, d, goc, so_do  # noqa: E402
from p4_ban2 import giao, rong, xet  # noqa: E402
from p4_ban3 import h_nen_tron_tron  # noqa: E402
from scripts.tikz_geo import Fig, polar, tangent_points  # noqa: E402
from p3_ban3 import hai_tt  # noqa: E402

D_ = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"
PHIEU = D_ / "phieu-5-luyen-tap-chung.json"
TM = D_ / "thuyet-minh.json"
R_THE = 1.2

PHUT = {"Bài 3": 0, "Bài 4": 0, "BTVN 6": 0}
if PHIEU.exists():
    for _st in json.loads(PHIEU.read_text("utf-8"))["stages"]:
        for _b in _st["blocks"]:
            if _b.get("phut_so_do"):
                PHUT[_b["label"].rstrip(".")] = _b["phut_so_do"]


# ── Hình ───────────────────────────────────────────────────────────────────────
def ba_tt(goc_m: float, r: float = R):
    """Đường kính AB nằm ngang; tiếp tuyến tại điểm góc goc_m cắt tiếp tuyến tại A, B ở hai điểm."""
    a, b, m = (-r, 0.0), (r, 0.0), polar(goc_m, r)
    c = (-r, (r * r + r * m[0]) / m[1])
    dd = (r, (r * r - r * m[0]) / m[1])
    return a, b, m, c, dd


def h_ba_tt(ten_m, ten_c, ten_d, goc_m=112.0, r=R, nua=False, tia=("", ""), noi_o=True, day_mb=False, trung=None):
    """Hình đầy đủ: A, B, O, tiếp điểm, hai giao điểm; tia: tên hai tia nếu đề gọi Ax, By."""
    a, b, m, c, dd = ba_tt(goc_m, r)
    o = (0.0, 0.0)
    f = Fig()
    if nua:
        f.arc(o, r, 0, 180)
    else:
        f.circle(o, r)
    f.pt("O", o); f.pt("A", a); f.pt("B", b); f.pt(ten_m, m); f.pt(ten_c, c); f.pt(ten_d, dd)
    y_max = max(c[1], dd[1]) + 0.55
    if tia[0]:
        f.pt(tia[0], (-r, y_max), dot=False); f.seg("A", tia[0])
        f.pt(tia[1], (r, y_max), dot=False); f.seg("B", tia[1])
    else:
        f.seg("A", ten_c); f.seg("B", ten_d)
    f.seg("A", "B"); f.seg(ten_c, ten_d); f.seg("O", ten_m)
    if noi_o:
        f.seg("O", ten_c); f.seg("O", ten_d)
    f.right("A", o, c); f.right("B", o, dd); f.right(ten_m, o, dd)
    if day_mb:
        f.seg(ten_m, "B")
    return f.tikz()


def h_nen_nua(day_du):
    return h_nen_duong_kinh_ngang("A", "B", day_du)


def h_ngo_si_lien():
    a, b, m, c, dd = ba_tt(112.0)
    o = (0.0, 0.0)
    h = ((m[0] + b[0]) / 2, (m[1] + b[1]) / 2)
    f = Fig()
    f.circle(o, R)
    f.pt("O", o); f.pt("A", a); f.pt("B", b); f.pt("M", m); f.pt("C", c); f.pt("D", dd)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("O", "C"), ("O", "M"), ("O", "D"), ("M", "B")]:
        f.seg(u, v)
    f.right("A", o, c); f.right("B", o, dd); f.right("M", o, dd); f.right(h, m, dd)
    return f.tikz()


def h_con_lac():
    o, a, b = (0.0, 0.0), polar(240, 2.4), polar(300, 2.4)
    f = Fig()
    f.fill_sector(o, 2.4, 240, 300, style="brand!12")
    f.pt("O", o); f.pt("A", a); f.pt("B", b)
    f.seg("O", "A"); f.seg("O", "B")
    f.arc(o, 2.4, 240, 300)
    f.angle("O", "A", "B", r=0.55, text="$60^\\circ$")
    f.seglabel("O", "A", "$1{,}2$ m")
    return rong(f.tikz(), -4.6, -2.7, 4.6, 0.4)


def h_c31(goc_m=112.0):
    return rong(h_ba_tt("C", "M", "N", goc_m=goc_m, nua=True, tia=("x", "y")), -3.8, -0.4, 3.8, 3.0)


def h_quat_tron(do_quat, nhan_r, full=True, rong_khung=True):
    """Hình tròn tâm O, quạt AOB tô màu đối xứng qua trục đứng."""
    a0, a1 = 90 - do_quat / 2, 90 + do_quat / 2
    o, b, a = (0.0, 0.0), polar(a0, R), polar(a1, R)
    f = Fig()
    f.fill_sector(o, R, a0, a1, style="brand!18")
    if full:
        f.circle(o, R)
    else:
        f.arc(o, R, a0, a1)
    f.pt("O", o); f.pt("A", a); f.pt("B", b)
    f.seg("O", "A"); f.seg("O", "B")
    f.angle("O", "A", "B", r=0.4, text=f"${do_quat}^\\circ$")
    f.seglabel("O", "A", nhan_r)
    if not rong_khung:
        return f.tikz()
    return rong(f.tikz(), -4.6, -1.8 if full else -0.5, 4.6, 1.9)


def b12():
    """STK Bài 12: A ngoài (O), tiếp tuyến AB, AC; tiếp tuyến tại M thuộc cung nhỏ BC cắt AB, AC tại D, E."""
    a, o = (3.5, 0.0), (0.0, 0.0)
    t = tangent_points(o, R, a)
    b, c = (t[0], t[1]) if t[0][1] > 0 else (t[1], t[0])
    m = polar(18, R)
    q = (m[0] - m[1], m[1] + m[0])  # một điểm khác trên tiếp tuyến tại M
    return a, b, c, m, giao(m, q, a, b), giao(m, q, a, c)


def h_b12():
    a, b, c, m, dd, e = b12()
    o = (0.0, 0.0)
    f = Fig()
    f.circle(o, R)
    f.pt("O", o); f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("M", m); f.pt("D", dd); f.pt("E", e)
    for u, v in [("A", "B"), ("A", "C"), ("D", "E")]:
        f.seg(u, v)
    return f.tikz()


def kiem_toan_do():
    """Kết luận của đề phải đúng trên chính hình vẽ."""
    o = (0.0, 0.0)
    for g in (112.0, 120.0, 65.0):
        a, b, m, c, dd = ba_tt(g)
        assert abs(d(c, dd) - d(a, c) - d(b, dd)) < 1e-9                       # CD = AC + BD
        assert abs(c[0] * dd[0] + c[1] * dd[1]) < 1e-9                         # OC ⊥ OD
        assert abs(d(m, c) * d(m, dd) - R * R) < 1e-9                          # MC·MD = R²
        assert abs(d(o, c) * d(o, dd) - d(c, dd) * R) < 1e-9                   # OC·OD = CD·R
        assert abs(dd[0] * (m[0] - b[0]) + dd[1] * (m[1] - b[1])) < 1e-9       # MB ⊥ OD
    a, b, c, m, dd, e = b12()
    assert abs(d(a, dd) + d(dd, e) + d(e, a) - 2 * d(a, b)) < 1e-9             # chu vi ADE = 2AB
    # Số các câu đo lường, π ≈ 3,14
    p = 3.14
    assert round(60 / 360 * 2 * p * 1.2, 3) == 1.256
    assert round(120 / 360 * 2 * p * 15 + 30, 1) == 61.4
    assert round((1 - 120 / 360) * p * 225, 1) == 471.0
    assert round(72 / 360 * p * 16, 2) == 10.05
    assert round(p * (45**2 - 30**2), 2) == 3532.50
    assert round(72 / 360 * 2 * p * 50 + 100, 2) == 162.80
    assert round(0.3 * 72 / 360 * p * 2500, 2) == 471.00


# ── Sơ đồ ──────────────────────────────────────────────────────────────────────
def sd_bon_diem(dich, a1, b1, a2, b2, a3, b3) -> str:
    return (
        HEAD
        + f"  \\node[dich] (g) at (0,0) {{{dich}}};\n"
        + f"  \\node[o] (a1) at (-2.35,-1) {{{a1}}};\n  \\node[o] (b1) at (2.35,-1) {{{b1}}};\n"
        + f"  \\node[o] (a2) at (-2.35,-1.97) {{{a2}}};\n  \\node[o] (b2) at (2.35,-1.97) {{{b2}}};\n"
        + f"  \\node[gt] (a3) at (-2.35,-2.97) {{{a3}}};\n  \\node[gt] (b3) at (2.35,-2.97) {{{b3}}};\n"
        + "  \\draw[m] (a1.north) -- (a1.north |- g.south);\n  \\draw[m] (b1.north) -- (b1.north |- g.south);\n"
        + "  \\draw[m] (a2) -- (a1);\n  \\draw[m] (b2) -- (b1);\n  \\draw[m] (a3) -- (a2);\n  \\draw[m] (b3) -- (b2);\n"
        + END
    )


def sd_tong(dich, giua, trai, phai, trai_gt, phai_gt) -> str:
    """Thầy 05/11/2026: ba ô (hai đoạn bằng nhau, điểm nằm giữa) đều là điều kiện của đích nên ba mũi tên cùng trỏ về ô đích."""
    giua = giua.replace(" (", "\\\\(")
    return (
        HEAD
        + f"  \\node[dich] (g) at (0,0) {{{dich}}};\n"
        + f"  \\node[o] (l) at (-3.3,-1.3) {{{trai}}};\n  \\node[gt] (c) at (0,-1.3) {{{giua}}};\n  \\node[o] (r) at (3.3,-1.3) {{{phai}}};\n"
        + f"  \\node[gt] (l2) at (-3.3,-2.6) {{{trai_gt}}};\n  \\node[gt] (r2) at (3.3,-2.6) {{{phai_gt}}};\n"
        + "  \\draw[m] (l.north) |- (g.west);\n  \\draw[m] (c) -- (g);\n  \\draw[m] (r.north) |- (g.east);\n"
        + "  \\draw[m] (l2) -- (l);\n  \\draw[m] (r2) -- (r);\n"
        + END
    )


def sd_tich(dich, song, tiep_diem, cung_phu, goc_vuong, ben="", nen=None) -> str:
    return so_do(dich, song, [f"{tiep_diem}"], [cung_phu, goc_vuong] + ([nen] if nen else []), rong=3.1, buoc=1.0, ben=ben, ben_x=4.2 if ben else 0.0)


# ── Lời giải dùng lại ──────────────────────────────────────────────────────────
def giai_tong(x, y, m, a, b):
    """x, y: hai giao điểm; m: tiếp điểm giữa; a, b: hai tiếp điểm đầu đường kính."""
    return (
        f"${x}{a}$, ${x}{m}$ là hai tiếp tuyến của $(O)$ cắt nhau tại ${x}$ $\\Rightarrow {x}{a} = {x}{m}$.{BR}"
        f"${y}{b}$, ${y}{m}$ là hai tiếp tuyến của $(O)$ cắt nhau tại ${y}$ $\\Rightarrow {y}{b} = {y}{m}$.{BR}"
        f"${m}$ nằm giữa ${x}$ và ${y}$ $\\Rightarrow {x}{y} = {x}{m} + {m}{y}${BR}"
    )


def giai_tich(x, y, m, ly_do):
    return (
        f"${goc(x + 'O' + y)} = 90^\\circ$ ({ly_do}) $\\Rightarrow {goc(m + x + 'O')} = {goc(m + 'O' + y)}$ (cùng phụ với ${goc(x + 'O' + m)}$).{BR}"
        f"Xét $\\triangle {m}{x}O$ và $\\triangle {m}O{y}$ có:{BR}"
        f"${goc(x + m + 'O')} = {goc('O' + m + y)} = 90^\\circ$ (${x}{y}$ là tiếp tuyến của $(O)$ tại ${m}$){BR}"
        f"${goc(m + x + 'O')} = {goc(m + 'O' + y)}$ (chứng minh trên){BR}"
        f"$\\Rightarrow \\triangle {m}{x}O \\backsim \\triangle {m}O{y}$ (g.g){BR}"
        f"$\\Rightarrow \\dfrac{{{m}{x}}}{{{m}O}} = \\dfrac{{{m}O}}{{{m}{y}}}${BR}"
        f"$\\Rightarrow {m}{x} \\cdot {m}{y} = O{m}^2$"
    )


GHI_CHU_LT1 = (
    "Khoảng 62 phút với lớp C theo định mức: Bài 1 nhớ lại nhanh ~3′, Bài 2 bồn cây (hình in sẵn, GV nhắc cách làm ở Phiếu 1: xác định $R$, $n$ rồi thay công thức; "
    "hàng rào có cả hai bán kính) ~10′, Ví dụ 1 ~9′ (gồm 2′ vẽ), Bài 3 HS vẽ tiếp, đọc sơ đồ ngược rồi trình bày vào vở ~12′, Ví dụ 2 ~15′ (gồm 3′ vẽ; viết đủ nửa góc, cộng lại, $\\dfrac{1}{2} \\cdot 180^\\circ$ như SGK Toán 7 tập 1 tr.58), Bài 4 cùng cách ~14′. "
    "Bỏ gương treo, tầm nhìn, số đo cung trên lớp, chuyển câu Đúng/Sai về nhà để đủ giờ."
)
GHI_CHU_LT2 = (
    "Khoảng 15 phút với lớp C theo định mức: HS tự vẽ hình đề Ngô Sĩ Liên (~5′), tự trình bày ý b, phần $MB \\perp OD$ (~10′). Ý a (bốn điểm, đã học ở Phiếu 2) GV chữa ở phần chữa bài cuối buổi. "
    "Đề gốc ý b hỏi thêm $MB \\parallel OC$: Thầy chốt 05/11/2026 bỏ vì phải lấy góc vuông từ đường kính. Đề gốc ý a có \\textquotedblleft Gọi $I$ là trung điểm của $OC$\\textquotedblright: bỏ cho đúng khuôn bốn điểm."
)
GHI_CHU_BTVN = (
    "BTVN khoảng 65 phút với lớp C, dày hơn quỹ 40 phút để HS có thêm bài: BTVN 1, BTVN 2 trắc nghiệm đo lường (~4′), BTVN 3 Đúng/Sai (~4′), BTVN 4 vẽ tiếp hình rồi điền khung (~9′), BTVN 5 công viên (~9′), "
    "BTVN 6 tự vẽ hình, đọc sơ đồ ngược rồi trình bày vào vở (~15′), BTVN 7 tự vẽ hình, tự trình bày đề Giang Biên (~25′): ý b đúng khuôn đích Phiếu 4."
)


def lesson() -> dict:
    # ── Chặng 1 ────────────────────────────────────────────────────────────────
    kham_pha = {
        "kind": "review", "number": 1, "title": "Khám phá",
        "teacher_note": "Buổi luyện tập: HS đo thật trên Hình 1 rồi tự phát hiện ba điều sẽ chứng minh trong buổi (Định lí 2 dùng hai lần, $\\widehat{COD} = 90^\\circ$). Đo thấy bằng chưa phải là chứng minh. Chặng này ~3′.",
        "blocks": [
            {"type": "para", "text": "\\textbf{Ba tiếp tuyến của một nửa đường tròn}"},
            {"type": "noted", "variant": "note",
             "text": "Nửa đường tròn tâm $O$ đường kính $AB$; tiếp tuyến tại $M$ cắt tiếp tuyến tại $A$ và tại $B$ lần lượt ở $C$ và $D$ (Hình 1).[[br]]"
                     "\\textbf{a)} Dùng thước đo $CA$ và $CM$, $DB$ và $DM$. Có những đoạn nào bằng nhau?[[br]]"
                     "\\textbf{b)} So sánh $CD$ với $AC + BD$.[[br]]"
                     "\\textbf{c)} Dùng thước đo góc đo $\\widehat{COD}$.",
             "figure": {"tikz": h_ba_tt("M", "C", "D", goc_m=70.0, nua=True), "caption": "Hình 1", "pos": "right"}},
        ],
    }

    # ── Chặng 2: thẻ ───────────────────────────────────────────────────────────
    the_a1 = {
        "type": "noted", "variant": "theory", "title": "1. CUNG TRÒN, HÌNH QUẠT TRÒN, HÌNH VÀNH KHUYÊN (BÀI 15)",
        "text": "\\nhanly{Độ dài cung $n^\\circ$:} $l = \\dfrac{n}{360} \\cdot 2\\pi R$.[[br]]"
                "\\nhanly{Diện tích hình quạt tròn:} $S_q = \\dfrac{n}{360} \\cdot \\pi R^2$.[[br]]"
                "\\nhanly{Hình vành khuyên:} $S = \\pi R^2 - \\pi r^2$.[[br]]"
                "\\nhanly{Khi giải bài:} xác định $R$, $n$ rồi thay vào công thức; đề cho đường kính thì đổi ra bán kính trước.",
        "figure": {"tikz": h_quat_tron(120, "$R$", rong_khung=False), "caption": "Hình quạt tròn $OAB$", "pos": "right"},
    }
    the_a2 = {
        "type": "noted", "variant": "theory", "title": "2. KIẾN THỨC ĐÃ HỌC THƯỜNG DÙNG",
        "text": "\\nhanly{Tiếp tuyến (Bài 16):} Tiếp tuyến vuông góc với bán kính đi qua tiếp điểm.[[br]]"
                "\\nhanly{Hai tiếp tuyến cắt nhau (Bài 16):} $CA$, $CM$ là hai tiếp tuyến cắt nhau tại $C$ thì $CA = CM$, $OC$ là tia phân giác của $\\widehat{AOM}$.[[br]]"
                "\\nhanly{Định lí (SGK Toán 7 tập 1, tr.58):} Góc tạo bởi hai tia phân giác của hai góc kề bù là một góc vuông: "
                "$\\widehat{COM} = \\dfrac{1}{2}\\widehat{AOM}$, $\\widehat{MOD} = \\dfrac{1}{2}\\widehat{MOB}$ $\\Rightarrow \\widehat{COD} = \\dfrac{1}{2}(\\widehat{AOM} + \\widehat{MOB}) = \\dfrac{1}{2} \\cdot 180^\\circ = 90^\\circ$.",
        "figure": {"tikz": h_ba_tt("M", "C", "D", goc_m=70.0, r=R_THE, nua=True), "caption": "$OC$, $OD$ là hai tia phân giác của $\\widehat{AOM}$, $\\widehat{MOB}$", "pos": "right"},
    }
    the_dang_1 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 1. BA TIẾP TUYẾN: TÍNH TỔNG HAI ĐOẠN",
        "text": "\\nhanly{Phương pháp.} dùng Định lí 2 hai lần, tại hai giao điểm.[[br]]"
                "\\nhanly{Bước 1:} $CA = CM$ (hai tiếp tuyến cắt nhau tại $C$).[[br]]"
                "\\nhanly{Bước 2:} $DB = DM$ (hai tiếp tuyến cắt nhau tại $D$).[[br]]"
                "\\nhanly{Bước 3:} $M$ nằm giữa $C$ và $D$ $\\Rightarrow CD = CM + MD = AC + BD$.",
        "so_do_nguoc": sd_tong("$CD = AC + BD$", "$CD = CM + MD$ ($M$ nằm giữa $C$, $D$)", "$CM = CA$", "$MD = DB$",
                               "$CA$, $CM$ là hai\\\\tiếp tuyến cắt nhau tại $C$", "$DB$, $DM$ là hai\\\\tiếp tuyến cắt nhau tại $D$"),
    }
    the_dang_2 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 2. BA TIẾP TUYẾN: GÓC VUÔNG RỒI ĐẲNG THỨC TÍCH",
        "text": "\\nhanly{Phương pháp.} có góc vuông ở $O$, rồi đưa về hai tam giác đồng dạng.[[br]]"
                "\\nhanly{Bước 1:} $OC$, $OD$ là hai tia phân giác $\\Rightarrow \\widehat{COD} = \\dfrac{1}{2}(\\widehat{AOM} + \\widehat{MOB}) = \\dfrac{1}{2} \\cdot 180^\\circ = 90^\\circ$.[[br]]"
                "\\nhanly{Bước 2:} $\\widehat{MCO} = \\widehat{MOD}$ (cùng phụ với $\\widehat{COM}$).[[br]]"
                "\\nhanly{Bước 3:} $\\triangle MCO \\backsim \\triangle MOD$ (g.g) $\\Rightarrow MC \\cdot MD = OM^2 = R^2$.",
        "so_do_nguoc": sd_tich("$MC \\cdot MD = R^2$", ["$MC \\cdot MD = OM^2$", "$\\triangle MCO \\backsim \\triangle MOD$ (g.g)"],
                               f"${goc('CMO')} = {goc('OMD')} = 90^\\circ$\\\\($CD$ là tiếp tuyến tại $M$)",
                               f"${goc('MCO')} = {goc('MOD')}$\\\\(cùng phụ với ${goc('COM')}$)",
                               f"${goc('COD')} = \\dfrac{{1}}{{2}}({goc('AOM')} + {goc('MOB')}) = 90^\\circ$", ben="$R = OM$ (bán kính)",
                               nen=f"$OC$, $OD$ là hai tia phân giác;\\\\${goc('AOM')}$, ${goc('MOB')}$ kề bù"),
    }

    # ── Mạch 1: Câu IV.1 ───────────────────────────────────────────────────────
    bai_1 = bai(
        "Bài 1.", 1, "onclass", "NB1",
        "[NB] Một con lắc di chuyển từ vị trí $A$ đến vị trí $B$ (Hình 2). Biết sợi dây $OA$ có chiều dài bằng $1{,}2$ mét và số đo góc $AOB$ bằng $60^\\circ$ "
        "(lấy $\\pi \\approx 3{,}14$, sợi dây không giãn trong quá trình di chuyển). Độ dài quãng đường $AB$ mà con lắc di chuyển là:",
        "A",
        options=["$1{,}256$ m.", "$0{,}628$ m.", "$0{,}754$ m.", "$7{,}536$ m."],
        figure_given=True,
        figure={"tikz": h_con_lac(), "caption": "Hình 2", "pos": "right"},
    )
    bai_2 = bai(
        "Bài 2.", 2, "onclass", "TH1",
        "Một gia đình xây một bồn cây hình tròn có bán kính $OA$ là $15$ m (Hình 3). Phần quạt tròn $AOB$ (phần tô màu) với $\\widehat{AOB} = 120^\\circ$ được dùng để trồng hoa. "
        "Phần còn lại của hình tròn (phần không tô màu) dùng để lát gạch.[[br]]"
        "a) [TH] Chủ nhà làm hàng rào xung quanh phần trồng hoa (bao gồm cung tròn $AB$, $2$ bán kính $OA$, $OB$). Tính chiều dài hàng rào.[[br]]"
        "b) [TH] Tính diện tích phần lát gạch.[[br]]"
        "(Lấy $\\pi \\approx 3{,}14$, các kết quả làm tròn đến hàng phần mười.)",
        f"a) Độ dài cung $AB$: $l = \\dfrac{{120}}{{360}} \\cdot 2\\pi \\cdot 15 = 10\\pi \\approx 31{{,}}4$ (m).{BR}"
        f"Chiều dài hàng rào: $31{{,}}4 + 15 + 15 = 61{{,}}4$ (m).{BR}"
        f"Vậy hàng rào dài khoảng $61{{,}}4$ m.{BR}"
        f"b) Phần lát gạch là hình quạt tròn có số đo cung $360^\\circ - 120^\\circ = 240^\\circ$.{BR}"
        f"$S = \\dfrac{{240}}{{360}} \\cdot \\pi \\cdot 15^2 = 150\\pi \\approx 471{{,}}0$ ($\\text{{m}}^2$).{BR}"
        f"Vậy diện tích phần lát gạch khoảng $471{{,}}0$ $\\text{{m}}^2$.",
        figure_given=True,
        figure={"tikz": h_quat_tron(120, "$15$ m"), "caption": "Hình 3", "pos": "right"},
        hints=["Hàng rào gồm những đoạn nào? Đã tính đủ chưa?", "Phần lát gạch chiếm bao nhiêu phần của hình tròn?"],
    )

    # ── Mạch 3: tổng hai đoạn ──────────────────────────────────────────────────
    vd1 = h_ba_tt("P", "M", "N", goc_m=62.0)
    vi_du_1 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 1.} Cho đường tròn $(O)$ đường kính $AB$, tiếp tuyến $xx'$ tại $A$ và tiếp tuyến $yy'$ tại $B$ của $(O)$. "
                "Một tiếp tuyến thứ ba của $(O)$ tại điểm $P$ ($P$ khác $A$ và $B$) cắt $xx'$ tại $M$ và cắt $yy'$ tại $N$ (Hình 4). "
                "Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề. Chứng minh rằng $MN = MA + NB$."
                f"{BR}{LG}{BR}"
                f"$MA$, $MP$ là hai [[fill:tiếp tuyến]] của $(O)$ cắt nhau tại $M$ $\\Rightarrow MA = [[fill:MP]]$.{BR}"
                f"$NB$, $NP$ là hai tiếp tuyến của $(O)$ cắt nhau tại $N$ $\\Rightarrow NB = [[fill:NP]]$.{BR}"
                f"$P$ nằm giữa $M$ và $N$ $\\Rightarrow MN = [[fill:MP + PN|1.8cm]]${BR}"
                "Vậy $MN = MA + [[fill:NB]]$.",
        "figure": {"tikz": h_nen_tron_ngang("A", "B", vd1), "tikz_gv": vd1, "caption": "Hình 4", "pos": "right"},
        "so_do_nguoc": sd_tong("$MN = MA + NB$", "$MN = [[fill:MP + PN|1.8cm]]$ ($P$ nằm giữa $M$, $N$)", "$MP = [[fill:MA]]$", "$PN = [[fill:NB]]$",
                               "$MA$, $MP$ là hai [[fill:tiếp tuyến]]\\\\cắt nhau tại $M$", "$NB$, $NP$ là hai\\\\tiếp tuyến cắt nhau tại $N$"),
    }
    cd = h_ba_tt("M", "C", "D", goc_m=118.0)
    bai_3 = bai(
        "Bài 3.", 2, "onclass", "TH3",
        "[TH] Cho đường tròn $(O; R)$, đường kính $AB$. Trên đường tròn $(O)$ lấy điểm $M$ ($MA < MB$). Tiếp tuyến tại $M$ cắt tiếp tuyến tại $A$ và $B$ lần lượt là $C$ và $D$ (Hình 5). "
        f"Chứng minh $CD = AC + BD$. {theo_so_do(5)}",
        giai_tong("C", "D", "M", "A", "B") + "Vậy $CD = AC + BD$.",
        figure={"tikz": h_nen_tron_ngang("A", "B", cd), "tikz_gv": cd, "caption": "Hình 5", "pos": "right"},
        so_do_nguoc=sd_tong("$CD = AC + BD$", "$CD = CM + MD$ ($M$ nằm giữa $C$, $D$)", "$CM = AC$", "$MD = BD$",
                            "$CA$, $CM$ là hai\\\\tiếp tuyến cắt nhau tại $C$", "$DB$, $DM$ là hai\\\\tiếp tuyến cắt nhau tại $D$"),
        phut_so_do=PHUT["Bài 3"], ve_tiep=3,
    )

    # ── Mạch 4: góc vuông, tích ────────────────────────────────────────────────
    vd2 = h_ba_tt("M", "C", "D", goc_m=66.0, nua=True, tia=("x", "y"))
    vi_du_2 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 2.} Cho nửa đường tròn tâm $O$, đường kính $AB$. Kẻ các tiếp tuyến $Ax$, $By$ cùng phía với nửa đường tròn đối với $AB$. "
                "Từ điểm $M$ trên nửa đường tròn kẻ tiếp tuyến thứ ba với đường tròn, nó cắt $Ax$ và $By$ lần lượt tại $C$ và $D$ (Hình 6). "
                "Vẽ tiếp vào Hình 6 các yếu tố còn thiếu theo đề. Chứng minh tam giác $COD$ là tam giác vuông và $MC \\cdot MD = OM^2$."
                f"{BR}{LG}{BR}"
                f"$CA$, $CM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C$ $\\Rightarrow OC$ là [[fill:tia phân giác]] của ${goc('AOM')}${BR}"
                f"$\\Rightarrow {goc('COM')} = [[fill:\\dfrac{{1}}{{2}}\\widehat{{AOM}}|1.6cm]]$.{BR}"
                f"$DB$, $DM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $D$ $\\Rightarrow OD$ là tia phân giác của ${goc('MOB')}${BR}"
                f"$\\Rightarrow {goc('MOD')} = [[fill:\\dfrac{{1}}{{2}}\\widehat{{MOB}}|1.6cm]]$.{BR}"
                f"${goc('COD')} = {goc('COM')} + {goc('MOD')} = \\dfrac{{1}}{{2}}({goc('AOM')} + {goc('MOB')})$.{BR}"
                f"${goc('AOM')}$, ${goc('MOB')}$ là hai góc [[fill:kề bù]] $\\Rightarrow {goc('AOM')} + {goc('MOB')} = 180^\\circ$.{BR}"
                f"$\\Rightarrow {goc('COD')} = \\dfrac{{1}}{{2}} \\cdot 180^\\circ = [[fill:90^\\circ]]$.{BR}"
                f"$\\Rightarrow \\triangle COD$ vuông tại $O$.{BR}"
                f"${goc('MCO')} = [[fill:\\widehat{{MOD}}]]$ (cùng phụ với ${goc('COM')}$).{BR}"
                f"Xét $\\triangle MCO$ và $\\triangle MOD$ có:{BR}"
                f"${goc('CMO')} = {goc('OMD')} = 90^\\circ$ ($CD$ là [[fill:tiếp tuyến]] của $(O)$ tại $M$){BR}"
                f"${goc('MCO')} = {goc('MOD')}$ (chứng minh trên){BR}"
                f"$\\Rightarrow \\triangle MCO \\backsim \\triangle [[fill:MOD]]$ (g.g){BR}"
                f"$\\Rightarrow \\dfrac{{MC}}{{MO}} = [[fill:\\dfrac{{MO}}{{MD}}|1.3cm]]${BR}"
                "Vậy $\\triangle COD$ vuông tại $O$ và $MC \\cdot MD = [[fill:OM^2]]$.",
        "figure": {"tikz": h_nen_nua(vd2), "tikz_gv": vd2, "caption": "Hình 6", "pos": "right"},
        "so_do_nguoc": sd_tich("$MC \\cdot MD = [[fill:OM^2]]$", ["$\\triangle MCO \\backsim \\triangle [[fill:MOD]]$ (g.g)"],
                               f"${goc('CMO')} = {goc('OMD')} = 90^\\circ$\\\\($CD$ là [[fill:tiếp tuyến]] tại $M$)",
                               f"${goc('MCO')} = [[fill:\\widehat{{MOD}}]]$\\\\(cùng phụ với ${goc('COM')}$)",
                               f"${goc('COD')} = \\dfrac{{1}}{{2}}({goc('AOM')} + {goc('MOB')}) = [[fill:90^\\circ]]$",
                               nen=f"$OC$, $OD$ là hai [[fill:tia phân giác]];\\\\${goc('AOM')}$, ${goc('MOB')}$ [[fill:kề bù]]"),
    }
    # Quốc Oai: D dựng từ OD ⊥ OC nên hình đầy đủ không kẻ thêm gì khác hình ba tiếp tuyến.
    qo = h_ba_tt("M", "C", "D", goc_m=108.0, nua=True, tia=("x", "y"))
    bai_4 = bai(
        "Bài 4.", 2, "onclass", "TH4",
        "[TH] Cho nửa đường tròn $(O, R)$ đường kính $AB$. Kẻ tiếp tuyến $Ax$ cùng phía với nửa đường tròn. Trên tia $Ax$ lấy điểm $C$, kẻ tiếp tuyến thứ hai $CM$ tới nửa đường tròn. "
        "Đường thẳng vuông góc với $OC$ tại $O$ cắt tiếp tuyến tại $B$ của $(O)$ ở $D$. Biết ba điểm $C$, $M$, $D$ thẳng hàng (Hình 7). "
        f"Chứng minh $MC \\cdot MD = R^2$. {theo_so_do(7)}",
        giai_tich("C", "D", "M", "$OD \\perp OC$ tại $O$")
        + f".{BR}Vậy $MC \\cdot MD = R^2$ (vì $OM = R$).",
        figure={"tikz": h_nen_nua(qo), "tikz_gv": qo, "caption": "Hình 7", "pos": "right"},
        so_do_nguoc=sd_tich("$MC \\cdot MD = R^2$", ["$MC \\cdot MD = OM^2$", "$\\triangle MCO \\backsim \\triangle MOD$ (g.g)"],
                            f"${goc('CMO')} = {goc('OMD')} = 90^\\circ$\\\\($CD$ là tiếp tuyến tại $M$)",
                            f"${goc('MCO')} = {goc('MOD')}$\\\\(cùng phụ với ${goc('COM')}$)",
                            f"${goc('COD')} = 90^\\circ$ ($OD \\perp OC$ tại $O$)", ben="$R = OM$ (bán kính)"),
        phut_so_do=PHUT["Bài 4"], ve_tiep=3,
    )

    # ── LT2: đích Ngô Sĩ Liên ──────────────────────────────────────────────────
    nsl = h_ngo_si_lien()
    bai_5 = bai(
        "Bài 5.", 2, "onclass", "TH2",
        "Cho đường tròn tâm $O$ đường kính $AB = 2R$ và một điểm $M$ tùy ý trên đường tròn ($M$ khác $A$, $B$). Các tiếp tuyến của $(O)$ tại $A$ và $M$ cắt nhau tại $C$.[[br]]"
        "a) [TH] Chứng minh rằng bốn điểm $C$, $M$, $O$, $A$ cùng thuộc đường tròn đường kính $OC$.[[br]]"
        "b) [TH] Tiếp tuyến của đường tròn $(O)$ tại $B$ cắt tia $CM$ tại $D$. Chứng minh rằng $MB \\perp OD$.",
        "a) " + giai_bon_diem("C", "A", "M")
        + f"Vậy bốn điểm $C, M, O, A$ cùng thuộc đường tròn đường kính $OC$.{BR}"
        + "b) " + giai_trung_truc("D", "M", "B", ket=f".{BR}Vậy $MB \\perp OD$."),
        figure_given=False, draw=True,
        figure={"tikz": h_nen_tron_ngang("A", "B", nsl), "tikz_gv": nsl, "caption": "Hình 8", "pos": "right"},
        hints=["Ý a: đỉnh góc vuông thuộc đường tròn đường kính nào? Ý b: hai điểm nào cùng cách đều $M$ và $B$?"],
    )

    # ── BTVN ───────────────────────────────────────────────────────────────────
    btvn_1 = bai(
        "BTVN 1.", 1, "btvn", "NB1",
        "[NB] Diện tích hình quạt tròn có bán kính $4$ cm và số đo cung là $72^\\circ$ (lấy $\\pi \\approx 3{,}14$ và làm tròn kết quả đến hàng phần trăm) là:",
        "A",
        options=["$10{,}05$ $\\text{cm}^2$.", "$5{,}02$ $\\text{cm}^2$.", "$50{,}24$ $\\text{cm}^2$.", "$40{,}19$ $\\text{cm}^2$."],
        figure_given=True,
    )
    btvn_2 = bai(
        "BTVN 2.", 1, "btvn", "NB1",
        "[NB] Một chiếc đèn thả hình vành khuyên, rỗng ở giữa, có đường kính đường tròn lớn là $90$ cm, đường kính đường tròn nhỏ là $60$ cm. "
        "Diện tích bề mặt của chiếc đèn (lấy $\\pi \\approx 3{,}14$, làm tròn kết quả đến hàng phần trăm) là:",
        "C",
        options=["$14130{,}00$ $\\text{cm}^2$.", "$942{,}00$ $\\text{cm}^2$.", "$3532{,}50$ $\\text{cm}^2$.", "$2826{,}00$ $\\text{cm}^2$."],
        figure_given=True,
    )
    khung = (
        "$DB$, $DM$ là hai [[blank:2.4cm]] của $(O)$ cắt nhau tại $D$[[br]]"
        "$\\Rightarrow DM = [[blank:1.1cm]]$.[[br]]"
        "$EC$, $EM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $E$[[br]]"
        "$\\Rightarrow EM = [[blank:1.1cm]]$.[[br]]"
        "b) [NB] Chứng minh chu vi $\\triangle ADE = 2AB$:[[br]]"
        "$M$ nằm giữa $D$ và $E$ $\\Rightarrow DE = DM + [[blank:1.1cm]]$.[[br]]"
        "Chu vi $\\triangle ADE = AD + DE + EA = AD + DB + EC + EA = AB + [[blank:1.1cm]]$.[[br]]"
        "$AB$, $AC$ là hai tiếp tuyến của $(O)$ cắt nhau tại $A$ $\\Rightarrow AB = [[blank:1.1cm]]$.[[br]]"
        "Vậy chu vi $\\triangle ADE = [[blank:1.6cm]]$."
    )
    b12_ = rong(h_b12(), -3.2, -1.8, 5.0, 1.8)
    btvn_3 = bai(
        "BTVN 3.", 1, "btvn", "NB2",
        "Cho nửa đường tròn $(O)$ đường kính $AB$. Về cùng phía với nửa đường tròn, vẽ hai tia $Ax$, $By$ vuông góc với $AB$. Gọi $M$ là một điểm bất kì thuộc tia $Ax$. "
        "Qua $M$ kẻ tiếp tuyến $MC$ ($C$ là tiếp điểm) với nửa đường tròn $(O)$, cắt $By$ tại $N$ (Hình 9). Mỗi khẳng định sau đúng hay sai?",
        "a) Đ · b) S",
        dung_sai=["$\\widehat{AOM} = \\widehat{COM}$.", "$\\widehat{MON} = 80^\\circ$."],
        figure_given=True,
        figure={"tikz": h_c31(), "caption": "Hình 9", "pos": "right"},
    )
    btvn_4 = bai(
        "BTVN 4.", 1, "btvn", "NB3",
        "Từ điểm $A$ nằm ngoài đường tròn $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ (với $B$ và $C$ là các tiếp điểm). Qua điểm $M$ thuộc cung nhỏ $BC$ vẽ tiếp tuyến với đường tròn $(O)$, "
        "cắt các tiếp tuyến $AB$, $AC$ lần lượt tại $D$ và $E$ (Hình 10).[[br]]"
        "Vẽ tiếp vào Hình 10 các yếu tố còn thiếu theo đề, rồi điền vào chỗ chấm để hoàn thành bài giải:[[br]]"
        "a) [NB] Chứng minh $DM = DB$, $EM = EC$:[[br]]" + khung,
        "a) tiếp tuyến; $DB$; $EC$.[[br]]b) $ME$; $AC$; $AC$; $2AB$.",
        statement_slide="Từ điểm $A$ nằm ngoài đường tròn $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ (với $B$ và $C$ là các tiếp điểm). Qua điểm $M$ thuộc cung nhỏ $BC$ vẽ tiếp tuyến với đường tròn $(O)$, "
                        "cắt các tiếp tuyến $AB$, $AC$ lần lượt tại $D$ và $E$ (Hình 10).[[br]]a) [NB] Chứng minh $DM = DB$, $EM = EC$.[[br]]b) [NB] Chứng minh chu vi $\\triangle ADE = 2AB$.",
        figure_given=True, ve_tiep=3,
        figure={"tikz": h_nen_tron_tron(b12_), "tikz_gv": b12_, "caption": "Hình 10", "pos": "right"},
    )
    btvn_5 = bai(
        "BTVN 5.", 2, "btvn", "TH1",
        "Một công viên có dạng một hình quạt tròn $OAB$ (Hình 11) giới hạn bởi hai bán kính $OA$, $OB$ sao cho $OA = 50$ m, $\\widehat{AOB} = 72^\\circ$.[[br]]"
        "a) [TH] Nếu người ta làm hàng rào xung quanh công viên thì hàng rào có chiều dài là bao nhiêu?[[br]]"
        "b) [TH] Người ta trồng cỏ trong công viên với diện tích bằng $30\\%$ diện tích công viên. Tính diện tích trồng cỏ trong công viên.[[br]]"
        "(Lấy $\\pi \\approx 3{,}14$ và các kết quả làm tròn $2$ chữ số thập phân.)",
        f"a) Độ dài cung $AB$: $l = \\dfrac{{72}}{{360}} \\cdot 2\\pi \\cdot 50 = 20\\pi \\approx 62{{,}}80$ (m).{BR}"
        f"Chiều dài hàng rào: $62{{,}}80 + 50 + 50 = 162{{,}}80$ (m).{BR}"
        f"Vậy hàng rào dài khoảng $162{{,}}80$ m.{BR}"
        f"b) Diện tích công viên: $S_q = \\dfrac{{72}}{{360}} \\cdot \\pi \\cdot 50^2 = 500\\pi \\approx 1570$ ($\\text{{m}}^2$).{BR}"
        f"Diện tích trồng cỏ: $30\\% \\cdot 1570 = 471{{,}}00$ ($\\text{{m}}^2$).{BR}"
        f"Vậy diện tích trồng cỏ khoảng $471{{,}}00$ $\\text{{m}}^2$.",
        figure_given=True,
        figure={"tikz": h_quat_tron(72, "$50$ m", full=False), "caption": "Hình 11", "pos": "right"},
        hints=["Hàng rào gồm những đoạn nào?", "Diện tích công viên tính bằng công thức nào?"],
    )
    ls = _ly_son()
    btvn_6 = bai(
        "BTVN 6.", 2, "btvn", "TH2",
        "[TH] Cho đường tròn $(O)$, đường kính $AB$. Kẻ tiếp tuyến $Ax$ với đường tròn $(O)$. Lấy điểm $C$ thuộc đường tròn $(O)$ ($AC < CB$). "
        "Kẻ tiếp tuyến tại $C$ của đường tròn $(O)$ cắt $Ax$ tại điểm $M$ (Hình 12). Chứng minh bốn điểm $M$, $A$, $C$, $O$ cùng thuộc một đường tròn. "
        "Vẽ tiếp vào Hình 12 các yếu tố còn thiếu, rồi dựa vào sơ đồ ngược để trình bày bài giải vào vở.",
        giai_bon_diem("M", "A", "C") + "Vậy bốn điểm $M, A, C, O$ cùng thuộc đường tròn đường kính $MO$.",
        draw=True, phut_so_do=PHUT["BTVN 6"],
        figure={"tikz": h_nen_tron_ngang("A", "B", ls), "tikz_gv": ls, "caption": "Hình 12", "pos": "right"},
        so_do_nguoc=sd_bon_diem("$M$, $A$, $C$, $O$ cùng thuộc đường tròn đường kính $MO$",
                                "$M$, $A$, $O$ cùng thuộc\\\\đường tròn đường kính $MO$", "$M$, $C$, $O$ cùng thuộc\\\\đường tròn đường kính $MO$",
                                "$\\triangle MAO$ vuông tại $A$", "$\\triangle MCO$ vuông tại $C$",
                                "$MA$ là tiếp tuyến\\\\của $(O)$ tại $A$", "$MC$ là tiếp tuyến\\\\của $(O)$ tại $C$"),
    )
    gb = hai_tt("A", "B", "C", "H")
    btvn_7 = bai(
        "BTVN 7.", 3, "btvn", "TH2+VD1",
        "Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn. Vẽ các tiếp tuyến $AB$, $AC$ với đường tròn $(O)$ ($B$, $C$ là các tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$.[[br]]"
        "a) [TH] Chứng minh bốn điểm $A$, $B$, $C$, $O$ cùng thuộc một đường tròn.[[br]]"
        "b) [VD] Chứng minh $OA$ là trung trực của $BC$ và $OH \\cdot OA = R^2$.",
        "a) " + giai_bon_diem("A", "B", "C")
        + f"Vậy bốn điểm $A, B, C, O$ cùng thuộc đường tròn đường kính $AO$.{BR}"
        + "b) " + giai_trung_truc("A", "B", "C", ket=f"{BR}$\\Rightarrow OA \\perp BC$ tại $H$.{BR}", duong="OA")
        + xet("OHB", "OBA", f"{goc('OHB')} = {goc('OBA')}", "$OA \\perp BC$ tại $H$, $AB$ là tiếp tuyến của $(O)$ tại $B$", goc("AOB"),
              "\\dfrac{OH}{OB} = \\dfrac{OB}{OA}", "OH \\cdot OA = OB^2") + f".{BR}"
        + "Vậy $OA$ là trung trực của $BC$ và $OH \\cdot OA = R^2$ (vì $OB = R$).",
        figure_given=False, draw=True,
        figure={"tikz": h_nen_diem_ngoai("A", gb), "tikz_gv": gb, "caption": "Hình 13", "pos": "right"},
        hints=["Hai điểm nào cùng cách đều $B$ và $C$? Đẳng thức $OH \\cdot OA = OB^2$ có được từ tỉ lệ thức nào?"],
    )

    return {
        "slug": PHIEU.stem,
        "title": "Luyện tập chung: hình ba tiếp tuyến của nửa đường tròn và bài toán đo lường",
        "eyebrow": "PHIẾU 5 • HÌNH HỌC 9 · CHƯƠNG V — LUYỆN TẬP CHUNG",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "btvn_phieu_rieng": True,
        "stages": [
            kham_pha,
            {"kind": "concept", "number": 2, "title": "Kiến thức trọng tâm",
             "teacher_note": "Chặng này ~5′, chỉ nhắc: thẻ 1 cho Câu IV.1 (đã học ở Phiếu 1), thẻ 2 cho hình ba tiếp tuyến. "
                             "Hai dạng B đọc lướt theo sơ đồ, giảng kỹ ở ví dụ. Đẳng thức tích nhóm hai tiếp tuyến có sẵn tam giác vuông chiếm 24\\% đề Kì I; "
                             "phiếu này không dùng góc vuông từ đường kính.",
             "blocks": [
                 {"type": "para", "variant": "part", "text": "A. Lý thuyết"},
                 the_a1, the_a2,
                 {"type": "para", "variant": "part", "text": "B. Phương pháp chứng minh — các dạng quen thuộc"},
                 the_dang_1, the_dang_2,
             ]},
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "teacher_note": GHI_CHU_LT1,
             "blocks": [
                 {"type": "para", "text": "\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề Ngô Sĩ Liên) ở Bài 5: ý a chứng minh bốn điểm cùng thuộc một đường tròn "
                                          "(đã học ở Phiếu 2), ý b chứng minh vuông góc (đã học ở Phiếu 3) trên hình ba tiếp tuyến."},
                 {"type": "para", "variant": "heading", "text": "Mạch 1. Câu IV.1 — Cung tròn, hình quạt tròn trong bài thực tế"},
                 bai_1, bai_2,
                 {"type": "para", "variant": "heading", "text": "Mạch 2. Ba tiếp tuyến — Tính tổng hai đoạn"},
                 vi_du_1, bai_3,
                 {"type": "para", "variant": "heading", "text": "Mạch 3. Ba tiếp tuyến — Góc vuông rồi đẳng thức tích"},
                 vi_du_2, bai_4,
             ]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "teacher_note": GHI_CHU_LT2,
             "blocks": [
                 {"type": "para", "variant": "heading", "text": "Đề thi Học kì I — THCS Ngô Sĩ Liên (Hoàn Kiếm)"},
                 bai_5,
             ]},
            {"kind": "reflection", "number": 5, "title": "Sơ đồ tư duy",
             "teacher_note": GHI_CHU_BTVN,
             "blocks": [
                 {"type": "mindmap", "caption": "Sơ đồ tư duy: Hình ba tiếp tuyến của nửa đường tròn",
                  "root": "BA TIẾP TUYẾN",
                  "branches": [
                      {"label": "ĐOẠN THẲNG", "children": [{"label": "$CA = CM$, $DB = DM$"},
                                                            {"label": "$CD = AC + BD$"}]},
                      {"label": "GÓC", "children": [{"label": "$OC$, $OD$ là hai tia phân giác"},
                                                     {"label": "$\\widehat{COD} = 90^\\circ$"}]},
                      {"label": "TÍCH", "children": [{"label": "$\\triangle MCO \\backsim \\triangle MOD$ (g.g)"},
                                                      {"label": "$MC \\cdot MD = OM^2 = R^2$"}]},
                      {"label": "VUÔNG GÓC", "children": [{"label": "$OD$ là đường trung trực của $MB$"},
                                                           {"label": "$MB \\perp OD$"}]},
                  ]},
                 btvn_1, btvn_2, btvn_3, btvn_4, btvn_5, btvn_6, btvn_7,
             ]},
        ],
    }


def _ly_son():
    """Lý Sơn ý a: tiếp tuyến Ax, tiếp tuyến tại C cắt Ax tại M (AC < CB nên C gần A)."""
    a, b, c_, m_, _ = ba_tt(118.0)
    o = (0.0, 0.0)
    # Đặt tên theo đề: tiếp điểm C, giao điểm M.
    c, m = c_, m_
    f = Fig()
    f.circle(o, R)
    f.pt("O", o); f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("M", m)
    x = (-R, m[1] + 0.5)
    f.pt("x", x, dot=False)
    for u, v in [("A", "B"), ("A", "x"), ("M", "C"), ("O", "M"), ("O", "C")]:
        f.seg(u, v)
    f.right("A", o, m); f.right("C", o, m)
    return f.tikz()


# ── Thuyết minh ────────────────────────────────────────────────────────────────
GIO_THUC_TM = [
    "\\quad Giờ thực lớp C (05/11/2026): Khám phá $+$ Kiến thức 8′ · Luyện tập 1 khoảng 62′ (1 trắc nghiệm, 1 bài Câu IV.1, 2 ví dụ HS vẽ cùng GV và điền sơ đồ ngược, "
    "2 bài theo sơ đồ ngược HS trình bày vào vở $+$ vẽ tiếp hình)",
    "\\quad Luyện tập 2 khoảng 15′ (đề đích Ngô Sĩ Liên, ý b phần $MB \\perp OD$, HS tự vẽ) · chữa bài (có ý a đề đích), chốt khoảng 5′ · BTVN khoảng 65′ (quỹ 40′, cố ý dày hơn)",
]
DANG_VD_5 = ("Buổi 5 — Câu IV.2 hai ý (đề Ngô Sĩ Liên, hình ba tiếp tuyến): bốn điểm $C$, $M$, $O$, $A$ cùng thuộc đường tròn đường kính $OC$; $MB \\perp OD$ (đường trung trực). "
             "Đề gốc còn hỏi $MB \\parallel OC$: bỏ vì phải lấy góc vuông từ đường kính (Thầy 05/11/2026). Dạng VD của buổi: $\\widehat{COD} = 90^\\circ$ rồi $MC \\cdot MD = R^2$. BTVN: đề Giang Biên Đề 01 ($OH \\cdot OA = R^2$).")
VIDU_5 = ("Buổi 5: SGK 5.30 ý a: ba tiếp tuyến — $MN = MA + NB$. Tài liệu Tiếp tuyến Dạng 3 Bài 10 ý a — $\\triangle COD$ vuông và $MC \\cdot MD = OM^2$.")
LOISAI_5 = ("Buổi 5: nhầm $C$, $D$ (giao điểm các tiếp tuyến) với tiếp điểm; cộng đoạn $CD = CM + MD$ mà quên $M$ nằm giữa $C$ và $D$; "
            "viết sai thứ tự đỉnh $\\triangle MCO \\backsim \\triangle MOD$; tính hàng rào quên hai bán kính; đề cho đường kính mà thay thẳng vào chỗ bán kính.")
NEN_KE_BU = "\\textbf{Góc tạo bởi hai tia phân giác của hai góc kề bù là một góc vuông} (Định lí, SGK Toán 7 tập 1, Luyện tập chung, Ví dụ, tr.58): viết đủ $\\widehat{COM} = \\dfrac{1}{2}\\widehat{AOM}$, $\\widehat{MOD} = \\dfrac{1}{2}\\widehat{MOB}$, cộng lại, $\\dfrac{1}{2} \\cdot 180^\\circ = 90^\\circ$ — chứng minh $\\widehat{COD} = 90^\\circ$ (buổi 5)."


def dong_tm(phut) -> list[dict]:
    quy = ["$OC$, $OD$ là hai tia phân giác $\\Rightarrow \\widehat{COD} = \\dfrac{1}{2}(\\widehat{AOM} + \\widehat{MOB}) = 90^\\circ$",
           "$\\widehat{MCO} = \\widehat{MOD}$ (cùng phụ với $\\widehat{COM}$), góc vuông tại $M$ $\\Rightarrow \\triangle MCO \\backsim \\triangle MOD$ (g.g) $\\Rightarrow MC \\cdot MD = OM^2$",
           "BTVN: $OA$ là đường trung trực của $BC$ rồi $\\triangle OHB \\backsim \\triangle OBA$ (g.g) $\\Rightarrow OH \\cdot OA = R^2$ (như Phiếu 4)"]
    return [
        {"band": "NB", "loai": "NB lẻ LT", "dang": "Câu IV.1, trắc nghiệm: độ dài cung (con lắc, trên lớp); diện tích hình quạt tròn, hình vành khuyên (BTVN, đề Ban Mai, đề Ngôi Sao)",
         "source_refs": ["ck1-hai-ba-trung-2024-IV1", "ck1-ban-mai-2024-6a", "ck1-ngoi-sao-2024-4.1"], "vidu": 0, "onclass": 1, "btvn": 2, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB kiến thức cũ", "dang": "Đúng/Sai trên hình ba tiếp tuyến (BTVN): $\\widehat{AOM} = \\widehat{COM}$ (Định lí 2), $\\widehat{MON} = 80^\\circ$ (góc tạo bởi hai tia phân giác của hai góc kề bù, SGK Toán 7 tập 1, tr.58)",
         "source_refs": ["stk-b16-II-C31-tr239.a", "stk-b16-II-C31-tr239.b"], "vidu": 0, "onclass": 0, "btvn": 2, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB ghép bài", "dang": "Vẽ tiếp hình nền, điền khung bài giải: Định lí 2 ba lần rồi chu vi $\\triangle ADE = 2AB$ (BTVN, STK Bài 12 ý a)",
         "source_refs": ["stk-b16-A-B12-tr229.a"], "vidu": 0, "onclass": 0, "btvn": 2, "lythuyet": 0, "decompose": "none",
         "hinh_san": True, "gian_giao": "dien-khuyet", "khung": True, "ve_tiep": {"btvn": 3}},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Câu IV.1 hai ý, hình in sẵn: chiều dài hàng rào (cung $+$ hai bán kính) và diện tích phần còn lại (trên lớp đề Nam Từ Liêm: bồn cây; BTVN đề Thọ Lộc: công viên). Ví dụ mẫu ở Phiếu 1",
         "source_refs": ["gk2-nam-tu-liem-2025-IV1", "v10-tho-loc-3-2025-IV1"], "vidu": 0, "onclass": 2, "btvn": 2, "lythuyet": 0, "decompose": "th2nb", "hinh_san": True},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Hai ý của đề thi. Trên lớp HS tự vẽ hình, tự trình bày đề đích Ngô Sĩ Liên: ý a bốn điểm, phần $MB \\perp OD$ của ý b (đường trung trực). BTVN: bốn điểm đọc sơ đồ ngược (đề Lý Sơn ý a), tự trình bày (đề Giang Biên Đề 01 ý a)",
         "source_refs": ["ck1-ngo-si-lien-2024-7.a", "ck1-ngo-si-lien-2024-7.b", "ck1-ly-son-2025-IV2.a", "ck1-giang-bien-2025-de01-4.2.a"], "vidu": 0, "onclass": 2, "btvn": 2, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_hinh": {"onclass": 1, "btvn": 2}, "phut_so_do": {"btvn": phut["BTVN 6"]}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Ba tiếp tuyến: Định lí 2 hai lần $\\Rightarrow CD = AC + BD$. Ví dụ mẫu SGK 5.30 ý a; HS vẽ tiếp hình nền, đọc sơ đồ ngược rồi tự trình bày vào vở (đề Cầu Diễn ý a)",
         "source_refs": ["sgk-5.30.a", "ck1-cau-dien-42.a"], "vidu": 1, "onclass": 1, "btvn": 0, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"vidu": 2, "onclass": 3}, "phut_so_do": {"onclass": phut["Bài 3"]}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Ba tiếp tuyến: đẳng thức tích $MC \\cdot MD = R^2$ theo sơ đồ ngược (đề Quốc Oai, phần $MC \\cdot MD = R^2$ của ý b). Ví dụ mẫu ở dòng VD",
         "source_refs": ["ck1-quoc-oai-2024-4.2.b"], "vidu": 0, "onclass": 1, "btvn": 0, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"onclass": 3}, "phut_so_do": {"onclass": phut["Bài 4"]}},
        {"band": "VD", "loai": "VD lẻ", "dang": "Đẳng thức tích: ví dụ mẫu tài liệu Tiếp tuyến Dạng 3 Bài 10 ý a ($\\triangle COD$ vuông, $MC \\cdot MD = OM^2$); BTVN đề Giang Biên Đề 01 ý b ($OA$ là trung trực của $BC$, $OH \\cdot OA = R^2$)",
         "source_refs": ["tl-4-53.a", "ck1-giang-bien-2025-de01-4.2.b"], "vidu": 1, "onclass": 0, "btvn": 1, "lythuyet": 0, "decompose": "vd",
         "hinh_san": False, "gian_giao": "ve-hinh", "ve_tiep": {"vidu": 3}, "quy_trinh": quy},
    ]


def main():
    kiem_toan_do()
    les = gon_hinh(lesson())
    PHIEU.write_text(json.dumps(les, ensure_ascii=False, indent=2) + "\n", "utf-8")
    tm = json.loads(TM.read_text("utf-8"))
    p5 = next(p for p in tm["phieu"] if p["code"] == "5")
    p5["rows"] = dong_tm(PHUT)
    i = next(i for i, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 5"))
    j = next(j for j, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 6"))
    tm["thoiluong"][i + 1:j] = GIO_THUC_TM
    tm["dang_vd"] = [DANG_VD_5 if x.startswith("Buổi 5") else x for x in tm["dang_vd"]]
    tm["vidu"] = [VIDU_5 if x.startswith("Buổi 5") else x for x in tm["vidu"]]
    tm["loisai"] = [LOISAI_5 if x.startswith("Buổi 5") else x for x in tm["loisai"]]
    tm["kien_thuc_nen"] = [x for x in tm["kien_thuc_nen"] if not x.startswith(("\\textbf{Hai góc kề bù}", "\\textbf{Góc tạo bởi hai tia"))] + [NEN_KE_BU]
    TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2), "utf-8")
    print("ghi xong", PHIEU.name)


if __name__ == "__main__":
    main()
