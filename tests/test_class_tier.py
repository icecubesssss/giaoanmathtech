"""Tiền tố tầng lớp `[A]/[B]/[C]/[X]` đứng TRƯỚC `tuanNN` không được phá
việc đọc số tuần / chủ đề (hệ đếm tuần) và phải suy ra đúng tầng lớp."""
import pytest

from src.main import _class_tier, _strip_tier, _topic_slug, _week_nums
from src.schema import LessonPackage


@pytest.mark.parametrize("name,weeks,topic", [
    ("[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an", [10, 11], "bat-phuong-trinh-bac-nhat-mot-an"),
    ("tuan10-11-bat-phuong-trinh-bac-nhat-mot-an", [10, 11], "bat-phuong-trinh-bac-nhat-mot-an"),
    ("[X]tuan27-ham-so-y-ax2", [27], "ham-so-y-ax2"),
    ("tuan05-pt-va-he-pt-bac-nhat-hai-an", [5], "pt-va-he-pt-bac-nhat-hai-an"),
])
def test_week_and_topic_ignore_tier_prefix(name, weeks, topic):
    assert _week_nums(name) == weeks
    assert _topic_slug(name) == topic


@pytest.mark.parametrize("name,tier", [
    ("[C]tuan10-11-x", "C"),
    ("[A]tuan01-02-on-tap", "A"),
    ("[X]tuan27-ham-so", "X"),
    ("tuan10-11-x", ""),
    ("[D]tuan10-x", ""),  # chỉ A/B/C/X là tầng hợp lệ
])
def test_class_tier_detected(name, tier):
    assert _class_tier(name) == tier
    if tier:
        assert _strip_tier(name) == name[3:]


def test_class_tier_default_empty_on_lesson():
    pkg = LessonPackage(slug="x", title="X")
    assert pkg.class_tier == ""
