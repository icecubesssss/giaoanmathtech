"""staleness_gate — PDF trong outputs/ có còn khớp seed + template hiện tại không?

Sinh sau ngày 19/08/2026: thuyết minh chương V nằm trên Drive 6 ngày ở bản build cũ hơn
renderer, Thầy mở ra thấy bố cục khác hẳn chương IV mà không cổng nào kêu.

Trọng tâm bộ test: đo bằng HASH nội dung, KHÔNG đo mtime — `git stash`/`checkout` sờ vào
file là đổi mtime dù nội dung y nguyên (bản đầu báo oan 4 phiếu vừa build xong).
"""
from __future__ import annotations

import hashlib
import json

from src.validators import staleness_gate as sg


def _dung_output(tmp_path, ten="ca-01-handout", tex="NOI DUNG TEX", co_sidecar=True):
    d = tmp_path / "phieu-a-test"
    d.mkdir(exist_ok=True)
    (d / f"{ten}.pdf").write_bytes(b"%PDF-1.7 gia lap")
    if co_sidecar:
        digest = hashlib.sha256(tex.encode("utf-8")).hexdigest()
        (d / f"{ten}.tex.sha256").write_text(digest, encoding="utf-8")
    return d


def _gia_lap_seed(monkeypatch, tmp_path, tex_hien_tai: dict | None):
    seed = tmp_path / "phieu-a-test.json"
    seed.write_text(json.dumps({"slug": "phieu-a-test"}), encoding="utf-8")
    monkeypatch.setattr(sg, "_seed_theo_slug", lambda: {"phieu-a-test": seed})
    monkeypatch.setattr(sg, "_tex_hien_tai", lambda _s: tex_hien_tai)
    return seed


def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ── Khớp thì im ─────────────────────────────────────────────────────────────

def test_pdf_con_khop_thi_sach(tmp_path, monkeypatch):
    d = _dung_output(tmp_path, tex="NOI DUNG TEX")
    _gia_lap_seed(monkeypatch, tmp_path, {"handout": _hash("NOI DUNG TEX")})
    assert sg.check_stale([d]) == []


# ── Ba lý do lỗi thời ───────────────────────────────────────────────────────

def test_template_doi_thi_keu_noi_dung(tmp_path, monkeypatch):
    """Đúng ca chương V: seed y nguyên, template đổi ⇒ .tex dựng lại khác bản đã build."""
    d = _dung_output(tmp_path, tex="TEX CU")
    _gia_lap_seed(monkeypatch, tmp_path, {"handout": _hash("TEX MOI SAU KHI DOI TEMPLATE")})
    w = sg.check_stale([d])
    assert len(w) == 1 and w[0].ly_do == "noi-dung"
    assert "chưa build lại" in str(w[0])


def test_thieu_sidecar_thi_keu(tmp_path, monkeypatch):
    d = _dung_output(tmp_path, co_sidecar=False)
    _gia_lap_seed(monkeypatch, tmp_path, {"handout": _hash("bat ky")})
    w = sg.check_stale([d])
    assert len(w) == 1 and w[0].ly_do == "thieu-dau"


def test_output_mo_coi_thi_keu(tmp_path, monkeypatch):
    d = _dung_output(tmp_path)
    monkeypatch.setattr(sg, "_seed_theo_slug", lambda: {})     # seed đã bị xoá
    w = sg.check_stale([d])
    assert len(w) == 1 and w[0].ly_do == "mat-nguon"
    assert "prune" in str(w[0])


# ── Không báo oan ───────────────────────────────────────────────────────────

def test_seed_dung_khong_noi_thi_khong_ket_luan(tmp_path, monkeypatch):
    """Seed hỏng/schema đổi ⇒ để schema_validator lo, cổng này im."""
    d = _dung_output(tmp_path)
    _gia_lap_seed(monkeypatch, tmp_path, None)
    assert sg.check_stale([d]) == []


def test_khong_do_bang_mtime(tmp_path, monkeypatch):
    """Chạm vào seed (như `git stash pop`) mà nội dung .tex không đổi thì KHÔNG kêu."""
    d = _dung_output(tmp_path, tex="TEX")
    seed = _gia_lap_seed(monkeypatch, tmp_path, {"handout": _hash("TEX")})
    import os
    sau = os.path.getmtime(d / "ca-01-handout.pdf") + 10_000
    os.utime(seed, (sau, sau))                                  # seed "mới" hơn PDF
    assert sg.check_stale([d]) == []


def test_thu_muc_khong_co_pdf_thi_bo_qua(tmp_path, monkeypatch):
    d = tmp_path / "phieu-a-test"
    d.mkdir()
    monkeypatch.setattr(sg, "_seed_theo_slug", lambda: {})
    assert sg.check_stale([d]) == []


# ── Nhận diện biến thể + tóm tắt ────────────────────────────────────────────

def test_nhan_dien_bien_the():
    from pathlib import Path
    assert sg._bien_the(Path("ca-01-handout.pdf")) == "handout"
    assert sg._bien_the(Path("ca-04-slide.pdf")) == "slide"
    # PDF thuyết minh đặt tên bằng chính slug, không có đuôi biến thể
    assert sg._bien_the(Path("thuyet-minh-lop-9c-chuong-05-duong-tron.pdf")) == "thuyetminh"


def test_tom_tat_dem_theo_ly_do(tmp_path):
    from pathlib import Path
    st = [sg.Stale(Path("a.pdf"), "noi-dung"), sg.Stale(Path("b.pdf"), "noi-dung"),
          sg.Stale(Path("c.pdf"), "mat-nguon")]
    s = sg.tom_tat(st)
    assert "3 PDF lỗi thời" in s and "2 noi-dung" in s and "1 mat-nguon" in s
    assert sg.tom_tat([]) == "không có"
