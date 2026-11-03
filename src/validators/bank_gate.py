"""bank_gate — cổng CHẤT LƯỢNG tab phân dạng (Thầy chốt 03/11/2026, mục 8 sheet quy chuẩn).

Vì sao có cổng này: tab chương IV lớp 9C (1.085 câu, commit 03/11/2026) được gom bằng
pdftotext + regex chứ không đọc ảnh. Cột đề lẫn cả lời giải ("Ví dụ 1. … Giải Xét ∆𝐴𝐵𝐶…"),
70% câu bị gán TH và 517 câu có phút = 6,0 đúng bằng định mức mặc định. Cổng cũ
`thuyetminh_gate.check_nguon_sheet` chỉ hỏi "mã câu có trên tab không", nên thuyết minh bốc
từ tab đó vẫn qua.

Cổng soi SNAPSHOT tab (`inputs/refs/ngan-hang-sheet/<grade>/<subject>/chuong-NN.json`):

LỖI (chặn thuyết minh bốc từ tab):
  • đề lẫn LỜI GIẢI ("Lời giải", "Hướng dẫn giải", "Giải:", "Giải Xét …");
    KHÔNG bắt "Giải tam giác / Giải thích / Giải phương trình …" (là yêu cầu của đề);
  • chữ toán kiểu pdftotext (khối Unicode Mathematical Alphanumeric: 𝐴 𝑥 …) — dấu hiệu
    chép chữ từ PDF chứ không đọc ảnh (luật L3);
  • mã câu trùng.
CẢNH BÁO:
  • đề trùng nguyên văn (L5 — đánh dấu "Bỏ" một bản);
  • một mức độ chiếm quá 65% số câu (mức có vẻ để mặc định, chưa chấm thật);
  • một giá trị phút chiếm quá 40% số câu (phút để mặc định, chưa tính theo từng ý);
  • cột "Phân loại câu" còn trống quá nửa (bước A của quy trình phân dạng chưa làm).
"""
from __future__ import annotations

import collections
import re

__all__ = ["check_bank", "LOI_GIAI_RE", "PDFTOTEXT_RE"]

LOI_GIAI_RE = re.compile(
    r"Lời giải|Hướng dẫn giải|\bGiải\s*[:.]|\bGiải\s+(?:Xét|Ta có|Vì|Gọi|Theo|Do)\b")
# U+1D400–U+1D7FF: chữ in nghiêng/đậm toán học mà pdftotext trả ra thay cho chữ thường.
PDFTOTEXT_RE = re.compile("[\U0001D400-\U0001D7FF]")

NGUONG_MUC = 0.65
NGUONG_PHUT = 0.40
NGUONG_VAI_TRONG = 0.50
MIN_CAU = 50  # tab ít câu hơn thì không soi phân bố (mẫu nhỏ dễ lệch thật)


def _chuan(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def check_bank(snap: dict) -> tuple[list[str], list[str]]:
    """Trả (errors, warnings) cho một snapshot tab phân dạng."""
    rows = snap.get("rows", [])
    tab = snap.get("tab", "?")
    errors: list[str] = []
    warnings: list[str] = []

    loi_giai = [r.get("ma", "?") for r in rows if LOI_GIAI_RE.search(r.get("de", ""))]
    if loi_giai:
        errors.append(
            f"bank: tab '{tab}' — {len(loi_giai)} câu có LỜI GIẢI lẫn trong cột đề: "
            f"{', '.join(loi_giai[:6])}" + (" …" if len(loi_giai) > 6 else "")
            + ". Chép lại đề từ ẢNH, bỏ phần lời giải.")
    pdf = [r.get("ma", "?") for r in rows if PDFTOTEXT_RE.search(r.get("de", ""))]
    if pdf:
        errors.append(
            f"bank: tab '{tab}' — {len(pdf)} câu chép chữ kiểu pdftotext (ký tự toán Unicode "
            f"𝐴, 𝑥…): {', '.join(pdf[:6])}" + (" …" if len(pdf) > 6 else "")
            + ". Đọc ẢNH trang gốc rồi chép lại (luật L3).")
    dem_ma = collections.Counter(r.get("ma", "") for r in rows if r.get("ma"))
    trung_ma = [m for m, n in dem_ma.items() if n > 1]
    if trung_ma:
        errors.append(f"bank: tab '{tab}' — mã câu trùng: {', '.join(trung_ma[:6])}.")

    nhom: dict[str, list[str]] = collections.defaultdict(list)
    for r in rows:
        if r.get("de"):
            nhom[_chuan(r["de"])].append(r.get("ma", "?"))
    trung_de = [v for v in nhom.values() if len(v) > 1]
    if trung_de:
        warnings.append(
            f"bank: tab '{tab}' — {len(trung_de)} đề trùng nguyên văn (L5, ghi 'Bỏ' một bản): "
            + "; ".join(" = ".join(v) for v in trung_de[:4]) + (" …" if len(trung_de) > 4 else ""))

    n = len(rows)
    if n >= MIN_CAU:
        muc = collections.Counter(r.get("band", "") for r in rows)
        b, k = muc.most_common(1)[0]
        if k / n > NGUONG_MUC:
            warnings.append(
                f"bank: tab '{tab}' — {k}/{n} câu ({k / n:.0%}) cùng mức {b}: mức độ có vẻ để mặc "
                f"định, chưa chấm từng câu.")
        phut = collections.Counter(str(r.get("phut", "")) for r in rows if r.get("phut") not in (None, ""))
        if phut:
            p, k = phut.most_common(1)[0]
            if k / n > NGUONG_PHUT:
                warnings.append(
                    f"bank: tab '{tab}' — {k}/{n} câu ({k / n:.0%}) cùng thời lượng {p}′: phút có vẻ "
                    f"để mặc định. Tính theo từng ý (tab Định mức thời lượng, mục D).")
        if any("vai" in r for r in rows):
            trong = sum(1 for r in rows if not (r.get("vai") or "").strip())
            if trong / n > NGUONG_VAI_TRONG:
                warnings.append(
                    f"bank: tab '{tab}' — cột 'Phân loại câu' còn trống {trong}/{n} câu: bước A "
                    f"của quy trình phân dạng chưa làm.")
    return errors, warnings
