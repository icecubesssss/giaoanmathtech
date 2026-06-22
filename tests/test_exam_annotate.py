"""Tool gắn band/phut ngân hàng đề: khoá _cau_id (2 schema) + rubric judge."""
from scripts.exam_annotate import _cau_id
from scripts.seed_exam_bands import judge


def test_cau_id_uses_existing():
    assert _cau_id("gk1-bat-trang", {"id": "gk1-bat-trang-1a", "bai": 1}) == "gk1-bat-trang-1a"


def test_cau_id_synthesizes_from_bai_y():
    # CK1 không có id → tổng hợp {stem}-{bai}{y}
    assert _cau_id("ck1-cau-dien", {"bai": "1", "y": "a"}) == "ck1-cau-dien-1a"
    assert _cau_id("ck1-x", {"bai": 5, "y": None}) == "ck1-x-5"


def test_judge_nb_technique():
    assert judge(["DS-PT-QUYVE"], 1)[0] == "NB"          # tích = 0, 1 bước


def test_judge_th_realworld_system():
    band, phut = judge(["DS-THUCTE-LAPHE"], 2)
    assert band == "TH" and phut == 11                   # lập hệ → dài hơn band-avg


def test_judge_vdc_extremum_keeps_high_despite_low_points():
    band, phut = judge(["DS-CUCTRI"], 4)
    assert band == "VDC" and phut >= 13                  # câu chốt: giờ cao dù 0,5đ


def test_judge_dokho_raises_band():
    # thực tế lập hệ do_kho 3 → VD (cao hơn sàn TH)
    assert judge(["DS-THUCTE-LAPHE"], 3)[0] == "VD"


def test_judge_cap_on_light_dang():
    # rút gọn do_kho cao vẫn KHÔNG vượt TH (trần dạng nhẹ)
    assert judge(["DS-CAN-TINH-RUTGON"], 4)[0] == "TH"


def test_judge_multi_dang_takes_max():
    # ["cực trị","pt thực tế"] → VDC
    assert judge(["DS-PT-THUCTE", "DS-CUCTRI"], 4)[0] == "VDC"
