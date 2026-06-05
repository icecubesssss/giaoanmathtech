# KẾ HOẠCH #3 — Tự động kiểm đáp án bằng SymPy trong `validate`

> **Giao cho:** Gemini Flash 3.5 (hoặc bất kỳ AI nào). **Người duyệt:** Thầy.
> **Mục tiêu:** Thêm trường `check` (đáp án MÁY-ĐỌC) **tùy chọn** vào mỗi bài tập trong file
> seed JSON, để lệnh `validate` **tự** chạy SymPy đối chiếu và **chặn build khi đáp án sai**.
> Hiện SymPy đã có sẵn (`src/validators/sympy_solver.py`) nhưng phải gọi tay; việc này nối nó vào cổng `validate`.

## Nguyên tắc BẮT BUỘC khi làm
1. **TƯƠNG THÍCH NGƯỢC TUYỆT ĐỐI.** Trường `check` là **tùy chọn** (mặc định `None`). 14 bài seed cũ KHÔNG có `check` → phải chạy y như trước, `validate-all` vẫn 14/14 qua. KHÔNG sửa nội dung toán của bài cũ.
2. **KHÔNG đụng template/giao diện.** `check` chỉ để máy soi, **KHÔNG in ra phiếu** (handout/guide/slide). Không sửa file trong `templates/`, không sửa `src/compiler/`.
3. **KHÔNG sửa toán trong `sympy_solver.py`.** Chỉ *gọi* các hàm có sẵn ở đó.
4. **Ba trạng thái rõ ràng:** `FAIL` (SymPy tìm thấy lệch) → **vi phạm CHẶN build**. `INCONCLUSIVE` (SymPy không kết luận được) → **chỉ cảnh báo**, nhường người kiểm tay. `OK` → im lặng.
5. Sau khi xong: `python -m pytest` phải xanh, và `python -m src.main validate-all --grade lop-9` vẫn 14/14 qua.

---

## Bối cảnh — SymPy có sẵn gì (CHỈ GỌI, đừng sửa)
File `src/validators/sympy_solver.py` xuất 3 hàm kiểm + 1 lớp kết quả:

| Hàm | Chữ ký | Dùng cho |
|---|---|---|
| `check_solution_set(equation, claimed, symbol="x")` | trả `Verdict` | giải PT 1 ẩn, so tập nghiệm |
| `verify_identity(lhs, rhs)` | trả `Verdict` | chứng minh đẳng thức 2 vế |
| `prove_quadratic_nonneg(expr, symbols)` | trả `Verdict` | CM biểu thức bậc hai ≥ 0 |

`Verdict` có `.status` ∈ `{VerdictStatus.OK, VerdictStatus.FAIL, VerdictStatus.INCONCLUSIVE}` và `.detail` (chuỗi mô tả).

---

## BƯỚC 1 — Thêm schema trường `check` vào `ProblemBlock`
File: `src/schema/lesson_package.py`

### 1a. Thêm 3 model "kiểm" + union, đặt NGAY TRƯỚC `class ProblemBlock` (sau `WriteLinesBlock`)
```python
# ----- Đáp án MÁY-ĐỌC để validate tự soi bằng SymPy (tùy chọn, KHÔNG in ra phiếu) -----


class SolvesetCheck(BaseModel):
    """Kiểm nghiệm phương trình một ẩn (→ sympy_solver.check_solution_set)."""
    kind: Literal["solveset"] = "solveset"
    equation: str = Field(..., description="PT dạng 'lhs = rhs' hoặc 'expr = 0' (LaTeX/text)")
    answer: list[Union[str, int, float]] = Field(..., description="Tập nghiệm người tuyên bố, vd [2, 3]")
    symbol: str = Field("x", description="Tên ẩn (mặc định x)")


class IdentityCheck(BaseModel):
    """Kiểm đẳng thức hai vế (→ sympy_solver.verify_identity)."""
    kind: Literal["identity"] = "identity"
    lhs: str = Field(..., description="Vế trái")
    rhs: str = Field(..., description="Vế phải")


class NonnegCheck(BaseModel):
    """Kiểm 'biểu thức bậc hai >= 0 với mọi biến thực' (→ sympy_solver.prove_quadratic_nonneg)."""
    kind: Literal["nonneg"] = "nonneg"
    expr: str = Field(..., description="Biểu thức bậc hai thuần nhất, vd 'a**2+b**2-2*a*b'")
    symbols: list[str] = Field(..., description="Danh sách biến, vd ['a','b']")


AnswerCheck = Union[SolvesetCheck, IdentityCheck, NonnegCheck]
```

