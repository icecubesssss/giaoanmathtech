#!/usr/bin/env python3
"""Dựng PHIẾU THUYẾT MINH (đặc tả) cho [C]tuần 10-11 — BPT bậc nhất một ẩn.
Gộp Phiếu A + B. Số câu / thời gian khớp duration_gate (1,5/6/12 trên lớp;
1,3/5,2/10,4 BTVN). Chạy: python -m scripts.build_thuyetminh_tuan10_11
"""
from __future__ import annotations
import subprocess

from config import settings
from src.compiler.jinja_renderer import _env, load_tokens

OUT_DIR = (settings.ROOT / "outputs/lop-9/dai-so/lop-c/"
           "[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an")


def esc(s: str) -> str:
    return s


def itemize(items: list[str]) -> str:
    body = "\n".join(rf"  \item {x}" for x in items)
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}"


def meta_table(rows: list[tuple[str, str]]) -> str:
    out = [r"\begin{tabular}{|>{\sffamily\bfseries\color{ink}}p{3.4cm}|"
           r">{\RaggedRight\arraybackslash}p{22.4cm}|}", r"\arrayrulecolor{rule}\hline"]
    for lbl, val in rows:
        out.append(f"{lbl} & {val} \\\\ \\hline")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def phieu_table(groups, total) -> str:
    col = (r"|>{\RaggedRight\arraybackslash}p{10.2cm}|"
           r"*{6}{>{\centering\arraybackslash}p{2.0cm}|}")
    L = [rf"\begin{{tabular}}{{{col}}}", r"\arrayrulecolor{rule}\hline"]
    # header 2 dòng
    L.append(r"\rowcolor{neutral}\multirow{2}{*}{\sffamily\bfseries Dạng bài} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Ví dụ lý thuyết} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Bài tập trên lớp} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries BTVN} \\ \cline{2-7}")
    L.append(r"\rowcolor{neutral} & \sffamily\footnotesize Số câu & \sffamily\footnotesize Thời gian "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize Thời gian "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize Thời gian \\ \hline")
    for title, tint, rows, sub in groups:
        L.append(rf"\multicolumn{{7}}{{|l|}}{{\cellcolor{{{tint}!16}}\sffamily\bfseries\color{{{tint}}}{title}}} \\ \hline")
        for dang, ex, exT, on, onT, bt, btT in rows:
            L.append(f"{dang} & {ex} & {exT} & {on} & {onT} & {bt} & {btT} \\\\ \\hline")
        sx, son, sonT, sbt, sbtT = sub
        L.append(rf"\multicolumn{{1}}{{|r|}}{{\itshape\bfseries Cộng nhóm}} & "
                 rf"\multicolumn{{2}}{{c|}}{{\itshape {sx}}} & "
                 rf"\bfseries {son} & \bfseries {sonT} & \bfseries {sbt} & \bfseries {sbtT} \\ \hline")
    tx, ton, tonT, tbt, tbtT = total
    L.append(rf"\rowcolor{{brand!12}}\multicolumn{{1}}{{|r|}}{{\sffamily\bfseries\color{{brand}}TỔNG}} & "
             rf"\multicolumn{{2}}{{>{{\columncolor{{brand!12}}}}c|}}{{\bfseries {tx}}} & "
             rf"\bfseries {ton} & \bfseries {tonT} & \bfseries {tbt} & \bfseries {tbtT} \\ \hline")
    L.append(r"\end{tabular}")
    return "\n".join(L)


