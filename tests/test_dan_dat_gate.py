"""dan_dat_gate — các góp ý Thầy nhắc khi duyệt phiếu 2 ch.V 9C (03–04/11/2026) thành cổng:
mượn hình bài trên, dễ → khó, khuôn bốn điểm, điền khuyết = khung bài giải đi thi, tiêu đề
trước BTVN; và giờ thực của khung bài giải (3′/thẻ) + dang_id nhiều mã."""
from src.schema import LessonPackage
from src.validators.dan_dat_gate import (
    check_de_den_kho, check_dich_buoi, check_khung_bai_giai, check_khuon_bon_diem,
    check_muon_hinh, check_tieu_de_truoc_btvn, la_khuon_moi)
from src.validators.duration_gate import check_duration

KG = "Điền vào chỗ chấm để hoàn thành bài giải:"
FIG = {"tikz": "\\begin{tikzpicture}\\draw (0,0)--(1,0);\\end{tikzpicture}"}


def _les(blocks, kind="practice1", **kw):
    return LessonPackage(slug="t", title="Bốn điểm", grade_label="Lớp 9 • Hình học",
                         class_tier="C", stages=[{"kind": kind, "number": 3, "title": "Luyện tập 1",
                                                  "blocks": blocks}], **kw)


def _bai(label, statement, level=1, tier="onclass", fig=None, **kw):
    b = {"type": "problem", "label": label, "level": level, "tier": tier, "statement": statement}
    if fig:
        b["figure"] = dict(FIG, caption=fig)
    b.update(kw)
    return b


# ── 1. Mượn hình ──────────────────────────────────────────────────────────────
def test_bai_duoi_dung_hinh_bai_tren_bi_chan():
    les = _les([_bai("Bài 5.", "Cho hình (Hình 5). Chứng minh…", fig="Hình 5"),
                _bai("Bài 8.", "Đề Ái Mộ — ý b (tiếp tục với Hình 5 ở Bài 5). Chứng minh…")])
    assert any("Bài 8" in m for m in check_muon_hinh(les))


def test_trinh_bay_lai_bai_tren_bi_chan():
    les = _les([_bai("Bài 10.", "Tự trình bày lại Bài 4. Chứng minh…", level=2)])
    assert check_muon_hinh(les)


def test_tro_hinh_cua_bai_khac_bi_chan():
    les = _les([_bai("Bài 1.", "Xem Hình 1.", fig="Hình 1"),
                _bai("Bài 2.", "Trên Hình 1, chứng minh…")])
    assert any("Bài 2 dùng Hình 1 của Bài 1" in m for m in check_muon_hinh(les))


def test_moi_bai_mot_hinh_thi_sach():
    les = _les([_bai("Bài 1.", "Cho … (Hình 1).", fig="Hình 1"),
                _bai("Bài 2.", "Cho … (Hình 2).", fig="Hình 2")])
    assert check_muon_hinh(les) == []


# ── 2. Dễ → khó ──────────────────────────────────────────────────────────────
def test_tut_muc_bi_chan():
    les = _les([_bai("Bài 1.", "a) x", level=2), _bai("Bài 2.", "a) x", level=1)])
    assert any("không tụt mức" in m for m in check_de_den_kho(les))


def test_hinh_thuc_quay_nguoc_trong_mach_bi_chan():
    les = _les([_bai("Bài 1.", "Chứng minh … [[blank:1cm]]"),
                _bai("Bài 2.", "Chọn: \\begin{mcq}{1}\\mcqitem{A}{x}\\end{mcq}")])
    assert any("không quay ngược" in m for m in check_de_den_kho(les))


