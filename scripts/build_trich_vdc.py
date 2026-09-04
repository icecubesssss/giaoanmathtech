#!/usr/bin/env python3
"""Dựng PDF 'TRÍCH XUẤT CÂU VDC' — in NGUYÊN VĂN đề bài để Thầy kiểm có thật là VDC không.

Anh An chốt 30/08/2026: chỉ CÂU CUỐI BÀI HÌNH và CÂU NÂNG CAO CUỐI ĐỀ mới là VDC
(lớp 6 chỉ câu cuối đề). Bản này KHÔNG dùng cột 'Vận dụng' của ma trận trường nữa mà
đi thẳng vào ĐỀ BÀI ở đúng hai vị trí đó.

Hai nguồn:
  • Lớp 9 học kì I — ngân hàng câu `inputs/refs/de-thi/lop-9/exams/` (21 đề ĐẦY ĐỦ
    10 điểm, đã tách từng ý nên chỉ ra được cả 'ý cuối bài hình').
  • Bốn khối 6-7-8-9 — trích câu cuối đề từ text PDF (`scripts/trich_cau_cuoi_de.py`),
    chỉ giữ mốc 'Bài' có ghi điểm ≤ 1,0 (đúng khuôn câu phân loại).

Dùng:  .venv/bin/python scripts/build_trich_vdc.py
Ra:    outputs/trich-vdc/trich-vdc.pdf
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import settings                                    # noqa: E402
from src.compiler.jinja_renderer import _env, load_tokens      # noqa: E402
from src.compiler.latex_builder import build_pdf               # noqa: E402

BANK = ROOT / "inputs" / "refs" / "de-thi" / "lop-9" / "exams"
CAU_CUOI = ROOT / "inputs" / "refs" / "de-thi" / "cau-cuoi-de.json"
BAN_DO = ROOT / "config" / "ban_do_vd_vdc.json"

_ESC = {"\\": " ", "&": r"\&", "%": r"\%", "$": " ", "#": r"\#", "_": r"\_",
        "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
HINH = {"C4", "C5", "C9-TRONTIEP", "C10-HINHKHOI"}
MA_CHUONG = {"C1": "I", "C2": "II", "C3": "III", "C4": "IV", "C5": "V",
             "C6-PTBH": "VI", "C7-TANSO": "VII", "C8-XACSUAT": "VIII",
             "C9-TRONTIEP": "IX", "C10-HINHKHOI": "X", "C6": "VII", "C7": "VIII"}
TEN_KHOI = {"lop-6": "LỚP 6", "lop-7": "LỚP 7", "lop-8": "LỚP 8", "lop-9": "LỚP 9"}


def tex(s: str, n: int = 460) -> str:
    s = re.sub(r"\s+", " ", str(s))[:n]
    return "".join(_ESC.get(c, c) for c in s)


def _so_bai(c: dict) -> str:
    b = c.get("bai")
    if b:
        return str(b)
    m = re.search(r"-(\d+)(?:[-.]|$)", c.get("id", ""))
    return m.group(1) if m else "?"


def tu_bank() -> list[dict]:
    """Câu VDC của lớp 9 HK1 từ ngân hàng — chỉ lấy ĐỀ ĐẦY ĐỦ (tổng 9-10,5đ)."""
    ra = []
    for f in sorted(BANK.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        cau = d.get("cau", [])
        tong = sum(c.get("diem") or 0 for c in cau)
        if not (9.0 <= tong <= 10.5):       # <9đ = trích một phần; >10,5đ = file GỘP nhiều đề
            continue
        bai: dict[str, list] = {}
        thu_tu: list[str] = []
        for i, c in enumerate(cau):
            b = _so_bai(c)
            if b not in bai:
                bai[b] = []
                thu_tu.append(b)
            bai[b].append((i, c))
        bai_cuoi = thu_tu[-1]
        for b in thu_tu:
            items = bai[b]
            i_cuoi = items[-1][0]
            diem_bai = sum((c.get("diem") or 0) for _, c in items)
            for i, c in items:
                diem = c.get("diem") or 0
                cuoi_de = (b == bai_cuoi and i == i_cuoi and diem <= 1.0)
                cuoi_hinh = (c.get("chuong") in HINH and i == i_cuoi
                             and len(items) >= 2 and diem_bai >= 2.0)
                if not (cuoi_de or cuoi_hinh):
                    continue
                ra.append({
                    "lop": "lop-9", "ky": f.stem.split("-")[0],
                    "chuong": MA_CHUONG.get(c.get("chuong"), c.get("chuong") or "?"),
                    "vitri": "câu cuối đề" if cuoi_de else "ý cuối bài hình",
                    "nguon": f.stem, "nhan": f"Bài {b}", "diem": diem,
                    "text": c.get("de") or ""})
    return ra


# Bài HÌNH của mỗi (khối, kỳ) thuộc chương nào — theo tiến độ SGK KNTT.
# Chỉ dùng để gán chương cho "ý cuối bài hình"; đề bài in nguyên văn để Thầy đối chiếu.
HINH_THEO_KY = {
    ("lop-7", "gk1"): "III", ("lop-7", "ck1"): "IV",
    ("lop-7", "gk2"): "IX",  ("lop-7", "ck2"): "IX",
    ("lop-8", "gk1"): "III", ("lop-8", "ck1"): "III",
    ("lop-8", "gk2"): "IX",  ("lop-8", "ck2"): "IX",
    ("lop-9", "gk1"): "IV",  ("lop-9", "ck1"): "V",
    ("lop-9", "gk2"): "IX",  ("lop-9", "ck2"): "IX",
}


def tu_text() -> list[dict]:
    """Câu cuối đề của cả 4 khối, trích từ text PDF."""
    if not CAU_CUOI.exists():
        return []
    d = json.loads(CAU_CUOI.read_text(encoding="utf-8"))
    ra = []
    for r in d:
        vt = r.get("vitri", "câu cuối đề")
        if vt == "ý cuối bài hình":
            # Anh An: LỚP 6 chỉ có câu cuối đề mới là VDC. Dữ liệu cũng cho thấy đúng vậy —
            # ý cuối bài hình lớp 6 chỉ là tính số viên gạch / diện tích, mức Thông hiểu.
            if r["lop"] == "lop-6":
                continue
            if r["lop"] == "lop-9" and r["ky"] in ("gk1", "ck1"):
                continue                    # HK1 đã có từ bank (tách sẵn từng ý); HK2 lấy ở đây
            ch = HINH_THEO_KY.get((r["lop"], r["ky"]), "?")
        else:
            if not (r.get("diem") and r["diem"] <= 1.0):
                continue
            if r["lop"] == "lop-9" and r["ky"] in ("gk1", "ck1"):
                continue                    # đã có từ bank, chuẩn hơn
            ch = r.get("chuong", "?")
        ra.append({"lop": r["lop"], "ky": r["ky"], "chuong": ch, "vitri": vt,
                   "nguon": r["file"].replace(".pdf", ""), "nhan": r["nhan"],
                   "diem": r.get("diem") or 0, "text": r["text"]})
    return ra


def bang_trich(rows: list[dict]) -> str:
    out = []
    for lop in ("lop-9", "lop-8", "lop-7", "lop-6"):
        sel = [r for r in rows if r["lop"] == lop]
        if not sel:
            continue
        sel.sort(key=lambda r: (str(r["chuong"]), r["nguon"]))
        dem = Counter(r["chuong"] for r in sel)
        tom = " · ".join(f"ch.{k}: {v}" for k, v in sorted(dem.items(), key=lambda x: str(x[0])))
        out.append(f"\\tmsec{{{TEN_KHOI[lop]} — {len(sel)} câu ở vị trí VDC ({tom})}}")
        out.append("\\begin{longtable}{@{}p{1.1cm}p{2.6cm}p{5.2cm}p{15.6cm}@{}}\n\\toprule\n"
                   "\\tmlbl{Ch.} & \\tmlbl{Vị trí} & \\tmlbl{Đề nguồn} & "
                   "\\tmlbl{ĐỀ BÀI (nguyên văn — Thầy chấm lại mức độ)} \\\\\n"
                   "\\midrule\n\\endhead")
        for r in sel:
            mau = "red!10" if r["chuong"] == "?" else "stage3!8"
            out.append(f"\\rowcolor{{{mau}}}\n{tex(r['chuong'], 12)} & "
                       f"{{\\scriptsize {tex(r['vitri'], 20)} · {r['diem']}đ}} & "
                       f"{{\\scriptsize {tex(r['nguon'], 46)}}} & "
                       f"{{\\scriptsize {tex(r['text'])}}} \\\\")
        out.append("\\bottomrule\n\\end{longtable}\n")
    return "\n".join(out)


def bang_phan_loai(rows: list[dict]) -> str:
    """Chương nào chỉ TH · TH+VD · TH+VD+VDC — VDC lấy từ chính bảng trích trên."""
    d = json.loads(BAN_DO.read_text(encoding="utf-8"))
    co_vdc = defaultdict(set)
    for r in rows:
        if r["chuong"] != "?":
            co_vdc[r["lop"]].add(str(r["chuong"]))
    out = ["\\tmsec{PHÂN LOẠI CHƯƠNG — chỉ TH · TH+VD · TH+VD+VDC}",
           "\\begin{longtable}{@{}p{1.4cm}p{1.1cm}p{6.4cm}p{4.4cm}p{10.8cm}@{}}\n\\toprule\n"
           "\\tmlbl{Khối} & \\tmlbl{Ch.} & \\tmlbl{Tên chương} & \\tmlbl{Nhóm} & "
           "\\tmlbl{Căn cứ} \\\\\n\\midrule\n\\endhead"]
    for lop in ("lop-9", "lop-8", "lop-7", "lop-6"):
        for c in d["khoi"][lop]["chuong"]:
            ma = c["ma"]
            vdc = ma in co_vdc[lop]
            if vdc:
                nhom, mau = "\\bfseries TH $+$ VD $+$ VDC", "stage4!14"
                cc = f"Có {sum(1 for r in rows if r['lop']==lop and str(r['chuong'])==ma)} câu ở vị trí VDC (xem phần trích)."
            elif c["co_vd"] is True:
                nhom, mau = "TH $+$ VD", "stage3!10"
                cc = "Ma trận có cột Vận dụng nhưng KHÔNG có câu nào ở vị trí VDC trong mẫu soi được."
            else:
                nhom, mau = "chỉ TH (và NB)", "stage1!10"
                cc = "Không có câu cuối đề / ý cuối bài hình nào thuộc chương này; các câu 'Vận dụng' trường ghi đều là thực tế 2--3 bước."
            out.append(f"\\rowcolor{{{mau}}}\n{TEN_KHOI[lop][4:]} & {tex(ma,8)} & "
                       f"{{\\scriptsize {tex(c['ten'],70)}}} & {nhom} & {{\\scriptsize {cc}}} \\\\")
    out.append("\\bottomrule\n\\end{longtable}\n")
    return "\n".join(out)


def main() -> int:
    rows = tu_bank() + tu_text()
    parts = [
        "\\tmtitle{TRÍCH XUẤT CÂU VDC — ĐỂ THẦY KIỂM}\\par",
        "\\tmsub{Đề bài NGUYÊN VĂN ở đúng hai vị trí anh An quy ước là VDC "
        "\\;·\\; khối 6·7·8·9 \\;·\\; 2026-08-30}\\par\\vspace{4pt}",
        "\\tmsec{Cách lấy — và chỗ con đã làm sai ở bản trước}",
        "\\begin{itemize}"
        "\\item \\tmlbl{Quy ước:} VDC $=$ câu cuối của BÀI HÌNH, hoặc câu nâng cao CUỐI ĐỀ "
        "(lớp 6 chỉ câu cuối đề). Bản này đi thẳng vào đề bài ở hai vị trí đó, "
        "\\tmlbl{không dùng cột ``Vận dụng'' của ma trận trường} nữa."
        "\\item \\tmlbl{Lỗi bản 0.2:} con lấy ``câu cuối'' theo thứ tự trong file ngân hàng, "
        "trong khi 24/45 file chỉ là TRÍCH MỘT PHẦN đề (dưới 10 điểm) và 1 file là GỘP nhiều "
        "đề. Vì vậy có câu chỉ ở mức Thông hiểu bị gán nhầm VDC --- ví dụ chương VII lớp 9 "
        "``lập bảng tần số, tìm tần số tương đối''. Nay chỉ dùng \\tmlbl{21 đề ĐẦY ĐỦ 10 điểm}."
        "\\item \\tmlbl{Phạm vi số liệu:} ngân hàng câu đầy đủ của lớp 9 mới phủ \\tmlbl{GK1 và "
        "CK1} (chương I--V). Chương VI--X và cả ba khối 6, 7, 8 lấy bằng cách trích câu cuối đề "
        "từ text PDF, nên chỉ đọc được đề nào có lớp text."
        "\\item \\tmlbl{Dòng đỏ ``?''} là câu con chưa gán chắc chương --- xin Thầy điền giúp."
        "\\end{itemize}",
    ]
    parts.append(bang_phan_loai(rows))
    parts.append("\\newpage")
    parts.append(bang_trich(rows))

    body = "\n\n".join(parts)
    tex_src = _env().get_template("base_thuyetminh.tex.j2").render(body=body, **load_tokens())
    pdf = build_pdf(tex_src, slug="trich-vdc", filename="trich-vdc",
                    out_root=settings.OUTPUTS_DIR, force=True)
    print(f"✓ {len(rows)} câu → {pdf.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
