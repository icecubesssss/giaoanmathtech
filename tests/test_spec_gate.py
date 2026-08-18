"""spec_gate — so số câu phiếu JSON với hợp đồng thuyet-minh.json (opt-in)."""
import json

from src.schema import LessonPackage
from src.validators.spec_gate import check_spec_conformance

_SPEC = {
    "slug": "tm", "title": "t", "grade": "lop-9", "subject": "dai-so", "tier": "C", "tuan": "1",
    "phieu": [{"code": "A", "title": "x", "rows": [
        {"dang": "Giải BPT", "band": "NB", "onclass": 8},
    ]}],
}


def _lesson(n_nb_onclass, dang_id="NB1"):
    """`dang_id` trỏ về dòng dạng trong thuyet-minh.json — Thầy chốt 14/08/2026:
    phiếu thật phải TƯƠNG ỨNG THẬT RÕ từng dạng, không chỉ khớp tổng theo band."""
    nb = " ".join(f"{c}) x" for c in "abcdefghij"[:n_nb_onclass])
    return LessonPackage(slug="phieu-a-test", title="t", class_tier="C", stages=[{
        "kind": "practice1", "number": 3, "title": "LT",
        "blocks": [{"type": "problem", "label": "Bài 1.", "tier": "onclass", "level": 1,
                    "statement": nb, "dang_id": dang_id}],
    }])


def test_no_spec_is_optin(tmp_path):
    # Không có thuyet-minh.json cạnh bên → bỏ qua (không cảnh báo).
    assert check_spec_conformance(_lesson(8), tmp_path / "phieu-a-test.json") == []


def test_match_ok(tmp_path):
    (tmp_path / "thuyet-minh.json").write_text(json.dumps(_SPEC), encoding="utf-8")
    assert check_spec_conformance(_lesson(8), tmp_path / "phieu-a-test.json") == []


def test_mismatch_warns(tmp_path):
    (tmp_path / "thuyet-minh.json").write_text(json.dumps(_SPEC), encoding="utf-8")
    warns = check_spec_conformance(_lesson(3), tmp_path / "phieu-a-test.json")  # 3 ≠ 8 → lệch > ±1
    assert warns and any("NB" in w and "phiếu A" in w for w in warns)


# ── Khớp theo MÃ DẠNG (Thầy chốt 14/08/2026) ─────────────────────────────────

def test_thieu_dang_id_thi_keu(tmp_path):
    """Bài không khai mã dạng ⇒ không thể đối chiếu với thuyết minh."""
    (tmp_path / "thuyet-minh.json").write_text(json.dumps(_SPEC), encoding="utf-8")
    warns = check_spec_conformance(_lesson(8, dang_id=""), tmp_path / "phieu-a-test.json")
    assert any("CHƯA khai" in w and "dang_id" in w for w in warns)


def test_ma_dang_khong_co_trong_thuyet_minh_thi_keu(tmp_path):
    (tmp_path / "thuyet-minh.json").write_text(json.dumps(_SPEC), encoding="utf-8")
    warns = check_spec_conformance(_lesson(8, dang_id="TH9"), tmp_path / "phieu-a-test.json")
    assert any("KHÔNG CÓ trong thuyết minh" in w for w in warns)


def test_dang_da_chot_ma_phieu_khong_co_bai_nao(tmp_path):
    """Spec chốt 2 dạng nhưng phiếu chỉ có bài của dạng NB1 ⇒ phải chỉ đích danh NB2."""
    spec = json.loads(json.dumps(_SPEC))
    spec["phieu"][0]["rows"].append({"dang": "Dạng bị bỏ quên", "band": "NB", "onclass": 4})
    (tmp_path / "thuyet-minh.json").write_text(json.dumps(spec), encoding="utf-8")
    warns = check_spec_conformance(_lesson(8), tmp_path / "phieu-a-test.json")
    assert any("NB2" in w and "KHÔNG có bài nào" in w for w in warns)
