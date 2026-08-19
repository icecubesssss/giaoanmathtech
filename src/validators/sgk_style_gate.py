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

KHỐI "VÍ DỤ" cũng phải theo khuôn đó (Thầy chấm Không đạt 17/08/2026 cả 4 phiếu chương
IV: "Phiếu đang cho ví dụ là cách giải, cách hướng dẫn => Phiếu cần: Ví dụ là bài giải,
trình bày chuẩn, làm mẫu"). Cổng cũ chỉ soi block `problem` nên ví dụ trôi tự do suốt —
nay `check_vi_du_style()` đòi mỗi ví dụ có tiêu đề "Lời giải" và câu kết "Vậy …".

GỌI TÊN CẠNH ĐỐI / CẠNH KỀ rồi mới viết tỉ số lượng giác cũng là "hướng dẫn" (Thầy
2026-08-18: *"k cần ghi cạnh đối / cạnh huyền đâu, trong bài thi chỉ cần xét tam giác
vuông là nói được tỉ số lượng giác luôn — đọc đáp án mấy đề thi là hiểu"*). Đáp án ngân
hàng đề viết thẳng: `$\tan\alpha = \frac{325}{600} \implies \alpha \approx 28^\circ$`.
`check_goi_ten_canh()` gác luật này cho CẢ lời giải bài lẫn ví dụ. Câu NB mà chính ĐỀ hỏi
"cạnh đối của góc B là cạnh nào?" thì đáp án dừng ở việc gọi tên, KHÔNG kèm tỉ số nào —
nên cổng chỉ kêu khi trong CÙNG MỘT DÒNG có cả lời gọi tên lẫn công thức tỉ số.

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


# ── Khối VÍ DỤ phải là BÀI GIẢI MẪU, không phải lời hướng dẫn ──────────────
_VI_DU = re.compile(r"\\textbf\{(Ví dụ [^}]*)\}")
# Câu mở kiểu "hướng dẫn cách làm" thay cho lời giải thật — Thầy gạch đúng mấy câu này.
_HUONG_DAN = re.compile(r"vẫn (?:đúng|làm) (?:như|theo)|làm tương tự|cách làm như|"
                        r"chỉ (?:việc |cần )?thay (?:bằng|số vào)|(?:các )?bước (?:làm|giải) như",
                        re.I)


def check_vi_du_style(lesson: LessonPackage) -> list[str]:
    """Mỗi khối `noted variant=example` chứa "Ví dụ N." phải là một BÀI GIẢI đầy đủ:
    có tiêu đề "Lời giải" và chốt bằng "Vậy …". Cảnh báo, không chặn."""
    out: list[str] = []
    for st in lesson.stages:
        for b in st.blocks:
            if getattr(b, "type", "") != "noted" or getattr(b, "variant", "") != "example":
                continue
            text = getattr(b, "text", "") or ""
            m = _VI_DU.search(text)
            if not m:
                continue                       # hộp mở màn/nhắc bài cũ — không phải ví dụ
            nhan = m.group(1).strip()
            noi_dung = _noi_dung_toan(text)
            if "Lời giải" not in noi_dung:
                out.append(f"sgk_style: {nhan} — thiếu tiêu đề “Lời giải”; ví dụ phải là "
                           f"BÀI GIẢI MẪU HS chép theo, không phải đoạn hướng dẫn cách làm.")
            if "Vậy" not in noi_dung:
                out.append(f"sgk_style: {nhan} — lời giải THIẾU câu kết “Vậy …” kèm đơn vị.")
            hd = _HUONG_DAN.search(noi_dung)
            if hd:
                out.append(f"sgk_style: {nhan} — viết “{hd.group(0)}” thay vì trình bày đủ "
                           f"bài giải; ví dụ phải làm mẫu trọn vẹn, không trỏ sang ví dụ khác.")
    return out


# ── Gọi tên cạnh đối/kề rồi mới viết tỉ số — lời hướng dẫn, không phải bài giải ──
# Mẫu HỎNG = gọi tên cạnh  →  "nên/thì/do đó"  →  tỉ số lượng giác, TRONG CÙNG một câu.
# Đòi đủ ba mảnh theo ĐÚNG THỨ TỰ mới khỏi báo oan hai ca hợp lệ:
#   • câu NB mà chính đề hỏi gọi tên ("Với góc B: cạnh đối là AC, cạnh kề là AB.") — không kèm tỉ số;
#   • câu dựng hình ("Vì sin α = 3/5 nên dựng tam giác vuông có cạnh đối bằng 3") — ngược thứ tự.
_GOI_TEN = re.compile(r"(?:là\s+cạnh\s+(?:đối|kề|huyền)|cạnh\s+(?:đối|kề|huyền)\s+(?:là|của))")
_GOI_TEN_ROI_TSLG = re.compile(
    r"(?:là\s+cạnh\s+(?:đối|kề|huyền)|cạnh\s+(?:đối|kề|huyền)\s+(?:là|của))"
    r"[^.]{0,160}?\b(?:nên|thì|do đó)\b[^.]{0,60}?\\(?:sin|cos|tan|cot)\b")
# $\dfrac{\text{cạnh đối}}{\text{cạnh huyền}}$ chỉ được dùng khi ĐANG NÊU ĐỊNH NGHĨA;
# đứng cạnh một phân số bằng SỐ là đang tính toán ⇒ thừa.
_FRAC_CHU = re.compile(r"\\text\{cạnh (?:đối|kề|huyền)\}")
_FRAC_SO = re.compile(r"\\dfrac\{\d")


def _dong(text: str):
    for d in (text or "").split("[[br]]"):
        yield d


def check_goi_ten_canh(lesson: LessonPackage) -> list[str]:
    """Cảnh báo dòng vừa gọi tên cạnh đối/kề/huyền vừa viết tỉ số lượng giác."""
    out: list[str] = []
    for st in lesson.stages:
        for b in st.blocks:
            typ = getattr(b, "type", "")
            if typ == "problem":
                nhan, text = (b.label or "?"), (b.solution or "")
            elif typ == "noted" and getattr(b, "variant", "") == "example":
                m = _VI_DU.search(getattr(b, "text", "") or "")
                if not m:
                    continue
                nhan, text = m.group(1).strip(), (b.text or "")
            else:
                continue
            for d in _dong(_noi_dung_toan(text)):
                if _GOI_TEN_ROI_TSLG.search(d):
                    out.append(f"sgk_style: {nhan} — gọi tên cạnh đối/kề rồi mới viết tỉ số "
                               f"(“{_GOI_TEN.search(d).group(0)}… nên …”). Bài thi viết thẳng "
                               f"tỉ số sau “Xét tam giác … vuông tại …”.")
                    break
            for d in _dong(text):
                if _FRAC_CHU.search(d) and _FRAC_SO.search(d):
                    out.append(f"sgk_style: {nhan} — viết $\\dfrac{{\\text{{cạnh đối}}}}"
                               f"{{\\text{{cạnh huyền}}}}$ trong một phép TÍNH; chỉ dùng cách "
                               f"viết đó khi đang nêu định nghĩa.")
                    break
    return out
