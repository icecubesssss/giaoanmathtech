"""Engine tiến hóa có kiểm soát — đọc FeedbackSchema và cập nhật style/prompt,
lưu snapshot lịch sử để rollback. Không vượt rào `style_boundary_limits.json`.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from config import settings
from src.agents.feedback_parser import FeedbackSchema

EVOLUTION_KB = settings.STORAGE_DIR / "evolution_kb"
STYLE_RULES = EVOLUTION_KB / "global_style_rules.json"
STYLE_LIMITS = EVOLUTION_KB / "style_boundary_limits.json"
HISTORY_DIR = EVOLUTION_KB / "style_history"


def _ensure_defaults():
    """Khởi tạo kho tiến hóa nếu chưa tồn tại."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    if not STYLE_RULES.exists():
        STYLE_RULES.write_text(json.dumps({
            "font_slide_min_pt": 32,
            "font_slide_max_pt": 36,
            "max_font_families": 2,
            "hook_tone": "engaging_puzzle",
            "slide_lines_per_frame": 5,
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    if not STYLE_LIMITS.exists():
        STYLE_LIMITS.write_text(json.dumps({
            "font_slide_min_pt": 24,
            "font_slide_max_pt": 36,
            "max_font_families": 2,
            "slide_lines_per_frame": 5,
        }, ensure_ascii=False, indent=2), encoding="utf-8")


def _save_snapshot(rules: dict):
    """Lưu bản snapshot trước mỗi lần ghi đè để có thể rollback."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap = HISTORY_DIR / f"style_{ts}.json"
    snap.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")


def _within_limits(candidate: dict, limits: dict) -> bool:
    """Kiểm tra giá trị mới không vượt rào giới hạn."""
    for key, limit_val in limits.items():
        if key in candidate:
            if "min" in key and candidate[key] < limit_val:
                return False
            if "max" in key and candidate[key] > limit_val:
                return False
    return True


def evolve_from_feedback(feedback: FeedbackSchema) -> dict:
    """
    Áp dụng phản hồi của Thầy vào bộ quy tắc style.
    Mỗi lần sửa đều lưu snapshot vào style_history/ trước khi ghi đè.
    Trả về dict style mới.
    """
    _ensure_defaults()

    current = json.loads(STYLE_RULES.read_text(encoding="utf-8"))
    limits = json.loads(STYLE_LIMITS.read_text(encoding="utf-8"))

    # Lưu snapshot TRƯỚC khi thay đổi
    _save_snapshot(current)

    updated = dict(current)
    changes: list[str] = []

    # Phân tích phản hồi thiết kế
    for note in feedback.design_notes:
        low = note.lower()
        if "chữ nhỏ" in low or "chữ bé" in low or "khó đọc" in low:
            new_val = min(updated.get("font_slide_min_pt", 32) + 2, limits.get("font_slide_max_pt", 36))
            if new_val != updated.get("font_slide_min_pt"):
                updated["font_slide_min_pt"] = new_val
                changes.append(f"Tăng font slide tối thiểu lên {new_val}pt")

        if "font quá nhiều" in low or "nhiều font" in low:
            updated["max_font_families"] = 2
            changes.append("Chốt tối đa 2 họ font")

    # Phân tích phản hồi độ khó
    for note in feedback.difficulty_notes:
        low = note.lower()
        if "hook quá dễ" in low or "hook nhạt" in low:
            updated["hook_tone"] = "challenging_puzzle"
            changes.append("Nâng tông Hook thành bài toán thách thức hơn")
        if "boss quá khó" in low:
            updated["boss_ceiling_buffer"] = -1
            changes.append("Hạ Boss 1 nấc khỏi trần tuyệt đối")

    # Kiểm tra không vượt rào
    if not _within_limits(updated, limits):
        # Rollback nếu vi phạm
        updated = current
        changes = ["[ROLLBACK] Thay đổi vi phạm style_boundary_limits — hoàn tác toàn bộ"]

    # Ghi đè style mới
    STYLE_RULES.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8")

    return {"applied_changes": changes, "new_rules": updated}
