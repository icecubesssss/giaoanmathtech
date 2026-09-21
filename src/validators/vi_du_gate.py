"""Cổng VÍ DỤ MẪU ↔ BÀI TẬP — Thầy chốt 21/09/2026 (chấm phiếu chương V Hình 9B).

Bốn lỗi Thầy gạch, nay có cổng gác để mỗi lần dựng khỏi phải nhắc lại:

1. **Ví dụ giống hệt bài** — ví dụ chỉ là bài tập chép lại đổi số ⇒ HS chép y nguyên,
   học xong không biết làm bài khác. `check_vi_du_trung_bai`.
2. **Ví dụ không đi cùng bài** — ví dụ dồn thành chuỗi ở đầu chặng, xa nhóm bài của
   dạng đó (có khi khác hẳn chặng). `check_vi_du_di_cung_bai`.
3. **Ví dụ phải là BÀI ĐIỀN KHUYẾT** — thầy trò cùng điền, không phải bài in sẵn đáp số
   để HS đọc suông. `check_vi_du_dien_khuyet`.
4. **Câu THÔNG HIỂU phải có gợi ý trong phiếu luyện tập chương**, và **BỎ gợi ý trong
   phiếu ôn tập giữa kì / cuối kì** (HS phải tự làm như đi thi). `check_goi_y_thong_hieu`.

Mọi hàm trả về list câu cảnh báo (không chặn build) — cùng kiểu với `sgk_style_gate`.
"""
from __future__ import annotations

import difflib
import re

from src.schema import LessonPackage

# ── Chuẩn hoá đề để so khuôn ───────────────────────────────────────────────────
_TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
_LENH = re.compile(r"\\[a-zA-Z]+\**(?:\{[^{}]*\}|\[[^\[\]]*\])*")
_THE_BAND = re.compile(r"\[(?:NB|TH|VD|VDC)\]")
_VI_DU = re.compile(r"\\textbf\{\s*(Ví dụ\s*\d+)\s*[.:]?\s*\}")
_LOI_GIAI = re.compile(r"Lời\s*giải")
_SO = re.compile(r"\d+(?:[,.]\d+)?")
_RAC = re.compile(r"[^\wÀ-ỹ #]+")

# Ô khuyết được chấp nhận trong ví dụ: [[fill:…]] (có đáp án cho Sổ tay GV) hoặc
# [[mblank:W]] / [[blank:W]] (bản cũ, không có đáp án).
_O_KHUYET = re.compile(r"\[\[(?:fill|mblank|blank)[:\]]")
_O_FILL = re.compile(r"\[\[fill:")

# Phiếu ÔN TẬP GIỮA KÌ / CUỐI KÌ và đề kiểm tra: bỏ gợi ý, HS tự làm như đi thi.
_ON_TAP_THI = re.compile(
    r"ôn\s*tập\s*(?:giữa|cuối)\s*(?:kì|kỳ|học\s*kì)|on-tap-(?:gk|ck|hk)|"
    r"đề\s*kiểm\s*tra|de-kiem-tra|thi\s*thử|thi-thu|de-gki|de-cki|gki-cki",
    re.IGNORECASE,
)


def _de_bai(text: str) -> str:
    """Phần ĐỀ (bỏ hình, bỏ lời giải, bỏ lệnh LaTeX, bỏ số) để so hai bài cùng khuôn."""
    s = _TIKZ.sub(" ", text or "")
    s = _LOI_GIAI.split(s)[0]
    s = s.replace("[[br]]", " ")
    s = _THE_BAND.sub(" ", s)
    s = _LENH.sub(" ", s)
    s = _SO.sub("#", s)
    s = _RAC.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def _ten_vi_du(text: str) -> str:
    m = _VI_DU.search(text or "")
    return m.group(1) if m else "Ví dụ"


def _la_vi_du(b) -> bool:
    return (getattr(b, "type", "") == "noted" and getattr(b, "variant", "") == "example"
            and bool(_VI_DU.search(getattr(b, "text", "") or "")))


def _phieu_on_tap_thi(lesson: LessonPackage) -> bool:
    """Phiếu ôn tập GK/CK hay đề kiểm tra? (nhận theo slug + tiêu đề + theme)."""
    if getattr(lesson, "theme", "") == "de_thi":
        return True
    moc = f"{getattr(lesson, 'slug', '')} {getattr(lesson, 'title', '')} {getattr(lesson, 'eyebrow', '')}"
    return bool(_ON_TAP_THI.search(moc))


# ── 1. Ví dụ giống hệt bài ─────────────────────────────────────────────────────
NGUONG_TRUNG = 0.75


