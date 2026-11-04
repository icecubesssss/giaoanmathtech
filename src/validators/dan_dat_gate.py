"""Cổng DẪN DẮT phiếu — gom các góp ý Thầy nhắc đi nhắc lại khi duyệt phiếu 2 ch.V 9C
(03–04/11/2026) thành luật máy soi, để phiếu sau khỏi phải nhắc lại.

Thầy 04/11/2026: *"sao các câu sắp xếp lộn xộn và không nhất quán thế nhỉ? bài ở dưới lại
dùng hình ở trên là sao? … chọn được bài có hình tương tự không được hả??? … mấy cái lưu ý
góp ý ở trên cũng tạo thêm thành cổng đi nhé. Tôi muốn phiếu sẽ cần được dẫn dắt từ dễ đến khó."*

Phạm vi: CHẶN với phiếu theo khuôn thang dẫn dắt (có đoạn "Đích của buổi học" — mọi phiếu
chứng minh dựng từ 03/11/2026); phiếu cũ chỉ CẢNH BÁO (≈150 phiếu cũ vấp luật dễ → khó,
chưa được Thầy giao sửa lại). Xem `la_khuon_moi`.

CHẶN (trả về ở `check_dan_dat_chan`):
  1. `check_muon_hinh` — bài/ví dụ dùng HÌNH của bài khác ("dùng Hình 5 ở Bài 5",
     "tiếp tục với Hình…", "tự trình bày lại Bài 4"). Mỗi bài một hình riêng: muốn luyện lại
     thì bốc bài KHÁC có hình tương tự trong tab phân dạng.
  2. `check_de_den_kho` — trong một chặng luyện tập (và trong BTVN), mức độ không được TỤT
     (bài NB đứng sau bài TH/VD); trong một MẠCH (đoạn giữa hai tiêu đề), hình thức đi
     chọn (trắc nghiệm, Đúng/Sai) → điền khuyết → tự trình bày, không quay ngược.
  3. `check_khuon_bon_diem` — chứng minh "bốn/ba điểm cùng thuộc một đường tròn" theo khuôn
     DUY NHẤT △ABC vuông tại A ⇒ A, B, C cùng thuộc đường tròn đường kính BC (Thầy 03/11):
     cấm "Gọi … là trung điểm", "trung tuyến ứng với cạnh huyền", "nửa cạnh huyền", "cách
     đều" — trừ ví dụ nền có dòng "Ghi nhớ" và chặng lý thuyết.
  4. `check_khung_bai_giai` — câu điền khuyết của bài CHỨNG MINH phải là khung bài giải đi
     thi (Thầy 03/11: "HS điền khuyết thì cũng điền khuyết bài trình bày như đi thi", cả
     BTVN): có cụm "hoàn thành bài giải", có dòng "Vậy …" riêng, mỗi dòng tối đa một ⇒.
  5. `check_tieu_de_truoc_btvn` — tiêu đề (para heading) đứng ngay trước bài BTVN đầu tiên
     rơi lên trang sơ đồ tư duy khi BTVN in trang riêng.

CẢNH BÁO (`check_dan_dat_canh_bao`):
  6. `check_dich_buoi` — phiếu chia "Mạch" phải có đoạn "Đích của buổi học" trỏ đúng bài
     đích (bài cuối Luyện tập 2).
"""
from __future__ import annotations

import re

from src.schema import LessonPackage

_HINH = re.compile(r"Hình\s+(\d+)")
_VI_DU = re.compile(r"\\textbf\{\s*Ví dụ\s*(\d+)\s*[.:]?\s*\}")
# "dùng Hình 5 ở Bài 5", "(tiếp tục với Hình 5 …)", "tự trình bày lại Bài 4", "hình của Bài 3"
_MUON = re.compile(
    r"(?:dùng|tiếp tục với|trên|xem|vẽ lại)\s+Hình\s+\d+\s+(?:ở|của)\s+(?:Bài|Ví dụ)"
    r"|tiếp tục với Hình"
    r"|(?:trình bày|làm|giải)\s+lại\s+(?:Bài|Ví dụ)\s*\d+"
    r"|hình (?:của|ở) (?:Bài|Ví dụ)\s*\d+"
    r"|\blàm tiếp\b|\bý\s*[a-e]\s*(?:của|ở)\s*(?:Bài|Ví dụ)\s*\d+",   # đề cụt — phải ghi lại ĐỦ đề (Thầy 04/11)
    re.IGNORECASE)
