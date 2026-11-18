#!/usr/bin/env python3
"""Sơ đồ Phiếu 1 ch.VII 9C (18/11/2026) — "Bảng tần số, tần số tương đối, ghép nhóm (Bài 22–24)".

Một phiếu 180′ trọn buổi t31 (Thầy chốt 17/11), khuôn `khong_vd`, cờ `luat_16_11`. Mã câu = chon-cau.json
(Thầy duyệt tab 9074 ngày 18/11: 56 Hay, dòng 19 Trung Vương GK2 "Không hay" ⇒ Lê Ngọc Hân GK2 2025 Bài I).
dang_id ↔ dòng TM phiếu 1: NB1 kiến thức cũ · NB2 C7-01 · NB3 C7-02 · NB4 C7-05 · NB5 C7-03 · NB6–NB10 câu NB
tách từ bài TH (C7-02, 05, 04, 03, 09) · TH1 C7-02 · TH2 C7-04 · TH3 C7-03 · TH4 C7-05 · TH5 C7-09.

Claude CHỐT ĐỀ (nguyên văn đề gốc, tách ý theo luật 16/11 + 17/11), thẻ, đáp số (máy đếm ở kiem()).
Bảng / biểu đồ vẽ bằng máy (hinh_thong_ke.py). Gemini chỉ viết lời giải, ví dụ điền khuyết, mở đầu, lý thuyết.

    .venv/bin/python scripts/gemini/so_do_p1_ch7_9c.py      # kiểm đáp số + đếm thẻ theo dang_id
"""
from __future__ import annotations

import collections
import re
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinh_thong_ke as HT  # noqa: E402

BR = "[[br]]"

# ── HÌNH: token trong đề; latex() thay bằng TikZ/bảng, cho_tho() thay bằng mô tả chữ cho Gemini ──────────
_HINH: list[tuple[str, str]] = []
_LOAI: list[str] = []


def _tok(tex: str, mota: str, loai: str = "bang") -> str:
    _HINH.append((tex, mota))
    _LOAI.append(loai)
    return f"⟦H{len(_HINH) - 1}⟧"


def xep(s: str) -> str:
    """Đề có đúng MỘT biểu đồ (không bảng) và có câu hỏi sau hình ⇒ hình sang phải, câu hỏi bên trái."""
    ids = [int(i) for i in re.findall(r"⟦H(\d+)⟧", s)]
    if len(ids) != 1 or _LOAI[ids[0]] != "hinh":
        return s
    tr, sau = s.split(f"⟦H{ids[0]}⟧")
    if not sau.strip() and "[[br]]" in tr:          # hình ở cuối đề (Ví dụ 1 ý b): đặt cạnh đoạn cuối
        tr, sau = tr.rsplit("[[br]]", 1)
        tr += "[[br]]"
    if not tr.strip() or not sau.strip():
        return s
    return tr + HT.ben_phai(sau, _HINH[ids[0]][0])


# Thầy 18/11: "Bài 2 cắt xuống trang khác, biểu đồ cho to lên để choán hết đám trắng" — soi thấy trang trắng thì
# phóng hình của bài trên trang đó: nhãn → bề rộng hình (phần \\linewidth), hình xếp DỌC, to trọn bề ngang.
PHONG = {"Bài 2.": 0.72, "Bài 3.": 0.62, "Bài 16.": 0.85}
PHONG_BANG: dict = {}    # nhãn → hệ số phóng BẢNG (bài chỉ có bảng / lưới số)
_TU_DO = Path(__file__).with_name("phong_p1_ch7_9c.json")   # do toi_uu_trang_p1_ch7_9c.py ghi (quét lấp trang)
if _TU_DO.exists():
    import json as _json
    _d = _json.loads(_TU_DO.read_text())
    PHONG.update(_d.get("hinh", {}))
    PHONG_BANG.update(_d.get("bang", {}))
# đoạn đề trước hình không được tách khỏi hình (Thầy 18/11: đề cuối trang 5, hình đầu trang 6)
GIU_ON = r"\interlinepenalty=10000\clubpenalty=10000\widowpenalty=10000 "
GIU_OFF = r"\interlinepenalty=0\clubpenalty=150\widowpenalty=150 "


def _phong(tex: str, r: float) -> str:
    noi = HT.ruot(tex)
    return (r"\par\nopagebreak\smallskip\nopagebreak{\centering\adjustbox{width=" + f"{r}" + r"\linewidth}{" + noi + "}"
            + r"\par}\smallskip ")


def _phong_bang(tex: str, f: float) -> str:
    return (r"\par\nopagebreak\smallskip\nopagebreak{\centering\adjustbox{scale=" + f"{f}" + r",max width=\linewidth}{"
            + HT.ruot(tex) + r"}\par}\smallskip ")


def latex(s: str, nhan: str = "") -> str:
    ids = [int(i) for i in re.findall(r"⟦H(\d+)⟧", s)]
    hinh = [i for i in ids if _LOAI[i] == "hinh"]
    if nhan in PHONG and hinh:
        h = hinh[0]
        s = s.replace(f"⟦H{h}⟧", "⟦P⟧")
        out = re.sub(r"⟦H(\d+)⟧", lambda m: _HINH[int(m[1])][0], s).replace("⟦P⟧", _phong(_HINH[h][0], PHONG[nhan]))
    elif nhan in PHONG_BANG and not hinh:
        out = re.sub(r"⟦H(\d+)⟧", lambda m: _phong_bang(_HINH[int(m[1])][0], PHONG_BANG[nhan]), s)
    else:
        out = re.sub(r"⟦H(\d+)⟧", lambda m: _HINH[int(m[1])][0], xep(s))
    k = out.find(r"\par")
    if k > 0 and "⟦" not in out:
        j = k + len(r"\par")
        out = GIU_ON + out[:j] + r"\nopagebreak" + GIU_OFF + out[j:]
    return out


def cho_tho(s: str) -> str:
    return re.sub(r"⟦H(\d+)⟧", lambda m: f" [HÌNH/BẢNG: {_HINH[int(m[1])][1]}] ", s)


def _o(c) -> str:
    return HT.vn(c) if isinstance(c, (int, float, F)) else re.sub(r"\\textbf\{|\}|\$", "", str(c))


def B(*hang, dam=True):
    return _tok(HT.bang([list(h) for h in hang], dam_cot1=dam),
                "bảng " + " / ".join(" | ".join(_o(c) for c in h) for h in hang))


def L(so, k):
    return _tok(HT.luoi(list(so), k), "dãy số liệu (bảng không tiêu đề): " + "; ".join(_o(c) for c in so))


def C(nhan, gt, tx, ty, ymax, buoc, sat=False, tren=None, tieu_de="", **kw):
    if sat:
        mo = [f"[{HT.vn(nhan[i])}; {HT.vn(nhan[i + 1])}): {_o(tren[i]) if tren else HT.vn(gt[i])}"
              for i in range(len(gt))]
    else:
        mo = [f"{_o(nhan[i])}: {_o(tren[i]) if tren else HT.vn(gt[i])}" for i in range(len(gt))]
    loai = "biểu đồ cột tần số ghép nhóm (cột sát nhau)" if sat else "biểu đồ cột"
    return _tok(HT.cot(nhan, gt, tx, ty, ymax, buoc, sat=sat, tren=tren, tieu_de=tieu_de, **kw),
                f"{loai} \"{tieu_de}\", trục ngang {_o(tx)}, trục đứng {_o(ty)}; " + "; ".join(mo), "hinh")


def D(nhan, gt, tx, ty, ymax, buoc, tieu_de="", **kw):
    return _tok(HT.doan(nhan, gt, tx, ty, ymax, buoc, tieu_de=tieu_de, **kw),
                f"biểu đồ đoạn thẳng \"{tieu_de}\", trục ngang {_o(tx)}, trục đứng {_o(ty)}; "
                + "; ".join(f"{_o(a)}: {HT.vn(b)}" for a, b in zip(nhan, gt)), "hinh")


def Q(pt, chu, tieu_de=""):
    return _tok(HT.quat(pt, chu, tieu_de=tieu_de),
                f"biểu đồ hình quạt tròn \"{tieu_de}\"; " + "; ".join(f"{_o(c)}: {HT.vn(p)}%" for p, c in zip(pt, chu)), "hinh")


def T(nhom, so, chu):
    return _tok(HT.tranh(nhom, so, chu),
                "biểu đồ tranh; " + "; ".join(f"{a}: {b} biểu tượng" for a, b in zip(nhom, so)) + f" ({chu})", "hinh")


def P(*tok, rong=0.47):
    """Hai hình cạnh nhau: gộp các token đã tạo thành một token."""
    ids = [int(re.match(r"⟦H(\d+)⟧", t)[1]) for t in tok]
    return _tok(HT.canh(*[_HINH[i][0] for i in ids], rong=rong), " ; ".join(_HINH[i][1] for i in ids))


def tn(*o):
    """Bốn phương án A–D chia cột đều (18/11 Thầy: phương án "ríu vào nhau"): ngắn 4 cột, vừa 2 cột, dài 1 cột."""
    dai = max(len(re.sub(r"\\[a-zA-Z]+|[{}$\\]", "", x)) for x in o)
    w, moi = ("0.23", 4) if dai <= 9 else ("0.46", 2) if dai <= 30 else ("0.92", 1)
    o = [rf"\makebox[{w}\linewidth][l]{{{c}. {x}}}" for c, x in zip("ABCD", o)]
    return "".join("[[br]]\\hspace*{1.4em}" + "".join(o[i:i + moi]) for i in range(0, 4, moi))


DS = r"Mỗi khẳng định sau đúng hay sai?"


def y(*ds):
    return BR.join(ds)


