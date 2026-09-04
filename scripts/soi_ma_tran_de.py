#!/usr/bin/env python3
"""Trích MA TRẬN (bảng 'câu → kiến thức → mức độ') từ kho đề THCS đã tải về.

VÌ SAO: để trả lời "chương nào CÓ bài Vận dụng / Vận dụng cao trong đề thi" thì
BẰNG CHỨNG TỐT NHẤT là chính bảng ma trận mà trường công bố kèm đề — không phải AI
đoán mức độ. Script chỉ ĐỌC những gì đề ghi, câu nào đề không ghi thì bỏ, không suy diễn.

Hai khuôn ma trận gặp trong kho:
  (1) khuôn DÒNG   — "Câu 3 (0,25 điểm)  Xác suất thực nghiệm …   Nhận biết"
  (2) khuôn LƯỚI   — bảng TT | Chương/Chủ đề | Nội dung | NB | TH | VD | VDC (đếm câu)
Bản này đọc khuôn (1) trước (rõ ràng, ít nhiễu); khuôn (2) trích riêng ở `--luoi`.

Dùng:
    .venv/bin/python scripts/soi_ma_tran_de.py                 # trích + ghi JSON
    .venv/bin/python scripts/soi_ma_tran_de.py --lieu-ke       # liệt kê cụm 'kiến thức'
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DE = ROOT / "inputs" / "refs" / "de-thi"
CACHE = ROOT / "storage" / "cache" / "de-txt"
OUT_JSON = ROOT / "inputs" / "refs" / "de-thi" / "ma-tran-trich-xuat.json"

KY_DIR = {"giua-ki-1": "gk1", "cuoi-ki-1": "ck1", "giua-ki-2": "gk2",
          "cuoi-ki-2": "ck2", "de-cuoi-ki-2": "ck2", "de-giua-ki-1": "gk1"}

BO_SACH = [
    ("kntt", re.compile(r"kết\s*nối\s*tri\s*thức", re.I)),
    ("canh-dieu", re.compile(r"cánh\s*diều", re.I)),
    ("ctst", re.compile(r"chân\s*trời\s*sáng\s*tạo", re.I)),
]

MUC = {"nhận biết": "NB", "thông hiểu": "TH", "vận dụng cao": "VDC", "vận dụng": "VD"}
_MUC_RE = re.compile(r"(vận\s*dụng\s*cao|vận\s*dụng|thông\s*hiểu|nhận\s*biết)\s*$", re.I)
_DONG_RE = re.compile(
    r"^\s*(?P<loai>Câu|Bài)\s*(?P<so>\d+)\s*\((?P<diem>[\d,\.]+)\s*(?:điểm|đ)\)\s*"
    r"(?P<kt>.+?)\s{2,}(?P<muc>Vận\s*dụng\s*cao|Vận\s*dụng|Thông\s*hiểu|Nhận\s*biết)\s*$",
    re.I | re.M)


def _txt(pdf: Path) -> str:
    """Text của PDF (cache ra storage/cache/de-txt/…)."""
    rel = pdf.relative_to(DE)
    dest = CACHE / rel.with_suffix(".txt")
    if not dest.exists() or dest.stat().st_mtime < pdf.stat().st_mtime:
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftotext", "-layout", str(pdf), str(dest)],
                       capture_output=True, check=False)
    try:
        return dest.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def bo_sach(t: str) -> str:
    for ten, rx in BO_SACH:
        if rx.search(t):
            return ten
    return "chua-ro"


def ky_thi(pdf: Path) -> str:
    for phan in pdf.parts:
        if phan in KY_DIR:
            return KY_DIR[phan]
    return "?"


def trich_ma_tran(t: str) -> list[dict]:
    """Các dòng ma trận khuôn (1). Trả [] nếu đề không kèm ma trận."""
    m = re.search(r"MA\s*TRẬN|BẢNG\s*ĐẶC\s*TẢ", t, re.I)
    if not m:
        return []
    khoi = t[m.start():]
    ra = []
    for d in _DONG_RE.finditer(khoi):
        kt = re.sub(r"\s+", " ", d.group("kt")).strip(" .")
        if len(kt) < 4:
            continue
        ra.append({
            "cau": f"{d.group('loai')} {d.group('so')}",
            "diem": float(d.group("diem").replace(",", ".")),
            "kien_thuc": kt,
            "muc": MUC[re.sub(r"\s+", " ", d.group("muc")).lower()],
        })
    return ra


def quet() -> list[dict]:
    ho_so = []
    for pdf in sorted(DE.rglob("*.pdf")):
        lop = next((p for p in pdf.parts if p.startswith("lop-")), "?")
        t = _txt(pdf)
        if len(t.replace(" ", "")) < 400:
            continue                                   # PDF ảnh, không có lớp text
        rows = trich_ma_tran(t)
        ho_so.append({
            "file": str(pdf.relative_to(ROOT)),
            "lop": lop, "ky": ky_thi(pdf), "bo_sach": bo_sach(t),
            "co_ma_tran": bool(rows), "dong": rows,
        })
    return ho_so


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lieu-ke", action="store_true", help="in các cụm 'kiến thức' hay gặp")
    args = ap.parse_args(argv[1:])

    ho_so = quet()
    OUT_JSON.write_text(json.dumps(ho_so, ensure_ascii=False, indent=1), encoding="utf-8")

    dem = defaultdict(Counter)
    for h in ho_so:
        dem[h["lop"]][h["ky"]] += 1
        if h["co_ma_tran"]:
            dem[h["lop"]][h["ky"] + "+mt"] += 1
        dem[h["lop"]]["bo:" + h["bo_sach"]] += 1
    print(f"Đọc {len(ho_so)} đề có lớp text → {OUT_JSON.relative_to(ROOT)}\n")
    for lop in sorted(dem):
        c = dem[lop]
        print(f"{lop}: " + "  ".join(f"{k.upper()} {c[k]}(mt {c[k+'+mt']})"
                                     for k in ("gk1", "ck1", "gk2", "ck2"))
              + "   | " + " ".join(f"{k[3:]}={v}" for k, v in c.items() if k.startswith("bo:")))

    if args.lieu_ke:
        for lop in sorted(dem):
            kt = Counter(r["kien_thuc"] for h in ho_so if h["lop"] == lop for r in h["dong"])
            print(f"\n### {lop} — {len(kt)} cụm kiến thức khác nhau")
            for k, v in kt.most_common(40):
                print(f"  {v:>3}×  {k[:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
