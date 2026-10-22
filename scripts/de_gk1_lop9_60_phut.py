#!/usr/bin/env python3
"""ĐỀ KIỂM TRA GIỮA HỌC KÌ I LỚP 9 — BẢN 60 PHÚT, KHÔNG CÓ VDC (20/10/2026).

Sếp KhanhNT góp ý đề chính thức GK1 (bản 90 phút ở scripts/de_on_tap_gk1_lop9*.py): "Bỏ câu VDC, điều chỉnh lại
thời gian thành 60p, điều chỉnh cả ma trận đề để phù hợp lại điểm nhé, chắc tăng điểm các câu tự luận, vd lên chút".
Thầy: "Xem đề lớp 9C và làm 1 phiên bản mới hẳn" ⇒ đề MỚI HẲN: mọi câu lấy từ 5 trường CHƯA dùng ở 8 đề cũ (bản 1 + bản 2),
rải 5 quận (không quận nào quá 30%). Hai bản cũ giữ nguyên.

Khung mới (10 điểm, 4 bài, ~58 phút làm bài):
  I 2,5 (PT tích 0,5 · BPT 0,5 · hệ 0,75 · PT chứa ẩn ở mẫu 0,75) — II 3,5 (lập hệ 2,0 + lập BPT 1,5)
  — III 1,0 lượng giác thực tế — IV 3,0 hình (a tính 1,5 · b hai cặp đồng dạng 1,5).
Phần 1,0 điểm VDC cũ (IV.c + Bài V) chuyển sang hai câu vận dụng: lập hệ 1,5→2,0 và chứng minh hình 1,0→1,5.

Mọi câu chép từ ẢNH đề gốc (inputs/refs/de-thi/lop-9/giua-ki-1/). Đáp số đã kiểm SymPy, hình kiểm bằng toạ độ.
SỬA ĐỀ THÌ SỬA Ở ĐÂY rồi chạy lại — không sửa tay JSON.

Chạy:  .venv/bin/python scripts/de_gk1_lop9_60_phut.py
       .venv/bin/python -m src.main build-folder inputs/seeds/lop-9/de-kiem-tra-giua-ki-1-60-phut
"""
import json
import re as _re
from math import atan2, degrees, hypot, radians, tan
from pathlib import Path

OUT = Path("inputs/seeds/lop-9/de-kiem-tra-giua-ki-1-60-phut")
OUT.mkdir(parents=True, exist_ok=True)
BR = " [[br]] "


def d(x):  # 0.25 -> "0,25"
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def st(text, diem=None):
    return text + (f" \\hfill \\textit{{({d(diem)}đ)}}" if diem else "")


def xuong_dong(t):
    """Câu văn mới (sau dấu chấm, chữ kế là chữ HOA) xuống dòng — như bo_tuong_duong của bản 90 phút."""
    out = []
    for seg in _re.split(r"(\$[^$]*\$)", t):
        if not (seg.startswith("$") and seg.endswith("$") and len(seg) > 1):
            seg = _re.sub(r"(?<=[.])\s+(?=[A-ZĐÂĂÊÔƠƯ])", BR, seg)
        out.append(seg)
    return "".join(out).strip()


def y(nhan, diem, steps):
    than = BR.join(xuong_dong(st(*s) if isinstance(s, tuple) else s) for s in steps)
    return (f"\\textbf{{{nhan} ({d(diem)}đ)}}" + BR + than) if nhan else than


# ─────────────────────────── HÌNH ───────────────────────────
def goc(cx, cy, a0, a1, r, nhan, rn):
    return (f"\\draw[line width=0.7pt] ({cx},{cy}) ++({a0}:{r}) arc ({a0}:{a1}:{r});"
            f"\\node at ($({cx},{cy})+({(a0+a1)/2}:{rn})$) {{{nhan}}};")


def vuong(x, y_, dx, dy, s=0.3):
    """kí hiệu góc vuông tại (x,y), hai cạnh theo hướng (dx,0) và (0,dy)"""
    return f"\\draw[line width=0.6pt] ({x+dx*s},{y_})--({x+dx*s},{y_+dy*s})--({x},{y_+dy*s});"