def check_vi_du_trung_bai(lesson: LessonPackage, nguong: float = NGUONG_TRUNG) -> list[str]:
    """Ví dụ mẫu KHÔNG được là bài tập chép lại đổi số.

    So đề ví dụ với đề từng bài sau khi bỏ số: giống ≥ `nguong` là một khuôn.
    Ví dụ phải cùng DẠNG với bài nhưng khác cấu hình (đổi chiều dữ kiện, đổi bối cảnh)."""
    out: list[str] = []
    vi_du = [(_ten_vi_du(b.text), _de_bai(b.text)) for st in lesson.stages
             for b in st.blocks if _la_vi_du(b)]
    bai = [(b.label or "?", _de_bai(b.statement)) for st in lesson.stages
           for b in st.blocks if getattr(b, "type", "") == "problem"]
    for ten, de_vd in vi_du:
        if len(de_vd) < 40:          # ví dụ nhắc lý thuyết, không phải bài toán
            continue
        for nhan, de_bt in bai:
            if len(de_bt) < 40:
                continue
            r = difflib.SequenceMatcher(None, de_vd, de_bt).ratio()
            if r >= nguong:
                out.append(
                    f"vi_du_gate: {ten} giống hệt {nhan} ({r:.0%} — chỉ khác số). Ví dụ phải "
                    f"cùng dạng nhưng KHÁC cấu hình (đổi chiều dữ kiện / đổi bối cảnh), "
                    f"không được chép lại đề của bài.")
    return out


# ── 2. Ví dụ không đi cùng bài ─────────────────────────────────────────────────
def check_vi_du_di_cung_bai(lesson: LessonPackage) -> list[str]:
    """Mỗi ví dụ phải đứng NGAY TRƯỚC nhóm bài của dạng đó (Thầy chốt 08/09 + 21/09).

    Hai lỗi bắt được: (a) hai ví dụ dính liền nhau ⇒ đang dồn thành chuỗi;
    (b) ví dụ đứng cuối chặng, sau nó không còn bài nào để áp dụng."""
    out: list[str] = []
    for st in lesson.stages:
        blocks = list(st.blocks)
        for i, b in enumerate(blocks):
            if not _la_vi_du(b):
                continue
            ten = _ten_vi_du(b.text)
            sau = blocks[i + 1:]
            ke_tiep = next((x for x in sau if _la_vi_du(x)
                            or getattr(x, "type", "") == "problem"), None)
            if ke_tiep is None or _la_vi_du(ke_tiep):
                gi = "ví dụ khác" if ke_tiep is not None else "không còn bài nào"
                out.append(
                    f"vi_du_gate: {ten} không đi cùng bài — ngay sau nó là {gi}. Đặt mỗi ví dụ "
                    f"SÁT TRƯỚC nhóm bài cùng dạng (giảng mẫu → trò làm ngay bài tương tự).")
    return out


# ── 3. Ví dụ phải là bài điền khuyết ───────────────────────────────────────────
def check_vi_du_dien_khuyet(lesson: LessonPackage, toi_thieu: int = 2) -> list[str]:
    """Ví dụ mẫu = BÀI ĐIỀN KHUYẾT thầy trò cùng làm (Thầy chốt 21/09/2026).

    Đòi ≥ `toi_thieu` ô khuyết trong phần lời giải, và nhắc dùng [[fill:đáp án]] thay cho
    [[mblank]] để Sổ tay GV vẫn in đủ đáp án."""
    out: list[str] = []
    for st in lesson.stages:
        for b in st.blocks:
            if not _la_vi_du(b):
                continue
            text = b.text or ""
            ten = _ten_vi_du(text)
            n_o = len(_O_KHUYET.findall(text))
            if n_o < toi_thieu:
                out.append(
                    f"vi_du_gate: {ten} chưa phải bài ĐIỀN KHUYẾT ({n_o} ô, cần ≥ {toi_thieu}) — "
                    f"chừa các bước then chốt bằng [[fill:đáp án]] để thầy trò cùng điền.")
            elif not _O_FILL.search(text):
                out.append(
                    f"vi_du_gate: {ten} đang dùng [[mblank]] — đổi sang [[fill:đáp án]] để "
                    f"Sổ tay GV in được đáp án của từng ô.")
    return out


# ── 4. Gợi ý ở câu Thông hiểu ──────────────────────────────────────────────────
def check_goi_y_thong_hieu(lesson: LessonPackage) -> list[str]:
    """Phiếu luyện tập chương: MỌI câu Thông hiểu (level 2) phải có `hints`.
    Phiếu ôn tập GK/CK & đề kiểm tra: NGƯỢC LẠI — phải bỏ hết gợi ý."""
    out: list[str] = []
    on_tap = _phieu_on_tap_thi(lesson)
    for st in lesson.stages:
        for b in st.blocks:
            if getattr(b, "type", "") != "problem" or getattr(b, "level", 0) != 2:
                continue
            nhan = b.label or "?"
            co_goi_y = bool(getattr(b, "hints", None))
            if on_tap and co_goi_y:
                out.append(
                    f"vi_du_gate: {nhan} (Thông hiểu) còn gợi ý — phiếu ôn tập giữa kì / cuối kì "
                    f"phải BỎ gợi ý để HS tự làm như đi thi.")
            elif not on_tap and not co_goi_y:
                out.append(
                    f"vi_du_gate: {nhan} (Thông hiểu) thiếu \"hints\" — phiếu luyện tập chương "
                    f"phải có gợi ý định hướng (không lộ lời giải).")
    return out


