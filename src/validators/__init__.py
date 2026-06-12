"""Tầng trọng tài — kiểm thử KHÔNG ba phải trước khi cho compile.

Mỗi module một việc, có thể gọi lẻ; CLI `validate` gom các kiểm tra áp dụng được
cho LessonPackage (sanitizer + schema + difficulty), còn `sympy_solver` /
`geometry_gate` dùng cho MathProblem trong ngân hàng đề (S4).
"""
from .latex_sanitizer import sanitize, find_unsafe, UnsafeLatexError
from .schema_validator import validate_lesson_structure, SchemaReport
from .difficulty_gate import check_difficulty, check_ramp, load_profile, DifficultyProfile, DifficultyReject
from .geometry_gate import check_geometry_problems, is_geometry, GeometryViolation
from .visual_linter import wrap_long_math, scan_build_log, BuildLogReport, find_presentation_warnings
from .answer_gate import check_answers
from .duration_gate import check_duration
from . import sympy_solver

__all__ = [
    "sanitize", "find_unsafe", "UnsafeLatexError",
    "validate_lesson_structure", "SchemaReport",
    "check_difficulty", "check_ramp", "load_profile", "DifficultyProfile", "DifficultyReject",
    "check_geometry_problems", "is_geometry", "GeometryViolation",
    "wrap_long_math", "scan_build_log", "BuildLogReport", "find_presentation_warnings",
    "check_answers",
    "check_duration",
    "sympy_solver",
]
