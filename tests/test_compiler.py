"""Smoke test khung biên dịch + chốt bảo mật -shell-escape."""
import os
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ["base_handout.tex.j2"]  # base_slide/base_guide là việc của S3
COMPONENTS = ["review", "concept", "practice1", "practice2", "reflection"]


def test_handout_template_and_five_components_exist():
    for t in TEMPLATES:
        assert (ROOT / "templates" / t).exists(), f"Thiếu template {t}"
    for c in COMPONENTS:
        assert (ROOT / "templates" / "components" / f"{c}.tex.j2").exists(), f"Thiếu chặng {c}"


def test_pydantic_schema_importable():
    from src.schema.lesson_package import LessonPackage  # noqa: F401


def test_jinja_renders_without_error():
    env = Environment(
        loader=FileSystemLoader(str(ROOT / "templates")),
        block_start_string="((*", block_end_string="*))",
        variable_start_string="(((", variable_end_string=")))",
        comment_start_string="((=", comment_end_string="=))",
    )
    # Renderer thật được test riêng (build-handout); ở đây chỉ smoke parse cú pháp Jinja.
    tpl = env.get_template("base_handout.tex.j2")
    assert tpl is not None


def test_no_shell_escape_in_build():
    """Chốt bảo mật: latex_builder TUYỆT ĐỐI không được bật -shell-escape."""
    src = (ROOT / "src" / "compiler" / "latex_builder.py").read_text(encoding="utf-8")
    assert "-shell-escape" not in src, "Phát hiện -shell-escape: nguy cơ thực thi mã!"


def test_strip_example_solution():
    """Slide TV: ví dụ mẫu tự động cắt bỏ Lời giải, chỉ giữ đề bài."""
    from src.compiler.jinja_renderer import strip_example_solution

    text_with_solution = (
        r"\begin{minipage}{0.6\linewidth}" "\n"
        r"\textbf{Ví dụ 1.} Rút gọn biểu thức $A$.[[br]]" "\n"
        r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]" "\n"
        r"\hspace*{1.4em}Ta có $A = \sqrt{x} + 1$." "\n"
        r"\end{minipage}\hfill\begin{minipage}{0.3\linewidth}tikz\end{minipage}"
    )
    cleaned = strip_example_solution(text_with_solution)
    assert "Lời giải" not in cleaned
    assert "Ta có" not in cleaned
    assert "Rút gọn biểu thức $A$." in cleaned
    assert "tikz" in cleaned


def test_statement_slide_and_text_slide_schema():
    """ProblemBlock và NotedBlock hỗ trợ field slide riêng."""
    from src.schema.lesson_package import ProblemBlock, NotedBlock

    p = ProblemBlock(
        label="Bài 1.",
        statement="Đề bài điền khuyết dài",
        statement_slide="Đề bài rút gọn chiếu TV",
    )
    assert p.statement_slide == "Đề bài rút gọn chiếu TV"

    n = NotedBlock(
        text="Nội dung ví dụ đầy đủ",
        text_slide="Nội dung ví dụ trên slide",
    )
    assert n.text_slide == "Nội dung ví dụ trên slide"


# ── Token [[fill:đáp án]] — ví dụ mẫu điền khuyết (Thầy chốt 21/09/2026) ──────

def test_fill_phieu_hs_in_o_trong_con_so_tay_gv_in_dap_an():
    from src.compiler.jinja_renderer import _texify
    t = r"$BC^2 = [[fill:225]]$ nên $BC = [[fill:15]]$ cm."
    hs, gv = _texify(t, False), _texify(t, True)
    assert "fillblank" in hs and "225" not in hs and "15" not in hs
    assert r"\fillans{225}" in gv and r"\fillans{15}" in gv