def test_moi_mach_lai_tu_trac_nghiem_thi_sach():
    les = _les([_bai("Bài 1.", "Chọn: \\begin{mcq}{1}\\mcqitem{A}{x}\\end{mcq}"),
                _bai("Bài 2.", "Chứng minh … [[blank:1cm]]"),
                {"type": "para", "variant": "heading", "text": "Mạch 2."},
                _bai("Bài 3.", "Chọn: \\begin{mcq}{1}\\mcqitem{A}{x}\\end{mcq}"),
                _bai("Bài 4.", "Chứng minh … [[blank:1cm]]"),
                _bai("Bài 5.", "[TH] Chứng minh …", level=2)])
    assert check_de_den_kho(les) == []


def test_btvn_soi_rieng_voi_bai_tren_lop():
    les = _les([_bai("Bài 1.", "[VD] x", level=3),
                _bai("BTVN 1.", "Chứng minh … [[blank:1cm]]", tier="btvn")], kind="reflection")
    assert check_de_den_kho(les) == []


# ── 3. Khuôn bốn điểm ────────────────────────────────────────────────────────
def test_khuon_cu_goi_trung_diem_bi_chan():
    les = _les([_bai("Bài 1.", "[TH] Chứng minh bốn điểm $A$, $B$, $C$, $D$ cùng thuộc một đường tròn.", level=2,
                     answer="Gọi $I$ là trung điểm $BC$. Trung tuyến ứng với cạnh huyền bằng nửa cạnh huyền.")])
    assert check_khuon_bon_diem(les)


def test_khuon_moi_thi_sach_va_vi_du_nen_duoc_mien():
    moi = _bai("Bài 1.", "[TH] Chứng minh bốn điểm $A$, $B$, $C$, $D$ cùng thuộc một đường tròn.", level=2,
               answer="$\\triangle ABC$ vuông tại $A$[[br]]$\\Rightarrow A$, $B$, $C$ cùng thuộc đường tròn đường kính $BC$.")
    nen = {"type": "noted", "variant": "example", "text": "\\textbf{Ví dụ 1.} Chứng minh ba điểm $A$, $B$, $C$ cùng thuộc "
           "một đường tròn. Lời giải … trung tuyến ứng với cạnh huyền … \\textbf{Ghi nhớ (dùng thẳng từ nay):} …"}
    assert check_khuon_bon_diem(_les([nen, moi])) == []


# ── 4. Khung bài giải đi thi ─────────────────────────────────────────────────
def test_manh_dien_roi_bi_chan():
    les = _les([_bai("Bài 1.", "Chứng minh $DF$ là tiếp tuyến. Điền vào chỗ chấm: $FC = [[blank:1cm]]$ nên …")])
    assert any("mẩu điền rời" in m for m in check_khung_bai_giai(les))


def test_khung_hai_suy_ra_mot_dong_bi_chan():
    st = (f"Chứng minh $DB$ là tiếp tuyến. {KG}[[br]]a) [NB] $OA = OB$[[br]]"
          "$\\Rightarrow OD$ là đường trung trực $\\Rightarrow DA = [[blank:1cm]]$.[[br]]Vậy $DB$ là tiếp tuyến.")
    assert any("hai dấu ⇒" in m for m in check_khung_bai_giai(_les([_bai("Bài 1.", st)])))


def test_khung_thieu_vay_bi_chan():
    st = f"Chứng minh $DB$ là tiếp tuyến. {KG}[[br]]a) x[[br]]b) $y = [[blank:1cm]]$[[br]]c) z"
    assert any("Vậy" in m for m in check_khung_bai_giai(_les([_bai("Bài 1.", st)])))


def test_khung_dung_chuan_thi_sach():
    st = (f"Chứng minh $DB$ là tiếp tuyến. {KG}[[br]]a) [NB] $OA = OB$ $\\Rightarrow \\triangle OAB$ cân.[[br]]"
          "$\\Rightarrow DA = [[blank:1cm]]$.[[br]]b) [NB] Vậy $DB$ là [[blank:2cm]] của $(O)$.")
    assert check_khung_bai_giai(_les([_bai("Bài 1.", st)])) == []


