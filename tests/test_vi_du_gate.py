"""vi_du_gate — bốn luật Thầy chốt 21/09/2026 khi chấm phiếu chương V Hình 9B.

Trọng tâm: KHÔNG BÁO OAN. Ví dụ cùng dạng với bài là ĐÚNG luật (phải đi cùng bài);
chỉ khi ví dụ chép lại đúng đề của bài rồi đổi số mới là lỗi.
"""
from __future__ import annotations

from src.schema.lesson_package import LessonPackage
from src.validators.vi_du_gate import (check_goi_y_thong_hieu, check_vi_du_di_cung_bai,
                                       check_vi_du_dien_khuyet, check_vi_du_trung_bai)

VD_TRUNG = (r"\textbf{Ví dụ 1.} Cho đường tròn $(O; 5\text{ cm})$ và điểm $A$ với $OA = 13$ cm. "
            r"Trên đường tròn lấy điểm $B$ sao cho $AB = 12$ cm. Chứng minh $AB$ là tiếp tuyến "
            r"của $(O)$. [[br]]Lời giải[[br]]Vậy $AB$ là tiếp tuyến.")
BAI_TRUNG = (r"[TH] Cho đường tròn $(O; 8\text{ cm})$ và điểm $A$ với $OA = 17$ cm. Trên đường "
             r"tròn lấy điểm $B$ sao cho $AB = 15$ cm. Chứng minh $AB$ là tiếp tuyến của $(O)$.")
BAI_KHAC = (r"[TH] Cho hai đường tròn $(O_1; 12\text{ cm})$ và $(O_2; 5\text{ cm})$. Tính khoảng "
            r"cách $O_1O_2$ khi hai đường tròn tiếp xúc ngoài.")


def _les(blocks, slug="phieu-a-luyen-tap", title="Luyện tập chương V") -> LessonPackage:
    return LessonPackage.model_validate({
        "slug": slug, "title": title, "eyebrow": "e", "grade_label": "Lớp 9",
        "stages": [{"kind": "practice1", "number": 1, "title": "Luyện tập 1", "blocks": blocks}],
    })


def _vd(text: str) -> dict:
    return {"type": "noted", "variant": "example", "text": text}


def _bai(statement: str, label="Bài 1.", level=2, **kw) -> dict:
    b = {"type": "problem", "label": label, "statement": statement,
         "tier": "onclass", "level": level}
    b.update(kw)
    return b


# ── 1. Ví dụ giống hệt bài ───────────────────────────────────────────────────

def test_vi_du_chep_lai_de_cua_bai_thi_keu():
    w = check_vi_du_trung_bai(_les([_vd(VD_TRUNG), _bai(BAI_TRUNG)]))
    assert len(w) == 1 and "Ví dụ 1" in w[0] and "Bài 1." in w[0]


def test_vi_du_cung_dang_nhung_khac_cau_hinh_thi_sach():
    """Cùng công cụ (tiếp tuyến), khác chiều hỏi ⇒ KHÔNG phải lỗi."""
    vd = (r"\textbf{Ví dụ 1.} Cho $(O; 6\text{ cm})$, tiếp tuyến $AB$ với $AB = 8$ cm. "
          r"Tính $OA$. [[br]]Lời giải[[br]]Vậy $OA = 10$ cm.")
    assert check_vi_du_trung_bai(_les([_vd(vd), _bai(BAI_TRUNG)])) == []


def test_vi_du_va_bai_khac_dang_thi_sach():
    assert check_vi_du_trung_bai(_les([_vd(VD_TRUNG), _bai(BAI_KHAC)])) == []


def test_hop_nhac_ly_thuyet_ngan_khong_bi_soi():
    assert check_vi_du_trung_bai(_les([_vd(r"\textbf{Ví dụ 1.} Nhắc lại công thức."),
                                       _bai(BAI_TRUNG)])) == []


# ── 2. Ví dụ đi cùng bài ─────────────────────────────────────────────────────

def test_hai_vi_du_dinh_lien_nhau_thi_keu():
    w = check_vi_du_di_cung_bai(_les([_vd(VD_TRUNG), _vd(r"\textbf{Ví dụ 2.} Tính $AB$."),
                                      _bai(BAI_KHAC)]))
    assert len(w) == 1 and "Ví dụ 1" in w[0]


def test_vi_du_dung_ngay_truoc_bai_thi_sach():
    w = check_vi_du_di_cung_bai(_les([_vd(VD_TRUNG), _bai(BAI_TRUNG),
                                      _vd(r"\textbf{Ví dụ 2.} Tính $AB$."), _bai(BAI_KHAC, "Bài 2.")]))
    assert w == []


def test_vi_du_cuoi_chang_khong_con_bai_thi_keu():
    w = check_vi_du_di_cung_bai(_les([_bai(BAI_TRUNG), _vd(VD_TRUNG)]))
    assert len(w) == 1 and "không còn bài nào" in w[0]


# ── 3. Ví dụ phải là bài điền khuyết ─────────────────────────────────────────

def test_vi_du_khong_co_o_khuyet_thi_keu():
    w = check_vi_du_dien_khuyet(_les([_vd(VD_TRUNG)]))
    assert len(w) == 1 and "ĐIỀN KHUYẾT" in w[0]


def test_vi_du_du_o_fill_thi_sach():
    vd = (r"\textbf{Ví dụ 1.} Tính $AB$. [[br]]Lời giải[[br]]$AB^2 = [[fill:169]]$ nên "
          r"$AB = [[fill:13]]$ cm. [[br]]Vậy $AB = 13$ cm.")
    assert check_vi_du_dien_khuyet(_les([_vd(vd)])) == []


