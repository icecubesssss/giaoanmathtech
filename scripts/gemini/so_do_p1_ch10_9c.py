#!/usr/bin/env python3
"""Sơ đồ Phiếu 1 ch.X 9C (19/11/2026) — "Bài 31--32. Hình trụ, hình nón, hình cầu" (t32, 90′).

Mã câu = chon-cau.json (Thầy duyệt tab 9104 ngày 19/11: 31 "Hay"). TM phiếu 1: trên lớp 9 NB + 2 TH + 1 VD
(58,5′), ví dụ 25,5′, BTVN 7 NB + 3 TH (41,5′). Đích = Bài 9 = Bài 5 HK2 THCS Đoàn Thị Điểm 2025--2026 (ly 5 bi).
dang_id ↔ dòng TM (đánh số theo band, stt 1–11): NB1 Pythagore lớp 8 · NB2 C10-01 · NB3 C10-02 · NB4 C10-04 ·
NB5 tách TH C10-05 · NB6 tách TH C10-03 · NB7 tách C10-07 · TH1 C10-05 · TH2 C10-03 · TH3 C10-07 · VD1 C10-07.

Claude CHỐT ĐỀ (nguyên văn đề gốc, tách ý theo luật 16/11 + 17/11), thẻ, hình (TikZ máy vẽ), đáp số (kiem()).
Gemini viết lời giải, ví dụ điền khuyết, mở đầu, lý thuyết.

    .venv/bin/python scripts/gemini/so_do_p1_ch10_9c.py      # kiểm đáp số + đếm thẻ theo dang_id
"""
from __future__ import annotations

import collections
import math
import re
import sys

BR = "[[br]]"
PI = 3.14


# ── HÌNH KHỐI (TikZ) ──────────────────────────────────────────────────────────
def _n(x: float) -> str:
    return f"{x:.3f}".rstrip("0").rstrip(".")


def _dau(*dong: str) -> str:
    return "\\begin{tikzpicture}[line width=0.8pt, font=\\small]\n  " + "\n  ".join(dong) + "\n\\end{tikzpicture}"


def _than_tru(rx, ry, H, x0=0.0):
    return [
        rf"\draw[ink] ({_n(x0)},{_n(H)}) ellipse ({_n(rx)} and {_n(ry)});",
        rf"\draw[ink] ({_n(x0 - rx)},0) arc (180:360:{_n(rx)} and {_n(ry)});",
        rf"\draw[ink, dashed] ({_n(x0 - rx)},0) arc (180:0:{_n(rx)} and {_n(ry)});",
        rf"\draw[ink] ({_n(x0 - rx)},0) -- ({_n(x0 - rx)},{_n(H)});",
        rf"\draw[ink] ({_n(x0 + rx)},0) -- ({_n(x0 + rx)},{_n(H)});",
    ]


def _nuoc(rx, ry, w, x0=0.0):
    return [rf"\fill[info!25] ({_n(x0 - rx)},{_n(w)}) -- ({_n(x0 - rx)},0) arc (180:360:{_n(rx)} and {_n(ry)}) -- "
            rf"({_n(x0 + rx)},{_n(w)}) arc (0:180:{_n(rx)} and {_n(ry)}) -- cycle;"]


def _do_doc(x, y0, y1, chu, ben="right"):
    return [rf"\draw[ink, <->, line width=0.6pt] ({_n(x)},{_n(y0)}) -- ({_n(x)},{_n(y1)});",
            rf"\node[{ben}, font=\scriptsize] at ({_n(x + (0.04 if ben == 'right' else -0.04))},{_n((y0 + y1) / 2)}) "
            rf"{{{chu}}};"]


def tru(r="", d="", h="", nuoc=None, nuoc_chu="", bi=0, da=False, truc=False, H=2.0, rx=1.0, x0=0.0):
    """Hình trụ đứng: r = nhãn bán kính (đoạn từ tâm đáy trên), d = nhãn đường kính, h = nhãn chiều cao (đo bên phải),
    nuoc = tỉ lệ mực nước (0..1), nuoc_chu = nhãn mực nước (đo bên trái), bi = số viên bi ở đáy, da = hòn đá."""
    ry = 0.32 * rx
    out = []
    if nuoc:
        out += _nuoc(rx, ry, nuoc * H, x0)
    out += _than_tru(rx, ry, H, x0)
    if nuoc and nuoc < 1:
        out.append(rf"\draw[ink, line width=0.6pt] ({_n(x0)},{_n(nuoc * H)}) ellipse ({_n(rx)} and {_n(ry)});")
    if truc:
        out.append(rf"\draw[ink, dashed] ({_n(x0)},0) -- ({_n(x0)},{_n(H)});")
    if r:
        out += [rf"\fill[ink] ({_n(x0)},{_n(H)}) circle (1.2pt);",
                rf"\draw[ink] ({_n(x0)},{_n(H)}) -- ({_n(x0 + rx)},{_n(H)});",
                rf"\node[above, fill=white, inner sep=0.6pt, font=\scriptsize] at ({_n(x0 + rx / 2)},{_n(H + 0.04)}) "
                rf"{{{r}}};"]
    if d:
        out += [rf"\draw[ink, <->, line width=0.6pt] ({_n(x0 - rx)},{_n(H)}) -- ({_n(x0 + rx)},{_n(H)});",
                rf"\node[above, font=\scriptsize] at ({_n(x0)},{_n(H + ry)}) {{{d}}};"]
    if h:
        out += _do_doc(x0 + rx + 0.28, 0, H, h)
    if nuoc_chu:
        out += _do_doc(x0 - rx - 0.28, 0, nuoc * H, nuoc_chu, ben="left")
    if bi:
        b = 0.15 * rx
        xs = [x0 - 0.6 * rx + i * (1.2 * rx / max(bi - 1, 1)) for i in range(bi)] if bi > 1 else [x0]
        out += [rf"\draw[ink, fill=gold!45] ({_n(x)},{_n(b + 0.12)}) circle ({_n(b)});" for x in xs]
    if da:
        out.append(rf"\draw[ink, fill=muted!45] ({_n(x0 - 0.35)},0.02) -- ({_n(x0 - 0.42)},0.22) -- ({_n(x0 - 0.15)},0.42) "
                   rf"-- ({_n(x0 + 0.2)},0.38) -- ({_n(x0 + 0.38)},0.16) -- ({_n(x0 + 0.25)},0.02) -- cycle;")
    return out


