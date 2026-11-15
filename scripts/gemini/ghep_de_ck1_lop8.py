"""Ghép 6 kết quả Gemini de8-ck1-* thành scripts/ck1_lop8_phu_dang.json + các chỗ Claude SOÁT SỬA (13/11/2026).

Chạy: python3 scripts/gemini/ghep_de_ck1_lop8.py
Mọi sửa của Claude nằm trong VA (theo mã đề) để dựng lại được khi chạy lại việc Gemini.
"""
import json
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
XONG = GOC / "storage/gemini/xong"
RA = GOC / "scripts/ck1_lop8_phu_dang.json"
MA = ["on-1", "on-2", "on-3", "ct-1", "ct-2", "ct-3"]

BR = " [[br]] "

# Biểu đồ đoạn thẳng áo ấm (on-3 Bài 3): đề cũ ghi "biểu đồ đoạn thẳng" nhưng chỉ in bảng rồi bắt lập bảng.
BD_AO_AM = r"""\begin{tikzpicture}[x=1.25cm,y=0.011cm,font=\footnotesize,line width=0.7pt]
  \draw[->] (0,0)--(4.7,0) node[right] {Năm};
  \draw[->] (0,0)--(0,310) node[above] {Số áo (chiếc)};
  \foreach \val in {50,100,150,200,250} \draw[gray!50,line width=0.3pt] (0,\val)--(4.4,\val);
  \foreach \val in {0,50,100,150,200,250} \node[left] at (0,\val) {$\val$};
  \foreach \xx/\nam in {1/2021,2/2022,3/2023,4/2024} {\draw (\xx,0)--(\xx,-6); \node[below] at (\xx,0) {$\nam$};}
  \draw[line width=1pt] (1,120)--(2,150)--(3,200)--(4,260);
  \foreach \xx/\val in {1/120,2/150,3/200,4/260} {\fill (\xx,\val) circle (2pt); \node[above left] at (\xx,\val) {$\val$};}
\end{tikzpicture}"""

# Biểu đồ cột khách quốc tế (ct-2 Bài 3): cùng lỗi như trên.
BD_KHACH = r"""\begin{tikzpicture}[x=1.25cm,y=0.2cm,font=\footnotesize,line width=0.7pt]
  \draw[->] (0,0)--(4.7,0) node[right] {Năm};
  \draw[->] (0,0)--(0,15) node[above] {Triệu lượt};
  \foreach \val in {2,4,6,8,10,12} \draw[gray!50,line width=0.3pt] (0,\val)--(4.5,\val);
  \foreach \val in {0,2,4,6,8,10,12} \node[left] at (0,\val) {$\val$};
  \foreach \xx/\nam/\val/\tx in {1/2020/3.8/3{,}8,2/2021/0.2/0{,}2,3/2022/3.6/3{,}6,4/2023/12.6/12{,}6} {
    \fill[gray!45] (\xx-0.25,0) rectangle (\xx+0.25,\val); \draw (\xx-0.25,0) rectangle (\xx+0.25,\val);
    \node[above] at (\xx,\val) {$\tx$}; \node[below] at (\xx,0) {$\nam$};}
\end{tikzpicture}"""

# on-3 Bài 4 (tòa nhà, Phan Chu Trinh 2025-26 Bài III): hình Gemini đúng tỉ lệ thật ⇒ chữ quanh A, D, E dính chùm.
# Vẽ minh hoạ KHÔNG theo tỉ lệ, DE ∥ BC (cùng hệ số góc −1).
HINH_TOA_NHA = r"""\begin{tikzpicture}[line width=0.8pt,font=\small]
  \fill[gray!15] (-0.5,0) rectangle (0,5);
  \draw (-0.5,0) -- (-0.5,5) -- (0,5);
  \foreach \yy in {0.6,1.4,2.2,3.0,3.8} \draw[gray!60,line width=0.4pt] (-0.38,\yy) rectangle (-0.12,\yy+0.45);
  \draw[line width=1pt] (0,0) -- (0,5);
  \draw[line width=1pt] (-0.8,0) -- (5.6,0);
  \coordinate (A) at (0,0); \coordinate (B) at (0,5); \coordinate (C) at (5,0);
  \coordinate (D) at (0,1.6); \coordinate (E) at (1.6,0);
  \draw (B) -- (C); \draw (D) -- (E);
  \draw[line width=0.5pt] (0,0.25) -- (0.25,0.25) -- (0.25,0);
  \foreach \p in {A,B,C,D,E} \fill (\p) circle (1.6pt);
  \node[below left] at (A) {$A$}; \node[above right] at (B) {$B$}; \node[right=1pt] at (D) {$D$};
  \node[below] at (E) {$E$}; \node[below] at (C) {$C$};
  \node[left] at (-0.5,0.8) {$3{,}2\text{ m}$};
  \node[above] at (0.85,0) {$1{,}5\text{ m}$};
  \node[below] at (3.3,0) {$21\text{ m}$};
\end{tikzpicture}"""