def vg(P, Q, R, s=0.16):
    """kí hiệu góc vuông tại Q (giữa QP và QR) — vẽ theo toạ độ"""
    (px, py), (qx, qy), (rx, ry) = P, Q, R
    u = (px - qx, py - qy); lu = hypot(*u); u = (u[0] / lu * s, u[1] / lu * s)
    v = (rx - qx, ry - qy); lv = hypot(*v); v = (v[0] / lv * s, v[1] / lv * s)
    return (f"\\draw[line width=0.5pt] ({qx+u[0]:.3f},{qy+u[1]:.3f})--({qx+u[0]+v[0]:.3f},{qy+u[1]+v[1]:.3f})"
            f"--({qx+v[0]:.3f},{qy+v[1]:.3f});")


def hinh(pts, segs, extra="", scale=1.3):
    s = f"\\begin{{tikzpicture}}[scale={scale},line width=1pt]"
    for k, (x, yy, pos) in pts.items():
        s += f"\\coordinate ({k}) at ({x:.3f},{yy:.3f});"
    for a, b in segs:
        s += f"\\draw ({a})--({b});"
    s += extra
    for k, (x, yy, pos) in pts.items():
        s += f"\\fill ({k}) circle (1.8pt);\\node[{pos}] at ({k}) {{${k}$}};"
    return s + "\\end{tikzpicture}"


# Bài III — Thạch Bàn: bóng AH = 36 m, góc 55°, nhà 13 tầng. Vẽ tỉ lệ 1 m = 0,1 cm.
_HB = 3.6 * tan(radians(55))
TIKZ_TOANHA = ("\\begin{tikzpicture}[line width=1pt]"
               "\\coordinate (A) at (0,0);\\coordinate (H) at (3.6,0);"
               f"\\coordinate (B) at (3.6,{_HB:.3f});"
               f"\\fill[gray!12] (3.6,0) rectangle (5.0,{_HB:.3f});"
               f"\\draw[gray!70,line width=0.6pt] (3.6,0) rectangle (5.0,{_HB:.3f});"
               f"\\foreach \\k in {{1,...,12}} {{\\draw[gray!45,line width=0.5pt] (3.6,{{\\k*{_HB/13:.4f}}}) -- (5.0,{{\\k*{_HB/13:.4f}}});}}"
               "\\draw (-0.6,0)--(5.6,0);\\draw (A)--(B)--(H);" + vuong(3.6, 0, -1, 1, 0.3)
               + goc(0, 0, 0, 55, 0.7, "", 1) +
               "\\node at (1.15,0.45) {$55^\\circ$};"
               "\\node[below left] at (A) {$A$};\\node[below] at (H) {$H$};\\node[above] at (B) {$B$};"
               "\\node[below=3pt] at (1.8,0) {$36$ m};\\end{tikzpicture}")

# Bài IV — Láng Thượng: A vuông, sin ACB = 3/5, BC = 20 ⇒ AB = 12, AC = 16; H chân đường cao;
# D = (đường vuông góc với BC tại B) ∩ (đường thẳng AC). Toạ độ chia 4.
_k = 0.25
B4, C4 = (0.0, 0.0), (20 * _k, 0.0)
A4, H4 = (7.2 * _k, 9.6 * _k), (7.2 * _k, 0.0)
D4 = (0.0, 15 * _k)
_dist = lambda P, Q: hypot(P[0] - Q[0], P[1] - Q[1])
assert abs(_dist(A4, B4) - 12 * _k) < 1e-9 and abs(_dist(A4, C4) - 16 * _k) < 1e-9
assert abs((A4[0] - B4[0]) * (C4[0] - A4[0]) + (A4[1] - B4[1]) * (C4[1] - A4[1])) < 1e-9      # AB ⊥ AC
assert abs((D4[0] - A4[0]) * (C4[1] - A4[1]) - (D4[1] - A4[1]) * (C4[0] - A4[0])) < 1e-9      # D, A, C thẳng hàng
assert abs(_dist(A4, D4) * _dist(A4, C4) - _dist(B4, H4) * _dist(B4, C4)) < 1e-9               # AD·AC = BH·BC
assert abs(degrees(atan2(A4[1], C4[0] - A4[0])) - 36.87) < 0.01                                 # góc ACB ≈ 37°
print("Hình IV: AB=12, AC=16, AB⊥AC, D∈AC, AD·AC=BH·BC: OK")
HINH_IV = hinh({"A": (*A4, "above right"), "B": (*B4, "below left"), "C": (*C4, "below right"),
                "H": (*H4, "below"), "D": (*D4, "left")},
               [("A", "B"), ("B", "C"), ("C", "A"), ("A", "H"), ("B", "D"), ("D", "A")],
               extra=vg(B4, A4, C4) + vg(A4, H4, C4) + vg(D4, B4, C4))

