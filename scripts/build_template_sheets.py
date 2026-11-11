#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dựng trọn bộ 4 Tab Template Google Sheets mẫu chuẩn cho MathTech:
Spreadsheet ID: 1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY
URL: https://docs.google.com/spreadsheets/d/1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY/edit
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SPREADSHEET_ID = "1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY"

def run_raw_batch(requests: list[dict], desc: str) -> None:
    payload = {"requests": requests}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f, ensure_ascii=False)
        tmp = f.name
    print(f"Executing {desc} ({len(requests)} requests)...", end=" ")
    sys.stdout.flush()
    res = subprocess.run(["gsheets", "mutate", "raw-batch", SPREADSHEET_ID, "-f", tmp], capture_output=True, text=True)
    os.remove(tmp)
    if res.returncode != 0:
        print(f"FAILED!\nError: {res.stderr}")
        raise RuntimeError(f"Failed {desc}: {res.stderr}")
    print("OK")

def run_write_batch(operations: list[dict], desc: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(operations, f, ensure_ascii=False)
        tmp = f.name
    print(f"Writing {desc}...", end=" ")
    sys.stdout.flush()
    res = subprocess.run(["gsheets", "mutate", "batch", SPREADSHEET_ID, "-f", tmp], capture_output=True, text=True)
    os.remove(tmp)
    if res.returncode != 0:
        print(f"FAILED!\nError: {res.stderr}")
        raise RuntimeError(f"Failed {desc}: {res.stderr}")
    print("OK")

def setup_grids_and_widths():
    """Thiết lập số hàng cột, frozen panes, tab colors và độ rộng cột cho 3 tab."""
    reqs = []
    
    # 1. Update Grid Properties & Frozen Panes & Tab Colors
    sheet_props = [
        (0, "01_Template_Phan_Dang", {"red": 0.12, "green": 0.23, "blue": 0.54}, 5, 1, 100, 47),
        (101, "02_Template_Thuyet_Minh", {"red": 0.85, "green": 0.47, "blue": 0.02}, 5, 3, 50, 15),
        (103, "03_Template_Quan_Tri_Tien_Do", {"red": 0.49, "green": 0.14, "blue": 0.80}, 4, 3, 50, 14),
    ]
    for sid, title, color, fr_row, fr_col, r_count, c_count in sheet_props:
        reqs.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sid,
                    "title": title,
                    "tabColor": color,
                    "gridProperties": {
                        "rowCount": r_count,
                        "columnCount": c_count,
                        "frozenRowCount": fr_row,
                        "frozenColumnCount": fr_col,
                    }
                },
                "fields": "title,tabColor,gridProperties(rowCount,columnCount,frozenRowCount,frozenColumnCount)"
            }
        })
    
    # 2. Column widths for Tab 0 (47 cột)
    col_widths_0 = [
        (0, 1, 380),   # A: Bài cụ thể
        (1, 2, 240),   # B: Nguồn
        (2, 3, 75),    # C: Mức độ
        (3, 4, 220),   # D: Dạng bài
        (4, 5, 110),   # E: Ưu tiên
        (5, 6, 150),   # F: Phân loại vào phiếu
        (6, 7, 75),    # G: Phút
        (7, 8, 70),    # H: Thực tế
        (8, 9, 95),    # I: Format
        (9, 10, 130),  # J: Mức độ từng ý
        (10, 11, 90),  # K: Bài học SGK
        (11, 12, 160), # L: Ghi chú
        (12, 13, 130), # M: Mã câu
        (13, 14, 120), # N: Phân loại câu
        (14, 15, 160), # O: Đề xuất thuyết minh
        (15, 16, 90),  # P: Trạng thái
        (16, 17, 85),  # Q: Loại ngay
        (17, 18, 80),  # R: Đã soi ảnh
        (18, 21, 65),  # S, T, U: Lớp C, B, X
        (21, 22, 100), # V: Chọn tay
        (22, 23, 110), # W: Loại nguồn
        (23, 24, 85),  # X: Có hình
        (24, 25, 120), # Y: Mã bài gốc
        (25, 26, 160), # Z: Dạng đề thật
        (26, 27, 80),  # AA: T7 gợi ý
        (27, 28, 150), # AB: Kỹ thuật giải
        (28, 29, 70),  # AC: Chương
        (29, 30, 100), # AD: Nhóm nghi trùng
        (30, 31, 90),  # AE: Cần soát đề
        (31, 39, 50),  # AF..AM: T1..T8
        (39, 42, 75),  # AN..AP: Điểm C, B, X
        (42, 43, 75),  # AQ: Ngưỡng đạt
        (43, 44, 130), # AR: Kết luận lớp C
        (44, 45, 110), # AS: THẦY DUYỆT
        (45, 46, 200), # AT: Lí do chấm
        (46, 47, 80),  # AU: Năm đầu đề
    ]
    for sc, ec, w in col_widths_0:
        reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": sc, "endIndex": ec},
                "properties": {"pixelSize": w},
                "fields": "pixelSize"
            }
        })

    # 3. Column widths for Tab 101 (Thuyết minh)
    col_widths_101 = [
        (0, 1, 50),    # A: STT
        (1, 2, 120),   # B: Loại câu (§4b)
        (2, 3, 260),   # C: Dạng bài
        (3, 4, 300),   # D: Mục tiêu kiến thức / Kỹ năng
        (4, 5, 85),    # E: Lý thuyết (phút)
        (5, 6, 85),    # F: Ví dụ mẫu (câu)
        (6, 7, 85),    # G: Trên lớp (câu)
        (7, 8, 85),    # H: BTVN (câu)
        (8, 9, 140),   # I: Mã câu đề xuất
        (9, 10, 140),  # J: THẦY CHỌN & ĐỔI CÂU
        (10, 11, 140), # K: Chốt mã
        (11, 12, 95),  # L: Phút trên lớp
        (12, 13, 95),  # M: Phút BTVN
        (13, 14, 180), # N: Ghi chú sư phạm
    ]
    for sc, ec, w in col_widths_101:
        reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": 101, "dimension": "COLUMNS", "startIndex": sc, "endIndex": ec},
                "properties": {"pixelSize": w},
                "fields": "pixelSize"
            }
        })

    # 3. Column widths for Tab 103 (Tiến độ)
    col_widths_103 = [
        (0, 1, 110),   # A: Tuần / Ca
        (1, 2, 110),   # B: Mã phiếu
        (2, 3, 260),   # C: Tên bài SGK
        (3, 4, 130),   # D: Sheet Phân dạng
        (4, 5, 130),   # E: Thuyết minh PDF
        (5, 6, 120),   # F: Trạng thái Thẩm định
        (6, 7, 130),   # G: Handout HS
        (7, 8, 130),   # H: Guide GV
        (8, 9, 130),   # I: Slide Beamer
        (9, 10, 130),  # J: Ghi chú bàn giao
        (10, 11, 110), # K: Bản Word DOCX
        (11, 12, 110), # L: Nghiệm thu bàn giao
        (12, 13, 160), # M: Ghi chú
    ]
    for sc, ec, w in col_widths_103:
        reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": 103, "dimension": "COLUMNS", "startIndex": sc, "endIndex": ec},
                "properties": {"pixelSize": w},
                "fields": "pixelSize"
            }
        })

    run_raw_batch(reqs, "Setup Grids, Panes, Colors, and Column Widths")

