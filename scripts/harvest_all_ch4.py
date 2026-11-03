#!/usr/bin/env python3
"""Harvest ALL remaining Chapter IV geometry materials in repo.
Target: reach 1,000+ questions matching Chapter V scale!
"""
from __future__ import annotations

import glob
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import docx


def clean_text(s: str) -> str:
    s = re.sub(r'TRANG:\s*\d+', '', s)
    s = re.sub(r'\x0c', '', s)
    lines = [l.strip() for l in s.split('\n')]
    out = []
    for l in lines:
        if l or (out and out[-1]):
            out.append(l)
    return '\n'.join(out).strip()


def harvest_word_files():
    rows = []
    word_dir = ROOT / 'inputs/seeds/lop-9/toan-9-cu/CHƯƠNG 4. HỆ THỨC LƯỢNG TRONG TAM GIÁC/FILE THAM KHẢO/2020-2021/WORD'
    for f in sorted(glob.glob(str(word_dir / '*.docx'))):
        fname = Path(f).name
        if any(k in fname for k in ['DA.', 'ĐA.', 'ggb']):
            continue

        doc = docx.Document(f)
        text = '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
        parts = re.split(r'\n(?=(?:Bài|Câu|\d+[\.:])\s+)', text)
        
        prefix = "doc-word-" + re.sub(r'[^a-zA-Z0-9]', '', fname)[:8].lower()
        idx = 0
        for p in parts:
            p_clean = clean_text(p)
            if len(p_clean) < 35 or p_clean.startswith('Dạng') or p_clean.startswith('CHƯƠNG'):
                continue

            idx += 1
            # Band & Phieu
            is_thuc_te = any(k in p_clean.lower() for k in ['tháp', 'cây', 'bóng', 'thang', 'tòa nhà', 'hải đăng', 'núi', 'máy bay', 'sông'])
            thuc_te = 'Có' if is_thuc_te else 'Không'

            if is_thuc_te:
                phieu = 'Phiếu 3 (Ứng dụng thực tế tỉ số lượng giác)'
                dang = 'Ứng dụng thực tế tỉ số lượng giác (chiều cao, khoảng cách)'
                band = 'TH'
                vai = 'TH của phiếu'
                phut = 8.0
            elif any(k in p_clean.lower() for k in ['đường cao ah', 'hệ thức giữa cạnh và đường cao', 'bh.ch', '1/ah']):
                phieu = 'Phiếu 3 (Hệ thức lượng liên quan đến đường cao)'
                dang = 'Hệ thức lượng liên quan đến đường cao trong tam giác vuông'
                band = 'TH' if 'chứng minh' not in p_clean.lower() else 'VD'
                vai = 'TH ghép VD' if band == 'VD' else 'TH của phiếu'
                phut = 10.0 if band == 'VD' else 6.0
            elif any(k in p_clean.lower() for k in ['giải tam giác', 'tính cạnh và góc', 'b = a.sin']):
                phieu = 'Phiếu 2 (Một số hệ thức về cạnh và góc trong tam giác vuông)'
                dang = 'Hệ thức giữa cạnh và góc và giải tam giác vuông'
                band = 'TH'
                vai = 'TH của phiếu'
                phut = 6.0
            else:
                phieu = 'Phiếu 1 (Tỉ số lượng giác của góc nhọn)'
                dang = 'Tỉ số lượng giác của góc nhọn'
                band = 'NB' if len(p_clean) < 120 and 'tính tỉ số' in p_clean.lower() else 'TH'
                vai = 'NB của phiếu' if band == 'NB' else 'TH của phiếu'
                phut = 3.0 if band == 'NB' else 6.0

            ma = f"{prefix}-{idx:03d}"
            rows.append({
                'de': p_clean,
                'nguon': f"Tài liệu Word chuyên đề Mathtech ({fname}), Bài {idx}",
                'band': band,
                'dang': dang,
                'uu': 'Ưu tiên 3: Tài liệu khác',
                'phieu': phieu,
                'phut': phut,
                'thuc_te': thuc_te,
                'fmt': 'Tự luận' if not p_clean.startswith('Câu') else 'Trắc nghiệm 4 lựa chọn',
                'muc_y': band,
                'bai': 'Bài 11' if 'Phiếu 1' in phieu else ('Bài 12' if 'Phiếu 2' in phieu else 'Bài 12 (bổ trợ)'),
                'note': f"Trích từ Word archive ({fname})",
                'ma': ma,
                'vai': vai,
                'de_xuat': '',
            })
    return rows