# ─────────────────────────── ĐỀ ───────────────────────────
D = dict(
    ten="ĐỀ KIỂM TRA GIỮA HỌC KÌ I (60 PHÚT)",
    slug_de="de-kiem-tra-giua-ki-1-chinh-thuc-60-phut", slug_mt="ma-tran-va-dap-an-giua-ki-1-chinh-thuc-60-phut",
    eyebrow="LỚP 9 • ĐỀ CHÍNH THỨC",
    cach_dung="Đề chốt 60 phút, không có câu vận dụng cao: làm như thi thật, chấm theo đúng biểu điểm. "
              "Không chữa trước khi chấm xong cả lớp. Trả kết quả cho HS theo từng bài bằng phiếu theo dõi ở cuối file này.",
    gioi_thieu=("\\textbf{ĐỀ KIỂM TRA GIỮA HỌC KÌ I -- TOÁN 9 (BẢN 60 PHÚT)} (60 phút -- Thang điểm 10 -- 4 bài tự luận, không có câu vận dụng cao)." + BR +
                "\\textbf{Mục đích:} đánh giá vì sự tiến bộ -- đo xem HS đã \\textbf{thành thạo} các dạng cơ bản của giữa kì I chưa. "
                "Đề \\textbf{mới hoàn toàn}: mọi câu lấy từ đề thật của 5 trường Hà Nội \\textbf{chưa dùng} ở 3 đề ôn và đề 90 phút."),
    bai=[
        dict(label="Bài I.", level=2,
             statement="\\textbf{(2,5 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:" + BR +
             "a) \\textbf{(0,5 điểm)} $(3-x)\\left(\\dfrac12x+1\\right)=0$" + BR +
             "b) \\textbf{(0,5 điểm)} $3(2x-3)\\ge 4(2-x)+13$" + BR +
             "c) \\textbf{(0,75 điểm)} $\\begin{cases}x+y=0\\\\ 4x+3y=2\\end{cases}$" + BR +
             "d) \\textbf{(0,75 điểm)} $\\dfrac{x-1}{x}+\\dfrac{1}{x+1}=\\dfrac{2x+1}{x^2+x}$",
             dap_an=[
                 y("a)", 0.5, [("$(3-x)\\left(\\dfrac12x+1\\right)=0$ nên $3-x=0$ hoặc $\\dfrac12x+1=0$", 0.25),
                               "$x=3$ hoặc $x=-2$.",
                               ("Vậy phương trình có hai nghiệm $x=3$; $x=-2$.", 0.25)]),
                 y("b)", 0.5, ["$3(2x-3)\\ge 4(2-x)+13$",
                               "$6x-9\\ge 8-4x+13$",
                               ("$10x\\ge 30$", 0.25),
                               "$x\\ge 3$.",
                               ("Vậy nghiệm của bất phương trình là $x\\ge 3$.", 0.25)]),
                 y("c)", 0.75, [("Từ phương trình thứ nhất: $y=-x$.", 0.25),
                                "Thế vào phương trình thứ hai: $4x+3\\cdot(-x)=2$",
                                ("$x=2$, suy ra $y=-2$.", 0.25),
                                ("Vậy hệ có nghiệm duy nhất $(x;y)=(2;-2)$.", 0.25)]),
                 y("d)", 0.75, [("ĐKXĐ: $x\\ne 0$; $x\\ne -1$. Ta có $x^2+x=x(x+1)$, mẫu chung $x(x+1)$.", 0.25),
                                "Quy đồng, khử mẫu: $(x-1)(x+1)+x=2x+1$",
                                "$x^2-1+x-2x-1=0$",
                                "$x^2-x-2=0$",
                                "$x^2-2x+x-2=0$",
                                ("$(x-2)(x+1)=0$", 0.25),
                                "$x=2$ (TMĐK) hoặc $x=-1$ (không TMĐK).",
                                ("Vậy phương trình có nghiệm $x=2$.", 0.25)]),
             ],
             mt=[("Ia", "Giải phương trình tích", "ĐS II", "NB", 0.5, 3, "THCS Lý Nam Đế"),
                 ("Ib", "Giải BPT bậc nhất (bỏ ngoặc, chuyển vế)", "ĐS II", "TH", 0.5, 4, "THCS Lý Nam Đế"),
                 ("Ic", "Giải hệ hai PT bậc nhất hai ẩn", "ĐS I", "NB", 0.75, 4, "THCS Chu Văn An"),
                 ("Id", "PT chứa ẩn ở mẫu: phân tích mẫu $x^2+x$, có nghiệm bị loại", "ĐS II", "VD", 0.75, 7, "THCS Phan Đình Giót")],
             note="Ý d: HS phải tự phân tích $x^2+x=x(x+1)$ để tìm ĐKXĐ và mẫu chung; giải ra $x=-1$ mà không loại thì trừ $0{,}25$đ."),
        dict(label="Bài II.", level=3,
             statement="\\textbf{(3,5 điểm)}" + BR +
             "1) \\textbf{(2,0 điểm)} \\textit{Giải bài toán bằng cách lập hệ phương trình.}" + BR +
             "Một người mua một cái bàn là và một cái quạt điện với tổng số tiền theo giá niêm yết là $750$ nghìn đồng. "
             "Khi trả tiền người đó được khuyến mại $10\\%$ đối với bàn là và $20\\%$ đối với quạt điện so với giá niêm yết. "
             "Vì vậy người đó phải trả tổng cộng $625$ nghìn đồng. Tính giá tiền bàn là và quạt điện theo giá niêm yết." + BR +
             "2) \\textbf{(1,5 điểm)} Trong phần thi ``Đố vui toán học'' của chương trình Ngày hội Toán học ở một trường THCS, "
             "mỗi thí sinh tham gia phải trả lời $10$ câu hỏi của ban tổ chức và không được phép bỏ qua câu hỏi nào. "
             "Với mỗi câu trả lời đúng, thí sinh được cộng $5$ điểm; với mỗi câu trả lời sai, thí sinh bị trừ $3$ điểm. "
             "Khi bắt đầu phần thi, mỗi thí sinh được nhận $20$ điểm. Thí sinh nào đạt từ $40$ điểm trở lên sẽ được vào phần thi tiếp theo." + BR +
             "a) \\textbf{(0,5 điểm)} Gọi $x$ là số câu trả lời đúng của mỗi thí sinh ($x$ là số nguyên dương), "
             "viết biểu thức biểu thị tổng số điểm đạt được của mỗi thí sinh." + BR +
             "b) \\textbf{(1,0 điểm)} Tính xem mỗi thí sinh phải trả lời đúng ít nhất bao nhiêu câu để được vào phần thi tiếp theo.",
             dap_an=[
                 y("1)", 2.0, [("Gọi giá niêm yết của cái bàn là, cái quạt điện lần lượt là $x$, $y$ (nghìn đồng; $0<x<750$, $0<y<750$).", 0.25),
                               ("Tổng giá niêm yết là $750$ nghìn đồng nên $x+y=750$ \\quad (1)", 0.25),
                               ("Sau khuyến mại, bàn là còn $90\\%$ giá niêm yết là $0{,}9x$; quạt điện còn $80\\%$ là $0{,}8y$.", 0.25),
                               ("Người đó trả $625$ nghìn đồng nên $0{,}9x+0{,}8y=625$ \\quad (2)", 0.25),
                               "Từ (1): $y=750-x$. Thế vào (2): $0{,}9x+0{,}8(750-x)=625$",
                               "$0{,}9x+600-0{,}8x=625$",
                               ("$0{,}1x=25$", 0.25),
                               ("$x=250$ (TMĐK).", 0.25),
                               ("Suy ra $y=750-250=500$ (TMĐK).", 0.25),
                               ("Vậy giá niêm yết của cái bàn là là $250$ nghìn đồng, của cái quạt điện là $500$ nghìn đồng.", 0.25)]),
                 y("2a)", 0.5, [("Số câu trả lời sai là $10-x$ (câu) (điều kiện $x\\in\\mathbb N^*$, $x\\le 10$).", 0.25),
                                ("Tổng số điểm đạt được: $20+5x-3(10-x)=8x-10$ (điểm).", 0.25)]),
                 y("2b)", 1.0, [("Để vào phần thi tiếp theo thì $8x-10\\ge 40$", 0.25),
                                "$8x\\ge 50$",
                                ("$x\\ge 6{,}25$.", 0.25),
                                ("Vì $x\\in\\mathbb N^*$, $x\\le 10$ nên $x\\in\\{7;8;9;10\\}$, giá trị nhỏ nhất là $x=7$.", 0.25),
                                ("Vậy mỗi thí sinh phải trả lời đúng ít nhất $7$ câu.", 0.25)]),
             ],
             mt=[("II.1", "Lập hệ PT -- khuyến mại hai mức $\\%$ trên giá niêm yết", "ĐS I", "VD", 2.0, 11, "THCS Phan Đình Giót"),
                 ("II.2", "Lập BPT thực tế -- ``ít nhất bao nhiêu câu'' (ý a dẫn dắt lập biểu thức)", "ĐS II", "TH", 1.5, 7, "THCS Chu Văn An")],
             note="Ý 1: đề gốc ghi ``lập phương trình'', ở đây yêu cầu lập hệ cho đúng dạng đã ôn; HS lập phương trình một ẩn đúng vẫn cho đủ điểm. "
                  "Ý 2b: $x\\ge 6{,}25$ phải làm tròn LÊN thành $7$; HS kết luận $6$ câu thì không cho $0{,}25$đ kết luận."),
        dict(label="Bài III.", level=2,
             statement="\\textbf{(1,0 điểm)} Tại một thời điểm trong ngày, tia nắng mặt trời hợp với mặt đất một góc bằng $55^\\circ$. "
             "Một tòa nhà có bóng xuống mặt đường một đoạn có độ dài $36$ m. Biết tòa nhà có $13$ tầng. "
             "Tính chiều cao của mỗi tầng? (Làm tròn các kết quả đến hàng đơn vị). Bài toán được mô tả như hình vẽ.",
             figure=dict(tikz=TIKZ_TOANHA, pos="right"),
             dap_an=[y("", 1.0, [("Từ hình vẽ: $BH$ là chiều cao tòa nhà, $AH=36$ m là bóng tòa nhà, $\\widehat{BAH}=55^\\circ$.", 0.25),
                                 ("Xét $\\triangle ABH$ vuông tại $H$: $BH=AH\\cdot\\tan\\widehat{BAH}=36\\cdot\\tan 55^\\circ\\approx 51$ (m).", 0.5),
                                 ("Chiều cao mỗi tầng: $\\dfrac{36\\cdot\\tan 55^\\circ}{13}\\approx 4$ (m). Vậy mỗi tầng cao khoảng $4$ m.", 0.25)])],
             mt=[("III", "Ứng dụng tỉ số lượng giác: chiều cao (dùng $\\tan$) rồi chia đều", "HH IV", "TH", 1.0, 5, "THCS Thạch Bàn")],
             note="$BH\\approx 51{,}4$ m; lấy $51:13$ hay $51{,}4:13$ đều ra khoảng $4$ m. HS dùng $\\sin$, $\\cos$ sai cạnh thì không cho điểm bước tính."),
        dict(label="Bài IV.", level=3,
             statement="\\textbf{(3,0 điểm)} Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$." + BR +
             "a) \\textbf{(1,5 điểm)} Nếu $\\sin\\widehat{ACB}=\\dfrac35$ và $BC=20$ cm. Hãy tính $\\widehat{ACB}$; $AB$, $AC$. "
             "(Số đo góc làm tròn đến độ)" + BR +
             "b) \\textbf{(1,5 điểm)} Kẻ đường thẳng vuông góc với $BC$ tại $B$ cắt đường thẳng $AC$ tại $D$. "
             "Chứng minh rằng: $AD\\cdot AC=BH\\cdot BC$.",
             hinh_da=HINH_IV,
             dap_an=[
                 y("a)", 1.5, [("Vẽ hình đúng (như hình vẽ).", 0.25),
                               ("$\\sin\\widehat{ACB}=\\dfrac35$ nên $\\widehat{ACB}\\approx 37^\\circ$.", 0.25),
                               ("$\\triangle ABC$ vuông tại $A$: $AB=BC\\cdot\\sin\\widehat{ACB}=20\\cdot\\dfrac35=12$ (cm).", 0.5),
                               ("$AC=\\sqrt{BC^2-AB^2}=\\sqrt{400-144}=\\sqrt{256}=16$ (cm).", 0.5),
                               "Vậy $\\widehat{ACB}\\approx 37^\\circ$, $AB=12$ cm, $AC=16$ cm."]),
                 y("b)", 1.5, ["$D$ thuộc đường thẳng $AC$, $AB\\perp AC$ nên $\\widehat{DAB}=90^\\circ$.",
                               "$\\triangle DBC$ vuông tại $B$ nên $\\widehat{ADB}+\\widehat{ACB}=90^\\circ$; "
                               "$\\triangle ABC$ vuông tại $A$ nên $\\widehat{ABC}+\\widehat{ACB}=90^\\circ$.",
                               ("Suy ra $\\widehat{ADB}=\\widehat{ABC}$.", 0.25),
                               "Xét $\\triangle ADB$ và $\\triangle ABC$: $\\widehat{DAB}=\\widehat{BAC}=90^\\circ$, $\\widehat{ADB}=\\widehat{ABC}$",
                               "$\\Rightarrow\\triangle ADB\\backsim\\triangle ABC$ (g.g) $\\Rightarrow\\dfrac{AD}{AB}=\\dfrac{AB}{AC}$",
                               ("$\\Rightarrow AD\\cdot AC=AB^2$. \\quad (1)", 0.5),
                               ("Xét $\\triangle BHA$ và $\\triangle BAC$: $\\widehat{BHA}=\\widehat{BAC}=90^\\circ$, $\\widehat{ABC}$ chung "
                                "$\\Rightarrow\\triangle BHA\\backsim\\triangle BAC$ (g.g)", 0.25),
                               ("$\\Rightarrow\\dfrac{BH}{BA}=\\dfrac{BA}{BC}\\Rightarrow BH\\cdot BC=AB^2$. \\quad (2)", 0.25),
                               ("Từ (1), (2) suy ra $AD\\cdot AC=BH\\cdot BC$.", 0.25)]),
             ],
             mt=[("IVa", "Tính góc, cạnh tam giác vuông từ $\\sin$ (có vẽ hình)", "HH IV", "TH", 1.5, 7, "THCS Láng Thượng"),
                 ("IVb", "Hai cặp tam giác đồng dạng g.g cùng cho tích $=AB^2$", "HH IV", "VD", 1.5, 10, "THCS Láng Thượng")],
             note="HS không được dùng hệ thức lượng trực tiếp ($AB^2=BH\\cdot BC$) -- phải chứng minh đồng dạng. "
                  "Chứng minh được một trong hai đẳng thức (1), (2) cho $0{,}75$đ. Ý c gốc của đề trường (vận dụng cao) đã bỏ."),
    ])

