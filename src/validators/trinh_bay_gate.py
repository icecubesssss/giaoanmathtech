"""trinh_bay_gate — gác CÁCH TRÌNH BÀY phiếu (Thầy chốt 24/09/2026).

Bốn luật dưới đây đều rút ra từ lỗi THẬT đã vấp khi dựng lại phiếu A chương V lớp 9C.
Mỗi luật ở đây thay cho một dòng nhắc trong tài liệu — vì nhắc bằng chữ thì lần sau
lại quên (luật "HS làm vào vở, không chừa dòng kẻ" đã có từ lâu mà phiếu A vẫn còn
36 khối dòng kẻ).
"""
from __future__ import annotations

import difflib
import re

from src.schema import LessonPackage

__all__ = ["check_trinh_bay", "check_lenh_dinh_chu"]

# ── 1. Lệnh LaTeX không đối số DÍNH LIỀN chữ cái ────────────────────────────────
# `\par` + "Đáp" → `\parĐáp`, `\bfseries` + "Bán" → `\bfseriesBán`: Tectonic chết
# "Undefined control sequence". Đã làm gãy build HAI LẦN trong một phiên. Lệnh kết
# thúc bằng `}` (vd `\color{brand}`) thì an toàn, nên chỉ soi lệnh trần.
_LENH_TRAN = re.compile(
    r"\\(par|bfseries|itshape|slshape|scshape|normalfont|centering|raggedright"
    r"|small|footnotesize|scriptsize|large|Large|huge|noindent)"
    r"(?=[A-Za-zÀ-ỹĐđ])")

# ── 2. Ô [[fill:…]] nằm TRONG $…$ mà đáp án lại bọc $ → math lồng math ──────────
_FILL = re.compile(r"\[\[fill:([^\]|]*?)(?:\|[^\]]+)?\]\]")

# ── 3. Nhịp lời giải: cấm chuỗi diễn giải nhiều tầng trong VÍ DỤ MẪU ───────────
# Thầy 24/09: "chỉ cần xét tam giác vuông ABC, trung tuyến AM / Suy ra AM = 1/2 BC
# = MB = MC / Đó thế thôi." Ví dụ là BẢN MẪU HS chép — viết dài thì HS học viết dài.
_DIEN_GIAI = re.compile(r"\b(?:Do đó|Mặt khác|Từ đó suy ra|Như vậy|Ta thấy rằng)\b")
_VI_DU = re.compile(r"Ví dụ\s*(\d+)")
_LOI_GIAI_TIEU_DE = r"{\sffamily\bfseries\color{brand}Lời giải}"


def _vi_du_blocks(lesson: LessonPackage):
    for st in lesson.stages:
        for b in st.blocks:
            if getattr(b, "type", "") == "noted" and getattr(b, "variant", "") == "example":
                t = getattr(b, "text", "") or ""
                m = _VI_DU.search(t)
                if m:
                    yield f"Ví dụ {m.group(1)}", t, b


def check_lenh_dinh_chu(lesson: LessonPackage) -> list[str]:
    """CHẶN: lệnh LaTeX trần dính liền chữ → Tectonic gãy ngay lúc build."""
    out: list[str] = []
    for st in lesson.stages:
        for i, b in enumerate(st.blocks, 1):
            for attr in ("text", "statement", "solution", "answer"):
                v = getattr(b, attr, None)
                if not isinstance(v, str):
                    continue
                for m in _LENH_TRAN.finditer(v):
                    nhan = getattr(b, "label", "") or f"khối {i}"
                    out.append(
                        f"[{st.kind} · {nhan}] `{m.group(0)}` dính liền chữ ngay sau — "
                        f"Tectonic đọc thành một lệnh không tồn tại và CHẾT. "
                        f"Viết `{m.group(1) and chr(92)+m.group(1)}{{}}` (thêm cặp ngoặc rỗng).")
    return out


def check_trinh_bay(lesson: LessonPackage) -> list[str]:
    """Cảnh báo về cách trình bày (không chặn)."""
    out: list[str] = []
    mon_hinh = "hinh" in (lesson.slug or "") or "hình" in (lesson.grade_label or "").lower()

    # (a) Dòng kẻ: HS trình bày vào VỞ, phiếu không chừa chỗ viết.
    n_ke = sum(1 for st in lesson.stages for b in st.blocks
               if getattr(b, "type", "") == "writelines"
               and getattr(b, "variant", None) != "draw")
    if n_ke:
        out.append(f"trinh_bay: còn {n_ke} khối dòng kẻ — HS trình bày vào VỞ, bỏ hết để "
                   f"tối ưu không gian phiếu (khối `variant: draw` là khung vẽ hình, được giữ).")

    # (b) `answer` và `solution` cùng nội dung ⇒ Sổ tay GV in LỜI GIẢI HAI LẦN.
    for st in lesson.stages:
        for b in st.blocks:
            if getattr(b, "type", "") != "problem":
                continue
            a = (getattr(b, "answer", "") or "").strip()
            s = (getattr(b, "solution", "") or "").strip()
            if not (a and s):
                continue
            def _tho(x: str) -> str:
                x = re.sub(r"\\[a-zA-Z]+|\[\[[^\]]*\]\]|[{}$\\,]", " ", x)
                return re.sub(r"\s+", " ", x).strip().lower()
            r = difflib.SequenceMatcher(None, _tho(a), _tho(s)).ratio()
            if r > 0.40:
                out.append(f"trinh_bay: {b.label} có CẢ `answer` lẫn `solution` giống nhau "
                           f"{r*100:.0f}% — Sổ tay GV in lời giải HAI LẦN. Gộp về một.")

    # (c) Ví dụ mẫu viết diễn giải nhiều tầng thay vì nhịp "cấu hình ⇒ chuỗi đẳng thức".
    for nhan, text, _b in _vi_du_blocks(lesson):
        lg = text.split(_LOI_GIAI_TIEU_DE)[-1]
        tu = sorted({m.group(0) for m in _DIEN_GIAI.finditer(lg)})
        if tu:
            out.append(f"trinh_bay: {nhan} dùng {', '.join(repr(t) for t in tu)} — lời giải mẫu "
                       f"phải theo nhịp đi thi: nêu cấu hình → \\Rightarrow → chuỗi đẳng thức "
                       f"→ dừng. HS chép bản mẫu này nên viết dài là dạy HS viết dài.")

    # (d) Ô [[fill:…]] trong $…$ mà đáp án bọc $ ⇒ math lồng math, Tectonic chết.
    for nhan, text, _b in _vi_du_blocks(lesson):
        for m in _FILL.finditer(text):
            if "$" in m.group(1):
                out.append(f"trinh_bay: {nhan} có ô `[[fill:…]]` mà đáp án bọc `$` — "
                           f"math lồng math, Tectonic chết. Bỏ `$` trong đáp án.")

    # (e) Phiếu HÌNH HỌC mà chặng lý thuyết không có hình nào.
    if mon_hinh:
        for st in lesson.stages:
            if st.kind != "concept":
                continue
            co_hinh = any(getattr(b, "type", "") == "figure"
                          or getattr(b, "figure", None) is not None
                          or "tikzpicture" in (getattr(b, "text", "") or "")
                          for b in st.blocks)
            if not co_hinh:
                out.append("trinh_bay: chặng Kiến thức cần nhớ KHÔNG có hình nào — phiếu hình "
                           "học thì mỗi mục lý thuyết phải kèm một hình minh hoạ.")
    return out