# ── 5. Tiêu đề trước BTVN ────────────────────────────────────────────────────
def test_tieu_de_truoc_btvn_trang_rieng_bi_chan():
    les = _les([{"type": "para", "variant": "heading", "text": "Bài tập về nhà"},
                _bai("BTVN 1.", "x", tier="btvn")], kind="reflection", btvn_trang_rieng=True)
    assert check_tieu_de_truoc_btvn(les)


# ── 6. Đích của buổi + phạm vi chặn ──────────────────────────────────────────
def test_dich_tro_sai_bai_cuoi():
    les = LessonPackage(slug="t", title="t", stages=[
        {"kind": "practice1", "number": 3, "title": "LT1", "blocks": [
            {"type": "para", "text": "\\textbf{Đích của buổi học:} tự giải trọn \\textbf{Bài 13}."},
            {"type": "para", "variant": "heading", "text": "Mạch 1. Ý a"}]},
        {"kind": "practice2", "number": 4, "title": "LT2", "blocks": [_bai("Bài 8.", "[VD] x", level=3)]}])
    assert la_khuon_moi(les)
    assert any("Bài 13" in m for m in check_dich_buoi(les))


# ── Giờ thực: khung bài giải 3′/thẻ; trắc nghiệm hình sẵn lớp 9 hình C 2,5′ (Thầy 04/11/2026) ──
def test_khung_bai_giai_tinh_3_phut_moi_the():
    st = f"Chứng minh … {KG}[[br]]a) [NB] x [[blank:1cm]][[br]]b) [NB] y[[br]]Vậy z [[blank:1cm]]."
    les = _les([_bai("Bài 1.", st, figure_given=True)])
    assert any("NB 2 câu/6′" in w for w in check_duration(les))
    tn = _les([_bai("Bài 1.", "a) [NB] x b) [NB] y", figure_given=True)])
    assert any("NB 2 câu/5′" in w for w in check_duration(tn))     # lớp 9 hình C: 2,5′/câu (04/11)


def test_dang_id_nhieu_ma_chia_the_theo_band():
    from src.validators.spec_gate import _dem_theo_ma
    from src.schema.lesson_package import ProblemBlock
    p = ProblemBlock(type="problem", label="Bài 8.", level=3, tier="onclass", dang_id="TH2+VD1",
                     statement="Cho …[[br]]a) [TH] x[[br]]b) [VD] y")
    assert _dem_theo_ma(p) == {"TH2": 1, "VD1": 1}


def test_rate_rieng_tang_c_lop_9_hinh():
    from src.schema.tier_spec import load_tier_spec, rates_for
    ts = load_tier_spec()
    c, b = rates_for(ts, "lop-9", "hinh-hoc", "C"), rates_for(ts, "lop-9", "hinh-hoc", "B")
    assert c["onclass"]["TH"] == 10.0 and c["onclass"]["VD"] == 16.0 and c["_quick_minutes"] == 2.5
    assert b["onclass"]["TH"] == 6.0 and "_quick_minutes" not in b


def test_ve_tiep_cong_phut_theo_bai():
    """Hình nền + HS vẽ tiếp (Thầy 04/11/2026: +2–4′ mỗi câu) — cộng đúng số phút khai."""
    st = f"Chứng minh … {KG}[[br]]a) [NB] x [[blank:1cm]][[br]]b) [NB] y[[br]]Vậy z [[blank:1cm]]."
    les = _les([_bai("Bài 1.", st, figure_given=True, ve_tiep=3)])
    assert any("NB 2 câu/9′" in w and "3′ vẽ tiếp" in w for w in check_duration(les))


def test_de_cut_lam_tiep_y_b_bi_chan():
    """Thầy 04/11/2026: 'ra đề thì cần đầy đủ' — không viết 'Làm tiếp ý b của Bài 7'."""
    les = _les([_bai("BTVN 4.", "Làm tiếp ý b của Bài 7: Chứng minh $DF$ là tiếp tuyến.", level=3, tier="btvn")],
               kind="reflection")
    assert check_muon_hinh(les)


