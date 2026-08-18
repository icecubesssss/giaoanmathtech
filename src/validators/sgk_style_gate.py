"""sgk_style_gate — soi LỜI GIẢI có trình bày theo đúng khuôn SGK không.

Thầy chốt 14/08/2026: thêm một bước "tự check lại trình bày cho chuẩn SGK".
Chuẩn rút từ SGK Toán 9 tập 1 KNTT (Bài 12, tr. 75-76 — Ví dụ 1, 2, 3):

    Giải. Xét △ABC vuông tại A.                 ← (1) MỞ: xác lập hình đang xét
    Theo định lí Pythagore, ta có: BC = …       ← (2) CĂN CỨ trước khi viết hệ thức
    = 500 · 1/50 = 10 (km)                      ← (3) ĐƠN VỊ trong ngoặc sau kết quả
    Vậy sau 1,2 phút, máy bay lên cao 5 km.     ← (4) KẾT: câu "Vậy…"

Cộng quy ước KÝ HIỆU của SGK: dấu phẩy thập phân (9,4) · dấu nhân `\\cdot` chứ không
`\\times` · dùng `\\approx` khi làm tròn.

CHỈ áp khuôn 4 nhịp cho bài TÍNH (level ≥ 2 = TH/VD/VDC). Câu NB gọi tên cạnh hay
trắc nghiệm thì SGK cũng không viết "Vậy" — bắt cả những bài đó là báo động giả.

BÀI HỌC TỪ LẦN SOI HỎNG: quét thô `\\d+\\.\\d+` trên phiếu chương IV ra 331 "lỗi",
soi lại thì gần như toàn bộ là toạ độ TikZ và `0.62\\linewidth`. Nên `_noi_dung_toan()`
phải BÓC HẾT phần LaTeX trình bày trước khi soi.
"""
from __future__ import annotations

import re

from src.schema.lesson_package import LessonPackage

# Bóc sạch phần LaTeX/TikZ — những chỗ dấu chấm là CÚ PHÁP chứ không phải số của đề.
_TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.S)
_OPTS = re.compile(r"\[[^\[\]]*\]")                    # [line width=0.8pt, …]
_LEN = re.compile(r"\d+(?:\.\d+)?\s*(?:cm|mm|pt|in|em|ex|\\linewidth|\\textwidth|\\baselineskip)")
_LEN_CMD = re.compile(r"\\(?:hspace|vspace|raisebox|scalebox|includegraphics|makebox|parbox|"
                      r"resizebox|rule|setlength|arraystretch)\s*\*?\s*(\{[^{}]*\}|\[[^\]]*\])*")

# Số thập phân dùng DẤU CHẤM (sau khi đã bóc LaTeX) — SGK Việt Nam dùng dấu PHẨY.
_DOT_DEC = re.compile(r"(?<![\w.])\d+\.\d+")
# Cụm "nêu căn cứ" mà SGK luôn có trước khi viết hệ thức. Gồm CẢ liên từ nhân quả
# ("Vì … nên …") vì bài LÝ THUYẾT không có tam giác nào để "Xét" — chỉ bắt mấy cụm
# thiên về hình thì bài kiểu "Vì 65° + 25° = 90° nên hai góc phụ nhau" bị kêu oan.
_CAN_CU = re.compile(r"Theo (?:định lí|đ\.l|hệ thức|tính chất)|Áp dụng|Xét\s+\$?\\triangle|"
                     r"Xét tam giác|Trong tam giác|vuông tại|\bVì\b|\bDo\b|\bnên\b|"
                     r"\bsuy ra\b|\bTa có\b", re.I)
_LAM_TRON = re.compile(r"làm tròn", re.I)

