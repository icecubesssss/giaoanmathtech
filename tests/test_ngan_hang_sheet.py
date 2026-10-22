"""Ngân hàng bài theo chương = tab phân dạng Google Sheets (Thầy chốt 22/10/2026)."""
from __future__ import annotations

import json

import pytest

from src.schema import ngan_hang_sheet as nhs
from src.schema.thuyetminh_spec import ThuyetMinhSpec
from src.validators.thuyetminh_gate import check_nguon_sheet

HEAD = ["Bài cụ thể", "Nguồn trong input", "Mức độ (cao nhất trong bài)", "Dạng bài",
        "Ưu tiên đưa vào phiếu", "Phân loại vào phiếu nào?", "Thời lượng làm dự kiến (phút)",
        "Có liên quan thực tế không?", "Format câu hỏi", "Mức độ từng ý", "Bài học SGK",
        "Ghi chú phạm vi", "Mã câu"]


def _row(ma, phieu="Phiếu 2 (tiếp tuyến)", muc="a) TH · b) VD"):
    return ["Cho …", "Đề …", "VD", "Tiếp tuyến", "Ưu tiên 1: Đề thi chính thức", phieu,
            "16", "Không", "Tự luận", muc, "Bài 16", "", ma]


def test_parse_muc_y_va_phieu():
    assert nhs.parse_muc_y("a) TH · b) VD · c) VDC") == [("a", "TH"), ("b", "VD"), ("c", "VDC")]
    assert nhs.parse_muc_y("NB") == [("", "NB")]
    assert nhs.phieu_so("Phiếu 2 (bốn điểm, tiếp tuyến); luyện tập P5–P6") == {2, 5, 6}
    assert nhs.phieu_so("Chưa có phiếu (bản 2 bỏ Bài 17)") == set()


def test_from_values_bo_hang_khong_ma_va_chan_trung():
    snap = nhs.from_values([HEAD, _row("a-1"), _row(""), _row("a-2")],
                           sheet_id="x", tab="T", pulled_at="t")
    assert [r["ma"] for r in snap["rows"]] == ["a-1", "a-2"]
    assert snap["rows"][0]["phut"] == 16.0
    with pytest.raises(ValueError, match="trùng"):
        nhs.from_values([HEAD, _row("a-1"), _row("a-1")], sheet_id="x", tab="T", pulled_at="t")


def test_resolve_cho_tro_mot_y():
    idx = {"ck1-ai-mo-2": {"ma": "ck1-ai-mo-2"}, "ck1-ban-mai-2024-6b": {"ma": "ck1-ban-mai-2024-6b"}}
    assert nhs.resolve("ck1-ai-mo-2.b", idx)
    assert nhs.resolve("ck1-ai-mo-2b", idx)
    assert nhs.resolve("ck1-ban-mai-2024-6b", idx)          # mã thật kết thúc bằng chữ
    assert nhs.resolve("ck1-khac-1", idx) is None


def _spec(refs):
    return ThuyetMinhSpec(slug="thuyet-minh-lop-9c-chuong-05-duong-tron", title="Chương V",
                          grade="lop-9", subject="hinh-hoc", tier="C",
                          phieu=[{"code": "1", "title": "P1", "rows": [
                              {"dang": "x", "band": "TH", "onclass": 1, "loai": "TH ghép bài",
                               "source_refs": refs}]}])


def test_gate_chi_boc_tu_sheet(tmp_path, monkeypatch):
    monkeypatch.setattr(nhs, "SNAP_DIR", tmp_path)
    nhs._CACHE.clear()
    # Chưa có tab của chương ⇒ cổng im (spec cũ không vỡ)
    assert check_nguon_sheet(_spec(["bat-ky"])) == []
    p = nhs.snapshot_path("lop-9", "hinh-hoc", 5)
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(nhs.from_values([HEAD, _row("ck1-ai-mo-2")],
                                            sheet_id="x", tab="Phân dạng Ch.V", pulled_at="t")))
    nhs._CACHE.clear()
    assert check_nguon_sheet(_spec(["ck1-ai-mo-2.a"])) == []
    loi = check_nguon_sheet(_spec(["ck1-ai-mo-2", "gk1-bia-1"]))
    assert len(loi) == 1 and "gk1-bia-1" in loi[0] and "Phân dạng Ch.V" in loi[0]
    nhs._CACHE.clear()


# ── Bước 0 tự động hoá (src/schema/ngan_hang_quy_trinh.py) ─────────────────────
from src.schema import ngan_hang_quy_trinh as q  # noqa: E402

KHUNG = {"luat_phieu": [
    {"nhan": "Phiếu 1 (quạt)", "bai": ["Bài 15"], "dung": True},
    {"nhan": "Chưa có phiếu", "bai": ["Bài 17"], "dung": True},
    {"nhan": "Phiếu 3 (hai tiếp tuyến)", "so": 3, "regex": "hai tiếp tuyến"},
    {"nhan": "Phiếu 4 (tích)", "so": 4, "regex": "đồng dạng"},
    {"nhan": "Phiếu 2 (tiếp tuyến)", "so": 2, "regex": "tiếp tuyến", "mac_dinh": True}],
    "nhan_luyen_tap": "luyện tập P5–P6"}