def non(r="", h="", l="", dinh="", tam="", A="", H=2.0, rx=1.05, vuong=True, nguoc=False):
    """Hình nón đỉnh trên: r = nhãn bán kính (đoạn tâm → A bên phải), h = nhãn chiều cao, l = nhãn đường sinh (SA)."""
    ry = 0.32 * rx
    out = [rf"\draw[ink] (-{_n(rx)},0) arc (180:360:{_n(rx)} and {_n(ry)});",
           rf"\draw[ink, dashed] (-{_n(rx)},0) arc (180:0:{_n(rx)} and {_n(ry)});",
           rf"\draw[ink] (-{_n(rx)},0) -- (0,{_n(H)}) -- ({_n(rx)},0);",
           rf"\draw[ink, dashed] (0,0) -- (0,{_n(H)});",
           r"\fill[ink] (0,0) circle (1.2pt);"]
    if vuong:
        out.append(r"\draw[ink, line width=0.5pt] (0.14,0) -- (0.14,0.14) -- (0,0.14);")
    if r or A:
        out.append(rf"\draw[ink, dashed] (0,0) -- ({_n(rx)},0);")
    if r:
        yd = -ry - 0.2
        out += [rf"\draw[ink, line width=0.4pt] (0,-0.05) -- (0,{_n(yd - 0.08)});",
                rf"\draw[ink, line width=0.4pt] ({_n(rx)},-0.05) -- ({_n(rx)},{_n(yd - 0.08)});",
                rf"\draw[ink, <->, line width=0.6pt] (0,{_n(yd)}) -- ({_n(rx)},{_n(yd)});",
                rf"\node[below, font=\scriptsize] at ({_n(rx / 2)},{_n(yd)}) {{{r}}};"]
    if h:
        out.append(rf"\node[left, font=\scriptsize] at (-0.02,{_n(H * 0.45)}) {{{h}}};")
    if l:
        out.append(rf"\node[right, font=\scriptsize] at ({_n(rx / 2 + 0.04)},{_n(H / 2 + 0.05)}) {{{l}}};")
    if dinh:
        out.append(rf"\node[above, font=\scriptsize] at (0,{_n(H)}) {{{dinh}}};")
    if tam:
        out.append(rf"\node[below left, font=\scriptsize] at (0.02,0) {{{tam}}};")
    if A:
        out.append(rf"\node[right, font=\scriptsize] at ({_n(rx)},0) {{{A}}};")
    return out


def non_vd1():
    """SGK H.10.10: nón đỉnh S, tâm O, MN đường kính, P trên đường tròn đáy."""
    rx, ry, H = 1.25, 0.4, 2.3
    px, py = rx * math.cos(math.radians(-62)), ry * math.sin(math.radians(-62))
    return _dau(*[rf"\draw[ink] (-{rx},0) arc (180:360:{rx} and {ry});",
                  rf"\draw[ink, dashed] (-{rx},0) arc (180:0:{rx} and {ry});",
                  rf"\draw[ink] (-{rx},0) -- (0,{H}) -- ({rx},0);",
                  rf"\draw[ink] (0,{H}) -- ({_n(px)},{_n(py)});",
                  rf"\draw[ink, dashed] (0,0) -- (0,{H});",
                  rf"\draw[ink, dashed] (-{rx},0) -- ({rx},0);",
                  rf"\draw[ink, dashed] (0,0) -- ({_n(px)},{_n(py)});",
                  r"\draw[ink, line width=0.5pt] (0.14,0) -- (0.14,0.14) -- (0,0.14);",
                  r"\fill[ink] (0,0) circle (1.2pt);",
                  rf"\node[above, font=\scriptsize] at (0,{H}) {{$S$}};",
                  r"\node[below left, font=\scriptsize] at (0.02,0) {$O$};",
                  rf"\node[left, font=\scriptsize] at (-{rx},0) {{$M$}};",
                  rf"\node[right, font=\scriptsize] at ({rx},0) {{$N$}};",
                  rf"\node[below, font=\scriptsize] at ({_n(px)},{_n(py)}) {{$P$}};"])


def kem(d="", h=""):
    """Kem ốc quế: hình nón đỉnh dưới, viên kem trên miệng."""
    rx, ry, H = 0.85, 0.27, 2.4
    return _dau(rf"\draw[ink, fill=gold!30] (-{rx},{H}) arc (180:0:{rx} and {_n(rx * 0.95)});",
                rf"\draw[ink, fill=white] (0,{H}) ellipse ({rx} and {ry});",
                rf"\draw[ink] (-{rx},{H}) -- (0,0) -- ({rx},{H});",
                rf"\draw[ink, dashed] (0,0) -- (0,{H});",
                rf"\draw[ink, line width=0.4pt] (-{rx},{_n(H + 0.05)}) -- (-{rx},{_n(H + rx + 0.3)});",
                rf"\draw[ink, line width=0.4pt] ({rx},{_n(H + 0.05)}) -- ({rx},{_n(H + rx + 0.3)});",
                rf"\draw[ink, <->, line width=0.6pt] (-{rx},{_n(H + rx + 0.2)}) -- ({rx},{_n(H + rx + 0.2)});",
                rf"\node[above, font=\scriptsize] at (0,{_n(H + rx + 0.2)}) {{{d}}};",
                *_do_doc(rx + 0.25, 0, H, h))


