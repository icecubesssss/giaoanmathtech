"""Kiểm thử các cấu phần thu thập và dọn dẹp dữ liệu toán học (Phase 4.1)."""
from __future__ import annotations

from pathlib import Path
from src.scrapers import clean_html, parse_mathjax, normalize_latex, are_similar, run_scraping_job, BANK_DIR
from src.schema.base_schema import MathProblem


def test_html_cleaner():
    html = """
    <html>
        <head><style>body { color: red; }</style></head>
        <body>
            <nav>Navigation</nav>
            <div class="main-content">
                <h1>Đề thi tuyển sinh lớp 10</h1>
                <p>Cho tam giác ABC.</p>
            </div>
            <div class="ads-banner">Quảng cáo cực lớn</div>
            <footer>Bản quyền thuộc MathTech</footer>
        </body>
    </html>
    """
    cleaned = clean_html(html)
    assert "Đề thi tuyển sinh lớp 10" in cleaned
    assert "Cho tam giác ABC." in cleaned
    assert "Navigation" not in cleaned
    assert "Quảng cáo" not in cleaned
    assert "Bản quyền" not in cleaned


def test_mathjax_parser():
    html_math = """
    <p>Tìm nghiệm của phương trình <script type="math/tex">x^2 - 4x + 3 = 0</script></p>
    <div>Hiển thị công thức: <script type="math/tex"; mode=display>x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}</script></div>
    """
    parsed = parse_mathjax(html_math)
    assert "$x^2 - 4x + 3 = 0$" in parsed
    assert "$$x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}$$" in parsed


def test_latex_deduplication():
    prob_a = "Cho tam giác $ABC$, chứng minh rằng $AB + BC > AC$."
    prob_b = "Chứng minh $AB+BC>AC$ cho tam giác $ABC$"
    
    assert are_similar(prob_a, prob_b)


def test_offline_worker_initialization():
    stats = run_scraping_job()
    assert stats["algebra_count"] >= 3
    assert stats["geometry_count"] >= 1
    
    assert (BANK_DIR / "algebra.json").exists()
    assert (BANK_DIR / "geometry.json").exists()
