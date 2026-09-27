"""Cổng sinh ra từ góp ý chương V lớp 9C (26/09/2026) — mỗi test là một lỗi người chấm gạch.

1. "Thời gian ca này là 45p + 45p kiểm tra" + LUẬT CỨNG "kiểm tra chương 45 phút cuối mỗi
   chương" → `check_kiem_tra_chuong` + `kiem_tra_phut` co quỹ buổi.
2. "Vẫn còn các chữ NB, TH, VD bên cạnh các bài ⇒ cần xoá" → renderer bỏ thẻ mức khi in.
3. "Các bài ví dụ phần kết luận chính là phần học sinh cần điền" → `check_vi_du_ket_luan`.
4. "Ví dụ 6: phần trên hỏi phần dưới cho đáp án" → `check_vi_du_lo_dap_an`.
5. "Tránh để tên điểm bị đường thẳng đè qua" → `nhan_hinh_gate`.
"""
from __future__ import annotations

from src.compiler.jinja_renderer import _texify
from src.schema import LessonPackage
from src.schema.thuyetminh_spec import ThuyetMinhSpec, he_so_con_lai
from src.validators.duration_gate import check_duration
from src.validators.nhan_hinh_gate import check_nhan_hinh, nhan_bi_de
from src.validators.thuyetminh_gate import check_kiem_tra_chuong, check_thuyetminh
from src.validators.vi_du_gate import check_vi_du_ket_luan, check_vi_du_lo_dap_an

LG = r"{\sffamily\bfseries\color{brand}Lời giải}"


# ── 1. Kiểm tra chương 45′ ───────────────────────────────────────────────────
def _row(band="NB", n=3):
    return {"band": band, "dang": "Tính $AB$", "onclass": n, "btvn": n, "vidu": 1,
            "loai": "NB lẻ LT", "decompose": "none"}


def _spec_chuong(so_phieu=3, kt=0, thoiluong=None):
    phieu = [{"code": str(i + 1), "title": f"Buổi {i + 1}", "rows": [_row()]} for i in range(so_phieu)]
    phieu[-1]["kiem_tra_phut"] = kt
    return ThuyetMinhSpec.model_validate({
        "slug": "thuyet-minh-chuong-thu", "title": "Chương X. Thử", "grade": "lop-9",
        "subject": "hinh-hoc", "tier": "C", "phieu": phieu,
        "thoiluong": thoiluong or [f"Buổi {i + 1}: 1 ca $=$ 90 phút" for i in range(so_phieu)]})


def test_ke_hoach_ca_chuong_thieu_kiem_tra_thi_chan():
    w = check_kiem_tra_chuong(_spec_chuong(kt=0))
    assert any("THIẾU KIỂM TRA CHƯƠNG" in m for m in w)


def test_phieu_cuoi_khai_45_phut_va_thoi_luong_ghi_ro_thi_sach():
    tl = ["Buổi 1: 1 ca $=$ 90 phút", "Buổi 2: 1 ca $=$ 90 phút",
          "Buổi 3: 1 ca $=$ 90 phút $=$ 45 phút luyện tập $+$ 45 phút kiểm tra chương"]
    assert check_kiem_tra_chuong(_spec_chuong(kt=45, thoiluong=tl)) == []


def test_thoi_luong_khong_ghi_buoi_kiem_tra_thi_nhac():
    w = check_kiem_tra_chuong(_spec_chuong(kt=45))
    assert any("THỜI LƯỢNG" in m for m in w)


def test_spec_theo_tuan_mot_hai_phieu_khong_bi_ep():
    assert check_kiem_tra_chuong(_spec_chuong(so_phieu=2, kt=0)) == []


def test_luat_kiem_tra_la_loi_chan_build():
    errors, _ = check_thuyetminh(_spec_chuong(kt=0))
    assert any("THIẾU KIỂM TRA CHƯƠNG" in e for e in errors)


def test_he_so_con_lai_cua_buoi_co_kiem_tra():
    assert he_so_con_lai(90, 1, 45) == 0.5
    assert he_so_con_lai(90, 1, 0) == 1.0
    assert he_so_con_lai(90, 2, 45) == 0.75


