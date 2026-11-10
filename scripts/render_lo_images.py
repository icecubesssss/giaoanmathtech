#!/usr/bin/env python3
"""RENDER ẢNH TỪ PDF CHO MỘT LÔ ĐỀ THI LỚP 8."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def render_batch(lo_name: str) -> None:
    cfg_path = ROOT / 'config' / 'chia-lo-lop-8.json'
    if not cfg_path.exists():
        print(f"Error: {cfg_path} does not exist. Run scripts/chia_lo_lop8.py first.")
        return
        
    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
        
    if lo_name not in cfg:
        print(f"Error: Batch '{lo_name}' not found in {cfg_path}. Available batches: {list(cfg.keys())}")
        return
        
    items = cfg[lo_name]
    out_dir = ROOT / 'scratch' / 'lop8_images' / lo_name
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Rendering images for {lo_name} ({len(items)} exams) to {out_dir.relative_to(ROOT)}...")
    
    total_rendered = 0
    for idx, it in enumerate(items, 1):
        pdf_path = ROOT / it['pdf_file']
        if not pdf_path.exists():
            print(f"  [{idx}/{len(items)}] WARNING: PDF not found: {pdf_path}")
            continue
            
        exam_id = it['id']
        pages = it['trang_list']
        print(f"  [{idx}/{len(items)}] {exam_id} ({len(pages)} pages: {pages})...", end=" ")
        
        for p in pages:
            prefix = out_dir / f"{exam_id}_p{p}"
            # Check if image already rendered
            png_check = out_dir / f"{exam_id}_p{p}-1.png"
            if not png_check.exists():
                cmd = ["pdftoppm", "-r", "150", "-png", "-f", str(p), "-l", str(p), str(pdf_path), str(prefix)]
                subprocess.run(cmd, capture_output=True, check=True)
            total_rendered += 1
        print("OK")
        
    print(f"Finished rendering {total_rendered} pages for {lo_name}.")

def main():
    parser = argparse.ArgumentParser(description="Render PDF images for a batch")
    parser.add_argument("--lo", default="Lo_01_CK1", help="Batch name (e.g. Lo_01_CK1)")
    args = parser.parse_args()
    render_batch(args.lo)

if __name__ == '__main__':
    main()