_TIEU_DE = ("heading", "part")
_KG = re.compile(r"hoàn thành (?:bài|lời) giải")
_O_TRONG = re.compile(r"\[\[(?:blank|mblank|fill)[:\]]|\\ldots|\\dots")
_CM = re.compile(r"Chứng minh|chứng minh")
_SUY = re.compile(r"\\Rightarrow")
_BON_DIEM = re.compile(r"(?:bốn|ba|4|3)\s+điểm[^.]*?cùng\s+(?:thuộc|nằm trên)", re.IGNORECASE)
_KHUON_CU = re.compile(
    r"Gọi\s*\$?[A-Z]\$?\s*là\s*trung điểm|trung tuyến ứng với cạnh huyền|nửa cạnh huyền"
    r"|cách đều (?:bốn|ba|các|4|3) (?:điểm|đỉnh)",
    re.IGNORECASE)


def _problems_and_examples(lesson: LessonPackage):
    """(chặng, chỉ số, block, nhãn) cho mọi bài + ví dụ của các chặng luyện tập/tổng kết."""
    for st in lesson.stages:
        for i, b in enumerate(st.blocks):
            typ = getattr(b, "type", "")
            if typ == "problem":
                yield st, i, b, (getattr(b, "label", "") or "?").rstrip(".")
            elif typ == "noted" and getattr(b, "variant", "") == "example":
                m = _VI_DU.search(getattr(b, "text", "") or "")
                yield st, i, b, (f"Ví dụ {m.group(1)}" if m else "Ví dụ")


def _de(b) -> str:
    """Phần ĐỀ của block (bài: statement; ví dụ: phần trước 'Lời giải')."""
    if getattr(b, "type", "") == "problem":
        return getattr(b, "statement", "") or ""
    return re.split(r"Lời\s*giải", getattr(b, "text", "") or "")[0]


# ── 1. Mượn hình bài khác ─────────────────────────────────────────────────────
def check_muon_hinh(lesson: LessonPackage) -> list[str]:
    chu: dict[str, str] = {}                 # số hình → nhãn block sở hữu
    for st in lesson.stages:
        for b in st.blocks:
            f = getattr(b, "figure", None)
            cap = (getattr(f, "caption", "") or "") if f is not None else ""
            m = _HINH.match(cap.strip())
            if m:
                nhan = (getattr(b, "label", "") or "").rstrip(".")
                if not nhan and getattr(b, "type", "") == "noted":
                    mv = _VI_DU.search(getattr(b, "text", "") or "")
                    nhan = f"Ví dụ {mv.group(1)}" if mv else "(khối lý thuyết)"
                chu[m.group(1)] = nhan or "(khối khác)"
    out: list[str] = []
    for st, _i, b, nhan in _problems_and_examples(lesson):
        if st.kind in ("review", "concept"):
            continue
        de = _de(b)
        m = _MUON.search(de)
        if m:
            out.append(f"dan_dat: {nhan} — '{m.group(0)}': bài dưới dựa vào hình/bài ở trên. "
                       f"Mỗi bài một hình riêng — bốc bài KHÁC có hình tương tự trong tab phân dạng "
                       f"(Thầy 04/11/2026).")
            continue
        f = getattr(b, "figure", None)
        cua_minh = None
        if f is not None:
            mm = _HINH.match((getattr(f, "caption", "") or "").strip())
            cua_minh = mm.group(1) if mm else None
        for so in dict.fromkeys(_HINH.findall(de)):
            if so != cua_minh and so in chu and chu[so] != nhan:
                out.append(f"dan_dat: {nhan} dùng Hình {so} của {chu[so]} — mỗi bài một hình riêng, "
                           f"không mượn hình bài khác (Thầy 04/11/2026).")
    return out


