#!/usr/bin/env python3
"""Ghép các tab-*.json của tieu_hoc_phan_dang.py thành một .xlsx (để tải lên Drive, chuyển Google Sheets).

    .venv/bin/python scripts/tieu_hoc_xlsx.py --lop 3
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
TABS = [("tab-de-thi", "Đề thi và nguồn", 1, {"A": 26, "D": 26, "E": 12, "I": 16, "J": 16, "K": 12, "L": 40, "M": 60}),
        ("tab-phan-dang", "Phân dạng", 1, {"A": 30, "B": 24, "E": 60, "I": 34, "L": 32, "N": 18, "O": 30, "R": 36, "S": 40, "V": 24, "W": 14, "X": 24}),
        ("tab-thong-ke-dang", "Thống kê dạng", 4, {"A": 52, "B": 12}),
        ("tab-thong-ke-chu-de", "Thống kê chủ đề", 4, {"A": 26, "B": 50, "C": 14}),
        ("tab-tien-do", "Tiến độ KNTT", 1, {"B": 46, "D": 62, "E": 14, "F": 60})]
HEAD = PatternFill("solid", fgColor="1F3864")
INPUT = PatternFill("solid", fgColor="FFF2CC")


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--lop", type=int, required=True); a = ap.parse_args()
    src = ROOT / f"outputs/ngan-hang-sheet/tieu-hoc/lop-{a.lop}"
    wb = Workbook(); wb.remove(wb.active)
    for key, title, hrow, widths in TABS:
        rows = json.loads((src / f"{key}.json").read_text(encoding="utf-8"))
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(r)
        ws.freeze_panes = ws.cell(row=hrow + 1, column=1)
        for c in ws[hrow]:
            c.font = Font(bold=True, color="FFFFFF"); c.fill = HEAD
            c.alignment = Alignment(wrap_text=True, vertical="center")
        for row in ws.iter_rows(min_row=hrow + 1):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        for col in range(1, ws.max_column + 1):
            L = get_column_letter(col)
            ws.column_dimensions[L].width = widths.get(L, 11)
        if key.startswith("tab-thong-ke"):
            ws["A1"].font = Font(bold=True); ws["B1"].fill = INPUT; ws["A2"].font = Font(bold=True)
            pct = "E" if key == "tab-thong-ke-dang" else "F"
            for c in ws[pct][hrow:]:
                c.number_format = "0%"
            for c in ws["G" if key == "tab-thong-ke-dang" else "H"][hrow:]:
                c.number_format = "0.00"
    out = src / f"Phan-dang-Toan{a.lop}-tieu-hoc.xlsx"
    wb.save(out); print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
