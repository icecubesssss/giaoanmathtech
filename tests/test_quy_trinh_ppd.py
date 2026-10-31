"""Quy trình tạo phiếu thuyết minh theo phiếu phân dạng (sếp chốt 30/10/2026).

Tab "Quy trình tạo phiếu TM theo PPD" của sheet tiến độ nhóm: phân loại câu (NB kiến thức
cũ / NB của phiếu / NB tách TH / TH của phiếu / TH ghép VD) → chạy thử thuyết minh ra cột
đề xuất → đọc VD→TH→NB, thay câu → chạy lại thuyết minh."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.schema import ngan_hang_sheet as nhs
from src.schema.thuyetminh_spec import ThuyetMinhSpec
from src.validators.thuyetminh_gate import LOAI_4B, check_loai_4b, check_nb_theo_ppd

ROOT = Path(__file__).resolve().parent.parent
HEAD = ["Bài cụ thể", "Nguồn trong input", "Mức độ", "Dạng bài", "Ưu tiên đưa vào phiếu",
        "Phân loại vào phiếu nào?", "Thời lượng làm dự kiến (phút)", "Có liên quan thực tế không?",
        "Format câu hỏi", "Mức độ từng ý", "Bài học SGK", "Ghi chú phạm vi", "Mã câu"]


def _row(ma, muc="a) TH · b) VD"):
    return ["Cho …", "Đề …", "VD", "d", "Ưu tiên 1", "Phiếu 2", "16", "Không", "Tự luận",
            muc, "Bài 16", "", ma]


def _r(band, loai, n=4, refs=()):
    return {"dang": f"{band} {loai}", "band": band, "onclass": n, "loai": loai,
            "source_refs": list(refs)}


def _spec(rows, tier="C", chuong=5):
    return ThuyetMinhSpec(slug=f"thuyet-minh-lop-9c-chuong-{chuong:02d}-x", title="T",
                          grade="lop-9", subject="hinh-hoc", tier=tier,
                          phieu=[{"code": "1", "title": "P1", "rows": rows}])


DU = [_r("NB", "NB lẻ LT", 4), _r("NB", "NB kiến thức cũ", 2),
      _r("NB", "NB tách TH", 3, ["ck1-a-2.a"]), _r("TH", "TH ghép bài", 2, ["ck1-a-2"])]


def test_nhan_moi_nb_kien_thuc_cu_hop_le():
    assert "NB kiến thức cũ" in LOAI_4B
    assert check_loai_4b(_spec(DU)) == []


def test_du_ba_loai_nb_va_ti_le_khong_canh_bao(tmp_path, monkeypatch):
    monkeypatch.setattr(nhs, "SNAP_DIR", tmp_path)
    nhs._CACHE.clear()
    assert check_nb_theo_ppd(_spec(DU)) == ([], [])          # 3/9 = 33% NB tách TH


def test_ti_le_nb_tach_th_ngoai_30_40_chi_canh_bao(tmp_path, monkeypatch):
    monkeypatch.setattr(nhs, "SNAP_DIR", tmp_path)
    nhs._CACHE.clear()
    rows = [_r("NB", "NB lẻ LT", 1), _r("NB", "NB kiến thức cũ", 1),
            _r("NB", "NB tách TH", 8, ["ck1-a-2"]), _r("TH", "TH ghép bài", 2, ["ck1-a-2"])]
    loi, cb = check_nb_theo_ppd(_spec(rows))
    assert loi == [] and any("80%" in m for m in cb)


def test_nb_tach_th_phai_lien_ket_cau_th(tmp_path, monkeypatch):
    monkeypatch.setattr(nhs, "SNAP_DIR", tmp_path)
    nhs._CACHE.clear()
    rows = DU[:2] + [_r("NB", "NB tách TH", 3, ["gk1-b-1"]), DU[3]]
    _, cb = check_nb_theo_ppd(_spec(rows))
    assert any("không trỏ bài gốc" in m and "NB3" in m for m in cb)


def test_lop_c_thieu_nb_kien_thuc_cu_chan_khi_chuong_co_tab(tmp_path, monkeypatch):
    monkeypatch.setattr(nhs, "SNAP_DIR", tmp_path)
    nhs._CACHE.clear()
    rows = [DU[0], DU[2], DU[3]]
    loi, cb = check_nb_theo_ppd(_spec(rows))                 # chưa có tab ⇒ chỉ cảnh báo
    assert loi == [] and any("NB kiến thức cũ" in m and "chỉ cảnh báo" in m for m in cb)
    p = nhs.snapshot_path("lop-9", "hinh-hoc", 5)
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(nhs.from_values([HEAD, _row("ck1-a-2")], sheet_id="x", tab="T",
                                            pulled_at="t")))
    nhs._CACHE.clear()
    loi, _ = check_nb_theo_ppd(_spec(rows))
    assert len(loi) == 1 and "NB kiến thức cũ" in loi[0]
    assert check_nb_theo_ppd(_spec(rows, tier="B"))[0] == []  # luật riêng lớp C
    nhs._CACHE.clear()


def test_ma_co_dau_cham_van_lien_ket(tmp_path, monkeypatch):
    """Mã câu thật có dấu chấm ('ck1-quoc-oai-2024-4.2') — không được cắt nhầm thành ý."""
    monkeypatch.setattr(nhs, "SNAP_DIR", tmp_path)
    p = nhs.snapshot_path("lop-9", "hinh-hoc", 5)
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(nhs.from_values([HEAD, _row("ck1-q-4.2"), _row("ck1-q-4.3")],
                                            sheet_id="x", tab="T", pulled_at="t")))
    nhs._CACHE.clear()
    rows = DU[:2] + [_r("NB", "NB tách TH", 3, ["ck1-q-4.3.a"]),
                     _r("TH", "TH ghép bài", 2, ["ck1-q-4.2"])]
    _, cb = check_nb_theo_ppd(_spec(rows))
    assert any("không trỏ bài gốc" in m for m in cb)         # 4.3 ≠ 4.2
    nhs._CACHE.clear()


def test_cot_tuy_chon_phan_loai_cau_va_de_xuat():
    snap = nhs.from_values([HEAD, _row("a-1")], sheet_id="x", tab="T", pulled_at="t")
    assert "vai" not in snap["rows"][0]                      # tab cũ 13 cột vẫn nạp được
    head = HEAD + ["Phân loại câu (vai trò)", "Đề xuất thuyết minh"]
    snap = nhs.from_values([head, _row("a-1") + ["a) TH của phiếu · b) TH ghép VD", "P1 · TH2"]],
                           sheet_id="x", tab="T", pulled_at="t")
    assert snap["rows"][0]["vai"].startswith("a) TH của phiếu")
    assert snap["rows"][0]["de_xuat"] == "P1 · TH2"


def test_lenh_de_xuat_sinh_cot_khop_hang(tmp_path):
    raw = tmp_path / "tab.json"
    raw.write_text(json.dumps({"values": [HEAD, _row("ck1-a-2"), _row(""), _row("ck1-b-1")]}))
    spec = tmp_path / "thuyet-minh.json"
    spec.write_text(_spec(DU, chuong=99).model_dump_json())
    r = subprocess.run([sys.executable, "scripts/ngan_hang_sheet.py", "de-xuat", str(raw),
                        "--spec", str(spec)], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    cot = json.loads((tmp_path / "de-xuat-cot.json").read_text())["values"]
    assert len(cot) == 4 and cot[0] == ["Đề xuất thuyết minh"]
    assert "P1 · NB3 · NB tách TH (ý a)" in cot[1][0] and "P1 · TH4" in cot[1][0]
    assert cot[2] == [""] and cot[3] == [""]