def _phieu_27_phut(kt):
    """9 NB hình sẵn + 2 TH + 1 VD điền khuyết ≈ 27′ — đúng quỹ buổi còn 45′."""
    bai = [{"type": "problem", "label": f"Bài {i}.", "level": 1, "tier": "onclass",
            "figure_given": True, "statement": "[NB] x"} for i in range(1, 10)]
    bai += [{"type": "problem", "label": f"Bài {i}.", "level": 2, "tier": "onclass",
             "statement": "[TH] y", "hints": ["?"]} for i in (10, 11)]
    bai += [{"type": "problem", "label": "Bài 12.", "level": 3, "tier": "onclass",
             "figure_given": True, "statement": "[VD] z"}]
    return LessonPackage.model_validate({
        "slug": "phieu-7-thu", "title": "T", "grade_label": "Lớp 9 • Hình học", "class_tier": "C",
        "kiem_tra_phut": kt,
        "stages": [{"kind": "practice1", "number": 3, "title": "Luyện tập 1", "blocks": bai}]})


def test_duration_gate_co_quy_theo_phan_con_lai_sau_kiem_tra():
    """Không khai `kiem_tra_phut` thì phiếu 45′ bị kêu oan "lệch quỹ 55′"."""
    assert any("lệch quỹ" in w and "Luyện tập" in w for w in check_duration(_phieu_27_phut(0)))
    assert not any("lệch quỹ" in w and "Luyện tập" in w for w in check_duration(_phieu_27_phut(45)))


# ── 2. Thẻ mức độ không in ra ────────────────────────────────────────────────
def test_the_muc_do_bi_xoa_khi_in():
    s = _texify("a) [NB] Tính $x$. [[br]]b) [TH] Rút gọn. [VD] c) [VDC] d)")
    assert "[NB]" not in s and "[TH]" not in s and "[VD]" not in s and "[VDC]" not in s
    assert "Tính $x$" in s


# ── 3–4. Ví dụ: kết luận là chỗ điền, phía dưới không lộ đáp án ───────────────
def _vi_du(loi_giai):
    return LessonPackage.model_validate({
        "slug": "phieu-thu", "title": "T", "grade_label": "Lớp 9",
        "stages": [{"kind": "practice1", "number": 3, "title": "Luyện tập 1", "blocks": [
            {"type": "noted", "variant": "example",
             "text": rf"\textbf{{Ví dụ 6.}} Tính độ sâu.[[br]]{LG}[[br]]" + loi_giai}]}]})


def test_ket_luan_in_san_dap_so_thi_bat():
    les = _vi_du(r"$OH = [[fill:15]]$ (cm).[[br]]Vậy lớp nước sâu $10$ cm.")
    assert check_vi_du_ket_luan(les)


def test_ket_luan_co_o_dien_thi_sach():
    les = _vi_du(r"$OH = [[fill:15]]$ (cm).[[br]]Vậy lớp nước sâu [[fill:10]] cm.")
    assert check_vi_du_ket_luan(les) == []


def test_phan_tren_hoi_phan_duoi_cho_dap_an():
    """Ví dụ 6 phiếu 2 cũ: ô OH = 15 ở trên, dòng dưới in trần `25 - 15`."""
    les = _vi_du(r"$OH^2 = 225 \Rightarrow OH = [[fill:15]]$ (cm).[[br]]$HD = 25 - 15 = 10$ (cm).[[br]]"
                 r"Vậy sâu [[fill:10]] cm.")
    assert check_vi_du_lo_dap_an(les)


def test_so_mot_chu_so_chi_bat_khi_dung_sau_dau_bang():
    """Đáp án "2" gặp lại trong \\dfrac{AB}{2} thì không phải lộ."""
    les = _vi_du(r"$R = [[fill:2]]$ cm.[[br]]$AH = \dfrac{AB}{2}$.[[br]]Vậy $R = [[fill:2]]$ cm.")
    assert check_vi_du_lo_dap_an(les) == []


# ── 5. Nhãn điểm bị nét vẽ đè ────────────────────────────────────────────────
_TIKZ_BI_DE = (r"\begin{tikzpicture}\draw (0,0) circle (1.5);\draw[dashed] (0,0) -- (-1.2287,0.8604);"
               r"\node[above right] at (-1.2287,0.8604) {$B$};\node[below right] at (0,0) {$O$};"
               r"\draw (0,0) -- (1.2,-0.9);\end{tikzpicture}")
