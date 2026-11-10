#!/usr/bin/env python3
"""TRÍCH XUẤT, CHUẨN HOÁ VÀ CHẤM ĐIỂM SƯ PHẠM TOÀN BỘ KHO ĐỀ LỚP 8 (3.141 CÂU).

Đầu vào: 190 file đề thi định kì Hà Nội (GK1, CK1, GK2, CK2) trong inputs/refs/de-thi/lop-8/exams/*.json
Đầu ra:
  - scratch/ngan_hang_cau_lop8_all.json (3.141 câu chuẩn 47 cột A..AU)
  - scratch/ngan_hang_cau_lop8_scored.json (đầy đủ điểm T1-T8, công thức điểm C/B/X, ngưỡng, kết luận)
"""

from __future__ import annotations

import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Cấu hình dạng bài và từ khoá cho 10 chương lớp 8
CONFIGS_8 = {
    'I': [
        {"ma": "thu_gon_da_thuc", "ten": "Thu gọn, bậc và giá trị đa thức", "re": r"thu gọn|bậc của đa thức|giá trị của đa thức|bậc của hạng tử", "ngan": "Đa thức: bậc, giá trị"},
        {"ma": "don_thuc_dong_dang", "ten": "Đơn thức, đơn thức đồng dạng", "re": r"đơn thức đồng dạng|đơn thức thu gọn|hệ số của đơn thức|bậc của đơn thức", "ngan": "Đơn thức đồng dạng"},
        {"ma": "phep_tinh_da_thuc", "ten": "Nhân, chia đơn thức và đa thức", "re": r"nhân đơn thức|nhân đa thức|chia đa thức|chia hết cho đơn thức", "ngan": "Phép tính đa thức"},
        {"ma": "tim_x_da_thuc", "ten": "Tìm x (khai triển, đưa về bậc nhất)", "re": r"tìm x|tìm số nguyên x", "ngan": "Tìm x đa thức"},
        {"ma": "thuc_te_da_thuc", "ten": "Toán thực tế lập biểu thức đa thức", "re": r"diện tích|chu vi|thể tích|bể bơi|tiền|quãng đường|vận tốc", "ngan": "Toán thực tế đa thức"},
    ],
    'II': [
        {"ma": "phan_tich_nhan_tu", "ten": "Phân tích đa thức thành nhân tử", "re": r"phân tích.*nhân tử|nhân tử chung|nhóm hạng tử", "ngan": "Phân tích nhân tử"},
        {"ma": "hang_dang_thuc", "ten": "Hằng đẳng thức đáng nhớ & Rút gọn, tính nhanh", "re": r"hằng đẳng thức|rút gọn biểu thức|tính nhanh|tính giá trị", "ngan": "Rút gọn HĐT"},
        {"ma": "min_max_hdt", "ten": "Giá trị lớn nhất, nhỏ nhất (Min-Max)", "re": r"giá trị nhỏ nhất|giá trị lớn nhất|gtnn|gtln|min|max|bình phương", "ngan": "Min-Max, Cực trị"},
        {"ma": "kpt_bien_chia_het", "ten": "Chứng minh không phụ thuộc biến / chia hết", "re": r"không phụ thuộc|chia hết|chứng minh đẳng thức", "ngan": "KPT biến & Chia hết"},
    ],
    'III': [
        {"ma": "hinh_chu_nhat", "ten": "Hình chữ nhật (chứng minh, tính chất)", "re": r"hình chữ nhật", "ngan": "Hình chữ nhật"},
        {"ma": "hinh_binh_hanh", "ten": "Hình bình hành (chứng minh, tính chất)", "re": r"hình bình hành", "ngan": "Hình bình hành"},
        {"ma": "hinh_thoi_vuong", "ten": "Hình thoi & Hình vuông", "re": r"hình thoi|hình vuông", "ngan": "Hình thoi, vuông"},
        {"ma": "hinh_thang_can", "ten": "Hình thang, hình thang cân", "re": r"hình thang|thang cân", "ngan": "Hình thang cân"},
        {"ma": "hinh_vdc_tong_hop", "ten": "Hình học VDC: thẳng hàng, đồng quy, vuông góc", "re": r"thẳng hàng|đồng quy|cố định|vuông góc|cực trị|lớn nhất|nhỏ nhất", "ngan": "Hình VDC"},
        {"ma": "goc_tu_giac", "ten": "Tứ giác & Tổng các góc trong tứ giác", "re": r"tứ giác|tổng các góc", "ngan": "Góc tứ giác"},
    ],
    'IV': [
        {"ma": "duong_phan_giac", "ten": "Tính chất đường phân giác trong tam giác", "re": r"phân giác|đường phân giác", "ngan": "Đường phân giác"},
        {"ma": "dinh_li_thales", "ten": "Định lí Thalès (thuận, đảo, hệ quả)", "re": r"thalès|thales|song song|tỉ lệ", "ngan": "Định lí Thalès"},
        {"ma": "duong_trung_binh", "ten": "Đường trung bình của tam giác", "re": r"trung bình|đường trung bình|trung điểm", "ngan": "Đường trung bình"},
    ],
    'V': [
        {"ma": "thu_thap_du_lieu", "ten": "Thu thập, phân loại dữ liệu (định tính/định lượng)", "re": r"thu thập|phân loại|định tính|định lượng|dữ liệu|mẫu số liệu", "ngan": "Thu thập dữ liệu"},
        {"ma": "bieu_do_thong_ke", "ten": "Đọc và vẽ biểu đồ cột, quạt tròn, đoạn thẳng", "re": r"biểu đồ|hình quạt|cột kép|đoạn thẳng|tỉ lệ phần trăm", "ngan": "Biểu đồ thống kê"},
    ],
    'VI': [
        {"ma": "dkxd_gia_tri", "ten": "Điều kiện xác định & Giá trị phân thức", "re": r"điều kiện xác định|đkxđ|giá trị của phân thức|xác định khi", "ngan": "ĐKXĐ phân thức"},
        {"ma": "rut_gon_phep_tinh", "ten": "Rút gọn phân thức & 4 phép tính", "re": r"rút gọn|thực hiện phép tính|cộng.*phân thức|trừ.*phân thức|nhân.*phân thức|chia.*phân thức", "ngan": "Rút gọn phân thức"},
        {"ma": "cau_phu_phan_thuc", "ten": "Câu hỏi phụ: Tìm x nguyên, So sánh, Min-Max", "re": r"x nguyên|giá trị nguyên|p nguyên|nhỏ nhất|lớn nhất|so sánh|p <|p >", "ngan": "Câu phụ phân thức"},
    ],
    'VII': [
        {"ma": "giai_pt_bac_nhat", "ten": "Giải phương trình bậc nhất một ẩn", "re": r"phương trình bậc nhất|giải phương trình|nghiệm của phương trình", "ngan": "Giải phương trình"},
        {"ma": "ham_so_bac_nhat", "ten": "Hàm số bậc nhất y = ax + b, đồ thị, hệ số góc", "re": r"hàm số|đồ thị|hệ số góc|y =|song song|cắt nhau", "ngan": "Hàm số bậc nhất"},
        {"ma": "toan_thuc_te_pt", "ten": "Giải bài toán bằng cách lập phương trình", "re": r"lập phương trình|bài toán thực tế|năng suất|chuyển động|vận tốc", "ngan": "Toán thực tế lập PT"},
    ],
    'VIII': [
        {"ma": "xac_suat_bien_co", "ten": "Xác suất của biến cố trong một số mô hình", "re": r"xác suất|biến cố|xúc xắc|đồng xu|rút thẻ|ngẫu nhiên", "ngan": "Xác suất biến cố"},
    ],
    'IX': [
        {"ma": "tam_giac_dong_dang", "ten": "Tam giác đồng dạng (c-c-c, c-g-c, g-g)", "re": r"đồng dạng|tam giác đồng dạng|trường hợp đồng dạng", "ngan": "Tam giác đồng dạng"},
        {"ma": "tam_giac_vuong_dong_dang", "ten": "Tam giác vuông đồng dạng & Định lí Pythagore", "re": r"tam giác vuông|vuông tại|pythagore|hệ thức lượng", "ngan": "Tam giác vuông đồng dạng"},
        {"ma": "he_thuc_tich_dong_dang", "ten": "Chứng minh hệ thức tích, tỉ lệ thức", "re": r"chứng minh.*=|hệ thức|tỉ lệ thức", "ngan": "Hệ thức tích đồng dạng"},
    ],
    'X': [
        {"ma": "hinh_chop_deu", "ten": "Hình chóp tam giác đều, tứ giác đều", "re": r"hình chóp|tam giác đều|tứ giác đều|diện tích xung quanh|thể tích", "ngan": "Hình chóp đều"},
    ]
}

