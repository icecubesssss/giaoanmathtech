"""Phân tích và quy chuẩn các công thức toán MathJax / KaTeX trên trang web về chuẩn LaTeX sạch.

Chuyển đổi:
  - <script type="math/tex">...</script>          -> $...$
  - <script type="math/tex; mode=display">...</script> -> $$...$$
  - Các ký tự phân cách \\( ... \\) và \\[ ... \\] -> $...$ và $$...$$
"""
from __future__ import annotations

import re
from bs4 import BeautifulSoup


def parse_mathjax(html_content: str) -> str:
    """Quét và chuyển đổi các thẻ MathJax/KaTeX trong HTML thành cú pháp LaTeX tiêu chuẩn."""
    if not html_content:
        return ""
        
    # Thay thế các dấu phân cách trước khi đưa vào BeautifulSoup
    html_content = re.sub(r"\\\\\(", " $ ", html_content)
    html_content = re.sub(r"\\\\\)", " $ ", html_content)
    html_content = re.sub(r"\\\\\[", " $$ ", html_content)
    html_content = re.sub(r"\\\\\]", " $$ ", html_content)
    
    html_content = re.sub(r"\\\((.*?)\\\)", r" $\1$ ", html_content)
    html_content = re.sub(r"\\\[(.*?)\\\]", r" $$\1$$ ", html_content)
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Chuyển đổi mọi thẻ <script type="math/tex">
    for script in soup.find_all("script"):
        t = script.get("type", "") or ""
        # Thầy cô đôi khi ghi type="math/tex"; mode=display không đúng chuẩn XML/HTML
        # BeautifulSoup có thể phân tách thành script attribute hoặc giữ nguyên trong text
        is_display = "mode=display" in t or "mode=display" in str(script) or script.get("mode") == "display"
        
        if "math/tex" in t or "math/tex" in str(script):
            content = script.string or ""
            if is_display:
                script.replace_with(f" $${content.strip()}$$ ")
            else:
                script.replace_with(f" ${content.strip()}$ ")
                
    # 2. Gom các thẻ có class 'katex-html' hoặc tương tự
    for annotation in soup.find_all("annotation", encoding="application/x-tex"):
        tex = annotation.get_text().strip()
        katex_parent = annotation.find_parent(class_="katex")
        if katex_parent:
            katex_parent.replace_with(f" ${tex}$ ")
        else:
            annotation.replace_with(f" ${tex}$ ")
            
    return str(soup)