# Biểu đồ cột kép CLB Toán (on-1 Bài 3).
BD_CLB = r"""\begin{tikzpicture}[x=1.3cm,y=0.13cm,font=\footnotesize,line width=0.7pt]
  \draw[->] (0,0)--(4.7,0) node[right] {Lớp};
  \draw[->] (0,0)--(0,19) node[above] {Số học sinh};
  \foreach \val in {5,10,15} {\draw[gray!50,line width=0.3pt] (0,\val)--(4.5,\val); \node[left] at (0,\val) {$\val$};}
  \node[left] at (0,0) {$0$};
  \foreach \xx/\lop/\nam/\nu in {1/8A/12/13,2/8B/15/10,3/8C/13/12,4/8D/10/15} {
    \fill[gray!60] (\xx-0.3,0) rectangle (\xx,\nam); \draw (\xx-0.3,0) rectangle (\xx,\nam);
    \fill[gray!15] (\xx,0) rectangle (\xx+0.3,\nu); \draw (\xx,0) rectangle (\xx+0.3,\nu);
    \node[above] at (\xx-0.15,\nam) {$\nam$}; \node[above] at (\xx+0.15,\nu) {$\nu$};
    \node[below] at (\xx,0) {\lop};}
  \fill[gray!60] (1,21.5) rectangle (1.25,23.5); \draw (1,21.5) rectangle (1.25,23.5); \node[right] at (1.25,22.5) {Nam};
  \fill[gray!15] (2.3,21.5) rectangle (2.55,23.5); \draw (2.3,21.5) rectangle (2.55,23.5); \node[right] at (2.55,22.5) {Nữ};
\end{tikzpicture}"""

BAREM_BANG = "Lập đúng bảng (đúng dòng tên năm và đúng 4 số liệu)."


def bang_tu_bieu_do(b, tikz, cau_dan):
    """Thay bảng trong đề bằng biểu đồ; barem ý a: 0,25 cho khung bảng + 0,25 cho đủ số liệu."""
    st = b["statement"]
    i, j = st.index("\\begin{center}"), st.index("\\end{center}") + len("\\end{center}")
    b["statement"] = st[:i] + "[[br]]" + st[j:]
    b["statement"] = b["statement"].replace("[[br]] [[br]] [[br]]", "[[br]]")
    b["hinh"], b["tikz"], b["width"] = "moi", tikz, "0.5"
    a = b["dap_an"][0]
    for bo in ["Vậy số lượng áo ấm tăng liên tục qua từng năm học.",
               "Vậy số liệu lượng khách du lịch quốc tế đã được thống kê đầy đủ theo từng năm."]:
        a = a.replace(bo, "(Đúng dòng tên năm: 0,25đ; đúng cả 4 số liệu: 0,25đ.)")
    b["dap_an"][0] = a.replace(cau_dan, cau_dan)


def dang_tn(R, nhan):
    """nhan = {số câu: mã} — Gemini gắn nhãn câu GIỮ khá ẩu (vd HĐT ra D04, tổng góc tứ giác ra D11)."""
    for c in R["tn"]:
        if c["cau"] in nhan:
            c["dang"] = nhan[c["cau"]]


def dang(R, nhan):
    """nhan = {(bài, ý-index): mã} — sửa nhãn dạng Gemini gắn sai."""
    for (bi, ri), m in nhan.items():
        R["bai"][bi]["mt"][ri]["dang"] = m


def va_on2(R):
    dang_tn(R, {3: "D05", 7: "D22"})
    dang(R, {(4, 0): "D16", (4, 2): "D19", (5, 0): "D30"})
    R["bai"][4]["bo_diem"] = ["Q"]  # ý b cũ (A trung điểm PQ) đã bỏ


