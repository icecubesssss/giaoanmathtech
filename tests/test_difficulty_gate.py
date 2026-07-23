"""Khóa chống 'đần' — Hook giảng vỡ lòng / Boss rỗng phải bị từ chối."""
import json
from pathlib import Path

import pytest

from src.schema import LessonPackage
from src.schema.lesson_package import ParaBlock
from src.validators.difficulty_gate import check_difficulty, load_profile

SEED_JSON = Path("inputs/seeds/lop-9/dai-so/lop-b/tuan09-bat-dang-thuc-va-giai-bpt/phieu-a-bdt-tinh-chat-va-so-sanh.json")


@pytest.fixture
def seed_lesson() -> LessonPackage:
    data = json.loads(SEED_JSON.read_text(encoding="utf-8"))
    return LessonPackage.model_validate(data)


def test_seed_passes_difficulty_gate(seed_lesson):
    """Gói mẫu chuẩn (so sánh 2024/2023 vs 2025/2024 + chứng minh bậc 2) phải qua."""
    rep = check_difficulty(seed_lesson)
    assert rep.passed, rep.reasons


def test_empty_practice2_rejected(seed_lesson):
    """Luyện tập 2 chỉ có chữ giảng suông, không công thức/đề — phải bị chặn."""
    seed_lesson.stages[3].blocks = [
        ParaBlock(type="para", text="Hôm nay khó lắm các em ơi.")
    ]
    rep = check_difficulty(seed_lesson)
    assert not rep.passed
    assert any("luyện tập 2" in r.lower() or "luyen tap 2" in r.lower() or "trần" in r.lower() for r in rep.reasons)


def test_profile_loads():
    prof = load_profile()
    assert prof.hook_forbidden_patterns, "Profile phải có danh sách mẫu Hook cấm."
    assert prof.boss_must_hit_ceiling is True
