"""Cổng gác SÀN độ khó — chống đẻ ra phiếu ngây ngô dưới tầm học sinh.

Đối chiếu LessonPackage với `config/difficulty_profile.json`:
  1. Ba chặng lõi (concept, practice1, practice2) phải có bài toán/công thức thực,
     không phải chữ giảng suông → giữ đúng tầm HS.
  2. practice2 (chặng khó nhất) phải mang dấu hiệu chạm trần độ khó.

Vi phạm → trả DifficultyReject; tầng trên đưa bài về `weave` làm lại, TUYỆT ĐỐI
không hạ tầm nội dung để lách cổng.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from config import settings
from src.schema import LessonPackage, Stage

__all__ = ["DifficultyProfile", "DifficultyReject", "load_profile", "check_difficulty", "check_ramp"]

_DEFAULT_PROFILE = settings.CONFIG_DIR / "difficulty_profile.json"


@dataclass
class DifficultyProfile:
    audience: str = ""
    hook_forbidden_patterns: list[str] = field(default_factory=list)
    boss_must_hit_ceiling: bool = True
    ramp: dict = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: Path) -> "DifficultyProfile":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            audience=data.get("audience", ""),
            hook_forbidden_patterns=data.get("hook_forbidden_patterns", []),
            boss_must_hit_ceiling=data.get("boss_must_hit_ceiling", True),
            ramp=data.get("ramp", {}),
        )


@dataclass
class DifficultyReject:
    reasons: list[str]

    @property
    def passed(self) -> bool:
        return not self.reasons


def load_profile(path: Path | None = None) -> DifficultyProfile:
    return DifficultyProfile.from_file(path or _DEFAULT_PROFILE)


def _has_math_substance(stage: Stage) -> bool:
    """Chặng có bài toán/công thức thực sự (không phải chỉ chữ giảng suông)?"""
    return any(
        b.type in ("math", "problem", "writelines") or "$" in getattr(b, "text", "") or "\\" in getattr(b, "text", "")
        for b in stage.blocks
    )


def check_difficulty(lesson: LessonPackage, profile: DifficultyProfile | None = None) -> DifficultyReject:
    profile = profile or load_profile()
    reasons: list[str] = []
    stages = {s.kind: s for s in lesson.stages}

    # 1. Ba chặng lõi phải có chất toán thực (chống đẻ phiếu dưới tầm).
    for kind, nhan in (("concept", "Khái niệm"), ("practice1", "Luyện tập 1"), ("practice2", "Luyện tập 2")):
        st = stages.get(kind)
        if st is not None and not _has_math_substance(st):
            reasons.append(f"Chặng {nhan} không có bài toán/công thức thực — nghi giảng suông, dưới tầm.")

    # 2. practice2 (chặng khó nhất) phải có và phải chạm trần độ khó.
    p2 = stages.get("practice2")
    if p2 is None:
        reasons.append("Thiếu chặng Luyện tập 2 — gói chưa leo tới trần độ khó.")
    elif profile.boss_must_hit_ceiling and not _has_math_substance(p2):
        reasons.append("Luyện tập 2 không chứa đề/công thức thực — chưa chạm trần độ khó của seed.")

    return DifficultyReject(reasons=reasons)


def check_ramp(lesson: LessonPackage, profile: DifficultyProfile | None = None) -> list[str]:
    """Cổng ĐỘ DỐC (cảnh báo, KHÔNG chặn build): tầng Mở rộng phải là thang nhiều
    bậc, có nhịp cầu dẫn vào, và mỗi bài khó có gợi ý "mở khi bí" để hạ ngưỡng nhập.

    Chỉ soi các bài đã gắn tier="extend" trong chặng reflection; gói cũ chưa gắn tier
    sẽ không phát cảnh báo (cổng kích hoạt theo mức độ áp dụng tier)."""
    profile = profile or load_profile()
    ramp = profile.ramp or {}
    warns: list[str] = []

    refl = next((s for s in lesson.stages if s.kind == "reflection"), None)
    if refl is None:
        return warns

    extend_idx = [i for i, b in enumerate(refl.blocks) if getattr(b, "type", "") == "problem" and getattr(b, "tier", "") == "extend"]
    if not extend_idx:
        return warns  # chưa gắn tier extend → không đánh giá độ dốc

    # 1. Thang ít nhất N bậc (mặc định 2) — tránh 1 bài khó dốc đứng.
    min_n = int(ramp.get("extend_min_problems", 2))
    if len(extend_idx) < min_n:
        warns.append(
            f"Tầng Mở rộng chỉ có {len(extend_idx)} bài — nên làm thang ≥{min_n} bậc "
            "(mỗi bài thêm đúng một bước kỹ thuật) để hạ độ dốc."
        )

    # 2. Có nhịp cầu (block para) trước bài Mở rộng đầu tiên?
    if ramp.get("require_bridge_before_extend", True):
        first = extend_idx[0]
        has_bridge = any(getattr(b, "type", "") == "para" for b in refl.blocks[:first])
        if not has_bridge:
            warns.append(
                "Trước cụm Mở rộng chưa có nhịp cầu (block para chỉ rõ kỹ thuật mới) "
                "— HS dễ hụt khi nhảy từ BTVN sang bài nâng cao."
            )

    # 3. Mỗi bài Mở rộng có gợi ý "mở khi bí"?
    if ramp.get("require_hints_on_extend", True):
        for i in extend_idx:
            b = refl.blocks[i]
            if not getattr(b, "hints", None):
                label = getattr(b, "label", f"block[{i}]")
                warns.append(f"Bài Mở rộng '{label}' chưa có \"hints\" (gợi ý mở khi bí) — nên thêm 1–2 gợi ý định hướng.")

    return warns