### 1b. Thêm field `check` vào `ProblemBlock` (sau field `video`)
```python
    # (TÙY CHỌN) Đáp án MÁY-ĐỌC để `validate` tự soi bằng SymPy. None = bỏ qua (như cũ).
    # KHÔNG in ra phiếu — chỉ phục vụ answer_gate. Phân biệt loại bằng khóa "kind".
    check: Optional[AnswerCheck] = Field(
        None, description="Đáp án máy-đọc cho answer_gate; KHÔNG hiển thị trên phiếu"
    )
```
> `Optional` và `Union` đã được import sẵn ở đầu file (`from typing import Literal, Union`). **Thêm `Optional`** vào dòng import đó: `from typing import Literal, Optional, Union`.
> KHÔNG dùng `discriminator=` — để pydantic v2 tự suy theo `kind` (giống `Block` hiện có, vốn không khai báo discriminator).

---

## BƯỚC 2 — Tạo validator mới `src/validators/answer_gate.py`
File MỚI, dán nguyên:
```python
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
```

---

## BƯỚC 3 — Xuất hàm trong `src/validators/__init__.py`
Thêm dòng import (cạnh các import khác):
```python
from .answer_gate import check_answers
```
Và thêm `"check_answers"` vào danh sách `__all__`.

---

## BƯỚC 4 — Nối vào `validate` trong `src/main.py`

### 4a. Bổ sung import
Trong khối `from src.validators import ( ... )` (khoảng dòng 30), thêm `check_answers` vào danh sách.

### 4b. Gọi trong `_run_validation` (hàm khoảng dòng 283)
Tìm đoạn cuối hàm:
```python
    warns = find_presentation_warnings(lesson)
    ramp_warns = check_ramp(lesson)
    return violations, warns, ramp_warns
```
Sửa thành:
```python
    warns = find_presentation_warnings(lesson)
    ramp_warns = check_ramp(lesson)

    ans_fail, ans_incon = check_answers(lesson)
    violations.extend(f"[answer_gate] {m}" for m in ans_fail)
    warns = warns + [f"[answer_gate] (cần kiểm tay) {m}" for m in ans_incon]
    return violations, warns, ramp_warns
```
> Như vậy `FAIL` chui vào `violations` (đã được mọi nơi coi là CHẶN: `validate`, `build`, `build-folder` đều dừng); `INCONCLUSIVE` thành cảnh báo (không chặn).

### 4c. Thêm dòng báo cáo trong `cmd_validate` (hàm khoảng dòng 306)
Sau dòng đếm `n_diff = ...`, thêm:
```python
    n_ans = sum(1 for v in violations if v.startswith("[answer_gate]"))
```
Và sau dòng `print(f"  • difficulty_gate:  ...")`, thêm:
```python
    print(f"  • answer_gate:      {'OK' if n_ans == 0 else f'{n_ans} đáp án SAI'}")
```

---

## BƯỚC 5 — Test `tests/test_answer_gate.py`
File MỚI, dán nguyên:
```python
from src.schema import LessonPackage
from src.validators.answer_gate import check_answers


def _lesson(check: dict) -> LessonPackage:
    """Gói bài tối thiểu 1 chặng, 1 ProblemBlock mang `check` để test cổng đáp án."""
    return LessonPackage.model_validate({
        "slug": "t", "title": "T",
        "stages": [{
            "kind": "practice1", "number": 3, "title": "Luyện",
            "blocks": [{"type": "problem", "label": "Bài 1.",
                        "statement": "x", "check": check}],
        }],
    })


def test_solveset_ok():
    fails, incon = check_answers(_lesson(
        {"kind": "solveset", "equation": "x^2 - 5x + 6 = 0", "answer": [2, 3]}))
    assert fails == [] and incon == []


def test_solveset_fail():
    fails, _ = check_answers(_lesson(
        {"kind": "solveset", "equation": "x^2 - 5x + 6 = 0", "answer": [2, 5]}))
    assert len(fails) == 1


def test_identity_ok():
    fails, _ = check_answers(_lesson(
        {"kind": "identity", "lhs": "(a+b)^2", "rhs": "a^2 + 2*a*b + b^2"}))
    assert fails == []


def test_identity_fail():
    fails, _ = check_answers(_lesson(
        {"kind": "identity", "lhs": "(a+b)^2", "rhs": "a^2 + b^2"}))
    assert len(fails) == 1


def test_nonneg_ok():
    fails, _ = check_answers(_lesson(
        {"kind": "nonneg", "expr": "a**2 + b**2 - 2*a*b", "symbols": ["a", "b"]}))
    assert fails == []


def test_no_check_is_skipped():
    lesson = LessonPackage.model_validate({
        "slug": "t", "title": "T",
        "stages": [{"kind": "practice1", "number": 3, "title": "L",
                    "blocks": [{"type": "problem", "label": "B1", "statement": "x"}]}],
    })
    assert check_answers(lesson) == ([], [])
```
> Nếu một hàm SymPy trả `INCONCLUSIVE` thay vì `OK`/`FAIL` (do `parse_latex` không nuốt được cú pháp), hãy đổi biểu thức trong test sang cú pháp SymPy thuần (dùng `**` cho lũy thừa, `*` cho nhân) — KHÔNG nới lỏng assert để test xanh giả.

