"""loi_giai_thi_gate — gác ĐÁP ÁN đề kiểm tra / đề ôn tập phải trình bày như HS ĐI THI.

Ba luật Thầy chốt ngày 01/10/2026 khi duyệt bộ 3 đề ôn + đề GK1 lớp 9
(`inputs/seeds/lop-9/de-on-tap-giua-ki-1/`). Mỗi luật là một lần con làm sai thật:

1. KHÔNG dùng dấu ⇔ — *"dấu tương đương HS cũng k được dùng, bạn chỉ đơn giản là xuống
   dòng thôi nhé"*. Mỗi phép biến đổi viết một dòng (nối bằng `[[br]]`), không nối bằng
   `\\Leftrightarrow`.
2. KHÔNG dùng hệ thức lượng trực tiếp — *"HS k được dùng hệ thức lượng trực tiếp, mà cần
   chứng minh tam giác đồng dạng nhé"*. Bước kiểu "△AHB vuông tại H, đường cao HM:
   AM·AB = AH²" phải thay bằng "Xét △AMH và △AHB: … ⇒ △AMH ∽ △AHB (g.g) ⇒ … ⇒ AM·AB = AH²".
3. Bài hình phải CÓ HÌNH trong đáp án — *"Hình k có"*: lời giải ghi "Vẽ hình đúng" mà
   không kèm hình vẽ.

Chỉ áp cho tài liệu `theme: de_thi` (đề HS có `solution` + file "Ma trận và đáp án").
Phiếu học tập có luật ví dụ mẫu riêng (vi_du_gate, sgk_style_gate).
"""
from __future__ import annotations

import re

from src.schema import LessonPackage

__all__ = ["check_loi_giai_thi"]

_TUONG_DUONG = re.compile(r"\\Leftrightarrow|\\iff\b|⇔")
# Một BƯỚC có "đường cao" làm căn cứ + một đẳng thức dạng tích (có \cdot) mà KHÔNG có
# cặp tam giác đồng dạng nào được chứng minh trong chính bước đó ⇒ đang dùng hệ thức lượng.
_DUONG_CAO = re.compile(r"đường\s+cao")
_TICH = re.compile(r"\\cdot[^$]*=|=[^$]*\\cdot|\^2\s*=|=\s*[A-Z]{2}\^2")
_DONG_DANG = re.compile(r"\\backsim|∽|\\sim\b|đồng\s+dạng")
_TEN_HTL = re.compile(r"(?<!dùng )(?<!được dùng )hệ\s+thức\s+lượng", re.IGNORECASE)
# Ghi chú cho GV ("Lưu ý chấm: … HS không được dùng hệ thức lượng") không phải lời giải.
_LUU_Y = re.compile(r"Lưu ý chấm|không được dùng")
_VE_HINH = re.compile(r"[Vv]ẽ\s+hình\s+đúng")
_CO_HINH = re.compile(r"\\begin\{tikzpicture\}|\\includegraphics")
_BUOC = re.compile(r"\s*\[\[br\]\]\s*|\\par\b")


def _cac_doan(lesson: LessonPackage):
    """(nơi, văn bản LỜI GIẢI, stage) — `solution` của bài + khối para (file đáp án)."""
    for st in lesson.stages:
        for i, b in enumerate(st.blocks, 1):
            t = getattr(b, "type", "")
            if t == "problem":
                sol = getattr(b, "solution", "") or ""
                if sol:
                    yield f"[{st.kind} · {getattr(b, 'label', '') or f'khối {i}'} · lời giải]", sol, st
            elif t == "para":
                yield f"[{st.kind} · khối {i}]", getattr(b, "text", "") or "", st


def check_loi_giai_thi(lesson: LessonPackage) -> list[str]:
    """CHẶN (đề `de_thi`): ⇔ trong lời giải, hệ thức lượng dùng trực tiếp, bài hình thiếu hình."""
    if getattr(lesson, "theme", "") != "de_thi":
        return []
    out: list[str] = []
    for noi, txt, st in _cac_doan(lesson):
        if _TUONG_DUONG.search(txt):
            out.append(f"{noi} lời giải dùng dấu ⇔ — HS đi thi KHÔNG dùng dấu tương đương; "
                       f"mỗi phép biến đổi viết một dòng ([[br]]) (Thầy 01/10/2026).")
        if _TEN_HTL.search(txt) and not _LUU_Y.search(txt):
            out.append(f"{noi} lời giải viện dẫn \"hệ thức lượng\" — HS phải chứng minh hai tam giác "
                       f"đồng dạng rồi mới suy ra tích (Thầy 01/10/2026).")
        for buoc in _BUOC.split(txt):
            if _DUONG_CAO.search(buoc) and _TICH.search(buoc) and not _DONG_DANG.search(buoc):
                ngan = re.sub(r"\s+", " ", buoc)[:90]
                out.append(f"{noi} dùng hệ thức lượng TRỰC TIẾP («{ngan}») — viết \"Xét △… và △…: "
                           f"góc vuông, góc chung ⇒ △… ∽ △… (g.g) ⇒ tỉ số ⇒ tích\" (Thầy 01/10/2026).")
        if _VE_HINH.search(txt) and not _CO_HINH.search(txt):
            # file đáp án: hình có thể là khối `figure` riêng trong cùng chặng
            co_figure = any(getattr(b, "type", "") == "figure" and (getattr(b, "tikz", "") or getattr(b, "image", ""))
                            for b in st.blocks)
            la_bai = noi.endswith("lời giải]")
            if la_bai or not co_figure:
                out.append(f"{noi} đáp án ghi \"Vẽ hình\" nhưng KHÔNG kèm hình vẽ — chèn hình ngay đầu "
                           f"lời giải bài hình (Thầy 01/10/2026: \"Hình k có\").")
    return out
