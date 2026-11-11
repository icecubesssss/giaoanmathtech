#!/usr/bin/env python3
r"""BỘ ĐỀ CUỐI HỌC KÌ I TOÁN 6 (KNTT, Hà Nội): 3 ĐỀ ÔN TẬP + 3 ĐỀ CHÍNH THỨC, mỗi đề kèm MA TRẬN + ĐÁP ÁN.

Thầy giao 11/11/2026: "3 đề ôn tập và 3 đề CKI chính thức" lớp 6; chỉ ĐỀ THI Hà Nội năm học 2025-2026,
bám tiến độ KNTT (Kì I = Chương I–V). Quy trình: docs/quy-trinh-bo-de-on-tap.md.

Ngân hàng: 15 đề CK1 Toán 6 Hà Nội 2025-2026 đã bóc từng ý (đọc ảnh) ở
inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi/ — phân dạng trên Sheets (scripts/lop6_ck1_phan_dang.py).
MỌI câu trỏ `mã-đề#câu` về bản ghi; script chặn câu dùng hai lần trong cả bộ 6 đề.

KHUNG (chốt từ thống kê 15 đề — 12/15 đề có TN 2đ; 15/15 có bài hình thực tế; 15/15 có câu VDC 0,5đ):
  Phần I  Trắc nghiệm 8 câu × 0,25 = 2,0đ (Ch.I–V)
  Bài 1   Thực hiện phép tính 4 ý × 0,5 = 2,0đ   (D12 cộng trừ hợp lí, D13 phân phối, D03 biểu thức ngoặc + luỹ thừa)
  Bài 2   Tìm x 3 ý × 0,5 = 1,5đ                  (D14, D15/D04/D08)
  Bài 3   Bài toán thực tế BCNN / ƯCLN 1,5đ        (D10 60% đề, D09 40% đề)
  Bài 4   Bài toán thực tế chu vi – diện tích 2,5đ (D22 100% đề)
  Bài 5   Vận dụng cao 0,5đ
Đề ôn 1, 2: dạng tần suất cao nhất, bốc nguyên văn; Đề ôn 3: dạng tần suất thứ nhì (luỹ thừa, ƯCLN, ước số nguyên);
Đề chính thức: câu CHƯA dùng ở đề ôn, cùng khung.

    .venv/bin/python scripts/de_ck1_lop6.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "inputs/seeds/lop-6/de-cuoi-ki-1"
BG = ROOT / "inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi"
BR = " [[br]] "
NAM = "Năm học 2026 -- 2027"

_MOI = {f.stem.split("-")[-1] for f in BG.glob("l6-ck1-2526-*.json")}
BANK = {f.stem.split("-")[-1] + ("24" if "-2425-" in f.stem and f.stem.split("-")[-1] in _MOI else ""):
        json.loads(f.read_text(encoding="utf-8")) for f in BG.glob("l6-ck1-*.json")}
# đề 2024-2025 trùng tên trường với 2025-2026 (Ngô Sĩ Liên, Ngọc Lâm, Phúc Đồng) thêm hậu tố "24"
QUAN = {"lyson": "Long Biên", "ngocthuy": "Long Biên", "ngoclam": "Long Biên", "aimo": "Long Biên",
        "ngogiatu": "Long Biên", "giangbien": "Long Biên", "nguyenbinhkhiem": "Long Biên", "phucdong": "Long Biên",
        "ngosilien": "Hoàn Kiếm", "tantrieu": "Thanh Trì", "dongocdu": "Thanh Trì", "lengochan": "Hai Bà Trưng",
        "donganh": "Đông Anh", "hatmon": "Phúc Thọ", "cum14": "Cụm CM số 14",
        "chuongmy": "Chương Mỹ", "quocoai": "Quốc Oai", "phandinhgiot": "Thanh Xuân", "ngosilien24": "Hoàn Kiếm",
        "banmai": "Ban Mai School", "phucdien": "Bắc Từ Liêm", "lomonoxop": "Nam Từ Liêm", "ngoclam24": "Long Biên",
        "phucdong24": "Long Biên"}
LA_MA = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
DA_DUNG: dict[str, str] = {}


def cau(ref):
    de, c = ref.split("#")
    return next(x for x in BANK[de]["cau"] if x["cau"] == c)


def nguon(ref, ghi=""):
    de, c = ref.split("#")
    ten = BANK[de]["truong"].replace("&", "\\&")  # "Phòng GD&ĐT" làm vỡ bảng tabular nếu không escape
    return f"{ten} ({QUAN[de]}, {BANK[de]['nam_hoc']}), câu {c}" + (f" -- {ghi}" if ghi else "")


def d(x):
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def dung(ref, o):
    cau(ref)  # ném lỗi nếu không có trong ngân hàng
    if ref in DA_DUNG:
        sys.exit(f"✗ {ref} dùng hai lần: {DA_DUNG[ref]} và {o}")
    DA_DUNG[ref] = o


# ------------------------------------------------------------------ dựng câu
def T(ref, stem, opts, dap, giai, nd, ghi=""):
    return dict(ref=ref, stem=stem, opts=opts, dap=dap, giai=giai, nd=nd, ghi=ghi)


def Y(nhan, diem, de, steps, ref, nd, phut, ghi=""):
    """Một ý tự luận. steps: list (văn bản, điểm) hoặc văn bản không điểm."""
    return dict(nhan=nhan, diem=diem, de=de, steps=steps, ref=ref, nd=nd, phut=phut, ghi=ghi)


def B(so, ten, mo, ys, hinh=None, note="", hinh_pos="right", hinh_w="0.40"):
    return dict(so=so, ten=ten, mo=mo, ys=ys, hinh=hinh, note=note, pos=hinh_pos, w=hinh_w)


def buoc(steps):
    out = []
    for s in steps:
        if isinstance(s, tuple):
            out.append(f"{s[0]} \\hfill \\textit{{({d(s[1])}đ)}}")
        else:
            out.append(s)
    return BR.join(out)


def diem_steps(steps):
    return round(sum(s[1] for s in steps if isinstance(s, tuple)), 2)


# ------------------------------------------------------------------ hình (TikZ)
def hinh_4_hinh():  # Tân Triều I.8: HBH, hình tròn, hình thang cân, HCN
    return (r"\begin{tikzpicture}[scale=0.48,line width=0.7pt]"
            r"\draw (0,0)--(2.2,0)--(2.9,1.5)--(0.7,1.5)--cycle;\node at (1.45,-0.45){\small (1)};"
            r"\draw (4.6,0.75) circle (0.85);\node at (4.6,-0.45){\small (2)};"
            r"\draw (6.4,0)--(8.6,0)--(8.1,1.5)--(6.9,1.5)--cycle;\node at (7.5,-0.45){\small (3)};"
            r"\draw (9.8,0)--(11.6,0)--(11.6,1.5)--(9.8,1.5)--cycle;\node at (10.7,-0.45){\small (4)};"
            r"\end{tikzpicture}")


def hinh_san_truong():  # Tân Triều II.4
    s = r"\begin{tikzpicture}[scale=0.1,line width=0.7pt]\draw (0,0) rectangle (30,20);"
    for x, y in ((5, 12), (21, 12), (5, 3), (21, 3)):
        s += rf"\draw[fill=green!12] ({x},{y}) rectangle ({x + 4},{y + 4});\node[font=\tiny] at ({x + 2},{y + 2}){{Hoa}};"
    return s + (r"\draw[<->] (0,21.5)--(30,21.5) node[midway,above]{\small $30$ m};"
                r"\draw[<->] (31.5,0)--(31.5,20) node[midway,right]{\small $20$ m};\end{tikzpicture}")


def hinh_ba_hinh_thoi():  # Ngô Sĩ Liên II.4
    s = r"\begin{tikzpicture}[scale=0.32,line width=0.7pt]\draw (0,0) rectangle (18,4);"
    for k in range(3):
        x = 6 * k
        s += rf"\draw[fill=green!15] ({x},2)--({x + 3},4)--({x + 6},2)--({x + 3},0)--cycle;"
    return s + (r"\draw[<->] (0,4.8)--(18,4.8) node[midway,above]{\small $18$ m};"
                r"\draw[<->] (18.8,0)--(18.8,4) node[midway,right]{\small $4$ m};\end{tikzpicture}")


def hinh_thang_can_dong_anh():  # Đông Anh Bài 5
    return (r"\begin{tikzpicture}[scale=0.1,line width=0.7pt]"
            r"\fill[gray!35] (0,0)--(7,0)--(7,24)--cycle;\fill[gray!35] (37,0)--(44,0)--(37,24)--cycle;"
            r"\draw (0,0)--(44,0)--(37,24)--(7,24)--cycle;\draw (7,24)--(7,0);\draw (37,24)--(37,0);"
            r"\draw (7,0) rectangle +(1.6,1.6);\draw (37,0) rectangle +(-1.6,1.6);"
            r"\node[above left] at (7,24){$A$};\node[above right] at (37,24){$B$};"
            r"\node[below] at (37,0){$C$};\node[below] at (7,0){$D$};"
            r"\node[below left] at (0,0){$F$};\node[below right] at (44,0){$E$};"
            r"\node[above] at (22,24){\small $30$ m};\node[left] at (37,12){\small $24$ m};\end{tikzpicture}")


def hinh_vuon_ao():  # Lê Ngọc Hân II.4: hình thoi ABCD (cạnh 60) + ao hình thang cân ABEF (FH = 40)
    return (r"\begin{tikzpicture}[scale=0.042,line width=0.7pt]"
            r"\draw (0,0)--(60,0)--(30,-52)--(-30,-52)--cycle;"
            r"\draw[fill=cyan!12] (0,0)--(60,0)--(50,40)--(10,40)--cycle;"
            r"\draw[dashed] (10,40)--(10,0);\draw (10,0) rectangle +(3.5,3.5);"
            r"\node[left] at (0,1){$A$};\node[right] at (60,0){$B$};"
            r"\node[below] at (30,-52){$C$};\node[below] at (-30,-52){$D$};"
            r"\node[above] at (10,40){$F$};\node[above] at (50,40){$E$};\node[below] at (10.5,0){$H$};"
            r"\node[left] at (10,20){\small $40$ m};\node[below] at (0,-52){\small $60$ m};\end{tikzpicture}")


def hinh_hbh_aecf():  # Ngọc Lâm II.4: HCN ABCD 36 × 20, HBH AECF với AE = FC = 26
    return (r"\begin{tikzpicture}[scale=0.12,line width=0.7pt]"
            r"\draw (0,0) rectangle (36,20);\draw[fill=cyan!20] (0,20)--(26,20)--(36,0)--(10,0)--cycle;"
            r"\node[above left] at (0,20){$A$};\node[above] at (26,20){$E$};\node[above right] at (36,20){$B$};"
            r"\node[below right] at (36,0){$C$};\node[below] at (10,0){$F$};\node[below left] at (0,0){$D$};"
            r"\draw[<->] (0,23.5)--(26,23.5) node[midway,above]{\small $26$ m};"
            r"\draw[<->] (37.5,0)--(37.5,20) node[midway,right]{\small $20$ m};"
            r"\draw[<->] (0,-3.5)--(36,-3.5) node[midway,below]{\small $36$ m};\end{tikzpicture}")


def hinh_hbh_cum14():  # Cụm 14 II.4: HCN 12 × 10, HBH trồng hoa đáy 6
    return (r"\begin{tikzpicture}[scale=0.3,line width=0.7pt]"
            r"\draw (0,0) rectangle (12,10);\draw[fill=pink!40] (0,10)--(6,10)--(12,0)--(6,0)--cycle;"
            r"\node at (6.1,5){\small Hoa};\node at (2.2,2.5){\small Cỏ};\node at (9.8,7.5){\small Cỏ};"
            r"\draw[<->] (0,10.8)--(6,10.8) node[midway,above]{\small $6$ m};"
            r"\draw[<->] (6,10.8)--(12,10.8) node[midway,above]{\small $6$ m};"
            r"\draw[<->] (0,-0.8)--(6,-0.8) node[midway,below]{\small $6$ m};"
            r"\draw[<->] (6,-0.8)--(12,-0.8) node[midway,below]{\small $6$ m};"
            r"\draw[<->] (-0.8,0)--(-0.8,10) node[midway,left]{\small $10$ m};\end{tikzpicture}")


def hinh_loi_di():  # Quốc Oai 2024-25 Bài 5: vườn 25 × 15, lối đi 2 m dọc cạnh trên và cạnh phải
    return (r"\begin{tikzpicture}[scale=0.17,line width=0.7pt]"
            r"\draw (0,0) rectangle (25,15);\draw[fill=red!10] (0,0) rectangle (23,13);\node at (11.5,6.5){\small Cà chua};"
            r"\draw[<->] (0,16.3)--(25,16.3) node[midway,above]{\small $25$ m};"
            r"\draw[<->] (26.3,0)--(26.3,15) node[midway,right]{\small $15$ m};"
            r"\node[font=\scriptsize] at (1.6,14){$2$ m};\node[font=\scriptsize] at (24,1.4){$2$ m};\end{tikzpicture}")


def bang_nhiet(ten, so, cot="Thành phố", hang="Nhiệt độ"):
    return ("\\par\\begin{center}\\small\\begin{tabular}{|l|" + "c|" * len(ten) + "}\\hline "
            + f"{cot} & " + " & ".join(ten) + r" \\ \hline " + f"{hang} & " + " & ".join(so)
            + r" \\ \hline\end{tabular}\end{center}")


CHIA = r"\,\vdots\,"

# ======================================================================= 6 ĐỀ
DE = {}

# ----------------------------------------------------------------- ĐỀ ÔN TẬP SỐ 1
DE["on1"] = dict(
    loai="on", so=1,
    tn=[
        T("tantrieu#I.1", r"Tập hợp $A=\{x\in\mathbb{Z}\mid -1\le x<4\}$ được viết dưới dạng liệt kê các phần tử là:",
          [r"$A=\{-1;0;1;2;3\}$", r"$A=\{-1;0;1;2;3;4\}$", r"$A=\{0;1;2;3\}$", r"$A=\{-1;1;2;3\}$"], "A",
          r"Các số nguyên $x$ thoả mãn $-1\le x<4$ là $-1;0;1;2;3$.", "Tập hợp: liệt kê phần tử"),
        T("lengochan#I.1", "Số nào sau đây chia hết cho cả $2$ và $5$?", ["$285$", "$282$", "$280$", "$504$"], "C",
          "Số chia hết cho cả $2$ và $5$ có chữ số tận cùng là $0$.", "Dấu hiệu chia hết cho 2, 5"),
        T("ngoclam#I.1", "Trong các số $2;\\ 15;\\ 39;\\ 51$, số nào là số nguyên tố?", ["$2$", "$15$", "$39$", "$51$"], "A",
          r"$15=3\cdot5$; $39=3\cdot13$; $51=3\cdot17$ là hợp số; $2$ là số nguyên tố.", "Số nguyên tố, hợp số"),
        T("cum14#I.1", "Số đối của số $14$ là", ["$-14$", "$14$", "$41$", "$-41$"], "A",
          "Số đối của $14$ là $-14$.", "Số đối"),
        T("lyson#I.1", r"Nhiệt độ buổi sáng của phòng ướp lạnh là $-9^\circ$C. Nhiệt độ buổi chiều của phòng ướp lạnh đó là bao nhiêu, biết nhiệt độ tăng $4^\circ$C so với buổi sáng?",
          [r"$13^\circ$C", r"$-13^\circ$C", r"$5^\circ$C", r"$-5^\circ$C"], "D", r"$-9+4=-5$ ($^\circ$C).", "Thực tế số nguyên (nhiệt độ)"),
        T("lengochan#I.6", r"Cho hình vuông $ABCD$ cạnh bằng $5$ cm. Khẳng định nào dưới đây là đúng?",
          [r"Chu vi của hình vuông là $25\text{ cm}^2$.", r"Các cạnh $AB$ và $AD$ song song.", r"$AC=BD$.", r"$AB=BC=AC$."], "C",
          "Hình vuông có hai đường chéo bằng nhau.", "Tính chất hình vuông"),
        T("ngogiatu#I.7", r"Cho hình bình hành có độ dài đường cao và cạnh đáy tương ứng lần lượt là $6$ cm, $12$ cm. Diện tích của hình bình hành đó là",
          [r"$36\text{ cm}^2$", r"$72\text{ cm}^2$", r"$144\text{ cm}^2$", r"$288\text{ cm}^2$"], "B", r"$S=12\cdot6=72$ (cm$^2$).", "Diện tích hình bình hành"),
        T("tantrieu#I.8", "Hình nào trong các hình sau không có trục đối xứng?" + "\\par\\begin{center}" + hinh_4_hinh() + "\\end{center}",
          ["Hình (1).", "Hình (2).", "Hình (3).", "Hình (4)."], "A",
          "Hình bình hành (1) không có trục đối xứng; hình tròn, hình thang cân, hình chữ nhật đều có.", "Hình có trục đối xứng"),
    ],
    bai=[
        B(1, "Thực hiện phép tính", "Thực hiện phép tính (tính hợp lí nếu có thể):", [
            Y("a", 0.5, r"$(-125)+15+125$", [(r"$=\big[(-125)+125\big]+15$", 0.25), (r"$=0+15=15$.", 0.25)],
              "cum14#II.1a", "Cộng số nguyên, tính hợp lí", 3),
            Y("b", 0.5, r"$(-25)\cdot64+36\cdot(-25)$", [(r"$=(-25)\cdot(64+36)$", 0.25), (r"$=(-25)\cdot100=-2500$.", 0.25)],
              "cum14#II.1b", "Tính chất phân phối", 4),
            Y("c", 0.5, r"$345+58-(145-42+150)$", [(r"$=345+58-145+42-150$", 0.25), (r"$=(345-145)+(58+42)-150=200+100-150=150$.", 0.25)],
              "ngoclam#II.1c", "Quy tắc dấu ngoặc", 4),
            Y("d", 0.5, r"$\{62\cdot5-[13+(10-7)^3]\}:9+2025^0$", [(r"$=\{310-[13+27]\}:9+1$", 0.25), (r"$=270:9+1=30+1=31$.", 0.25)],
              "ngosilien#II.1c", "Biểu thức nhiều tầng ngoặc, luỹ thừa", 6),
        ]),
        B(2, "Tìm x", "Tìm số nguyên $x$, biết:", [
            Y("a", 0.5, r"$x+13=-19$", [(r"$x=-19-13$", 0.25), (r"$x=-32$.", 0.25)], "lengochan#II.2a", "Tìm x một bước", 3),
            Y("b", 0.5, r"$3\cdot(x-9)=45$", [(r"$x-9=45:3=15$", 0.25), (r"$x=24$.", 0.25)], "ngogiatu#II.2b", "Tìm x hai bước", 4),
            Y("c", 0.5, r"$(x+2)(10-5x)=0$", [(r"$x+2=0$ hoặc $10-5x=0$", 0.25), (r"$x=-2$ hoặc $x=2$. Vậy $x\in\{-2;2\}$.", 0.25)],
              "dongocdu#II.2c", "Tích bằng 0", 5),
        ]),
        B(3, "Bài toán BCNN", "Khối 6 của một trường THCS đi tham quan dã ngoại. Nếu chia số học sinh thành các đội sao cho mỗi đội có $12$ bạn, $18$ bạn và $30$ bạn thì đều vừa đủ không thừa bạn nào. Biết số học sinh khối 6 trong khoảng từ $500$ đến $700$ em. Tính số học sinh khối 6 của trường đó đi tham quan dã ngoại.", [
            Y("", 1.5, "", [
                (r"Gọi số học sinh khối 6 là $x$ (học sinh), $x\in\mathbb{N}^*$, $500\le x\le700$.", 0.25),
                (rf"Vì $x{CHIA}12$, $x{CHIA}18$, $x{CHIA}30$ nên $x\in\mathrm{{BC}}(12,18,30)$.", 0.25),
                (r"Ta có $12=2^2\cdot3$; $18=2\cdot3^2$; $30=2\cdot3\cdot5$.", 0.25),
                (r"$\mathrm{BCNN}(12,18,30)=2^2\cdot3^2\cdot5=180$.", 0.25),
                (r"$\mathrm{BC}(12,18,30)=\mathrm{B}(180)=\{0;180;360;540;720;\ldots\}$.", 0.25),
                (r"Mà $500\le x\le700$ nên $x=540$. Vậy khối 6 có $540$ học sinh.", 0.25),
            ], "lengochan#II.3", "Bài toán thực tế BCNN", 12),
        ]),
        B(4, "Chu vi, diện tích", "Một sân trường có dạng hình chữ nhật như hình vẽ, chiều dài $30$ m, chiều rộng $20$ m.", [
            Y("a", 0.75, "Tính chu vi và diện tích sân trường.", [
                (r"Chu vi sân trường là $(30+20)\cdot2=100$ (m).", 0.25),
                (r"Diện tích sân trường là $30\cdot20=600$ (m$^2$).", 0.25),
                (r"Vậy sân trường có chu vi $100$ m, diện tích $600$ m$^2$.", 0.25)], "tantrieu#II.4a", "Chu vi, diện tích HCN", 5),
            Y("b", 0.75, "Nhà trường mới xây thêm bốn bồn hoa hình vuông có cạnh dài $2$ m như hình vẽ. Tính tổng diện tích của bốn bồn hoa.", [
                (r"Diện tích một bồn hoa là $2\cdot2=4$ (m$^2$).", 0.25),
                (r"Tổng diện tích bốn bồn hoa là $4\cdot4=16$ (m$^2$).", 0.25),
                (r"Vậy bốn bồn hoa có tổng diện tích $16$ m$^2$.", 0.25)], "tantrieu#II.4b", "Diện tích hình vuông", 5),
            Y("c", 1.0, "Nhà trường muốn trồng các cây hoa hồng trong bốn bồn hoa. Biết rằng cứ $1$ m$^2$ trồng được một cây hoa hồng và giá tiền một cây hoa hồng là $260\\,000$ đồng. Hỏi nhà trường phải trả bao nhiêu tiền để mua cây?", [
                (r"Cứ $1$ m$^2$ trồng một cây nên số cây hoa hồng cần trồng là $16$ cây.", 0.5),
                (r"Số tiền mua cây là $16\cdot260\,000=4\,160\,000$ (đồng).", 0.25),
                (r"Vậy nhà trường phải trả $4\,160\,000$ đồng.", 0.25)], "tantrieu#II.4c", "Thực tế: chi phí theo diện tích", 8),
        ], hinh=hinh_san_truong(), hinh_w="0.30", note="Câu b: bồn hoa có cạnh 2 m, không lấy kích thước sân."),
        B(5, "Vận dụng cao", r"Cho số tự nhiên $n\ge2$. Chứng minh rằng $2n-3$ và $3n-4$ là hai số nguyên tố cùng nhau.", [
            Y("", 0.5, "", [
                r"Gọi $d=\mathrm{ƯCLN}(2n-3,\,3n-4)$ ($d\in\mathbb{N}^*$).",
                (rf"Khi đó $2n-3{CHIA}d$ và $3n-4{CHIA}d$ nên $3(2n-3){CHIA}d$ và $2(3n-4){CHIA}d$.", 0.25),
                rf"Suy ra $3(2n-3)-2(3n-4){CHIA}d$, tức là $(6n-9)-(6n-8)=-1{CHIA}d$.",
                (r"Do đó $d=1$. Vậy $2n-3$ và $3n-4$ là hai số nguyên tố cùng nhau.", 0.25),
            ], "lyson#II.5", "Chứng minh hai số nguyên tố cùng nhau", 8,
              ghi="đề gốc in “$x\\in\\mathbb N^*$”, sửa thành $n\\ge2$ để hai số là số tự nhiên"),
        ]),
    ],
)

# ----------------------------------------------------------------- ĐỀ ÔN TẬP SỐ 2
DE["on2"] = dict(
    loai="on", so=2,
    tn=[
        T("aimo#I.2", r"Cho tập hợp $A=\{x\in\mathbb{Z}\mid -2<x\le3\}$. Viết tập hợp $A$ bằng cách liệt kê các phần tử.",
          [r"$A=\{-2;-1;0;1;2;3\}$", r"$A=\{-2;-1;0;1;2\}$", r"$A=\{-1;0;1;2\}$", r"$A=\{-1;0;1;2;3\}$"], "D",
          r"Các số nguyên lớn hơn $-2$ và không vượt quá $3$ là $-1;0;1;2;3$.", "Tập hợp: liệt kê phần tử"),
        T("aimo#I.6", r"Để số $\overline{30*}$ chia hết cho cả $2$; $3$ và $9$ thì $*$ bằng:", ["$3$", "$9$", "$6$", "$0$"], "C",
          r"$\overline{30*}$ chẵn và $3+0+*$ chia hết cho $9$ nên $*=6$.", "Dấu hiệu chia hết cho 2, 9"),
        T("phucdong#I.4", "Kết quả phân tích số $60$ ra tích các thừa số nguyên tố là",
          [r"$6\cdot10$", r"$2\cdot3\cdot5$", r"$12\cdot5$", r"$2^2\cdot3\cdot5$"], "D", r"$60=2^2\cdot3\cdot5$.", "Phân tích ra thừa số nguyên tố"),
        T("dongocdu#I.1", r"Sắp xếp các số $-21;\ 8;\ 0;\ -19;\ 5;\ -3;\ 1$ theo thứ tự giảm dần ta được thứ tự đúng là:",
          [r"$8;5;1;0;-3;-19;-21$", r"$-21;-19;-3;0;1;5;8$", r"$0;1;5;8;-21;-19;-3$", r"$-3;-19;-21;0;1;5;8$"], "A",
          "Số dương lớn hơn $0$, lớn hơn mọi số âm; trong hai số âm, số nào có số đối lớn hơn thì nhỏ hơn.", "Sắp thứ tự số nguyên"),
        T("tantrieu#I.6", r"Tổng các số nguyên $x$ thoả mãn $-6<x<5$ là:", ["$0$", "$-6$", "$-5$", "$5$"], "C",
          r"$x\in\{-5;-4;\ldots;4\}$; tổng $=-5+[(-4)+4]+\ldots+[(-1)+1]+0=-5$.", "Tổng các số nguyên trong khoảng"),
        T("giangbien#I.6", "Chọn câu trả lời \\textbf{sai} trong các câu sau:",
          ["Hình vuông có hai đường chéo bằng nhau.", "Hình tam giác đều có ba cạnh bằng nhau.",
           "Hình bình hành có hai đường chéo bằng nhau.", "Hình thoi có bốn cạnh bằng nhau."], "C",
          "Hình bình hành có hai đường chéo cắt nhau tại trung điểm mỗi đường, nhưng nói chung không bằng nhau.", "Tính chất các hình"),
        T("lengochan#I.7", r"Hình chữ nhật có chu vi là $120$ cm và chiều dài là $40$ cm. Vậy chiều rộng của hình chữ nhật có số đo là:",
          ["$80$ cm", "$40$ cm", "$30$ cm", "$20$ cm"], "D", r"Nửa chu vi $60$ cm; chiều rộng $60-40=20$ (cm).", "Chu vi HCN"),
        T("ngosilien#I.2", "Cho các chữ cái sau: \\textsf{H}, \\textsf{M}, \\textsf{Z}, \\textsf{E}. Chữ cái không có trục đối xứng là:",
          ["Chữ \\textsf{H}", "Chữ \\textsf{M}", "Chữ \\textsf{Z}", "Chữ \\textsf{E}"], "C",
          "Chữ Z chỉ có tâm đối xứng, không có trục đối xứng.", "Trục đối xứng"),
    ],
    bai=[
        B(1, "Thực hiện phép tính", "Thực hiện phép tính (tính hợp lí nếu có thể):", [
            Y("a", 0.5, r"$(-238)+476+(-162)+(-176)$", [(r"$=\big[(-238)+(-162)\big]+\big[476+(-176)\big]$", 0.25), (r"$=(-400)+300=-100$.", 0.25)],
              "dongocdu#II.1b", "Cộng số nguyên, tính hợp lí", 4),
            Y("b", 0.5, r"$63\cdot79+79\cdot38-79$", [(r"$=79\cdot(63+38-1)$", 0.25), (r"$=79\cdot100=7900$.", 0.25)],
              "ngocthuy#1c", "Tính chất phân phối", 4),
            Y("c", 0.5, r"$65\cdot37+65\cdot63-4^3\cdot10^2$", [(r"$=65\cdot(37+63)-64\cdot100$", 0.25), (r"$=6500-6400=100$.", 0.25)],
              "lengochan#II.1c", "Phân phối + luỹ thừa", 5),
            Y("d", 0.5, r"$120-\{17+[3^2\cdot2:(10-2^5:2^3)]\}$", [(r"$=120-\{17+[9\cdot2:(10-4)]\}$", 0.25), (r"$=120-\{17+18:6\}=120-20=100$.", 0.25)],
              "tantrieu#II.1c", "Biểu thức nhiều tầng ngoặc, luỹ thừa", 6),
        ]),
        B(2, "Tìm x", "Tìm số nguyên $x$, biết:", [
            Y("a", 0.5, r"$(x-3)-12=25$", [(r"$x-3=25+12=37$", 0.25), (r"$x=40$.", 0.25)], "donganh#2a", "Tìm x hai bước", 3),
            Y("b", 0.5, r"$100-2\cdot(1-x)=16$", [(r"$2\cdot(1-x)=84$", 0.25), (r"$1-x=42$, suy ra $x=-41$.", 0.25)], "dongocdu#II.2b", "Tìm x nhiều bước", 5),
            Y("c", 0.5, r"$2^{x+3}\cdot2^2=2^2\cdot3+20$", [(r"$2^{x+5}=12+20=32=2^5$", 0.25), (r"$x+5=5$, suy ra $x=0$.", 0.25)],
              "lengochan#II.2c", "Tìm x ở số mũ", 6),
        ]),
        B(3, "Bài toán BCNN", "Học sinh của một trường THCS đồng diễn thể dục thể thao. Biết số học sinh của trường khi xếp thành $12$ hàng, $18$ hàng, $28$ hàng đều vừa đủ. Hỏi trường đó có bao nhiêu học sinh? Biết số học sinh trong khoảng từ $500$ đến $600$ em.", [
            Y("", 1.5, "", [
                (r"Gọi số học sinh của trường là $x$ (học sinh), $x\in\mathbb{N}^*$, $500\le x\le600$.", 0.25),
                (rf"Vì $x{CHIA}12$, $x{CHIA}18$, $x{CHIA}28$ nên $x\in\mathrm{{BC}}(12,18,28)$.", 0.25),
                (r"Ta có $12=2^2\cdot3$; $18=2\cdot3^2$; $28=2^2\cdot7$.", 0.25),
                (r"$\mathrm{BCNN}(12,18,28)=2^2\cdot3^2\cdot7=252$.", 0.25),
                (r"$\mathrm{BC}(12,18,28)=\mathrm{B}(252)=\{0;252;504;756;\ldots\}$.", 0.25),
                (r"Mà $500\le x\le600$ nên $x=504$. Vậy trường có $504$ học sinh.", 0.25),
            ], "donganh#4.1", "Bài toán thực tế BCNN", 12),
        ]),
        B(4, "Chu vi, diện tích", "Sân vườn nhà bạn Dũng có dạng hình chữ nhật với chiều rộng $4$ m, chiều dài $18$ m (hình minh hoạ).", [
            Y("a", 0.75, "Tính chu vi và diện tích sân vườn.", [
                (r"Chu vi sân vườn là $(18+4)\cdot2=44$ (m).", 0.25),
                (r"Diện tích sân vườn là $18\cdot4=72$ (m$^2$).", 0.25),
                (r"Vậy sân vườn có chu vi $44$ m, diện tích $72$ m$^2$.", 0.25)], "ngosilien#II.4a", "Chu vi, diện tích HCN", 5),
            Y("b", 1.0, "Trong sân vườn, bố Dũng thiết kế ba khu trồng cỏ dạng hình thoi có kích thước như nhau (như hình vẽ). Tính diện tích một khu trồng cỏ.", [
                (r"Ba hình thoi xếp liền nhau theo chiều dài nên mỗi hình thoi có một đường chéo dài $18:3=6$ (m).", 0.5),
                (r"Đường chéo còn lại bằng chiều rộng sân, dài $4$ m.", 0.25),
                (r"Diện tích một khu trồng cỏ là $6\cdot4:2=12$ (m$^2$).", 0.25)], "ngosilien#II.4b", "Diện tích hình thoi (đọc hình)", 9),
            Y("c", 0.75, "Biết chi phí trồng mỗi mét vuông cỏ là $120\\,000$ đồng. Tính số tiền bố Dũng phải trả để trồng cỏ cho cả ba khu.", [
                (r"Diện tích ba khu trồng cỏ là $12\cdot3=36$ (m$^2$).", 0.25),
                (r"Số tiền trồng cỏ là $36\cdot120\,000=4\,320\,000$ (đồng).", 0.25),
                (r"Vậy bố Dũng phải trả $4\,320\,000$ đồng.", 0.25)], "ngosilien#II.4c", "Thực tế: chi phí theo diện tích", 6),
        ], hinh=hinh_ba_hinh_thoi(), hinh_pos="below", hinh_w="0.62",
          note="Câu b: HS phải đọc hình để thấy đường chéo $18:3$ m và $4$ m; ghi thiếu lập luận đường chéo trừ $0{,}25$đ."),
        B(5, "Vận dụng cao", r"Tìm các số nguyên $x$, $y$ biết: $2xy-4x+y=14$.", [
            Y("", 0.5, "", [
                r"$2xy-4x+y-2=12$",
                r"$2x(y-2)+(y-2)=12$",
                (r"$(2x+1)(y-2)=12$.", 0.25),
                r"Vì $2x+1$ là số lẻ nên $2x+1\in\{1;-1;3;-3\}$, ta có bảng:"
                r" \par\begin{center}\begin{tabular}{|c|c|c|c|c|}\hline $2x+1$ & $1$ & $-1$ & $3$ & $-3$ \\ \hline $y-2$ & $12$ & $-12$ & $4$ & $-4$ \\ \hline $x$ & $0$ & $-1$ & $1$ & $-2$ \\ \hline $y$ & $14$ & $-10$ & $6$ & $-2$ \\ \hline\end{tabular}\end{center}",
                (r"Vậy $(x;y)\in\{(0;14);(-1;-10);(1;6);(-2;-2)\}$.", 0.25),
            ], "tantrieu#II.5", "Tìm x, y nguyên (đưa về tích)", 8),
        ]),
    ],
)

# ----------------------------------------------------------------- ĐỀ ÔN TẬP SỐ 3
DE["on3"] = dict(
    loai="on", so=3,
    tn=[
        T("phucdien#I.2", r"Kết quả của phép tính $13^6:13^2$ là", [r"$13^4$", r"$13^3$", r"$13^{12}$", r"$13^8$"], "A",
          r"$13^6:13^2=13^{6-2}=13^4$.", "Chia hai luỹ thừa cùng cơ số"),
        T("phucdong#I.5", r"Cho $a=2^4\cdot3$; $b=2\cdot3\cdot7$. Khi đó $\mathrm{ƯCLN}(a,b)$ bằng",
          [r"$2\cdot3$", r"$2^4\cdot3$", r"$2\cdot3\cdot7$", r"$2^4\cdot3\cdot7$"], "A", "Lấy thừa số chung $2$, $3$ với số mũ nhỏ nhất.", "ƯCLN"),
        T("ngogiatu#I.3", "Trong các số sau, số nào là bội chung của $2$ và $3$?", ["$40$", "$60$", "$21$", "$45$"], "B",
          "$60$ chia hết cho cả $2$ và $3$.", "Bội chung"),
        T("hatmon#I.5", r"Trên tập hợp số nguyên $\mathbb{Z}$, các ước của $7$ là",
          ["$1;\\,-1;\\,7;\\,-7$", "$1;\\,7$", "$-1;\\,-7$", "$7;\\,-7$"], "A", "Ước của $7$ trong $\\mathbb Z$ gồm $\\pm1$, $\\pm7$.", "Ước số nguyên"),
        T("lengochan#I.5", "Trong các khẳng định sau, khẳng định \\textbf{sai} là:",
          ["Số đối của $0$ là $0$.", "Số lớn nhất có hai chữ số chia hết cho $5$ là $95$.", "Số nguyên âm lớn nhất là $-1$.",
           "Số nguyên âm nhỏ nhất có hai chữ số là $-10$."], "D", "Số nguyên âm nhỏ nhất có hai chữ số là $-99$.", "Số nguyên âm, số đối"),
        T("nguyenbinhkhiem#I.6", "Trong hình chữ nhật thì:",
          ["Hai đường chéo song song.", "Hai đường chéo song song và cắt nhau tại trung điểm của mỗi đường.",
           "Hai đường chéo vuông góc với nhau.", "Hai đường chéo bằng nhau và cắt nhau tại trung điểm của mỗi đường."], "D",
          "Tính chất hai đường chéo của hình chữ nhật.", "Tính chất HCN", ),
        T("lomonoxop#I.8", "Một hình thoi có độ dài hai đường chéo là $30$ cm và $20$ cm. Diện tích hình thoi đó là:",
          [r"$600\text{ cm}^2$", r"$300\text{ cm}^2$", r"$1200\text{ cm}^2$", r"$50\text{ cm}^2$"], "B", r"$S=30\cdot20:2=300$ (cm$^2$).", "Diện tích hình thoi"),
        T("aimo#I.8", "Trong các chữ cái \\textsf{H}, \\textsf{M}, \\textsf{N}, \\textsf{X}, chữ cái nào có tâm đối xứng?",
          ["Chữ \\textsf{H}, \\textsf{X}.", "Chữ \\textsf{H}, \\textsf{N}, \\textsf{X}.", "Chữ \\textsf{H}, \\textsf{M}, \\textsf{N}, \\textsf{X}.",
           "Chữ \\textsf{M}, \\textsf{N}, \\textsf{X}."], "B", "Chữ M không có tâm đối xứng; H, N, X có.", "Tâm đối xứng"),
    ],
    bai=[
        B(1, "Thực hiện phép tính", "Thực hiện phép tính (tính hợp lí nếu có thể):", [
            Y("a", 0.5, r"$58\cdot19+58\cdot(-119)$", [(r"$=58\cdot(19-119)$", 0.25), (r"$=58\cdot(-100)=-5800$.", 0.25)],
              "hatmon#II.1b", "Tính chất phân phối", 4),
            Y("b", 0.5, r"$47\cdot69-31\cdot(-47)$", [(r"$=47\cdot69+31\cdot47$", 0.25), (r"$=47\cdot(69+31)=4700$.", 0.25)],
              "donganh#3c", "Phân phối với số âm", 4),
            Y("c", 0.5, r"$5\cdot2^3-4^5:4^3+81:3^2$", [(r"$=5\cdot8-4^2+81:9$", 0.25), (r"$=40-16+9=33$.", 0.25)],
              "aimo#II.1c", "Thứ tự phép tính có luỹ thừa", 4),
            Y("d", 0.5, r"$143-[68+8\cdot(27-25)^2]$", [(r"$=143-[68+8\cdot2^2]=143-[68+32]$", 0.25), (r"$=143-100=43$.", 0.25)],
              "lomonoxop#II.1.2", "Biểu thức có ngoặc, luỹ thừa", 5),
        ]),
        B(2, "Tìm x", "Tìm số tự nhiên $x$, biết:", [
            Y("a", 0.5, r"$80:2^x-70=-30$", [(r"$80:2^x=40$", 0.25), (r"$2^x=2$, suy ra $x=1$.", 0.25)], "ngosilien#II.2.2a", "Tìm x ở số mũ", 5),
            Y("b", 0.5, r"$5^x\cdot7+5^x=1000$", [(r"$5^x\cdot(7+1)=1000$, tức là $5^x\cdot8=1000$", 0.25),
                                             (r"$5^x=125=5^3$, suy ra $x=3$.", 0.25)], "ngosilien24#II.2c", "Tìm x ở số mũ (mở rộng)", 6),
            Y("c", 0.5, rf"$48{CHIA}x$, $120{CHIA}x$, $168{CHIA}x$ và $x$ lớn nhất", [
                (r"$x=\mathrm{ƯCLN}(48,120,168)$; $48=2^4\cdot3$, $120=2^3\cdot3\cdot5$, $168=2^3\cdot3\cdot7$", 0.25),
                (r"$x=2^3\cdot3=24$.", 0.25)], "donganh#2d", "x là ƯCLN", 5),
        ]),
        B(3, "Bài toán ƯCLN", "Cô Hoa muốn chia $160$ quyển vở, $96$ chiếc bút chì và $192$ chiếc bút bi thành một số phần thưởng như nhau để trao trong dịp tổng kết học kì I. Hỏi cô Hoa có thể chia thành nhiều nhất bao nhiêu phần thưởng? Khi chia được số phần thưởng nhiều nhất thì mỗi phần thưởng có bao nhiêu quyển vở, bao nhiêu bút chì và bao nhiêu bút bi?", [
            Y("", 1.5, "", [
                (r"Gọi số phần thưởng là $x$ (phần), $x\in\mathbb{N}^*$.", 0.25),
                (rf"Vì $160{CHIA}x$, $96{CHIA}x$, $192{CHIA}x$ và $x$ lớn nhất nên $x=\mathrm{{ƯCLN}}(160,96,192)$.", 0.25),
                (r"Ta có $160=2^5\cdot5$; $96=2^5\cdot3$; $192=2^6\cdot3$.", 0.25),
                (r"$\mathrm{ƯCLN}(160,96,192)=2^5=32$, nên chia được nhiều nhất $32$ phần thưởng.", 0.25),
                (r"Mỗi phần thưởng có $160:32=5$ quyển vở; $96:32=3$ bút chì; $192:32=6$ bút bi.", 0.25),
                (r"Vậy chia được nhiều nhất $32$ phần thưởng, mỗi phần gồm $5$ quyển vở, $3$ bút chì, $6$ bút bi.", 0.25),
            ], "hatmon#II.2", "Bài toán thực tế ƯCLN", 12),
        ]),
        B(4, "Chu vi, diện tích", "Một khu đất hình thang cân $ABEF$ (hình bên) có đáy nhỏ $AB=30$ m, chiều cao $BC=24$ m và đáy $EF$ dài hơn đáy $AB$ là $14$ m.", [
            Y("a", 0.5, "Tính độ dài đáy $EF$ của khu đất.", [(r"$EF=30+14=44$ (m).", 0.5)], "donganh#5a", "Độ dài đáy hình thang", 2),
            Y("b", 0.5, "Tính diện tích khu đất hình thang cân đó.", [(r"Diện tích khu đất là $(30+44)\cdot24:2=888$ (m$^2$).", 0.5)],
              "donganh#5b", "Diện tích hình thang cân", 4),
            Y("c", 1.5, "Người ta rào phần đất hình chữ nhật $ABCD$, phần còn lại ở hai bên (phần tô đậm) trồng hoa hướng dương. Tính diện tích đất trồng hoa hướng dương. Nếu mỗi túi hạt giống hoa gieo vừa đủ trên $56$ m$^2$ đất thì cần bao nhiêu túi hạt giống để gieo hết phần đất đó?", [
                (r"Diện tích hình chữ nhật $ABCD$ là $30\cdot24=720$ (m$^2$).", 0.5),
                (r"Diện tích đất trồng hoa hướng dương là $888-720=168$ (m$^2$).", 0.5),
                (r"Số túi hạt giống cần dùng là $168:56=3$ (túi).", 0.25), (r"Vậy cần $3$ túi hạt giống.", 0.25)], "donganh#5c", "Thực tế: diện tích phần còn lại", 12),
        ], hinh=hinh_thang_can_dong_anh(), hinh_w="0.30", note="Câu c: diện tích phần tô đậm = diện tích hình thang trừ diện tích hình chữ nhật."),
        B(5, "Vận dụng cao", r"Cho $A=1+2+2^2+\ldots+2^{2024}+2^{2025}$ và $B=2^{2026}$. Chứng minh rằng $A$ và $B$ là hai số tự nhiên liên tiếp.", [
            Y("", 0.5, "", [
                (r"$2A=2+2^2+2^3+\ldots+2^{2025}+2^{2026}$.", 0.25),
                r"$2A-A=2^{2026}-1$, tức là $A=2^{2026}-1=B-1$.",
                (r"Vậy $A$ và $B$ là hai số tự nhiên liên tiếp.", 0.25),
            ], "cum14#II.5", "Tổng luỹ thừa cùng cơ số", 8),
        ]),
    ],
)

# ----------------------------------------------------------------- ĐỀ CHÍNH THỨC SỐ 1
DE["ct1"] = dict(
    loai="ct", so=1,
    tn=[
        T("ngogiatu#I.1", r"Tập hợp $A=\{x\in\mathbb{Z}\mid -3\le x<1\}$ được viết dưới dạng liệt kê các phần tử là:",
          [r"$A=\{-3;-2;-1;0\}$", r"$A=\{-3;-2;-1;0;1\}$", r"$A=\{-2;-1;0\}$", r"$A=\{-2;-1;0;1\}$"], "A",
          r"Các số nguyên $x$ thoả mãn $-3\le x<1$ là $-3;-2;-1;0$.", "Tập hợp: liệt kê phần tử"),
        T("nguyenbinhkhiem#I.2", "Trong các số sau, số nào chia hết cho $9$?", ["$108$", "$201$", "$512$", "$465$"], "A",
          "$1+0+8=9$ chia hết cho $9$.", "Dấu hiệu chia hết cho 9"),
        T("hatmon#I.3", "Tập hợp nào sau đây chỉ gồm số nguyên tố?",
          [r"$\{2;3;5\}$", r"$\{3;5;6\}$", r"$\{4;5;6\}$", r"$\{8;2;4\}$"], "A", "$4$, $6$, $8$ là hợp số.", "Số nguyên tố"),
        T("hatmon#I.7", "Bảng sau cho biết nhiệt độ của một số thành phố ở cùng một thời điểm:"
          + bang_nhiet(["Hà Nội", "Bắc Kinh", "Moskva", "Washington D.C"], [r"$18^\circ$C", r"$-3^\circ$C", r"$-13^\circ$C", r"$5^\circ$C"])
          + "Thành phố nào có nhiệt độ thấp nhất?", ["Hà Nội", "Bắc Kinh", "Moskva", "Washington D.C"], "C",
          r"$-13<-3<5<18$.", "So sánh số nguyên (thực tế)"),
        T("giangbien#I.5", r"Sắp xếp các số $-15;\ -26;\ 3;\ 0;\ 2025$ theo thứ tự tăng dần là:",
          [r"$-15;-26;3;0;2025$", r"$-15;-26;0;3;2025$", r"$2025;3;0;-15;-26$", r"$-26;-15;0;3;2025$"], "D",
          r"$-26<-15<0<3<2025$.", "Sắp thứ tự số nguyên"),
        T("hatmon#I.9", "Hình vuông có cạnh bằng $3$ cm thì chu vi của nó là", ["$9$ cm", "$6$ cm", "$12$ cm", "$3$ cm"], "C",
          r"$C=4\cdot3=12$ (cm).", "Chu vi hình vuông"),
        T("dongocdu#I.4", r"Một mảnh đất hình vuông có diện tích là $100\text{ m}^2$. Chu vi mảnh đất đó là",
          ["$10$ m", r"$10\text{ m}^2$", "$40$ m", r"$40\text{ m}^2$"], "C", r"Cạnh $10$ m (vì $10\cdot10=100$); chu vi $40$ m.", "Diện tích, cạnh, chu vi"),
        T("dongocdu#I.3", "Số trục đối xứng của hình thoi là:", ["$1$", "$2$", "$3$", "$4$"], "B",
          "Hai đường chéo của hình thoi là hai trục đối xứng.", "Trục đối xứng"),
    ],
    bai=[
        B(1, "Thực hiện phép tính", "Thực hiện phép tính (tính hợp lí nếu có thể):", [
            Y("a", 0.5, r"$-36+95+136+(-95)$", [(r"$=(-36+136)+\big[95+(-95)\big]$", 0.25), (r"$=100+0=100$.", 0.25)],
              "ngogiatu#II.1b", "Cộng số nguyên, tính hợp lí", 3),
            Y("b", 0.5, r"$(-20)\cdot18+(-20)\cdot82+2000$", [(r"$=(-20)\cdot(18+82)+2000$", 0.25), (r"$=-2000+2000=0$.", 0.25)],
              "quocoai#II.1c", "Tính chất phân phối", 4),
            Y("c", 0.5, r"$(55-537)-(463-45)$", [(r"$=55-537-463+45$", 0.25), (r"$=(55+45)-(537+463)=100-1000=-900$.", 0.25)],
              "donganh#3b", "Quy tắc dấu ngoặc", 4),
            Y("d", 0.5, r"$63\cdot27-20\cdot[(30-3^2):3+2^3]$", [(r"$=1701-20\cdot[21:3+8]$", 0.25), (r"$=1701-20\cdot15=1701-300=1401$.", 0.25)],
              "phucdien#II.1c", "Biểu thức có ngoặc, luỹ thừa", 6),
        ]),
        B(2, "Tìm x", "Tìm số nguyên $x$, biết:", [
            Y("a", 0.5, r"$23-x=19$", [(r"$x=23-19$", 0.25), (r"$x=4$.", 0.25)], "phucdong#II.2a", "Tìm x một bước", 3),
            Y("b", 0.5, r"$16:x-2=6$", [(r"$16:x=8$", 0.25), (r"$x=2$.", 0.25)], "cum14#II.2b", "Tìm x hai bước", 4),
            Y("c", 0.5, r"$(x-1)\cdot(3x+6)=0$", [(r"$x-1=0$ hoặc $3x+6=0$", 0.25), (r"$x=1$ hoặc $x=-2$. Vậy $x\in\{1;-2\}$.", 0.25)],
              "cum14#II.2c", "Tích bằng 0", 5),
        ]),
        B(3, "Bài toán BCNN", "Trong một đợt quyên góp sách để ủng hộ các bạn học sinh có hoàn cảnh khó khăn, lớp 6A thu được khoảng từ $150$ đến $200$ quyển sách. Biết rằng khi xếp số sách đó theo từng bó $10$ quyển, $12$ quyển hay $15$ quyển thì đều vừa đủ bó. Hỏi các bạn học sinh lớp 6A đã quyên góp được bao nhiêu quyển sách?", [
            Y("", 1.5, "", [
                (r"Gọi số sách lớp 6A quyên góp được là $x$ (quyển), $x\in\mathbb{N}^*$, $150\le x\le200$.", 0.25),
                (rf"Vì $x{CHIA}10$, $x{CHIA}12$, $x{CHIA}15$ nên $x\in\mathrm{{BC}}(10,12,15)$.", 0.25),
                (r"Ta có $10=2\cdot5$; $12=2^2\cdot3$; $15=3\cdot5$.", 0.25),
                (r"$\mathrm{BCNN}(10,12,15)=2^2\cdot3\cdot5=60$.", 0.25),
                (r"$\mathrm{BC}(10,12,15)=\mathrm{B}(60)=\{0;60;120;180;240;\ldots\}$.", 0.25),
                (r"Mà $150\le x\le200$ nên $x=180$. Vậy lớp 6A quyên góp được $180$ quyển sách.", 0.25),
            ], "cum14#II.3.2", "Bài toán thực tế BCNN", 12),
        ]),
        B(4, "Chu vi, diện tích", "Mảnh vườn nhà bác Nam có dạng hình thoi $ABCD$ với cạnh bằng $60$ m. Ngay bên cạnh, bác Nam đào một cái ao hình thang cân $ABEF$ có chiều cao $FH=40$ m (hình vẽ bên).", [
            Y("a", 0.75, "Tính chu vi của mảnh vườn $ABCD$.", [
                (r"Chu vi mảnh vườn hình thoi $ABCD$ là $60\cdot4=240$ (m).", 0.5),
                (r"Vậy chu vi mảnh vườn là $240$ m.", 0.25)], "lengochan#II.4a", "Chu vi hình thoi", 3),
            Y("b", 1.0, "Biết đáy $EF$ nhỏ hơn đáy lớn $AB$ là $20$ m. Tính diện tích của cái ao $ABEF$.", [
                (r"$AB$ là cạnh hình thoi nên $AB=60$ m.", 0.25),
                (r"Đáy nhỏ $EF=60-20=40$ (m).", 0.25),
                (r"Diện tích cái ao là $(60+40)\cdot40:2=2000$ (m$^2$).", 0.5)], "lengochan#II.4b", "Diện tích hình thang cân", 9),
            Y("c", 0.75, "Biết rằng cứ $2$ m$^2$ mặt nước thu hoạch được $9$ kg cá. Hỏi bác Nam thu hoạch được bao nhiêu ki-lô-gam cá trong ao đó?", [
                (r"Ao có $2000:2=1000$ phần, mỗi phần $2$ m$^2$.", 0.25),
                (r"Số cá thu hoạch được là $1000\cdot9=9000$ (kg).", 0.25),
                (r"Vậy bác Nam thu hoạch được $9000$ kg cá.", 0.25)], "lengochan#II.4c", "Thực tế: sản lượng theo diện tích", 6),
        ], hinh=hinh_vuon_ao(), hinh_w="0.36", note="Câu b: HS phải nhận ra $AB$ vừa là cạnh hình thoi vừa là đáy lớn của ao."),
        B(5, "Vận dụng cao", r"Chứng tỏ rằng với $n$ là số tự nhiên thì $7n+10$ và $5n+7$ là hai số nguyên tố cùng nhau.", [
            Y("", 0.5, "", [
                r"Gọi $d=\mathrm{ƯCLN}(7n+10,\,5n+7)$ ($d\in\mathbb{N}^*$).",
                (rf"Khi đó $5(7n+10){CHIA}d$ và $7(5n+7){CHIA}d$.", 0.25),
                rf"Suy ra $5(7n+10)-7(5n+7){CHIA}d$, tức là $(35n+50)-(35n+49)=1{CHIA}d$, nên $d=1$.",
                (r"Vậy $7n+10$ và $5n+7$ là hai số nguyên tố cùng nhau.", 0.25),
            ], "chuongmy#II.5", "Chứng minh hai số nguyên tố cùng nhau", 8),
        ]),
    ],
)

# ----------------------------------------------------------------- ĐỀ CHÍNH THỨC SỐ 2
DE["ct2"] = dict(
    loai="ct", so=2,
    tn=[
        T("hatmon#I.1", r"Tập hợp $M=\{x\in\mathbb{Z}\mid -1\le x<3\}$ được viết dưới dạng liệt kê là",
          [r"$M=\{-1;0;1;2;3\}$", r"$M=\{-1;0;1;2\}$", r"$M=\{0;1;2;3\}$", r"$M=\{0;1;2\}$"], "B",
          r"Các số nguyên $x$ thoả mãn $-1\le x<3$ là $-1;0;1;2$.", "Tập hợp: liệt kê phần tử"),
        T("tantrieu#I.3", "Số chia hết cho $2$; $3$ và $5$ là:", ["$660$", "$492$", "$601$", "$875$"], "A",
          "$660$ tận cùng $0$ và $6+6+0=12$ chia hết cho $3$.", "Dấu hiệu chia hết cho 2, 3, 5"),
        T("tantrieu#I.4", "Cho các số: $6;\\ 17;\\ 26;\\ 39$, trong đó số nguyên tố là:", ["$6$", "$17$", "$26$", "$39$"], "B",
          r"$6=2\cdot3$; $26=2\cdot13$; $39=3\cdot13$; $17$ chỉ có hai ước.", "Số nguyên tố"),
        T("phucdong#I.2", "Cho biết nhiệt độ nóng chảy của 4 chất như sau:"
          + bang_nhiet(["Oxygen", "Rượu", "Thuỷ ngân", "Chlorine"], [r"$-219^\circ$C", r"$-114^\circ$C", r"$-39^\circ$C", r"$-102^\circ$C"], cot="Chất", hang="Nhiệt độ")
          + "Chất có nhiệt độ nóng chảy \\textbf{thấp nhất} là", ["Oxygen", "Rượu", "Thuỷ ngân", "Chlorine"], "A",
          r"$-219$ là số nhỏ nhất.", "So sánh số nguyên (thực tế)"),
        T("lengochan#I.4", r"Tổng các số nguyên $x$ thoả mãn $-21\le x\le22$ là:", ["$-21$", "$22$", "$0$", "$1$"], "B",
          r"Các cặp số đối từ $-21$ đến $21$ có tổng $0$; còn lại $22$.", "Tổng các số nguyên trong khoảng"),
        T("aimo#I.7", "Khẳng định nào \\textbf{đúng} trong các khẳng định sau?",
          ["Đoạn thẳng có vô số trục đối xứng.", "Hình bình hành là hình có trục đối xứng.",
           "Hình lục giác đều có nhiều trục đối xứng.", "Hình tam giác đều không có trục đối xứng."], "C",
          "Lục giác đều có 6 trục đối xứng.", "Trục đối xứng"),
        T("cum14#I.2", "Tập hợp tất cả các số nguyên là ước của $5$ là:",
          [r"$\{1;5\}$", r"$\{-1;-5\}$", r"$\{0;1;5\}$", r"$\{-1;1;-5;5\}$"], "D", r"Ư$(5)=\{\pm1;\pm5\}$.", "Ước số nguyên"),
        T("tantrieu#I.7", r"Cho hình chữ nhật $ABCD$ có độ dài cạnh $AB=10$ cm, $BC=16$ cm. Chu vi hình chữ nhật $ABCD$ là:",
          ["$26$ cm", r"$52\text{ cm}^2$", "$52$ cm", "$13$ cm"], "C", r"$C=(10+16)\cdot2=52$ (cm).", "Chu vi HCN"),
    ],
    bai=[
        B(1, "Thực hiện phép tính", "Thực hiện phép tính (tính hợp lí nếu có thể):", [
            Y("a", 0.5, r"$(-141)+(-62)+(-38)+141$", [(r"$=\big[(-141)+141\big]+\big[(-62)+(-38)\big]$", 0.25), (r"$=0+(-100)=-100$.", 0.25)],
              "ngosilien#II.1a", "Cộng số nguyên, tính hợp lí", 3),
            Y("b", 0.5, r"$(-57)\cdot84+(-57)\cdot16$", [(r"$=(-57)\cdot(84+16)$", 0.25), (r"$=(-57)\cdot100=-5700$.", 0.25)],
              "tantrieu#II.1b", "Tính chất phân phối", 4),
            Y("c", 0.5, r"$18+50:(-2)-1^{2025}$", [(r"$=18+(-25)-1$", 0.25), (r"$=-7-1=-8$.", 0.25)], "dongocdu#II.1d", "Thứ tự phép tính", 4),
            Y("d", 0.5, r"$500:\{150-[8^2+7\cdot(-2)]\}$", [(r"$=500:\{150-[64+(-14)]\}$", 0.25), (r"$=500:(150-50)=500:100=5$.", 0.25)],
              "cum14#II.1d", "Biểu thức nhiều tầng ngoặc, luỹ thừa", 6),
        ]),
        B(2, "Tìm x", "Tìm số nguyên $x$, biết:", [
            Y("a", 0.5, r"$x-16=10+(-5)$", [(r"$x-16=5$", 0.25), (r"$x=21$.", 0.25)], "ngosilien#II.2.1a", "Tìm x một bước", 3),
            Y("b", 0.5, r"$(x+18)\cdot(-40)=80$", [(r"$x+18=80:(-40)=-2$", 0.25), (r"$x=-20$.", 0.25)], "tantrieu#II.2b", "Tìm x hai bước", 4),
            Y("c", 0.5, r"$(x-3)(2x-8)=0$", [(r"$x-3=0$ hoặc $2x-8=0$", 0.25), (r"$x=3$ hoặc $x=4$. Vậy $x\in\{3;4\}$.", 0.25)],
              "ngoclam#II.2c", "Tích bằng 0", 5),
        ]),
        B(3, "Bài toán ƯCLN", "Nhân dịp kỉ niệm ngày thành lập trường, đội văn nghệ của trường gồm $24$ học sinh khối 6, $36$ học sinh khối 7 và $30$ học sinh khối 8. Ban tổ chức muốn chia toàn bộ đội văn nghệ thành các nhóm hát múa sao cho số học sinh của mỗi khối trong mỗi nhóm là như nhau. Hỏi ban tổ chức có thể chia nhiều nhất bao nhiêu nhóm hát múa? Khi đó, mỗi nhóm có bao nhiêu học sinh khối 6?", [
            Y("", 1.5, "", [
                (r"Gọi số nhóm hát múa có thể chia là $x$ (nhóm), $x\in\mathbb{N}^*$.", 0.25),
                (rf"Theo đề bài $24{CHIA}x$, $36{CHIA}x$, $30{CHIA}x$ và $x$ lớn nhất.", 0.25),
                (r"Suy ra $x=\mathrm{ƯCLN}(24,36,30)$.", 0.25),
                (r"Ta có $24=2^3\cdot3$; $36=2^2\cdot3^2$; $30=2\cdot3\cdot5$ nên $x=2\cdot3=6$.", 0.25),
                (r"Vậy có thể chia nhiều nhất thành $6$ nhóm hát múa.", 0.25),
                (r"Khi đó mỗi nhóm có $24:6=4$ học sinh khối 6.", 0.25),
            ], "ngosilien#II.3", "Bài toán thực tế ƯCLN", 12),
        ]),
        B(4, "Chu vi, diện tích", "Nhà bác Hoa có một mảnh vườn hình chữ nhật có chiều dài $25$ m, chiều rộng $15$ m. Bác làm lối đi rộng $2$ m như hình vẽ. Phần đất còn lại bác Hoa để trồng cà chua.", [
            Y("a", 0.5, "Tính diện tích mảnh vườn.", [(r"Diện tích mảnh vườn là $25\cdot15=375$ (m$^2$).", 0.5)], "quocoai#II.5a", "Diện tích HCN", 3),
            Y("b", 1.0, "Tính diện tích phần vườn trồng cà chua.", [
                (r"Phần trồng cà chua là hình chữ nhật có chiều dài $25-2=23$ (m), chiều rộng $15-2=13$ (m).", 0.5),
                (r"Diện tích phần trồng cà chua là $23\cdot13=299$ (m$^2$).", 0.5)], "quocoai#II.5b", "Diện tích phần còn lại (đọc hình)", 8),
            Y("c", 1.0, "Biết mỗi m$^2$ chi phí trồng cà chua hết $15\\,000$ đồng (gồm tiền cây giống, phân bón và nhân công), mỗi m$^2$ thu hoạch và bán được $25\\,000$ đồng. Tính số tiền lãi bác Hoa thu được từ phần vườn trồng cà chua, biết tiền lãi là hiệu của doanh thu và tổng chi phí.", [
                (r"Mỗi m$^2$ lãi $25\,000-15\,000=10\,000$ (đồng).", 0.5),
                (r"Tiền lãi thu được là $10\,000\cdot299=2\,990\,000$ (đồng).", 0.25),
                (r"Vậy bác Hoa lãi $2\,990\,000$ đồng.", 0.25)], "quocoai#II.5c", "Thực tế: lãi = doanh thu trừ chi phí", 8),
        ], hinh=hinh_loi_di(), note="Câu b: lối đi chạy dọc hai cạnh nên chiều dài, chiều rộng phần trồng cà chua mỗi chiều chỉ bớt $2$ m."),
        B(5, "Vận dụng cao", r"Tìm các cặp số nguyên $(x;y)$ biết: $2xy+x+10y+5=4$.", [
            Y("", 0.5, "", [
                r"$x(2y+1)+5(2y+1)=4$",
                (r"$(x+5)(2y+1)=4$.", 0.25),
                r"Vì $2y+1$ là số lẻ nên $2y+1\in\{1;-1\}$, ta có bảng:"
                r" \par\begin{center}\begin{tabular}{|c|c|c|}\hline $2y+1$ & $1$ & $-1$ \\ \hline $x+5$ & $4$ & $-4$ \\ \hline $y$ & $0$ & $-1$ \\ \hline $x$ & $-1$ & $-9$ \\ \hline\end{tabular}\end{center}",
                (r"Vậy $(x;y)\in\{(-1;0);(-9;-1)\}$.", 0.25),
            ], "hatmon#II.4", "Tìm x, y nguyên (đưa về tích)", 8),
        ]),
    ],
)

# ----------------------------------------------------------------- ĐỀ CHÍNH THỨC SỐ 3
DE["ct3"] = dict(
    loai="ct", so=3,
    tn=[
        T("tantrieu#I.2", r"Thực hiện phép tính $6^{15}:6^5$ ta được kết quả là:", [r"$6^3$", r"$6^{10}$", r"$6^{20}$", r"$10^{20}$"], "B",
          r"$6^{15}:6^5=6^{15-5}=6^{10}$.", "Chia hai luỹ thừa cùng cơ số"),
        T("quocoai#I.4", r"$\mathrm{BCNN}(12,16)$ là:", ["$12$", "$16$", "$0$", "$48$"], "D",
          r"$12=2^2\cdot3$, $16=2^4$ nên $\mathrm{BCNN}(12,16)=2^4\cdot3=48$.", "BCNN"),
        T("phucdong#I.6", "Tập hợp các ước nguyên tố của $12$ là",
          [r"$\{1;2;3;4;6;12\}$", r"$\{1;2;3;4\}$", r"$\{1;2;3\}$", r"$\{2;3\}$"], "D", "Ước nguyên tố của $12$ là $2$ và $3$.", "Ước nguyên tố"),
        T("nguyenbinhkhiem#I.3", "Số đối của $-15$ là:", ["$-15$", r"$-(-15)$", "$15$", "Đáp án B và C đều đúng"], "D",
          r"Số đối của $-15$ là $-(-15)=15$.", "Số đối"),
        T("banmai#I.4", r"Nhiệt độ ở Trái Đất, Sao Thổ, Sao Hoả và Sao Mộc lần lượt là $20^\circ$C; $-140^\circ$C; $-20^\circ$C; $-120^\circ$C. Hành tinh có nhiệt độ thấp nhất là",
          ["Trái Đất.", "Sao Thổ.", "Sao Hoả.", "Sao Mộc."], "B", r"$-140<-120<-20<20$.", "So sánh số nguyên (thực tế)"),
        T("ngoclam#I.4", "So sánh ba số $0$; $3$; $-5$ ta có:", [r"$0<3<-5$", r"$-5<0<3$", r"$3<-5<0$", r"$-5<3<0$"], "B",
          "Số âm nhỏ hơn $0$, $0$ nhỏ hơn số dương.", "So sánh số nguyên"),
        T("ngosilien#I.8", "Diện tích của hình vuông có chu vi bằng $40$ cm là:",
          [r"$40\text{ cm}^2$", r"$100\text{ cm}^2$", r"$160\text{ cm}^2$", r"$1600\text{ cm}^2$"], "B",
          r"Cạnh hình vuông $40:4=10$ (cm); diện tích $10\cdot10=100$ (cm$^2$).", "Chu vi, cạnh, diện tích",
          ghi="đề gốc là câu trả lời ngắn, chuyển sang trắc nghiệm"),
        T("hatmon#I.6", "Trong các chữ cái \\textsf{A}, \\textsf{B}, \\textsf{G}, \\textsf{H}, \\textsf{E}, \\textsf{F}, những chữ cái có trục đối xứng là:",
          ["\\textsf{A}, \\textsf{H}, \\textsf{F}.", "\\textsf{A}, \\textsf{H}, \\textsf{G}.", "\\textsf{B}, \\textsf{F}.",
           "\\textsf{A}, \\textsf{B}, \\textsf{H}, \\textsf{E}."], "D", "G, F không có trục đối xứng.", "Trục đối xứng"),
    ],
    bai=[
        B(1, "Thực hiện phép tính", "Thực hiện phép tính (tính hợp lí nếu có thể):", [
            Y("a", 0.5, r"$(-156)+64+(-44)+236$", [(r"$=\big[(-156)+(-44)\big]+(64+236)$", 0.25), (r"$=(-200)+300=100$.", 0.25)],
              "chuongmy#II.1b", "Cộng số nguyên, tính hợp lí", 3),
            Y("b", 0.5, r"$45+(-128)+55+28$", [(r"$=(45+55)+\big[(-128)+28\big]$", 0.25), (r"$=100+(-100)=0$.", 0.25)],
              "lengochan#II.1a", "Cộng số nguyên, tính hợp lí", 4),
            Y("c", 0.5, r"$37\cdot52+37\cdot48-115$", [(r"$=37\cdot(52+48)-115$", 0.25), (r"$=3700-115=3585$.", 0.25)],
              "chuongmy#II.1a", "Tính chất phân phối", 4),
            Y("d", 0.5, r"$3^5:3^2+(-25)\cdot(-4)$", [(r"$=3^3+100$", 0.25), (r"$=27+100=127$.", 0.25)], "cum14#II.1c", "Luỹ thừa + nhân số nguyên", 5),
        ]),
        B(2, "Tìm x", "Tìm $x$, biết:", [
            Y("a", 0.5, r"$x:2-5=-8$ (với $x\in\mathbb{Z}$)", [(r"$x:2=-8+5=-3$", 0.25), (r"$x=(-3)\cdot2=-6$.", 0.25)],
              "quocoai#II.2b", "Tìm x hai bước", 3),
            Y("b", 0.5, r"$3+9(x-4)=12$ (với $x\in\mathbb{Z}$)", [(r"$9(x-4)=9$", 0.25), (r"$x-4=1$, suy ra $x=5$.", 0.25)], "ngosilien#II.2.1b", "Tìm x hai bước", 4),
            Y("c", 0.5, r"$(x+1)^2=1^3+2^3+3^3$ (với $x\in\mathbb{N}$)", [(r"$(x+1)^2=1+8+27=36=6^2$", 0.25), (r"$x+1=6$, suy ra $x=5$.", 0.25)],
              "ngosilien#II.2.2b", "Tìm x ở cơ số luỹ thừa", 6),
        ]),
        B(3, "Bài toán BCNN", "Số học sinh của một trường THCS tham gia đại hội thể thao có khoảng từ $300$ đến $400$ học sinh. Khi xếp hàng $8$, hàng $10$, hàng $12$ đều vừa đủ. Tính số học sinh của trường tham gia đại hội thể thao.", [
            Y("", 1.5, "", [
                (r"Gọi số học sinh tham gia là $x$ (học sinh), $x\in\mathbb{N}^*$, $300\le x\le400$.", 0.25),
                (rf"Vì $x{CHIA}8$, $x{CHIA}10$, $x{CHIA}12$ nên $x\in\mathrm{{BC}}(8,10,12)$.", 0.25),
                (r"Ta có $8=2^3$; $10=2\cdot5$; $12=2^2\cdot3$.", 0.25),
                (r"$\mathrm{BCNN}(8,10,12)=2^3\cdot3\cdot5=120$.", 0.25),
                (r"$\mathrm{BC}(8,10,12)=\mathrm{B}(120)=\{0;120;240;360;480;\ldots\}$.", 0.25),
                (r"Mà $300\le x\le400$ nên $x=360$. Vậy có $360$ học sinh tham gia.", 0.25),
            ], "tantrieu#II.3", "Bài toán thực tế BCNN", 12, ghi="bỏ tên trường trong đề gốc"),
        ]),
        B(4, "Chu vi, diện tích", "Một mảnh đất hình chữ nhật có chiều dài là $12$ m, chiều rộng $10$ m. Người ta chia mảnh đất thành hai khu, một khu trồng hoa và một khu trồng cỏ. Hoa được trồng trong khu vực hình bình hành và cỏ trồng ở phần đất còn lại (như hình vẽ).", [
            Y("a", 0.75, "Tính diện tích mảnh đất hình chữ nhật.", [
                (r"Diện tích mảnh đất là $12\cdot10=120$ (m$^2$).", 0.5),
                (r"Vậy mảnh đất có diện tích $120$ m$^2$.", 0.25)], "cum14#II.4a", "Diện tích HCN", 3),
            Y("b", 0.75, "Tính diện tích trồng hoa.", [
                (r"Hình bình hành trồng hoa có cạnh đáy $6$ m, chiều cao tương ứng bằng chiều rộng mảnh đất là $10$ m.", 0.25),
                (r"Diện tích trồng hoa là $6\cdot10=60$ (m$^2$).", 0.5)], "cum14#II.4b", "Diện tích HBH (đọc hình)", 6),
            Y("c", 1.0, "Tính số tiền cần trả để trồng cỏ, biết giá mỗi mét vuông trồng cỏ là $30\\,000$ đồng.", [
                (r"Diện tích trồng cỏ là $120-60=60$ (m$^2$).", 0.5),
                (r"Số tiền trồng cỏ là $60\cdot30\,000=1\,800\,000$ (đồng).", 0.25),
                (r"Vậy cần trả $1\,800\,000$ đồng.", 0.25)], "cum14#II.4c", "Thực tế: chi phí phần còn lại", 7),
        ], hinh=hinh_hbh_cum14(), hinh_w="0.34"),
        B(5, "Vận dụng cao", r"Tìm số nguyên $x$ sao cho $2x-1$ là ước của $4x+3$.", [
            Y("", 0.5, "", [
                rf"Vì $2x-1$ là ước của $4x+3$ nên $4x+3{CHIA}(2x-1)$, tức là $2(2x-1)+5{CHIA}(2x-1)$.",
                (rf"Mà $2(2x-1){CHIA}(2x-1)$ nên $5{CHIA}(2x-1)$, hay " + r"$2x-1\in\text{Ư}(5)=\{1;-1;5;-5\}$.", 0.25),
                r"\par\begin{center}\begin{tabular}{|c|c|c|c|c|}\hline $2x-1$ & $1$ & $-1$ & $5$ & $-5$ \\ \hline $x$ & $1$ & $0$ & $3$ & $-2$ \\ \hline\end{tabular}\end{center}",
                (r"Vậy $x\in\{1;0;3;-2\}$.", 0.25),
            ], "dongocdu#II.5", "Ước số nguyên (VDC)", 8),
        ]),
    ],
)


# ======================================================================= KIỂM + XUẤT
def kiem():
    loi = []
    bo_quan, bo_truong = {}, {}
    for k, D in DE.items():
        if len(D["tn"]) != 8:
            loi.append(f"{k}: {len(D['tn'])} câu TN")
        for i, c in enumerate(D["tn"], 1):
            dung(c["ref"], f"{k} TN{i}")
            if c["dap"] not in "ABCD" or len(c["opts"]) != 4:
                loi.append(f"{k} TN{i}: phương án lỗi")
        tong = 2.0
        quan = {}
        for c in D["tn"]:
            q = QUAN[c["ref"].split("#")[0]]
            quan[q] = quan.get(q, 0) + 0.25
        for b in D["bai"]:
            for yy in b["ys"]:
                dung(yy["ref"], f"{k} Bài {b['so']}{yy['nhan']}")
                sd = diem_steps(yy["steps"])
                if abs(sd - yy["diem"]) > 1e-9:
                    loi.append(f"{k} Bài {b['so']}{yy['nhan']}: điểm bước {sd} ≠ {yy['diem']}")
                tong += yy["diem"]
                q = QUAN[yy["ref"].split("#")[0]]
                quan[q] = quan.get(q, 0) + yy["diem"]
        if abs(tong - 10) > 1e-9:
            loi.append(f"{k}: tổng {tong}")
        D["quan"] = quan
        for q, v in quan.items():
            bo_quan[q] = bo_quan.get(q, 0) + v
        if max(quan.values()) > 4.0 + 1e-9:
            loi.append(f"{k}: một quận quá 40% ({quan})")
        if len(quan) < 4:
            loi.append(f"{k}: chỉ {len(quan)} quận")
    for r in DA_DUNG:
        t = r.split("#")[0]
        bo_truong[t] = bo_truong.get(t, 0) + 1
    return loi, bo_quan


def chuong(ref):
    return "Ch." + LA_MA[cau(ref)["cd"]]


def muc(ref):
    return cau(ref)["muc"]


def ten_de(D):
    return (f"Đề ôn tập số {D['so']}" if D["loai"] == "on" else f"Đề kiểm tra chính thức số {D['so']}")


def slug(D, mt=False):
    if D["loai"] == "on":
        return f"ma-tran-va-dap-an-on-tap-cuoi-ki-1-so-{D['so']}" if mt else f"de-on-tap-cuoi-ki-1-so-{D['so']}"
    return f"ma-tran-va-dap-an-cuoi-ki-1-de-{D['so']}" if mt else f"de-kiem-tra-cuoi-ki-1-de-{D['so']}"


TN_DAU = (r"\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm).} \textit{Mỗi câu 0,25 điểm. Chọn chữ cái đứng trước "
          r"câu trả lời đúng rồi ghi vào bài làm (ví dụ: 1 -- A).}")
TL_DAU = r"\textbf{PHẦN II. TỰ LUẬN (8,0 điểm)}"


def khoi_tn(i, c):
    return dict(type="problem", label=f"Câu {i}.", level=1 if muc(c["ref"]) == "NB" else 2, statement=c["stem"],
                options=c["opts"], answer=c["dap"], solution=f"Chọn \\textbf{{{c['dap']}}}. " + c["giai"], tier="onclass")


def de_bai(b):
    tong = sum(yy["diem"] for yy in b["ys"])
    st = f"\\textbf{{({d(tong)} điểm)}} " + b["mo"]
    if b["hinh"]:  # hình đứng cạnh lời dẫn (renderer ép hình dưới đề rộng 0,44 ⇒ đề tràn trang 3)
        st = (f"\\begin{{minipage}}[t]{{0.50\\linewidth}}\\raggedright {st}\\end{{minipage}}\\hfill"
              f"\\begin{{minipage}}[t]{{0.36\\linewidth}}\\centering\\adjustbox{{valign=t,max width=\\linewidth,max totalheight=4.2cm}}{{{b['hinh']}}}\\end{{minipage}}")
    if b["so"] in (1, 2):  # ý ngắn: hai ý một dòng cho đề gọn 2 trang
        o = [f"\\makebox[0.48\\linewidth][l]{{{yy['nhan']}) {yy['de']}}}" for yy in b["ys"]]
        st += "".join(BR + "".join(o[i:i + 2]) for i in range(0, len(o), 2))
    elif b["ys"][0]["nhan"]:
        st += "".join(BR + f"{yy['nhan']}) " + (f"\\textit{{({d(yy['diem'])}đ)}} " if b["so"] == 4 else "") + yy["de"] for yy in b["ys"])
    return st


def loi_giai_bai(b):
    parts = []
    for yy in b["ys"]:
        dau = f"\\textbf{{{yy['nhan']}) ({d(yy['diem'])}đ)}}" + BR if yy["nhan"] else ""
        parts.append(dau + buoc(yy["steps"]))
    return BR.join(parts)


def khoi_bai(b):
    blk = dict(type="problem", label=f"Bài {b['so']}.", level=3 if b["so"] in (4, 5) else 2, statement=de_bai(b),
               solution=loi_giai_bai(b), tier="onclass")
    return blk


def bai5_het(b):
    blk = khoi_bai(b)
    blk["statement"] += "\\par\\smallskip\\centerline{\\textit{$-$ HẾT $-$}}"
    return blk


def de_json(D):
    st = [dict(kind="review", number=1, title="", blocks=[dict(type="para", text=TN_DAU)] + [khoi_tn(i, c) for i, c in enumerate(D["tn"], 1)]),
          dict(kind="concept", number=2, title="", blocks=[dict(type="para", text=TL_DAU), khoi_bai(D["bai"][0])]),
          dict(kind="practice1", number=3, title="", blocks=[khoi_bai(D["bai"][1]), khoi_bai(D["bai"][2])]),
          dict(kind="practice2", number=4, title="", blocks=[khoi_bai(D["bai"][3])]),
          dict(kind="reflection", number=5, title="", blocks=[bai5_het(D["bai"][4])])]
    if D["loai"] == "on":
        tit, eb = f"Đề ôn tập cuối học kì I — Số {D['so']} (90 phút)", f"LỚP 6 • ĐỀ ÔN TẬP SỐ {D['so']}"
    else:
        tit, eb = f"Đề kiểm tra cuối học kì I — Đề {D['so']} (90 phút)", f"LỚP 6 • ĐỀ CHÍNH THỨC SỐ {D['so']}"
    return dict(slug=slug(D), title=tit, eyebrow=eb, grade_label="Lớp 6", class_tier="", theme="de_thi", stages=st)


def hang_mt(D):
    rows = []
    for i, c in enumerate(D["tn"], 1):
        rows.append((f"Câu {i}", c["nd"], chuong(c["ref"]), muc(c["ref"]), 0.25, 2, nguon(c["ref"], c["ghi"])))
    for b in D["bai"]:
        for yy in b["ys"]:
            nh = f"Bài {b['so']}" + (f"{yy['nhan']}" if yy["nhan"] else "")
            rows.append((nh, yy["nd"], chuong(yy["ref"]), muc(yy["ref"]), yy["diem"], yy["phut"], nguon(yy["ref"], yy["ghi"])))
    return rows


def bang_mt(rows):
    s = ("\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.05}\n"
         "\\begin{tabular}{|c|p{4.1cm}|c|c|c|c|p{5.2cm}|}\\hline\n"
         "\\textbf{Câu} & \\textbf{Nội dung (dạng bài)} & \\textbf{Chương} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} & \\textbf{Nguồn đề (Hà Nội)} \\\\ \\hline\n")
    for c, nd, ch, m, di, ph, ng in rows:
        s += f"{c} & {nd} & {ch} & {m} & {d(di)} & {ph} & {ng} \\\\ \\hline\n"
    s += (f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{TỔNG}}}} & \\textbf{{{d(sum(r[4] for r in rows))}}} & "
          f"\\textbf{{{sum(r[5] for r in rows)}}} & \\\\ \\hline\n\\end{{tabular}}\\end{{center}}")
    return s


def bang_tong(rows):
    M = ["NB", "TH", "VD", "VDC"]
    ch = ["Ch.I", "Ch.II", "Ch.III", "Ch.IV", "Ch.V"]
    t = {c: {m: 0.0 for m in M} for c in ch}
    for r in rows:
        t[r[2]][r[3]] += r[4]
    ten = {"Ch.I": "I. Tập hợp các số tự nhiên", "Ch.II": "II. Tính chia hết", "Ch.III": "III. Số nguyên",
           "Ch.IV": "IV. Hình phẳng trong thực tiễn", "Ch.V": "V. Tính đối xứng"}
    s = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\\begin{tabular}{|l|c|c|c|c|c|}\\hline\n"
         "\\textbf{Chương (KNTT)} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{VDC} & \\textbf{Tổng} \\\\ \\hline\n")
    for c in ch:
        s += ten[c] + " & " + " & ".join(d(t[c][m]) if t[c][m] else "--" for m in M) + f" & \\textbf{{{d(sum(t[c].values()))}}} \\\\ \\hline\n"
    tm = {m: sum(t[c][m] for c in ch) for m in M}
    s += "\\textbf{Tổng điểm} & " + " & ".join(f"\\textbf{{{d(tm[m])}}}" for m in M) + " & \\textbf{10,0} \\\\ \\hline\n"
    s += "\\textbf{Tỉ lệ} & " + " & ".join(f"{round(tm[m] * 10)}\\%" for m in M) + " & 100\\% \\\\ \\hline\n\\end{tabular}\\end{center}"
    return s


KHUNG_TXT = ("\\textbf{Khung đề} (chốt từ 24 đề cuối kì I Toán 6 của các trường, phòng GD Hà Nội: 15 đề năm học 2025--2026 và 9 đề 2024--2025; "
             "phân dạng trên Google Sheets “Phân dạng Toán lớp 6 -- đề CK1 chính thức Hà Nội 2024-2026”): Phần I trắc nghiệm 8 câu (2,0đ; 19/24 đề trường có trắc nghiệm 2đ) · "
             "Bài 1 thực hiện phép tính (2,0đ) · Bài 2 tìm $x$ (1,5đ) · Bài 3 bài toán thực tế BCNN/ƯCLN (1,5đ; 24/24 đề) · "
             "Bài 4 bài toán thực tế chu vi, diện tích (2,5đ; 23/24 đề) · Bài 5 vận dụng cao (0,5đ; 24/24 đề). Phạm vi: Chương I--V SGK Toán 6 KNTT.")


def mt_json(D):
    rows = hang_mt(D)
    q = D["quan"]
    nguon_txt = ", ".join(f"{k} {d(v)}đ" for k, v in sorted(q.items(), key=lambda t: -t[1]))
    vai = ("\\textbf{Vai trò:} đề ÔN TẬP -- dạng tần suất cao" + (" nhất, câu bốc nguyên văn từ đề trường." if D["so"] < 3 else
                                                                   " thứ nhì (luỹ thừa, ƯCLN, ước số nguyên, tìm $x$ ở số mũ) để mở rộng.")
           if D["loai"] == "on" else
           "\\textbf{Vai trò:} đề KIỂM TRA CHÍNH THỨC -- cùng khung với 3 đề ôn nhưng mọi câu lấy từ đề trường CHƯA dùng trong đề ôn, để đo năng lực chứ không đo trí nhớ.")
    s1 = [dict(type="para", text=KHUNG_TXT + BR + vai),
          dict(type="para", text=f"\\textbf{{MA TRẬN {ten_de(D).upper()} -- CUỐI HỌC KÌ I TOÁN 6 (90 phút)}}" + BR
               + f"\\textbf{{Nguồn theo quận/huyện cũ:}} {nguon_txt} (mỗi quận $\\le 40\\%$ điểm của đề)." + BR + bang_mt(rows)),
          dict(type="para", text="\\textbf{TỔNG HỢP THEO CHƯƠNG VÀ MỨC ĐỘ (điểm)}" + BR + bang_tong(rows))]
    s2 = [dict(type="para", text="\\textbf{ĐÁP ÁN PHẦN I. TRẮC NGHIỆM (2,0 điểm)} -- mỗi câu đúng 0,25 điểm."),
          dict(type="para", text="\\begin{center}\\small\\begin{tabular}{|c|c|c|c|c|c|c|c|}\\hline "
               + " & ".join(f"\\textbf{{{i}}}" for i in range(1, 9)) + r" \\ \hline "
               + " & ".join(c["dap"] for c in D["tn"]) + r" \\ \hline\end{tabular}\end{center}"),
          dict(type="para", text=BR.join(f"\\textbf{{Câu {i} -- {c['dap']}.}} {c['giai']}" for i, c in enumerate(D["tn"], 1)))]
    stages = [dict(kind="review", number=1, title=f"Ma trận {ten_de(D).lower()}", blocks=s1),
              dict(kind="concept", number=2, title="Đáp án Phần I", blocks=s2)]
    kinds = ["practice1", "practice2", "reflection"]
    nhom = [[0, 1], [2, 3], [4]]
    for j, idx in enumerate(nhom):
        bl = []
        for i in idx:
            b = D["bai"][i]
            bl.append(dict(type="para", text=f"\\textbf{{BÀI {b['so']} ({d(sum(yy['diem'] for yy in b['ys']))} điểm).}}"))
            if b["hinh"]:
                bl.append(dict(type="figure", tikz=b["hinh"], width="0.5\\linewidth"))
            bl.append(dict(type="para", text=loi_giai_bai(b)))
            if b["note"]:
                bl.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + b["note"] + "}"))
        if j == 2:
            bl.append(dict(type="para", text="\\textbf{Tổng: 10,0 điểm.} Học sinh làm cách khác đúng vẫn cho điểm tối đa từng phần. "
                                            "Điểm toàn bài làm tròn đến một chữ số thập phân."))
        stages.append(dict(kind=kinds[j], number=3 + j, title=["Đáp án Bài 1, Bài 2", "Đáp án Bài 3, Bài 4", "Đáp án Bài 5"][j], blocks=bl))
    tit = f"Ma trận đề và đáp án chi tiết — {ten_de(D)}"
    eb = "TÀI LIỆU GIÁO VIÊN • LỚP 6 • " + ten_de(D).upper()
    return dict(slug=slug(D, True), title=tit, eyebrow=eb, grade_label="Lớp 6", class_tier="", theme="de_thi",
                trinh_bay="thoang", stages=stages)


def main():
    loi, bo_quan = kiem()
    for x in loi:
        print("✗", x)
    if loi:
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    for k, D in DE.items():
        (OUT / f"{slug(D)}.json").write_text(json.dumps(de_json(D), ensure_ascii=False, indent=1), encoding="utf-8")
        (OUT / f"{slug(D, True)}.json").write_text(json.dumps(mt_json(D), ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {k}: {len(D['quan'])} quận — " + ", ".join(f"{a} {d(v)}" for a, v in sorted(D['quan'].items(), key=lambda t: -t[1])))
    tong = sum(bo_quan.values())
    print("  cả bộ: " + ", ".join(f"{a} {round(100 * v / tong)}%" for a, v in sorted(bo_quan.items(), key=lambda t: -t[1])))
    print(f"✓ {len(DA_DUNG)} ý dùng, không trùng; ghi {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
