"""check_meta_wrap — cổng soi BẢNG ĐẦU thuyết minh có XUỐNG DÒNG đúng không.

Thầy phản hồi 14/08/2026: bảng đầu "ríu rít… có dấu bullet mà lại không xuống dòng,
thành ra RẤT KHÓ ĐỌC". Bộ test này khoá lại hành vi đó.
"""
from __future__ import annotations

from src.compiler.thuyetminh_renderer import _cell_lines, render_thuyetminh
from src.schema.thuyetminh_spec import (
    META_MARK_BEGIN, META_MARK_END, SpecPhieu, SpecRow, ThuyetMinhSpec,
)
from src.validators.thuyetminh_gate import check_meta_wrap


def _meta(rows: list[str]) -> str:
    """Dựng một khối META tối thiểu để test gate (không cần render thật)."""
    body = "\n".join(rows)
    return f"{META_MARK_BEGIN}\n\\begin{{tabular}}{{|l|l|}}\n{body}\n\\end{{tabular}}\n{META_MARK_END}"


def _spec_6_phieu() -> ThuyetMinhSpec:
    """Spec giống bản mẫu Thầy duyệt: chương 6 phiếu ⇒ ô 'Tên bài' rất dài."""
    return ThuyetMinhSpec(
        slug="thuyet-minh-test",
        title="Chương IV. Hai tam giác bằng nhau — Toán 7 Kết nối tri thức (Lớp C)",
        grade="lop-7", subject="hinh-hoc", tier="C", tuan="12-17",
        thoiluong=[
            "Buổi 1 — Bài 12: Tổng các góc trong một tam giác (1 ca)",
            "Buổi 2 — Bài 13: Hai tam giác bằng nhau, trường hợp c.c.c (1 ca)",
            "Buổi 3 — Bài 14: Trường hợp bằng nhau c.g.c và g.c.g (1 ca)",
        ],
        phieu=[
            SpecPhieu(code=str(i), title=f"Tuần {11 + i}: Tên bài khá dài của phiếu số {i} (Bài {11 + i})",
                      rows=[SpecRow(dang=f"Dạng {i}", band="NB", onclass=3)])
            for i in range(1, 7)
        ],
    )


# ── Gate bắt đúng lỗi ────────────────────────────────────────────────────────

def test_bat_nhieu_muc_ma_khong_xuong_dong():
    """Nhiều chấm đầu dòng nằm ngang trong MỘT ô ⇒ lỗi (đúng cảnh Thầy gặp)."""
    tex = _meta([r"Thời lượng & $\bullet$~Buổi 1 \quad $\bullet$~Buổi 2 \quad $\bullet$~Buổi 3 \\ \hline"])
    errs = check_meta_wrap(tex)
    assert len(errs) == 1
    assert "Thời lượng" in errs[0] and "KHÔNG xuống dòng" in errs[0]


def test_bat_doan_lien_qua_dai():
    """Không có bullet nhưng cả ô là một đoạn văn dài ⇒ vẫn phải bắt."""
    tex = _meta([r"Tên bài & " + ("Chương IV hai tam giác bằng nhau rất dài. " * 12) + r" \\ \hline"])
    errs = check_meta_wrap(tex)
    assert len(errs) == 1
    assert "đoạn liền" in errs[0] and "RẤT KHÓ ĐỌC" in errs[0]


def test_bat_dung_ten_o_bi_loi():
    """Báo lỗi phải chỉ ĐÍCH DANH ô nào, để Thầy biết sửa chỗ nào."""
    tex = _meta([
        r"Tên bài & $\bullet$~A \newline $\bullet$~B \\ \hline",
        r"Thời lượng & $\bullet$~X $\bullet$~Y $\bullet$~Z \\ \hline",
    ])
    errs = check_meta_wrap(tex)
    assert len(errs) == 1 and "Thời lượng" in errs[0]


# ── Gate KHÔNG kêu oan ───────────────────────────────────────────────────────

def test_moi_muc_mot_dong_thi_sach():
    tex = _meta([r"Tên bài & Chương IV. \newline $\bullet$~Phiếu 1 — Tuần 12 "
                 r"\newline $\bullet$~Phiếu 2 — Tuần 13 \\ \hline"])
    assert check_meta_wrap(tex) == []


def test_o_mot_muc_ngan_thi_sach():
    """Ô 'Thời gian' chỉ một câu ⇒ không có bullet, không cần xuống dòng."""
    tex = _meta([r"Thời gian & \textbf{1 ca $=$ 120 phút} (trừ giải lao 10′): "
                 r"GV giảng $\approx$30′ $+$ Luyện tập 80′. BTVN $\approx$60′ ở nhà. \\ \hline"])
    assert check_meta_wrap(tex) == []


def test_khong_co_moc_meta_thi_bo_qua_em():
    """Bản render cũ/template khác không có mốc ⇒ trả [] chứ không báo lỗi giả."""
    assert check_meta_wrap(r"\begin{tabular}{|l|l|} Tên bài & x \\ \hline \end{tabular}") == []


# ── _cell_lines + renderer thật ──────────────────────────────────────────────

def test_cell_lines_moi_muc_mot_dong():
    out = _cell_lines(["A", "B", "C"])
    assert out.count(r"\newline") == 2 and out.count(r"$\bullet$") == 3


def test_cell_lines_plain_first_khong_cham_dau_dong():
    """Dòng đầu (tên chương) là tiêu đề, không phải một mục ⇒ không có chấm."""
    out = _cell_lines(["Chương IV.", "Phiếu 1", "Phiếu 2"], plain_first=True)
    assert out.startswith("Chương IV.") and out.count(r"$\bullet$") == 2


def test_renderer_that_qua_duoc_cong():
    """Chốt end-to-end: spec 6 phiếu + 3 mục thời lượng render ra phải SẠCH cổng —
    đây chính là ca Thầy chê trước khi sửa."""
    assert check_meta_wrap(render_thuyetminh(_spec_6_phieu())) == []