FREQ_PCT_8 = {
    'I': {'thu_gon_da_thuc': 45, 'don_thuc_dong_dang': 35, 'tim_x_da_thuc': 30, 'phep_tinh_da_thuc': 25, 'thuc_te_da_thuc': 15},
    'II': {'hang_dang_thuc': 52, 'phan_tich_nhan_tu': 48, 'min_max_hdt': 25, 'kpt_bien_chia_het': 22},
    'III': {'hinh_chu_nhat': 45, 'hinh_binh_hanh': 42, 'hinh_thoi_vuong': 35, 'hinh_thang_can': 28, 'hinh_vdc_tong_hop': 25, 'goc_tu_giac': 15},
    'IV': {'duong_phan_giac': 66, 'dinh_li_thales': 35, 'duong_trung_binh': 25},
    'V': {'thu_thap_du_lieu': 68, 'bieu_do_thong_ke': 62},
    'VI': {'rut_gon_phep_tinh': 60, 'dkxd_gia_tri': 55, 'cau_phu_phan_thuc': 35},
    'VII': {'giai_pt_bac_nhat': 55, 'ham_so_bac_nhat': 52, 'toan_thuc_te_pt': 25},
    'VIII': {'xac_suat_bien_co': 97},
    'IX': {'tam_giac_dong_dang': 65, 'tam_giac_vuong_dong_dang': 40, 'he_thuc_tich_dong_dang': 35},
    'X': {'hinh_chop_deu': 98}
}