def harvest_2024_2025_pdfs():
    rows = []
    pdf_dir = ROOT / 'inputs/seeds/lop-9/toan-9-cu/CHƯƠNG 4. HỆ THỨC LƯOƠNG TRONG TAM GIÁC/FILE THAM KHẢO/2024-2025/PDF'
    # Use glob with fuzzy pattern to avoid unicode normalization
    for f in sorted(glob.glob(str(ROOT / 'inputs/seeds/lop-9/toan-9-cu/*/FILE THAM KHẢO/2024-2025/PDF/*.pdf'))):
        if 'CHƯƠNG 4' not in f and 'CHƯO' not in f:
            continue
        fname = Path(f).name
        res = subprocess.run(['pdftotext', f, '-'], stdout=subprocess.PIPE, text=True)
        txt = res.stdout
        parts = re.split(r'\n(?=(?:Bài|Ví dụ|Câu)\s+\d+[\.:])', txt)
        prefix = "mt25-" + re.sub(r'[^a-zA-Z0-9]', '', fname)[:6].lower()
        idx = 0
        for p in parts:
            p_clean = clean_text(p)
            if len(p_clean) < 35 or p_clean.startswith('LÝ THUYẾT') or p_clean.startswith('Dạng'):
                continue
            idx += 1

            is_thuc_te = any(k in p_clean.lower() for k in ['tháp', 'cây', 'bóng', 'thang', 'tòa nhà', 'hải đăng', 'núi', 'máy bay', 'sông'])
            thuc_te = 'Có' if is_thuc_te else 'Không'

            if 'Ứng dụng' in fname or is_thuc_te:
                phieu = 'Phiếu 3 (Ứng dụng thực tế tỉ số lượng giác)'
                dang = 'Ứng dụng thực tế tỉ số lượng giác (chiều cao, khoảng cách)'
                band = 'TH'
                vai = 'TH của phiếu'
                phut = 8.0
            elif 'Một số hệ thức' in fname:
                phieu = 'Phiếu 2 (Một số hệ thức về cạnh và góc trong tam giác vuông)'
                dang = 'Hệ thức giữa cạnh và góc và giải tam giác vuông'
                band = 'TH'
                vai = 'TH của phiếu'
                phut = 6.0
            elif 'Luyện tập chung' in fname:
                phieu = 'Phiếu 4 (Luyện tập chung và kiểm tra chương)'
                dang = 'Luyện tập tổng hợp hệ thức lượng'
                band = 'VD' if 'chứng minh' in p_clean.lower() else 'TH'
                vai = 'TH ghép VD' if band == 'VD' else 'TH của phiếu'
                phut = 10.0 if band == 'VD' else 6.0
            else:
                phieu = 'Phiếu 1 (Tỉ số lượng giác của góc nhọn)'
                dang = 'Tỉ số lượng giác của góc nhọn'
                band = 'NB' if 'tính tỉ số' in p_clean.lower() and len(p_clean) < 120 else 'TH'
                vai = 'NB của phiếu' if band == 'NB' else 'TH của phiếu'
                phut = 3.0 if band == 'NB' else 6.0

            ma = f"{prefix}-{idx:03d}"
            rows.append({
                'de': p_clean,
                'nguon': f"Tài liệu Mathtech 2024-2025 ({fname}), Bài {idx}",
                'band': band,
                'dang': dang,
                'uu': 'Ưu tiên 3: Tài liệu khác',
                'phieu': phieu,
                'phut': phut,
                'thuc_te': thuc_te,
                'fmt': 'Tự luận',
                'muc_y': band,
                'bai': 'Bài 11' if 'Phiếu 1' in phieu else ('Bài 12' if 'Phiếu 2' in phieu else 'Bài 12 (bổ trợ)'),
                'note': f"Mathtech 2024-2025 ({fname})",
                'ma': ma,
                'vai': vai,
                'de_xuat': '',
            })
    return rows


