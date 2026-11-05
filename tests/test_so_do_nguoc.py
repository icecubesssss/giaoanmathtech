"""Sơ đồ ngược trong thẻ phương pháp (Thầy 05/11/2026, thử ở phiếu 2 ch.V 9C)."""
from __future__ import annotations

from src.compiler.jinja_renderer import group_slide_segments
from src.schema.lesson_package import LessonPackage, NotedBlock, ProblemBlock
from src.validators.vi_du_gate import check_goi_y_thong_hieu

TIKZ = r"\begin{tikzpicture}\node {x};\end{tikzpicture}"


def test_khoa_khong_bi_pydantic_vut():
    b = NotedBlock.model_validate({"text": "x", "variant": "theory", "so_do_nguoc": TIKZ})
    assert b.so_do_nguoc == TIKZ


def test_slide_tach_so_do_thanh_slide_rieng_ngay_sau_the():
    the = NotedBlock(text="Phương pháp", variant="theory", title="DẠNG 1. BỐN ĐIỂM", so_do_nguoc=TIKZ)
    ke = NotedBlock(text="Thẻ kế", variant="theory", title="DẠNG 2")
    segs = group_slide_segments([the, ke])
    assert [s["mode"] for s in segs] == ["textonly", "figonly", "textonly"]
    assert segs[1]["figures"][0].tikz == TIKZ
    assert "Dạng 1" in segs[1]["figures"][0].caption


def test_the_khong_khai_so_do_thi_slide_khong_doi():
    segs = group_slide_segments([NotedBlock(text="x", variant="theory", title="T")])
    assert len(segs) == 1 and not segs[0]["figures"]


def test_slide_doi_o_trong_trong_so_do_va_dat_ten_bai():
    bai = ProblemBlock(label="Bài 4.", statement="Đề", so_do_nguoc=r"\node {$[[fill:BC]]$};")
    sd = group_slide_segments([bai])[1]["figures"][0]
    assert "[[fill" not in sd.tikz and r"\fillblank" in sd.tikz
    assert "Bài 4" in sd.caption


def test_so_do_tinh_la_goi_y_cho_cau_thong_hieu():
    pack = LessonPackage.model_validate({
        "slug": "x", "title": "x", "stages": [{"kind": "practice1", "number": 3, "title": "LT", "blocks": [
            {"type": "problem", "label": "Bài 1.", "statement": "Đề", "level": 2, "so_do_nguoc": TIKZ},
            {"type": "problem", "label": "Bài 2.", "statement": "Đề", "level": 2},
        ]}]})
    loi = check_goi_y_thong_hieu(pack)
    assert len(loi) == 1 and "Bài 2" in loi[0]


def test_cong_thuc_phut_bo_nghi_them_doc_so_do():
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, "scripts")
    from phut_so_do import P, phut_co_so_do

    luat = json.loads(Path("config/khung-phan-dang/lop-9-hinh-hoc-chuong-05.json").read_text("utf-8"))["dang_y"]
    de = "[TH] Cho đường tròn $(O)$, điểm $A$, $B$, $C$, $D$. Chứng minh $AB$ là tiếp tuyến của $(O)$. Vẽ tiếp vào hình."
    tikz = r"\node[o] (a) at (0,0) {$AB$ là tiếp tuyến};"
    k = phut_co_so_do(de, tikz, "TH", luat)
    t = P["tang"]["C"]
    assert k["nghi"] == t["nghi"]["TH"]
    assert k["viet"] == round(P["so_dong"]["tiep_tuyen"] * t["phut_moi_dong"], 1)
    assert k["phut"] == round(k["doc"] + (len("AB là tiếp tuyến") / t["doc_ky_tu_phut"]) + k["viet"], 1)
    assert k["phut"] < k["binh_thuong"]


def test_phut_so_do_nhan_dang_song_song_viet_bang_latex():
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, "scripts")
    from phut_so_do import P, phut_co_so_do

    luat = json.loads(Path("config/khung-phan-dang/lop-9-hinh-hoc-chuong-05.json").read_text("utf-8"))["dang_y"]
    de = "Cho tam giác $ABC$, điểm $D$, điểm $E$. Chứng minh $AB$ là đường trung trực của $CD$. Từ đó suy ra $AB \\parallel DE$."
    k = phut_co_so_do(de, "", "TH", luat)
    assert k["viet"] == (P["so_dong"]["vuong_goc"] + P["so_dong"]["song_song"]) * P["tang"]["C"]["phut_moi_dong"]


def test_dong_thuyet_minh_dung_phut_so_do_va_tinh_gian_giao():
    from src.schema.thuyetminh_spec import SpecRow, row_minutes

    r = SpecRow(band="TH", dang="x", onclass=1, btvn=1, phut_so_do={"onclass": 9.4, "btvn": 14.1}, ve_tiep={"onclass": 3})
    m = row_minutes(r, {"onclass": {"TH": 10.0}, "btvn": {"TH": 8.7}, "vidu": {"TH": 7.0}})
    assert m["onclass"] == 12.4 and m["btvn"] == 14.1


def test_duration_tinh_phut_so_do_thay_dinh_muc():
    from src.validators.duration_gate import so_do_tally

    pack = LessonPackage.model_validate({
        "slug": "x", "title": "x", "stages": [{"kind": "practice1", "number": 3, "title": "LT", "blocks": [
            {"type": "problem", "label": "Bài 1.", "statement": "Đề", "level": 2, "tier": "onclass", "phut_so_do": 9.4},
            {"type": "problem", "label": "BTVN 1.", "statement": "Đề", "level": 2, "tier": "btvn", "phut_so_do": 14.1},
        ]}]})
    t = so_do_tally(pack)
    assert t["onclass"]["TH"] == [1, 9.4] and t["btvn"]["TH"] == [1, 14.1]


def test_cong_thuyet_minh_nhan_so_do_thay_khung_nb():
    import json
    from pathlib import Path

    from src.schema.thuyetminh_spec import ThuyetMinhSpec
    from src.validators.thuyetminh_gate import check_nb_theo_ppd, check_scaffold_rails

    p = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/thuyet-minh.json")
    spec = ThuyetMinhSpec.model_validate(json.loads(p.read_text("utf-8")))
    spec.phieu = [q for q in spec.phieu if q.code == "2"]
    assert check_scaffold_rails(spec) == []
    loi, canh_bao = check_nb_theo_ppd(spec)
    assert not [m for m in loi + canh_bao if "NB tách TH" in m]
    # bỏ sơ đồ thì cổng vẫn đòi như cũ
    for r in spec.phieu[0].rows:
        r.phut_so_do = {}
    assert check_scaffold_rails(spec)
    assert [m for m in check_nb_theo_ppd(spec)[0] if "NB tách TH" in m]
