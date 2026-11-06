#!/usr/bin/env python3
"""TẠO & ĐỊNH DẠNG TAB 'Thống kê VD - VDC' TRÊN GOOGLE SHEETS LỚP 9.

Cấu trúc:
- Phần A (Hàng 1..25): Dashboard thống kê tỉ lệ VD/VDC theo nguồn, theo 10 chương và top 15 dạng bài thi vào 10.
- Phần B (Hàng 27..1932): Tiêu đề, header chuẩn và toàn bộ 1.901 câu hỏi VD & VDC có công thức tự động tính điểm C/B/A và kết luận.
- Định dạng: Màu tab cam rực rỡ, độ rộng cột chuẩn, borders, wrap CLIP, conditional formatting nổi bật.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from format_tabs_beautifully import COLUMN_WIDTHS
SPREADSHEET_ID = "1OuzuBOhfWQu5RQJ7BxRRpP98bs6aOin2xvN0udz8yqg"
SHEET_TITLE = "Thống kê VD - VDC"
SHEET_ID = 893984615
CACHE_FILE = ROOT / "scratch" / "ngan_hang_cau_scored_all.json"

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


def step1_expand_grid_and_tab_color():
    # Mở rộng sheet lên 2200 hàng x 50 cột, tabColor màu cam
    requests = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": SHEET_ID,
                    "title": SHEET_TITLE,
                    "tabColor": {"red": 1.0, "green": 0.43, "blue": 0.0},
                    "gridProperties": {
                        "rowCount": 2200,
                        "columnCount": 50,
                        "frozenColumnCount": 0
                    }
                },
                "fields": "title,tabColor,gridProperties.rowCount,gridProperties.columnCount,gridProperties.frozenColumnCount"
            }
        }
    ]
    run_raw_batch(requests, "Step 1: Expand grid & set tabColor")


def build_dashboard_rows() -> list[list]:
    # 26 hàng Dashboard (Hàng 1..26)
    rows = []
    
    # Hàng 1: Banner Tiêu đề lớn
    r1 = ["BẢNG THỐNG KÊ TỈ LỆ & MA TRẬN DẠNG BÀI VẬN DỤNG (VD) — VẬN DỤNG CAO (VDC) TOÁN 9 VÀO 10"] + [""] * 46
    rows.append(r1)
    
    # Hàng 2: Trống
    rows.append([""] * 47)
    
    # Hàng 3: Header Bảng 1 & Bảng 3
    r3 = [""] * 47
    # Bảng 1 (Cột A..G)
    r3[0] = "Nguồn tài liệu"
    r3[1] = "Tổng câu"
    r3[2] = "Số câu VD"
    r3[3] = "Số câu VDC"
    r3[4] = "Tổng VD+VDC"
    r3[5] = "% VD/VDC của nguồn"
    r3[6] = "% Đóng góp kho VD"
    r3[7] = ""
    r3[8] = ""
    r3[9] = ""
    # Bảng 3 (Cột K..R) -> index 10..17
    r3[10] = "Hạng"
    r3[11] = "Chương"
    r3[12] = "Dạng bài cụ thể trong đề thi"
    r3[13] = "Tần suất đề thật"
    r3[14] = "Số câu VD"
    r3[15] = "Số câu VDC"
    r3[16] = "Tổng câu kho"
    r3[17] = "Vị trí trong đề thi Vào 10"
    rows.append(r3)
    
    # Dữ liệu Bảng 1 (Hàng 4..7)
    b1_data = [
        ["Đề thi thật (Sở & Trường)", 2229, 653, 406, "=C4+D4", "=E4/B4", "=E4/$E$7"],
        ["Sách tham khảo & Chuyên đề", 2535, 580, 166, "=C5+D5", "=E5/B5", "=E5/$E$7"],
        ["SGK, SBT GDPT 2018", 801, 95, 1, "=C6+D6", "=E6/B6", "=E6/$E$7"],
        ["TỔNG TOÀN KHO TOÁN 9", 5565, 1328, 573, "=C7+D7", "=E7/B7", "=E7/$E$7"],
    ]
    
    # Dữ liệu Bảng 3 (Top 15 dạng bài - Hàng 4..18)
    b3_data = [
        [1, "[III]", "Rút gọn biểu thức chứa căn", "99%", 205, 25, 230, "Câu I.3 (Phân loại rút gọn)"],
        [2, "[IX]", "Tứ giác nội tiếp & thẳng hàng", "96%", 69, 151, 220, "Câu IV.2 ý b, c (Hình phân loại)"],
        [3, "[VI]", "Giải PT bậc 2 & ứng dụng", "84%", 151, 17, 168, "Câu III.1 (Phương trình)"],
        [4, "[V]", "Tính chất góc & đoạn tròn", "51%", 79, 15, 94, "Câu IV.2 ý a (Khởi động hình)"],
        [5, "[IV]", "Tỉ số lượng giác góc nhọn", "60%", 59, 29, 88, "Câu IV.1 (Hình thực tế)"],
        [6, "[V]", "Bốn điểm cùng thuộc đường tròn", "77%", 37, 49, 86, "Câu IV.2 ý a, b"],
        [7, "[I]", "Giải hệ PT cơ bản & tham số", "76%", 84, 1, 85, "Câu III.1 (Hệ phương trình)"],
        [8, "[VI]", "Hệ thức Vi-ét & nghiệm tham số", "66%", 63, 17, 80, "Câu III.2 ý b (Vi-ét phân loại)"],
        [9, "[V]", "Chứng minh quan hệ vuông góc", "69%", 56, 18, 74, "Câu IV.2 ý b, c"],
        [10, "[IV]", "TSLG thực tế đo khoảng cách", "74%", 50, 5, 55, "Câu IV.1 (Thực tế góc dốc/chiều cao)"],
        [11, "[III]", "Phương trình chứa căn thức", "98%", 27, 24, 51, "Câu I.3 / Câu V"],
        [12, "[II]", "Bất phương trình bậc nhất thực tế", "57%", 42, 5, 47, "Câu II.1 (Toán thực tế)"],
        [13, "[VDC]", "Tối ưu hóa kinh tế (Lợi nhuận/chi phí)", "51%", 6, 40, 46, "Câu II.1 / Câu V (Cực trị mới)"],
        [14, "[VDC]", "Hình học tối ưu & Min-Max", "47%", 7, 35, 42, "Câu V (Điểm 10 phân loại cao)"],
        [15, "[X]", "Hình trụ, hình nón, hình cầu thực tế", "84%", 33, 0, 33, "Câu II.2 (Hình học không gian)"],
    ]
    
    # Ghép hàng 4..7
    for idx in range(4):
        r = [""] * 47
        r[0:7] = b1_data[idx]
        if idx < len(b3_data):
            r[10:18] = b3_data[idx]
        rows.append(r)
        
    # Hàng 8: Nhận xét Bảng 1
    r8 = [""] * 47
    r8[0] = "💡 NHẬN XÉT: Đề thi thật là nguồn câu hỏi VD & VDC trọng yếu (chiếm 55.7% toàn kho; 47.5% câu từ đề thi là VD/VDC)."
    if 4 < len(b3_data):
        r8[10:18] = b3_data[4]
    rows.append(r8)
    
    # Hàng 9: Trống bên trái, Bảng 3 tiếp
    r9 = [""] * 47
    if 5 < len(b3_data):
        r9[10:18] = b3_data[5]
    rows.append(r9)
    
    # Hàng 10: Header Bảng 2
    r10 = [""] * 47
    r10[0] = "Mã ch."
    r10[1] = "Tên chương học môn Toán 9"
    r10[2] = "Tổng câu"
    r10[3] = "Số câu VD"
    r10[4] = "Số câu VDC"
    r10[5] = "Tổng VD+VDC"
    r10[6] = "% VD/VDC ch."
    r10[7] = "% Tỉ trọng kho"
    r10[8] = "Dạng bài điểm nóng thi Vào 10 (Trọng tâm phân loại)"
    if 6 < len(b3_data):
        r10[10:18] = b3_data[6]
    rows.append(r10)
    
    # Dữ liệu Bảng 2 (10 chương + Cực trị + Tổng = 12 dòng, từ hàng 11..22)
    b2_data = [
        ["[I]", "Phương trình & Hệ hai PT bậc nhất 2 ẩn", 413, 130, 1, "=D11+E11", "=F11/C11", "=F11/$F$22", "Toán thực tế lập hệ PT, Hệ đối xứng / chứa tham số"],
        ["[II]", "Bất đẳng thức & Bất phương trình bậc nhất 1 ẩn", 461, 97, 10, "=D12+E12", "=F12/C12", "=F12/$F$22", "BPT bậc nhất thực tế, BĐT Cô-si / Min-Max cơ bản"],
        ["[III]", "Căn bậc hai & Căn bậc ba (Biểu thức chứa căn)", 545, 260, 60, "=D13+E13", "=F13/C13", "=F13/$F$22", "Rút gọn biểu thức căn & Câu hỏi phụ (Tìm x nguyên, Min-Max, P < k)"],
        ["[IV]", "Hệ thức lượng trong tam giác vuông", 1162, 140, 39, "=D14+E14", "=F14/C14", "=F14/$F$22", "Toán thực tế đo chiều cao/khoảng cách, Tỉ số lượng giác góc dốc"],
        ["[V]", "Đường tròn (Khái niệm, Vị trí tương đối, Tiếp tuyến)", 1041, 229, 95, "=D15+E15", "=F15/C15", "=F15/$F$22", "Hai tiếp tuyến cắt nhau, 4 điểm cùng thuộc đường tròn, góc vuông"],
        ["[VI]", "Hàm số bậc hai y = ax² & Hệ thức Viète", 600, 243, 41, "=D16+E16", "=F16/C16", "=F16/$F$22", "Tương giao Parabol & đường thẳng, Hệ thức Vi-ét có tham số m"],
        ["[VII]", "Tần số & Bảng biểu đồ thống kê", 235, 12, 0, "=D17+E17", "=F17/C17", "=F17/$F$22", "Đọc bảng tần số tương đối ghép nhóm, Phân tích biểu đồ thực tế"],
        ["[VIII]", "Xác suất của biến cố trong một số mô hình", 225, 16, 0, "=D18+E18", "=F18/C18", "=F18/$F$22", "Tính xác suất thực tế bằng sơ đồ hình cây, Không gian mẫu"],
        ["[IX]", "Đa giác đều, Phép quay & Tứ giác nội tiếp", 450, 104, 173, "=D19+E19", "=F19/C19", "=F19/$F$22", "Tứ giác nội tiếp, Chứng minh thẳng hàng, Đồng quy, Điểm cố định"],
        ["[X]", "Hình trụ, Hình nón, Hình cầu", 240, 55, 9, "=D20+E20", "=F20/C20", "=F20/$F$22", "Toán thực tế tính thể tích, diện tích xung quanh vật thể trong đời sống"],
        ["[VDC]", "Toán tối ưu hóa & Cực trị thực tế (GDPT 2018)", 91, 13, 77, "=D21+E21", "=F21/C21", "=F21/$F$22", "Tối ưu hóa kinh tế (lợi nhuận/chi phí), Bất đẳng thức thực tế"],
        ["TỔNG", "Toàn bộ chương trình Toán 9", 5565, 1328, 573, "=SUM(F11:F21)", "=F22/C22", "100.0%", "3 Trụ cột phân loại: Rút gọn căn (17%) + Đường tròn (32%) + Hàm số Vi-ét (15%)"]
    ]
    
    for idx, b2_row in enumerate(b2_data):
        r = [""] * 47
        r[0:9] = b2_row
        b3_idx = 7 + idx
        if b3_idx < len(b3_data):
            r[10:18] = b3_data[b3_idx]
        rows.append(r)
        
    # Hàng 23..24: Đánh giá tổng kết Bảng 2
    r23 = [""] * 47
    r23[0] = "📌 ĐÁNH GIÁ CẤU TRÚC ĐỀ VÀO 10: Ba khu vực chiếm tới 64% lượng câu VD/VDC là: Hình học đường tròn (Ch.V & IX: 601 câu), Biểu thức căn (Ch.III: 320 câu), và Hàm số bậc hai Vi-ét (Ch.VI: 284 câu)."
    rows.append(r23)
    
    # Hàng 24: Trống
    rows.append([""] * 47)
    # Hàng 25: Trống
    rows.append([""] * 47)
    # Hàng 26: Trống (để Hàng 27 là Tiêu đề danh sách, Hàng 28 là Trọng số C!)
    rows.append([""] * 47)
    
    return rows


def build_list_header_rows() -> list[list]:
    # Hàng 27: Tiêu đề danh sách
    r27 = ["DANH SÁCH CHI TIẾT 1.901 CÂU HỎI VẬN DỤNG & VẬN DỤNG CAO ĐÃ CHẤM ĐIỂM (CÓ BỘ LỌC)"] + [""] * 46
    
    # Hàng 28: Trọng số C
    r28 = [""] * 47
    r28[30] = "Trọng số lớp C"
    r28[31:39] = [3, 1, 2, 1, 2, 2, 2, 0]
    r28[41] = ""
    r28[42] = "Ngưỡng VD, VDC"
    r28[43] = 7
    
    # Hàng 29: Trọng số B
    r29 = [""] * 47
    r29[30] = "Trọng số lớp B"
    r29[31:39] = [2, 2, 2, 3, 2, 1, 3, 1]
    r29[42] = "Ngưỡng TH"
    r29[43] = 6
    
    # Hàng 30: Trọng số X
    r30 = [""] * 47
    r30[30] = "Trọng số lớp X"
    r30[31:39] = [1, 3, 1, 2, 1, 1, 2, 3]
    r30[42] = "Ngưỡng NB"
    r30[43] = 5
    
    # Hàng 31: Tên 47 cột
    r31 = [
        "Bài cụ thể", "Nguồn trong input", "Mức độ (cao nhất trong bài; VD lên trước để lựa chọn)", "Dạng bài",
        "Ưu tiên đưa vào phiếu", "Phân loại vào phiếu nào? (gợi ý theo khung 4 buổi)", "Thời lượng làm dự kiến (phút)",
        "Có liên quan thực tế không?", "Format câu hỏi", "Mức độ từng ý", "Bài học SGK", "Ghi chú phạm vi",
        "Mã câu (định danh duy nhất)", "Loại câu (NB lẻ LT, TH tách VD...)", "Dạng quy chuẩn theo khung", "Mục tiêu bài học",
        "Đã dùng", "Trạng thái", "Lớp C", "Lớp B", "Lớp A", "Ghi chú chọn câu", "Loại nguồn",
        "Dạng phiếu C (Khung phân dạng)", "Mã nguồn", "Dạng từng ý trong đề thật", "T7 gợi ý", "Link", "Chương",
        "Dự phòng", "Dự phòng 2", "T1: Đúng trọng tâm", "T2: Nghiệm đẹp", "T3: Vừa sức", "T4: Chuẩn thi",
        "T5: Dễ biến đổi", "T6: Tường minh", "T7: Đề thi thật", "T8: Lừa bẫy", "Điểm C", "Điểm B", "Điểm A",
        "Ngưỡng đạt", "Kết luận", "Lý do chọn câu", "Lí do chấm điểm chi tiết (T1-T8)", "Dạng bài bổ sung"
    ]
    
    return [r27, r28, r29, r30, r31]


def make_vd_formulas(row_num: int) -> tuple[str, str, str, str, str]:
    an = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$28:$AM$28)/(2*SUM($AF$28:$AM$28))*10,1))'
    ao = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$29:$AM$29)/(2*SUM($AF$29:$AM$29))*10,1))'
    ap = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$30:$AM$30)/(2*SUM($AF$30:$AM$30))*10,1))'
    aq = f'=IF($C{row_num}="TH",$AR$29,IF($C{row_num}="NB",$AR$30,$AR$28))'
    ar = f'=IF($Q{row_num}<>"","Loại ("&$Q{row_num}&")",IF($AN{row_num}="","Chưa chấm",IF($AN{row_num}>=$AQ{row_num},"Đưa vào bài",IF($AN{row_num}>=5,"Dự phòng / sửa","Loại hoặc sửa"))))'
    return an, ao, ap, aq, ar


def step2_write_dashboard_and_header():
    dash_rows = build_dashboard_rows()  # Hàng 1..26 (26 rows)
    header_rows = build_list_header_rows()  # Hàng 27..31 (5 rows)
    all_top = dash_rows + header_rows  # 31 rows (1..31)
    
    op = [{"op": "write", "range": f"'{SHEET_TITLE}'!A1:AU31", "data": all_top}]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(op, f, ensure_ascii=False)
        tmp_path = f.name
        
    cmd = ["gsheets", "mutate", "batch", SPREADSHEET_ID, "-f", tmp_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to write dashboard: {res.stderr}")
    print("  -> SUCCESS: Dashboard & Headers written (Rows 1..31)")


def step3_populate_vd_vdc_rows():
    with open(CACHE_FILE) as f:
        all_rows = json.load(f)
        
    vd_vdc_rows = [r for r in all_rows if len(r) > 2 and r[2].strip() in ("VD", "VDC")]
    print(f"Extracted {len(vd_vdc_rows)} VD & VDC rows from bank.")
    
    chunk_size = 150
    total_chunks = (len(vd_vdc_rows) + chunk_size - 1) // chunk_size
    
    for c_idx in range(total_chunks):
        start_i = c_idx * chunk_size
        end_i = min(start_i + chunk_size, len(vd_vdc_rows))
        chunk_data = vd_vdc_rows[start_i:end_i]
        
        start_row = 32 + start_i
        end_row = 32 + end_i - 1
        
        chunk_values = []
        for r_offset, r in enumerate(chunk_data):
            cur_row = start_row + r_offset
            row_copy = list(r)
            if len(row_copy) < 47:
                row_copy += [""] * (47 - len(row_copy))
            an, ao, ap, aq, ar = make_vd_formulas(cur_row)
            row_copy[39] = an
            row_copy[40] = ao
            row_copy[41] = ap
            row_copy[42] = aq
            row_copy[43] = ar
            chunk_values.append(row_copy[:47])
            
        op = [{"op": "write", "range": f"'{SHEET_TITLE}'!A{start_row}:AU{end_row}", "data": chunk_values}]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(op, f, ensure_ascii=False)
            tmp_path = f.name
            
        cmd = ["gsheets", "mutate", "batch", SPREADSHEET_ID, "-f", tmp_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Failed chunk {c_idx+1}: {res.stderr}")
        print(f"  [{c_idx+1}/{total_chunks}] Rows {start_row}..{end_row} ({len(chunk_values)} rows)... OK")
        time.sleep(0.5)
        
    print(f"Successfully populated all {len(vd_vdc_rows)} VD/VDC rows!")


def step4_format_and_style():
    max_row = 1935
    requests = []
    
    # 0. Unfreeze columns to allow merges
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": SHEET_ID,
                "gridProperties": {
                    "frozenColumnCount": 0,
                    "frozenRowCount": 0
                }
            },
            "fields": "gridProperties.frozenColumnCount,gridProperties.frozenRowCount"
        }
    })
    
    # 1. Merges
    # Merge A1:R1 (Tiêu đề lớn)
    requests.append({
        "mergeCells": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 18},
            "mergeType": "MERGE_ALL"
        }
    })
    # Merge A8:G8 (Nhận xét Bảng 1)
    requests.append({
        "mergeCells": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 7, "endRowIndex": 8, "startColumnIndex": 0, "endColumnIndex": 7},
            "mergeType": "MERGE_ALL"
        }
    })
    # Merge A23:I24 (Đánh giá Bảng 2)
    requests.append({
        "mergeCells": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 22, "endRowIndex": 24, "startColumnIndex": 0, "endColumnIndex": 9},
            "mergeType": "MERGE_ALL"
        }
    })
    # Merge A27:AU27 (Tiêu đề danh sách)
    requests.append({
        "mergeCells": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 26, "endRowIndex": 27, "startColumnIndex": 0, "endColumnIndex": 47},
            "mergeType": "MERGE_ALL"
        }
    })
    
    # 2. Format Tiêu đề lớn (Row 1)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 18},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.102, "green": 0.137, "blue": 0.494}, # Navy đậm #1A237E
                    "textFormat": {"fontFamily": "Arial", "fontSize": 12, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    })
    
    # 3. Format Header Bảng 1 & Bảng 3 (Row 3: startRowIndex: 2, endRowIndex: 3)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 7},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.173, "green": 0.243, "blue": 0.314}, # Dark Slate
                    "textFormat": {"fontFamily": "Arial", "fontSize": 10, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    })
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 10, "endColumnIndex": 18},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.824, "green": 0.353, "blue": 0.0}, # Dark Amber #D35400
                    "textFormat": {"fontFamily": "Arial", "fontSize": 10, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    })
    
    # 4. Format Header Bảng 2 (Row 10: startRowIndex: 9, endRowIndex: 10)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 9, "endRowIndex": 10, "startColumnIndex": 0, "endColumnIndex": 9},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.012, "green": 0.408, "blue": 0.216}, # Dark Green #026837
                    "textFormat": {"fontFamily": "Arial", "fontSize": 10, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    })
    
    # 5. Format Dòng tổng Bảng 1 (Row 7) và Bảng 2 (Row 22)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 6, "endRowIndex": 7, "startColumnIndex": 0, "endColumnIndex": 7},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.94, "green": 0.94, "blue": 0.94},
                    "textFormat": {"bold": True}
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat.bold)"
        }
    })
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 21, "endRowIndex": 22, "startColumnIndex": 0, "endColumnIndex": 9},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.94, "green": 0.94, "blue": 0.94},
                    "textFormat": {"bold": True}
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat.bold)"
        }
    })
    
    # 6. Format Tiêu đề danh sách (Row 27: startRowIndex: 26, endRowIndex: 27)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 26, "endRowIndex": 27, "startColumnIndex": 0, "endColumnIndex": 47},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.173, "green": 0.243, "blue": 0.314},
                    "textFormat": {"fontFamily": "Arial", "fontSize": 11, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    })
    
    # 7. Format Header câu hỏi (Row 31: startRowIndex: 30, endRowIndex: 31)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 30, "endRowIndex": 31, "startColumnIndex": 0, "endColumnIndex": 47},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.204, "green": 0.286, "blue": 0.369},
                    "textFormat": {"fontFamily": "Arial", "fontSize": 10, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE",
                    "wrapStrategy": "WRAP"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)"
        }
    })
    
    # 8. Format Data rows (Hàng 32 trở đi)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 0, "endColumnIndex": 47},
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
    
    # 9. Format các cột căn giữa: C (Cấp độ), G, H, I, S, T, U, AA, AC, AF..AM, AN..AR
    center_ranges = [
        (2, 3), (6, 9), (18, 21), (26, 29), (31, 39), (39, 44)
    ]
    for sc, ec in center_ranges:
        requests.append({
            "repeatCell": {
                "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": sc, "endColumnIndex": ec},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(horizontalAlignment)"
            }
        })
        
    # In đậm Cột C, AN, AO, AP, AR
    bold_cols = [(2, 3), (39, 42), (43, 44)]
    for sc, ec in bold_cols:
        requests.append({
            "repeatCell": {
                "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": sc, "endColumnIndex": ec},
                "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                "fields": "userEnteredFormat(textFormat.bold)"
            }
        })
        
    # Cột Z nền vàng pastel nhẹ
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 25, "endColumnIndex": 26},
            "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1.0, "green": 0.99, "blue": 0.90}}},
            "fields": "userEnteredFormat(backgroundColor)"
        }
    })
    
    # 10. Column widths
    from format_tabs_beautifully import COLUMN_WIDTHS
    for sc, ec, w in COLUMN_WIDTHS:
        requests.append({
            "updateDimensionProperties": {
                "range": {"sheetId": SHEET_ID, "dimension": "COLUMNS", "startIndex": sc, "endIndex": ec},
                "properties": {"pixelSize": w},
                "fields": "pixelSize"
            }
        })

    # 10b. Number formats: % cho Dashboard và 0.0 cho Điểm số
    # % cho Bảng 1: F4:G7
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 3, "endRowIndex": 7, "startColumnIndex": 5, "endColumnIndex": 7},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}}},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    # % cho Bảng 2: G11:H22
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 10, "endRowIndex": 22, "startColumnIndex": 6, "endColumnIndex": 8},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}}},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    # Điểm C, B, A (Cột AN..AP: col 39..42) -> 0.0
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 39, "endColumnIndex": 42},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "0.0"}}},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    # Ngưỡng đạt (Cột AQ: col 42..43) -> 0
    requests.append({
        "repeatCell": {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 42, "endColumnIndex": 43},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "0"}}},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
        
    # 11. BasicFilter từ Hàng 31 (startRowIndex: 30) đến max_row
    requests.append({
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": SHEET_ID,
                    "startRowIndex": 30,
                    "endRowIndex": max_row,
                    "startColumnIndex": 0,
                    "endColumnIndex": 47
                }
            }
        }
    })
    
    # 12. Conditional formatting rules
    cf_rules = [
        # Cột AR: "Đưa vào bài"
        {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 43, "endColumnIndex": 44},
            "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Đưa vào bài"}]},
            "format": {
                "backgroundColor": {"red": 0.902, "green": 0.957, "blue": 0.918},
                "textFormat": {"foregroundColor": {"red": 0.075, "green": 0.451, "blue": 0.200}, "bold": True}
            }
        },
        # Cột AR: "Dự phòng"
        {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 43, "endColumnIndex": 44},
            "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Dự phòng"}]},
            "format": {
                "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                "textFormat": {"foregroundColor": {"red": 0.690, "green": 0.376, "blue": 0.0}, "bold": True}
            }
        },
        # Cột AR: "Loại"
        {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 43, "endColumnIndex": 44},
            "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Loại"}]},
            "format": {
                "backgroundColor": {"red": 0.988, "green": 0.910, "blue": 0.902},
                "textFormat": {"foregroundColor": {"red": 0.773, "green": 0.133, "blue": 0.122}, "italic": True}
            }
        },
        # Cột C: "VD"
        {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 2, "endColumnIndex": 3},
            "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VD"}]},
            "format": {
                "backgroundColor": {"red": 0.996, "green": 0.969, "blue": 0.878},
                "textFormat": {"foregroundColor": {"red": 0.890, "green": 0.455, "blue": 0.0}, "bold": True}
            }
        },
        # Cột C: "VDC"
        {
            "range": {"sheetId": SHEET_ID, "startRowIndex": 31, "endRowIndex": max_row, "startColumnIndex": 2, "endColumnIndex": 3},
            "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "VDC"}]},
            "format": {
                "backgroundColor": {"red": 0.953, "green": 0.910, "blue": 0.992},
                "textFormat": {"foregroundColor": {"red": 0.518, "green": 0.188, "blue": 0.808}, "bold": True}
            }
        },
    ]
    for idx, r in enumerate(cf_rules):
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
        
    run_raw_batch(requests, "Step 4: Full formatting, merges, filter & conditional rules")


def main():
    print("=== UPDATING TAB 'Thống kê VD - VDC' ===")
    step2_write_dashboard_and_header()
    step3_populate_vd_vdc_rows()
    step4_format_and_style()
    print("=== TAB 'Thống kê VD - VDC' COMPLETED SUCCESSFULLY! ===")


if __name__ == "__main__":
    main()
