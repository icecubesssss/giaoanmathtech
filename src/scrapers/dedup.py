"""Khử trùng lặp đề toán trong ngân hàng dữ liệu.

Sử dụng phương pháp chuẩn hóa cú pháp LaTeX và so sánh tập hợp/danh sách từ khóa sắp xếp
để phát hiện trùng lặp một cách chính xác mà không phụ thuộc vào thứ tự diễn đạt.
"""
from __future__ import annotations

import re
from src.schema.base_schema import MathProblem


def normalize_latex(text: str) -> str:
    """Chuẩn hóa chuỗi văn bản toán học để đối sánh trùng lặp (không phụ thuộc thứ tự)."""
    if not text:
        return ""
    # Chuyển chữ thường
    text = text.lower()
    
    # Loại bỏ các từ trang trí tiếng Việt phổ biến
    ornaments = ["chứng minh rằng", "chứng minh", "hãy", "tính", "giải", "cho", "tìm"]
    for orn in ornaments:
        text = text.replace(orn, "")
        
    # Loại bỏ các dấu ngoặc và định dạng LaTeX
    text = text.replace(r"\left", "").replace(r"\right", "")
    text = text.replace("{", "").replace("}", "").replace("[", "").replace("]", "")
    text = text.replace("(", "").replace(")", "").replace("$", "")
    text = text.replace(";", "").replace(".", "").replace(",", "")
    
    # Tách chuỗi thành các từ/token độc lập
    tokens = re.findall(r"\w+|[+\-*/>=<]+", text)
    # Loại bỏ các token rỗng hoặc quá ngắn không mang thông tin toán học
    tokens = [t.strip() for t in tokens if t.strip()]
    # Sắp xếp để độc lập với thứ tự diễn đạt
    tokens.sort()
    
    return "".join(tokens)


def are_similar(statement_a: str, statement_b: str) -> bool:
    """So sánh hai đề bài xem có trùng lặp không."""
    return normalize_latex(statement_a) == normalize_latex(statement_b)


def filter_duplicates(problems: list[MathProblem]) -> list[MathProblem]:
    """Lọc bỏ các đề toán trùng lặp trong một danh sách."""
    seen: set[str] = set()
    unique_problems: list[MathProblem] = []
    
    for p in problems:
        norm = normalize_latex(p.statement)
        if norm not in seen:
            seen.add(norm)
            unique_problems.append(p)
            
    return unique_problems