# ----------------------------------------------------------------------------
meta = [
    ("Tên bài", r"\textbf{Bất phương trình bậc nhất một ẩn} — Tuần 10–11 \textbf{(LỚP C)}. "
                r"Gồm 2 phiếu: \textbf{Phiếu A} — Nhận biết \& giải BPT; "
                r"\textbf{Phiếu B} — Toán thực tế lập BPT."),
    ("Thời gian", r"Mỗi phiếu $=$ 1 buổi $=$ 180′ ($=$ 165′ trên lớp $+$ 15′ giải lao). "
                  r"Trên lớp: Ví dụ/giảng (Khám phá \& Khái niệm) $\approx$ 25–30′ "
                  r"$+$ Luyện tập 120′. BTVN $\approx$ 90′ ở nhà."),
    ("Nguồn đề", r"$\approx$ 70\% bê nguyên từ 10 đề GIỮA KÌ I 2024–2025 (ghi rõ tên trường) "
                 r"$+$ 30\% phiếu bổ trợ TOANMATH/SGK. \textbf{Không bịa đề.}"),
    ("Cách dùng", r"\textbf{Phiếu A:} Luyện tập \& BTVN in \textbf{ĐỀ BÀI tối giản} — HS chép đề, làm vào vở "
                  r"(Thầy hướng dẫn trực tiếp). \textbf{Phiếu B:} \textbf{GIỮ GIÀN GIÁO} — bài toán thực tế (boss) "
                  r"chẻ câu nhỏ a–h có ô điền, gỡ giàn dần; các bài drill nhận biết in đề gọn."),
]

lythuyet = [
    r"Khái niệm BPT bậc nhất một ẩn: dạng $ax+b>0$ (hoặc $<0,\ \le 0,\ \ge 0$) với $a\neq0$.",
    r"Nghiệm của BPT; \emph{giải} BPT $=$ tìm tất cả nghiệm (thay số $\to$ khẳng định đúng).",
    r"Hai quy tắc biến đổi: chuyển vế $\to$ đổi \textbf{DẤU} (không đổi chiều); nhân/chia hai vế "
    r"$\to$ số dương \emph{giữ} chiều, số âm \textbf{ĐỔI CHIỀU}.",
    r"Quy đồng khử mẫu (mẫu chung dương $\to$ giữ chiều).",
    r"4 bước giải toán thực tế bằng cách lập BPT: gọi ẩn $+$ điều kiện $\to$ lập BPT theo từ khoá "
    r"$\to$ giải $\to$ đối chiếu/làm tròn \& trả lời (kèm đơn vị).",
]

vidu = [
    r"Giải BPT bậc nhất cơ bản $2x-6\ge0$; minh hoạ đổi chiều với $-2x-4>0$ (bắt lỗi ``bạn Minh'').",
    r"Giải BPT có ngoặc / khai triển HĐT; giải BPT có mẫu (quy đồng khử mẫu).",
    r"Lập \& giải BPT từ bài toán thực tế: mua vở trong hạn mức tiền (bẫy làm tròn của ``bạn Lan'').",
    r"Lập ``từ điển'' từ khoá $\to$ dấu so sánh.",
]

dangVD = [
    r"Giải BPT bậc nhất: cơ bản, có ngoặc, khai triển HĐT, quy đồng khử mẫu.",
    r"Tìm số nguyên lớn nhất / nhỏ nhất thoả BPT.",
    r"Toán thực tế lập BPT: tải trọng (thang máy), mua sắm trong hạn mức tiền, lãi suất tiết kiệm, "
    r"trả góp, năng suất \& điểm xét tuyển…",
    r"(Bản chuẩn còn có BPT vô nghiệm / vô số nghiệm; lớp C tập trung dạng cơ bản.)",
]

loisai = [
    r"Quên \textbf{ĐỔI CHIỀU} khi nhân/chia hai vế với số \textbf{ÂM}.",
    r"Khử mẫu: nhân \emph{thiếu} số đứng một mình; dấu trừ trước phân số $\to$ quên đổi dấu \textbf{cả tử}.",
    r"Dịch sai dấu từ từ khoá (``không quá'' $\leftrightarrow \le$; ``ít nhất'' $\leftrightarrow \ge$).",
    r"Làm tròn sai chiều (``nhiều nhất'' $\to$ xuống; ``ít nhất'' $\to$ lên); quên thử lại đáp số.",
    r"Quên điều kiện của ẩn; quên đơn vị khi trả lời.",
    r"Nhận nhầm BPT bậc nhất (bậc $\ge2$, hệ số ẩn $=0$, ẩn ở mẫu).",
]

