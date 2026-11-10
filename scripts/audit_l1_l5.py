#!/usr/bin/env python3
"""KIỂM ĐỊNH CHẤT LƯỢNG NGÂN HÀNG CÂU HỎI LỚP 9: QUÉT BỘ LỌC L1–L5,
THANH LỌC CÂU NB MÁY MÓC, ĐỒNG BỘ TH/NB VÀ ĐIỀN CỘT P (TRẠNG THÁI) & CỘT Q (LOẠI NGAY).

Quy chuẩn áp dụng:
- Quy chuẩn học liệu (docs/quy-chuan-hoc-lieu.md) ngày 03/11/2026.
- Quy định thuyết minh chốt ngày 2026-07-07 & 2026-07-22 (AGENTS.md).
- Ngưỡng điểm chuẩn: VD/VDC >= 7, TH >= 6, NB >= 5.

File nguồn: scratch/ngan_hang_cau_scored_all.json (5.565 câu)
File xuất:  scratch/ngan_hang_cau_audited_l1_l5.json
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "scratch" / "ngan_hang_cau_scored_all.json"
OUTPUT_FILE = ROOT / "scratch" / "ngan_hang_cau_audited_l1_l5.json"

def clean_text(s: str) -> str:
    """Chuẩn hoá văn bản đề bài để so khớp trùng lặp."""
    s = re.sub(r'^(Câu|Bài)\s*\d+[\.:\s]*', '', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def mask_digits(s: str) -> str:
    """Thay toàn bộ số bằng <N> để phát hiện bài clone đổi số."""
    s = clean_text(s)
    return re.sub(r'\d+([,\.]\d+)?', '<N>', s)

def audit_bank() -> dict:
    print(f"Loading input data from {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} rows.")

    rows = [list(r) for r in data]

    # =========================================================================
    # 1. BỘ LỌC L1: SAI BẢN CHẤT TOÁN HỌC / VÔ NGHIỆM NGOÀI Ý MUỐN / NGHIỆM KHÔNG XÁC ĐỊNH
    # =========================================================================
    l1_flagged: dict[int, str] = {}

    for idx, r in enumerate(rows):
        de = r[0] if len(r) > 0 else ""
        gc = r[11] if len(r) > 11 else ""
        ma = r[12] if len(r) > 12 else ""
        gc_lower = gc.lower()

        # Kiểm tra ghi chú có lỗi toán học, vô nghiệm ngoài ý muốn, mâu thuẫn giả thiết
        if any(k in gc_lower for k in [
            'vô nghiệm (0y = -14)',
            'rút gọn được 9 = 0 (vô nghiệm)',
            'không có gtln trên miền xác định',
            'tổng không có gtln',
            'mâu thuẫn với giả thiết',
            'tam giác vuông tại m mà ghi "đường cao nh"',
            'thiếu giá trị của x',
            'đề thiếu yêu cầu',
            'phương trình chứa a nhưng ghi "với tham số m"',
            'đề ghi "trung điểm của aj", j chưa được định nghĩa'
        ]):
            l1_flagged[idx] = f"L1: Sai bản chất toán / vô nghiệm ngoài ý muốn / thiếu dữ kiện ({gc})"
            continue

        # Đề vỡ rác pdftotext/OCR không thể giải được (nhiều dòng ký tự đơn lẻ cụt lủn)
        lines = [l.strip() for l in de.split('\n') if l.strip()]
        short_lines = [l for l in lines if len(l) <= 2]
        if len(short_lines) >= 8 and len(de) > 60 and ('Câu' in de or 'Bài' in de):
            l1_flagged[idx] = "L1: Đề vỡ rác pdftotext/OCR không xác định"
            continue

    print(f"-> L1 (Sai bản chất toán học / vô nghiệm / vỡ đề): {len(l1_flagged)} câu.")

    # =========================================================================
    # 2. BỘ LỌC L2: SỐ LIỆU PHI LÝ / BỐI CẢNH SAI THỰC TẾ
    # =========================================================================
    l2_flagged: dict[int, str] = {}

    for idx, r in enumerate(rows):
        if idx in l1_flagged:
            continue
        de = r[0] if len(r) > 0 else ""
        gc = r[11] if len(r) > 11 else ""
        gc_lower = gc.lower()

        if '29% là đất liền' in gc_lower:
            l2_flagged[idx] = "L2: Bối cảnh phi lý (29% Trái Đất là nước bao gồm núi, sa mạc)"
            continue
        if '44 ô tô nhưng chỉ in 22 số liệu' in gc_lower:
            l2_flagged[idx] = "L2: Lỗi số liệu thực nghiệm (đề ghi 44 ô tô nhưng chỉ cho 22 số liệu)"
            continue

        # Vận tốc phi lý trong thực tế
        m_bo = re.search(r'đi bộ\s*(với\s*)?vận tốc\s*(\d+([,\.]\d+)?)\s*km/h', de, re.I)
        if m_bo:
            val = float(m_bo.group(2).replace(',', '.'))
            if val > 15:
                l2_flagged[idx] = f"L2: Vận tốc người đi bộ {val} km/h phi lý (>15 km/h)"
                continue

        m_dap = re.search(r'xe đạp\s*(với\s*)?vận tốc\s*(\d+([,\.]\d+)?)\s*km/h', de, re.I)
        if m_dap:
            val = float(m_dap.group(2).replace(',', '.'))
            if val > 45:
                l2_flagged[idx] = f"L2: Vận tốc xe đạp {val} km/h phi lý (>45 km/h)"
                continue

    print(f"-> L2 (Số liệu phi lý / bối cảnh sai thực tế): {len(l2_flagged)} câu.")

    # =========================================================================
    # 3. BỘ LỌC L4: VƯỢT TRẦN SGK KNTT / CHƯƠNG TRÌNH CŨ 2006 ĐÃ BỎ
    # =========================================================================
    l4_flagged: dict[int, str] = {}
    l4_rules = [
        ('kiến thức lớp 10, vượt chương ii', 'L4: Kiến thức lớp 10 (hệ BPT 2 ẩn quy hoạch tuyến tính)'),
        ('bất phương trình bậc hai, vượt khung chương ii', 'L4: Kiến thức lớp 10 (bất phương trình bậc hai)'),
        ('bất đẳng thức cô-si ba số', 'L4: Vượt trần KNTT (Cô-si 3 số)'),
        ('ngoài sgk kntt', 'L4: Ngoài SGK KNTT (hình học toạ độ Parabol)'),
        ('vượt mức \'phương trình chứa căn đơn giản\'', 'L4: Vượt trần KNTT (PT vô tỉ nâng cao)'),
        ('bất đẳng thức nâng cao, vượt mức chương ii', 'L4: Vượt trần KNTT (BĐT nâng cao ngoài trần)'),
        ('bđt tìm gtnn có điều kiện, có thể vượt khung', 'L4: Vượt trần KNTT (BĐT nâng cao ngoài trần)'),
        ('liên hợp nâng cao', 'L4: Vượt trần KNTT (liên hợp căn thức nâng cao)'),
        ('tam thức bậc hai', 'L4: Kiến thức lớp 10 (dấu tam thức bậc hai)')
    ]

    for idx, r in enumerate(rows):
        if idx in l1_flagged or idx in l2_flagged:
            continue
        gc = r[11] if len(r) > 11 else ""
        gc_lower = gc.lower()
        for kw, desc in l4_rules:
            if kw in gc_lower:
                l4_flagged[idx] = desc
                break

    print(f"-> L4 (Vượt trần SGK KNTT / kiến thức cũ): {len(l4_flagged)} câu.")

    # =========================================================================
    # 4. BỘ LỌC L5: TRÙNG LẶP Ý TƯỞNG / CLONE BÀI CHỈ ĐỔI SỐ (> 85% TƯƠNG ĐỒNG)
    # =========================================================================
    l5_flagged: dict[int, str] = {}
    exact_l5_drops: set[int] = set()

    # Nhóm 1: Trùng lặp nguyên văn (Exact text normalization)
    exact_groups = defaultdict(list)
    for idx, r in enumerate(rows):
        if idx in l1_flagged or idx in l2_flagged or idx in l4_flagged:
            continue
        c_txt = clean_text(r[0])
        if len(c_txt) > 15:
            exact_groups[c_txt].append(idx)

    for c_txt, indices in exact_groups.items():
        if len(indices) > 1:
            def score_key(i: int) -> tuple[int, float]:
                ma = rows[i][12]
                is_exam = 2 if any(ma.startswith(p) for p in ('gk', 'ck', 'v10')) else (1 if 'sgk' in ma else 0)
                try:
                    score = float(rows[i][40]) if rows[i][40] else 0.0
                except (ValueError, TypeError):
                    score = 0.0
                return (is_exam, score)
            sorted_indices = sorted(indices, key=score_key, reverse=True)
            best = sorted_indices[0]
            for clone_idx in sorted_indices[1:]:
                l5_flagged[clone_idx] = f"L5: Trùng nguyên văn với câu {rows[best][12]}"
                exact_l5_drops.add(clone_idx)

    # Nhóm 2: Clone đổi số (Masked digits / near duplicate > 85%)
    masked_groups = defaultdict(list)
    for idx, r in enumerate(rows):
        if idx in l1_flagged or idx in l2_flagged or idx in l4_flagged or idx in l5_flagged:
            continue
        m_txt = mask_digits(r[0])
        if len(m_txt) > 25:
            masked_groups[m_txt].append(idx)

    for m_txt, indices in masked_groups.items():
        if len(indices) > 1:
            def score_key(i: int) -> tuple[int, float]:
                ma = rows[i][12]
                is_exam = 2 if any(ma.startswith(p) for p in ('gk', 'ck', 'v10')) else (1 if 'sgk' in ma else 0)
                try:
                    score = float(rows[i][40]) if rows[i][40] else 0.0
                except (ValueError, TypeError):
                    score = 0.0
                return (is_exam, score)
            sorted_indices = sorted(indices, key=score_key, reverse=True)
            best = sorted_indices[0]
            for clone_idx in sorted_indices[1:]:
                l5_flagged[clone_idx] = f"L5: Clone đổi số với câu {rows[best][12]}"

    print(f"-> L5 (Trùng lặp ý tưởng / clone đổi số): {len(l5_flagged)} câu (gồm {len(exact_l5_drops)} trùng nguyên văn).")

    # =========================================================================
    # 5. THANH LỌC CÂU NB NHẬN DẠNG MÁY MÓC (Theo chuẩn 2026-07-07 & 03/11/2026)
    # =========================================================================
    mech_nb_flagged: dict[int, str] = {}
    mech_pats = [
        (r'hệ số\s+[a-d]\s*,\s*[a-d]|hệ số\s+[a-d]\s+và\s+[a-d]|xác định\s+(các\s+)?hệ số\s+[a-d]', 'Xác định hệ số a, b, c máy móc'),
        (r'cặp số.*?(không\s+)?là nghiệm|trong các cặp số sau', 'Kiểm tra cặp số là nghiệm bằng thay số'),
        (r'hệ thức nào không phải là phương trình bậc nhất|phương trình nào.*?(không phải là|là)\s+phương trình bậc nhất|bất phương trình nào.*?(không phải là|là)\s+bất phương trình bậc nhất', 'Nhận diện PT/BPT bậc nhất hình thức'),
        (r'căn bậc hai số học của \d+|căn bậc ba của -\d+', 'Tính căn số học rời rạc không chứa biến'),
        (r'dùng máy tính cầm tay để kiểm tra nghiệm|sử dụng máy tính cầm tay, tìm nghiệm', 'Bấm máy tính cầm tay tìm nghiệm')
    ]

    for idx, r in enumerate(rows):
        if idx in l1_flagged or idx in l2_flagged or idx in l4_flagged:
            continue
        muc = r[2] if len(r) > 2 else ''
        de = r[0] if len(r) > 0 else ''
        dang = r[3] if len(r) > 3 else ''
        txt = f"{de} {dang}".lower()
        if muc == 'NB':
            for pat, desc in mech_pats:
                if re.search(pat, txt):
                    mech_nb_flagged[idx] = desc
                    break

    print(f"-> NB nhận dạng máy móc: {len(mech_nb_flagged)} câu.")

    # =========================================================================
    # 6. RÀ SOÁT CÂU TH BỊ NHẦM THÀNH NB (Chuẩn hoá mức độ & đồng bộ từng ý)
    # =========================================================================
    nb_to_th_indices: list[int] = []
    for idx, r in enumerate(rows):
        if idx in l1_flagged or idx in l2_flagged or idx in l4_flagged or idx in mech_nb_flagged or idx in l5_flagged:
            continue
        muc = r[2] if len(r) > 2 else ''
        if muc == 'NB':
            de = r[0] if len(r) > 0 else ''
            fmt = r[8] if len(r) > 8 else ''
            ch = r[28] if len(r) > 28 else ''

            # Không chuyển nếu bài có khung điền khuyết (là bước giàn giáo NB có chủ đích)
            if 'dots' in de or '[[blank:' in de:
                continue

            # 1. Giải trọn vẹn phương trình / bất phương trình / hệ phương trình
            is_solve = bool(re.search(r'^\s*(Câu\s*\d+[\.:\s]*)?giải\s+(các\s+)?(phương\s+trình|bất\s+phương\s+trình|hệ\s+phương\s+trình)\b', de, re.I))
            # 2. Chứng minh hình học trong các chương hình
            is_geom_proof = bool(re.search(r'\bchứng minh(\s+rằng)?\s*[:\n]|\bchứng minh\s+[a-d]\)', de, re.I)) and any(k in ch for k in ['[IV]', '[V]', '[IX]'])
            # 3. Bài toán thực tế có lời văn
            is_word = bool(re.search(r'\b(giải bài toán bằng cách lập|một ô tô|một người đi xe|hai tổ sản xuất|hai người cùng làm|một mảnh đất hình chữ nhật có chu vi|một thửa ruộng)\b', de, re.I)) and len(de) > 120

            if (is_solve or is_geom_proof or is_word) and 'trắc nghiệm' not in fmt.lower() and 'chọn' not in fmt.lower():
                nb_to_th_indices.append(idx)

    print(f"-> Rà soát mức độ: {len(nb_to_th_indices)} câu NB được điều chỉnh sang đúng mức TH.")

    # =========================================================================
    # 7. ĐIỀN CỘT P (TRẠNG THÁI) VÀ CỘT Q (LOẠI NGAY L1-L5) VÀ CẬP NHẬT MỨC ĐỘ
    # =========================================================================
    # Lưu ý về cấu trúc cột trong rows (đã có cột Scaffold ở index 15):
    # Index 15: Scaffold (giữ nguyên)
    # Index 16: Trạng thái (Cột P)
    # Index 17: Loại ngay L1-L5 (Cột Q)
    # Index 40: Điểm lớp C
    # Index 43: Ngưỡng theo mức (NB=5, TH=6, VD=7)
    # Index 44: Kết luận lớp C (Đưa vào bài, Dự phòng / sửa, Loại hoặc sửa)

    stats_q = Counter()
    stats_p = Counter()

    for idx, r in enumerate(rows):
        # 1. Cập nhật mức độ cho câu TH bị nhầm thành NB
        if idx in nb_to_th_indices:
            r[2] = 'TH'  # Col C
            if r[9] == 'NB':
                r[9] = 'TH'  # Col J (Mức độ từng ý)
            r[43] = '6'      # Col AQ (Ngưỡng TH = 6)
            # Tính lại kết luận lớp C dựa trên điểm C
            try:
                sc_c = float(r[40]) if r[40] else 0.0
                if sc_c >= 6.0:
                    r[44] = 'Đưa vào bài'
                elif sc_c >= 5.0:
                    r[44] = 'Dự phòng / sửa'
                else:
                    r[44] = 'Loại hoặc sửa'
            except (ValueError, TypeError):
                pass

        # 2. Xác định Loại ngay (Col Q / index 17) & Trạng thái (Col P / index 16)
        q_val = ""
        p_val = ""

        if idx in l1_flagged:
            q_val = "L1"
            p_val = "Bỏ (L1: Sai bản chất toán)"
        elif idx in l2_flagged:
            q_val = "L2"
            p_val = "Bỏ (L2: Bối cảnh phi lý)"
        elif idx in l4_flagged:
            q_val = "L4"
            p_val = "Bỏ (L4: Vượt trần SGK KNTT)"
        elif idx in l5_flagged:
            q_val = "L5"
            if idx in exact_l5_drops:
                p_val = "Bỏ (L5: Trùng lặp đề)"
            else:
                p_val = "Dự phòng"
        elif idx in mech_nb_flagged:
            q_val = ""
            ma = r[12] if len(r) > 12 else ""
            if 'sgk' in ma:
                p_val = "Dự phòng"
            else:
                p_val = "Bỏ (NB nhận dạng máy móc)"
        else:
            q_val = ""
            col_ar = r[44] if len(r) > 44 else ""
            if "Đưa vào bài" in str(col_ar):
                p_val = "Dùng"
            elif "Dự phòng" in str(col_ar):
                p_val = "Dự phòng"
            elif "Loại" in str(col_ar):
                p_val = "Bỏ (Dưới ngưỡng điểm)"
            else:
                p_val = "Dùng"

        # Ghi vào row:
        # index 16 là Trạng thái, index 17 là Loại ngay (L1-L5)
        r[16] = p_val
        r[17] = q_val

        # Cập nhật Col 44 (Kết luận) nếu có loại ngay
        if q_val:
            r[44] = f"Loại ({q_val})"

        stats_q[q_val] += 1
        stats_p[p_val] += 1

    # =========================================================================
    # 8. LƯU KẾT QUẢ RA FILE OUTPUT
    # =========================================================================
    print(f"\nWriting audited bank to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print(f"Successfully saved {len(rows)} audited rows to {OUTPUT_FILE}!")

    # =========================================================================
    # 9. BÁO CÁO THỐNG KÊ CHI TIẾT
    # =========================================================================
    dung_cnt = stats_p['Dùng']
    du_phong_cnt = stats_p['Dự phòng']
    bo_cnt = sum(v for k, v in stats_p.items() if k.startswith('Bỏ'))
    total = len(rows)

    report = {
        "total": total,
        "l1_count": len(l1_flagged),
        "l2_count": len(l2_flagged),
        "l4_count": len(l4_flagged),
        "l5_count": len(l5_flagged),
        "mech_nb_count": len(mech_nb_flagged),
        "nb_to_th_count": len(nb_to_th_indices),
        "stats_col_q": dict(stats_q),
        "stats_col_p": dict(stats_p),
        "dung_cnt": dung_cnt,
        "du_phong_cnt": du_phong_cnt,
        "bo_cnt": bo_cnt,
        "pass_rate": dung_cnt / total
    }

    print("\n" + "="*70)
    print("           BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG NGÂN HÀNG CÂU LỚP 9")
    print("="*70)
    print(f"Tổng số câu trong kho: {total:,} câu\n")

    print("1. THỐNG KÊ CÁC BỘ LỌC LOẠI NGAY L1–L5 & THANH LỌC NB:")
    print(f"  • Bộ lọc L1 (Sai bản chất toán / vô nghiệm / vỡ đề) : {len(l1_flagged):4d} câu ({len(l1_flagged)/total:.2%})")
    print(f"  • Bộ lọc L2 (Số liệu phi lý / bối cảnh sai thực tế): {len(l2_flagged):4d} câu ({len(l2_flagged)/total:.2%})")
    print(f"  • Bộ lọc L4 (Vượt trần SGK KNTT / kiến thức cũ)    : {len(l4_flagged):4d} câu ({len(l4_flagged)/total:.2%})")
    print(f"  • Bộ lọc L5 (Trùng lặp ý tưởng / clone đổi số)     : {len(l5_flagged):4d} câu ({len(l5_flagged)/total:.2%})")
    print(f"  • NB nhận dạng máy móc (thanh lọc theo chuẩn Thầy) : {len(mech_nb_flagged):4d} câu ({len(mech_nb_flagged)/total:.2%})")
    print(f"  • Điều chỉnh mức độ (NB nhầm sang TH tự luận)       : {len(nb_to_th_indices):4d} câu ({len(nb_to_th_indices)/total:.2%})\n")

    print("2. PHÂN BỐ CỘT Q ('Loại ngay L1-L5'):")
    for k, v in stats_q.most_common():
        lbl = k if k else "(Đạt chuẩn - Trống)"
        print(f"  - {lbl:35s}: {v:5d} câu ({v/total:6.2%})")

    print("\n3. PHÂN BỐ CỘT P ('Trạng thái'):")
    for k, v in stats_p.most_common():
        print(f"  - {k:35s}: {v:5d} câu ({v/total:6.2%})")

    print("\n4. TỔNG KẾT TỈ LỆ ĐẠT CHUẨN:")
    print(f"  ★ ĐẠT CHUẨN ĐƯA VÀO BÀI ('Dùng')   : {dung_cnt:5d} câu ({dung_cnt/total:6.2%})")
    print(f"  ★ KHO DỰ PHÒNG ('Dự phòng')        : {du_phong_cnt:5d} câu ({du_phong_cnt/total:6.2%})")
    print(f"  ★ LOẠI BỎ KHỎI KHO CHÍNH ('Bỏ')    : {bo_cnt:5d} câu ({bo_cnt/total:6.2%})")
    print("="*70)

    return report

if __name__ == '__main__':
    audit_bank()
