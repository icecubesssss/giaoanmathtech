#!/usr/bin/env python3
"""Sinh 2 việc Gemini: phiếu GỘP chương VII lớp 9C (Bài 22 + 23 + 24 trong MỘT buổi 180′).

Thầy (tiến độ sửa 11/11/2026): "Chương VII gộp 1 buổi: Bài 22–24 bảng tần số, tần số tương đối,
biểu đồ, ghép nhóm" — dạy 17/01/2027 (tuần 31). BTVN 6 bài. Câu vào 10 phục vụ: I.1.
Phiếu A, B cũ (2 buổi) GIỮ NGUYÊN, Thầy quyết sau.

Mọi BẢNG và BIỂU ĐỒ do script này sinh từ số liệu đã kiểm (HINH); Gemini chỉ đặt chỗ
[[HINH:khoá]] — lap_gop_phieu_ch7_9c.py thay bằng mã LaTeX/TikZ khi ráp seed.

    python3 scripts/gemini/viec_gop_phieu_ch7_9c.py
    python3 scripts/gemini/tho.py --mot gop-9c-ch7-tren-lop   (song song với)
    python3 scripts/gemini/tho.py --mot gop-9c-ch7-btvn
    python3 scripts/gemini/lap_gop_phieu_ch7_9c.py
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/dai-so/lop-c/chuong-07-tan-so-va-tan-so-tuong-doi"
SLUG = "phieu-a-doc-bieu-do-ghep-nhom-lap-bang-tinh-tan-so-tuong-doi"
TITLE = "Đọc biểu đồ ghép nhóm: lập bảng, tính tần số tương đối, đếm theo điều kiện"
MAU = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-d-tinh-gia-tri-bieu-thuc-chua-hai-nghiem.json"


# ── Bộ dựng bảng / biểu đồ (số liệu tuyệt đối đúng, không để Gemini chép TikZ) ──────────
def _boc(noi_dung: str) -> str:
    return r"\par\nopagebreak\smallskip\begin{center}" + noi_dung + r"\end{center}\smallskip "


def bang(dong: list[list[str]]) -> str:
    """dong[0] = dòng tiêu đề (in đậm). Mỗi ô là chuỗi LaTeX."""
    k = len(dong[0])
    out = [r"\footnotesize\renewcommand\arraystretch{1.25}\begin{tabular}{|l|" + "c|" * (k - 1) + r"}\hline "]
    for i, d in enumerate(dong):
        o = [rf"\textbf{{{x}}}" if i == 0 else x for x in d]
        out.append(" & ".join(o) + r" \\ \hline ")
    out.append(r"\end{tabular}")
    return _boc("".join(out))


def _buoc(vmax: float) -> float:
    for s in (1, 2, 5, 10, 20, 25, 50, 100):
        if vmax / s <= 6:
            return s
    return 100


def _so(x) -> str:
    s = f"{x:g}".replace(".", "{,}")
    return s


def bieu_do_cot(nhan: list[str], gia_tri: list[float], truc_x: str, truc_y: str,
                sat: bool = False, nhan_cot: list[str] | None = None) -> str:
    """Biểu đồ cột: sat=False cột rời (Bài 22, 23); sat=True cột liền (ghép nhóm, Bài 24)."""
    vmax = max(gia_tri)
    st = _buoc(vmax)
    top = st * (int(vmax // st) + 1)
    H = 2.5
    k = H / top
    w = 1.35 if sat else 0.9
    buoc = w if sat else 1.6
    x0 = 0.3
    L = x0 + buoc * len(nhan) + (0 if sat else 0.0) + 0.3
    t = [r"\adjustbox{max width=0.66\linewidth}{\begin{tikzpicture}[font=\small,line width=0.6pt]"]
    v = 0
    while v <= top + 1e-9:
        y = v * k
        t.append(rf"\draw[ink!25,line width=0.3pt] (0,{y:.2f}) -- ({L:.2f},{y:.2f});")
        t.append(rf"\node[left,font=\scriptsize,fill=white,inner sep=1pt] at (-0.05,{y:.2f}) {{{_so(v)}}};")
        v += st
    t.append(rf"\draw[->,ink] (0,0) -- ({L + 0.4:.2f},0);")
    t.append(rf"\node[font=\scriptsize,align=left,text width=1.6cm,anchor=south west] at ({L + 0.3:.2f},0.12) {{{truc_x}}};")
    t.append(rf"\draw[->,ink] (0,0) -- (0,{H + 0.5:.2f}) node[above,font=\scriptsize]{{{truc_y}}};")
    for i, (n, g) in enumerate(zip(nhan, gia_tri)):
        a = x0 + i * buoc + (0 if sat else (buoc - w) / 2)
        b = a + w
        h = g * k
        mau = "stage3" if sat else "stage2"
        t.append(rf"\fill[{mau}!25] ({a:.2f},0) rectangle ({b:.2f},{h:.2f});")
        t.append(rf"\draw[{mau}] ({a:.2f},0) rectangle ({b:.2f},{h:.2f});")
        nc = nhan_cot[i] if nhan_cot else _so(g)
        t.append(rf"\node[above,font=\scriptsize,fill=white,inner sep=1pt] at ({(a + b) / 2:.2f},{h + 0.04:.2f}) {{{nc}}};")
        t.append(rf"\node[below,font=\scriptsize,align=center,text width={max(w, 1.3):.2f}cm] at ({(a + b) / 2:.2f},0) {{{n}}};")
    t.append(r"\end{tikzpicture}}")
    return _boc("".join(t))


def bieu_do_quat(nhan: list[str], phan_tram: list[float]) -> str:
    mau = ["stage2", "stage3", "stage1", "brand", "ink"]
    t = [r"\adjustbox{max width=0.86\linewidth}{\begin{tikzpicture}[font=\small,line width=0.6pt]"]
    goc = 90.0
    for i, (n, p) in enumerate(zip(nhan, phan_tram)):
        g2 = goc - p * 3.6
        giua = (goc + g2) / 2
        t.append(rf"\filldraw[{mau[i % 5]}!25,draw={mau[i % 5]}] (0,0) -- ({goc:.2f}:1.4) arc ({goc:.2f}:{g2:.2f}:1.4) -- cycle;")
        t.append(rf"\node[font=\scriptsize,fill=white,inner sep=1pt] at ({giua:.2f}:{0.85 if p >= 15 else 1.1}) {{{_so(p)}\%}};")
        import math
        c = math.cos(math.radians(giua))
        neo = "east" if c < -0.3 else ("west" if c > 0.3 else ("south" if math.sin(math.radians(giua)) > 0 else "north"))
        t.append(rf"\node[font=\scriptsize,align=center] at ({giua:.2f}:2.55) {{{n}}};")
        goc = g2
    t.append(r"\end{tikzpicture}}")
    return _boc("".join(t))


def o(w="1.3cm"):
    return f"[[blank:{w}]]"


def nhom(a, b):
    return f"$[{a};{b})$".replace(".", "{,}")


# Mọi số liệu dưới đây đã đối chiếu đề gốc (bank Ch.VII snapshot 01/11) và tính lại bằng Python.
HINH = {
    # ── Luyện tập 1 ──
    "B1": bang([["Thời gian (phút)", "9", "10", "11", "12", "15"], ["Số bạn", o(), o(), o(), o(), o()]]),
    "B2_bd": bieu_do_cot(["Sách giáo khoa", "Truyện ngắn", "Sách tham khảo", "Tiểu thuyết"], [15, 20, 35, 30],
                         "Loại sách", "Số lượt mượn"),
    "B2": bang([["Loại sách", "Sách giáo khoa", "Truyện ngắn", "Sách tham khảo", "Tiểu thuyết"],
                ["Số lượt mượn", o(), o(), o(), o()]]),
    "VD2": bang([["Chất lượng không khí", "M1", "M2", "M3", "M4"],
                 ["Tần số", "[[fill:9]]", "[[fill:12]]", "[[fill:6]]", "[[fill:3]]"],
                 ["Tần số tương đối", r"[[fill:30]]\%", r"[[fill:40]]\%", r"[[fill:20]]\%", r"[[fill:10]]\%"]]),
    "B3": bang([["Điểm", "7", "8", "9", "10"], ["Số học sinh", "6", "14", "16", "4"],
                ["Tần số tương đối", o(), o(), o(), o()]]),
    "B4": bang([["Môn học", "Toán", "Ngữ văn", "Lịch sử", "Thể dục"], ["Số học sinh yêu thích", "11", "8", "9", "12"]]),
    "VD3": bang([["Thời gian tự học (giờ)", nhom(0, 4), nhom(4, 8), nhom(8, 12), nhom(12, 16), nhom(16, 20)],
                 ["Số học sinh", "17", "72", "94", "75", "42"]]),
    "B5": bang([["Chiều cao (cm)", nhom(140, 145), nhom(145, 150), nhom(150, 155), nhom(155, 160), nhom(160, 165)],
                ["Số học sinh", "10", "18", "14", "6", "2"]]),
    "B6_bd": bieu_do_cot([nhom(34, 36), nhom(36, 38), nhom(38, 40), nhom(40, 42)], [15, 10, 10, 5],
                         "Số học sinh", "Tần số (n)", sat=True),
    "B7": bang([["Độ dài (mét)", nhom(6, 7), nhom(7, 8), nhom(8, 9), nhom(9, 10), nhom(10, 11)],
                ["Tần số", "23", "10", "9", "6", "2"]]),
    "B8": bang([["Tuổi", nhom(18, 20), nhom(20, 22), nhom(22, 24), nhom(24, 26), nhom(26, 28), nhom(28, 30)],
                ["Số đồng chí", "114", "86", "97", "61", "73", "69"]]),
    "B9": bang([["Độ dài (cm)", nhom(27, 28), nhom(28, 29), nhom(29, 30), nhom(30, 31), nhom(31, 32)],
                ["Tần số", "2", "8", "20", o("1cm"), "4"]]),
    "B10": bang([["Số lần truy cập Internet", nhom(30, 40), nhom(40, 50), nhom(50, 60), nhom(60, 70), nhom(70, 80), nhom(80, 90)],
                 ["Tần số", "6", "12", "6", "9", "6", "9"]]),
    # ── Luyện tập 2 ──
    "VD4_bd": bieu_do_cot(["36", "37", "38", "39", "40"], [28, 37, 30, 10, 15], "Cỡ giày", "Số học sinh"),
    "B11_bd": bieu_do_cot(["6", "7", "8", "9", "10"], [8, 11, 10, 7, 4], "Điểm", "Số học sinh"),
    "B11": bang([["Điểm", "6", "7", "8", "9", "10"], ["Số học sinh", "?", "?", "?", "?", "?"]]),
    "VD5": bang([["Loại phim", "Hài", "Khoa học viễn tưởng", "Kinh dị"],
                 ["Tỉ lệ bạn yêu thích", r"50\%", r"37{,}5\%", r"12{,}5\%"]]),
    "VD5_quat": bieu_do_quat(["Hài", "Khoa học\\\\viễn tưởng", "Kinh dị"], [50, 37.5, 12.5]),
    "B12": bang([["Mức", "Tốt", "Khá", "Đạt", "Chưa đạt"], ["Số học sinh", "16", "11", "10", "3"]]),
    "B12_quat": bieu_do_quat(["Tốt", "Khá", "Đạt", "Chưa đạt"], [40, 27.5, 25, 7.5]),
    "VD6": bang([["Lượng điện (kWh)", nhom(100, 130), nhom(130, 160), nhom(160, 190), nhom(190, 220)],
                 ["Số hộ gia đình", "[[fill:3]]", "[[fill:5]]", "[[fill:5]]", "[[fill:7]]"]]),
    "VD7": bang([["Tuổi thọ (ngày)", nhom(30, 40), nhom(40, 50), nhom(50, 60)], ["Tần số", "12", "23", "15"]]),
    "VD7_bd": bieu_do_cot([nhom(30, 40), nhom(40, 50), nhom(50, 60)], [24, 46, 30], "Tuổi thọ (ngày)",
                          r"Tần số tương đối (\%)", sat=True, nhan_cot=[r"24\%", r"46\%", r"30\%"]),
    "B14": bang([["Chiều cao (cm)", nhom(140, 145), nhom(145, 150), nhom(150, 155), nhom(155, 160)],
                 ["Số học sinh", "5", "15", "12", "8"]]),
    "B14_bd": bieu_do_cot([nhom(140, 145), nhom(145, 150), nhom(150, 155), nhom(155, 160)], [5, 15, 12, 8],
                          "Chiều cao (cm)", "Số học sinh", sat=True),
    "VD8": bang([["Số ngoại ngữ", "1", "2", "3", "4", r"$\ge 5$"], ["Số đại biểu", "84", "64", "24", "16", "12"]]),
    "B15_bd": bieu_do_cot(["Xe 4 chỗ", "Xe 7 chỗ", "Xe 16 chỗ", "Xe trên 16 chỗ"], [35, 20, 15, 10], "Loại xe", "Tần số"),
    "VD9_bd": bieu_do_cot([nhom(40, 50), nhom(50, 60), nhom(60, 70), nhom(70, 80), nhom(80, 90)], [3, 6, 19, 23, 9],
                          "Số tiền (nghìn đồng)", "Tần số (n)", sat=True),
    "B16_bd": bieu_do_cot([nhom(90, 95), nhom(95, 100), nhom(100, 105), nhom(105, 110), nhom(110, 115), nhom(115, 120)],
                          [3, 5, 6, 7, 9, 10], "Thời gian (phút)", "Tần số (n)", sat=True),
    "B16": bang([["Nhóm", nhom(90, 95), nhom(95, 100), nhom(100, 105), nhom(105, 110), nhom(110, 115), nhom(115, 120), "Tổng"],
                 [r"Tần số ($n$)", "", "", "", "", "", "", r"$N=$"]]),
    # ── BTVN ──
    "T1": bang([["Điểm số", "3", "4", "5", "6", "7", "8", "9", "10"], [r"Tần số ($n$)", "1", "2", "6", "5", "7", "8", "7", "4"]]),
    "T2": bang([["Nhóm", nhom(150, 155), nhom(155, 160), nhom(160, 165), nhom(165, 170), nhom(170, 175), "Cộng"],
                ["Tần số", "5", "8", "10", "12", "5", r"$N=40$"]]),
    "T4_bd": bieu_do_cot([nhom(35, 40), nhom(40, 45), nhom(45, 50), nhom(50, 55), nhom(55, 60), nhom(60, 65), nhom(65, 70)],
                         [3, 5, 9, 15, 10, 5, 3], "Cân nặng (kg)", "Tần số (n)", sat=True),
    "T6_bd": bieu_do_cot([nhom(1, 1.25), nhom(1.25, 1.5), nhom(1.5, 1.75), nhom(1.75, 2)], [18, 21, 56, 5],
                         "Tuổi thọ (nghìn giờ)", r"Tần số tương đối (\%)", sat=True,
                         nhan_cot=[r"18\%", r"21\%", r"56\%", r"5\%"]),
    # BTVN thêm (Thầy 15/11: BTVN 49′ < 90′ ⇒ thêm 3 bài thật từ ngân hàng)
    "T7_bd": bieu_do_cot(["$0{,}5$", "$1$", "$2$", "$3$", "$4$"], [15, 36, 48, 39, 12], "Thời gian (giờ)", "Số học sinh"),
    "T8_bd": bieu_do_cot([nhom(5, 10), nhom(10, 15), nhom(15, 20)], [15, 13, 2], "Thời gian (phút)", "Tần số (n)", sat=True),
    "T9": bang([["Khối lượng (g)", "92", "96", "100", "105", "110", ""], ["Tần số", "7", "18", "38", "9", "8", r"$N=80$"]]),
    "T9_quat": bieu_do_quat(["92 g", "96 g", "100 g", "105 g", "110 g"], [8.75, 22.5, 47.5, 11.25, 10]),
}

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VII: Tần số và tần số tương đối, Bài 22 + Bài 23 + Bài 24 SGK Kết nối tri thức) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu, ôn thi vào 10 Hà Nội). Làm CẨN THẬN, KHÔNG bịa đề: mọi đề bài lấy ĐÚNG số liệu trong SƠ ĐỒ bên dưới (đã đối chiếu đề gốc), giữ ngoặc nguồn "(… )" sau đề như sơ đồ ghi.

KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Bối cảnh
Trước đây chương VII dạy 2 buổi. Giáo viên chốt GỘP thành MỘT buổi 180 phút (45 phút giáo viên giảng lý thuyết + ví dụ, 120 phút học sinh luyện, 15 phút giải lao; bài về nhà in phiếu riêng). Câu thi vào 10 phục vụ: Câu I.1 (1,0 điểm) — đọc bảng/biểu đồ ghép nhóm, tìm tần số và tần số tương đối của một nhóm.

## BẢNG VÀ BIỂU ĐỒ — KHÔNG TỰ VẼ
Mọi bảng số liệu và biểu đồ đã được dựng sẵn bằng máy. Chỗ nào sơ đồ ghi [[HINH:khoá]] thì bạn chép NGUYÊN chuỗi đó (ví dụ "[[HINH:B2_bd]]") vào đúng vị trí: ngay sau câu dẫn đề, TRƯỚC các ý a), b). KHÔNG viết \begin{tabular}, \begin{tikzpicture}, \begin{center}. KHÔNG đặt [[br]] ngay trước hoặc ngay sau [[HINH:…]] (máy tự lo ngắt dòng). Ví dụ đúng: "Biểu đồ dưới đây cho biết … (nguồn).[[HINH:B6_bd]]a) [NB] …[[br]]b) [NB] …". Dãy số liệu thô (không có khoá HINH) thì bạn viết trong đề dạng: "[[br]]\hspace*{1.4em}$9;\;15;\;11;\;\ldots$" (chép đủ, đúng thứ tự).

## Khuôn JSON (xem "Mẫu khối" cuối prompt — lấy từ phiếu đại số đã duyệt)
- problem: {"type":"problem","label":"Bài N.","tier":"onclass" hoặc "btvn","level":1|2|3,"dang_id":"…","statement":"…","solution":"…","hints":[…]}. Không dùng "writelines", không dùng "figure".
- Mỗi ý trong statement mở đầu bằng thẻ mức: "a) [NB] …", "b) [TH] …". Bài một thẻ thì thẻ đứng đầu statement. SỐ THẺ và loại thẻ phải ĐÚNG sơ đồ (thẻ = số câu tính giờ).
- Ví dụ = khối {"type":"noted","variant":"example","text":"\\textbf{Ví dụ N.} đề (nguồn)[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}…"}. Ví dụ là BÀI ĐIỀN KHUYẾT: các số/từ khoá cần nhớ trong lời giải bọc [[fill:đáp án]] (trong $…$ thì đáp án KHÔNG bọc $; ví dụ "$f=\dfrac{[[fill:9]]}{30}\cdot 100\%=[[fill:30]]\%$"). Ít nhất 3 ô [[fill:…]] mỗi ví dụ. Lời giải ví dụ trình bày như bài thi: mỗi bước một dòng "[[br]]\hspace*{1.4em}…", có căn cứ ("Ta có", "Áp dụng công thức …, ta có"), dòng cuối "Vậy …".
- Ô điền trong bài Luyện tập 1: [[blank:1.6cm]] (không dùng \ldots làm ô điền). Bài Luyện tập 2 và mọi bài level 2, 3: KHÔNG có ô điền, KHÔNG có \ldots — học sinh tự trình bày vào vở.
- Bài level 2 (TH) có "hints": 1–2 câu hỏi gợi mở ngắn (dạng câu hỏi, không đọc thẳng đáp án). Bài level 1 và 3: "hints": [].
- solution: lời giải đầy đủ, mỗi ý a), b) tách riêng, mỗi bước một dòng [[br]]; bài level ≥ 2 phải có căn cứ ("Ta có", "Vì", "Áp dụng công thức") và câu "Vậy …" ở cuối mỗi ý. Bảng trong lời giải: viết thành lời ("các tần số lần lượt là $4;\;14;\;8$") hoặc dùng khoá [[HINH:…]] nếu sơ đồ cho.
- KHÔNG dùng \needspace, \dfrac giữa dòng chữ (\dfrac chỉ khi công thức đứng riêng sau "ta có"; trong câu dùng \frac).

## Luật trình bày (giáo viên đã chốt — vi phạm là bị trả lại)
1. Đề nêu dữ kiện trước, yêu cầu sau; câu yêu cầu rõ mục tiêu ("Tìm tần số …", "Tính tần số tương đối …").
2. Không văn nói, không xưng hô: cấm "em", "các em", "hôm nay", "ở lớp", "Kiểm" (phải "Kiểm tra"), "Soi", "khuôn", "mẹo", "bẫy điểm", "mất điểm", "thang điểm", "tầng C". Không viết tắt (viết "học sinh", không "HS"; viết "tần số tương đối", không "TSTĐ").
3. Mỗi bài/ví dụ một đề gốc khác nhau; không "làm tiếp Bài N", không "dùng bảng ở Bài N" — đề phải ghi ĐỦ dữ kiện.
4. Toán trong $…$; số thập phân viết $12{,}5$; phần trăm viết $28\%$; giữ escape \% \& \# ở MỌI chỗ (kể cả ngoài $…$: "Phòng GD\&ĐT"). Nhóm số liệu viết $[150;155)$. JSON hợp lệ (gạch chéo ngược nhân đôi trong chuỗi JSON).
5. Công thức tần số tương đối viết đúng SGK: $f=\frac{m}{n}\cdot 100\%$ (dùng chữ $n$ cho cỡ mẫu như SGK).
6. TỰ TÍNH LẠI mọi đáp số (đáp số đúng đã ghi trong sơ đồ — phải khớp). Nghi sai chỗ nào ghi vào "ghi_chu".
7. KHÔNG chèn dòng nháp, lời bình, câu tự hỏi ("Suy ra gì không", "viết lại:") vào bất kỳ trường nào.
'''

VIEC1 = r'''
## Việc của bạn: dựng 4 chặng ĐẦU (Khám phá, Kiến thức cần nhớ, Luyện tập 1, Luyện tập 2)

### Chặng 1 — {"kind":"review","number":1,"title":"Khám phá"}
- Khối "opener" (chỉ "text", không tikz): 4–5 câu đời sống học sinh, KHÔNG nêu tên khái niệm mới (không nói "tần số", "ghép nhóm"): lớp trưởng ghi lại thời gian dùng điện thoại mỗi ngày (phút) của 40 bạn trong lớp, gần như bạn nào cũng một con số khác nhau; câu hỏi gợi mở: liệt kê 40 con số thì khó nhìn — làm thế nào để thấy ngay khoảng thời gian nào nhiều bạn nhất và khoảng đó chiếm bao nhiêu phần của cả lớp? Câu cuối: cuối buổi làm trọn Bài 16 (một câu đề thi thật).
- Khối noted variant "note" (không title), text bắt đầu "\textbf{Nhắc lại.}[[br]]" rồi 3 gạch đầu dòng "$\bullet$\; …" (mỗi dòng [[br]]), đúng chữ SGK:
  • Tỉ số phần trăm của $a$ và $b$ là $\frac{a}{b}\cdot 100\%$. Ví dụ $\frac{57}{200}\cdot 100\%=28{,}5\%$. (SGK Toán 6 tập hai, Bài 31, tr.38)
  • Muốn tìm $m\%$ của số $a$, ta tính $a\cdot\frac{m}{100}$. (SGK Toán 6 tập hai, Bài 31, tr.39)
  • Làm tròn số thập phân đến một hàng: nếu chữ số ngay bên phải hàng làm tròn nhỏ hơn $5$ thì giữ nguyên chữ số hàng làm tròn; nếu lớn hơn hoặc bằng $5$ thì tăng chữ số hàng làm tròn thêm $1$ đơn vị; bỏ các chữ số ở phần thập phân sau hàng làm tròn. Ví dụ $8{,}333\ldots\approx 8{,}33$ (làm tròn đến hàng phần trăm). (SGK Toán 6 tập hai, Bài 30, tr.35)
- teacher_note: mở màn 5 phút, hỏi nhanh cả lớp, chưa giải; 5 phút nhắc lại tỉ số phần trăm và làm tròn.

### Chặng 2 — {"kind":"concept","number":2,"title":"Kiến thức cần nhớ"}
CHỈ là lý thuyết SGK (cấm mẹo, cấm "khuôn", cấm cấu trúc đề thi). Mỗi mục = một khối para tiêu đề "\textbf{N. Tên}" + một khối para nội dung (xuống dòng [[br]], gạch đầu dòng "$\bullet$\;"), cuối nội dung ghi nguồn "(SGK Toán 9 tập hai, tr.…)". Bảng tổng quát viết thành lời, không vẽ bảng. Nội dung đúng chữ SGK:
1. "Tần số và bảng tần số" — Số giá trị của mẫu dữ liệu được gọi là cỡ mẫu. Tần số của một giá trị là số lần xuất hiện giá trị đó trong mẫu dữ liệu. Bảng tần số là bảng thống kê cho biết tần số của các giá trị trong mẫu dữ liệu: dòng trên ghi các giá trị $x_1, x_2, \ldots, x_k$, dòng dưới ghi tần số tương ứng $m_1, m_2, \ldots, m_k$. (tr.33)
2. "Biểu đồ tần số" — Biểu đồ biểu diễn bảng tần số được gọi là biểu đồ tần số. Biểu đồ tần số thường gặp là biểu đồ tần số dạng cột và biểu đồ tần số dạng đoạn thẳng. (tr.34)
3. "Tần số tương đối và bảng tần số tương đối" — Cho $x_1, x_2, \ldots, x_k$ là các giá trị khác nhau của mẫu dữ liệu cỡ $n$. Tần số tương đối $f_i$ của giá trị $x_i$ là tỉ số giữa tần số $m_i$ của $x_i$ với $n$. Trong đó $n=m_1+\ldots+m_k$ và $f_i=\frac{m_i}{n}\cdot 100\%$. Bảng tần số tương đối: dòng trên ghi các giá trị, dòng dưới ghi tần số tương đối $f_1, \ldots, f_k$. (tr.38)
4. "Biểu đồ tần số tương đối" — Biểu đồ biểu diễn bảng tần số tương đối được gọi là biểu đồ tần số tương đối; dạng thường gặp là biểu đồ cột và biểu đồ hình quạt tròn. Vẽ biểu đồ hình quạt tròn: Bước 1. Xác định số đo cung của các hình quạt theo công thức $360^\circ\cdot f_i$. Bước 2. Vẽ hình tròn và chia thành các hình quạt có số đo cung tương ứng. Bước 3. Định dạng các hình quạt (tô màu), ghi tần số tương đối, chú giải và tiêu đề. (tr.40)
5. "Bảng tần số và bảng tần số tương đối ghép nhóm" — Nhóm số liệu $[a;b)$ gồm các số liệu lớn hơn hoặc bằng $a$ và nhỏ hơn $b$; $a$ là đầu mút trái, $b$ là đầu mút phải. Bảng tần số ghép nhóm là bảng tần số của các nhóm số liệu. Tần số $m_i$ của nhóm $[a_i;a_{i+1})$ là số giá trị của mẫu số liệu lớn hơn hoặc bằng $a_i$ và nhỏ hơn $a_{i+1}$. Bảng tần số tương đối ghép nhóm là bảng tần số tương đối của các nhóm số liệu, với $n=m_1+\ldots+m_k$ và $f_i=\frac{m_i}{n}\cdot 100\%$ là tần số tương đối của nhóm $[a_i;a_{i+1})$. (tr.46--47)
6. "Biểu đồ ghép nhóm dạng cột" — Biểu đồ tần số tương đối ghép nhóm dạng cột gồm các cột liền nhau biểu diễn bảng tần số tương đối ghép nhóm; chiều cao mỗi cột biểu diễn tần số tương đối của nhóm số liệu. Nếu chiều cao mỗi cột biểu diễn tần số của nhóm số liệu thì ta có biểu đồ tần số ghép nhóm dạng cột. (tr.49)
- teacher_note: giảng khoảng 20 phút, nhấn: cỡ mẫu là tổng các tần số; giá trị bằng đầu mút phải thuộc nhóm sau.

### Chặng 3 — {"kind":"practice1","number":3,"title":"Luyện tập 1 — Nhận biết"}
Mọi bài level 1, tier "onclass", điền khuyết [[blank:1.6cm]] (câu dẫn mở bằng "Điền vào chỗ chấm …" hoặc bảng có ô trống). Thứ tự khối đúng như sau:
1. para: "\textbf{Đích của buổi học:} Bài 16 — Câu I.1 đề giữa kì II THCS Nam Từ Liêm (2025--2026): đọc biểu đồ tần số ghép nhóm, lập bảng tần số ghép nhóm (Mạch 3), tính tần số tương đối của một nhóm (Mạch 2, Mạch 3) và đếm số người thoả mãn một điều kiện (Mạch 3). Mạch 1 và Mạch 2 là Bài 22, Bài 23; Mạch 3 là Bài 24 — dạng Câu I.1 đề thi vào 10."  (giữ đúng: chữ "Bài" đầu tiên trong đoạn phải là "Bài 16")
2. para variant "heading": "Mạch 1. Bảng tần số và biểu đồ tần số"
3. Ví dụ 1 — (SGK Toán 9 tập hai, Bài 22, Ví dụ 1, tr.33): cỡ giày của các bạn nam một lớp: $40;\;36;\;37;\;36;\;40;\;38;\;39;\;38;\;37;\;36;\;40;\;39;\;36;\;38;\;37;\;38;\;38;\;37;\;38;\;38;\;38;\;36$. Yêu cầu: lập bảng tần số, tìm cỡ mẫu, cho biết cỡ giày nào nhiều bạn đi nhất. Lời giải điền khuyết: đếm cỡ 36: [[fill:5]], 37: [[fill:4]], 38: [[fill:8]], 39: [[fill:2]], 40: [[fill:3]] (viết thành dòng "Cỡ giày $36$ có $[[fill:5]]$ bạn; …"); cỡ mẫu $n=5+4+8+2+3=[[fill:22]]$; Vậy cỡ giày [[fill:38]] có nhiều bạn đi nhất.
4. Bài 1. dang_id "NB1", 3 thẻ — (Kiểm tra học kì II Phòng GD\&ĐT Hoài Đức, 2024--2025): "Thời gian đi từ nhà đến trường (đơn vị: phút) của 16 bạn học sinh được ghi lại như sau:" + dãy $9;\;15;\;11;\;15;\;10;\;9;\;10;\;12;\;11;\;10;\;12;\;10;\;9;\;12;\;9;\;15$ + "[[br]]Điền vào chỗ chấm để trả lời các câu hỏi sau." + [[HINH:B1]] + a) [NB] Đếm và điền vào bảng tần số trên. b) [NB] Cỡ mẫu $n=$ [[blank:1.6cm]]. c) [NB] Số bạn đi đến trường hết nhiều hơn $10$ phút là [[blank:1.6cm]] bạn. Đáp số: 9:4, 10:4, 11:2, 12:3, 15:3; $n=16$; $2+3+3=8$ bạn.
5. Bài 2. dang_id "NB2", 3 thẻ — (Kiểm tra học kì II THCS Xuân Đỉnh, 2025--2026): "Số lượt mượn các loại sách trong một tuần tại thư viện một trường trung học cơ sở được biểu diễn bằng biểu đồ dưới đây." [[HINH:B2_bd]] "Điền vào chỗ chấm để trả lời các câu hỏi sau." [[HINH:B2]] a) [NB] Điền vào bảng tần số trên. b) [NB] Loại sách được mượn nhiều nhất là [[blank:2.6cm]]. c) [NB] Tổng số lượt mượn sách trong tuần là $n=$ [[blank:1.6cm]]. Đáp số: 15; 20; 35; 30; Sách tham khảo; $n=100$.
   (Chú ý: giữa [[HINH:B2_bd]] và [[HINH:B2]] có câu "Điền vào chỗ chấm …" — viết liền, không [[br]].)
6. para variant "heading": "Mạch 2. Tần số tương đối"
7. Ví dụ 2 — (SGK Toán 9 tập hai, Bài 23, Ví dụ 1, tr.38--39): chất lượng không khí 30 ngày mùa xuân: M1 có $9$ ngày, M2 có $12$ ngày, M3 có $6$ ngày, M4 có $3$ ngày (M1: Tốt; M2: Trung bình; M3: Kém; M4: Xấu). Yêu cầu: lập bảng tần số tương đối. Lời giải: "Cỡ mẫu $n=9+12+6+3=[[fill:30]]$." rồi một dòng tính $f_1=\frac{9}{30}\cdot 100\%=[[fill:30]]\%$ … (4 giá trị 30\%, 40\%, 20\%, 10\%), rồi "Ta có bảng tần số tương đối:" [[HINH:VD2]] rồi "Tổng các tần số tương đối bằng $[[fill:100]]\%$." và dòng "Vậy …". (Bảng VD2 đã có ô [[fill]].)
8. Bài 3. dang_id "NB3", 3 thẻ — (Kiểm tra học kì II THCS Đại Áng, 2025--2026): "Thống kê điểm kiểm tra khảo sát môn Toán của 40 học sinh lớp 9A được cho trong bảng sau. Điền vào chỗ chấm để hoàn thành bảng." [[HINH:B3]] a) [NB] Tần số tương đối của điểm $7$ là $f=\frac{6}{40}\cdot 100\%=$ [[blank:1.6cm]]. b) [NB] Tần số tương đối của điểm $10$ là [[blank:1.6cm]]. c) [NB] Tổng bốn tần số tương đối trong bảng bằng [[blank:1.6cm]]. Đáp số: 15\%; 35\%; 40\%; 10\%; tổng 100\%.
9. Bài 4. dang_id "NB4", 3 thẻ — (Kiểm tra học kì II Phòng GD\&ĐT Hai Bà Trưng, 2024--2025): "Bạn Minh hỏi 40 bạn học sinh bất kì về môn học mà bạn đó yêu thích nhất. Kết quả được ghi lại ở bảng sau. Điền vào chỗ chấm để trả lời các câu hỏi." [[HINH:B4]] a) [NB] Tần số của môn Lịch sử là [[blank:1.6cm]]. b) [NB] Tần số tương đối của môn Lịch sử là [[blank:1.6cm]]. c) [NB] Tần số tương đối của môn Thể dục là [[blank:1.6cm]]. Đáp số: 9; 22,5\%; 30\%.
10. para variant "heading": "Mạch 3. Tần số và tần số tương đối ghép nhóm"
11. Ví dụ 3 — (Câu I.1 đề thi tuyển sinh vào lớp 10 Hà Nội, 2025): "Kết quả khảo sát 300 học sinh lớp 9 về thời gian tự học của mỗi bạn trong một tuần (đơn vị: giờ) được cho trong bảng tần số ghép nhóm sau đây." [[HINH:VD3]] "Xác định tần số và tần số tương đối của nhóm $[12;16)$." Lời giải 3 dòng + Vậy: tần số của nhóm $[12;16)$ là $m=[[fill:75]]$; cỡ mẫu $n=17+72+94+75+42=[[fill:300]]$; tần số tương đối $f=\frac{75}{300}\cdot 100\%=[[fill:25]]\%$; Vậy tần số của nhóm $[12;16)$ là [[fill:75]], tần số tương đối là [[fill:25]]\%.
12. Bài 5. dang_id "NB5", 2 thẻ, KHUNG BÀI GIẢI — (Câu I.1 đề thi tuyển sinh vào lớp 10 Hà Nội, 2026): "Kết quả đo chiều cao của 50 học sinh lớp 6 (đơn vị: cm) được thống kê trong bảng tần số ghép nhóm sau đây." [[HINH:B5]] "Xác định tần số và tần số tương đối của nhóm $[150;155)$.[[br]]Điền vào chỗ chấm để hoàn thành bài giải.[[br]]a) [NB] Tần số của nhóm $[150;155)$ là $m=$ [[blank:1.6cm]].[[br]]b) [NB] Cỡ mẫu $n=10+18+14+6+2=$ [[blank:1.6cm]].[[br]]\hspace*{1.4em}Tần số tương đối của nhóm $[150;155)$ là $f=\frac{\ldots}{\ldots}\cdot 100\%=$ [[blank:1.6cm]].[[br]]\hspace*{1.4em}Vậy tần số của nhóm $[150;155)$ là [[blank:1.2cm]], tần số tương đối là [[blank:1.2cm]]." Đáp số 14; 50; 28\%.
13. Bài 6. dang_id "NB6", 2 thẻ — (Câu I.1 đề minh họa tuyển sinh vào lớp 10, Sở GD\&ĐT Hà Nội): "Sau khi điều tra số học sinh trong 40 lớp học (đơn vị: học sinh), người ta có biểu đồ tần số ghép nhóm dưới đây. Điền vào chỗ chấm để trả lời các câu hỏi." [[HINH:B6_bd]] a) [NB] Tần số ghép nhóm của nhóm $[40;42)$ là [[blank:1.6cm]]. b) [NB] Tần số tương đối ghép nhóm của nhóm $[40;42)$ là [[blank:1.6cm]]. Đáp số 5; 12,5\%.
14. Bài 7. dang_id "NB6", 2 thẻ — (Giữa kì II THCS Nhật Tân, 2025--2026): "Độ dài một cú nhảy ba bước (đơn vị: mét) của 50 học sinh lớp 9A1 được ghi lại ở bảng tần số ghép nhóm sau. Điền vào chỗ chấm." [[HINH:B7]] a) [NB] Tần số ghép nhóm của nhóm $[9;10)$ là [[blank:1.6cm]]. b) [NB] Tần số tương đối ghép nhóm của nhóm $[9;10)$ là [[blank:1.6cm]]. Đáp số 6; 12\%.
15. Bài 8. dang_id "NB7", 2 thẻ — (Thi thử vào 10 THCS Tự Lập, 2025--2026): "Kết quả khảo sát độ tuổi của 500 đồng chí tham gia Lễ diễu binh, diễu hành Kỷ niệm 80 năm Quốc khánh 2/9 được cho trong bảng tần số ghép nhóm sau đây. Điền vào chỗ chấm." [[HINH:B8]] a) [NB] Cỡ mẫu $n=$ [[blank:1.6cm]]. b) [NB] Tần số tương đối của nhóm $[20;22)$ là $f=\frac{\ldots}{500}\cdot 100\%=$ [[blank:1.6cm]]. Đáp số 500; 17,2\%.
16. Bài 9. dang_id "NB8", 2 thẻ — (Cuối kì II THCS Thị trấn Văn Điển, 2024--2025): "Một bác thợ đóng giày thống kê lại độ dài bàn chân (đơn vị: cm) của 40 khách hàng ở bảng tần số ghép nhóm như sau, tần số của nhóm $[30;31)$ chưa kịp ghi. Điền vào chỗ chấm." [[HINH:B9]] a) [NB] Tần số ghép nhóm của nhóm $[30;31)$ là $40-(2+8+20+4)=$ [[blank:1.6cm]]. b) [NB] Tần số tương đối ghép nhóm của nhóm $[30;31)$ là [[blank:1.6cm]]. Đáp số 6; 15\%.
17. Bài 10. dang_id "NB9", 2 thẻ — (Giữa kì II THCS Lê Ngọc Hân, 2024--2025): "Thống kê số lần truy cập Internet của toàn bộ học sinh lớp 9A trong một tuần cho kết quả bảng tần số ghép nhóm như sau. Điền vào chỗ chấm." [[HINH:B10]] a) [NB] Lớp 9A có $n=$ [[blank:1.6cm]] học sinh. b) [NB] Nhóm $[60;80)$ gồm hai nhóm $[60;70)$ và $[70;80)$ nên có tần số [[blank:1.6cm]] và tần số tương đối [[blank:1.6cm]]. Đáp số 48; 15; 31,25\%.
- teacher_note chặng 3: khoảng 40 phút; mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh điền ngay; Bài 5 là bài giải trọn vẹn đầu tiên của Câu I.1, chữa kĩ cách trình bày.

### Chặng 4 — {"kind":"practice2","number":4,"title":"Luyện tập 2 — Thông hiểu \& Vận dụng"}
Bài tự trình bày, KHÔNG ô điền, KHÔNG \ldots trong statement. Thứ tự khối:
1. Ví dụ 4 — (Bộ đề minh họa tuyển sinh lớp 10 Phòng GD\&ĐT Đống Đa, Đề 18, 2025--2026): "Biểu đồ cột dưới đây cho biết cỡ giày của các bạn nam khối 9 của một trường." [[HINH:VD4_bd]] "Lập bảng tần số cho dữ liệu được biểu diễn trên biểu đồ. Tìm tần số tương đối của cỡ giày $39$ (làm tròn đến hàng phần trăm)." Lời giải: đọc chiều cao cột: cỡ 36: [[fill:28]], 37: [[fill:37]], 38: [[fill:30]], 39: [[fill:10]], 40: [[fill:15]] (viết thành lời, mỗi cỡ một mục trên cùng dòng); cỡ mẫu $n=[[fill:120]]$; $f=\frac{10}{120}\cdot 100\%\approx [[fill:8{,}33]]\%$; Vậy ….
2. Bài 11. level 2, dang_id "TH1", 2 thẻ — (Thi thử vào 10 THCS Thái Thịnh, 2026--2027): "Cho biểu đồ về điểm số môn Tiếng Anh thi học kì I của lớp 9A1 tại một trường trung học cơ sở." [[HINH:B11_bd]] a) [TH] Lập bảng thống kê về điểm số môn Tiếng Anh theo mẫu sau.[[HINH:B11]]b) [TH] Số học sinh đạt từ điểm $8$ trở lên chiếm bao nhiêu phần trăm số học sinh cả lớp? Đáp số: 8; 11; 10; 7; 4; $n=40$; từ điểm 8 trở lên $10+7+4=21$ học sinh, $\frac{21}{40}\cdot 100\%=52{,}5\%$. hints 2 câu.
   (Chú ý: [[HINH:B11]] đứng ngay sau câu "a) [TH] … theo mẫu sau." — không [[br]] trước/sau.)
3. Ví dụ 5 — (SGK Toán 9 tập hai, Bài 23, Ví dụ 2, tr.40--41): "Cho bảng tần số tương đối về loại phim yêu thích của các học sinh lớp 9A như sau." [[HINH:VD5]] "Vẽ biểu đồ hình quạt tròn biểu diễn bảng tần số tương đối trên." Lời giải: Bước 1 số đo cung: Hài $360^\circ\cdot 50\%=[[fill:180]]^\circ$; Khoa học viễn tưởng $360^\circ\cdot 37{,}5\%=[[fill:135]]^\circ$; Kinh dị $360^\circ\cdot 12{,}5\%=[[fill:45]]^\circ$. Bước 2 vẽ hình tròn, chia các hình quạt có số đo cung vừa tính. Bước 3 tô màu, ghi tỉ lệ, chú giải, tiêu đề. Ta được biểu đồ:[[HINH:VD5_quat]] Vậy ….
4. Bài 12. level 2, dang_id "TH2", 2 thẻ — (Giữa kì II THCS Phúc Lợi, 2024--2025): "Đánh giá kết quả học tập trong Học kì I của học sinh lớp 8A ở một trường trung học cơ sở được thống kê trong bảng dưới đây." [[HINH:B12]] a) [TH] Lập bảng tần số tương đối rồi vẽ biểu đồ hình quạt tròn biểu diễn bảng đó. b) [TH] Giáo viên chủ nhiệm thông báo: tỉ lệ học sinh được đánh giá ở mức Tốt và Khá so với cả lớp là trên $67\%$. Thông báo đó có đúng không? Đáp số: $n=40$; 40\%; 27,5\%; 25\%; 7,5\%; số đo cung $144^\circ$; $99^\circ$; $90^\circ$; $27^\circ$; solution có [[HINH:B12_quat]]; b) $40\%+27{,}5\%=67{,}5\%>67\%$ nên thông báo đúng. hints 2 câu.
5. Ví dụ 6 — (Thi thử vào 10 lần 2 Phòng GD\&ĐT Thanh Oai, 2025--2026): "Công ty điện lực thống kê lượng điện tiêu thụ (đơn vị: kWh) của một số hộ gia đình trong tháng 3 năm 2025 như sau:" + dãy (2 dòng, mỗi dòng 10 số): $150;\;120;\;180;\;200;\;130;\;100;\;160;\;190;\;219;\;210$ / $170;\;140;\;110;\;130;\;160;\;180;\;150;\;200;\;210;\;190$ + "Lập bảng tần số ghép nhóm theo các nhóm $[100;130)$, $[130;160)$, $[160;190)$, $[190;220)$. Nhóm nào có nhiều hộ gia đình nhất?" Lời giải: đếm từng nhóm (ghi rõ các số thuộc nhóm: $[100;130)$: $120;100;110$ ⇒ [[fill:3]] hộ; $[130;160)$: $130;140;130;150;150$ ⇒ [[fill:5]] hộ; $[160;190)$: $180;160;170;160;180$ ⇒ [[fill:5]] hộ; $[190;220)$: $200;190;219;210;200;210;190$ ⇒ [[fill:7]] hộ — dùng chữ "nên" thay ⇒), chú ý số $190$ thuộc nhóm $[190;220)$ chứ không thuộc $[160;190)$; "Ta có bảng tần số ghép nhóm:" [[HINH:VD6]] "Tổng $3+5+5+7=[[fill:20]]$ hộ." Vậy nhóm [[fill:[190;220)]] có nhiều hộ nhất. (Trong $…$ thì đáp án nhóm viết không bọc $.)
6. Bài 13. level 2, dang_id "TH3", 2 thẻ — (Cuối kì II THCS Thái Thịnh, 2025--2026): "Chiều cao (đơn vị: cm) của 30 học sinh lớp 4 của một trường tiểu học là:" + dãy (3 dòng, mỗi dòng 10 số): $90;\;73;\;88;\;93;\;101;\;104;\;111;\;95;\;78;\;95$ / $81;\;97;\;96;\;92;\;95;\;83;\;90;\;101;\;103;\;117$ / $109;\;110;\;112;\;87;\;75;\;90;\;82;\;97;\;86;\;96$ + a) [TH] Ghép các số liệu trên thành năm nhóm $[70;80)$, $[80;90)$, $[90;100)$, $[100;110)$, $[110;120)$ rồi lập bảng tần số ghép nhóm. b) [TH] Tìm tần số tương đối của nhóm $[90;100)$. Đáp số: 3; 6; 12; 5; 4 (tổng 30); $\frac{12}{30}\cdot 100\%=40\%$. solution liệt kê các số của từng nhóm. hints 2 câu.
7. Ví dụ 7 — (SGK Toán 9 tập hai, Bài 24, Luyện tập 1, tr.48 và mục 2, tr.49): "Cho bảng tần số ghép nhóm về tuổi thọ của một số ong mật cái như sau." [[HINH:VD7]] "Lập bảng tần số tương đối ghép nhóm rồi vẽ biểu đồ tần số tương đối ghép nhóm dạng cột." Lời giải: $n=12+23+15=[[fill:50]]$; $f_1=\frac{12}{50}\cdot 100\%=[[fill:24]]\%$; $f_2=[[fill:46]]\%$; $f_3=[[fill:30]]\%$; vẽ theo 3 bước SGK (trục, các cột liền nhau cao bằng tần số tương đối, chú giải); "Ta được biểu đồ:"[[HINH:VD7_bd]] Vậy ….
8. Bài 14. level 2, dang_id "TH4", 2 thẻ — (Thi thử vào 10 lần 3 Phòng GD\&ĐT Ứng Hòa, 2024--2025): "Một lớp gồm 40 học sinh được khảo sát về chiều cao, ta có bảng tần số ghép nhóm dưới đây." [[HINH:B14]] a) [TH] Lập bảng tần số tương đối ghép nhóm cho bảng trên. b) [TH] Vẽ biểu đồ tần số ghép nhóm dạng cột cho bảng tần số ghép nhóm trên. Đáp số 12,5\%; 37,5\%; 30\%; 20\%; b) solution mô tả cách vẽ (các cột liền nhau, chiều cao bằng tần số 5; 15; 12; 8) rồi [[HINH:B14_bd]]. hints 2 câu.
9. Ví dụ 8 — (Thi thử vào 10 lần 2 THCS Thọ Lộc, 2025--2026): "Tại một trại hè thanh thiếu niên quốc tế, người ta tìm hiểu xem mỗi đại biểu tham dự có thể sử dụng được bao nhiêu ngoại ngữ. Kết quả như bảng sau." [[HINH:VD8]] "a) Tính tỉ lệ phần trăm đại biểu sử dụng được ít nhất 2 ngoại ngữ.[[br]]b) Ở trại hè tổ chức một năm trước đó, có $54$ trong tổng số $220$ đại biểu sử dụng được từ 3 ngoại ngữ trở lên. Có ý kiến cho rằng tỉ lệ đại biểu sử dụng được từ 3 ngoại ngữ trở lên đã tăng giữa hai năm. Ý kiến đó đúng hay sai?" Lời giải: $n=84+64+24+16+12=[[fill:200]]$; ít nhất 2 ngoại ngữ: $64+24+16+12=[[fill:116]]$, tỉ lệ $\frac{116}{200}\cdot 100\%=[[fill:58]]\%$; năm nay từ 3 trở lên $24+16+12=[[fill:52]]$, tỉ lệ $[[fill:26]]\%$; năm trước $\frac{54}{220}\cdot 100\%\approx[[fill:24{,}55]]\%$; vì $26\%>24{,}55\%$ nên ý kiến [[fill:đúng]]. Vậy ….
10. Bài 15. level 3, dang_id "VD1", MỘT thẻ "[VD]" đầu statement (ý a, b không gắn thẻ) — (Bộ đề minh họa tuyển sinh lớp 10 Phòng GD\&ĐT Đống Đa, Đề 14 THCS Thái Thịnh, 2025--2026): "[VD] Biểu đồ dưới đây cho biết số lượng các loại ô tô một cửa hàng bán được trong năm 2023." [[HINH:B15_bd]] "a) Lập bảng tần số và bảng tần số tương đối cho dữ liệu được biểu diễn trên biểu đồ.[[br]]b) Giả sử tỉ lệ các loại xe bán được không đổi và cửa hàng bán được tổng số $240$ ô tô các loại trong năm 2024. Hãy ước lượng số ô tô 4 chỗ cửa hàng bán được." Đáp số: tần số 35; 20; 15; 10; $n=80$; tần số tương đối 43,75\%; 25\%; 18,75\%; 12,5\%; b) $240\cdot 43{,}75\%=105$ xe. hints [].
11. Ví dụ 9 — (Thi thử vào 10 Cụm trường THCS công lập, 2026--2027): "Một cửa hàng bán đồ chơi cho trẻ em thống kê số tiền (đơn vị: nghìn đồng) mà 60 khách hàng mua đồ ở cửa hàng đó trong một ngày. Số liệu được ghi lại trong biểu đồ tần số ghép nhóm sau." [[HINH:VD9_bd]] "a) Tính tần số tương đối ghép nhóm của nhóm $[80;90)$.[[br]]b) Chủ cửa hàng nhận xét: có không ít hơn $70\%$ số người mua hàng với số tiền từ $60$ nghìn đồng đến dưới $80$ nghìn đồng. Nhận xét đó đúng hay sai?" Lời giải: $n=3+6+19+23+9=[[fill:60]]$; a) $f=\frac{9}{60}\cdot 100\%=[[fill:15]]\%$; b) từ 60 đến dưới 80 nghìn đồng gồm hai nhóm $[60;70)$ và $[70;80)$, có $19+23=[[fill:42]]$ người, chiếm $\frac{42}{60}\cdot 100\%=[[fill:70]]\%$; vì $70\%\ge 70\%$ nên nhận xét [[fill:đúng]]. Vậy ….
12. Bài 16. ĐÍCH — level 3, dang_id "VD2", MỘT thẻ "[VD]" đầu statement (ý a–d không gắn thẻ) — (Câu I.1 đề giữa kì II THCS Nam Từ Liêm, 2025--2026): "[VD] Một đội công nhân tham gia hội thi tay nghề giỏi. Mỗi công nhân phải hoàn thành bài thi (lí thuyết và thực hành) trong thời gian $120$ phút. Biểu đồ tần số ghép nhóm dưới đây biểu diễn thời gian hoàn thành bài thi của các công nhân trong đội." [[HINH:B16_bd]] "a) Lập bảng tần số ghép nhóm theo mẫu sau (kẻ bảng vào vở).[[HINH:B16]]b) Xác định tần số tương đối của nhóm $[105;110)$.[[br]]c) Nhóm công nhân hoàn thành bài thi muộn nhất chiếm bao nhiêu phần trăm?[[br]]d) Tính số công nhân đã hoàn thành bài thi trước khi hết giờ trên $20$ phút." Đáp số: tần số 3; 5; 6; 7; 9; 10; $N=40$; b) $\frac{7}{40}\cdot 100\%=17{,}5\%$; c) nhóm muộn nhất là $[115;120)$, $\frac{10}{40}\cdot 100\%=25\%$; d) hoàn thành trước khi hết giờ trên 20 phút nghĩa là thời gian làm bài dưới $120-20=100$ phút, gồm nhóm $[90;95)$ và $[95;100)$: $3+5=8$ công nhân. hints [].
- teacher_note chặng 4: khoảng 80 phút; Bài 11–14 mỗi ý khoảng 6 phút, chữa theo cặp; Bài 15 và Bài 16 làm cá nhân rồi gọi lên bảng; Bài 16 là đích của buổi học, chấm theo từng ý.

## Đầu ra
JSON đúng schema: {"stages": [4 chặng trên, đúng thứ tự], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''

VIEC2 = r'''
## Việc của bạn: dựng chặng 5 — {"kind":"reflection","number":5,"title":"Tổng kết"} (sơ đồ tư duy + BÀI TẬP VỀ NHÀ)
Bài tập về nhà in thành phiếu riêng. Thứ tự khối:
1. mindmap: "root": "Tần số và tần số tương đối", "caption": "Điền các ô trống để tự tóm tắt cả buổi", bốn nhánh, chỉ khoét ô [[blank:…]] ở chỗ cần nhớ:
   - "Bảng tần số": con "Tần số là số lần [[blank:2cm]]"; con "Cỡ mẫu $n=$ [[blank:2cm]] các tần số".
   - "Tần số tương đối": con "$f=\frac{m}{n}\cdot$ [[blank:1.4cm]]"; con "Tổng các $f$ bằng [[blank:1.4cm]]".
   - "Biểu đồ": con "Tần số: dạng cột, dạng [[blank:1.8cm]]"; con "Quạt tròn: số đo cung $=360^\circ\cdot$ [[blank:1cm]]".
   - "Ghép nhóm": con "$[a;b)$: từ $a$ đến [[blank:1.8cm]] $b$"; con "Biểu đồ ghép nhóm: các cột [[blank:1.6cm]]".
2. para: "\textbf{Bài tập về nhà} — làm vào vở, buổi sau nộp."
3. Sáu bài BTVN (tier "btvn", label nối tiếp "Bài 17." … "Bài 22."), tự trình bày, KHÔNG ô điền, KHÔNG \ldots trong statement. Thứ tự dễ → khó:
- Bài 17. level 1, dang_id "NB3", 3 thẻ — (Giữa kì II THCS Trưng Vương, 2025--2026): "Kết quả điểm khảo sát tháng 2 môn Toán của học sinh lớp 9G được thống kê trong bảng tần số sau." [[HINH:T1]] a) [NB] Lớp 9G có bao nhiêu học sinh? b) [NB] Tính tần số tương đối của điểm $9$. c) [NB] Tính tần số tương đối của điểm $10$. Đáp số $n=40$; 17,5\%; 10\%.
- Bài 18. level 1, dang_id "NB6", 3 thẻ — (Cuối kì II Phòng GD\&ĐT Gia Lâm, 2024--2025): "Một nhà may thống kê chiều cao (đơn vị: cm) của 40 học sinh một lớp 9 để may đồng phục. Sau khi ghép nhóm, nhà may nhận được bảng tần số ghép nhóm sau." [[HINH:T2]] a) [NB] Tìm tần số ghép nhóm của nhóm $[160;165)$ và của nhóm $[165;170)$. b) [NB] Tìm tần số tương đối ghép nhóm của nhóm $[160;165)$. c) [NB] Tìm tần số tương đối ghép nhóm của nhóm $[165;170)$. Đáp số 10 và 12; 25\%; 30\%.
- Bài 19. level 2, dang_id "TH1", 2 thẻ — (Cuối kì II THCS Hát Môn, 2025--2026): "Điểm bài kiểm tra môn Toán học kì I của 32 học sinh lớp 9 được ghi lại như sau:" + dãy (2 dòng, mỗi dòng 16 số): $7;\;4;\;4;\;6;\;6;\;4;\;6;\;8;\;8;\;7;\;2;\;6;\;4;\;8;\;5;\;6$ / $9;\;8;\;4;\;7;\;9;\;5;\;5;\;5;\;7;\;2;\;7;\;6;\;7;\;8;\;6;\;10$ + a) [TH] Lập bảng tần số. b) [TH] Tìm tần số tương đối của điểm $8$ và điểm $9$ (làm tròn kết quả đến hàng phần trăm). Đáp số: điểm 2:2, 4:5, 5:4, 6:7, 7:6, 8:5, 9:2, 10:1 (tổng 32); $\frac{5}{32}\cdot 100\%=15{,}625\%\approx 15{,}63\%$; $\frac{2}{32}\cdot 100\%=6{,}25\%$. hints 2 câu.
- Bài 20. level 2, dang_id "TH4", 2 thẻ — (Cuối kì II THCS Nghĩa Tân, 2025--2026): "Sau khi điều tra cân nặng (đơn vị: kg) của các học sinh trong một lớp, người ta thu được biểu đồ tần số ghép nhóm sau." [[HINH:T4_bd]] a) [TH] Xác định tần số và tần số tương đối của nhóm $[50;55)$. b) [TH] Lập bảng tần số tương đối ghép nhóm cho dữ liệu trên biểu đồ. Đáp số: $n=3+5+9+15+10+5+3=50$; 15 và 30\%; 6\%; 10\%; 18\%; 30\%; 20\%; 10\%; 6\% (tổng 100\%). hints 2 câu.
- Bài 21. level 2, dang_id "TH3", 2 thẻ — (Giữa kì II THCS Phúc Đồng, 2024--2025): "Đo chiều cao (đơn vị: cm) của học sinh lớp 9/1 cho kết quả như sau:" + dãy (4 dòng, mỗi dòng 10 số): $156;\;157;\;161;\;158;\;166;\;160;\;162;\;157;\;163;\;160$ / $163;\;164;\;158;\;159;\;166;\;162;\;161;\;165;\;163;\;163$ / $162;\;159;\;165;\;163;\;162;\;161;\;155;\;159;\;158;\;164$ / $165;\;162;\;161;\;160;\;164;\;162;\;161;\;162;\;166;\;160$ + a) [TH] Lập bảng tần số ghép nhóm với các nhóm $[155;158)$, $[158;161)$, $[161;164)$, $[164;167)$. b) [TH] Lập bảng tần số tương đối ghép nhóm. Đáp số: 4; 10; 17; 9 (tổng 40); 10\%; 25\%; 42,5\%; 22,5\%. hints 2 câu.
- Bài 22. level 3, dang_id "VD2", MỘT thẻ "[VD]" đầu statement — (Tài liệu Mathtech "Tần số ghép nhóm. Tần số ghép nhóm tương đối", Dạng 2, Bài 3): "[VD] Biểu đồ dưới đây mô tả tuổi thọ (đơn vị: nghìn giờ) của $100$ chiếc bóng đèn dây tóc trong một lô sản xuất." [[HINH:T6_bd]] "a) Lập bảng tần số ghép nhóm mô tả dữ liệu ở biểu đồ.[[br]]b) Một bóng đèn được cho là thuộc loại I nếu có tuổi thọ từ $1\,500$ giờ trở lên. Hỏi có bao nhiêu bóng đèn thuộc loại I trong số các bóng đèn được thống kê?" Đáp số: a) tần số $m=100\cdot f$: 18; 21; 56; 5; b) $1\,500$ giờ $=1{,}5$ nghìn giờ, gồm nhóm $[1{,}5;1{,}75)$ và $[1{,}75;2)$: $56+5=61$ bóng. hints [].
- teacher_note chặng 5: sơ đồ tư duy điền 5 phút cuối buổi; bài tập về nhà gồm Bài 17 đến Bài 22, in phiếu riêng; buổi sau chữa Bài 21 và Bài 22 trước.

## Đầu ra
JSON đúng schema: {"stages": [chỉ chặng 5], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''

VIEC3 = r'''
## Việc của bạn: soạn THÊM 3 bài tập về nhà (giáo viên duyệt: phiếu bài tập về nhà đang thiếu giờ)
Trả về JSON {"stages":[{"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":"","blocks":[3 khối problem theo thứ tự dưới]}],"ghi_chu":""}. Mỗi khối: tier "btvn", label tạm "Bài A.", "Bài B.", "Bài C." (máy đánh số lại), tự trình bày, KHÔNG ô điền, KHÔNG \\ldots trong statement; level 2 có "hints" 2 câu hỏi gợi mở; level 3 "hints": [].
- Bài A. level 2, dang_id "TH1" — (Kiểm tra học kì II Phòng GD\\&ĐT Cầu Giấy, 2024--2025): "Một trường trung học cơ sở khảo sát thời gian tiếp xúc với các thiết bị điện tử (điện thoại thông minh, máy tính bảng, máy tính, ti vi) trung bình trong một ngày của 150 học sinh và biểu diễn kết quả trong biểu đồ sau." [[HINH:T7_bd]] "a) [NB] Lập bảng tần số cho dữ liệu được biểu diễn trên biểu đồ.[[br]]b) [TH] Các chuyên gia khuyến nghị thời gian tiếp xúc các thiết bị điện tử an toàn là ít hơn $2$ giờ mỗi ngày. Trong $150$ học sinh tham gia khảo sát, có bao nhiêu phần trăm học sinh đã thực hiện đúng khuyến nghị trên?" Đáp số: thời gian $0{,}5;\;1;\;2;\;3;\;4$ giờ có tần số $15;\;36;\;48;\;39;\;12$ (tổng $150$); ít hơn 2 giờ gồm $0{,}5$ giờ và $1$ giờ: $15+36=51$ học sinh, $\\frac{51}{150}\\cdot 100\\%=34\\%$.
- Bài B. level 2, dang_id "TH4" — (Bộ đề minh họa tuyển sinh lớp 10 Phòng GD\\&ĐT Đống Đa, Đề 12 THCS Quang Trung, 2025--2026): "Sau khi theo dõi thời gian làm bài tập (đơn vị: phút) của $30$ học sinh, một thầy giáo đã có biểu đồ tần số ghép nhóm dưới đây." [[HINH:T8_bd]] "a) [TH] Lập bảng tần số tương đối ghép nhóm gồm ba nhóm $[5;10)$, $[10;15)$, $[15;20)$ (làm tròn đến hàng phần trăm).[[br]]b) [TH] Thầy giáo yêu cầu giải bài toán dưới $15$ phút. Số bạn không đạt yêu cầu chiếm bao nhiêu phần trăm?" Đáp số: $\\frac{15}{30}\\cdot 100\\%=50\\%$; $\\frac{13}{30}\\cdot 100\\%\\approx 43{,}33\\%$; $\\frac{2}{30}\\cdot 100\\%\\approx 6{,}67\\%$ (tổng $100\\%$); không đạt là làm từ $15$ phút trở lên, thuộc nhóm $[15;20)$, chiếm khoảng $6{,}67\\%$.
- Bài C. level 3, dang_id "VD1" — (Tài liệu Mathtech "Tần số. Tần số tương đối", Dạng 2, Bài 10): "Kiểm tra khối lượng một số hộp sữa chua được lấy ngẫu nhiên từ thành phẩm của máy đóng hộp X, nhà máy chế biến sữa thu được bảng sau." [[HINH:T9]] "a) [TH] Lập bảng tần số tương đối và vẽ biểu đồ tần số tương đối dạng hình quạt tròn biểu diễn dữ liệu đã cho.[[br]]b) [TH] Những hộp cân nặng từ $95$ g đến $105$ g được xem là đạt yêu cầu về khối lượng. Trong $80$ hộp sữa chua được kiểm tra có bao nhiêu phần trăm hộp đạt yêu cầu?[[br]]c) [VD] Máy đóng hộp được xem là vận hành tốt nếu trên $90\\%$ sản phẩm có chất lượng đạt yêu cầu. Nếu $80$ hộp sữa chua này đại diện được cho sản phẩm của máy X thì có thể xem máy này vận hành tốt hay không?" Đáp số: a) $8{,}75\\%$; $22{,}5\\%$; $47{,}5\\%$; $11{,}25\\%$; $10\\%$ (tổng $100\\%$), số đo cung $31{,}5^\\circ$; $81^\\circ$; $171^\\circ$; $40{,}5^\\circ$; $36^\\circ$, solution có [[HINH:T9_quat]]; b) các hộp $96$ g, $100$ g, $105$ g: $18+38+9=65$ hộp, $\\frac{65}{80}\\cdot 100\\%=81{,}25\\%$; c) $81{,}25\\%<90\\%$ nên không thể xem máy vận hành tốt.
'''


def mau_khoi():
    d = json.loads((REPO / MAU).read_text())
    out, seen = [], set()
    for s in d["stages"]:
        for b in s["blocks"]:
            k = (s["kind"], b["type"], b.get("variant"), bool(b.get("hints")))
            if k not in seen and b["type"] in ("noted", "problem", "para", "mindmap"):
                seen.add(k)
                out.append(b)
    return out[:12]


def main():
    du_lieu = ("\n## Mẫu khối (phiếu đại số kiểu mới đã duyệt, chỉ để xem khuôn — KHÔNG chép nội dung)\n"
               + json.dumps(mau_khoi(), ensure_ascii=False, indent=1) + "\n")
    import sys
    viec_ds = (("gop-9c-ch7-btvn-them", VIEC3),) if "--them" in sys.argv else (
        ("gop-9c-ch7-tren-lop", VIEC1), ("gop-9c-ch7-btvn", VIEC2))
    for vid, phan in viec_ds:
        viec = {"id": vid, "model": "gemini-4-hydrogen-medium", "prompt": CHUNG + phan + du_lieu,
                "files": [], "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1500s",
                "meta": {"loai": "gop-phieu", "seed_dich": f"{D}/{SLUG}.json"}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(viec['prompt'])//1000}k ký tự)")


if __name__ == "__main__":
    main()
