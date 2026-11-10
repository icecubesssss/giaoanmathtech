#!/usr/bin/env python3
"""TÁCH NGÂN HÀNG CÂU LỚP 9 THÀNH 3 TAB RIÊNG: ĐỀ THI, SGK, SÁCH THAM KHẢO.

Theo yêu cầu của Thầy:
- Tab 1: 'Đề thi' (2.189 câu)
- Tab 2: 'SGK' (807 câu)
- Tab 3: 'Sách tham khảo' (2.569 câu)
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
SPREADSHEET_ID = '1OuzuBOhfWQu5RQJ7BxRRpP98bs6aOin2xvN0udz8yqg'
CACHE_FILE = ROOT / 'scratch' / 'ngan_hang_cau_scored_all.json'

def make_formulas(row_num: int, offset: int = 0) -> tuple[str, str, str, str, str]:
    if offset == 1:
        ao = f'=IF(COUNT($AG{row_num}:$AN{row_num})<8,"",ROUND(SUMPRODUCT($AG{row_num}:$AN{row_num},$AG$2:$AN$2)/(2*SUM($AG$2:$AN$2))*10,1))'
        ap = f'=IF(COUNT($AG{row_num}:$AN{row_num})<8,"",ROUND(SUMPRODUCT($AG{row_num}:$AN{row_num},$AG$3:$AN$3)/(2*SUM($AG$3:$AN$3))*10,1))'
        aq = f'=IF(COUNT($AG{row_num}:$AN{row_num})<8,"",ROUND(SUMPRODUCT($AG{row_num}:$AN{row_num},$AG$4:$AN$4)/(2*SUM($AG$4:$AN$4))*10,1))'
        ar = f'=IF($C{row_num}="TH",$AS$3,IF($C{row_num}="NB",$AS$4,$AS$2))'
        as_ = f'=IF($R{row_num}<>"","Loại ("&$R{row_num}&")",IF($AO{row_num}="","Chưa chấm",IF($AO{row_num}>=$AR{row_num},"Đưa vào bài",IF($AO{row_num}>=5,"Dự phòng / sửa","Loại hoặc sửa"))))'
        return ao, ap, aq, ar, as_
    else:
        an = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$2:$AM$2)/(2*SUM($AF$2:$AM$2))*10,1))'
        ao = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$3:$AM$3)/(2*SUM($AF$3:$AM$3))*10,1))'
        ap = f'=IF(COUNT($AF{row_num}:$AM{row_num})<8,"",ROUND(SUMPRODUCT($AF{row_num}:$AM{row_num},$AF$4:$AM$4)/(2*SUM($AF$4:$AM$4))*10,1))'
        aq = f'=IF($C{row_num}="TH",$AR$3,IF($C{row_num}="NB",$AR$4,$AR$2))'
        ar = f'=IF($Q{row_num}<>"","Loại ("&$Q{row_num}&")",IF($AN{row_num}="","Chưa chấm",IF($AN{row_num}>=$AQ{row_num},"Đưa vào bài",IF($AN{row_num}>=5,"Dự phòng / sửa","Loại hoặc sửa"))))'
        return an, ao, ap, aq, ar

def build_tab_data(rows: list, tab_title: str) -> list[list]:
    offset = 1 if rows and len(rows[0]) >= 47 else 0
    total_cols = 48 if offset else 47
    formula_start = 40 if offset else 39
    
    out = []
    for idx, r in enumerate(rows):
        row_num = idx + 6
        f1, f2, f3, f4, f5 = make_formulas(row_num, offset)
        
        row = []
        for i in range(total_cols):
            if i == formula_start:
                row.append(f1)
            elif i == formula_start + 1:
                row.append(f2)
            elif i == formula_start + 2:
                row.append(f3)
            elif i == formula_start + 3:
                row.append(f4)
            elif i == formula_start + 4:
                row.append(f5)
            else:
                val = r[i] if i < len(r) else ''
                row.append(val)
        out.append(row)
    return out

def populate_sheet(tab_name: str, title_note: str, raw_rows: list, header_template: list[list]) -> bool:
    print(f"\n==================== POPULATING TAB '{tab_name}' ({len(raw_rows)} rows) ====================")
    offset = 1 if raw_rows and len(raw_rows[0]) >= 47 else 0
    total_cols = 48 if offset else 47
    max_col_letter = "AV" if offset else "AU"
    
    # 1. Header rows 1-5
    padded_header = []
    for idx, r in enumerate(header_template):
        row = list(r)
        while len(row) < total_cols:
            row.append('')
        if idx == 0:
            row[0] = title_note
        padded_header.append(row)
        
    op_header = [{"op": "write", "range": f"'{tab_name}'!A1:{max_col_letter}5", "data": padded_header}]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(op_header, f)
        tmp_h = f.name
    res = subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp_h], capture_output=True, text=True)
    os.remove(tmp_h)
    if res.returncode != 0:
        print(f"Error writing header for {tab_name}: {res.stderr}")
        return False
    print(f"Header rows 1-5 written to '{tab_name}'.")
    
    # 2. Data rows
    tab_data = build_tab_data(raw_rows, tab_name)
    CHUNK_SIZE = 150
    total_chunks = (len(tab_data) + CHUNK_SIZE - 1) // CHUNK_SIZE
    
    print(f"Writing {len(tab_data)} rows in {total_chunks} chunks...")
    for c_idx in range(total_chunks):
        start_idx = c_idx * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, len(tab_data))
        
        start_row = start_idx + 6
        end_row = end_idx + 5
        
        chunk = tab_data[start_idx:end_idx]
        rng = f"'{tab_name}'!A{start_row}:{max_col_letter}{end_row}"
        op = [{"op": "write", "range": rng, "data": chunk}]
        
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(op, f)
            tmp_p = f.name
            
        print(f"  [{c_idx+1}/{total_chunks}] Writing rows {start_row}..{end_row} ({len(chunk)} rows)...", end=" ")
        sys.stdout.flush()
        
        res = subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp_p], capture_output=True, text=True)
        os.remove(tmp_p)
        
        if res.returncode != 0:
            print(f"FAILED!\nError: {res.stderr}")
            return False
        else:
            print("OK")
        time.sleep(0.4)
        
    print(f"Successfully populated '{tab_name}' with {len(tab_data)} rows!")
    return True

def main() -> int:
    print(f"Loading data from {CACHE_FILE}...")
    data = json.load(open(CACHE_FILE, 'r', encoding='utf-8'))
    print(f"Loaded {len(data)} rows.")
    
    offset = 1 if data and len(data[0]) >= 47 else 0
    max_h_col = "AV" if offset else "AU"
    src_header_tab = 'Đề thi' if offset else 'Ngân hàng câu'
    
    # Fetch exact header template
    res = subprocess.run(['gsheets', 'readonly', 'read', SPREADSHEET_ID, f"'{src_header_tab}'!A1:{max_h_col}5", '--json'], capture_output=True, text=True)
    header_template = json.loads(res.stdout)
    
    # Split rows
    de_thi_rows = []
    sgk_rows = []
    stk_rows = []
    
    for r in data:
        w = r[22 + offset] if len(r) > (22 + offset) else ''
        ma = r[12] if len(r) > 12 else ''
        if w in ('Đề thi', 'Đề thi trên trường', 'Đề vào 6, vào 10') or any(ma.startswith(p) for p in ('gk1', 'ck1', 'gk2', 'ck2', 'v10')):
            de_thi_rows.append(r)
        elif w in ('SGK', 'SBT') or any(p in ma for p in ('sgk', 'sbt', 'sgv')):
            sgk_rows.append(r)
        elif w == 'Sách tham khảo':
            stk_rows.append(r)
        else:
            stk_rows.append(r)
            
    print(f"\nSplit summary:")
    print(f"  * Đề thi          : {len(de_thi_rows)} rows")
    print(f"  * SGK             : {len(sgk_rows)} rows")
    print(f"  * Sách tham khảo  : {len(stk_rows)} rows")
    print(f"  * Total           : {len(de_thi_rows) + len(sgk_rows) + len(stk_rows)} rows")
    
    # 1. Populate Đề thi
    ok = populate_sheet(
        'Đề thi',
        'NGÂN HÀNG CÂU — ĐỀ THI LỚP 9: toàn bộ các câu từ đề thi chính thức của Sở, đề thi thử và đề kiểm tra trường (2.189 câu)',
        de_thi_rows,
        header_template
    )
    if not ok:
        return 1
        
    # 2. Populate SGK
    ok = populate_sheet(
        'SGK',
        'NGÂN HÀNG CÂU — SGK & SBT LỚP 9: toàn bộ các câu chuẩn theo chương trình GDPT 2018 (807 câu)',
        sgk_rows,
        header_template
    )
    if not ok:
        return 1
        
    # 3. Populate Sách tham khảo
    ok = populate_sheet(
        'Sách tham khảo',
        'NGÂN HÀNG CÂU — SÁCH THAM KHẢO LỚP 9: toàn bộ các câu từ sách tham khảo, tài liệu chuyên đề và bài tập mở rộng (2.569 câu)',
        stk_rows,
        header_template
    )
    if not ok:
        return 1
        
    print("\nALL 3 TABS ('Đề thi', 'SGK', 'Sách tham khảo') HAVE BEEN POPULATED SUCCESSFULLY!")
    return 0

if __name__ == '__main__':
    sys.exit(main())

