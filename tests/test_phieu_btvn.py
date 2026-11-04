"""Phiếu BTVN tách riêng (Thầy chốt 04/11/2026: "phiếu nào tạo từ giờ cũng sẽ cắt phần BTVN
thành phiếu riêng nhé, gọi là phiếu BTVN luôn")."""
from src.compiler.jinja_renderer import co_phieu_btvn, render_btvn, render_guide, render_handout
from src.exporters.ten_file import BAN_IN
from src.schema import LessonPackage


def _les(tach=True):
    return LessonPackage(slug="t", title="Bài thử", class_tier="C", btvn_phieu_rieng=tach, stages=[
        {"kind": "practice1", "number": 3, "title": "Luyện tập 1", "blocks": [
            {"type": "problem", "label": "Bài 1.", "tier": "onclass", "level": 1, "statement": "TRENLOP xyz"}]},
        {"kind": "reflection", "number": 5, "title": "Sơ đồ tư duy", "blocks": [
            {"type": "problem", "label": "BTVN 1.", "tier": "btvn", "level": 1, "statement": "VENHA abc",
             "answer": "DAPANBTVN"}]}])


def test_phieu_hs_bo_btvn_khi_tach():
    tex = render_handout(_les())
    assert "TRENLOP" in tex and "VENHA" not in tex


def test_phieu_btvn_chi_co_btvn_va_tieu_de():
    tex = render_btvn(_les())
    assert "VENHA" in tex and "TRENLOP" not in tex and "PHIẾU BÀI TẬP VỀ NHÀ" in tex


def test_dap_an_gv_van_giu_btvn():
    assert "VENHA" in render_guide(_les()) and "DAPANBTVN" in render_guide(_les())


def test_khong_tach_thi_nhu_cu():
    les = _les(tach=False)
    assert not co_phieu_btvn(les) and "VENHA" in render_handout(les)


def test_ten_file_va_kinds():
    from src.main import _kinds_for
    assert BAN_IN["btvn"] == "Phieu-BTVN"
    assert _kinds_for(_les()) == ["handout", "guide", "slide", "btvn"]
    assert _kinds_for(_les(tach=False)) == ["handout", "guide", "slide"]


def test_new_lesson_bat_san():
    from src.main import _skeleton
    assert _skeleton("s", "t", "e", "Lớp 9")["btvn_phieu_rieng"] is True


def test_khuon_moi_thieu_tach_btvn_bi_chan():
    from src.validators.dan_dat_gate import check_phieu_btvn
    assert check_phieu_btvn(_les(tach=False)) and check_phieu_btvn(_les()) == []
