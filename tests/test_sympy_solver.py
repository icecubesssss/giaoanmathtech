"""Độ nhạy bộ giải toán độc lập SymPy — máy phải bắt được lệch dù 1 nghiệm/1 dấu."""
import pytest

from src.validators.sympy_solver import (
    VerdictStatus,
    check_solution_set,
    verify_identity,
    prove_quadratic_nonneg,
)


def test_solution_set_match():
    v = check_solution_set("x**2 - 4 = 0", claimed=[2, -2])
    assert v.ok, v.detail


def test_solution_set_missing_negative_root_fails():
    """Mất nghiệm âm là FAIL — không được "ba phải" cho qua."""
    v = check_solution_set("x**2 - 4 = 0", claimed=[2])
    assert v.status == VerdictStatus.FAIL


def test_solution_set_extra_spurious_root_fails():
    v = check_solution_set("x - 1 = 0", claimed=[1, 7])
    assert v.status == VerdictStatus.FAIL


def test_identity_a2b2_minus_2ab_is_square():
    """Hằng đẳng thức cốt lõi của seed: a^2+b^2-2ab = (a-b)^2."""
    v = verify_identity("a**2 + b**2 - 2*a*b", "(a-b)**2")
    assert v.ok, v.detail


def test_identity_off_by_sign_fails():
    v = verify_identity("a**2 + b**2 + 2*a*b", "(a-b)**2")
    assert v.status == VerdictStatus.FAIL


def test_prove_a2b2_ge_2ab():
    """a^2+b^2-2ab >= 0 — dạng toàn phương PSD, máy phải chứng minh được."""
    v = prove_quadratic_nonneg("a**2 + b**2 - 2*a*b", ["a", "b"])
    assert v.ok, v.detail


def test_prove_boss_inequality_three_vars():
    """Trùm cuối của seed: a^2+b^2+c^2 - (ab+bc+ca) >= 0 với mọi a,b,c."""
    v = prove_quadratic_nonneg(
        "a**2 + b**2 + c**2 - a*b - b*c - c*a", ["a", "b", "c"]
    )
    assert v.ok, v.detail


def test_prove_quadratic_finds_counterexample():
    """a^2 - b^2 KHÔNG luôn không âm — máy phải FAIL chứ không INCONCLUSIVE."""
    v = prove_quadratic_nonneg("a**2 - b**2", ["a", "b"])
    assert v.status == VerdictStatus.FAIL


def test_non_quadratic_returns_inconclusive():
    """Bậc khác 2 thì trả INCONCLUSIVE, không tự nhận đã chứng minh."""
    v = prove_quadratic_nonneg("a**4 + b**4", ["a", "b"])
    assert v.status == VerdictStatus.INCONCLUSIVE