# ── 2. Dễ → khó ───────────────────────────────────────────────────────────────
def _hinh_thuc(b) -> int:
    """0 = chọn (trắc nghiệm, Đúng/Sai, nối cột) · 1 = điền khuyết · 2 = tự trình bày."""
    st = getattr(b, "statement", "") or ""
    if ("\\begin{mcq}" in st or getattr(b, "options", None) or getattr(b, "dung_sai", None)
            or getattr(b, "noi_cot_trai", None) or re.search(r"Đúng\s*(?:/|hay|hoặc)\s*Sai", st)):
        return 0
    if _O_TRONG.search(st):
        return 1
    return 2


_TEN_HT = {0: "trắc nghiệm/Đúng–Sai", 1: "điền khuyết", 2: "tự trình bày"}


def check_de_den_kho(lesson: LessonPackage) -> list[str]:
    out: list[str] = []
    for st in lesson.stages:
        if st.kind in ("review", "concept"):
            continue
        # Mỗi đoạn soi riêng: bài trên lớp của chặng, và BTVN (tier btvn) gom riêng.
        doan: dict[str, list] = {}
        mach_id = 0
        for b in st.blocks:
            typ = getattr(b, "type", "")
            if typ == "para" and getattr(b, "variant", "") in _TIEU_DE:
                mach_id += 1
                continue
            if typ != "problem":
                continue
            seg = "btvn" if getattr(b, "tier", "") == "btvn" else (
                "extend" if getattr(b, "tier", "") == "extend" else "lop")
            if seg == "extend":
                continue
            doan.setdefault(seg, []).append((mach_id, b))
        for seg, ds in doan.items():
            ten_doan = "BTVN" if seg == "btvn" else st.title
            max_lv, max_nhan = 0, ""
            for mach, b in ds:
                lv = getattr(b, "level", 0) or 0
                nhan = (getattr(b, "label", "") or "?").rstrip(".")
                if lv and lv < max_lv:
                    out.append(f"dan_dat: {ten_doan} — {nhan} (mức {lv}) đứng sau {max_nhan} "
                               f"(mức {max_lv}): phiếu phải dẫn dắt từ dễ đến khó, không tụt mức.")
                if lv >= max_lv:
                    max_lv, max_nhan = lv, nhan
            # Hình thức trong cùng mạch + cùng mức: chọn → điền → trình bày.
            truoc: dict[tuple[int, int], tuple[int, str]] = {}
            for mach, b in ds:
                lv = getattr(b, "level", 0) or 0
                ht = _hinh_thuc(b)
                nhan = (getattr(b, "label", "") or "?").rstrip(".")
                k = (mach, lv)
                if k in truoc and ht < truoc[k][0]:
                    out.append(f"dan_dat: {ten_doan} — {nhan} ({_TEN_HT[ht]}) đứng sau {truoc[k][1]} "
                               f"({_TEN_HT[truoc[k][0]]}) trong cùng mạch: đi chọn → điền khuyết → "
                               f"tự trình bày, không quay ngược.")
                if k not in truoc or ht >= truoc[k][0]:
                    truoc[k] = (ht, nhan)
    return out


# ── 3. Khuôn bốn điểm ─────────────────────────────────────────────────────────
def check_khuon_bon_diem(lesson: LessonPackage) -> list[str]:
    out: list[str] = []
    for st, _i, b, nhan in _problems_and_examples(lesson):
        if st.kind in ("review", "concept"):
            continue
        texts = [getattr(b, k, "") or "" for k in ("text", "statement", "answer", "solution")]
        toan = " ".join(texts)
        if not _BON_DIEM.search(toan) or "Ghi nhớ" in toan:
            continue
        m = _KHUON_CU.search(toan)
        if m:
            out.append(f"dan_dat: {nhan} chứng minh điểm cùng thuộc đường tròn bằng khuôn cũ ('{m.group(0)}'). "
                       f"Khuôn duy nhất (Thầy 03/11/2026): △ABC vuông tại A ⇒ A, B, C cùng thuộc "
                       f"đường tròn đường kính BC — không gọi trung điểm, không viết lại trung tuyến.")
    return out


