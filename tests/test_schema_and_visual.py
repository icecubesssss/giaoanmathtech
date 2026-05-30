"""Cấu trúc 5 chặng + bộ lint thị giác (deterministic, không LLM)."""
import json
from pathlib import Path

import pytest

from src.schema import LessonPackage
from src.validators.schema_validator import validate_lesson_structure
from src.validators.visual_linter import wrap_long_math, scan_build_log

SEED_JSON = Path("inputs/seeds/lop-9/dai-so/tuan09-bat-dang-thuc/bdt-tinh-chat-va-so-sanh.json")


@pytest.fixture
def seed_lesson() -> LessonPackage:
    return LessonPackage.model_validate(json.loads(SEED_JSON.read_text(encoding="utf-8")))


def test_seed_lesson_structure_ok(seed_lesson):
    assert validate_lesson_structure(seed_lesson).ok


def test_wrong_stage_order_detected(seed_lesson):
    seed_lesson.stages[0], seed_lesson.stages[1] = seed_lesson.stages[1], seed_lesson.stages[0]
    rep = validate_lesson_structure(seed_lesson)
    assert not rep.ok
    assert any("Thứ tự" in e for e in rep.errors)


def test_slug_with_space_rejected(seed_lesson):
    seed_lesson.slug = "bat dang thuc"
    rep = validate_lesson_structure(seed_lesson)
    assert not rep.ok


def test_wrap_long_math_inserts_aligned():
    s = r"a^2 + b^2 + c^2 \ge ab + bc + ca \quad\text{với mọi } a,b,c \in \mathbb{R}"
    out = wrap_long_math(s, max_len=40)
    assert "aligned" in out and "\\\\" in out


def test_wrap_long_math_keeps_short_intact():
    s = r"a^2 + b^2 \ge 2ab"
    assert wrap_long_math(s, max_len=40) == s


def test_scan_log_catches_errors_and_warnings():
    log = """
This is XeTeX, Version 3.14
! Undefined control sequence.
Overfull \\hbox (12.3pt too wide) in paragraph at lines 5--6
Output written on out.pdf
"""
    rep = scan_build_log(log)
    assert rep.errors and rep.warnings
    assert not rep.clean