# Quận/huyện CŨ đọc từ header đề — khớp inputs/refs/de-thi/lop-9/luoi-dang/gk1.json.
QUAN = {"THCS Lý Nam Đế": "Nam Từ Liêm", "THCS Chu Văn An": "Tây Hồ",
        "THCS Phan Đình Giót": "Thanh Xuân", "THCS Thạch Bàn": "Long Biên",
        "THCS Láng Thượng": "Đống Đa"}
# So với đề 90 phút (bản 1 = bản 2): (bài, điểm cũ, điểm mới, thay đổi)
SO_SANH = [("Bài I -- PT, BPT, hệ", "3,0", "2,5", "4 ý giữ đủ dạng, mỗi ý gọn hơn (0,5 -- 0,75đ)"),
           ("Bài II -- lập hệ / lập BPT", "3,0", "3,5", "lập hệ $1{,}5\\to 2{,}0$; lập BPT giữ $1{,}5$ (thêm ý a dẫn dắt)"),
           ("Bài III -- lượng giác thực tế", "1,0", "1,0", "giữ nguyên"),
           ("Bài IV -- hình học", "2,5", "3,0", "ý chứng minh $1{,}0\\to 1{,}5$; \\textbf{bỏ ý c (VDC 0,5)}"),
           ("Bài V -- tối ưu", "0,5", "--", "\\textbf{bỏ (VDC)}")]