# ── NGUỒN in sau đề ───────────────────────────────────────────────────────────
DD = r"đề minh họa tuyển sinh lớp 10, Phòng GD\&ĐT Đống Đa, "
N = {
    "bvd2": DD + r"đề 02 (THCS Bế Văn Đàn), 2025--2026", "bvd1": DD + r"đề 01 (THCS Bế Văn Đàn), 2025--2026",
    "lnh25": r"GK2 THCS Lê Ngọc Hân, 2025--2026", "lnh24": r"GK2 THCS Lê Ngọc Hân, 2024--2025",
    "xd": r"HK2 THCS Xuân Đỉnh, 2025--2026", "hm": r"HK2 THCS Hát Môn (Phúc Thọ), 2025--2026",
    "hn26": r"đề tuyển sinh lớp 10 Hà Nội, 2026--2027", "hn25": r"đề tuyển sinh lớp 10 Hà Nội, 2025--2026",
    "hnmh": r"đề minh họa tuyển sinh lớp 10 Hà Nội", "gl": r"HK2 Phòng GD\&ĐT Gia Lâm, 2024--2025",
    "tl": r"thi thử vào 10 THCS Tự Lập, 2025--2026", "cva": r"HK2 THCS Chu Văn An (Tây Hồ), 2024--2025",
    "kt": DD + r"đề 07 (THCS Khương Thượng), 2025--2026",
    "hd": r"khảo sát lớp 9 Phòng GD\&ĐT Hà Đông, 2025--2026",
    "tll2": r"thi thử vào 10 lần 2 THCS Thọ Lộc, 2025--2026", "tll5": r"thi thử vào 10 lần 5 THCS Thọ Lộc, 2025--2026",
    "tll3": r"thi thử vào 10 lần 3 THCS Thọ Lộc, 2026--2027",
    "tt26": r"thi thử vào 10 THCS Thái Thịnh, 2026--2027", "tt25": DD + r"đề 14 (THCS Thái Thịnh), 2025--2026",
    "cg": r"HK2 Phòng GD\&ĐT Cầu Giấy, 2024--2025", "lt": DD + r"đề 08 (THCS Láng Thượng), 2025--2026",
    "lmns": r"HK2 THCS\&THPT M.V. Lômônôxốp, 2024--2025", "cm2": r"thi thử vào 10 lần 2 Phòng GD\&ĐT Chương Mỹ, 2025--2026",
    "cm4": r"thi thử vào 10 lần 4 Phòng GD\&ĐT Chương Mỹ, 2025--2026",
    "cl": DD + r"đề 03 (THCS Cát Linh), 2025--2026", "to": r"thi thử vào 10 lần 2 Phòng GD\&ĐT Thanh Oai, 2025--2026",
    "cum": r"thi thử vào 10 cụm trường THCS công lập, 2026--2027", "dg": r"GK2 THCS Đức Giang, 2025--2026",
    "ntl": r"GK2 THCS Nam Từ Liêm, 2025--2026", "nd": r"HK2 THCS Nguyễn Du, 2025--2026",
    "nbk": r"GK2 THCS Nguyễn Bỉnh Khiêm, 2024--2025", "ngt": r"HK2 THCS Ngô Gia Tự (Việt Hưng), 2025--2026",
    "vd": r"HK2 THCS Thị trấn Văn Điển, 2024--2025", "nt": r"HK2 THCS Ngọc Thụy, 2024--2025",
    "dd5": DD + r"đề 05 (THCS Đống Đa), 2025--2026", "lhp": r"GK2 THCS Lê Hồng Phong, 2025--2026",
    "nl24": r"GK2 THCS Ngọc Lâm, 2024--2025", "tlmt": r"tài liệu Mathtech \textquotedblleft Tần số. Tần số tương đối\textquotedblright",
    "hdu": r"HK2 Phòng GD\&ĐT Hoài Đức, 2024--2025", "tv": r"HK2 THCS Trưng Vương, 2025--2026",
    "cd": r"HK2 THCS Cầu Diễn (Nam Từ Liêm), 2025--2026",
}


def ng(k):
    return r" \textit{(" + N[k] + ")}"


def sgk(s):
    return r" \textit{(SGK Toán 9 tập hai, " + s + ")}"


# ── SỐ LIỆU (dùng chung cho hình + kiem) ──────────────────────────────────────
GIAY = [40, 36, 37, 36, 40, 38, 39, 38, 37, 36, 40, 39, 36, 38, 37, 38, 38, 37, 38, 38, 38, 36]
DEN = [1180, 1150, 1190, 1170, 1180, 1170, 1160, 1170, 1160, 1150, 1190, 1180, 1170, 1170, 1170, 1190, 1170, 1170,
       1170, 1180, 1170, 1160, 1160, 1160, 1170, 1160, 1180, 1180, 1150, 1170]
HM = [7, 4, 4, 6, 6, 4, 6, 8, 8, 7, 2, 6, 4, 8, 5, 6, 9, 8, 4, 7, 9, 5, 5, 5, 7, 2, 7, 6, 7, 8, 6, 10]
KK = "M1 M1 M2 M2 M2 M2 M1 M2 M2 M2 M2 M2 M2 M2 M2 M4 M1 M3 M3 M3 M4 M4 M1 M1 M1 M1 M3 M3 M3 M1".split()
HO = [3, 2, 2, 4, 5, 5, 6, 7, 3, 4, 4, 4, 5, 4, 6, 6, 7, 3, 4, 5]
CAO_SGK = [156, 157, 164, 166, 166, 165, 157, 154, 155, 158, 160, 163, 163, 161, 162, 159, 159, 160, 160, 160, 159,
           158, 160, 160, 158, 163, 162, 162, 162, 161, 162, 161, 163, 161, 163, 161, 164, 166, 165, 165]
CAO_CL = [140, 142, 145, 141, 147, 148, 150, 155, 156, 157, 158, 158, 159, 160, 159, 159, 160, 161, 162, 162, 163,
          163, 165, 165, 167, 169, 168, 169, 170, 172, 175, 173, 174, 172, 172, 171, 177, 166, 166, 158, 155, 160,
          158, 159, 155, 157, 164, 165, 164, 177]
DIEN = [150, 120, 180, 200, 130, 100, 160, 190, 219, 210, 170, 140, 110, 130, 160, 180, 150, 200, 210, 190]
VS = ("Tốt, Trung bình, Tốt, Trung bình, Khá, Tốt, Khá, Tốt, Tốt, Khá, Trung bình, Kém, Khá, Tốt, Khá, Tốt, "
      "Trung bình, Khá, Tốt, Tốt, Tốt, Khá, Kém, Trung bình, Tốt, Khá, Tốt, Khá, Tốt, Khá, Khá").split(", ")
CHU = "I S I I H S H B I I H H I H I H I I H S H".split()
HD = [9, 15, 11, 15, 10, 9, 10, 12, 11, 10, 12, 10, 9, 12, 9, 15]
HDI = [0.939, 0.829, 0.803, 0.8, 0.705, 0.703, 0.699, 0.607, 0.607, 0.593, 0.585]


def dem(ds, nhom=None):
    if nhom is None:
        return dict(sorted(collections.Counter(ds).items()))
    return [sum(1 for v in ds if a <= v < b) for a, b in nhom]


def pt(m, n):
    return F(m, n) * 100


# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# Tiêu đề: (chữ, chặng, "heading").
# Ví dụ:  (nhãn, chặng, "", "", 0, mã, "", "vi_du", ĐỀ IN (có nguồn), GHI lời giải cho thợ).
# Bài:    (nhãn, chặng, tier, dang_id, level, mã, "", hình thức, ĐỀ IN NGUYÊN VĂN, GHI đáp số cho thợ).
NAM = ["2015--2016", "2016--2017", "2017--2018", "2018--2019", "2019--2020"]
KHOI = [
    # ───────────── LUYỆN TẬP 1 — chỉ NB (21 thẻ) ─────────────
    ("Mạch 1. Lập bảng tần số", "practice1", "heading"),
    ("Ví dụ 1.", "practice1", "", "", 0, "sgk-b22-vd1 + sgk-7.3", "", "vi_du",
     y(r"a) Để mua giày thể thao cho các bạn nam trong lớp luyện tập chuẩn bị cho giải bóng đá của trường, Huy đã thu "
       r"thập cỡ giày của các bạn nam trong lớp và thu được kết quả như sau:",
       r"\hspace*{1.4em}" + ", ".join(f"${v}$" for v in GIAY) + ".",
       r"Lập bảng tần số cho dãy dữ liệu trên. Từ bảng tần số, cho biết cỡ giày nào phù hợp với nhiều bạn nam trong lớp "
       r"nhất." + sgk("Bài 22, Ví dụ 1"),
       r"b) Biểu đồ dưới đây cho biết số ngày sử dụng phương tiện đến trường của bạn Mai trong tháng Chín. Lập bảng tần "
       r"số cho dữ liệu được biểu diễn trên biểu đồ." + sgk("Bài tập 7.3"))
     + C(["Xe buýt", "Xe máy", "Xe đạp"], [9, 5, 8], "Phương tiện", "Số ngày", 16, 4,
         tieu_de="Phương tiện đến trường của Mai", bw=1.0, gap=0.8),
     "a) Đếm từng cỡ: 36 có 5, 37 có 4, 38 có 8, 39 có 2, 40 có 3 (tổng 22 = số bạn). Kẻ bảng tần số dạng ngang hai "
     "dòng \"Cỡ giày | 36 | 37 | 38 | 39 | 40\" và \"Tần số | 5 | 4 | 8 | 2 | 3\" bằng tabular trong lời giải, các ô tần "
     "số là ô fill. Cỡ 38 có tần số lớn nhất (8) nên phù hợp nhiều bạn nhất. b) Đọc chiều cao từng cột: Xe buýt 9, "
     "Xe máy 5, Xe đạp 8 ⇒ bảng tần số (ô fill). Cuối mỗi ý một dòng \"Vậy …\". 7–9 ô."),
    # 18/11 Thầy: đẩy Ví dụ 1 lên trước Bài 1 cho kín trang 4 (hộp ví dụ không ngắt trang)
    ("Bài 1.", "practice1", "onclass", "NB1", 1, "v10-be-van-dan-2025-I1-md2 (ý c)", "", "trac_nghiem",
     r"Biểu đồ dưới đây cho biết thông tin về số học sinh trung bình trong một lớp học của cả nước trong $5$ năm học."
     + ng("bvd2")
     + C(NAM, [33.5, 34.5, 35, 35.9, 36.6], "Năm học", "Số học sinh", 40, 10, tieu_de="Số học sinh trung bình trong một lớp",
         bw=1.0, gap=0.5, nhan_rong=1.3)
     + r"[NB] Năm học $2016$ -- $2017$, số học sinh trung bình trong một lớp ở nước ta là",
     "Kiến thức cũ (đọc biểu đồ cột, Toán 8), MỘT bước: cột năm học 2016–2017 ghi 34,5. Chọn B. Lời giải 1 dòng."),
    ("Ví dụ 2.", "practice1", "", "", 0, "sgk-b22-hd2", "", "vi_du",
     r"Cho hai biểu đồ sau." + sgk("Bài 22, HĐ2")
     + P(C([6, 7, 8, 9, 10], [3, 8, 12, 6, 4], "Điểm", "Tần số", 15, 5, tieu_de="Biểu đồ A. Kết quả kiểm tra môn Toán",
           bw=0.7, gap=0.5),
         D([6, 7, 8, 9, 10], [3, 8, 12, 6, 4], "Điểm", "Số học sinh", 15, 5, tieu_de="Biểu đồ B. Kết quả kiểm tra môn Toán",
           step=1.1, nhan_rong=0.8))
     + y(r"a) Đọc và giải thích mỗi biểu đồ trên.",
         r"b) Hai biểu đồ trên có biểu diễn cùng một dữ liệu không? Lập bảng thống kê cho dữ liệu đó. Bảng thống kê thu "
         r"được có phải là bảng tần số hay không?"),
     "a) Biểu đồ A (cột): cột ở điểm 6 cao 3 nghĩa là có 3 học sinh được điểm 6 … điểm 10 có 4 học sinh. Biểu đồ B "
     "(đoạn thẳng): điểm (8; 12) nghĩa là có 12 học sinh được điểm 8. b) Hai biểu đồ cùng biểu diễn một dữ liệu (cùng "
     "các số 3, 8, 12, 6, 4). Bảng: Điểm | 6 | 7 | 8 | 9 | 10 / Số học sinh | 3 | 8 | 12 | 6 | 4 (tabular, ô fill ở dòng "
     "dưới). Bảng cho biết số lần xuất hiện của mỗi giá trị điểm nên là bảng tần số. Cỡ mẫu 3+8+12+6+4=33. 6–8 ô."),
    # 18/11 đổi chỗ 7.4 (đoạn thẳng) lên Bài 2, 7.2 (tranh, kiểm bảng) xuống Bài 3 sau Ví dụ 2 — cho hộp Ví dụ 2 lọt trang 5
    ("Bài 2.", "practice1", "onclass", "NB2", 1, "sgk-7.4", "", "dung_sai",
     r"Người ta thống kê các loại ô tô chạy qua một trạm thu phí trong $1$ giờ và vẽ được biểu đồ tần số như sau."
     + sgk("Bài tập 7.4")
     + D(["Xe 4 chỗ", "Xe 7 chỗ", "Xe 9 chỗ", "Xe 16 chỗ trở lên"], [9, 14, 5, 3], "Loại xe", "Số xe", 15, 5,
         tieu_de="Số lượng các loại ô tô", step=1.5, nhan_rong=1.4)
     + y(DS, r"a) [NB] Trong $1$ giờ có tất cả $31$ ô tô chạy qua trạm thu phí.",
         r"b) [NB] Xe $4$ chỗ là loại xe đi qua trạm thu phí nhiều nhất."),
     "18/11 đổi Đúng/Sai. a) Đúng: 9+14+5+3=31. b) Sai: xe 7 chỗ có tần số lớn nhất (14). Mỗi ý một dòng \"a) Đúng. …\"."),
    ("Bài 3.", "practice1", "onclass", "NB2", 1, "sgk-7.2", "", "dung_sai",
     r"Cho biểu đồ tranh biểu diễn số lượng học sinh trong lớp đăng kí tham gia các câu lạc bộ của trường như sau."
     + sgk("Bài tập 7.2")
     + T(["Câu lạc bộ võ thuật", "Câu lạc bộ tiếng Anh", "Câu lạc bộ nghệ thuật"], [6, 9, 5],
         r"(Mỗi \tikz[baseline=-0.5ex]{\fill[stage2] (0,0.06) circle (0.05);\fill[stage2] (-0.06,-0.14) rectangle (0.06,0.01);} "
         r"biểu diễn cho $1$ học sinh)")
     + r"[NB] Khẳng định sau đúng hay sai: \textquotedblleft Bảng dưới đây là bảng tần số của dữ liệu trong biểu đồ "
       r"tranh trên.\textquotedblright"
     + B(["Câu lạc bộ", "Võ thuật", "Tiếng Anh", "Nghệ thuật"], ["Tần số", 6, 9, 4]),
     "18/11 đổi Đúng/Sai (lập bảng → kiểm bảng). Đếm biểu tượng: Võ thuật 6, Tiếng Anh 9, Nghệ thuật 5 ⇒ SAI vì bảng "
     "ghi Nghệ thuật 4. Lời giải: \"Sai.\" + một dòng lí do + bảng đúng [[bang: …]] + dòng Vậy."),
    ("Mạch 2. Tần số, tần số tương đối của một giá trị, một nhóm", "practice1", "heading"),
    ("Ví dụ 3.", "practice1", "", "", 0, "sgk-7.22 + so-hn-2025-I1", "", "vi_du",
     y(r"a) Gieo một con xúc xắc $50$ lần cho kết quả như sau." + sgk("Bài tập 7.22")
       + B(["Số chấm xuất hiện", 1, 2, 3, 4, 5, 6], ["Tần số", 8, 7, "?", 8, 6, 11])
       + r"Tần số xuất hiện của mặt $3$ chấm là" + tn("$9$", "$10$", "$11$", "$12$"),
       r"b) Kết quả khảo sát $300$ học sinh lớp 9 về thời gian tự học của mỗi bạn trong một tuần (đơn vị: giờ) được "
       r"cho trong bảng tần số ghép nhóm sau đây." + ng("hn25"))
     + B(["Thời gian tự học (giờ)", "$[0; 4)$", "$[4; 8)$", "$[8; 12)$", "$[12; 16)$", "$[16; 20)$"],
         ["Số học sinh", 17, 72, 94, 75, 42])
     + r"Xác định tần số và tần số tương đối của nhóm $[12; 16)$.",
     "a) Tổng các tần số bằng cỡ mẫu 50 nên tần số mặt 3 chấm là 50−(8+7+8+6+11)=50−40=10. Chọn B. b) Tần số của "
     "nhóm [12; 16) là 75 (đọc ở bảng) · cỡ mẫu n=300 · tần số tương đối f=75/300·100%=25% (viết công thức "
     "f=\\dfrac{m}{n}\\cdot 100\\% trước rồi thay số, phân số \\dfrac đứng riêng một dòng) · Vậy tần số là 75, tần số tương đối "
     "là 25%. 6–8 ô."),
    ("Bài 4.", "practice1", "onclass", "NB3", 1, "so-hn-2026-I1", "", "tra_loi_ngan",
     r"Kết quả đo chiều cao của $50$ học sinh lớp 6 (đơn vị: cm) được thống kê trong bảng tần số ghép nhóm sau đây."
     + ng("hn26")
     + B(["Chiều cao (cm)", "$[140; 145)$", "$[145; 150)$", "$[150; 155)$", "$[155; 160)$", "$[160; 165)$"],
         ["Số học sinh", 10, 18, 14, 6, 2])
     + y(r"a) [NB] Tần số của nhóm $[150; 155)$ là bao nhiêu?",
         r"b) [NB] Tần số tương đối của nhóm $[150; 155)$ là" + tn(r"$14\%$", r"$20\%$", r"$28\%$", r"$0{,}28\%$")),
     "a) 14 (một dòng). b) f=14/50·100%=28%. Chọn C (một dòng)."),
    ("Bài 5.", "practice1", "onclass", "NB3", 1, "so-hn-minhhoa-I1", "", "tra_loi_ngan",
     r"Sau khi điều tra số học sinh trong $40$ lớp học (đơn vị: học sinh), người ta có biểu đồ tần số ghép nhóm dưới đây."
     + ng("hnmh")
     + C([34, 36, 38, 40, 42], [15, 10, 10, 5], "Số học sinh", "Tần số ($n$)", 20, 5, sat=True)
     + y(r"a) [NB] Tần số ghép nhóm của nhóm $[40; 42)$ là bao nhiêu?",
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[40; 42)$ là"
         + tn(r"$5\%$", r"$12{,}5\%$", r"$25\%$", r"$0{,}125\%$")),
     "a) 5. b) 5/40·100%=12,5%. Chọn B."),
    ("Bài 6.", "practice1", "onclass", "NB3", 1, "ck2-gia-lam-2024-I1", "", "tra_loi_ngan",
     r"Một nhà may thống kê chiều cao (đơn vị: centimét) của $40$ học sinh của một lớp 9 để may đồng phục. Sau khi ghép "
     r"nhóm mẫu số liệu thu được, nhà may nhận được bảng tần số ghép nhóm như sau." + ng("gl")
     + B(["Nhóm", "$[150; 155)$", "$[155; 160)$", "$[160; 165)$", "$[165; 170)$", "$[170; 175)$", "Cộng"],
         ["Tần số", 5, 8, 10, 12, 5, "$N=40$"])
     + y(r"a) [NB] Tần số ghép nhóm của nhóm $[160; 165)$ và của nhóm $[165; 170)$ lần lượt là bao nhiêu?",
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[160; 165)$ là"
         + tn(r"$25\%$", r"$10\%$", r"$30\%$", r"$0{,}25\%$")),
     "a) 10 và 12. b) 10/40·100%=25%. Chọn A."),
    ("Bài 7.", "practice1", "onclass", "NB3", 1, "v10-tu-lap-2026-I1", "", "tra_loi_ngan",
     r"Kết quả khảo sát độ tuổi của $500$ đồng chí tham gia Lễ diễu binh, diễu hành Kỷ niệm $80$ năm Quốc khánh $2/9$ "
     r"được cho trong bảng tần số ghép nhóm sau đây." + ng("tl")
     + B(["Tuổi", "$[18; 20)$", "$[20; 22)$", "$[22; 24)$", "$[24; 26)$", "$[26; 28)$", "$[28; 30)$"],
         ["Số đồng chí", 114, 86, 97, 61, 73, 69])
     + y(r"a) [NB] Tần số của nhóm $[20; 22)$ là bao nhiêu?",
         r"b) [NB] Tần số tương đối của nhóm $[20; 22)$ là"
         + tn(r"$86\%$", r"$22{,}8\%$", r"$0{,}172\%$", r"$17{,}2\%$")),
     "a) 86. b) 86/500·100%=17,2%. Chọn D."),
    ("Bài 8.", "practice1", "onclass", "NB2", 1, "gk2-le-ngoc-han-2025-I", "", "tra_loi_ngan",
     r"Thống kê tuổi thọ của $30$ bóng đèn điện được lắp thử (đơn vị: giờ) được cho trong bảng dưới đây." + ng("lnh25")
     + L(DEN, 10)
     + y(r"a) [NB] Lập bảng tần số của dữ liệu trên.",
         r"b) [NB] Tần số tương đối của các bóng đèn có tuổi thọ cao nhất là"
         + tn(r"$3\%$", r"$40\%$", r"$10\%$", r"$0{,}1\%$")),
     "a) GIỮ tự luận lập bảng: Tuổi thọ (giờ) | 1150 | 1160 | 1170 | 1180 | 1190 / Tần số | 3 | 6 | 12 | 6 | 3. "
     "b) 1190 giờ có tần số 3 ⇒ 3/30·100%=10%. Chọn C."),
    ("Bài 9.", "practice1", "onclass", "NB2", 1, "ck2-xuan-dinh-2025-I", "", "dung_sai",
     r"Số lượt mượn các loại sách trong một tuần tại thư viện một trường THCS được biểu diễn bằng biểu đồ dưới đây."
     + ng("xd")
     + C(["Sách giáo khoa", "Truyện ngắn", "Sách tham khảo", "Tiểu thuyết"], [15, 20, 35, 30], "Loại sách", "Tần số",
         40, 10, tieu_de="Số lượt mượn các loại sách trong một tuần", bw=0.9, gap=0.7)
     + y(DS, r"a) [NB] Tổng số lượt mượn sách trong tuần là $100$.",
         r"b) [NB] Tần số tương đối của số lượt mượn sách tham khảo là $30\%$."),
     "18/11 đổi Đúng/Sai. a) Đúng: 15+20+35+30=100. b) Sai: 35/100·100%=35% (30% là của tiểu thuyết)."),
    ("Bài 10.", "practice1", "onclass", "NB2", 1, "ck2-hat-mon-2025-I1", "", "tra_loi_ngan",
     r"Điểm bài kiểm tra môn toán học kì I của $32$ học sinh lớp 9 được ghi trong bảng sau." + ng("hm")
     + L(HM, 16)
     + y(r"a) [NB] Lập bảng tần số.",
         r"b) [NB] Tìm tần số tương đối của điểm $8$, điểm $9$ (làm tròn kết quả đến chữ số thập phân thứ hai)."),
     "a) Bảng: Điểm | 2 | 4 | 5 | 6 | 7 | 8 | 9 | 10 / Tần số | 2 | 5 | 4 | 7 | 6 | 5 | 2 | 1 (tổng 32). "
     "b) f(8)=5/32·100%=15,625%≈15,63% · f(9)=2/32·100%=6,25%. Dòng Vậy."),
    ("Bài 11.", "practice1", "onclass", "NB5", 1, "ck2-chu-van-an-2024-I1", "", "trac_nghiem",
     r"Cho bảng thống kê điểm kiểm tra khảo sát môn Toán của một lớp gồm $50$ học sinh như sau." + ng("cva")
     + B(["Điểm", 4, 5, 6, 7, 8, 9, "Cộng"], ["Số học sinh", 1, 3, 5, 14, 17, 10, "$N=50$"])
     + r"Mẫu số liệu trên được ghép nhóm thành ba nhóm sau: $[4; 6)$, $[6; 8)$, $[8; 10)$."
     + BR + y(r"a) [NB] Tần số của nhóm $[4; 6)$ là" + tn("$9$", "$4$", "$3$", "$1$"),
              r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[4; 6)$ là"
              + tn(r"$4\%$", r"$18\%$", r"$0{,}08\%$", r"$8\%$")),
     "a) Nhóm [4; 6) gồm điểm 4 và 5 (không lấy điểm 6) ⇒ 1+3=4. Chọn B (phương án 9 là lỗi lấy cả điểm 6). "
     "b) 4/50·100%=8%. Chọn D."),
    ("Mạch 3. Đọc bảng ghép nhóm, giá trị đại diện", "practice1", "heading"),
    ("Ví dụ 4.", "practice1", "", "", 0, "sgk-7.25", "", "vi_du",
     r"Cho bảng tần số tương đối ghép nhóm về thời gian đi từ nhà đến trường của học sinh lớp 9A như sau."
     + sgk("Bài tập 7.25")
     + B(["Thời gian đến trường (phút)", "$[0; 10)$", "$[10; 20)$", "$[20; 30)$"],
         ["Tần số tương đối", r"$20\%$", r"$55\%$", r"$25\%$"])
     + r"Để vẽ biểu đồ tần số tương đối ghép nhóm dạng đoạn thẳng, ta dùng giá trị nào đại diện cho nhóm số liệu "
       r"$[10; 20)$?" + tn("$10$", "$15$", "$20$", "$30$"),
     "Giá trị đại diện của nhóm [a; b) là trung điểm (a+b)/2 (viết công thức trước) · nhóm [10; 20) có giá trị "
     "đại diện (10+20)/2=15 · Chọn B. Thêm một dòng đọc bảng: nhóm [10; 20) có tần số tương đối 55% nghĩa là 55% "
     "số học sinh lớp 9A đi đến trường hết từ 10 phút đến dưới 20 phút. 4–5 ô."),
    ("Bài 12.", "practice1", "onclass", "NB4", 1, "sgk-b24-lt1 (ý a)", "", "trac_nghiem",
     r"Cho bảng tần số ghép nhóm về tuổi thọ của một số ong mật cái như sau." + sgk("Bài 24, Luyện tập 1")
     + B(["Tuổi thọ (ngày)", "$[30; 40)$", "$[40; 50)$", "$[50; 60)$"], ["Tần số", 12, 23, 15])
     + r"[NB] Số $23$ trong bảng cho biết",
     "18/11 đổi trắc nghiệm (đọc, giải thích bảng). Đúng: có 23 con ong sống từ 40 ngày đến dưới 50 ngày. Chọn C "
     "(B là lỗi lấy cả đầu mút 50). Lời giải 1 dòng."),
    ("Mạch 4. Lập bảng tần số tương đối", "practice2", "heading"),
    ("Ví dụ 5.", "practice2", "", "", 0, "sgk-b23-vd1 (ý a)", "", "vi_du",
     y(r"Thu thập dữ liệu về chất lượng không khí tại một địa điểm trong $30$ ngày mùa xuân cho kết quả như sau:",
       r"\hspace*{1.4em}" + ", ".join(KK) + ".",
       r"(M1: Tốt; M2: Trung bình; M3: Kém; M4: Xấu). Lập bảng tần số tương đối cho dãy dữ liệu trên."
       + sgk("Bài 23, Ví dụ 1")),
     "Tách 18/11 từ ví dụ gộp (hộp ví dụ không ngắt trang). Đếm: M1 9, M2 12, M3 6, M4 3 · 30%, 40%, 20%, 10%."),
    ("Bài 13.", "practice2", "onclass", "NB6+TH1", 2, "v10-ha-dong-2025-I1", "", "th_dan",
     r"Kết quả khảo sát chất lượng môn Toán một lớp 9 của trường THCS A như sau." + ng("hd")
     + B(["Điểm ($x$)", 5, 6, 7, 8, 9, 10], ["Tần số ($n$)", 4, 6, 12, 8, 8, 2])
     + y(r"a) [NB] Tính cỡ mẫu.", r"b) [TH] Lập bảng tần số tương đối của mẫu số liệu thống kê đó."),
     "a) n=4+6+12+8+8+2=40. b) Theo câu a): f(5)=4/40=10%, f(6)=15%, f(7)=30%, f(8)=20%, f(9)=20%, f(10)=5% · bảng "
     "tabular · Vậy … ."),
    ("Ví dụ 6.", "practice2", "", "", 0, "sgk-7.19", "", "vi_du",
     r"Giáo viên ghi lại thời gian chạy cự li $100$ mét của các học sinh lớp 9A cho kết quả như sau." + sgk("Bài tập 7.19")
     + B(["Thời gian (giây)", "$[13; 15)$", "$[15; 17)$", "$[17; 19)$", "$[19; 21)$"], ["Số học sinh", 5, 20, 13, 2])
     + r"Nêu các nhóm số liệu và tần số tương ứng, rồi lập bảng tần số tương đối ghép nhóm.",
     "Tách 18/11 từ ví dụ gộp. Cỡ mẫu 40 · 12,5%, 50%, 32,5%, 5%."),
    ("Bài 14.", "practice2", "onclass", "NB6+TH1", 2, "v10-khuong-thuong-2025-I1", "", "th_dan",
     r"Sau khi điều tra về thời gian của một nhóm học sinh làm bài kiểm tra trắc nghiệm, kết quả được ghi lại trong bảng "
     r"sau." + ng("kt")
     + B(["Thời gian (phút)", "$[0; 5)$", "$[5; 10)$", "$[10; 15)$", "$[15; 20)$"], ["Tần số", 1, 5, 9, 5])
     + y(r"a) [NB] Hỏi có bao nhiêu học sinh tham gia điều tra?",
         r"b) [TH] Lập bảng tần số tương đối ghép nhóm cho bảng dữ liệu trên."),
     "a) 1+5+9+5=20 học sinh. b) Theo câu a) cỡ mẫu n=20 · f: 1/20=5%, 5/20=25%, 9/20=45%, 5/20=25% (mỗi nhóm một "
     "dòng hoặc gộp một dòng) · bảng tabular (Thời gian (phút) | [0; 5) | … / Tần số tương đối | 5% | 25% | 45% | 25%) "
     "· Vậy … ."),
    ("Mạch 5. Đếm theo điều kiện, tính tỉ lệ phần trăm", "practice2", "heading"),
    ("Ví dụ 7.", "practice2", "", "", 0, "v10-tho-loc-l2-2025-I1 (ý a)", "", "vi_du",
     r"Tại một trại hè thanh thiếu niên quốc tế, người ta tìm hiểu xem mỗi đại biểu tham dự có thể sử dụng được bao nhiêu "
     r"ngoại ngữ. Kết quả được như bảng sau." + ng("tll2")
     + B(["Số ngoại ngữ", 1, 2, 3, 4, r"$\ge 5$"], ["Số đại biểu", 84, 64, 24, 16, 12])
     + r"Tính tỉ lệ phần trăm đại biểu sử dụng được ít nhất $2$ ngoại ngữ.",
     "Tổng số đại biểu 84+64+24+16+12=200 · \"ít nhất 2 ngoại ngữ\" gồm các cột 2, 3, 4, ≥5 (không lấy cột 1) · số đại "
     "biểu: 64+24+16+12=116 · tỉ lệ 116/200·100%=58% · Vậy 58%. 6–8 ô."),
    ("Bài 15.", "practice2", "onclass", "NB9+TH3", 2, "v10-thai-thinh-2026-I1", "", "th_dan",
     r"Cho biểu đồ về điểm số môn Tiếng Anh thi học kì I của lớp 9A1 tại một trường THCS." + ng("tt26")
     + C([6, 7, 8, 9, 10], [8, 11, 10, 7, 4], "Điểm", "Số học sinh", 12, 4,
         tieu_de="Kết quả kiểm tra học kì I môn Tiếng Anh lớp 9A1", bw=0.8, gap=0.6)
     + y(r"a) [NB] Lập bảng thống kê về điểm số môn Tiếng Anh theo bảng sau."
         + B(["Điểm", 6, 7, 8, 9, 10], ["Số học sinh", "?", "?", "?", "?", "?"]),
         r"b) [TH] Số học sinh đạt từ điểm $8$ trở lên chiếm bao nhiêu phần trăm của cả lớp?"),
     "a) 8, 11, 10, 7, 4. b) Theo câu a): cả lớp 8+11+10+7+4=40 học sinh · từ điểm 8 trở lên gồm điểm 8, 9, 10: "
     "10+7+4=21 học sinh · 21/40·100%=52,5% · Vậy 52,5%. (Đề gốc viết \"đạt từ điểm 8\" — sơ đồ đã viết rõ \"từ điểm 8 "
     "trở lên\".)"),
    ("Bài 16.", "practice2", "onclass", "NB9+TH3", 2, "ck2-cau-giay-2024-I", "", "th_dan",
     r"Một trường THCS khảo sát thời gian tiếp xúc với các thiết bị điện tử (điện thoại thông minh, máy tính bảng, máy "
     r"tính, ti vi) trung bình trong một ngày của $150$ học sinh và biểu diễn kết quả thu được trong biểu đồ sau." + ng("cg")
     + C(["$0{,}5$", "$1$", "$2$", "$3$", "$4$"], [15, 36, 48, 39, 12], "Thời gian (giờ)", "Số học sinh", 50, 10,
         tieu_de="Thời gian tiếp xúc với các thiết bị điện tử trung bình trong một ngày", bw=0.8, gap=0.6)
     + y(r"a) [NB] Lập bảng tần số cho dữ liệu được biểu diễn trên biểu đồ.",
         r"b) [TH] Các chuyên gia khuyến nghị thời gian trẻ em tiếp xúc các thiết bị điện tử an toàn là ít hơn $2$ giờ mỗi "
         r"ngày. Trong $150$ học sinh tham gia khảo sát, có bao nhiêu phần trăm học sinh đã thực hiện đúng khuyến cáo "
         r"trên?"),
     "a) Bảng: Thời gian (giờ) | 0,5 | 1 | 2 | 3 | 4 / Tần số | 15 | 36 | 48 | 39 | 12. b) Theo câu a): \"ít hơn 2 giờ\" "
     "gồm 0,5 giờ và 1 giờ (không lấy 2 giờ) · 15+36=51 học sinh · 51/150·100%=34% · Vậy 34%."),
    ("Bài 17.", "practice2", "onclass", "NB9+TH3", 2, "v10-tho-loc-l5-2025-I1", "", "th_dan",
     r"Mẫu số liệu dưới đây ghi lại số người trong mỗi hộ gia đình (đơn vị: người) của $20$ hộ gia đình trong một cụm "
     r"dân cư của xã Tích Lộc." + ng("tll5")
     + L(HO, 10)
     + y(r"a) [NB] Tìm tần số của nhóm $[2; 4)$.",
         r"b) [TH] Số hộ gia đình có ít hơn $4$ người bằng bao nhiêu phần trăm so với tổng số hộ gia đình trong mẫu số "
         r"liệu trên?"),
     "a) Nhóm [2; 4) gồm hộ 2 người (2 hộ) và hộ 3 người (3 hộ) ⇒ tần số 5. b) Theo câu a): hộ có ít hơn 4 người "
     "chính là nhóm [2; 4), có 5 hộ · 5/20·100%=25% · Vậy 25%."),
    ("Mạch 6. Tính số lượng từ tần số tương đối", "practice2", "heading"),
    ("Ví dụ 8.", "practice2", "", "", 0, "v10-lang-thuong-2025-II1", "", "vi_du",
     r"Biểu đồ bên biểu diễn tỉ lệ đại biểu tham dự hội nghị theo độ tuổi. Biết rằng có $160$ đại biểu." + ng("lt")
     + C([25, 35, 45, 55, 65], [33.75, 28.75, 26.25, 11.25], "Độ tuổi", r"Tần số tương đối (\%)", 40, 10, sat=True,
         tren=[r"$33{,}75\%$", r"$28{,}75\%$", r"$26{,}25\%$", r"$11{,}25\%$"], tieu_de="Tỉ lệ đại biểu theo độ tuổi",
         bw=1.1)
     + r"Tìm tần số tương đối ghép nhóm và tần số ghép nhóm của nhóm $[25; 35)$.",
     "Đọc biểu đồ: tần số tương đối của nhóm [25; 35) là 33,75% · từ f=m/n·100% ta có m=n·f (viết công thức) · "
     "m=160·33,75%=160·0,3375=54 · Vậy tần số tương đối 33,75%, tần số 54. 5–7 ô."),
    ("Bài 18.", "practice2", "onclass", "NB8+TH2", 2, "ck2-lomonoxop-2024-I1", "", "th_dan",
     r"Sau khi khảo sát về số học sinh trong một lớp học của $200$ lớp (đơn vị: học sinh), người ta có biểu đồ tần số "
     r"tương đối ghép nhóm như hình bên." + ng("lmns")
     + C([25, 30, 35, 40, 45, 50], [15, 25, 40, 15, 5], "Số học sinh", r"Tần số tương đối (\%)", 40, 10, sat=True,
         tren=[r"$15\%$", r"$25\%$", r"$40\%$", r"$15\%$", r"$5\%$"])
     + y(r"a) [NB] Tìm tần số tương đối ghép nhóm của nhóm $[35; 40)$.",
         r"b) [TH] Trong $200$ lớp được khảo sát, có bao nhiêu lớp mà mỗi lớp có từ $35$ đến dưới $40$ học sinh?"),
     "a) 40%. b) Theo câu a): lớp có từ 35 đến dưới 40 học sinh là nhóm [35; 40), f=40% · số lớp 200·40%=80 · "
     "Vậy 80 lớp."),
    ("Ví dụ 9.", "practice2", "", "", 0, "v10-thai-thinh-2025-I1", "", "vi_du",
     r"Biểu đồ dưới đây cho biết số lượng các loại ô tô một cửa hàng bán được trong năm $2023$." + ng("tt25")
     + C(["Xe 4 chỗ ngồi", "Xe 7 chỗ ngồi", "Xe 16 chỗ ngồi", "Xe trên 16 chỗ ngồi"], [35, 20, 15, 10], "Loại xe",
         "Tần số", 40, 10, tieu_de="Số lượng xe các loại bán được năm 2023", bw=0.9, gap=0.7)
     + y(r"a) Lập bảng tần số và bảng tần số tương đối cho dữ liệu được biểu diễn trên biểu đồ.",
         r"b) Giả sử tỉ lệ các loại xe bán được không đổi và cửa hàng bán được tổng số $240$ ô tô các loại trong năm "
         r"$2024$. Hãy ước lượng số ô tô $4$ chỗ cửa hàng bán được."),
     "a) Tần số 35, 20, 15, 10 · cỡ mẫu 80 · f: 43,75%, 25%, 18,75%, 12,5% (bảng tabular gộp hai dòng tần số và "
     "tần số tương đối). b) Theo câu a), xe 4 chỗ chiếm 43,75% · 240·43,75%=105 · Vậy khoảng 105 xe 4 chỗ. 7–9 ô."),
    ("Bài 19.", "practice2", "onclass", "NB8+TH2", 2, "v10-chuong-my-l2-2025-I1", "", "th_dan",
     r"Biểu đồ hình quạt tròn cho biết tỉ lệ mỗi loại điểm kiểm tra môn Tiếng Anh của $200$ học sinh tại một trung tâm "
     r"anh ngữ (hình vẽ bên)." + ng("cm2")
     + Q([10, 30, 20, 40], ["Điểm 6", "Điểm 7", "Điểm 8", "Điểm 9"], tieu_de="Điểm kiểm tra môn Tiếng Anh")
     + y(r"a) [NB] Lập bảng thống kê tỉ lệ phần trăm mỗi loại điểm học sinh đạt được.",
         r"b) [TH] Tính tổng số học sinh đạt điểm $8$ và điểm $9$."),
     "a) Bảng: Điểm | 6 | 7 | 8 | 9 / Tỉ lệ | 10% | 30% | 20% | 40%. b) Theo câu a): điểm 8 và điểm 9 chiếm "
     "20%+40%=60% · 200·60%=120 học sinh (hoặc tính riêng 40 + 80) · Vậy 120 học sinh."),
    ("Mạch 7. Ghép nhóm số liệu", "practice2", "heading"),
    ("Ví dụ 10.", "practice2", "", "", 0, "sgk-b24-vd1", "", "vi_du",
     r"Đo chiều cao (đơn vị là cm) của học sinh lớp 9C cho kết quả như sau." + sgk("Bài 24, Ví dụ 1")
     + L(CAO_SGK, 10)
     + r"Lập bảng tần số ghép nhóm và bảng tần số tương đối ghép nhóm cho mẫu số liệu này với các nhóm $[150; 158)$, "
       r"$[158; 161)$, $[161; 164)$, $[164; 167)$.",
     "SGK tr.47 in nhóm đầu [155; 158) nhưng dãy có 154 và lời giải SGK dùng [150; 158) — phiếu đã in [150; 158), KHÔNG "
     "nhắc chuyện này trong lời giải. Đếm từng nhóm (đầu mút phải không lấy: 158 sang nhóm [158; 161), 161 sang "
     "[161; 164), 164 sang [164; 167)): [150;158) có 5, [158;161) có 12, [161;164) có 15, [164;167) có 8 · cỡ mẫu 40 · "
     "f: 12,5%, 30%, 37,5%, 20% · một bảng tabular hai dòng tần số + tần số tương đối. Dòng Vậy. 7–9 ô."),
    ("Bài 20.", "practice2", "onclass", "NB7+TH4", 2, "v10-cat-linh-2025-I1", "", "th_dan",
     r"Sau khi điều tra về chiều cao của $50$ học sinh (đơn vị: cm), người ta thống kê trong bảng dưới đây." + ng("cl")
     + L(CAO_CL, 10)
     + y(r"a) [TH] Lập bảng tần số ghép nhóm theo mẫu sau."
         + B(["Nhóm", "$[140; 150)$", "$[150; 160)$", "$[160; 170)$", "$[170; 180)$", "Cộng"],
             ["Tần số ($n$)", "?", "?", "?", "?", "?"]),
         r"b) [NB] Tính tần số tương đối ghép nhóm của nhóm $[150; 160)$."),
     "a) Đếm: [140;150) có 6, [150;160) có 15, [160;170) có 19, [170;180) có 10, cộng 50 (nhắc 150 thuộc [150;160), "
     "160 thuộc [160;170), 170 thuộc [170;180)) · bảng tabular. b) Theo câu a): f=15/50·100%=30%. Dòng Vậy."),
    ("Bài 21.", "practice2", "onclass", "TH4", 2, "v10-thanh-oai-l2-2025-I1", "", "th_dan",
     r"Công ty điện lực Thanh Oai thống kê lượng điện tiêu thụ (đơn vị: kWh) của một số hộ gia đình trong tháng $3$ năm "
     r"$2025$. Dữ liệu được ghi lại như sau." + ng("to")
     + L(DIEN, 10)
     + r"[TH] Lập bảng tần số ghép nhóm lượng điện tiêu thụ theo các nhóm sau: $[100; 130)$, $[130; 160)$, "
       r"$[160; 190)$, $[190; 220)$. Nhóm lượng điện nào có nhiều gia đình tiêu thụ trong tháng $3$ nhất?",
     "Đếm (130 sang [130;160), 160 sang [160;190), 190 sang [190;220)): 3, 5, 5, 7 · bảng tabular · nhóm [190; 220) có "
     "tần số lớn nhất (7) · Vậy …"),
    ("Mạch 8. Kiểm tra một nhận định", "practice2", "heading"),
    ("Ví dụ 11.", "practice2", "", "", 0, "v10-cum-thcs-cong-lap-2026-I1", "", "vi_du",
     r"Một cửa hàng bán đồ chơi cho trẻ em thống kê số tiền (đơn vị: nghìn đồng) mà $60$ khách hàng mua đồ ở cửa hàng đó "
     r"trong một ngày. Số liệu được ghi lại trong biểu đồ tần số ghép nhóm sau." + ng("cum")
     + C([40, 50, 60, 70, 80, 90], [3, 6, 19, 23, 9], "Số tiền (nghìn đồng)", "Tần số ($n$)", 25, 5, sat=True)
     + y(r"a) Tính tần số tương đối ghép nhóm của nhóm $[80; 90)$.",
         r"b) Chủ của cửa hàng nhận xét: \textquotedblleft Có không ít hơn $70\%$ số người mua hàng với số tiền từ $60$ "
         r"nghìn đồng đến dưới $80$ nghìn đồng\textquotedblright. Nhận định đó đúng hay sai?"),
     "a) f=9/60·100%=15%. b) Từ 60 đến dưới 80 nghìn đồng gồm hai nhóm [60;70) và [70;80): 19+23=42 người · "
     "42/60·100%=70% · \"không ít hơn 70%\" nghĩa là ≥70%, mà 70%≥70% · Vậy nhận định đúng. 6–8 ô."),
    ("Bài 22.", "practice2", "onclass", "TH5", 2, "gk2-duc-giang-2025-I1", "", "th_dan",
     r"Khảo sát về chiều cao của $40$ học sinh được bảng tần số ghép nhóm sau." + ng("dg")
     + B(["Nhóm chiều cao (cm)", "$[140; 148)$", "$[148; 156)$", "$[156; 164)$", "$[164; 172)$"],
         ["Số học sinh", 5, 15, 12, 8])
     + y(r"a) [TH] Tính tần số tương đối ghép nhóm của các nhóm trên.",
         r"b) [TH] Bạn Hà nói có $30\%$ học sinh trên có chiều cao từ $156$ cm trở lên. Bạn Hà nói đúng không? Tại sao?"),
     "a) 5/40=12,5%, 15/40=37,5%, 12/40=30%, 8/40=20% (bảng hoặc liệt kê từng dòng). b) Theo câu a): từ 156 cm trở lên "
     "gồm [156;164) và [164;172) · 30%+20%=50% · 50%≠30% · Vậy bạn Hà nói sai (bạn chỉ tính nhóm [156; 164))."),
    ("Bài 23.", "practice2", "onclass", "NB9+TH3", 2, "gk2-nam-tu-liem-2025-I1 — ĐÍCH", "", "th_dan",
     r"Một đội công nhân tham gia hội thi tay nghề giỏi. Mỗi công nhân phải hoàn thành bài thi (lí thuyết và thực hành) "
     r"trong thời gian $120$ phút. Biểu đồ tần số ghép nhóm dưới đây biểu diễn thời gian hoàn thành bài thi của các công "
     r"nhân trong đội." + ng("ntl")
     + C([90, 95, 100, 105, 110, 115, 120], [3, 5, 6, 7, 9, 10], "Thời gian (phút)", "Tần số ($n$)", 12, 2, sat=True,
         bw=0.85)
     + y(r"a) [NB] Lập bảng tần số ghép nhóm theo mẫu sau."
         + B(["Nhóm", "$[90; 95)$", "$[95; 100)$", "$[100; 105)$", "$[105; 110)$", "$[110; 115)$", "$[115; 120)$",
              "Tổng"], ["Tần số ($n$)", "?", "?", "?", "?", "?", "?", "$N=\\,?$"]),
         r"b) [NB] Xác định tần số tương đối của nhóm $[105; 110)$.",
         r"c) [NB] Nhóm công nhân hoàn thành bài thi muộn nhất chiếm bao nhiêu phần trăm?",
         r"d) [TH] Tính số công nhân đã hoàn thành bài thi trước khi hết giờ trên $20$ phút."),
     "a) 3, 5, 6, 7, 9, 10, N=40. b) 7/40·100%=17,5%. c) Nhóm muộn nhất [115; 120): 10/40·100%=25%. d) Theo câu a): "
     "hết giờ ở phút 120, xong trước khi hết giờ trên 20 phút nghĩa là thời gian dưới 120−20=100 phút · gồm nhóm "
     "[90;95) và [95;100) · 3+5=8 công nhân · Vậy 8 công nhân."),
    # ───────────── BTVN — NB rồi TH (26 NB + 10 TH) ─────────────
    ("Bài 24.", "reflection", "btvn", "NB2", 1, "sgk-7.1", "", "tra_loi_ngan",
     y(r"Một nhóm học sinh đã khảo sát ý kiến về ý thức giữ gìn vệ sinh công cộng của các bạn trong trường với các mức "
       r"đánh giá Tốt, Khá, Trung bình, Kém và thu được kết quả như sau:" + sgk("Bài tập 7.1"),
       r"\hspace*{1.4em}" + ", ".join(VS) + ".",
       r"a) [NB] Lập bảng tần số cho dãy dữ liệu trên.",
       r"b) [NB] Từ bảng tần số, hãy cho biết mức đánh giá nào chiếm ưu thế nhất. Vì sao?"),
     "a) Tốt 13, Khá 11, Trung bình 5, Kém 2 (tổng 31). b) Tốt — tần số lớn nhất (13)."),
    ("Bài 25.", "reflection", "btvn", "NB2", 1, "ck2-nguyen-du-2025-III1", "", "tra_loi_ngan",
     r"Sau khi điều tra về chiều cao (đơn vị: cm) của toàn bộ các học sinh lớp 9A, người ta có được biểu đồ tần số ghép "
     r"nhóm dưới đây." + ng("nd")
     + C([140, 150, 160, 170, 180], [10, 15, 20, 5], "Chiều cao (cm)", "Tần số ($n$)", 20, 5, sat=True)
     + y(r"a) [NB] Lớp 9A có bao nhiêu học sinh?",
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[160; 170)$ là"
         + tn(r"$40\%$", r"$20\%$", r"$0{,}4\%$", r"$30\%$")),
     "a) 10+15+20+5=50. b) 20/50·100%=40%. Chọn A."),
    ("Bài 26.", "reflection", "btvn", "NB2", 1, "v10-tho-loc-l3-2026-I1", "", "tra_loi_ngan",
     r"Trong bài thơ \textquotedblleft Gọi mẹ\textquotedblright, nhà thơ Lưu Quang Vũ viết:[[br]]"
     r"\hspace*{1.4em}\textit{Mẹ ơi nếu con được sống lại tuổi thơ}[[br]]"
     r"\hspace*{1.4em}\textit{Con sẽ chẳng bao giờ mải chơi trốn học}[[br]]"
     r"\hspace*{1.4em}\textit{Đứa con trai nhiều lỗi lầm ương ngạnh}[[br]]"
     r"\hspace*{1.4em}\textit{Sẽ không lần nào làm mẹ xót xa.}[[br]]"
     r"Mẫu dữ liệu thống kê các chữ cái B, H, I, S xuất hiện trong đoạn thơ trên được mô tả ở bảng sau." + ng("tll3")
     + L(CHU, 11)
     + r"[NB] Lập bảng tần số của mẫu dữ liệu thống kê đã cho ở bảng trên.",
     "B 1, H 8, I 9, S 3 (tổng 21)."),
    ("Bài 27.", "reflection", "btvn", "NB2", 1, "v10-chuong-my-l4-2025-I1", "", "tra_loi_ngan",
     r"Trong đợt thi đua thu gom kế hoạch nhỏ do Liên đội phát động dịp Tết Ất Tỵ $2025$, số vỏ lon các lớp khối 9 của "
     r"một trường THCS thu gom được biểu diễn trên biểu đồ." + ng("cm4")
     + C(["9A", "9B", "9C", "9D"], [274, 280, 370, 516], "Lớp", "Số lượng (chiếc)", 600, 100,
         tieu_de="Số lượng thu gom vỏ lon", bw=0.8, gap=0.7)
     + y(r"a) [NB] Khẳng định sau đúng hay sai: \textquotedblleft Khối 9 thu gom được tất cả $1\,340$ vỏ "
         r"lon.\textquotedblright",
         r"b) [NB] Tỉ số phần trăm số vỏ lon của lớp 9B so với cả khối 9 (làm tròn đến chữ số thập phân thứ hai) là"
         + tn(r"$28\%$", r"$0{,}19\%$", r"$19{,}44\%$", r"$19{,}45\%$")),
     "a) Sai: 274+280+370+516=1440. b) 280/1440·100%=19,444…%≈19,44%. Chọn C."),
    ("Bài 28.", "reflection", "btvn", "NB3", 1, "v10-be-van-dan-2025-I1", "", "tra_loi_ngan",
     r"Sau khi điều tra số lần truy cập Internet của $40$ người trong vòng $1$ tuần (đơn vị: số lần truy cập), người ta "
     r"có biểu đồ tần số ghép nhóm dưới đây." + ng("bvd1")
     + C([30, 40, 50, 60, 70, 80], [4, 6, 8, 10, 12], "Số lần truy cập", "Tần số ($n$)", 14, 2, sat=True)
     + y(r"a) [NB] Tần số ghép nhóm của nhóm $[60; 70)$ là bao nhiêu?",
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[60; 70)$ là"
         + tn(r"$25\%$", r"$10\%$", r"$30\%$", r"$0{,}25\%$")),
     "a) 10. b) 10/40·100%=25%. Chọn A."),
    ("Bài 29.", "reflection", "btvn", "NB3", 1, "gk2-nguyen-binh-khiem-2024-I1", "", "tra_loi_ngan",
     r"Một cửa hàng tạp hóa thống kê số tiền lãi (đơn vị: nghìn đồng) trong $60$ ngày. Số liệu được ghi lại trong biểu đồ "
     r"tần số ghép nhóm sau." + ng("nbk")
     + C([500, 1000, 1500, 2000, 2500, 3000], [5, 8, 12, 20, 15], "Số tiền (nghìn đồng)", "Tần số ($n$)", 25, 5,
         sat=True, bw=1.0)
     + y(r"a) [NB] Tần số ghép nhóm của nhóm $[2500; 3000)$ là bao nhiêu?",
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[2500; 3000)$ là"
         + tn(r"$15\%$", r"$20\%$", r"$0{,}25\%$", r"$25\%$")),
     "a) 15. b) 15/60·100%=25%. Chọn D."),
    ("Bài 30.", "reflection", "btvn", "NB3", 1, "ck2-ngo-gia-tu-2025-d1-1", "", "trac_nghiem",
     r"Một xã thống kê khối lượng ngô (đơn vị: tạ) mà $60$ hộ gia đình trong xã thu hoạch được năm $2023$. Số liệu được "
     r"ghi lại trong biểu đồ tần số ghép nhóm sau." + ng("ngt")
     + C([20, 30, 40, 50, 60, 70, 80], [6, 9, 12, 18, 12, 3], "Khối lượng (tạ)", "Tần số ($n$)", 20, 5, sat=True)
     + y(r"a) [NB] Nhóm có nhiều hộ gia đình nhất là"
         + tn(r"$[40; 50)$", r"$[50; 60)$", r"$[60; 70)$", r"$[70; 80)$"),
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[60; 70)$ là"
         + tn(r"$12\%$", r"$30\%$", r"$20\%$", r"$0{,}2\%$")),
     "a) [50; 60) có tần số lớn nhất (18). Chọn B. b) 12/60·100%=20%. Chọn C."),
    ("Bài 31.", "reflection", "btvn", "NB3", 1, "ck2-van-dien-2024-I", "", "tra_loi_ngan",
     r"Một bác thợ đóng giày thống kê lại độ dài bàn chân (đơn vị: cm) của $40$ khách hàng ở bảng tần số ghép nhóm như "
     r"sau." + ng("vd")
     + B(["Độ dài (cm)", "$[27; 28)$", "$[28; 29)$", "$[29; 30)$", "$[30; 31)$", "$[31; 32)$"],
         ["Tần số", 2, 8, 20, "?", 4])
     + y(r"a) [NB] Tần số ghép nhóm của nhóm $[30; 31)$ (bác thợ chưa kịp thống kê) là bao nhiêu?",
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[30; 31)$ là"
         + tn(r"$6\%$", r"$15\%$", r"$20\%$", r"$0{,}15\%$")),
     "a) 40−(2+8+20+4)=6. b) 6/40·100%=15%. Chọn B."),
    ("Bài 32.", "reflection", "btvn", "NB3", 1, "ck2-ngoc-thuy-2024-I1", "", "tra_loi_ngan",
     r"Cho bảng tần số ghép nhóm sau về tuổi thọ của một số ong mật cái." + ng("nt")
     + B(["Tuổi thọ (ngày)", "$[30; 40)$", "$[40; 50)$", "$[50; 60)$"], ["Tần số", 14, 24, 22])
     + y(r"a) [NB] Tần số ghép nhóm của nhóm $[40; 50)$ là bao nhiêu?",
         r"b) [NB] Tần số tương đối ghép nhóm của nhóm $[40; 50)$ là"
         + tn(r"$24\%$", r"$23{,}33\%$", r"$0{,}4\%$", r"$40\%$")),
     "a) 24. b) cỡ mẫu 14+24+22=60, 24/60·100%=40%. Chọn D."),
    ("Bài 33.", "reflection", "btvn", "NB4", 1, "sgk-7.30 (ý a)", "", "trac_nghiem",
     r"Lương của các công nhân một nhà máy được cho trong bảng sau." + sgk("Bài tập 7.30")
     + B(["Lương (triệu đồng)", "$[5; 7)$", "$[7; 9)$", "$[9; 11)$", "$[11; 13)$", "$[13; 15)$"],
         ["Số công nhân", 20, 50, 70, 40, 20])
     + r"[NB] Số $70$ trong bảng cho biết"
     + tn(r"có $70$ công nhân có lương đúng $9$ triệu đồng",
          r"có $70$ công nhân có lương từ $9$ triệu đồng đến dưới $11$ triệu đồng",
          r"có $70$ công nhân có lương từ $9$ triệu đồng đến $11$ triệu đồng, kể cả $11$ triệu đồng",
          r"lương trung bình của công nhân là $70$ triệu đồng"),
     "18/11 đổi trắc nghiệm. Đúng: có 70 công nhân có lương từ 9 triệu đồng đến dưới 11 triệu đồng. Chọn B. 1 dòng."),
    ("Bài 34.", "reflection", "btvn", "NB5", 1, "v10-dong-da-2025-I1-md2 (ý b)", "", "trac_nghiem",
     r"Điều tra tốc độ của $44$ ô tô khi đi qua một trạm đo tốc độ, người ta có biểu đồ tần số ghép nhóm dưới đây."
     + ng("dd5")
     + C([40, 45, 50, 55, 60, 65, 70], [4, 14, 8, 10, 6, 2], "Tốc độ (km/h)", "Tần số ($n$)", 14, 2, sat=True)
     + r"[NB] Số xe ô tô đi với vận tốc thấp hơn $50$ km/h là" + tn("$4$", "$14$", "$18$", "$26$"),
     "Thấp hơn 50 km/h gồm nhóm [40;45) và [45;50): 4+14=18 xe. Chọn C (26 là lỗi lấy cả nhóm [50;55)). 1 dòng."),
    ("Bài 35.", "reflection", "btvn", "TH1", 2, "gk2-le-hong-phong-2025-21", "", "th_dan",
     r"Giáo viên ghi lại thời gian chạy cự li $100$ mét của $40$ học sinh lớp 9A và ghi lại kết quả bởi bảng tần số ghép "
     r"nhóm như sau." + ng("lhp")
     + B(["Thời gian (giây)", "$[13; 15)$", "$[15; 17)$", "$[17; 19)$", "$[19; 21)$", "Tổng"],
         ["Tần số ($n$)", 12, 15, 8, 5, "$N=40$"])
     + r"[TH] Tìm tần số tương đối ghép nhóm của mỗi nhóm rồi lập bảng tần số tương đối ghép nhóm của mẫu số liệu.",
     "12/40=30%, 15/40=37,5%, 8/40=20%, 5/40=12,5% · bảng tabular · Vậy …"),
    ("Bài 36.", "reflection", "btvn", "TH1", 2, "sgk-7.6", "", "th_dan",
     r"[TH] Lớp 9A có $40$ bạn, trong đó $20$ bạn mặc áo cỡ M, $13$ bạn mặc áo cỡ S, $7$ bạn mặc áo cỡ L. Hãy lập bảng "
     r"tần số tương đối cho dữ liệu này." + sgk("Bài tập 7.6"),
     "f(M)=20/40=50%, f(S)=13/40=32,5%, f(L)=7/40=17,5% · bảng tabular (Cỡ áo | S | M | L hoặc M | S | L như đề) · Vậy …"),
    ("Bài 37.", "reflection", "btvn", "NB6+TH1", 2, "gk2-ngoc-lam-2024-I1", "", "th_dan",
     r"Cô giáo đã ghi lại điểm thi môn Toán của học sinh lớp 9A trong bảng dưới đây." + ng("nl24")
     + B(["Điểm", 7, 8, 9, 10], ["Số học sinh", 6, 14, 16, 4])
     + y(r"a) [NB] Lớp 9A có bao nhiêu học sinh?",
         r"b) [TH] Lập bảng tần số tương đối của mẫu số liệu thống kê đó."),
     "a) 40. b) Theo câu a): 15%, 35%, 40%, 10% · bảng · Vậy …"),
    ("Bài 38.", "reflection", "btvn", "NB9+TH3", 2, "tl-tanso-5-tr4", "", "th_dan",
     r"Biểu đồ bên thống kê thời gian công tác (theo năm) của các y tá ở một phòng khám." + ng("tlmt")
     + C([1, 2, 3, 4, 5, 6, 7], [6, 5, 5, 7, 9, 5, 2], "Số năm công tác", "Số y tá", 10, 2,
         tieu_de="Số lượng y tá theo năm công tác", bw=0.6, gap=0.45)
     + y(r"a) [NB] Các y tá của phòng khám có thời gian công tác nhận những giá trị nào? Tìm tần số của mỗi giá trị đó.",
         r"b) [NB] Phòng khám có tổng số bao nhiêu y tá?",
         r"c) [TH] Có bao nhiêu y tá đã công tác ở phòng khám ít nhất $3$ năm?"),
     "a) 1, 2, …, 7 năm với tần số 6, 5, 5, 7, 9, 5, 2. b) 39 y tá. c) Theo câu a): ít nhất 3 năm gồm 3, 4, 5, 6, 7 "
     "năm · 5+7+9+5+2=28 · Vậy 28 y tá."),
    ("Bài 39.", "reflection", "btvn", "NB9+TH3", 2, "ck2-hoai-duc-2024-I1", "", "th_dan",
     r"Thời gian đi từ nhà đến trường (đơn vị: phút) của $16$ bạn học sinh được ghi lại ở bảng sau." + ng("hdu")
     + L(HD, 8)
     + y(r"a) [NB] Lập bảng tần số của mẫu số liệu thống kê trên.",
         r"b) [TH] Trong $16$ bạn học sinh trên, có bao nhiêu bạn dành thời gian để đi đến trường nhiều hơn $10$ phút?"),
     "a) 9 phút: 4, 10: 4, 11: 2, 12: 3, 15: 3. b) Theo câu a): nhiều hơn 10 phút gồm 11, 12, 15 (không lấy 10) · "
     "2+3+3=8 · Vậy 8 bạn."),
    ("Bài 40.", "reflection", "btvn", "NB9+TH3", 2, "gk2-le-ngoc-han-2024-I1", "", "th_dan",
     r"Thống kê số lần truy cập Internet của toàn bộ học sinh lớp 9A trong một tuần cho kết quả bảng tần số ghép nhóm như "
     r"sau." + ng("lnh24")
     + B(["Số lần truy cập", "$[30; 40)$", "$[40; 50)$", "$[50; 60)$", "$[60; 70)$", "$[70; 80)$", "$[80; 90)$"],
         ["Tần số", 6, 12, 6, 9, 6, 9])
     + y(r"a) [NB] Lớp 9A có bao nhiêu học sinh?",
         r"b) [TH] Tìm tần số tương đối ghép nhóm của nhóm $[60; 80)$."),
     "a) 48. b) Theo câu a): nhóm [60; 80) gồm [60;70) và [70;80), tần số 9+6=15 · 15/48·100%=31,25% · Vậy 31,25%."),
    ("Bài 41.", "reflection", "btvn", "TH2", 2, "sgk-7.12", "", "th_dan",
     r"Tỉ lệ bình chọn các tiết mục văn nghệ của các lớp 9A, 9B, 9C, 9D tham gia hội diễn văn nghệ khối lớp 9 như sau."
     + sgk("Bài tập 7.12")
     + B(["Lớp", "9A", "9B", "9C", "9D"], ["Tỉ lệ học sinh bình chọn", r"$35\%$", r"$25\%$", r"$30\%$", r"$10\%$"])
     + r"[TH] Biết rằng có $300$ học sinh tham gia bình chọn. Lập bảng tần số biểu diễn số học sinh bình chọn cho tiết "
       r"mục văn nghệ của mỗi lớp.",
     "300·35%=105, 300·25%=75, 300·30%=90, 300·10%=30 · bảng · Vậy …"),
    ("Bài 42.", "reflection", "btvn", "NB8+TH2", 2, "ck2-trung-vuong-2025-I1", "", "th_dan",
     r"Một tổ chức khảo sát thời gian sử dụng điện thoại thông minh mỗi ngày của một nhóm sinh viên thu được kết quả sau."
     + ng("tv")
     + C([3, 4, 5, 6, 7, 8], [10, 20, 33, 25, 12], "Thời gian (h)", r"Tần số tương đối (\%)", 40, 10, sat=True,
         tren=[r"$10\%$", r"$20\%$", r"$33\%$", r"$25\%$", r"$12\%$"])
     + y(r"a) [NB] Tìm tần số tương đối của nhóm $[5; 6)$.",
         r"b) [TH] Biết số người sử dụng điện thoại trong nhóm $[3; 4)$ là $20$ người. Tính số người tham gia khảo sát "
         r"ban đầu."),
     "a) 33%. b) Theo câu a) (đọc biểu đồ), nhóm [3; 4) có f=10% ứng với 20 người · từ f=m/n·100% ta có n=m:f · "
     "n=20:10%=200 · Vậy 200 người."),
    ("Bài 43.", "reflection", "btvn", "TH4", 2, "sgk-b24-lt2", "", "th_dan",
     r"Các nước và vùng lãnh thổ trên thế giới được chia thành bốn nhóm theo chỉ số phát triển con người (HDI): Nhóm 1 "
     r"(rất cao) có HDI từ $0{,}8$ trở lên, Nhóm 2 (cao) có HDI từ $0{,}7$ đến dưới $0{,}8$, Nhóm 3 (trung bình) có HDI "
     r"từ $0{,}55$ đến dưới $0{,}7$, Nhóm 4 (thấp) có HDI dưới $0{,}55$. Năm $2021$, chỉ số HDI của $11$ quốc gia Đông Nam "
     r"Á như sau:[[br]]\hspace*{1.4em}" + ", \\ ".join(f"${HT.vn(v)}$" for v in HDI) + "." + sgk("Bài 24, Luyện tập 2")
     + BR + r"[TH] Dựa vào dữ liệu trên, hãy hoàn thành bảng tần số ghép nhóm sau."
     + B(["Chỉ số HDI", "$[0; 0{,}55)$", "$[0{,}55; 0{,}7)$", "$[0{,}7; 0{,}8)$", "$[0{,}8; 1{,}0)$"],
         ["Tần số", "?", "?", "?", "?"]),
     "0, 5, 2, 4 (0,8 thuộc [0,8; 1,0); 0,699 thuộc [0,55; 0,7)) · Vậy …"),
    ("Bài 44.", "reflection", "btvn", "NB10+TH5", 2, "ck2-cau-dien-2025-I1", "", "th_dan",
     r"Biểu đồ dưới đây biểu diễn kết quả khảo sát thành tích chạy $100$ m của $16$ học sinh." + ng("cd")
     + C([11, 12, 13, 14, 15, 16], [3, 6, 4, 2, 1], "Thời gian chạy (giây)", "Tần số ($n$)", 8, 2, sat=True)
     + y(r"a) [NB] Có bao nhiêu học sinh chạy $100$ m hết ít hơn $13$ giây?",
         r"b) [TH] Thầy giáo đã nhận định \textquotedblleft Có trên $18\%$ học sinh chạy $100$ m hết từ $14$ giây đến "
         r"$16$ giây\textquotedblright. Nhận định đó đúng hay sai?"),
     "a) [11;12) và [12;13): 3+6=9. b) Từ 14 đến 16 giây gồm [14;15) và [15;16): 2+1=3 học sinh · 3/16·100%=18,75% · "
     "18,75%>18% · Vậy nhận định đúng."),
]

