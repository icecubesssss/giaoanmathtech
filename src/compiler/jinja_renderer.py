"""Đổ dữ liệu JSON sạch (LessonPackage) vào template Jinja2 → mã LaTeX.

Dùng cú pháp Jinja riêng để không đụng dấu ngoặc LaTeX:
  khối:   ((* ... *))      biến: ((( ... )))      chú thích: ((= ... =))

Token chỗ trống (do AI sinh ra trong text, KHÔNG phải lệnh LaTeX) được filter
`tex` dịch sang lệnh an toàn:
  [[blank]]      -> \\blank[5cm]      (dòng kẻ chấm để HS viết)
  [[blank:W]]    -> \\blank[W]
  [[mblank:W]]   -> \\rule{W}{0.4pt}  (gạch ngắn trong công thức)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from config import settings
from src.schema import LessonPackage

_BLANK_W = re.compile(r"\[\[blank:([^\]]+)\]\]")
_BLANK = re.compile(r"\[\[blank\]\]")
_MBLANK = re.compile(r"\[\[mblank:([^\]]+)\]\]")
# [[br]] -> xuống dòng LaTeX. Bỏ [[br]] thừa ở cuối chuỗi (xuống dòng cuối đoạn
# gây lỗi "There's no line here to end") rồi mới đổi phần còn lại thành "\\".
_BR_TRAIL = re.compile(r"(?:\s*\[\[br\]\]\s*)+$")
_BR = re.compile(r"\s*\[\[br\]\]\s*")


def _texify(s: str) -> str:
    """Dịch token chỗ trống / xuống dòng sang lệnh LaTeX. (Khử mã độc là việc của S2.)"""
    s = _BLANK_W.sub(r"\\blank[\1]", s)
    s = _BLANK.sub(r"\\blank[5cm]", s)
    s = _MBLANK.sub(r"\\rule{\1}{0.4pt}", s)
    s = _BR_TRAIL.sub("", s)
    # [[br]] -> xuống dòng kèm 3pt hở dọc, để dòng chứa \dfrac không chạm dòng kế.
    s = _BR.sub(r" \\\\[3pt] ", s)
    return s


_HEAD_BTVN = re.compile(r"về\s*nhà|btvn", re.IGNORECASE)
_HEAD_EXT = re.compile(r"mở\s*rộng|nhịp\s*cầu", re.IGNORECASE)
_STRIP_TEX = re.compile(r"\\[a-zA-Z]+|\[\[[^\]]*\]\]|[{}$]")


def split_reflection(blocks):
    """Chia blocks chặng reflection thành 3 mục để tách BTVN/Mở rộng khỏi 'Tổng kết'.

    Phân mục theo `tier` của bài (btvn/extend) HOẶC tiêu đề ('về nhà'/'mở rộng'/
    'nhịp cầu'). Block tiêu đề NGẮN bị bỏ (template tự in banner mục) — block dài
    (vd câu nhịp cầu) được giữ. Sơ đồ tư duy nằm ở phần đầu sẽ thuộc 'Tổng kết'.
    Trả về dict {tong_ket, btvn, mo_rong} (list block giữ nguyên thứ tự)."""
    out = {"tong_ket": [], "btvn": [], "mo_rong": []}
    seg = "tong_ket"
    for b in blocks:
        typ = getattr(b, "type", "")
        text = getattr(b, "text", "") or getattr(b, "statement", "") or ""
        tier = getattr(b, "tier", "")
        is_head = typ in ("para", "noted")
        head_btvn = is_head and bool(_HEAD_BTVN.search(text))
        head_ext = is_head and bool(_HEAD_EXT.search(text))
        if tier == "btvn" or head_btvn:
            seg = "btvn"
        elif tier == "extend" or head_ext:
            seg = "mo_rong"
        # Bỏ block CHỈ là tiêu đề ngắn (banner do \worksheetsection in).
        if (head_btvn or head_ext) and len(_STRIP_TEX.sub("", text).strip()) < 70:
            continue
        out[seg].append(b)
    return out


def group_slide_segments(blocks):
    """Gom blocks của một frame slide thành các "đơn vị dạy" để bố cục đẹp.

    Mỗi segment = {text: [...], figures: [...]} ứng với MỘT slide con. Quy tắc:
      • `problem`/`noted`/`para`/`mindmap` mở segment mới (một đề/một ý/một ví dụ
        một slide) — tránh dồn nhiều đoạn vào một slide rồi tràn/tự ngắt lung tung.
      • `math`/`table` NỐI vào segment hiện hành (công thức/bảng đi liền phần dẫn
        ngay trước, không tách rời).
      • `figure` GẮN vào segment hiện hành (render cột phải, cạnh chữ bên trái).
    Nhờ vậy: phiếu CÓ hình → 'chữ trái, hình phải' cùng một slide; phiếu KHÔNG
    hình (đại số) → mỗi đề/ý một slide gọn, không dính đoạn trước."""
    HEADERS = ("problem", "noted", "para", "mindmap")
    segs: list[dict] = []
    for b in blocks:
        typ = getattr(b, "type", "")
        if typ == "figure":
            if not segs:
                segs.append({"text": [], "figures": []})
            segs[-1]["figures"].append(b)
            continue
        if typ in HEADERS or not segs:
            segs.append({"text": [], "figures": []})
        segs[-1]["text"].append(b)
    return segs


def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(settings.TEMPLATES_DIR)),
        block_start_string="((*", block_end_string="*))",
        variable_start_string="(((", variable_end_string=")))",
        comment_start_string="((=", comment_end_string="=))",
        trim_blocks=True, lstrip_blocks=True,
        autoescape=False, undefined=StrictUndefined,
    )
    env.filters["tex"] = _texify
    env.globals["split_reflection"] = split_reflection
    env.globals["group_slide_segments"] = group_slide_segments
    return env


def load_tokens() -> dict:
    tokens = json.loads(Path(settings.DESIGN_TOKENS).read_text(encoding="utf-8"))
    # Chuyển đổi tương đối sang tuyệt đối động để XeLaTeX/Tectonic tìm thấy chính xác
    root_str = str(settings.ROOT.resolve()).replace("\\", "/") + "/"
    if "fonts" in tokens and "dir" in tokens["fonts"]:
        if not tokens["fonts"]["dir"].startswith("/") and not (len(tokens["fonts"]["dir"]) > 1 and tokens["fonts"]["dir"][1] == ":"):
            tokens["fonts"]["dir"] = f"{root_str}assets/fonts/"
    # Thêm các hằng số assets tuyệt đối vào tokens để chèn vào watermark/logo
    tokens["assets_dir"] = f"{root_str}assets/"
    return tokens


def _render(template_name: str, lesson: LessonPackage, tokens: dict | None) -> str:
    tokens = tokens or load_tokens()
    env = _env()
    tpl = env.get_template(template_name)
    return tpl.render(lesson=lesson, **tokens)


def render_handout(lesson: LessonPackage, tokens: dict | None = None) -> str:
    """Mã LaTeX phiếu HS (A4 dọc, ẩn lời giải)."""
    return _render("base_handout.tex.j2", lesson, tokens)


def render_guide(lesson: LessonPackage, tokens: dict | None = None) -> str:
    """Mã LaTeX Sổ tay GV (A4 dọc, hiện lời giải đỏ trầm + mẹo sư phạm)."""
    return _render("base_guide.tex.j2", lesson, tokens)


def render_slide(lesson: LessonPackage, tokens: dict | None = None) -> str:
    """Mã LaTeX Slide TV (Beamer 16:9, font sans to, ẩn lời giải)."""
    return _render("base_slide.tex.j2", lesson, tokens)


def render_summary(summary, tokens: dict | None = None, show_solution: bool = False) -> str:
    """Mã LaTeX phiếu TỔNG KẾT CHƯƠNG (A4 1 trang, sơ đồ tư duy to).

    show_solution=False → bản HS (sơ đồ trống); True → bản GV (kèm đáp án ô trống)."""
    tokens = tokens or load_tokens()
    env = _env()
    tpl = env.get_template("base_summary.tex.j2")
    return tpl.render(summary=summary, show_solution=show_solution, **tokens)
