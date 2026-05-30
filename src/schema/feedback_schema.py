"""Định dạng cấu trúc tệp phản hồi (feedback_parser.py sẽ map từ active_feedback.md sang đây)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class FeedbackItem(BaseModel):
    lesson_slug: str
    target: Literal["content", "design", "difficulty", "other"]
    sentiment: Literal["keep", "change"]
    note: str = Field(..., description="Nhận xét thực tế của Thầy sau buổi dạy")


class FeedbackBundle(BaseModel):
    items: list[FeedbackItem] = Field(default_factory=list)