OPTIONS = {
    "Bài 1.": ["$33{,}5$", "$34{,}5$", "$35$", "$35{,}9$"],
    "Bài 12.": [r"có $23$ con ong sống được đúng $40$ ngày",
                r"có $23$ con ong sống từ $40$ ngày đến $50$ ngày, kể cả $50$ ngày",
                r"có $23$ con ong sống từ $40$ ngày đến dưới $50$ ngày",
                r"tuổi thọ trung bình của đàn ong là $23$ ngày"],
}
# Bài 33, 34 in phương án ngay trong đề (dan_dat_gate: bài có "options" không được đứng sau bài nhiều ý trong BTVN)
# 18/11 (Thầy duyệt phương án a): câu NB tính tần số tương đối → trắc nghiệm A–D, đọc biểu đồ → Đúng/Sai,
# "tần số / cỡ mẫu" → trả lời ngắn chỉ ghi số. Bài TH, bài đích, lập bảng chính (Bài 8a, 10, 20, 23) giữ tự luận.
DAP_TN = {"Bài 4.": "C", "Bài 5.": "B", "Bài 6.": "A", "Bài 7.": "D", "Bài 8.": "C", "Bài 11.": "BD", "Bài 12.": "C",
          "Bài 25.": "A", "Bài 27.": "C", "Bài 29.": "D", "Bài 28.": "A", "Bài 30.": "BC", "Bài 31.": "B",
          "Bài 32.": "D", "Bài 33.": "B", "Bài 34.": "C"}
