"""Hai cổng sinh ngày 19/08/2026 sau câu hỏi của Thầy:
"sang chat mới soạn lại chương 6 thì có ra đúng output như chương 4, 5 không?"

Trước đó câu trả lời là KHÔNG — `kien_thuc_nen` và `thoiluong` không cổng nào soi và
khung `new-thuyetminh` cũng không sinh ra, nên 70/75 spec trong kho thiếu chúng.
"""
from __future__ import annotations

from src.schema.thuyetminh_spec import ThuyetMinhSpec
from src.validators.thuyetminh_gate import (check_kien_thuc_nen, check_thoiluong,
                                            goi_y_kien_thuc_nen)


def _spec(**kw) -> ThuyetMinhSpec:
    base = {
        "slug": "thuyet-minh-test", "title": "Chương X. Thử", "grade": "lop-9",
        "subject": "hinh-hoc", "tier": "C", "tuan": "01-02",
        "phieu": [{"code": "A", "title": "Buổi 1", "rows": [
            {"band": "NB", "dang": "Tính $AB$ bằng định lí Pythagore", "onclass": 3,
             "btvn": 3, "vidu": 1, "loai": "NB lẻ LT", "decompose": "none"}]}],
    }
    base.update(kw)
    return ThuyetMinhSpec.model_validate(base)


# ── Kiến thức nền ───────────────────────────────────────────────────────────

def test_thieu_kien_thuc_nen_thi_chan():
    w = check_kien_thuc_nen(_spec())
    assert len(w) == 1 and "KIẾN THỨC NỀN" in w[0]


def test_co_kien_thuc_nen_thi_sach():
    assert check_kien_thuc_nen(_spec(kien_thuc_nen=["Định lí Pythagore (Lớp 8)"])) == []


def test_khung_rong_chua_soan_thi_bo_qua():
    """Spec mới sinh, chưa có dòng nào — đừng kêu, chưa đến lúc."""
    s = _spec()
    s.phieu[0].rows = []
    assert check_kien_thuc_nen(s) == [] and check_thoiluong(s) == []


def test_tu_do_ra_nen_dang_dung_chua_khai():
    w = check_kien_thuc_nen(_spec())
    assert "Pythagore" in w[0]          # gợi ý nằm ngay trong thông báo


def test_khong_goi_y_thu_von_la_noi_dung_cua_chuong():
    """Chương dạy chính căn bậc hai thì căn bậc hai không phải 'nền'."""
    s = _spec(title="Chương III. Căn bậc hai và căn bậc ba",
              lythuyet=[r"Rút gọn biểu thức chứa căn bậc hai"], kien_thuc_nen=["x"])
    assert not any("Căn bậc hai" in g for g in goi_y_kien_thuc_nen(s))


# ── Thời lượng ──────────────────────────────────────────────────────────────

def test_thieu_thoi_luong_thi_chan():
    w = check_thoiluong(_spec(kien_thuc_nen=["x"]))
    assert len(w) == 1 and "THỜI LƯỢNG" in w[0]


def test_con_gia_dinh_kiem_tra_15_thi_chan():
    for dong in ["Buổi 2 (Bài 14): 55 phút — sau kiểm tra $15'$ đầu buổi",
                 "Buổi 3 (tuần 24): 150′ dạy (15′ KIỂM TRA đầu buổi)"]:
        w = check_thoiluong(_spec(thoiluong=[dong, "Tổng 1 ca $=$ 55 phút"]))
        assert any("KIỂM TRA 15" in x for x in w), dong


def test_tong_khong_khop_phep_cong_thi_chan():
    """Bản chương V cũ: các dòng cộng ra 520′ nhưng dòng tổng ghi 630′."""
    tl = ["Buổi 1 (Bài 13): 1 ca $=$ 90 phút", "Buổi 2 (Bài 14): 55 phút",
          r"\textbf{Tổng 2 ca $=$ 630 phút}"]
    w = check_thoiluong(_spec(thoiluong=tl))
    assert any("sai phép cộng" in x for x in w)


def test_tong_khop_thi_sach():
    tl = ["Buổi 1 (Bài 13): 1 ca $=$ 90 phút", "Buổi 2 (Bài 14): 1 ca $=$ 90 phút",
          r"\textbf{Tổng 2 ca $=$ 180 phút}"]
    assert check_thoiluong(_spec(thoiluong=tl)) == []


def test_doc_duoc_ca_dau_phut_lan_chu_phut():
    """Chương VI viết '165′', chương V viết '90 phút' — cổng phải đọc được cả hai."""
    tl = ["Ca 1 (Tuần 12): 1 ca $=$ 90′", "Ca 2 (Tuần 13): 1 ca $=$ 90′",
          "ĐỐI CHIẾU: 2 ca $=$ 180′"]
    assert check_thoiluong(_spec(thoiluong=tl)) == []


def test_chu_tong_trong_noi_dung_toan_khong_bi_nham_la_dong_tong():
    """'Tổng và hiệu hai lập phương' là tên bài SGK, không phải dòng tổng kết."""
    tl = ["Ca 1 (Tuần 13): Tổng và hiệu hai lập phương: 1 ca $=$ 90′",
          "ĐỐI CHIẾU: 1 ca $=$ 90′"]
    assert check_thoiluong(_spec(thoiluong=tl)) == []
