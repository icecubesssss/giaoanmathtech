"""print_gate — soi BẢN IN sau khi build: trang loãng, tiêu đề chặng mồ côi.

Thầy chốt 15/08/2026: mấy lỗi bố cục chỉ lộ ra khi NHÌN PDF, spec/JSON không thấy được
(hộp hình đè nhau, đầu mục "3. Luyện tập 1" nằm trơ cuối trang rồi bài nhảy sang trang
sau, trang bỏ trống 70%). Cổng này đọc PDF ĐÃ BUILD nên bắt được đúng thứ Thầy nhìn thấy.

Hai luật:
  • TRANG HỤT ĐÁY — nội dung dừng quá sớm, chừa một mảng trắng to ở đáy ⇒ phí giấy.
    Trang CUỐI được miễn (tài liệu hết thì hết, không ép được).
  • TIÊU ĐỀ MỒ CÔI — trang kết thúc bằng đầu mục chặng ("3. Luyện tập 1") mà dưới nó
    không còn bài nào; bài đầu tiên của chặng đã bị đẩy sang trang sau.

⚠️ Đo bằng TOẠ ĐỘ chứ KHÔNG đếm ký tự. Bản đầu đếm ký tự/trang, nhưng phiếu HS vốn
đầy dòng kẻ trống để viết — trang chừa chỗ viết tử tế chỉ có vài trăm ký tự nên bị
kêu oan hàng loạt (sau khi vá 666 bài thiếu chỗ viết thì kêu gần như mọi trang).
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

# Đáy trang bỏ trắng quá ngần này (pt; 240pt ≈ 8,4cm) thì coi là phí giấy. Để rộng tay
# vì dòng kẻ / khung vẽ hình KHÔNG phải chữ nên không vào toạ độ text: trang kết thúc
# bằng một bài + 5 dòng kẻ đo ra ~7cm "trắng" mà thật ra đặc. Đo trên chương IV: trang
# hỏng thật 9,2–11,0cm · trang đầy 0,1–7,5cm.
_HUT_DAY = 240.0
# Đầu mục chặng: "3. Luyện tập 1", "5. Sơ đồ tư duy"… Chỉ dùng khi KHÔNG biết
# tiêu đề thật (xem `dau_muc` của check_print_layout): mẫu này ăn nhầm cả mục đánh
# số trong hộp kiến thức ("3. Tính chất hình thang: …") lẫn "Bài 2." nên hay báo oan.
_DAU_MUC = re.compile(r"^\s*\d+\.\s+\S")
# Banner mục phụ (\worksheetsection) — cũng là "đầu mục" theo mắt Thầy nhìn trang in.
_BANNER = ("BÀI TẬP VỀ NHÀ", "BÀI TẬP MỞ RỘNG (TỰ CHỌN)")
# Cuối trang còn bao nhiêu ký tự sau đầu mục thì vẫn coi là mồ côi
_MO_COI_DUOI = 60
# CHÂN TRANG in ở MỌI trang — phải bỏ trước khi đếm, nếu không thì đầu mục nằm trơ
# cuối trang vẫn "còn ~70 ký tự bên dưới" nên lọt cổng (đúng ca Thầy soi 15/08/2026),
# và trang loãng cũng được cộng khống mấy chục ký tự.
_CHAN_TRANG = re.compile(
    r"^\s*(CÔNG TY CỔ PHẦN GIÁO DỤC VÀ CÔNG NGHỆ MATHTECH|Website:.*|\d{1,3})\s*$")


def _bo_chan_trang(txt: str) -> list[str]:
    """Các dòng CÓ NỘI DUNG của trang (đã bỏ dòng trống và chân trang)."""
    return [d for d in txt.splitlines() if d.strip() and not _CHAN_TRANG.match(d)]


def _text_tung_trang(pdf: Path) -> list[str] | None:
    """Trả list text mỗi trang; None nếu máy không có pdftotext (bỏ qua êm)."""
    if not shutil.which("pdftotext") or not pdf.exists():
        return None
    try:
        n = int(re.search(r"^Pages:\s+(\d+)", subprocess.run(
            ["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=60).stdout,
            re.M).group(1))
    except Exception:                                     # noqa: BLE001
        return None
    out = []
    for p in range(1, n + 1):
        r = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"],
                           capture_output=True, text=True, timeout=60)
        out.append(r.stdout)
    return out


_PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
_WORD = re.compile(r'<word [^>]*yMax="([\d.]+)"[^>]*>(.*?)</word>', re.S)
_HOP = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',
                  re.S)

# Dấu CỐ Ý nằm đè lên chữ (mũ của \widehat, vector) — không phải lỗi.
_DAU_TREN = set("ˆ˜¯˙⃗→")
# Giao nhau bao nhiêu pt mới coi là đè thật (nhỏ hơn là do font nhô ra tí).
_DE_NGANG, _DE_DOC = 3.0, 5.0


def _cac_hop(than: str) -> list[tuple[float, float, float, float, str]]:
    return [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in _HOP.findall(than)]


def _la_chi_so_can(tren: str, duoi: str) -> bool:
    """Cặp "chỉ số căn bậc n đè dấu căn" — ký hiệu ĐÚNG, không phải lỗi in.

    `\\sqrt[3]{-27}` dựng ra chữ số 3 nằm lọt trong nhánh trái dấu $\\sqrt{}$, nên hộp
    chữ của nó LUÔN giao với hộp dấu căn. Không loại trừ thì mọi phiếu dạy căn bậc ba
    đều bị báo "bản in hỏng" oan (chương III lớp 9, 16/08/2026).
    """
    t = tren.strip()
    return bool(t) and t.isdigit() and len(t) <= 2 and "√" in duoi


def _soi_de_chu(xml: str) -> list[tuple[int, str, str]]:
    """Tìm CHỮ ĐÈ CHỮ: hai dòng kề nhau mà hộp chữ giao nhau cả ngang lẫn dọc.

    Đây là lỗi Thầy nhìn phát thấy ngay mà mọi cổng cũ đều mù (spec/JSON không thấy,
    print_gate đo đáy trang cũng không thấy): 15/08/2026 một bản `wrapclump` hỏng ép
    hộp cao 3,1cm trong khi ruột 6cm, phần thừa tràn ra đè lên bài kế — lọt tới tận
    Drive mới bị bắt.
    """
    ra: list[tuple[int, str, str]] = []
    for i, (_w, _h, than) in enumerate(_PAGE.findall(xml), 1):
        dong: dict[int, list] = {}
        for w in _cac_hop(than):
            dong.setdefault(round(w[1] / 2), []).append(w)
        khoa = sorted(dong)
        for k1, k2 in zip(khoa, khoa[1:]):
            xong = False
            for a in dong[k1]:
                if xong:
                    break
                if a[4].strip() in _DAU_TREN or "…" in a[4]:
                    continue
                for b in dong[k2]:
                    if "…" in b[4]:
                        continue
                    if _la_chi_so_can(a[4], b[4]):
                        continue
                    if (min(a[2], b[2]) - max(a[0], b[0]) > _DE_NGANG
                            and min(a[3], b[3]) - max(a[1], b[1]) > _DE_DOC):
                        ra.append((i, a[4][:24], b[4][:24]))
                        xong = True
                        break
    return ra


# Lề dưới của vùng chữ (geometry bottom=1.15in) và bề dày dải chân trang. `-bbox` cho
# toạ độ theo TỪNG TỪ nên không lọc chân trang bằng regex dòng được — lọc theo VỊ TRÍ:
# mọi từ nằm dưới (cao trang − _DAI_CHAN) là chân trang, bỏ.
_LE_DUOI = 82.8
_DAI_CHAN = 60.0


def _bbox_xml(pdf: Path) -> str | None:
    """XHTML toạ độ từng từ (`pdftotext -bbox`); None nếu không soi được."""
    if not shutil.which("pdftotext") or not pdf.exists():
        return None
    try:
        return subprocess.run(["pdftotext", "-bbox", str(pdf), "-"],
                              capture_output=True, text=True, timeout=120).stdout
    except Exception:                                     # noqa: BLE001
        return None


def _day_chu_tung_trang(pdf: Path, xml: str | None = None) -> list[tuple[float, float]] | None:
    """Mỗi trang trả (y đáy chữ cuối, y mép dưới vùng chữ) — toạ độ tính từ MÉP TRÊN.

    None nếu không soi được → cổng bỏ qua êm.
    """
    xml = xml if xml is not None else _bbox_xml(pdf)
    if xml is None:
        return None
    out: list[tuple[float, float]] = []
    for _w, h, than in _PAGE.findall(xml):
        cao = float(h)
        chu = [float(y) for y, _t in _WORD.findall(than) if float(y) < cao - _DAI_CHAN]
        out.append((max(chu) if chu else 0.0, cao - _LE_DUOI))
    return out


def _la_dau_muc(dong: str, biet: set[str] | None) -> bool:
    """Dòng này có phải ĐẦU MỤC không? Biết tiêu đề thật thì so khớp thẳng cho chắc."""
    gon = " ".join(dong.split())
    if gon.upper() in _BANNER:
        return True
    return gon in biet if biet is not None else bool(_DAU_MUC.match(dong))


def check_print_layout(pdf: str | Path, dau_muc: list[str] | None = None) -> list[str]:
    """Cảnh báo bố cục bản in. [] khi sạch hoặc không soi được.

    `dau_muc` = danh sách tiêu đề chặng THẬT của phiếu (vd "3. Luyện tập 1"), lấy từ
    lesson lúc build. Có nó thì cổng so khớp thẳng, khỏi đoán bằng mẫu số-chấm — mẫu
    đó ăn nhầm mục đánh số trong hộp kiến thức nên báo oan hàng loạt.
    """
    pdf = Path(pdf)
    trang = _text_tung_trang(pdf)
    if not trang:
        return []
    biet = {" ".join(d.split()) for d in dau_muc} if dau_muc is not None else None
    xml = _bbox_xml(pdf)
    hinh_hoc = _day_chu_tung_trang(pdf, xml) or []

    out: list[str] = []
    # CHỮ ĐÈ CHỮ — hỏng nặng nhất, báo trước.
    for so, a, b in (_soi_de_chu(xml) if xml else [])[:5]:
        out.append(f"print_gate: trang {so} CHỮ ĐÈ CHỮ — {a!r} chồng lên {b!r}; "
                   f"bản in hỏng, KHÔNG được giao cho Thầy.")
    for i, txt in enumerate(trang, 1):
        cuoi_cung = (i == len(trang))
        dong = _bo_chan_trang(txt)

        # Tiêu đề chặng nằm trơ cuối trang. Xét đầu mục CUỐI CÙNG của trang: đầu mục
        # ở giữa trang thì đương nhiên có bài bên dưới, chỉ cái chốt trang mới mồ côi.
        for k in range(len(dong) - 1, -1, -1):
            if _la_dau_muc(dong[k], biet):
                sau = len("".join("".join(dong[k + 1:]).split()))
                if sau < _MO_COI_DUOI:
                    out.append(
                        f"print_gate: trang {i} kết thúc bằng đầu mục '{dong[k].strip()[:40]}' "
                        f"mà dưới nó không còn bài nào — tiêu đề chặng MỒ CÔI, "
                        f"tăng \\stageneedspace trước \\begin{{stage}}.")
                break

        # Đáy trang bỏ trắng một mảng to
        if not cuoi_cung and i <= len(hinh_hoc):
            day_chu, day_trang = hinh_hoc[i - 1]
            trong = day_trang - day_chu
            if day_chu and trong > _HUT_DAY:
                out.append(f"print_gate: trang {i}/{len(trang)} bỏ trắng "
                           f"{trong / 28.45:.1f}cm ở đáy — phí giấy khi in.")
    return out
