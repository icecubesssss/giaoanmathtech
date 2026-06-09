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
# Ký tự đặc biệt LaTeX chưa escape — sanitizer KHÔNG bắt, nhưng sẽ làm VỠ build.
#  - '%' '#' thô SAI Ở MỌI NƠI (kể cả trong $...$): '%' là comment (nuốt luôn lệnh
#    đóng hộp tcolorbox -> hỏng guide.pdf), '#' là tham số macro.
#  - '&' chỉ sai NGOÀI công thức (trong $...$ như aligned/array/cases thì '&' hợp lệ).
# Phải viết \% \# \&. Quét TOÀN BỘ field văn bản, không chỉ title/eyebrow/label.
_RAW_PCT_HASH = re.compile(r"(?<!\\)[%#]")
_RAW_AMP = re.compile(r"(?<!\\)&")
_MATH_SPAN = re.compile(r"(?<!\\)\$.*?(?<!\\)\$", re.DOTALL)

# Glyph TOÁN nằm NGOÀI $...$ -> dùng font chữ thường (STIX Two Text) vốn THIẾU các
# ký hiệu này -> in ra "khung ?" (tofu) trên phiếu. Phải bọc trong $...$ để dùng font
# toán: '→' viết '$\to$', '√2' viết '$\sqrt2$', 'α' viết '$\alpha$'… (loại × ÷ ° · ′ ″
# vì STIX Text có sẵn, tránh báo nhầm).
_TOFU_GLYPHS = set(
    "←→↔⇐⇒⇔√≤≥≠≈≡≢∞∑∏∫∮∈∉∋⊂⊃⊆⊇⊄∪∩∅±∓∝∠∥⊥∀∃∄∂∇⋅"
    "αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΠΣΦΨΩ"
)


def _check_special(loc: str, s: str, out: list[str], is_math: bool = False) -> None:
    """Quét một chuỗi: '%'/'#' thô (mọi nơi) và '&' thô (ngoài $...$)."""
    if not s:
        return
    if _RAW_PCT_HASH.search(s):
        out.append(f"{loc}: có '%' hoặc '#' chưa escape — phải viết \\% \\# (nếu không sẽ VỠ build).")
    # '&' hợp lệ trong môi trường toán; chỉ quét phần NGOÀI $...$ (trừ field thuần math).
    outside = s if is_math is False else ""
    if not is_math:
        outside = _MATH_SPAN.sub(" ", s)
        if _RAW_AMP.search(outside):
            out.append(f"{loc}: có '&' chưa escape ngoài công thức — phải viết \\& (nếu không sẽ VỠ build).")
        tofu = sorted({c for c in outside if c in _TOFU_GLYPHS})
        if tofu:
            out.append(
                f"{loc}: ký hiệu {' '.join(tofu)} nằm NGOÀI $...$ — sẽ in ra 'khung ?' "
                f"(font chữ thiếu glyph); hãy bọc trong $...$ (vd $\\to$, $\\sqrt2$, $\\alpha$)."
            )


def _walk_mindmap_labels(node, loc, out):
    lab = node.get("label") if isinstance(node, dict) else getattr(node, "label", None)
    if lab:
        _check_special(loc, lab, out)
    kids = node.get("children") if isinstance(node, dict) else getattr(node, "children", None)
    for c in (kids or []):
        _walk_mindmap_labels(c, loc, out)


def _raw_special_warnings(lesson) -> list[str]:
    """Cảnh báo '&' '%' '#' chưa escape ở MỌI field (title, text, statement, solution,
    teacher_note, caption, hints, nhãn mindmap, ô bảng) — sẽ làm vỡ LaTeX khi build."""
    out: list[str] = []
    for name in ("title", "eyebrow", "grade_label"):
        _check_special(f"lesson.{name}", getattr(lesson, name, "") or "", out)
    for st in lesson.stages:
        base = f"stage[{st.kind}]"
        _check_special(f"{base}.title", st.title or "", out)
        _check_special(f"{base}.solution", getattr(st, "solution", "") or "", out)
        _check_special(f"{base}.teacher_note", getattr(st, "teacher_note", "") or "", out)
        for i, b in enumerate(st.blocks):
            loc = f"{base}.block[{i}]"
            for attr in ("text", "statement", "caption", "label", "root"):
                v = getattr(b, attr, None)
                if v:
                    _check_special(f"{loc}.{attr}", v, out)
            # MathBlock.latex: cả chuỗi là toán -> '&' hợp lệ, vẫn cấm '%' '#'.
            lx = getattr(b, "latex", None)
            if lx:
                _check_special(f"{loc}.latex", lx, out, is_math=True)
            for h in (getattr(b, "hints", None) or []):
                _check_special(f"{loc}.hint", h, out)
            for nd in (getattr(b, "branches", None) or []):
                _walk_mindmap_labels(nd, f"{loc}.mindmap", out)
            for r, row in enumerate(getattr(b, "rows", None) or []):
                for c, cell in enumerate(row or []):
                    _check_special(f"{loc}.row[{r}][{c}]", cell, out)
            for h in (getattr(b, "headers", None) or []):
                _check_special(f"{loc}.header", h, out)
    return out