def kiem_nguon():
    from collections import defaultdict
    q, tt = defaultdict(float), defaultdict(float)
    for b in D["bai"]:
        for r in b["mt"]:
            q[QUAN[r[6]]] += r[4]; tt[r[6]] += r[4]
    assert len(q) >= 4 and max(q.values()) <= 4.0 + 1e-9, dict(q)
    return len(tt), q


N_TRUONG, NGUON_Q = kiem_nguon()
print(N_TRUONG, "trường,", len(NGUON_Q), "quận:", ", ".join(f"{a} {d(v)}" for a, v in sorted(NGUON_Q.items(), key=lambda t: -t[1])))


# ─────────────────────────── DỰNG JSON ───────────────────────────
KIND = ["review", "concept", "practice1", "practice2", "reflection"]


def bang_mt(rows):
    s = ("\\vspace{-6pt}\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.05}\n"
         "\\begin{tabular}{|c|p{5.6cm}|c|c|c|c|p{3.3cm}|}\n\\hline\n"
         "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Chương} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} & \\textbf{Nguồn đề} \\\\ \\hline\n")
    tong_d = tong_p = 0
    for c, nd, ch, m, di, ph, ng in rows:
        s += f"{c} & {nd} & {ch} & {m} & {d(di)} & {ph} & {ng} \\\\ \\hline\n"
        tong_d += di; tong_p += ph
    s += f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{TỔNG CỘNG}}}} & \\textbf{{{d(tong_d)}}} & \\textbf{{{tong_p}}} & \\\\ \\hline\n"
    return s + "\\end{tabular}\\end{center}", tong_d, tong_p