# ── 4. Điền khuyết = khung bài giải đi thi ─────────────────────────────────────
def _la_phieu_hinh(lesson: LessonPackage) -> bool:
    t = " ".join([getattr(lesson, "grade_label", "") or "", getattr(lesson, "eyebrow", "") or "",
                  getattr(lesson, "title", "") or ""]).lower()
    return "hình" in t or "hinh" in t


def check_khung_bai_giai(lesson: LessonPackage) -> list[str]:
    if getattr(lesson, "theme", "") == "de_thi" or not _la_phieu_hinh(lesson):
        return []
    out: list[str] = []
    for st in lesson.stages:
        if st.kind in ("review", "concept"):
            continue
        for b in st.blocks:
            if getattr(b, "type", "") != "problem":
                continue
            s = getattr(b, "statement", "") or ""
            if not (_CM.search(s) and re.search(r"\[\[(?:blank|mblank)", s)) or _hinh_thuc(b) == 0:
                continue
            nhan = (getattr(b, "label", "") or "?").rstrip(".")
            loi: list[str] = []
            if not _KG.search(s):
                loi.append("thiếu lời dẫn \"Điền vào chỗ chấm để hoàn thành bài giải\" (đang là mẩu điền rời)")
                khung = s
            else:
                khung = _KG.split(s, 1)[1]
            dong = [d.strip() for d in khung.split("[[br]]") if d.strip()]
            if len(dong) < 3:
                loi.append(f"khung chỉ {len(dong)} dòng — bài giải đi thi phải đủ các bước")
            if not any(re.sub(r"^[a-z]\)\s*(\[(?:NB|TH|VD|VDC)\]\s*)?", "", d).startswith("Vậy") for d in dong):
                loi.append("thiếu dòng kết luận \"Vậy …\" riêng")
            hai = [d for d in dong if len(_SUY.findall(d)) >= 2]
            if hai:
                loi.append(f"{len(hai)} dòng có hai dấu ⇒ (mỗi mắt suy luận một dòng): '{hai[0][:60]}…'")
            if loi:
                out.append(f"dan_dat: {nhan} — câu điền khuyết bài chứng minh chưa là khung bài giải đi thi: "
                           f"{'; '.join(loi)}. (Thầy 03/11/2026: điền khuyết = điền vào bài trình bày như đi thi, cả BTVN.)")
    return out


# ── 5. Tiêu đề trước BTVN đầu tiên ─────────────────────────────────────────────
def check_tieu_de_truoc_btvn(lesson: LessonPackage) -> list[str]:
    if not (getattr(lesson, "btvn_trang_rieng", False) or getattr(lesson, "btvn_phieu_rieng", False)):
        return []
    for st in lesson.stages:
        trc = None
        for b in st.blocks:
            if getattr(b, "type", "") == "problem" and getattr(b, "tier", "") == "btvn":
                if trc is not None and getattr(trc, "type", "") == "para" and getattr(trc, "variant", "") in _TIEU_DE:
                    return [f"dan_dat: tiêu đề '{(trc.text or '')[:40]}' đứng ngay trước bài BTVN đầu tiên — "
                            f"BTVN in trang riêng nên tiêu đề rơi lại trang trước (trang sơ đồ tư duy). Bỏ tiêu đề này."]
                return []
            trc = b
    return []


