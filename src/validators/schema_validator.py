"""Kiểm toàn vẹn cấu trúc GÓI BÀI ngoài Pydantic.

Pydantic chặn sai kiểu/thiếu trường; lớp này chặn sai LOGIC SƯ PHẠM:
đủ và đúng thứ tự 5 chặng (review→concept→practice1→practice2→reflection), số chặng
1..5 không trùng, slug không dấu/không khoảng trắng, mỗi chặng có nội dung.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from src.schema import LessonPackage

__all__ = ["SchemaReport", "validate_lesson_structure"]

_EXPECTED_ORDER = ["review", "concept", "practice1", "practice2", "reflection"]
_SLUG_RX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class SchemaReport:
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_lesson_structure(lesson: LessonPackage) -> SchemaReport:
    errors: list[str] = []

    if not _SLUG_RX.match(lesson.slug):
        errors.append(f"slug '{lesson.slug}' phải là kebab-case không dấu (vd 'bdt-xet-hieu').")

    kinds = [s.kind for s in lesson.stages]
    if kinds != _EXPECTED_ORDER:
        errors.append(
            f"Thứ tự/đủ 5 chặng sai: nhận {kinds}, cần {_EXPECTED_ORDER}."
        )

    numbers = [s.number for s in lesson.stages]
    if sorted(numbers) != list(range(1, len(lesson.stages) + 1)):
        errors.append(f"Số chặng phải 1..{len(lesson.stages)} không trùng, nhận {numbers}.")

    for s in lesson.stages:
        if not s.blocks:
            errors.append(f"Chặng '{s.kind}' rỗng — không có block nội dung nào.")
        if not s.title.strip():
            errors.append(f"Chặng '{s.kind}' thiếu tiêu đề.")

    return SchemaReport(errors=errors)