def cau(R_chu="", d_chu="", tam="$O$", diem=False, R=1.15):
    ry = 0.3 * R
    out = [rf"\draw[ink] (0,0) circle ({R});",
           rf"\draw[ink] (-{R},0) arc (180:360:{R} and {_n(ry)});",
           rf"\draw[ink, dashed] (-{R},0) arc (180:0:{R} and {_n(ry)});",
           r"\fill[ink] (0,0) circle (1.2pt);"]
    if tam:
        out.append(rf"\node[below left, font=\scriptsize] at (0,-0.02) {{{tam}}};")
    if R_chu:
        out += [rf"\draw[ink] (0,0) -- (40:{R});", rf"\node[above left, font=\scriptsize] at (40:{_n(R * 0.55)}) {{{R_chu}}};"]
    if d_chu:
        out += [rf"\draw[ink, <->, line width=0.6pt] (-{R},0) -- ({R},0);",
                rf"\node[above, font=\scriptsize] at (-{_n(R * 0.45)},0.02) {{{d_chu}}};"]
    if diem:   # SGK H.10.21: M, N đầu một đường kính, P trên mặt cầu
        out += [rf"\draw[ink] (150:{R}) -- (-30:{R});", rf"\draw[ink] (0,0) -- (65:{R});",
                *[rf"\fill[ink] ({a}:{R}) circle (1.2pt);" for a in (150, -30, 65)],
                rf"\node[above left, font=\scriptsize] at (150:{R}) {{$M$}};",
                rf"\node[below right, font=\scriptsize] at (-30:{R}) {{$N$}};",
                rf"\node[above right, font=\scriptsize] at (65:{R}) {{$P$}};"]
    return _dau(*out)


def hai_ly(H1, H2):
    """Đích: Hình H1 ly đang chứa nước cao 10, Hình H2 thả 5 bi nước dâng tới miệng."""
    a = tru(d="$5$ cm", h="$15$ cm", nuoc=10 / 15, nuoc_chu="$10$ cm", H=2.4, x0=0)
    b = tru(nuoc=1.0, bi=5, H=2.4, x0=4.2)
    return _dau(*a, *b, rf"\node[font=\scriptsize\itshape] at (0,-0.65) {{{H1}}};",
                rf"\node[font=\scriptsize\itshape] at (4.2,-0.65) {{{H2}}};")


def hinh(tikz_dong, mota, pos="right", width="0.30"):
    tikz = tikz_dong if isinstance(tikz_dong, str) else _dau(*tikz_dong)
    return {"tikz": tikz, "mota": mota, "pos": pos, "width": width}


# ── TIỆN ÍCH CHỮ ──────────────────────────────────────────────────────────────
def tn(*o):
    """Bốn phương án A–D chia cột đều: ngắn 4 cột, vừa 2 cột (khuôn ch.VIII)."""
    dai = max(len(re.sub(r"\\[a-zA-Z]+|[{}$\\]", "", x)) for x in o)
    if dai > 30:
        return "".join(rf"[[br]]\hspace*{{1.4em}}{c}. {x}" for c, x in zip("ABCD", o))
    w, moi = ("0.22", 4) if dai <= 9 else ("0.45", 2)
    o = [rf"\makebox[{w}\linewidth][l]{{{c}. {x}}}" for c, x in zip("ABCD", o)]
    return "".join("[[br]]\\hspace*{1.4em}" + "".join(o[i:i + moi]) for i in range(0, 4, moi))


def y(*ds):
    return BR.join(ds)


N = {
    "pd902": r"HK2 THCS Phúc Đồng (Long Biên), 2024--2025, mã đề 902",
    "pd901": r"HK2 THCS Phúc Đồng (Long Biên), 2024--2025, mã đề 901",
    "bvd": r"HK2 THCS Bế Văn Đàn (Đống Đa), 2025--2026",
    "tv25": r"HK2 THCS Trưng Vương, 2025--2026",
    "hn25": r"đề tuyển sinh lớp 10 Hà Nội, 2025--2026",
    "nthuy": r"HK2 THCS Ngọc Thụy (Long Biên), 2024--2025",
    "dtd": r"HK2 THCS Đoàn Thị Điểm (TP. Hồ Chí Minh), 2025--2026",
    "tm3": r"GK2 THCS Tây Mỗ 3, 2025--2026",
    "tv24": r"GK2 THCS Trưng Vương, 2024--2025",
    "xd": r"HK2 THCS Xuân Đỉnh, 2025--2026",
    "tt": r"HK2 THCS Thái Thịnh (Đống Đa), 2025--2026",
    "tcnc": r"tài liệu Mathtech \textquotedblleft Hình trụ. Hình nón. Hình cầu\textquotedblright",
}


def ng(k):
    return r" \textit{(" + N[k] + ")}"


def sgk(s):
    return r" \textit{(SGK Toán 9 tập hai, " + s + ")}"


PI_ = r"$\pi\approx 3{,}14$"

# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# Tiêu đề: dict(tieu_de=…, chang=…). Ví dụ / Bài: dict(nhan, chang, tier, dang, level, ma, ht, de, ghi, hinh, hints).
# Trong đề "{H0}", "{H1}" = số hình của khối (lap đánh số toàn phiếu). ht: vi_du | trac_nghiem | tra_loi_ngan | th_dan | vd.
KHOI = [
    # ───────────── LUYỆN TẬP 1 — Nhận biết (6 thẻ NB) ─────────────
    dict(tieu_de="Mạch 1. Các yếu tố của hình trụ, hình nón, hình cầu", chang="practice1"),
    dict(nhan="Ví dụ 1.", chang="practice1", ma="sgk-b31-vd3", ht="vi_du",
         de=r"Hãy kể tên đỉnh, đường cao, một bán kính đáy và một đường sinh của hình nón trong {H0}."
            + sgk("Bài 31, Ví dụ 3"),
         hinh=[hinh(non_vd1(), "hình nón đỉnh S, tâm đáy O, M và N là hai đầu một đường kính đáy, P nằm trên đường "
                               "tròn đáy; vẽ SO (nét đứt, vuông góc với đáy tại O), SM, SN, SP, OP")],
         ghi="ĐỌC ẢNH sgk9t2-tr97 (Ví dụ 3, Giải) theo đúng SGK: Đỉnh: S. Đường cao: SO. Một bán kính đáy: OM. Một đường "
             "sinh: SM. Mỗi yếu tố một dòng, ô ở tên yếu tố (4 ô). Dòng Vậy ngắn: đường sinh nối đỉnh với một điểm của "
             "đường tròn đáy (vd SN, SP cũng là đường sinh)."),
    dict(nhan="Bài 1.", chang="practice1", tier="onclass", dang="NB2", level=1, ma="sgk-10.17", ht="trac_nghiem",
         de=r"[NB] Khi quay hình chữ nhật $ABCD$ một vòng quanh cạnh $AB$ ta được một hình trụ có bán kính đáy bằng độ "
            r"dài đoạn thẳng" + sgk("Bài tập 10{.}17") + tn("$AB$.", "$CD$.", "$AD$.", "$AC$."),
         ghi="Chọn C: AB là trục (chiều cao), cạnh AD vuông góc với trục quét thành đáy nên r = AD. 1–2 dòng."),
    dict(nhan="Bài 2.", chang="practice1", tier="onclass", dang="NB1", level=1, ma="sgk-10.18", ht="trac_nghiem",
         de=r"[NB] Cho tam giác $ABC$ vuông tại $A$ có $AB=4$ cm, $BC=5$ cm. Khi quay tam giác $ABC$ một vòng quanh "
            r"cạnh $AC$ ta được một hình nón có chiều cao bằng" + sgk("Bài tập 10{.}18")
            + tn("$4$ cm.", "$3$ cm.", "$5$ cm.", "$9$ cm."),
         ghi="Chọn B: quay quanh AC nên chiều cao h = AC · tam giác ABC vuông tại A: AC² = BC² − AB² = 25 − 16 = 9, "
             "AC = 3 cm. 2 dòng."),
    dict(tieu_de="Mạch 2. Thay số vào một công thức", chang="practice1"),
    dict(nhan="Ví dụ 2.", chang="practice1", ma="sgk-b32-vd3", ht="vi_du",
         de=r"Tính diện tích mặt cầu và thể tích hình cầu có bán kính bằng $10$ cm." + sgk("Bài 32, Ví dụ 3"),
         ghi="ĐỌC ẢNH sgk9t2-tr103, tr104 theo đúng lời giải SGK: S = 4πR² = 4π·10² = 400π (cm²) · V = (4/3)πR³ = "
             "(4/3)π·10³ = 4000π/3 (cm³). Ô: công thức S (4πR²), 400π, công thức V, 4000π/3 (ít nhất 4 ô)."),
    dict(nhan="Bài 3.", chang="practice1", tier="onclass", dang="NB3", level=1, ma="ck2-phuc-dong-2024-902-IV1",
         ht="tra_loi_ngan",
         de=r"[NB] Một lon nước ngọt hình trụ có đường kính đáy là $6$ cm, độ dài trục là $11$ cm. Tính thể tích lon "
            r"nước ngọt (cho " + PI_ + ")." + ng("pd902"),
         ghi="r = 6 : 2 = 3 cm, h = 11 cm (độ dài trục = chiều cao) · V = πr²h ≈ 3,14·3²·11 = 310,86 (cm³). Vậy."),
    dict(nhan="Bài 4.", chang="practice1", tier="onclass", dang="NB3", level=1, ma="ck2-be-van-dan-2025-IV1",
         ht="tra_loi_ngan",
         de=r"[NB] {H0} mô tả một chiếc kem ốc quế có dạng hình nón với đường kính đáy khoảng $5{,}8$ cm và chiều cao "
            r"khoảng $12{,}5$ cm. Tính thể tích chiếc kem (lấy " + PI_ + r", làm tròn kết quả đến hàng đơn vị của "
            r"centimét khối)." + ng("bvd"),
         hinh=[hinh(kem(d="$5{,}8$ cm", h="$12{,}5$ cm"),
                    "chiếc kem ốc quế: hình nón đỉnh ở dưới, đường kính miệng 5,8 cm, chiều cao 12,5 cm")],
         ghi="r = 5,8 : 2 = 2,9 cm · V = (1/3)πr²h ≈ (1/3)·3,14·2,9²·12,5 ≈ 110,03 ≈ 110 (cm³). Vậy."),
    dict(nhan="Bài 5.", chang="practice1", tier="onclass", dang="NB3", level=1, ma="ck2-trung-vuong-2025-IV1 (ý a)",
         ht="tra_loi_ngan",
         de=r"Trong các trận thi đấu bóng đá chuyên nghiệp, người ta sử dụng loại bóng bằng da có dạng hình cầu với "
            r"đường kính $22$ cm." + ng("tv25")
            + BR + r"[NB] Hỏi diện tích da để làm một quả bóng đó là bao nhiêu cm$^2$? (Lấy " + PI_
            + r", bỏ qua tỉ lệ hao hụt của da.)",
         ghi="R = 22 : 2 = 11 cm · S = 4πR² ≈ 4·3,14·11² = 1519,76 (cm²). Vậy."),
    dict(nhan="Bài 6.", chang="practice1", tier="onclass", dang="NB4", level=1, ma="ck2-phuc-dong-2024-901-IV1",
         ht="tra_loi_ngan",
         de=r"[NB] Đường ống nối hai bể cá trong một thủy cung có dạng hình trụ, độ dài của đường ống là $30$ m. Dung "
            r"tích của đường ống nói trên là $1800$ m$^3$. Tính diện tích đáy của đường ống." + ng("pd901"),
         ghi="Độ dài đường ống là chiều cao h = 30 m · V = S_đáy·h nên S_đáy = V : h = 1800 : 30 = 60 (m²). Vậy."),
    # ───────────── LUYỆN TẬP 2 — Thông hiểu, vận dụng ─────────────
    dict(tieu_de="Mạch 3. Bài toán thực tế về một hình trụ", chang="practice2"),
    dict(nhan="Ví dụ 3.", chang="practice2", ma="sgk-b31-lt2", ht="vi_du",
         de=y(r"Một thùng nước có dạng hình trụ với chiều cao bằng $1{,}6$ m và bán kính đáy bằng $0{,}5$ m ({H0}).",
              r"a) Tính diện tích xung quanh của thùng nước.",
              r"b) Hỏi thùng chứa được bao nhiêu lít nước?",
              r"(Coi chiều dày của thùng không đáng kể và làm tròn kết quả ở câu b đến hàng đơn vị của lít.)"
              + sgk("Bài 31, Luyện tập 2")),
         hinh=[hinh(tru(r="$0{,}5$ m", h="$1{,}6$ m"), "thùng hình trụ bán kính đáy 0,5 m, chiều cao 1,6 m")],
         ghi="ĐỌC ẢNH sgk9t2-tr96 (Ví dụ 2) để theo nhịp SGK. a) S_xq = 2πrh = 2π·0,5·1,6 = 1,6π ≈ 5,03 (m²). "
             "b) V = πr²h = π·0,5²·1,6 = 0,4π (m³) ≈ 1,2566 m³. Đổi 1 m³ = 1000 lít nên V ≈ 1257 lít. Ô: 2πrh, 1,6π, "
             "πr²h, 0,4π, 1000, 1257 (6 ô)."),
    dict(nhan="Bài 7.", chang="practice2", tier="onclass", dang="NB5+TH1", level=2, ma="so-hn-2025-IV1", ht="th_dan",
         de=y(r"Gia đình bạn Khánh đang sử dụng một thùng đựng nước dạng hình trụ với bán kính đáy bằng $50$ cm và chiều "
              r"cao bằng $150$ cm ({H0}). Thùng đựng nước được đặt thẳng đứng trên mặt sàn. (Lấy " + PI_
              + r" và coi chiều dày của thùng không đáng kể.)" + ng("hn25"),
              r"a) [NB] Tính diện tích xung quanh của thùng đựng nước.",
              r"b) [TH] Sau một thời gian gia đình bạn Khánh sử dụng nước trong thùng thì mực nước còn lại đã thấp hơn "
              r"$40$ cm so với mực nước ban đầu. Tính thể tích nước trong thùng mà gia đình bạn Khánh đã sử dụng trong "
              r"khoảng thời gian đó."),
         hinh=[hinh(tru(r="$50$ cm", h="$150$ cm"), "thùng hình trụ bán kính đáy 50 cm, chiều cao 150 cm")],
         hints=["Phần nước đã sử dụng có dạng hình gì?", "Bán kính đáy và chiều cao của phần nước đó bằng bao nhiêu?"],
         ghi="a) S_xq = 2πrh ≈ 2·3,14·50·150 = 47100 (cm²). b) Phần nước đã dùng là hình trụ bán kính đáy 50 cm, chiều "
             "cao 40 cm · V = πr²h ≈ 3,14·50²·40 = 314000 (cm³) (= 314 lít, có thể ghi thêm). Vậy mỗi ý."),
    dict(tieu_de="Mạch 4. Hình nón biết bán kính đáy và đường sinh", chang="practice2"),
    dict(nhan="Ví dụ 4.", chang="practice2", ma="sgk-b31-vd4", ht="vi_du",
         de=y(r"Cho một hình nón có độ dài đường sinh bằng $10$ cm, bán kính đáy bằng $6$ cm ({H0}).",
              r"a) Tính diện tích xung quanh của hình nón.",
              r"b) Tính thể tích của hình nón." + sgk("Bài 31, Ví dụ 4")),
         hinh=[hinh(non(r="$6$ cm", l="$10$ cm", dinh="$S$", tam="$O$", A="$A$"),
                    "hình nón đỉnh S, tâm đáy O, A trên đường tròn đáy; OA = 6 cm, đường sinh SA = 10 cm; SO vuông góc "
                    "với OA")],
         ghi="ĐỌC ẢNH sgk9t2-tr99 (Ví dụ 4, Giải) theo đúng SGK. a) S_xq = πrl = π·6·10 = 60π (cm²). b) Tam giác SOA "
             "vuông tại O: SO² + OA² = SA² (định lí Pythagore) nên SO² = 10² − 6² = 64, SO = 8 cm · V = (1/3)πr²h = "
             "(1/3)π·6²·8 = 96π (cm³). Ô: πrl, 60π, 64, 8, 96π (ít nhất 5 ô)."),
    dict(nhan="Bài 8.", chang="practice2", tier="onclass", dang="NB6+TH2", level=2, ma="sgk-10.3", ht="th_dan",
         de=y(r"Khi cho tam giác $SOA$ vuông tại $O$ quay quanh cạnh $SO$ một vòng, ta được một hình nón. Biết "
              r"$OA=8$ cm, $SA=17$ cm ({H0})." + sgk("Bài tập 10{.}3"),
              r"a) [NB] Tính diện tích xung quanh của hình nón.",
              r"b) [TH] Tính thể tích của hình nón."),
         hinh=[hinh(non(r="$8$ cm", l="$17$ cm", dinh="$S$", tam="$O$", A="$A$"),
                    "hình nón đỉnh S, tâm đáy O, A trên đường tròn đáy; OA = 8 cm, SA = 17 cm; tam giác SOA vuông tại O")],
         hints=["Muốn tính thể tích hình nón cần biết thêm độ dài nào?",
                "Độ dài đó là một cạnh của tam giác vuông nào? Tính độ dài cạnh đó."],
         ghi="a) r = OA = 8, l = SA = 17 · S_xq = πrl = π·8·17 = 136π (cm²). b) Tam giác SOA vuông tại O: SO² = SA² − "
             "OA² = 289 − 64 = 225 nên SO = 15 cm · V = (1/3)πr²h = (1/3)π·8²·15 = 320π (cm³). Vậy mỗi ý."),
    dict(tieu_de="Mạch 5. Thả vật chìm vào nước", chang="practice2"),
    dict(nhan="Ví dụ 5.", chang="practice2", ma="ck2-ngoc-thuy-2024-IV1", ht="vi_du",
         de=y(r"Một cái cốc hình trụ có chiều cao là $15$ cm, bán kính đáy là $5$ cm, chiều cao mực nước trong cốc là "
              r"$10$ cm ({H0}). (Lấy " + PI_ + r", làm tròn kết quả đến hàng phần mười.)",
              r"a) Tính thể tích nước ở trong cốc.",
              r"b) Người ta thả một hòn đá vào trong cốc nước, nước trong cốc dâng lên đến miệng cốc và không bị tràn "
              r"ra ngoài. Tính thể tích của hòn đá." + ng("nthuy")),
         hinh=[hinh(tru(r="$5$ cm", h="$15$ cm", nuoc=10 / 15, nuoc_chu="$10$ cm"),
                    "cốc hình trụ bán kính đáy 5 cm, cao 15 cm, mực nước cao 10 cm")],
         ghi="a) Phần nước là hình trụ r = 5 cm, h = 10 cm · V_nước = πr²h ≈ 3,14·5²·10 = 785 (cm³). b) Hòn đá chìm "
             "hẳn nên thể tích hòn đá bằng thể tích phần nước dâng thêm · nước dâng thêm 15 − 10 = 5 cm · V_đá ≈ "
             "3,14·5²·5 = 392,5 (cm³). Ô: 785, 15 − 10, 5, 392,5 … (ít nhất 5 ô)."),
    dict(nhan="Bài 9.", chang="practice2", tier="onclass", dang="NB7+VD1", level=3, ma="ck2-doan-thi-diem-2025-5",
         ht="vd",
         de=y(r"Một ly nước dạng hình trụ có chiều cao là $15$ cm, đường kính đáy là $5$ cm. Bên trong ly có chứa một "
              r"lượng nước cao $10$ cm như {H0}." + ng("dtd"),
              r"a) [NB] Tính thể tích lượng nước chứa trong ly (giả sử độ dày của ly là không đáng kể).",
              r"b) [VD] Người ta thả vào ly nước $5$ viên bi hình cầu có cùng thể tích ngập hoàn toàn trong nước làm "
              r"nước trong ly dâng lên bằng miệng ly như {H1}. Tính bán kính của mỗi viên bi.",
              r"Các kết quả được làm tròn đến hàng phần trăm."),   # 19/11 Thầy: bỏ câu cho sẵn công thức trụ/cầu
         hinh=[hinh("HAI_LY", "Hình thứ nhất: ly hình trụ đường kính đáy 5 cm, cao 15 cm, nước cao 10 cm. Hình thứ hai: "
                              "cùng ly, có 5 viên bi ở đáy, nước dâng tới miệng ly", pos="below", width="0.42")],
         ghi="Đề KHÔNG cho π ≈ 3,14 ⇒ giữ π rồi mới làm tròn. a) r = 5 : 2 = 2,5 cm · V_nước = πr²h = π·2,5²·10 = "
             "62,5π ≈ 196,35 (cm³). b) Nước dâng thêm 15 − 10 = 5 cm · tổng thể tích 5 viên bi = π·2,5²·5 = 31,25π "
             "(cm³) · mỗi viên 31,25π : 5 = 6,25π (cm³) · (4/3)πR³ = 6,25π ⇒ R³ = 4,6875 ⇒ R ≈ 1,67 (cm). Lời giải "
             "đầy đủ theo nhịp bài thi (đây là bài học sinh tự làm, lời giải chỉ in ở sổ tay giáo viên)."),
    # ───────────── BÀI TẬP VỀ NHÀ (7 NB + 3 TH) ─────────────
    dict(nhan="Bài 10.", chang="reflection", tier="btvn", dang="NB2", level=1, ma="sgk-b32-vd1", ht="tra_loi_ngan",
         de=r"[NB] Hãy kể tên tâm và một bán kính của mặt cầu trong {H0}." + sgk("Bài 32, Ví dụ 1"),
         hinh=[hinh(cau(diem=True), "mặt cầu tâm O; M, N, P nằm trên mặt cầu, MN đi qua O; vẽ đoạn OP")],
         ghi="ĐỌC ẢNH sgk9t2-tr102: Tâm mặt cầu: O. Một bán kính: OM (hoặc ON, OP). 2 dòng."),
    dict(nhan="Bài 11.", chang="reflection", tier="btvn", dang="NB3", level=1, ma="gk2-tay-mo-3-2025-IV1",
         ht="tra_loi_ngan",
         de=r"[NB] Một thùng đựng nước hình trụ có đường kính đáy là $40$ cm và chiều cao là $60$ cm. Tính thể tích của "
            r"thùng đựng nước (lấy " + PI_ + ")." + ng("tm3"),
         ghi="r = 40 : 2 = 20 cm · V = πr²h ≈ 3,14·20²·60 = 75360 (cm³). Vậy."),
    dict(nhan="Bài 12.", chang="reflection", tier="btvn", dang="NB3", level=1, ma="sgk-10.19", ht="trac_nghiem",
         de=r"[NB] Diện tích mặt cầu có đường kính $10$ cm là" + sgk("Bài tập 10{.}19")
            + tn(r"$10\pi$ cm$^2$.", r"$400\pi$ cm$^2$.", r"$50\pi$ cm$^2$.", r"$100\pi$ cm$^2$."),
         ghi="Chọn D: R = 10 : 2 = 5 cm, S = 4πR² = 4π·5² = 100π (cm²). (400π là lỗi lấy R = 10.) 1–2 dòng."),
    dict(nhan="Bài 13.", chang="reflection", tier="btvn", dang="NB3", level=1, ma="gk2-trung-vuong-2024-IV1 (ý a)",
         ht="tra_loi_ngan",
         de=r"[NB] Kem ốc quế sử dụng loại vỏ có dạng hình nón với bán kính đáy $2{,}5$ cm và chiều cao $6$ cm. Tính "
            r"thể tích lượng kem mà một vỏ ốc quế có thể chứa được, coi độ dày vỏ là không đáng kể (lấy " + PI_ + ")."
            + ng("tv24"),
         ghi="V = (1/3)πr²h ≈ (1/3)·3,14·2,5²·6 = 39,25 (cm³). Vậy."),
    dict(nhan="Bài 14.", chang="reflection", tier="btvn", dang="NB5+TH1", level=2, ma="ck2-xuan-dinh-2025-IV1",
         ht="th_dan",
         de=y(r"Một bồn nước inox có dạng một hình trụ với chiều cao $1{,}75$ m và bán kính đáy là $0{,}5$ m. Lấy "
              + PI_ + r", làm tròn kết quả đến hàng phần trăm." + ng("xd"),
              r"a) [NB] Tính thể tích của bồn nước inox đó.",
              r"b) [TH] Trong bồn đang chứa đầy nước, người ta tháo nước ở trong bồn ra cho đến khi mực nước trong bồn "
              r"còn cao $1$ m. Hỏi số lít nước đã tháo ra ngoài là bao nhiêu? (Bỏ qua bề dày của bồn nước.)"),
         hints=["Phần nước đã tháo ra có dạng hình gì? Chiều cao của phần đó bằng bao nhiêu?",
                "$1$ m$^3$ bằng bao nhiêu lít?"],
         ghi="a) V = πr²h ≈ 3,14·0,5²·1,75 = 1,37375 ≈ 1,37 (m³). b) Phần nước tháo ra là hình trụ r = 0,5 m, chiều "
             "cao 1,75 − 1 = 0,75 m · V ≈ 3,14·0,5²·0,75 = 0,58875 (m³) = 588,75 lít. Vậy mỗi ý."),
    dict(nhan="Bài 15.", chang="reflection", tier="btvn", dang="NB6+TH2", level=2, ma="tl-tcnc-23-tr9", ht="th_dan",
         # 19/11 Thầy "đổi đi": thay sgk-10.23 (giống Ví dụ 4 SGK 77%, chỉ khác số); sgk-b31-lt4 nằm trong đề KT X cũ
         de=y(r"Cho tam giác $ABC$ vuông tại $A$, $AB=5$ cm, $BC=13$ cm. Quay tam giác vuông $ABC$ một vòng xung quanh "
              r"đường thẳng $AC$ ta được hình nón ({H0})." + ng("tcnc"),
              r"a) [NB] Tính chiều cao của hình nón.",
              r"b) [TH] Hỏi thể tích của hình nón đó bằng bao nhiêu centimét khối (làm tròn kết quả đến hàng phần "
              r"trăm)?"),
         hinh=[hinh(non(r="$5$ cm", l="$13$ cm", dinh="$C$", tam="$A$", A="$B$"),
                    "hình nón đỉnh C, tâm đáy A, B trên đường tròn đáy; AB = 5 cm, BC = 13 cm; tam giác ABC vuông tại A")],
         hints=["Khi quay quanh $AC$, cạnh nào quét thành đáy của hình nón?",
                "Bán kính đáy và chiều cao của hình nón bằng bao nhiêu?"],
         ghi="Quay quanh AC nên chiều cao h = AC, bán kính đáy r = AB = 5 cm. a) Tam giác ABC vuông tại A: AC² = BC² − "
             "AB² = 169 − 25 = 144 nên AC = 12 cm (theo định lí Pythagore, ghi rõ căn cứ). b) V = (1/3)πr²h = "
             "(1/3)π·5²·12 = 100π ≈ 314,16 (cm³). Đề KHÔNG cho π ≈ 3,14 ⇒ giữ π rồi mới làm tròn. Vậy mỗi ý."),
    dict(nhan="Bài 16.", chang="reflection", tier="btvn", dang="NB7+TH3", level=2, ma="ck2-thai-thinh-2025-IV1",
         ht="th_dan",
         de=y(r"Một cái cốc hình trụ có đường kính đáy bằng $10$ cm đựng nước với mực nước trong cốc cao $15$ cm."
              + ng("tt"),
              r"a) [NB] Tính thể tích lượng nước trong cốc (bỏ qua bề dày của thành cốc, lấy " + PI_ + ").",
              r"b) [TH] Nếu thả viên bi sắt dạng hình cầu có bán kính $2$ cm vào cốc thì lượng nước trong cốc dâng lên "
              r"bao nhiêu milimét, biết rằng viên bi chìm hẳn trong nước và nước không bị tràn ra ngoài (làm tròn đến "
              r"hàng đơn vị)."),
         hints=["Thể tích phần nước dâng lên bằng thể tích của vật nào?",
                "Phần nước dâng lên có dạng hình gì? Bán kính đáy của phần đó bằng bao nhiêu?"],
         ghi="a) r = 10 : 2 = 5 cm · V = πr²h ≈ 3,14·5²·15 = 1177,5 (cm³). b) V_bi = (4/3)πR³ ≈ (4/3)·3,14·2³ ≈ "
             "33,49 (cm³) · phần nước dâng lên là hình trụ r = 5 cm, chiều cao x: 3,14·5²·x = V_bi ⇒ x = 32/75 ≈ 0,43 cm "
             "≈ 4 mm (π triệt tiêu: x = (4/3)·8 : 25 = 32/75). Vậy."),
]

