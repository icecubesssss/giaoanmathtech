from src.schema import LessonPackage
from src.validators.answer_gate import check_answers


def _lesson(check: dict) -> LessonPackage:
    """Gói bài tối thiểu 1 chặng, 1 ProblemBlock mang `check` để test cổng đáp án."""
    return LessonPackage.model_validate({
        "slug": "t", "title": "T",
        "stages": [{
            "kind": "practice1", "number": 3, "title": "Luyện",
            "blocks": [{"type": "problem", "label": "Bài 1.",
                        "statement": "x", "check": check}],
        }],
    })


def test_solveset_ok():
    fails, incon = check_answers(_lesson(
        {"kind": "solveset", "equation": "x**2 - 5*x + 6 = 0", "answer": [2, 3]}))
    assert fails == [] and incon == []


def test_solveset_fail():
    fails, _ = check_answers(_lesson(
        {"kind": "solveset", "equation": "x**2 - 5*x + 6 = 0", "answer": [2, 5]}))
    assert len(fails) == 1


def test_identity_ok():
    fails, _ = check_answers(_lesson(
        {"kind": "identity", "lhs": "(a+b)^2", "rhs": "a^2 + 2*a*b + b^2"}))
    assert fails == []


def test_identity_fail():
    fails, _ = check_answers(_lesson(
        {"kind": "identity", "lhs": "(a+b)^2", "rhs": "a^2 + b^2"}))
    assert len(fails) == 1


def test_nonneg_ok():
    fails, _ = check_answers(_lesson(
        {"kind": "nonneg", "expr": "a**2 + b**2 - 2*a*b", "symbols": ["a", "b"]}))
    assert fails == []


def test_no_check_is_skipped():
    lesson = LessonPackage.model_validate({
        "slug": "t", "title": "T",
        "stages": [{"kind": "practice1", "number": 3, "title": "L",
                    "blocks": [{"type": "problem", "label": "B1", "statement": "x"}]}],
    })
    assert check_answers(lesson) == ([], [])
