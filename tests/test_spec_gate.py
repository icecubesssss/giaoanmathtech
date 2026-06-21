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


def _lesson(n_nb_onclass):
    nb = " ".join(f"{c}) x" for c in "abcdefghij"[:n_nb_onclass])
    return LessonPackage(slug="phieu-a-test", title="t", class_tier="C", stages=[{
        "kind": "practice1", "number": 3, "title": "LT",
        "blocks": [{"type": "problem", "label": "Bài 1.", "tier": "onclass", "level": 1, "statement": nb}],
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