def test_fill_rong_o_theo_do_dai_dap_an_va_ep_tay_duoc():
    from src.compiler.jinja_renderer import _texify
    assert r"\fillblank{1.2cm}" in _texify(r"$x = [[fill:225|1.2cm]]$", False)
    ngan, dai = _texify(r"[[fill:5]]", False), _texify(r"[[fill:trung điểm của $BC$]]", False)
    assert float(ngan.split("{")[1].rstrip("cm}")) < float(dai.split("{")[1].rstrip("cm}"))


def test_fill_o_khong_co_dap_an_van_ra_o_trong_o_so_tay_gv():
    from src.compiler.jinja_renderer import _texify
    assert "fillblank" in _texify(r"$R = [[fill:]]$", True)


def test_de_ngan_dinh_cung_voi_hinh_de_dai_phat_mem():
    """Đề NGẮN (1–2 dòng) dính cứng với hình (\\figbelowkeep = \\nobreak): tách ra chẳng
    cứu được giấy mà HS phải lật trang mới thấy hình (phiếu 2 ch.5 9C, Bài 2 cuối trang).
    Đề DÀI vẫn dùng \\figbelow phạt mềm để khỏi nhảy nguyên khối bỏ trắng nửa trang."""
    from src.compiler.jinja_renderer import render_handout
    from src.schema.lesson_package import LessonPackage

    tikz = "\\begin{tikzpicture}\\draw (0,0) circle (1);\\end{tikzpicture}"
    dai = "[TH] " + "Một đề bài rất dài kể lể bối cảnh thực tế. " * 8
    lesson = LessonPackage.model_validate({
        "slug": "t", "title": "T", "stages": [{"kind": "practice1", "number": 3, "title": "L", "blocks": [
            {"type": "problem", "label": "Bài 1.", "statement": "[NB] Trên Hình 1, $CD$ là gì?",
             "level": 1, "tier": "onclass", "options": ["A1", "B1", "C1", "D1"],
             "figure": {"tikz": tikz, "caption": "Hình 1", "pos": "below"}},
            {"type": "problem", "label": "Bài 2.", "statement": dai, "level": 2, "tier": "onclass",
             "figure": {"tikz": tikz, "caption": "Hình 2", "pos": "below"}}]}]})
    tex = render_handout(lesson)
    assert tex.count("\\figbelowkeep{0.44}") == 1
    assert tex.count("\\figbelow{0.44}") == 1


def test_slide_giu_hinh_va_phuong_an_cua_khuon_moi():
    """Bài khai hình bằng trường `figure` + phương án bằng `options` (khuôn 22/09/2026):
    slide phải có ĐỦ hình và A, B, C, D — trước đây cả hai rơi mất trên bản chiếu."""
    from src.compiler.jinja_renderer import group_slide_segments, render_slide
    from src.schema.lesson_package import LessonPackage

    tikz = "\\begin{tikzpicture}\\draw (0,0) rectangle (1,1);\\end{tikzpicture}"
    lesson = LessonPackage.model_validate({
        "slug": "t", "title": "T", "stages": [{"kind": "practice1", "number": 3, "title": "L", "blocks": [
            {"type": "problem", "label": "Bài 1.", "statement": "[NB] Chọn đáp án.", "level": 1,
             "tier": "onclass", "options": ["Mot", "Hai", "Ba", "Bon"],
             "figure": {"tikz": tikz, "caption": "Hình 1", "pos": "below"}},
            {"type": "noted", "variant": "example", "text": "\\textbf{Ví dụ 1.} Đề.",
             "figure": {"tikz": tikz, "caption": "Hình 2", "pos": "below"}}]}]})
    blocks = lesson.stages[0].blocks
    segs = group_slide_segments(blocks)
    assert [len(s["figures"]) for s in segs] == [1, 1]
    assert all(s["mode"] == "cols" for s in segs)
    tex = render_slide(lesson)
    assert tex.count("rectangle (1,1)") == 2
    for nhan in ("A.}~Mot", "B.}~Hai", "C.}~Ba", "D.}~Bon"):
        assert nhan in tex
