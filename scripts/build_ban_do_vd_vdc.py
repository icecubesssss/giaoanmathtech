#!/usr/bin/env python3
"""Dựng PDF 'BẢN ĐỒ VD/VDC THEO CHƯƠNG' từ config/ban_do_vd_vdc.json — cho Thầy & sếp duyệt.

Mỗi khối một bảng: chương → kết luận (CÓ VD / KHÔNG VD / CẦN CHỐT) → tỉ lệ áp dụng cho
phiếu tầng B → BẰNG CHỨNG (trích từ ma trận trường công bố kèm đề). Dòng 'CẦN CHỐT' bôi
màu để Thầy nhìn ra ngay chỗ phải quyết.

Dùng:  .venv/bin/python scripts/build_ban_do_vd_vdc.py
Ra:    outputs/ban-do-vd-vdc/ban-do-vd-vdc.pdf
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import settings                                    # noqa: E402
from src.compiler.jinja_renderer import _env, load_tokens      # noqa: E402
from src.compiler.latex_builder import build_pdf               # noqa: E402

SRC = ROOT / "config" / "ban_do_vd_vdc.json"

_ESC = {"\\": " ", "&": r"\&", "%": r"\%", "$": " ", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}"}


# Đề trích từ PDF hay lẫn kí tự lạ — font của template không có glyph nên in ra Ô VUÔNG
# trên PDF Thầy đọc. Đổi sang chữ thường dùng, và XOÁ hẳn vùng dùng-riêng (U+F000–U+F8FF)
# mà pdftotext sinh ra khi PDF gốc nhúng font symbol.
_THAY_GLYPH = {"\u2206": "tam giác ", "\u2212": "-", "\u22c5": ".", "\u2264": " <= ",
               "\u2265": " >= ", "\u2260": " != ", "\u221a": "căn ", "\u00b0": " độ"}
_PUA = re.compile(r"[\uE000-\uF8FF]")


def tex(s: str, n: int | None = None) -> str:
    """Escape sang LaTeX; `n` cắt bớt độ dài (trích dẫn đề bài in trong ô bảng)."""
    s = str(s)
    for a, b in _THAY_GLYPH.items():
        s = s.replace(a, b)
    s = _PUA.sub("", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s)     # bỏ lệnh LaTeX trong đề gốc (\widehat, \dfrac…)
    s = re.sub(r"\s+", " ", s)
    if n:
        s = s[:n]
    return "".join(_ESC.get(c, c) for c in s)


# muc_do → (nhãn nhóm, màu nền dòng, tỉ lệ áp dụng, cách đóng phiếu)
_KL = {
    "TH-VD-VDC":    ("\\bfseries TH $+$ VD $+$ VDC", "stage4!14",
                     "NB 15\\% · TH 30\\% · VD+VDC 55\\%", "1 phiếu $=$ 1 buổi"),
    "TH-VD":        ("TH $+$ VD", "stage3!10",
                     "NB 15\\% · TH 30\\% · VD+VDC 55\\%", "1 phiếu $=$ 1 buổi"),
    "chi-TH":       ("chỉ TH (và NB)", "stage1!10", "NB 30\\% · TH 70\\%",
                     "\\bfseries GỘP 2 phiếu $=$ 1"),
    "can-Thay-chot": ("\\bfseries CẦN THẦY CHỐT", "red!14", "\\itshape chưa chốt",
                      "\\itshape chưa chốt"),
}

_TEN_KHOI = {"lop-6": "LỚP 6", "lop-7": "LỚP 7", "lop-8": "LỚP 8", "lop-9": "LỚP 9"}


def bang_khoi(ma_khoi: str, khoi: dict, so_mt: dict) -> str:
    rows = []
    for c in khoi["chuong"]:
        nhan, mau, tyle, dong_phieu = _KL[c.get("muc_do", "chi-TH")]
        n = c.get("so_de_co_vdc", c.get("so_cau_vdc_tho_ban_0_3", 0))
        # Bản 0.4: cột tỉ lệ in ĐÚNG phân bổ của chương (khối 55% chia theo tần suất VDC).
        v = c.get("vdc") or {}
        pb = v.get("phan_bo_55")
        if pb and c.get("muc_do") != "chi-TH":
            tyle = (f"NB 15\\% · TH 30\\% · \\textbf{{VD {pb['VD']}\\% · VDC {pb['VDC']}\\%}}")
        if v.get("p") is not None:
            t = v["tan_suat"]
            # `\\` trong ô p{} sẽ NGẮT DÒNG BẢNG — phải dùng \newline.
            nhan += (f"\\newline{{\\scriptsize $p=\\mathbf{{{v['p']:.2f}}}$".replace(".", "{,}")
                     + f" ({tex(v['nhom_uu_tien'])})\\newline "
                     f"cuối đề {t['cau_cuoi_de']['so_de']}/{t['cau_cuoi_de']['tong_de']} · "
                     f"ý cuối hình {t['y_cuoi_bai_hinh']['so_de']}/"
                     f"{t['y_cuoi_bai_hinh']['tong_de']}\\newline "
                     f"trần \\textbf{{{str(v['tran_diem']).replace('.', '{,}')}}} · "
                     f"{tex(v['muc_tieu_vdc'])}}}")
        # Bằng chứng nay là ĐỀ BÀI THẬT ở vị trí VDC, không phải cột 'Vận dụng' của ma trận.
        if c.get("ghi_chu_can_chot"):
            bc = "\\bfseries " + tex(c["ghi_chu_can_chot"])
        elif n:
            vd = " \\quad ".join("``" + tex(x, 150) + "''" for x in c.get("vdc_vi_du", []))
            ng = tex(", ".join(c.get("vdc_nguon", [])), 90)
            bc = (f"\\textbf{{{n} đề có câu VDC ở vị trí này}}"
                  + (f" (nguồn: {ng})" if ng.strip() else "") + ". " + vd)
        else:
            bc = tex(c["bang_chung"])
        rows.append(
            f"\\rowcolor{{{mau}}}\n"
            f"{tex(c['ma'])} & {tex(c['ten'])} & {nhan} & {tyle} & {dong_phieu} & "
            f"{{\\scriptsize {bc}}} \\\\")
    dem = {}
    for c in khoi["chuong"]:
        dem[c.get("muc_do", "chi-TH")] = dem.get(c.get("muc_do", "chi-TH"), 0) + 1
    tom = (f"{dem.get('TH-VD-VDC',0)} chương TH+VD+VDC · {dem.get('TH-VD',0)} chương TH+VD · "
           f"{dem.get('chi-TH',0)} chương chỉ TH (gộp 2 phiếu) · "
           f"{dem.get('can-Thay-chot',0)} cần Thầy chốt")
    return (
        f"\\tmsec{{{_TEN_KHOI[ma_khoi]} — {tex(khoi['bo_sach'])} · {tom}}}\n"
        "\\begin{longtable}{@{}p{0.9cm}p{4.0cm}p{3.2cm}p{3.3cm}p{2.3cm}p{9.0cm}@{}}\n"
        "\\toprule\n"
        "\\tmlbl{Ch.} & \\tmlbl{Tên chương} & \\tmlbl{Kết luận} & "
        "\\tmlbl{Tỉ lệ phiếu tầng B} & \\tmlbl{Đóng phiếu} & "
        "\\tmlbl{Bằng chứng (ma trận trường công bố kèm đề)} \\\\\n"
        "\\midrule\n\\endhead\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{longtable}\n")


def main() -> int:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    so_mt = d["nguon"]["so_ma_tran_doc_duoc"]
    q = d["quy_uoc"]
    qu = d["quy_uoc_phan_muc"]

    parts = [
        "\\tmtitle{BẢN ĐỒ VD/VDC THEO CHƯƠNG — KHỐI 6·7·8·9}\\par",
        f"\\tmsub{{Nguồn sự thật chọn tỉ lệ thời lượng cho PHIẾU HỌC LIỆU TẦNG B "
        f"\\;·\\; bản {tex(d['phien_ban'])} \\;·\\; {tex(d['ngay'])}}}\\par\\vspace{{4pt}}",
        f"{{\\setlength{{\\fboxsep}}{{5pt}}\\colorbox{{red!12}}{{\\parbox{{\\linewidth}}"
        f"{{\\bfseries {tex(d['trang_thai'])}}}}}}}\\par",

        "\\tmsec{Luật đóng phiếu tầng B — Thầy chốt 30/08/2026}",
        "\\begin{itemize}"
        "\\item \\tmlbl{Chương KHÔNG có bài VD--VDC trong đề thi:} "
        f"Nhận biết {q['ty_le_khong_vd']['NB']}\\% thời lượng · Thông hiểu "
        f"{q['ty_le_khong_vd']['TH']}\\%; phần NB gồm \\tmlbl{{{'~'}5 dạng, mỗi dạng 2 câu}} "
        "($\\approx$10 câu --- ràng buộc CỨNG, tỉ lệ 30\\% chỉ để tham chiếu). "
        "\\tmlbl{GỘP 2 PHIẾU THÀNH 1} (một phiếu dạy trong 2 buổi): buổi 1 gánh "
        "15\\% NB $+$ 35\\% TH, buổi 2 gánh 15\\% NB $+$ 35\\% TH."
        "\\item \\tmlbl{Chương CÓ VD--VDC trong đề thi:} "
        f"Nhận biết {q['ty_le_co_vd']['NB']}\\% · Thông hiểu {q['ty_le_co_vd']['TH']}\\% · "
        f"\\tmlbl{{Vận dụng \\& VDC {q['ty_le_co_vd']['VD']}\\%}} (gộp chung, không tách). "
        "Mỗi phiếu vẫn là một buổi."
        "\\item Dạng \\tmlbl{Vận dụng} (không phải VDC): phiếu phải có phần "
        "\\tmlbl{quy trình giải bài} ngay ở từng bài."
        "\\item Phiếu \\tmlbl{ôn tập chương}: thêm bài tập cho HS \\tmlbl{tự viết lại và "
        "giải thích quy trình} làm bài."
        "\\end{itemize}",

        "\\tmsec{BẢN 0.4 --- Thầy chốt 04/09/2026: chỉ CÂU CUỐI mới tính VDC, "
        "và ưu tiên theo TẦN SUẤT}",
        "\\begin{itemize}"
        "\\item \\tmlbl{Chỉ ý cuối mới là VDC:} một BÀI nhiều ý (bài hình a,b,c) chỉ có "
        "\\tmlbl{ĐÚNG MỘT} ý mức VDC --- ý cuối; các ý trước là TH hoặc VD. Áp cho cả cách "
        "đếm kho đề ở bảng này lẫn cách gắn thẻ trong phiếu (cổng "
        "\\texttt{check\\_vdc\\_cuoi\\_bai})."
        "\\item \\tmlbl{Đếm bằng TẦN SUẤT, không đếm số câu thô:} $p$ = số ĐỀ mà chương chiếm "
        "một trong hai vị trí VDC, chia cho số đề của các kỳ kiểm tra chương đó. Mẫu lớp 9: "
        "\\tmlbl{21 đề GK1/CK1 đủ 9--10,5 điểm} $+$ \\tmlbl{14 đề GK2/CK2} phân loại bằng mắt "
        "(\\texttt{vdc-phan-loai-hk2.json}, \\tmlbl{chờ Thầy duyệt}). Đo lại: "
        "\\texttt{scripts/tan\\_suat\\_vdc.py}."
        "\\item \\tmlbl{Chương VDC hay ra thì được nhiều phút VDC hơn:} $p\\ge0{,}50$ $\\to$ "
        "VD 35\\% · VDC 20\\%; $0{,}20\\le p<0{,}50$ $\\to$ 43/12; $0<p<0{,}20$ $\\to$ 50/5 "
        "(5\\% của 120$'$ là 6$'$, chưa đủ một câu VDC 18$'$ $\\Rightarrow$ dồn VDC vào phiếu ôn tập chương); "
        "$p=0$ $\\to$ 55/0. \\tmlbl{Tổng luôn là 55\\%.}"
        "\\item \\tmlbl{Trần điểm là đích của phiếu:} GK1/CK1 $\\to$ \\tmlbl{10,0} (dạy HẾT, kể cả "
        "câu nâng cao 0,5đ cuối đề); GK2/CK2 $\\to$ \\tmlbl{9,5} --- nhường 0,5đ ở \\tmlbl{ý cuối "
        "bài hình}, vẫn dạy tới đó nhưng đích là \\tmlbl{ăn điểm từng phần}."
        "\\item \\tmlbl{Phát hiện chính (lớp 9):} \\tmlbl{27/33 đề (82\\%)} kết thúc bằng bài "
        "\\tmlbl{CỰC TRỊ/TỐI ƯU 0,5đ} --- một khuôn lặp (gọi ẩn $\\to$ lập biểu thức $\\to$ đưa về "
        "$(x-a)^2+b$ hoặc Cô-si $\\to$ kết luận), \\tmlbl{dạy được}. Và \\tmlbl{34/34} ý cuối bài "
        "hình là câu CHỨNG MINH nhiều bước: thẳng hàng 8 · vuông góc 5 · song song--đồng dạng 4 "
        "· hệ thức 4."
        "\\item \\tmlbl{Khối 6, 7, 8 CHƯA ĐO ĐƯỢC} tần suất (kho đề chưa có bank chấm band; "
        "69/161 bản ghi câu cuối đề còn để chương ``?'' và toàn bộ 80 bản ghi ý cuối bài hình "
        "chưa gán chương) $\\Rightarrow$ giữ 15--30--55 mặc định, \\tmlbl{không bịa số}."
        "\\end{itemize}",

        "\\tmsec{Quy ước chấm mức độ — anh An chốt 30/08/2026 (ĐÈ LÊN mức trường ghi)}",
        "\\begin{itemize}"
        f"\\item \\tmlbl{{Cách kiểm:}} {tex(qu['cach_kiem'])}"
        f"\\item \\tmlbl{{Lỗi bản 0.2 đã sửa:}} {tex(qu['loi_da_sua'])}"
        f"\\item \\tmlbl{{Thực tế 2--3 bước là THÔNG HIỂU:}} {tex(qu['thuc_te_2_3_buoc_la_TH'])}"
        f"\\item \\tmlbl{{VDC chỉ ở hai chỗ:}} {tex(qu['VDC_chi_o_hai_cho'])} "
        f"{tex(qu['VDC_lop_6'])}"
        f"\\item \\tmlbl{{Hệ quả:}} {tex(qu['he_qua'])}"
        "\\end{itemize}",

        "\\tmsec{Cách dựng bảng này --- và chỗ nào chưa chắc}",
        "\\begin{itemize}"
        f"\\item \\tmlbl{{Kho đề:}} {tex(d['nguon']['kho_de'])}"
        f"\\item \\tmlbl{{Bằng chứng:}} {tex(d['nguon']['bang_chung_chinh'])}"
        f"\\item \\tmlbl{{Đối chứng lớp 9:}} {tex(d['nguon']['doi_chung_lop_9'])}"
        f"\\item \\tmlbl{{Lưu ý:}} {tex(d['nguon']['luu_y_CV7991'])}"
        "\\item \\tmlbl{Dòng đỏ ``CẦN THẦY CHỐT'':} \\tmlbl{chưa chốt thì chưa soạn phiếu} cho "
        "chương đó, vì chọn nhầm tỉ lệ là lệch cả buổi. Bản 0.3 có \\tmlbl{2 dòng}: lớp 7 "
        "chương III và lớp 8 chương VIII (lí do ghi ngay ở cột bằng chứng)."
        "\\end{itemize}",
    ]
    for ma in ("lop-9", "lop-8", "lop-7", "lop-6"):
        parts.append(bang_khoi(ma, d["khoi"][ma], so_mt))

    parts.append(
        "\\tmsec{Thầy \\& sếp cần soi kỹ chỗ này}"
        "\\begin{itemize}"
        "\\item \\tmlbl{Hai dòng đỏ} con chưa dám chốt: \\tmlbl{lớp 7 chương III} (ý cuối bài "
        "hình GK1 lớp 7 thường chỉ là tính số đo góc) và \\tmlbl{lớp 8 chương VIII} (câu ``bốc "
        "ít nhất bao nhiêu viên bi'' là toán tư duy chứ không phải xác suất)."
        "\\item \\tmlbl{Chương VI lớp 9} (hàm số $y=ax^2$ và PT bậc hai) nay là \\tmlbl{TH $+$ VD}, "
        "KHÔNG có VDC --- hai câu con từng tính là VDC hoá ra là bài lập phương trình 1,0đ trong "
        "file trích một phần, chính ngân hàng cũng gắn band VD."
        "\\item Xem \\tmlbl{đề bài nguyên văn} của cả 157 câu ở vị trí VDC trong "
        "\\texttt{outputs/trich-vdc/trich-vdc.pdf} --- 26 câu con chưa gán chắc chương, bôi đỏ."
        "\\item Duyệt xong, con khoá số vào \\texttt{config/ban\\_do\\_vd\\_vdc.json}; cổng "
        "\\texttt{thuyetminh\\_gate} đã tự soi tỉ lệ, số ca (gộp phiếu), quy trình giải bài "
        "và bài tự viết lại quy trình."
        "\\end{itemize}")

    body = "\n\n".join(parts)
    tex_src = _env().get_template("base_thuyetminh.tex.j2").render(body=body, **load_tokens())
    pdf = build_pdf(tex_src, slug="ban-do-vd-vdc", filename="ban-do-vd-vdc",
                    out_root=settings.OUTPUTS_DIR, force=True)
    print("✓", pdf.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