_TIKZ_SACH = (r"\begin{tikzpicture}\draw (0,0) circle (1.5);\draw[dashed] (0,0) -- (0.6339,1.3595);"
              r"\node[inner sep=0pt] at (0.7539,1.5673) {$A$};\end{tikzpicture}")


def test_nhan_nam_tren_duong_tron_bi_bat():
    """Hình 'OA = OB = OC = OD' phiếu 1 cũ: nhãn B đặt 'above right' rơi đúng lên đường tròn."""
    assert "$B$" in nhan_bi_de(_TIKZ_BI_DE)


def test_nhan_dat_ra_ngoai_theo_ban_kinh_thi_sach():
    assert nhan_bi_de(_TIKZ_SACH) == []


def test_nhan_nen_trang_duoc_bo_qua():
    """Số trên mặt đồng hồ có nền trắng vẽ đè lên kim — vẫn đọc được."""
    tz = (r"\begin{tikzpicture}\draw (0,0) -- (0,1.5);"
          r"\node[font=\small, fill=white, inner sep=0.5pt] at (0,1.1) {12};\end{tikzpicture}")
    assert nhan_bi_de(tz) == []


def test_check_nhan_hinh_doc_ca_hinh_ly_thuyet():
    les = LessonPackage.model_validate({
        "slug": "phieu-thu", "title": "T", "stages": [{"kind": "concept", "number": 2, "title": "K",
                                                      "blocks": [{"type": "figure", "tikz": _TIKZ_BI_DE,
                                                                  "caption": "cap"}]}]})
    assert check_nhan_hinh(les)


# ── 6. Nhịp lời giải đi thi (Thầy nhắc 27/09/2026: "chưa xuống dòng, không như HS đi thi") ──
from src.validators.trinh_bay_gate import check_nhip_loi_giai  # noqa: E402


def _bai(loi_giai, level=2, statement="[TH] Tính $OH$."):
    return LessonPackage.model_validate({
        "slug": "phieu-thu", "title": "T", "grade_label": "Lớp 9 • Hình học",
        "stages": [{"kind": "practice2", "number": 4, "title": "Luyện tập 2", "blocks": [
            {"type": "problem", "label": "Bài 1.", "level": level, "tier": "onclass",
             "statement": statement, "answer": "[[br]]".join(loi_giai)}]}]})


def test_vay_dinh_dong_tren_bi_bat():
    w = check_nhip_loi_giai(_bai([r"$AB = 2AH = 16$ (cm). Vậy $AB = 16$ cm."]))
    assert any("dính dòng trên" in m for m in w)


def test_tinh_pythagore_khong_neu_can_cu_bi_bat():
    w = check_nhip_loi_giai(_bai([r"$\triangle OAH$ vuông tại $H$: $OH^2 = 15^2 - 12^2 = 81 \Rightarrow OH = 9$ (cm).",
                                  r"Vậy $OH = 9$ cm."]))
    assert any("Pythagore" in m for m in w)


def test_hai_cau_mot_dong_va_thieu_vay_bi_bat():
    w = check_nhip_loi_giai(_bai([r"Kẻ $OH \perp AB$ tại $H$. $\triangle OAB$ cân tại $O$."]))
    assert any("nhiều bước" in m for m in w) and any("thiếu câu" in m for m in w)


def test_loi_giai_dung_nhip_thi_sach():
    ok = [r"Kẻ $OH \perp AB$ tại $H$.",
          r"$OA = OB = R \Rightarrow \triangle OAB$ cân tại $O$ $\Rightarrow H$ là trung điểm $AB$.",
          r"Xét $\triangle OAH$ vuông tại $H$, theo định lí Pythagore:",
          r"$OH^2 = OA^2 - AH^2 = 17^2 - 15^2 = 64 \Rightarrow OH = 8$ (cm).",
          r"Vậy khoảng cách từ $O$ đến $AB$ bằng $8$ cm."]
    assert check_nhip_loi_giai(_bai(ok)) == []


def test_bai_khung_dien_khuyet_chi_soi_de_khong_soi_dap_an():
    """`answer` của bài khung điền khuyết là đáp án từng ô, không phải bài giải."""
    assert check_nhip_loi_giai(_bai([r"a) $90^\circ$; $I$."], level=3,
                                    statement="[VD] a) $\\widehat{ABO} =$ [[blank:1.6cm]].")) == []
