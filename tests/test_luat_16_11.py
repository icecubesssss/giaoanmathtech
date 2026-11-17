"""Luật hình thức câu + bản chất 40-40-20 (Thầy chốt 16/11/2026, AGENTS.md khối đầu file).

Phiếu/thuyết minh khai `luat_16_11: true` thì:
  • dan_dat_gate CHẶN ô điền / khung "hoàn thành bài giải" trong bài tập (chỉ Ví dụ được điền);
  • dan_dat_gate CHẶN gợi ý ở bài VD (VD = chỉ đề);
  • vi_du_gate nhận câu hỏi dẫn [NB] trong đề TH thay cho `hints`;
  • thuyetminh_gate bỏ mốc "NB tách TH 30–40%" (quy trình 30/10);
  • tier_spec có khuôn "khong_vd" (40-60-0) cho phiếu cố ý không VD;
  • spec_gate soi cờ `luat_16_11` + `khuon` của phiếu khớp thuyết minh.
Không khai cờ thì mọi cổng giữ hành vi cũ.
"""
import json

from src.schema import LessonPackage
from src.schema import ngan_hang_sheet as nhs
from src.schema.thuyetminh_spec import ThuyetMinhSpec
from src.schema.tier_spec import khuon_ratio, load_tier_spec
from src.validators.dan_dat_gate import (check_dan_dat_chan, check_dien_khuyet_chi_vi_du,
                                         check_vd_chi_de, la_khuon_moi)
from src.validators.spec_gate import check_spec_conformance
from src.validators.thuyetminh_gate import check_nb_theo_ppd
from src.validators.vi_du_gate import check_goi_y_thong_hieu


def _les(blocks, luat=True, **kw):
    return LessonPackage(slug="phieu-a-test", title="PT bậc hai", grade_label="Lớp 9 • Đại số",
                         class_tier="C", luat_16_11=luat,
                         stages=[{"kind": "practice1", "number": 3, "title": "Luyện tập 1",
                                  "blocks": blocks}], **kw)


def _bai(statement, label="Bài 1.", level=2, tier="onclass", **kw):
    b = {"type": "problem", "label": label, "level": level, "tier": tier, "statement": statement}
    b.update(kw)
    return b


VI_DU = {"type": "noted", "variant": "example",
         "text": r"\textbf{Ví dụ 1.} Giải $x^2-3x+2=0$. Lời giải: $\Delta=[[fill:1]]$. Vậy $x\in[[fill:\{1;2\}]]$."}


# ── dan_dat: điền khuyết chỉ trong Ví dụ ──────────────────────────────────────
def test_bai_tap_co_o_dien_bi_chan():
    les = _les([VI_DU, _bai(r"Giải $x^2-5x+6=0$.[[br]]$\Delta=[[blank:1.5cm]]$")])
    m = check_dien_khuyet_chi_vi_du(les)
    assert len(m) == 1 and "Bài 1" in m[0] and "CHỈ trong Ví dụ" in m[0]


def test_btvn_khung_hoan_thanh_bai_giai_bi_chan():
    les = _les([_bai("Điền vào chỗ chấm để hoàn thành bài giải: …", label="Bài 9.", tier="btvn")])
    assert any("Bài 9 (BTVN)" in m for m in check_dien_khuyet_chi_vi_du(les))


def test_vi_du_dien_khuyet_va_bai_tu_trinh_bay_thi_qua():
    les = _les([VI_DU, _bai(r"Giải các phương trình: a) [TH] $x^2-5x+6=0$; b) [TH] $2x^2+x-3=0$.")])
    assert check_dien_khuyet_chi_vi_du(les) == []


def test_phieu_cu_khong_co_co_thi_khong_soi():
    les = _les([_bai(r"$\Delta=[[blank:1.5cm]]$")], luat=False)
    assert check_dien_khuyet_chi_vi_du(les) == [] and check_vd_chi_de(les) == []


# ── dan_dat: VD chỉ đề ───────────────────────────────────────────────────────
def test_vd_co_hints_bi_chan():
    les = _les([_bai("[VD] Tìm $m$ để $x_1^2+x_2^2=10$.", level=3, hints=["Dùng Viète"])])
    assert any("VD = CHỈ ĐỀ" in m for m in check_vd_chi_de(les))


def test_vd_khong_the_level_3_co_goi_y_trong_de_bi_chan():
    les = _les([_bai("Tìm $m$ để $x_1^2+x_2^2=10$. Gợi ý: dùng Viète.", level=3)])
    assert check_vd_chi_de(les)


def test_vd_tach_buoc_th_co_cau_dan_thi_qua():
    """Bài VD hạ thành TH bằng câu hỏi định hướng — thẻ [TH] ⇒ không phải VD, được dẫn."""
    les = _les([_bai("Cho PT … a) [NB] Điều kiện có hai nghiệm? b) [TH] Tính $x_1+x_2$ theo $m$.",
                     level=3, hints=["Viết Viète trước"])])
    assert check_vd_chi_de(les) == []


def test_vd_chi_de_thi_qua():
    les = _les([_bai("[VD] Tìm $m$ để $x_1^2+x_2^2=10$.", level=3)])
    assert check_vd_chi_de(les) == []


def test_co_luat_la_khuon_moi_nen_chan_that():
    les = _les([_bai(r"$\Delta=[[blank:1.5cm]]$")])
    assert la_khuon_moi(les) and check_dan_dat_chan(les)


