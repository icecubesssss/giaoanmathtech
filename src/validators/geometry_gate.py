"""Cổng hình học — SymPy YẾU với hình học tổng hợp nên KHÔNG được "duyệt mù".

Bài nào thuộc nhánh hình học (mã topic bắt đầu bằng 'hinh' / 'geo', hoặc statement
chứa từ khóa hình) thì BẮT BUỘC mang nhãn `human_verified=True` mới được dùng. Trọng
tài đại số (sympy_solver) không có quyền tự nhận đã kiểm bài hình.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from src.schema import MathProblem

__all__ = ["is_geometry", "GeometryViolation", "check_geometry_problems"]

_GEO_TOPIC = re.compile(r"^(hinh|geo)", re.IGNORECASE)
_GEO_WORDS = re.compile(
    r"tam giác|đường tròn|góc|tiếp tuyến|đường cao|trung tuyến|"
    r"hình thang|tứ giác|đồng dạng|vuông góc|song song|bán kính|chu vi|diện tích",
    re.IGNORECASE,
)


def is_geometry(problem: MathProblem) -> bool:
    return bool(_GEO_TOPIC.search(problem.topic) or _GEO_WORDS.search(problem.statement))


@dataclass
class GeometryViolation:
    topic: str
    reason: str


def check_geometry_problems(problems: list[MathProblem]) -> list[GeometryViolation]:
    """Trả về danh sách vi phạm: bài hình chưa có nhãn human_verified (rỗng = đạt)."""
    violations: list[GeometryViolation] = []
    for p in problems:
        if is_geometry(p) and not p.human_verified:
            violations.append(
                GeometryViolation(
                    topic=p.topic,
                    reason="Bài hình học CHƯA có human_verified=True — SymPy không được duyệt mù.",
                )
            )
    return violations