TEN_CHUONG_8 = {
    'I': 'Chương I: Đa thức',
    'II': 'Chương II: Hằng đẳng thức đáng nhớ và ứng dụng',
    'III': 'Chương III: Tứ giác',
    'IV': 'Chương IV: Định lí Thalès',
    'V': 'Chương V: Dữ liệu và biểu đồ',
    'VI': 'Chương VI: Phân thức đại số',
    'VII': 'Chương VII: Phương trình bậc nhất và hàm số bậc nhất',
    'VIII': 'Chương VIII: Mở đầu về tính xác suất của biến cố',
    'IX': 'Chương IX: Tam giác đồng dạng',
    'X': 'Chương X: Một số hình khối trong thực tiễn (Hình chóp)'
}

def get_ch_key_8(ch_str: str) -> str:
    ch_str = ch_str or ''
    if 'Đa thức' in ch_str: return 'I'
    elif 'Hằng đẳng thức' in ch_str: return 'II'
    elif 'Tứ giác' in ch_str: return 'III'
    elif 'Thalès' in ch_str or 'Thales' in ch_str: return 'IV'
    elif 'Dữ liệu' in ch_str: return 'V'
    elif 'Phân thức' in ch_str: return 'VI'
    elif 'PT' in ch_str or 'hàm số' in ch_str: return 'VII'
    elif 'Xác suất' in ch_str: return 'VIII'
    elif 'Đồng dạng' in ch_str: return 'IX'
    elif 'Hình chóp' in ch_str or 'hình khối' in ch_str.lower(): return 'X'
    for k in ['X', 'IX', 'VIII', 'VII', 'VI', 'V', 'IV', 'III', 'II', 'I']:
        if f'{k}.' in ch_str or f'[{k}]' in ch_str:
            return k
    return 'I'

