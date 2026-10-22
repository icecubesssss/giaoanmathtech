"""Bản Word (.docx) — test các bẫy đã học khi nghiên cứu typ2docx / tex2gdoc /
formula-flow / tex_math_to_word (22/10/2026) và các lỗi đã dính khi dựng."""
from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path

import pytest
from lxml import etree

from config import settings
from src.compiler.docx_text import (Ctx, DMath, Fig, M, P, Reader, T, Tbl, formulas_in, set_palette,
                                    split_math_raw)

ROOT = settings.ROOT
need_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="chưa cài pandoc")


@pytest.fixture(autouse=True)
def _palette():
    set_palette(json.loads(Path(settings.DESIGN_TOKENS).read_text(encoding="utf-8"))["colors"])


def rd():
    ctx = Ctx()
    return Reader(ctx), ctx


# ───────────────────────── tách công thức ─────────────────────────
def test_xuong_dong_khong_bi_nham_la_cong_thuc():
    # `\\[3pt]` là xuống dòng, KHÔNG phải mở công thức `\[`.
    assert [k for k, _ in split_math_raw(r"a\\[3pt]b")] == ["text"]


def test_hieu_ca_ba_kieu_dau_cong_thuc():
    kinds = [k for k, _ in split_math_raw(r"$x$ và \(y\) và \[z\]")]
    assert kinds.count("math") == 2 and kinds.count("dmath") == 1


def test_token_trong_cong_thuc_thanh_text_cham():
    # Cắt đôi \dfrac quanh ô trống là vỡ cú pháp ⇒ ô trống thành \text{……} ngay trong công thức.
    f = formulas_in(r"$\dfrac{[[mblank:1cm]]}{3}$")
    assert len(f) == 1 and f[0].startswith(r"\dfrac{\text{.") and f[0].endswith("}{3}")


def test_cong_thuc_trong_token_fill_van_duoc_gom():
    assert formulas_in(r"bán kính [[fill:$\dfrac{BC}{2}$]].") == [r"\dfrac{BC}{2}"]


# ───────────────────────── bộ đọc chữ/dàn trang ─────────────────────────
def test_minipage_de_trai_hinh_phai_thanh_bang_hai_cot():
    r, ctx = rd()
    s = (r"\begin{minipage}[t]{0.64\linewidth}Đề bài $x$.\end{minipage}\hfill"
         r"\begin{minipage}[t]{0.31\linewidth}\centering\adjustbox{max width=\linewidth, max totalheight=2.4cm}"
         r"{\begin{tikzpicture}\draw (0,0)--(1,1);\end{tikzpicture}}\end{minipage}")
    b = r.blocks(s)
    assert len(b) == 1 and isinstance(b[0], Tbl) and b[0].widths == [0.64, 0.31]
    assert isinstance(b[0].rows[0][1].blocks[0], Fig) and b[0].rows[0][1].blocks[0].max_h_cm == 2.4
    assert not ctx.unknown


def test_parbox_phuong_an_trac_nghiem_thanh_bang():
    r, _ = rd()
    b = r.blocks(r"Chọn:\par\parbox[t]{0.30\linewidth}{\textbf{A.} $1$}\parbox[t]{0.30\linewidth}{\textbf{B.} $2$}")
    assert isinstance(b[-1], Tbl) and len(b[-1].rows[0]) == 2


def test_tabular_multicolumn_gop_o():
    r, _ = rd()
    b = r.blocks(r"\begin{tabular}{|l|c|c|}\hline a & b & c \\ \hline \multicolumn{2}{|r|}{TỔNG} & 6 \\ \hline\end{tabular}")
    t = b[0]
    assert isinstance(t, Tbl) and t.borders and [c.span for c in t.rows[1]] == [2, 1]


def test_lenh_la_khong_bi_vut_im_lang():
    # tex2gdoc: "pandoc bỏ nội dung mà vẫn exit 0" ⇒ ở đây lệnh lạ phải BÁO, chữ trong ngoặc giữ lại.
    r, ctx = rd()
    b = r.blocks(r"xem \foo{bar} nhé")
    assert "\\foo" in ctx.unknown[0]
    assert "bar" in "".join(x.text for x in b[0].inl if isinstance(x, T))


def test_khoang_trang_sau_lenh_bi_nuot_nhu_tex():
    r, _ = rd()
    b = r.blocks(r"\textquotedblleft xem\textquotedblright")
    assert b[0].inl[0].text == "\u201Cxem\u201D"


