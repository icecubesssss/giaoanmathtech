# -*- coding: utf-8 -*-
import json, glob, os

slugs = [
    'gk2-2023-thcs-nguyen-duc-luong',
    'gk2-2023-thcs-thuong-cat',
    'gk2-2024-ban-mai-school',
    'gk2-2024-luong-the-vinh',
    'gk2-2024-thcs-ai-mo',
    'gk2-2024-thcs-cau-giay',
    'gk2-2024-thcs-chuong-duong'
]

required_cau_fields = [
    'id', 'vi_tri', 'loai', 'chuong', 'dang', 'band',
    'phut', 'diem_bai', 'de', 'trang', 'co_hinh', 'can_doc_anh', 'da_duyet'
]

all_passed = True

print(f"{'SLUG':<35} | {'CAU':<4} | {'DIEM':<6} | {'CAN_DOC':<7} | {'DUYET':<5} | {'TANG':<4} | {'STATUS'}")
print("-" * 80)

for s in slugs:
    p = f'inputs/refs/de-thi/lop-8/exams/{s}.json'
    if not os.path.exists(p):
        print(f"ERROR: File not found {p}")
        all_passed = False
        continue

    with open(p, encoding='utf-8') as f:
        d = json.load(f)

    # Top-level checks
    tang = d.get('tang')
    da_duyet = d.get('da_duyet')
    ghi_chu = d.get('ghi_chu', '')
    cau_list = d.get('cau', [])
    
    total_score = round(sum(c.get('diem_bai', 0) or 0 for c in cau_list), 4)
    can_doc_count = sum(1 for c in cau_list if c.get('can_doc_anh', False))
    cau_duyet_count = sum(1 for c in cau_list if c.get('da_duyet', False))

    errors = []
    if tang != 2:
        errors.append(f"tang={tang} != 2")
    if da_duyet is not True:
        errors.append(f"top da_duyet={da_duyet}")
    if abs(total_score - 10.0) > 1e-6:
        errors.append(f"total_score={total_score} != 10.0")
    if can_doc_count != 0:
        errors.append(f"can_doc_count={can_doc_count} != 0")
    if cau_duyet_count != len(cau_list):
        errors.append(f"cau_duyet={cau_duyet_count}/{len(cau_list)}")

    for idx, c in enumerate(cau_list, 1):
        for fld in required_cau_fields:
            if fld not in c:
                errors.append(f"c{idx} missing {fld}")
        if 'loi_giai' not in c and 'dap_an' not in c:
            errors.append(f"c{idx} missing both loi_giai and dap_an")
        if c.get('can_doc_anh') is not False:
            errors.append(f"c{idx} can_doc_anh is not False")
        if c.get('da_duyet') is not True:
            errors.append(f"c{idx} da_duyet is not True")
        if c.get('diem_bai') is None or c.get('diem_bai') <= 0:
            errors.append(f"c{idx} diem_bai={c.get('diem_bai')} invalid")

    status = "PASSED" if not errors else f"FAILED: {'; '.join(errors)}"
    if errors:
        all_passed = False

    print(f"{s:<35} | {len(cau_list):<4} | {total_score:<6.2f} | {can_doc_count:<7} | {str(da_duyet):<5} | {tang:<4} | {status}")

print("-" * 80)
if all_passed:
    print("ALL 7 EXAMS FULLY COMPLIANT AND VERIFIED! 100% OK.")
else:
    print("SOME CHECKS FAILED! Please review output above.")