kienthucNB = [
    r"Nhận biết BPT bậc nhất một ẩn; xác định hệ số $a,\ b$.",
    r"Tính chất bất đẳng thức: cộng/trừ giữ chiều; nhân/chia số âm đổi chiều.",
    r"Giải BPT một bước; thử nghiệm bằng cách thay số.",
    r"Từ khoá $\to$ dấu; viết biểu thức theo ẩn; xác định chiều làm tròn.",
]

phieuA = ([
    (r"NHẬN BIẾT — NB ($\bigstar$)", "stage1", [
        (r"Nhận biết BPT bậc nhất một ẩn; hệ số $a,b$; điều kiện tham số (Bài 1, 3 / BTVN 11, 14)", "1", "~2′", "10", "15′", "12", "16′"),
        (r"Giải BPT một bước; điền dấu khi nhân/chia (Bài 2 / BTVN 12)", "1", "~2′", "10", "15′", "8", "10′"),
        (r"Thử nghiệm: thay số xét nghiệm đúng/sai (Bài 4 / BTVN 13)", "1", "~1′", "7", "11′", "7", "9′"),
        (r"Nhận \& sửa lỗi đổi chiều — Đúng/Sai (Bài 5)", "—", "—", "5", "8′", "—", "—"),
    ], ("3 ví dụ", "32", "48′", "27", "35′")),
    (r"THÔNG HIỂU — TH ($\bigstar\bigstar$)", "stage2", [
        (r"Giải BPT: cơ bản, có ngoặc, khai triển HĐT (Bài 6, 7, 8 / BTVN 15)", "2", "~8′", "6", "36′", "7", "36′"),
        (r"Giải BPT có mẫu: quy đồng khử mẫu (Bài 9)", "—", "—", "2", "12′", "—", "—"),
    ], ("2 ví dụ", "8", "48′", "7", "36′")),
    (r"VẬN DỤNG — VD ($\bigstar\bigstar\bigstar$)", "stage3", [
        (r"Tìm số nguyên lớn nhất / nhỏ nhất thoả BPT (Bài 10 / BTVN 16)", "—", "—", "2", "24′", "2", "21′"),
    ], ("—", "2", "24′", "2", "21′")),
], ("4 ví dụ", "42", "120′", "36", "92′"))

phieuB = ([
    (r"NHẬN BIẾT — NB ($\bigstar$)", "stage1", [
        (r"Từ khoá $\to$ dấu; dịch câu thành BPT (Bài 1 / BTVN 7, 8)", "1", "~1′", "6", "9′", "14", "18′"),
        (r"Viết biểu thức theo ẩn $x$ (Bài 2 / BTVN 9)", "—", "—", "10", "15′", "8", "10′"),
        (r"Xác định chiều làm tròn (Bài 3 / BTVN 10)", "—", "—", "6", "9′", "6", "8′"),
        (r"Ý nhận biết trong toán thực tế chẻ câu (Bài 5, 6 / BTVN 11)", "—", "—", "5", "8′", "1", "1′"),
    ], ("1 ví dụ", "27", "40′", "29", "38′")),
    (r"THÔNG HIỂU — TH ($\bigstar\bigstar$)", "stage2", [
        (r"Lập BPT từ tình huống — chưa giải (Bài 4 / BTVN 12)", "1", "~4′", "3", "18′", "4", "21′"),
        (r"Ý thông hiểu trong toán thực tế chẻ câu: lập \& biến đổi BPT (Bài 5, 6 / BTVN 11, 13)", "—", "—", "5", "30′", "3", "15′"),
    ], ("1 ví dụ", "8", "48′", "7", "36′")),
    (r"VẬN DỤNG — VD ($\bigstar\bigstar\bigstar$)", "stage3", [
        (r"Kết luận \& thử lại trong toán thực tế (Bài 5, 6 / BTVN 11, 13)", "—", "—", "2", "24′", "2", "21′"),
    ], ("—", "2", "24′", "2", "21′")),
], ("2 ví dụ", "37", "112′", "38", "95′"))

