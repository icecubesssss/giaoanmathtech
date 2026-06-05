"""Cổng đáp án — chạy SymPy đối chiếu trường `check` (máy-đọc) của từng ProblemBlock.

FAIL (SymPy tìm thấy lệch)        → vi phạm CHẶN build.
INCONCLUSIVE (không kết luận được) → cảnh báo, nhường người kiểm tay.
OK / bài không có `check`          → im lặng (tương thích ngược).
"""
from __future__ import annotations

from . import sympy_solver
from .sympy_solver import Verdict, VerdictStatus


def _run_check(check) -> Verdict:
    if check.kind == "solveset":
        return sympy_solver.check_solution_set(check.equation, check.answer, symbol=check.symbol)
    if check.kind == "identity":
        return sympy_solver.verify_identity(check.lhs, check.rhs)
    if check.kind == "nonneg":
        return sympy_solver.prove_quadratic_nonneg(check.expr, check.symbols)
    return Verdict(VerdictStatus.INCONCLUSIVE, f"kind không nhận diện: {check.kind}")


def check_answers(lesson) -> tuple[list[str], list[str]]:
    """Trả (fails, inconclusive). `fails` CHẶN build; `inconclusive` chỉ cảnh báo.

    Duyệt mọi ProblemBlock có `check`; bài không có `check` thì bỏ qua."""
    fails: list[str] = []
    inconclusive: list[str] = []
    for stage in lesson.stages:
        for i, b in enumerate(stage.blocks):
            check = getattr(b, "check", None)
            if check is None:
                continue
            loc = f"stage[{stage.kind}].block[{i}] '{getattr(b, 'label', '')}'"
            v = _run_check(check)
            if v.status == VerdictStatus.FAIL:
                fails.append(f"{loc}: {v.detail}")
            elif v.status == VerdictStatus.INCONCLUSIVE:
                inconclusive.append(f"{loc}: SymPy không kết luận — {v.detail}")
    return fails, inconclusive
