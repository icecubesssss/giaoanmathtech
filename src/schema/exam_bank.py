"""Loader ngân hàng đề (đã gắn band/phut) — tra cứu câu theo id cho gate/spec.

Cho phép spec (`SpecRow.source_refs`) trỏ vào câu thật trong đề thi; gate/đối chiếu
đọc được band + phút THẬT của câu đó (thay vì chỉ rate trung bình band).
"""
from __future__ import annotations

import json

from config import settings

EXAMS_DIR = settings.ROOT / "inputs" / "refs" / "de-thi" / "lop-9" / "exams"
_CACHE: dict[str, dict] | None = None


def load_bank(force: bool = False) -> dict[str, dict]:
    """id câu → {band, phut, diem, dang, chuong, de}. Cache; rỗng nếu chưa có bank."""
    global _CACHE
    if _CACHE is not None and not force:
        return _CACHE
    bank: dict[str, dict] = {}
    if EXAMS_DIR.exists():
        for f in sorted(EXAMS_DIR.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            for c in d.get("cau", []):
                cid = c.get("id") or f"{f.stem}-{c.get('bai','')}{c.get('y','') or ''}"
                bank[cid] = {k: c.get(k) for k in ("band", "phut", "diem", "dang", "chuong", "de")}
    _CACHE = bank
    return bank


def lookup(ids: list[str]) -> list[tuple[str, dict]]:
    """Các (id, record) có thật trong bank (bỏ qua id không khớp — opt-in, không báo lỗi)."""
    bank = load_bank()
    return [(i, bank[i]) for i in ids if i in bank]
