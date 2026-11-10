#!/usr/bin/env python3
"""ÁP DỤNG CONDITIONAL FORMATTING VÀ CĂN LỀ CHUYÊN NGHIỆP CHO 13 TAB LỚP 8."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

SPREADSHEET_ID = "10cWCHRtvudOET8fAKy425VS4CphAJY8FitScoAmXsow"

TARGET_SHEETS = [
    (0, 3200, 5),      # Ngân hàng câu
    (101, 3200, 5),    # Đề thi
    (102, 900, 32),    # Thống kê VD - VDC (data bắt đầu từ hàng 33)
    (201, 800, 5),     # Ch.I
    (202, 400, 5),     # Ch.II
    (203, 650, 5),     # Ch.III
    (204, 150, 5),     # Ch.IV
    (205, 200, 5),     # Ch.V
    (206, 500, 5),     # Ch.VI
    (207, 350, 5),     # Ch.VII
    (208, 150, 5),     # Ch.VIII
    (209, 350, 5),     # Ch.IX
    (210, 200, 5),     # Ch.X
]

def run_raw_batch(requests: list[dict], desc: str) -> None:
    payload = {"requests": requests}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f, ensure_ascii=False)
        tmp_path = f.name
    print(f"Executing {desc} ({len(requests)} requests)...", end=" ")
    res = subprocess.run(["gsheets", "mutate", "raw-batch", SPREADSHEET_ID, "-f", tmp_path], capture_output=True, text=True)
    os.remove(tmp_path)
    if res.returncode != 0:
        print(f"FAILED!\nError: {res.stderr}")
        raise RuntimeError(f"Failed {desc}: {res.stderr}")
    print("OK")

def main():
    print("Applying professional formatting and conditional rules...")
    
    # 1. Alignments and cell styles
    align_reqs = []
    for sid, max_r, data_start in TARGET_SHEETS:
        # Cột C (Cấp độ): Căn giữa, Bold
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "textFormat": {"bold": True}}},
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        })
        # Cột G, H, I: Căn giữa
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 6, "endColumnIndex": 9},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })
        # Cột S, T, U: Căn giữa
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 18, "endColumnIndex": 21},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })
        # Cột Z: Nền vàng pastel nhẹ
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 25, "endColumnIndex": 26},
                "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1.0, "green": 0.99, "blue": 0.90}}},
                "fields": "userEnteredFormat(backgroundColor)"
            }
        })
        # Cột AA, AC: Căn giữa
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 26, "endColumnIndex": 29},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })
        # Cột AF..AM (T1..T8): Căn giữa
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 31, "endColumnIndex": 39},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })
        # Cột AN..AP (Điểm C, B, X): Căn giữa, Bold
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 39, "endColumnIndex": 42},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "textFormat": {"bold": True}}},
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        })
        # Cột AQ, AR: Căn giữa, Bold
        align_reqs.append({
            "repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 42, "endColumnIndex": 44},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "textFormat": {"bold": True}}},
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        })
    run_raw_batch(align_reqs, "Alignments and Column Formats")
    
    # 2. Conditional Formatting Rules
    cond_reqs = []
    for sid, max_r, data_start in TARGET_SHEETS:
        rules = [
            # 1. Cột AR: "Đưa vào bài" -> Nền xanh lá nhạt, chữ xanh đậm, Bold
            {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 43, "endColumnIndex": 44},
                "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Đưa vào bài"}]},
                "format": {
                    "backgroundColor": {"red": 0.902, "green": 0.957, "blue": 0.918},
                    "textFormat": {"foregroundColor": {"red": 0.075, "green": 0.451, "blue": 0.200}, "bold": True}
                }
            },
            # 2. Cột AR: "Dự phòng / sửa" -> Nền vàng cam nhạt, chữ cam đậm, Bold
            {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 43, "endColumnIndex": 44},
                "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Dự phòng"}]},
                "format": {
                    "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                    "textFormat": {"foregroundColor": {"red": 0.690, "green": 0.376, "blue": 0.0}, "bold": True}
                }
            },
            # 3. Cột AR: "Loại" -> Nền hồng đỏ, chữ đỏ đậm, Italic
            {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 43, "endColumnIndex": 44},
                "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Loại"}]},
                "format": {
                    "backgroundColor": {"red": 0.988, "green": 0.910, "blue": 0.902},
                    "textFormat": {"foregroundColor": {"red": 0.773, "green": 0.133, "blue": 0.122}, "italic": True}
                }
            },
            # 4. Cột C: "NB" -> Nền xanh dương nhạt, chữ xanh đậm
            {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "NB"}]},
                "format": {
                    "backgroundColor": {"red": 0.910, "green": 0.941, "blue": 0.996},
                    "textFormat": {"foregroundColor": {"red": 0.102, "green": 0.451, "blue": 0.910}, "bold": True}
                }
            },
            # 5. Cột C: "TH" -> Nền xanh ngọc nhạt, chữ xanh lá đậm
            {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "TH"}]},
                "format": {
                    "backgroundColor": {"red": 0.902, "green": 0.957, "blue": 0.918},
                    "textFormat": {"foregroundColor": {"red": 0.075, "green": 0.451, "blue": 0.200}, "bold": True}
                }
            },
            # 6. Cột C: "VD" -> Nền vàng cam nhạt, chữ cam đậm
            {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VD"}]},
                "format": {
                    "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                    "textFormat": {"foregroundColor": {"red": 0.890, "green": 0.455, "blue": 0.0}, "bold": True}
                }
            },
            # 7. Cột C: "VDC" -> Nền tím nhạt, chữ tím đậm
            {
                "range": {"sheetId": sid, "startRowIndex": data_start, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VDC"}]},
                "format": {
                    "backgroundColor": {"red": 0.953, "green": 0.910, "blue": 0.992},
                    "textFormat": {"foregroundColor": {"red": 0.518, "green": 0.188, "blue": 0.808}, "bold": True}
                }
            },
        ]
        for idx, r in enumerate(rules):
            cond_reqs.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [r["range"]],
                        "booleanRule": {
                            "condition": r["condition"],
                            "format": r["format"]
                        }
                    },
                    "index": idx
                }
            })
    run_raw_batch(cond_reqs, "Conditional Formatting Rules across 13 Sheets")
    print("Formatting completed successfully!")

if __name__ == '__main__':
    main()