def populate_tab1_data():
    """Đổ dữ liệu và công thức chuẩn cho Tab 1: 01_Template_Phan_Dang."""
    # Rows 1..5
    headers = [
        ["TEMPLATE PHÂN DẠNG & NGÂN HÀNG CÂU HỎI THEO CHƯƠNG (47 CỘT CHUẨN MATHTECH)"] + [""] * 46,
        [
            "Lấy câu cho một chương: Lọc cột AC chứa nhãn chương (ví dụ [V]), rồi lọc AS = Hay. Chép Mã câu sang tab Thuyết minh (Template 2).",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
            "Trọng số lớp C", "3", "1", "2", "1", "2", "2", "2", "0", "", "", "", "Ngưỡng VD, VDC", "7", "", "", ""
        ],
        [
            "Chấm điểm: điền T1-T8 (0, 1, 2) ở cột AF:AM. Điểm, ngưỡng và kết luận tự tính khi đủ 8 tiêu chí theo công thức quy chuẩn.",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
            "Trọng số lớp B", "2", "2", "2", "3", "2", "1", "3", "1", "", "", "", "Ngưỡng TH", "6", "", "", ""
        ],
        [
            "Cột R = Chưa nghĩa là đề chưa đối chiếu lại với ảnh scan gốc. Cột Q ghi mã vi phạm L1-L5 để loại ngay.",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
            "Trọng số lớp X", "1", "3", "1", "2", "1", "1", "2", "3", "", "", "", "Ngưỡng NB", "5", "", "", ""
        ],
        [
            "Bài cụ thể", "Nguồn trong input", "Mức độ", "Dạng bài", "Ưu tiên", "Phân loại vào phiếu",
            "Thời lượng (phút)", "Thực tế", "Format", "Mức độ từng ý", "Bài học SGK", "Ghi chú",
            "Mã câu", "Phân loại câu", "Đề xuất thuyết minh", "Trạng thái", "Loại ngay (L1-L5)",
            "Đã soi ảnh", "Lớp C", "Lớp B", "Lớp X", "Chọn tay", "Loại nguồn", "Có hình · ảnh chụp",
            "Mã bài gốc", "Dạng từng ý trong đề thật", "T7 gợi ý", "Kỹ thuật giải", "Chương",
            "Nhóm nghi trùng", "Cần soát đề", "T1 Trọng tâm SGK", "T2 Ý toán", "T3 Bối cảnh",
            "T4 Phân hoá ý con", "T5 Lỗi sai kinh điển", "T6 Vừa sức, nghiệm đẹp", "T7 Dạng đề thi",
            "T8 Mở rộng", "Điểm lớp C", "Điểm lớp B", "Điểm lớp X", "Ngưỡng theo mức", "Kết luận lớp C",
            "THẦY DUYỆT (Chờ duyệt / Hay / Không hay)", "Lí do chấm", "Năm đầu của năm học đề"
        ]
    ]

    # Sample rows (Rows 6..11)
    samples = [
        # Row 6: NB đệm
        [
            "Cho đường tròn (O; R) và điểm A nằm ngoài đường tròn. Kẻ tiếp tuyến AB với đường tròn (B là tiếp điểm). Hãy chỉ ra tam giác vuông và góc vuông tương ứng.",
            "SGK Toán 9 KNTT Tập 1, Bài 15.1", "NB", "Nhận diện tiếp tuyến và góc vuông", "Ưu tiên 2",
            "Phiếu 2; Khám phá", 1.5, False, "Tự luận", "NB", "Bài 15", "Bước đệm nhận diện góc vuông",
            "9H5-P02-001-nb1", "NB kiến thức cũ", "P02 · Khám phá", "Đang dùng", "", "Đã soi",
            "Phù hợp", "Phù hợp", "Phù hợp", "", "SGK KNTT", "Có hình TikZ", "9H5-P02-001",
            "Nhận diện góc vuông tại tiếp điểm", "Câu đệm", "Tiếp tuyến vuông góc bán kính", "[V]",
            "Nhóm 1", "", 2, 2, 2, 1, 1, 2, 2, 1,
            '=IF(COUNT($AF6:$AM6)<8,"",ROUND(SUMPRODUCT($AF6:$AM6,$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))',
            '=IF(COUNT($AF6:$AM6)<8,"",ROUND(SUMPRODUCT($AF6:$AM6,$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))',
            '=IF(COUNT($AF6:$AM6)<8,"",ROUND(SUMPRODUCT($AF6:$AM6,$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))',
            '=IF($C6="TH",$AR$3,IF($C6="NB",$AR$4,$AR$2))',
            '=IF($Q6<>"","Loại ("&$Q6&")",IF($AN6="","Chưa chấm",IF($AN6>=$AQ6,"Đưa vào bài",IF($AN6>=5,"Dự phòng / sửa","Loại hoặc sửa"))))',
            "Hay", "Bám sát SGK, dẫn xuất tự nhiên", 2024
        ],
        # Row 7: NB tách TH
        [
            "Cho đường tròn (O; R) và hai tiếp tuyến AB, AC cắt nhau tại A. Chứng minh tam giác OAB bằng tam giác OAC (c.c.c hoặc cạnh huyền - góc nhọn).",
            "Đề thi HK1 THCS Giảng Võ 2024–2025, Bài IV.1", "NB", "Chứng minh hai tam giác bằng nhau", "Ưu tiên 1",
            "Phiếu 2; Luyện tập 1", 2.0, True, "Điền khuyết", "NB", "Bài 15", "Giàn giáo điền khuyết trên hình in sẵn",
            "9H5-P02-002-nb1", "NB tách TH", "P02 · Luyện tập 1", "Đang dùng", "", "Đã soi",
            "Phù hợp", "Phù hợp", "Phù hợp", "", "Đề thi thật Hà Nội", "inputs/refs/hinh/9H5-P02-002.png", "9H5-P02-002",
            "Tách bước chứng minh tính chất 2 tiếp tuyến", "Câu đệm đề thi", "Cạnh huyền chung + bán kính bằng nhau", "[V]",
            "Nhóm 2", "", 2, 2, 2, 2, 2, 2, 2, 1,
            '=IF(COUNT($AF7:$AM7)<8,"",ROUND(SUMPRODUCT($AF7:$AM7,$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))',
            '=IF(COUNT($AF7:$AM7)<8,"",ROUND(SUMPRODUCT($AF7:$AM7,$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))',
            '=IF(COUNT($AF7:$AM7)<8,"",ROUND(SUMPRODUCT($AF7:$AM7,$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))',
            '=IF($C7="TH",$AR$3,IF($C7="NB",$AR$4,$AR$2))',
            '=IF($Q7<>"","Loại ("&$Q7&")",IF($AN7="","Chưa chấm",IF($AN7>=$AQ7,"Đưa vào bài",IF($AN7>=5,"Dự phòng / sửa","Loại hoặc sửa"))))',
            "Hay", "Bước đệm tuyệt vời từ đề Giảng Võ", 2024
        ],
        # Row 8: TH ghép VD
        [
            "Cho đường tròn (O), từ điểm A ngoài đường tròn kẻ 2 tiếp tuyến AB, AC. Gọi H là giao điểm của OA và BC. Chứng minh OA là đường trung trực của BC và OA vuông góc BC tại H.",
            "Đề thi HK1 THCS Trưng Vương 2024–2025, Bài IV.1", "TH", "Chứng minh đường trung trực và vuông góc", "Ưu tiên 1",
            "Phiếu 2; Ví dụ mẫu", 6.0, True, "Tự luận", "a) TH · b) TH", "Bài 15", "Ví dụ GV cùng làm với HS có sơ đồ ngược",
            "9H5-P02-003", "TH ghép VD", "P02 · Ví dụ mẫu", "Đang dùng", "", "Đã soi",
            "Phù hợp", "Phù hợp", "Phù hợp", "", "Đề thi thật Hà Nội", "inputs/refs/hinh/9H5-P02-003.png", "9H5-P02-003",
            "Ý 1 đề thi HK1 Trưng Vương", "Dạng chuẩn thi 100%", "Tính chất 2 tiếp tuyến cắt nhau", "[V]",
            "Nhóm 2", "", 2, 2, 2, 2, 2, 2, 2, 2,
            '=IF(COUNT($AF8:$AM8)<8,"",ROUND(SUMPRODUCT($AF8:$AM8,$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))',
            '=IF(COUNT($AF8:$AM8)<8,"",ROUND(SUMPRODUCT($AF8:$AM8,$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))',
            '=IF(COUNT($AF8:$AM8)<8,"",ROUND(SUMPRODUCT($AF8:$AM8,$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))',
            '=IF($C8="TH",$AR$3,IF($C8="NB",$AR$4,$AR$2))',
            '=IF($Q8<>"","Loại ("&$Q8&")",IF($AN8="","Chưa chấm",IF($AN8>=$AQ8,"Đưa vào bài",IF($AN8>=5,"Dự phòng / sửa","Loại hoặc sửa"))))',
            "Hay", "Câu kinh điển thi vào 10 và HK1", 2024
        ],
        # Row 9: VD đích
        [
            "Cho đường tròn (O; R) và điểm A ngoài (O). Kẻ tiếp tuyến AB và cát tuyến ACD (C nằm giữa A và D). Chứng minh hệ thức tích: AB^2 = AC . AD.",
            "Đề thi Tuyển sinh vào 10 Hà Nội 2024, Bài IV.2", "VD", "Chứng minh hệ thức tích bằng tam giác đồng dạng", "Ưu tiên 1",
            "Phiếu 2; Luyện tập 2", 12.0, True, "Tự luận", "VD", "Bài 15", "Bài đích buổi học — HS bắt buộc tự vẽ hình",
            "9H5-P02-004", "VD lẻ", "P02 · Luyện tập 2", "Đang dùng", "", "Đã soi",
            "Phù hợp", "Phù hợp", "Phù hợp", "", "Đề thi thật Hà Nội", "inputs/refs/hinh/9H5-P02-004.png", "9H5-P02-004",
            "Câu hình ý 2 đề vào 10", "Xuất hiện 59% trong đề thi", "Tam giác đồng dạng góc - góc", "[V]",
            "Nhóm 3", "", 2, 2, 2, 2, 2, 2, 2, 2,
            '=IF(COUNT($AF9:$AM9)<8,"",ROUND(SUMPRODUCT($AF9:$AM9,$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))',
            '=IF(COUNT($AF9:$AM9)<8,"",ROUND(SUMPRODUCT($AF9:$AM9,$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))',
            '=IF(COUNT($AF9:$AM9)<8,"",ROUND(SUMPRODUCT($AF9:$AM9,$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))',
            '=IF($C9="TH",$AR$3,IF($C9="NB",$AR$4,$AR$2))',
            '=IF($Q9<>"","Loại ("&$Q9&")",IF($AN9="","Chưa chấm",IF($AN9>=$AQ9,"Đưa vào bài",IF($AN9>=5,"Dự phòng / sửa","Loại hoặc sửa"))))',
            "Hay", "Trọng tâm thi vào 10 Hà Nội", 2024
        ],
        # Row 10: Bị loại L3
        [
            "Giải phương trình: căn(2x^2 + 5x - 7) = 3x - 11/17 (nghiệm lẻ vô tỉ).",
            "Sách tham khảo cũ 2021", "VD", "Phương trình chứa căn", "Ưu tiên 4",
            "Chưa có phiếu", 15.0, False, "Tự luận", "VD", "Bài 3", "Số liệu xấu, cồng kềnh",
            "9D1-099", "VD lẻ", "", "Bỏ", "L3", "Đã soi",
            "Không", "Không", "Không", "Bỏ", "Sách tham khảo", "", "9D1-099",
            "Nghiệm vô tỉ cồng kềnh", "Không có trong đề thi", "Bình phương hai vế", "[I]",
            "Nhóm cũ", "Nghiệm xấu", 1, 0, 0, 1, 0, 0, 0, 0,
            '=IF(COUNT($AF10:$AM10)<8,"",ROUND(SUMPRODUCT($AF10:$AM10,$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))',
            '=IF(COUNT($AF10:$AM10)<8,"",ROUND(SUMPRODUCT($AF10:$AM10,$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))',
            '=IF(COUNT($AF10:$AM10)<8,"",ROUND(SUMPRODUCT($AF10:$AM10,$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))',
            '=IF($C10="TH",$AR$3,IF($C10="NB",$AR$4,$AR$2))',
            '=IF($Q10<>"","Loại ("&$Q10&")",IF($AN10="","Chưa chấm",IF($AN10>=$AQ10,"Đưa vào bài",IF($AN10>=5,"Dự phòng / sửa","Loại hoặc sửa"))))',
            "Không hay", "Dính L3 nghiệm xấu, không bám đề thi", 2021
        ],
        # Row 11: VDC Lớp B/A/X
        [
            "Từ điểm M ngoài (O), kẻ 2 tiếp tuyến MA, MB. Kẻ cát tuyến MCD. Tìm vị trí cát tuyến MCD để diện tích tam giác MAB đạt giá trị lớn nhất.",
            "Đề thi HSG Quận Cầu Giấy 2024–2025", "VDC", "Cực trị hình học", "Ưu tiên 1",
            "Chuyên đề Lớp A/X", 18.0, True, "Tự luận", "VDC", "Bài 15", "Dành riêng lớp A/X, CẤM đưa lớp C",
            "9H5-VDC-001", "VD lẻ", "Chuyên đề VDC", "Dự phòng", "", "Đã soi",
            "Không", "Phù hợp", "Phù hợp", "", "Đề thi thật Hà Nội", "inputs/refs/hinh/9H5-VDC-001.png", "9H5-VDC-001",
            "Cực trị hình học câu cuối", "Câu 9,5-10đ", "Bất đẳng thức Cauchy + tiếp tuyến", "[V]",
            "Nhóm cực trị", "", 2, 2, 2, 2, 1, 2, 2, 2,
            '=IF(COUNT($AF11:$AM11)<8,"",ROUND(SUMPRODUCT($AF11:$AM11,$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))',
            '=IF(COUNT($AF11:$AM11)<8,"",ROUND(SUMPRODUCT($AF11:$AM11,$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))',
            '=IF(COUNT($AF11:$AM11)<8,"",ROUND(SUMPRODUCT($AF11:$AM11,$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))',
            '=IF($C11="TH",$AR$3,IF($C11="NB",$AR$4,$AR$2))',
            '=IF($Q11<>"","Loại ("&$Q11&")",IF($AN11="","Chưa chấm",IF($AN11>=$AQ11,"Đưa vào bài",IF($AN11>=5,"Dự phòng / sửa","Loại hoặc sửa"))))',
            "Hay", "Bài hay phân hóa sâu cho lớp khá giỏi", 2024
        ]
    ]

    all_data = headers + samples
    run_write_batch([{"op": "write", "range": "'01_Template_Phan_Dang'!A1:AU11", "data": all_data}], "Tab 1 Data")

