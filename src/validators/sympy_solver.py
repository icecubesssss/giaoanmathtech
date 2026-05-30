"""Trọng tài Đại số — giải ĐỘC LẬP bằng SymPy rồi đối chiếu với đáp án con người.

Nguyên tắc: máy KHÔNG sửa toán, chỉ phán "khớp / lệch / không kết luận được".
- `solve_equation` + `check_solution_set`: giải phương trình một ẩn, so khớp tập nghiệm
  (lệch dù một nghiệm/một dấu ± là FAIL).
- `verify_identity`: chứng minh hai vế bằng nhau (rút gọn hiệu về 0).
- `prove_quadratic_nonneg`: với BẤT ĐẲNG THỨC dạng "biểu thức bậc hai >= 0 với mọi
  biến thực" (đúng họ bài seed: $a^2+b^2-2ab\\ge0$, $a^2+b^2+c^2\\ge ab+bc+ca$),
  kiểm bằng ma trận dạng toàn phương nửa-xác-định-dương (eigenvalue >= 0). Đây là
  thuật toán ĐÚNG và quyết-định-được cho lớp bài này, không phải lấy mẫu may rủi.

Mọi hàm phân biệt rõ ba trạng thái: khớp/đúng, sai (có phản ví dụ), và
INCONCLUSIVE (ngoài năng lực SymPy) — để tầng trên không "duyệt mù".
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import sympy as sp
from sympy.parsing.latex import parse_latex

__all__ = [
    "VerdictStatus",
    "Verdict",
    "to_expr",
    "solve_equation",
    "check_solution_set",
    "verify_identity",
    "prove_quadratic_nonneg",
]


class VerdictStatus:
    OK = "ok"               # máy xác nhận khớp / đúng
    FAIL = "fail"           # máy tìm thấy lệch / phản ví dụ
    INCONCLUSIVE = "inconclusive"  # ngoài năng lực giải độc lập → cần người


@dataclass
class Verdict:
    status: str
    detail: str

    @property
    def ok(self) -> bool:
        return self.status == VerdictStatus.OK


_TRANSLATE = {"\\ge": ">=", "\\geq": ">=", "\\le": "<=", "\\leq": "<=",
              "\\cdot": "*", "\\times": "*", "\\dfrac": "\\frac"}


def to_expr(latex_or_text: str) -> sp.Expr:
    """Phân tích LaTeX (hoặc biểu thức sympy text) thành biểu thức SymPy.

    Thử `parse_latex` trước; nếu thất bại quay về `sympify` sau khi dọn vài macro.
    """
    s = latex_or_text.strip().strip("$")
    try:
        return parse_latex(s)
    except Exception:
        for a, b in _TRANSLATE.items():
            s = s.replace(a, b)
        s = s.replace("^", "**")
        return sp.sympify(s)


def solve_equation(equation: str, symbol: str = "x") -> set[sp.Expr]:
    """Giải độc lập phương trình một ẩn. Chấp nhận 'lhs = rhs' hoặc biểu thức = 0."""
    x = sp.Symbol(symbol)
    if "=" in equation and "==" not in equation:
        lhs_s, rhs_s = equation.split("=", 1)
        eq = sp.Eq(to_expr(lhs_s), to_expr(rhs_s))
    else:
        eq = sp.Eq(to_expr(equation), 0)
    return set(sp.solveset(eq, x, domain=sp.S.Reals))


def check_solution_set(equation: str, claimed: Iterable, symbol: str = "x") -> Verdict:
    """So khớp tập nghiệm SymPy giải được với tập nghiệm con người tuyên bố."""
    try:
        machine = solve_equation(equation, symbol)
    except Exception as exc:  # noqa: BLE001 — giải không nổi thì trả INCONCLUSIVE
        return Verdict(VerdictStatus.INCONCLUSIVE, f"SymPy không giải được: {exc}")

    claimed_set = {to_expr(str(c)) for c in claimed}
    machine_simpl = {sp.nsimplify(sp.simplify(m)) for m in machine}
    claimed_simpl = {sp.nsimplify(sp.simplify(c)) for c in claimed_set}
    if machine_simpl == claimed_simpl:
        return Verdict(VerdictStatus.OK, f"Khớp tập nghiệm: {sorted(map(str, machine_simpl))}")
    missing = claimed_simpl - machine_simpl
    extra = machine_simpl - claimed_simpl
    return Verdict(
        VerdictStatus.FAIL,
        f"Lệch nghiệm — người thừa {sorted(map(str, missing))}, "
        f"máy còn {sorted(map(str, extra))}",
    )


def verify_identity(lhs: str, rhs: str) -> Verdict:
    """Chứng minh đẳng thức: rút gọn (lhs - rhs) về 0 thì OK."""
    try:
        diff = sp.simplify(to_expr(lhs) - to_expr(rhs))
    except Exception as exc:  # noqa: BLE001
        return Verdict(VerdictStatus.INCONCLUSIVE, f"Không rút gọn được: {exc}")
    if diff == 0:
        return Verdict(VerdictStatus.OK, "Hai vế đồng nhất.")
    return Verdict(VerdictStatus.FAIL, f"Hiệu hai vế = {diff} ≠ 0")


def prove_quadratic_nonneg(expr: str, symbols: Iterable[str]) -> Verdict:
    """Chứng minh `expr >= 0 với mọi biến thực` cho biểu thức BẬC HAI thuần nhất.

    Lập ma trận dạng toàn phương đối xứng và kiểm nửa-xác-định-dương qua dấu các
    trị riêng. PSD ⇔ đúng với mọi giá trị thực ⇒ chứng minh chặt, không lấy mẫu.
    Nếu biểu thức không phải dạng toàn phương bậc hai → INCONCLUSIVE (nhường người).
    """
    syms = [sp.Symbol(s) for s in symbols]
    try:
        poly = sp.Poly(sp.expand(to_expr(expr)), *syms)
    except Exception as exc:  # noqa: BLE001
        return Verdict(VerdictStatus.INCONCLUSIVE, f"Không lập được đa thức: {exc}")

    if poly.total_degree() != 2 or any(
        sum(monom) != 2 for monom in poly.monoms()
    ):
        return Verdict(
            VerdictStatus.INCONCLUSIVE,
            "Không phải dạng toàn phương bậc hai thuần nhất — cần kiểm tay.",
        )

    n = len(syms)
    M = sp.zeros(n, n)
    for i in range(n):
        M[i, i] = poly.coeff_monomial(syms[i] ** 2)
        for j in range(i + 1, n):
            c = poly.coeff_monomial(syms[i] * syms[j])
            M[i, j] = M[j, i] = sp.Rational(c, 2)

    eigs = list(M.eigenvals().keys())
    if all(sp.simplify(e) >= 0 for e in eigs):
        return Verdict(VerdictStatus.OK, f"Dạng toàn phương PSD (trị riêng {eigs}) ⇒ ≥ 0.")
    return Verdict(VerdictStatus.FAIL, f"Có trị riêng âm {eigs} ⇒ KHÔNG luôn ≥ 0.")
