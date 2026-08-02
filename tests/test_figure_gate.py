"""Cổng đề↔hình: dựng lại đúng ba lỗi Thầy An bắt được ngày 2026-07-28."""
from __future__ import annotations

import pytest

from src.schema import LessonPackage
from src.validators import check_figure_symbols, check_clone_problems, check_hinh_thieu


def _lesson(problems: list[dict]) -> LessonPackage:
    """Gói bài tối thiểu đủ 5 chặng, nhét bài cần soi vào practice1."""
    stages = [
        {"kind": "review", "number": 1, "title": "Khám phá", "blocks": [{"type": "para", "text": "x"}]},
        {"kind": "concept", "number": 2, "title": "Khái niệm", "blocks": [{"type": "para", "text": "x"}]},
        {"kind": "practice1", "number": 3, "title": "Luyện tập 1", "blocks": problems},
        {"kind": "practice2", "number": 4, "title": "Luyện tập 2", "blocks": [{"type": "para", "text": "x"}]},
        {"kind": "reflection", "number": 5, "title": "Tổng kết", "blocks": [{"type": "para", "text": "x"}]},
    ]
    return LessonPackage.model_validate(
        {"slug": "thu-nghiem", "title": "Thử nghiệm", "eyebrow": "", "stages": stages}
    )


def _tikz(*labels: str) -> str:
    nodes = "\n".join(f"  \\node at (0,0){{${lab}$}};" for lab in labels)
    return "\\begin{tikzpicture}\n" + nodes + "\n\\end{tikzpicture}"


def _problem(label: str, text: str, figure: str = "") -> dict:
    return {"type": "problem", "label": label, "level": 1, "tier": "onclass",
            "statement": text + figure, "solution": "Đáp án A."}


# --- Lỗi 1: hình thiếu nhãn mà đề đang hỏi (phiếu C) ------------------------
def test_bat_hinh_thieu_nhan_goc_de_dang_hoi():
    """Đề hỏi A_2/B_2 mà hình chỉ dán A_1/B_1 → HS không có căn cứ trả lời."""
    lesson = _lesson([
        _problem("Bài 1.", r"Cặp góc nào so le trong? A. $\widehat{A_2}$ và $\widehat{B_1}$",
                 _tikz(r"\widehat{A_1}", r"\widehat{B_1}")),
    ])
    viols = check_figure_symbols(lesson)
    assert len(viols) == 1
    assert r"\widehat{A_2}" in viols[0].reason


def test_hinh_dan_du_nhan_thi_qua_cong():
    lesson = _lesson([
        _problem("Bài 1.", r"Cặp góc nào so le trong? A. $\widehat{A_2}$ và $\widehat{B_1}$",
                 _tikz(r"\widehat{A_1}", r"\widehat{A_2}", r"\widehat{B_1}")),
    ])
    assert check_figure_symbols(lesson) == []


# --- Lỗi 2: nhãn đầu tia ghi cả tên tia (phiếu B: "lỗi tia Ot/Od") ----------
def test_bat_nhan_dau_tia_ghi_ca_ten_tia():
    lesson = _lesson([
        _problem("Bài 2.", "Tia $Ot$ là phân giác của $\\widehat{mOn}$.", _tikz("m", "n", "Ot", "O")),
    ])
    viols = check_figure_symbols(lesson)
    assert len(viols) == 1
    assert "$Ot$" in viols[0].reason and "$t$" in viols[0].reason


def test_nhan_dau_tia_mot_chu_thi_qua_cong():
    lesson = _lesson([
        _problem("Bài 2.", "Tia $Ot$ là phân giác của $\\widehat{mOn}$.", _tikz("m", "n", "t", "O")),
    ])
    assert check_figure_symbols(lesson) == []


# --- Lỗi 3: bài chép nhân bản (phiếu C bị Thầy gạch chéo 4 trang) -----------
def test_bat_de_chep_nhieu_lan():
    de = ("Cho hai đường thẳng $a, b$ bị cắt bởi đường thẳng $c$ tại $A$ và $B$. "
          "Cặp góc nào sau đây là hai góc so le trong?")
    lesson = _lesson([
        _problem(f"Bài {i}.", de, _tikz(rf"\widehat{{A_{i}}}")) for i in range(1, 6)
    ])
    viols = check_clone_problems(lesson)
    assert len(viols) == 1
    assert "5 lần" in viols[0].reason


