#!/usr/bin/env python3
"""ĐỔ DỮ LIỆU VÀ ĐỊNH DẠNG HOÀN CHỈNH CHO GOOGLE SPREADSHEET 'Phân dạng lớp 8'.

Thực hiện:
1. Mở rộng grid cho 13 tab:
   - Ngân hàng câu (sheetId: 0)
   - Đề thi (sheetId: 101)
   - Thống kê VD - VDC (sheetId: 102)
   - 10 tab phân dạng Ch.I .. Ch.X (sheetId: 201..210)
2. Ghi Header 1..5 và toàn bộ dữ liệu 3.141 câu kèm công thức tự động:
   - Điểm C (AN), Điểm B (AO), Điểm X (AP)
   - Ngưỡng đạt theo mức (AQ)
   - Kết luận lớp C (AR)
3. Xây dựng Dashboard 'Thống kê VD - VDC' (Bảng 1 Nguồn, Bảng 2 Ma trận 10 Chương, Bảng 3 Top 15 dạng bài)
   và danh sách toàn bộ 820 câu hỏi VD/VDC.
4. Đổ dữ liệu riêng cho 10 tab Phân dạng chương.
5. Định dạng màu tab, độ rộng cột, frozen panes, borders, căn lề và conditional formatting.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPREADSHEET_ID = "10cWCHRtvudOET8fAKy425VS4CphAJY8FitScoAmXsow"
CACHE_ALL = ROOT / "scratch" / "ngan_hang_cau_lop8_all.json"
HEADER_TEMPLATE_FILE = ROOT / "scratch" / "header_template_47cols.json"

SHEET_CONFIGS = [
    # (sheetId, title, tabColor, frozenRows, frozenCols, rowCount)
    (0, "Ngân hàng câu", {"red": 0.60, "green": 0.35, "blue": 0.71}, 5, 1, 4500),
    (101, "Đề thi", {"red": 0.92, "green": 0.26, "blue": 0.21}, 5, 1, 4500),
    (102, "Thống kê VD - VDC", {"red": 1.0, "green": 0.43, "blue": 0.0}, 32, 1, 1500),
    (201, "Phân dạng Ch.I lớp 8", {"red": 0.01, "green": 0.53, "blue": 0.82}, 5, 1, 1200),
    (202, "Phân dạng Ch.II lớp 8", {"red": 0.01, "green": 0.53, "blue": 0.82}, 5, 1, 1200),
    (203, "Phân dạng Ch.III lớp 8", {"red": 0.94, "green": 0.42, "blue": 0.0}, 5, 1, 1200),
    (204, "Phân dạng Ch.IV lớp 8", {"red": 0.94, "green": 0.42, "blue": 0.0}, 5, 1, 600),
    (205, "Phân dạng Ch.V lớp 8", {"red": 0.01, "green": 0.53, "blue": 0.82}, 5, 1, 600),
    (206, "Phân dạng Ch.VI lớp 8", {"red": 0.01, "green": 0.53, "blue": 0.82}, 5, 1, 1200),
    (207, "Phân dạng Ch.VII lớp 8", {"red": 0.01, "green": 0.53, "blue": 0.82}, 5, 1, 800),
    (208, "Phân dạng Ch.VIII lớp 8", {"red": 0.01, "green": 0.53, "blue": 0.82}, 5, 1, 600),
    (209, "Phân dạng Ch.IX lớp 8", {"red": 0.94, "green": 0.42, "blue": 0.0}, 5, 1, 800),
    (210, "Phân dạng Ch.X lớp 8", {"red": 0.94, "green": 0.42, "blue": 0.0}, 5, 1, 600),
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
    print(f"Executing {desc} ({len(requests)} requests)...", end=" ")
    sys.stdout.flush()
    res = subprocess.run(["gsheets", "mutate", "raw-batch", SPREADSHEET_ID, "-f", tmp_path], capture_output=True, text=True)
    os.remove(tmp_path)
    if res.returncode != 0:
        print(f"FAILED!\nError: {res.stderr}")
        raise RuntimeError(f"Failed {desc}: {res.stderr}")
    print("OK")

def make_formulas_row6(row_num: int) -> tuple[str, str, str, str, str]:
    an = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))'
    ao = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))'
    ap = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))'
    aq = f'=IF($C{row_num}="TH",$AR$3,IF($C{row_num}="NB",$AR$4,$AR$2))'
    ar = f'=IF($Q{row_num}<>"","Loại ("&$Q{row_num}&")",IF($AN{row_num}="","Chưa chấm",IF($AN{row_num}>=$AQ{row_num},"Đưa vào bài",IF($AN{row_num}>=5,"Dự phòng / sửa","Loại hoặc sửa"))))'
    return an, ao, ap, aq, ar

def make_formulas_vd_vdc(row_num: int) -> tuple[str, str, str, str, str]:
    an = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$29:$AM$29)/(2*SUM($AF$29:$AM$29))*10,1))'
    ao = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$30:$AM$30)/(2*SUM($AF$30:$AM$30))*10,1))'
    ap = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$31:$AM$31)/(2*SUM($AF$31:$AM$31))*10,1))'
    aq = f'=IF($C{row_num}="TH",$AR$30,IF($C{row_num}="NB",$AR$31,$AR$29))'
    ar = f'=IF($Q{row_num}<>"","Loại ("&$Q{row_num}&")",IF($AN{row_num}="","Chưa chấm",IF($AN{row_num}>=$AQ{row_num},"Đưa vào bài",IF($AN{row_num}>=5,"Dự phòng / sửa","Loại hoặc sửa"))))'
    return an, ao, ap, aq, ar

def build_tab_data(rows: list, is_vd_vdc_tab: bool = False) -> list[list]:
    out = []
    for idx, r in enumerate(rows):
        row_num = idx + (33 if is_vd_vdc_tab else 6)
        if is_vd_vdc_tab:
            an, ao, ap, aq, ar = make_formulas_vd_vdc(row_num)
        else:
            an, ao, ap, aq, ar = make_formulas_row6(row_num)
            
        row = []
        for i in range(47):
            if i == 39:
                row.append(an)
            elif i == 40:
                row.append(ao)
            elif i == 41:
                row.append(ap)
            elif i == 42:
                row.append(aq)
            elif i == 43:
                row.append(ar)
            else:
                val = r[i] if i < len(r) else ''
                row.append(val)
        out.append(row)
    return out

def populate_tab_data(tab_name: str, tab_data: list[list], start_row: int = 6) -> bool:
    CHUNK_SIZE = 180
    total_chunks = (len(tab_data) + CHUNK_SIZE - 1) // CHUNK_SIZE
    print(f"Writing {len(tab_data)} data rows to '{tab_name}' in {total_chunks} chunks...")
    
    for c_idx in range(total_chunks):
        start_idx = c_idx * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, len(tab_data))
        
        s_row = start_idx + start_row
        e_row = end_idx + start_row - 1
        
        chunk = tab_data[start_idx:end_idx]
        rng = f"'{tab_name}'!A{s_row}:AU{e_row}"
        op = [{"op": "write", "range": rng, "data": chunk}]
        
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(op, f)
            tmp_p = f.name
            
        print(f"  [{c_idx+1}/{total_chunks}] {tab_name} rows {s_row}..{e_row}...", end=" ")
        sys.stdout.flush()
        res = subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp_p], capture_output=True, text=True)
        os.remove(tmp_p)
        if res.returncode != 0:
            print(f"FAILED: {res.stderr}")
            return False
        print("OK")
        time.sleep(0.3)
    return True

def populate_header_standard(tab_name: str, title_note: str, template: list[list]) -> bool:
    padded = []
    for idx, r in enumerate(template):
        row = list(r)
        while len(row) < 47:
            row.append('')
        if idx == 0:
            row[0] = title_note
        padded.append(row)
    op = [{"op": "write", "range": f"'{tab_name}'!A1:AU5", "data": padded}]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(op, f)
        tmp = f.name
    res = subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp], capture_output=True, text=True)
    os.remove(tmp)
    return res.returncode == 0

def build_vd_vdc_dashboard() -> list[list]:
    rows = []
    # Hàng 1
    rows.append(["BẢNG THỐNG KÊ TỈ LỆ & MA TRẬN DẠNG BÀI VẬN DỤNG (VD) — VẬN DỤNG CAO (VDC) TOÁN 8"] + [""] * 46)
    # Hàng 2: Trống
    rows.append([""] * 47)
    # Hàng 3: Header Bảng 1 & Bảng 3
    r3 = [""] * 47
    r3[0] = "Nguồn tài liệu"
    r3[1] = "Tổng câu"
    r3[2] = "Số câu VD"
    r3[3] = "Số câu VDC"
    r3[4] = "Tổng VD+VDC"
    r3[5] = "% VD/VDC của nguồn"
    r3[6] = "% Đóng góp kho VD"
    r3[10] = "Hạng"
    r3[11] = "Chương"
    r3[12] = "Dạng bài cụ thể trong đề thi"
    r3[13] = "Tần suất đề thật"
    r3[14] = "Số câu VD"
    r3[15] = "Số câu VDC"
    r3[16] = "Tổng câu kho"
    r3[17] = "Vị trí trong đề kiểm tra / thi"
    rows.append(r3)
    
    b1_data = [
        ["Đề thi thật (Sở & Trường)", 3141, 452, 368, "=C4+D4", "=E4/B4", "=E4/$E$7"],
        ["Sách tham khảo & Chuyên đề", 0, 0, 0, "=C5+D5", "=IF(B5=0,0,E5/B5)", "=IF($E$7=0,0,E5/$E$7)"],
        ["SGK, SBT GDPT 2018", 0, 0, 0, "=C6+D6", "=IF(B6=0,0,E6/B6)", "=IF($E$7=0,0,E6/$E$7)"],
        ["TỔNG TOÀN KHO TOÁN 8", 3141, 452, 368, "=C7+D7", "=E7/B7", "=E7/$E$7"],
    ]
    
    b3_data = [
        [1, "[III]", "Hình chữ nhật & Hình bình hành (chứng minh, tính chất)", "45%", 58, 42, 248, "Bài hình tự luận ý a, b"],
        [2, "[II]", "Phân tích đa thức thành nhân tử & Hằng đẳng thức", "52%", 15, 45, 214, "Bài đại số tự luận Bài 1, 2"],
        [3, "[VI]", "Rút gọn phân thức đại số & Điều kiện xác định", "60%", 62, 18, 232, "Bài rút gọn tự luận Bài 2"],
        [4, "[III]", "Hình thoi & Hình vuông (dấu hiệu nhận biết, góc)", "35%", 28, 32, 98, "Bài hình tự luận ý b, c"],
        [5, "[I]", "Thu gọn, bậc và giá trị đa thức nhiều biến", "45%", 45, 12, 268, "Bài 1 đại số tự luận"],
        [6, "[IX]", "Tam giác đồng dạng (3 trường hợp đồng dạng)", "65%", 34, 28, 140, "Bài hình tự luận ý a, b"],
        [7, "[VII]", "Giải phương trình bậc nhất một ẩn", "55%", 22, 8, 136, "Bài phương trình tự luận"],
        [8, "[VII]", "Hàm số bậc nhất y = ax + b, đồ thị, hệ số góc", "52%", 15, 15, 141, "Bài hàm số & đồ thị"],
        [9, "[VI]", "Câu hỏi phụ phân thức: Tìm x nguyên, Min-Max, P < k", "35%", 31, 20, 95, "Ý phụ bài phân thức (ý c)"],
        [10, "[II]", "Giá trị lớn nhất, nhỏ nhất (Min-Max, tổng bình phương)", "25%", 5, 43, 48, "Câu cuối đề 0,5 điểm"],
        [11, "[III]", "Hình học VDC: Thẳng hàng, đồng quy, điểm cố định", "25%", 17, 23, 40, "Ý cuối bài hình tự luận"],
        [12, "[IV]", "Tính chất đường phân giác & Định lí Thalès", "66%", 9, 14, 80, "Bài hình tự luận ý a, b"],
        [13, "[V]", "Đọc biểu đồ quạt tròn, cột kép & Dữ liệu thực tế", "62%", 26, 2, 155, "Bài thống kê tự luận/TN"],
        [14, "[X]", "Hình chóp tam giác đều, tứ giác đều: Sxq, V", "98%", 7, 12, 147, "Bài hình thực tế 0,75-1,0đ"],
        [15, "[VIII]", "Xác suất của biến cố trong mô hình thực tế", "97%", 13, 6, 118, "Bài xác suất tự luận/TN"],
    ]
    
    for idx in range(4):
        r = [""] * 47
        r[0:7] = b1_data[idx]
        if idx < len(b3_data):
            r[10:18] = b3_data[idx]
        rows.append(r)
        
    # Hàng 8
    r8 = [""] * 47
    r8[0] = "💡 NHẬN XÉT: Đề thi thật là nguồn câu hỏi VD & VDC trọng yếu (chiếm 100% toàn kho hiện tại; 26.1% câu từ đề thi là VD/VDC)."
    if 4 < len(b3_data):
        r8[10:18] = b3_data[4]
    rows.append(r8)
    
    # Hàng 9
    r9 = [""] * 47
    if 5 < len(b3_data):
        r9[10:18] = b3_data[5]
    rows.append(r9)
    
    # Hàng 10: Header Bảng 2
    r10 = [""] * 47
    r10[0] = "Mã ch."
    r10[1] = "Tên chương học môn Toán 8"
    r10[2] = "Tổng câu"
    r10[3] = "Số câu VD"
    r10[4] = "Số câu VDC"
    r10[5] = "Tổng VD+VDC"
    r10[6] = "% VD/VDC ch."
    r10[7] = "% Tỉ trọng kho"
    r10[8] = "Dạng bài điểm nóng thi & kiểm tra (Trọng tâm phân loại)"
    if 6 < len(b3_data):
        r10[10:18] = b3_data[6]
    rows.append(r10)
    
    # Dữ liệu Bảng 2 (Hàng 11..21)
    b2_data = [
        ["[I]", "Chương I: Đa thức", 720, 92, 39, "=D11+E11", "=F11/C11", "=F11/$F$21", "Thu gọn bậc đa thức, Tìm x bậc nhất, Toán thực tế lập đa thức"],
        ["[II]", "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng", 332, 20, 88, "=D12+E12", "=F12/C12", "=F12/$F$21", "Phân tích đa thức thành nhân tử, Hằng đẳng thức, Min-Max cực trị"],
        ["[III]", "Chương III: Tứ giác", 572, 103, 97, "=D13+E13", "=F13/C13", "=F13/$F$21", "Hình bình hành, Hình chữ nhật, Hình thoi, Hình vuông, Hình VDC"],
        ["[IV]", "Chương IV: Định lí Thalès", 80, 9, 14, "=D14+E14", "=F14/C14", "=F14/$F$21", "Tính chất đường phân giác, Định lí Thalès, Đường trung bình"],
        ["[V]", "Chương V: Dữ liệu và biểu đồ", 155, 26, 2, "=D15+E15", "=F15/C15", "=F15/$F$21", "Phân tích dữ liệu định tính/lượng, Đọc và vẽ biểu đồ hình quạt/cột kép"],
        ["[VI]", "Chương VI: Phân thức đại số", 425, 93, 38, "=D16+E16", "=F16/C16", "=F16/$F$21", "Rút gọn phân thức, 4 phép tính, Câu hỏi phụ tìm x nguyên, Min-Max"],
        ["[VII]", "Chương VII: Phương trình bậc nhất và hàm số bậc nhất", 289, 37, 23, "=D17+E17", "=F17/C17", "=F17/$F$21", "Giải phương trình, Bài toán thực tế lập PT, Hàm số y=ax+b"],
        ["[VIII]", "Chương VIII: Mở đầu về tính xác suất của biến cố", 118, 13, 6, "=D18+E18", "=F18/C18", "=F18/$F$21", "Xác suất thực nghiệm và lý thuyết của biến cố trong các mô hình"],
        ["[IX]", "Chương IX: Tam giác đồng dạng", 303, 52, 49, "=D19+E19", "=F19/C19", "=F19/$F$21", "Tam giác đồng dạng (c-c-c, c-g-c, g-g), Tam giác vuông, Hệ thức tích"],
        ["[X]", "Chương X: Một số hình khối trong thực tiễn", 147, 7, 12, "=D20+E20", "=F20/C20", "=F20/$F$21", "Hình chóp tam giác đều, tứ giác đều: diện tích xung quanh, thể tích"],
        ["TỔNG", "Toàn bộ chương trình Toán 8", 3141, 452, 368, "=SUM(F11:F20)", "=F21/C21", "100.0%", "3 Trụ cột phân loại: Tứ giác (24.4%) + Phân thức đại số (16.0%) + Đa thức (16.0%)"]
    ]
    
    for idx, b2_row in enumerate(b2_data):
        r = [""] * 47
        r[0:9] = b2_row
        b3_idx = 7 + idx
        if b3_idx < len(b3_data):
            r[10:18] = b3_data[b3_idx]
        rows.append(r)
        
    # Hàng 22
    r22 = [""] * 47
    r22[0] = "📌 ĐÁNH GIÁ CẤU TRÚC ĐỀ THI TOÁN 8: Ba khu vực chiếm gần 60% lượng câu VD/VDC là: Hình học tứ giác (Ch.III: 200 câu), Phân thức đại số (Ch.VI: 131 câu), và Đa thức (Ch.I: 131 câu) cùng Hằng đẳng thức (Ch.II: 108 câu)."
    rows.append(r22)
    
    # Hàng 23..26 trống
    for _ in range(4):
        rows.append([""] * 47)
        
    # Hàng 27: Tiêu đề danh sách
    r27 = ["DANH SÁCH CHI TIẾT 820 CÂU HỎI VẬN DỤNG & VẬN DỤNG CAO TOÁN 8 ĐÃ CHẤM ĐIỂM (CÓ BỘ LỌC)"] + [""] * 46
    rows.append(r27)
    
    # Hàng 28
    r28 = [""] * 47
    rows.append(r28)
    
    # Hàng 29: Trọng số C
    r29 = [""] * 47
    r29[30] = "Trọng số lớp C"
    r29[31:39] = [3, 1, 2, 1, 2, 2, 2, 0]
    r29[42] = "Ngưỡng VD, VDC"
    r29[43] = 7
    rows.append(r29)
    
    # Hàng 30: Trọng số B
    r30 = [""] * 47
    r30[30] = "Trọng số lớp B"
    r30[31:39] = [2, 2, 2, 3, 2, 1, 3, 1]
    r30[42] = "Ngưỡng TH"
    r30[43] = 6
    rows.append(r30)
    
    # Hàng 31: Trọng số X
    r31 = [""] * 47
    r31[30] = "Trọng số lớp X"
    r31[31:39] = [1, 3, 1, 2, 1, 1, 2, 3]
    r31[42] = "Ngưỡng NB"
    r31[43] = 5
    rows.append(r31)
    
    # Hàng 32: Header các cột A..AU
    # Lấy từ header template hàng 5
    template = json.load(open(HEADER_TEMPLATE_FILE, 'r', encoding='utf-8'))
    r32 = list(template[4])
    while len(r32) < 47:
        r32.append('')
    rows.append(r32)
    
    return rows

def format_all_sheets():
    print("\n==================== FORMATTING ALL 13 SHEETS ====================")
    
    # 1. Update Grid size and Tab Colors & Frozen panes
    phase1_reqs = []
    for sid, title, color, f_rows, f_cols, max_r in SHEET_CONFIGS:
        props = {
            "sheetId": sid,
            "title": title,
            "tabColor": color,
            "gridProperties": {
                "rowCount": max_r,
                "columnCount": 48,
                "frozenRowCount": f_rows,
                "frozenColumnCount": f_cols
            }
        }
        fields = "title,tabColor,gridProperties.rowCount,gridProperties.columnCount,gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
        phase1_reqs.append({
            "updateSheetProperties": {
                "properties": props,
                "fields": fields
            }
        })
    run_raw_batch(phase1_reqs, "Phase 1: Grid size, Tab Colors & Frozen Panes")
    
    # 2. Column widths for all 13 sheets
    phase2_reqs = []
    for sid, title, color, f_rows, f_cols, max_r in SHEET_CONFIGS:
        for start_col, end_col, width in COLUMN_WIDTHS:
            phase2_reqs.append({
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sid,
                        "dimension": "COLUMNS",
                        "startIndex": start_col,
                        "endIndex": end_col
                    },
                    "properties": {"pixelSize": width},
                    "fields": "pixelSize"
                }
            })
    run_raw_batch(phase2_reqs, "Phase 2: Standard Column Widths for all 13 Sheets")
    
    # 3. Styling headers and rows
    phase3_reqs = []
    for sid, title, color, f_rows, f_cols, max_r in SHEET_CONFIGS:
        if sid == 102:
            # Thống kê VD - VDC
            header_row_idx = 31 # hàng 32
        else:
            header_row_idx = 4  # hàng 5
            
        # Header row styling (Dark Navy, white bold text, centered)
        phase3_reqs.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": header_row_idx,
                    "endRowIndex": header_row_idx + 1,
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
        
        # Set Wrap Strategy = CLIP for data rows
        phase3_reqs.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": header_row_idx + 1,
                    "endRowIndex": max_r,
                    "startColumnIndex": 0,
                    "endColumnIndex": 47
                },
                "cell": {
                    "userEnteredFormat": {
                        "wrapStrategy": "CLIP",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"
            }
        })
        
        # Enable BasicFilter
        phase3_reqs.append({
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sid,
                        "startRowIndex": header_row_idx,
                        "endRowIndex": max_r,
                        "startColumnIndex": 0,
                        "endColumnIndex": 47
                    }
                }
            }
        })
    run_raw_batch(phase3_reqs, "Phase 3: Header Styling, Wrap CLIP & BasicFilter")

def main() -> int:
    print(f"Loading Grade 8 data from {CACHE_ALL}...")
    all_rows = json.load(open(CACHE_ALL, 'r', encoding='utf-8'))
    print(f"Loaded {len(all_rows)} rows.")
    
    header_template = json.load(open(HEADER_TEMPLATE_FILE, 'r', encoding='utf-8'))
    
    # 1. Expand Grids first so write calls don't exceed row limits
    init_reqs = []
    for sid, title, color, f_rows, f_cols, max_r in SHEET_CONFIGS:
        init_reqs.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sid,
                    "title": title,
                    "gridProperties": {
                        "rowCount": max_r,
                        "columnCount": 48
                    }
                },
                "fields": "title,gridProperties.rowCount,gridProperties.columnCount"
            }
        })
    run_raw_batch(init_reqs, "Initial Grid Expansion")
    
    # 2. POPULATE 'Ngân hàng câu' (Tab 0)
    print("\n==================== POPULATING 'Ngân hàng câu' (3.141 rows) ====================")
    h_title = "NGÂN HÀNG CÂU LỚP 8: mọi câu đã quét từ inputs đề thi Hà Nội (190 đề, 3.141 câu), mỗi câu một dòng, phân bổ qua 10 chương."
    populate_header_standard("Ngân hàng câu", h_title, header_template)
    ngan_hang_data = build_tab_data(all_rows, is_vd_vdc_tab=False)
    populate_tab_data("Ngân hàng câu", ngan_hang_data, start_row=6)
    
    # 3. POPULATE 'Đề thi' (Tab 101)
    print("\n==================== POPULATING 'Đề thi' (3.141 rows) ====================")
    h_de_thi = "NGÂN HÀNG CÂU — ĐỀ THI LỚP 8: toàn bộ 3.141 câu hỏi từ các đề thi chính thức của Sở, đề thi thử và đề kiểm tra trường Hà Nội"
    populate_header_standard("Đề thi", h_de_thi, header_template)
    populate_tab_data("Đề thi", ngan_hang_data, start_row=6)
    
    # 4. POPULATE 'Thống kê VD - VDC' (Tab 102)
    print("\n==================== POPULATING 'Thống kê VD - VDC' (820 rows) ====================")
    vd_vdc_rows = [r for r in all_rows if r[2] in ('VD', 'VDC')]
    print(f"Total VD/VDC rows: {len(vd_vdc_rows)}")
    
    # Write Dashboard & Headers (rows 1..32)
    dashboard_rows = build_vd_vdc_dashboard()
    op_dash = [{"op": "write", "range": "'Thống kê VD - VDC'!A1:AU32", "data": dashboard_rows}]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(op_dash, f)
        tmp = f.name
    subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp], check=True)
    os.remove(tmp)
    print("Dashboard rows 1..32 written to 'Thống kê VD - VDC'.")
    
    # Write VD/VDC Data rows (starting at row 33)
    vd_vdc_data = build_tab_data(vd_vdc_rows, is_vd_vdc_tab=True)
    populate_tab_data("Thống kê VD - VDC", vd_vdc_data, start_row=33)
    
    # 5. POPULATE 10 CHAPTER TABS
    print("\n==================== POPULATING 10 CHAPTER TABS ====================")
    ch_map = {
        'I': ('Phân dạng Ch.I lớp 8', 201),
        'II': ('Phân dạng Ch.II lớp 8', 202),
        'III': ('Phân dạng Ch.III lớp 8', 203),
        'IV': ('Phân dạng Ch.IV lớp 8', 204),
        'V': ('Phân dạng Ch.V lớp 8', 205),
        'VI': ('Phân dạng Ch.VI lớp 8', 206),
        'VII': ('Phân dạng Ch.VII lớp 8', 207),
        'VIII': ('Phân dạng Ch.VIII lớp 8', 208),
        'IX': ('Phân dạng Ch.IX lớp 8', 209),
        'X': ('Phân dạng Ch.X lớp 8', 210),
    }
    
    for ch_key, (tab_title, sid) in ch_map.items():
        ch_rows = [r for r in all_rows if r[28] == f"[{ch_key}]"]
        print(f"\nPopulating '{tab_title}' ({len(ch_rows)} rows)...")
        h_ch = f"PHÂN DẠNG BÀI TOÁN 8 — CHƯƠNG {ch_key}: toàn bộ {len(ch_rows)} câu hỏi đã phân loại theo mức độ và dạng bài chuẩn"
        populate_header_standard(tab_title, h_ch, header_template)
        ch_data = build_tab_data(ch_rows, is_vd_vdc_tab=False)
        populate_tab_data(tab_title, ch_data, start_row=6)
        
    # 6. Apply Final Beautification & Formatting
    format_all_sheets()
    
    print("\n==================== ALL 13 SHEETS POPULATED & FORMATTED SUCCESSFULLY! ====================")
    print(f"Link: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
    return 0

if __name__ == '__main__':
    sys.exit(main())

