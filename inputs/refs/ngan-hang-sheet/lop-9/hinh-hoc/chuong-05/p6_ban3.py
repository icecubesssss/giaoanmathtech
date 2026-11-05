#!/usr/bin/env python3
"""Phiếu 6 ch.V 9C — Bài tập cuối chương (45′) + kiểm tra chương (45′), dựng lại theo bản mẫu phiếu 2, 05/11/2026.

Đề soi từ ẢNH: SGK KNTT 9 tập 1 Bài 5.33, 5.32 (tr.112, PDF trang 113) · Chương Mỹ thi thử lần 4 2025-2026 IV.1 ý b ·
Thanh Quan GK1 2024-2025 Đề 1 Bài IV ý 1, 2 · Nguyễn Trường Tộ HK1 2025-2026 Bài IV ý 1, 2 (đích) ·
BTVN: STK Trương Ngọc Vỹ Câu 9 tr.232, Câu 25 tr.237 · Cụm 14 HK1 2025-2026 Bài 4.1 · Hoài Đức CK1 2024-2025 Bài 4.2 a, phần tích của b · Ban Mai HK1 2024-2025 Bài 3.

Không dùng trung tuyến chiều ngược. Đích bỏ ý 3 (cát tuyến qua tâm, 3% đề) và ý 4 (ý phân loại) theo luật chọn câu VD lớp C.

Chạy lại được:
    .venv/bin/python inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-05/p6_ban3.py
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
from p3_ban2 import R, h_nen_diem_ngoai, nen  # noqa: E402
from p3_ban3 import bai, giai_bon_diem, giai_trung_truc, gon_hinh, hai_tt  # noqa: E402
from p4_ban2 import BR, LG, d, goc, rong, so_do, xet  # noqa: E402
from p4_ban3 import h_nen_tron_tron  # noqa: E402
from p5_ban3 import h_quat_tron  # noqa: E402
from scripts.tikz_geo import Fig, foot, polar, tangent_points  # noqa: E402

D_ = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"
PHIEU = D_ / "phieu-6-bai-tap-cuoi-chuong-v.json"
TM = D_ / "thuyet-minh.json"

PHUT = {"BTVN 6": 0}
if PHIEU.exists():
    for _st in json.loads(PHIEU.read_text("utf-8"))["stages"]:
        for _b in _st["blocks"]:
            if _b.get("phut_so_do"):
                PHUT[_b["label"].rstrip(".")] = _b["phut_so_do"]


# ── Hình ───────────────────────────────────────────────────────────────────────
def h_543():
    """SGK Hình 5.43: BD đường kính, góc AOB = 40°, góc BOC = 100°."""
    o, b, dd, c, a = (0.0, 0.0), polar(280, R), polar(100, R), polar(20, R), polar(240, R)
    f = Fig()
    f.circle(o, R)
    f.pt("O", o); f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("D", dd)
    for u, v in [("B", "D"), ("O", "A"), ("O", "C")]:
        f.seg(u, v)
    f.angle("O", "A", "B", r=0.5, text="$40^\\circ$")
    f.angle("O", "B", "C", r=0.4, text="$100^\\circ$")
    return rong(f.tikz(), -4.0, -1.8, 4.0, 1.8)


def h_long_den():
    """Hai đường tròn đồng tâm, đường kính lỗ AB, đường kính viền CD (như hình trong đề gốc)."""
    r_ngoai, r_trong = 1.6, 1.2
    o = (0.0, 0.0)
    f = Fig()
    f.fill_raw(f"  \\fill[brand!18, even odd rule] (0,0) circle ({r_ngoai}) (0,0) circle ({r_trong});\n")
    f.circle(o, r_ngoai); f.circle(o, r_trong)
    f.pt("O", o)
    f.pt("A", polar(125, r_trong)); f.pt("B", polar(305, r_trong))
    f.pt("C", polar(155, r_ngoai)); f.pt("D", polar(335, r_ngoai))
    f.seg("A", "B"); f.seg("C", "D")
    return rong(f.tikz(), -4.0, -1.9, 4.0, 1.9)


def h_khan():
    """Nhìn từ trên xuống: mặt bàn đường kính 120 cm, khăn rủ thêm 40 cm quanh mép (đúng tỉ lệ 60 : 100)."""
    r_ban, r_khan = 1.5, 2.5
    o = (0.0, 0.0)
    f = Fig()
    f.fill_raw(f"  \\fill[brand!12, even odd rule] (0,0) circle ({r_khan}) (0,0) circle ({r_ban});\n")
    f.circle(o, r_khan); f.circle(o, r_ban)
    # fill_raw đẩy lệnh xuống dưới phần tô nên đoạn thẳng, chữ phải nối vào sau.
    f.cmds.append(f"  \\draw[ink] ({-r_ban},0) -- ({r_khan},0);")
    f.cmds.append("  \\node[inner sep=1pt] at (0,0.28) {$120$ cm};")
    f.cmds.append("  \\node[inner sep=1pt] at (3.2,0) {$40$ cm};")
    return rong(f.tikz(), -5.0, -2.6, 5.0, 2.6)


def h_c25():
    """STK C25: hai tiếp tuyến tại A, B cắt nhau tại I; đường qua I vuông góc IA cắt OB tại K."""
    o, a, b, i, k = c25()
    f = Fig()
    f.circle(o, R)
    f.pt("O", o); f.pt("A", a); f.pt("B", b); f.pt("I", i); f.pt("K", k)
    for u, v in [("O", "A"), ("O", "K"), ("O", "I"), ("A", "I"), ("I", "B"), ("I", "K")]:
        f.seg(u, v)
    f.right("A", o, i); f.right("B", o, i); f.right("I", a, k)
    return rong(f.tikz(), -3.6, -1.8, 4.6, 2.8)


def c25():
    o, b = (0.0, 0.0), (R, 0.0)
    a = polar(116, R)
    t = R * 1.6003345290410507  # tan 58°
    i = (R, t)
    k = ((R * R + t * t) / (2 * R), 0.0)
    return o, a, b, i, k


def hai_cao(a, b=(0.0, 0.0), c=(3.4, 0.0)):
    dd, e = foot(b, a, c), foot(c, a, b)
    return a, b, c, dd, e


def h_hai_cao(a, co_h=True):
    a, b, c, dd, e = hai_cao(a)
    f = Fig()
    f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("D", dd); f.pt("E", e)
    for u, v in [("A", "B"), ("B", "C"), ("A", "C"), ("B", "D"), ("C", "E")]:
        f.seg(u, v)
    f.right("D", a, b); f.right("E", a, c)
    if co_h:
        f.pt("H", foot(a, b, c) if False else _truc_tam(a, b, c))
    return f.tikz()


def _truc_tam(a, b, c):
    """Giao của hai đường cao từ B, C."""
    dd, e = foot(b, a, c), foot(c, a, b)
    x1, y1, x2, y2 = b[0], b[1], dd[0], dd[1]
    x3, y3, x4, y4 = c[0], c[1], e[0], e[1]
    m = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / m
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def h_nen_tam_giac(a, day_du):
    a, b, c, *_ = hai_cao(a)
    f = Fig()
    f.pt("A", a); f.pt("B", b); f.pt("C", c)
    f.seg("A", "B"); f.seg("B", "C"); f.seg("A", "C")
    return nen(f, day_du)


A_TQ = (2.2, 2.5)   # AB > AC
A_HD = (1.2, 2.5)   # AB < AC


def ban_mai():
    o, m = (0.0, 0.0), (3.5, 0.0)
    a, b = tangent_points(o, R, m)
    if a[1] < b[1]:
        a, b = b, a
    c, dd = foot(a, b, m), foot(b, a, m)
    # H: giao của AC và BD
    x1, y1, x2, y2 = a[0], a[1], c[0], c[1]
    x3, y3, x4, y4 = b[0], b[1], dd[0], dd[1]
    n = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / n
    h = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return o, m, a, b, c, dd, h, foot(a, o, m)


def h_ban_mai():
    o, m, a, b, c, dd, h, i = ban_mai()
    f = Fig()
    f.circle(o, R)
    f.pt("O", o); f.pt("M", m); f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("D", dd); f.pt("H", h); f.pt("I", i)
    for u, v in [("M", "A"), ("M", "B"), ("O", "A"), ("O", "B"), ("O", "M"), ("A", "B"), ("A", "C"), ("B", "D")]:
        f.seg(u, v)
    f.right("A", o, m); f.right("B", o, m); f.right(i, a, m); f.right("C", a, m); f.right("D", b, m)
    return f.tikz()


def kiem_toan_do():
    """Kết luận của đề phải đúng trên chính hình vẽ."""
    # Đích: hai tiếp tuyến, OH·OA = R²
    o, a = (0.0, 0.0), (3.5, 0.0)
    b, c = tangent_points(o, R, a)
    h = foot(b, o, a)
    assert abs(d(o, h) * d(o, a) - R * R) < 1e-9
    assert abs(b[0] * 0 + (b[1] - c[1]) * a[0] * 0 + (b[0] - c[0])) < 1e-9       # BC ⊥ OA (BC đứng, OA ngang)
    # Hai đường cao: AB·AE = AC·AD
    for pt in (A_TQ, A_HD):
        aa, bb, cc, dd, e = hai_cao(pt)
        assert abs(d(aa, bb) * d(aa, e) - d(aa, cc) * d(aa, dd)) < 1e-9
    assert d(A_TQ, (0, 0)) > d(A_TQ, (3.4, 0))                                    # Thanh Quan: AB > AC
    assert d(A_HD, (0, 0)) < d(A_HD, (3.4, 0))                                    # Hoài Đức: AB < AC
    # C25: IK ⊥ IA, KI = KO
    oo, a25, b25, i25, k25 = c25()
    assert abs(d(i25, a25) - d(i25, b25)) < 1e-6                                  # I đúng giao hai tiếp tuyến
    assert abs((k25[0] - i25[0]) * (a25[0] - i25[0]) + (k25[1] - i25[1]) * (a25[1] - i25[1])) < 1e-6  # IK ⊥ IA
    assert abs(d(k25, i25) - d(k25, oo)) < 1e-9
    # Ban Mai: OAHB hình thoi, OI·OM = R²
    om, mm, am, bm, cm, dm, hm, im = ban_mai()
    assert abs(d(om, im) * d(om, mm) - R * R) < 1e-9
    assert abs(d(am, hm) - R) < 1e-9 and abs(d(bm, hm) - R) < 1e-9
    # Số: π ≈ 3,14
    assert round(0.63 * 3.14159, 2) == 1.98
    assert 3.14 * 100 ** 2 == 31400.0
    assert 180 - 100 == 80 and 180 - 40 == 140


# ── Sơ đồ ──────────────────────────────────────────────────────────────────────
def sd_hai_tt(dich_tich, tich, cap, g1, g2, chung, trung_truc, gt, ben):
    return so_do(dich_tich, [tich, cap], [f"{g1}\\\\{g2}", trung_truc, gt], [chung], rong=3.0, buoc=1.05, ben=ben, ben_x=4.1)


def sd_cao(dich, ti_so, cap, goc_vuong, chung):
    return so_do(dich, [ti_so, cap], [goc_vuong], [chung], rong=2.9)


GHI_CHU_LT1 = (
    "Khoảng 16 phút với lớp C theo định mức: Bài 1 long đen (hình in sẵn; đề gốc có thêm ý a tính diện tích lỗ, bỏ để đủ giờ) ~5′, "
    "Ví dụ 1 ~11′ (gồm 2′ vẽ). Không có bài theo sơ đồ sau ví dụ vì buổi chỉ 45′; đề đích ở Luyện tập 2 đi cùng cách (hai tam giác vuông có chung góc nhọn) trên hình hai tiếp tuyến."
)
GHI_CHU_LT2 = (
    "Khoảng 21 phút với lớp C theo định mức: HS tự vẽ hình (~5′), tự trình bày (~16′). Còn ~3′ chữa nhanh rồi chuyển sang kiểm tra chương 45 phút. "
    "Đề gốc Bài IV còn: ý 1 bốn điểm (bỏ để đủ giờ, đã luyện ở Ví dụ 1 và BTVN 7), ý 3 $AM \\cdot AN = AH \\cdot AO$ (cát tuyến qua tâm, 2/66 đề Kì I), ý 4 trung điểm (ý phân loại)."
)
GHI_CHU_BTVN = (
    "Sơ đồ là tổng kết chương, HS chép vào sổ tay. BTVN khoảng 80 phút với lớp C, dày hơn quỹ 40 phút để HS có thêm bài: BTVN 1 đến BTVN 4 trắc nghiệm (~10′), BTVN 5 khăn trải bàn (~5′), "
    "BTVN 6 tự vẽ hình, đọc sơ đồ ngược rồi trình bày vào vở (~20′), BTVN 7 tự vẽ hình, tự trình bày trọn ba ý đề Ban Mai (~45′)."
)
QUY_TRINH_DICH = [
    "$AB = AC$, $OB = OC$ $\\Rightarrow OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$",
    "$\\triangle OHB \\backsim \\triangle OBA$ (g.g) $\\Rightarrow OH \\cdot OA = OB^2 = R^2$",
]
QUY_TRINH_BM = [
    "Ý a: hai tam giác vuông chung cạnh huyền $OM$",
    "Ý b: $OM$ là đường trung trực của $AB$; $\\triangle OIA \\backsim \\triangle OAM$ (g.g) $\\Rightarrow OI \\cdot OM = OA^2 = R^2$",
    "Ý c: hai đường cùng vuông góc với một đường thì song song $\\Rightarrow$ hình bình hành; hai cạnh kề bằng nhau $\\Rightarrow$ hình thoi",
]


def lesson() -> dict:
    # ── Chặng 1 ────────────────────────────────────────────────────────────────
    kham_pha = {
        "kind": "review", "number": 1, "title": "Khám phá",
        "teacher_note": "Chỉ 2 phút, GV hỏi miệng: mỗi ý đã học ở phiếu nào, chứng minh bằng cách nào. Nửa sau buổi là bài kiểm tra chương 45 phút.",
        "blocks": [
            {"type": "para", "text": "\\textbf{Câu IV của đề thi hỏi những gì?}"},
            {"type": "noted", "variant": "note",
             "text": "Câu IV của đề thi thường gồm một bài đo lường và một bài chứng minh trên đường tròn. Các ý sau đã học ở phiếu nào? Chứng minh hoặc tính bằng cách nào?[[br]]"
                     "\\textbf{a)} Tính độ dài cung, diện tích hình quạt tròn, hình vành khuyên.[[br]]"
                     "\\textbf{b)} Chứng minh bốn điểm cùng thuộc một đường tròn.[[br]]"
                     "\\textbf{c)} Chứng minh $OA \\perp BC$ từ hai tiếp tuyến $AB$, $AC$.[[br]]"
                     "\\textbf{d)} Chứng minh một đẳng thức tích, ví dụ $OH \\cdot OA = R^2$."},
        ],
    }

    # ── Chặng 2: thẻ ───────────────────────────────────────────────────────────
    the_a1 = {
        "type": "noted", "variant": "theory", "title": "1. CUNG TRÒN, HÌNH QUẠT TRÒN, HÌNH VÀNH KHUYÊN (BÀI 15)",
        "text": "\\nhanly{Số đo cung:} Cung nhỏ bằng số đo góc ở tâm chắn cung; nửa đường tròn bằng $180^\\circ$.[[br]]"
                "\\nhanly{Độ dài cung $n^\\circ$:} $l = \\dfrac{n}{360} \\cdot 2\\pi R$.[[br]]"
                "\\nhanly{Diện tích hình quạt tròn:} $S_q = \\dfrac{n}{360} \\cdot \\pi R^2$.[[br]]"
                "\\nhanly{Hình vành khuyên:} $S = \\pi R^2 - \\pi r^2$.",
        "figure": {"tikz": h_quat_tron(120, "$R$", rong_khung=False), "caption": "Hình quạt tròn $OAB$", "pos": "right"},
    }
    the_a2 = {
        "type": "noted", "variant": "theory", "title": "2. TIẾP TUYẾN VÀ BỐN ĐIỂM CÙNG THUỘC MỘT ĐƯỜNG TRÒN",
        "text": "\\nhanly{Bốn điểm:} $\\triangle ABO$ vuông tại $B$ $\\Rightarrow A$, $B$, $O$ cùng thuộc đường tròn đường kính $AO$.[[br]]"
                "\\nhanly{Tiếp tuyến (Bài 16):} Tiếp tuyến vuông góc với bán kính đi qua tiếp điểm.[[br]]"
                "\\nhanly{Hai tiếp tuyến cắt nhau (Bài 16):} $AB$, $AC$ là hai tiếp tuyến cắt nhau tại $A$ thì $AB = AC$.[[br]]"
                "\\nhanly{Đường trung trực (SGK Toán 7 tập 1, Bài 16, tr.83):} Điểm cách đều hai mút của một đoạn thẳng thì thuộc đường trung trực của đoạn thẳng đó.[[br]]"
                "\\nhanly{Đồng dạng (SGK Toán 8 tập 2, Bài 36, tr.98):} Nếu một góc nhọn của tam giác vuông này bằng một góc nhọn của tam giác vuông kia thì hai tam giác vuông đó đồng dạng với nhau.",
        "figure": {"tikz": hai_tt("A", "B", "C", "H", r=1.2, xa=2.9), "caption": "Hai tiếp tuyến $AB$, $AC$", "pos": "right"},
    }
    the_dang_1 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 1. TAM GIÁC CÓ HAI ĐƯỜNG CAO",
        "text": "\\nhanly{Phương pháp.} dùng hai góc vuông ở chân đường cao.[[br]]"
                "\\nhanly{Bước 1:} Hai tam giác vuông chung cạnh huyền $BC$ $\\Rightarrow$ bốn điểm $B$, $E$, $D$, $C$ cùng thuộc đường tròn đường kính $BC$.[[br]]"
                "\\nhanly{Bước 2:} $\\triangle ABD \\backsim \\triangle ACE$ (g.g) $\\Rightarrow AB \\cdot AE = AC \\cdot AD$.",
        "so_do_nguoc": sd_cao("$AB \\cdot AE = AC \\cdot AD$", "$\\dfrac{AB}{AC} = \\dfrac{AD}{AE}$", "$\\triangle ABD \\backsim \\triangle ACE$ (g.g)",
                              f"${goc('ADB')} = {goc('AEC')} = 90^\\circ$\\\\($BD$, $CE$ là đường cao)", f"${goc('BAC')}$ chung"),
    }
    the_dang_2 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 2. HAI TIẾP TUYẾN: VUÔNG GÓC RỒI ĐẲNG THỨC TÍCH",
        "text": "\\nhanly{Phương pháp.} đường trung trực cho góc vuông, rồi đưa về hai tam giác đồng dạng.[[br]]"
                "\\nhanly{Bước 1:} $AB = AC$, $OB = OC$ $\\Rightarrow OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$ tại $H$.[[br]]"
                "\\nhanly{Bước 2:} $\\triangle OHB \\backsim \\triangle OBA$ (g.g) $\\Rightarrow OH \\cdot OA = OB^2 = R^2$.",
        "so_do_nguoc": sd_hai_tt("$OH \\cdot OA = R^2$", "$OH \\cdot OA = OB^2$", "$\\triangle OHB \\backsim \\triangle OBA$ (g.g)",
                                 f"${goc('OHB')} = {goc('OBA')} = 90^\\circ$", "($AB$ là tiếp tuyến tại $B$)", f"${goc('AOB')}$ chung",
                                 "$OA$ là đường trung trực của $BC$", "$AB = AC$; $OB = OC$", "$R = OB$ (bán kính)"),
    }

    # ── Mạch 1 ─────────────────────────────────────────────────────────────────
    bai_1 = bai(
        "Bài 1.", 2, "onclass", "TH1",
        "[TH] Long đen, hay còn gọi là vòng đệm, là một chi tiết cơ khí có dạng $2$ hình tròn đồng tâm, có lỗ ở giữa (Hình 1). "
        "Phần lỗ ở giữa là hình tròn có đường kính $AB = 1{,}8$ cm. Viền ngoài của long đen là hình tròn có đường kính $CD = 2{,}4$ cm. "
        "Tính diện tích một bề mặt long đen (làm tròn kết quả với độ chính xác $0{,}005$).",
        f"Bán kính lỗ tròn: $r = 1{{,}}8 : 2 = 0{{,}}9$ (cm).{BR}"
        f"Bán kính viền ngoài: $R = 2{{,}}4 : 2 = 1{{,}}2$ (cm).{BR}"
        f"$S = \\pi R^2 - \\pi r^2 = \\pi(1{{,}}2^2 - 0{{,}}9^2) = 0{{,}}63\\pi \\approx 1{{,}}98$ ($\\text{{cm}}^2$).{BR}"
        f"Vậy diện tích một bề mặt long đen khoảng $1{{,}}98$ $\\text{{cm}}^2$.",
        figure_given=True,
        figure={"tikz": h_long_den(), "caption": "Hình 1", "pos": "right"},
        hints=["Đề cho đường kính hay bán kính? Bề mặt long đen là hình gì?"],
    )

    # ── Mạch 2: Ví dụ hai đường cao ────────────────────────────────────────────
    tq = h_hai_cao(A_TQ)
    vi_du_1 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 1.} Cho $\\triangle ABC$ có ba góc nhọn, $AB > AC$, hai đường cao $BD$ và $CE$ cắt nhau tại $H$ (Hình 2). Vẽ tiếp vào Hình 2 các yếu tố còn thiếu theo đề.[[br]]"
                "1) Chứng minh rằng bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn. Hãy chỉ rõ tâm $O$ của đường tròn này.[[br]]"
                "2) Chứng minh $AB \\cdot AE = AC \\cdot AD$."
                f"{BR}{LG}{BR}"
                f"1) $CE$ là đường cao của $\\triangle ABC$ $\\Rightarrow \\triangle BEC$ vuông tại $[[fill:E]]${BR}"
                f"$\\Rightarrow B, E, C$ cùng thuộc đường tròn đường kính $[[fill:BC]]$.{BR}"
                f"$BD$ là đường cao của $\\triangle ABC$ $\\Rightarrow \\triangle BDC$ vuông tại $[[fill:D]]${BR}"
                f"$\\Rightarrow B, D, C$ cùng thuộc đường tròn đường kính $BC$.{BR}"
                f"Vậy bốn điểm $B, E, D, C$ cùng thuộc đường tròn đường kính $BC$, tâm $O$ là [[fill:trung điểm]] của $BC$.{BR}"
                f"2) Xét $\\triangle ABD$ và $\\triangle ACE$ có:{BR}"
                f"${goc('ADB')} = {goc('AEC')} = [[fill:90^\\circ]]$ ($BD$, $CE$ là đường cao của $\\triangle ABC$){BR}"
                f"${goc('BAC')}$ [[fill:chung]]{BR}"
                f"$\\Rightarrow \\triangle ABD \\backsim \\triangle [[fill:ACE]]$ (g.g){BR}"
                f"$\\Rightarrow \\dfrac{{AB}}{{AC}} = [[fill:\\dfrac{{AD}}{{AE}}|1.3cm]]${BR}"
                "Vậy $AB \\cdot AE = [[fill:AC \\cdot AD|1.8cm]]$.",
        "figure": {"tikz": h_nen_tam_giac(A_TQ, tq), "tikz_gv": tq, "caption": "Hình 2", "pos": "right"},
        "so_do_nguoc": sd_cao("$AB \\cdot AE = AC \\cdot AD$", "$\\dfrac{AB}{AC} = [[fill:\\dfrac{AD}{AE}|1.3cm]]$", "$\\triangle ABD \\backsim \\triangle [[fill:ACE]]$ (g.g)",
                              f"${goc('ADB')} = {goc('AEC')} = [[fill:90^\\circ]]$\\\\($BD$, $CE$ là đường cao)", f"${goc('BAC')}$ [[fill:chung]]"),
    }

    # ── LT2: đích Nguyễn Trường Tộ ─────────────────────────────────────────────
    ntt = hai_tt("A", "B", "C", "H")
    bai_2 = bai(
        "Bài 2.", 3, "onclass", "VD1",
        "[VD] Từ điểm $A$ ở ngoài đường tròn $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ (với $B$ và $C$ là hai tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$. "
        "Chứng minh $OA \\perp BC$ và $OA \\cdot OH = R^2$.",
        giai_trung_truc("A", "B", "C", ket=f"{BR}$\\Rightarrow OA \\perp BC$ tại $H$.{BR}", duong="OA")
        + xet("OHB", "OBA", f"{goc('OHB')} = {goc('OBA')}", "$OA \\perp BC$ tại $H$, $AB$ là tiếp tuyến của $(O)$ tại $B$", goc("AOB"),
              "\\dfrac{OH}{OB} = \\dfrac{OB}{OA}", "OH \\cdot OA = OB^2") + f".{BR}"
        + "Vậy $OA \\perp BC$ và $OA \\cdot OH = R^2$ (vì $OB = R$).",
        figure_given=False, draw=True, quy_trinh=QUY_TRINH_DICH,
        figure={"tikz": h_nen_tron_tron(ntt), "tikz_gv": ntt, "caption": "Hình 3", "pos": "right"},
        hints=["Hai điểm nào cùng cách đều $B$ và $C$? Đẳng thức $OH \\cdot OA = OB^2$ có được từ tỉ lệ thức nào?"],
    )

    # ── BTVN ───────────────────────────────────────────────────────────────────
    btvn_1 = bai(
        "BTVN 1.", 1, "btvn", "NB1",
        "[NB] Cho đường tròn $(O; 4$ cm$)$ và hai điểm $A$, $B$. Biết rằng $OA = \\sqrt{15}$ cm và $OB = 4$ cm. Khi đó:",
        "D",
        options=["Điểm $A$ nằm trong $(O)$, điểm $B$ nằm ngoài $(O)$.", "Điểm $A$ nằm ngoài $(O)$, điểm $B$ nằm trên $(O)$.",
                 "Điểm $A$ nằm trên $(O)$, điểm $B$ nằm trong $(O)$.", "Điểm $A$ nằm trong $(O)$, điểm $B$ nằm trên $(O)$."],
        figure_given=True,
    )
    btvn_2 = bai(
        "BTVN 2.", 1, "btvn", "NB1",
        "[NB] Cho đường tròn $(O; 5$ cm$)$ và đường thẳng $a$. Biết khoảng cách từ tâm $O$ đến đường thẳng $a$ bằng $4$ cm. Nhận xét nào sau đây đúng?",
        "C",
        options=["Đường thẳng $a$ không cắt đường tròn $(O)$.", "Đường thẳng $a$ tiếp xúc đường tròn $(O)$.",
                 "Đường thẳng $a$ cắt đường tròn $(O)$.", "Đáp án A, B, C đều sai."],
        figure_given=True,
    )
    btvn_3 = bai(
        "BTVN 3.", 1, "btvn", "NB1",
        f"[NB] Cho Hình 4, trong đó $BD$ là đường kính, ${goc('AOB')} = 40^\\circ$, ${goc('BOC')} = 100^\\circ$. Khi đó:",
        "D",
        options=["sđ$\\overset{\\frown}{DC} = 80^\\circ$ và sđ$\\overset{\\frown}{AD} = 220^\\circ$.",
                 "sđ$\\overset{\\frown}{DC} = 280^\\circ$ và sđ$\\overset{\\frown}{AD} = 220^\\circ$.",
                 "sđ$\\overset{\\frown}{DC} = 280^\\circ$ và sđ$\\overset{\\frown}{AD} = 140^\\circ$.",
                 "sđ$\\overset{\\frown}{DC} = 80^\\circ$ và sđ$\\overset{\\frown}{AD} = 140^\\circ$."],
        figure_given=True,
        figure={"tikz": h_543(), "caption": "Hình 4", "pos": "right"},
    )
    btvn_4 = bai(
        "BTVN 4.", 1, "btvn", "NB2",
        "[NB] Hai tiếp tuyến tại $A$ và $B$ của đường tròn $(O)$ cắt nhau tại $I$. Đường thẳng qua $I$ và vuông góc với $IA$ cắt $OB$ tại $K$ (Hình 5). Chọn khẳng định đúng.",
        "B",
        options=["$OI = OK = KI$.", "$KI = KO$.", "$OI = OK$.", "$OI = IK$."],
        figure_given=True,
        figure={"tikz": h_c25(), "caption": "Hình 5", "pos": "right"},
    )
    btvn_5 = bai(
        "BTVN 5.", 2, "btvn", "TH1",
        "[TH] Người ta muốn may một chiếc khăn trải bàn hình tròn để phủ một chiếc bàn hình tròn sao cho khăn rủ xuống ở mép bàn là $40$ cm, biết mặt bàn có đường kính $120$ cm (Hình 6). "
        "Tính diện tích vải cần may khăn (lấy $\\pi \\approx 3{,}14$).",
        f"Bán kính mặt bàn: $120 : 2 = 60$ (cm).{BR}"
        f"Bán kính khăn: $R = 60 + 40 = 100$ (cm).{BR}"
        f"$S = \\pi R^2 \\approx 3{{,}}14 \\cdot 100^2 = 31400$ ($\\text{{cm}}^2$).{BR}"
        f"Vậy diện tích vải cần may khăn khoảng $31400$ $\\text{{cm}}^2$.",
        figure_given=True,
        figure={"tikz": h_khan(), "caption": "Hình 6 (nhìn từ trên xuống)", "pos": "right"},
        hints=["Bán kính khăn gồm những đoạn nào?"],
    )
    hd = h_hai_cao(A_HD)
    btvn_6 = bai(
        "BTVN 6.", 2, "btvn", "TH2",
        "Cho tam giác $ABC$ nhọn ($AB < AC$) có hai đường cao $BD$ và $CE$ cắt nhau tại $H$ (Hình 7).[[br]]"
        "a) [TH] Chứng minh bốn điểm $B$, $E$, $D$, $C$ cùng nằm trên một đường tròn. Xác định tâm $I$ của đường tròn này.[[br]]"
        "b) [TH] Chứng minh $AE \\cdot AB = AD \\cdot AC$.[[br]]"
        "Vẽ tiếp vào Hình 7 các yếu tố còn thiếu, rồi dựa vào sơ đồ ngược để trình bày ý b vào vở.",
        f"a) $CE$ là đường cao của $\\triangle ABC$ $\\Rightarrow \\triangle BEC$ vuông tại $E${BR}"
        f"$\\Rightarrow B, E, C$ cùng thuộc đường tròn đường kính $BC$.{BR}"
        f"$BD$ là đường cao của $\\triangle ABC$ $\\Rightarrow \\triangle BDC$ vuông tại $D${BR}"
        f"$\\Rightarrow B, D, C$ cùng thuộc đường tròn đường kính $BC$.{BR}"
        f"Vậy bốn điểm $B, E, D, C$ cùng thuộc đường tròn đường kính $BC$, tâm $I$ là trung điểm của $BC$.{BR}"
        f"b) Xét $\\triangle ABD$ và $\\triangle ACE$ có:{BR}"
        f"${goc('ADB')} = {goc('AEC')} = 90^\\circ$ ($BD$, $CE$ là đường cao của $\\triangle ABC$){BR}"
        f"${goc('BAC')}$ chung{BR}"
        f"$\\Rightarrow \\triangle ABD \\backsim \\triangle ACE$ (g.g){BR}"
        f"$\\Rightarrow \\dfrac{{AB}}{{AC}} = \\dfrac{{AD}}{{AE}}${BR}"
        "Vậy $AE \\cdot AB = AD \\cdot AC$.",
        draw=True, phut_so_do=PHUT["BTVN 6"],
        figure={"tikz": h_nen_tam_giac(A_HD, hd), "tikz_gv": hd, "caption": "Hình 7", "pos": "right"},
        so_do_nguoc=sd_cao("$AE \\cdot AB = AD \\cdot AC$", "$\\dfrac{AB}{AC} = \\dfrac{AD}{AE}$", "$\\triangle ABD \\backsim \\triangle ACE$ (g.g)",
                           f"${goc('ADB')} = {goc('AEC')} = 90^\\circ$\\\\($BD$, $CE$ là đường cao)", f"${goc('BAC')}$ chung"),
    )
    bm = h_ban_mai()
    btvn_7 = bai(
        "BTVN 7.", 3, "btvn", "TH3+VD1",
        "Cho $(O; R)$. Từ một điểm $M$ nằm ngoài $(O)$ kẻ hai tiếp tuyến $MA$, $MB$ ($A$, $B$ là các tiếp điểm).[[br]]"
        "a) [TH] Chứng minh bốn điểm $A$, $M$, $B$, $O$ cùng thuộc một đường tròn.[[br]]"
        "b) [VD] Gọi $I$ là giao điểm của $AB$ và $OM$. Chứng minh $OI \\cdot OM = R^2$.[[br]]"
        "c) [VD] Kẻ $AC \\perp BM$ ($C \\in BM$); $BD \\perp AM$ ($D \\in AM$). Gọi $H$ là giao điểm của $BD$ và $AC$. Chứng minh $OAHB$ là hình thoi.",
        "a) " + giai_bon_diem("M", "A", "B")
        + f"Vậy bốn điểm $A, M, B, O$ cùng thuộc đường tròn đường kính $MO$.{BR}"
        + "b) " + giai_trung_truc("M", "A", "B", ket=f"{BR}$\\Rightarrow OM \\perp AB$ tại $I$.{BR}", duong="OM")
        + xet("OIA", "OAM", f"{goc('OIA')} = {goc('OAM')}", "$OM \\perp AB$ tại $I$, $MA$ là tiếp tuyến của $(O)$ tại $A$", goc("AOM"),
              "\\dfrac{OI}{OA} = \\dfrac{OA}{OM}", "OI \\cdot OM = OA^2") + f".{BR}"
        + f"Vậy $OI \\cdot OM = R^2$ (vì $OA = R$).{BR}"
        + f"c) $AC \\perp BM$, $OB \\perp BM$ ($MB$ là tiếp tuyến của $(O)$ tại $B$) $\\Rightarrow AC \\parallel OB$ hay $AH \\parallel OB$.{BR}"
        + f"$BD \\perp AM$, $OA \\perp AM$ ($MA$ là tiếp tuyến của $(O)$ tại $A$) $\\Rightarrow BD \\parallel OA$ hay $BH \\parallel OA$.{BR}"
        + f"$\\Rightarrow OAHB$ là hình bình hành.{BR}"
        + f"Mà $OA = OB$ (bán kính của $(O)$).{BR}"
        + "Vậy $OAHB$ là hình thoi.",
        figure_given=False, draw=True, quy_trinh=QUY_TRINH_BM,
        figure={"tikz": h_nen_tron_tron(bm), "tikz_gv": bm, "caption": "Hình 8", "pos": "right"},
    )

    return {
        "slug": PHIEU.stem,
        "title": "Bài tập cuối chương V",
        "eyebrow": "PHIẾU 6 • HÌNH HỌC 9 · CHƯƠNG V — BÀI TẬP CUỐI CHƯƠNG",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "kiem_tra_phut": 45,
        "btvn_phieu_rieng": True,
        "stages": [
            kham_pha,
            {"kind": "concept", "number": 2, "title": "Kiến thức trọng tâm",
             "teacher_note": "Chặng này ~3′, chỉ nhắc, không giảng lại: thẻ 1 cho Câu IV.1, thẻ 2 cho Câu IV.2. Hai dạng B đọc lướt theo sơ đồ: Dạng 1 giảng ở Ví dụ 1, Dạng 2 là đường đi của đề đích.",
             "blocks": [
                 {"type": "para", "variant": "part", "text": "A. Lý thuyết"},
                 the_a1, the_a2,
                 {"type": "para", "variant": "part", "text": "B. Phương pháp chứng minh — các dạng quen thuộc"},
                 the_dang_1, the_dang_2,
             ]},
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "teacher_note": GHI_CHU_LT1,
             "blocks": [
                 {"type": "para", "text": "\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề Nguyễn Trường Tộ) ở Bài 2: chứng minh vuông góc (đã học ở Phiếu 3) "
                                          "và đẳng thức tích (đã học ở Phiếu 4). Bốn điểm cùng thuộc một đường tròn (Phiếu 2) luyện ở Ví dụ 1."},
                 {"type": "para", "variant": "heading", "text": "Mạch 1. Câu IV.1 — Hình vành khuyên trong bài thực tế"},
                 bai_1,
                 {"type": "para", "variant": "heading", "text": "Mạch 2. Câu IV.2 — Tam giác có hai đường cao: bốn điểm, đẳng thức tích"},
                 vi_du_1,
             ]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "teacher_note": GHI_CHU_LT2,
             "blocks": [
                 {"type": "para", "variant": "heading", "text": "Đề thi Học kì I — THCS Nguyễn Trường Tộ"},
                 bai_2,
             ]},
            {"kind": "reflection", "number": 5, "title": "Sơ đồ tư duy",
             "teacher_note": GHI_CHU_BTVN,
             "blocks": [
                 {"type": "mindmap", "caption": "Sơ đồ tư duy: Câu IV của đề thi",
                  "root": "CÂU IV",
                  "branches": [
                      {"label": "ĐO LƯỜNG", "children": [{"label": "Cung, quạt: $R$, $n$ rồi thay công thức"},
                                                          {"label": "Vành khuyên: $\\pi R^2 - \\pi r^2$"}]},
                      {"label": "BỐN ĐIỂM", "children": [{"label": "Hai tam giác vuông"},
                                                          {"label": "Chung cạnh huyền"}]},
                      {"label": "VUÔNG GÓC", "children": [{"label": "Hai điểm cách đều hai đầu đoạn"},
                                                           {"label": "Đường trung trực"}]},
                      {"label": "TÍCH", "children": [{"label": "Hai tam giác đồng dạng (g.g)"},
                                                      {"label": "Tỉ lệ thức, nhân chéo"}]},
                  ]},
                 btvn_1, btvn_2, btvn_3, btvn_4, btvn_5, btvn_6, btvn_7,
             ]},
        ],
    }


# ── Thuyết minh ────────────────────────────────────────────────────────────────
GIO_THUC_TM = [
    "\\quad Giờ thực lớp C (05/11/2026): Khám phá $+$ Kiến thức 5′ · Luyện tập 1 khoảng 16′ (1 bài Câu IV.1, 1 ví dụ HS vẽ cùng GV và điền sơ đồ ngược)",
    "\\quad Luyện tập 2 khoảng 21′ (đề đích Nguyễn Trường Tộ, ý 2, HS tự vẽ) · chữa bài, chốt khoảng 3′ · BTVN khoảng 80′ (quỹ 40′, cố ý dày hơn)",
]
VIDU_6 = "Buổi 6: Đề mẫu (Thanh Quan): tam giác có hai đường cao — bốn điểm $B$, $E$, $D$, $C$ và $AB \\cdot AE = AC \\cdot AD$."
DANG_VD_6 = ("Buổi 6 — Câu IV.2 ý 2 (đề Nguyễn Trường Tộ): $OA \\perp BC$ và $OA \\cdot OH = R^2$. "
             "Đề gốc còn ý 1 (bỏ để đủ giờ 45′, bốn điểm luyện ở ví dụ và BTVN), ý 3 $AM \\cdot AN = AH \\cdot AO$, ý 4: bỏ (cát tuyến qua tâm 2/66 đề Kì I; ý 4 phân loại). BTVN: đề Ban Mai (bốn điểm, $OI \\cdot OM = R^2$, $OAHB$ là hình thoi).")
LOISAI_6 = ("Buổi 6: vẽ hình sai vị trí các điểm; kết luận thiếu \\textquotedblleft Vậy\\textquotedblright{} ở cuối mỗi ý; dùng thẳng $OH \\cdot OA = R^2$ mà không chứng minh tam giác đồng dạng; "
            "đề cho đường kính mà thay thẳng vào chỗ bán kính; viết sai thứ tự đỉnh $\\triangle ABD \\backsim \\triangle ACE$.")


def dong_tm(phut) -> list[dict]:
    return [
        {"band": "NB", "loai": "NB lẻ LT", "dang": "Trắc nghiệm ôn chương (BTVN): vị trí điểm, vị trí đường thẳng đối với đường tròn (SGK 5.32, STK Câu 9); số đo cung (SGK 5.33)",
         "source_refs": ["sgk-5.32", "stk-b16-I-C9-tr232", "sgk-5.33"], "vidu": 0, "onclass": 0, "btvn": 3, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB kiến thức cũ", "dang": "Hai góc so le trong và tam giác cân (Lớp 7) trên hình hai tiếp tuyến: đường thẳng qua $I$ vuông góc $IA$ $\\Rightarrow KI = KO$ (trắc nghiệm, BTVN)",
         "source_refs": ["stk-b16-I-C25-tr237"], "vidu": 0, "onclass": 0, "btvn": 1, "lythuyet": 0, "decompose": "none", "hinh_san": True},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Bài thực tế Câu IV.1 có hình: diện tích hình vành khuyên (trên lớp, long đen ý b); diện tích hình tròn (BTVN, khăn trải bàn)",
         "source_refs": ["v10-chuong-my-l4-2025-IV1.b", "ck1-cum-14-2025-4.1"], "vidu": 0, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb", "hinh_san": True},
        {"band": "TH", "loai": "TH tách VD", "dang": "Tam giác có hai đường cao: bốn điểm và đẳng thức tích. Ví dụ mẫu đề Thanh Quan ý 1, 2 (HS vẽ tiếp, điền sơ đồ ngược); BTVN đề Hoài Đức ý a, phần tích của ý b (tự vẽ, đọc sơ đồ ngược)",
         "source_refs": ["gk1-thanh-quan-2024-IV.a", "gk1-thanh-quan-2024-IV.b", "ck1-hoai-duc-2024-4.2.a", "ck1-hoai-duc-2024-4.2.b"], "vidu": 1, "onclass": 0, "btvn": 2, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"vidu": 2}, "ve_hinh": {"btvn": 1}, "phut_so_do": {"btvn": phut["BTVN 6"]}},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Hai tiếp tuyến: bốn điểm (BTVN, đề Ban Mai ý a)",
         "source_refs": ["ck1-ban-mai-2024-3.a"], "vidu": 0, "onclass": 0, "btvn": 1, "lythuyet": 0, "decompose": "th2nb", "hinh_san": False},
        {"band": "VD", "loai": "VD lẻ", "dang": "Hai tiếp tuyến: $OA \\perp BC$ và $OA \\cdot OH = R^2$ (đề đích Nguyễn Trường Tộ, HS tự vẽ, tự trình bày). BTVN đề Ban Mai: $OI \\cdot OM = R^2$, $OAHB$ là hình thoi",
         "source_refs": ["ck1-nguyen-truong-to-2025-IV.b", "ck1-ban-mai-2024-3.b", "ck1-ban-mai-2024-3.c"], "vidu": 0, "onclass": 1, "btvn": 2, "lythuyet": 0, "decompose": "vd",
         "hinh_san": False, "ve_hinh": {"onclass": 1, "btvn": 1}, "quy_trinh": QUY_TRINH_DICH},
    ]


def main():
    kiem_toan_do()
    les = gon_hinh(lesson())
    PHIEU.write_text(json.dumps(les, ensure_ascii=False, indent=2) + "\n", "utf-8")
    tm = json.loads(TM.read_text("utf-8"))
    p6 = next(p for p in tm["phieu"] if p["code"] == "6")
    p6["rows"] = dong_tm(PHUT)
    i = next(i for i, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 6"))
    j = next(j for j, x in enumerate(tm["thoiluong"]) if x.startswith("\\textbf{Tổng"))
    tm["thoiluong"][i + 1:j] = GIO_THUC_TM
    tm["dang_vd"] = [DANG_VD_6 if x.startswith("Buổi 6") else x for x in tm["dang_vd"]]
    tm["vidu"] = [VIDU_6 if x.startswith("Buổi 6") else x for x in tm["vidu"]]
    tm["loisai"] = [LOISAI_6 if x.startswith("Buổi 6") else x for x in tm["loisai"]]
    TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2), "utf-8")
    print("ghi xong", PHIEU.name)


if __name__ == "__main__":
    main()
