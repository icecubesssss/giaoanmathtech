#!/usr/bin/env python3
"""Build expanded question bank for Chapter IV Geometry Grade 9.

Gom toàn diện:
1. 276 câu hiện có trong inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-04.json
2. 51+ câu đề thi thật GK1/CK1/V10 trong inputs/refs/de-thi/lop-9/exams/*.json (Ưu tiên 1)
3. 79 câu trắc nghiệm cuối chương từ tài liệu học tập KNTT HK1 (tr. 128-138)
4. 40+ câu tự luận từ tài liệu học tập KNTT HK1 (tr. 105-127)
5. 95+ câu từ 3 PDF chuyên đề Vũ Kim Lan (TSLG, Hệ thức cạnh-góc, Ứng dụng thực tế)
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.schema import ngan_hang_sheet as nhs


def clean_text(s: str) -> str:
    s = re.sub(r'TRANG:\s*\d+', '', s)
    s = re.sub(r'TOÁN 9 \(KNTT\) - HK1 - TÀI LIỆU HỌC TẬP\s*\n\s*NĂM HỌC:\s*\d+\s*-\s*\d+', '', s)
    s = re.sub(r'\x0c', '', s)
    # clean extra newlines
    lines = [l.strip() for l in s.split('\n')]
    # filter empty lines in sequence
    out = []
    for l in lines:
        if l or (out and out[-1]):
            out.append(l)
    return '\n'.join(out).strip()


def get_exam_questions():
    exam_rows = []
    for f in sorted(glob.glob(str(ROOT / 'inputs/refs/de-thi/lop-9/exams/*.json'))):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        truong = d.get('xuat_xu', {}).get('truong', '')
        ky = d.get('xuat_xu', {}).get('ky', '')
        nam = d.get('xuat_xu', {}).get('nam', '')
        exam_id = Path(f).stem
        for c in d.get('cau', []):
            ch = str(c.get('chuong', ''))
            dang = str(c.get('dang', []))
            de = str(c.get('de', '')).strip()
            # Chapter 4 geometry
            is_c4 = (
                ('C4' in ch or 'HH-C4' in ch or 'HH4' in ch or 'HETHUC' in dang or 'TSLG' in dang or 'LUONGGIAC' in dang)
                or any(k in de.lower() for k in [
                    'tỉ số lượng giác', 'hệ thức lượng', 'chiều cao của cây', 'bóng của cột cờ',
                    'chiều cao cột cờ', 'hải đăng', 'độ dốc', 'tòa nhà', 'khinh khí cầu',
                    'góc nghiêng', 'máy bay cất cánh', 'tháp eiffel', 'cây cau bị'
                ])
            )
            # Exclude circle chapter (C5) if it's purely circle
            if 'tiếp tuyến' in de.lower() and 'đường tròn' in de.lower() and not any(k in de.lower() for k in ['hệ thức lượng', 'sin', 'cos', 'tan', 'cot', 'chiều cao', 'bóng']):
                is_c4 = False

            if not is_c4 or len(de) < 15:
                continue

            band = c.get('band', 'TH')
            if band not in ('NB', 'TH', 'VD', 'VDC'):
                band = 'TH'

            # Assign phieu
            if any(k in de.lower() for k in ['máy bay', 'bóng', 'chiều cao', 'ngọn núi', 'tòa tháp', 'hải đăng', 'cây cau', 'cột cờ', 'khu vườn']):
                phieu = 'Phiếu 3 (Ứng dụng thực tế tỉ số lượng giác)'
                dang_txt = 'Ứng dụng thực tế tỉ số lượng giác (chiều cao, khoảng cách)'
                thuc_te = 'Có'
                vai = 'TH của phiếu' if band == 'TH' else ('VD của phiếu' if band in ('VD', 'VDC') else 'NB của phiếu')
            elif any(k in de.lower() for k in ['đường cao ah', 'hệ thức lượng', 'bh.ch', 'hình chiếu', 'ab.ac = ah.bc']):
                phieu = 'Phiếu 3 (Hệ thức lượng liên quan đến đường cao)'
                dang_txt = 'Hệ thức lượng liên quan đến đường cao trong tam giác vuông'
                thuc_te = 'Không'
                vai = 'TH ghép VD' if band in ('VD', 'VDC') else 'TH của phiếu'
            elif any(k in de.lower() for k in ['giải tam giác', 'tính cạnh', 'tính góc']):
                phieu = 'Phiếu 2 (Một số hệ thức về cạnh và góc trong tam giác vuông)'
                dang_txt = 'Giải tam giác vuông và hệ thức giữa cạnh và góc'
                thuc_te = 'Không'
                vai = 'TH của phiếu'
            else:
                phieu = 'Phiếu 1 (Tỉ số lượng giác của góc nhọn)'
                dang_txt = 'Tỉ số lượng giác của góc nhọn'
                thuc_te = 'Không'
                vai = 'NB của phiếu' if band == 'NB' else 'TH của phiếu'

            cid = c.get('id', '')
            ma = f"de-{cid}" if not cid.startswith('de-') else cid

            phut = float(c.get('phut', 6.0))
            if phut <= 0:
                phut = {'NB': 2.0, 'TH': 6.0, 'VD': 10.0, 'VDC': 15.0}.get(band, 6.0)

            exam_rows.append({
                'de': de,
                'nguon': f"Đề thi {truong} {ky} {nam}, {c.get('vi_tri', '')}".strip(', '),
                'band': band,
                'dang': dang_txt,
                'uu': 'Ưu tiên 1: Đề thi thật',
                'phieu': phieu,
                'phut': phut,
                'thuc_te': thuc_te,
                'fmt': 'Tự luận',
                'muc_y': band,
                'bai': 'Đề thi tổng hợp',
                'note': f"Trích từ exam {exam_id}",
                'ma': ma,
                'vai': vai,
                'de_xuat': '',
            })
    return exam_rows

print("get_exam_questions defined")

def get_kntt_mcq_questions():
    txt_path = ROOT / "storage/cache/dump_kntt_ch4.txt"
    if not txt_path.exists():
        txt_path = Path("/Users/admin/.gemini/antigravity/brain/e5344d42-dbc2-487f-a4b0-f711429657a3/scratch/dump_kntt_ch4.txt")
    txt = txt_path.read_text(encoding='utf-8')
    pos = txt.find('Bài tập trắc nghiệm cuối chương')
    mcq_txt = txt[pos:]
    
    # Split by "Câu N."
    pattern = r'\n(?=Câu\s+\d+\.)'
    parts = re.split(pattern, mcq_txt)
    
    mcq_rows = []
    # Section markers to identify dang & phieu
    cur_sec = "Một số hệ thức về cạnh và đường cao trong tam giác vuông"
    
    for p in parts[1:]:
        p_clean = clean_text(p)
        if '2. Định nghĩa tỉ số lượng giác' in p_clean or '2. Tỉ số lượng giác của góc nhọn' in p_clean:
            cur_sec = "Định nghĩa tỉ số lượng giác của một góc nhọn"
        elif '3. Một số hệ thức về cạnh và góc' in p_clean:
            cur_sec = "Một số hệ thức về cạnh và góc trong tam giác vuông"
        elif '4. Ứng dụng thực tế' in p_clean:
            cur_sec = "Ứng dụng thực tế các tỉ số lượng giác"

        # extract number
        m_num = re.match(r'Câu\s+(\d+)\.', p_clean)
        if not m_num:
            continue
        cnum = int(m_num.group(1))

        # Assign phieu, dang, band
        if "đường cao" in cur_sec:
            phieu = "Phiếu 3 (Hệ thức lượng liên quan đến đường cao)"
            dang = "Hệ thức về cạnh và đường cao trong tam giác vuông"
            bai = "Bài 12 (bổ trợ)"
            band = "NB" if cnum <= 10 else "TH"
            vai = "NB của phiếu" if band == "NB" else "TH của phiếu"
            thuc_te = "Không"
        elif "Tỉ số lượng giác" in cur_sec:
            phieu = "Phiếu 1 (Tỉ số lượng giác của góc nhọn)"
            dang = "Định nghĩa và tính chất tỉ số lượng giác góc nhọn"
            bai = "Bài 11"
            band = "NB" if cnum <= 35 else "TH"
            vai = "NB của phiếu" if band == "NB" else "TH của phiếu"
            thuc_te = "Không"
        elif "cạnh và góc" in cur_sec:
            phieu = "Phiếu 2 (Một số hệ thức về cạnh và góc trong tam giác vuông)"
            dang = "Hệ thức giữa cạnh và góc của tam giác vuông"
            bai = "Bài 12"
            band = "NB" if cnum <= 55 else "TH"
            vai = "NB của phiếu" if band == "NB" else "TH của phiếu"
            thuc_te = "Không"
        else:
            phieu = "Phiếu 3 (Ứng dụng thực tế tỉ số lượng giác)"
            dang = "Ứng dụng thực tế tỉ số lượng giác"
            bai = "Bài 12"
            band = "TH" if cnum <= 70 else "VD"
            vai = "TH của phiếu" if band == "TH" else "VD của phiếu"
            thuc_te = "Có"

        ma = f"kntt-hk1-tn-c{cnum:02d}"
        mcq_rows.append({
            'de': p_clean,
            'nguon': f"Tài liệu học tập Toán 9 KNTT HK1, Trắc nghiệm cuối chương 4, Câu {cnum}",
            'band': band,
            'dang': dang,
            'uu': 'Ưu tiên 2: SGK và SBT',
            'phieu': phieu,
            'phut': 1.5 if band == 'NB' else (3.0 if band == 'TH' else 5.0),
            'thuc_te': thuc_te,
            'fmt': 'Trắc nghiệm 4 lựa chọn',
            'muc_y': band,
            'bai': bai,
            'note': f"Trắc nghiệm cuối chương 4 ({cur_sec})",
            'ma': ma,
            'vai': vai,
            'de_xuat': '',
        })
    return mcq_rows


def get_kntt_tuluan_questions():
    txt_path = ROOT / "storage/cache/dump_kntt_ch4.txt"
    if not txt_path.exists():
        txt_path = Path("/Users/admin/.gemini/antigravity/brain/e5344d42-dbc2-487f-a4b0-f711429657a3/scratch/dump_kntt_ch4.txt")
    txt = txt_path.read_text(encoding='utf-8')
    pos = txt.find('Bài tập trắc nghiệm cuối chương')
    tl_txt = txt[:pos]

    pattern = r'\n(?=(?:Bài|Ví dụ)\s+\d+\.)'
    parts = re.split(pattern, tl_txt)

    tl_rows = []
    seen_texts = set()
    idx = 0
    cur_bai = "Bài 11"
    cur_sec = "Bài tập tự luận tỉ số lượng giác"

    for p in parts[1:]:
        p_clean = clean_text(p)
        if len(p_clean) < 25:
            continue
        if 'A. KIẾN THỨC CƠ BẢN' in p_clean and len(p_clean) < 150:
            continue

        if 'Bài 2. Hệ thức giữa cạnh và góc' in p_clean:
            cur_bai = "Bài 12"
            cur_sec = "Hệ thức giữa cạnh và góc của tam giác vuông"
        elif 'Bài 1. Tỉ số lượng giác' in p_clean:
            cur_bai = "Bài 11"
            cur_sec = "Tỉ số lượng giác của góc nhọn"

        # deduplicate very similar text
        norm = re.sub(r'\s+', ' ', p_clean[:80])
        if norm in seen_texts:
            continue
        seen_texts.add(norm)

        idx += 1
        # determine phieu, dang, band
        is_thuc_te = any(k in p_clean.lower() for k in ['tháp', 'cây', 'bóng', 'nắng', 'thang', 'tòa nhà', 'núi', 'khoảng cách', 'máy bay', 'vật được ném'])
        thuc_te = 'Có' if is_thuc_te else 'Không'

        if is_thuc_te:
            phieu = 'Phiếu 3 (Ứng dụng thực tế tỉ số lượng giác)'
            dang = 'Ứng dụng thực tế tỉ số lượng giác (chiều cao, khoảng cách)'
            band = 'TH'
            vai = 'TH của phiếu'
            phut = 8.0
        elif 'đường cao' in p_clean.lower() or 'hệ thức' in p_clean.lower() or 'tam giác vuông tại a , đường cao ah' in p_clean.lower():
            phieu = 'Phiếu 3 (Hệ thức lượng liên quan đến đường cao)'
            dang = 'Hệ thức lượng liên quan đến đường cao trong tam giác vuông'
            band = 'TH' if 'chứng minh' not in p_clean.lower() else 'VD'
            vai = 'TH ghép VD' if band == 'VD' else 'TH của phiếu'
            phut = 10.0 if band == 'VD' else 6.0
        elif cur_bai == 'Bài 12' or 'giải tam giác' in p_clean.lower() or 'tính độ dài cạnh x' in p_clean.lower():
            phieu = 'Phiếu 2 (Một số hệ thức về cạnh và góc trong tam giác vuông)'
            dang = 'Hệ thức giữa cạnh và góc và giải tam giác vuông'
            band = 'TH'
            vai = 'TH của phiếu'
            phut = 6.0
        else:
            phieu = 'Phiếu 1 (Tỉ số lượng giác của góc nhọn)'
            dang = 'Tỉ số lượng giác của góc nhọn'
            band = 'NB' if any(k in p_clean.lower() for k in ['tính tỉ số lượng giác', 'so sánh']) and len(p_clean) < 150 else 'TH'
            vai = 'NB của phiếu' if band == 'NB' else 'TH của phiếu'
            phut = 3.0 if band == 'NB' else 6.0

        ma = f"kntt-hk1-tl-b{idx:02d}"
        tl_rows.append({
            'de': p_clean,
            'nguon': f"Tài liệu học tập Toán 9 KNTT HK1, {cur_sec}",
            'band': band,
            'dang': dang,
            'uu': 'Ưu tiên 2: SGK và SBT',
            'phieu': phieu,
            'phut': phut,
            'thuc_te': thuc_te,
            'fmt': 'Tự luận',
            'muc_y': band,
            'bai': cur_bai,
            'note': f"Tự luận KNTT HK1 ({cur_sec})",
            'ma': ma,
            'vai': vai,
            'de_xuat': '',
        })
    return tl_rows


def get_lan_specialized_questions():
    lan_rows = []
    
    files = [
        ('dump_lan_p1.txt', 'chde-vkl1', 'Bài 11', 'Phiếu 1 (Tỉ số lượng giác của góc nhọn)', 'Tỉ số lượng giác của góc nhọn (Vũ Kim Lan)'),
        ('dump_lan_p2.txt', 'chde-vkl2', 'Bài 12', 'Phiếu 2 (Một số hệ thức về cạnh và góc trong tam giác vuông)', 'Hệ thức cạnh và góc tam giác vuông (Vũ Kim Lan)'),
        ('dump_lan_p3.txt', 'chde-vkl3', 'Bài 12', 'Phiếu 3 (Ứng dụng thực tế tỉ số lượng giác)', 'Ứng dụng thực tế tỉ số lượng giác (Vũ Kim Lan)'),
    ]

    for fname, prefix, bai, phieu, nguon_base in files:
        fpath = ROOT / f"storage/cache/{fname}"
        if not fpath.exists():
            fpath = Path(f"/Users/admin/.gemini/antigravity/brain/e5344d42-dbc2-487f-a4b0-f711429657a3/scratch/{fname}")
        txt = fpath.read_text(encoding='utf-8')
        
        parts = re.split(r'\n(?=(?:Bài|Ví dụ)\s+\d+\.)', txt)
        cur_dang = "Bài tập chuyên đề"
        idx = 0
        for p in parts[1:]:
            p_clean = clean_text(p)
            if len(p_clean) < 25:
                continue

            # check if a new Dạng starts
            m_dang = re.search(r'(Dạng\s+\d+\.[^\n]+)', p_clean)
            if m_dang:
                cur_dang = m_dang.group(1).strip()

            idx += 1
            is_thuc_te = 'Ứng dụng' in nguon_base or any(k in p_clean.lower() for k in ['tháp', 'cây', 'bóng', 'thang', 'tòa nhà', 'hải đăng', 'núi', 'sông', 'ca nô', 'tàu thủy', 'máy bay', 'khinh khí cầu'])
            thuc_te = 'Có' if is_thuc_te else 'Không'

            # determine band
            if any(k in p_clean.lower() for k in ['chứng minh', 'nâng cao', 'cực trị', 'tìm giá trị lớn nhất', 'rô-bốt']):
                band = 'VD'
                vai = 'VD của phiếu'
                phut = 12.0
            elif 'So sánh' in cur_dang or ('Tính các tỉ số' in p_clean and len(p_clean) < 120):
                band = 'NB'
                vai = 'NB của phiếu'
                phut = 2.0
            else:
                band = 'TH'
                vai = 'TH của phiếu'
                phut = 6.0

            ma = f"{prefix}-b{idx:02d}"
            lan_rows.append({
                'de': p_clean,
                'nguon': f"Chuyên đề {nguon_base}, {cur_dang}, Bài {idx}",
                'band': band,
                'dang': f"{cur_dang}",
                'uu': 'Ưu tiên 3: Tài liệu khác',
                'phieu': phieu,
                'phut': phut,
                'thuc_te': thuc_te,
                'fmt': 'Tự luận',
                'muc_y': band,
                'bai': bai,
                'note': f"{nguon_base} - {cur_dang}",
                'ma': ma,
                'vai': vai,
                'de_xuat': '',
            })
    return lan_rows