def harvest_exam_review_pdfs():
    rows = []
    # All review PDFs in Đề KT CK1 and Đề KT GK1
    pdf_files = (
        glob.glob(str(ROOT / 'inputs/seeds/lop-9/toan-9-cu/Đề KT CK1/*.pdf')) +
        glob.glob(str(ROOT / 'inputs/seeds/lop-9/toan-9-cu/Đề KT CK1/Đề KT GK1/*/*.pdf'))
    )
    for f in sorted(pdf_files):
        fname = Path(f).name
        res = subprocess.run(['pdftotext', f, '-'], stdout=subprocess.PIPE, text=True)
        txt = res.stdout
        parts = re.split(r'\n(?=(?:Bài|Câu)\s+\d+[\.:])', txt)
        prefix = "dc-" + re.sub(r'[^a-zA-Z0-9]', '', fname)[:6].lower()
        idx = 0
        for p in parts:
            p_clean = clean_text(p)
            if len(p_clean) < 35:
                continue
            # Must be Chapter 4 geometry
            is_c4 = any(k in p_clean.lower() for k in [
                'tỉ số lượng giác', 'tam giác vuông', 'đường cao ah', 'hệ thức lượng',
                'sin', 'cos', 'tan', 'cot', 'chiều cao', 'bóng', 'hải đăng', 'máy bay'
            ])
            # Exclude purely circle
            if 'tiếp tuyến' in p_clean.lower() and 'đường tròn' in p_clean.lower() and not any(k in p_clean.lower() for k in ['hệ thức lượng', 'sin', 'cos', 'tan', 'cot', 'chiều cao', 'bóng']):
                is_c4 = False

            if not is_c4:
                continue

            idx += 1
            is_thuc_te = any(k in p_clean.lower() for k in ['tháp', 'cây', 'bóng', 'thang', 'tòa nhà', 'hải đăng', 'núi', 'máy bay', 'sông', 'khu vườn'])
            thuc_te = 'Có' if is_thuc_te else 'Không'

            if is_thuc_te:
                phieu = 'Phiếu 3 (Ứng dụng thực tế tỉ số lượng giác)'
                dang = 'Ứng dụng thực tế tỉ số lượng giác (chiều cao, khoảng cách)'
                band = 'TH'
                vai = 'TH của phiếu'
                phut = 8.0
            elif any(k in p_clean.lower() for k in ['đường cao ah', 'hệ thức lượng', 'bh.ch', '1/ah']):
                phieu = 'Phiếu 3 (Hệ thức lượng liên quan đến đường cao)'
                dang = 'Hệ thức lượng liên quan đến đường cao trong tam giác vuông'
                band = 'TH' if 'chứng minh' not in p_clean.lower() else 'VD'
                vai = 'TH ghép VD' if band == 'VD' else 'TH của phiếu'
                phut = 10.0 if band == 'VD' else 6.0
            elif any(k in p_clean.lower() for k in ['giải tam giác', 'tính cạnh và góc']):
                phieu = 'Phiếu 2 (Một số hệ thức về cạnh và góc trong tam giác vuông)'
                dang = 'Hệ thức giữa cạnh và góc và giải tam giác vuông'
                band = 'TH'
                vai = 'TH của phiếu'
                phut = 6.0
            else:
                phieu = 'Phiếu 1 (Tỉ số lượng giác của góc nhọn)'
                dang = 'Tỉ số lượng giác của góc nhọn'
                band = 'NB' if 'tính tỉ số' in p_clean.lower() and len(p_clean) < 120 else 'TH'
                vai = 'NB của phiếu' if band == 'NB' else 'TH của phiếu'
                phut = 3.0 if band == 'NB' else 6.0

            ma = f"{prefix}-{idx:03d}"
            rows.append({
                'de': p_clean,
                'nguon': f"Đề cương / Đề thi {fname}, Bài {idx}",
                'band': band,
                'dang': dang,
                'uu': 'Ưu tiên 1: Đề thi thật',
                'phieu': phieu,
                'phut': phut,
                'thuc_te': thuc_te,
                'fmt': 'Tự luận' if not p_clean.startswith('Câu') else 'Trắc nghiệm 4 lựa chọn',
                'muc_y': band,
                'bai': 'Đề ôn tập định kì',
                'note': f"Đề cương ôn tập ({fname})",
                'ma': ma,
                'vai': vai,
                'de_xuat': '',
            })
    return rows

if __name__ == '__main__':
    w_rows = harvest_word_files()
    pdf_rows = harvest_2024_2025_pdfs()
    ex_rows = harvest_exam_review_pdfs()
    print(f"Word files: {len(w_rows)}")
    print(f"2024-2025 PDFs: {len(pdf_rows)}")
    print(f"Exam review PDFs: {len(ex_rows)}")
    print(f"Total new: {len(w_rows) + len(pdf_rows) + len(ex_rows)}")
