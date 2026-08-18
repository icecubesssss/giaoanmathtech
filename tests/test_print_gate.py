"""print_gate — soi bố cục BẢN IN (Thầy chốt 15/08/2026).

Mấy lỗi này chỉ nhìn PDF mới thấy: đầu mục chặng nằm trơ cuối trang, trang bỏ trống.
Test gọi thẳng phần logic trên text từng trang (không cần pdftotext) để chạy nhanh.
"""
from __future__ import annotations

from unittest.mock import patch

from src.validators.print_gate import _soi_de_chu, check_print_layout

DAY = "Bài 1. Cho tam giác vuông tính cạnh huyền rồi viết bốn tỉ số lượng giác. " * 12


DAY_TRANG = 759.0          # mép dưới vùng chữ (A4, lề dưới 1,15in)
DAC = (750.0, DAY_TRANG)   # chữ chạy tới sát đáy
HUT = (400.0, DAY_TRANG)   # chữ dừng giữa chừng → hụt đáy 12,6cm


def _soi(pages: list[str], hinh: list[tuple[float, float]] | None = None) -> list[str]:
    """`hinh` = toạ độ (đáy chữ, đáy vùng chữ) từng trang; None = mọi trang đều đặc."""
    with patch("src.validators.print_gate._text_tung_trang", return_value=pages), \
         patch("src.validators.print_gate._day_chu_tung_trang",
               return_value=hinh if hinh is not None else [DAC] * len(pages)):
        return check_print_layout("x.pdf")


def test_trang_day_thi_sach():
    assert _soi([DAY, DAY, DAY]) == []


def test_bat_trang_hut_day_o_giua():
    w = _soi([DAY, "Bài 9. Tính $BC$.", DAY], [DAC, HUT, DAC])
    assert len(w) == 1 and "trang 2/3" in w[0] and "bỏ trắng" in w[0]


def test_trang_cuoi_hut_day_thi_bo_qua():
    """Tài liệu hết thì hết — không ép được, đừng kêu."""
    assert _soi([DAY, DAY, "BTVN 20. Tính $BC$."], [DAC, DAC, HUT]) == []


def test_trang_it_chu_nhung_day_dong_ke_thi_sach():
    """Phiếu HS chừa chỗ viết ⇒ trang ít chữ mà vẫn đặc. Bản cũ đếm ký tự nên kêu oan."""
    assert _soi(["Bài 9. Tính $BC$.", DAY], [DAC, DAC]) == []


def test_bat_tieu_de_chang_mo_coi():
    """Trang kết thúc bằng đầu mục mà dưới không còn bài nào."""
    w = _soi([DAY + "\n3. Luyện tập 1\n", DAY])
    assert any("MỒ CÔI" in m for m in w), w


def test_dau_muc_co_bai_ngay_duoi_thi_sach():
    w = _soi([DAY + "\n3. Luyện tập 1\n" + DAY, DAY])
    assert not any("MỒ CÔI" in m for m in w), w


CHAN = ("\nCÔNG TY CỔ PHẦN GIÁO DỤC VÀ CÔNG NGHỆ MATHTECH\n"
        "Website: www.mathtech.vn\n5\n")


def test_chan_trang_khong_duoc_tinh_la_noi_dung():
    """Ca Thầy soi 15/08/2026: '3. Luyện tập 1' trơ cuối trang mà cổng vẫn cho qua,
    vì chân trang in ở mọi trang đủ ~70 ký tự nên bị tính là 'còn bài bên dưới'."""
    w = _soi([DAY + "\n3. Luyện tập 1" + CHAN, DAY])
    assert any("MỒ CÔI" in m for m in w), w


def test_dau_muc_giua_trang_van_sach():
    """Chỉ đầu mục CHỐT trang mới mồ côi; đầu mục ở giữa trang thì kệ."""
    w = _soi(["2. Kiến thức cần nhớ\n" + DAY + "\n3. Luyện tập 1\n" + DAY + CHAN, DAY])
    assert not any("MỒ CÔI" in m for m in w), w


def _xml(*words: tuple[float, float, float, float, str]) -> str:
    o = '<page width="595.0" height="841.0">'
    for a, b, c, d, t in words:
        o += f'<word xMin="{a}" yMin="{b}" xMax="{c}" yMax="{d}">{t}</word>'
    return o + "</page>"


def test_bat_chu_de_chu():
    """Bản wrapclump hỏng 15/08/2026 tràn hộp, chữ chồng chữ mà lọt tới tận Drive."""
    r = _soi_de_chu(_xml((54, 100, 90, 112, "Bài"), (60, 104, 96, 116, "cạnh")))
    assert r and r[0][0] == 1, r


def test_dau_mu_widehat_khong_tinh_la_de():
    """'ˆ' của \\widehat{B} CỐ Ý nằm trên chữ — bản đầu kêu oan 72 chỗ ở một phiếu."""
    assert _soi_de_chu(_xml((54, 100, 62, 106, "ˆ"), (54, 103, 62, 115, "𝐵"))) == []


def test_dong_ke_cham_khong_tinh_la_de():
    assert _soi_de_chu(_xml((54, 100, 500, 112, "…"), (54, 104, 500, 116, "…"))) == []


def test_hai_dong_binh_thuong_thi_sach():
    assert _soi_de_chu(_xml((54, 100, 90, 112, "Bài"), (54, 118, 96, 130, "cạnh"))) == []


def test_khong_doc_duoc_pdf_thi_bo_qua_em():
    with patch("src.validators.print_gate._text_tung_trang", return_value=None):
        assert check_print_layout("khong-co.pdf") == []
