"""Dựng lại phiếu C chương X lớp 9C (12/11/2026) — Luyện tập chung 45′ + KT chương 45′.

Thầy chốt 12/11: đích = Câu IV.1 đề chính thức Vào 10 năm 2026 (trọn hai ý); hiệu hai khối
(Ba Đình) + ghép khối chuyển hẳn sang BTVN. Chạy TỪ GỐC REPO:
    .venv/bin/python inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10/phieu-c/lap_phieu_c.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

OUT = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/"
           "phieu-c-luyen-tap-chung-va-bai-tap-cuoi-chuong-x.json")
PI = 3.14

# ── kiểm đáp số (π ≈ 3,14) ───────────────────────────────────────────────────
def near(a, b, eps=1e-6):
    assert abs(a - b) < eps, (a, b)

near(PI * 5**2 * 15, 1177.5)                       # Bài 3 Thái Thịnh
near(PI * 0.2**2 * 0.4, 0.05024)                   # Ví dụ 1 Mai Dịch
near(PI * 3**2 * 5, 141.3)                         # Bài 4 Hai Bà Trưng
near(0.9 * 200, 180); near(1000 / 180, 5.5555, 1e-3)   # Bài 5
near(PI * 15**2 * 40, 28260); near(PI * 60**2 * 150, 1695600); near(1695600 / 28260, 60)  # Ví dụ 2
near(2 * PI * 12 * 25, 1884); near(PI * 12**2 * 25, 11304)                 # Bài 6 (đích)
near(0.8 * 11304, 9043.2); near(150 / 9.0432, 16.587, 1e-3)
near(PI * 11**2 * 30, 11398.2)                     # BTVN 3
near(PI * 0.5**2 * 1.75, 1.37375); near(PI * 0.5**2 * 0.75, 0.58875)     # BTVN 4
near(8 * 12 * 20, 1920); near(PI * 2.5**2 * 12, 235.5); near(0.9 * 235.5, 211.95)
near(1920 / 211.95, 9.0587, 1e-3)                  # BTVN 5
near(PI * 1**2 * 1.55, 4.867); near(PI * 1.1**2 * 1.6, 6.07904)
near(6.07904 - 4.867, 1.21204)                     # BTVN 6
near(PI * 5**2 * 12, 942); near(2 / 3 * PI * 5**3, 261.6667, 1e-3)       # BTVN 7
near(942 + 2 / 3 * PI * 125, 1203.667, 1e-3)
near(2 * PI * 6 * 12, 452.16); near(PI * 6**2 * 12, 1356.48)           # BTVN 5 Cầu Diễn
near(PI * 0.5**2 * 1.8, 1.413); near(1.413 / 2, 0.7065)                  # BTVN 8

# ── hình ─────────────────────────────────────────────────────────────────────
HEAD = "\\begin{tikzpicture}[line width=0.8pt, font=\\small]\n"
TAIL = "\\end{tikzpicture}"


def tru(rx=1.0, h=2.0, nuoc=None, r_lab=None, d_lab=None, h_lab=None, n_lab=None, x0=0.0,
        mo=False):
    """Hình trụ đứng tâm đáy (x0,0). nuoc = chiều cao mực nước (đơn vị vẽ)."""
    ry = round(0.32 * rx, 3)
    L, R = x0 - rx, x0 + rx
    s = ""
    if nuoc is not None:
        s += (f"  \\fill[info!25] ({L},{nuoc}) -- ({L},0) arc (180:360:{rx} and {ry}) -- ({R},{nuoc}) "
              f"arc (0:180:{rx} and {ry}) -- cycle;\n"
              f"  \\fill[info!40] ({x0},{nuoc}) ellipse ({rx} and {ry});\n"
              f"  \\draw[ink] ({x0},{nuoc}) ellipse ({rx} and {ry});\n")
    s += (f"  \\draw[ink] ({x0},{h}) ellipse ({rx} and {ry});\n"
          f"  \\draw[ink] ({L},0) arc (180:360:{rx} and {ry});\n"
          f"  \\draw[ink, dashed] ({L},0) arc (180:0:{rx} and {ry});\n"
          f"  \\draw[ink] ({L},0) -- ({L},{h});\n  \\draw[ink] ({R},0) -- ({R},{h});\n")
    if r_lab:
        s += (f"  \\fill[ink] ({x0},{h}) circle (1.2pt);\n  \\draw[ink, ->] ({x0},{h}) -- ({R},{h});\n"
              f"  \\node[above, font=\\scriptsize] at ({x0 + rx / 2},{h + 0.04}) {{{r_lab}}};\n")
    if d_lab:
        s += (f"  \\draw[ink, <->] ({L},{h}) -- ({R},{h});\n"
              f"  \\node[anchor=center, font=\\scriptsize, fill=white, inner sep=1pt] at ({x0},{h}) {{{d_lab}}};\n")
    if h_lab:
        s += (f"  \\draw[ink, <->] ({R + 0.3},0) -- ({R + 0.3},{h});\n"
              f"  \\node[right, font=\\scriptsize] at ({R + 0.35},{h / 2}) {{{h_lab}}};\n")
    if n_lab and nuoc is not None:
        s += (f"  \\draw[ink, <->] ({L - 0.3},0) -- ({L - 0.3},{nuoc});\n"
              f"  \\node[left, font=\\scriptsize] at ({L - 0.35},{nuoc / 2}) {{{n_lab}}};\n")
    return s


def cau(R=1.1, d_lab=None, r_lab=None):
    s = (f"  \\draw[ink] (0,0) circle ({R});\n"
         f"  \\draw[ink] (-{R},0) arc (180:360:{R} and {round(0.3 * R, 3)});\n"
         f"  \\draw[ink, dashed] (-{R},0) arc (180:0:{R} and {round(0.3 * R, 3)});\n"
         f"  \\fill[ink] (0,0) circle (1.2pt);\n")
    if d_lab:
        s += (f"  \\draw[ink, <->] (-{R},0) -- ({R},0);\n"
              f"  \\node[above, font=\\scriptsize, fill=white, inner sep=1pt] at (0.45,0.05) {{{d_lab}}};\n")
    if r_lab:
        s += (f"  \\draw[ink, ->] (0,0) -- (40:{R});\n"
              f"  \\node[above left, font=\\scriptsize] at (0.42,0.4) {{{r_lab}}};\n")
    return s


def non(r_lab, l_lab):
    return ("  \\draw[ink] (0,0) ellipse (1.05 and 0.336);\n"
            "  \\draw[ink] (-1.05,0) -- (0,1.9) -- (1.05,0);\n"
            "  \\draw[ink, dashed] (0,0) -- (0,1.9);\n  \\fill[ink] (0,0) circle (1.2pt);\n"
            "  \\draw[ink, ->] (0,0) -- (1.05,0);\n"
            f"  \\node[below, font=\\scriptsize] at (0.5,-0.36) {{{r_lab}}};\n"
            f"  \\node[right, font=\\scriptsize] at (0.6,1.05) {{{l_lab}}};\n")


def fig(body, width="0.22", given=True):
    return {"type": "tikz", "tikz": HEAD + body + TAIL, "pos": "right", "width": width,
            "caption": "Hình ?"}


LG = "{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]"

# ── KHÁM PHÁ ─────────────────────────────────────────────────────────────────
opener_tikz = (HEAD + tru(0.55, 1.1, nuoc=0.75, x0=0) +
               "  \\draw[ink, ->, thick] (0.85,0.9) .. controls (1.4,1.5) .. (2.0,1.1);\n"
               "  \\node[above, font=\\scriptsize] at (1.4,1.45) {$80\\%$};\n" +
               tru(1.0, 1.6, nuoc=0.35, x0=3.2) +
               "  \\node[below, font=\\scriptsize] at (0,-0.35) {xô};\n"
               "  \\node[below, font=\\scriptsize] at (3.2,-0.45) {bể $150$ lít};\n" + TAIL)

kham_pha = {
    "kind": "review", "number": 1, "title": "Khám phá",
    "teacher_note": "Buổi cuối của chương X: 45 phút luyện tập rồi 45 phút kiểm tra chương. GV hỏi nhanh cả lớp: múc một xô đầy rồi chỉ đổ được 80\\% thì mỗi lần vào bể bao nhiêu? Tính ra 16,6 lần thì phải múc 16 hay 17 lần?",
    "blocks": [
        {"type": "opener", "tikz": opener_tikz,
         "text": "Nhà Lan cần đổ đầy một bể nước $150$ lít bằng một chiếc xô. Mỗi lần múc đầy xô nhưng đi đường bị sánh ra ngoài, chỉ còn khoảng $80\\%$ đổ được vào bể. Lan bấm máy tính ra $16{,}6$ lần rồi bảo: \\emph{\"Múc $16$ lần là xong!\"}. Lan nói đúng không? Nếu múc $16$ lần thì bể đã đầy chưa?"},
        {"type": "noted", "variant": "note", "title": "NHẮC LẠI",
         "text": "$\\bullet$ Bán kính bằng nửa đường kính: $r = d : 2$.[[br]]$\\bullet$ $a\\%$ của một số $x$ là $x\\cdot \\dfrac{a}{100}$; ví dụ $80\\%$ của $500$ là $500\\cdot 0{,}8 = 400$.[[br]]$\\bullet$ $1$ lít $= 1$ dm$^3 = 1000$ cm$^3$; $\\quad 1$ m$^3 = 1000$ lít; $\\quad 1$ ml $= 1$ cm$^3$.[[br]]$\\bullet$ Bài hỏi \\emph{\"cần ít nhất bao nhiêu lần\"} mà phép chia ra số thập phân thì làm tròn LÊN: thiếu một lần là chưa đủ."},
        {"type": "noted", "variant": "target", "title": "MỤC TIÊU BUỔI HỌC",
         "text": "$\\bullet$ Lấy trọn $1{,}0$ điểm Câu IV.1 đề Vào 10: ý a thay số đúng công thức, ý b một bước thực tế.[[br]]$\\bullet$ Ôn lại sáu công thức của chương và ba bẫy: đường kính, chiều cao theo mực nước, đổi đơn vị.[[br]]$\\bullet$ Luyện khuôn ĐẾM SỐ LẦN của đề chính thức năm 2026: lấy phần trăm, đổi đơn vị, chia rồi làm tròn LÊN."},
    ],
}

# ── KIẾN THỨC ────────────────────────────────────────────────────────────────
kien_thuc = {
    "kind": "concept", "number": 2, "title": "Kiến thức cần nhớ",
    "teacher_note": "Chốt nhanh khoảng 5 phút: cho cả lớp đọc đồng thanh sáu công thức, rồi chỉ vào Hình 2 hỏi phần nước có chiều cao bao nhiêu.",
    "blocks": [
        {"type": "noted", "variant": "theory", "title": "1. SÁU CÔNG THỨC CỦA CHƯƠNG X",
         "text": "\\nhanly{Hình trụ} (bán kính đáy $r$, chiều cao $h$): $S_{xq} = 2\\pi rh$; $\\quad V = \\pi r^2h$.[[br]]\\nhanly{Hình nón} (bán kính đáy $r$, chiều cao $h$, đường sinh $l$): $S_{xq} = \\pi rl$; $\\quad V = \\dfrac{1}{3}\\pi r^2h$; $\\quad l^2 = r^2 + h^2$.[[br]]\\nhanly{Hình cầu} (bán kính $R$): $S = 4\\pi R^2$; $\\quad V = \\dfrac{4}{3}\\pi R^3$.[[br]]Diện tích đo bằng cm$^2$, m$^2$; thể tích đo bằng cm$^3$, m$^3$, lít.",
         "figure": fig(tru(0.9, 1.8, r_lab="$r$", h_lab="$h$"), "0.24")},
        {"type": "noted", "variant": "theory", "title": "2. CHIỀU CAO LẤY THEO PHẦN NƯỚC ĐANG XÉT",
         "text": "\\nhanly{Nước trong bình trụ} là một hình trụ cùng bán kính đáy $r$ với bình, chiều cao bằng MỰC NƯỚC $h_1$: $V_{\\text{nước}} = \\pi r^2h_1$.[[br]]\\nhanly{Phần còn trống} (cần rót thêm cho đầy) cao $h - h_1$: $V_{\\text{trống}} = \\pi r^2(h - h_1)$.[[br]]\\nhanly{Nước đã dùng} khi mực nước hạ từ $h_1$ xuống $h_2$: $V_{\\text{dùng}} = \\pi r^2(h_1 - h_2)$.[[br]]Mực nước cho bằng phân số (\\emph{bằng $\\dfrac{2}{3}$ chiều cao}) thì tính $h_1$ trước rồi mới thay số.",
         "figure": fig(tru(0.9, 1.8, nuoc=1.1, r_lab="$r$", h_lab="$h$", n_lab="$h_1$"), "0.26")},
        {"type": "noted", "variant": "theory", "title": "3. KHUÔN ĐẾM SỐ LẦN",
         "text": "\\nhanly{Bước 1.} Tính thể tích một lần đổ (nhân phần trăm nếu đề cho, ví dụ $80\\%$ thể tích xô).[[br]]\\nhanly{Bước 2.} Đổi về CÙNG đơn vị với thể tích cần đổ đầy.[[br]]\\nhanly{Bước 3.} Số lần $=$ thể tích cần đổ đầy $:$ thể tích một lần.[[br]]\\nhanly{Bước 4.} Chia hết thì lấy đúng thương; ra số thập phân thì làm tròn LÊN (ra $16{,}59$ thì cần ít nhất $17$ lần, vì $16$ lần bể chưa đầy)."},
        {"type": "noted", "variant": "trap", "title": "BA BẪY VÀ HAI LỖI TRÌNH BÀY",
         "text": "$\\bullet$ Đề cho ĐƯỜNG KÍNH mà thay thẳng vào chỗ bán kính.[[br]]$\\bullet$ Lấy chiều cao CẢ BÌNH trong khi đề hỏi phần nước, phần trống hoặc phần đã dùng.[[br]]$\\bullet$ Không đổi đơn vị: ra cm$^3$ mà trả lời bằng lít, hoặc chia lít cho cm$^3$.[[br]]$\\bullet$ Làm tròn XUỐNG ở bài đếm số lần.[[br]]$\\bullet$ Thiếu đơn vị hoặc thiếu câu \\emph{\"Vậy …\"} ở cuối mỗi ý: barem trừ $0{,}25$ điểm."},
    ],
}

# ── LUYỆN TẬP 1 ──────────────────────────────────────────────────────────────
lt1 = {
    "kind": "practice1", "number": 3, "title": "Luyện tập 1",
    "teacher_note": "Bài 1, 2 cho cả lớp giơ bảng chọn đáp án. Bài 3, 4 soát từng ô trống: ô chiều cao là chỗ HS sai nhiều nhất. Bài 5 là kiến thức lớp 6 dùng ngay ở ý b của bài đích.",
    "blocks": [
        {"type": "para",
         "text": "\\textbf{Đích của buổi học:} Câu IV.1 đề chính thức Vào 10 năm 2026 (Bài 7) — ý a tính diện tích xung quanh của xô hình trụ (Mạch 1), ý b múc $80\\%$ thể tích xô để đổ đầy bể $150$ lít: tính thể tích theo đúng phần nước (Mạch 2), lấy phần trăm và làm tròn LÊN (Mạch 3)."},
        {"type": "para", "variant": "heading", "text": "Mạch 1. Sáu công thức và bẫy đường kính"},
        {"type": "problem", "tier": "onclass", "level": 1, "dang_id": "NB1", "label": "Bài 1.",
         "figure_given": True, "figure": fig(cau(1.05, d_lab="$10$ cm")),
         "statement": "[NB] Diện tích mặt cầu có đường kính $10$ cm (Hình ?) là",
         "options": ["$10\\pi$ cm$^2$", "$400\\pi$ cm$^2$", "$50\\pi$ cm$^2$", "$100\\pi$ cm$^2$"],
         "answer": "D",
         "solution": "Bán kính mặt cầu là $R = 10 : 2 = 5$ (cm).[[br]]Diện tích mặt cầu là $S = 4\\pi R^2 = 4\\pi\\cdot 5^2 = 100\\pi$ (cm$^2$).[[br]]Vậy chọn D. (Chọn B là thay nhầm đường kính $10$ cm vào chỗ bán kính.)"},
        {"type": "problem", "tier": "onclass", "level": 1, "dang_id": "NB1", "label": "Bài 2.",
         "figure_given": True, "figure": fig(non("$2$ cm", "$5$ cm")),
         "statement": "[NB] Cho hình nón có bán kính đáy $R = 2$ cm, độ dài đường sinh $l = 5$ cm (Hình ?). Diện tích xung quanh của hình nón đã cho bằng",
         "options": ["$\\dfrac{10\\pi}{3}$ cm$^2$", "$\\dfrac{50\\pi}{3}$ cm$^2$", "$20\\pi$ cm$^2$", "$10\\pi$ cm$^2$"],
         "answer": "D",
         "solution": "Diện tích xung quanh của hình nón là $S_{xq} = \\pi Rl = \\pi\\cdot 2\\cdot 5 = 10\\pi$ (cm$^2$).[[br]]Vậy chọn D."},
        {"type": "problem", "tier": "onclass", "level": 1, "dang_id": "NB2", "label": "Bài 3.",
         "figure_given": True,
         "figure": fig(tru(0.95, 2.0, nuoc=1.45, d_lab="$10$ cm", n_lab="$15$ cm"), "0.18"),
         "statement": "[NB] Một cái cốc hình trụ có đường kính đáy bằng $10$ cm đựng nước với mực nước trong cốc cao $15$ cm (Hình ?). Điền vào chỗ trống để hoàn thành bài giải tính thể tích lượng nước trong cốc (bỏ qua bề dày của thành cốc, lấy $\\pi \\approx 3{,}14$):[[br]]Bán kính đáy của cốc là $r = 10 : 2 = [[blank:1.6cm]]$ (cm).[[br]]Lượng nước trong cốc có dạng hình trụ bán kính đáy $r$, chiều cao bằng [[blank:2.6cm]] là $15$ cm.[[br]]Thể tích lượng nước trong cốc là[[br]]$V = [[blank:1.6cm]] \\approx 3{,}14\\cdot [[blank:1.6cm]]^2\\cdot 15 = [[blank:1.6cm]]$ ([[blank:1.6cm]]).[[br]]Vậy thể tích lượng nước trong cốc là [[blank:2.2cm]] cm$^3$.",
         "solution": "Bán kính đáy của cốc là $r = 10 : 2 = 5$ (cm).[[br]]Lượng nước trong cốc có dạng hình trụ bán kính đáy $5$ cm, chiều cao bằng mực nước là $15$ cm.[[br]]Thể tích lượng nước trong cốc là[[br]]$V = \\pi r^2h \\approx 3{,}14\\cdot 5^2\\cdot 15 = 1177{,}5$ (cm$^3$).[[br]]Vậy thể tích lượng nước trong cốc là $1177{,}5$ cm$^3$."},
        {"type": "para", "variant": "heading", "text": "Mạch 2. Chiều cao lấy theo phần nước đang xét"},
        {"type": "noted", "variant": "example",
         "figure": fig(tru(0.8, 2.1, nuoc=1.4, d_lab="$0{,}4$ m", h_lab="$0{,}6$ m"), "0.17"),
         "text": "\\textbf{Ví dụ 1.} \\textbf{(CK2 THCS Mai Dịch.)} Một xô nước inox hình trụ có chiều cao $0{,}6$ m, đường kính đáy $0{,}4$ m (Hình ?). Trong xô có chứa nước, mực nước đó bằng $\\dfrac{2}{3}$ chiều cao của xô. Tính thể tích nước có trong xô (lấy $\\pi \\approx 3{,}14$).[[br]]" + LG +
                 "Bán kính đáy của xô là $r = 0{,}4 : 2 = [[fill:0{,}2]]$ (m).[[br]]"
                 "Mực nước trong xô cao $h_1 = \\dfrac{2}{3}\\cdot 0{,}6 = [[fill:0{,}4]]$ (m).[[br]]"
                 "Nước trong xô là hình trụ bán kính đáy $r$, chiều cao $h_1$, nên thể tích nước là $V = [[fill:\\pi r^2h_1]] \\approx 3{,}14\\cdot [[fill:0{,}2]]^2\\cdot [[fill:0{,}4]] = [[fill:0{,}05024]]$ (m$^3$).[[br]]"
                 "Vậy thể tích nước có trong xô khoảng $[[fill:0{,}05024]]$ m$^3$, tức khoảng $[[fill:50{,}24]]$ lít."},
        {"type": "problem", "tier": "onclass", "level": 1, "dang_id": "NB3", "label": "Bài 4.",
         "figure_given": True,
         "figure": fig(tru(0.75, 2.0, nuoc=1.0, r_lab="$3$ cm", h_lab="$10$ cm"), "0.18"),
         "statement": "[NB] Một chiếc cốc thủy tinh dạng hình trụ có bán kính đáy bằng $3$ cm, chiều cao $10$ cm. Lượng nước hiện tại trong cốc có chiều cao bằng một nửa chiều cao của cốc (Hình ?). Điền vào chỗ trống để hoàn thành bài giải: cần rót thêm bao nhiêu mi-li-lít nước vào cốc để nước đầy tới miệng cốc, biết $1$ ml $= 1$ cm$^3$ (bỏ qua độ dày của thành cốc và đáy cốc, lấy $\\pi \\approx 3{,}14$):[[br]]Mực nước hiện tại cao $10 : 2 = [[blank:1.6cm]]$ (cm).[[br]]Phần còn trống của cốc có dạng hình trụ bán kính đáy $3$ cm, chiều cao $10 - 5 = [[blank:1.6cm]]$ (cm).[[br]]Thể tích phần còn trống là $V = \\pi r^2h \\approx 3{,}14\\cdot [[blank:1.6cm]]\\cdot [[blank:1.6cm]] = [[blank:1.6cm]]$ (cm$^3$).[[br]]Vậy cần rót thêm khoảng [[blank:1.6cm]] ml nước.",
         "solution": "Mực nước hiện tại cao $10 : 2 = 5$ (cm).[[br]]Phần còn trống của cốc có dạng hình trụ bán kính đáy $3$ cm, chiều cao $10 - 5 = 5$ (cm).[[br]]Thể tích phần còn trống là $V = \\pi r^2h \\approx 3{,}14\\cdot 3^2\\cdot 5 = 141{,}3$ (cm$^3$).[[br]]Vậy cần rót thêm khoảng $141{,}3$ ml nước."},
        {"type": "para", "variant": "heading", "text": "Mạch 3. Phần trăm, chia rồi làm tròn LÊN"},
        {"type": "problem", "tier": "onclass", "level": 1, "dang_id": "NB4", "label": "Bài 5.",
         "figure_given": False,
         "statement": "[NB] Mỗi lần rót, người ta chỉ rót vào bình một lượng nước bằng $90\\%$ của một cốc $200$ cm$^3$. Điền vào chỗ trống.[[br]]a) Mỗi lần rót được $200\\cdot 0{,}9 = [[blank:1.6cm]]$ (cm$^3$).[[br]]b) Bình $1$ lít chứa $[[blank:1.6cm]]$ cm$^3$.[[br]]c) $1000 : 180 \\approx [[blank:1.6cm]]$, nên muốn đổ đầy bình cần rót ít nhất $[[blank:1.6cm]]$ lần (rót $5$ lần mới được $[[blank:1.6cm]]$ cm$^3$, bình chưa đầy).",
         "solution": "a) Mỗi lần rót được $200\\cdot 0{,}9 = 180$ (cm$^3$).[[br]]b) Bình $1$ lít chứa $1000$ cm$^3$.[[br]]c) $1000 : 180 \\approx 5{,}56$, nên cần rót ít nhất $6$ lần (rót $5$ lần mới được $5\\cdot 180 = 900$ cm$^3$, bình chưa đầy)."},
    ],
}

lt_tikz = ("  \\draw[ink] (0,0) rectangle (1.2,1.6);\n  \\draw[ink] (0,1.6) -- (0.4,1.9) -- (1.6,1.9) -- (1.2,1.6);\n"
           "  \\draw[ink] (1.6,1.9) -- (1.6,0.3) -- (1.2,0);\n  \\draw[ink, dashed] (0,0) -- (0.4,0.3) -- (1.6,0.3);\n"
           "  \\draw[ink, dashed] (0.4,0.3) -- (0.4,1.9);\n"
           "  \\node[below, font=\\scriptsize] at (0.6,0) {$12$};\n  \\node[right, font=\\scriptsize] at (1.42,0.1) {$8$};\n"
           "  \\node[left, font=\\scriptsize] at (0,0.8) {$20$};\n" +
           tru(0.4, 1.1, nuoc=0.95, d_lab="$5$", h_lab="$12$", x0=2.6))
LANG = ({"type": "problem", "tier": "onclass", "level": 2, "dang_id": "TH1", "label": "Bài 6.",
           "figure_given": True, "figure": fig(lt_tikz, "0.34"),
           "statement": "[TH] \\textbf{(Đề minh hoạ vào 10 Phòng GD\\&ĐT Đống Đa, THCS Láng Thượng.)} Một bình nước hình hộp chữ nhật có chiều rộng, chiều dài đáy bình và chiều cao lần lượt là $8$ cm, $12$ cm, $20$ cm (Hình ?, đơn vị cm).[[br]]a) Tính thể tích nước tối đa mà bình chứa được.[[br]]b) Bình nước được rót ra các ly thủy tinh hình trụ có đường kính đáy là $5$ cm, chiều cao $12$ cm. Biết bình đựng đầy nước và khi rót vào ly, nước chiếm $90\\%$ thể tích của ly. Tính số ly cần dùng để chứa hết số nước từ bình (lấy $\\pi \\approx 3{,}14$).",
           "hints": ["Ý a: thể tích hình hộp chữ nhật tính thế nào (đã học ở lớp 7)?",
                     "Ý b: mỗi ly chứa được bao nhiêu nước? Chia xong ra số thập phân thì lấy bao nhiêu ly?"],
           "solution": "a) Thể tích nước tối đa bình chứa được là $V = 8\\cdot 12\\cdot 20 = 1920$ (cm$^3$).[[br]]Vậy bình chứa được tối đa $1920$ cm$^3$ nước.[[br]]b) Bán kính đáy của ly là $r = 5 : 2 = 2{,}5$ (cm).[[br]]Thể tích của một ly là $V_{\\text{ly}} = \\pi r^2h \\approx 3{,}14\\cdot 2{,}5^2\\cdot 12 = 235{,}5$ (cm$^3$).[[br]]Lượng nước rót vào mỗi ly là $235{,}5\\cdot 90\\% = 211{,}95$ (cm$^3$).[[br]]Ta có $1920 : 211{,}95 \\approx 9{,}06$.[[br]]Vì $9$ ly chưa chứa hết nước nên phải làm tròn lên.[[br]]Vậy cần $10$ ly để chứa hết số nước từ bình."})

# ── LUYỆN TẬP 2 ──────────────────────────────────────────────────────────────
vd2_tikz = (tru(0.45, 1.0, r_lab="$15$", h_lab="$40$", x0=0) +
            tru(1.1, 1.9, r_lab="$60$", h_lab="$150$", x0=2.6) +
            "  \\node[below, font=\\scriptsize] at (0,-0.3) {thùng};\n"
            "  \\node[below, font=\\scriptsize] at (2.6,-0.5) {bồn};\n")
dich_tikz = tru(1.0, 1.9, r_lab="$12$ cm", h_lab="$25$ cm")

lt2 = {
    "kind": "practice2", "number": 4, "title": "Luyện tập 2",
    "teacher_note": "Ví dụ 2 GV giảng theo đúng bốn bước của khuôn đếm số lần. Bài 6 HS tự làm theo bốn bước của Ví dụ 2. Bài 7 cho HS làm vào vở như đi thi rồi chấm chéo theo thang 0,5 + 0,5; trừ 0,25 nếu thiếu đơn vị hoặc thiếu câu kết luận, và trừ hết ý b nếu làm tròn xuống 16.",
    "blocks": [
        {"type": "para", "variant": "heading", "text": "Bậc 1. Khuôn đếm số lần"},
        {"type": "noted", "variant": "example", "figure": fig(vd2_tikz, "0.36"),
         "text": "\\textbf{Ví dụ 2.} \\textbf{(CK2 Phòng GD\\&ĐT Hoài Đức.)} Một thùng đựng nước có dạng hình trụ với chiều cao là $40$ cm và bán kính đáy là $15$ cm. Bạn Minh Trí dùng thùng trên để múc nước đổ vào một bồn chứa dạng hình trụ có chiều cao $150$ cm và bán kính đáy $60$ cm (Hình ?). Lúc đầu bồn không có nước, mỗi lần múc thùng đều đầy nước và đều được đổ hết vào bồn. Tính thể tích của thùng và số thùng nước Minh Trí cần múc để đổ đầy bồn (lấy $\\pi \\approx 3{,}14$).[[br]]" + LG +
                 "Thể tích của thùng là $V_{\\text{thùng}} = [[fill:\\pi r^2h]] \\approx 3{,}14\\cdot 15^2\\cdot 40 = [[fill:28\\,260]]$ (cm$^3$).[[br]]"
                 "Thể tích của bồn chứa là $V_{\\text{bồn}} \\approx 3{,}14\\cdot 60^2\\cdot 150 = [[fill:1\\,695\\,600]]$ (cm$^3$).[[br]]"
                 "Hai thể tích đã cùng đơn vị cm$^3$, nên số thùng nước cần múc là $1\\,695\\,600 : 28\\,260 = [[fill:60]]$ (thùng).[[br]]"
                 "Vậy thể tích của thùng là $[[fill:28\\,260]]$ cm$^3$ và Minh Trí cần múc $[[fill:60]]$ thùng nước.[[br]](Phép chia hết nên lấy đúng thương; nếu ra số thập phân thì phải làm tròn [[fill:LÊN]].)"},
        LANG,
        {"type": "para", "variant": "heading", "text": "Bậc 2. Trọn Câu IV.1 đề thi"},
        {"type": "problem", "tier": "onclass", "level": 3, "dang_id": "VD1", "label": "Bài 7.",
         "figure_given": True, "figure": fig(dich_tikz),
         "statement": "[VD] \\textbf{(Câu IV.1 đề chính thức Vào 10 năm 2026.)} Một xô đựng nước dạng hình trụ có chiều cao bằng $25$ cm và bán kính đáy bằng $12$ cm (Hình ?). Lấy $\\pi \\approx 3{,}14$ và coi độ dày của xô đựng nước không đáng kể.[[br]]a) Tính diện tích xung quanh của xô đựng nước đó.[[br]]b) Người ta dùng xô đựng nước trên để múc nước đổ vào một bể có thể tích $150$ lít. Mỗi lần người ta chỉ múc lượng nước bằng $80\\%$ thể tích của xô. Lúc đầu bể không có nước, hỏi cần múc ít nhất bao nhiêu xô để đổ đầy bể? (Biết $1$ lít $= 1000$ cm$^3$.)",
         "hints": ["Ý a: đề cho bán kính hay đường kính? Diện tích xung quanh dùng công thức nào trong sáu công thức?",
                   "Ý b: mỗi lần đổ vào bể được bao nhiêu lít? Thể tích bể và thể tích một lần đã cùng đơn vị chưa?",
                   "Ra số thập phân thì múc bấy nhiêu lần bể đã đầy chưa?"],
         "quy_trinh": ["Bước 1 (Ý a): Đề cho bán kính $r = 12$ cm; thay vào $S_{xq} = 2\\pi rh$, ghi đơn vị cm$^2$ và câu kết luận.",
                       "Bước 2 (Ý b): Tính thể tích xô $V = \\pi r^2h$, rồi lấy $80\\%$ để được thể tích một lần đổ.",
                       "Bước 3: Đổi thể tích một lần đổ ra lít ($1$ lít $= 1000$ cm$^3$) cho cùng đơn vị với bể $150$ lít.",
                       "Bước 4: Lấy $150$ chia cho thể tích một lần, làm tròn LÊN và kết luận."],
         "solution": "a) Diện tích xung quanh của xô đựng nước là[[br]]$S_{xq} = 2\\pi rh \\approx 2\\cdot 3{,}14\\cdot 12\\cdot 25 = 1884$ (cm$^2$).[[br]]Vậy diện tích xung quanh của xô là $1884$ cm$^2$.[[br]]b) Thể tích của xô là[[br]]$V = \\pi r^2h \\approx 3{,}14\\cdot 12^2\\cdot 25 = 11\\,304$ (cm$^3$).[[br]]Mỗi lần múc được lượng nước là[[br]]$11\\,304\\cdot 80\\% = 9043{,}2$ (cm$^3$) $= 9{,}0432$ (lít).[[br]]Ta có $150 : 9{,}0432 \\approx 16{,}59$.[[br]]Vì múc $16$ xô thì bể chưa đầy nên phải làm tròn lên.[[br]]Vậy cần múc ít nhất $17$ xô để đổ đầy bể."},
    ],
}

# ── TỔNG KẾT + BTVN ─────────────────────────────────────────────────────────
mindmap = {"type": "mindmap", "size": "small", "root": "Câu IV.1",
           "caption": "Điền các ô trống rồi ghi nhớ",
           "branches": [
               {"label": "Ý a: thay số", "children": [
                   {"label": "$r = d :$ [[blank:0.8cm]]", "children": []},
                   {"label": "Trụ: $S_{xq} =$ [[blank:1.3cm]]", "children": []},
                   {"label": "Trụ: $V =$ [[blank:1.3cm]]", "children": []}]},
               {"label": "Phần nước", "children": [
                   {"label": "chiều cao $=$ [[blank:1.6cm]]", "children": []},
                   {"label": "$1$ lít $=$ [[blank:1.2cm]] cm$^3$", "children": []}]},
               {"label": "Đếm số lần", "children": [
                   {"label": "chia rồi làm tròn [[blank:1.0cm]]", "children": []}]},
           ]}

bt = []
bt.append({"type": "problem", "tier": "btvn", "level": 1, "dang_id": "NB1", "label": "BTVN 1.",
           "figure_given": False,
           "statement": "[NB] Cho tam giác $ABC$ vuông tại $A$ có $AB = 4$ cm, $BC = 5$ cm. Khi quay tam giác $ABC$ một vòng quanh cạnh $AC$ ta được một hình nón có chiều cao bằng",
           "options": ["$4$ cm", "$3$ cm", "$5$ cm", "$9$ cm"], "answer": "B",
           "solution": "Quay quanh cạnh $AC$ thì chiều cao của hình nón là $AC$.[[br]]Xét $\\triangle ABC$ vuông tại $A$, theo định lí Pythagore: $AC^2 = BC^2 - AB^2 = 5^2 - 4^2 = 9$, nên $AC = 3$ cm.[[br]]Vậy chọn B."})
bt.append({"type": "problem", "tier": "btvn", "level": 1, "dang_id": "NB1", "label": "BTVN 2.",
           "figure_given": False,
           "statement": "[NB] Một mặt phẳng đi qua tâm hình cầu, cắt hình cầu theo một hình tròn có diện tích $9\\pi$ cm$^2$. Thể tích của hình cầu bằng",
           "options": ["$972\\pi$ cm$^3$", "$36\\pi$ cm$^3$", "$6\\pi$ cm$^3$", "$81\\pi$ cm$^3$"], "answer": "B",
           "solution": "Mặt cắt qua tâm là hình tròn có bán kính bằng bán kính $R$ của hình cầu: $\\pi R^2 = 9\\pi$ nên $R = 3$ cm.[[br]]Thể tích hình cầu là $V = \\dfrac{4}{3}\\pi R^3 = \\dfrac{4}{3}\\pi\\cdot 3^3 = 36\\pi$ (cm$^3$).[[br]]Vậy chọn B."})
bt.append({"type": "problem", "tier": "btvn", "level": 1, "dang_id": "NB2", "label": "BTVN 3.",
           "figure_given": True, "figure": fig(tru(0.85, 1.9, r_lab="$11$ cm", h_lab="$30$ cm")),
           "statement": "[NB] Một thùng rác có dạng hình trụ với bán kính đáy bằng $11$ cm, chiều cao bằng $30$ cm (Hình ?). Điền vào chỗ trống để hoàn thành bài giải tính thể tích của thùng rác (kết quả làm tròn đến hàng đơn vị, lấy $\\pi \\approx 3{,}14$):[[br]]Thể tích của thùng rác là[[br]]$V = [[blank:1.6cm]] \\approx 3{,}14\\cdot [[blank:1.6cm]]^2\\cdot [[blank:1.6cm]] = [[blank:1.6cm]] \\approx [[blank:1.6cm]]$ ([[blank:1.6cm]]).[[br]]Vậy thể tích của thùng rác khoảng [[blank:2.2cm]] cm$^3$.",
           "solution": "Thể tích của thùng rác là[[br]]$V = \\pi r^2h \\approx 3{,}14\\cdot 11^2\\cdot 30 = 11\\,398{,}2 \\approx 11\\,398$ (cm$^3$).[[br]]Vậy thể tích của thùng rác khoảng $11\\,398$ cm$^3$."})
bt.append({"type": "problem", "tier": "btvn", "level": 1, "dang_id": "NB3", "label": "BTVN 4.",
           "figure_given": False, "draw": True, "draw_height": 4.0,
           "statement": "[NB] Một bồn nước inox có dạng một hình trụ với chiều cao $1{,}75$ m và bán kính đáy là $0{,}5$ m. Trong bồn đang chứa đầy nước, người ta tháo nước ra cho đến khi mực nước trong bồn còn cao $1$ m. Lấy $\\pi \\approx 3{,}14$, bỏ qua bề dày của bồn.[[br]]Vẽ phác bồn nước vào khung dưới đây, ghi bán kính đáy, chiều cao bồn, mực nước còn lại và tô phần nước đã tháo ra; rồi điền vào chỗ trống.[[br]]a) Thể tích của bồn là $V = \\pi r^2h \\approx 3{,}14\\cdot 0{,}5^2\\cdot 1{,}75 = [[blank:1.6cm]] \\approx [[blank:1.6cm]]$ (m$^3$) (làm tròn đến hàng phần trăm).[[br]]b) Mực nước đã hạ $1{,}75 - 1 = [[blank:1.6cm]]$ (m). Thể tích nước đã tháo ra là $\\approx 3{,}14\\cdot 0{,}5^2\\cdot [[blank:1.6cm]] = [[blank:1.6cm]]$ (m$^3$) $= [[blank:1.6cm]]$ lít.[[br]]Vậy số nước đã tháo ra khoảng [[blank:1.6cm]] lít.",
           "solution": "Hình vẽ: hình trụ, ghi $r = 0{,}5$ m, $h = 1{,}75$ m, vạch mực nước còn lại cao $1$ m; phần đã tháo là hình trụ phía trên vạch đó, cao $0{,}75$ m.[[br]]a) $V = \\pi r^2h \\approx 3{,}14\\cdot 0{,}5^2\\cdot 1{,}75 = 1{,}37375 \\approx 1{,}37$ (m$^3$).[[br]]b) Mực nước đã hạ $1{,}75 - 1 = 0{,}75$ (m).[[br]]Thể tích nước đã tháo ra là $\\approx 3{,}14\\cdot 0{,}5^2\\cdot 0{,}75 = 0{,}58875$ (m$^3$) $= 588{,}75$ lít.[[br]]Vậy số nước đã tháo ra khoảng $588{,}75$ lít."})


bt.append({"type": "problem", "tier": "btvn", "level": 2, "dang_id": "TH1", "label": "BTVN 5.",
           "figure_given": True, "figure": fig(tru(0.95, 1.9, r_lab="$6$ dm", h_lab="$12$ dm")),
           "statement": "[TH] \\textbf{(CK2 THCS Cầu Diễn.)} Một thùng nước có dạng hình trụ với chiều cao là $12$ dm và bán kính đáy bằng $6$ dm (Hình ?). Coi chiều dày của thùng không đáng kể, lấy $\\pi \\approx 3{,}14$ và $1$ dm$^3 = 1$ lít.[[br]]a) Tính diện tích xung quanh của thùng nước.[[br]]b) Hỏi thùng nước đó chứa hết $1500$ lít nước không? (Làm tròn kết quả ở câu b đến hàng đơn vị của lít.)",
           "hints": ["Ý a: đề cho bán kính hay đường kính?",
                     "Ý b: thùng chứa được nhiều nhất bao nhiêu lít? So số đó với $1500$ lít."],
           "solution": "a) Diện tích xung quanh của thùng nước là[[br]]$S_{xq} = 2\\pi rh \\approx 2\\cdot 3{,}14\\cdot 6\\cdot 12 = 452{,}16$ (dm$^2$).[[br]]Vậy diện tích xung quanh của thùng nước là $452{,}16$ dm$^2$.[[br]]b) Thể tích của thùng nước là[[br]]$V = \\pi r^2h \\approx 3{,}14\\cdot 6^2\\cdot 12 = 1356{,}48$ (dm$^3$).[[br]]Đổi $1356{,}48$ dm$^3 \\approx 1356$ lít.[[br]]Vì $1356 < 1500$ nên thùng không chứa hết $1500$ lít nước.[[br]]Vậy thùng nước đó không chứa hết $1500$ lít nước."})

be_tikz = ("  \\draw[ink] (0,1.9) ellipse (1.1 and 0.33);\n  \\draw[ink] (0,1.9) ellipse (0.95 and 0.285);\n"
           "  \\draw[ink] (-1.1,0) arc (180:360:1.1 and 0.33);\n  \\draw[ink, dashed] (-1.1,0) arc (180:0:1.1 and 0.33);\n"
           "  \\draw[ink] (-1.1,0) -- (-1.1,1.9);\n  \\draw[ink] (1.1,0) -- (1.1,1.9);\n"
           "  \\draw[ink, dashed] (-0.95,0.15) arc (180:360:0.95 and 0.285);\n"
           "  \\draw[ink, dashed] (-0.95,0.15) -- (-0.95,1.9);\n  \\draw[ink, dashed] (0.95,0.15) -- (0.95,1.9);\n"
           "  \\fill[ink] (0,1.9) circle (1.2pt);\n  \\draw[ink, ->] (0,1.9) -- (-0.95,1.9);\n"
           "  \\node[below, font=\\scriptsize] at (-0.48,1.88) {$1$ m};\n"
           "  \\draw[ink, <->] (1.4,0.15) -- (1.4,1.9);\n  \\node[right, font=\\scriptsize] at (1.45,1.0) {$1{,}55$ m};\n"
           "  \\node[right, font=\\scriptsize] at (1.12,2.25) {thành dày $10$ cm};\n"
           "  \\node[right, font=\\scriptsize] at (1.12,-0.25) {đáy dày $5$ cm};\n")
bt.append({"type": "problem", "tier": "btvn", "level": 2, "dang_id": "TH2", "label": "BTVN 6.",
           "figure_given": True, "figure": fig(be_tikz, "0.36"),
           "statement": "[TH] \\textbf{(CK2 Phòng GD\\&ĐT Ba Đình.)} Chú Hùng muốn làm một bể nước bằng bê tông dạng hình trụ có chiều sâu lòng bể là $1{,}55$ m, bán kính lòng bể là $1$ m, bề dày của thành bể là $10$ cm và bề dày của đáy bể là $5$ cm (Hình ?, lấy $\\pi \\approx 3{,}14$).[[br]]a) Bể có thể chứa được nhiều nhất bao nhiêu lít nước?[[br]]b) Nếu chú Hùng có $1{,}3$ triệu đồng thì có đủ tiền mua bê tông tươi để làm bể nước trên không? Biết giá $1$ m$^3$ bê tông tươi là $1\\,000\\,000$ đồng.",
           "hints": ["Ý a: nước chứa trong phần nào của bể — lòng bể hay cả khối bể?",
                     "Ý b: khối trụ bên ngoài có bán kính và chiều cao bằng bao nhiêu khi cộng thêm bề dày thành và đáy? Bê tông là phần nào còn lại?"],
           "solution": "a) Lòng bể là hình trụ bán kính đáy $1$ m, chiều cao $1{,}55$ m nên thể tích lòng bể là[[br]]$V_1 = \\pi r^2h \\approx 3{,}14\\cdot 1^2\\cdot 1{,}55 = 4{,}867$ (m$^3$).[[br]]Đổi $4{,}867$ m$^3 = 4867$ lít.[[br]]Vậy bể chứa được nhiều nhất $4867$ lít nước.[[br]]b) Đổi $10$ cm $= 0{,}1$ m.[[br]]Đổi $5$ cm $= 0{,}05$ m.[[br]]Khối trụ bên ngoài có bán kính đáy $1 + 0{,}1 = 1{,}1$ (m) và chiều cao $1{,}55 + 0{,}05 = 1{,}6$ (m), nên thể tích là[[br]]$V_2 \\approx 3{,}14\\cdot 1{,}1^2\\cdot 1{,}6 = 6{,}07904$ (m$^3$).[[br]]Phần bê tông là khối trụ bên ngoài bỏ đi lòng bể, nên thể tích bê tông cần dùng là[[br]]$V_2 - V_1 \\approx 6{,}07904 - 4{,}867 = 1{,}21204$ (m$^3$).[[br]]Số tiền mua bê tông là[[br]]$1{,}21204\\cdot 1\\,000\\,000 = 1\\,212\\,040$ (đồng).[[br]]Vì $1\\,212\\,040 < 1\\,300\\,000$ nên số tiền chú Hùng có là đủ.[[br]]Vậy chú Hùng đủ tiền mua bê tông tươi để làm bể."})

kho_tikz = (tru(1.0, 1.5, d_lab="$10$ m", h_lab="$12$ m").replace(
    "  \\draw[ink] (0,1.5) ellipse (1.0 and 0.32);\n",
    "  \\draw[ink] (-1.0,1.5) arc (180:360:1.0 and 0.32);\n  \\draw[ink, dashed] (-1.0,1.5) arc (180:0:1.0 and 0.32);\n") +
    "  \\draw[ink] (-1.0,1.5) arc (180:0:1.0);\n")
# đường kính ghi ở đáy dưới cho khỏi đè mái vòm
kho_tikz = kho_tikz.replace(
    "  \\draw[ink, <->] (-1.0,1.5) -- (1.0,1.5);\n  \\node[anchor=center, font=\\scriptsize, fill=white, inner sep=1pt] at (0,1.5) {$10$ m};\n",
    "  \\draw[ink, <->] (-1.0,-0.55) -- (1.0,-0.55);\n  \\node[below, font=\\scriptsize] at (0,-0.6) {$10$ m};\n")
bt.append({"type": "problem", "tier": "btvn", "level": 2, "dang_id": "TH3", "label": "BTVN 7.",
           "figure_given": True, "figure": fig(kho_tikz),
           "statement": "[TH] Một kho chứa ngũ cốc có dạng một hình trụ và một mái vòm có dạng nửa hình cầu. Phần hình trụ có đường kính đáy là $10$ m và chiều cao là $12$ m. Phần mái vòm là nửa hình cầu đường kính $10$ m (Hình ?). Hỏi dung tích của kho đó là bao nhiêu mét khối (bỏ qua bề dày của tường nhà kho, lấy $\\pi \\approx 3{,}14$ và làm tròn kết quả đến hàng phần trăm)?",
           "hints": ["Kho gồm mấy khối? Mỗi khối dùng công thức thể tích nào?",
                     "Mái vòm là NỬA hình cầu: lấy thể tích hình cầu rồi làm gì?"],
           "solution": "Bán kính đáy của phần hình trụ và bán kính của mái vòm là $R = 10 : 2 = 5$ (m).[[br]]Theo công thức thể tích hình trụ, thể tích phần hình trụ là[[br]]$V_1 = \\pi R^2h \\approx 3{,}14\\cdot 5^2\\cdot 12 = 942$ (m$^3$).[[br]]Mái vòm là nửa hình cầu nên thể tích bằng một nửa thể tích hình cầu:[[br]]$V_2 = \\dfrac{1}{2}\\cdot \\dfrac{4}{3}\\pi R^3 \\approx \\dfrac{2}{3}\\cdot 3{,}14\\cdot 5^3 = \\dfrac{785}{3}$ (m$^3$).[[br]]Dung tích của kho bằng tổng thể tích hai phần:[[br]]$V = V_1 + V_2 \\approx 942 + \\dfrac{785}{3} \\approx 1203{,}67$ (m$^3$).[[br]]Vậy dung tích của kho khoảng $1203{,}67$ m$^3$."})
bt.append({"type": "problem", "tier": "btvn", "level": 3, "dang_id": "VD1", "label": "BTVN 8.",
           "figure_given": True, "figure": fig(tru(0.8, 2.0, r_lab="$0{,}5$ m", h_lab="$1{,}8$ m")),
           "statement": "[VD] \\textbf{(CK2 THCS Thị trấn Văn Điển.)} Một bể nước hình trụ có chiều cao $1{,}8$ m và bán kính đáy $0{,}5$ m (Hình ?).[[br]]a) Tính thể tích của bể nước (bỏ qua bề dày của thành bể).[[br]]b) Ban đầu bể cạn nước. Một vòi nước được đặt phía trên miệng bể và chảy được $2$ m$^3$ nước mỗi giờ. Hỏi vòi nước chảy sau bao lâu thì đầy bể? (Không cho nước chảy ra trước khi vòi chảy đầy bể; lấy $\\pi \\approx 3{,}14$ và làm tròn kết quả đến hàng phần mười.)",
           "solution": "a) Xét bể nước có dạng hình trụ bán kính đáy $0{,}5$ m, chiều cao $1{,}8$ m.[[br]]Theo công thức thể tích hình trụ, thể tích của bể nước là[[br]]$V = \\pi r^2h \\approx 3{,}14\\cdot 0{,}5^2\\cdot 1{,}8 = 1{,}413$ (m$^3$).[[br]]Vậy thể tích của bể nước là $1{,}413$ m$^3$.[[br]]b) Mỗi giờ vòi chảy được $2$ m$^3$, cùng đơn vị với thể tích bể.[[br]]Thời gian vòi chảy đầy bể là[[br]]$1{,}413 : 2 = 0{,}7065 \\approx 0{,}7$ (giờ).[[br]]Vậy sau khoảng $0{,}7$ giờ (khoảng $42$ phút) thì vòi chảy đầy bể."})

tong_ket = {"kind": "reflection", "number": 5, "title": "Sơ đồ tư duy",
            "teacher_note": "BTVN cố ý dôi; nếu cắt thì giữ BTVN 3, 4, 5, 8. BTVN 6, 7 là hai khuôn đề trường (hiệu hai khối, ghép khối) không dạy trên lớp — GV chữa ở đầu buổi luyện đề.",
            "blocks": [mindmap] + bt}

lesson = {
    "slug": "phieu-c-luyen-tap-chung-va-bai-tap-cuoi-chuong-x",
    "title": "Buổi 2 — Luyện tập chung chương X",
    "eyebrow": "PHIẾU C • HÌNH HỌC 9 · CHƯƠNG X — LUYỆN TẬP CHUNG",
    "grade_label": "Lớp 9 • Hình học",
    "class_tier": "C",
    "so_ca": 1,
    "kiem_tra_phut": 45,
    "btvn_phieu_rieng": True,
    "stages": [kham_pha, kien_thuc, lt1, lt2, tong_ket],
}

# ── đánh số Hình theo thứ tự xuất hiện ───────────────────────────────────────
n = 0
for st in lesson["stages"]:
    for b in st["blocks"]:
        f = b.get("figure")
        if f:
            n += 1
            f["caption"] = f"Hình {n}"
            for k in ("statement", "text"):
                if k in b:
                    b[k] = b[k].replace("Hình ?", f"Hình {n}")
for st in lesson["stages"]:
    for b in st["blocks"]:
        for k in ("statement", "text"):
            assert "Hình ?" not in b.get(k, ""), b.get("label")

OUT.write_text(json.dumps(lesson, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ghi", OUT, "—", n, "hình")
