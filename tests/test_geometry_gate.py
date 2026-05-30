"""Cổng hình học: bài hình BẮT BUỘC human_verified, đại số thì không cần."""
from src.schema import MathProblem
from src.validators.geometry_gate import check_geometry_problems, is_geometry


def _mk(topic: str, statement: str, human_verified: bool = False) -> MathProblem:
    return MathProblem(
        source="seed", topic=topic, difficulty=5,
        statement=statement, solution="(người giải)", answer="",
        human_verified=human_verified,
    )


def test_geometry_detected_by_topic():
    assert is_geometry(_mk("hinh.tam_giac", "Cho tam giác ABC..."))


def test_geometry_detected_by_keywords():
    assert is_geometry(_mk("bdt.misc", "Cho tam giác ABC có đường cao AH."))


def test_geometry_without_human_verified_rejected():
    problems = [_mk("hinh.duong_tron", "Cho đường tròn (O)...", human_verified=False)]
    vs = check_geometry_problems(problems)
    assert len(vs) == 1 and "human_verified" in vs[0].reason


def test_geometry_with_human_verified_passes():
    problems = [_mk("hinh.duong_tron", "Cho đường tròn (O)...", human_verified=True)]
    assert check_geometry_problems(problems) == []


def test_algebra_problem_not_required_to_be_human_verified():
    problems = [_mk("bdt.xet_hieu", "Chứng minh a^2+b^2 >= 2ab.", human_verified=False)]
    assert check_geometry_problems(problems) == []