def find_presentation_warnings(lesson) -> list[str]:
    """Cảnh báo trình bày (không chặn build): chú thích GV lọt phiếu HS; nhiều ý
    a)b)c) thiếu [[br]] (dính chữ); đoạn quá dài thiếu xuống dòng; thiếu BTVN."""
    warns: list[str] = []
    for st in lesson.stages:
        # Tiêu đề chặng đặt trong thanh header (TikZ node), tự co nhưng dài quá sẽ
        # bị thu nhỏ/ép — giữ <= ~46 ký tự để hiện đẹp một dòng cạnh badge.
        if st.title and len(st.title) > 46:
            warns.append(
                f"stage[{st.kind}].title: tiêu đề dài ({len(st.title)} ký tự) — dễ tràn/ép ở thanh header, nên rút gọn ≤ 46 ký tự."
            )
        for i, b in enumerate(st.blocks):
            # Figure/opener: phải có nguồn hình hợp lệ (tikz hoặc image); nếu khai
            # báo tikz thì phải là mã tikzpicture đầy đủ (tránh hình rỗng/hỏng).
            if getattr(b, "type", "") in ("figure", "opener"):
                tk = (getattr(b, "tikz", "") or "").strip()
                img = (getattr(b, "image", "") or "").strip()
                loc = f"stage[{st.kind}].block[{i}]"
                if b.type == "figure" and not tk and not img:
                    warns.append(f"{loc}: block figure không có 'tikz' lẫn 'image' — hình rỗng.")
                if tk and "\\begin{tikzpicture}" not in tk:
                    warns.append(f"{loc}.tikz: thiếu \\begin{{tikzpicture}} — mã hình không đầy đủ, sẽ vỡ/khuyết khi build.")
            # Chấm sao MỨC ĐỘ: mỗi bài nên gắn level 1..4 (1 NB, 2 TH, 3 VD, 4 VD cao).
            # Chưa gắn (level 0) -> renderer lùi về sao theo tier, nhưng nhắc Thầy chấm
            # đúng mức nhận thức để sao phản ánh độ khó thật, không phải nơi làm bài.
            if getattr(b, "type", "") == "problem" and getattr(b, "level", 0) == 0:
                lbl = getattr(b, "label", "") or f"block[{i}]"
                warns.append(
                    f"stage[{st.kind}] '{lbl}': chưa chấm sao mức độ — gắn level 1..4 "
                    "(1=Nhận biết, 2=Thông hiểu, 3=Vận dụng, 4=Vận dụng cao)."
                )
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

        # Lời giải KHÔNG được là 'bức tường chữ': tách theo [[br]] / \par, nếu còn
        # đoạn quá dài (nhiều bước dồn một dòng) -> cảnh báo chèn [[br]] tách bước.
        if st.solution:
            segs = re.split(r"\[\[br\]\]|\\par", st.solution)
            longest = max((len(s.strip()) for s in segs), default=0)
            if longest > 220:
                warns.append(f"stage[{st.kind}].solution: có đoạn dài {longest} ký tự không xuống dòng — chèn [[br]] tách từng bước cho dễ đọc.")

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

    warns.extend(_raw_special_warnings(lesson))
    warns.extend(_scaffolding_warnings(lesson))
    return warns


# Dạng dễ trừu tượng mà Thầy yêu cầu PHẢI có "ví dụ mồi" dẫn dắt (hạ độ dốc) —
# nếu xuất hiện dạng này mà cả phiếu không có chữ "mồi" thì nhắc soạn thêm scaffolding
# (hoặc hỏi Thầy cách dạy). Cố ý hẹp & chính xác để khỏi báo nhầm.
_HARD_SCAFFOLD = (
    (re.compile(r"làm\s+chung|làm\s+riêng", re.I),
     "Có dạng 'làm chung – làm riêng' nhưng chưa thấy 'ví dụ mồi' dẫn dắt (vd hình ảnh pizza/vòi nước) — nên thêm scaffolding hoặc HỎI Thầy cách dạy."),
    (re.compile(r"xu[ôo]i\s*dòng|ngược\s*dòng", re.I),
     "Có dạng 'xuôi/ngược dòng' nhưng chưa thấy 'ví dụ mồi' (vd con thuyền trôi theo dòng) — nên thêm scaffolding hoặc HỎI Thầy cách dạy."),
)


def _scaffolding_warnings(lesson) -> list[str]:
    joined = " ".join(
        str(getattr(b, a, "") or "")
        for st in lesson.stages for b in st.blocks for a in ("text", "statement")
    )
    if "mồi" in joined.lower():  # đã có ví dụ mồi -> coi như đã dẫn dắt
        return []
    return [msg for rx, msg in _HARD_SCAFFOLD if rx.search(joined)]

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