def test_loi_xung_ho_trong_de_bi_chan():
    from src.validators.dan_dat_gate import check_loi_xung_ho
    les = _les([_bai("Bài 7.", "Cho … (Làm ở nhà, trên hình em vẽ hôm nay.)", level=3)])
    assert check_loi_xung_ho(les)
    assert check_loi_xung_ho(_les([_bai("Bài 7.", "Cho tam giác $ABC$ … Chứng minh … Vẽ tiếp vào Hình 3.")])) == []


def test_luyen_tap_2_va_btvn_chung_minh_bi_chan():
    """Thầy chốt 04/11/2026: Luyện tập 2 và BTVN chứng minh tự luận HS phải tự vẽ hình (draw=True) và tự trình bày lời giải."""
    from src.validators.dan_dat_gate import check_luyen_tap_2_va_btvn_chung_minh
    # Điền khuyết ở Luyện tập 2 bị chặn
    les_loi_p2_blank = LessonPackage(
        slug="t", title="Bốn điểm", grade_label="Lớp 9 • Hình học", class_tier="C",
        stages=[
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "blocks": [{"type": "para", "variant": "heading", "text": "Đề thi Ái Mộ: Bài 6"}]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "blocks": [_bai("Bài 6.", f"Cho đường tròn... {KG}[[br]]Điền [[blank:1.5cm]]", level=2, draw=True)]}
        ]
    )
    assert check_luyen_tap_2_va_btvn_chung_minh(les_loi_p2_blank)

    # Không bật draw ở Luyện tập 2 bài chứng minh bị chặn
    les_loi_p2_no_draw = LessonPackage(
        slug="t", title="Bốn điểm", grade_label="Lớp 9 • Hình học", class_tier="C",
        stages=[
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "blocks": [{"type": "para", "variant": "heading", "text": "Đề thi Ái Mộ: Bài 6"}]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "blocks": [_bai("Bài 6.", "Cho đường tròn... Chứng minh $OA \\perp BC$", level=2, draw=False)]}
        ]
    )
    assert check_luyen_tap_2_va_btvn_chung_minh(les_loi_p2_no_draw)

    # Điền khuyết ở bài chứng minh BTVN bị chặn
    les_loi_btvn_blank = LessonPackage(
        slug="t", title="Bốn điểm", grade_label="Lớp 9 • Hình học", class_tier="C",
        stages=[
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "blocks": [_bai("Bài 6.", "Cho đường tròn... Chứng minh...", level=2, draw=True)]},
            {"kind": "reflection", "number": 5, "title": "Sơ đồ",
             "blocks": [_bai("BTVN 3.", f"Cho đường tròn... Chứng minh... {KG}[[br]]Điền [[blank:1cm]]", level=2, tier="btvn", draw=True)]}
        ]
    )
    assert check_luyen_tap_2_va_btvn_chung_minh(les_loi_btvn_blank)

    # Đúng chuẩn: Luyện tập 2 và BTVN chứng minh chỉ có đề và bật draw=True
    les_sach = LessonPackage(
        slug="t", title="Bốn điểm", grade_label="Lớp 9 • Hình học", class_tier="C",
        stages=[
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "blocks": [{"type": "para", "variant": "heading", "text": "Đề thi Ái Mộ: Bài 6"}]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "blocks": [_bai("Bài 6.", "Cho đường tròn... a) Chứng minh... b) Chứng minh...", level=2, draw=True)]},
            {"kind": "reflection", "number": 5, "title": "Sơ đồ",
             "blocks": [_bai("BTVN 3.", "Cho đường tròn... Chứng minh...", level=2, tier="btvn", draw=True)]}
        ]
    )
    assert check_luyen_tap_2_va_btvn_chung_minh(les_sach) == []
