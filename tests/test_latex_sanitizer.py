"""Đảm bảo chặn được lệnh LaTeX độc hại, không chặn nhầm toán sạch."""
import pytest

from src.validators.latex_sanitizer import sanitize, find_unsafe, UnsafeLatexError


DANGEROUS = [
    r"\write18{rm -rf /}",
    r"\input{/etc/passwd}",
    r"\openout1=x",
    r"\immediate\write18{ls}",
    r"\catcode`\@=11",
    r"\def\evil{boom}",
    r"\include{secret}",
    r"\csname foo\endcsname",
    r"\directlua{os.execute('ls')}",
    r"\usepackage{shellesc}",
]


@pytest.mark.parametrize("payload", DANGEROUS)
def test_blocks_dangerous_commands(payload):
    with pytest.raises(UnsafeLatexError):
        sanitize(payload)


def test_allows_clean_math():
    s = r"\frac{1}{2} + \sqrt{x}"
    assert sanitize(s) == s


def test_allows_seed_inequality_math():
    """Toán điển hình của seed phải qua sạch — không chặn nhầm."""
    s = r"a^2+b^2+c^2 \;\ge\; ab+bc+ca."
    assert sanitize(s) == s


def test_reports_all_violations():
    """find_unsafe trả về danh sách để tầng trên báo cụ thể, không chỉ first-hit."""
    hits = find_unsafe(r"\input{a} and \write18{b}")
    assert any("input" in h.lower() for h in hits)
    assert any("write" in h.lower() for h in hits)
