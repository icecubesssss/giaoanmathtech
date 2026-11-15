#!/usr/bin/env python3
r"""BỘ ĐỀ CUỐI HỌC KÌ I TOÁN 7 (KNTT, Hà Nội): 3 ĐỀ ÔN TẬP + 3 ĐỀ CHÍNH THỨC, mỗi đề kèm MA TRẬN + ĐÁP ÁN.

Nguồn (11/11/2026):
  - câu đã bốc: storage/gemini/bo-cau/l7-ck1.json   (scripts/bo_cau_ck1_lop7.py — khung, chặn trùng)
  - chữ LaTeX + lời giải + hình: storage/gemini/xong/chep-l7-ck1-*.json (Gemini chép từ ảnh trang,
    việc sinh bằng scripts/gemini/viec_chep_cau.py), Claude soát ⇒ mọi chỗ sửa ghi trong SUA bên dưới.
  - bản ghi phân dạng: inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi/
Phạm vi: Ch.I–V + Ch.VI bài 20–21 (tiến độ B/C của Thầy, trường pham_vi_ck1 trong
config/khung-phan-dang/lop-7-ck1-kntt.json).

KHUNG (bản 2, 12/11/2026 — chi tiết ở scripts/bo_cau_ck1_lop7.py):
  đề ôn  : TN 12 · B1 tính 1,0 · B2 tìm x 1,5 · B3 thực tế/biểu đồ 0,75 · B4 chia tỉ lệ 1,0 · B5 song song 1,0
           · B6 tam giác 1,25 · B7 VDC 0,5 (phủ đủ 22 dạng)
  đề CT  : TN 8 · B1 tính 1,5 · B2 tìm x 1,5 · B3 chia tỉ lệ 1,5 · B4 song song 1,5 · B5 tam giác 1,5 · B6 VDC 0,5
           (mỗi câu chỉ top 1–3 dạng).

    python3 scripts/de_ck1_lop7.py   → inputs/seeds/lop-7/de-cuoi-ki-1/*.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "inputs/seeds/lop-7/de-cuoi-ki-1"
BG = ROOT / "inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi"
CHEP = ROOT / "storage/gemini/xong"
BO = json.loads((ROOT / "storage/gemini/bo-cau/l7-ck1.json").read_text())
BR = " [[br]] "

BANK = {f.stem: json.loads(f.read_text()) for f in BG.glob("l7-ck1-*.json")}
CH: dict[str, dict] = {}
for f in sorted(CHEP.glob("chep*-l7-ck1-*.json")):  # chep-* (bản 1) + chepb2-* (ý mới của bản 2)
    kq = json.loads(f.read_text()).get("ket_qua") or {}
    CH.setdefault(f.stem.split("-", 1)[1], {}).update({c["cau"]: c for c in kq.get("cau", [])})

TEN_TRUONG = {
    "banmai": "Ban Mai School", "lomonoxop": "THCS M.V. Lômônôxốp", "mariecurie": "THCS Marie Curie",
    "ngoclam": "THCS Ngọc Lâm", "nguyentruongto": "THCS Nguyễn Trường Tộ", "phandinhgiot": "THCS Phan Đình Giót",
    "phucdien": "THCS Phúc Diễn", "phucdong": "THCS Phúc Đồng", "thachthat": "Phòng GD\\&ĐT Thạch Thất",
    "aimo": "THCS Ái Mộ", "cum14": "Cụm chuyên môn số 14", "donganh": "Phòng GD\\&ĐT Đông Anh",
    "dongocdu": "THCS Đỗ Ngọc Du", "ducgiang": "THCS Đức Giang", "giangbien": "THCS Giang Biên",
    "hatmon": "THCS Hát Môn", "lengochan": "THCS Lê Ngọc Hân", "lyson": "THCS Lý Sơn", "ngocthuy": "THCS Ngọc Thụy",
    "ngogiatu": "THCS Ngô Gia Tự", "ngosilien": "THCS Ngô Sĩ Liên", "nguyenbinhkhiem": "THCS Nguyễn Bỉnh Khiêm",
    "tantrieu": "THCS Tân Triều", "thaithinh": "THCS Thái Thịnh", "thanhcong": "THCS Thành Công",
}
LA_MA = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 0: "VDC"}

# ----------------------------------------------------------- SỬA SAU KHI SOÁT (Claude, đối chiếu ảnh đề)
# khoá = "mã-đề#câu"; giá trị = các trường đè lên kết quả Gemini (de_bai, loi_dan, phuong_an, dap_an,
# loi_giai = list[(văn bản, điểm|None)], tikz, hinh_de: True/False). Mỗi chỗ ghi lí do.
HINH_PHUCDONG = r"""\begin{tikzpicture}[line cap=round,font=\small,scale=1]
\draw (-0.4,2) -- (5.4,2); \draw (-0.4,0) -- (5.4,0);
\coordinate (D) at (1.5,2); \coordinate (H) at (0.1,0); \coordinate (C) at (2.02,2.74);
\coordinate (F) at (4.2,0); \coordinate (B) at (3.045,2); \coordinate (M) at (2.6,2.78);
\draw (-0.13,-0.33) -- (C); \draw (4.44,-0.42) -- (M);
\node[above left] at (C) {$C$}; \node[above right] at (M) {$M$};
\node[below left] at (D) {$D$}; \node[below right] at (B) {$B$}; \node[above] at (4.6,2) {$E$};
\node[below left] at (H) {$H$}; \node[below right] at (F) {$F$}; \node[below] at (5.2,0) {$A$};
\draw (1.85,2) arc (0:55:0.35); \node[font=\scriptsize] at (2.15,2.28) {$55^\circ$};
\draw (0.45,0) arc (0:55:0.35); \node[font=\scriptsize] at (0.78,0.25) {$55^\circ$};
\draw (4.55,0) arc (0:120:0.35); \node[font=\scriptsize] at (4.85,0.38) {$120^\circ$};
\draw (2.86,2.32) arc (120:180:0.37); \node[font=\scriptsize] at (2.55,2.25) {?};
\end{tikzpicture}"""
HINH_CAY_DAU = r"""\begin{tikzpicture}[font=\scriptsize,x=0.9cm,y=0.9cm]
\draw[gray!30] (0,0) grid[xstep=1,ystep=0.5] (5.5,3);
\draw[->] (0,0) -- (5.8,0) node[below] {Ngày};
\draw[->] (0,0) -- (0,3.3);
\node[rotate=90] at (-0.95,1.5) {Chiều cao (cm)};
\foreach \y/\t in {0/0,0.5/{0{,}5},1/1,1.5/{1{,}5},2/2,2.5/{2{,}5},3/3} \node[left] at (0,\y) {$\t$};
\foreach \x in {1,...,5} \node[below] at (\x,0) {$\x$};
\draw[thick,blue!70!black] (1,0.5) -- (2,0.75) -- (3,1) -- (4,1.4) -- (5,2.5);
\foreach \x/\y/\t in {1/0.5/{0{,}5},2/0.75/{0{,}75},3/1/1,4/1.4/{1{,}4},5/2.5/{2{,}5}}
  {\fill[blue!70!black] (\x,\y) circle (1.5pt); \node[above left] at (\x,\y) {$\t$};}
