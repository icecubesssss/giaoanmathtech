#!/usr/bin/env python3
"""Trích CÂU CUỐI ĐỀ (ứng viên VDC) từ kho đề đã tải — để Thầy soi đề bài thật.

VÌ SAO: anh An chốt 30/08/2026 "chỉ câu cuối bài hình và câu nâng cao cuối đề mới
được gọi là VDC". Muốn kiểm chương nào THẬT SỰ có VDC thì phải đọc chính ĐỀ BÀI của
câu cuối, chứ không tin cột 'Vận dụng' của ma trận trường.

Cách làm (không suy diễn):
  1. Cắt lấy phần ĐỀ (bỏ mọi thứ từ 'HƯỚNG DẪN CHẤM' / 'ĐÁP ÁN' / 'MA TRẬN' trở đi).
  2. Tìm mốc bài cuối cùng trong phần đề: 'Bài 5.', 'Câu V.', 'Bài IV', …
  3. In nguyên văn khối chữ đó ra để người đọc tự chấm mức độ.
Đề không có lớp text (PDF ảnh) thì bỏ qua — script KHÔNG đoán.

Dùng:
    .venv/bin/python scripts/trich_cau_cuoi_de.py --lop lop-9 --ky gk2 --so 12
    .venv/bin/python scripts/trich_cau_cuoi_de.py --json   # xuất tất cả ra JSON
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DE = ROOT / "inputs" / "refs" / "de-thi"
CACHE = ROOT / "storage" / "cache" / "de-txt"
OUT = ROOT / "inputs" / "refs" / "de-thi" / "cau-cuoi-de.json"

KY_DIR = {"giua-ki-1": "gk1", "cuoi-ki-1": "ck1", "giua-ki-2": "gk2",
          "cuoi-ki-2": "ck2", "de-cuoi-ki-2": "ck2"}

# Mọi thứ từ đây trở đi KHÔNG còn là đề nữa
_HET_DE = re.compile(r"HƯỚNG\s*DẪN\s*CHẤM|ĐÁP\s*ÁN|BIỂU\s*ĐIỂM|MA\s*TRẬN|ĐẶC\s*TẢ|"
                     r"BẢNG\s*NĂNG\s*LỰC|Xem\s*thêm\s*:", re.I)
# Mốc bài. KHÔNG bắt buộc đứng đầu dòng: pdftotext hay dán "II. PHẦN TỰ LUẬN: (7,0
# điểm) Bài 1 (1,5 điểm):" thành MỘT dòng, khiến mốc "Bài" của phần tự luận không khớp
# và script vớ phải câu trắc nghiệm cuối phần I. Cho phép mốc đứng sau dấu câu hoặc sau
# hai dấu cách, và cho phép số bài theo ngay bởi "(" (dạng "Bài 5 (0,5 điểm)").
_MOC = re.compile(r"(?:^|(?<=[.:;\)\]]\s)|(?<=\s{2}))(Bài|Câu)[ \t]*([0-9]{1,2}|[IVX]{1,5})"
                  r"[ \t]*[\.:\)\(]", re.M)
# Bài cuối của đề Hà Nội gần như luôn là câu phân loại 0,5-1,0đ
_DIEM = re.compile(r"\(\s*([\d,\.]+)\s*(?:điểm|đ)\s*\)")


def _txt(pdf: Path) -> str:
    dest = CACHE / pdf.relative_to(DE).with_suffix(".txt")
    if not dest.exists() or dest.stat().st_mtime < pdf.stat().st_mtime:
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftotext", "-layout", str(pdf), str(dest)],
                       capture_output=True, check=False)
    try:
        return dest.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def phan_de(t: str) -> str:
    """Phần ĐỀ: cắt trước mốc đáp án/ma trận đầu tiên nằm sau 20% đầu văn bản."""
    for m in _HET_DE.finditer(t):
        if m.start() > len(t) * 0.2:
            return t[:m.start()]
    return t


def cau_cuoi(t: str) -> dict | None:
    """Mốc cuối cùng của phần tự luận. Ưu tiên 'Bài' — phần trắc nghiệm đánh 'Câu 1..12'
    nên nếu lấy 'Câu' cuối là vớ phải câu trắc nghiệm chứ không phải câu phân loại."""
    de = phan_de(t)
    marks = list(_MOC.finditer(de))
    if not marks:
        return None
    bai = [m for m in marks if m.group(1) == "Bài"]
    m = bai[-1] if bai else marks[-1]
    khoi = de[m.start(): m.start() + 700]
    khoi = re.sub(r"[ \t]+", " ", khoi).strip()
    d = _DIEM.search(khoi[:120])
    return {"nhan": f"{m.group(1)} {m.group(2)}",
            "diem": float(d.group(1).replace(",", ".")) if d else None,
            "text": khoi}


_Y = re.compile(r"(?:^|\s)([a-d])\s*[\)\.]", re.M)
_HINH = re.compile(r"đường tròn|tam giác|tứ giác|hình vuông|hình thang|hình bình hành", re.I)


def y_cuoi_bai_hinh(t: str) -> dict | None:
    """Ý CUỐI của BÀI HÌNH — vị trí VDC thứ hai theo quy ước anh An.

    Bài hình nhận ra bằng từ khoá hình học + phải có từ 3 ý trở lên (bài 1-2 ý là bài
    tính toán ngắn, ý cuối của nó không phải câu phân loại)."""
    de = phan_de(t)
    marks = list(_MOC.finditer(de))
    for i, m in enumerate(marks):
        blk = de[m.start(): marks[i + 1].start() if i + 1 < len(marks) else len(de)]
        if not _HINH.search(blk):
            continue
        ys = list(_Y.finditer(blk))
        if len(ys) < 3:
            continue
        khoi = re.sub(r"[ \t]+", " ", blk[ys[-1].start():]).strip()
        return {"nhan": f"{m.group(1)} {m.group(2)}", "diem": None, "text": khoi[:500]}
    return None


def quet(lop: str | None, ky: str | None, so: int) -> list[dict]:
    ra: list[dict] = []
    dem: dict[tuple[str, str], int] = {}
    for pdf in sorted(DE.rglob("*.pdf")):
        g = next((p for p in pdf.parts if p.startswith("lop-")), "?")
        k = next((KY_DIR[p] for p in pdf.parts if p in KY_DIR), "?")
        if g in ("lop-10", "?") or k == "?":
            continue
        if (lop and g != lop) or (ky and k != ky):
            continue
        # CHỈ đề thi thật tải từ toanmath (slug 'de-…-ha-noi.pdf'). Kho còn lẫn ĐỀ CƯƠNG
        # ôn tập và đề bộ Cánh Diều — hai thứ đó không dùng để chấm mức độ được.
        if not (pdf.name.startswith("de-") and pdf.stem.endswith("-ha-noi")):
            continue
        if pdf.name.startswith(("de-cuong", "de-cuong-on")):
            continue                       # ĐỀ CƯƠNG ôn tập, không phải đề thi
        if dem.get((g, k), 0) >= so:
            continue
        t = _txt(pdf)
        if len(t.replace(" ", "")) < 400:
            continue                       # PDF ảnh — không đoán
        c = cau_cuoi(t)
        if c:
            ra.append({"lop": g, "ky": k, "file": pdf.name, "vitri": "câu cuối đề", **c})
        h = y_cuoi_bai_hinh(t)
        if h:
            ra.append({"lop": g, "ky": k, "file": pdf.name, "vitri": "ý cuối bài hình", **h})
        if c or h:
            dem[(g, k)] = dem.get((g, k), 0) + 1
    return ra


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop")
    ap.add_argument("--ky")
    ap.add_argument("--so", type=int, default=12, help="số đề mỗi (khối, kỳ)")
    ap.add_argument("--json", action="store_true", help="ghi ra inputs/refs/de-thi/cau-cuoi-de.json")
    ap.add_argument("--dai", type=int, default=320, help="số ký tự in mỗi câu")
    args = ap.parse_args(argv[1:])

    ra = quet(args.lop, args.ky, args.so)
    if args.json:
        OUT.write_text(json.dumps(ra, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {len(ra)} câu cuối đề → {OUT.relative_to(ROOT)}")
        return 0
    cur = None
    for r in ra:
        if (r["lop"], r["ky"]) != cur:
            cur = (r["lop"], r["ky"])
            print(f"\n{'='*96}\n{cur[0].upper()} · {cur[1].upper()}\n{'='*96}")
        d = f"{r['diem']}đ" if r["diem"] else "?đ"
        print(f"• [{r['nhan']} · {d}] {r['file'][:62]}")
        print(f"  {r['text'][:args.dai]}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