def bang_muc(rows):
    muc = {"NB": 0, "TH": 0, "VD": 0}
    ds = {"Đại số (Chương I, II)": dict(muc), "Hình học (Chương IV)": dict(muc)}
    for c, nd, ch, m, di, ph, ng in rows:
        ds["Hình học (Chương IV)" if ch.startswith("HH") else "Đại số (Chương I, II)"][m] += di
    s = ("\\noindent\\textbf{TỔNG HỢP THEO MẠCH KIẾN THỨC VÀ CẤP ĐỘ (điểm)}\\par\\nopagebreak\\vspace{-6pt}\n"
         "\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.05}\n\\begin{tabular}{|l|c|c|c|c|c|}\n\\hline\n"
         "\\textbf{Mạch kiến thức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{VDC} & \\textbf{Tổng} \\\\ \\hline\n")
    tot = dict(muc)
    for k, v in ds.items():
        s += f"{k} & " + " & ".join(d(v[m]) if v[m] else "0" for m in muc) + f" & 0 & \\textbf{{{d(sum(v.values()))}}} \\\\ \\hline\n"
        for m in muc:
            tot[m] += v[m]
    s += "\\textbf{Tổng điểm} & " + " & ".join(f"\\textbf{{{d(tot[m])}}}" for m in muc) + " & \\textbf{0} & \\textbf{10,0} \\\\ \\hline\n"
    s += "\\textbf{Tỉ lệ} & " + " & ".join(f"{tot[m]*10:g}".replace(".", ",") + "\\%" for m in muc) + " & 0\\% & 100\\% \\\\ \\hline\n"
    return s + "\\end{tabular}\\end{center}"


