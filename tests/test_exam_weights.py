"""build_exam_weights: gom bank → trọng số tần suất; + bank loader."""
from scripts.build_exam_weights import build
from src.schema.exam_bank import load_bank, lookup


def test_weights_have_both_ky():
    w = build()["by_ky"]
    assert {"GK1", "CK1"} <= set(w)
    assert w["GK1"]["so_de"] == 10 and w["CK1"]["so_de"] == 11


def test_weight_diem_matches_freq_times_points():
    dang = build()["by_ky"]["GK1"]["dang"]
    # DS-THUCTE-LAPHE ra 100% đề GK1 → weight = diem_tb (đối chiếu ma trận cũ ~1.85)
    laphe = dang["DS-THUCTE-LAPHE"]
    assert laphe["ty_le_de"] == 100
    assert abs(laphe["weight_diem"] - laphe["diem_tb_moi_de"]) < 0.01


def test_dang_sorted_by_weight_desc():
    dang = list(build()["by_ky"]["GK1"]["dang"].values())
    ws = [d["weight_diem"] for d in dang]
    assert ws == sorted(ws, reverse=True)


def test_bank_loader_has_band_phut():
    bank = load_bank()
    # 252 câu GK1/CK1 (chương I–V) + 22 câu chương VI trích từ đề Vào 10 & đề thi thử
    # Hà Nội (19/08/2026) — GK1/CK1 học kì I không hề có phương trình bậc hai.
    assert len(bank) == 274
    rec = bank["gk1-bat-trang-1a"]
    assert rec["band"] in ("NB", "TH", "VD", "VDC") and rec["phut"] is not None


def test_bank_phu_chuong_6():
    """Thuyết minh chương VI chỉ qua `check_source_refs` khi bank có câu chương VI."""
    bank = load_bank()
    ch6 = [i for i, r in bank.items() if r.get("chuong") == "C6-PTBH"]
    assert len(ch6) >= 20
    assert bank["v10-so-2026-III3"]["band"] == "VD"


def test_lookup_skips_unknown():
    got = lookup(["gk1-bat-trang-1a", "khong-co-id-nay"])
    assert [i for i, _ in got] == ["gk1-bat-trang-1a"]
