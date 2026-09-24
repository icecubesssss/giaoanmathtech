"""Đổ dữ liệu JSON sạch (LessonPackage) vào template Jinja2 → mã LaTeX.

Dùng cú pháp Jinja riêng để không đụng dấu ngoặc LaTeX:
  khối:   ((* ... *))      biến: ((( ... )))      chú thích: ((= ... =))

Token chỗ trống (do AI sinh ra trong text, KHÔNG phải lệnh LaTeX) được filter
`tex` dịch sang lệnh an toàn:
  [[blank]]      -> \\blank[5cm]      (dòng kẻ chấm để HS viết)
  [[blank:W]]    -> \\blank[W]
  [[mblank:W]]   -> \\rule{W}{0.4pt}  (gạch ngắn trong công thức)
  [[fill:đáp án]] -> ô khuyết của VÍ DỤ MẪU: phiếu HS/slide in gạch trống
                     (\\fillblank), Sổ tay GV in sẵn đáp án (\\fillans).
                     Rộng ô tự suy theo độ dài đáp án, ép tay bằng [[fill:đáp án|1.6cm]].
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
# Ô khuyết CÓ ĐÁP ÁN của Ví dụ mẫu — Thầy chốt 21/09/2026 ("ví dụ phải thành bài điền
# khuyết"). Một nguồn sự thật cho cả ba bản in: sửa số chỉ sửa ở đây, không chép đôi.
_FILL = re.compile(r"\[\[fill:([^\]|]*?)(?:\|([^\]]+))?\]\]")
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


def _be_rong_o(dap_an: str) -> str:
    """Bề rộng ô khuyết suy từ ĐỘ DÀI ĐÁP ÁN (bỏ lệnh LaTeX), kẹp trong [0,9cm; 4,5cm]
    để ô không bao giờ hẹp hơn chữ số lẫn không đẩy dòng vỡ sang trang sau."""
    n = len(_STRIP_TEX.sub("", dap_an or "").strip()) or 3
    return f"{min(max(0.34 * n + 0.45, 0.9), 4.5):.2f}cm"


def _fill_sub(m: "re.Match[str]", show_solution: bool) -> str:
    dap_an = (m.group(1) or "").strip()
    rong = (m.group(2) or "").strip() or _be_rong_o(dap_an)
    if show_solution and dap_an:
        return rf"\fillans{{{dap_an}}}"
    return rf"\fillblank{{{rong}}}"


def _texify(s: str, show_solution: bool = False) -> str:
    """Dịch token chỗ trống / xuống dòng sang lệnh LaTeX. (Khử mã độc là việc của S2.)

    `show_solution` CHỈ đổi cách in [[fill:…]]: Sổ tay GV in đáp án, hai bản kia in ô trống."""
    s = _WRAP_TAG.sub("", s)
    s = _FILL.sub(lambda m: _fill_sub(m, show_solution), s)
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

# Mẫu nhận diện bắt đầu phần Lời giải trong Ví dụ mẫu để ẩn trên Slide
_LOI_GIAI_PAT = (
    r"(?:(?:\s*\[\[br\]\])*\s*(?:\{\s*(?:\\[a-zA-Z]+(?:\{[^{}]*\})?\s*)*Lời\s*giải[.:\-]?\s*\}"
    r"|\\(?:textbf|textit|textsf|text)\{\s*Lời\s*giải[.:\-]?\s*\}|Lời\s*giải\s*[.:\-]?)).*?(?=(\\end\{minipage\}|$))"
)
_LOI_GIAI_RE = re.compile(_LOI_GIAI_PAT, re.DOTALL)


def strip_example_solution(text: str) -> str:
    """Trên slide TV: ví dụ mẫu CHỈ CẦN ĐỀ BÀI + HÌNH VẼ, không in phần 'Lời giải'.

    (Thầy tự giải/hướng dẫn trực tiếp trên lớp — Thầy chốt 09/09/2026).
    """
    s = _LOI_GIAI_RE.sub("", text)
    s = re.sub(r"(?:\s*\[\[br\]\]\s*)+(?=\\end\{minipage\}|$)", "", s)
    return s


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
        # Hình khai bằng TRƯỜNG `figure` (khuôn tách bố cục 22/09/2026) của bài/ví dụ:
        # đưa sang cột phải như block `figure`. Thiếu dòng này thì slide MẤT HÌNH —
        # bản in có biểu đồ mà bản chiếu chỉ còn đề "Biểu đồ dưới đây cho biết…".
        f = getattr(b, "figure", None) if typ in ("problem", "noted") else None
        if f is not None and (getattr(f, "tikz", "") or getattr(f, "image", "")) \
                and getattr(f, "pos", "") != "none":
            segs[-1]["figures"].append(f)
        if typ == "problem":
            # Đề có hộp hình [[wrap]]: bóc hình ra cột phải (mode "cols") thay vì để
            # mã định vị khổ A4 chạy trên slide.
            stmt = getattr(b, "statement_slide", "") or getattr(b, "statement", "") or ""
            fig, rest = split_wrap(stmt)
            if rest != stmt:
                b = b.model_copy(update={"statement": rest, "statement_slide": rest})
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


_STRIP_TEX = re.compile(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?|\[\[[^\]]*\]\]|[{}$\\]")


def plainlen(s: str) -> int:
    """Độ dài CHỮ THẬT (bỏ lệnh LaTeX, token [[…]], ngoặc, $) — thước đo bố cục."""
    return len(_STRIP_TEX.sub("", s or "").strip())


def mcq_cols(options) -> int:
    """SỐ CỘT xếp phương án trắc nghiệm, chọn theo phương án DÀI NHẤT.

    Cột chữ trong hộp \\begin{stage} rộng ~16,2cm; font 12pt ⇒ bề ngang trung bình một
    ký tự ~0,2cm. 4 cột ⇒ mỗi ô ~3,9cm ≈ 19 ký tự kể cả nhãn 'A. ' ⇒ ~16 ký tự nội
    dung; 2 cột ⇒ ~39 ký tự. Vượt ngưỡng cũng KHÔNG vỡ (ô \\raggedright tự xuống dòng),
    chỉ là ô cao hai dòng — nên ngưỡng đặt rộng tay được.
    Phần lớn phương án chương V là '$OA$', 'Dây cung', '$6\\pi$ cm$^2$' (≤10 ký tự)
    ⇒ 4 cột, MỘT hàng thay vì hai hàng + đệm."""
    if not options:
        return 0
    n = max(plainlen(o) for o in options)
    if n <= 14:
        return 4
    if n <= 34:
        return 2
    return 1


_LOI_GIAI = re.compile(r"(\[\[br\]\]\s*)?\{\\sffamily\\bfseries\\color\{brand\}L[ờo]i gi[ảa]i\}")


def tach_loi_giai(text: str) -> tuple[str, str]:
    """Cắt hộp ví dụ thành (ĐỀ, LỜI GIẢI) ở tiêu đề "Lời giải".

    Vì sao cần: hộp ví dụ CÓ HÌNH mà nhét cả lời giải vào cột trái cạnh hình thì cụm
    thành một khối cao không cắt trang được (phiếu A trang 8 bỏ trắng 11,1cm), lại để
    trống toang cột phải bên dưới hình — đúng thủ phạm đã ghi trong "không chừa chỗ
    trống". Đề thì ngắn, đứng cạnh hình vừa đẹp; lời giải dài phải CHẠY FULL WIDTH.

    Không tìm thấy tiêu đề ⇒ trả (toàn bộ, "") để chỗ gọi tự xử."""
    m = _LOI_GIAI.search(text or "")
    if not m:
        return text, ""
    de, lg = text[:m.start()].rstrip(), text[m.start():].lstrip()
    # BỎ [[br]] mở đầu: nó dịch ra `\\` mà đứng ngay sau `\par` của \sidefig thì
    # LaTeX kêu "There's no line here to end" — phần lời giải đã tự mở đoạn mới rồi.
    if lg.startswith("[[br]]"):
        lg = lg[len("[[br]]"):].lstrip()
    return de, lg


_Y_CON = re.compile(r"\[\[br\]\]\s*(?=\\textbf\{?a\)|a\))")


def tach_y_con(statement: str) -> tuple[str, str]:
    """Cắt đề thành (ĐỀ CHUNG, CÁC Ý a) b) c)…) ở ý đầu tiên.

    Thầy chốt 22/09/2026: *"với những bài trắc nghiệm hay điền khuyết thì sẽ là đề bài
    trước → Hình → các đáp án / các câu điền khuyết"*. Các ý con vốn nằm chung trong
    `statement` nối bằng `[[br]]`, nên nếu in cả cục rồi mới tới hình thì HS phải đọc
    ý a), b) trước khi nhìn thấy hình mà ý đó nói về — ngược chiều tư duy.

    Không có ý con ⇒ trả (toàn bộ, "")."""
    m = _Y_CON.search(statement or "")
    if not m:
        return statement, ""
    return statement[:m.start()].rstrip(), statement[m.end():].lstrip()


def fig_side(prob) -> str:
    """Chỗ đặt hình: 'below' | 'none'. KHÔNG còn 'right'.

    Thầy chốt 22/09/2026: *"hình vẽ quá bé, việc để cột cho hình có vẻ không hợp lý nếu
    bài quá dài nên bỏ cái định dạng đó… đề bài trước → Hình → các đáp án / các câu điền
    khuyết"*. Nhốt hình vào cột hẹp 0,30–0,32\\linewidth (~5cm) thì hình hình học chi tiết
    co lại còn đọc không ra nhãn; mà nới cột hình thì cột đề hẹp đi, bài dài càng xấu.
    Xếp DỌC thì hình được trọn bề ngang, to gấp đôi, và cụm cắt trang được tự nhiên.

    Giữ lại `pos: "none"` cho bài chỉ TRỎ sang hình của bài trước (`ref`)."""
    f = getattr(prob, "figure", None)
    if f is None or f.pos == "none" or not (f.tikz or f.image):
        return "none"
    return "below"


def _env(show_solution: bool = False) -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(settings.TEMPLATES_DIR)),
        block_start_string="((*", block_end_string="*))",
        variable_start_string="(((", variable_end_string=")))",
        comment_start_string="((=", comment_end_string="=))",
        trim_blocks=True, lstrip_blocks=True,
        autoescape=False, undefined=StrictUndefined,
    )
    # Filter đóng gói cờ bản in: chỉ Sổ tay GV mới thay [[fill:…]] bằng đáp án.
    env.filters["tex"] = lambda t: _texify(t, show_solution)
    env.filters["strip_example_solution"] = strip_example_solution
    env.globals["split_reflection"] = split_reflection
    env.globals["group_slide_segments"] = group_slide_segments
    env.globals["mcq_cols"] = mcq_cols
    env.globals["fig_side"] = fig_side
    env.globals["tach_loi_giai"] = tach_loi_giai
    env.globals["tach_y_con"] = tach_y_con
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
    env = _env(show_solution)
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
    env = _env(show_solution)
    tpl = env.get_template("base_summary.tex.j2")
    return tpl.render(summary=summary, show_solution=show_solution, **tokens)