def test_caption_hinh_khac_so_van_tinh_la_ban_sao():
    """'Hình 1' vs 'Hình 7' là đánh số tự động — không được coi là hai đề khác nhau."""
    de = "Cho hai đường thẳng $a, b$ bị cắt bởi $c$. Cặp góc nào là so le trong?"
    lesson = _lesson([
        _problem("Bài 1.", de + " Hình 1", _tikz("a")),
        _problem("Bài 2.", de + " Hình 7", _tikz("a")),
        _problem("Bài 3.", de + " Hình 9", _tikz("a")),
    ])
    assert len(check_clone_problems(lesson)) == 1


def test_khac_so_do_thi_KHONG_phai_ban_sao():
    """Cùng lời văn nhưng khác số đo = bài luyện tập hợp lệ, không được báo nhầm."""
    lesson = _lesson([
        _problem("Bài 1.", r"Cho $\widehat{xOy} = 80^\circ$, $Oz$ là phân giác. Tính $\widehat{xOz}$."),
        _problem("Bài 2.", r"Cho $\widehat{xOy} = 120^\circ$, $Oz$ là phân giác. Tính $\widehat{xOz}$."),
        _problem("Bài 3.", r"Cho $\widehat{xOy} = 50^\circ$, $Oz$ là phân giác. Tính $\widehat{xOz}$."),
    ])
    assert check_clone_problems(lesson) == []


@pytest.mark.parametrize("n_ban_sao,co_bao", [(2, False), (3, True)])
def test_nguong_toi_da_2_ban(n_ban_sao: int, co_bao: bool):
    de = "Cho hai đường thẳng $a, b$ bị cắt bởi $c$ tại $A, B$. Cặp góc nào là so le trong?"
    lesson = _lesson([_problem(f"Bài {i}.", de) for i in range(1, n_ban_sao + 1)])
    assert bool(check_clone_problems(lesson)) is co_bao


# --- Lỗi 4: đề trỏ tới hình có sẵn mà không kèm hình (phiếu E BTVN 7, 8) ----
def test_bat_de_tro_toi_hinh_ma_khong_co_hinh():
    lesson = _lesson([_problem("BTVN 7.", "Hình vẽ bên minh họa cho định lý nào?")])
    viols = check_hinh_thieu(lesson)
    assert len(viols) == 1 and "KHÔNG kèm hình" in viols[0].reason


def test_de_tro_toi_hinh_va_co_hinh_thi_qua_cong():
    lesson = _lesson([_problem("BTVN 7.", "Hình vẽ bên minh họa cho định lý nào?", _tikz("a", "b"))])
    assert check_hinh_thieu(lesson) == []


# --- Lỗi 5: bắt HS tự vẽ mà chưa bật draw (Thầy: "tạo thêm chỗ cho hs vẽ") --
def test_bat_ve_hinh_ma_chua_bat_draw():
    lesson = _lesson([_problem("Bài 12.", "Vẽ hình và ghi GT, KL theo định lý trên.")])
    viols = check_hinh_thieu(lesson)
    assert len(viols) == 1 and "draw: true" in viols[0].reason


def test_bat_ve_hinh_da_bat_draw_thi_qua_cong():
    p = _problem("Bài 12.", "Vẽ hình và ghi GT, KL theo định lý trên.")
    p["draw"] = True
    assert check_hinh_thieu(_lesson([p])) == []


def test_da_co_hinh_san_thi_KHONG_doi_draw():
    """'Vẽ tia Ot là tia phân giác' trong bài ĐÃ CÓ HÌNH vẽ sẵn tia Ot → không phải
    việc của HS, không được báo nhầm."""
    lesson = _lesson([_problem(
        "Bài 16.", r"Cho $\widehat{xOy} = 110^\circ$ (hình vẽ). Vẽ tia $Ot$ là tia phân giác.",
        _tikz("x", "y", "t", "O"))])
    assert check_hinh_thieu(lesson) == []
