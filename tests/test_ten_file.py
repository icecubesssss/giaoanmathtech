"""ten_file — tên PDF thành phẩm phải tự nói ra mình là bài gì (Thầy chốt 06/09/2026).

Thầy gửi hàng loạt PDF vào Zalo: người nhận chỉ thấy TÊN FILE, không thấy thư mục.
Trước đây mọi thư mục đều đẻ ra `ca-01-handout.pdf` nên cả kho trùng tên nhau.
"""
from src.exporters.ten_file import bo_dau, ten_ban_in
from src.schema import LessonPackage


def _les(slug="phieu-a-on-tap-hbh-hcn", tier="B", grade_label="Lớp 8 • Chương III. Tứ giác"):
    return LessonPackage(slug=slug, title="t", class_tier=tier, grade_label=grade_label,
                         stages=[{"kind": "practice1", "number": 3, "title": "LT", "blocks": []}])


_SEED = ("inputs/seeds/lop-8/hinh-hoc/lop-b/chuong-03-tu-giac/"
         "tuan10-on-tap-hbh-hcn/phieu-a-on-tap-hbh-hcn.json")


def test_du_khoi_tuan_ten_bai_va_ban_in():
    assert ten_ban_in(_les(), _SEED, "handout") == "Toan8B-Tuan10-On-tap-hbh-hcn-Phieu-HS"
    assert ten_ban_in(_les(), _SEED, "guide") == "Toan8B-Tuan10-On-tap-hbh-hcn-Dap-an-GV"
    assert ten_ban_in(_les(), _SEED, "slide") == "Toan8B-Tuan10-On-tap-hbh-hcn-Slide"


def test_hai_phieu_cung_thu_muc_khong_dung_ten():
    """Thư mục nhiều phiếu: tên lấy theo slug PHIẾU nên không bao giờ đè nhau."""
    seed = "inputs/seeds/lop-9/dai-so/lop-c/[C]tuan10-11-bpt/phieu-{}.json"
    a = ten_ban_in(_les("phieu-a-giai-bpt", "C", "Lớp 9 • Đại số"), seed.format("a"), "handout")
    b = ten_ban_in(_les("phieu-b-toan-thuc-te", "C", "Lớp 9 • Đại số"), seed.format("b"), "handout")
    assert a == "Toan9C-Tuan10-11-Giai-bpt-Phieu-HS"
    assert b == "Toan9C-Tuan10-11-Toan-thuc-te-Phieu-HS"


def test_thieu_du_kien_thi_lui_ve_ten_cu():
    """Seed ngoài cây tuần (không đọc được số tuần) → giữ 'ca-NN-…', không đoán bừa."""
    assert ten_ban_in(_les(), "inputs/seeds/lop-8/le-te.json", "handout",
                      ca_pre="ca-01-") == "ca-01-handout"
    assert ten_ban_in(_les(), None, "guide", ca_pre="ca-02-") == "ca-02-guide"


def test_ten_khong_dau_va_khong_ky_tu_la():
    assert bo_dau("Ôn tập hình bình hành") == "On tap hinh binh hanh"
    ten = ten_ban_in(_les("phieu-a-do-dai-cung-tron"), _SEED, "handout")
    assert ten.isascii() and " " not in ten
