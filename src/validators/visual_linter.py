"""Trọng tài Thị giác — xử lý BẰNG CODE XÁC ĐỊNH (không giao LLM).

Hai việc:
  1. `wrap_long_math`: dòng toán quá dài (đặc biệt cho slide TV) thì tự bẻ tại các
     toán tử quan hệ/cộng trừ thành môi trường `aligned` — chống "chữ kiến" tràn khung.
  2. `scan_build_log`: đọc log Tectonic/latexmk, gom lỗi (error/fatal) và cảnh báo
     đáng lo (Overfull/Underfull hbox, Missing font) để báo người, không nuốt log.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

__all__ = ["wrap_long_math", "BuildLogReport", "scan_build_log", "find_presentation_warnings"]

# Chú thích dành cho GIÁO VIÊN không được lọt vào block hiển thị cho HS
# (para/math/noted/problem). Lời giải + mẹo thuộc solution/teacher_note (chỉ in ở Guide).
_TEACHER_ASIDE = re.compile(r"\bGV\b|gi[áa]o\s*vi[êe]n", re.IGNORECASE)
# Nhiều ý a)…b)…c) nằm cùng một block mà không có token xuống dòng [[br]] -> dễ dính chữ.
_SUBITEM = re.compile(r"(?<![A-Za-zÀ-ỹ])[b-fB-F]\)")


def find_presentation_warnings(lesson) -> list[str]:
    """Cảnh báo trình bày (không chặn build): chú thích GV lọt phiếu HS; nhiều ý
    a)b)c) thiếu [[br]] (dính chữ); đoạn quá dài thiếu xuống dòng; thiếu BTVN."""
    warns: list[str] = []
    for st in lesson.stages:
        for i, b in enumerate(st.blocks):
            for attr in ("text", "latex", "statement"):
                v = getattr(b, attr, None)
                if not v:
                    continue
                loc = f"stage[{st.kind}].block[{i}].{attr}"
                if _TEACHER_ASIDE.search(v):
                    warns.append(f"{loc}: có chú thích cho GV trong block hiển thị cho HS — chuyển sang teacher_note.")
                if len(_SUBITEM.findall(v)) >= 2 and "[[br]]" not in v:
                    warns.append(f"{loc}: nhiều ý a)b)c) cùng block nhưng thiếu [[br]] — dễ dính chữ, nên xuống dòng.")
                if attr == "text" and len(v) > 240 and "[[br]]" not in v:
                    warns.append(f"{loc}: đoạn dài ({len(v)} ký tự) không có [[br]] — nên tách bước/dòng cho dễ đọc.")

        # Lời giải (chỉ in ở Guide) cũng phải xuống dòng: nhiều ý a)b)c) mà thiếu
        # [[br]] -> dồn một dòng, GV khó dò (đặc biệt khi có phân số \dfrac).
        if st.solution and len(_SUBITEM.findall(st.solution)) >= 2 and "[[br]]" not in st.solution:
            warns.append(f"stage[{st.kind}].solution: nhiều ý a)b)c) nhưng thiếu [[br]] — nên xuống dòng từng ý.")

    # Reflection phải giao BTVN (bài tập về nhà).
    refl = next((s for s in lesson.stages if s.kind == "reflection"), None)
    if refl is not None:
        joined = " ".join(
            str(getattr(b, a, "") or "") for b in refl.blocks for a in ("text", "statement", "label")
        ).lower()
        has_btvn = (
            any(getattr(b, "tier", "") == "btvn" for b in refl.blocks)
            or "btvn" in joined or "về nhà" in joined or "ve nha" in joined
        )
        if not has_btvn:
            warns.append("stage[reflection]: chưa thấy BÀI TẬP VỀ NHÀ (gắn tier=\"btvn\") — nên giao bài cho HS.")
    return warns

# Bẻ ưu tiên tại toán tử quan hệ trước, rồi cộng/trừ ở mức ngoài cùng.
_REL = re.compile(r"\s*(\\ge|\\geq|\\le|\\leq|=|\\Longleftrightarrow|\\Rightarrow)\s*")


def wrap_long_math(latex: str, max_len: int = 60) -> str:
    """Nếu công thức dài hơn `max_len` ký tự, bẻ tại quan hệ thành aligned.

    Trả về nguyên văn nếu đủ ngắn hoặc đã có môi trường ngắt dòng sẵn.
    """
    s = latex.strip()
    if len(s) <= max_len or "aligned" in s or "\\\\" in s:
        return s

    parts = _REL.split(s)
    if len(parts) < 3:  # không có chỗ bẻ hợp lý
        return s

    # parts = [lhs, op, mid, op, rhs, ...]; ghép lại, xuống dòng & canh trước mỗi op.
    out = parts[0].strip()
    for i in range(1, len(parts) - 1, 2):
        op, term = parts[i], parts[i + 1].strip()
        out += f" \\\\\n  &{op} {term}"
    return "\\begin{aligned}\n  &" + out + "\n\\end{aligned}"


@dataclass
class BuildLogReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not self.errors


_ERR_RX = re.compile(r"^(?:!|.*?\berror\b|.*?\bfatal\b)", re.IGNORECASE)
_WARN_RX = re.compile(r"(Overfull|Underfull)\s+\\hbox|Missing character|missing font", re.IGNORECASE)


def scan_build_log(log_text: str) -> BuildLogReport:
    rep = BuildLogReport()
    for line in log_text.splitlines():
        if _WARN_RX.search(line):
            rep.warnings.append(line.strip())
        elif _ERR_RX.match(line.strip()):
            rep.errors.append(line.strip())
    return rep