def populate_tab2_data():
    """Đổ dữ liệu và công thức chuẩn cho Tab 2: 02_Template_Thuyet_Minh (Spec)."""
    rows = [
        # Row 1: Title
        ["BẢNG THUYẾT MINH PHIẾU HỌC TẬP (SPEC-FIRST) — MÔ HÌNH CA HỌC 90 PHÚT (LỚP C)"] + [""] * 13,
        # Row 2: Sub-title
        ["Chủ đề: Chương V — Đường tròn | Phiếu 02: Bốn điểm cùng thuộc một đường tròn & Tiếp tuyến của đường tròn"] + [""] * 13,
        # Row 3: KPI Card Headers
        [
            "Tổng thời lượng trên lớp", "Tổng BTVN", "Tổng GV giảng & mẫu",
            "Tỉ lệ Nhận biết (NB)", "Tỉ lệ Thông hiểu (TH)", "Tỉ lệ Vận dụng (VD)",
            "Trạng thái Thuyết Minh Gate"
        ] + [""] * 7,
        # Row 4: KPI Card Values (Formulas)
        [
            '=SUM(L7:L16)&" phút"', '=SUM(M7:M16)&" phút"', '=(SUM(E7:E16)+SUM(F7:F16)*6)&" phút"',
            '=TEXT(SUMIF(B7:B16,"*NB*",L7:L16)/SUM(L7:L16),"0.0%")',
            '=TEXT(SUMIF(B7:B16,"*TH*",L7:L16)/SUM(L7:L16),"0.0%")',
            '=TEXT(SUMIF(B7:B16,"*VD*",L7:L16)/SUM(L7:L16),"0.0%")',
            '=IF(AND(SUM(L7:L16)>=45,SUM(L7:L16)<=65),"✓ ĐẠT CHUẨN","CẢNH BÁO LỆCH GIỜ")'
        ] + [""] * 7,
        # Row 5: Empty separator
        [""] * 14,
        # Row 6: Table Header
        [
            "STT", "Loại câu (§4b)", "Dạng bài", "Mục tiêu kiến thức / Kỹ năng",
            "Lý thuyết (phút)", "Ví dụ mẫu (câu)", "Trên lớp (câu)", "BTVN (câu)",
            "Mã câu đề xuất", "THẦY CHỌN & ĐỔI CÂU", "Chốt mã", "Phút trên lớp", "Phút BTVN", "Ghi chú sư phạm"
        ],
        # Rows 7..16: 10 Dạng bài mẫu
        [
            1, "NB kiến thức cũ", "Nhận diện tâm và bán kính đường tròn ngoại tiếp tam giác vuông",
            "Nhớ định lý: trung điểm cạnh huyền là tâm đường tròn ngoại tiếp",
            2, 0, 2, 1, "9H5-P02-001-nb1", "", '=IF(J7<>"",J7,I7)', 3.0, 1.5, "Chặng 1 Khám phá"
        ],
        [
            2, "NB tách TH", "Nhận diện góc vuông tại tiếp điểm ($AB \\perp OB$)",
            "Biết bán kính vuông góc tiếp tuyến tại tiếp điểm",
            0, 0, 2, 2, "9H5-P02-001-nb2", "", '=IF(J8<>"",J8,I8)', 3.0, 2.4, "Chặng 1 Khám phá"
        ],
        [
            3, "NB tách TH", "Đọc cạnh huyền chung và các bán kính bằng nhau",
            "Nhận diện cạnh huyền chung OA và OB = OC = R",
            0, 0, 2, 2, "9H5-P02-002-nb1", "", '=IF(J9<>"",J9,I9)', 3.0, 2.4, "Bước đệm cho bài mẫu"
        ],
        [
            4, "TH lẻ LT", "Tính độ dài đoạn thẳng bằng định lý Pythagore",
            "Tính cạnh huyền OA = căn(R^2 + d^2)",
            1, 1, 1, 1, "9H5-P02-002-th1", "", '=IF(J10<>"",J10,I10)', 6.0, 4.8, "Chặng 2 Kiến thức mới"
        ],
        [
            5, "TH ghép VD", "Chứng minh 4 điểm cùng thuộc một đường tròn",
            "Chỉ ra 2 tam giác vuông chung cạnh huyền",
            0, 1, 1, 1, "9H5-P02-003", "", '=IF(J11<>"",J11,I11)', 6.0, 4.8, "Chặng 3 Ví dụ mẫu (GV cùng HS)"
        ],
        [
            6, "TH ghép VD", "Chứng minh OA là đường trung trực của BC",
            "Áp dụng tính chất 2 tiếp tuyến cắt nhau",
            0, 1, 1, 1, "9H5-P02-003-th2", "", '=IF(J12<>"",J12,I12)', 6.0, 4.8, "Chặng 3 Ví dụ mẫu"
        ],
        [
            7, "NB ghép bài", "Điền khuyết chứng minh 4 điểm cùng thuộc đường tròn",
            "Rèn kỹ năng điền mẫu suy luận vào hình có sẵn",
            0, 0, 3, 2, "9H5-P02-004-lt1", "", '=IF(J13<>"",J13,I13)', 4.5, 3.0, "Chặng 4 Luyện tập 1"
        ],
        [
            8, "TH tách VD", "Chứng minh tiếp tuyến thứ hai (AC là tiếp tuyến)",
            "Chứng minh tam giác OBA = OCA (c.c.c)",
            0, 0, 2, 2, "9H5-P02-004-lt2", "", '=IF(J14<>"",J14,I14)', 12.0, 9.6, "Chặng 4 Luyện tập 1"
        ],
        [
            9, "VD lẻ", "Chứng minh hệ thức tích AB^2 = AH . AO",
            "Áp dụng hệ thức lượng trong tam giác vuông",
            0, 0, 1, 1, "9H5-P02-005", "", '=IF(J15<>"",J15,I15)', 12.0, 9.6, "Chặng 4 Luyện tập 2 (Tự vẽ hình)"
        ],
        [
            10, "VD lẻ", "Bài toán thực tế: Đo bán kính Trái Đất từ ngọn hải đăng",
            "Vận dụng tiếp tuyến và định lý Pythagore vào thực tế",
            0, 0, 1, 1, "9H5-P02-006", "", '=IF(J16<>"",J16,I16)', 5.0, 4.0, "Chặng 4 Luyện tập 2 (Thực tế)"
        ],
    ]
    run_write_batch([{"op": "write", "range": "'02_Template_Thuyet_Minh'!A1:N16", "data": rows}], "Tab 2 Data")