ND_ON3 = {  # mô tả ngắn cho ma trận (bản Gemini dài ⇒ bảng tràn chân trang)
    "Bài 1.a": "Nhân đơn thức với đa thức", "Bài 1.b": "Rút gọn biểu thức có HĐT",
    "Bài 1.c": "Phân tích đa thức thành nhân tử", "Bài 2.a": "Tìm $x$: khai triển, rút gọn",
    "Bài 2.b": "Tìm $x$: đưa về tích bằng 0", "Bài 3.a": "Lập bảng từ biểu đồ đoạn thẳng",
    "Bài 3.b": "Tính mức tăng, tỉ số phần trăm", "Bài 4.a": "Tính chiều cao bằng định lí Thalès",
    "Bài 4.b": "Thực tế: quãng đường, thời gian", "Bài 5.a": "Chứng minh hình chữ nhật",
    "Bài 5.b": "Chứng minh hình thoi", "Bài 5.c": "Chứng minh hình bình hành",
    "Bài 6": "Đẳng thức có điều kiện, tính $a, b, c$",
}


def va_on3(R):
    for b in R["bai"]:
        for r in b["mt"]:
            r["nd"] = ND_ON3.get(r["ma"], r["nd"])
    dang_tn(R, {3: "D05"})
    dang(R, {(4, 0): "D16", (4, 1): "D17"})
    R["bai"][4]["bo_diem"] = ["H"]  # ý c cũ dùng đường cao AH, ý mới không dùng
    bang_tu_bieu_do(R["bai"][2], BD_AO_AM, "")
    R["bai"][3]["tikz"], R["bai"][3]["width"] = HINH_TOA_NHA, "0.5"


def va_ct2(R):
    dang_tn(R, {2: "D03", 5: "D13", 7: "D22"})
    dang(R, {(2, 0): "D27", (2, 1): "D28", (5, 0): "D29"})
    bang_tu_bieu_do(R["bai"][2], BD_KHACH, "")
    R["bai"][3]["statement"] = R["bai"][3]["statement"].replace("Em hãy tính", "Tính")


def va_ct3(R):
    dang_tn(R, {5: "D13", 6: "D13"})
    dang(R, {(5, 0): "D29"})
    b = R["bai"][3]
    b["statement"] = b["statement"].replace("a) \\textbf{(1,0 điểm)} ", "")
    b["dap_an"] = [d.replace("\\textbf{a) (1,0đ)} [[br]] ", "") for d in b["dap_an"]]
    b["statement"] = b["statement"].replace("(như hình vẽ bên)", "(như hình vẽ)")
    b["tikz"] = b["tikz"].replace("\\node[above left] at (A) {$A$};", "\\node[left=3pt] at (A) {$A$};")
    R["gioi_thieu"] = R["gioi_thieu"].replace("Đề bốc 100\\% từ các trường chưa xuất hiện ở các đề ôn tập: ", "")


def va_on1(R):
    dang_tn(R, {3: "D05", 5: "D12", 6: "D13"})
    dang(R, {(4, 0): "D16", (4, 2): "D17", (5, 0): "D29"})
    R["bai"][4]["bo_diem"] = ["H"]  # ý b cũ dùng đường cao AH
    bang_tu_bieu_do(R["bai"][2], BD_CLB, "")
    R["bai"][2]["statement"] = R["bai"][2]["statement"].replace("Biểu đồ cột kép bên", "Biểu đồ cột kép sau")
    R["bai"][2]["dap_an"][0] = R["bai"][2]["dap_an"][0].replace("Dựa vào bảng số liệu trên", "Dựa vào biểu đồ")
    R["bai"][3]["statement"] = R["bai"][3]["statement"].replace("(hình bên)", "(như hình vẽ)")
    R["bai"][3]["tikz"] = R["bai"][3]["tikz"].replace("\\fill[red]", "\\fill")


def va_ct1(R):
    dang_tn(R, {2: "D03", 3: "D05"})
    dang(R, {(4, 0): "D16", (4, 1): "D19", (4, 2): "D14", (5, 0): "D29"})
    b = R["bai"][3]
    b["statement"] = (b["statement"].replace("a) \\textbf{(1,0 điểm)} ", "").replace("(như hình vẽ bên)", "(như hình vẽ)")
                      .replace("Em hãy tính", "Tính"))
    b["dap_an"] = [d.replace("\\textbf{a) (1,0đ)} [[br]] ", "") for d in b["dap_an"]]


VA = {"on-1": va_on1, "ct-1": va_ct1, "on-2": va_on2, "on-3": va_on3, "ct-2": va_ct2, "ct-3": va_ct3}


def main():
    out = {}
    for k in MA:
        p = XONG / f"de8-ck1-{k}.json"
        if not p.exists():
            print("CHƯA CÓ", k)
            continue
        d = json.loads(p.read_text())
        R = d.get("ket_qua") or d.get("structured_output")
        if k in VA:
            VA[k](R)
        else:
            print("CHƯA SOÁT", k, "— không ghép")
            continue
        out[k] = R
    RA.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("ghi", RA, list(out))


if __name__ == "__main__":
    main()
