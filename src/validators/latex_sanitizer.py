"""Chốt bảo mật LaTeX — quét và TỪ CHỐI mọi lệnh có thể thực thi mã / đọc-ghi file.

Triết lý: danh sách CẤM tường minh (deny-list) cho các lệnh nguy hiểm đã biết, cộng
một lớp chặn heuristic cho \\def lạ và họ \\write/\\open/\\catcode. Hàm `sanitize`
trả lại chuỗi NGUYÊN VẸN nếu sạch (không chỉnh sửa thầm), hoặc ném `UnsafeLatexError`
nêu rõ lệnh vi phạm — để tầng trên ghi log và trả bài về `weave`, không "im lặng vá".

KHÔNG bao giờ là nơi duy nhất chống mã độc: latex_builder cũng TẮT -shell-escape.
Đây là phòng tuyến thứ nhất (nội dung), builder là phòng tuyến thứ hai (engine).
"""
from __future__ import annotations

import re

__all__ = ["sanitize", "find_unsafe", "UnsafeLatexError"]


class UnsafeLatexError(ValueError):
    """Phát hiện lệnh LaTeX nguy hiểm trong nội dung — từ chối, không tự sửa."""


# Mỗi mục: (tên đọc được, regex bắt lệnh). \b sau tên lệnh chặn khớp nhầm
# (vd \input vs \inputencoding) nhưng vẫn bắt \input{...} và \input ở cuối.
_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("\\write18 (shell escape)", re.compile(r"\\write\s*18\b")),
    ("\\write (ghi file)",        re.compile(r"\\write(?![a-zA-Z])")),
    ("\\immediate",               re.compile(r"\\immediate\b")),
    ("\\openout / \\openin",      re.compile(r"\\open(?:out|in)(?![a-zA-Z])")),
    ("\\read",                    re.compile(r"\\read(?:line)?(?![a-zA-Z])")),
    ("\\input",                   re.compile(r"\\input(?![a-zA-Z])")),
    ("\\include / \\includeonly",  re.compile(r"\\include(?:only)?(?![a-zA-Z])")),
    ("\\catcode",                 re.compile(r"\\catcode\b")),
    ("\\def (định nghĩa lệnh)",    re.compile(r"\\(?:e|g|x|long|outer)?def(?![a-zA-Z])")),
    ("\\let",                     re.compile(r"\\let(?![a-zA-Z])")),
    ("\\csname (dựng lệnh động)", re.compile(r"\\csname\b")),
    ("\\special",                 re.compile(r"\\special\b")),
    ("\\usepackage (nạp gói)",     re.compile(r"\\usepackage\b")),
    ("\\directlua / \\latelua",    re.compile(r"\\(?:directlua|latelua)\b")),
    ("\\ShellEscape",             re.compile(r"\\ShellEscape\b")),
    ("\\loop / \\repeat",          re.compile(r"\\(?:loop|repeat)(?![a-zA-Z])")),
]


def find_unsafe(text: str) -> list[str]:
    """Trả về danh sách tên lệnh nguy hiểm tìm thấy (rỗng nếu sạch)."""
    return [name for name, rx in _RULES if rx.search(text)]


def sanitize(text: str) -> str:
    """Trả lại `text` y nguyên nếu an toàn; ném UnsafeLatexError nếu phát hiện vi phạm."""
    hits = find_unsafe(text)
    if hits:
        raise UnsafeLatexError(
            "Nội dung chứa lệnh LaTeX bị cấm: " + ", ".join(hits)
        )
    return text