# ── vi_du_gate: câu hỏi dẫn [NB] trong đề TH là gợi ý ────────────────────────
def test_th_co_cau_dan_nb_trong_de_khong_doi_hints():
    st = "Cho $x^2-2(m+1)x+m^2=0$.[[br]]a) [NB] Hệ số $a,b,c$ là gì?[[br]]b) [TH] Tìm $m$ để PT có hai nghiệm."
    assert check_goi_y_thong_hieu(_les([_bai(st)])) == []


def test_th_khong_co_dan_van_bi_nhac():
    m = check_goi_y_thong_hieu(_les([_bai("[TH] Tìm $m$ để PT có hai nghiệm.")]))
    assert m and "luật 16/11" in m[0]


def test_phieu_cu_van_doi_hints():
    st = "a) [NB] Hệ số? b) [TH] Tìm $m$."
    assert check_goi_y_thong_hieu(_les([_bai(st)], luat=False))


# ── thuyetminh: bỏ mốc NB tách TH 30–40% ─────────────────────────────────────
def _r(band, loai, n=4, refs=()):
    return {"dang": f"{band} {loai}", "band": band, "onclass": n, "loai": loai, "source_refs": list(refs)}


def _spec(luat, **kw):
    rows = [_r("NB", "NB kiến thức cũ", 1), _r("NB", "NB tách TH", 20, ["ck1-a-2"]),
            _r("TH", "TH ghép bài", 4, ["ck1-a-2"])]
    return ThuyetMinhSpec(slug="thuyet-minh-lop-9c-chuong-06-x", title="T", grade="lop-9",
                          subject="dai-so", tier="C", luat_16_11=luat,
                          phieu=[{"code": "A", "title": "P1", "rows": rows, **kw}])


def test_tm_luat_16_11_bo_moc_30_40(tmp_path, monkeypatch):
    monkeypatch.setattr(nhs, "SNAP_DIR", tmp_path)
    nhs._CACHE.clear()
    assert not any("30–40%" in m for m in check_nb_theo_ppd(_spec(True))[1])
    assert any("30–40%" in m for m in check_nb_theo_ppd(_spec(False))[1])   # chương cũ giữ mốc


def test_khuon_khong_vd_40_60():
    r = khuon_ratio(load_tier_spec(), "lop-9", "dai-so", "C", "khong_vd")
    assert r == {"NB": 40, "TH": 60, "VD": 0, "VDC": 0}


# ── spec_gate: cờ + khuôn khớp thuyết minh ───────────────────────────────────
def _ghi_tm(tmp_path, luat, khuon=""):
    spec = _spec(luat, **({"khuon": khuon} if khuon else {})).model_dump()
    (tmp_path / "thuyet-minh.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")


def test_spec_gate_co_luat_lech_thi_keu(tmp_path):
    _ghi_tm(tmp_path, True, "khong_vd")
    w = check_spec_conformance(_les([_bai("x", dang_id="NB1")], luat=False), tmp_path / "phieu-a-test.json")
    assert any("luat_16_11" in m for m in w) and any("`khuon` lệch" in m for m in w)


def test_spec_gate_co_luat_khop_thi_im(tmp_path):
    _ghi_tm(tmp_path, True, "khong_vd")
    les = _les([_bai("x", dang_id="NB1")], khuon="khong_vd")
    w = check_spec_conformance(les, tmp_path / "phieu-a-test.json")
    assert not any("luat_16_11" in m or "`khuon` lệch" in m for m in w)


# ── trinh_bay: thụt dòng con \hspace*{1.4em} đầu dòng là kiểu đã duyệt (12/11/2026) ──
def test_nhip_loi_giai_bo_qua_thut_dau_dong():
    from src.validators.trinh_bay_gate import check_nhip_loi_giai
    sol = (r"Ta có $\Delta=25>0$ nên phương trình có hai nghiệm phân biệt[[br]]"
           r"\hspace*{1.4em}$x_1=2$ và $x_2=3$.[[br]]\hspace*{1.4em}Vậy phương trình có hai nghiệm $x_1=2$ và $x_2=3$.")
    assert check_nhip_loi_giai(_les([_bai("[TH] Giải $x^2-5x+6=0$.", solution=sol)])) == []


def test_nhip_loi_giai_van_bat_suy_ra_va_vay_dinh_dong():
    from src.validators.trinh_bay_gate import check_nhip_loi_giai
    sol = r"\hspace*{1.4em}$\Delta>0$, suy ra hai nghiệm. Vậy $x=2$."
    m = check_nhip_loi_giai(_les([_bai("[TH] Giải $x^2-5x+6=0$.", solution=sol)]))
    assert m and "nối lời dài" in m[0] and "dính dòng trên" in m[0]


# ── renderer: thẻ mức sau nhãn ý in thành sao (Thầy 16/11/2026 "các câu a, b, c, d cần đánh dấu mức độ") ──
def test_the_muc_sau_y_in_thanh_sao():
    from src.compiler.jinja_renderer import _texify
    t = _texify(r"Cho PT.[[br]]a) [NB] Tính $\Delta$.[[br]]b) [TH] Giải.[[br]]c) [VD] Tìm $m$.")
    assert r"a)~\diffstars{1}" in t and r"b)~\diffstars{2}" in t and r"c)~\diffstars{3}" in t
    assert "[NB]" not in t and "NB" not in t


def test_the_dau_de_bai_mot_y_van_xoa():
    from src.compiler.jinja_renderer import _texify
    assert _texify("[NB] Các nghiệm của phương trình là") == "Các nghiệm của phương trình là"