def bang_so_sanh():
    s = ("\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.1}\n"
         "\\begin{tabular}{|p{4.0cm}|c|c|p{7.6cm}|}\n\\hline\n"
         "\\textbf{Bài} & \\textbf{90 phút} & \\textbf{60 phút} & \\textbf{Thay đổi} \\\\ \\hline\n")
    for r in SO_SANH:
        s += " & ".join(r) + " \\\\ \\hline\n"
    return s + "\\textbf{Tổng} & \\textbf{10,0} & \\textbf{10,0} & VDC $1{,}0$đ chuyển sang hai câu vận dụng \\\\ \\hline\n\\end{tabular}\\end{center}"


def bang_theo_doi():
    s = ("\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.35}\n"
         "\\begin{tabular}{|l|c|c|c|}\n\\hline\n"
         "\\textbf{Bài (điểm tối đa)} & \\textbf{Mức thành thạo} & \\textbf{Điểm HS} & \\textbf{Đạt?} \\\\ \\hline\n")
    for b, m in [("Bài I -- phương trình, BPT, hệ (2,5)", "$\\ge 2{,}0$"), ("Bài II -- lập hệ / lập BPT (3,5)", "$\\ge 2{,}75$"),
                 ("Bài III -- lượng giác thực tế (1,0)", "đủ $1{,}0$"), ("Bài IV -- hình học (3,0)", "$\\ge 2{,}25$"),
                 ("\\textbf{Tổng (10,0)}", "$\\ge 8{,}0$")]:
        s += f"{b} & {m} & & \\\\ \\hline\n"
    return s + "\\end{tabular}\\end{center}"


