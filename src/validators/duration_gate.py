"""duration_gate — kiểm thời lượng & tỉ lệ NB-TH-VD cho phiếu PHÂN TẦNG.

Thầy chốt 2026-06-11 (xem HUONG-DAN-PHAN-TANG-LOP §2):
  • "Câu" = Ý NHỎ a), b), c)… (mỗi ý 1 câu); bài VD đã tách thì đếm theo thẻ
    [NB]/[TH]/[VD] gắn ở đầu từng ý. KHÔNG đếm phần Khám phá/Khái niệm
    (giờ GV giảng, thực tế ~20–30′/bài).
  • Phút/câu: trên lớp ×1,5 = 1,5/6/12 (NB/TH/VD); BTVN ×1,3 = 1,3/5,2/10,4.
  • Quỹ: Luyện tập trên lớp 120′ · BTVN 90′ (sai số ±10%).
  • Tỉ lệ 40-40-20 áp cho TỪNG PHIẾU, theo THỜI GIAN, sai số ±5 điểm % —
    CHỈ tính phần TRÊN LỚP (Thầy chốt: BTVN không thuộc tỉ lệ này,
    BTVN chỉ cần giữ quỹ phút).

Hiện chuẩn hoá cho tầng C (lớp 9 đại số). Trả về list cảnh báo (kiểu
visual_linter) — "validate sạch" nghĩa là phải xử lý hết trước khi trình Thầy.
"""
from __future__ import annotations

import re

from src.schema.lesson_package import LessonPackage

# Phút/câu theo mức (NB, TH, VD) — Thầy chốt 2026-06-11.
_MIN_ONCLASS = {"NB": 1.5, "TH": 6.0, "VD": 12.0}
_MIN_BTVN = {"NB": 1.3, "TH": 5.2, "VD": 10.4}
_BUDGET = {"onclass": 120.0, "btvn": 90.0}
_BUDGET_TOL = 0.10        # ±10% tổng phút mỗi đoạn
_RATIO_TARGET = {"NB": 40.0, "TH": 40.0, "VD": 20.0}
_RATIO_TOL = 5.0          # ±5 điểm % từng mức

_TAG_RE = re.compile(r"\[(NB|TH|VD)\]")
# Ý a)…j): không dính sau chữ (kể cả chữ Việt có dấu — né "chữa)"), số hay
# backslash (né "(2x-1)", "\linewidth)" …). \w của Python bắt cả Unicode.
_ITEM_RE = re.compile(r"(?<!\w)(?<!\\)([a-j])\)")
_BULLET_RE = re.compile(r"\\bullet")

_LEVEL_TO_BAND = {1: "NB", 2: "TH", 3: "VD", 4: "VD"}


def _count_items(text: str) -> int:
    """Đếm số "câu" trong một bài KHÔNG gắn thẻ mức: mỗi ý a),b)… = 1 câu;
    ý nào liệt kê bullet con thì đếm theo số bullet (vd "b) thử 3 BPT" = 3 câu)."""
    marks = list(_ITEM_RE.finditer(text))
    if not marks:
        return max(1, len(_BULLET_RE.findall(text)))
    total = 0
    for i, m in enumerate(marks):
        chunk = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        bullets = len(_BULLET_RE.findall(chunk))
        total += bullets if bullets else 1
    return total


def _problem_units(lesson: LessonPackage):
    """Gom mỗi `problem` + các `para` đi liền sau nó thành một đơn vị đếm.
    CHỈ đếm các chặng luyện tập/tổng kết (review/concept = giờ GV giảng, bỏ)."""
    for stage in lesson.stages:
        if stage.kind in ("review", "concept"):
            continue
        current = None  # (tier, level, [texts])
        for b in stage.blocks:
            typ = getattr(b, "type", "")
            if typ == "problem":
                if current:
                    yield current
                current = (getattr(b, "tier", "") or "onclass",
                           getattr(b, "level", 0), [b.statement or ""])
            elif typ == "para" and current:
                current[2].append(getattr(b, "text", "") or "")
            elif typ in ("noted", "mindmap"):  # ví dụ mẫu/sơ đồ cắt chuỗi para của đề
                if current:
                    yield current
                    current = None
        if current:
            yield current


def check_duration(lesson: LessonPackage) -> list[str]:
    """Cảnh báo khi phiếu tầng lệch quỹ phút hoặc tỉ lệ 40-40-20 (±5%)."""
    if lesson.class_tier != "C":
        return []  # mới chuẩn hoá tầng C; tầng khác bổ sung khi có SPEC

    minutes = {"onclass": {"NB": 0.0, "TH": 0.0, "VD": 0.0},
               "btvn": {"NB": 0.0, "TH": 0.0, "VD": 0.0}}
    counts = {"onclass": {"NB": 0, "TH": 0, "VD": 0},
              "btvn": {"NB": 0, "TH": 0, "VD": 0}}

    for tier, level, texts in _problem_units(lesson):
        if tier not in minutes:      # extend… không thuộc quỹ giờ tầng C
            continue
        rate = _MIN_ONCLASS if tier == "onclass" else _MIN_BTVN
        text = " ".join(texts)
        tags = _TAG_RE.findall(text)
        if tags:
            for band in tags:
                counts[tier][band] += 1
                minutes[tier][band] += rate[band]
        else:
            band = _LEVEL_TO_BAND.get(level, "TH")
            n = _count_items(text)
            counts[tier][band] += n
            minutes[tier][band] += n * rate[band]

    warns: list[str] = []
    label = {"onclass": "Luyện tập trên lớp", "btvn": "BTVN"}
    for seg, budget in _BUDGET.items():
        total = sum(minutes[seg].values())
        if total == 0:
            continue
        c, m = counts[seg], minutes[seg]
        detail = (f"NB {c['NB']} câu/{m['NB']:.0f}′ · TH {c['TH']} câu/{m['TH']:.0f}′ "
                  f"· VD {c['VD']} câu/{m['VD']:.0f}′ = {total:.0f}′")
        if abs(total - budget) > budget * _BUDGET_TOL:
            warns.append(
                f"duration: {label[seg]} {total:.0f}′ lệch quỹ {budget:.0f}′ quá ±10% — {detail}.")
        if seg != "onclass":   # 40-40-20 là tỉ lệ giờ TRÊN LỚP — BTVN chỉ soi quỹ phút
            continue
        for band, target in _RATIO_TARGET.items():
            share = minutes[seg][band] / total * 100
            if abs(share - target) > _RATIO_TOL:
                warns.append(
                    f"duration: {label[seg]} tỉ lệ {band} = {share:.0f}% lệch chuẩn "
                    f"{target:.0f}% quá ±5 điểm (Thầy chốt 40-40-20 TỪNG PHIẾU) — {detail}.")
    return warns
