"""de_gate — gác cổng THUYẾT MINH ĐỀ KIỂM TRA.

Soi hai loại lỗi mà mắt người rất dễ bỏ sót khi ra đề: cộng nhầm điểm (Σ ≠ thang điểm)
và ra đề dài hơn thời gian làm bài. Cộng thêm mấy luật riêng của tầng C.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.schema.de_spec import DeSpec, band_share, de_totals
from src.validators.de_gate import check_de

SPEC_THAT = (Path(__file__).resolve().parents[1] / "inputs" / "seeds" / "lop-9" / "dai-so" /
             "lop-c" / "chuong-06-ham-so-va-pt-bac-hai" / "de-kiem-tra.json")


def _cau(ma="Câu 1", band="NB", diem=10.0, phut=5.0, hinh_thuc="trắc nghiệm"):
    return {"ma": ma, "dang": "dạng thử", "band": band, "diem": diem,
            "phut": phut, "hinh_thuc": hinh_thuc}


def _spec(cau, phut=15, diem_toi_da=10.0):
    return DeSpec.model_validate({
        "slug": "thu", "title": "Đề thử", "grade": "lop-9", "subject": "dai-so", "tier": "C",
        "de": [{"ma": "T1", "ten": "Đề thử", "tuan": 1, "phut": phut,
                "diem_toi_da": diem_toi_da, "cau": cau}],
    })


def test_tong_diem_lech_thang_diem_bi_chan():
    errors, _ = check_de(_spec([_cau(diem=4.0), _cau(ma="Câu 2", diem=4.0)]))
    assert any("Σ điểm" in e for e in errors)


def test_tong_diem_khop_thi_khong_bao_loi_diem():
    errors, _ = check_de(_spec([_cau(diem=5.0), _cau(ma="Câu 2", diem=5.0)]))
    assert not any("Σ điểm" in e for e in errors)


def test_de_dai_hon_thoi_gian_lam_bai_bi_chan():
    errors, _ = check_de(_spec([_cau(diem=10.0, phut=20.0)], phut=15))
    assert any("VƯỢT thời gian đề" in e for e in errors)


def test_ma_cau_trung_bi_chan():
    errors, _ = check_de(_spec([_cau(diem=5.0), _cau(diem=5.0)]))
    assert any("TRÙNG" in e for e in errors)


def test_de_rong_bi_chan():
    errors, _ = check_de(_spec([]))
    assert any("RỖNG" in e for e in errors)


def test_vdc_o_tang_c_bi_chan():
    errors, _ = check_de(_spec([_cau(diem=10.0, band="VDC")]))
    assert any("VDC" in e for e in errors)


def test_de_qua_ngan_chi_canh_bao():
    errors, warns = check_de(_spec([_cau(diem=10.0, phut=3.0)], phut=15))
    assert not errors
    assert any("hơi ngắn" in w for w in warns)


def test_vd_qua_nhieu_canh_bao():
    # VD 100% thời gian, vượt xa trần (20% chuẩn tầng C + 10 điểm phần trăm).
    _, warns = check_de(_spec([_cau(diem=10.0, phut=12.0, band="VD")], phut=15))
    assert any("VD chiếm" in w for w in warns)


def test_khong_co_cau_nb_canh_bao():
    _, warns = check_de(_spec([_cau(diem=10.0, phut=12.0, band="TH")], phut=15))
    assert any("KHÔNG có câu NB" in w for w in warns)


def test_de_toan_tu_luan_canh_bao():
    _, warns = check_de(_spec([_cau(diem=10.0, phut=12.0, hinh_thuc="tự luận")], phut=15))
    assert any("100% tự luận" in w for w in warns)


def test_totals_va_band_share_khop_nhau():
    spec = _spec([_cau(diem=6.0, phut=6.0, band="NB"),
                  _cau(ma="Câu 2", diem=4.0, phut=4.0, band="TH")], phut=15)
    de = spec.de[0]
    t = de_totals(de)
    assert t["tong_diem"] == pytest.approx(10.0)
    assert t["tong_phut"] == pytest.approx(10.0)
    assert band_share(de)["NB"] == pytest.approx(60.0)


def test_spec_that_cua_chuong_6_qua_cong():
    """Thuyết minh đề chương VI trong repo phải luôn sạch — đây là bản Thầy đọc."""
    spec = DeSpec.model_validate(json.loads(SPEC_THAT.read_text(encoding="utf-8")))
    errors, warns = check_de(spec)
    assert errors == [], f"de_gate báo lỗi: {errors}"
    assert warns == [], f"de_gate cảnh báo: {warns}"


def test_spec_that_moi_de_deu_co_cau_khong_phai_tu_luan():
    """§4c — mỗi đề phải có ít nhất một câu trắc nghiệm/điền khuyết/đúng-sai."""
    spec = DeSpec.model_validate(json.loads(SPEC_THAT.read_text(encoding="utf-8")))
    for de in spec.de:
        assert any(c.hinh_thuc != "tự luận" for c in de.cau), f"đề {de.ma} toàn tự luận"
