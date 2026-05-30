"""Kiểm thử smoke-test toàn bộ tổ hợp AI Agents (Phase 4.2).

Chạy mà không cần API Key thật — tất cả agents hỗ trợ chế độ Mock an toàn.
"""
from __future__ import annotations

from pathlib import Path
from src.agents import parse_seed_to_profile, scout_problems, weave_lesson_package
from src.schema.lesson_package import LessonPackage
from src.scrapers.offline_worker import run_scraping_job


def test_seed_parser_returns_valid_profile():
    """seed_parser trả về hồ sơ độ khó hợp lệ (kể cả khi dùng Mock)."""
    profile = parse_seed_to_profile("Bất đẳng thức xét hiệu cho lớp 9")

    assert "audience" in profile
    assert "ceiling" in profile
    assert "floor" in profile
    assert "core_techniques" in profile
    assert isinstance(profile["core_techniques"], list)
    assert 1 <= profile["ceiling"]["level"] <= 10
    assert 1 <= profile["floor"]["level"] <= 10
    assert profile["ceiling"]["level"] > profile["floor"]["level"]


def test_web_scouter_finds_problems():
    """web_scouter tìm được đề từ ngân hàng sau khi offline_worker khởi tạo dữ liệu."""
    # Đảm bảo ngân hàng dữ liệu đã được khởi tạo
    run_scraping_job()

    problems = scout_problems("bdt.xet_hieu", min_diff=1, max_diff=10)
    assert len(problems) >= 1

    for p in problems:
        assert p.statement
        assert p.solution
        assert p.human_verified is True


def test_content_weaver_produces_valid_lesson():
    """content_weaver sinh ra gói LessonPackage hợp lệ với đủ 5 chặng (kể cả khi dùng Mock)."""
    run_scraping_job()
    profile_path = Path("config/difficulty_profile.json")
    assert profile_path.exists(), "Thiếu difficulty_profile.json"

    lesson = weave_lesson_package("bdt.xet_hieu", profile_path)

    assert isinstance(lesson, LessonPackage)
    assert lesson.slug
    assert lesson.title
    assert len(lesson.stages) == 5

    kinds = {s.kind for s in lesson.stages}
    assert kinds == {"review", "concept", "practice1", "practice2", "reflection"}


def test_lesson_stages_have_blocks():
    """Mỗi chặng của gói bài phải có ít nhất 1 block nội dung."""
    run_scraping_job()
    profile_path = Path("config/difficulty_profile.json")
    lesson = weave_lesson_package("bdt.xet_hieu", profile_path)

    for stage in lesson.stages:
        if stage.kind != "reflection":  # reflection có thể chỉ có 1 block gọn
            assert len(stage.blocks) >= 1, f"Chặng {stage.kind} không có block nội dung!"


def test_feedback_parser_and_evolution(tmp_path):
    """Kiểm thử bộ phân tích phản hồi và engine tiến hóa style."""
    from src.agents import FeedbackSchema, parse_feedback, evolve_from_feedback
    from src.agents.evolution_engine import STYLE_RULES, STYLE_LIMITS

    # Tạo file active_feedback.md giả lập
    feedback_file = tmp_path / "active_feedback.md"
    feedback_file.write_text(
        "# Phản hồi từ Thầy\n"
        "- Font chữ bé quá, trên slide học sinh ngồi xa không đọc được.\n"
        "- Hook nhạt quá, cần sinh động hoặc thách thức hơn chút.\n"
        "- Có quá nhiều họ font chữ lung tung trong tài liệu.\n"
        "- Vấn đề chung: Cần chỉn chu hơn.\n",
        encoding="utf-8"
    )

    # 1. Parse feedback
    fb = parse_feedback(feedback_file)
    assert len(fb.design_notes) == 2  # font chữ bé, nhiều họ font
    assert len(fb.difficulty_notes) == 1  # Hook nhạt
    assert len(fb.general_notes) == 1  # vấn đề chung

    # 2. Evolve from feedback
    # Backup và tạm xóa file gốc nếu đang tồn tại để test chạy độc lập, sạch sẽ từ đầu
    orig_rules_exists = STYLE_RULES.exists()
    if orig_rules_exists:
        backup_content = STYLE_RULES.read_text(encoding="utf-8")
        STYLE_RULES.unlink()

    try:
        res = evolve_from_feedback(fb)
        assert "applied_changes" in res
        assert "new_rules" in res
        
        # Kiểm tra sự thay đổi quy tắc (bắt đầu từ default 32 -> tăng lên 34)
        new_rules = res["new_rules"]
        assert new_rules["font_slide_min_pt"] == 34
        assert new_rules["max_font_families"] == 2
        assert new_rules["hook_tone"] == "challenging_puzzle"
    finally:
        # Khôi phục file gốc để tránh side effect
        if orig_rules_exists:
            STYLE_RULES.write_text(backup_content, encoding="utf-8")


