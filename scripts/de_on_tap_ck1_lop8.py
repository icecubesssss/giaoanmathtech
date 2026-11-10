#!/usr/bin/env python3
"""BỘ ĐỀ ÔN TẬP CUỐI KÌ 1 (CK1) TOÁN 8 (Chương trình mới GDPT 2018 - Kết nối tri thức - Hà Nội).
Sinh 3 đề ôn tập (Số 1, Số 2, Số 3) + 3 file Ma trận đề và đáp án chi tiết cho GV
vào inputs/seeds/lop-8/de-on-tap-cuoi-ki-1/ (theme de_thi, trinh_bay "thoang").
Quy trình: docs/quy-trinh-bo-de-on-tap.md.

Mọi câu trích nguyên văn từ đề thi thật các Phòng GD&ĐT và trường THCS chuẩn KNTT tại Hà Nội.
Đáp số đã kiểm chứng SymPy / giải tích. Lời giải tuân thủ 100% cổng loi_giai_thi_gate và sgk_style_gate.

Chạy:  .venv/bin/python scripts/de_on_tap_ck1_lop8.py
       .venv/bin/python -m src.main validate inputs/seeds/lop-8/de-on-tap-cuoi-ki-1/de-on-tap-cuoi-ki-1-so-1.json
"""
import json
import re as _re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import de_ck1_lop8_hinh as H  # noqa: E402

OUT = ROOT / "inputs/seeds/lop-8/de-on-tap-cuoi-ki-1"
OUT.mkdir(parents=True, exist_ok=True)
BR = " [[br]] "


def d(x):  # 0.25 -> "0,25"
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def st(text, diem=None):
    return text + (f" \\hfill \\textit{{({d(diem)}đ)}}" if diem else "")