# ── 5. Ô [[fill:…]] lồng math trong math ───────────────────────────────────────
_DOLLAR = re.compile(r"(?<!\\)\$")
_FILL_TOKEN = re.compile(r"\[\[fill:([^\]|]*?)(?:\|[^\]]+)?\]\]")


def check_fill_math_long_nhau(lesson: LessonPackage) -> list[str]:
    """Ô nằm TRONG $…$ mà đáp án lại tự bọc $…$ ⇒ Tectonic chết "Missing } inserted".

    Quy ước: đáp án KHÔNG tự bọc $. Ô cần công thức thì đặt token bên trong $…$ của dòng."""
    out: list[str] = []
    for st in lesson.stages:
        for b in st.blocks:
            for attr in ("text", "statement", "solution"):
                text = getattr(b, attr, "") or ""
                if "[[fill:" not in text:
                    continue
                nhan = _ten_vi_du(text) if attr == "text" else (getattr(b, "label", "") or "?")
                for m in _FILL_TOKEN.finditer(text):
                    trong_math = len(_DOLLAR.findall(text[:m.start()])) % 2 == 1
                    if trong_math and "$" in (m.group(1) or ""):
                        out.append(
                            f"vi_du_gate: {nhan} — ô [[fill:{m.group(1)[:24]}…]] nằm trong $…$ mà "
                            f"đáp án lại bọc $…$ (math lồng math ⇒ Tectonic chết). Bỏ cặp $ của đáp án.")
    return out


# ── 6. Số ghi trên HÌNH của ví dụ phải có trong ĐỀ ví dụ ───────────────────────
_NODE = re.compile(r"\\node(?:\[[^\]]*\])?\s*at\s*\([^()]*\)\s*\{")
_SO_NHAN = re.compile(r"\d+(?:[,.]\d+)?")


def _nhan_tikz(tikz: str) -> list[str]:
    """Nội dung mọi nhãn `\\node … {…}` của một hình (ngoặc cân bằng)."""
    ra = []
    for m in _NODE.finditer(tikz):
        i = m.end() - 1
        d, j = 0, i
        while j < len(tikz):
            if tikz[j] == "{":
                d += 1
            elif tikz[j] == "}":
                d -= 1
                if d == 0:
                    break
            j += 1
        ra.append(tikz[i + 1:j])
    return ra


def check_so_tren_hinh_vi_du(lesson: LessonPackage) -> list[str]:
    """Viết lại đề ví dụ mà quên sửa số ghi trên hình ⇒ đề một đằng, hình một nẻo.

    Chỉ soi NHÃN chữ của TikZ (`\\node … {…}`), không đụng toạ độ; nhãn chỉ mang tên điểm
    ($O$, $A$…) thì bỏ qua."""
    out: list[str] = []
    for st in lesson.stages:
        for b in st.blocks:
            if not _la_vi_du(b):
                continue
            text = b.text or ""
            ten = _ten_vi_du(text)
            de = _TIKZ.sub(" ", text)
            so_de = set(_SO_NHAN.findall(de))
            for m_tikz in _TIKZ.finditer(text):
                tikz = m_tikz.group(0)
                nhan_so = [n for n in _nhan_tikz(tikz) if _SO_NHAN.search(n)]
                # Mặt số đồng hồ / thước chia độ: nhiều nhãn số là CHI TIẾT CỦA HÌNH,
                # không phải số liệu đề — soi thì báo oan cả loạt.
                if len(nhan_so) >= 5:
                    continue
                for m in _NODE.finditer(tikz):
                    i = m.end() - 1
                    d, j = 0, i
                    while j < len(tikz):
                        if tikz[j] == "{":
                            d += 1
                        elif tikz[j] == "}":
                            d -= 1
                            if d == 0:
                                break
                        j += 1
                    nhan = tikz[i + 1:j]
                    for so in _SO_NHAN.findall(nhan):
                        if so not in so_de:
                            out.append(
                                f"vi_du_gate: {ten} — hình ghi \"{nhan.strip()}\" mà đề không có "
                                f"số {so}; sửa đề thì phải sửa cả nhãn trên hình.")
    return out


def check_vi_du(lesson: LessonPackage) -> list[str]:
    """Chạy cả bốn luật một lượt (dùng trong `validate` / `audit`)."""
    return (check_vi_du_trung_bai(lesson)
            + check_vi_du_di_cung_bai(lesson)
            + check_vi_du_dien_khuyet(lesson)
            + check_goi_y_thong_hieu(lesson)
            + check_fill_math_long_nhau(lesson)
            + check_so_tren_hinh_vi_du(lesson))
