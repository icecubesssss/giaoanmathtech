"""Cấu trúc 5 chặng + bộ lint thị giác (deterministic, không LLM)."""
import json
from pathlib import Path

import pytest

from src.schema import LessonPackage
from src.validators.schema_validator import validate_lesson_structure
from src.validators.visual_linter import wrap_long_math, scan_build_log

SEED_JSON = Path("inputs/seeds/lop-9/dai-so/tuan09-bat-dang-thuc/phieu-a-bdt-tinh-chat-va-so-sanh.json")


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


# --- Cảnh báo ký tự đặc biệt thô ('%' '#' mọi nơi, '&' ngoài $...$) — chống lỗi vỡ build ---
from src.validators.visual_linter import find_presentation_warnings


def _mk_lesson(**over):
    base = {
        "slug": "x", "title": "T", "eyebrow": "E", "grade_label": "G",
        "stages": [
            {"kind": "review", "number": 1, "title": "r", "blocks": [{"type": "para", "text": "ok"}]},
            {"kind": "concept", "number": 2, "title": "c", "blocks": [{"type": "math", "latex": "x=1"}]},
            {"kind": "practice1", "number": 3, "title": "p1", "blocks": [{"type": "problem", "label": "Bài 1.", "statement": "$x=1$"}]},
            {"kind": "practice2", "number": 4, "title": "p2", "blocks": [{"type": "problem", "label": "Bài 2.", "statement": "$x=2$"}]},
            {"kind": "reflection", "number": 5, "title": "tk", "blocks": [{"type": "problem", "label": "Bài 3.", "tier": "btvn", "statement": "$x=3$"}]},
        ],
    }
    base.update(over)
    return LessonPackage.model_validate(base)


def test_raw_percent_in_teacher_note_warned():
    """Regression: '%' thô trong teacher_note (làm vỡ guide.pdf) phải bị cảnh báo."""
    les = _mk_lesson()
    les.stages[4].teacher_note = "ôn dạng % phần trăm"
    ws = find_presentation_warnings(les)
    assert any("teacher_note" in w and "%" in w for w in ws)


def test_raw_amp_outside_math_warned_but_inside_math_ok():
    les = _mk_lesson()
    les.stages[0].blocks[0].text = "A & B ngoài toán"   # '&' thô ngoài $...$ -> cảnh báo
    assert any("&" in w for w in find_presentation_warnings(les))
    les2 = _mk_lesson()
    les2.stages[0].blocks[0].text = "Hệ $\\begin{aligned} x &= 1 \\end{aligned}$ và PT \\& kia"  # '&' trong toán + '\&' escaped -> sạch
    assert not any("&" in w for w in find_presentation_warnings(les2))


def test_scaffolding_workrate_without_moi_warned():
    """'làm chung – làm riêng' mà thiếu 'ví dụ mồi' -> nhắc thêm scaffolding."""
    les = _mk_lesson()
    les.stages[2].blocks[0].statement = "Hai đội làm chung xong trong 18 ngày; đội I làm riêng bao lâu?"
    assert any("làm chung" in w for w in find_presentation_warnings(les))


def test_scaffolding_ok_when_moi_present():
    les = _mk_lesson()
    les.stages[0].blocks[0].text = "Ví dụ mồi — pizza dẫn vào năng suất."
    les.stages[2].blocks[0].statement = "Hai đội làm chung xong trong 18 ngày."
    assert not any("làm chung" in w for w in find_presentation_warnings(les))
