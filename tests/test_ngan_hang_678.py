"""Ngân hàng câu lớp 6-8 tầng 1 (scripts/build_ngan_hang_678.py)."""
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_ngan_hang_678 as B  # noqa: E402
from trich_cau_cuoi_de import hop_le_de_thi  # noqa: E402


def test_ten_file_nfd_van_la_de_thi():
    # macOS lưu tên tiếng Việt dạng NFD — từng làm mất 17 đề lớp 8 (14 đề CK2)
    ten = unicodedata.normalize("NFD", "(2023-2024) Đề thi HK2 - THCS Ba Đình HN.pdf")
    assert hop_le_de_thi(Path(ten))
    assert not hop_le_de_thi(Path(unicodedata.normalize("NFD", "Đề cương ôn tập HK2.pdf")))


def test_chon_chuong_lay_chuong_hoc_sau_trong_pham_vi_ky():
    nhan = B.nhan_chuong("7")
    # bài tam giác bằng nhau khớp cả "góc" (III) lẫn tam giác (IV) ⇒ lấy IV
    ch, doan = B.chon_chuong("7", "ck1", "cho tam giác abc ... chứng minh", True,
                             [nhan["III"], nhan["IV"]], nhan)
    assert ch == nhan["IV"] and doan == ""
    # chương ngoài phạm vi kỳ (IX ở GK1) không được chọn từ khoá ⇒ đoán trong phạm vi
    ch, doan = B.chon_chuong("7", "gk1", "cho tam giác abc", True, [nhan["IX"]], nhan)
    assert ch in (nhan["III"], nhan["IV"]) and doan == "theo-ky"
    # đề đảo chương: phạm vi cả năm
    ch, _ = B.chon_chuong("7", "*", "cho tam giác abc có trọng tâm g", True, [nhan["IX"]], nhan)
    assert ch == nhan["IX"]


def test_tach_y_theo_thu_tu_a_b_c():
    bai = "Bài 1 (2 điểm) Cho A = x - y\n a) Tính A tại x = 2\n b) Rút gọn\n c) Tìm x"
    ys = B.tach_y(bai)
    assert [n for n, _ in ys] == ["a", "b", "c"]
    # "a)" lạc một mình (không có b) liền sau) thì không tách
    assert len(B.tach_y("Bài 2. Tính a) giá trị")) == 1