def _rec(**kw):
    r = {"id": "gk2-x-2024-IV2", "nguon": "Đề …", "file": "AGENTS.md", "uu": 1, "bai": "Bài 16",
         "de": "Cho …", "y": [["a", "TH"], ["b", "VD"]], "dang": "", "tt": False, "fmt": "Tự luận"}
    r.update(kw)
    return r


def test_gan_phieu_theo_khung():
    assert q.gan_phieu(_rec(bai="Bài 15"), KHUNG) == "Phiếu 1 (quạt)"
    assert q.gan_phieu(_rec(bai="Bài 17"), KHUNG) == "Chưa có phiếu"
    # nhiều nhãn, sắp theo số phiếu; mặc định luôn có khi regex của nó khớp
    s = q.gan_phieu(_rec(de="Kẻ hai tiếp tuyến … chứng minh đồng dạng"), KHUNG)
    assert s == "Phiếu 2 (tiếp tuyến); Phiếu 3 (hai tiếp tuyến); Phiếu 4 (tích)"
    # không nhãn nào khớp ⇒ mặc định; bài tổng hợp ⇒ thêm nhãn luyện tập
    assert q.gan_phieu(_rec(de="Cho △ABC", bai="Bài 13 (tổng hợp)"), KHUNG) == \
        "Phiếu 2 (tiếp tuyến); luyện tập P5–P6"


def test_kiem_ban_ghi_bat_loi():
    loi = q.kiem_ban_ghi([_rec(), _rec(), _rec(id="b", y=[["a", "XX"]], fmt="Lạ", file="khong/co.pdf")],
                         co_san={"gk2-x-2024-IV2"})
    s = " | ".join(loi)
    assert "id trùng trong lô" in s and "đã có trên tab" in s and "mức ý lạ" in s
    assert "fmt lạ" in s and "file không tồn tại" in s


def test_dung_hang_phut_va_thu_tu():
    rows = q.dung_hang([_rec(id="a", y=[["", "NB"]]), _rec(id="b", bai="Bài 16 (tổng hợp)",
                        y=[["a", "TH"], ["b", "VD"], ["c", "VDC"]]), _rec(id="c", de="-x")], KHUNG)
    assert [r[12] for r in rows] == ["b", "c", "a"]           # VDC trước, NB sau
    assert rows[0][6] == 6 + 10 + 13 + 5                      # tổng hợp tự luận: +5′ vẽ hình
    assert rows[0][9] == "a) TH · b) VD · c) VDC"
    assert rows[1][0] == "'-x"                                # chặn Sheets hiểu là công thức


def test_nen_giai_nen_chia_khoi_va_doi_chieu():
    rows = [["đường tròn tâm O và tiếp tuyến " * 3, "Nguồn chung dài dài dài", "VD", "d", "u", "p", 10,
             "Không", "Tự luận", "VD", "Bài 16", "", f"id{i}"] for i in range(30)]
    nen, pairs = q.nen(rows, tu_them=("đường tròn",))
    assert q.giai_nen(nen, pairs) == rows and pairs
    dai = lambda rs: sum(len(str(c)) for r in rs for c in r)  # noqa: E731 (assert-rewrite py3.9 vấp genexpr lồng)
    assert dai(nen) < dai(rows)
    khoi = q.chia_khoi(nen, 674, max_bytes=800)
    assert khoi[0]["start"] == 674 and khoi[-1]["end"] == 674 + 29
    assert all(k2["start"] == k1["end"] + 1 for k1, k2 in zip(khoi, khoi[1:]))
    fr = q.find_replace_requests(pairs, 777005, 674, 703)
    assert fr[0]["findReplace"]["range"]["startRowIndex"] == 673
    tab = [["tiêu đề"] * 13] + [[str(c) for c in r] for r in reversed(rows)]   # tab đã sắp lại
    assert q.doi_chieu(tab, rows) == []
    tab[5][3] = "sai"
    assert len(q.doi_chieu(tab, rows)) == 1
    assert q.ma_con_sot([["a ~AB~ b"]]) == 1


def test_kiem_ke_chia_viec_khong_bo_file():
    kh = q.load_khung("lop-9", "hinh-hoc", 5)
    items = q.kiem_ke(kh)
    files = {it["file"] for it in items}
    assert any("thi-thu-vao-10" in f for f in files) and kh["sgk"]["file"] in files
    per = {}
    for it in items:
        per.setdefault(it["viec"], []).append(it)
    assert all(len(v) <= q.SO_FILE_MOI_VIEC[v[0]["nhom"]] for v in per.values())
