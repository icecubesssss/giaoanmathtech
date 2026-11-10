import json
import glob

slugs = [
    'gk2-2025-thcs-khuong-thuong',
    'gk2-2025-thcs-mai-dich',
    'gk2-2025-thcs-nghia-tan',
    'gk2-2025-thcs-nghia-tan-2',
    'gk2-2025-thcs-ngoc-lam',
    'gk2-2025-thcs-nguyen-cong-tru',
    'gk2-2025-thcs-nguyen-khe',
    'gk2-2025-thcs-phan-chu-trinh',
    'gk2-2025-thcs-phan-dinh-giot',
    'gk2-2025-thcs-phuong-liet',
    'gk2-2025-thcs-van-yen',
    'gk2-x-kntt-gk2-de-1',
    'gk2-x-kntt-gk2-de-2'
]

required_cau_fields = [
    'id', 'vi_tri', 'loai', 'chuong', 'dang', 'band', 
    'phut', 'diem_bai', 'de', 'trang', 'co_hinh', 
    'can_doc_anh', 'da_duyet'
]

print(f"{'SLUG':<30} | {'TẦNG':<4} | {'DUYỆT':<5} | {'SỐ CÂU':<6} | {'CẦN ẢNH':<7} | {'TỔNG ĐIỂM':<9} | {'TRẠNG THÁI'}")
print("-" * 85)

all_ok = True
summary_details = []

for s in slugs:
    p = f"inputs/refs/de-thi/lop-8/exams/{s}.json"
    data = json.load(open(p, 'r', encoding='utf-8'))
    
    tang = data.get('tang')
    da_duyet = data.get('da_duyet')
    cau = data.get('cau', [])
    
    total_pts = round(sum(c.get('diem_bai', 0) for c in cau), 2)
    can_doc_anh_count = sum(1 for c in cau if c.get('can_doc_anh', False))
    cau_chua_duyet = sum(1 for c in cau if not c.get('da_duyet', False))
    
    missing_fields = []
    for idx, c in enumerate(cau):
        for f in required_cau_fields:
            if f not in c:
                missing_fields.append(f"Câu {c.get('vi_tri', idx)} thiếu {f}")
        # Lời giải / đáp án
        if not c.get('dap_an') and not c.get('loi_giai'):
            missing_fields.append(f"Câu {c.get('vi_tri', idx)} thiếu dap_an/loi_giai")
            
    is_ok = True
    issues = []
    if tang != 2:
        is_ok = False
        issues.append(f"tang={tang}")
    if da_duyet is not True:
        is_ok = False
        issues.append(f"da_duyet={da_duyet}")
    if can_doc_anh_count > 0:
        is_ok = False
        issues.append(f"can_doc_anh={can_doc_anh_count}")
    if cau_chua_duyet > 0:
        is_ok = False
        issues.append(f"cau_chua_duyet={cau_chua_duyet}")
    if abs(total_pts - 10.0) > 1e-4:
        is_ok = False
        issues.append(f"total_pts={total_pts}")
    if missing_fields:
        is_ok = False
        issues.append(f"missing={len(missing_fields)}")
        
    if not is_ok:
        all_ok = False
        status = "LỖI: " + ", ".join(issues)
    else:
        status = "CHÍNH XÁC 100%"
        
    print(f"{s:<30} | {tang:<4} | {str(da_duyet):<5} | {len(cau):<6} | {can_doc_anh_count:<7} | {total_pts:<9.2f} | {status}")
    
    summary_details.append({
        'slug': s,
        'cau_count': len(cau),
        'total_pts': total_pts,
        'status': status
    })

print("-" * 85)
if all_ok:
    print(">>> TẤT CẢ 13 ĐỀ ĐỀU ĐẠT CHUẨN XUẤT SẮC! KHÔNG CÓ BẤT KỲ LỖI NÀO! <<<")
else:
    print(">>> CÓ ĐỀ CHƯA ĐẠT CHUẨN, CẦN KIỂM TRA LẠI! <<<")
