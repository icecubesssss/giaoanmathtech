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


_OLY_W = re.compile(r"\[\[oly:([^\]]+)\]\]")

# Cờ [[wrap]]…[[/wrap]] (hộp hình treo góc phải, chữ chảy quanh) chỉ có nghĩa ở bản A4:
# `_blocks.j2` tự tách trước khi gọi filter. Mọi nơi khác (slide, tổng kết) mà token còn
# sót lại thì XOÁ — trước 2026-08-12 slide in sống ra chữ "[[wrap]][[/wrap]]" trên màn chiếu.
_WRAP_BOX = re.compile(r"\[\[wrap\]\].*?\[\[/wrap\]\]", re.DOTALL)
_WRAP_TAG = re.compile(r"\[\[/?wrap\]\]")
_TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)


def _texify(s: str) -> str:
    """Dịch token chỗ trống / xuống dòng sang lệnh LaTeX. (Khử mã độc là việc của S2.)"""
    s = _WRAP_TAG.sub("", s)
    s = _BLANK_W.sub(r"\\blank[\1]", s)
    s = _BLANK.sub(r"\\blank[5cm]", s)
    s = _MBLANK.sub(r"\\rule{\1}{0.4pt}", s)
    s = _OLY_W.sub(r"\\olybox{\1}", s)
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


class _WrapFigure:
    """Hình bóc ra từ cờ `[[wrap]]` của `statement`, đủ giống FigureBlock để
    `_slide_blocks.j2` dựng được ở cột phải."""
    type = "figure"
    image = ""
    width = ""
    caption = ""

    def __init__(self, tikz: str):
        self.tikz = tikz


def split_wrap(statement: str):
    """Tách hộp hình `[[wrap]]…[[/wrap]]` khỏi đề → (figure|None, đề còn lại).

    Hộp wrap là mã LaTeX định vị cho khổ A4 (`\\makebox` + `\\hspace{0.62\\linewidth}`),
    đem nguyên sang slide 16:9 thì hình văng khỏi khung. Bóc lấy `tikzpicture` bên trong
    rồi trả về để slide xếp 'chữ trái — hình phải'; không tìm thấy tikz thì bỏ hẳn hộp
    (vẫn hơn in sống token ra màn chiếu)."""
    m = _WRAP_BOX.search(statement or "")
    if not m:
        return None, statement
    rest = (statement[:m.start()] + statement[m.end():]).lstrip()
    tikz = _TIKZ.search(m.group(0))
    return (_WrapFigure(tikz.group(0)) if tikz else None), rest


def _seg_mode(seg) -> str:
    """Chọn bố cục cho MỘT segment slide (xem group_slide_segments).

      • "cols"    : chữ trái — hình phải (segment có cả chữ lẫn hình hình học).
      • "stacked" : chữ TRÊN — sơ đồ bước (B1→B2→B3) NẰM NGANG ở DƯỚI, full-width
                    (hình flownode quá rộng, nhét cột phải bị bóp/đè watermark).
      • "opener"  : thẻ Mở màn bên trái — hình minh hoạ bên phải (luôn CÙNG slide).
      • "figonly" : chỉ hình → căn giữa.   • "textonly": chỉ chữ → full width.
    """
    txt, figs = seg["text"], seg["figures"]
    if figs and txt:
        wide = any(getattr(f, "tikz", "") and "flownode" in f.tikz for f in figs)
        return "stacked" if wide else "cols"
    op = txt[0] if txt and getattr(txt[0], "type", "") == "opener" else None
    if op is not None and (getattr(op, "tikz", "") or getattr(op, "image", "")):
        return "opener"
    if figs:
        return "figonly"
    # Đề bài (+ các câu nhỏ a,b,c kèm theo): giữ TRỌN trên MỘT slide, tự co nếu
    # quá dài — tránh allowframebreaks bẻ "đề một chỗ, câu nhỏ một nẻo".
    if any(getattr(b, "type", "") == "problem" for b in txt):
        return "probfit"
    return "textonly"


def group_slide_segments(blocks):
    """Gom blocks của một frame slide thành các "đơn vị dạy" để bố cục đẹp.

    Mỗi segment = {text: [...], figures: [...], mode: ...} ứng với MỘT slide con:
      • `problem`/`noted`/`mindmap` mở segment mới (một đề/một ý/một ví dụ một
        slide) — tránh dồn nhiều đoạn vào một slide rồi tràn/tự ngắt lung tung.
      • `para` đứng NGAY SAU một `problem` = các câu nhỏ (a,b,c) của đề đó → DÍNH
        vào cùng segment (đề và câu nhỏ KHÔNG bị tách hai slide). `para` đứng một
        mình (dẫn nhập/tổng kết) thì mở segment riêng như cũ.
      • `math`/`table`/`writelines` NỐI vào segment hiện hành.
      • `figure` GẮN vào segment hiện hành (cột phải hoặc xếp dưới — xem _seg_mode).
    Nhờ vậy: phiếu CÓ hình → 'chữ trái, hình phải' cùng một slide; phiếu KHÔNG
    hình (đại số) → mỗi đề/ý một slide gọn, không dính đoạn trước."""
    # "opener" phải MỞ segment riêng: nếu dính vào segment của block đứng trước
    # (vd hộp "Ôn bài cũ"), txt[0] không còn là opener → mode "opener" không kích
    # hoạt và HÌNH minh hoạ mở màn bị RƠI khỏi slide.
    HEADERS = ("problem", "noted", "mindmap", "opener")
    segs: list[dict] = []
    for b in blocks:
        typ = getattr(b, "type", "")
        if typ == "figure":
            if not segs:
                segs.append({"text": [], "figures": []})
            segs[-1]["figures"].append(b)
            continue
        if typ == "para":
            prev = segs[-1]["text"][-1] if (segs and segs[-1]["text"]) else None
            if getattr(prev, "type", "") != "problem":
                segs.append({"text": [], "figures": []})
            segs[-1]["text"].append(b)
            continue
        if typ in HEADERS or not segs:
            segs.append({"text": [], "figures": []})
        if typ == "problem":
            # Đề có hộp hình [[wrap]]: bóc hình ra cột phải (mode "cols") thay vì để
            # mã định vị khổ A4 chạy trên slide.
            fig, rest = split_wrap(getattr(b, "statement", "") or "")
            if rest != getattr(b, "statement", ""):
                b = b.model_copy(update={"statement": rest})
                if fig is not None:
                    segs[-1]["figures"].append(fig)
        segs[-1]["text"].append(b)
    segs = _tidy_segments(segs)
    for seg in segs:
        seg["mode"] = _seg_mode(seg)
    return segs


