"""Kiểm toàn vẹn cấu trúc GÓI BÀI ngoài Pydantic.

Pydantic chặn sai kiểu/thiếu trường; lớp này chặn sai LOGIC SƯ PHẠM:
đủ và đúng thứ tự 5 chặng (review→concept→practice1→practice2→reflection), số chặng
1..5 không trùng, slug không dấu/không khoảng trắng, mỗi chặng có nội dung.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, get_args

from src.schema import Block, LessonPackage, Stage

__all__ = ["SchemaReport", "validate_lesson_structure", "check_khoa_la"]

_EXPECTED_ORDER = ["review", "concept", "practice1", "practice2", "reflection"]
_SLUG_RX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# type → model, dựng từ chính Union `Block` nên thêm block mới là tự có, khỏi sửa tay.
_BLOCK_MODELS: dict[str, Any] = {}
for _m in get_args(Block):
    _f = _m.model_fields.get("type")
    if _f is not None and isinstance(_f.default, str):
        _BLOCK_MODELS[_f.default] = _m


@dataclass
class SchemaReport:
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def check_khoa_la(raw: dict) -> list[str]:
    """Soi JSON THÔ tìm trường không có trong schema — pydantic sẽ ÂM THẦM VỨT ĐI.

    Vì sao cần: pydantic mặc định BỎ QUA khoá lạ, không kêu một tiếng. Repo đã dính
    đúng họ lỗi này BA LẦN, mỗi lần mất hàng tháng mới phát hiện vì PDF vẫn build đẹp:
      • `solution` (12/08/2026) — seed viết lời giải từng bài, bị vứt ⇒ guide.pdf TRẮNG đáp án.
      • `writelines` (15/08/2026) — 666 bài ở 30 phiếu, bị vứt ⇒ HS không có dòng nào để viết.
      • `answer` (22/09/2026) — 43 bài chương V lớp 9C, bị vứt ⇒ 32 bài trắng đáp án ở Sổ tay GV.
    Cả ba lần đều là "dữ liệu có thật trong seed nhưng không tới được bản in".

    Trả về danh sách CẢNH BÁO (không chặn): khoá lạ đôi khi là ghi chú người soạn tự
    thêm (`_ghi_chu`), nên chặn cứng thì phiền; nhưng phải nói ra để không ai mất dữ liệu
    trong im lặng nữa. Khoá bắt đầu bằng '_' được coi là ghi chú, bỏ qua.
    """
    warns: list[str] = []

    def soi(obj: Any, model: Any, duong: str) -> None:
        if not isinstance(obj, dict):
            return
        biet = set(model.model_fields)
        for k in sorted(k for k in obj if k not in biet and not k.startswith("_")):
            warns.append(
                f"{duong}: trường '{k}' KHÔNG có trong {model.__name__} — "
                f"pydantic sẽ VỨT ĐI, dữ liệu này không tới được bản in."
            )

    soi(raw, LessonPackage, "gói bài")
    for i, s in enumerate(raw.get("stages") or [], start=1):
        if not isinstance(s, dict):
            continue
        soi(s, Stage, f"chặng {i} '{s.get('kind', '?')}'")
        for b in s.get("blocks") or []:
            if not isinstance(b, dict):
                continue
            model = _BLOCK_MODELS.get(b.get("type"))
            if model is None:
                continue
            nhan = b.get("label") or f"block {b.get('type')}"
            soi(b, model, f"chặng {i} · {nhan}")
    return warns


def validate_lesson_structure(lesson: LessonPackage) -> SchemaReport:
    errors: list[str] = []

    if not _SLUG_RX.match(lesson.slug):
        errors.append(f"slug '{lesson.slug}' phải là kebab-case không dấu (vd 'bdt-xet-hieu').")

    kinds = [s.kind for s in lesson.stages]
    if kinds != _EXPECTED_ORDER:
        errors.append(
            f"Thứ tự/đủ 5 chặng sai: nhận {kinds}, cần {_EXPECTED_ORDER}."
        )

    numbers = [s.number for s in lesson.stages]
    if sorted(numbers) != list(range(1, len(lesson.stages) + 1)):
        errors.append(f"Số chặng phải 1..{len(lesson.stages)} không trùng, nhận {numbers}.")

    # Đề kiểm tra (theme "de_thi") KHÔNG chia chặng: nó chỉ mượn 5 chặng làm chỗ chứa
    # các bài. In ra 5 thanh tiêu đề thì sai bộ mặt đề thi và ngốn ~1,3cm mỗi thanh,
    # nên `title` rỗng là hợp lệ — `components/plain.tex.j2` bỏ luôn thanh tiêu đề.
    # Phiếu học tập thường vẫn phải có tiêu đề chặng (HS cần biết đang ở chặng nào).
    bat_buoc_tieu_de = lesson.theme != "de_thi"

    for s in lesson.stages:
        if not s.blocks:
            errors.append(f"Chặng '{s.kind}' rỗng — không có block nội dung nào.")
        if bat_buoc_tieu_de and not s.title.strip():
            errors.append(f"Chặng '{s.kind}' thiếu tiêu đề.")

    return SchemaReport(errors=errors)
