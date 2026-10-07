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
    r"(?=([A-Za-zÀ-ỹĐđ]+))")
# Lệnh LaTeX THẬT có tên bắt đầu bằng một lệnh trong danh sách trên — không phải lỗi dính
# chữ. `\parallel` (song song) từng bị chặn oan khi dựng chương V bản 2 (05/10/2026).
_LENH_HOP_LE = {"parallel", "partial", "paragraph", "parbox", "parskip", "parindent",
                "smallskip", "smallint", "smallsetminus", "largestar"}

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
                    if m.group(1) + m.group(2) in _LENH_HOP_LE:
                        continue
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

    # (e) Phiếu HÌNH HỌC mà chặng lý thuyết không có hình nào. Tờ ĐỀ KIỂM TRA (theme de_thi)
    # không có chặng lý thuyết — chặng "concept" chỉ là khung chứa phần tự luận.
    if mon_hinh and getattr(lesson, "theme", "") != "de_thi":
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

    # (f) Dùng định lí KHÔNG có trong SGK KNTT (Thầy bắt 24/09/2026, phiếu 2 ch.V 9C):
    #     "đường kính ⊥ dây ⇒ qua trung điểm" và "dây bằng nhau ⇔ cách đều tâm" là định lí
    #     sách CŨ. KNTT 9 Bài 14 chỉ có "đường kính là dây lớn nhất" ⇒ mỗi lần dùng phải đi
    #     qua △OAB cân (đường cao đồng thời là trung tuyến), hoặc qua OH² = R² − AH².
    if mon_hinh:
        for st in lesson.stages:
            for b in st.blocks:
                nhan = getattr(b, "label", "") or ""
                for attr in ("text", "statement", "answer", "solution"):
                    txt = getattr(b, attr, "") or ""
                    if not nhan and attr == "text":
                        m = _VI_DU.search(txt)
                        nhan = f"Ví dụ {m.group(1)}" if m else "(lý thuyết)"
                    for dong in re.split(r"\[\[br\]\]|\n", txt):
                        suy = re.search(r"\\Rightarrow|\bnên\b|suy ra", dong)
                        if (suy and "\\perp" in dong and "trung điểm" in dong
                                and not _CAN_CU_CAN.search(dong)):
                            out.append(f"trinh_bay: {nhan or '?'} suy '⊥ ⇔ trung điểm' thẳng "
                                       f"— SGK KNTT KHÔNG có định lí này. Viết đủ: OA = OB = R ⇒ "
                                       f"△OAB cân tại O ⇒ đường cao OH đồng thời là trung tuyến.")
                        if (suy and "cách đều tâm" in dong
                                and not re.search(r"\^2|Pythagore|mục", dong)):
                            out.append(f"trinh_bay: {nhan or '?'} dùng 'dây bằng nhau ⇔ cách đều "
                                       f"tâm' như định lí — KNTT không có; suy qua OH² = R² − AH².")
    return out + check_nhip_loi_giai(lesson)


_CAN_CU_CAN = re.compile(r"cân|trung tuyến|đường cao|trung trực|mục 2")


# ── (g) NHỊP LỜI GIẢI ĐI THI: mỗi bước một dòng, có căn cứ (Thầy nhắc 27/09/2026) ─────
# *"check lại các lỗi trình bày như chưa xuống dòng, trình bày không như HS trình bày khi
# đi thi"*. Soi từng DÒNG (tách theo [[br]]) của ví dụ mẫu và lời giải bài TH/VD — đúng
# phần HS chép theo. Bảy lỗi đã gặp thật ở chương V lớp 9C:
_MATH = re.compile(r"(?<!\\)\$.*?(?<!\\)\$")
_HAI_CAU = re.compile(r"\.\s+(?=Vậy|Xét|Gọi|Kẻ|Mà|Theo|Tương tự|Hai lần|§)")
_PYTHAGORE_TINH = re.compile(r"(?:[A-Z]{2}\^2|\d+\^2)\s*[-+]\s*(?:[A-Z]{2}\^2|\d+\^2)")
_NOI_DAI = re.compile(r"\b(?:Do đó|Mặt khác|Như vậy|suy ra|Suy ra)\b|\\implies|\\hspace\*")
_BAI_TRINH_BAY = ("solution", "answer")


def _dong_loi_giai(lesson: LessonPackage):
    """(nhãn, [dòng…]) cho ví dụ mẫu (phần sau "Lời giải") và lời giải bài TH/VD."""
    for st in lesson.stages:
        for b in st.blocks:
            if getattr(b, "type", "") == "noted" and getattr(b, "variant", "") == "example":
                t = b.text or ""
                m = _VI_DU.search(t)
                if "Lời giải" in t:
                    yield (f"Ví dụ {m.group(1)}" if m else "Ví dụ"), t.split("Lời giải", 1)[1].split("[[br]]")[1:]
            elif (getattr(b, "type", "") == "problem" and (getattr(b, "level", 0) or 0) >= 2
                  and not re.search(r"\[\[blank|\\ldots", getattr(b, "statement", "") or "")):
                # Bài khung ĐIỀN KHUYẾT: `answer` chỉ là đáp án từng ô, khung trong đề mới là bài giải.
                for k in _BAI_TRINH_BAY:
                    t = getattr(b, k, "") or ""
                    if t:
                        yield (b.label or "?"), t.split("[[br]]")


def check_nhip_loi_giai(lesson: LessonPackage) -> list[str]:
    """Cảnh báo lời giải không theo nhịp bài thi: dồn nhiều bước một dòng, "Vậy" dính dòng
    trên, tính Pythagore không nêu căn cứ, nối lời bằng "Do đó/suy ra", thiếu câu "Vậy"."""
    if getattr(lesson, "theme", "") == "de_thi":
        return []                     # tờ đề / đáp án có barem riêng, soi bằng mắt
    out: list[str] = []
    for nhan, dong in _dong_loi_giai(lesson):
        loi: list[str] = []
        for i, d in enumerate(dong):
            ngoai = _MATH.sub("§", d)
            if _HAI_CAU.search(ngoai) or (re.search(r";\s*§", ngoai) and d.count("=") >= 2):
                loi.append("nhiều bước trên một dòng")
            if "Vậy" in ngoai and not ngoai.lstrip().startswith("Vậy"):
                loi.append("\"Vậy\" dính dòng trên")
            if _PYTHAGORE_TINH.search(d):
                ke = " ".join(dong[max(0, i - 1):i + 3])   # Pythagore đảo nêu tên ở dòng kết luận
                if "Pythagore" not in ke:
                    loi.append("tính theo Pythagore mà không nêu \"theo định lí Pythagore\"")
            if "theo Pythagore" in d:
                loi.append("\"theo Pythagore\" → \"theo định lí Pythagore\"")
            if _NOI_DAI.search(d):
                loi.append("nối lời dài (Do đó / suy ra / \\implies / \\hspace*)")
        if not any("Vậy" in d for d in dong):
            loi.append("thiếu câu \"Vậy …\"")
        if loi:
            out.append(f"trinh_bay: {nhan} — lời giải chưa đúng nhịp đi thi: "
                       f"{'; '.join(dict.fromkeys(loi))}. Mỗi bước một dòng, căn cứ trước, \"Vậy\" dòng riêng.")
    return out
