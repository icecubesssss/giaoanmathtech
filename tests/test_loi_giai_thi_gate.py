"""Cổng đáp án "như HS đi thi" — mỗi test là một lỗi THẬT Thầy bắt ngày 01/10/2026 khi duyệt
bộ 3 đề ôn + đề GK1 lớp 9 (inputs/seeds/lop-9/de-on-tap-giua-ki-1/)."""
from src.schema import LessonPackage
from src.validators.loi_giai_thi_gate import check_loi_giai_thi

TIKZ = r"\begin{tikzpicture}\draw (0,0)--(1,0);\end{tikzpicture}"


def _de(blocks, theme="de_thi"):
    return LessonPackage.model_validate({
        "slug": "de-thu", "title": "Đề thử", "grade_label": "Lớp 9", "theme": theme,
        "stages": [{"kind": "review", "number": 1, "title": "", "blocks": blocks}]})


def _bai(solution, statement="Giải phương trình."):
    return {"type": "problem", "label": "Bài I.", "statement": statement, "solution": solution}


# ── 1. Dấu ⇔ ────────────────────────────────────────────────────────────────
def test_bat_dau_tuong_duong_trong_loi_giai():
    les = _de([_bai(r"$(x-2)(2x+6)=0\Leftrightarrow x=2$ hoặc $x=-3$.")])
    assert any("⇔" in m for m in check_loi_giai_thi(les))


def test_bat_dau_tuong_duong_trong_file_dap_an():
    """File 'Ma trận và đáp án' chứa lời giải ở khối para."""
    les = _de([{"type": "para", "text": r"$2x-6<5x \Leftrightarrow -3x<6$"}])
    assert check_loi_giai_thi(les)


def test_xuong_dong_tung_buoc_thi_qua():
    les = _de([_bai(r"$(x-2)(2x+6)=0$ [[br]] $x-2=0$ hoặc $2x+6=0$ [[br]] $x=2$ hoặc $x=-3$.")])
    assert check_loi_giai_thi(les) == []


# ── 2. Hệ thức lượng dùng trực tiếp ─────────────────────────────────────────
def test_bat_he_thuc_luong_dung_thang():
    """Bản sai thật (Ôn 3 IV.2): "△AHB vuông tại H, đường cao HM: AM·AB = AH²"."""
    les = _de([_bai(r"$\triangle AHB$ vuông tại $H$, đường cao $HM$: $AM\cdot AB=AH^2$.")])
    assert any("TRỰC TIẾP" in m for m in check_loi_giai_thi(les))


def test_bat_viet_ten_he_thuc_luong():
    """Đề tháng 9 lớp 9B: "Áp dụng hệ thức lượng trong tam giác vuông: OH·OM = OA²"."""
    les = _de([_bai(r"Áp dụng hệ thức lượng trong tam giác vuông: $OH\cdot OM=OA^2$.")])
    assert any("hệ thức lượng" in m for m in check_loi_giai_thi(les))


def test_chung_minh_dong_dang_thi_qua():
    les = _de([_bai(r"Xét $\triangle AMH$ và $\triangle AHB$: $\widehat{AMH}=\widehat{AHB}=90^\circ$, "
                    r"$\widehat{BAH}$ chung [[br]] $\Rightarrow\triangle AMH\backsim\triangle AHB$ (g.g) "
                    r"$\Rightarrow\dfrac{AM}{AH}=\dfrac{AH}{AB}\Rightarrow AM\cdot AB=AH^2$.")])
    assert check_loi_giai_thi(les) == []


def test_luu_y_cham_nhac_khong_dung_he_thuc_luong_khong_bi_bat_oan():
    les = _de([{"type": "para", "text": r"\textit{Lưu ý chấm: HS không được dùng hệ thức lượng trực tiếp.}"}])
    assert check_loi_giai_thi(les) == []


# ── 3. Bài hình phải có hình ────────────────────────────────────────────────
def test_bat_ve_hinh_dung_ma_khong_co_hinh():
    les = _de([_bai(r"Vẽ hình đúng (như hình vẽ). \hfill (0,25đ) [[br]] Xét ...")])
    assert any("KHÔNG kèm hình" in m for m in check_loi_giai_thi(les))


def test_hinh_trong_loi_giai_thi_qua():
    les = _de([_bai(r"\begin{center}" + TIKZ + r"\end{center}Vẽ hình đúng (như hình vẽ).")])
    assert check_loi_giai_thi(les) == []


def test_file_dap_an_co_khoi_figure_cung_chang_thi_qua():
    les = _de([{"type": "figure", "tikz": TIKZ}, {"type": "para", "text": "Vẽ hình đúng (như hình vẽ)."}])
    assert check_loi_giai_thi(les) == []


def test_hs_tu_ve_hinh_trong_ma_tran_khong_bi_bat_oan():
    """Đề tháng 8: "… cộng khoảng 5 phút học sinh tự vẽ hình Bài 4" — không phải lời giải."""
    les = _de([{"type": "para", "text": "Tổng thời gian ước 83 phút, cộng 5 phút học sinh tự vẽ hình Bài 4."}])
    assert check_loi_giai_thi(les) == []


# ── Phạm vi ────────────────────────────────────────────────────────────────
def test_chi_ap_cho_de_thi():
    les = _de([_bai(r"$a\Leftrightarrow b$")], theme="")
    assert check_loi_giai_thi(les) == []


def test_bo_de_on_gk1_lop9_sach_cong():
    """Bộ đề đã sửa theo góp ý phải qua cổng (chốt chặn hồi quy)."""
    import glob
    import json
    files = glob.glob("inputs/seeds/lop-9/de-on-tap-giua-ki-1/*.json")       # bản 1
    files_v2 = glob.glob("inputs/seeds/lop-9/de-on-tap-giua-ki-1-v2/*.json")  # bản 2 (rải nguồn)
    assert files and files_v2
    files += files_v2
    for f in files:
        les = LessonPackage.model_validate(json.load(open(f, encoding="utf-8")))
        assert check_loi_giai_thi(les) == [], f
