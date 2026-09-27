"""Cổng trình bày — mỗi test là một lỗi THẬT đã vấp khi dựng phiếu A chương V lớp 9C."""
from src.schema import LessonPackage
from src.validators.trinh_bay_gate import check_lenh_dinh_chu, check_trinh_bay

LG = r"{\sffamily\bfseries\color{brand}Lời giải}"


def _les(blocks, slug="phieu-hinh-thu", grade="Lớp 9 • Hình học"):
    return LessonPackage.model_validate({
        "slug": slug, "title": "T", "grade_label": grade,
        "stages": [{"kind": "concept", "number": 2, "title": "Kiến thức cần nhớ",
                    "blocks": blocks}]})


def test_bat_lenh_par_dinh_chu_viet():
    """`\\par` + "Đáp" = `\\parĐáp` → Tectonic chết. Đã làm gãy build thật."""
    les = _les([{"type": "problem", "label": "Bài 1.", "statement": "x",
                 "solution": r"a) 1.\parĐáp án B."}])
    assert any("dính liền chữ" in m for m in check_lenh_dinh_chu(les))


def test_bat_bfseries_dinh_chu_viet():
    les = _les([{"type": "problem", "label": "Bài 1.", "statement": r"{\bfseriesBán kính}"}])
    assert check_lenh_dinh_chu(les)


def test_lenh_ket_thuc_bang_ngoac_thi_khong_bao_oan():
    """`\\color{brand}Lời giải` là hợp lệ — lệnh đã kết bằng `}`."""
    les = _les([{"type": "problem", "label": "Bài 1.",
                 "statement": r"{\sffamily\bfseries\color{brand}Lời giải} xong."}])
    assert check_lenh_dinh_chu(les) == []


def test_bat_dong_ke_vi_hs_lam_vao_vo():
    les = _les([{"type": "para", "text": "x"}, {"type": "writelines", "count": 3}])
    assert any("dòng kẻ" in m for m in check_trinh_bay(les))


def test_khung_ve_hinh_khong_bi_bat_nham():
    """`variant: draw` là khung HS tự vẽ hình — việc khác, phải giữ."""
    les = _les([{"type": "figure", "tikz": "\\begin{tikzpicture}\\end{tikzpicture}"},
                {"type": "writelines", "count": 3, "variant": "draw"}])
    assert not any("dòng kẻ" in m for m in check_trinh_bay(les))


def test_bat_answer_va_solution_in_hai_lan():
    """Sau khi bật trường `answer`, bài có sẵn `solution` in lời giải HAI LẦN."""
    chung = r"Xét tam giác $ABC$ vuông tại $A$, theo Pythagore: $BC = 13$ cm."
    les = _les([{"type": "figure", "tikz": "\\begin{tikzpicture}\\end{tikzpicture}"},
                {"type": "problem", "label": "Bài 13.", "statement": "x",
                 "answer": chung, "solution": chung + " Vậy xong."}])
    assert any("HAI LẦN" in m for m in check_trinh_bay(les))


def test_answer_va_solution_bo_sung_nhau_thi_khong_bao_oan():
    les = _les([{"type": "figure", "tikz": "\\begin{tikzpicture}\\end{tikzpicture}"},
                {"type": "problem", "label": "Bài 1.", "statement": "x",
                 "answer": "B", "solution": r"Gọi $O$ là trung điểm $AC$, dựng đường tròn."}])
    assert not any("HAI LẦN" in m for m in check_trinh_bay(les))


def test_bat_vi_du_dien_giai_nhieu_tang():
    les = _les([{"type": "figure", "tikz": "\\begin{tikzpicture}\\end{tikzpicture}"},
                {"type": "noted", "variant": "example",
                 "text": r"\textbf{Ví dụ 1.} Đề." + LG + r" Do đó $x = 1$. Vậy $x = 1$."}])
    assert any("nhịp đi thi" in m for m in check_trinh_bay(les))


def test_bat_fill_long_math():
    les = _les([{"type": "figure", "tikz": "\\begin{tikzpicture}\\end{tikzpicture}"},
                {"type": "noted", "variant": "example",
                 "text": r"\textbf{Ví dụ 1.} Đề." + LG + r" $x = [[fill:$5$]]$. Vậy xong."}])
    assert any("math lồng math" in m for m in check_trinh_bay(les))


def test_bat_phieu_hinh_ma_ly_thuyet_khong_co_hinh():
    les = _les([{"type": "para", "text": "Đường tròn tâm $O$ bán kính $R$."}])
    assert any("KHÔNG có hình" in m for m in check_trinh_bay(les))


def test_phieu_dai_so_thi_khong_doi_hinh_o_ly_thuyet():
    les = _les([{"type": "para", "text": "x"}], slug="phieu-dai-so", grade="Lớp 9 • Đại số")
    assert not any("KHÔNG có hình" in m for m in check_trinh_bay(les))


def test_bat_suy_vuong_goc_ra_trung_diem_khong_qua_tam_giac_can():
    """Thầy 24/09: "Vuông góc đâu có suy ra được luôn H là trung điểm đâu?" — SGK KNTT
    không có định lí đường kính ⊥ dây ⇒ trung điểm; phải qua △OAB cân."""
    sai = _les([{"type": "problem", "label": "Bài 12.", "statement": "x",
                 "answer": r"Kẻ $OH \perp AB$ tại $H \Rightarrow H$ là trung điểm $AB$."}])
    assert any("SGK KNTT KHÔNG có" in m for m in check_trinh_bay(sai))
    dung = _les([{"type": "problem", "label": "Bài 12.", "statement": "x",
                  "answer": r"Kẻ $OH \perp AB$.[[br]]$\triangle OAB$ cân tại $O$, $OH \perp AB$ "
                            r"$\Rightarrow$ đường cao $OH$ đồng thời là trung tuyến $\Rightarrow H$ là trung điểm $AB$."}])
    assert not any("SGK KNTT" in m for m in check_trinh_bay(dung))


def test_bat_day_bang_nhau_cach_deu_tam_dung_nhu_dinh_li():
    sai = _les([{"type": "problem", "label": "Bài 7.", "statement": "x",
                 "answer": r"$AB = CD \Rightarrow$ hai dây cách đều tâm $\Rightarrow OK = OH$."}])
    assert any("cách đều" in m for m in check_trinh_bay(sai))


def test_duong_trung_truc_la_can_cu_hop_le():
    """A, O cùng cách đều B, C ⇒ AO là trung trực của BC (lớp 7) — không được báo oan."""
    les = _les([{"type": "problem", "label": "Bài 15.", "statement": "x",
                 "solution": r"$\Rightarrow AO$ là đường trung trực của $BC$ $\Rightarrow AO \perp BC$ tại trung điểm $H$."}])
    assert not any("SGK KNTT" in m for m in check_trinh_bay(les))
