#!/usr/bin/env python3
"""THIẾT KẾ & ĐỊNH DẠNG ĐẸP CHO CÁC TAB TRÊN GOOGLE SHEETS PHÂN DẠNG LỚP 9.

Thực hiện:
1. Đặt Tab Color theo từng nhóm:
   - Đề thi (Đỏ cam)
   - SGK (Xanh lá cây)
   - Sách tham khảo (Xanh dương)
   - Ngân hàng câu (Tím quý phái)
   - Đại số (Xanh ngọc biển)
   - Hình học (Cam ấm)
   - Thuyết minh / Thống kê (Lục ngọc / Hổ phách)
2. Cố định hàng & cột (Frozen Rows & Columns):
   - 3 tab mới ('Đề thi', 'SGK', 'Sách tham khảo'): frozenRowCount: 5, frozenColumnCount: 1
   - 'Phân dạng Ch.I', 'Phân dạng Ch.II': frozenRowCount: 1
   - 'TM Ch.V': frozenRowCount: 5
3. Đặt độ rộng cột chuẩn (Column Widths) cho các tab ngân hàng.
4. Định dạng Header Hàng 1..5 và Data rows (Căn lề, màu sắc, font, wrap strategy CLIP).
5. Bật Bộ lọc tự động (BasicFilter).
6. Thêm Conditional Formatting (Màu Kết luận, Cấp độ, Dạng đề thật, Điểm số).
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

SPREADSHEET_ID = "1OuzuBOhfWQu5RQJ7BxRRpP98bs6aOin2xvN0udz8yqg"

SHEET_CONFIGS = [
    # (sheetId, title, tabColor, frozenRows, frozenCols)
    (460491728, "Đề thi", {"red": 0.92, "green": 0.26, "blue": 0.21}, 5, 1),
    (738848035, "SGK", {"red": 0.20, "green": 0.66, "blue": 0.33}, 5, 1),
    (149419875, "Sách tham khảo", {"red": 0.26, "green": 0.52, "blue": 0.96}, 5, 1),
    (5100, "Ngân hàng câu", {"red": 0.60, "green": 0.35, "blue": 0.71}, 5, 1),
    (5101, "Đối soát inputs", {"red": 0.45, "green": 0.55, "blue": 0.60}, 0, 0),
    (5102, "Đối soát đề theo chương", {"red": 0.45, "green": 0.55, "blue": 0.60}, 3, 2),
    (100064378, "Phân dạng Ch.I lớp 9C", {"red": 0.01, "green": 0.53, "blue": 0.82}, 1, 0),
    (1752326748, "Thống kê dạng Ch.I lớp 9C", {"red": 0.18, "green": 0.69, "blue": 0.84}, 3, 0),
    (98386104, "Phân dạng Ch.II lớp 9C", {"red": 0.01, "green": 0.53, "blue": 0.82}, 1, 0),
    (903, "Phân dạng Ch.III lớp 9C", {"red": 0.01, "green": 0.53, "blue": 0.82}, 1, 0),
    (1970943964, "Phân dạng Ch.IV lớp 9C", {"red": 0.94, "green": 0.42, "blue": 0.0}, 1, 0),
    (394223343, "TM Ch.IV lớp 9C", {"red": 0.0, "green": 0.54, "blue": 0.48}, 6, 0),
    (799696883, "Phân dạng Ch.V lớp 9C", {"red": 0.94, "green": 0.42, "blue": 0.0}, 1, 0),
    (2008590306, "TM Ch.V lớp 9C", {"red": 0.0, "green": 0.54, "blue": 0.48}, 5, 0),
    (5060, "Thống kê dạng Ch.V lớp 9C", {"red": 1.0, "green": 0.63, "blue": 0.0}, 3, 0),
    (5050, "Chọn câu Ch.V lớp 9C", {"red": 1.0, "green": 0.63, "blue": 0.0}, 4, 0),
    (906, "Phân dạng Ch.VI lớp 9C", {"red": 0.01, "green": 0.53, "blue": 0.82}, 1, 0),
    (907, "Phân dạng Ch.VII lớp 9C", {"red": 0.01, "green": 0.53, "blue": 0.82}, 1, 0),
    (908, "Phân dạng Ch.VIII lớp 9C", {"red": 0.01, "green": 0.53, "blue": 0.82}, 1, 0),
    (1678075297, "Phân dạng Ch.IX lớp 9C", {"red": 0.94, "green": 0.42, "blue": 0.0}, 1, 0),
    (910, "Phân dạng Ch.X lớp 9C", {"red": 0.94, "green": 0.42, "blue": 0.0}, 1, 0),
]

COLUMN_WIDTHS = [
    (0, 1, 380),   # A: Bài cụ thể
    (1, 2, 240),   # B: Nguồn
    (2, 3, 65),    # C: Mức độ
    (3, 4, 220),   # D: Dạng bài
    (4, 5, 120),   # E: Ưu tiên
    (5, 6, 160),   # F: Phiếu
    (6, 7, 60),    # G: Phút
    (7, 8, 65),    # H: Có hình
    (8, 9, 90),    # I: Format
    (9, 10, 130),  # J: Mức độ từng ý
    (10, 11, 80),  # K: Bài SGK
    (11, 12, 180), # L: Ghi chú
    (12, 13, 135), # M: Mã câu
    (13, 14, 90),  # N: Loại câu
    (14, 15, 180), # O: Dạng quy chuẩn
    (15, 16, 95),  # P: Mục tiêu
    (16, 17, 75),  # Q: Đã dùng
    (17, 18, 70),  # R: Trạng thái
    (18, 21, 55),  # S, T, U: Lớp C, B, A
    (21, 22, 100), # V: Ghi chú chọn
    (22, 23, 110), # W: Loại nguồn
    (23, 24, 130), # X: Dạng phiếu C
    (24, 25, 120), # Y: Mã nguồn
    (25, 26, 160), # Z: Dạng từng ý đề thật
    (26, 27, 70),  # AA: T7 gợi ý
    (27, 28, 60),  # AB: Link
    (28, 29, 60),  # AC: Chương
    (29, 31, 60),  # AD, AE: Dự phòng
    (31, 39, 45),  # AF..AM: T1..T8
    (39, 42, 65),  # AN..AP: Điểm C, B, A
    (42, 43, 75),  # AQ: Ngưỡng đạt
    (43, 44, 125), # AR: Kết luận
    (44, 45, 110), # AS: Lý do chọn
    (45, 46, 220), # AT: Lí do chấm
    (46, 47, 120), # AU: Dạng bổ sung
]

def run_raw_batch(requests: list[dict], desc: str) -> None:
    payload = {"requests": requests}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f, ensure_ascii=False)
        tmp_path = f.name
    
    print(f"Executing {desc} ({len(requests)} requests)...")
    cmd = ["gsheets", "mutate", "raw-batch", SPREADSHEET_ID, "-f", tmp_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in {desc}:", res.stderr)
        raise RuntimeError(f"Failed {desc}: {res.stderr}")
    print(f"  -> SUCCESS: {desc}")


def phase1_tab_colors_and_frozen_panes():
    requests = []
    for sid, title, color, f_rows, f_cols in SHEET_CONFIGS:
        props = {"sheetId": sid, "tabColor": color}
        fields = ["tabColor"]
        
        if f_rows > 0 or f_cols > 0:
            grid_props = {}
            if f_rows > 0:
                grid_props["frozenRowCount"] = f_rows
            if f_cols > 0:
                grid_props["frozenColumnCount"] = f_cols
            props["gridProperties"] = grid_props
            fields.append("gridProperties.frozenRowCount")
            fields.append("gridProperties.frozenColumnCount")
            
        requests.append({
            "updateSheetProperties": {
                "properties": props,
                "fields": ",".join(fields)
            }
        })
    run_raw_batch(requests, "Phase 1: Tab colors & Frozen panes")


def phase2_column_widths():
    # Áp dụng độ rộng cột cho 4 tab: Đề thi, SGK, Sách tham khảo, Ngân hàng câu
    target_sids = [460491728, 738848035, 149419875, 5100]
    requests = []
    for sid in target_sids:
        for start_col, end_col, width in COLUMN_WIDTHS:
            requests.append({
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sid,
                        "dimension": "COLUMNS",
                        "startIndex": start_col,
                        "endIndex": end_col
                    },
                    "properties": {
                        "pixelSize": width
                    },
                    "fields": "pixelSize"
                }
            })
    run_raw_batch(requests, "Phase 2: Column widths for 4 bank tabs")


def phase3_header_and_data_styling():
    # 3 tab mới
    target_sheets = [
        (460491728, 2200),
        (738848035, 820),
        (149419875, 2580),
    ]
    requests = []
    for sid, max_r in target_sheets:
        # 1. Hàng 5 (Header chính): Nền Slate Blue sẫm, chữ trắng, in đậm, căn giữa
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 4,
                    "endRowIndex": 5,
                    "startColumnIndex": 0,
                    "endColumnIndex": 47
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.173, "green": 0.243, "blue": 0.314},
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 10,
                            "bold": True,
                            "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}
                        },
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)"
            }
        })
        
        # 2. Hàng 2 (Trọng số C): Nền kem vàng nhẹ
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 30,
                    "endColumnIndex": 47
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 1.0, "green": 0.965, "blue": 0.88},
                        "textFormat": {"fontFamily": "Arial", "fontSize": 10, "bold": True},
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
            }
        })

        # 3. Hàng 3 (Trọng số B): Nền xanh nhẹ
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 2,
                    "endRowIndex": 3,
                    "startColumnIndex": 30,
                    "endColumnIndex": 47
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.94, "green": 0.97, "blue": 0.92},
                        "textFormat": {"fontFamily": "Arial", "fontSize": 10},
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
            }
        })

        # 4. Hàng 4 (Trọng số A): Nền tím nhẹ
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 3,
                    "endRowIndex": 4,
                    "startColumnIndex": 30,
                    "endColumnIndex": 47
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.93, "green": 0.91, "blue": 0.96},
                        "textFormat": {"fontFamily": "Arial", "fontSize": 10},
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
            }
        })

        # 5. Data rows (Hàng 6 trở đi): Font Arial 10pt, verticalAlignment TOP, wrap CLIP
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 0,
                    "endColumnIndex": 47
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"fontFamily": "Arial", "fontSize": 10},
                        "verticalAlignment": "TOP",
                        "wrapStrategy": "CLIP"
                    }
                },
                "fields": "userEnteredFormat(textFormat,verticalAlignment,wrapStrategy)"
            }
        })

        # 6. Cột C (Cấp độ): Căn giữa, Bold
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {"bold": True}
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        })

        # 7. Cột G, H, I: Căn giữa
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 6,
                    "endColumnIndex": 9
                },
                "cell": {
                    "userEnteredFormat": {"horizontalAlignment": "CENTER"}
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

        # 8. Cột S, T, U: Căn giữa
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 18,
                    "endColumnIndex": 21
                },
                "cell": {
                    "userEnteredFormat": {"horizontalAlignment": "CENTER"}
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

        # 9. Cột Z (Dạng từng ý trong đề thật): Nền vàng pastel nhẹ để dễ nhìn
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 25,
                    "endColumnIndex": 26
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 1.0, "green": 0.99, "blue": 0.90}
                    }
                },
                "fields": "userEnteredFormat(backgroundColor)"
            }
        })

        # 10. Cột AA (T7 gợi ý), AC (Chương): Căn giữa
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 26,
                    "endColumnIndex": 29
                },
                "cell": {
                    "userEnteredFormat": {"horizontalAlignment": "CENTER"}
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

        # 11. Cột AF..AM (T1..T8): Căn giữa
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 31,
                    "endColumnIndex": 39
                },
                "cell": {
                    "userEnteredFormat": {"horizontalAlignment": "CENTER"}
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

        # 12. Cột AN..AP (Điểm C, B, A): Căn giữa, Bold
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 39,
                    "endColumnIndex": 42
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {"bold": True}
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        })

        # 13. Cột AQ (Ngưỡng đạt): Căn giữa
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 42,
                    "endColumnIndex": 43
                },
                "cell": {
                    "userEnteredFormat": {"horizontalAlignment": "CENTER"}
                },
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

        # 14. Cột AR (Kết luận): Căn giữa, Bold
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 5,
                    "endRowIndex": max_r,
                    "startColumnIndex": 43,
                    "endColumnIndex": 44
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {"bold": True}
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        })

        # 15. Set basicFilter cho từng tab
        requests.append({
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sid,
                        "startRowIndex": 4,
                        "endRowIndex": max_r,
                        "startColumnIndex": 0,
                        "endColumnIndex": 47
                    }
                }
            }
        })

    run_raw_batch(requests, "Phase 3: Header & Data styling, Basic filters")


def phase4_conditional_formatting():
    target_sheets = [
        (460491728, 2200),
        (738848035, 820),
        (149419875, 2580),
        (5100, 5600)  # Áp dụng thêm cho Ngân hàng câu
    ]
    requests = []
    for sid, max_r in target_sheets:
        rules = [
            # 1. Cột AR: "Đưa vào bài" -> Nền xanh lá nhạt, chữ xanh đậm, Bold
            {
                "range": {"sheetId": sid, "startRowIndex": 5, "endRowIndex": max_r, "startColumnIndex": 43, "endColumnIndex": 44},
                "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Đưa vào bài"}]},
                "format": {
                    "backgroundColor": {"red": 0.902, "green": 0.957, "blue": 0.918},
                    "textFormat": {"foregroundColor": {"red": 0.075, "green": 0.451, "blue": 0.200}, "bold": True}
                }
            },
            # 2. Cột AR: "Dự phòng / sửa" -> Nền vàng cam nhạt, chữ cam đậm, Bold
            {
                "range": {"sheetId": sid, "startRowIndex": 5, "endRowIndex": max_r, "startColumnIndex": 43, "endColumnIndex": 44},
                "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Dự phòng"}]},
                "format": {
                    "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                    "textFormat": {"foregroundColor": {"red": 0.690, "green": 0.376, "blue": 0.0}, "bold": True}
                }
            },
            # 3. Cột AR: "Loại" -> Nền hồng đỏ, chữ đỏ đậm, Italic
            {
                "range": {"sheetId": sid, "startRowIndex": 5, "endRowIndex": max_r, "startColumnIndex": 43, "endColumnIndex": 44},
                "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Loại"}]},
                "format": {
                    "backgroundColor": {"red": 0.988, "green": 0.910, "blue": 0.902},
                    "textFormat": {"foregroundColor": {"red": 0.773, "green": 0.133, "blue": 0.122}, "italic": True}
                }
            },
            # 4. Cột C: "NB" -> Nền xanh dương nhạt, chữ xanh đậm
            {
                "range": {"sheetId": sid, "startRowIndex": 5, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "NB"}]},
                "format": {
                    "backgroundColor": {"red": 0.910, "green": 0.941, "blue": 0.996},
                    "textFormat": {"foregroundColor": {"red": 0.102, "green": 0.451, "blue": 0.910}, "bold": True}
                }
            },
            # 5. Cột C: "TH" -> Nền xanh ngọc nhạt, chữ xanh lá đậm
            {
                "range": {"sheetId": sid, "startRowIndex": 5, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "TH"}]},
                "format": {
                    "backgroundColor": {"red": 0.902, "green": 0.957, "blue": 0.918},
                    "textFormat": {"foregroundColor": {"red": 0.075, "green": 0.451, "blue": 0.200}, "bold": True}
                }
            },
            # 6. Cột C: "VD" -> Nền vàng cam nhạt, chữ cam đậm
            {
                "range": {"sheetId": sid, "startRowIndex": 5, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VD"}]},
                "format": {
                    "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                    "textFormat": {"foregroundColor": {"red": 0.890, "green": 0.455, "blue": 0.0}, "bold": True}
                }
            },
            # 7. Cột C: "VDC" -> Nền tím nhạt, chữ tím đậm
            {
                "range": {"sheetId": sid, "startRowIndex": 5, "endRowIndex": max_r, "startColumnIndex": 2, "endColumnIndex": 3},
                "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VDC"}]},
                "format": {
                    "backgroundColor": {"red": 0.953, "green": 0.910, "blue": 0.992},
                    "textFormat": {"foregroundColor": {"red": 0.518, "green": 0.188, "blue": 0.808}, "bold": True}
                }
            },
        ]
        
        for idx, r in enumerate(rules):
            requests.append({
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

    run_raw_batch(requests, "Phase 4: Conditional formatting for 4 bank tabs")


def main():
    print("=== STARTING SHEET BEAUTIFICATION ===")
    phase1_tab_colors_and_frozen_panes()
    phase2_column_widths()
    phase3_header_and_data_styling()
    phase4_conditional_formatting()
    print("=== ALL BEAUTIFICATION PHASES COMPLETED SUCCESSFULLY! ===")


if __name__ == "__main__":
    main()