noteB = (r"\textit{\small\color{muted}Ghi chú:} bài toán thực tế (boss) của Phiếu B \textbf{giữ giàn giáo} — chẻ câu nhỏ "
         r"a–h có ô điền, gỡ giàn dần (Bài 5 đủ 8 ý $\to$ Bài 6 còn 4 ý $\to$ BTVN gần đề trần); ý gắn thẻ NB/TH/VD "
         r"nên trải ở cả 3 mức. Tỉ lệ giờ trên lớp $\approx$ \textbf{36-43-21\%} (trong sai số 40-40-20 $\pm$5).")

# ----------------------------------------------------------------------------
parts = []
parts.append(r"\tmtitle{PHIẾU THUYẾT MINH}\quad\tmsub{Bất phương trình bậc nhất một ẩn "
             r"• Lớp 9 (Ôn vào 10) • LỚP C • Tuần 10–11}")
parts.append(r"\par\vspace{4pt}")
parts.append(meta_table(meta))

parts.append(r"\tmsec{LÝ THUYẾT}")
parts.append(itemize(lythuyet))

parts.append(r"\tmsec{BÀI TẬP}")
parts.append(r"\begin{minipage}[t]{0.485\linewidth}\tmlbl{Ví dụ với BPT (GV làm mẫu — Khám phá/Khái niệm):}" + itemize(vidu) + r"\end{minipage}\hfill\begin{minipage}[t]{0.485\linewidth}\tmlbl{Các dạng bài VẬN DỤNG trong đề kiểm tra GK/CK:}" + itemize(dangVD) + r"\end{minipage}")
parts.append(r"\par\vspace{4pt}")
parts.append(r"\begin{minipage}[t]{0.485\linewidth}\tmlbl{Lỗi sai thường gặp ở học sinh:}" + itemize(loisai) + r"\end{minipage}\hfill\begin{minipage}[t]{0.485\linewidth}\tmlbl{Kiến thức NHẬN BIẾT cần nhớ (để làm bài VẬN DỤNG):}" + itemize(kienthucNB) + r"\end{minipage}")

parts.append(r"\tmsec{NỘI DUNG PHIẾU — PHIẾU A: NHẬN BIẾT \& GIẢI BPT}")
parts.append(phieu_table(*phieuA))

parts.append(r"\tmsec{NỘI DUNG PHIẾU — PHIẾU B: TOÁN THỰC TẾ LẬP BPT}")
parts.append(phieu_table(*phieuB))
parts.append(r"\par\vspace{3pt}" + noteB)

parts.append(r"\par\vspace{6pt}{\footnotesize\color{muted}\itshape Quy ước đếm (Thầy chốt): "
             r"``câu'' $=$ ý nhỏ a),b)…; phút/câu trên lớp 1,5/6/12 (NB/TH/VD), BTVN 1,3/5,2/10,4; "
             r"Ví dụ lý thuyết $=$ số ví dụ GV làm mẫu ở Khám phá/Khái niệm (giờ giảng $\approx$25–30′/buổi, "
             r"ngoài quỹ Luyện tập 120′). Số liệu khớp cổng \texttt{duration-gate}.}")

body = "\n\n".join(parts)

tokens = load_tokens()
env = _env()
tpl = env.get_template("base_thuyetminh.tex.j2")
tex = tpl.render(body=body, **tokens)

tex_path = OUT_DIR / "thuyet-minh-tuan10-11.tex"
tex_path.write_text(tex, encoding="utf-8")
print("Wrote", tex_path)

proc = subprocess.run([settings.TECTONIC_BIN, "-X", "compile", str(tex_path),
                       "--outdir", str(OUT_DIR)], capture_output=True, text=True)
if proc.returncode != 0:
    print("TECTONIC FAILED:\n", proc.stderr[-4000:])
    raise SystemExit(1)
print("PDF:", OUT_DIR / "thuyet-minh-tuan10-11.pdf")