DAP_TN = {"Bài 1.": "C", "Bài 2.": "B", "Bài 12.": "D"}

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu 1 (19/11)
    "NB1": (1, 0), "NB2": (1, 1), "NB3": (3, 3), "NB4": (1, 0), "NB5": (1, 1), "NB6": (1, 1), "NB7": (1, 1),
    "TH1": (1, 1), "TH2": (1, 1), "TH3": (0, 1), "VD1": (1, 0),
}


def khoi_bai():
    return [k for k in KHOI if "nhan" in k]


def danh_so_hinh():
    """Đánh số Hình 1, 2, … theo thứ tự xuất hiện; trả {nhãn: [số hình]}."""
    so, out = 0, {}
    for k in khoi_bai():
        ds = []
        for h in k.get("hinh", []):
            so += 1
            ds.append(so)
            if h["tikz"] == "HAI_LY":
                so += 1
                ds.append(so)
        out[k["nhan"]] = ds
    return out


def de_in(k, so):
    ds = so[k["nhan"]]
    s = k["de"]
    for i, n in enumerate(ds):
        s = s.replace("{H%d}" % i, f"Hình {n}")
    return s


def hinh_in(k, so):
    """→ dict ProblemFigure (hoặc None)."""
    if not k.get("hinh"):
        return None
    h, ds = k["hinh"][0], so[k["nhan"]]
    if h["tikz"] == "HAI_LY":
        return {"type": "tikz", "tikz": hai_ly(f"Hình {ds[0]}", f"Hình {ds[1]}"), "caption": "", "pos": h["pos"],
                "width": h["width"]}
    return {"type": "tikz", "tikz": h["tikz"], "caption": f"Hình {ds[0]}", "pos": h["pos"], "width": h["width"]}


