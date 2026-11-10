#!/usr/bin/env python3
"""LẬP KẾ HOẠCH CHIA LÔ QUÉT VÀ SOÁT ĐỀ LỚP 8 TỪ ẢNH PDF GỐC.

Chia 190 đề thi thành 14 lô (mỗi lô 13-14 đề, ~220 câu, ~25 trang PDF):
  - Lô 01..04: Cuối kì 1 (CK1) — 55 đề
  - Lô 05..08: Giữa kì 1 (GK1) — 56 đề
  - Lô 09..11: Giữa kì 2 (GK2) — 40 đề
  - Lô 12..14: Cuối kì 2 (CK2) — 39 đề

Sinh ra:
  - config/chia-lo-lop-8.json
  - outputs/ngan-hang-sheet/lop-8/viec/*.md (mẫu prompt cho từng subagent)
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main():
    files = sorted(glob.glob(str(ROOT / 'inputs/refs/de-thi/lop-8/exams/*.json')))
    print(f"Loaded {len(files)} exam files.")
    
    by_ky = {'CK1': [], 'GK1': [], 'GK2': [], 'CK2': []}
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            d = json.load(fp)
        xx = d.get('xuat_xu', {})
        ky = xx.get('ky', 'Other')
        cau = d.get('cau', [])
        pages = sorted(list({c.get('trang', 1) for c in cau}))
        doc_anh_cnt = sum(1 for c in cau if c.get('can_doc_anh', False))
        
        info = {
            'id': os.path.basename(f).replace('.json', ''),
            'json_file': str(Path(f).relative_to(ROOT)),
            'pdf_file': xx.get('nguon', ''),
            'truong': xx.get('truong', ''),
            'nam': xx.get('nam', ''),
            'ky': ky,
            'so_cau': len(cau),
            'so_trang_de': len(pages),
            'trang_list': pages,
            'can_doc_anh': doc_anh_cnt
        }
        if ky in by_ky:
            by_ky[ky].append(info)
        else:
            by_ky.setdefault(ky, []).append(info)

    def chunk_list(lst, n_chunks):
        k, m = divmod(len(lst), n_chunks)
        return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n_chunks)]

    lo_dict = {}
    lo_idx = 1

    # CK1: 4 lô
    for sub in chunk_list(by_ky['CK1'], 4):
        lo_dict[f'Lo_{lo_idx:02d}_CK1'] = sub
        lo_idx += 1

    # GK1: 4 lô
    for sub in chunk_list(by_ky['GK1'], 4):
        lo_dict[f'Lo_{lo_idx:02d}_GK1'] = sub
        lo_idx += 1

    # GK2: 3 lô
    for sub in chunk_list(by_ky['GK2'], 3):
        lo_dict[f'Lo_{lo_idx:02d}_GK2'] = sub
        lo_idx += 1

    # CK2: 3 lô
    for sub in chunk_list(by_ky['CK2'], 3):
        lo_dict[f'Lo_{lo_idx:02d}_CK2'] = sub
        lo_idx += 1

    # Lưu config JSON
    cfg_path = ROOT / 'config' / 'chia-lo-lop-8.json'
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cfg_path, 'w', encoding='utf-8') as fp:
        json.dump(lo_dict, fp, ensure_ascii=False, indent=2)
    print(f"Saved config to {cfg_path}")

    # Sinh prompt công việc .md cho từng lô
    out_dir = ROOT / 'outputs' / 'ngan-hang-sheet' / 'lop-8' / 'viec'
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for name, items in lo_dict.items():
        md_file = out_dir / f"{name}.md"
        lines = [
            f"# NHIỆM VỤ SOÁT ĐỀ TỪ ẢNH PDF: {name}",
            "",
            f"- **Số lượng đề:** {len(items)} đề",
            f"- **Tổng số câu hỏi:** {sum(x['so_cau'] for x in items)} câu",
            f"- **Số câu cắm cờ OCR lỗi (`can_doc_anh`):** {sum(x['can_doc_anh'] for x in items)} câu",
            f"- **Thư mục ảnh cắt:** `scratch/lop8_images/{name}/`",
            "",
            "## Danh sách file đề trong lô:",
            ""
        ]
        for it in items:
            lines.append(f"### {it['id']}")
            lines.append(f"- **Trường:** {it['truong']} (Năm: {it['nam']}, Kỳ: {it['ky']})")
            lines.append(f"- **PDF gốc:** `{it['pdf_file']}`")
            lines.append(f"- **JSON đề:** `{it['json_file']}`")
            lines.append(f"- **Trang chứa câu hỏi:** {it['trang_list']} ({it['so_trang_de']} trang)")
            lines.append(f"- **Số câu:** {it['so_cau']} (cần soát: {it['can_doc_anh']} câu)")
            lines.append("")
            
        lines.append("## Hướng dẫn thực hiện:")
        lines.append("1. Chạy lệnh cắt ảnh: `python scripts/render_lo_images.py --lo " + name + "`")
        lines.append("2. Đọc trực tiếp các file ảnh PNG đã cắt trong `scratch/lop8_images/" + name + "/`.")
        lines.append("3. Đối chiếu từng câu hỏi trong file JSON tương ứng:")
        lines.append("   - Chuyển toàn bộ biểu thức toán sang LaTeX chuẩn bọc trong `$ ... $` (phân số `\\dfrac{a}{b}`, số mũ `x^n`, căn thức `\\sqrt{...}`).")
        lines.append("   - Khắc phục các lỗi OCR: mất dấu âm, dính chữ, rác ký tự.")
        lines.append("   - Cập nhật trường `de_latex` và cập nhật trường `de` thành đề bài sạch.")
        lines.append("   - Đặt `can_doc_anh: false` và `da_duyet: true` cho câu đã soát.")
        lines.append("4. Lưu lại file JSON đề.")
        
        md_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        
    print(f"Generated 14 job files in {out_dir}")

if __name__ == '__main__':
    main()

