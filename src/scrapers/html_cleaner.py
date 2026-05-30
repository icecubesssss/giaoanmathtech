"""Lọc sạch mã rác quảng cáo, định dạng script, style từ nội dung HTML cào được.

Giữ lại khung cấu trúc văn bản sạch phục vụ bóc tách đề toán.
"""
from __future__ import annotations

from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:
    """Loại bỏ các thẻ HTML rác và trả về text sạch giữ lại cấu trúc."""
    if not raw_html:
        return ""
        
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Loại bỏ các thẻ không liên quan đến nội dung toán học
    for s in soup(["script", "style", "nav", "header", "footer", "iframe", "noscript", "aside"]):
        s.decompose()
        
    # Loại bỏ quảng cáo phổ biến
    for ad in soup.find_all(class_=lambda c: c and any(kw in c.lower() for kw in ["ads", "advertisement", "banner", "sidebar", "social"])):
        ad.decompose()
        
    # Trích xuất văn bản sạch nhưng giữ khoảng cách dòng tương đối
    text = soup.get_text(separator="\n")
    
    # Loại bỏ khoảng trắng thừa
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)