def de_json():
    stages = []
    for i, b in enumerate(D["bai"]):
        sol = BR.join(b["dap_an"])
        if b.get("hinh_da"):
            sol = "\\begin{center}\\adjustbox{max width=0.62\\linewidth}{" + b["hinh_da"] + "}\\end{center}" + sol
        blk = dict(type="problem", label=b["label"], level=b["level"], statement=b["statement"], tier="onclass", solution=sol)
        if b.get("figure"):
            blk["figure"] = dict(tikz=b["figure"]["tikz"], pos=b["figure"]["pos"])
        stages.append(dict(kind=KIND[i], number=i + 1, title="", blocks=[blk], teacher_note=b["note"]))
    # đề 4 bài, schema cần đủ 5 chặng ⇒ chặng cuối chỉ có dòng HẾT
    stages.append(dict(kind=KIND[4], number=5, title="", blocks=[
        dict(type="para", text="\\nopagebreak\\centerline{\\textit{$-$ HẾT $-$}}")],
        teacher_note="Thu bài đúng 60 phút."))
    return dict(slug=D["slug_de"], title="Đề kiểm tra giữa học kì I (60 phút)", eyebrow=D["eyebrow"], grade_label="Lớp 9",
                class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


def mt_json():
    rows = [r for b in D["bai"] for r in b["mt"]]
    t1, td, tp = bang_mt(rows)
    assert abs(td - 10) < 1e-9 and tp <= 60, (td, tp)
    nguon = (f"\\textbf{{Nguồn đề:}} câu lấy từ {N_TRUONG} trường thuộc {len(NGUON_Q)} quận/huyện ("
             + "; ".join(f"{a} {d(v)}đ" for a, v in sorted(NGUON_Q.items(), key=lambda t: -t[1]))
             + "), đều là đề năm học 2024--2025; không quận nào quá $30\\%$ số điểm của đề. Không trường nào trùng với 3 đề ôn và đề 90 phút.")
    st0 = [dict(type="para", text=D["gioi_thieu"] + BR + nguon), dict(type="para", text=t1), dict(type="para", text=bang_muc(rows)),
           dict(type="para", text=f"\\noindent\\textit{{\\footnotesize Tổng thời gian làm bài ước tính: {tp} phút (còn khoảng 2 phút soát bài). "
                                  "Mức NB/TH/VD chấm theo cách trường ghi trong ma trận đề gốc.}"),
           dict(type="para", text="\\noindent\\textbf{SO VỚI ĐỀ 90 PHÚT}\\par\\nopagebreak" + bang_so_sanh())]
    stages = [dict(kind="review", number=1, title="Ma trận đề", blocks=st0, teacher_note=D["cach_dung"])]
    grp = [("Đáp án Bài I", [0]), ("Đáp án Bài II", [1]), ("Đáp án Bài III và Bài IV", [2, 3])]
    for j, (ti, idx) in enumerate(grp, 2):
        blocks = []
        for i in idx:
            b = D["bai"][i]
            diem = sum(r[4] for r in b["mt"])
            blocks.append(dict(type="para", text=f"\\textbf{{{b['label'].upper().replace('.', '')} ({d(diem)} điểm).}}"))
            if b.get("hinh_da"):
                blocks.append(dict(type="figure", tikz=b["hinh_da"], width="0.5\\linewidth"))
            if b.get("figure"):
                blocks.append(dict(type="figure", tikz=b["figure"]["tikz"], width="0.4\\linewidth"))
            for a in b["dap_an"]:
                blocks.append(dict(type="para", text=a))
            blocks.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + b["note"] + "}"))
        stages.append(dict(kind=KIND[j - 1], number=j, title=ti, blocks=blocks))
    bd = BR.join(f"\\textbf{{{b['label']} ({d(sum(r[4] for r in b['mt']))}đ):}} " +
                 " $-$ ".join(f"{r[0]} {d(r[4])}đ" for r in b["mt"]) for b in D["bai"])
    stages.append(dict(kind=KIND[4], number=5, title="Biểu điểm và phiếu theo dõi", blocks=[
        dict(type="para", text="\\textbf{BIỂU ĐIỂM TỔNG HỢP}" + BR + bd),
        dict(type="para", text="\\textbf{Tổng: 10,0 điểm.} Điểm toàn bài làm tròn đến $0{,}25$ điểm. "
                               "Học sinh giải theo cách khác đúng vẫn cho điểm tối đa từng phần. Bài hình vẽ sai hình không chấm điểm."),
        dict(type="para", text="\\textbf{PHIẾU THEO DÕI TIẾN BỘ (ghi điểm từng bài của mỗi học sinh)}" + BR +
             "Đề không có câu vận dụng cao, nên HS đã thành thạo các dạng cơ bản phải đạt đủ bốn mức dưới đây (khoảng $8{,}0$ điểm trở lên). "
             "Bài nào chưa đạt mức thì ôn lại đúng dạng đó trước khi sang phần mới."),
        dict(type="para", text=bang_theo_doi()),
    ]))
    return dict(slug=D["slug_mt"], title="Ma trận đề và đáp án chi tiết — Đề GK1 chính thức (60 phút)",
                eyebrow="TÀI LIỆU GIÁO VIÊN • LỚP 9 • " + D["ten"], grade_label="Lớp 9",
                class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


(OUT / f"{D['slug_de']}.json").write_text(json.dumps(de_json(), ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / f"{D['slug_mt']}.json").write_text(json.dumps(mt_json(), ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", OUT)