def cho_tho(k, so):
    s = de_in(k, so)
    for i, h in enumerate(k.get("hinh", [])):
        s += f" [HÌNH ĐÃ VẼ SẴN: {h['mota']}]"
    return s


def kiem():
    loi = []

    def bang(ten, that, mong, tol=1e-9):
        if abs(that - mong) > tol:
            loi.append(f"{ten}: máy {that} ≠ sơ đồ {mong}")

    p = math.pi
    bang("B2 AC", math.sqrt(5 ** 2 - 4 ** 2), 3)
    bang("VD2 S/π", 4 * 10 ** 2, 400)
    bang("B3", PI * 3 ** 2 * 11, 310.86, 1e-6)
    bang("B4", round(PI * 2.9 ** 2 * 12.5 / 3), 110)
    bang("B5", 4 * PI * 11 ** 2, 1519.76, 1e-6)
    bang("B6", 1800 / 30, 60)
    bang("VD3a", round(2 * p * 0.5 * 1.6, 2), 5.03)
    bang("VD3b", round(p * 0.25 * 1.6 * 1000), 1257)
    bang("B7a", 2 * PI * 50 * 150, 47100, 1e-6)
    bang("B7b", PI * 50 ** 2 * 40, 314000, 1e-6)
    bang("VD4 h", math.sqrt(10 ** 2 - 6 ** 2), 8)
    bang("VD4 V/π", 6 ** 2 * 8 / 3, 96)
    bang("B8 h", math.sqrt(17 ** 2 - 8 ** 2), 15)
    bang("B8 S/π", 8 * 17, 136)
    bang("B8 V/π", 8 ** 2 * 15 / 3, 320)
    bang("VD5a", PI * 25 * 10, 785, 1e-6)
    bang("VD5b", PI * 25 * 5, 392.5, 1e-6)
    bang("B9a", round(p * 2.5 ** 2 * 10, 2), 196.35)
    bang("B9b", round((p * 2.5 ** 2 * 5 / 5 / (4 / 3 * p)) ** (1 / 3), 2), 1.67)
    bang("B11", PI * 20 ** 2 * 60, 75360, 1e-6)
    bang("B12 S/π", 4 * 5 ** 2, 100)
    bang("B13", PI * 2.5 ** 2 * 6 / 3, 39.25, 1e-6)
    bang("B14a", round(PI * 0.25 * 1.75, 2), 1.37)
    bang("B14b", PI * 0.25 * 0.75 * 1000, 588.75, 1e-6)
    bang("B15 h", math.sqrt(13 ** 2 - 5 ** 2), 12)
    bang("B15 V", round(math.pi * 5 ** 2 * 12 / 3, 2), 314.16)
    bang("B16a", PI * 25 * 15, 1177.5, 1e-6)
    bang("B16b mm", round(4 / 3 * PI * 8 / (PI * 25) * 10), 4)
    return loi


def dem_the():
    dem_ = collections.Counter()
    for k in khoi_bai():
        if k["ht"] == "vi_du":
            continue
        ma = k["dang"].split("+")
        for t in re.findall(r"\[(NB|TH|VD)\]", k["de"]):
            dem_[(next(mm for mm in ma if re.match(rf"{t}\d", mm)), k["tier"])] += 1
    loi = []
    for d, (lop, btvn) in TM_DANG.items():
        for tier, want in (("onclass", lop), ("btvn", btvn)):
            if dem_[(d, tier)] != want:
                loi.append(f"{d} {tier}: sơ đồ {dem_[(d, tier)]} thẻ, TM {want}")
    tong = collections.Counter()
    for (d, tier), n in dem_.items():
        tong[(re.match(r"[A-Z]+", d)[0], tier)] += n
    return loi, dict(tong)


if __name__ == "__main__":
    l1 = kiem()
    l2, tong = dem_the()
    so = danh_so_hinh()
    print("thẻ:", tong, "· hình:", sum(len(v) for v in so.values()), so)
    for l in l1 + l2:
        print("✗", l)
    print("SẠCH" if not (l1 + l2) else f"{len(l1 + l2)} lỗi")
    sys.exit(1 if (l1 + l2) else 0)