def populate_tab3_data():
    """Đổ dữ liệu và công thức chuẩn cho Tab 3: 03_Template_De_Thi_KTC."""
    rows = [
        # Row 1: Banner 1
        ["BẢNG MA TRẬN ĐỀ KIỂM TRA CHƯƠNG 45 PHÚT (CHUẨN 3 HÌNH THỨC — THANG 10,0Đ)"] + [""] * 6,
        ["Mục tiêu khảo thí: Đánh giá quá trình (Diagnostic Assessment), rà soát lỗ hổng kiến thức trước khi qua chương mới."] + [""] * 6,
        # Row 3: Header Ma Trận
        [
            "Phần thi", "Hình thức câu hỏi", "Mức độ", "Số câu", "Điểm/câu", "Tổng điểm", "Mục tiêu khảo thí chẩn đoán"
        ],
        # Rows 4..8: Data
        [
            "Phần I", "Trắc nghiệm 4 lựa chọn (A/B/C/D)", "NB - TH", 4, 0.50, 2.0,
            "Quét nhanh toàn bộ định nghĩa, tính chất, công thức cốt lõi của chương."
        ],
        [
            "Phần II", "Điền khuyết / Trả lời ngắn", "NB - TH", 2, 0.50, 1.0,
            "Kiểm tra ĐKXĐ, giá trị biên, số mũ, định lý, khắc phục lỗi sai kinh điển."
        ],
        [
            "Phần III.1", "Tự luận ngắn (Bài 1 — Kỹ năng cơ bản)", "TH", 1, 2.00, 2.0,
            "Chứng minh 4 điểm thuộc đường tròn / Rút gọn biểu thức."
        ],
        [
            "Phần III.2", "Tự luận ngắn (Bài 2 — Bài toán đích)", "TH - VD", 1, 2.50, 2.5,
            "Chứng minh tiếp tuyến của đường tròn / Hệ thức tích."
        ],
        [
            "Phần III.3", "Tự luận ngắn (Bài 3 — Toán thực tế)", "VD", 1, 2.50, 2.5,
            "Bài toán thực tế có lời văn, tính toán độ dài, diện tích, góc."
        ],
        # Row 9: Total
        [
            "TỔNG CỘNG", "Đầy đủ 3 hình thức (Bắt buộc)", "NB 40% - TH 40% - VD 20%", 9, "",
            '=SUM(F4:F8)', "Đạt chuẩn 10,0 điểm tuyệt đối; 0% VDC đối với Lớp C"
        ],
        [""] * 7,
        # Row 11: Banner 2
        ["BẢNG KIỂM SOÁT PHÂN BỔ NGUỒN ĐỀ THẬT HÀ NỘI (T_GKCK 5 — RẢI NGUỒN >= 4 QUẬN)"] + [""] * 6,
        # Row 12: Header Rải nguồn
        [
            "Quận / Huyện", "Trường THCS / Phòng GD", "Năm học", "Số câu lấy", "Điểm thành phần", "Tỉ lệ % đề (<= 40%)", "Đánh giá rải nguồn"
        ],
        # Rows 13..16: Data rải nguồn
        [
            "Hoàn Kiếm", "THCS Trưng Vương", "2024–2025", 2, 2.5, '=E13/$F$9', '=IF(F13<=0.4,"✓ Hợp lệ","Cảnh báo > 40%")'
        ],
        [
            "Cầu Giấy", "THCS Cầu Giấy", "2024–2025", 3, 3.0, '=E14/$F$9', '=IF(F14<=0.4,"✓ Hợp lệ","Cảnh báo > 40%")'
        ],
        [
            "Long Biên", "THCS Ái Mộ", "2024–2025", 2, 2.5, '=E15/$F$9', '=IF(F15<=0.4,"✓ Hợp lệ","Cảnh báo > 40%")'
        ],
        [
            "Ba Đình", "THCS Giảng Võ", "2024–2025", 2, 2.0, '=E16/$F$9', '=IF(F16<=0.4,"✓ Hợp lệ","Cảnh báo > 40%")'
        ],
        # Row 17: Total rải nguồn
        [
            "TỔNG SỐ QUẬN: 4", "Quy chuẩn: >= 4 quận Hà Nội", "Từ năm 2024 trở đi", 9, '=SUM(E13:E16)', '=SUM(F13:F16)', "✓ ĐẠT CHUẨN RẢI NGUỒN"
        ],
        [""] * 7,
        # Row 19: Banner 3
        ["QUY CHUẨN LỜI GIẢI THI & BAREM ĐIỂM (0,25Đ TỪNG DÒNG)"] + [""] * 6,
        [
            "1. CẤM dấu tương đương (\\Leftrightarrow). Mỗi bước biến đổi viết một dòng riêng biệt ngắt bằng [[br]].", "", "", "", "", "", ""
        ],
        [
            "2. CẤM dùng hệ thức lượng trực tiếp: Bắt buộc chứng minh 2 tam giác đồng dạng (g.g) rồi mới suy ra tỉ số.", "", "", "", "", "", ""
        ],
        [
            "3. BÀI HÌNH BẮT BUỘC có hình vẽ TikZ chuẩn ở đầu lời giải. Barem phân rã chi tiết 0,25đ mỗi bước suy luận.", "", "", "", "", "", ""
        ]
    ]
    run_write_batch([{"op": "write", "range": "'03_Template_De_Thi_KTC'!A1:G22", "data": rows}], "Tab 3 Data")