# ── 6. Đích của buổi ───────────────────────────────────────────────────────────
def check_dich_buoi(lesson: LessonPackage) -> list[str]:
    luyen = [st for st in lesson.stages if st.kind in ("practice1", "practice2")]
    co_mach = any(getattr(b, "type", "") == "para" and getattr(b, "variant", "") in _TIEU_DE
                  and (getattr(b, "text", "") or "").startswith("Mạch")
                  for st in luyen for b in st.blocks)
    if not co_mach:
        return []
    dich = next(((getattr(b, "text", "") or "") for st in luyen for b in st.blocks
                 if getattr(b, "type", "") == "para" and "Đích của buổi" in (getattr(b, "text", "") or "")), "")
    if not dich:
        return ["dan_dat: phiếu chia Mạch nhưng thiếu đoạn \"Đích của buổi học\" (đề thi đích + ý nào ứng với mạch nào)."]
    m = re.search(r"Bài\s*(\d+)", dich)
    p2 = next((st for st in lesson.stages if st.kind == "practice2"), None)
    cuoi = [b for b in (p2.blocks if p2 else []) if getattr(b, "type", "") == "problem"]
    if m and cuoi and (getattr(cuoi[-1], "label", "") or "").rstrip(".") != f"Bài {m.group(1)}":
        return [f"dan_dat: \"Đích của buổi học\" trỏ Bài {m.group(1)} nhưng bài cuối Luyện tập 2 là "
                f"{(cuoi[-1].label or '?').rstrip('.')} — đích phải là bài chốt buổi."]
    return []


def la_khuon_moi(lesson: LessonPackage) -> bool:
    """Phiếu dựng theo khuôn thang dẫn dắt (03/11/2026): có btvn_phieu_rieng hoặc có stage practice2."""
    return (getattr(lesson, "btvn_phieu_rieng", False)
            or any("Đích của buổi" in (getattr(b, "text", "") or "")
                   for st in lesson.stages for b in st.blocks if getattr(b, "type", "") == "para")
            or any(st.kind == "practice2" for st in lesson.stages))


# ── 7. Lời xưng hô với HS trong đề (Thầy 04/11/2026: "bỏ những lời kiểu em làm cái này cái nọ") ──
_XUNG_HO = re.compile(r"\b(?:các em|em hãy|em đã|em vẽ|em làm|hôm nay|ở lớp)\b|\bem\b(?=\s+[a-zà-ỹ])", re.IGNORECASE)


def check_loi_xung_ho(lesson: LessonPackage) -> list[str]:
    out: list[str] = []
    for st, _i, b, nhan in _problems_and_examples(lesson):
        if st.kind in ("review", "concept"):
            continue
        m = _XUNG_HO.search(_de(b))
        if m:
            out.append(f"dan_dat: {nhan} — đề có lời xưng hô với HS ('{m.group(0)}'): đề viết như đề thi, "
                       f"bỏ lời dặn kiểu 'em làm…', 'trên hình em vẽ hôm nay' (Thầy 04/11/2026).")
    return out


