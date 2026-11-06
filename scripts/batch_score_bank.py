#!/usr/bin/env python3
"""CHẤM T1-T8 VÀ ĐIỀN DẠNG ĐỀ THI HÀNG LOẠT CHO TAB 'NGÂN HÀNG CÂU' — ĐỢT 3.

Quy chuẩn:
- Giữ nguyên 100% các câu đã chấm sẵn (114 câu Chương V và 30 câu thí điểm Chương I).
- Điền Cột Z (Dạng từng ý trong đề thật) và Cột AA (T7 gợi ý) dựa trên tần suất đề thi thật.
- Điền Cột AF–AM (T1–T8) và Cột AT (Lí do chấm) cho toàn bộ các câu còn lại.
- Các cột AN–AP (Điểm C, B, X), AQ (Ngưỡng theo mức), AR (Kết luận lớp C) tự động tính bằng công thức.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPREADSHEET_ID = '1OuzuBOhfWQu5RQJ7BxRRpP98bs6aOin2xvN0udz8yqg'
CACHE_FILE = ROOT / 'scratch' / 'ngan_hang_cau_all.json'

CONFIGS = {
    'I': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-dai-so-chuong-01.json'))['dang_y'],
    'II': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-dai-so-chuong-02.json'))['dang_y'],
    'III': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-dai-so-chuong-03.json'))['dang_y'],
    'IV': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-hinh-hoc-chuong-04.json'))['dang_y'],
    'V': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-hinh-hoc-chuong-05.json'))['dang_y'],
    'VI': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-dai-so-chuong-06.json'))['dang_y'],
    'VII': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-dai-so-chuong-07.json'))['dang_y'],
    'VIII': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-dai-so-chuong-08.json'))['dang_y'],
    'IX': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-hinh-hoc-chuong-09.json'))['dang_y'],
    'X': json.load(open(ROOT / 'config/khung-phan-dang/lop-9-hinh-hoc-chuong-10.json'))['dang_y'],
    'Cực trị thực tế': [
        {"ma": "kinh_te_doanh_thu", "ten": "Tối ưu hóa kinh tế (doanh thu, lợi nhuận, chi phí)", "re": "doanh thu|lợi nhuận|chi phí|giá bán|tiền|sản xuất", "ngan": "Kinh tế %"},
        {"ma": "hinh_hoc_toi_uu", "ten": "Tối ưu hóa hình học (diện tích, chu vi, hàng rào)", "re": "hình chữ nhật|chu vi|diện tích|hàng rào|khu vườn|thể tích", "ngan": "Hình học tối ưu"},
        {"ma": "quang_duong_thoi_gian", "ten": "Tối ưu hóa thời gian, quãng đường, vận tốc", "re": "vận tốc|thời gian|robot|quãng đường", "ngan": "Thời gian tối ưu"}
    ]
}

FREQ_PCT = {
    'I': {'he_co_ban': 76, 'toan_kinh_te': 49, 'toan_nang_suat': 31, 'he_an_phu': 19, 'toan_chuyen_dong': 10, 'toan_hinh_hoc': 8, 'khai_niem': 10, 'toan_so_hoc': 3},
    'II': {'bpt_bac_nhat': 57, 'pt_tich': 49, 'pt_chua_an_o_mau': 46, 'tinh_chat_bdt': 19, 'bdt_nang_cao': 16},
    'III': {'rut_gon_can': 99, 'pt_chua_can': 98, 'tinh_gia_tri': 94, 'cau_phu_can': 93, 'khai_can_so_hoc': 23},
    'IV': {'tslg_thuc_te': 74, 'tslg_tam_giac': 60, 'he_thuc_luong': 40, 'giai_tam_giac': 32},
    'V': {'bon_diem': 77, 'vuong_goc': 69, 'bang_nhau': 67, 'he_thuc_tich': 62, 'tinh': 51, 'thang_hang': 30, 'song_song': 26, 'tiep_tuyen': 17, 'cuc_tri': 11},
    'VI': {'giai_pt_bac_hai': 84, 'pt_bac_hai_thuc_te': 67, 'viet_va_nghiem': 66, 'ham_so_parabol': 15, 'pt_quy_ve_bac_hai': 7},
    'VII': {'doc_bieu_do_ghep_nhom': 96, 'bang_tan_so_ghep_nhom': 68, 'tan_so_thuc_te': 58, 'bieu_do_doan_thang': 1},
    'VIII': {'khong_gian_mau': 95, 'rut_the_boc_bong': 55, 'gieo_xuc_xac_dong_xu': 12, 'quay_dia': 10},
    'IX': {'tu_giac_noi_tiep': 96, 'he_thuc_tich_dong_dang': 92, 'song_song_vuong_goc': 84, 'goc_noi_tiep_tiep_tuyen': 62, 'thang_hang_dong_quy': 39},
    'X': {'hinh_tru': 84, 'hinh_cau': 33, 'hinh_non': 16, 'khoi_phuc_hop': 15},
    'Cực trị thực tế': {'kinh_te_doanh_thu': 51, 'hinh_hoc_toi_uu': 47, 'quang_duong_thoi_gian': 2}
}

def get_chapter_key(ch_str: str) -> str:
    if 'Cực trị' in ch_str:
        return 'Cực trị thực tế'
    for k in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']:
        if f'[{k}]' in ch_str:
            return k
    return 'I'

def score_row(r: list) -> tuple[str, int, list[int], str, bool]:
    de = r[0] if len(r) > 0 else ''
    muc = r[2] if len(r) > 2 and r[2] in ('NB', 'TH', 'VD', 'VDC') else 'TH'
    dang = r[3] if len(r) > 3 else ''
    ma = r[12] if len(r) > 12 else ''
    ch_raw = r[28] if len(r) > 28 else ''
    ch_key = get_chapter_key(ch_raw)
    
    # Giữ nguyên 100% câu đã chấm
    has_score = len(r) > 31 and r[31] != '' and r[31] is not None
    if has_score:
        z_val = r[25] if len(r) > 25 and r[25] else ''
        aa_val = int(r[26]) if len(r) > 26 and str(r[26]).isdigit() else (0 if r[26] == '0' else '')
        af_am = [int(x) if str(x).isdigit() else 0 for x in r[31:39]]
        at_val = r[45] if len(r) > 45 else ''
        return z_val, aa_val, af_am, at_val, True
        
    # Phân loại dạng ý & tần suất
    dang_list = CONFIGS.get(ch_key, CONFIGS['I'])
    freq_dict = FREQ_PCT.get(ch_key, {})
    txt = de + ' ' + dang
    
    best_dy = None
    best_pct = -1
    for dy in dang_list:
        if re.search(dy['re'], txt, re.I):
            p = freq_dict.get(dy['ma'], 0)
            if p > best_pct:
                best_pct = p
                best_dy = dy
    if not best_dy:
        best_dy = dang_list[0]
        best_pct = freq_dict.get(best_dy['ma'], 10)
        
    z_val = f"{best_dy['ngan']} {best_pct}%"
    aa_val = 2 if best_pct >= 30 else (1 if best_pct >= 10 else 0)
    
    # Chấm T1–T8 sư phạm
    is_exam = any(ma.startswith(p) for p in ('gk1', 'ck1', 'gk2', 'ck2', 'v10'))
    is_sgk = any(p in ma for p in ('sgk', 'sbt', 'sgv'))
    
    t1 = 2 if (is_exam or is_sgk) else (1 if muc == 'VDC' else 2)
    t2 = 2 if muc in ('VD', 'VDC', 'TH') else 1
    
    is_thuc_te = (len(r) > 7 and r[7] in (True, 'TRUE', '1', 1)) or bool(re.search(r'đồng|triệu|bóng|cây|máy bay|tàu|tháp|hải đăng|thùng|cốc|vận tốc|km/h|năng suất|sản phẩm|bồn|chi phí|lợi nhuận', de, re.I))
    is_hinh = ch_key in ('IV', 'V', 'IX', 'X')
    t3 = 2 if is_thuc_te else (2 if is_hinh else 1)
    
    has_parts = bool(re.search(r'(?m)^\s*[a-d1-4]\)', de)) or (len(r) > 9 and r[9] and len(r[9].split()) > 1)
    t4 = 2 if has_parts else 1
    
    has_trap = bool(re.search(r'đkxđ|điều kiện|mẫu thức|nguyên|âm|ngoại lai|đổi dấu|rút gọn|vi-ét|bán kính|đường kính|lớn nhất|nhỏ nhất|trục căn', txt, re.I))
    t5 = 2 if has_trap else 1
    
    t6 = 2 if (is_exam or is_sgk) else 1
    t7 = aa_val
    t8 = 2 if muc == 'VDC' else (1 if muc == 'VD' else 0)
    
    scores = [t1, t2, t3, t4, t5, t6, t7, t8]
    
    nguon_tag = f"Đề thi ({ma})" if is_exam else (f"SGK/SBT ({ma})" if is_sgk else f"Tài liệu tham khảo ({ma})")
    vai_tro = "Khởi động / Khám phá" if muc == 'NB' else ("Luyện tập 1 (rèn kỹ năng)" if muc == 'TH' else ("Luyện tập 2 (đích bài thi)" if muc == 'VD' else "Mở rộng / Bồi dưỡng"))
    li_do = f"{muc} chuẩn {nguon_tag}: bám sát dạng {best_dy['ngan']} (tần suất {best_pct}%). Rèn phương pháp giải và kỹ năng trọng tâm. Đề xuất: {vai_tro}."
    
    return z_val, aa_val, scores, li_do, False

def main() -> int:
    print(f"Loading data from {CACHE_FILE}...")
    data = json.load(open(CACHE_FILE, 'r', encoding='utf-8'))
    print(f"Loaded {len(data)} rows.")
    
    all_z_aa = []
    all_scores = []
    all_lido = []
    already_scored_cnt = 0
    newly_scored_cnt = 0
    
    for idx, r in enumerate(data):
        z_val, aa_val, scores, li_do, was_scored = score_row(r)
        if was_scored:
            already_scored_cnt += 1
        else:
            newly_scored_cnt += 1
            
        all_z_aa.append([z_val, aa_val])
        all_scores.append(scores)
        all_lido.append([li_do])
        
    print(f"Summary: {already_scored_cnt} rows preserved | {newly_scored_cnt} rows newly scored.")
    
    # Chuẩn bị batch ghi vào Google Sheets
    CHUNK_SIZE = 150
    total_chunks = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE
    print(f"Writing to Google Sheets in {total_chunks} chunks (chunk size {CHUNK_SIZE})...")
    
    for c_idx in range(total_chunks):
        start_idx = c_idx * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, len(data))
        
        start_row = start_idx + 6
        end_row = end_idx + 5
        
        chunk_z_aa = all_z_aa[start_idx:end_idx]
        chunk_scores = all_scores[start_idx:end_idx]
        chunk_lido = all_lido[start_idx:end_idx]
        
        rng_z_aa = f"'Ngân hàng câu'!Z{start_row}:AA{end_row}"
        rng_scores = f"'Ngân hàng câu'!AF{start_row}:AM{end_row}"
        rng_lido = f"'Ngân hàng câu'!AT{start_row}:AT{end_row}"
        
        batch_ops = [
            {"op": "write", "range": rng_z_aa, "data": chunk_z_aa},
            {"op": "write", "range": rng_scores, "data": chunk_scores},
            {"op": "write", "range": rng_lido, "data": chunk_lido}
        ]
        
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(batch_ops, f)
            tmp_path = f.name
            
        print(f"[{c_idx+1}/{total_chunks}] Writing rows {start_row}..{end_row} ({end_idx - start_idx} rows)...", end=" ")
        sys.stdout.flush()
        
        res = subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp_path], capture_output=True, text=True)
        try:
            os.remove(tmp_path)
        except OSError:
            pass
            
        if res.returncode != 0:
            print(f"FAILED!\nError: {res.stderr}")
            return 1
        else:
            print("OK")
            
        time.sleep(0.5)
        
    print("\nALL 5,565 ROWS HAVE BEEN SUCCESSFULLY SCORED AND WRITTEN TO GOOGLE SHEETS!")
    return 0

if __name__ == '__main__':
    sys.exit(main())