\node[font=\small\bfseries] at (2.75,3.45) {Chiều cao của cây đậu};
\end{tikzpicture}"""
HINH_QUAT_TT = r"""\begin{tikzpicture}[font=\scriptsize]
\fill[yellow!70!orange] (0,0) -- (90:1.6) arc (90:234:1.6) -- cycle;
\fill[green!55!lime] (0,0) -- (234:1.6) arc (234:306:1.6) -- cycle;
\fill[orange!75!red] (0,0) -- (306:1.6) arc (306:360:1.6) -- cycle;
\fill[blue!45!cyan] (0,0) -- (0:1.6) arc (0:90:1.6) -- cycle;
\foreach \a in {90,234,306,360} \draw[white,thick] (0,0) -- (\a:1.6);
\node[align=center] at (162:0.95) {Bóng đá\\$40\%$};
\node[align=center] at (45:0.95) {Cầu lông\\$25\%$};
\node[align=center,anchor=west] at (333:1.75) {Bóng bàn $15\%$};
\node[align=center,anchor=north] at (270:1.7) {Bóng chuyền $20\%$};
\end{tikzpicture}"""
BANG_DIEM_HM = (r"\begin{center}\small\begin{tabular}{|l|*{10}{c|}}\hline Điểm & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 \\ \hline "
                r"Số học sinh & 0 & 0 & 3 & 1 & 6 & 8 & 12 & 6 & 5 & 3 \\ \hline\end{tabular}\end{center}")
SUA: dict[str, dict] = {
    # câu Hát Môn I.4 dùng riêng ⇒ bỏ câu "Sử dụng dữ kiện … Câu 4; câu 5"
    "l7-ck1-2526-hatmon#I.4": {"loi_dan": "Biểu đồ hình quạt tròn ở hình bên biểu diễn kết quả thống kê (tính theo tỉ lệ phần trăm) "
                               "chọn môn thể thao ưa thích nhất trong bốn môn: bóng đá, bóng bàn, cầu lông, bóng chuyền của học sinh khối 7 trường THCS."},
    # bảng $$array$$ nhiều dòng ⇒ tabular
    "l7-ck1-2526-hatmon#I.6": {"de_bai": "Kết quả kiểm tra môn Toán của học sinh lớp 7A được cho trong bảng sau:" + BANG_DIEM_HM
                               + "Từ bảng thống kê hãy cho biết lớp 7A có bao nhiêu học sinh?"},
    # đề in "3,5,4" (liền nhau) ⇒ 3; 5; 4
    "l7-ck1-2425-ngoclam#II.3": {"de_bai": "Hưởng ứng phong trào “Tuần lễ quyên góp sách giáo khoa cũ” của Liên đội, ba chi đội 7A, 7B, 7C "
                                 "quyên góp được số bộ sách giáo khoa lần lượt tỉ lệ với các số $3; 5; 4$. Hỏi mỗi chi đội quyên góp được bao nhiêu "
                                 "bộ sách giáo khoa, biết tổng số bộ sách của hai chi đội 7A và 7C là $35$ bộ."},
    # đề lớp 7 in nhầm lớp 6A, 6B, 6C ⇒ 7A, 7B, 7C (đề + lời giải)
    "l7-ck1-2526-mariecurie#II.3": {"_thay": [("6A", "7A"), ("6B", "7B"), ("6C", "7C"), ("ba số 5; 7; 8", "ba số $5; 7; 8$"),
                                              ("380 quyển", "$380$ quyển")]},
    # "tỉ lệ thuận với" là cách nói của đại lượng tỉ lệ (học GK2) ⇒ "tỉ lệ với"
    "l7-ck1-2526-cum14#II.3": {"_thay": [("tỉ lệ thuận với", "tỉ lệ với")]},
    # đề in thiếu đơn vị: "là 63." (HDC dùng cm)
    "l7-ck1-2526-giangbien#II.6": {"_thay": [("là $63$.", "là $63$ cm.")]},
    # đề in "Cho hình vẽ bên, (HS vẽ hình vào bài làm)" ⇒ bỏ dấu phẩy thừa
    "l7-ck1-2526-lyson#II.5.2a": {"_thay": [("Cho hình vẽ bên, (HS vẽ hình vào bài làm)", "Cho hình vẽ bên (học sinh vẽ lại hình vào bài làm).")]},
    # Bài 6: biểu thức cần tính dài ⇒ đứng riêng một dòng, giữa trang (khỏi gãy sau dấu +)
    "l7-ck1-2425-ngoclam#II.5": {"_thay": [(". Tính $M = ", ". Tính giá trị biểu thức\n\\centerline{$\\displaystyle M = "),
                                           ("+ \\frac{y+z}{x}$", "+ \\frac{y+z}{x}.$}")]},
    "l7-ck1-2425-thachthat#II.5": {"_thay": [("biểu thức: $A = ", "biểu thức\n\\centerline{$\\displaystyle A = "),
                                             ("{xy - yz + zx}$", "{xy - yz + zx}.$}")]},
    "l7-ck1-2526-ngoclam#II.5": {"_thay": [("biết: $\\frac{y + z + 1}", "biết\n\\centerline{$\\displaystyle \\frac{y + z + 1}"),
                                           ("{x + y + z}$.", "{x + y + z}.$}")]},
    "l7-ck1-2526-tantrieu#I.7": {"_thay": [("số đo của góc F là", "số đo của $\\widehat{F}$ là")]},
    # điều kiện dài + biểu thức P: đứng riêng dòng, giữa trang (bản cũ dãn chữ vì phân số to nằm trong dòng)
    "l7-ck1-2526-lomonoxop#II.5": {"_thay": [("thỏa mãn $\\frac{a+b-c}", "thỏa mãn\n\\centerline{$\\displaystyle \\frac{a+b-c}"),
                                             ("{2b}$. Tính giá trị của biểu thức $P = ", "{2b}.$}\nTính giá trị của biểu thức\n\\centerline{$\\displaystyle P = "),
                                             ("\\left(1 + \\frac{c}{b}\\right)$.", "\\left(1 + \\frac{c}{b}\\right).$}")]},
    "l7-ck1-2526-ngocthuy#3": {"_thay": [("tết trông cây", "Tết trồng cây")]},
    "l7-ck1-2425-mariecurie#I.7": {"_thay": [("Eculid", "Euclid")]},
    # ý tìm hai/ba ẩn dưới lời dẫn chung "Tìm x" ⇒ ghi rõ ẩn
    "l7-ck1-2425-phucdong#II.2b": {"de_bai": r"Tìm $x, y$ biết $\frac{x}{3} = \frac{y}{5}$ và $y - x = 16$."},
    "l7-ck1-2425-banmai#II.2a": {"loi_dan": "", "de_bai": r"Tìm $x, y, z$ biết $\frac{x}{2} = \frac{y}{5} = \frac{z}{6}$ và $x - y + z = -18$."},
    # dấu chấm làm dấu nhân ⇒ \cdot
    "l7-ck1-2526-ducgiang#I.4": {"_thay": [("7.x = 5.y", r"7 \cdot x = 5 \cdot y")]},
    "l7-ck1-2526-lengochan#II.2a": {"_thay": [("0{,}2.x", r"0{,}2 \cdot x")]},
    # lời giải Gemini dùng ⇔ + "điều kiện xác định" (lớp 8) ⇒ viết lại theo tính chất tỉ lệ thức
    "l7-ck1-2526-ngoclam#II.2b": {"loi_giai": [
        {"buoc": r"Từ $\frac{x - 3}{5} = \frac{20}{x - 3}$ suy ra $(x - 3) \cdot (x - 3) = 5 \cdot 20$, hay $(x - 3)^2 = 100$.", "diem": 0.25},
        {"buoc": "Do đó $x - 3 = 10$ hoặc $x - 3 = -10$.\n$x = 13$ hoặc $x = -7$. Vậy $x \\in \\{13; -7\\}$.", "diem": 0.25}]},
    # cổng dan_dat bắt "Hôm nay" như lời xưng hô ⇒ đổi chữ, giữ nghĩa
    "l7-ck1-2526-thaithinh#II.5": {"_thay": [("Hôm nay, bạn Việt", "Một hôm, bạn Việt")]},
    # HÌNH VẼ LẠI (soi PDF 11/11: hình Gemini nhãn chồng nhau). Số đo đúng tỉ lệ, nhãn như đề gốc.
    "l7-ck1-2526-phucdong#II.5a": {"tikz": HINH_PHUCDONG},
    "l7-ck1-2526-tantrieu#I.5": {"tikz": HINH_CAY_DAU},
    "l7-ck1-2526-tantrieu#I.6": {"tikz": HINH_QUAT_TT},
    # THAY CÂU (xem THAY): chép tay từ ảnh đề
    "l7-ck1-2425-phucdien#II.1.1b": {
        "de_bai": r"$\sqrt{\frac{9}{25}} - \frac{3}{17} \cdot \frac{34}{15} + \left(-\frac{1}{3}\right)^2$", "dap_an": r"$\frac{14}{45}$",
        "loi_giai": [{"buoc": r"$= \frac{3}{5} - \frac{2}{5} + \frac{1}{9}$", "diem": 0.25},
                     {"buoc": r"$= \frac{1}{5} + \frac{1}{9} = \frac{9}{45} + \frac{5}{45} = \frac{14}{45}$.", "diem": 0.25}]},
    "l7-ck1-2526-thaithinh#I.4": {
        "de_bai": r"Trong các dữ liệu sau, dữ liệu nào \textbf{không} phải là số liệu?",
        "phuong_an": ["Chiều cao của các bạn học sinh khối 7.", "Nơi sinh của các học sinh trong một trường.",
                      "Số học sinh đạt loại giỏi môn Toán.", "Cân nặng của trẻ sơ sinh."], "dap_an": "B",
        "loi_giai": [{"buoc": "Nơi sinh là dữ liệu không phải số (chữ); chiều cao, số học sinh, cân nặng đều là số liệu."}]},
}
# câu bốc thay sau khi soát (cũ → mới)
THAY = {
    "l7-ck1-2526-lyson#II.1.1": "l7-ck1-2425-phucdien#II.1.1b",   # "chọn số vô tỉ, làm tròn" không phải phép tính
    "l7-ck1-2526-hatmon#I.5": "l7-ck1-2526-thaithinh#I.4",        # câu dựa vào biểu đồ của I.4 (đã dùng ở đề ôn 1), đề không có hình
}

LOI_DAN = {"tinh": "Thực hiện phép tính (tính hợp lí nếu có thể):", "timx": "Tìm $x$, biết:"}
BAI_HINH = ("songsong", "tamgiac")


def d(x):
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def ban_ghi(ref):
    m, c = ref.split("#")
    return next(q for q in BANK[m]["cau"] if q["cau"] == c)


def chep(ref):
    m, c = ref.split("#")
    g = json.loads(json.dumps(CH.get(m, {}).get(c) or {}))
    s = dict(SUA.get(ref, {}))
    thay = s.pop("_thay", [])
    g.update(s)
    if not g.get("de_bai"):
        raise SystemExit(f"✗ chưa có bản chép {ref}")
    for a, b in thay:
        for k in ("de_bai", "loi_dan", "dap_an"):
            if g.get(k):
                g[k] = g[k].replace(a, b)
        for st in g.get("loi_giai", []):
            st["buoc"] = st["buoc"].replace(a, b)
    return g


def doi(x):
    """Áp THAY: câu bị thay ⇒ lấy câu mới cùng dạng/mức từ bản ghi."""
    if x.get("ref") not in THAY:
        return x
    r = THAY[x["ref"]]
    q = ban_ghi(r)
    return dict(x, ref=r, dang=q["dang"], muc=q["muc"], diem_goc=q["diem"])


def nguon(ref):
    m, c = ref.split("#")
    k = m.split("-")[-1]
    nam = "2024--2025" if "-2425-" in m else "2025--2026"
    return f"{TEN_TRUONG.get(k, k)} ({nam}), câu {c}"


XUONG_DONG = re.compile(r"(?<!\\)\\n(?![a-z])")  # giữ \\neq \\ne \\notin \\node


def sach(s: str) -> str:
    """Chuẩn hoá chữ Gemini: bỏ nhãn đầu, $$..$$ → \\[..\\], xuống dòng NGOÀI công thức → [[br]]
    (xuống dòng TRONG công thức chỉ là khoảng trắng — [[br]] trong math làm vỡ LaTeX)."""
    s = (s or "").strip()
    s = re.sub(r"^\s*(Câu\s*\d+[.:]?|[a-d]\)|\d+\)|Bài\s*[IVX\d.]+[.:)]?)\s*", "", s)
    s = s.replace("Điều kiện xác định", "Điều kiện").replace("điều kiện xác định", "điều kiện")  # thuật ngữ lớp 8
    s = XUONG_DONG.sub("\n", s)  # Gemini hay viết "\\n" (2 kí tự) thay cho xuống dòng
    s = re.sub(r"\$\$(.+?)\$\$", lambda m: "\\[" + m.group(1) + "\\]", s, flags=re.S)
    s = bao_aligned(s)
    s = re.sub(r"\\\[(.*?)\\\]", lambda m: "\n$\\displaystyle " + m.group(1).strip() + "$\n", s, flags=re.S)
    parts = re.split(r"(\\\[.*?\\\]|\$[^$]*\$)", s, flags=re.S)
    out = []
    for i, p in enumerate(parts):
        if i % 2:
            out.append(re.sub(r"\s*\n\s*", " ", p))
        else:
            out.append(p.replace("\n- ", BR + "-- ").replace("\n", BR))
    s = "".join(out).strip()
    s = re.sub(r"(\s*\[\[br\]\]\s*){2,}", BR, s)
    s = re.sub(r"^(\s*\[\[br\]\]\s*)+|(\s*\[\[br\]\]\s*)+$", "", s)
    if "\\" in s and "$" not in s and "\\[" not in s and "[[br]]" not in s and "\\begin" not in s \
            and not re.search(r"[À-ỹ]|\b[a-z]{3,}\b(?<!frac)(?<!left)", re.sub(r"\\[a-zA-Z]+", "", s)):
        s = f"${s}$"  # biểu thức trơ Gemini quên bọc $ (chỉ một dòng, không có chữ)
    return dep(s)


def dep(s: str) -> str:
    r"""Trình bày (soi PDF 11/11, Thầy chê "lộn xộn"):
    - phân số trong dòng chữ bé tí ⇒ \dfrac (trừ phân số nằm ở số mũ/chỉ số);
    - "|-20|" in ra "| − 20|" (TeX coi − là phép trừ) ⇒ "|{-}20|";
    - tên lớp 7A, 7B trong $..$ in nghiêng ⇒ \text{7A};
    - "Cạnh- góc- cạnh" ⇒ "cạnh -- góc -- cạnh"."""
    def toan(m):
        t = m.group(0)
        t = re.sub(r"(?<![\^_a-zA-Z])(?<![\^_]\{)\\frac(?![a-z])", r"\\dfrac", t)
        t = re.sub(r"(?<=[\^_])\{\\dfrac", r"{\\tfrac", t)
        t = re.sub(r"((?:^\$|[=+(,;:<>\[]|\\cdot|\\left[(\[]|-)\s*)\|\s*-", r"\1|{-}", t)
        t = re.sub(r"(?<![\w\\])([6-9][A-E])(?![\w])", r"\\text{\1}", t)
        return t
    s = re.sub(r"\$[^$]+\$", toan, s)
    s = re.sub(r"\b(cạnh|góc|huyền|nhọn)\s*[-–]+\s*(?=(cạnh|góc)\b)", r"\1 -- ", s, flags=re.I)
    s = re.sub(r"\b(Cạnh|Góc)(?= -- | huyền -- )", lambda m: m.group(1).lower(), s)
    return s


def bao_aligned(s):
    """Bọc $..$ cho \\begin{aligned} nằm NGOÀI chế độ toán (Gemini quên)."""
    out, i = [], 0
    for m in re.finditer(r"\\begin\{aligned\}.*?\\end\{aligned\}", s, flags=re.S):
        truoc = s[:m.start()]
        trong_math = truoc.count("$") % 2 == 1 or truoc.rfind("\\[") > truoc.rfind("\\]")
        out.append(s[i:m.start()] + (m.group(0) if trong_math else f"${m.group(0)}$"))
        i = m.end()
    return "".join(out) + s[i:]


def chia_diem(steps, tong):
    """steps: list (text, diem|None). Phân lại `tong` theo bội 0,25, tỉ lệ với điểm gốc; bước 0đ gộp vào bước sau."""
    if not steps:
        return [("", tong)]
    w = [s[1] if s[1] else 0 for s in steps]
    if sum(w) == 0:
        w = [1] * len(steps)
    n = round(tong / 0.25)
    raw = [x / sum(w) * n for x in w]
    q = [int(r) for r in raw]
    for i in sorted(range(len(raw)), key=lambda i: -(raw[i] - q[i]))[: n - sum(q)]:
        q[i] += 1
    out, cho = [], []
    for (t, _), k in zip(steps, q):
        cho.append(t)
        if k:
            out.append((BR.join(cho), k * 0.25))
            cho = []
    if cho:  # đuôi không điểm: gộp vào bước cuối có điểm
        t, k = out[-1]
        out[-1] = (BR.join([t] + cho), k)
    return out


def buoc(steps):
    return BR.join(f"{t} \\hfill \\textit{{({d(k)}đ)}}" if k else t for t, k in steps)


def steps_cua(g):
    return [(sach(s["buoc"]), s.get("diem")) for s in g.get("loi_giai", [])]


def tikz(g):
    t = (g.get("tikz") or (g.get("hinh") or {}).get("tikz") or "").strip()
    if not t:
        return ""
    t = XUONG_DONG.sub("\n", t)
    t = re.sub(r"(?<!\\)%.*", "", t)  # chú thích TikZ: gộp dòng ⇒ % nuốt hết phần sau
    t = re.sub(r"\n\s*\n+", "\n", t)
    for ten, v in re.findall(r"\\def\\(\w+)\{([^}]*)\}", t):  # sanitizer cấm \def
        t = re.sub(r"\\def\\" + ten + r"\{[^}]*\}\s*", "", t)
        t = re.sub(r"\\" + ten + r"(?![A-Za-z])", v, t)
    if "tikzpicture" not in t:
        t = "\\begin{tikzpicture}[line cap=round,line join=round,font=\\small]\n" + t + "\n\\end{tikzpicture}"
    return t


# ------------------------------------------------------------------ dựng đề
def tn(x):
    g = chep(x["ref"])
    opts = [sach(o) for o in g.get("phuong_an", [])]
    dap = g["dap_an"].strip()[:1]
    stem = (sach(g["loi_dan"]) + " " if g.get("loi_dan") else "") + sach(g["de_bai"])
    h = tikz(g)
    if h:  # hình đứng CẠNH phương án (cột phải), không chiếm cả một khúc giữa trang
        stem += ("\\par\\nopagebreak\\smallskip\\nopagebreak\\noindent\\begin{minipage}[c]{0.58\\linewidth}" + luoi_pa(opts, 0.58)
                 + "\\end{minipage}\\hfill\\begin{minipage}[c]{0.40\\linewidth}\\centering"
                 "\\adjustbox{max width=\\linewidth,max totalheight=3.9cm}{" + h + "}\\end{minipage}")
    else:
        stem += "\\par\\nopagebreak\\noindent\\begin{minipage}{\\linewidth}" + luoi_pa(opts, 1) + "\\end{minipage}"
    giai = " ".join(sach(s["buoc"]) for s in g.get("loi_giai", []))
    return dict(ref=x["ref"], stem=stem, opts=opts, dap=dap, giai=giai, muc=x["muc"], dang=x["dang"],
                nd=x.get("nd_mt") or ten_dang(x["dang"]))


def plainlen(s):
    return len(re.sub(r"\\[a-zA-Z]+\*?|\[\[[^\]]*\]\]|[{}$\\^_]", "", s or "").strip())


def luoi_pa(opts, rong):
    r"""Lưới phương án dựng THẲNG trong đề (không qua trường `options` của template: môi
    trường mcq ở đó để lọt một dấu cách sau \begin{mcq}{n} ⇒ phương án A thụt lệch B, C, D).
    `rong` = bề ngang cột chứa (1 = cả dòng). Số cột theo phương án dài nhất."""
    n = max(plainlen(o) for o in opts)
    if rong < 1:  # cột cạnh hình: tối đa 2 cột (4 cột thì "120°" rớt dòng — soi PDF 11/11)
        k = 2 if n <= 14 else 1
    else:
        k = 4 if n <= 13 else 2 if n <= 32 else 1
    return ("\\par\\noindent\\begin{mcq}{" + str(k) + "}"
            + "".join(f"\\mcqitem{{{'ABCD'[i]}}}{{{o}}}" for i, o in enumerate(opts)) + "\\end{mcq}")


def ten_dang(ma):
    k = json.loads((ROOT / "config/khung-phan-dang/lop-7-ck1-kntt.json").read_text())
    t = next(dd["ten"] for dd in k["dang"] if dd["ma"] == ma).split("(")[0].split(":")[0].strip()
    for u, m in (("ℚ", "Q"), ("ℝ", "R"), ("ℕ", "N"), ("ℤ", "Z"), ("ℚ", "Q")):
        t = t.replace(u, f"$\\mathbb{{{m}}}$")
    return t


def chuong(ma):
    k = json.loads((ROOT / "config/khung-phan-dang/lop-7-ck1-kntt.json").read_text())
    return next(dd["cd"] for dd in k["dang"] if dd["ma"] == ma)


def bai_le(b, so):  # Bài tính / tìm x: ý từ nhiều đề
    ys, out = b["items"], []
    dy = b["tong"] / len(ys)
    for nh, x in zip("abc", map(doi, ys)):
        g = chep(x["ref"])
        out.append(dict(nhan=nh, diem=dy, de=sach(g["de_bai"]), ref=x["ref"], muc=x["muc"], dang=x["dang"],
                        steps=chia_diem(steps_cua(g), dy)))
    return dict(so=so, key=b["key"], ten=b["ten"], mo=LOI_DAN[b["key"]], ys=out, hinh="", hinh_de=False)


def bai_nguyen(b, so):  # nguyên bài một đề
    key, B = b["key"], b["items"]
    ys = B["y"] if "y" in B else [B]
    goc = [y["diem_goc"] for y in ys]
    n = round(b["tong"] / 0.25)
    raw = [x / sum(goc) * n for x in goc]
    q = [max(1, int(r)) for r in raw]
    while sum(q) > n:
        q[q.index(max(q))] -= 1
    for i in sorted(range(len(raw)), key=lambda i: -(raw[i] - int(raw[i]))):
        if sum(q) >= n:
            break
        q[i] += 1
    g0 = chep(ys[0]["ref"])
    mo = sach(g0.get("loi_dan", ""))
    hinh, hinh_de = "", False
    out = []
    for y, k in zip(ys, q):
        g = chep(y["ref"])
        hinh = hinh or tikz(g)
        hinh_de = hinh_de or g.get("hinh_de", key == "songsong")
        nhan = "" if len(ys) == 1 else (y["ref"].split("#")[1][-1] if y["ref"][-1] in "abcd" else "hinh")
        de = sach(g["de_bai"])
        if len(ys) == 1 and not mo:
            mo, de = de, ""
        out.append(dict(nhan=nhan, diem=k * 0.25, de=de, ref=y["ref"], muc=y["muc"], dang=y["dang"],
                        steps=chia_diem(steps_cua(g), k * 0.25)))
    # đánh lại nhãn a, b, c liên tục (ý "vẽ hình" giữ tên riêng)
    i = 0
    for yy in out:
        if yy["nhan"] and yy["nhan"] != "hinh":
            yy["nhan"] = "abcd"[i]
            i += 1
    return dict(so=so, key=key, ten=b["ten"], mo=mo, ys=out, hinh=hinh, hinh_de=hinh_de)


def dung_de(D, i):
    return dict(ten=D["ten"], loai=D["loai"], so=D["so"], tn=[tn(doi(x)) for x in D["TN"]],
                bai=[(bai_le if b["loai"] == "le" else bai_nguyen)(b, j) for j, b in enumerate(D["bai"], 1)])


# ------------------------------------------------------------------ kiểm
def kiem(DS):
    loi, da = [], {}
    for D in DS:
        if len(D["tn"]) != (12 if D["loai"] == "on" else 8):
            loi.append(f"{D['ten']}: {len(D['tn'])} câu TN")
        tong = 0.0
        for i, c in enumerate(D["tn"], 1):
            tong += 0.25
            if c["dap"] not in "ABCD" or len(c["opts"]) != 4:
                loi.append(f"{D['ten']} TN{i} {c['ref']}: phương án/đáp án lỗi ({c['dap']}, {len(c['opts'])} PA)")
            bg = ban_ghi(c["ref"]).get("dap_an", "")[:1]
            if bg in "ABCD" and bg and bg != c["dap"]:
                loi.append(f"{D['ten']} TN{i} {c['ref']}: đáp án chép {c['dap']} ≠ bản ghi {bg}")
            da.setdefault(c["ref"], []).append(D["ten"])
        for b in D["bai"]:
            for yy in b["ys"]:
                sd = round(sum(k for _, k in yy["steps"] if k), 2)
                if abs(sd - yy["diem"]) > 1e-9:
                    loi.append(f"{D['ten']} Bài {b['so']}{yy['nhan']}: điểm bước {sd} ≠ {yy['diem']}")
                tong += yy["diem"]
                da.setdefault(yy["ref"], []).append(D["ten"])
        if abs(tong - 10) > 1e-9:
            loi.append(f"{D['ten']}: tổng {tong}")
        for b in D["bai"]:
            if b["hinh_de"] and not b["hinh"]:
                loi.append(f"{D['ten']} Bài {b['so']}: đề cần hình nhưng chưa có TikZ")
    for r, v in da.items():
        if len(v) > 1:
            loi.append(f"{r} dùng {len(v)} lần: {v}")
    return loi


# ------------------------------------------------------------------ xuất seed (khuôn de_ck1_lop6.py)
def tn_dau(n):
    return (f"\\textbf{{PHẦN I. TRẮC NGHIỆM ({d(n * 0.25)} điểm).}} \\textit{{Mỗi câu 0,25 điểm. Chọn chữ cái đứng trước "
            "câu trả lời đúng rồi ghi vào bài làm (ví dụ: 1 -- A).}")


def tl_dau(n):
    return f"\\textbf{{PHẦN II. TỰ LUẬN ({d(10 - n * 0.25)} điểm)}}"


def ten_de(D):
    return f"Đề ôn tập số {D['so']}" if D["loai"] == "on" else f"Đề kiểm tra chính thức số {D['so']}"


def slug(D, mt=False):
    if D["loai"] == "on":
        return f"ma-tran-va-dap-an-on-tap-cuoi-ki-1-so-{D['so']}" if mt else f"de-on-tap-cuoi-ki-1-so-{D['so']}"
    return f"ma-tran-va-dap-an-cuoi-ki-1-de-{D['so']}" if mt else f"de-kiem-tra-cuoi-ki-1-de-{D['so']}"


def khoi_tn(i, c):
    return dict(type="problem", label=f"Câu {i}.", level=1 if c["muc"] == "NB" else 2, statement=c["stem"],
                answer=c["dap"], solution=f"Chọn \\textbf{{{c['dap']}}}. " + c["giai"], tier="onclass")


def de_bai(b):
    tong = sum(yy["diem"] for yy in b["ys"])
    st = f"\\textbf{{({d(tong)} điểm)}} " + b["mo"]
    ys = [yy for yy in b["ys"] if yy["de"]]
    dong = [("Vẽ hình, ghi giả thiết, kết luận." if yy["nhan"] == "hinh" else
             (f"{yy['nhan']}) " if yy["nhan"] else "") + yy["de"]) for yy in ys]
    if b["hinh"] and b["hinh_de"]:
        # đề chung trọn dòng; các ý a) b) c) cột trái, HÌNH cột phải (hết khoảng trắng dưới hình)
        trai = "\\\\[3pt]".join(dong)
        return (st + "\\par\\nopagebreak\\smallskip\\nopagebreak\\noindent\\begin{minipage}[c]{0.55\\linewidth}\\raggedright " + trai
                + "\\end{minipage}\\hfill\\begin{minipage}[c]{0.43\\linewidth}\\centering"
                "\\adjustbox{max width=\\linewidth,max totalheight=4.4cm}{" + b["hinh"] + "}\\end{minipage}")
    if b["key"] in ("tinh", "timx") and all(yy["nhan"] for yy in ys):
        n = max(plainlen(x) for x in dong)
        k = 3 if n <= 22 else 2 if n <= 36 else 1  # ý ngắn xếp 2–3 cột như đề lớp 6
        if k > 1:
            w = f"{0.98 / k:.2f}"
            hang = [dong[i:i + k] for i in range(0, len(dong), k)]
            return st + BR + BR.join("".join(f"\\makebox[{w}\\linewidth][l]{{{x}}}" for x in h[:-1]) + h[-1]
                                     for h in hang)
    return st + "".join(BR + x for x in dong)


def loi_giai_bai(b):
    parts = []
    if b["hinh"] and b["key"] in BAI_HINH:  # cổng loi_giai_thi_gate: bài hình phải có hình đầu lời giải
        parts.append("\\begin{center}\\adjustbox{max width=0.5\\linewidth,max totalheight=5cm}{" + b["hinh"] + "}\\end{center}")
    for yy in b["ys"]:
        ten = "Vẽ hình, GT -- KL" if yy["nhan"] == "hinh" else yy["nhan"] + ")"
        dau = f"\\textbf{{{ten} ({d(yy['diem'])}đ)}}" + BR if yy["nhan"] else ""
        parts.append(dau + buoc(yy["steps"]))
    return BR.join(parts)


def khoi_bai(b, het=False):
    st = de_bai(b) + ("\\par\\smallskip\\centerline{\\textit{$-$ HẾT $-$}}" if het else "")
    return dict(type="problem", label=f"Bài {b['so']}.", level=3 if b["key"] in (*BAI_HINH, "vdc") else 2, statement=st,
                solution=loi_giai_bai(b), tier="onclass")


def de_json(D):
    B, n = D["bai"], len(D["tn"])
    st = [dict(kind="review", number=1, title="", blocks=[dict(type="para", text=tn_dau(n))] + [khoi_tn(i, c) for i, c in enumerate(D["tn"], 1)]),
          dict(kind="concept", number=2, title="", blocks=[dict(type="para", text=tl_dau(n)), khoi_bai(B[0]), khoi_bai(B[1])]),
          dict(kind="practice1", number=3, title="", blocks=[khoi_bai(b) for b in B[2:4]]),
          dict(kind="practice2", number=4, title="", blocks=[khoi_bai(b) for b in B[4:-1]]),
          dict(kind="reflection", number=5, title="", blocks=[khoi_bai(B[-1], het=True)])]
    if D["loai"] == "on":
        tit, eb = f"Đề ôn tập cuối học kì I — Số {D['so']} (90 phút)", f"LỚP 7 • ĐỀ ÔN TẬP SỐ {D['so']}"
    else:
        tit, eb = f"Đề kiểm tra cuối học kì I — Đề {D['so']} (90 phút)", f"LỚP 7 • ĐỀ CHÍNH THỨC SỐ {D['so']}"
    return dict(slug=slug(D), title=tit, eyebrow=eb, grade_label="Lớp 7", class_tier="", theme="de_thi", stages=st)


def hang_mt(D):
    rows = []
    for i, c in enumerate(D["tn"], 1):
        rows.append((f"Câu {i}", ten_dang(c["dang"]), chuong(c["dang"]), c["muc"], 0.25, nguon(c["ref"])))
    for b in D["bai"]:
        for yy in b["ys"]:
            nh = f"Bài {b['so']}" + ("" if not yy["nhan"] else ("(hình)" if yy["nhan"] == "hinh" else yy["nhan"]))
            rows.append((nh, ten_dang(yy["dang"]), chuong(yy["dang"]), yy["muc"], yy["diem"], nguon(yy["ref"])))
    return rows


def bang_mt(rows):
    s = ("\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.05}\n"
         "\\begin{tabular}{|c|p{5.0cm}|c|c|c|p{5.6cm}|}\\hline\n"
         "\\textbf{Câu} & \\textbf{Dạng bài} & \\textbf{Chương} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Nguồn đề (Hà Nội)} \\\\ \\hline\n")
    for c, nd, ch, m, di, ng in rows:
        s += f"{c} & {nd} & {LA_MA[ch]} & {m} & {d(di)} & {ng} \\\\ \\hline\n"
    s += f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{TỔNG}}}} & \\textbf{{{d(sum(r[4] for r in rows))}}} & \\\\ \\hline\n\\end{{tabular}}\\end{{center}}"
    return s


def bang_tong(rows):
    M = ["NB", "TH", "VD", "VDC"]
    ch = sorted({r[2] for r in rows}, key=lambda c: (c == 0, c))
    t = {c: {m: 0.0 for m in M} for c in ch}
    for r in rows:
        t[r[2]][r[3]] += r[4]
    ten = {1: "I. Số hữu tỉ", 2: "II. Số thực", 3: "III. Góc và đường thẳng song song", 4: "IV. Tam giác bằng nhau",
           5: "V. Thu thập và biểu diễn dữ liệu", 6: "VI. Tỉ lệ thức, dãy tỉ số bằng nhau", 0: "Vận dụng cao tổng hợp"}
    s = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\\begin{tabular}{|l|c|c|c|c|c|}\\hline\n"
         "\\textbf{Chương (KNTT)} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{VDC} & \\textbf{Tổng} \\\\ \\hline\n")
    for c in ch:
        s += ten[c] + " & " + " & ".join(d(t[c][m]) if t[c][m] else "--" for m in M) + f" & \\textbf{{{d(sum(t[c].values()))}}} \\\\ \\hline\n"
    tm = {m: sum(t[c][m] for c in ch) for m in M}
    s += "\\textbf{Tổng điểm} & " + " & ".join(f"\\textbf{{{d(tm[m])}}}" for m in M) + " & \\textbf{10,0} \\\\ \\hline\n"
    s += "\\textbf{Tỉ lệ} & " + " & ".join(f"{round(tm[m] * 10)}\\%" for m in M) + " & 100\\% \\\\ \\hline\n\\end{tabular}\\end{center}"
    return s


PHAM_VI_TXT = ("\\textbf{Phạm vi:} Chương I--V và Chương VI bài 20--21 (tỉ lệ thức, dãy tỉ số bằng nhau) SGK Toán 7 KNTT, theo tiến độ trung tâm. "
               "KHÔNG ra đại lượng tỉ lệ thuận, tỉ lệ nghịch (học giữa kì II) và hình hộp, lăng trụ (học cuối kì II), dù nhiều trường Hà Nội có ra.")
NGUON_TXT = "30 đề cuối kì I Toán 7 của các trường, phòng GD Hà Nội năm học 2024--2025 và 2025--2026"
KHUNG_ON = ("\\textbf{Khung đề ôn} (phủ ĐỦ 22 dạng có thể ra trong " + NGUON_TXT + "): Phần I trắc nghiệm 12 câu (3,0đ), mỗi câu "
            "một dạng nhận biết/thông hiểu: số hữu tỉ, luỹ thừa, làm tròn -- số thập phân, căn bậc hai -- số vô tỉ, góc, song song, "
            "tổng ba góc, nhận biết tam giác bằng nhau, tam giác cân -- trung trực, dữ liệu, biểu đồ quạt, biểu đồ đoạn thẳng · "
            "Bài 1 phép tính (1,0đ) · Bài 2 tìm $x$ gồm chuyển vế, luỹ thừa, giá trị tuyệt đối (1,5đ) · Bài 3 bài toán thực tế "
            "hoặc biểu đồ (0,75đ) · Bài 4 chia theo tỉ lệ (1,0đ) · Bài 5 song song (1,0đ) · Bài 6 tam giác bằng nhau (1,25đ) · "
            "Bài 7 vận dụng cao (0,5đ) -- CHỈ 2 dạng ra nhiều nhất: tỉ lệ thức nâng cao, đẳng thức, bài suy luận (63\\% đề) và "
            "giá trị lớn nhất, nhỏ nhất có $|x|$, luỹ thừa chẵn (20\\% đề).")
KHUNG_CT = ("\\textbf{Khung đề chính thức} (chốt từ " + NGUON_TXT + "; mỗi câu chỉ lấy 1--3 dạng hay ra nhất ở đúng vị trí đó): "
            "Phần I trắc nghiệm 8 câu (2,0đ): căn bậc hai -- số vô tỉ (2 câu; 83\\% đề), làm tròn -- số thập phân (56\\%), "
            "giá trị tuyệt đối (90\\%), góc kề bù -- đối đỉnh (63\\%), song song (66\\%), tỉ lệ thức (66\\%), tam giác bằng nhau · "
            "Bài 1 phép tính: cộng trừ nhân chia, thứ tự phép tính (1,5đ; 96\\% và 90\\% đề) · Bài 2 tìm $x$: chuyển vế, giá trị "
            "tuyệt đối (1,5đ; 93\\% và 90\\%) · Bài 3 chia theo tỉ lệ (1,5đ; 66\\%) · Bài 4 chứng minh song song, tính góc "
            "(1,5đ; 80\\%) · Bài 5 tam giác bằng nhau (1,5đ) · Bài 6 vận dụng cao (0,5đ): tỉ lệ thức nâng cao/bài suy luận (63\\%) "
            "hoặc giá trị lớn nhất, nhỏ nhất (20\\%).")


def mt_json(D):
    rows = hang_mt(D)
    n = len(D["tn"])
    if D["loai"] == "on":
        vai = KHUNG_ON + BR + "\\textbf{Vai trò:} đề ÔN TẬP -- học sinh gặp đủ mọi dạng có thể ra; lỡ một buổi vẫn gặp đủ dạng ở đề ôn khác."
    else:
        vai = KHUNG_CT + BR + ("\\textbf{Vai trò:} đề KIỂM TRA CHÍNH THỨC -- chỉ các dạng hay ra nhất; "
                              "mọi câu lấy từ đề trường KHÔNG dùng trong 3 đề ôn.")
    s1 = [dict(type="para", text=vai + BR + PHAM_VI_TXT),
          dict(type="para", text=f"\\textbf{{MA TRẬN {ten_de(D).upper()} -- CUỐI HỌC KÌ I TOÁN 7 (90 phút)}}" + BR + bang_mt(rows)),
          dict(type="para", text="\\textbf{TỔNG HỢP THEO CHƯƠNG VÀ MỨC ĐỘ (điểm)}" + BR + bang_tong(rows))]
    s2 = [dict(type="para", text=f"\\textbf{{ĐÁP ÁN PHẦN I. TRẮC NGHIỆM ({d(n * 0.25)} điểm)}} -- mỗi câu đúng 0,25 điểm."),
          dict(type="para", text="\\begin{center}\\small\\begin{tabular}{|" + "c|" * n + "}\\hline "
               + " & ".join(f"\\textbf{{{i}}}" for i in range(1, n + 1)) + r" \\ \hline "
               + " & ".join(c["dap"] for c in D["tn"]) + r" \\ \hline\end{tabular}\end{center}"),
          dict(type="para", text=BR.join(f"\\textbf{{Câu {i} -- {c['dap']}.}} {c['giai']}" for i, c in enumerate(D["tn"], 1)))]
    stages = [dict(kind="review", number=1, title=f"Ma trận {ten_de(D).lower()}", blocks=s1),
              dict(kind="concept", number=2, title="Đáp án Phần I", blocks=s2)]
    B = D["bai"]
    k = len(B)
    nhom = [list(range(0, k - 3)), list(range(k - 3, k - 1)), [k - 1]]
    for j, idx in enumerate(nhom):
        bl = []
        for i in idx:
            b = B[i]
            bl.append(dict(type="para", text=f"\\textbf{{BÀI {b['so']} ({d(sum(yy['diem'] for yy in b['ys']))} điểm).}}"))
            bl.append(dict(type="para", text=loi_giai_bai(b)))
        if j == 2:
            bl.append(dict(type="para", text="\\textbf{Tổng: 10,0 điểm.} Học sinh làm cách khác đúng vẫn cho điểm tối đa từng phần. "
                                            "Điểm toàn bài làm tròn đến một chữ số thập phân."))
        tit = "Đáp án Bài " + ", ".join(str(B[i]["so"]) for i in idx)
        stages.append(dict(kind=["practice1", "practice2", "reflection"][j], number=3 + j, title=tit, blocks=bl))
    return dict(slug=slug(D, True), title=f"Ma trận đề và đáp án chi tiết — {ten_de(D)}",
                eyebrow="TÀI LIỆU GIÁO VIÊN • LỚP 7 • " + ten_de(D).upper(), grade_label="Lớp 7", class_tier="",
                theme="de_thi", trinh_bay="thoang", stages=stages)


def main():
    DS = [dung_de(D, i) for i, D in enumerate(BO)]
    loi = kiem(DS)
    for x in loi:
        print("✗", x)
    if loi:
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    for D in DS:
        (OUT / f"{slug(D)}.json").write_text(json.dumps(de_json(D), ensure_ascii=False, indent=1), encoding="utf-8")
        (OUT / f"{slug(D, True)}.json").write_text(json.dumps(mt_json(D), ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {D['ten']}")
    print(f"✓ ghi {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
