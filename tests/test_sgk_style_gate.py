"""sgk_style_gate + spec_gate.check_dang_mapping — Thầy chốt 14/08/2026.

Chuẩn trình bày rút từ SGK Toán 9 tập 1 KNTT (Bài 12, tr. 75-76).
Trọng tâm bộ test: KHÔNG ĐƯỢC BÁO ĐỘNG GIẢ — lần soi thô đầu tiên ra 331 "lỗi dấu
chấm thập phân" mà gần như toàn bộ là toạ độ TikZ.
"""
from __future__ import annotations

from src.schema.lesson_package import LessonPackage
from src.validators.sgk_style_gate import check_sgk_style


def _les(**kw) -> LessonPackage:
    prob = {"type": "problem", "label": "Bài 1.", "tier": "onclass", "level": 2,
            "statement": "Tính $BC$.", "solution": ""}
    prob.update(kw)
    return LessonPackage.model_validate({
        "slug": "phieu-a-test", "title": "T", "eyebrow": "e", "grade_label": "Lớp 9",
        "stages": [{"kind": "practice1", "number": 1, "title": "L", "blocks": [prob]}],
    })


# ── Khuôn 4 nhịp ─────────────────────────────────────────────────────────────

def test_loi_giai_chuan_sgk_thi_sach():
    s = (r"Xét $\triangle ABC$ vuông tại $A$. Theo định lí Pythagore, ta có "
         r"$BC = 10$ (cm). Vậy $BC = 10$ cm.")
    assert check_sgk_style(_les(solution=s)) == []


def test_thieu_cau_vay_thi_keu():
    s = r"Xét $\triangle ABC$ vuông tại $A$, ta có $BC = 10$ (cm)."
    w = check_sgk_style(_les(solution=s))
    assert len(w) == 1 and "Vậy" in w[0]


def test_thieu_can_cu_thi_keu():
    w = check_sgk_style(_les(solution=r"$BC = 10$. Vậy $BC = 10$ cm."))
    assert len(w) == 1 and "căn cứ" in w[0]


def test_bai_ly_thuyet_dung_vi_nen_van_tinh_la_co_can_cu():
    """Bài lý thuyết không có tam giác nào để 'Xét' — 'Vì … nên …' là căn cứ hợp lệ.
    (Bài 15 phiếu A từng bị kêu oan vì mẫu nhận dạng chỉ thiên về hình.)"""
    s = (r"Vì $65^\circ + 25^\circ = 90^\circ$ nên hai góc phụ nhau. "
         r"Vậy $\sin 65^\circ = \cos 25^\circ$.")
    assert check_sgk_style(_les(solution=s)) == []


def test_cau_NB_khong_bi_doi_khuon():
    """level 1 = NB gọi tên/trắc nghiệm — SGK cũng không viết 'Vậy'."""
    assert check_sgk_style(_les(level=1, solution="Cạnh huyền là $BC$.")) == []


# ── Ký hiệu ──────────────────────────────────────────────────────────────────

def test_bat_times():
    w = check_sgk_style(_les(level=1, solution=r"$AC = BC \times \sin B$."))
    assert len(w) == 1 and "cdot" in w[0]


def test_bat_dau_cham_thap_phan():
    w = check_sgk_style(_les(level=1, solution=r"$BC \approx 9.4$ cm."))
    assert len(w) == 1 and "DẤU CHẤM" in w[0]


def test_dau_phay_thap_phan_thi_sach():
    assert check_sgk_style(_les(level=1, solution=r"$BC \approx 9,4$ cm.")) == []


def test_de_bat_lam_tron_ma_khong_co_approx():
    w = check_sgk_style(_les(
        statement="Tính $BC$ (làm tròn đến chữ số thập phân thứ nhất).",
        solution=r"Xét $\triangle ABC$ vuông tại $A$, ta có $BC = 9,4$. Vậy $BC = 9,4$ cm."))
    assert len(w) == 1 and "approx" in w[0]


# ── KHÔNG báo động giả trên LaTeX/TikZ ───────────────────────────────────────

def test_toa_do_tikz_khong_bi_tinh_la_so_thap_phan():
    """Đây chính là lỗi của lần soi đầu: 331 'lỗi' hoá ra là toạ độ hình."""
    s = (r"\begin{tikzpicture}[line width=0.8pt] \draw (0,0) -- (3.2,0) -- (0,1.7) -- cycle;"
         r"\end{tikzpicture} Cạnh huyền là $BC$.")
    assert check_sgk_style(_les(level=1, solution=s)) == []


def test_do_dai_latex_khong_bi_tinh_la_so_thap_phan():
    s = r"\hspace{0.62\linewidth}\raisebox{-2.35cm}{x} Cạnh huyền là $BC$."
    assert check_sgk_style(_les(level=1, statement=s, solution="Cạnh huyền là $BC$.")) == []


def test_bai_khong_co_loi_giai_thi_bo_qua_khuon():
    assert check_sgk_style(_les(solution="")) == []


# ── Hộp hình phải tự chừa chỗ (Thầy phát hiện 14/08/2026) ────────────────────

_FIG = r"[[wrap]]\makebox[0pt][l]{\raisebox{-2.35cm}{hình}}[[/wrap]]"


def test_bat_hop_hinh_khong_chua_cho():
    """Hộp hình rộng 0 mà đề không `\\vspace` ⇒ 12 bài ngắn liên tiếp đè hình lên nhau."""
    w = check_sgk_style(_les(level=1, statement=_FIG + "Tính $BC$.", solution="$BC=1$."))
    assert len(w) == 1 and "ĐÈ LÊN" in w[0]


def test_bat_cho_chua_qua_hep():
    s = _FIG + r"Tính $BC$.\par\vspace{0.40cm}"
    w = check_sgk_style(_les(level=1, statement=s, solution="$BC=1$."))
    assert len(w) == 1 and "chỗ chừa" in w[0]


def test_chua_du_cho_thi_sach():
    s = _FIG + r"Tính $BC$.\par\vspace{1.90cm}"
    assert check_sgk_style(_les(level=1, statement=s, solution="$BC=1$.")) == []


def test_bai_khong_co_hop_hinh_thi_khong_doi_vspace():
    assert check_sgk_style(_les(level=1, statement="Tính $BC$.", solution="$BC=1$.")) == []


def test_bai_trac_nghiem_co_hinh_khong_bi_keu_oan():
    """Bốn đáp án trong \\parbox đã tự chiếm chỗ ⇒ 0,71cm là đủ, không phải lỗi."""
    s = (_FIG + r"Cạnh huyền là? \parbox[t]{0.3\linewidth}{\textbf{A.} $AB$}"
         r"\parbox[t]{0.3\linewidth}{\textbf{B.} $BC$}\par\vspace{0.71cm}")
    assert check_sgk_style(_les(level=1, statement=s, solution="Đáp án B.")) == []
