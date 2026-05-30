"""Agent săn lùng đề toán tương đồng trong ngân hàng đề thực tế.

Lọc các bài toán từ `verified_scraped_bank/` khớp với mục tiêu kiến thức (topic)
và thang độ khó (difficulty) mong muốn, không tự bịa đề toán mới.
"""
from __future__ import annotations

from pathlib import Path
from src.schema.base_schema import MathProblem
from src.scrapers.offline_worker import load_bank, BANK_DIR


def scout_problems(topic: str, min_diff: int, max_diff: int) -> list[MathProblem]:
    """Tìm kiếm các đề toán có sẵn từ ngân hàng khớp với chủ đề và độ khó."""
    algebra_path = BANK_DIR / "algebra.json"
    geometry_path = BANK_DIR / "geometry.json"
    
    # Gom tất cả các đề từ ngân hàng
    all_problems: list[MathProblem] = []
    if "hinh_hoc" in topic:
        all_problems.extend(load_bank(geometry_path))
    else:
        all_problems.extend(load_bank(algebra_path))
        
    # Lọc theo tiêu chí chặt chẽ
    matched = [
        p for p in all_problems
        if p.topic == topic and min_diff <= p.difficulty <= max_diff
    ]
    
    return matched