def populate_tab4_data():
    """Đổ dữ liệu và công thức chuẩn cho Tab 4: 04_Template_Quan_Tri_Tien_Do."""
    rows = [
        # Row 1: Title
        ["BẢNG QUẢN TRỊ TIẾN ĐỘ HỌC LIỆU & ĐỒNG BỘ GOOGLE DRIVE (KHUÔN MẪU TIẾN ĐỘ MATHTECH)"] + [""] * 12,
        # Row 2: Sub-title
        ["Quản lý vòng đời sản phẩm: Soạn thảo ➔ Thẩm định sư phạm ➔ Duyệt ➔ Đồng bộ 3 PDF & Đề thi lên Drive"] + [""] * 12,
        # Row 3: KPI Metrics
        [
            "Tổng số buổi học: 12 ca", "Đã duyệt: =COUNTIF(F5:F16,\"*ĐÃ DUYỆT*\")",
            "Đã up Drive: =COUNTIF(L5:L16,TRUE)", "Tỉ lệ hoàn thành: =TEXT(COUNTIF(L5:L16,TRUE)/12,\"0.0%\")"
        ] + [""] * 9,
        # Row 4: Table Header
        [
            "Tuần / Ca", "Mã phiếu", "Tên bài học SGK Kết nối tri thức",
            "Sheet Phân dạng", "Spec Thuyết minh (PDF)", "Trạng thái Thẩm định",
            "Handout HS (PDF)", "Guide GV (PDF)", "Slide Beamer (PDF)",
            "Đề KT Chương (PDF)", "Bản Word (DOCX)", "Nghiệm thu bàn giao", "Ghi chú"
        ],
        # Rows 5..16: 12 ca học mẫu
        [
            "Tuần 01 · Ca 1", "9C-H5-P01", "Bài 14: Cung và dây của một đường tròn",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟢 ĐÃ DUYỆT",
            "https://drive.google.com/...", "https://drive.google.com/...", "https://drive.google.com/...",
            "—", "https://drive.google.com/...", True, "Đã in ấn bàn giao cơ sở"
        ],
        [
            "Tuần 01 · Ca 2", "9C-H5-P02", "Bài 15: Độ dài cung tròn và diện tích hình quạt",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟢 ĐÃ DUYỆT",
            "https://drive.google.com/...", "https://drive.google.com/...", "https://drive.google.com/...",
            "—", "https://drive.google.com/...", True, "Đã in ấn bàn giao cơ sở"
        ],
        [
            "Tuần 02 · Ca 1", "9C-H5-P03", "Bài 16: Vị trí tương đối của đường thẳng và đường tròn",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟢 ĐÃ DUYỆT",
            "https://drive.google.com/...", "https://drive.google.com/...", "https://drive.google.com/...",
            "—", "https://drive.google.com/...", True, "Đã in ấn bàn giao cơ sở"
        ],
        [
            "Tuần 02 · Ca 2", "9C-H5-P04", "Bài 16: Tiếp tuyến của đường tròn (Tính chất 2 tiếp tuyến)",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟠 Chờ duyệt",
            "https://drive.google.com/...", "https://drive.google.com/...", "https://drive.google.com/...",
            "—", "https://drive.google.com/...", False, "Thầy đang thẩm định sư phạm"
        ],
        [
            "Tuần 03 · Ca 1", "9C-H5-P05", "Bài 17: Vị trí tương đối của hai đường tròn",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "—", "—", False, "Đang chạy spec và bốc câu"
        ],
        [
            "Tuần 03 · Ca 2", "9C-H5-P06", "Luyện tập chung: Tiếp tuyến và hệ thức tích",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "—", "—", False, "Chờ duyệt P04 & P05"
        ],
        [
            "Tuần 04 · Ca 1", "9C-H5-P07", "Bài 18: Góc ở tâm, góc nội tiếp",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "—", "—", False, "Đang quét đề ngân hàng"
        ],
        [
            "Tuần 04 · Ca 2", "9C-H5-P08", "Bài 19: Tứ giác nội tiếp đường tròn",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "—", "—", False, "Đang quét đề ngân hàng"
        ],
        [
            "Tuần 05 · Ca 1", "9C-H5-P09", "Bài 19: Chứng minh tứ giác nội tiếp (Tổng hai góc đối = 180°)",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "—", "—", False, "Kế hoạch tuần 5"
        ],
        [
            "Tuần 05 · Ca 2", "9C-H5-P10", "Bài 19: Chứng minh tứ giác nội tiếp (Hai đỉnh kề cùng nhìn một cạnh)",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "—", "—", False, "Kế hoạch tuần 5"
        ],
        [
            "Tuần 06 · Ca 1", "9C-H5-P11", "Ôn tập tổng kết Chương V: Chuỗi bài toán đích vào 10",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "—", "—", False, "Kế hoạch tuần 6"
        ],
        [
            "Tuần 06 · Ca 2", "9C-H5-KTC", "Kiểm tra tổng kết Chương V (45 phút) + Chữa đề",
            "https://docs.google.com/...", "https://drive.google.com/...", "🟡 Đang soạn",
            "—", "—", "—", "https://drive.google.com/...", "—", False, "Kèm tờ đề + Ma trận đáp án"
        ],
    ]
    run_write_batch([{"op": "write", "range": "'04_Template_Quan_Tri_Tien_Do'!A1:M16", "data": rows}], "Tab 4 Data")