# Hộp hình cạnh đề dùng `\makebox[0pt][l]{…}` — RỘNG 0 nên không chiếm chỗ theo chiều
# dọc: hình được vẽ đè lên vùng bên phải. Bài phải tự chừa chỗ bằng `\vspace` ở cuối đề,
# nếu không thì nhiều bài NGẮN liên tiếp sẽ vẽ hình CHỒNG LÊN NHAU thành một đống
# (phiếu C từng chồng 12 bài liền — Thầy phát hiện 14/08/2026).
_CO_HOP_HINH = "[[wrap]]"
_TAIL_VSPACE = re.compile(r"\\vspace\{([0-9.]+)cm\}\s*$")
_VSPACE_TOI_THIEU = 1.5     # cm — hộp hình cao tối đa 2,6cm, đề thường chiếm ~1cm
# Bài TRẮC NGHIỆM in bốn đáp án bằng \parbox — mấy dòng đáp án đã tự chiếm chỗ nên chỉ
# cần chừa thêm chút. Không tách riêng thì mọi bài trắc nghiệm có hình đều bị kêu oan.
_CO_DAP_AN = re.compile(r"\\parbox")
_VSPACE_TOI_THIEU_TN = 0.5


def _noi_dung_toan(s: str) -> str:
    """Phần chữ + công thức HS ĐỌC ĐƯỢC, đã bóc TikZ và tham số độ dài LaTeX."""
    s = _TIKZ.sub(" ", s or "")
    s = _LEN_CMD.sub(" ", s)
    s = _OPTS.sub(" ", s)
    return _LEN.sub(" ", s)


def check_sgk_style(lesson: LessonPackage) -> list[str]:
    """Cảnh báo trình bày lệch chuẩn SGK. Trả list chuỗi (rỗng = sạch)."""
    out: list[str] = []
    for st in lesson.stages:
        for b in st.blocks:
            if getattr(b, "type", "") != "problem":
                continue
            nhan = b.label or "?"
            de = _noi_dung_toan(b.statement)
            giai_raw = (b.solution or "").strip()
            giai = _noi_dung_toan(giai_raw)

            # ── Hộp hình phải tự chừa chỗ, không thì đè lên bài sau ──────
            if _CO_HOP_HINH in (b.statement or ""):
                m = _TAIL_VSPACE.search(b.statement)
                if not m:
                    out.append(f"sgk_style: {nhan} — có hộp hình nhưng đề KHÔNG kết bằng "
                               f"`\\par\\vspace{{…cm}}`; hộp hình rộng 0 nên hình sẽ ĐÈ LÊN "
                               f"bài kế tiếp.")
                else:
                    can = (_VSPACE_TOI_THIEU_TN if _CO_DAP_AN.search(b.statement)
                           else _VSPACE_TOI_THIEU)
                    if float(m.group(1)) < can:
                        out.append(f"sgk_style: {nhan} — chỗ chừa cho hình chỉ {m.group(1)}cm "
                                   f"(cần ≥ {can}cm), hình dễ đè sang bài sau.")

            # ── Ký hiệu (áp cho MỌI bài) ─────────────────────────────────
            for ten, txt in (("đề", de), ("lời giải", giai)):
                if r"\times" in txt:
                    out.append(f"sgk_style: {nhan} — {ten} dùng `\\times`; SGK dùng `\\cdot`.")
                sai = _DOT_DEC.findall(txt)
                if sai:
                    out.append(f"sgk_style: {nhan} — {ten} viết số thập phân bằng DẤU CHẤM "
                               f"({', '.join(sorted(set(sai))[:4])}); SGK dùng dấu phẩy.")
            if _LAM_TRON.search(de) and giai_raw and r"\approx" not in giai_raw:
                out.append(f"sgk_style: {nhan} — đề bắt LÀM TRÒN nhưng lời giải không có "
                           f"`\\approx`, đang viết `=` cho số đã làm tròn.")

            # ── Khuôn 4 nhịp: chỉ bài TÍNH (TH/VD/VDC) ───────────────────
            if not giai_raw or (b.level or 0) < 2:
                continue
            if not _CAN_CU.search(giai):
                out.append(f"sgk_style: {nhan} — lời giải KHÔNG nêu căn cứ/hình đang xét "
                           f"(SGK: “Xét △… vuông tại …”, “Theo định lí …, ta có”).")
            if "Vậy" not in giai_raw:
                out.append(f"sgk_style: {nhan} — lời giải THIẾU câu kết “Vậy …” "
                           f"(SGK luôn chốt lại kết quả kèm đơn vị).")
    return out
