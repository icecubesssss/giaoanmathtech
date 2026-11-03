"""Hai hình thức câu hỏi Đúng/Sai và Nối 2 cột (sheet quy chuẩn Cấu trúc 2, chốt 03/11/2026)."""
import json
from pathlib import Path

from src.compiler.jinja_renderer import render_guide, render_handout, render_slide
from src.schema.lesson_package import LessonPackage
from src.validators.duration_gate import band_counts

_SEED = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json")


def _lesson():
    d = json.loads(_SEED.read_text(encoding="utf-8"))
    st = next(s for s in d["stages"] if s["kind"] == "practice1")
    st["blocks"].insert(0, {"type": "problem", "label": "Bài 0.", "tier": "onclass", "level": 1,
                            "statement": "Khẳng định nào đúng, khẳng định nào sai?",
                            "dung_sai": ["Góc nội tiếp chắn nửa đường tròn là góc vuông.",
                                         "Hai góc nội tiếp bằng nhau thì cùng chắn một cung."],
                            "answer": "a) Đ · b) S"})
    st["blocks"].insert(1, {"type": "problem", "label": "Bài 00.", "tier": "onclass", "level": 1,
                             "statement": "Nối mỗi hình ở cột A với tâm đường tròn ngoại tiếp ở cột B.",
                             "noi_cot_trai": ["Tam giác vuông", "Tam giác đều", "Hình chữ nhật"],
                             "noi_cot_phai": ["giao hai đường chéo", "trung điểm cạnh huyền", "trọng tâm"],
                             "answer": "1 – b · 2 – c · 3 – a"})
    return LessonPackage.model_validate(d)


def test_render_bang_dung_sai_va_noi_cot():
    for render in (render_handout, render_guide, render_slide):
        tex = render(_lesson())
        assert "Góc nội tiếp chắn nửa đường tròn là góc vuông." in tex
        assert "trung điểm cạnh huyền" in tex
    tex = render_handout(_lesson())
    assert "\\textbf{Khẳng định} & \\textbf{Đ} & \\textbf{S}" in tex
    assert "\\textbf{Cột A} & \\textbf{Cột B}" in tex


def test_moi_khang_dinh_va_dong_noi_la_mot_cau():
    goc = json.loads(_SEED.read_text(encoding="utf-8"))
    truoc = band_counts(LessonPackage.model_validate(goc))["onclass"]["NB"]
    sau = band_counts(_lesson())["onclass"]["NB"]
    assert sau - truoc == 2 + 3


def _chu(x) -> str:
    """Gom mọi chữ (trường `text`) trong một nút IR Word, đi xuống mọi danh sách con."""
    if isinstance(x, list):
        return " ".join(_chu(c) for c in x)
    if isinstance(getattr(x, "text", None), str):
        return x.text
    return " ".join(_chu(v) for v in vars(x).values() if isinstance(v, list)) if hasattr(x, "__dict__") else ""


def test_docx_co_bang():
    from src.compiler.docx_renderer import LessonIR, load_tokens
    from src.compiler.docx_text import Tbl
    les = _lesson()
    ir = LessonIR(les, load_tokens())
    st = next(s for s in les.stages if s.kind == "practice1")
    ir.problem(st.blocks[0], "handout")
    ir.problem(st.blocks[1], "handout")

    def duyet(xs):
        for x in xs:
            yield x
            for ten in ("blocks", "body", "children"):
                if isinstance(getattr(x, ten, None), list):
                    yield from duyet(getattr(x, ten))
            if isinstance(getattr(x, "rows", None), list):
                for r in x.rows:
                    yield from duyet(r)
    bang = [_chu(x) for x in duyet(ir.out) if isinstance(x, Tbl)]
    assert any("Khẳng định" in b and "Góc nội tiếp chắn nửa đường tròn" in b for b in bang)
    assert any("Cột A" in b and "trung điểm cạnh huyền" in b for b in bang)