def format_all_tabs():
    """Áp dụng màu sắc, viền kẻ, căn lề và conditional formatting chuyên nghiệp."""
    reqs = []

    # 1. Format Header Rows for Tab 0 (01_Template_Phan_Dang)
    # Row 1 banner: Navy bold
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 47},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.12, "green": 0.23, "blue": 0.54},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 12},
                    "horizontalAlignment": "LEFT"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
        }
    })
    # Rows 2..4 note rows: light gray
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 47},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.96, "green": 0.97, "blue": 0.98},
                    "textFormat": {"foregroundColor": {"red": 0.28, "green": 0.33, "blue": 0.41}, "fontSize": 9},
                    "horizontalAlignment": "LEFT"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
        }
    })
    # Row 5 column headers: Navy blue, bold white text
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 0, "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 0, "endColumnIndex": 47},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.12, "green": 0.23, "blue": 0.54},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 10},
                    "horizontalAlignment": "CENTER",
                    "wrapStrategy": "WRAP"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,wrapStrategy)"
        }
    })

    # Căn giữa các cột mã số, cấp độ của Tab 0
    center_cols_tab0 = [2, 4, 6, 7, 8, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46]
    for c in center_cols_tab0:
        reqs.append({
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": c, "endColumnIndex": c + 1},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

    # 2. Format Tab 101 (Thuyết minh)
    # Row 1 banner: Orange bold
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 101, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 14},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.85, "green": 0.47, "blue": 0.02},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 12},
                    "horizontalAlignment": "LEFT"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
        }
    })
    # Row 3 KPI Headers: light yellow
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 101, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 7},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 1.0, "green": 0.95, "blue": 0.80},
                    "textFormat": {"bold": True, "fontSize": 9},
                    "horizontalAlignment": "CENTER"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
        }
    })
    # Row 4 KPI Values: bold numbers
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 101, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 7},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 1.0, "green": 0.98, "blue": 0.90},
                    "textFormat": {"bold": True, "fontSize": 11, "foregroundColor": {"red": 0.85, "green": 0.47, "blue": 0.02}},
                    "horizontalAlignment": "CENTER"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
        }
    })
    # Row 6 Table Header: Navy bold
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 101, "startRowIndex": 5, "endRowIndex": 6, "startColumnIndex": 0, "endColumnIndex": 14},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.12, "green": 0.23, "blue": 0.54},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 10},
                    "horizontalAlignment": "CENTER",
                    "wrapStrategy": "WRAP"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,wrapStrategy)"
        }
    })
    # Center numeric/code cols in Tab 101: A, B, E, F, G, H, I, J, K, L, M
    for c in [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        reqs.append({
            "repeatCell": {
                "range": {"sheetId": 101, "startRowIndex": 6, "endRowIndex": 50, "startColumnIndex": c, "endColumnIndex": c + 1},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

    # 3. Format Tab 103 (Tiến độ)
    # Row 1 banner: Purple bold
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 103, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 13},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.49, "green": 0.14, "blue": 0.80},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 12},
                    "horizontalAlignment": "LEFT"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
        }
    })
    # Row 4 Table Header: Purple dark
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": 103, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 13},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.35, "green": 0.10, "blue": 0.60},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 10},
                    "horizontalAlignment": "CENTER",
                    "wrapStrategy": "WRAP"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,wrapStrategy)"
        }
    })
    # Center cols in Tab 103: A, B, F, L
    for c in [0, 1, 5, 11]:
        reqs.append({
            "repeatCell": {
                "range": {"sheetId": 103, "startRowIndex": 4, "endRowIndex": 50, "startColumnIndex": c, "endColumnIndex": c + 1},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })

    # 5. Conditional Formatting for Tab 0 (Phân dạng)
    cond_rules_tab0 = [
        # AR: Đưa vào bài -> Green
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 43, "endColumnIndex": 44},
            "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Đưa vào bài"}]},
            "format": {
                "backgroundColor": {"red": 0.902, "green": 0.957, "blue": 0.918},
                "textFormat": {"foregroundColor": {"red": 0.075, "green": 0.451, "blue": 0.200}, "bold": True}
            }
        },
        # AR: Dự phòng -> Orange
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 43, "endColumnIndex": 44},
            "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Dự phòng"}]},
            "format": {
                "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                "textFormat": {"foregroundColor": {"red": 0.690, "green": 0.376, "blue": 0.0}, "bold": True}
            }
        },
        # AR: Loại -> Red
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 43, "endColumnIndex": 44},
            "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Loại"}]},
            "format": {
                "backgroundColor": {"red": 0.988, "green": 0.910, "blue": 0.902},
                "textFormat": {"foregroundColor": {"red": 0.773, "green": 0.133, "blue": 0.122}, "italic": True}
            }
        },
        # Cột C: VD -> Orange
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 2, "endColumnIndex": 3},
            "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VD"}]},
            "format": {
                "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                "textFormat": {"foregroundColor": {"red": 0.890, "green": 0.455, "blue": 0.0}, "bold": True}
            }
        },
        # Cột C: VDC -> Purple
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 2, "endColumnIndex": 3},
            "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VDC"}]},
            "format": {
                "backgroundColor": {"red": 0.953, "green": 0.910, "blue": 0.992},
                "textFormat": {"foregroundColor": {"red": 0.518, "green": 0.188, "blue": 0.808}, "bold": True}
            }
        },
        # Cột C: TH -> Green
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 2, "endColumnIndex": 3},
            "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "TH"}]},
            "format": {
                "backgroundColor": {"red": 0.902, "green": 0.957, "blue": 0.918},
                "textFormat": {"foregroundColor": {"red": 0.075, "green": 0.451, "blue": 0.200}, "bold": True}
            }
        },
        # Cột C: NB -> Blue
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 2, "endColumnIndex": 3},
            "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "NB"}]},
            "format": {
                "backgroundColor": {"red": 0.910, "green": 0.941, "blue": 0.996},
                "textFormat": {"foregroundColor": {"red": 0.102, "green": 0.451, "blue": 0.910}, "bold": True}
            }
        },
        # Cột N: NB kiến thức cũ -> Lavender Purple
        {
            "range": {"sheetId": 0, "startRowIndex": 5, "endRowIndex": 100, "startColumnIndex": 13, "endColumnIndex": 14},
            "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "NB kiến thức cũ"}]},
            "format": {
                "backgroundColor": {"red": 0.93, "green": 0.90, "blue": 0.96},
                "textFormat": {"foregroundColor": {"red": 0.42, "green": 0.13, "blue": 0.65}, "bold": True}
            }
        },
    ]
    for idx, r in enumerate(cond_rules_tab0):
        reqs.append({
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

    run_raw_batch(reqs, "Formatting, Borders, Colors and Conditional Rules across All Tabs")

def main():
    print("=" * 70)
    print("DỰNG BỘ 4 TAB TEMPLATE SHEETS MẪU TRÊN GOOGLE SHEETS")
    print(f"Spreadsheet ID: {SPREADSHEET_ID}")
    print("=" * 70)

    setup_grids_and_widths()
    populate_tab1_data()
    populate_tab2_data()
    populate_tab4_data()
    format_all_tabs()

    print("=" * 70)
    print("HOÀN THÀNH 100% BỘ TEMPLATE TRÊN GOOGLE SHEETS!")
    print(f"👉 Link truy cập: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
    print("=" * 70)

if __name__ == '__main__':
    main()

