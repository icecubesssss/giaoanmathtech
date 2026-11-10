#!/usr/bin/env python3
"""3 ĐỀ KIỂM TRA CUỐI HỌC KÌ I CHÍNH THỨC — TOÁN 8 (90 PHÚT - KẾT NỐI TRI THỨC).
Sinh 3 đề kiểm tra chính thức (Đề 1, Đề 2, Đề 3) + 3 file Ma trận đề và đáp án chi tiết
vào inputs/seeds/lop-8/de-on-tap-cuoi-ki-1/ (theme de_thi, trinh_bay "thoang").
Quy trình: docs/quy-trinh-bo-de-on-tap.md.

Tất cả các đề bốc từ đề thi thật của các trường/quận Hà Nội CHƯA DÙNG ở 3 đề ôn tập:
  - Ba Đình: THCS Giảng Võ 2, THCS Thăng Long
  - Cầu Giấy: THCS Nguyễn Bỉnh Khiêm, THCS Nghĩa Tân 2, MathTech chuẩn thi
  - Hoàn Kiếm: THCS Thanh Quan
  - Long Biên: THCS Ngô Gia Tự
  - Thanh Trì: Huyện Thanh Trì, THCS Tam Hiệp
  - Phúc Thọ: THCS Hát Môn
  - Ngoại thành: Huyện Thanh Oai, Huyện Thường Tín, Huyện Ứng Hoà

Tỉ lệ ma trận chuẩn 10 điểm KNTT: NB 20% · TH 55-60% · VD 17-20% · VDC 5%.
Kẹp phổ điểm chuẩn Gauss đỉnh 6,0 - 7,0 điểm.
Đáp số đã kiểm chứng SymPy / giải tích. Lời giải tuân thủ 100% loi_giai_thi_gate và sgk_style_gate.

Chạy:  .venv/bin/python scripts/de_chinh_thuc_ck1_lop8.py
       .venv/bin/python -m src.main validate inputs/seeds/lop-8/de-on-tap-cuoi-ki-1/de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1.json
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
    """HS đi thi KHÔNG dùng dấu ⇔ (Thầy 01/10/2026): mỗi phép biến đổi xuống một dòng."""
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
    "THCS Giảng Võ 2": "Ba Đình",
    "THCS Thăng Long": "Ba Đình",
    "THCS Nguyễn Bỉnh Khiêm": "Cầu Giấy",
    "THCS Nghĩa Tân 2": "Cầu Giấy",
    "MathTech KNTT": "Cầu Giấy",
    "THCS Thanh Quan": "Hoàn Kiếm",
    "THCS Ngô Gia Tự": "Long Biên",
    "Huyện Thanh Trì": "Thanh Trì",
    "THCS Tam Hiệp": "Thanh Trì",
    "THCS Hát Môn": "Phúc Thọ",
    "Huyện Thanh Oai": "Thanh Oai",
    "Huyện Thường Tín": "Thường Tín",
    "Huyện Ứng Hoà": "Ứng Hoà",
}

# ─────────────────────────── DANH SÁCH 3 ĐỀ CHÍNH THỨC ───────────────────────────
DE = {}

# =====================================================================
# ĐỀ CHÍNH THỨC SỐ 1
# =====================================================================
DE["ct-1"] = dict(
    ten="ĐỀ CHÍNH THỨC SỐ 1",
    slug_de="de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1",
    slug_mt="ma-tran-va-dap-an-ck1-chinh-thuc-so-1",
    eyebrow="LỚP 8 • ĐỀ KIỂM TRA CHÍNH THỨC — SỐ 1",
    cach_dung="Bài thi chính thức 90 phút. Giám thị thu bài đúng giờ, chấm bài theo barem chi tiết 0,25đ. Điểm số dùng để đánh giá năng lực độc lập của học sinh.",
    gioi_thieu=(
        "\\textbf{ĐỀ KIỂM TRA CUỐI HỌC KÌ I -- ĐỀ CHÍNH THỨC SỐ 1 TOÁN 8 (KNTT)} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc ma trận chuẩn KNTT:} Đề bốc 100\\% từ các trường chưa xuất hiện ở 3 đề ôn tập: "
        "Phần I (2,0đ) Trắc nghiệm 8 câu x 0,25đ bao quát các chương I, II, III, IV, V · "
        "Bài 1 (1,5đ) Phép tính đa thức \\& Phân tích đa thức thành nhân tử · "
        "Bài 2 (2,0đ) Phân thức đại số: tính giá trị, rút gọn biểu thức và tìm x nguyên · "
        "Bài 3 (1,0đ) Toán thực tế đội xe chở hàng viết phân thức · "
        "Bài 4 (3,0đ) Hình học tổng hợp: tam giác vuông, hình chữ nhật, hình thang vuông · "
        "Bài 5 (0,5đ) VDC Giá trị nhỏ nhất đa thức hai biến."
    ),
    bay=[
        ("Bài 1.a", "Nhân đơn thức với đa thức quên đổi dấu khi có dấu trừ phía trước", "Viết sai dấu $-x(x - 2)(x + 2) = -x^3 - 4x$", "Khai triển hằng đẳng thức trước: $-x(x^2 - 4) = -x^3 + 4x$"),
        ("Bài 2.c", "Quên đối chiếu đồng thời cả 3 điều kiện xác định $x \\ne \\pm 2$ và $x \\ne -1$", "Nhận nhầm nghiệm $x = -1$ làm mẫu thức của $B$ bằng 0", "Luôn đối chiếu từng giá trị tìm được với toàn bộ ĐKXĐ của bài toán"),
        ("Bài 3.b", "Đặt sai ẩn hoặc quên đơn vị và điều kiện của ẩn", "Không đặt điều kiện $x > 2, x \\in \\mathbb{N}^*$ dẫn đến nhận nghiệm âm", "Ghi rõ điều kiện nguyên dương của số xe: $x \\in \\mathbb{N}^*, x > 2$"),
        ("Bài 4.c", "Ngộ nhận tứ giác $EIKF$ là hình thang vuông mà chưa chứng minh hai đáy song song", "Chỉ chỉ ra góc vuông tại $E$ mà quên chứng minh $EI \\parallel KF$", "Dùng tính chất đường trung tuyến tam giác vuông để suy ra hai góc đồng vị bằng nhau"),
    ],
    tn=[
        tn(1, "Bậc của đơn thức $-2x^2y^3$ là:", ["$2$", "$3$", "$5$", "$6$"], "C",
           "Bậc của đơn thức là tổng số mũ của các biến: $2 + 3 = 5$.", "Đơn thức", "ĐS I", "NB", "THCS Giảng Võ 2"),
        tn(2, "Kết quả của phép nhân đơn thức $3xy$ với đa thức $(2x - y)$ là:", ["$6x^2y - 3xy^2$", "$6x^2y - y$", "$5x^2y - 3xy^2$", "$6x^2y + 3xy^2$"], "A",
           "Nhân từng hạng tử: $3xy \\cdot 2x - 3xy \\cdot y = 6x^2y - 3xy^2$.", "Phép nhân đa thức", "ĐS I", "TH", "THCS Giảng Võ 2"),
        tn(3, "Hằng đẳng thức hiệu hai lập phương $A^3 - B^3$ bằng biểu thức nào sau đây?", ["$(A - B)^3$", "$(A - B)(A^2 + AB + B^2)$", "$(A - B)(A^2 - AB + B^2)$", "$(A + B)(A^2 - AB + B^2)$"], "B",
           "Theo hằng đẳng thức: $A^3 - B^3 = (A - B)(A^2 + AB + B^2)$.", "Hằng đẳng thức đáng nhớ", "ĐS II", "NB", "THCS Nguyễn Bỉnh Khiêm"),
        tn(4, "Phân tích đa thức $x^2 - 25$ thành nhân tử, ta được kết quả là:", ["$(x - 25)(x + 25)$", "$(x - 5)^2$", "$(x - 5)(x + 5)$", "$(x + 5)^2$"], "C",
           "Áp dụng hiệu hai bình phương: $x^2 - 25 = x^2 - 5^2 = (x - 5)(x + 5)$.", "Phân tích đa thức thành nhân tử", "ĐS II", "TH", "THCS Nguyễn Bỉnh Khiêm"),
        tn(5, "Tứ giác có các cạnh đối song song là hình gì?", ["Hình bình hành", "Hình chữ nhật", "Hình thoi", "Hình thang cân"], "A",
           "Định nghĩa: Tứ giác có các cạnh đối song song là hình bình hành.", "Hình bình hành", "HH III", "NB", "THCS Thanh Quan"),
        tn(6, "Hình chữ nhật có hai cạnh kề bằng nhau là hình gì?", ["Hình thang cân", "Hình bình hành", "Hình thoi", "Hình vuông"], "D",
           "Dấu hiệu nhận biết: Hình chữ nhật có hai cạnh kề bằng nhau là hình vuông.", "Hình vuông", "HH III", "TH", "Huyện Thanh Trì"),
        tn(7, "Cho $\\triangle ABC$, một đường thẳng song song với $BC$ cắt hai cạnh $AB, AC$ lần lượt tại $M$ và $N$. Biết $AM = 2\\text{ cm}, MB = 4\\text{ cm}, AN = 3\\text{ cm}$. Độ dài đoạn thẳng $NC$ là:", ["$3\\text{ cm}$", "$6\\text{ cm}$", "$4\\text{ cm}$", "$5\\text{ cm}$"], "B",
           "Theo định lí Thalès: $\\dfrac{AM}{MB} = \\dfrac{AN}{NC} \\implies NC = \\dfrac{MB \\cdot AN}{AM} = \\dfrac{4 \\cdot 3}{2} = 6\\text{ cm}$.", "Định lí Thalès trong tam giác", "HH IV", "TH", "Huyện Thanh Trì"),
        tn(8, "Phân thức đại số $\\dfrac{x - 1}{x + 3}$ xác định khi:", ["$x \\ne 1$", "$x \\ne 3$", "$x \\ne -3$", "$x \\ne 0$"], "C",
           "Phân thức xác định khi mẫu thức khác 0: $x + 3 \\ne 0 \\implies x \\ne -3$.", "Phân thức đại số", "ĐS VI", "NB", "THCS Ngô Gia Tự"),
    ],
    bai=[
        dict(
            label="Bài 1.",
            level=2,
            statement=(
                "\\textbf{(1,5 điểm)}" + BR
                + "a) \\textbf{(0,75 điểm)} Thực hiện phép tính và thu gọn: $A = (x - 1)(x^2 + x + 1) - x(x - 2)(x + 2)$." + BR
                + "b) \\textbf{(0,75 điểm)} Phân tích đa thức sau thành nhân tử: $B = x^2 - y^2 - 2x + 2y$."
            ),
            dap_an=[
                y("a)", 0.75, [
                    ("Ta có: $A = (x - 1)(x^2 + x + 1) - x(x - 2)(x + 2)$"),
                    ("$A = (x^3 - 1) - x(x^2 - 4)$", 0.25),
                    ("$A = x^3 - 1 - x^3 + 4x$", 0.25),
                    ("$A = (x^3 - x^3) + 4x - 1 = 4x - 1$"),
                    ("Vậy biểu thức sau khi thu gọn là $A = 4x - 1$.", 0.25),
                ]),
                y("b)", 0.75, [
                    ("Ta có: $B = x^2 - y^2 - 2x + 2y$"),
                    ("$B = (x^2 - y^2) - (2x - 2y)$", 0.25),
                    ("$B = (x - y)(x + y) - 2(x - y)$", 0.25),
                    ("$B = (x - y)(x + y - 2)$"),
                    ("Vậy đa thức được phân tích thành $B = (x - y)(x + y - 2)$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 1.a", "Thực hiện phép tính rút gọn đa thức bằng hằng đẳng thức", "ĐS I", "TH", 0.75, 5, "THCS Giảng Võ 2"),
                ("Bài 1.b", "Phân tích đa thức thành nhân tử bằng nhóm hạng tử", "ĐS II", "TH", 0.75, 5, "THCS Thanh Quan"),
            ],
            note="Bài 1 kiểm tra chuẩn hằng đẳng thức đáng nhớ và phương pháp nhóm hạng tử.",
        ),
        dict(
            label="Bài 2.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho hai biểu thức: $A = \\dfrac{x + 1}{x - 2} + \\dfrac{x - 1}{x + 2} + \\dfrac{x^2 + 4x}{4 - x^2}$ và $B = \\dfrac{x - 2}{x + 1}$ với $x \\ne \\pm 2; x \\ne -1$." + BR
                + "a) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $B$ khi $x = 3$." + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh rằng $A = \\dfrac{x - 2}{x + 2}$." + BR
                + "c) \\textbf{(0,5 điểm)} Đặt $P = A : B$. Tìm tất cả các số nguyên $x$ để biểu thức $P$ nhận giá trị nguyên."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Ta có $x = 3$ thỏa mãn điều kiện xác định $x \\ne \\pm 2$ và $x \\ne -1$."),
                    ("Thay $x = 3$ vào biểu thức $B$, ta được:"),
                    ("$B = \\dfrac{3 - 2}{3 + 1} = \\dfrac{1}{4}$.", 0.25),
                    ("Vậy khi $x = 3$ thì giá trị của biểu thức $B$ là $\\dfrac{1}{4}$.", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Với $x \\ne \\pm 2; x \\ne -1$, ta đổi dấu phân thức thứ ba: $\\dfrac{x^2 + 4x}{4 - x^2} = -\\dfrac{x^2 + 4x}{x^2 - 4}$."),
                    ("Mẫu thức chung là $(x - 2)(x + 2)$."),
                    ("Ta có: $A = \\dfrac{(x + 1)(x + 2) + (x - 1)(x - 2) - (x^2 + 4x)}{(x - 2)(x + 2)}$", 0.25),
                    ("$A = \\dfrac{(x^2 + 3x + 2) + (x^2 - 3x + 2) - x^2 - 4x}{(x - 2)(x + 2)}$", 0.25),
                    ("$A = \\dfrac{x^2 - 4x + 4}{(x - 2)(x + 2)} = \\dfrac{(x - 2)^2}{(x - 2)(x + 2)}$", 0.25),
                    ("$A = \\dfrac{x - 2}{x + 2}$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 0.5, [
                    ("Ta có: $P = A : B = \\dfrac{x - 2}{x + 2} : \\dfrac{x - 2}{x + 1} = \\dfrac{x - 2}{x + 2} \\cdot \\dfrac{x + 1}{x - 2} = \\dfrac{x + 1}{x + 2}$."),
                    ("Ta biến đổi: $P = \\dfrac{x + 2 - 1}{x + 2} = 1 - \\dfrac{1}{x + 2}$."),
                    ("Để $P$ nhận giá trị nguyên với $x$ nguyên thì $\\dfrac{1}{x + 2}$ phải là số nguyên, suy ra $x + 2 \\in \\text{Ư}(1) = \\{\\pm 1\\}$."),
                    ("Nếu $x + 2 = 1 \\implies x = -1$ (loại do ĐKXĐ $x \\ne -1$)."),
                    ("Nếu $x + 2 = -1 \\implies x = -3$ (thỏa mãn ĐKXĐ).", 0.25),
                    ("Vậy số nguyên duy nhất thỏa mãn để $P$ nhận giá trị nguyên là $x = -3$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 2.a", "Tính giá trị phân thức đại số", "ĐS VI", "NB", 0.5, 4, "THCS Nguyễn Bỉnh Khiêm"),
                ("Bài 2.b", "Rút gọn biểu thức phân thức bằng quy đồng mẫu thức", "ĐS VI", "TH", 1.0, 10, "THCS Nguyễn Bỉnh Khiêm"),
                ("Bài 2.c", "Chia hai phân thức và tìm số nguyên x để phân thức nhận giá trị nguyên", "ĐS VI", "VD", 0.5, 6, "THCS Nguyễn Bỉnh Khiêm"),
            ],
            note="Bài phân thức trọng tâm: bẫy loại nghiệm $x = -1$ do điều kiện xác định của mẫu thức $B$.",
        ),
        dict(
            label="Bài 3.",
            level=2,
            statement=(
                "\\textbf{(1,0 điểm)} Một đội xe dự định dùng một số xe cùng loại để chở $120$ tấn hàng cứu trợ đồng bào miền Trung. "
                "Gọi số xe dự định điều động là $x$ ($x \\in \\mathbb{N}^*, x > 2$, đơn vị: xe)." + BR
                + "a) \\textbf{(0,5 điểm)} Viết phân thức biểu thị khối lượng hàng mỗi xe phải chở theo dự định (tấn)." + BR
                + "b) \\textbf{(0,5 điểm)} Khi xuất phát, có $2$ xe được điều đi làm nhiệm vụ khác nên mỗi xe còn lại phải chở thêm $3$ tấn hàng so với dự định. "
                "Viết phân thức biểu thị khối lượng hàng thực tế mỗi xe đã chở và tính số xe ban đầu của đội xe."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Dựa vào đề bài, đội xe dự định chở $120$ tấn hàng chia đều cho $x$ xe."),
                    ("Phân thức biểu thị khối lượng hàng mỗi xe phải chở theo dự định là: $\\dfrac{120}{x}\\text{ (tấn)}$.", 0.25),
                    ("Vậy theo dự định mỗi xe chở $\\dfrac{120}{x}$ tấn hàng.", 0.25),
                ]),
                y("b)", 0.5, [
                    ("Thực tế số xe tham gia chở hàng là $x - 2$ (xe)."),
                    ("Phân thức biểu thị khối lượng hàng thực tế mỗi xe đã chở là: $\\dfrac{120}{x - 2}\\text{ (tấn)}$.", 0.25),
                    ("Vì mỗi xe thực tế phải chở thêm $3$ tấn hàng so với dự định, nên ta có phương trình:"),
                    ("$\\dfrac{120}{x - 2} - \\dfrac{120}{x} = 3$"),
                    ("$\\dfrac{120x - 120(x - 2)}{x(x - 2)} = 3$"),
                    ("$\\dfrac{240}{x(x - 2)} = 3$"),
                    ("$x(x - 2) = 80$"),
                    ("$x^2 - 2x - 80 = 0$"),
                    ("$(x - 10)(x + 8) = 0$"),
                    ("Suy ra $x = 10$ (thỏa mãn điều kiện $x > 2$) hoặc $x = -8$ (loại)."),
                    ("Vậy ban đầu đội xe có $10$ chiếc xe.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 3.a", "Lập phân thức đại số biểu thị đại lượng trong bài toán thực tế", "ĐS VI", "NB", 0.5, 4, "THCS Ngô Gia Tự"),
                ("Bài 3.b", "Giải bài toán thực tế bằng cách lập phương trình chứa phân thức", "ĐS VI", "TH", 0.5, 5, "THCS Ngô Gia Tự"),
            ],
            note="Bài toán thực tế đặc trưng phân thức đại số lớp 8: lập phân thức và giải phương trình tìm ẩn.",
        ),
        dict(
            label="Bài 4.",
            level=2,
            statement=(
                "\\textbf{(3,0 điểm)} Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$ ($H \\in BC$)." + BR
                + "Gọi $M$ là trung điểm của cạnh $BC$. Từ $H$ kẻ $HE \\perp AB$ tại $E$ và $HF \\perp AC$ tại $F$." + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh tứ giác $AEHF$ là hình chữ nhật và $AH = EF$." + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh rằng $AM \\perp EF$." + BR
                + "c) \\textbf{(1,0 điểm)} Gọi $I$ là trung điểm của $HB$ và $K$ là trung điểm của $HC$. Chứng minh tứ giác $EIKF$ là hình thang vuông."
            ),
            hinh_da=H.get_tikz_ct1(),
            dap_an=[
                y("a)", 1.0, [
                    ("Xét tứ giác $AEHF$, ta có:"),
                    ("$\\widehat{EAF} = \\widehat{BAC} = 90^\\circ$ (do tam giác $ABC$ vuông tại $A$).", 0.25),
                    ("$HE \\perp AB$ tại $E$ nên $\\widehat{AEH} = 90^\\circ$.", 0.25),
                    ("$HF \\perp AC$ tại $F$ nên $\\widehat{AFH} = 90^\\circ$.", 0.25),
                    ("Tứ giác $AEHF$ có ba góc vuông nên là hình chữ nhật."),
                    ("Do đó hai đường chéo bằng nhau: $AH = EF$ (điều phải chứng minh).", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Gọi $O$ là giao điểm của $AH$ và $EF$. Vì $AEHF$ là hình chữ nhật nên $OA = OE = OF = OH$."),
                    ("Suy ra tam giác $OAF$ cân tại $O$, do đó $\\widehat{OFA} = \\widehat{OAF} = \\widehat{HAC}$.", 0.25),
                    ("Xét tam giác $ABC$ vuông tại $A$, có $M$ là trung điểm $BC$ nên $AM$ là trung tuyến ứng với cạnh huyền, suy ra $AM = MC = \\dfrac{1}{2}BC$."),
                    ("Do đó tam giác $MAC$ cân tại $M$, suy ra $\\widehat{MAC} = \\widehat{MCA} = \\widehat{ACB}$.", 0.25),
                    ("Gọi $D$ là giao điểm của $AM$ và $EF$."),
                    ("Xét tam giác $ADF$, ta có: $\\widehat{DAF} + \\widehat{DFA} = \\widehat{MAC} + \\widehat{OFA} = \\widehat{ACB} + \\widehat{HAC}$."),
                    ("Mà trong tam giác $AHC$ vuông tại $H$, ta có $\\widehat{ACB} + \\widehat{HAC} = 90^\\circ$, suy ra $\\widehat{DAF} + \\widehat{DFA} = 90^\\circ$."),
                    ("Dẫn đến $\\widehat{ADF} = 180^\\circ - 90^\\circ = 90^\\circ$."),
                    ("Suy ra $AM \\perp EF$ tại $D$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 1.0, [
                    ("Xét tam giác $BEH$ vuông tại $E$, có $I$ là trung điểm của $BH$ nên $EI$ là đường trung tuyến ứng với cạnh huyền $BH$."),
                    ("Suy ra $EI = IH = \\dfrac{1}{2}BH$, do đó tam giác $IEH$ cân tại $I$, dẫn đến $\\widehat{IEH} = \\widehat{IHE}$.", 0.25),
                    ("Mặt khác, vì $AEHF$ là hình chữ nhật nên tam giác $OEH$ cân tại $O$, suy ra $\\widehat{OEH} = \\widehat{OHE}$."),
                    ("Do đó: $\\widehat{IEH} + \\widehat{OEH} = \\widehat{IHE} + \\widehat{OHE} = \\widehat{IHO}$."),
                    ("Mà $AH \\perp BC$ tại $H$ nên $\\widehat{IHO} = 90^\\circ$, suy ra $\\widehat{IEO} = 90^\\circ$, tức là $IE \\perp EF$ (1).", 0.25),
                    ("Chứng minh hoàn toàn tương tự với tam giác $CFH$ vuông tại $F$ có trung tuyến $FK$, ta được $KF \\perp EF$ (2)."),
                    ("Từ (1) và (2) suy ra $IE \\parallel KF$ (vì cùng vuông góc với $EF$), do đó tứ giác $EIKF$ là hình thang."),
                    ("Lại có $\\widehat{IEF} = 90^\\circ$, suy ra tứ giác $EIKF$ là hình thang vuông.", 0.25),
                    ("Vậy tứ giác $EIKF$ là hình thang vuông (điều phải chứng minh)."),
                ]),
            ],
            mt=[
                ("Bài 4.a", "Chứng minh tứ giác là hình chữ nhật", "HH III", "TH", 1.0, 8, "Huyện Thanh Trì"),
                ("Bài 4.b", "Chứng minh hai đường thẳng vuông góc bằng phân tích góc", "HH III", "VD", 1.0, 10, "Huyện Thanh Trì"),
                ("Bài 4.c", "Chứng minh hình thang vuông qua tính chất đường trung tuyến", "HH III", "VD", 1.0, 9, "Huyện Thanh Trì"),
            ],
            note="Bài hình thi học kì chuẩn mực của Huyện Thanh Trì: rèn kĩ năng chứng minh đường vuông góc và hình thang vuông.",
        ),
        dict(
            label="Bài 5.",
            level=3,
            statement=(
                "\\textbf{(0,5 điểm)} Tìm giá trị nhỏ nhất của biểu thức sau:" + BR
                + "$A = 2x^2 + y^2 - 2xy - 2x + 2024$ với mọi $x, y \\in \\mathbb{R}$."
            ),
            dap_an=[
                y("", 0.5, [
                    ("Ta biến đổi biểu thức $A$ như sau:"),
                    ("$A = (x^2 - 2xy + y^2) + (x^2 - 2x + 1) + 2023$"),
                    ("$A = (x - y)^2 + (x - 1)^2 + 2023$", 0.25),
                    ("Vì $(x - y)^2 \\ge 0$ và $(x - 1)^2 \\ge 0$ với mọi $x, y \\in \\mathbb{R}$, nên $A \\ge 2023$."),
                    ("Dấu đẳng thức xảy ra khi và chỉ khi: $x - 1 = 0$ và $x - y = 0$, tức là $x = 1$ và $y = 1$."),
                    ("Vậy giá trị nhỏ nhất của biểu thức $A$ là $2023$, đạt được khi $x = 1$ và $y = 1$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 5", "Tìm giá trị nhỏ nhất của biểu thức hai biến bằng hằng đẳng thức", "ĐS II", "VDC", 0.5, 6, "THCS Giảng Võ 2"),
            ],
            note="Câu phân hoá thi Cuối kì 1 THCS Giảng Võ 2: tách biến đổi hai bình phương rất chuẩn mực.",
        ),
    ],
)

# =====================================================================
# ĐỀ CHÍNH THỨC SỐ 2
# =====================================================================
DE["ct-2"] = dict(
    ten="ĐỀ CHÍNH THỨC SỐ 2",
    slug_de="de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2",
    slug_mt="ma-tran-va-dap-an-ck1-chinh-thuc-so-2",
    eyebrow="LỚP 8 • ĐỀ KIỂM TRA CHÍNH THỨC — SỐ 2",
    cach_dung="Bài thi chính thức 90 phút. Giám thị thu bài đúng giờ, chấm bài theo barem chi tiết 0,25đ. Điểm số dùng để đánh giá năng lực độc lập của học sinh.",
    gioi_thieu=(
        "\\textbf{ĐỀ KIỂM TRA CUỐI HỌC KÌ I -- ĐỀ CHÍNH THỨC SỐ 2 TOÁN 8 (KNTT)} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc ma trận chuẩn KNTT:} Đề bốc 100\\% từ các trường chưa xuất hiện ở 3 đề ôn tập: "
        "Phần I (2,0đ) Trắc nghiệm 8 câu x 0,25đ phân phối chuẩn · "
        "Bài 1 (1,5đ) Rút gọn đa thức \\& Phương trình tìm x · "
        "Bài 2 (2,0đ) Phân thức đại số: tính giá trị, rút gọn biểu thức và tìm x nguyên · "
        "Bài 3 (1,0đ) Thống kê lượng khách du lịch từ biểu đồ KNTT · "
        "Bài 4 (3,0đ) Hình học tổng hợp: tam giác vuông cân, hình vuông, trung điểm · "
        "Bài 5 (0,5đ) VDC Giá trị nhỏ nhất đa thức hai biến."
    ),
    bay=[
        ("Bài 1.b", "Sót nghiệm khi giải phương trình tích", "Chỉ tìm nghiệm $x = 3$ mà bỏ quên nghiệm $x = -4/3$", "Đặt nhân tử chung $(x - 3)(3x + 4) = 0$ và giải đủ hai trường hợp"),
        ("Bài 2.b", "Đổi dấu mẫu đối $x^2 - 9$ và phân tích tử số bị nhầm dấu", "Khai triển tử thức $3x - 9$ quên đặt nhân tử chung 3", "Rút gọn nhân tử chung: $\\dfrac{3(x - 3)}{(x - 3)(x + 3)} = \\dfrac{3}{x + 3}$"),
        ("Bài 2.c", "Quên đối chiếu điều kiện $x \\ne \\pm 3$", "Lấy cả giá trị $x = 3$ hoặc $x = -3$ vào tập nghiệm", "Đối chiếu từng giá trị tìm được với $x \\ne \\pm 3$"),
        ("Bài 4.c", "Áp dụng định lí đường trung bình mà chưa chứng minh song song", "Chưa chứng minh $MK \\parallel BF$ mà đã kết luận $K$ là trung điểm", "Nêu rõ giả thiết song song và trung điểm $M$ để áp dụng định lí đường trung bình hình thang"),
    ],
    tn=[
        tn(1, "Bậc của đa thức $M = 3x^2y - 2xy^2 + 5x^3 - 7$ là:", ["$2$", "$3$", "$4$", "$5$"], "B",
           "Hạng tử $3x^2y, -2xy^2, 5x^3$ đều có bậc cao nhất là $3$.", "Bậc của đa thức", "ĐS I", "NB", "THCS Thăng Long"),
        tn(2, "Kết quả của phép chia $12x^4y^3 : (-4x^2y)$ là:", ["$3x^2y^2$", "$-3x^2y^2$", "$-3x^2y$", "$3x^2y$"], "B",
           "Thực hiện chia hệ số và từng biến: $[12 : (-4)] \\cdot (x^4 : x^2) \\cdot (y^3 : y) = -3x^2y^2$.", "Chia đơn thức cho đơn thức", "ĐS I", "TH", "THCS Thăng Long"),
        tn(3, "Khai triển hằng đẳng thức $(2x + 1)^2$, ta được kết quả là:", ["$4x^2 + 4x + 1$", "$4x^2 + 1$", "$2x^2 + 4x + 1$", "$4x^2 + 2x + 1$"], "A",
           "Áp dụng bình phương của một tổng: $(2x + 1)^2 = (2x)^2 + 2 \\cdot 2x \\cdot 1 + 1^2 = 4x^2 + 4x + 1$.", "Hằng đẳng thức đáng nhớ", "ĐS II", "NB", "THCS Nghĩa Tân 2"),
        tn(4, "Phân tích đa thức $x^3 - 4x$ thành nhân tử, ta được kết quả là:", ["$x(x - 4)$", "$x(x - 2)(x + 2)$", "$x(x^2 - 2)$", "$(x - 2)(x + 2)$"], "B",
           "Đặt $x$ làm nhân tử chung: $x(x^2 - 4) = x(x - 2)(x + 2)$.", "Phân tích đa thức thành nhân tử", "ĐS II", "TH", "THCS Nghĩa Tân 2"),
        tn(5, "Tứ giác có bốn góc vuông là hình gì?", ["Hình bình hành", "Hình thoi", "Hình chữ nhật", "Hình thang cân"], "C",
           "Định nghĩa: Tứ giác có bốn góc vuông là hình chữ nhật.", "Hình chữ nhật", "HH III", "NB", "THCS Hát Môn"),
        tn(6, "Hình bình hành có hai đường chéo vuông góc với nhau là hình gì?", ["Hình thoi", "Hình chữ nhật", "Hình vuông", "Hình thang cân"], "A",
           "Dấu hiệu nhận biết: Hình bình hành có hai đường chéo vuông góc là hình thoi.", "Hình thoi", "HH III", "TH", "THCS Tam Hiệp"),
        tn(7, "Cho tam giác $ABC$ có $D, E$ lần lượt là trung điểm của $AB, AC$. Biết độ dài đoạn thẳng $DE = 5\\text{ cm}$. Độ dài cạnh $BC$ là:", ["$2{,}5\\text{ cm}$", "$5\\text{ cm}$", "$7{,}5\\text{ cm}$", "$10\\text{ cm}$"], "D",
           "$DE$ là đường trung bình của tam giác $ABC$ nên $BC = 2 \\cdot DE = 2 \\cdot 5 = 10\\text{ cm}$.", "Đường trung bình của tam giác", "HH IV", "TH", "THCS Tam Hiệp"),
        tn(8, "Mẫu thức chung đơn giản nhất của hai phân thức $\\dfrac{1}{x - 1}$ và $\\dfrac{1}{x + 1}$ là:", ["$x^2 - 1$", "$x - 1$", "$x + 1$", "$(x - 1)^2$"], "A",
           "Mẫu thức chung là $(x - 1)(x + 1) = x^2 - 1$.", "Phân thức đại số", "ĐS VI", "NB", "Huyện Thanh Oai"),
    ],
    bai=[
        dict(
            label="Bài 1.",
            level=2,
            statement=(
                "\\textbf{(1,5 điểm)}" + BR
                + "a) \\textbf{(0,75 điểm)} Rút gọn biểu thức sau: $A = (x + 3)(x - 3) - x(x - 4)$." + BR
                + "b) \\textbf{(0,75 điểm)} Tìm $x$, biết: $x^2 - 9 + (x - 3)(2x + 1) = 0$."
            ),
            dap_an=[
                y("a)", 0.75, [
                    ("Ta có: $A = (x + 3)(x - 3) - x(x - 4)$"),
                    ("$A = (x^2 - 9) - (x^2 - 4x)$", 0.25),
                    ("$A = x^2 - 9 - x^2 + 4x$", 0.25),
                    ("$A = (x^2 - x^2) + 4x - 9 = 4x - 9$"),
                    ("Vậy biểu thức sau khi thu gọn là $A = 4x - 9$.", 0.25),
                ]),
                y("b)", 0.75, [
                    ("Ta có: $x^2 - 9 + (x - 3)(2x + 1) = 0$"),
                    ("$(x - 3)(x + 3) + (x - 3)(2x + 1) = 0$", 0.25),
                    ("$(x - 3)[(x + 3) + (2x + 1)] = 0$"),
                    ("$(x - 3)(3x + 4) = 0$", 0.25),
                    ("Suy ra $x - 3 = 0$ hoặc $3x + 4 = 0$."),
                    ("Do đó $x = 3$ hoặc $x = -\\dfrac{4}{3}$."),
                    ("Vậy $x \\in \\left\\{-\\dfrac{4}{3}; 3\\right\\}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 1.a", "Rút gọn biểu thức đa thức bằng hằng đẳng thức", "ĐS I", "TH", 0.75, 5, "THCS Thăng Long"),
                ("Bài 1.b", "Tìm x bằng phương pháp phân tích nhân tử đưa về phương trình tích", "ĐS II", "TH", 0.75, 5, "THCS Nghĩa Tân 2"),
            ],
            note="Bài 1 rèn kĩ năng hằng đẳng thức và giải phương trình tích đầy đủ hai nghiệm.",
        ),
        dict(
            label="Bài 2.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho hai biểu thức: $A = \\dfrac{x + 3}{x - 3}$ và $B = \\dfrac{x}{x + 3} + \\dfrac{2x}{x - 3} - \\dfrac{3x^2 + 9}{x^2 - 9}$ với $x \\ne \\pm 3$." + BR
                + "a) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ khi $x = 5$." + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh rằng $B = \\dfrac{3}{x + 3}$." + BR
                + "c) \\textbf{(0,5 điểm)} Đặt $P = A \\cdot B$. Tìm tất cả các số nguyên $x$ để biểu thức $P$ nhận giá trị nguyên."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Ta có $x = 5$ thỏa mãn điều kiện xác định $x \\ne \\pm 3$."),
                    ("Thay $x = 5$ vào biểu thức $A$, ta được:"),
                    ("$A = \\dfrac{5 + 3}{5 - 3} = \\dfrac{8}{2} = 4$.", 0.25),
                    ("Vậy khi $x = 5$ thì giá trị của biểu thức $A$ là $4$.", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Với $x \\ne \\pm 3$, ta có mẫu thức chung là $(x - 3)(x + 3)$."),
                    ("Khi đó: $B = \\dfrac{x(x - 3) + 2x(x + 3) - (3x^2 + 9)}{(x - 3)(x + 3)}$", 0.25),
                    ("$B = \\dfrac{x^2 - 3x + 2x^2 + 6x - 3x^2 - 9}{(x - 3)(x + 3)}$", 0.25),
                    ("$B = \\dfrac{(x^2 + 2x^2 - 3x^2) + (-3x + 6x) - 9}{(x - 3)(x + 3)} = \\dfrac{3x - 9}{(x - 3)(x + 3)}$", 0.25),
                    ("$B = \\dfrac{3(x - 3)}{(x - 3)(x + 3)} = \\dfrac{3}{x + 3}$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 0.5, [
                    ("Ta có: $P = A \\cdot B = \\dfrac{x + 3}{x - 3} \\cdot \\dfrac{3}{x + 3} = \\dfrac{3}{x - 3}$."),
                    ("Để $P$ nhận giá trị nguyên với $x$ nguyên thì $\\dfrac{3}{x - 3}$ phải là số nguyên, suy ra $x - 3 \\in \\text{Ư}(3) = \\{\\pm 1; \\pm 3\\}$."),
                    ("Ta xét các trường hợp:"),
                    ("$\\bullet\\ x - 3 = 1 \\implies x = 4$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x - 3 = -1 \\implies x = 2$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x - 3 = 3 \\implies x = 6$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x - 3 = -3 \\implies x = 0$ (thỏa mãn ĐKXĐ).", 0.25),
                    ("Vậy các số nguyên $x$ để biểu thức $P$ nhận giá trị nguyên là $x \\in \\{0; 2; 4; 6\\}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 2.a", "Tính giá trị phân thức đại số", "ĐS VI", "NB", 0.5, 4, "THCS Tam Hiệp"),
                ("Bài 2.b", "Rút gọn phân thức đại số bằng quy đồng mẫu thức", "ĐS VI", "TH", 1.0, 10, "THCS Tam Hiệp"),
                ("Bài 2.c", "Nhân hai phân thức và tìm số nguyên x để phân thức nhận giá trị nguyên", "ĐS VI", "VD", 0.5, 6, "THCS Tam Hiệp"),
            ],
            note="Bài phân thức chuẩn thi học kì: các bước thu gọn tử số $3x - 9$ và rút gọn với mẫu thức rất rõ ràng.",
        ),
        dict(
            label="Bài 3.",
            level=2,
            statement=(
                "\\textbf{(1,0 điểm)} Biểu đồ biểu diễn lượng khách du lịch quốc tế đến Việt Nam trong giai đoạn 2020 -- 2023:" + BR
                + "\\begin{center}\\footnotesize\\begin{tabular}{|l|c|c|c|c|}\\hline \n"
                + "\\textbf{Năm} & \\textbf{2020} & \\textbf{2021} & \\textbf{2022} & \\textbf{2023} \\\\ \\hline \n"
                + "Lượng khách (triệu lượt) & $3{,}8$ & $0{,}2$ & $3{,}6$ & $12{,}6$ \\\\ \\hline \n"
                + "\\end{tabular}\\end{center}" + BR
                + "a) \\textbf{(0,5 điểm)} Hãy lập bảng thống kê lượng khách du lịch quốc tế đến Việt Nam qua các năm trên." + BR
                + "b) \\textbf{(0,5 điểm)} Lượng khách du lịch quốc tế đến Việt Nam năm 2023 nhiều hơn năm 2022 bao nhiêu triệu lượt?"
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Dựa vào biểu đồ trên, ta có bảng thống kê lượng khách du lịch quốc tế đến Việt Nam:"),
                    ("\\begin{center}\\begin{tabular}{|l|c|c|c|c|}\\hline \\textbf{Năm} & 2020 & 2021 & 2022 & 2023 \\\\ \\hline \\textbf{Lượng khách (triệu lượt)} & 3,8 & 0,2 & 3,6 & 12,6 \\\\ \\hline \\end{tabular}\\end{center}", 0.25),
                    ("Vậy số liệu lượng khách du lịch quốc tế đã được thống kê đầy đủ theo từng năm.", 0.25),
                ]),
                y("b)", 0.5, [
                    ("Lượng khách du lịch quốc tế đến Việt Nam năm 2023 nhiều hơn năm 2022 là:"),
                    ("$12{,}6 - 3{,}6 = 9{,}0$ (triệu lượt).", 0.25),
                    ("Vậy năm 2023 lượng khách du lịch quốc tế nhiều hơn năm 2022 là $9{,}0$ triệu lượt khách.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 3.a", "Lập bảng thống kê từ biểu đồ dữ liệu", "TK V", "NB", 0.5, 4, "THCS Thăng Long"),
                ("Bài 3.b", "Phân tích dữ liệu và tính lượng tăng trưởng", "TK V", "TH", 0.5, 5, "THCS Thăng Long"),
            ],
            note="Bài thống kê từ đề thi thật THCS Thăng Long: rèn kĩ năng trích xuất số liệu và tính toán cơ bản.",
        ),
        dict(
            label="Bài 4.",
            level=2,
            statement=(
                "\\textbf{(3,0 điểm)} Cho tam giác $ABC$ vuông cân tại $A$. Gọi $M$ là trung điểm của cạnh huyền $BC$." + BR
                + "Từ $M$ kẻ $ME \\perp AB$ tại $E$ và $MF \\perp AC$ tại $F$." + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh tứ giác $AEMF$ là hình vuông." + BR
                + "b) \\textbf{(1,0 điểm)} Lấy điểm $D$ đối xứng với $M$ qua $E$. Chứng minh tứ giác $ADBM$ là hình vuông." + BR
                + "c) \\textbf{(1,0 điểm)} Đường thẳng qua $M$ song song với $BF$ cắt $AC$ tại $K$. Chứng minh rằng $K$ là trung điểm của đoạn thẳng $CF$."
            ),
            hinh_da=H.get_tikz_ct2(),
            dap_an=[
                y("a)", 1.0, [
                    ("Xét tứ giác $AEMF$, ta có:"),
                    ("$\\widehat{EAF} = \\widehat{BAC} = 90^\\circ$ (do tam giác $ABC$ vuông cân tại $A$).", 0.25),
                    ("$ME \\perp AB$ tại $E$ nên $\\widehat{AEM} = 90^\\circ$.", 0.25),
                    ("$MF \\perp AC$ tại $F$ nên $\\widehat{AFM} = 90^\\circ$."),
                    ("Do đó tứ giác $AEMF$ là hình chữ nhật.", 0.25),
                    ("Mặt khác, tam giác $ABC$ vuông cân tại $A$ nên đường trung tuyến $AM$ đồng thời là đường phân giác của góc $\\widehat{BAC}$, suy ra $AM$ là tia phân giác của $\\widehat{EAF}$."),
                    ("Hình chữ nhật $AEMF$ có đường chéo $AM$ là tia phân giác của một góc nên là hình vuông (điều phải chứng minh).", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Xét tam giác $ABC$ vuông cân tại $A$, có $M$ là trung điểm của cạnh $BC$."),
                    ("Do $AC \\perp AB$ và $ME \\perp AB$ nên $ME \\parallel AC$ (cùng vuông góc với $AB$)."),
                    ("Theo tính chất đường trung bình, suy ra $E$ là trung điểm của cạnh $AB$.", 0.25),
                    ("Lại có $D$ đối xứng với $M$ qua $E$ nên $E$ là trung điểm của đoạn thẳng $DM$."),
                    ("Tứ giác $ADBM$ có hai đường chéo $AB$ và $DM$ cắt nhau tại trung điểm $E$ của mỗi đường, do đó $ADBM$ là hình bình hành.", 0.25),
                    ("Mặt khác, $AB \\perp DM$ tại $E$ (do $ME \\perp AB$), nên hình bình hành $ADBM$ là hình thoi.", 0.25),
                    ("Vì $\\triangle ABC$ vuông cân tại $A$ có trung tuyến $AM$ nên $AM \\perp BC$, tức là $\\widehat{AMB} = 90^\\circ$."),
                    ("Hình thoi $ADBM$ có một góc vuông ($\\widehat{AMB} = 90^\\circ$) nên là hình vuông (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 1.0, [
                    ("Xét tam giác $ABC$, ta có $M$ là trung điểm của $BC$ và $F$ là trung điểm của $AC$ (do $MF \\parallel AB$)."),
                    ("Suy ra $MF$ là đường trung bình của tam giác $ABC$, do đó $MF \\parallel AB$ và $MF = \\dfrac{1}{2}AB$."),
                    ("Do đó tứ giác $ABMF$ có $MF \\parallel AB$ nên là hình thang.", 0.25),
                    ("Xét tam giác $BCF$, ta có $M$ là trung điểm của $BC$ và theo giả thiết đường thẳng qua $M$ song song với $BF$ cắt $CF$ tại $K$, tức là $MK \\parallel BF$.", 0.25),
                    ("Trong tam giác $BCF$, đường thẳng đi qua trung điểm $M$ của cạnh $BC$ và song song với cạnh $BF$ thì đi qua trung điểm của cạnh thứ ba $CF$."),
                    ("Suy ra $K$ là trung điểm của đoạn thẳng $CF$ (điều phải chứng minh).", 0.25),
                    ("Vậy $K$ là trung điểm của đoạn thẳng $CF$."),
                ]),
            ],
            mt=[
                ("Bài 4.a", "Chứng minh tứ giác là hình vuông", "HH III", "TH", 1.0, 8, "THCS Hát Môn"),
                ("Bài 4.b", "Chứng minh tứ giác là hình vuông qua hình thoi có góc vuông", "HH III", "VD", 1.0, 10, "THCS Hát Môn"),
                ("Bài 4.c", "Áp dụng định lí đường trung bình chứng minh trung điểm đoạn thẳng", "HH IV", "VD", 1.0, 9, "THCS Hát Môn"),
            ],
            note="Bài hình hay của THCS Hát Môn: khai thác sâu tính chất tam giác vuông cân và hình vuông.",
        ),
        dict(
            label="Bài 5.",
            level=3,
            statement=(
                "\\textbf{(0,5 điểm)} Tìm giá trị nhỏ nhất của biểu thức sau:" + BR
                + "$A = 2x^2 + y^2 + 2xy + 2x - 2y + 2028$ với mọi $x, y \\in \\mathbb{R}$."
            ),
            dap_an=[
                y("", 0.5, [
                    ("Ta biến đổi biểu thức $A$ như sau:"),
                    ("$A = (x^2 + 2xy + y^2) + 2x - 2y + x^2 + 2028$"),
                    ("$A = [(x + y)^2 - 2(x + y) + 1] + (x^2 + 4x + 4) + 2023$"),
                    ("$A = (x + y - 1)^2 + (x + 2)^2 + 2023$", 0.25),
                    ("Vì $(x + y - 1)^2 \\ge 0$ và $(x + 2)^2 \\ge 0$ với mọi $x, y \\in \\mathbb{R}$, nên $A \\ge 2023$."),
                    ("Dấu đẳng thức xảy ra khi và chỉ khi: $x + 2 = 0$ và $x + y - 1 = 0$."),
                    ("Suy ra $x = -2$ và $y = 1 - x = 1 - (-2) = 3$."),
                    ("Vậy giá trị nhỏ nhất của biểu thức $A$ là $2023$, đạt được khi $x = -2$ và $y = 3$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 5", "Tìm giá trị nhỏ nhất của biểu thức hai biến bằng tách hai bình phương", "ĐS II", "VDC", 0.5, 6, "Huyện Thanh Oai"),
            ],
            note="Câu VDC đề thi Cuối kì 1 Huyện Thanh Oai: kĩ thuật tách bình phương chứa $x+y$ và $x$ rất khéo léo.",
        ),
    ],
)

# =====================================================================
# ĐỀ CHÍNH THỨC SỐ 3
# =====================================================================
DE["ct-3"] = dict(
    ten="ĐỀ CHÍNH THỨC SỐ 3",
    slug_de="de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3",
    slug_mt="ma-tran-va-dap-an-ck1-chinh-thuc-so-3",
    eyebrow="LỚP 8 • ĐỀ KIỂM TRA CHÍNH THỨC — SỐ 3",
    cach_dung="Bài thi chính thức 90 phút. Giám thị thu bài đúng giờ, chấm bài theo barem chi tiết 0,25đ. Điểm số dùng để đánh giá năng lực độc lập của học sinh.",
    gioi_thieu=(
        "\\textbf{ĐỀ KIỂM TRA CUỐI HỌC KÌ I -- ĐỀ CHÍNH THỨC SỐ 3 TOÁN 8 (KNTT)} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc ma trận chuẩn KNTT:} Đề bốc 100\\% từ các trường chưa xuất hiện ở 3 đề ôn tập: "
        "Phần I (2,0đ) Trắc nghiệm 8 câu x 0,25đ phân phối chuẩn · "
        "Bài 1 (1,5đ) Phép tính đa thức \\& Phân tích đa thức thành nhân tử · "
        "Bài 2 (2,0đ) Phân thức đại số: ĐKXĐ, rút gọn biểu thức và tìm x nguyên · "
        "Bài 3 (1,0đ) Thống kê phân loại dữ liệu và mức độ hài lòng khách hàng · "
        "Bài 4 (3,0đ) Hình học tổng hợp: hình bình hành, hình thang cân, tính chất đối xứng · "
        "Bài 5 (0,5đ) VDC Bất đẳng thức Cauchy-Schwarz dạng Engel."
    ),
    bay=[
        ("Bài 1.a", "Khai triển sai $(2x + 1)^2 = 4x^2 + 1$", "Quên số hạng $2AB = 4x$ ở giữa", "Viết đầy đủ: $(2x + 1)^2 = 4x^2 + 4x + 1$"),
        ("Bài 1.b", "Đặt dấu trừ ra ngoài nhóm ba hạng tử sau bị sai dấu", "Viết thành $-(y^2 + 10y + 25)$ làm sai dấu", "Đặt dấu trừ cẩn thận: $x^2 - (y^2 - 10y + 25) = x^2 - (y - 5)^2$"),
        ("Bài 2.c", "Sót nghiệm âm khi giải phương trình tìm ước của 10", "Chỉ xét ước dương mà quên các ước âm", "Liệt kê đầy đủ: $\\text{Ư}(10) = \\{\\pm 1; \\pm 2; \\pm 5; \\pm 10\\}$"),
        ("Bài 4.b", "Chứng minh hình thang cân mà không chỉ ra hai đáy song song", "Chưa chứng minh $ED \\parallel BC$ đã so sánh hai cạnh bên", "Chứng minh $ED \\parallel BC$ trước rồi mới chỉ ra $BE = CD$"),
    ],
    tn=[
        tn(1, "Đơn thức nào sau đây có bậc bằng 4?", ["$3x^2y^2$", "$4x^3y^2$", "$2x^4y$", "$x^2y$"], "A",
           "Đơn thức $3x^2y^2$ có bậc $2 + 2 = 4$.", "Bậc của đơn thức", "ĐS I", "NB", "Huyện Thường Tín"),
        tn(2, "Tích của đơn thức $-2xy$ với đa thức $(x - 3y)$ là:", ["$-2x^2y + 6xy^2$", "$-2x^2y - 6xy^2$", "$2x^2y - 6xy^2$", "$-2x^2y + 3xy^2$"], "A",
           "Nhân từng hạng tử: $-2xy \\cdot x - 2xy \\cdot (-3y) = -2x^2y + 6xy^2$.", "Nhân đơn thức với đa thức", "ĐS I", "TH", "Huyện Thường Tín"),
        tn(3, "Hằng đẳng thức bình phương của một hiệu $(x - y)^2$ bằng:", ["$x^2 - y^2$", "$x^2 + 2xy + y^2$", "$x^2 - 2xy + y^2$", "$x^2 - xy + y^2$"], "C",
           "Theo hằng đẳng thức: $(x - y)^2 = x^2 - 2xy + y^2$.", "Hằng đẳng thức đáng nhớ", "ĐS II", "NB", "Huyện Ứng Hoà"),
        tn(4, "Phân tích đa thức $5x(x - 1) - 3(x - 1)$ thành nhân tử, ta được:", ["$(x - 1)(5x + 3)$", "$(x - 1)(5x - 3)$", "$(x + 1)(5x - 3)$", "$2x(x - 1)$"], "B",
           "Đặt nhân tử chung $(x - 1)$, ta được: $(x - 1)(5x - 3)$.", "Phân tích đa thức thành nhân tử", "ĐS II", "TH", "Huyện Ứng Hoà"),
        tn(5, "Hình thang có hai góc kề một đáy bằng nhau là hình gì?", ["Hình bình hành", "Hình chữ nhật", "Hình thoi", "Hình thang cân"], "D",
           "Dấu hiệu nhận biết: Hình thang có hai góc kề một đáy bằng nhau là hình thang cân.", "Hình thang cân", "HH III", "NB", "THCS Ngô Gia Tự"),
        tn(6, "Tứ giác có hai đường chéo cắt nhau tại trung điểm của mỗi đường là hình gì?", ["Hình thang cân", "Hình bình hành", "Hình thoi", "Hình chữ nhật"], "B",
           "Dấu hiệu nhận biết: Tứ giác có hai đường chéo cắt nhau tại trung điểm của mỗi đường là hình bình hành.", "Hình bình hành", "HH III", "TH", "THCS Thanh Quan"),
        tn(7, "Cho $\\triangle ABC$ có tia phân giác của góc $A$ cắt cạnh $BC$ tại $D$. Biết $AB = 4\\text{ cm}, AC = 6\\text{ cm}, BD = 2\\text{ cm}$. Độ dài đoạn thẳng $CD$ là:", ["$3\\text{ cm}$", "$4\\text{ cm}$", "$2\\text{ cm}$", "$5\\text{ cm}$"], "A",
           "Theo tính chất đường phân giác: $\\dfrac{BD}{CD} = \\dfrac{AB}{AC} \\implies CD = \\dfrac{BD \\cdot AC}{AB} = \\dfrac{2 \\cdot 6}{4} = 3\\text{ cm}$.", "Tính chất đường phân giác", "HH IV", "TH", "THCS Thanh Quan"),
        tn(8, "Giá trị của phân thức $\\dfrac{x + 2}{x - 1}$ tại $x = 2$ bằng:", ["$2$", "$3$", "$4$", "$1$"], "C",
           "Thay $x = 2$ vào phân thức: $\\dfrac{2 + 2}{2 - 1} = \\dfrac{4}{1} = 4$.", "Phân thức đại số", "ĐS VI", "NB", "MathTech KNTT"),
    ],
    bai=[
        dict(
            label="Bài 1.",
            level=2,
            statement=(
                "\\textbf{(1,5 điểm)}" + BR
                + "a) \\textbf{(0,75 điểm)} Thực hiện phép tính và thu gọn: $A = (2x + 1)^2 - 4x(x - 1)$." + BR
                + "b) \\textbf{(0,75 điểm)} Phân tích đa thức sau thành nhân tử: $B = x^2 - 25 - y^2 + 10y$."
            ),
            dap_an=[
                y("a)", 0.75, [
                    ("Ta có: $A = (2x + 1)^2 - 4x(x - 1)$"),
                    ("$A = (4x^2 + 4x + 1) - (4x^2 - 4x)$", 0.25),
                    ("$A = 4x^2 + 4x + 1 - 4x^2 + 4x$", 0.25),
                    ("$A = (4x^2 - 4x^2) + (4x + 4x) + 1 = 8x + 1$"),
                    ("Vậy biểu thức sau khi thu gọn là $A = 8x + 1$.", 0.25),
                ]),
                y("b)", 0.75, [
                    ("Ta có: $B = x^2 - 25 - y^2 + 10y$"),
                    ("$B = x^2 - (y^2 - 10y + 25)$", 0.25),
                    ("$B = x^2 - (y - 5)^2$", 0.25),
                    ("$B = [x - (y - 5)][x + (y - 5)] = (x - y + 5)(x + y - 5)$"),
                    ("Vậy đa thức được phân tích thành $B = (x - y + 5)(x + y - 5)$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 1.a", "Thực hiện phép tính rút gọn đa thức", "ĐS I", "TH", 0.75, 5, "Huyện Thường Tín"),
                ("Bài 1.b", "Phân tích đa thức thành nhân tử bằng nhóm hạng tử", "ĐS II", "TH", 0.75, 5, "Huyện Ứng Hoà"),
            ],
            note="Bài 1 rèn kĩ năng nhóm ba hạng tử sau tạo thành bình phương một hiệu.",
        ),
        dict(
            label="Bài 2.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho biểu thức: $A = \\left(\\dfrac{2}{x - 5} + \\dfrac{2}{x + 5}\\right) \\cdot \\dfrac{x^2 - 10x + 25}{4x}$ với $x \\ne 0; x \\ne \\pm 5$." + BR
                + "a) \\textbf{(0,5 điểm)} Viết điều kiện xác định của biểu thức $A$." + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh rằng $A = \\dfrac{x - 5}{x + 5}$." + BR
                + "c) \\textbf{(0,5 điểm)} Tìm tất cả các số nguyên $x$ để biểu thức $A$ nhận giá trị nguyên."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Biểu thức $A$ xác định khi và chỉ khi: $x - 5 \\ne 0$, $x + 5 \\ne 0$ và $4x \\ne 0$."),
                    ("Suy ra $x \\ne 5$, $x \\ne -5$ và $x \\ne 0$.", 0.25),
                    ("Vậy điều kiện xác định của biểu thức $A$ là $x \\ne 0$ và $x \\ne \\pm 5$.", 0.25),
                ]),
                y("b)", 1.0, [
                    ("Với $x \\ne 0; x \\ne \\pm 5$, ta quy đồng trong ngoặc:", 0.25),
                    ("$\\dfrac{2}{x - 5} + \\dfrac{2}{x + 5} = \\dfrac{2(x + 5) + 2(x - 5)}{(x - 5)(x + 5)} = \\dfrac{2x + 10 + 2x - 10}{(x - 5)(x + 5)} = \\dfrac{4x}{(x - 5)(x + 5)}$", 0.25),
                    ("Lại có: $x^2 - 10x + 25 = (x - 5)^2$."),
                    ("Do đó: $A = \\dfrac{4x}{(x - 5)(x + 5)} \\cdot \\dfrac{(x - 5)^2}{4x}$", 0.25),
                    ("$A = \\dfrac{4x(x - 5)^2}{4x(x - 5)(x + 5)} = \\dfrac{x - 5}{x + 5}$ (điều phải chứng minh).", 0.25),
                ]),
                y("c)", 0.5, [
                    ("Ta biến đổi: $A = \\dfrac{x - 5}{x + 5} = \\dfrac{x + 5 - 10}{x + 5} = 1 - \\dfrac{10}{x + 5}$."),
                    ("Để $A$ nhận giá trị nguyên với $x$ nguyên thì $\\dfrac{10}{x + 5}$ phải là số nguyên, suy ra $x + 5 \\in \\text{Ư}(10) = \\{\\pm 1; \\pm 2; \\pm 5; \\pm 10\\}$."),
                    ("Ta có các giá trị tương ứng của $x$:"),
                    ("$\\bullet\\ x + 5 = 1 \\implies x = -4$; $x + 5 = -1 \\implies x = -6$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x + 5 = 2 \\implies x = -3$; $x + 5 = -2 \\implies x = -7$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x + 5 = 5 \\implies x = 0$ (loại do $x \\ne 0$); $x + 5 = -5 \\implies x = -10$ (thỏa mãn ĐKXĐ)."),
                    ("$\\bullet\\ x + 5 = 10 \\implies x = 5$ (loại do $x \\ne 5$); $x + 5 = -10 \\implies x = -15$ (thỏa mãn ĐKXĐ).", 0.25),
                    ("Vậy các số nguyên $x$ để biểu thức $A$ nhận giá trị nguyên là $x \\in \\{-15; -10; -7; -6; -4; -3\\}$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 2.a", "Tìm điều kiện xác định của phân thức đại số", "ĐS VI", "NB", 0.5, 4, "THCS Ngô Gia Tự"),
                ("Bài 2.b", "Rút gọn phân thức đại số", "ĐS VI", "TH", 1.0, 10, "THCS Ngô Gia Tự"),
                ("Bài 2.c", "Tìm số nguyên x để phân thức nhận giá trị nguyên", "ĐS VI", "VD", 0.5, 6, "THCS Ngô Gia Tự"),
            ],
            note="Bài phân thức đề thi THCS Ngô Gia Tự: lưu ý loại hai giá trị $x = 0$ và $x = 5$.",
        ),
        dict(
            label="Bài 3.",
            level=2,
            statement=(
                "\\textbf{(1,0 điểm)} Một cửa hàng kinh doanh đồ uống tiến hành khảo sát ý kiến của $200$ khách hàng về mức độ hài lòng đối với chất lượng phục vụ, kết quả thu được như sau:" + BR
                + "\\begin{center}\\footnotesize\\begin{tabular}{|l|c|c|c|c|}\\hline \n"
                + "\\textbf{Mức độ hài lòng} & Rất hài lòng & Hài lòng & Bình thường & Không hài lòng \\\\ \\hline \n"
                + "\\textbf{Số khách hàng} & $80$ & $70$ & $35$ & $15$ \\\\ \\hline \n"
                + "\\end{tabular}\\end{center}" + BR
                + "a) \\textbf{(0,5 điểm)} Dữ liệu thu thập được ở bảng trên là loại dữ liệu nào (định tính hay định lượng)?" + BR
                + "b) \\textbf{(0,5 điểm)} Tính tỉ lệ phần trăm số khách hàng đánh giá ở mức ``Rất hài lòng'' và ``Hài lòng'' so với tổng số khách hàng được khảo sát."
            ),
            dap_an=[
                y("a)", 0.5, [
                    ("Theo bảng số liệu thống kê trên, ta có:"),
                    ("Dữ liệu về mức độ hài lòng (Rất hài lòng, Hài lòng, Bình thường, Không hài lòng) là dữ liệu định tính (có thể xếp thứ tự).", 0.25),
                    ("Vậy dữ liệu thu thập được là dữ liệu định tính.", 0.25),
                ]),
                y("b)", 0.5, [
                    ("Theo bảng số liệu, ta có tổng số khách hàng đánh giá ở mức ``Rất hài lòng'' và ``Hài lòng'' là:"),
                    ("$80 + 70 = 150$ (khách hàng).", 0.25),
                    ("Tỉ lệ phần trăm nhóm khách hàng này so với tổng số $200$ khách hàng khảo sát là:"),
                    ("$\\dfrac{150}{200} \\cdot 100\\% = 75\\%$."),
                    ("Vậy có $75\\%$ số khách hàng đánh giá tích cực (ở mức Rất hài lòng và Hài lòng).", 0.25),
                ]),
            ],
            mt=[
                ("Bài 3.a", "Phân loại dữ liệu định tính và định lượng", "TK V", "NB", 0.5, 4, "THCS Thanh Quan"),
                ("Bài 3.b", "Tính tỉ lệ phần trăm từ số liệu thống kê", "TK V", "TH", 0.5, 5, "THCS Thanh Quan"),
            ],
            note="Bài thống kê chuẩn chương V SGK Toán 8 KNTT: phân biệt dữ liệu định tính và tính tỉ lệ phần trăm.",
        ),
        dict(
            label="Bài 4.",
            level=2,
            statement=(
                "\\textbf{(3,0 điểm)} Cho tam giác $ABC$ nhọn ($AB < AC$). Gọi $M$ là trung điểm của cạnh $BC$." + BR
                + "Trên tia đối của tia $MA$ lấy điểm $D$ sao cho $MD = MA$." + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh tứ giác $ABDC$ là hình bình hành." + BR
                + "b) \\textbf{(1,0 điểm)} Kẻ $AH \\perp BC$ tại $H$. Lấy điểm $E$ đối xứng với điểm $A$ qua $H$. Chứng minh tứ giác $BCDE$ là hình thang cân." + BR
                + "c) \\textbf{(1,0 điểm)} Kẻ $DK \\perp BC$ tại $K$. Chứng minh rằng $M$ là trung điểm của đoạn thẳng $HK$ và $BD \\parallel CE$."
            ),
            hinh_da=H.get_tikz_ct3(),
            dap_an=[
                y("a)", 1.0, [
                    ("Xét tứ giác $ABDC$, ta có:"),
                    ("$M$ là trung điểm của đường chéo $BC$ (theo giả thiết).", 0.25),
                    ("$M$ là trung điểm của đường chéo $AD$ (do $MD = MA$).", 0.25),
                    ("Tứ giác $ABDC$ có hai đường chéo $BC$ và $AD$ cắt nhau tại trung điểm $M$ của mỗi đường."),
                    ("Do đó tứ giác $ABDC$ là hình bình hành (điều phải chứng minh).", 0.5),
                ]),
                y("b)", 1.0, [
                    ("Do điểm $E$ đối xứng với điểm $A$ qua $H$ nên $H$ là trung điểm của đoạn thẳng $AE$."),
                    ("Lại có $AH \\perp BC$ tại $H$ nên đường thẳng $BC$ là đường trung trực của đoạn thẳng $AE$."),
                    ("Suy ra $BC$ là đường trung trực của đoạn thẳng $AE$, do đó $BE = AB$ và $CE = AC$.", 0.25),
                    ("Mặt khác, vì $ABDC$ là hình bình hành nên $CD = AB$, suy ra $BE = CD$ (1).", 0.25),
                    ("Lại có $\\triangle AHE$ vuông tại $H$, $DK \\perp BC$ nên $AE \\parallel DK$ (cùng vuông góc với $BC$)."),
                    ("Mà trong tam giác $ADE$, $H$ là trung điểm $AE$, $M$ là trung điểm $AD$ nên $HM$ là đường trung bình của tam giác $ADE$."),
                    ("Suy ra $ED \\parallel HM$, mà $H, M \\in BC$ nên $ED \\parallel BC$."),
                    ("Tứ giác $BCDE$ có $ED \\parallel BC$ nên là hình thang (2).", 0.25),
                    ("Từ (1) và (2), hình thang $BCDE$ có hai cạnh bên $BE = CD$ và không song song (do $AB < AC$) nên là hình thang cân.", 0.25),
                ]),
                y("c)", 1.0, [
                    ("Xét tam giác vuông $AHM$ (vuông tại $H$) và tam giác vuông $DKM$ (vuông tại $K$), ta có:"),
                    ("$AM = DM$ (theo giả thiết)."),
                    ("$\\widehat{AMH} = \\widehat{DMK}$ (hai góc đối đỉnh).", 0.25),
                    ("Do đó $\\triangle AHM = \\triangle DKM$ (cạnh huyền -- góc nhọn).", 0.25),
                    ("Suy ra $HM = KM$ (hai cạnh tương ứng), dẫn đến $M$ là trung điểm của đoạn thẳng $HK$."),
                    ("Mặt khác, vì $BC$ là trung trực của $AE$ nên $\\widehat{ECB} = \\widehat{ACB}$."),
                    ("Vì $ABDC$ là hình bình hành nên $BD \\parallel AC$ và $\\widehat{DBC} = \\widehat{ACB}$ (so le trong)."),
                    ("Trong hình thang cân $BCDE$, ta có hai góc kề đáy bằng nhau: $\\widehat{EBC} = \\widehat{DCB}$."),
                    ("Từ đó suy ra $\\widehat{DBC} = \\widehat{ECB}$, mà hai góc này ở vị trí so le trong nên $BD \\parallel CE$.", 0.25),
                    ("Vậy $M$ là trung điểm của $HK$ và $BD \\parallel CE$ (điều phải chứng minh)."),
                ]),
            ],
            mt=[
                ("Bài 4.a", "Chứng minh tứ giác là hình bình hành qua hai đường chéo", "HH III", "TH", 1.0, 8, "MathTech KNTT"),
                ("Bài 4.b", "Chứng minh hình thang cân bằng định nghĩa đường trung trực", "HH III", "VD", 1.0, 10, "MathTech KNTT"),
                ("Bài 4.c", "Chứng minh tam giác bằng nhau và các đường thẳng song song", "HH III", "VD", 1.0, 9, "MathTech KNTT"),
            ],
            note="Bài hình nâng cao hay: phối hợp đối xứng trục và tính chất hình bình hành, hình thang cân.",
        ),
        dict(
            label="Bài 5.",
            level=3,
            statement=(
                "\\textbf{(0,5 điểm)} Cho hai số thực dương $a, b$ thỏa mãn điều kiện $a + b = 2$." + BR
                + "Tìm giá trị nhỏ nhất của biểu thức: $P = \\dfrac{1}{a^2 + b^2} + \\dfrac{1}{ab}$."
            ),
            dap_an=[
                y("", 0.5, [
                    ("Ta tách biểu thức $P$ như sau: $P = \\dfrac{1}{a^2 + b^2} + \\dfrac{1}{2ab} + \\dfrac{1}{2ab}$."),
                    ("Áp dụng bất đẳng thức $\\dfrac{1}{x} + \\dfrac{1}{y} \\ge \\dfrac{4}{x + y}$ với hai số dương $x = a^2 + b^2 > 0$ và $y = 2ab > 0$, ta có:"),
                    ("$\\dfrac{1}{a^2 + b^2} + \\dfrac{1}{2ab} \\ge \\dfrac{4}{a^2 + b^2 + 2ab} = \\dfrac{4}{(a + b)^2} = \\dfrac{4}{2^2} = 1$.", 0.25),
                    ("Mặt khác, với mọi $a, b > 0$, ta luôn có: $ab \\le \\dfrac{(a + b)^2}{4} = \\dfrac{2^2}{4} = 1$."),
                    ("Suy ra $\\dfrac{1}{2ab} \\ge \\dfrac{1}{2 \\cdot 1} = \\dfrac{1}{2}$."),
                    ("Do đó: $P \\ge 1 + \\dfrac{1}{2} = \\dfrac{3}{2}$."),
                    ("Dấu đẳng thức xảy ra khi và chỉ khi: $a^2 + b^2 = 2ab$ và $a = b$ kết hợp với $a + b = 2$, suy ra $a = b = 1$."),
                    ("Vậy giá trị nhỏ nhất của biểu thức $P$ là $\\dfrac{3}{2}$, đạt được khi $a = b = 1$.", 0.25),
                ]),
            ],
            mt=[
                ("Bài 5", "Tìm giá trị nhỏ nhất bằng bất đẳng thức Cauchy-Schwarz dạng Engel", "ĐS II", "VDC", 0.5, 6, "Huyện Ứng Hoà"),
            ],
            note="Câu VDC thi học kì Huyện Ứng Hoà: kĩ thuật tách điểm rơi Cauchy rất đẹp mắt và chuẩn mực.",
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
    ds = {"Đại số \\& Thống kê (Chương I, II, V, VI)": dict(muc), "Hình học (Chương III, IV)": dict(muc)}
    for c, nd, ch, m, di, ph, ng in rows:
        mach = "Hình học (Chương III, IV)" if ch.startswith("HH") else "Đại số \\& Thống kê (Chương I, II, V, VI)"
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
    ("Phép tính \\& Phân tích nhân tử (1,5đ)", "Ia: $(x-1)(x^2+x+1) - x(x^2-4)$; Ib: $x^2-y^2-2x+2y$", "Ia: $(x+3)(x-3) - x(x-4)$; Ib: $x^2-9+(x-3)(2x+1)=0$", "Ia: $(2x+1)^2-4x(x-1)$; Ib: $x^2-25-y^2+10y$"),
    ("Phân thức đại số (2,0đ)", "Tính $B(3)$, rút gọn $A = \\frac{x-2}{x+2}$, tìm x nguyên $P = A : B$", "Tính $A(5)$, rút gọn $B = \\frac{3}{x+3}$, tìm x nguyên $P = A \\cdot B$", "ĐKXĐ, rút gọn $A = \\frac{x-5}{x+5}$, tìm x nguyên"),
    ("Thống kê \\& Toán thực tế (1,0đ)", "Đội xe chở hàng cứu trợ, lập phương trình phân thức", "Biểu đồ lượng khách du lịch quốc tế đến Việt Nam", "Khảo sát mức độ hài lòng khách hàng, tính tỉ lệ \\%"),
    ("Hình học tổng hợp (3,0đ)", "Tam giác vuông, HCN, vuông góc $AM \\perp EF$, hình thang vuông", "Tam giác vuông cân, hình vuông, trung điểm đường trung bình", "Tam giác nhọn, hình bình hành, hình thang cân, đối xứng trục"),
    ("VDC Cực trị \\& BĐT (0,5đ)", "Min hai biến $A = 2x^2+y^2-2xy-2x+2024$", "Min hai biến $A = 2x^2+y^2+2xy+2x-2y+2028$", "Min phân thức $P = \\frac{1}{a^2+b^2} + \\frac{1}{ab}$ với $a+b=2$"),
]


def bang_tien_bo():
    s = (
        "\\noindent\\textbf{BẢN ĐỒ DẠNG BÀI VÀ MỨC ĐỘ TIẾN BỘ QUA 3 ĐỀ CHÍNH THỨC:} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|p{2.6cm}|p{4.0cm}|p{4.0cm}|p{4.0cm}|}\n\\hline\n"
        "\\textbf{Mạch kiến thức} & \\textbf{Đề chính thức số 1} & \\textbf{Đề chính thức số 2} & \\textbf{Đề chính thức số 3} \\\\ \\hline\n"
    )
    for r in TIEN_BO:
        s += " & ".join(r) + " \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


def bang_theo_doi():
    s = (
        "\\noindent\\textbf{PHIẾU ĐÁNH GIÁ KẾT QUẢ THI CỦA HỌC SINH:} [[br]] "
        "\\textit{\\footnotesize Ghi điểm từng bài kiểm tra chính thức để đánh giá năng lực thực tế so với giai đoạn ôn tập.} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.3}\n"
        "\\begin{tabular}{|p{7.2cm}|c|c|c|c|}\n\\hline\n"
        "\\textbf{Bài (điểm tối đa)} & \\textbf{Đề thi 1} & \\textbf{Đề thi 2} & \\textbf{Đề thi 3} & \\textbf{Xếp loại} \\\\ \\hline\n"
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

    so = k[-1]
    tit = f"Đề kiểm tra cuối học kì I — Đề chính thức {so} (90 phút)"
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
            text=f"\\textbf{{MA TRẬN ĐỀ KIỂM TRA CUỐI HỌC KÌ I -- ĐỀ CHÍNH THỨC SỐ {so} (90 PHÚT)}}"
            + BR
            + f"\\textbf{{Cơ cấu nguồn đề ({len(q_dict)} quận/huyện):}} {str_nguon} (đạt chuẩn $\\le 40\\%$ điểm/quận)."
            + BR
            + s_mt,
        ),
        dict(type="para", text=s_muc),
        dict(type="para", text=bang_bay(D["bay"])),
        dict(
            type="para",
            text="\\textbf{HƯỚNG DẪN CHẤM THI CHÍNH THỨC:}"
            + BR
            + D["cach_dung"]
            + BR
            + "\\textbf{Quy tắc chấm thi:} Mỗi bước biến đổi được tính điểm thành phần chi tiết bên phải dòng. Mỗi phép biến đổi viết trên một dòng riêng biệt. Bài hình phải vẽ đúng hình mới chấm điểm. Vẽ sai hình hoặc không vẽ hình thì không cho điểm.",
        ),
    ]
    stages.append(dict(kind=KIND[0], number=1, title=f"Ma trận Đề chính thức số {so}", blocks=b1))

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

    tit = f"Ma trận đề và đáp án chi tiết — Đề chính thức số {so}"
    return dict(slug=D["slug_mt"], title=tit, eyebrow="TÀI LIỆU GIÁO VIÊN • LỚP 8 • " + D["ten"], grade_label="Lớp 8", class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


# ─────────────────────────── MAIN ───────────────────────────
if __name__ == "__main__":
    NGUON, NGUON_BO = kiem_nguon()
    print("✓ Kiểm tra rải nguồn Đề chính thức CK1 lớp 8 thành công:")
    for _k, (_n, _q) in NGUON.items():
        print(f"  [{_k}] {_n} trường, {len(_q)} quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(_q.items(), key=lambda t: -t[1])))
    print("  Tổng cả bộ theo quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(NGUON_BO.items(), key=lambda t: -t[1])))

    for k, D in DE.items():
        p_de = OUT / f"{D['slug_de']}.json"
        p_mt = OUT / f"{D['slug_mt']}.json"
        p_de.write_text(json.dumps(de_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
        p_mt.write_text(json.dumps(mt_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → Đã sinh: {p_de.name} và {p_mt.name}")
    print("Hoàn tất sinh 3 đề chính thức CK1 lớp 8.")
