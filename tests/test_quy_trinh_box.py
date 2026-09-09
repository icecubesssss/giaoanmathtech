"""Hộp QUY TRÌNH GIẢI in trên phiếu HS phải ra LaTeX biên dịch được.

Bug bắt được 06/09/2026 khi dựng phiếu tầng B tuần 10 lớp 8: template nối các bước
bằng `\\par`, mà `trim_blocks` của Jinja nuốt dấu xuống dòng ngay sau `endif`, nên
LaTeX sinh ra là `…chứng minh.\\parBước 2 —`. TeX đọc `\\parB` là một lệnh — không
tồn tại — và Tectonic chết ngay ở bài VD đầu tiên.

Hộp Gợi ý thoát nạn thuần tuý vì mỗi ý của nó mở đầu bằng `\\textbullet`, nên
`\\par\\textbullet` vẫn tách lệnh đúng. `quy_trinh` là trường BẮT BUỘC của mọi bài
VD tầng B (Thầy chốt 30/08/2026) nên lỗi này chặn cả luật mới.
"""
import re

from src.compiler.jinja_renderer import render_handout
from src.schema import LessonPackage


def _than_hop(tex: str, ten: str) -> str:
    """Ruột một hộp tcolorbox trong phần thân phiếu (preamble có \\parindent, \\parskip…
    nên soi cả file là báo oan)."""
    m = re.search(r"\\begin\{" + ten + r"\}(.*?)\\end\{" + ten + r"\}", tex, re.S)
    assert m, f"không thấy hộp {ten} trong bản in"
    return m.group(1)


def _phieu(**bai):
    b = {"type": "problem", "label": "Bài 1.", "tier": "onclass", "level": 3,
         "statement": "[VD] Chứng minh tứ giác $AHMK$ là hình chữ nhật."}
    b.update(bai)
    return LessonPackage(slug="t", title="t", class_tier="B", stages=[{
        "kind": "practice2", "number": 4, "title": "Luyện tập 2", "blocks": [b]}])


def test_cac_buoc_quy_trinh_khong_dinh_vao_par():
    tex = render_handout(_phieu(quy_trinh=[
        "Bước 1 — Cái phải tìm là gì?",
        "Bước 2 — Vẽ hình, đánh dấu dữ kiện.",
        "Bước 3 — Đã dùng hết giả thiết chưa?",
    ]))
    than = _than_hop(tex, "quytrinhbox")
    # `\parBước`, `\parTa`, … — chữ cái dính ngay sau \par là lệnh không tồn tại.
    assert not re.search(r"\\par[A-Za-z]", than), \
        "\\par dính chữ cái ⇒ TeX đọc thành lệnh lạ:\n" + \
        "\n".join(re.findall(r".{0,40}\\par[A-Za-z].{0,40}", than))
    for i in (1, 2, 3):
        assert f"Bước {i} —" in tex


def test_hop_goi_y_van_tach_dung_y():
    than = _than_hop(render_handout(_phieu(hints=["Gợi ý một.", "Gợi ý hai."])), "hintbox")
    assert not re.search(r"\\par[A-Za-z]", than)
    assert than.count(r"\textbullet") == 2
