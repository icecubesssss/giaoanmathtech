"""spec_gate — so số câu phiếu (JSON) với HỢP ĐỒNG thuyet-minh.json cạnh bên.

CẢNH BÁO (chưa chặn cứng — sẽ nâng cấp khi Thầy duyệt) khi số câu luyện tập lệch
> `spec_count_tol` mỗi band so với spec đã chốt. OPT-IN: chỉ chạy khi folder phiếu
có `thuyet-minh.json`. Khớp phiếu↔spec theo mã (slug `phieu-a-…` ↔ code A).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from src.schema.lesson_package import LessonPackage
from src.schema.thuyetminh_spec import ThuyetMinhSpec, phieu_band_counts
from src.schema.tier_spec import load_tier_spec, subject_block
from src.validators.duration_gate import band_counts, _grade_subject

_SEGS = ("onclass", "btvn")
_BANDS = ("NB", "TH", "VD", "VDC")


def _match_phieu(spec: ThuyetMinhSpec, lesson: LessonPackage):
    """Phiếu trong spec ứng với lesson: theo tiền tố slug phieu-a-/b-…; nếu spec chỉ
    1 phiếu thì khớp luôn."""
    m = re.match(r"phieu-([a-z])-", lesson.slug or "")
    if m:
        code = m.group(1).upper()
        for p in spec.phieu:
            if p.code.upper() == code:
                return p
    return spec.phieu[0] if len(spec.phieu) == 1 else None


def check_spec_conformance(lesson: LessonPackage, lesson_path: str | Path) -> list[str]:
    """[] nếu không có spec cạnh bên (opt-in) hoặc khớp; ngược lại list cảnh báo."""
    spec_path = Path(lesson_path).parent / "thuyet-minh.json"
    if not spec_path.exists():
        return []
    try:
        spec = ThuyetMinhSpec.model_validate(json.loads(spec_path.read_text(encoding="utf-8")))
    except Exception:                       # noqa: BLE001 — spec hỏng thì báo nhẹ, không chặn
        return ["spec_gate: thuyet-minh.json cạnh bên không đọc được — bỏ qua so khớp."]

    phieu = _match_phieu(spec, lesson)
    if phieu is None:
        return [f"spec_gate: không khớp phiếu '{lesson.slug}' với spec ({len(spec.phieu)} phiếu) "
                "— đặt slug phieu-a-/b-… để so số câu."]

    try:
        block = subject_block(load_tier_spec(), *_grade_subject(lesson))
        tol = int(block.get("spec_count_tol", 1))
    except KeyError:
        tol = 1

    spec_counts = phieu_band_counts(phieu)   # {vidu|onclass|btvn: {band: n}}
    got_counts = band_counts(lesson)         # {onclass|btvn: {band: n}}
    warns: list[str] = []
    for seg in _SEGS:
        for band in _BANDS:
            want = spec_counts.get(seg, {}).get(band, 0)
            got = got_counts.get(seg, {}).get(band, 0)
            if abs(got - want) > tol:
                warns.append(
                    f"spec_gate: phiếu {phieu.code} · {seg} · {band} = {got} câu, "
                    f"spec chốt {want} (lệch > ±{tol}).")
    return warns
