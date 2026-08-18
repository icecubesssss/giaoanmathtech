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
from src.validators.duration_gate import _TAG_RE, band_counts, _count_items, _grade_subject

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
    return warns + check_dang_mapping(lesson, phieu, tol)


def _so_cau(p) -> int:
    """Số CÂU của một bài, dùng ĐÚNG luật của `duration_gate.band_counts`: bài có gắn
    thẻ mức ([NB]/[TH]/…) thì đếm số thẻ, không thì đếm ý a), b)…

    Không dùng chung luật thì hai cổng đếm lệch nhau (phiếu A: 18 câu theo thẻ nhưng
    20 câu theo ý) và Thầy nhận hai con số mâu thuẫn trong cùng một lần validate."""
    text = " ".join([p.statement or ""] + [h or "" for h in (p.hints or [])])
    tags = _TAG_RE.findall(text)
    return len(tags) if tags else _count_items(text)


def _spec_dang_ids(phieu) -> dict[str, object]:
    """{'NB1','NB2','TH1'…} → dòng spec. Đánh số THEO THỨ TỰ TRONG NHÓM BAND, khớp
    đúng cách bảng thuyết minh in ra (renderer cũng đánh NB1, NB2… TH1…)."""
    out, dem = {}, {}
    for r in phieu.rows:
        dem[r.band] = dem.get(r.band, 0) + 1
        out[f"{r.band}{dem[r.band]}"] = r
    return out


def check_dang_mapping(lesson: LessonPackage, phieu, tol: int) -> list[str]:
    """Soi phiếu thật có TƯƠNG ỨNG THẬT RÕ với thuyết minh không (Thầy chốt 14/08/2026).

    Mỗi bài khai `dang_id` ('NB5'…) trỏ về một dòng của phiếu trong thuyet-minh.json.
    Bắt ba chuyện mà cổng đếm-theo-band cũ bỏ lọt hoàn toàn:
      • bài trỏ vào mã dạng KHÔNG CÓ trong thuyết minh (gõ nhầm / dạng đã bỏ);
      • dạng đã chốt trong thuyết minh mà phiếu KHÔNG CÓ bài nào;
      • số câu mỗi dạng lệch quá ±tol so với hợp đồng.
    """
    probs = [b for st in lesson.stages for b in st.blocks
             if getattr(b, "type", "") == "problem"]
    if not probs:
        return []
    hop_dong = _spec_dang_ids(phieu)

    chua_khai = [p.label for p in probs if not (p.dang_id or "").strip()]
    if chua_khai:
        return [f"spec_gate: phiếu {phieu.code} — {len(chua_khai)}/{len(probs)} bài CHƯA khai "
                f"`dang_id` (mã dạng trong thuyết minh): {', '.join(chua_khai[:8])}"
                + (" …" if len(chua_khai) > 8 else "")]

    warns: list[str] = []
    la = sorted({(p.dang_id or "").strip() for p in probs} - set(hop_dong))
    if la:
        warns.append(f"spec_gate: phiếu {phieu.code} — mã dạng KHÔNG CÓ trong thuyết minh: "
                     f"{', '.join(la)}. Mã hợp lệ: {', '.join(sorted(hop_dong))}.")

    for seg in _SEGS:
        # Đếm theo Ý (a, b, c…) chứ KHÔNG theo bài — đúng đơn vị "câu = ý" mà spec và
        # duration_gate/band_counts đang dùng. Đếm theo bài thì một bài 8 ý sẽ ra 1,
        # lệch hẳn với con số spec chốt.
        dem: dict[str, int] = {}
        for p in probs:
            if p.tier == seg:
                ma = (p.dang_id or "").strip()
                dem[ma] = dem.get(ma, 0) + _so_cau(p)
        for ma, r in hop_dong.items():
            want, got = getattr(r, seg), dem.get(ma, 0)
            if want and got == 0:
                warns.append(f"spec_gate: phiếu {phieu.code} · {seg} — dạng {ma} "
                             f"'{r.dang[:44]}' chốt {want} câu nhưng phiếu KHÔNG có bài nào.")
            elif abs(got - want) > tol:
                warns.append(f"spec_gate: phiếu {phieu.code} · {seg} — dạng {ma} có {got} câu, "
                             f"spec chốt {want} (lệch > ±{tol}).")
    return warns