DAP_DS = {"Bài 3.": "S", "Bài 2.": "ĐS", "Bài 9.": "ĐS", "Bài 27.": "S"}

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu 1 (18/11)
    "NB1": (1, 0), "NB2": (9, 7), "NB3": (8, 10), "NB4": (1, 1), "NB5": (2, 1), "NB6": (2, 1), "NB7": (1, 0),
    "NB8": (2, 1), "NB9": (6, 4), "NB10": (0, 1),
    "TH1": (2, 3), "TH2": (2, 2), "TH3": (4, 3), "TH4": (2, 1), "TH5": (2, 1),
}


def kiem():
    loi = []

    def bang(ten, that, mong):
        if that != mong:
            loi.append(f"{ten}: máy ra {that}, sơ đồ ghi {mong}")

    bang("VD1 cỡ giày", dem(GIAY), {36: 5, 37: 4, 38: 8, 39: 2, 40: 3})
    bang("B8 bóng đèn", dem(DEN), {1150: 3, 1160: 6, 1170: 12, 1180: 6, 1190: 3})
    bang("B8 f", pt(3, 30), 10)
    bang("B10 Hát Môn", dem(HM), {2: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 5, 9: 2, 10: 1})
    from decimal import Decimal, ROUND_HALF_UP
    bang("B10 f8", Decimal(str(float(pt(5, 32)))).quantize(Decimal("0.01"), ROUND_HALF_UP), Decimal("15.63"))
    bang("B10 f9", pt(2, 32), F(25, 4))
    bang("VD5 không khí", dem(KK), {"M1": 9, "M2": 12, "M3": 6, "M4": 3})
    bang("B17 hộ", dem(HO, [(2, 4)]), [5])
    bang("VD9 SGK", dem(CAO_SGK, [(150, 158), (158, 161), (161, 164), (164, 167)]), [5, 12, 15, 8])
    bang("B20 Cát Linh", dem(CAO_CL, [(140, 150), (150, 160), (160, 170), (170, 180)]), [6, 15, 19, 10])
    bang("B21 Thanh Oai", dem(DIEN, [(100, 130), (130, 160), (160, 190), (190, 220)]), [3, 5, 5, 7])
    bang("B24 vệ sinh", dem(VS), {"Khá": 11, "Kém": 2, "Trung bình": 5, "Tốt": 13})
    bang("B26 chữ cái", dem(CHU), {"B": 1, "H": 8, "I": 9, "S": 3})
    bang("B39 Hoài Đức", dem(HD), {9: 4, 10: 4, 11: 2, 12: 3, 15: 3})
    bang("B39 >10", sum(1 for v in HD if v > 10), 8)
    bang("B43 HDI", dem(HDI, [(0, 0.55), (0.55, 0.7), (0.7, 0.8), (0.8, 1.0)]), [0, 5, 2, 4])
    for ten, m, n, f in [("VD3b", 75, 300, 25), ("B4", 14, 50, 28), ("B5", 5, 40, F(25, 2)), ("B6", 10, 40, 25),
                         ("B7", 86, 500, F(86, 5)), ("B9", 35, 100, 35), ("B11", 4, 50, 8), ("VD6", 116, 200, 58),
                         ("B15", 21, 40, F(105, 2)), ("B16", 51, 150, 34), ("B17", 5, 20, 25), ("B22b", 20, 40, 50),
                         ("VD10a", 9, 60, 15), ("VD10b", 42, 60, 70), ("B23b", 7, 40, F(35, 2)), ("B23c", 10, 40, 25),
                         ("B25", 20, 50, 40), ("B28", 10, 40, 25), ("B29", 15, 60, 25), ("B30", 12, 60, 20),
                         ("B31", 6, 40, 15), ("B32", 24, 60, 40), ("B40", 15, 48, F(125, 4)), ("B44", 3, 16, F(75, 4))]:
        bang(ten, pt(m, n), f)
    bang("VD3a", 50 - (8 + 7 + 8 + 6 + 11), 10)
    bang("VD7", 160 * F(3375, 10000), 54)
    bang("VD8 tổng", 35 + 20 + 15 + 10, 80)
    bang("VD8 f", [pt(v, 80) for v in (35, 20, 15, 10)], [F(175, 4), 25, F(75, 4), F(25, 2)])
    bang("VD8 ước lượng", 240 * pt(35, 80) / 100, 105)
    bang("B18", 200 * F(40, 100), 80)
    bang("B19", 200 * F(60, 100), 120)
    bang("B27", (sum([274, 280, 370, 516]), round(float(pt(280, 1440)), 2)), (1440, 19.44))
    bang("B31 thiếu", 40 - (2 + 8 + 20 + 4), 6)
    bang("B38", (sum([6, 5, 5, 7, 9, 5, 2]), sum([5, 7, 9, 5, 2])), (39, 28))
    bang("B41", [300 * p // 100 for p in (35, 25, 30, 10)], [105, 75, 90, 30])
    bang("B42", 20 * 100 // 10, 200)
    bang("B35", [pt(v, 40) for v in (12, 15, 8, 5)], [30, F(75, 2), 20, F(25, 2)])
    bang("B13", [pt(v, 20) for v in (1, 5, 9, 5)], [5, 25, 45, 25])
    bang("B14", [pt(v, 40) for v in (4, 6, 12, 8, 8, 2)], [10, 15, 30, 20, 20, 5])
    bang("B37", [pt(v, 40) for v in (6, 14, 16, 4)], [15, 35, 40, 10])
    bang("B36", [pt(v, 40) for v in (20, 13, 7)], [50, F(65, 2), F(35, 2)])
    bang("VD5b", [pt(v, 40) for v in (5, 20, 13, 2)], [F(25, 2), 50, F(65, 2), 5])
    bang("VD9 f", [pt(v, 40) for v in (5, 12, 15, 8)], [F(25, 2), 30, F(75, 2), 20])
    bang("B22a", [pt(v, 40) for v in (5, 15, 12, 8)], [F(25, 2), F(75, 2), 30, 20])
    for ten, ds in [("B5", [15, 10, 10, 5]), ("B23", [3, 5, 6, 7, 9, 10]), ("B28", [4, 6, 8, 10, 12]),
                    ("B29", [5, 8, 12, 20, 15]), ("B30", [6, 9, 12, 18, 12, 3]), ("B34", [4, 14, 8, 10, 6, 2]),
                    ("B44", [3, 6, 4, 2, 1]), ("VD10", [3, 6, 19, 23, 9]), ("B6", [5, 8, 10, 12, 5]),
                    ("B7", [114, 86, 97, 61, 73, 69]), ("B25", [10, 15, 20, 5])]:
        bang(ten + " cỡ mẫu", sum(ds), {"B5": 40, "B23": 40, "B28": 40, "B29": 60, "B30": 60, "B34": 44, "B44": 16,
                                         "VD10": 60, "B6": 40, "B7": 500, "B25": 50}[ten])
    return loi


def dem_the():
    dem_ = collections.Counter()
    for k in KHOI:
        if len(k) < 9 or k[7] == "vi_du":
            continue
        _, _, tier, dang, *_ = k
        ma = dang.split("+")
        for t in re.findall(r"\[(NB|TH|VD)\]", k[8]):
            dem_[(next(mm for mm in ma if re.match(rf"{t}\d", mm)), tier)] += 1
    loi = []
    for d, (lop, btvn) in TM_DANG.items():
        for tier, want in (("onclass", lop), ("btvn", btvn)):
            if dem_[(d, tier)] != want:
                loi.append(f"{d} {tier}: sơ đồ {dem_[(d, tier)]} thẻ, TM {want}")
    tong = collections.Counter()
    for (d, tier), n in dem_.items():
        tong[(d[:2], tier)] += n
    return loi, dict(tong)


if __name__ == "__main__":
    l1 = kiem()
    l2, tong = dem_the()
    print("thẻ:", tong, "· số hình/bảng:", len(_HINH))
    for l in l1 + l2:
        print("✗", l)
    print("SẠCH" if not (l1 + l2) else f"{len(l1 + l2)} lỗi")
    sys.exit(1 if (l1 + l2) else 0)