---

## BƯỚC 6 — Cập nhật tài liệu
1. `AGENTS.md` — mục "Nguyên tắc BẮT BUỘC khi soạn" điểm 2: bổ sung một câu: *"Bài đại số NÊN kèm trường `check` (đáp án máy-đọc) trong seed để `validate` tự soi SymPy và chặn nếu sai; xem KE-HOACH-AUTO-CHECK-DAP-AN.md / HUONG-DAN §..."*.
2. `HUONG-DAN-SOAN-BAI.md` — thêm một mục nhỏ mô tả trường `check` với ví dụ JSON (xem mục "Ví dụ seed" dưới đây), nhấn mạnh: tùy chọn, không in ra phiếu, 3 `kind`.

---

## Ví dụ seed sau khi xong (để minh hoạ — KHÔNG bắt sửa bài cũ)
```jsonc
{
  "type": "problem",
  "label": "Bài 1.",
  "statement": "Giải phương trình $x^2 - 5x + 6 = 0$.",
  "tier": "onclass",
  "check": { "kind": "solveset", "equation": "x^2 - 5x + 6 = 0", "answer": [2, 3] }
}
```
Đẳng thức:
```jsonc
"check": { "kind": "identity", "lhs": "(a+b)^2", "rhs": "a^2 + 2*a*b + b^2" }
```
Bất đẳng thức bậc hai:
```jsonc
"check": { "kind": "nonneg", "expr": "a**2 + b**2 - 2*a*b", "symbols": ["a", "b"] }
```

---

## NGHIỆM THU (chạy hết, dán kết quả cho Thầy)
```bash
# 1) Test xanh (phải có các test_answer_gate mới)
python -m pytest -q

# 2) Kho cũ KHÔNG vỡ — vẫn 14/14 qua (vì chưa bài nào có `check`)
python -m src.main validate-all --grade lop-9

# 3) Bằng chứng cổng CHẶN khi đáp án sai: tạo bản lỗi tạm rồi validate
python - <<'PY'
import json, pathlib
src = "inputs/seeds/lop-9/dai-so/tuan09-bat-dang-thuc/tong-ket-bat-dang-thuc.json"  # hoặc 1 bài đại số bất kỳ
d = json.loads(pathlib.Path(src).read_text(encoding="utf-8"))
# gắn check SAI vào 1 problem block đầu tiên tìm được
for st in d["stages"]:
    for b in st.get("blocks", []):
        if b.get("type") == "problem":
            b["check"] = {"kind": "solveset", "equation": "x^2 - 5x + 6 = 0", "answer": [2, 5]}
            raise SystemExit(pathlib.Path("/tmp/_chk.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8") or "wrote /tmp/_chk.json")
PY
python -m src.main validate /tmp/_chk.json   # KỲ VỌNG: answer_gate báo SAI, exit code 1
rm -f /tmp/_chk.json
```
**Đạt yêu cầu khi:** (1) pytest xanh; (2) validate-all 14/14 qua; (3) file lỗi tạm bị `answer_gate` từ chối (exit 1).

## Phạm vi — ĐƯỢC và KHÔNG
- ✅ Sửa: `src/schema/lesson_package.py`, `src/validators/__init__.py`, `src/main.py`; tạo `src/validators/answer_gate.py`, `tests/test_answer_gate.py`; cập nhật `AGENTS.md`, `HUONG-DAN-SOAN-BAI.md`.
- ❌ KHÔNG sửa: `src/validators/sympy_solver.py`, bất kỳ file nào trong `templates/` hay `src/compiler/`, và KHÔNG sửa nội dung toán của 14 seed cũ.
