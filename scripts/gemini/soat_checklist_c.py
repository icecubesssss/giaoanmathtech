#!/usr/bin/env python3
"""So tab checklist đã ghi (bản xuất xlsx) với kỳ vọng của lap_checklist_c.py.

    python3 scripts/gemini/soat_checklist_c.py <file.xlsx> 4c [5c 7c]

Soát: A/B/C đúng chữ, C có link đúng; D:U dòng phiếu là ô tích FALSE, dòng chương rỗng;
V đúng; W là GIÁ TRỊ (không còn công thức) và trùng nguyên văn ô gốc.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parents[2]
SOAT = REPO / "storage" / "gemini" / "soat"
TEN = {"4c": "QuyenHM - Checklist duyệt phiếu chi tiết 4C", "5c": "BichVN - Checklist duyệt phiếu chi tiết 5C",
       "7c": "AnDV - Checklist duyệt phiếu chi tiết 7C"}


def chuan(s):
    return "\n".join(x.rstrip() for x in str(s or "").replace("\r\n", "\n").split("\n")).strip()


def main():
    wb_v = openpyxl.load_workbook(sys.argv[1], data_only=True)
    wb_f = openpyxl.load_workbook(sys.argv[1])
    for k in sys.argv[2:]:
        ten = TEN[k][:31]
        ws, wf = wb_v[ten], wb_f[ten]
        lo = json.loads((SOAT / f"checklist-{k}-lo.json").read_text())
        abc = [r["updateCells"]["rows"] for r in lo if "updateCells" in r
               and r["updateCells"]["start"]["rowIndex"] == 3 and r["updateCells"]["start"]["columnIndex"] == 0][0]
        vw = json.loads((SOAT / f"checklist-{k}-VW.json").read_text())
        W = json.loads((SOAT / f"checklist-{k}-W.json").read_text())
        loi = 0
        for i, row in enumerate(abc):
            r = 4 + i
            A, B, C = (row["values"][j]["userEnteredValue"] for j in range(3))
            chuong = B.get("stringValue") == "Thuyết minh"
            if (ws.cell(r, 1).value or "") != A["stringValue"] or (ws.cell(r, 2).value or "") != B["stringValue"]:
                print(k, r, "A/B lệch", ws.cell(r, 1).value, ws.cell(r, 2).value); loi += 1
            fc = str(wf.cell(r, 3).value or "")
            if "formulaValue" in C:
                if not fc.startswith("=HYPERLINK") or C["formulaValue"].split('"')[1] not in fc:
                    print(k, r, "C link lệch", fc[:80]); loi += 1
            elif fc != C["stringValue"]:
                print(k, r, "C lệch", fc[:60]); loi += 1
            for c in range(4, 22):
                v = ws.cell(r, c).value
                ghi_chu = c in (7, 10, 14, 17, 21)
                if chuong or ghi_chu:
                    if v not in (None, ""):
                        print(k, r, c, "ô lẽ ra rỗng:", v); loi += 1
                elif v is not False:
                    print(k, r, c, "ô tích lẽ ra FALSE:", v); loi += 1
            if chuan(ws.cell(r, 22).value) != chuan(vw[i][0]):
                print(k, r, "V lệch"); loi += 1
            wv = wf.cell(r, 23).value
            if isinstance(wv, str) and wv.startswith("="):
                print(k, r, "W còn công thức"); loi += 1
            if chuan(ws.cell(r, 23).value) != chuan(W[i]):
                a, b = chuan(ws.cell(r, 23).value), chuan(W[i])
                j = next((x for x in range(min(len(a), len(b))) if a[x] != b[x]), min(len(a), len(b)))
                print(k, r, "W lệch tại", j, repr(a[j - 20:j + 30]), "≠", repr(b[j - 20:j + 30])); loi += 1
        du = ws.cell(4 + len(abc), 2).value
        print(f"{k}: {len(abc)} dòng, {sum(1 for x in W if x)} ô nhận xét, {loi} lỗi; dòng sau cuối B={du!r}")


if __name__ == "__main__":
    main()