def test_mblank_cu_thi_nhac_doi_sang_fill():
    vd = (r"\textbf{Ví dụ 1.} Tính $AB$. [[br]]Lời giải[[br]]$AB^2 = [[mblank:1cm]]$ nên "
          r"$AB = [[mblank:1cm]]$ cm. [[br]]Vậy $AB = 13$ cm.")
    w = check_vi_du_dien_khuyet(_les([_vd(vd)]))
    assert len(w) == 1 and "[[fill:" in w[0]


# ── 4. Gợi ý ở câu Thông hiểu ────────────────────────────────────────────────

def test_phieu_luyen_tap_thieu_goi_y_thi_keu():
    w = check_goi_y_thong_hieu(_les([_bai(BAI_TRUNG, level=2)]))
    assert len(w) == 1 and "thiếu" in w[0]


def test_phieu_luyen_tap_co_goi_y_thi_sach():
    assert check_goi_y_thong_hieu(_les([_bai(BAI_TRUNG, level=2, hints=["Nối $OB$."])])) == []


def test_bai_nhan_biet_va_van_dung_khong_bi_doi_goi_y():
    les = _les([_bai(BAI_TRUNG, "Bài 1.", level=1), _bai(BAI_KHAC, "Bài 2.", level=3)])
    assert check_goi_y_thong_hieu(les) == []


def test_phieu_on_tap_cuoi_ki_con_goi_y_thi_keu():
    les = _les([_bai(BAI_TRUNG, level=2, hints=["Nối $OB$."])],
               slug="on-tap-cuoi-ki-1", title="Ôn tập cuối kì I")
    w = check_goi_y_thong_hieu(les)
    assert len(w) == 1 and "BỎ gợi ý" in w[0]


def test_phieu_on_tap_cuoi_ki_bo_goi_y_thi_sach():
    les = _les([_bai(BAI_TRUNG, level=2)], slug="on-tap-cuoi-ki-1", title="Ôn tập cuối kì I")
    assert check_goi_y_thong_hieu(les) == []


# ── 5. Ô [[fill:…]] lồng math trong math (bẫy làm Tectonic chết) ─────────────

def test_dap_an_boc_dollar_trong_math_thi_keu():
    from src.validators.vi_du_gate import check_fill_math_long_nhau
    vd = (r"\textbf{Ví dụ 1.} Tính. [[br]]Lời giải[[br]]$OA = [[fill:$\dfrac{BC}{2}$]]$. "
          r"[[br]]Vậy xong.")
    w = check_fill_math_long_nhau(_les([_vd(vd)]))
    assert len(w) == 1 and "math lồng math" in w[0]


def test_dap_an_cong_thuc_dat_ngoai_math_thi_sach():
    from src.validators.vi_du_gate import check_fill_math_long_nhau
    vd = (r"\textbf{Ví dụ 1.} Tính. [[br]]Lời giải[[br]]bán kính [[fill:$\dfrac{BC}{2}$]] và "
          r"$OA = [[fill:\dfrac{BC}{2}]]$. [[br]]Vậy xong.")
    assert check_fill_math_long_nhau(_les([_vd(vd)])) == []


# ── 6. Số trên hình lệch số trong đề ────────────────────────────────────────

VD_HINH = (r"\textbf{Ví dụ 1.} Vòm rộng $AB$, điểm cao nhất cách $AB$ một khoảng %s m. "
           r"[[br]]Lời giải[[br]]Vậy xong."
           r"\begin{tikzpicture}\draw[ink] (0,0) -- (3.2,0);"
           r"\node[left] at (0,0) {$A$};\node[above] at (1.6,0.4) {$4$ m};\end{tikzpicture}")


def test_hinh_ghi_so_de_khong_co_thi_keu():
    from src.validators.vi_du_gate import check_so_tren_hinh_vi_du
    w = check_so_tren_hinh_vi_du(_les([_vd(VD_HINH % 6)]))
    assert len(w) == 1 and "4" in w[0]


def test_hinh_ghi_dung_so_cua_de_thi_sach():
    from src.validators.vi_du_gate import check_so_tren_hinh_vi_du
    assert check_so_tren_hinh_vi_du(_les([_vd(VD_HINH % 4)])) == []


def test_nhan_ten_diem_va_toa_do_khong_bi_soi():
    from src.validators.vi_du_gate import check_so_tren_hinh_vi_du
    vd = (r"\textbf{Ví dụ 1.} Cho tam giác $ABC$. [[br]]Lời giải[[br]]Vậy xong."
          r"\begin{tikzpicture}\draw[ink] (0.5720,1.2250) circle (1.3);"
          r"\node[left] at (0,0) {$A$};\node[right] at (3.2,0) {$B$};\end{tikzpicture}")
    assert check_so_tren_hinh_vi_du(_les([_vd(vd)])) == []


def test_mat_so_dong_ho_khong_bi_bao_oan():
    """Hình mặt đồng hồ có 12 nhãn số — chi tiết của hình, không phải số liệu đề."""
    from src.validators.vi_du_gate import check_so_tren_hinh_vi_du
    nodes = "".join(rf"\node at ({i},0) {{${i}$}};" for i in range(1, 13))
    vd = (r"\textbf{Ví dụ 1.} Kim phút dài $15$ cm quay trong $20$ phút. [[br]]Lời giải[[br]]"
          r"Vậy xong.\begin{tikzpicture}" + nodes + r"\end{tikzpicture}")
    assert check_so_tren_hinh_vi_du(_les([_vd(vd)])) == []
