#!/usr/bin/env python3
"""CẬP NHẬT CỘT GIÀN GIÁO (SCAFFOLD), SỬA LỖI PHÂN LOẠI CÂU VÀ ĐỒNG BỘ MỨC ĐỘ / THỜI LƯỢNG.

Nhiệm vụ:
1. Thêm cột 'Chi tiết tách ý giàn giáo (Scaffold)' tại Cột P (index 15) cho tab 'Đề thi' và 'Phân dạng Ch.V lớp 9C'.
2. Sửa dứt điểm lỗi gán nhãn sai ở Cột N ('Phân loại câu'):
   - Các câu TH bị gán 'NB tách TH' -> 'TH của phiếu'.
   - Các câu VD/VDC bị gán 'NB tách TH' -> 'VD lẻ'.
3. Điền mẫu giàn giáo scaffold cho các câu VD Chương V theo định dạng chuẩn:
   a) [TH · ★★] ... · b) [TH · ★★] ... · c) [TH · ★★] ...
4. Cập nhật đồng bộ Cột J ('Mức độ từng ý') thành 'a) TH · b) TH · c) TH' và Cột G ('Thời lượng') thành 18 phút (6 phút/ý).
5. Cập nhật cache JSON scratch/ngan_hang_cau_scored_all.json và tương thích scripts.
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

SCAFFOLD_SAMPLES = {
    # Mẫu Thầy yêu cầu: tiếp tuyến tam giác cân -> trung trực -> c.c.c -> tiếp tuyến
    'ck1-tan-trieu-42': {
        'scaffold': 'a) [TH · ★★] CM OD là trung trực của MB · b) [TH · ★★] CM △ODM = △ODB · c) [TH · ★★] CM DB là tiếp tuyến của (O) tại B',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-cum-14-2025-4.2': {
        'scaffold': 'a) [TH · ★★] CM OD là trung trực của MB · b) [TH · ★★] CM △ODM = △ODB · c) [TH · ★★] CM DB là tiếp tuyến của (O) tại B',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'v10-dong-da-de04-IV2': {
        'scaffold': 'a) [TH · ★★] CM OD là trung trực của MB · b) [TH · ★★] CM △ODM = △ODB · c) [TH · ★★] CM DB là tiếp tuyến của (O) tại B',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-dich-vong-42': {
        'scaffold': 'a) [TH · ★★] CM OD là trung trực của MB · b) [TH · ★★] CM △ODM = △ODB · c) [TH · ★★] CM DB là tiếp tuyến của (O) tại B',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-ngoc-thuy-III2': {
        'scaffold': 'a) [TH · ★★] CM OD là trung trực của MB · b) [TH · ★★] CM △ODM = △ODB · c) [TH · ★★] CM DB là tiếp tuyến của (O) tại B',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-hai-ba-trung-2024-IV3': {
        'scaffold': 'a) [TH · ★★] CM OD là trung trực của MB · b) [TH · ★★] CM △ODM = △ODB · c) [TH · ★★] CM DB là tiếp tuyến của (O) tại B',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    # Đề Ái Mộ (đích P2)
    'ck1-ai-mo-2': {
        'scaffold': 'a) [TH · ★★] CM OF là trung trực của CD · b) [TH · ★★] CM △OCF = △ODF · c) [TH · ★★] CM DF là tiếp tuyến của (O) tại D',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    # Đề Phúc Đồng (đích P3)
    'ck1-phuc-dong-IV2': {
        'scaffold': 'a) [TH · ★★] CM OA là trung trực của BC suy ra OA ⊥ BC tại H · b) [TH · ★★] CM △BCD vuông tại C suy ra CD ⊥ BC · c) [TH · ★★] Từ quan hệ vuông góc đến song song suy ra OA ∥ CD',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-ba-dinh-2024-IV2': {
        'scaffold': 'a) [TH · ★★] CM OC là trung trực của AD suy ra OC ⊥ AD · b) [TH · ★★] CM △ABD vuông tại D suy ra BD ⊥ AD · c) [TH · ★★] Từ quan hệ vuông góc đến song song suy ra OC ∥ BD',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-dong-da-2025-IV2': {
        'scaffold': 'a) [TH · ★★] CM OA là trung trực của BC suy ra OA ⊥ BC tại H · b) [TH · ★★] CM CD ⊥ BC do tam giác BCD nội tiếp nửa đường tròn · c) [TH · ★★] Suy ra OA ∥ CD',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-nguyen-binh-khiem-2025-4.2': {
        'scaffold': 'a) [TH · ★★] CM OD là tia phân giác góc BOC · b) [TH · ★★] CM △OAB cân tại O suy ra phân giác OD là đường cao · c) [TH · ★★] Kết luận OD ⊥ AB',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-lomonoxop-2024-IV2': {
        'scaffold': 'a) [TH · ★★] CM OA là trung trực của BC suy ra OA ⊥ BC · b) [TH · ★★] CM BD ⊥ BC do góc nội tiếp chắn nửa đường tròn · c) [TH · ★★] Suy ra OA ∥ BD',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-cau-dien-42': {
        'scaffold': 'a) [TH · ★★] CM OC ⊥ AD do tính chất hai tiếp tuyến cắt nhau · b) [TH · ★★] CM MB ⊥ AD do góc MAD chắn nửa đường tròn · c) [TH · ★★] Suy ra OC ∥ MB',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-xuan-la-2024-4.2': {
        'scaffold': 'a) [TH · ★★] CM AM = AN do tính chất hai tiếp tuyến cắt nhau · b) [TH · ★★] CM OM = ON = R suy ra OA là đường trung trực của MN · c) [TH · ★★] Kết luận OA ⊥ MN',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    # Đề phường Ba Đình (đích P4)
    'ck1-phuong-ba-dinh-2025-IV2': {
        'scaffold': 'a) [TH · ★★] CM MO là trung trực của AB suy ra MO ⊥ AB tại H · b) [TH · ★★] CM △OAH đồng dạng △OMA (g-g) · c) [TH · ★★] Suy ra OH · OM = OA² = R²',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-ngo-gia-tu-2025-IV2': {
        'scaffold': 'a) [TH · ★★] CM OA là trung trực của BC suy ra OA ⊥ BC tại H · b) [TH · ★★] CM △OBH đồng dạng △OAB (g-g) · c) [TH · ★★] Suy ra OH · OA = OB² = R²',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-gia-lam-2024-4.2': {
        'scaffold': 'a) [TH · ★★] CM MO là trung trực của AB suy ra MO ⊥ AB tại H · b) [TH · ★★] CM △OAH đồng dạng △OMA (g-g) · c) [TH · ★★] Suy ra OH · OM = OA² = R²',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'v10-dong-da-de03-IV2': {
        'scaffold': 'a) [TH · ★★] CM OM ⊥ AB tại I do OM là trung trực của AB · b) [TH · ★★] CM △OAI đồng dạng △OMA (g-g) · c) [TH · ★★] Suy ra OI · OM = OA² = R²',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'gk1-nghia-tan-2025-IV': {
        'scaffold': 'a) [TH · ★★] CM △BHD vuông tại D và △BAE vuông tại E · b) [TH · ★★] CM △BHD đồng dạng △BAE (g-g) có góc B chung · c) [TH · ★★] Suy ra BH/BA = BD/BE nên BE · BA = BH · BD',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    # Đề Quốc Oai (P5)
    'ck1-quoc-oai-2024-4.2': {
        'scaffold': 'a) [TH · ★★] CM tia OC, OD là phân giác và góc COD = 90° · b) [TH · ★★] CM △COD vuông tại O có đường cao OM · c) [TH · ★★] CM MC · MD = OM² = R²',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-giang-bien-2025-de01-4.2': {
        'scaffold': 'a) [TH · ★★] CM OA là trung trực của BC suy ra OA ⊥ BC tại H · b) [TH · ★★] CM △OBH đồng dạng △OAB (g-g) · c) [TH · ★★] Suy ra OH · OA = OB² = R²',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    # Đề Nguyễn Trường Tộ (đích P6)
    'ck1-nguyen-truong-to-2025-IV': {
        'scaffold': 'a) [TH · ★★] CM OA là trung trực của BC suy ra OA ⊥ BC tại H · b) [TH · ★★] CM △OBH đồng dạng △OAB (g-g) · c) [TH · ★★] Suy ra OA · OH = OB² = R²',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-ban-mai-2024-3': {
        'scaffold': 'a) [TH · ★★] CM OM ⊥ AB tại I · b) [TH · ★★] CM △OAI đồng dạng △OMA (g-g) suy ra OI · OM = OA² = R² · c) [TH · ★★] CM OAHB có 4 cạnh bằng nhau suy ra là hình thoi',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-ngo-si-lien-2024-7': {
        'scaffold': 'a) [TH · ★★] CM OM là trung trực của AB suy ra H là trung điểm AB và OM ⊥ AB · b) [TH · ★★] CM △ABD vuông tại A suy ra AD ⊥ AB · c) [TH · ★★] CM △AMH đồng dạng △ABD (g-g) suy ra AM · AD = AB · R',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-ngo-si-lien-2025-5': {
        'scaffold': 'a) [TH · ★★] CM 4 điểm M, B, O, A cùng thuộc một đường tròn · b) [TH · ★★] CM H là trung điểm AB và OM ⊥ AB · c) [TH · ★★] CM △AMH đồng dạng △ABD (g-g) suy ra AM · AD = AB · R',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'gk1-thanh-quan-2024-IV': {
        'scaffold': 'a) [TH · ★★] CM 4 điểm B, C, D, E cùng thuộc đường tròn đường kính BC · b) [TH · ★★] CM △ABD đồng dạng △ACE (g-g) có góc A chung · c) [TH · ★★] Suy ra AB/AC = AD/AE nên AB · AE = AC · AD',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-hoai-duc-2024-4.2': {
        'scaffold': 'a) [TH · ★★] CM △ABD vuông tại D và △ACE vuông tại E · b) [TH · ★★] CM △ABD đồng dạng △ACE (g-g) có góc A chung · c) [TH · ★★] Suy ra AE · AB = AD · AC',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-hat-mon-2025-IV2': {
        'scaffold': 'a) [TH · ★★] CM 4 điểm A, C, H, O cùng thuộc một đường tròn · b) [TH · ★★] CM CD là tiếp tuyến của (O) · c) [TH · ★★] CM △ACD đồng dạng △CBD',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-duc-giang-2025-IV2': {
        'scaffold': 'a) [TH · ★★] CM 4 điểm A, B, C, D cùng thuộc một đường tròn · b) [TH · ★★] CM tiếp tuyến song song · c) [TH · ★★] CM hệ thức tích qua tam giác đồng dạng',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    'ck1-nguyen-du-2025-4.2': {
        'scaffold': 'a) [TH · ★★] CM 4 điểm cùng thuộc đường tròn · b) [TH · ★★] CM đường trung trực suy ra vuông góc · c) [TH · ★★] CM hệ thức tích qua tam giác đồng dạng',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    },
    # Mẫu Đại số (dòng 10 Đề thi)
    'gk1-ai-mo-2025-b2': {
        'scaffold': 'a) [TH · ★★] Giải HPT bằng phương pháp cộng đại số · b) [TH · ★★] Đặt ẩn phụ u = 1/(x-1), v = 1/(y+2) · c) [TH · ★★] Giải hệ theo u, v và tìm nghiệm (x; y)',
        'muc_y': 'a) TH · b) TH · c) TH',
        'phut': 18
    }
}

def fix_vai(muc: str, vai: str) -> str:
    if vai == 'NB tách TH':
        if muc == 'TH':
            return 'TH của phiếu'
        elif muc in ('VD', 'VDC'):
            return 'VD lẻ'
    return vai

def update_phan_dang_ch5() -> dict:
    print("\n==================== UPDATING 'Phân dạng Ch.V lớp 9C' ====================")
    # Read rows from Google Sheets (A..P)
    # Note: Column P was inserted at 15. So A..O is cols 0..14, P is 15.
    res = subprocess.run(['gsheets', 'readonly', 'read', SPREADSHEET_ID, "'Phân dạng Ch.V lớp 9C'!A2:P1115", '--json'], capture_output=True, text=True)
    rows = json.loads(res.stdout)
    print(f"Read {len(rows)} data rows.")
    
    fixed_vai_cnt = 0
    scaffold_cnt = 0
    
    # We will update:
    # G (Thời lượng - col 6), J (Mức độ từng ý - col 9), N (Phân loại câu - col 13), P (Scaffold - col 15)
    batch_ops = []
    
    for idx, r in enumerate(rows):
        row_num = idx + 2
        de = r[0] if len(r) > 0 else ''
        muc = r[2] if len(r) > 2 else ''
        phut_cur = r[6] if len(r) > 6 else ''
        muc_y_cur = r[9] if len(r) > 9 else ''
        ma = r[12] if len(r) > 12 else ''
        vai_cur = r[13] if len(r) > 13 else ''
        
        # 1. Fix vai (Phân loại câu)
        new_vai = fix_vai(muc, vai_cur)
        vai_changed = (new_vai != vai_cur)
        if vai_changed:
            fixed_vai_cnt += 1
            
        # 2. Check scaffold
        scaffold_info = SCAFFOLD_SAMPLES.get(ma)
        if scaffold_info:
            scaffold_cnt += 1
            scaffold_str = scaffold_info['scaffold']
            new_muc_y = scaffold_info['muc_y']
            new_phut = str(scaffold_info['phut'])
            
            # Write G, J, N, P
            batch_ops.append({
                "op": "write",
                "range": f"'Phân dạng Ch.V lớp 9C'!G{row_num}",
                "data": [[new_phut]]
            })
            batch_ops.append({
                "op": "write",
                "range": f"'Phân dạng Ch.V lớp 9C'!J{row_num}",
                "data": [[new_muc_y]]
            })
            batch_ops.append({
                "op": "write",
                "range": f"'Phân dạng Ch.V lớp 9C'!N{row_num}",
                "data": [[new_vai]]
            })
            batch_ops.append({
                "op": "write",
                "range": f"'Phân dạng Ch.V lớp 9C'!P{row_num}",
                "data": [[scaffold_str]]
            })
        elif vai_changed:
            batch_ops.append({
                "op": "write",
                "range": f"'Phân dạng Ch.V lớp 9C'!N{row_num}",
                "data": [[new_vai]]
            })
            
    print(f"Summary for Phân dạng Ch.V: {fixed_vai_cnt} rows fixed 'Phân loại câu', {scaffold_cnt} rows added scaffold.")
    print(f"Executing {len(batch_ops)} cell writes in batches...")
    
    # Run batch in chunks of 100 ops
    CHUNK = 100
    for i in range(0, len(batch_ops), CHUNK):
        chunk = batch_ops[i:i+CHUNK]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(chunk, f, ensure_ascii=False)
            tmp_p = f.name
        res = subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp_p], capture_output=True, text=True)
        os.remove(tmp_p)
        if res.returncode != 0:
            print(f"Failed at batch {i}: {res.stderr}")
            raise RuntimeError(res.stderr)
        time.sleep(0.3)
        
    print("✓ Tab 'Phân dạng Ch.V lớp 9C' updated successfully!")
    return {"fixed_vai": fixed_vai_cnt, "scaffold": scaffold_cnt}


def update_de_thi() -> dict:
    print("\n==================== UPDATING 'Đề thi' ====================")
    # Read rows from Google Sheets (A..P)
    # Row 6..2653
    res = subprocess.run(['gsheets', 'readonly', 'read', SPREADSHEET_ID, "'Đề thi'!A6:P2655", '--json'], capture_output=True, text=True)
    rows = json.loads(res.stdout)
    print(f"Read {len(rows)} data rows.")
    
    fixed_vai_cnt = 0
    scaffold_cnt = 0
    
    batch_ops = []
    
    for idx, r in enumerate(rows):
        row_num = idx + 6
        de = r[0] if len(r) > 0 else ''
        muc = r[2] if len(r) > 2 else ''
        phut_cur = r[6] if len(r) > 6 else ''
        muc_y_cur = r[9] if len(r) > 9 else ''
        ma = r[12] if len(r) > 12 else ''
        vai_cur = r[13] if len(r) > 13 else ''
        
        # 1. Fix vai (Phân loại câu)
        new_vai = fix_vai(muc, vai_cur)
        vai_changed = (new_vai != vai_cur)
        if vai_changed:
            fixed_vai_cnt += 1
            
        # 2. Check scaffold
        scaffold_info = SCAFFOLD_SAMPLES.get(ma)
        if scaffold_info:
            scaffold_cnt += 1
            scaffold_str = scaffold_info['scaffold']
            new_muc_y = scaffold_info['muc_y']
            new_phut = str(scaffold_info['phut'])
            
            # Write G, J, N, P
            batch_ops.append({
                "op": "write",
                "range": f"'Đề thi'!G{row_num}",
                "data": [[new_phut]]
            })
            batch_ops.append({
                "op": "write",
                "range": f"'Đề thi'!J{row_num}",
                "data": [[new_muc_y]]
            })
            batch_ops.append({
                "op": "write",
                "range": f"'Đề thi'!N{row_num}",
                "data": [[new_vai]]
            })
            batch_ops.append({
                "op": "write",
                "range": f"'Đề thi'!P{row_num}",
                "data": [[scaffold_str]]
            })
        elif vai_changed:
            batch_ops.append({
                "op": "write",
                "range": f"'Đề thi'!N{row_num}",
                "data": [[new_vai]]
            })
            
    print(f"Summary for Đề thi: {fixed_vai_cnt} rows fixed 'Phân loại câu', {scaffold_cnt} rows added scaffold.")
    print(f"Executing {len(batch_ops)} cell writes in batches...")
    
    CHUNK = 100
    for i in range(0, len(batch_ops), CHUNK):
        chunk = batch_ops[i:i+CHUNK]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(chunk, f, ensure_ascii=False)
            tmp_p = f.name
        res = subprocess.run(['gsheets', 'mutate', 'batch', SPREADSHEET_ID, '-f', tmp_p], capture_output=True, text=True)
        os.remove(tmp_p)
        if res.returncode != 0:
            print(f"Failed at batch {i}: {res.stderr}")
            raise RuntimeError(res.stderr)
        time.sleep(0.3)
        
    print("✓ Tab 'Đề thi' updated successfully!")
    return {"fixed_vai": fixed_vai_cnt, "scaffold": scaffold_cnt}


def update_cache_json() -> dict:
    print(f"\n==================== UPDATING CACHE {CACHE_FILE} ====================")
    data = json.load(open(CACHE_FILE, 'r', encoding='utf-8'))
    print(f"Loaded {len(data)} rows.")
    
    fixed_vai_cnt = 0
    scaffold_cnt = 0
    new_data = []
    
    for idx, r in enumerate(data):
        muc = r[2] if len(r) > 2 else ''
        ma = r[12] if len(r) > 12 else ''
        vai = r[13] if len(r) > 13 else ''
        
        # 1. Fix vai
        new_vai = fix_vai(muc, vai)
        if new_vai != vai:
            fixed_vai_cnt += 1
            r[13] = new_vai
            
        # 2. Check scaffold
        scaffold_str = ""
        scaffold_info = SCAFFOLD_SAMPLES.get(ma)
        if scaffold_info:
            scaffold_cnt += 1
            scaffold_str = scaffold_info['scaffold']
            r[6] = str(scaffold_info['phut'])
            r[9] = scaffold_info['muc_y']
            
        # 3. Insert Column P (scaffold) at index 15
        # If row has >= 46 elements:
        # r[0:15] + [scaffold_str] + r[15:]
        new_row = list(r[:15]) + [scaffold_str] + list(r[15:])
        new_data.append(new_row)
        
    print(f"Summary for cache: {fixed_vai_cnt} rows fixed 'Phân loại câu', {scaffold_cnt} rows added scaffold.")
    print(f"New row 0 length: {len(new_data[0])}")
    
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=1)
        
    print(f"✓ Saved updated cache to {CACHE_FILE}!")
    return {"fixed_vai": fixed_vai_cnt, "scaffold": scaffold_cnt}


def main():
    res_ch5 = update_phan_dang_ch5()
    res_de = update_de_thi()
    res_cache = update_cache_json()
    
    print("\n==================== FINAL SUMMARY ====================")
    print(f"1. Tab 'Phân dạng Ch.V lớp 9C': {res_ch5['fixed_vai']} câu sửa phân loại, {res_ch5['scaffold']} câu thêm scaffold")
    print(f"2. Tab 'Đề thi': {res_de['fixed_vai']} câu sửa phân loại, {res_de['scaffold']} câu thêm scaffold")
    print(f"3. Cache JSON: {res_cache['fixed_vai']} câu sửa phân loại, {res_cache['scaffold']} câu thêm scaffold, 5565 dòng đã mở rộng cột P")
    print("ALL UPDATES COMPLETED!")

if __name__ == '__main__':
    main()