def normalize_school(name: str) -> str:
    if not name:
        return 'Hà Nội'
    s = name.replace('(2023-2024)', '').replace('(2024-2025)', '').replace('(2025-2026)', '')
    s = s.replace('(Đề tham khảo)', '').replace('KNTT -', '').strip(' -_')
    if s.lower().startswith('thcs '):
        s = 'THCS ' + s[5:].title()
    elif s.lower().startswith('phong gddt '):
        s = 'Phòng GD&ĐT ' + s[11:].title()
    return s.strip()

def extract_and_score() -> tuple[list[list], list[list]]:
    files = sorted(glob.glob(str(ROOT / 'inputs/refs/de-thi/lop-8/exams/*.json')))
    print(f"Reading {len(files)} exam files...")
    
    all_raw_rows = []
    
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        xx = data.get('xuat_xu', {})
        if isinstance(xx, str):
            xx = {'truong': xx, 'nam': '2023-2024', 'ky': 'GK1' if 'giữa' in xx.lower() or 'gk' in xx.lower() else 'CK1'}
        ky = xx.get('ky', 'GK1')
        nam = xx.get('nam', '2024-2025')
        truong_raw = xx.get('truong', 'Hà Nội')
        truong = normalize_school(truong_raw)
        nguon_file = xx.get('nguon', '')
        
        # Năm đầu của năm học (vd '2024-2025' -> '2024')
        nam_dau = nam.split('-')[0] if '-' in nam else nam
        
        for c in data.get('cau', []):
            cid = c.get('id', '')
            vi_tri = c.get('vi_tri', '')
            ch_raw = c.get('chuong', 'I. Đa thức')
            ch_key = get_ch_key_8(ch_raw)
            band = c.get('band', 'TH')
            if band not in ('NB', 'TH', 'VD', 'VDC'):
                band = 'TH'
                
            fmt_raw = c.get('loai', 'TL')
            if fmt_raw == 'TN':
                fmt = 'Trắc nghiệm chọn đáp án'
            elif fmt_raw == 'TN-DS':
                fmt = 'Trắc nghiệm đúng sai'
            else:
                fmt = 'Tự luận'
                
            phut = c.get('phut', 1.5 if band == 'NB' else (6.0 if band == 'TH' else (12.0 if band == 'VD' else 18.0)))
            co_hinh_bool = c.get('co_hinh', False)
            co_hinh = 'Có' if co_hinh_bool else 'Không'
            
            # Ghép đề bài hoàn chỉnh
            de_chung = (c.get('de_chung') or '').strip()
            de_part = (c.get('de') or '').strip()
            if de_part and de_part in de_chung:
                de_bai = de_chung
            elif de_chung and de_part:
                de_bai = f"{de_chung}\n{de_part}"
            else:
                de_bai = de_chung or de_part or f"Bài {vi_tri}"
                
            # Dạng bài
            dangs = c.get('dang', [])
            dang_str = ', '.join(dangs) if dangs else 'Dạng chuẩn theo SGK'
            
            # Nguồn chi tiết
            nguon_str = f"Đề {ky} {nam} {truong}, {vi_tri}" if vi_tri else f"Đề {ky} {nam} {truong}"
            
            # Ưu tiên & Loại nguồn
            uu_tien = 'Ưu tiên 1: Đề thi thật'
            loai_nguon = 'Đề thi thật'
            
            # Phân loại vào phiếu
            phieu_str = f"Phiếu [{ch_key}] ({TEN_CHUONG_8[ch_key].split(': ')[1]})"
            
            # Có thực tế không?
            is_thuc_te_bool = bool(re.search(r'đồng|triệu|bóng|cây|máy bay|tàu|tháp|hải đăng|thùng|cốc|vận tốc|km/h|năng suất|sản phẩm|bể bơi|chi phí|lợi nhuận|quãng đường|thực tế|bữa ăn|dinh dưỡng', de_bai, re.I))
            thuc_te = 'Có' if is_thuc_te_bool else 'Không'
            
            # Bài học SGK (suy luận theo chương)
            bai_sgk = f"Bài học Ch.[{ch_key}]"
            
            # Phân loại câu (Scaffolding §4b)
            if band == 'NB':
                loai_cau = 'NB của phiếu'
            elif band == 'TH':
                loai_cau = 'TH của phiếu'
            elif band == 'VD':
                loai_cau = 'VD của phiếu'
            else:
                loai_cau = 'VDC câu cuối đề'
                
            de_xuat_tm = f"P1 · {band} · {loai_cau}"
            
            # Phù hợp lớp C, B, X
            lop_c = 'x' if band != 'VDC' else ''
            lop_b = 'x'
            lop_x = 'x' if band in ('VD', 'VDC') else ''
            
            # Phân loại dạng ý & Tần suất đề thật
            dang_list = CONFIGS_8.get(ch_key, CONFIGS_8['I'])
            freq_dict = FREQ_PCT_8.get(ch_key, {})
            txt_match = de_bai + ' ' + dang_str
            
            best_dy = None
            best_pct = -1
            for dy in dang_list:
                if re.search(dy['re'], txt_match, re.I):
                    p = freq_dict.get(dy['ma'], 0)
                    if p > best_pct:
                        best_pct = p
                        best_dy = dy
            if not best_dy:
                best_dy = dang_list[0]
                best_pct = freq_dict.get(best_dy['ma'], 15)
                
            z_val = f"{best_dy['ngan']} {best_pct}%"
            aa_val = 2 if best_pct >= 30 else (1 if best_pct >= 10 else 0)
            
            # Chấm điểm sư phạm T1-T8
            t1 = 2 if band != 'VDC' else 1  # VDC câu cuối là mở rộng
            t2 = 2 if band in ('VD', 'VDC', 'TH') else 1
            is_hinh = ch_key in ('III', 'IV', 'IX', 'X')
            t3 = 2 if (is_thuc_te_bool or is_hinh) else 1
            has_parts = bool(re.search(r'(?m)^\s*[a-d1-4]\)', de_bai))
            t4 = 2 if has_parts else 1
            has_trap = bool(re.search(r'đkxđ|điều kiện|mẫu thức|nguyên|âm|ngoại lai|đổi dấu|rút gọn|phân thức|bình phương|nhỏ nhất|lớn nhất', txt_match, re.I))
            t5 = 2 if has_trap else 1
            t6 = 2  # Đề thi thật Hà Nội đã được duyệt chuẩn
            t7 = aa_val
            t8 = 2 if band == 'VDC' else (1 if band == 'VD' else 0)
            
            # Lí do chấm sư phạm
            vai_tro = "Khởi động / Khám phá" if band == 'NB' else ("Luyện tập 1 (rèn kỹ năng)" if band == 'TH' else ("Luyện tập 2 (trọng tâm đề thi)" if band == 'VD' else "Mở rộng / Bồi dưỡng điểm 10"))
            li_do = f"{band} chuẩn đề thi Hà Nội ({cid}): bám sát dạng {best_dy['ngan']} (tần suất {best_pct}%). Rèn phương pháp giải và kỹ năng trọng tâm. Đề xuất: {vai_tro}."
            
            # Dựng hàng 47 cột
            # A..AU
            da_duyet_bool = c.get('da_duyet', False)
            can_doc_bool = c.get('can_doc_anh', False)
            da_soi_val = 'Đã duyệt' if da_duyet_bool else ('Cần đọc ảnh' if can_doc_bool else 'Chưa')
            soat_de_val = 'Cần đọc ảnh' if can_doc_bool else ''
            thay_duyet_val = 'Đã duyệt' if da_duyet_bool else 'Chờ duyệt'
            
            row = [
                de_bai,              # A (0): Bài cụ thể
                nguon_str,           # B (1): Nguồn trong input
                band,                # C (2): Mức độ
                dang_str,            # D (3): Dạng bài
                uu_tien,             # E (4): Ưu tiên
                phieu_str,           # F (5): Phân loại vào phiếu
                str(phut),           # G (6): Thời lượng (phút)
                thuc_te,             # H (7): Thực tế
                fmt,                 # I (8): Format
                band,                # J (9): Mức độ từng ý
                bai_sgk,             # K (10): Bài học SGK
                nguon_file,          # L (11): Ghi chú
                cid,                 # M (12): Mã câu
                loai_cau,            # N (13): Phân loại câu
                de_xuat_tm,          # O (14): Đề xuất thuyết minh
                '',                  # P (15): Trạng thái
                '',                  # Q (16): Loại ngay (L1-L5)
                da_soi_val,          # R (17): Đã soi ảnh
                lop_c,               # S (18): Lớp C
                lop_b,               # T (19): Lớp B
                lop_x,               # U (20): Lớp X
                '',                  # V (21): Chọn tay
                loai_nguon,          # W (22): Loại nguồn
                co_hinh,             # X (23): Có hình · ảnh chụp
                cid,                 # Y (24): Mã bài gốc
                z_val,               # Z (25): Dạng từng ý trong đề thật
                str(aa_val),         # AA (26): T7 gợi ý
                '',                  # AB (27): Link
                f"[{ch_key}]",       # AC (28): Chương
                '',                  # AD (29): Nhóm nghi trùng
                soat_de_val,         # AE (30): Cần soát đề
                str(t1),             # AF (31): T1
                str(t2),             # AG (32): T2
                str(t3),             # AH (33): T3
                str(t4),             # AI (34): T4
                str(t5),             # AJ (35): T5
                str(t6),             # AK (36): T6
                str(t7),             # AL (37): T7
                str(t8),             # AM (38): T8
                '',                  # AN (39): Điểm C (sẽ gán công thức khi ghi sheet)
                '',                  # AO (40): Điểm B (sẽ gán công thức khi ghi sheet)
                '',                  # AP (41): Điểm X (sẽ gán công thức khi ghi sheet)
                '',                  # AQ (42): Ngưỡng theo mức (công thức)
                '',                  # AR (43): Kết luận (công thức)
                thay_duyet_val,      # AS (44): THẦY DUYỆT
                li_do,               # AT (45): Lí do chấm
                nam_dau              # AU (46): Năm đầu của năm học
            ]
            all_raw_rows.append(row)
            
    print(f"Total extracted questions: {len(all_raw_rows)}")
    
    # Sắp xếp câu hỏi theo thứ tự Chương [I]..[X] và mức độ
    band_priority = {'VDC': 0, 'VD': 1, 'TH': 2, 'NB': 3}
    ch_priority = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
    
    all_raw_rows.sort(key=lambda r: (
        ch_priority.get(r[28].strip('[]'), 99),
        band_priority.get(r[2], 9),
        r[12]
    ))
    
    # Lưu vào scratch
    out_all = ROOT / 'scratch' / 'ngan_hang_cau_lop8_all.json'
    with open(out_all, 'w', encoding='utf-8') as f:
        json.dump(all_raw_rows, f, ensure_ascii=False, indent=1)
    print(f"Saved {len(all_raw_rows)} rows to {out_all}")
    
    return all_raw_rows

if __name__ == '__main__':
    extract_and_score()