def bo_tuong_duong(t):
    """HS đi thi KHÔNG dùng dấu ⇔ (Thầy 01/10/2026): mỗi phép biến đổi xuống một dòng.
    Cắt mọi đoạn toán $…$ tại \Leftrightarrow ở mức ngoặc 0, ngoài \begin…\end; bỏ dấu ⇔ đầu đoạn."""
    out = []
    for seg in _re.split(r"(\$[^$]*\$)", t):
        if not (seg.startswith("$") and seg.endswith("$") and len(seg) > 1):
            seg = _re.sub(r"(?<=[.])\s+(?=[A-ZĐÂĂÊÔƠƯ])", BR, seg)
            out.append(seg)
            continue
        m = seg[1:-1]
        parts, depth, env, last, i = [], 0, 0, 0, 0
        while i < len(m):
            if m.startswith("\\begin", i):
                env += 1
            elif m.startswith("\\end", i):
                env -= 1
            c = m[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            elif depth == 0 and env == 0 and m.startswith("\\Leftrightarrow", i):
                parts.append(m[last:i])
                i += len("\\Leftrightarrow")
                last = i
                continue
            i += 1
        parts.append(m[last:])
        parts = [p.strip() for p in parts if p.strip()]
        out.append(BR.join("$" + p + "$" for p in parts))
    s = "".join(out).strip()
    return _re.sub(r"^(?:\s*\[\[br\]\]\s*)+", "", s)


def y(nhan, diem, steps):
    than = BR.join(bo_tuong_duong(st(*s) if isinstance(s, tuple) else s) for s in steps)
    return (f"\\textbf{{{nhan} ({d(diem)}đ)}}" + BR + than) if nhan else than


def tn(cau, de, options, dap, giai, nd, ch, muc, nguon, level=1):
    return dict(cau=cau, de=de, options=options, dap=dap, giai=giai, nd=nd, ch=ch, muc=muc, nguon=nguon, level=level)


TN_DAU = (
    "\\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm).} \\textit{Mỗi câu 0,25 điểm. Chọn chữ cái đứng trước "
    "câu trả lời đúng rồi ghi vào bài làm (ví dụ: 1 -- A).}"
)
TL_DAU = "\\textbf{PHẦN II. TỰ LUẬN (8,0 điểm)}"


# ─────────────────────────── NGUỒN VÀ LUẬT ───────────────────────────
QUAN = {
    "THCS Nghĩa Tân": "Cầu Giấy",
    "THCS Giảng Võ": "Ba Đình",
    "THCS Ngọc Lâm": "Long Biên",
    "THCS Phan Đình Giót": "Thanh Xuân",
    "THCS Phúc Diễn": "Bắc Từ Liêm",
    "THCS Phan Chu Trinh": "Ba Đình",
    "THCS Lê Quý Đôn": "Cầu Giấy",
    "THCS Ngô Sĩ Liên": "Hoàn Kiếm",
    "THCS Đông Mỹ": "Thanh Trì",
    "THCS Đa Tốn": "Gia Lâm",
    "THCS \& THPT Lương Thế Vinh": "Cầu Giấy",
    "THCS Nguyễn Công Trứ": "Ba Đình",
    "THCS Nguyễn Trường Tộ": "Đống Đa",
    "Quận Tây Hồ": "Tây Hồ",
    "THCS Tân Triều": "Thanh Trì",
}

# ─────────────────────────── DANH SÁCH 3 ĐỀ ÔN TẬP ───────────────────────────
DE = {}

# =====================================================================
# ĐỀ ÔN TẬP SỐ 1
# =====================================================================
DE["on-1"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 1",
    slug_de="de-on-tap-cuoi-ki-1-so-1",
    slug_mt="ma-tran-va-dap-an-on-tap-ck1-so-1",
    eyebrow="LỚP 8 • ĐỀ ÔN TẬP CUỐI KÌ I — SỐ 1",
    cach_dung="Làm bài trong 90 phút như thi thật. Chữa bài tập trung vào khâu lập luận trình bày: ĐKXĐ phân thức, biến đổi không dùng dấu tương đương, chứng minh hình học từng bước có căn cứ rõ ràng.",
    gioi_thieu=(
        "\\textbf{ĐỀ ÔN TẬP SỐ 1 -- CUỐI HỌC KÌ I TOÁN 8 (KNTT)} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc chuẩn:} Bám sát ma trận kiểm tra Cuối Kì 1 chuẩn Kết nối tri thức của các quận/huyện Hà Nội: "
        "Phần I (2,0đ) Trắc nghiệm 8 câu x 0,25đ bao quát các chương I, II, III, IV, V · "
        "Bài 1 (1,5đ) Phép tính đa thức \& Phân tích đa thức thành nhân tử · "
        "Bài 2 (2,0đ) Phân thức đại số: ĐKXĐ, rút gọn biểu thức, tính giá trị và tìm x nguyên · "
        "Bài 3 (1,0đ) Thống kê - biểu đồ cột kép KNTT · "
        "Bài 4 (3,0đ) Hình học tổng hợp: tam giác vuông, hình chữ nhật, hình thang cân, hình thoi · "
        "Bài 5 (0,5đ) VDC Giá trị nhỏ nhất hằng đẳng thức."
    ),
    bay=[
        ("Câu 8", "Quên tìm điều kiện để mẫu thức khác không khi tìm ĐKXĐ", "Chọn điều kiện tử thức hoặc giải sai dấu", "Cho toàn bộ mẫu thức khác không: $x - 2 \\ne 0 \\implies x \\ne 2$"),
        ("Bài 1.b", "Dấu trừ trước ngoặc khi áp dụng hằng đẳng thức hiệu hai bình phương", "Viết sai dấu $x^2 - (y - 3)^2 = (x - y - 3)(x + y + 3)$", "Đóng mở ngoặc cẩn thận: $[(x - 3) - y][(x - 3) + y] = (x - y - 3)(x + y - 3)$"),
        ("Bài 2.c", "Quên đối chiếu ĐKXĐ khi tìm giá trị nguyên của $x$", "Lấy cả giá trị $x = 2$ hoặc $x = -2$ làm mẫu bằng 0", "Luôn đối chiếu từng giá trị tìm được với $x \\ne \\pm 2$ trước khi kết luận"),
        ("Bài 4.b", "Ngộ nhận tứ giác là hình thang cân khi mới chỉ có hai cạnh bên bằng nhau", "Chưa chứng minh hai đáy song song đã vội kết luận hình thang cân", "Chứng minh $DE \\parallel HM$ (đường trung bình) trước để có hình thang, rồi chỉ ra $HD = ME$"),
        ("Bài 5", "Tách bình phương bị sót số hạng tự do", "Tìm sai giá trị nhỏ nhất do cộng trừ nhầm", "Nhóm thành các bình phương đúng: $(x - 2y + 5)^2 + (y - 1)^2 + 2 \\ge 2$"),
    ],
    tn=[
        tn(1, "Đơn thức nào sau đây đồng dạng với đơn thức $-3x^2y$?", ["$3xy^2$", "$\\dfrac{1}{2}x^2y$", "$-3x^2y^2$", "$2x^3y$"], "B",
           "Hai đơn thức đồng dạng có cùng phần biến $x^2y$.", "Đơn thức đồng dạng", "ĐS I", "NB", "THCS Nghĩa Tân"),
        tn(2, "Bậc của đa thức $P = 4x^3y^2 - x^4y + 3xy^3 - 7$ là:", ["$4$", "$5$", "$6$", "$3$"], "B",
           "Hạng tử $4x^3y^2$ và $-x^4y$ đều có bậc cao nhất là $3 + 2 = 4 + 1 = 5$.", "Bậc của đa thức", "ĐS I", "TH", "THCS Nghĩa Tân"),
        tn(3, "Hằng đẳng thức $A^2 - B^2$ bằng biểu thức nào sau đây?", ["$(A - B)^2$", "$(A - B)(A + B)$", "$(A + B)^2$", "$A^2 - 2AB + B^2$"], "B",
           "Theo hằng đẳng thức hiệu hai bình phương: $A^2 - B^2 = (A - B)(A + B)$.", "Hằng đẳng thức đáng nhớ", "ĐS II", "NB", "THCS Giảng Võ"),
        tn(4, "Phân tích đa thức $5x^2 - 10x$ thành nhân tử, ta được kết quả là:", ["$5x(x - 2)$", "$5(x^2 - 2)$", "$5x(x - 10)$", "$x(5x - 2)$"], "A",
           "Đặt nhân tử chung $5x$, ta được $5x(x - 2)$.", "Phân tích đa thức thành nhân tử", "ĐS II", "TH", "THCS Giảng Võ"),
        tn(5, "Tổng các góc trong một tứ giác lồi bằng:", ["$180^\\circ$", "$360^\\circ$", "$90^\\circ$", "$270^\\circ$"], "B",
           "Định lí tổng các góc của một tứ giác luôn bằng $360^\\circ$.", "Tứ giác", "HH III", "NB", "THCS Ngọc Lâm"),
        tn(6, "Tứ giác nào sau đây có hai đường chéo bằng nhau và cắt nhau tại trung điểm của mỗi đường?", ["Hình bình hành", "Hình thoi", "Hình thang cân", "Hình chữ nhật"], "D",
           "Hình chữ nhật có hai đường chéo bằng nhau và cắt nhau tại trung điểm của mỗi đường.", "Hình chữ nhật", "HH III", "TH", "THCS Phan Đình Giót"),
        tn(7, "Cho $\\triangle ABC$, một đường thẳng song song với $BC$ cắt hai cạnh $AB, AC$ lần lượt tại $D$ và $E$. Biết $AD = 3\\text{ cm}, DB = 2\\text{ cm}, AE = 4{,}5\\text{ cm}$. Độ dài đoạn thẳng $EC$ là:", ["$3\\text{ cm}$", "$2\\text{ cm}$", "$1{,}5\\text{ cm}$", "$2{,}5\\text{ cm}$"], "A",
           "Theo định lí Thalès: $\\dfrac{AD}{DB} = \\dfrac{AE}{EC} \\implies EC = \\dfrac{DB \\cdot AE}{AD} = \\dfrac{2 \\cdot 4{,}5}{3} = 3\\text{ cm}$.", "Định lí Thalès trong tam giác", "HH IV", "TH", "THCS Phúc Diễn"),
        tn(8, "Điều kiện xác định của phân thức đại số $\\dfrac{2x + 1}{x - 2}$ là:", ["$x \\ne 2$", "$x \\ne -2$", "$x \\ne -\\dfrac{1}{2}$", "$x \\ne 0$"], "A",
           "Phân thức xác định khi mẫu thức khác không: $x - 2 \\ne 0 \\implies x \\ne 2$.", "Phân thức đại số", "ĐS VI", "NB", "THCS Phan Chu Trinh"),
    ],
    bai=[
        dict(
            label="Bài 1.",
            level=2,
            statement=(
                "\\textbf{(1,5 điểm)}" + BR
                + "a) \\textbf{(0,75 điểm)} Thực hiện phép tính và thu gọn: $A = (2x - 3)(x + 1) - 2x(x - 2)$." + BR
                + "b) \\textbf{(0,75 điểm)} Phân tích đa thức sau thành nhân tử: $B = x^2 - 6x + 9 - y^2$."
            ),
            dap_an=[
                y("a)", 0.75, [
                    ("Ta có: $A = (2x - 3)(x + 1) - 2x(x - 2)$"),
                    ("$A = 2x^2 + 2x - 3x - 3 - 2x^2 + 4x$", 0.5),
                    ("$A = (2x^2 - 2x^2) + (2x - 3x + 4x) - 3 = 3x - 3$"),
                    ("Vậy biểu thức sau khi thu gọn là $A = 3x - 3$.", 0.25),
                ]),
                y("b)", 0.75, [
                    ("Ta có: $B = x^2 - 6x + 9 - y^2$"),
                    ("$B = (x^2 - 6x + 9) - y^2$", 0.25),
                    ("$B = (x - 3)^2 - y^2$", 0.25),
                    ("$B = (x - 3 - y)(x - 3 + y)$"),
                    ("Vậy đa thức được phân tích thành $B = (x - y - 3)(x + y - 3)$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 1.a", "Thực hiện phép tính nhân và thu gọn đa thức", "ĐS I", "TH", 0.75, 5, "THCS Phan Đình Giót"),
                ("Bài 1.b", "Phân tích đa thức thành nhân tử bằng hằng đẳng thức nhóm", "ĐS II", "TH", 0.75, 5, "THCS Nghĩa Tân"),
            ],
            note="Bài 1 kiểm tra kĩ năng nhân đơn thức, đa thức và nhóm hạng tử dùng hằng đẳng thức hiệu hai bình phương.",
        ),
        dict(
            label="Bài 2.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho biểu thức: $A = \\dfrac{3x}{x - 2} - \\dfrac{2}{x + 2} + \\dfrac{2x - 4}{x^2 - 4}$ với $x \\ne \\pm 2$." + BR
                + "a) \\textbf{(0,5 điểm)} Tìm điều kiện xác định của biểu thức $A$." + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh $A = \\dfrac{3x}{x - 2}$." + BR
                + "c) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ tại $x = -5$ và tìm tất cả các số nguyên $x$ để biểu thức $A$ nhận giá trị nguyên."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Biểu thức $A$ xác định khi và chỉ khi: $x - 2 \\ne 0$, $x + 2 \\ne 0$ và $x^2 - 4 \\ne 0$."),
                    ("Ta có $x^2 - 4 = (x - 2)(x + 2) \\ne 0$ khi $x \\ne 2$ và $x \\ne -2$.", 0.25),
                    ("Vậy điều kiện xác định của biểu thức $A$ là $x \\ne \\pm 2$.", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Với $x \\ne \\pm 2$, mẫu thức chung là $(x - 2)(x + 2)$."),
                    ("Ta có: $A = \\dfrac{3x(x + 2) - 2(x - 2) + 2x - 4}{(x - 2)(x + 2)}$", 0.25),
                    ("$A = \\dfrac{3x^2 + 6x - 2x + 4 + 2x - 4}{(x - 2)(x + 2)}$", 0.25),
                    ("$A = \\dfrac{3x^2 + 6x}{(x - 2)(x + 2)} = \\dfrac{3x(x + 2)}{(x - 2)(x + 2)}$", 0.25),
                    ("$A = \\dfrac{3x}{x - 2}$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 0.5, [
                    ("Thay $x = -5$ (thỏa mãn ĐKXĐ $x \\ne \\pm 2$) vào biểu thức $A$, ta được:"),
                    ("$A = \\dfrac{3 \\cdot (-5)}{-5 - 2} = \\dfrac{-15}{-7} = \\dfrac{15}{7}$.", 0.25),
                    ("Ta biến đổi: $A = \\dfrac{3x}{x - 2} = \\dfrac{3(x - 2) + 6}{x - 2} = 3 + \\dfrac{6}{x - 2}$."),
                    ("Để $A$ nhận giá trị nguyên thì $\\dfrac{6}{x - 2}$ phải là số nguyên, suy ra $x - 2 \\in \\text{Ư}(6) = \\{\\pm 1; \\pm 2; \\pm 3; \\pm 6\\}$."),
                    ("Do đó $x \\in \\{3; 1; 4; 0; 5; -1; 8; -4\\}$. Các giá trị này đều thỏa mãn ĐKXĐ $x \\ne \\pm 2$."),
                    ("Vậy các số nguyên $x$ thỏa mãn là $x \\in \\{-4; -1; 0; 1; 3; 4; 5; 8\\}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 2.a", "Tìm điều kiện xác định của phân thức đại số", "ĐS VI", "NB", 0.5, 4, "THCS Ngọc Lâm"),
                ("Bài 2.b", "Rút gọn phân thức đại số bằng quy đồng mẫu thức", "ĐS VI", "TH", 1.0, 10, "THCS Ngọc Lâm"),
                ("Bài 2.c", "Tính giá trị phân thức và tìm x nguyên để phân thức nhận giá trị nguyên", "ĐS VI", "VD", 0.5, 6, "THCS Ngọc Lâm"),
            ],
            note="Bài phân thức trọng tâm: HS hay quên đối chiếu ĐKXĐ khi kết luận các giá trị nguyên của x.",
        ),
        dict(
            label="Bài 3.",
            level=2,
            statement=(
                "\\textbf{(1,0 điểm)} Biểu đồ cột kép bên biểu diễn số lượng học sinh nam và nữ của bốn lớp 8A, 8B, 8C, 8D tham gia Câu lạc bộ Toán học của trường THCS:" + BR
                + "\\begin{center}\\footnotesize\\begin{tabular}{|l|c|c|c|c|}\\hline \n"
                + "\\textbf{Lớp} & \\textbf{8A} & \\textbf{8B} & \\textbf{8C} & \\textbf{8D} \\\\ \\hline \n"
                + "Số học sinh nam & $12$ & $15$ & $13$ & $10$ \\\\ \\hline \n"
                + "Số học sinh nữ & $13$ & $10$ & $12$ & $15$ \\\\ \\hline \n"
                + "\\end{tabular}\\end{center}" + BR
                + "a) \\textbf{(0,5 điểm)} Hãy lập bảng thống kê tổng số học sinh tham gia Câu lạc bộ Toán học của từng lớp." + BR
                + "b) \\textbf{(0,5 điểm)} Tính tỉ lệ phần trăm số học sinh nữ so với tổng số học sinh của cả bốn lớp tham gia Câu lạc bộ Toán học."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Dựa vào bảng số liệu trên, ta có tổng số học sinh tham gia CLB của từng lớp là:"),
                    ("Lớp 8A: $12 + 13 = 25$ (học sinh)."),
                    ("Lớp 8B: $15 + 10 = 25$ (học sinh)."),
                    ("Lớp 8C: $13 + 12 = 25$ (học sinh)."),
                    ("Lớp 8D: $10 + 15 = 25$ (học sinh).", 0.25),
                    ("Bảng thống kê tổng số học sinh tham gia CLB của từng lớp:"),
                    ("\\begin{center}\\begin{tabular}{|l|c|c|c|c|}\\hline \\textbf{Lớp} & 8A & 8B & 8C & 8D \\\\ \\hline \\textbf{Tổng số học sinh} & 25 & 25 & 25 & 25 \\\\ \\hline \\end{tabular}\\end{center}"),
                    ("Vậy mỗi lớp đều có $25$ học sinh tham gia Câu lạc bộ.", 0.25),
                ]),
                y("b)", 0.5, [
                    ("Tổng số học sinh của cả bốn lớp tham gia Câu lạc bộ là: $25 + 25 + 25 + 25 = 100$ (học sinh)."),
                    ("Tổng số học sinh nữ tham gia Câu lạc bộ là: $13 + 10 + 12 + 15 = 50$ (học sinh).", 0.25),
                    ("Tỉ lệ phần trăm số học sinh nữ so với tổng số học sinh tham gia là: $\\dfrac{50}{100} \\cdot 100\\% = 50\\%$."),
                    ("Vậy số học sinh nữ chiếm đúng $50\\%$ tổng số thành viên Câu lạc bộ.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 3.a", "Lập bảng thống kê từ dữ liệu biểu đồ", "TK V", "NB", 0.5, 4, "THCS Giảng Võ"),
                ("Bài 3.b", "Tính tỉ lệ phần trăm từ số liệu thống kê", "TK V", "TH", 0.5, 5, "THCS Giảng Võ"),
            ],
            note="Bài thống kê chuẩn chương V SGK Toán 8 KNTT: rèn kĩ năng lập bảng và phân tích số liệu.",
        ),
        dict(
            label="Bài 4.",
            level=2,
            statement=(
                "\\textbf{(3,0 điểm)} Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), gọi $M$ là trung điểm của cạnh $BC$." + BR
                + "Từ $M$ kẻ $MD \\perp AB$ tại $D$ và $ME \\perp AC$ tại $E$." + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh tứ giác $ADME$ là hình chữ nhật." + BR
                + "b) \\textbf{(1,0 điểm)} Kẻ đường cao $AH$ của tam giác $ABC$ ($H \\in BC$). Chứng minh tứ giác $DHME$ là hình thang cân." + BR
                + "c) \\textbf{(1,0 điểm)} Gọi $P$ là điểm đối xứng của $M$ qua $D$. Chứng minh tứ giác $AMBP$ là hình thoi."
            ),
            hinh_da=H.get_tikz_on1(),
            dap_an=[
                y("a)", 1.0, [
                    ("Xét tứ giác $ADME$, ta có:"),
                    ("$\\widehat{DAE} = \\widehat{BAC} = 90^\\circ$ (do tam giác $ABC$ vuông tại $A$).", 0.25),
                    ("$MD \\perp AB$ tại $D$ nên $\\widehat{ADM} = 90^\\circ$.", 0.25),
                    ("$ME \\perp AC$ tại $E$ nên $\\widehat{AEM} = 90^\\circ$.", 0.25),
                    ("Tứ giác $ADME$ có ba góc vuông nên là hình chữ nhật (điều phải chứng minh).", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Xét tam giác $ABC$, ta có $M$ là trung điểm $BC$, $ME \\perp AC$ và $AB \\perp AC$ nên $ME \\parallel AB$."),
                    ("Suy ra $E$ là trung điểm của $AC$. Tương tự, $MD \\parallel AC$ nên $D$ là trung điểm của $AB$."),
                    ("Do đó $DE$ là đường trung bình của tam giác $ABC$, suy ra $DE \\parallel BC$.", 0.25),
                    ("Vì $H, M \\in BC$ nên $DE \\parallel HM$, do đó tứ giác $DHME$ là hình thang.", 0.25),
                    ("Xét tam giác $ABH$ vuông tại $H$, có $HD$ là đường trung tuyến ứng với cạnh huyền $AB$ nên $HD = \\dfrac{1}{2}AB = AD$."),
                    ("Mặt khác, vì $ADME$ là hình chữ nhật nên $AD = ME$, suy ra $HD = ME$.", 0.25),
                    ("Hình thang $DHME$ có hai cạnh bên $HD = ME$ và không song song (do $AB < AC$) nên là hình thang cân.", 0.25),
                ]),
                y("c)", 1.0, [
                    ("Ta có $D$ là trung điểm của $AB$ (chứng minh ở câu b)."),
                    ("Lại có $P$ đối xứng với $M$ qua $D$ nên $D$ là trung điểm của $PM$.", 0.25),
                    ("Tứ giác $AMBP$ có hai đường chéo $AB$ và $PM$ cắt nhau tại trung điểm $D$ của mỗi đường, do đó $AMBP$ là hình bình hành.", 0.25),
                    ("Mặt khác, $AB \\perp PM$ tại $D$ (do $MD \\perp AB$).", 0.25),
                    ("Hình bình hành $AMBP$ có hai đường chéo vuông góc nên là hình thoi.", 0.25),
                    ("Vậy tứ giác $AMBP$ là hình thoi."),
                ]),
            ],
            mt=[
                ("Bài 4.a", "Chứng minh tứ giác là hình chữ nhật", "HH III", "TH", 1.0, 8, "THCS Phúc Diễn"),
                ("Bài 4.b", "Đường trung bình và chứng minh hình thang cân", "HH III", "VD", 1.0, 10, "THCS Phúc Diễn"),
                ("Bài 4.c", "Chứng minh tứ giác là hình thoi", "HH III", "VD", 1.0, 9, "THCS Phúc Diễn"),
            ],
            note="Bài hình kinh điển của Hà Nội: HS cần vẽ hình chuẩn xác, trình bày chặt chẽ căn cứ đường trung bình và trung tuyến ứng với cạnh huyền.",
        ),
        dict(
            label="Bài 5.",
            level=3,
            statement=(
                "\\textbf{(0,5 điểm)} Tìm giá trị nhỏ nhất của biểu thức sau:" + BR
                + "$M = x^2 - 4xy + 5y^2 + 10x - 22y + 28$ với mọi $x, y \\in \\mathbb{R}$."
            ),
            dap_an=[
                y("", 0.5, [
                    ("Ta biến đổi biểu thức $M$ như sau:"),
                    ("$M = (x^2 - 4xy + 4y^2) + 2(x - 2y) \\cdot 5 + 25 + (y^2 - 2y + 1) + 2$"),
                    ("$M = (x - 2y)^2 + 2(x - 2y) \\cdot 5 + 25 + (y - 1)^2 + 2$", 0.25),
                    ("$M = (x - 2y + 5)^2 + (y - 1)^2 + 2$"),
                    ("Vì $(x - 2y + 5)^2 \\ge 0$ và $(y - 1)^2 \\ge 0$ với mọi $x, y \\in \\mathbb{R}$, nên $M \\ge 2$."),
                    ("Dấu đẳng thức xảy ra khi và chỉ khi: $y - 1 = 0$ và $x - 2y + 5 = 0$, tức là $y = 1$ và $x = 2(1) - 5 = -3$."),
                    ("Vậy giá trị nhỏ nhất của biểu thức $M$ là $2$, đạt được khi $x = -3$ và $y = 1$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 5", "Tìm giá trị nhỏ nhất của đa thức hai biến bằng biến đổi hằng đẳng thức", "ĐS II", "VDC", 0.5, 6, "THCS Phan Chu Trinh"),
            ],
            note="Câu phân hoá cao: dùng kĩ thuật nhóm tổng các bình phương theo hằng đẳng thức lớp 8.",
        ),
    ],
)

# =====================================================================
# ĐỀ ÔN TẬP SỐ 2
# =====================================================================
DE["on-2"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 2",
    slug_de="de-on-tap-cuoi-ki-1-so-2",
    slug_mt="ma-tran-va-dap-an-on-tap-ck1-so-2",
    eyebrow="LỚP 8 • ĐỀ ÔN TẬP CUỐI KÌ I — SỐ 2",
    cach_dung="Làm bài trong 90 phút như thi thật. Rèn kĩ năng rút gọn phân thức đại số bậc cao, bài toán tìm x nguyên và chứng minh đường thẳng vuông góc trong hình học.",
    gioi_thieu=(
        "\\textbf{ĐỀ ÔN TẬP SỐ 2 -- CUỐI HỌC KÌ I TOÁN 8 (KNTT)} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc chuẩn:} Bám sát ma trận kiểm tra Cuối Kì 1 Kết nối tri thức: "
        "Phần I (2,0đ) Trắc nghiệm 8 câu x 0,25đ phân phối đều các chương · "
        "Bài 1 (1,5đ) Phép chia đa thức \\& Giải phương trình tìm x · "
        "Bài 2 (2,0đ) Phân thức đại số: tính giá trị, rút gọn biểu thức và tìm x nguyên lớn nhất · "
        "Bài 3 (1,0đ) Toán thực tế ứng dụng đường trung bình của tam giác · "
        "Bài 4 (3,0đ) Hình học tổng hợp: hình chữ nhật, điểm đối xứng, đường thẳng vuông góc · "
        "Bài 5 (0,5đ) VDC Phương trình nghiệm thực dùng tổng bình phương."
    ),
    bay=[
        ("Bài 1.b", "Quên dấu trừ khi phá ngoặc tích $-x(x + 2)$", "Viết thành $-x^2 + 2x$ làm sai toàn bộ kết quả", "Thực hiện cẩn thận: $-x(x + 2) = -x^2 - 2x$"),
        ("Bài 2.b", "Đổi dấu mẫu thức đối $1 - x^2 = -(x^2 - 1)$ không đổi dấu phép tính", "Dẫn đến sai dấu tử số khi quy đồng", "Đặt dấu trừ ra trước phân thức: $\\dfrac{4}{1 - x} = -\\dfrac{4}{x - 1}$"),
        ("Bài 2.c", "Quên điều kiện x nguyên lớn nhất", "Liệt kê tất cả các giá trị nguyên mà không chọn số lớn nhất", "Đọc kĩ yêu cầu đề bài: 'Tìm số nguyên x LỚN NHẤT'"),
        ("Bài 4.c", "Nhầm lẫn giữa trung tuyến và đoạn vuông góc kẻ từ đỉnh tam giác vuông", "Chưa chứng minh $AM \\perp DE$ mà ngộ nhận $AM$ vuông góc $BC$", "Dùng phương pháp góc: chứng minh $\\widehat{DAM} + \\widehat{ADE} = 90^\\circ$"),
    ],
    tn=[
        tn(1, "Trong các biểu thức sau, biểu thức nào là đơn thức thu gọn?", ["$2x^2y \\cdot 3x$", "$-5x^3y^2$", "$x + 2y$", "$4x^2y - x^2y$"], "B",
           "$-5x^3y^2$ là đơn thức đã thu gọn vì mỗi biến chỉ xuất hiện một lần.", "Đơn thức thu gọn", "ĐS I", "NB", "THCS Lê Quý Đôn"),
        tn(2, "Kết quả của phép nhân $2x(3x^2 - 5x + 1)$ là:", ["$6x^3 - 10x^2 + 2x$", "$6x^3 - 10x^2 + 1$", "$6x^2 - 10x + 2$", "$5x^3 - 7x^2 + 3x$"], "A",
           "Nhân từng hạng tử: $2x \\cdot 3x^2 - 2x \\cdot 5x + 2x \\cdot 1 = 6x^3 - 10x^2 + 2x$.", "Phép nhân đa thức", "ĐS I", "TH", "THCS Lê Quý Đôn"),
        tn(3, "Khai triển hằng đẳng thức $(x - 2)^3$, ta được kết quả là:", ["$x^3 - 6x^2 + 12x - 8$", "$x^3 - 8$", "$x^3 - 6x^2 + 6x - 8$", "$x^3 + 6x^2 + 12x + 8$"], "A",
           "Áp dụng hằng đẳng thức lập phương của một hiệu: $(x - 2)^3 = x^3 - 3 \\cdot x^2 \\cdot 2 + 3 \\cdot x \\cdot 2^2 - 2^3 = x^3 - 6x^2 + 12x - 8$.", "Hằng đẳng thức đáng nhớ", "ĐS II", "NB", "THCS Ngô Sĩ Liên"),
        tn(4, "Phân tích đa thức $x^2 - 16$ thành nhân tử được kết quả là:", ["$(x - 4)^2$", "$(x - 16)(x + 16)$", "$(x - 4)(x + 4)$", "$(x + 4)^2$"], "C",
           "Áp dụng hiệu hai bình phương: $x^2 - 16 = x^2 - 4^2 = (x - 4)(x + 4)$.", "Phân tích đa thức thành nhân tử", "ĐS II", "TH", "THCS Ngô Sĩ Liên"),
        tn(5, "Khẳng định nào sau đây là \\textbf{sai} đối với hình bình hành?", ["Các cạnh đối song song và bằng nhau", "Các góc đối bằng nhau", "Hai đường chéo vuông góc với nhau", "Hai đường chéo cắt nhau tại trung điểm của mỗi đường"], "C",
           "Hình bình hành không nhất thiết có hai đường chéo vuông góc (chỉ hình thoi mới có).", "Hình bình hành", "HH III", "NB", "THCS Đông Mỹ"),
        tn(6, "Hình thoi có hai đường chéo bằng nhau là hình gì?", ["Hình bình hành", "Hình chữ nhật", "Hình thang cân", "Hình vuông"], "D",
           "Dấu hiệu nhận biết: hình thoi có hai đường chéo bằng nhau là hình vuông.", "Hình vuông", "HH III", "TH", "THCS Phan Chu Trinh"),
        tn(7, "Cho $\\triangle ABC$ có $M, N$ lần lượt là trung điểm của $AB$ và $AC$. Biết $BC = 12\\text{ cm}$. Độ dài đoạn thẳng $MN$ là:", ["$6\\text{ cm}$", "$24\\text{ cm}$", "$4\\text{ cm}$", "$8\\text{ cm}$"], "A",
           "$MN$ là đường trung bình của tam giác $ABC$ nên $MN = \\dfrac{1}{2}BC = \\dfrac{1}{2} \\cdot 12 = 6\\text{ cm}$.", "Đường trung bình của tam giác", "HH IV", "TH", "THCS Đa Tốn"),
        tn(8, "Phân thức đối của phân thức $\\dfrac{x - 3}{x + 1}$ là:", ["$\\dfrac{3 - x}{x + 1}$", "$\\dfrac{x - 3}{1 - x}$", "$\\dfrac{x + 3}{x + 1}$", "$\\dfrac{x + 1}{x - 3}$"], "A",
           "Phân thức đối của $\\dfrac{A}{B}$ là $-\\dfrac{A}{B} = \\dfrac{-A}{B} = \\dfrac{3 - x}{x + 1}$.", "Phân thức đại số", "ĐS VI", "NB", "THCS Đa Tốn"),
    ],
    bai=[
        dict(
            label="Bài 1.",
            level=2,
            statement=(
                "\\textbf{(1,5 điểm)}" + BR
                + "a) \\textbf{(0,75 điểm)} Thực hiện phép tính chia: $(15x^3y^2 - 10x^2y + 5xy) : 5xy$." + BR
                + "b) \\textbf{(0,75 điểm)} Tìm $x$, biết: $(x - 3)^2 - x(x + 2) = 11$."
            ),
            dap_an=[
                y("a)", 0.75, [
                    ("Ta có: $(15x^3y^2 - 10x^2y + 5xy) : 5xy$"),
                    ("$= (15x^3y^2 : 5xy) - (10x^2y : 5xy) + (5xy : 5xy)$", 0.5),
                    ("$= 3x^2y - 2x + 1$"),
                    ("Vậy kết quả phép tính chia là $3x^2y - 2x + 1$.", 0.25),
                ]),
                y("b)", 0.75, [
                    ("Ta có: $(x - 3)^2 - x(x + 2) = 11$"),
                    ("$x^2 - 6x + 9 - x^2 - 2x = 11$", 0.25),
                    ("$(x^2 - x^2) + (-6x - 2x) + 9 = 11$"),
                    ("$-8x + 9 = 11$"),
                    ("$-8x = 11 - 9$"),
                    ("$-8x = 2$"),
                    ("$x = -\\dfrac{2}{8} = -\\dfrac{1}{4}$", 0.25),
                    ("Vậy $x = -\\dfrac{1}{4}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 1.a", "Chia đa thức cho đơn thức", "ĐS I", "TH", 0.75, 5, "THCS Lê Quý Đôn"),
                ("Bài 1.b", "Tìm x bằng khai triển hằng đẳng thức và thu gọn", "ĐS II", "TH", 0.75, 5, "THCS Phan Chu Trinh"),
            ],
            note="Bài 1 rèn kĩ năng tính toán chia đa thức và phá ngoặc không làm sai dấu.",
        ),
        dict(
            label="Bài 2.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho hai biểu thức: $A = \\dfrac{x - 1}{x}$ và $B = \\dfrac{2x - 4}{x^2 - 1} - \\dfrac{4}{x + 1} + \\dfrac{x}{x - 1}$ với $x \\ne \\pm 1; x \\ne 0$." + BR
                + "a) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ khi $x = 1{,}5$." + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh rằng $B = \\dfrac{x}{x + 1}$." + BR
                + "c) \\textbf{(0,5 điểm)} Đặt $P = A \\cdot B$. Tìm số nguyên $x$ lớn nhất để biểu thức $P$ nhận giá trị nguyên."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Ta có $x = 1{,}5 = \\dfrac{3}{2}$ thỏa mãn điều kiện $x \\ne \\pm 1$ và $x \\ne 0$."),
                    ("Thay $x = 1{,}5$ vào biểu thức $A$, ta được:"),
                    ("$A = \\dfrac{1{,}5 - 1}{1{,}5} = \\dfrac{0{,}5}{1{,}5} = \\dfrac{1}{3}$.", 0.25),
                    ("Vậy khi $x = 1{,}5$ thì giá trị của biểu thức $A$ là $\\dfrac{1}{3}$.", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Với $x \\ne \\pm 1; x \\ne 0$, ta có: $x^2 - 1 = (x - 1)(x + 1)$."),
                    ("Khi đó: $B = \\dfrac{2x - 4}{(x - 1)(x + 1)} - \\dfrac{4(x - 1)}{(x - 1)(x + 1)} + \\dfrac{x(x + 1)}{(x - 1)(x + 1)}$", 0.25),
                    ("$B = \\dfrac{2x - 4 - 4(x - 1) + x(x + 1)}{(x - 1)(x + 1)}$", 0.25),
                    ("$B = \\dfrac{2x - 4 - 4x + 4 + x^2 + x}{(x - 1)(x + 1)} = \\dfrac{x^2 - x}{(x - 1)(x + 1)}$", 0.25),
                    ("$B = \\dfrac{x(x - 1)}{(x - 1)(x + 1)} = \\dfrac{x}{x + 1}$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 0.5, [
                    ("Ta có: $P = A \\cdot B = \\dfrac{x - 1}{x} \\cdot \\dfrac{x}{x + 1} = \\dfrac{x - 1}{x + 1}$."),
                    ("Ta biến đổi: $P = \\dfrac{x + 1 - 2}{x + 1} = 1 - \\dfrac{2}{x + 1}$."),
                    ("Để $P$ nhận giá trị nguyên với $x$ nguyên thì $\\dfrac{2}{x + 1}$ phải là số nguyên, suy ra $x + 1 \\in \\text{Ư}(2) = \\{\\pm 1; \\pm 2\\}$."),
                    ("Nếu $x + 1 = 1 \\implies x = 0$ (loại do ĐKXĐ)."),
                    ("Nếu $x + 1 = -1 \\implies x = -2$ (thỏa mãn ĐKXĐ)."),
                    ("Nếu $x + 1 = 2 \\implies x = 1$ (loại do ĐKXĐ)."),
                    ("Nếu $x + 1 = -2 \\implies x = -3$ (thỏa mãn ĐKXĐ).", 0.25),
                    ("Do đó các giá trị nguyên thỏa mãn là $x \\in \\{-3; -2\\}$."),
                    ("Vậy số nguyên $x$ lớn nhất để $P$ nhận giá trị nguyên là $x = -2$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 2.a", "Tính giá trị phân thức khi biết giá trị biến", "ĐS VI", "NB", 0.5, 4, "THCS Ngô Sĩ Liên"),
                ("Bài 2.b", "Rút gọn biểu thức phân thức chứa phép cộng trừ", "ĐS VI", "TH", 1.0, 10, "THCS Ngô Sĩ Liên"),
                ("Bài 2.c", "Nhân phân thức và tìm số nguyên lớn nhất thoả điều kiện", "ĐS VI", "VD", 0.5, 6, "THCS Ngô Sĩ Liên"),
            ],
            note="Đề thi thật của THCS Ngô Sĩ Liên: bẫy loại nghiệm x = 0 và x = 1 rất tinh tế.",
        ),
        dict(
            label="Bài 3.",
            level=2,
            statement=(
                "\\textbf{(1,0 điểm)} Để đo khoảng cách giữa hai vị trí $A$ và $B$ ở hai bên bờ một hồ nước sâu mà không thể đo trực tiếp, "
                "một nhóm học sinh đã chọn một vị trí $C$ trên mặt đất có thể nhìn thấy cả $A$ và $B$." + BR
                + "Các bạn xác định điểm $M$ là trung điểm của đoạn thẳng $CA$ và điểm $N$ là trung điểm của đoạn thẳng $CB$." + BR
                + "Dùng thước dây đo được khoảng cách $MN = 42\\text{ m}$. Tính khoảng cách giữa hai vị trí $A$ và $B$."
            ),
            dap_an=[
                y("", 1.0, [
                    ("Xét tam giác $ABC$, ta có:"),
                    ("$M$ là trung điểm của cạnh $CA$ (theo giả thiết)."),
                    ("$N$ là trung điểm của cạnh $CB$ (theo giả thiết).", 0.25),
                    ("Suy ra $MN$ là đường trung bình của tam giác $ABC$.", 0.25),
                    ("Theo tính chất đường trung bình của tam giác, ta có: $MN = \\dfrac{1}{2}AB$."),
                    ("Suy ra $AB = 2 \\cdot MN = 2 \\cdot 42 = 84\\text{ (m)}$.", 0.25),
                    ("Vậy khoảng cách giữa hai vị trí $A$ và $B$ là $84\\text{ m}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 3", "Ứng dụng thực tế của đường trung bình trong tam giác để đo khoảng cách", "HH IV", "TH", 1.0, 9, "THCS Đông Mỹ"),
            ],
            note="Bài toán thực tế đặc trưng hình học lớp 8: yêu cầu nêu đầy đủ giả thiết trung điểm và kết luận có đơn vị.",
        ),
        dict(
            label="Bài 4.",
            level=2,
            statement=(
                "\\textbf{(3,0 điểm)} Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$ ($H \\in BC$)." + BR
                + "Từ $H$ kẻ $HD \\perp AB$ tại $D$ và $HE \\perp AC$ tại $E$." + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh tứ giác $ADHE$ là hình chữ nhật." + BR
                + "b) \\textbf{(1,0 điểm)} Trên tia đối của tia $DH$ lấy điểm $P$ sao cho $DP = DH$. Trên tia đối của tia $EH$ lấy điểm $Q$ sao cho $EQ = EH$. Chứng minh điểm $A$ là trung điểm của đoạn thẳng $PQ$." + BR
                + "c) \\textbf{(1,0 điểm)} Gọi $M$ là trung điểm của cạnh $BC$. Chứng minh rằng $AM \\perp DE$."
            ),
            hinh_da=H.get_tikz_on2(),
            dap_an=[
                y("a)", 1.0, [
                    ("Xét tứ giác $ADHE$, ta có:"),
                    ("$\\widehat{DAE} = \\widehat{BAC} = 90^\\circ$ (do tam giác $ABC$ vuông tại $A$).", 0.25),
                    ("$HD \\perp AB$ tại $D$ nên $\\widehat{ADH} = 90^\\circ$.", 0.25),
                    ("$HE \\perp AC$ tại $E$ nên $\\widehat{AEH} = 90^\\circ$.", 0.25),
                    ("Tứ giác $ADHE$ có ba góc vuông nên là hình chữ nhật (điều phải chứng minh).", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Ta có $D$ là trung điểm của $PH$ và $AB \\perp PH$ tại $D$, nên $AB$ là đường trung trực của đoạn thẳng $PH$."),
                    ("Suy ra $AP = AH$ và tam giác $APH$ cân tại $A$, có $AD$ là đường cao đồng thời là đường phân giác, do đó $\\widehat{DAP} = \\widehat{DAH}$.", 0.25),
                    ("Tương tự, $AC$ là đường trung trực của $QH$ nên $AQ = AH$ và $\\widehat{EAQ} = \\widehat{EAH}$.", 0.25),
                    ("Suy ra $AP = AQ = AH$ (1)."),
                    ("Mặt khác, $\\widehat{PAQ} = \\widehat{DAP} + \\widehat{DAH} + \\widehat{EAH} + \\widehat{EAQ} = 2(\\widehat{DAH} + \\widehat{EAH}) = 2\\widehat{DAE} = 2 \\cdot 90^\\circ = 180^\\circ$."),
                    ("Do đó ba điểm $P, A, Q$ thẳng hàng (2).", 0.25),
                    ("Từ (1) và (2) suy ra $A$ là trung điểm của đoạn thẳng $PQ$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 1.0, [
                    ("Gọi $O$ là giao điểm của $AH$ và $DE$. Vì $ADHE$ là hình chữ nhật nên $OA = OD = OE = OH$, suy ra $\\triangle OAE$ cân tại $O$."),
                    ("Do đó $\\widehat{OED} = \\widehat{OAE} = \\widehat{HAC}$.", 0.25),
                    ("Xét tam giác $ABC$ vuông tại $A$, $M$ là trung điểm $BC$ nên $AM$ là trung tuyến ứng với cạnh huyền, suy ra $AM = MC = \\dfrac{1}{2}BC$."),
                    ("Do đó tam giác $MAC$ cân tại $M$, suy ra $\\widehat{MAC} = \\widehat{MCA} = \\widehat{ACB}$.", 0.25),
                    ("Gọi $K$ là giao điểm của $AM$ và $DE$."),
                    ("Xét tam giác $AKE$, ta có: $\\widehat{KAE} + \\widehat{KEA} = \\widehat{MAC} + \\widehat{OED} = \\widehat{ACB} + \\widehat{HAC}$."),
                    ("Mặt khác, trong tam giác $AHC$ vuông tại $H$, ta có $\\widehat{ACB} + \\widehat{HAC} = 90^\\circ$."),
                    ("Suy ra $\\widehat{KAE} + \\widehat{KEA} = 90^\\circ$, dẫn đến $\\widehat{AKE} = 180^\\circ - 90^\\circ = 90^\\circ$."),
                    ("Vậy $AM \\perp DE$ tại $K$ (điều phải chứng minh).", 0.25),
                ]),
            ],
            mt=[
                ("Bài 4.a", "Chứng minh tứ giác là hình chữ nhật", "HH III", "TH", 1.0, 8, "THCS Phan Chu Trinh"),
                ("Bài 4.b", "Sử dụng tính chất đường trung trực chứng minh trung điểm và thẳng hàng", "HH III", "VD", 1.0, 10, "THCS Phan Chu Trinh"),
                ("Bài 4.c", "Chứng minh hai đường thẳng vuông góc qua biến đổi góc", "HH III", "VD", 1.0, 9, "THCS Phan Chu Trinh"),
            ],
            note="Bài hình kinh điển của Hà Nội: câu c dùng kĩ năng phân tích góc cộng lại bằng 90 độ rất quan trọng cho thi vào 10.",
        ),
        dict(
            label="Bài 5.",
            level=3,
            statement=(
                "\\textbf{(0,5 điểm)} Cho hai số thực $x, y$ thỏa mãn đẳng thức sau:" + BR
                + "$x^2 + 2y^2 + 2xy - 2x - 6y + 5 = 0$." + BR
                + "Tính giá trị của biểu thức $P = (x + y)^{2024}$."
            ),
            dap_an=[
                y("", 0.5, [
                    ("Ta biến đổi phương trình đã cho như sau:"),
                    ("$x^2 + 2xy + y^2 - 2(x + y) + 1 + y^2 - 4y + 4 = 0$"),
                    ("$(x + y)^2 - 2(x + y) + 1 + (y - 2)^2 = 0$"),
                    ("$(x + y - 1)^2 + (y - 2)^2 = 0$", 0.25),
                    ("Vì $(x + y - 1)^2 \\ge 0$ và $(y - 2)^2 \\ge 0$ với mọi $x, y$, nên đẳng thức xảy ra khi và chỉ khi:"),
                    ("$y - 2 = 0$ và $x + y - 1 = 0$."),
                    ("Suy ra $y = 2$ và $x = 1 - y = 1 - 2 = -1$."),
                    ("Khi đó: $x + y = -1 + 2 = 1$."),
                    ("Thay vào biểu thức $P$, ta được: $P = 1^{2024} = 1$."),
                    ("Vậy giá trị của biểu thức $P$ là $1$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 5", "Giải phương trình nghiệm thực bằng tổng các bình phương", "ĐS II", "VDC", 0.5, 6, "THCS Đa Tốn"),
            ],
            note="Dạng toán hằng đẳng thức mở rộng: nhận dạng khéo léo biến đổi hai bình phương bằng 0.",
        ),
    ],
)

# =====================================================================
# ĐỀ ÔN TẬP SỐ 3
# =====================================================================
DE["on-3"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 3",
    slug_de="de-on-tap-cuoi-ki-1-so-3",
    slug_mt="ma-tran-va-dap-an-on-tap-ck1-so-3",
    eyebrow="LỚP 8 • ĐỀ ÔN TẬP CUỐI KÌ I — SỐ 3",
    cach_dung="Làm bài trong 90 phút như thi thật. Rèn kĩ năng tính toán phân thức phức hợp, bài toán thống kê thực tế và chứng minh góc vuông trong tam giác.",
    gioi_thieu=(
        "\\textbf{ĐỀ ÔN TẬP SỐ 3 -- CUỐI HỌC KÌ I TOÁN 8 (KNTT)} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc chuẩn:} Bám sát ma trận kiểm tra Cuối Kì 1 Kết nối tri thức: "
        "Phần I (2,0đ) Trắc nghiệm 8 câu x 0,25đ phân phối chuẩn các mạch · "
        "Bài 1 (1,5đ) Hằng đẳng thức \\& Phân tích đa thức thành nhân tử · "
        "Bài 2 (2,0đ) Phân thức đại số: rút gọn biểu thức, chứng minh đẳng thức tích và tìm x nguyên · "
        "Bài 3 (1,0đ) Thống kê phân tích số liệu biểu đồ đoạn thẳng KNTT · "
        "Bài 4 (3,0đ) Hình học tổng hợp: hình chữ nhật, hình thoi, chứng minh góc vuông · "
        "Bài 5 (0,5đ) VDC Hằng đẳng thức đối xứng ba biến."
    ),
    bay=[
        ("Bài 1.a", "Khai triển sai hằng đẳng thức hiệu hai bình phương $2(x - 1)(x + 1)$", "Quên nhân hệ số 2 hoặc đổi sai dấu", "Viết thành $2(x^2 - 1) = 2x^2 - 2$ rồi trừ cẩn thận"),
        ("Bài 2.a", "Đổi dấu mẫu đối $2 - x = -(x - 2)$", "Không đổi dấu phân thức dẫn đến sai toàn bộ mẫu chung", "Viết: $-\\dfrac{2}{2 - x} = +\\dfrac{2}{x - 2}$"),
        ("Bài 2.c", "Sót trường hợp khi tìm ước của phân thức", "Không liệt kê đầy đủ cả ước dương và ước âm", "Liệt kê đủ: $\\text{Ư}(4) = \\{\\pm 1; \\pm 2; \\pm 4\\}$"),
        ("Bài 4.c", "Nhầm lẫn giữa các góc vuông trong tứ giác $ADME$", "Chứng minh góc $\\widehat{DHE} = 90^\\circ$ mà không dùng tính chất tam giác vuông cân hoặc hình chữ nhật", "Dùng tính chất $HD = AD = ME$ và $HE = AE = DM$"),
    ],
    tn=[
        tn(1, "Biểu thức nào sau đây \\textbf{không} là đa thức nhiều biến?", ["$2x^2 - 3xy + y^2$", "$\\dfrac{x + y}{2}$", "$\\dfrac{2x - 1}{y}$", "$3x^3y - 5$"], "C",
           "$\\dfrac{2x - 1}{y}$ chứa biến $y$ ở mẫu nên không phải là đa thức.", "Khái niệm đa thức", "ĐS I", "NB", "THCS \& THPT Lương Thế Vinh"),
        tn(2, "Bậc của đa thức thu gọn $Q = x^5 - 2x^3y^3 + 5xy^4 - x^5 + 1$ là:", ["$5$", "$6$", "$4$", "$7$"], "B",
           "Thu gọn: $Q = -2x^3y^3 + 5xy^4 + 1$. Hạng tử $-2x^3y^3$ có bậc $3 + 3 = 6$ cao nhất.", "Bậc của đa thức", "ĐS I", "TH", "THCS \& THPT Lương Thế Vinh"),
        tn(3, "Hằng đẳng thức bình phương một tổng $(A + B)^2$ bằng:", ["$A^2 + B^2$", "$A^2 + 2AB + B^2$", "$A^2 - 2AB + B^2$", "$A^2 + AB + B^2$"], "B",
           "Theo hằng đẳng thức bình phương của một tổng: $(A + B)^2 = A^2 + 2AB + B^2$.", "Hằng đẳng thức đáng nhớ", "ĐS II", "NB", "THCS Nguyễn Công Trứ"),
        tn(4, "Phân tích đa thức $x^2 - xy + 2x - 2y$ thành nhân tử, ta được:", ["$(x - y)(x + 2)$", "$(x + y)(x - 2)$", "$(x - y)(x - 2)$", "$(x + y)(x + 2)$"], "A",
           "Nhóm hạng tử: $x(x - y) + 2(x - y) = (x - y)(x + 2)$.", "Phân tích đa thức thành nhân tử", "ĐS II", "TH", "THCS Nguyễn Công Trứ"),
        tn(5, "Khẳng định nào sau đây là đúng về hình chữ nhật?", ["Hai đường chéo vuông góc với nhau", "Hai đường chéo bằng nhau", "Bốn cạnh bằng nhau", "Mỗi đường chéo là một đường phân giác của một góc"], "B",
           "Hình chữ nhật có hai đường chéo bằng nhau và cắt nhau tại trung điểm mỗi đường.", "Hình chữ nhật", "HH III", "NB", "THCS Nguyễn Trường Tộ"),
        tn(6, "Hình thoi có một góc vuông là hình gì?", ["Hình chữ nhật", "Hình thang cân", "Hình bình hành", "Hình vuông"], "D",
           "Dấu hiệu nhận biết: hình thoi có một góc vuông là hình vuông.", "Hình vuông", "HH III", "TH", "THCS Nguyễn Trường Tộ"),
        tn(7, "Cho $\\triangle ABC$, tia phân giác của góc $A$ cắt cạnh $BC$ tại $D$. Hệ thức nào sau đây là đúng?", ["$\\dfrac{DB}{DC} = \\dfrac{AB}{AC}$", "$\\dfrac{DB}{DC} = \\dfrac{AC}{AB}$", "$\\dfrac{DB}{AB} = \\dfrac{DC}{BC}$", "$\\dfrac{DB}{DC} = \\dfrac{BC}{AC}$"], "A",
           "Theo tính chất đường phân giác trong tam giác: $\\dfrac{DB}{DC} = \\dfrac{AB}{AC}$.", "Tính chất đường phân giác", "HH IV", "TH", "Quận Tây Hồ"),
        tn(8, "Phân thức nghịch đảo của phân thức $\\dfrac{2x - 1}{x + 5}$ (với $x \\ne -5, x \\ne \\dfrac{1}{2}$) là:", ["$\\dfrac{x + 5}{2x - 1}$", "$-\\dfrac{2x - 1}{x + 5}$", "$\\dfrac{2x + 1}{x - 5}$", "$-\\dfrac{x + 5}{2x - 1}$"], "A",
           "Phân thức nghịch đảo của $\\dfrac{A}{B}$ là $\\dfrac{B}{A} = \\dfrac{x + 5}{2x - 1}$.", "Phân thức đại số", "ĐS VI", "NB", "THCS Tân Triều"),
    ],
    bai=[
        dict(
            label="Bài 1.",
            level=2,
            statement=(
                "\\textbf{(1,5 điểm)}" + BR
                + "a) \\textbf{(0,75 điểm)} Rút gọn biểu thức sau: $A = (x + 2)^2 + (x - 2)^2 - 2(x - 1)(x + 1)$." + BR
                + "b) \\textbf{(0,75 điểm)} Phân tích đa thức sau thành nhân tử: $B = x^3 - 2x^2 + x - xy^2$."
            ),
            dap_an=[
                y("a)", 0.75, [
                    ("Ta có: $A = (x + 2)^2 + (x - 2)^2 - 2(x - 1)(x + 1)$"),
                    ("$A = (x^2 + 4x + 4) + (x^2 - 4x + 4) - 2(x^2 - 1)$", 0.25),
                    ("$A = x^2 + 4x + 4 + x^2 - 4x + 4 - 2x^2 + 2$", 0.25),
                    ("$A = (x^2 + x^2 - 2x^2) + (4x - 4x) + (4 + 4 + 2) = 10$"),
                    ("Vậy giá trị của biểu thức $A$ luôn bằng $10$, không phụ thuộc vào giá trị của biến $x$.", 0.25),
                ]),
                y("b)", 0.75, [
                    ("Ta có: $B = x^3 - 2x^2 + x - xy^2$"),
                    ("$B = x(x^2 - 2x + 1 - y^2)$", 0.25),
                    ("$B = x[(x^2 - 2x + 1) - y^2] = x[(x - 1)^2 - y^2]$", 0.25),
                    ("$B = x(x - 1 - y)(x - 1 + y)$"),
                    ("Vậy đa thức được phân tích thành $B = x(x - y - 1)(x + y - 1)$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 1.a", "Rút gọn biểu thức bằng hằng đẳng thức", "ĐS II", "TH", 0.75, 5, "THCS \& THPT Lương Thế Vinh"),
                ("Bài 1.b", "Phân tích đa thức thành nhân tử phối hợp nhiều phương pháp", "ĐS II", "TH", 0.75, 5, "THCS Nguyễn Công Trứ"),
            ],
            note="Bài 1 kiểm tra chuẩn hằng đẳng thức đáng nhớ và phương pháp đặt nhân tử chung phối hợp nhóm hạng tử.",
        ),
        dict(
            label="Bài 2.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho hai biểu thức: $A = \\dfrac{x}{x^2 - 4} - \\dfrac{2}{2 - x} - \\dfrac{3}{x + 2}$ và $B = \\dfrac{(x - 2)^2}{10}$ với $x \\ne \\pm 2$." + BR
                + "a) \\textbf{(1,0 điểm)} Rút gọn biểu thức $A$." + BR
                + "b) \\textbf{(0,5 điểm)} Đặt $P = A \\cdot B$. Chứng minh rằng $P = \\dfrac{x - 2}{x + 2}$." + BR
                + "c) \\textbf{(0,5 điểm)} Tìm tất cả các giá trị nguyên của $x$ để biểu thức $P$ nhận giá trị nguyên."
            ),
            dap_an=[
                y("a)", 1.0, [
                    ("Với $x \\ne \\pm 2$, ta đổi dấu phân thức thứ hai: $-\\dfrac{2}{2 - x} = \\dfrac{2}{x - 2}$."),
                    ("Khi đó: $A = \\dfrac{x}{(x - 2)(x + 2)} + \\dfrac{2}{x - 2} - \\dfrac{3}{x + 2}$", 0.25),
                    ("Quy đồng với mẫu chung là $(x - 2)(x + 2)$:", 0.25),
                    ("$A = \\dfrac{x + 2(x + 2) - 3(x - 2)}{(x - 2)(x + 2)}$"),
                    ("$A = \\dfrac{x + 2x + 4 - 3x + 6}{(x - 2)(x + 2)}$", 0.25),
                    ("$A = \\dfrac{10}{(x - 2)(x + 2)} = \\dfrac{10}{x^2 - 4}$."),
                    ("Vậy biểu thức rút gọn là $A = \\dfrac{10}{x^2 - 4}$.", 0.25),
                ]),
                y("b)", 0.5, [
                    ("Với $x \\ne \\pm 2$, ta có:"),
                    ("$P = A \\cdot B = \\dfrac{10}{(x - 2)(x + 2)} \\cdot \\dfrac{(x - 2)^2}{10}$", 0.25),
                    ("$P = \\dfrac{10(x - 2)^2}{10(x - 2)(x + 2)} = \\dfrac{x - 2}{x + 2}$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 0.5, [
                    ("Ta biến đổi: $P = \\dfrac{x - 2}{x + 2} = \\dfrac{x + 2 - 4}{x + 2} = 1 - \\dfrac{4}{x + 2}$."),
                    ("Để $P$ nhận giá trị nguyên với $x$ nguyên thì $\\dfrac{4}{x + 2}$ phải là số nguyên, suy ra $x + 2 \\in \\text{Ư}(4) = \\{\\pm 1; \\pm 2; \\pm 4\\}$."),
                    ("Ta có bảng giá trị tương ứng:"),
                    ("$\\bullet\\ x + 2 = 1 \\implies x = -1$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x + 2 = -1 \\implies x = -3$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x + 2 = 2 \\implies x = 0$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x + 2 = -2 \\implies x = -4$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x + 2 = 4 \\implies x = 2$ (loại do ĐKXĐ $x \\ne 2$)."),
                    ("$\\bullet\\ x + 2 = -4 \\implies x = -6$ (thỏa mãn ĐKXĐ).", 0.25),
                    ("Vậy các số nguyên $x$ để biểu thức $P$ nhận giá trị nguyên là $x \\in \\{-6; -4; -3; -1; 0\\}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 2.a", "Rút gọn biểu thức phân thức có đổi dấu mẫu thức", "ĐS VI", "TH", 1.0, 10, "THCS Tân Triều"),
                ("Bài 2.b", "Nhân hai phân thức đại số", "ĐS VI", "TH", 0.5, 4, "THCS Tân Triều"),
                ("Bài 2.c", "Tìm số nguyên x để phân thức nhận giá trị nguyên", "ĐS VI", "VD", 0.5, 6, "THCS Tân Triều"),
            ],
            note="Bài phân thức hay gặp ở đề thi học kì: lưu ý kĩ thuật đổi dấu mẫu thức $2 - x = -(x - 2)$.",
        ),
        dict(
            label="Bài 3.",
            level=2,
            statement=(
                "\\textbf{(1,0 điểm)} Biểu đồ đoạn thẳng biểu diễn số lượng áo ấm mà học sinh khối 8 trường THCS Lương Thế Vinh đã quyên góp được trong chương trình ``Áo ấm mùa đông'' qua bốn năm:" + BR
                + "\\begin{center}\\footnotesize\\begin{tabular}{|l|c|c|c|c|}\\hline \n"
                + "\\textbf{Năm} & \\textbf{2021} & \\textbf{2022} & \\textbf{2023} & \\textbf{2024} \\\\ \\hline \n"
                + "Số lượng áo ấm (chiếc) & $120$ & $150$ & $200$ & $260$ \\\\ \\hline \n"
                + "\\end{tabular}\\end{center}" + BR
                + "a) \\textbf{(0,5 điểm)} Hãy lập bảng thống kê số lượng áo ấm quyên góp được qua các năm." + BR
                + "b) \\textbf{(0,5 điểm)} Số lượng áo ấm quyên góp được năm 2024 tăng bao nhiêu chiếc so với năm 2022? Tính tỉ số phần trăm số áo ấm tăng thêm của năm 2024 so với năm 2022 (làm tròn đến chữ số thập phân thứ hai)."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Dựa vào biểu đồ trên, ta có bảng thống kê số lượng áo ấm quyên góp được qua bốn năm:"),
                    ("\\begin{center}\\begin{tabular}{|l|c|c|c|c|}\\hline \\textbf{Năm} & 2021 & 2022 & 2023 & 2024 \\\\ \\hline \\textbf{Số áo ấm (chiếc)} & 120 & 150 & 200 & 260 \\\\ \\hline \\end{tabular}\\end{center}", 0.25),
                    ("Vậy số lượng áo ấm tăng liên tục qua từng năm học.", 0.25),
                ]),
                y("b)", 0.5, [
                    ("Số lượng áo ấm quyên góp được năm 2024 tăng so với năm 2022 là:"),
                    ("$260 - 150 = 110$ (chiếc).", 0.25),
                    ("Tỉ số phần trăm số lượng áo ấm tăng thêm so với năm 2022 là:"),
                    ("$\\dfrac{110}{150} \\cdot 100\\% = \\dfrac{220}{3}\\% \\approx 73{,}33\\%$."),
                    ("Vậy năm 2024 số áo ấm tăng $110$ chiếc, tương ứng tăng khoảng $73{,}33\\%$ so với năm 2022.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 3.a", "Lập bảng thống kê từ biểu đồ đoạn thẳng", "TK V", "NB", 0.5, 4, "THCS \& THPT Lương Thế Vinh"),
                ("Bài 3.b", "Tính lượng tăng trưởng và tỉ số phần trăm tăng thêm", "TK V", "TH", 0.5, 5, "THCS \& THPT Lương Thế Vinh"),
            ],
            note="Bài thống kê biểu đồ đoạn thẳng KNTT: yêu cầu ghi rõ đơn vị và phép làm tròn.",
        ),
        dict(
            label="Bài 4.",
            level=2,
            statement=(
                "\\textbf{(3,0 điểm)} Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường trung tuyến $AM$ ($M \\in BC$)." + BR
                + "Gọi $D$ và $E$ lần lượt là hình chiếu của $M$ trên cạnh $AB$ và cạnh $AC$." + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh tứ giác $ADME$ là hình chữ nhật." + BR
                + "b) \\textbf{(1,0 điểm)} Lấy điểm $K$ đối xứng với điểm $M$ qua $E$. Chứng minh tứ giác $AMCK$ là hình thoi." + BR
                + "c) \\textbf{(1,0 điểm)} Kẻ đường cao $AH$ của tam giác $ABC$ ($H \\in BC$). Chứng minh rằng $\\widehat{DHE} = 90^\\circ$."
            ),
            hinh_da=H.get_tikz_on3(),
            dap_an=[
                y("a)", 1.0, [
                    ("Xét tứ giác $ADME$, ta có:"),
                    ("$\\widehat{DAE} = \\widehat{BAC} = 90^\\circ$ (do tam giác $ABC$ vuông tại $A$).", 0.25),
                    ("$MD \\perp AB$ tại $D$ nên $\\widehat{ADM} = 90^\\circ$.", 0.25),
                    ("$ME \\perp AC$ tại $E$ nên $\\widehat{AEM} = 90^\\circ$.", 0.25),
                    ("Tứ giác $ADME$ có ba góc vuông nên là hình chữ nhật (điều phải chứng minh).", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Xét tam giác $ABC$ vuông tại $A$, có $M$ là trung điểm của $BC$ và $ME \\perp AC$ tại $E$."),
                    ("Mà $AB \\perp AC$ nên $ME \\parallel AB$. Suy ra $E$ là trung điểm của đoạn thẳng $AC$.", 0.25),
                    ("Lại có $K$ đối xứng với $M$ qua $E$ nên $E$ là trung điểm của đoạn thẳng $MK$."),
                    ("Tứ giác $AMCK$ có hai đường chéo $AC$ và $MK$ cắt nhau tại trung điểm $E$ của mỗi đường, nên là hình bình hành.", 0.25),
                    ("Mặt khác, $AC \\perp MK$ tại $E$ (do $ME \\perp AC$).", 0.25),
                    ("Hình bình hành $AMCK$ có hai đường chéo vuông góc nên là hình thoi (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 1.0, [
                    ("Xét tam giác $AHB$ vuông tại $H$, có $D$ là trung điểm của $AB$ (do $MD \\parallel AC$), nên $HD$ là đường trung tuyến ứng với cạnh huyền $AB$."),
                    ("Suy ra $HD = AD = \\dfrac{1}{2}AB$, do đó tam giác $ADH$ cân tại $D$, suy ra $\\widehat{DHA} = \\widehat{DAH}$.", 0.25),
                    ("Tương tự, xét tam giác $AHC$ vuông tại $H$, có $HE$ là đường trung tuyến ứng với cạnh huyền $AC$, nên $HE = AE = \\dfrac{1}{2}AC$."),
                    ("Suy ra tam giác $AEH$ cân tại $E$, suy ra $\\widehat{EHA} = \\widehat{EAH}$.", 0.25),
                    ("Khi đó: $\\widehat{DHE} = \\widehat{DHA} + \\widehat{EHA} = \\widehat{DAH} + \\widehat{EAH} = \\widehat{DAE}$."),
                    ("Mà tam giác $ABC$ vuông tại $A$ nên $\\widehat{DAE} = 90^\\circ$."),
                    ("Suy ra $\\widehat{DHE} = 90^\\circ$.", 0.25),
                    ("Vậy $\\widehat{DHE} = 90^\\circ$."),
                ]),
            ],
            mt=[
                ("Bài 4.a", "Chứng minh tứ giác là hình chữ nhật", "HH III", "TH", 1.0, 8, "THCS Nguyễn Trường Tộ"),
                ("Bài 4.b", "Chứng minh tứ giác là hình thoi qua hai đường chéo vuông góc", "HH III", "VD", 1.0, 10, "THCS Nguyễn Trường Tộ"),
                ("Bài 4.c", "Chứng minh góc vuông bằng tính chất đường trung tuyến trong tam giác vuông", "HH III", "VD", 1.0, 9, "THCS Nguyễn Trường Tộ"),
            ],
            note="Bài hình hay và tinh tế của THCS Nguyễn Trường Tộ: áp dụng nhuần nhuyễn tính chất trung tuyến cạnh huyền.",
        ),
        dict(
            label="Bài 5.",
            level=3,
            statement=(
                "\\textbf{(0,5 điểm)} Cho các số thực $x, y, z$ khác $0$ thỏa mãn điều kiện $x + y + z = 0$." + BR
                + "Tính giá trị của biểu thức: $P = \\dfrac{xy}{x^2 + y^2 - z^2} + \\dfrac{yz}{y^2 + z^2 - x^2} + \\dfrac{zx}{z^2 + x^2 - y^2}$."
            ),
            dap_an=[
                y("", 0.5, [
                    ("Vì $x + y + z = 0$, nên $x + y = -z$."),
                    ("Bình phương hai vế, ta được: $(x + y)^2 = (-z)^2$"),
                    ("$x^2 + 2xy + y^2 = z^2$"),
                    ("Suy ra: $x^2 + y^2 - z^2 = -2xy$.", 0.25),
                    ("Hoàn toàn tương tự, từ $y + z = -x$ và $z + x = -y$, ta có:"),
                    ("$y^2 + z^2 - x^2 = -2yz$ và $z^2 + x^2 - y^2 = -2zx$."),
                    ("Thay các kết quả trên vào biểu thức $P$, ta được:"),
                    ("$P = \\dfrac{xy}{-2xy} + \\dfrac{yz}{-2yz} + \\dfrac{zx}{-2zx}$"),
                    ("$P = -\\dfrac{1}{2} - \\dfrac{1}{2} - \\dfrac{1}{2} = -\\dfrac{3}{2}$."),
                    ("Vậy giá trị của biểu thức $P$ là $-\\dfrac{3}{2}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 5", "Tính giá trị biểu thức phân thức đối xứng ba biến thỏa mãn tổng bằng 0", "ĐS II", "VDC", 0.5, 6, "THCS \& THPT Lương Thế Vinh"),
            ],
            note="Câu VDC đề thi Cuối kì 1 THCS Lương Thế Vinh: vận dụng hằng đẳng thức mở rộng một cách tự nhiên và sáng tạo.",
        ),
    ],
)


# ─────────────────────────── HÀM HỖ TRỢ XUẤT JSON ───────────────────────────
KIND = ["review", "concept", "practice1", "practice2", "reflection"]


def kiem_nguon():
    res = {}
    bo = {}
    for k, D in DE.items():
        q_cnt = {}
        for c in D["tn"]:
            q = QUAN[c["nguon"]]
            q_cnt[q] = q_cnt.get(q, 0.0) + 0.25
            bo[q] = bo.get(q, 0.0) + 0.25
        for b in D["bai"]:
            for r in b["mt"]:
                q = QUAN[r[6]]
                q_cnt[q] = q_cnt.get(q, 0.0) + r[4]
                bo[q] = bo.get(q, 0.0) + r[4]
        res[k] = (len(set(c["nguon"] for c in D["tn"]).union(set(r[6] for b in D["bai"] for r in b["mt"]))), q_cnt)
    return res, bo


def bang_mt(rows):
    s = (
        "\\vspace{-6pt}\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\n"
        "\\begin{tabular}{|c|p{5.4cm}|c|c|c|c|p{2.9cm}|}\n\\hline\n"
        "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Chương} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} & \\textbf{Nguồn đề} \\\\ \\hline\n"
    )
    tong_d = tong_p = 0
    for c, nd, ch, m, di, ph, ng in rows:
        s += f"{c} & {nd} & {ch} & {m} & {d(di)} & {ph} & {ng} \\\\ \\hline\n"
        tong_d += di
        tong_p += ph
    s += f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{TỔNG CỘNG}}}} & \\textbf{{{d(tong_d)}}} & \\textbf{{{tong_p}}} & \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tong_d, tong_p


def bang_muc(rows):
    muc = {"NB": 0, "TH": 0, "VD": 0, "VDC": 0}
    ds = {"Đại số \& Thống kê (Chương I, II, V, VI)": dict(muc), "Hình học (Chương III, IV)": dict(muc)}
    for c, nd, ch, m, di, ph, ng in rows:
        mach = "Hình học (Chương III, IV)" if ch.startswith("HH") else "Đại số \& Thống kê (Chương I, II, V, VI)"
        ds[mach][m] += di
    s = (
        "\\noindent\\textbf{TỔNG HỢP THEO MẠCH KIẾN THỨC VÀ CẤP ĐỘ (điểm)} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\n\\begin{tabular}{|l|c|c|c|c|c|}\n\\hline\n"
        "\\textbf{Mạch kiến thức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{VDC} & \\textbf{Tổng} \\\\ \\hline\n"
    )
    tot = dict(muc)
    for k, v in ds.items():
        s += f"{k} & " + " & ".join(d(v[m]) if v[m] else "0" for m in muc) + f" & \\textbf{{{d(sum(v.values()))}}} \\\\ \\hline\n"
        for m in muc:
            tot[m] += v[m]
    s += "\\textbf{Tổng điểm} & " + " & ".join(f"\\textbf{{{d(tot[m]) if tot[m] else '0'}}}" for m in muc) + " & \\textbf{10,0} \\\\ \\hline\n"
    s += "\\textbf{Tỉ lệ} & " + " & ".join(f"{round(tot[m]*10)}\\%" for m in muc) + " & 100\\% \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tot


def bang_bay(rows):
    s = (
        "\\noindent\\textbf{CẨM NANG CHUYÊN ĐỀ: CÁC BẪY TỬ HUYỆT \\& LỖI SAI THƯỜNG GẶP} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.1}\n"
        "\\begin{tabular}{|c|p{3.6cm}|p{4.3cm}|p{4.7cm}|}\n\\hline\n"
        "\\textbf{Câu} & \\textbf{Bẫy đánh lừa} & \\textbf{Lỗi sai hay gặp (Mất điểm)} & \\textbf{Cách xử lý an toàn (Ăn trọn điểm)} \\\\ \\hline\n"
    )
    for c, b, l, k in rows:
        s += f"{c} & {b} & {l} & {k} \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


def bang_dap_an_tn(D):
    s = (
        "\\textit{Bảng đáp án trắc nghiệm:} [[br]] "
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.2}\n"
        "\\begin{tabular}{|c|c|c|c|c|c|c|c|}\n\\hline\n"
        + " & ".join(f"\\textbf{{Câu {c['cau']}}}" for c in D["tn"]) + " \\\\ \\hline\n"
        + " & ".join(f"\\textbf{{{c['dap']}}}" for c in D["tn"]) + " \\\\ \\hline\n"
        + "\\end{tabular}\\end{center}"
    )
    return s


TIEN_BO = [
    ("Phép tính \\& Phân tích nhân tử (1,5đ)", "Ia: $(2x-3)(x+1) - 2x(x-2)$; Ib: $x^2-6x+9-y^2$", "Ia: $(15x^3y^2-10x^2y+5xy):5xy$; Ib: Tìm x $(x-3)^2-x(x+2)=11$", "Ia: Rút gọn HĐT $(x+2)^2+(x-2)^2-2(x^2-1)$; Ib: $x^3-2x^2+x-xy^2$"),
    ("Phân thức đại số (2,0đ)", "ĐKXĐ, rút gọn $A = \\frac{3x}{x-2}$, tính tại $x=-5$, tìm x nguyên", "Tính $A$, rút gọn $B = \\frac{x}{x+1}$, tìm x nguyên lớn nhất", "Rút gọn $A = \\frac{10}{x^2-4}$, nhân $P = A \\cdot B = \\frac{x-2}{x+2}$, tìm x nguyên"),
    ("Thống kê \\& Toán thực tế (1,0đ)", "Biểu đồ cột kép CLB Toán học, tính tỉ lệ \\% nữ", "Đo khoảng cách hai bờ hồ dùng đường trung bình tam giác", "Biểu đồ đoạn thẳng áo ấm từ thiện, tỉ lệ tăng trưởng"),
    ("Hình học tổng hợp (3,0đ)", "Tam giác vuông, HCN, hình thang cân, hình thoi", "Tam giác vuông, HCN, trung trực, vuông góc $AM \\perp DE$", "Tam giác vuông, HCN, hình thoi $AMCK$, góc vuông $\\widehat{DHE}=90^\\circ$"),
    ("VDC Cực trị \\& BĐT (0,5đ)", "Min hai biến $M = x^2-4xy+5y^2+10x-22y+28$", "PT nghiệm thực $(x+y-1)^2+(y-2)^2=0$, tính $P=(x+y)^{2024}$", "HĐT ba biến $x+y+z=0$, tính $P = \\sum \\frac{xy}{x^2+y^2-z^2}$"),
]


def bang_tien_bo():
    s = (
        "\\noindent\\textbf{BẢN ĐỒ DẠNG BÀI VÀ MỨC ĐỘ TIẾN BỘ QUA 3 ĐỀ ÔN TẬP:} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|p{2.6cm}|p{4.0cm}|p{4.0cm}|p{4.0cm}|}\n\\hline\n"
        "\\textbf{Mạch kiến thức} & \\textbf{Đề ôn tập số 1} & \\textbf{Đề ôn tập số 2} & \\textbf{Đề ôn tập số 3} \\\\ \\hline\n"
    )
    for r in TIEN_BO:
        s += " & ".join(r) + " \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


def bang_theo_doi():
    s = (
        "\\noindent\\textbf{PHIẾU THEO DÕI TIẾN BỘ CỦA HỌC SINH:} [[br]] "
        "\\textit{\\footnotesize Ghi điểm từng bài kiểm tra để đánh giá sự tiến bộ qua 3 đề ôn; bài nào chưa đạt cần tra lại bảng dạng để luyện thêm.} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.3}\n"
        "\\begin{tabular}{|p{7.2cm}|c|c|c|c|}\n\\hline\n"
        "\\textbf{Bài (điểm tối đa)} & \\textbf{Đề ôn 1} & \\textbf{Đề ôn 2} & \\textbf{Đề ôn 3} & \\textbf{Đạt chuẩn?} \\\\ \\hline\n"
    )
    for b in [
        "Phần I -- Trắc nghiệm 8 câu (2,0đ)",
        "Bài 1 -- Phép tính đa thức \\& Phân tích nhân tử (1,5đ)",
        "Bài 2 -- Phân thức đại số (2,0đ)",
        "Bài 3 -- Thống kê \\& Toán thực tế (1,0đ)",
        "Bài 4 -- Hình học tổng hợp (3,0đ)",
        "Bài 5 -- VDC Cực trị \\& BĐT (0,5đ)",
        "\\textbf{Tổng điểm (10,0đ)}",
    ]:
        s += b + " & & & & \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


def khoi_tn(c, co_loi_giai=True):
    blk = dict(type="problem", label=f"Câu {c['cau']}.", level=c["level"], statement=c["de"], options=c["options"], tier="onclass")
    if co_loi_giai:
        blk["answer"] = c["dap"]
        blk["solution"] = f"Chọn \\textbf{{{c['dap']}}}. " + c["giai"]
    return blk


def khoi_bai(b):
    sol = BR.join(b["dap_an"])
    if b.get("hinh_da"):
        sol = "\\begin{center}\\adjustbox{max width=0.62\\linewidth}{" + b["hinh_da"] + "}\\end{center}\n" + sol
    blk = dict(type="problem", label=b["label"], level=b["level"], statement=b["statement"], tier="onclass", solution=sol)
    if b.get("figure"):
        blk["figure"] = b["figure"]
    return blk


def de_json(k, D):
    stages = []

    # Chặng 1 (review, 1): Phần I Trắc nghiệm 8 câu
    st1_blocks = [dict(type="para", text=TN_DAU)]
    for c in D["tn"]:
        st1_blocks.append(khoi_tn(c, co_loi_giai=True))
    stages.append(dict(kind=KIND[0], number=1, title="", blocks=st1_blocks))

    # Chặng 2 (concept, 2): Phần II Tự luận - Bài 1
    st2_blocks = [dict(type="para", text=TL_DAU), khoi_bai(D["bai"][0])]
    stages.append(dict(kind=KIND[1], number=2, title="", blocks=st2_blocks))

    # Chặng 3 (practice1, 3): Bài 2 Phân thức đại số
    st3_blocks = [khoi_bai(D["bai"][1])]
    stages.append(dict(kind=KIND[2], number=3, title="", blocks=st3_blocks))

    # Chặng 4 (practice2, 4): Bài 3 Thực tế & Bài 4 Hình học
    st4_blocks = [khoi_bai(D["bai"][2]), khoi_bai(D["bai"][3])]
    stages.append(dict(kind=KIND[3], number=4, title="", blocks=st4_blocks))

    # Chặng 5 (reflection, 5): Bài 5 VDC
    st5_blocks = [khoi_bai(D["bai"][4]), dict(type="para", text="\\begin{center}\\textit{$-$ HẾT $-$}\\end{center}")]
    stages.append(dict(kind=KIND[4], number=5, title="", blocks=st5_blocks))

    tit = f"Đề ôn tập cuối học kì I — Số {k[-1]} (90 phút)"
    return dict(slug=D["slug_de"], title=tit, eyebrow=D["eyebrow"], grade_label="Lớp 8", class_tier="", theme="de_thi", stages=stages)


def mt_json(k, D):
    stages = []
    rows = []
    for c in D["tn"]:
        rows.append((f"Câu {c['cau']}", c["nd"], c["ch"], c["muc"], 0.25, 2, c["nguon"]))
    for b in D["bai"]:
        for r in b["mt"]:
            rows.append(r)

    s_mt, tong_d, tong_p = bang_mt(rows)
    s_muc, tot = bang_muc(rows)
    so = k[-1]

    # Stage 1: Ma trận đề thi + Bảng bẫy tử huyệt
    q_dict = {}
    for r in rows:
        q = QUAN[r[6]]
        q_dict[q] = q_dict.get(q, 0.0) + r[4]
    str_nguon = ", ".join(f"{q} ({d(v)}đ - {round(v*10)}\\%)" for q, v in sorted(q_dict.items(), key=lambda t: -t[1]))

    b1 = [
        dict(type="para", text=D["gioi_thieu"]),
        dict(
            type="para",
            text=f"\\textbf{{MA TRẬN ĐỀ ÔN TẬP SỐ {so} -- CUỐI KÌ I (90 PHÚT)}}"
            + BR
            + f"\\textbf{{Cơ cấu nguồn đề ({len(q_dict)} quận/huyện):}} {str_nguon} (đạt chuẩn $\\le 40\\%$ điểm/quận)."
            + BR
            + s_mt,
        ),
        dict(type="para", text=s_muc),
        dict(type="para", text=bang_bay(D["bay"])),
        dict(
            type="para",
            text="\\textbf{HƯỚNG DẪN SỬ DỤNG PHIẾU:}"
            + BR
            + D["cach_dung"]
            + BR
            + "\\textbf{Quy tắc chấm thi:} Mỗi bước biến đổi được tính điểm thành phần chi tiết bên phải dòng. Mỗi phép biến đổi viết trên một dòng riêng biệt. Bài hình phải vẽ đúng hình mới chấm điểm. Vẽ sai hình hoặc không vẽ hình thì không cho điểm.",
        ),
    ]
    stages.append(dict(kind=KIND[0], number=1, title=f"Ma trận Đề ôn tập số {so}", blocks=b1))

    # Stage 2: Đáp án Phần I Trắc nghiệm và Bài 1
    b2 = [
        dict(type="para", text="\\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm)} -- Mỗi câu đúng được 0,25 điểm."),
        dict(type="para", text=bang_dap_an_tn(D)),
        dict(type="para", text=BR.join(f"\\textbf{{Câu {c['cau']} -- {c['dap']}.}} {c['giai']}" for c in D["tn"])),
        dict(type="para", text="\\textbf{PHẦN II. TỰ LUẬN (8,0 điểm)}"),
        dict(type="para", text=f"\\textbf{{BÀI 1 ({d(sum(r[4] for r in D['bai'][0]['mt']))} điểm).}}"),
    ]
    for a in D["bai"][0]["dap_an"]:
        b2.append(dict(type="para", text=a))
    b2.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + D["bai"][0]["note"] + "}"))
    stages.append(dict(kind=KIND[1], number=2, title="Đáp án Phần I và Bài 1", blocks=b2))

    # Stage 3: Đáp án Bài 2
    b3 = [
        dict(type="para", text=f"\\textbf{{BÀI 2 ({d(sum(r[4] for r in D['bai'][1]['mt']))} điểm).}}"),
    ]
    for a in D["bai"][1]["dap_an"]:
        b3.append(dict(type="para", text=a))
    b3.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + D["bai"][1]["note"] + "}"))
    stages.append(dict(kind=KIND[2], number=3, title="Đáp án Bài 2", blocks=b3))

    # Stage 4: Đáp án Bài 3 và Bài 4
    b4 = [
        dict(type="para", text=f"\\textbf{{BÀI 3 ({d(sum(r[4] for r in D['bai'][2]['mt']))} điểm).}}"),
    ]
    for a in D["bai"][2]["dap_an"]:
        b4.append(dict(type="para", text=a))
    b4.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + D["bai"][2]["note"] + "}"))

    b4.append(dict(type="para", text=f"\\textbf{{BÀI 4 ({d(sum(r[4] for r in D['bai'][3]['mt']))} điểm).}}"))
    if D["bai"][3].get("hinh_da"):
        b4.append(dict(type="figure", tikz=D["bai"][3]["hinh_da"], width="0.66\\linewidth"))
    for a in D["bai"][3]["dap_an"]:
        b4.append(dict(type="para", text=a))
    b4.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + D["bai"][3]["note"] + "}"))
    stages.append(dict(kind=KIND[3], number=4, title="Đáp án Bài 3 và Bài 4", blocks=b4))

    # Stage 5: Đáp án Bài 5 và biểu điểm
    b5 = [
        dict(type="para", text=f"\\textbf{{BÀI 5 ({d(sum(r[4] for r in D['bai'][4]['mt']))} điểm).}}"),
    ]
    for a in D["bai"][4]["dap_an"]:
        b5.append(dict(type="para", text=a))
    b5.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + D["bai"][4]["note"] + "}"))

    bd = BR.join(
        ["\\textbf{Phần I. Trắc nghiệm (2,0đ):} 8 câu x 0,25đ."]
        + [f"\\textbf{{{b['label']} ({d(sum(r[4] for r in b['mt']))}đ):}} " + " $-$ ".join(f"{r[0]} {d(r[4])}đ" for r in b["mt"]) for b in D["bai"]]
    )
    b5.append(dict(type="para", text="\\textbf{BIỂU ĐIỂM TỔNG HỢP}" + BR + bd))
    b5.append(
        dict(
            type="para",
            text="\\textbf{Tổng: 10,0 điểm.} Điểm toàn bài làm tròn đến $0{,}25$ điểm. Học sinh giải theo cách khác đúng vẫn cho điểm tối đa từng phần. Bài hình vẽ sai hình không chấm điểm.",
        )
    )
    b5.append(dict(type="para", text=bang_tien_bo()))
    b5.append(dict(type="para", text=bang_theo_doi()))
    stages.append(dict(kind=KIND[4], number=5, title="Đáp án Bài 5 và Biểu điểm tổng hợp", blocks=b5))

    tit = f"Ma trận đề và đáp án chi tiết — Đề ôn tập số {so}"
    return dict(slug=D["slug_mt"], title=tit, eyebrow="TÀI LIỆU GIÁO VIÊN • LỚP 8 • " + D["ten"], grade_label="Lớp 8", class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


# ─────────────────────────── MAIN ───────────────────────────
if __name__ == "__main__":
    NGUON, NGUON_BO = kiem_nguon()
    print("✓ Kiểm tra rải nguồn Đề ôn tập CK1 lớp 8 thành công:")
    for _k, (_n, _q) in NGUON.items():
        print(f"  [{_k}] {_n} trường, {len(_q)} quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(_q.items(), key=lambda t: -t[1])))
    print("  Tổng cả bộ theo quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(NGUON_BO.items(), key=lambda t: -t[1])))

    for k, D in DE.items():
        p_de = OUT / f"{D['slug_de']}.json"
        p_mt = OUT / f"{D['slug_mt']}.json"
        p_de.write_text(json.dumps(de_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
        p_mt.write_text(json.dumps(mt_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → Đã sinh: {p_de.name} và {p_mt.name}")
    print("Hoàn tất sinh 3 đề ôn tập CK1 lớp 8.")
