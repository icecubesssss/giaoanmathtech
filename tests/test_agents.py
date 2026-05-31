"""Kiểm thử bộ phân tích phản hồi của Thầy và engine tiến hóa style."""
from __future__ import annotations


def test_feedback_parser_and_evolution(tmp_path):
    """Parse active_feedback.md và áp dụng tiến hóa style có kiểm soát."""
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
