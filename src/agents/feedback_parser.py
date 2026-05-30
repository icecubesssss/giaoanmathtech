"""Đọc và phân tích `feedback/active_feedback.md` của Thầy,
chuyển đổi nhận xét tự do thành cấu trúc FeedbackSchema cứng.
"""
from __future__ import annotations

import re
from pathlib import Path


class FeedbackSchema:
    """Cấu trúc phản hồi đã được phân tích từ file Markdown của Thầy."""

    def __init__(
        self,
        design_notes: list[str],
        difficulty_notes: list[str],
        tone_notes: list[str],
        general_notes: list[str],
    ):
        self.design_notes = design_notes
        self.difficulty_notes = difficulty_notes
        self.tone_notes = tone_notes
        self.general_notes = general_notes

    def is_empty(self) -> bool:
        return not any([self.design_notes, self.difficulty_notes, self.tone_notes, self.general_notes])

    def __repr__(self) -> str:
        return (
            f"FeedbackSchema("
            f"design={self.design_notes}, "
            f"difficulty={self.difficulty_notes}, "
            f"tone={self.tone_notes}, "
            f"general={self.general_notes})"
        )


def parse_feedback(feedback_path: Path) -> FeedbackSchema:
    """Đọc file feedback Markdown và rút trích phân loại từng nhận xét."""
    if not feedback_path.exists():
        return FeedbackSchema([], [], [], [])

    text = feedback_path.read_text(encoding="utf-8")

    design_notes: list[str] = []
    difficulty_notes: list[str] = []
    tone_notes: list[str] = []
    general_notes: list[str] = []

    # Phân tích từng dòng bullet hoặc đoạn văn
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line = line.lstrip("-*•").strip()
        if not line:
            continue

        low = line.lower()

        # Phân loại theo từ khóa
        if any(kw in low for kw in ["font", "màu", "color", "lề", "bố cục", "thiết kế", "giao diện", "design", "spacing", "phông"]):
            design_notes.append(line)
        elif any(kw in low for kw in ["khó", "dễ", "tầm", "trùm", "boss", "hook", "sàn", "trần", "difficulty", "level"]):
            difficulty_notes.append(line)
        elif any(kw in low for kw in ["giọng", "câu chữ", "tone", "cách viết", "phong cách", "văn phong"]):
            tone_notes.append(line)
        else:
            general_notes.append(line)

    return FeedbackSchema(design_notes, difficulty_notes, tone_notes, general_notes)
