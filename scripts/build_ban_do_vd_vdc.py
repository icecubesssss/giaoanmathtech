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


def tex(s: str, n: int | None = None) -> str:
    """Escape sang LaTeX; `n` cắt bớt độ dài (trích dẫn đề bài in trong ô bảng)."""
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", str(s))     # bỏ lệnh LaTeX trong đề gốc (\widehat, \dfrac…)
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
        n = c.get("so_cau_vdc", 0)
        # Bằng chứng nay là ĐỀ BÀI THẬT ở vị trí VDC, không phải cột 'Vận dụng' của ma trận.
        if c.get("ghi_chu_can_chot"):
            bc = "\\bfseries " + tex(c["ghi_chu_can_chot"])
        elif n:
            vd = " \\quad ".join("``" + tex(x, 150) + "''" for x in c.get("vdc_vi_du", []))
            bc = (f"\\textbf{{{n} câu ở vị trí VDC}} (nguồn: "
                  + tex(", ".join(c.get("vdc_nguon", [])), 90) + "). " + vd)
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
        "\\begin{longtable}{@{}p{0.9cm}p{4.6cm}p{2.3cm}p{3.4cm}p{2.5cm}p{9.6cm}@{}}\n"
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