def _plain(b) -> str:
    """Chữ trần của một block (bỏ lệnh LaTeX + token) để đo độ dài thật."""
    raw = getattr(b, "text", "") or getattr(b, "statement", "") or ""
    return _STRIP_TEX.sub("", raw).strip()


def _tidy_segments(segs: list[dict]) -> list[dict]:
    """Dọn segment trước khi chia slide — hai lỗi từng lọt ra bản chiếu:

    1. Segment CHỈ có `writelines` (dòng kẻ viết tay, slide không in) ⇒ frame trắng.
       Hay gặp ở đầu mục BTVN: block tiêu đề bị `split_reflection` bỏ, còn trơ dòng kẻ.
    2. Đoạn tiêu đề mục NGẮN ("1. Gọi tên ba cạnh theo góc nhọn α") đứng riêng một
       segment ⇒ slide chỉ có tiêu đề, nội dung rơi sang slide sau. Gộp nó xuống
       segment kế tiếp (adjustbox tự co nếu cụm dài)."""
    def renderable(seg) -> bool:
        return bool(seg["figures"]) or any(
            getattr(b, "type", "") != "writelines" for b in seg["text"])

    def lone_heading(seg) -> bool:
        txt = [b for b in seg["text"] if getattr(b, "type", "") != "writelines"]
        return (not seg["figures"] and len(txt) == 1
                and getattr(txt[0], "type", "") == "para" and len(_plain(txt[0])) < 60)

    out: list[dict] = []
    for seg in segs:
        if not renderable(seg):
            continue
        if out and lone_heading(out[-1]):
            prev = out.pop()
            seg = {"text": prev["text"] + seg["text"],
                   "figures": prev["figures"] + seg["figures"]}
        out.append(seg)
    return out


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


def _render(template_name: str, lesson: LessonPackage, tokens: dict | None,
            show_solution: bool = False) -> str:
    """`show_solution` đi vào context để `_blocks.j2` in `problem.solution` — CHỈ bật ở
    Sổ tay GV. Phải truyền cho CẢ BA bản (StrictUndefined nổ nếu biến thiếu)."""
    tokens = tokens or load_tokens()
    env = _env()
    tpl = env.get_template(template_name)
    return tpl.render(lesson=lesson, show_solution=show_solution, **tokens)


def render_handout(lesson: LessonPackage, tokens: dict | None = None) -> str:
    """Mã LaTeX phiếu HS (A4 dọc, ẩn lời giải)."""
    theme = getattr(lesson, "theme", "")
    template = "base_handout_thay_thai.tex.j2" if theme == "thay_thai" else "base_handout.tex.j2"
    return _render(template, lesson, tokens, show_solution=False)


def render_guide(lesson: LessonPackage, tokens: dict | None = None) -> str:
    """Mã LaTeX Sổ tay GV (A4 dọc, hiện lời giải đỏ trầm + mẹo sư phạm)."""
    theme = getattr(lesson, "theme", "")
    template = "base_guide_thay_thai.tex.j2" if theme == "thay_thai" else "base_guide.tex.j2"
    return _render(template, lesson, tokens, show_solution=True)


def render_slide(lesson: LessonPackage, tokens: dict | None = None) -> str:
    """Mã LaTeX Slide TV (Beamer 16:9, font sans to, ẩn lời giải)."""
    theme = getattr(lesson, "theme", "")
    template = "base_slide_thay_thai.tex.j2" if theme == "thay_thai" else "base_slide.tex.j2"
    return _render(template, lesson, tokens, show_solution=False)


def render_summary(summary, tokens: dict | None = None, show_solution: bool = False) -> str:
    """Mã LaTeX phiếu TỔNG KẾT CHƯƠNG (A4 1 trang, sơ đồ tư duy to).

    show_solution=False → bản HS (sơ đồ trống); True → bản GV (kèm đáp án ô trống)."""
    tokens = tokens or load_tokens()
    env = _env()
    tpl = env.get_template("base_summary.tex.j2")
    return tpl.render(summary=summary, show_solution=show_solution, **tokens)