def test_ngoac_khai_bao_kieu_chu_chi_tac_dung_trong_ngoac():
    r, _ = rd()
    b = r.blocks(r"{\sffamily\bfseries\color{brand}Lời giải} tiếp")
    head, tail = b[0].inl[0], b[0].inl[1]
    assert head.fmt.bold and head.fmt.sans and head.fmt.color == "C0392B"
    assert not tail.fmt.bold


def test_xuong_dong_br_tach_thanh_dong_khit():
    r, _ = rd()
    b = r.blocks("a) một[[br]]b) hai")
    assert [p.tight for p in b] == [True, False]


def test_the_muc_do_bi_xoa_khoi_ban_in():
    r, _ = rd()
    b = r.blocks("a) [NB] Tính")
    assert "[NB]" not in b[0].inl[0].text


# ───────────────────────── công thức → Equation Word ─────────────────────────
@need_pandoc
def test_omml_widehat_la_accent_va_cung_la_accent():
    from src.compiler.omml import convert_many
    res = convert_many([r"\widehat{ABC}", r"\overset{\frown}{AB}", r"A \setminus B"])
    for tex in res:
        assert res[tex][0] is not None, res[tex][1]
    m = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
    assert res[r"\widehat{ABC}"][0].find(f".//{m}acc") is not None
    # formula-flow: mover phải là accent, nếu không dấu cung bay xa chữ.
    assert res[r"\overset{\frown}{AB}"][0].find(f".//{m}acc") is not None
    assert "\u2216" in "".join(res[r"A \setminus B"][0].itertext())


@need_pandoc
def test_omml_rule_strut_khong_lam_hong_cong_thuc():
    from src.compiler.omml import convert_many
    tex = r"\dfrac{\text{....}\rule[-0.9ex]{0pt}{2.6ex}}{x-3}"
    assert convert_many([tex])[tex][0] is not None


# ───────────────────────── cổng & khuôn ─────────────────────────
def test_khuon_co_watermark_banner_so_trang_o_ca_ba_header():
    from src.validators.docx_gate import check_docx
    tpl = ROOT / "templates" / "docx" / "mathtech.docx"
    errs = [e for e in check_docx(tpl) if "header" in e or "footer" in e]
    assert errs == []
    z = zipfile.ZipFile(tpl)
    hdrs = [n for n in z.namelist() if n.startswith("word/header") and n.endswith(".xml")]
    assert len(hdrs) == 3
    assert all("WordPictureWatermark" in z.read(h).decode() for h in hdrs)


def test_cong_bat_sai_thu_tu_tblPr():
    # 22/10/2026: tblBorders chèn SAU tblLook ⇒ Word mở file treo hộp thoại "unreadable content".
    from src.validators.docx_gate import check_order
    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    x = etree.fromstring(f'<w:tbl xmlns:w="{W}"><w:tblPr><w:tblLook w:val="0"/><w:tblBorders/></w:tblPr></w:tbl>')
    assert check_order(x, "t")


@need_pandoc
def test_de_thi_ra_word_sach_cong_va_du_cong_thuc(tmp_path):
    from src.compiler.docx_builder import build_docx
    from src.main import _load
    seed = ROOT / "inputs/seeds/lop-9/de-kiem-tra-thang-08/phieu-b-de-kiem-tra-thang-8-de-02.json"
    lesson = _load(str(seed))
    path, errs = build_docx(lesson, tmp_path, "de", lesson_dir=seed.parent)
    assert path is not None, errs
    doc = etree.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    m = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
    # tex_math_to_word: oMath nằm trong w:r là sai chuẩn.
    assert all(o.getparent().tag.split("}")[1] != "r" for o in doc.iter(f"{m}oMath"))


@need_pandoc
def test_thuyet_minh_word_cung_so_lieu_voi_pdf(tmp_path):
    from src.compiler.docx_builder import build_thuyetminh_docx
    from src.compiler.thuyetminh_renderer import _phieu_table
    from src.schema.thuyetminh_spec import ThuyetMinhSpec, rates_for_spec, session_info
    from src.compiler.thuyetminh_renderer import _t
    f = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/thuyet-minh.json"
    spec = ThuyetMinhSpec.model_validate(json.loads(f.read_text(encoding="utf-8")))
    path, errs = build_thuyetminh_docx(spec, tmp_path, "tm")
    assert path is not None, errs
    text = "".join(etree.fromstring(zipfile.ZipFile(path).read("word/document.xml")).itertext())
    for p in spec.phieu:
        _, grand = _phieu_table(p, rates_for_spec(spec), session_info(spec))
        assert _t(grand[5]) in text and _t(grand[7]) in text