def check_luyen_tap_2_va_btvn_chung_minh(lesson: LessonPackage) -> list[str]:
    """Luyện tập 2 (Chặng 4 - practice2) và bài chứng minh tự luận BTVN:
    HS bắt buộc phải tự vẽ hình (bật draw: true) và tự trình bày lời giải,
    chỉ có đề bài, KHÔNG được điền khuyết (Thầy chốt 04/11/2026:
    'Phần BTVN cũng tương tự nhé! HS cần đọc lại để làm được... Với cái luật Hình HS phải tự vẽ đâu r? Fix thành luật cứng với bài chứng minh và phải vẽ hình nhé')."""
    if getattr(lesson, "theme", "") == "de_thi" or not la_khuon_moi(lesson):
        return []
    out: list[str] = []
    is_hinh = _la_phieu_hinh(lesson)

    # 1. Luyện tập 2 (Chặng 4)
    p2 = next((st for st in lesson.stages if st.kind == "practice2"), None)
    if p2:
        for b in p2.blocks:
            if getattr(b, "type", "") != "problem":
                continue
            s = getattr(b, "statement", "") or ""
            nhan = (getattr(b, "label", "") or "?").rstrip(".")
            if _O_TRONG.search(s) or _KG.search(s):
                out.append(
                    f"dan_dat: {nhan} (Luyện tập 2) — Luyện tập 2 HS bắt buộc phải tự trình bày lời giải, "
                    f"chỉ có đề bài, KHÔNG được điền khuyết (Thầy chốt 04/11/2026: 'Luyện Tập 2 HS bắt buộc "
                    f"phải trình bày lời giải, chỉ có đề thôi nhé!')."
                )
            if is_hinh and _CM.search(s) and not getattr(b, "draw", False):
                out.append(
                    f"dan_dat: {nhan} (Luyện tập 2) — bài chứng minh hình học ở Luyện tập 2 HS bắt buộc "
                    f"phải tự vẽ hình (bật draw: true) (Thầy chốt 04/11/2026: 'Với cái luật Hình HS phải tự vẽ đâu r? Fix thành luật cứng với bài chứng minh và phải vẽ hình nhé')."
                )

    # 2. BTVN
    for st in lesson.stages:
        for b in st.blocks:
            if getattr(b, "type", "") != "problem" or getattr(b, "tier", "") != "btvn":
                continue
            s = getattr(b, "statement", "") or ""
            nhan = (getattr(b, "label", "") or "?").rstrip(".")
            lvl = getattr(b, "level", 1) or 1
            has_options = bool(getattr(b, "options", None) or getattr(b, "dung_sai", None) or getattr(b, "noi_cot_trai", None))
            if is_hinh and lvl >= 2 and _CM.search(s) and not has_options:
                if _O_TRONG.search(s) or _KG.search(s):
                    out.append(
                        f"dan_dat: {nhan} (BTVN) — bài chứng minh tự luận ở BTVN HS bắt buộc phải tự trình bày lời giải, "
                        f"chỉ có đề bài, KHÔNG được điền khuyết (Thầy chốt 04/11/2026: 'Phần BTVN cũng tương tự nhé! HS cần đọc lại để làm được...')."
                    )
                if not getattr(b, "draw", False):
                    out.append(
                        f"dan_dat: {nhan} (BTVN) — bài chứng minh tự luận ở BTVN HS bắt buộc phải tự vẽ hình "
                        f"(bật draw: true) (Thầy chốt 04/11/2026: 'Với cái luật Hình HS phải tự vẽ đâu r? Fix thành luật cứng với bài chứng minh và phải vẽ hình nhé')."
                    )
    return out


def check_phieu_btvn(lesson: LessonPackage) -> list[str]:
    """Thầy chốt 04/11/2026: phiếu tạo từ giờ (khuôn mới) phải tách BTVN thành Phiếu BTVN riêng."""
    co_btvn = any(getattr(b, "type", "") == "problem" and getattr(b, "tier", "") == "btvn"
                  for st in lesson.stages for b in st.blocks)
    if co_btvn and not getattr(lesson, "btvn_phieu_rieng", False):
        return ["dan_dat: phiếu có BTVN nhưng chưa bật `btvn_phieu_rieng: true` — từ 04/11/2026 mọi phiếu "
                "mới tách BTVN thành file Phiếu BTVN riêng (Thầy chốt)."]
    return []


def check_dan_dat_chan(lesson: LessonPackage) -> list[str]:
    return (check_muon_hinh(lesson) + check_de_den_kho(lesson) + check_khuon_bon_diem(lesson)
            + check_khung_bai_giai(lesson) + check_tieu_de_truoc_btvn(lesson) + check_loi_xung_ho(lesson)
            + (check_phieu_btvn(lesson) if la_khuon_moi(lesson) else [])
            + check_luyen_tap_2_va_btvn_chung_minh(lesson))


def check_dan_dat_canh_bao(lesson: LessonPackage) -> list[str]:
    return check_dich_buoi(lesson)
