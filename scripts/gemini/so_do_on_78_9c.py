#!/usr/bin/env python3
"""Sơ đồ Phiếu 2 ch.VIII 9C (19/11/2026) — "Ôn tập chương VII và VIII" (135′ + 45′ kiểm tra gộp VII+VIII, t33).

Thầy chốt 19/11: ôn NHƯ ĐI THI (bài thông hiểu không câu dẫn, không gợi ý — giữ đúng cấu trúc ý của đề gốc),
BTVN đủ 90′ (phiếu riêng). Khuôn `khong_vd` 40–60. Quỹ (he_so 0,75): ví dụ 34′, trên lớp 90′ = 24 NB + 9 TH;
BTVN 22 NB + 10 TH ≈ 81′.
Câu MỚI hoàn toàn: không trùng chon-cau ch.VII, ch.VIII, đề KT gộp, nhóm TRUNG của hai script chọn câu (máy soát ở
kiem_trung()). Bỏ tl-ptnn-xsbc-28-tr7 và v10-huy-van-2024-I2 vì gần y hệt đề KT Câu 6 (số hai chữ số, chia hết 2 và 5).
ĐÍCH = Bài 21: Câu I đề HK2 THCS Bế Văn Đàn 2025--2026 (I.1 biểu đồ ghép nhóm + I.2 xác suất một hành động).

Claude CHỐT ĐỀ (nguyên văn đề gốc, tách ý), thẻ, đáp số (máy kiểm ở kiem()). Hình máy vẽ (hinh_thong_ke.py).
Gemini viết lời giải, lời giải ví dụ điền khuyết, mở đầu, kiến thức cần nhớ.

    .venv/bin/python scripts/gemini/so_do_on_78_9c.py      # kiểm đáp số + đếm thẻ + soát trùng
"""
from __future__ import annotations

import collections
import itertools
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
    """Đề có đúng MỘT hình (không bảng) và có chữ sau hình ⇒ hình sang phải, chữ bên trái."""
    ids = [int(i) for i in re.findall(r"⟦H(\d+)⟧", s)]
    if len(ids) != 1 or _LOAI[ids[0]] != "hinh":
        return s
    tr, sau = s.split(f"⟦H{ids[0]}⟧")
    if not sau.strip() and "[[br]]" in tr:
        tr, sau = tr.rsplit("[[br]]", 1)
        tr += "[[br]]"
    if not tr.strip() or not sau.strip():
        return s
    sau = re.sub(r"^\s*(\[\[br\]\]\s*)+", "", sau)   # khung chữ cạnh hình không mở bằng dòng trống (LaTeX lỗi)
    return tr + HT.ben_phai(sau, _HINH[ids[0]][0], rong_hinh=RONG.get(ids[0], 0.41))


RONG: dict[int, float] = {}     # token → bề rộng cột hình khi xếp cạnh (đĩa quay nhỏ ⇒ cột hẹp)
PHONG: dict = {}                # nhãn → bề rộng hình (phần \linewidth) khi cần lấp trang trắng
PHONG_BANG: dict = {}
_TU_DO = Path(__file__).with_name("phong_on_78_9c.json")
if _TU_DO.exists():
    import json as _json
    _d = _json.loads(_TU_DO.read_text())
    PHONG.update(_d.get("hinh", {}))
    PHONG_BANG.update(_d.get("bang", {}))
GIU_ON = r"\interlinepenalty=10000\clubpenalty=10000\widowpenalty=10000 "
GIU_OFF = r"\interlinepenalty=0\clubpenalty=150\widowpenalty=150 "


def _phong(tex: str, r: float) -> str:
    return (r"\par\nopagebreak\smallskip\nopagebreak{\centering\adjustbox{width=" + f"{r}" + r"\linewidth}{"
            + HT.ruot(tex) + r"}\par}\smallskip ")


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


def C(nhan, gt, tx, ty, ymax, buoc, sat=False, tieu_de="", **kw):
    if sat:
        mo = [f"[{HT.vn(nhan[i])}; {HT.vn(nhan[i + 1])}): {HT.vn(gt[i])}" for i in range(len(gt))]
    else:
        mo = [f"{_o(nhan[i])}: {HT.vn(gt[i])}" for i in range(len(gt))]
    loai = "biểu đồ cột tần số ghép nhóm (cột sát nhau)" if sat else "biểu đồ cột"
    return _tok(HT.cot(nhan, gt, tx, ty, ymax, buoc, sat=sat, tieu_de=tieu_de, **kw),
                f"{loai} \"{tieu_de}\", trục ngang {_o(tx)}, trục đứng {_o(ty)}; " + "; ".join(mo), "hinh")


def K(nhan, a, b, chu, tx, ty, ymax, buoc, tieu_de=""):
    return _tok(HT.cot_kep(nhan, a, b, chu, tx, ty, ymax, buoc, tieu_de=tieu_de),
                f"biểu đồ cột kép \"{tieu_de}\" ({chu[0]}, {chu[1]}); "
                + "; ".join(f"{t}: {chu[0]} {x}, {chu[1]} {y}" for t, x, y in zip(nhan, a, b)), "hinh")


def Q(pt, chu, tieu_de=""):
    return _tok(HT.quat(pt, chu, tieu_de=tieu_de),
                f"biểu đồ hình quạt tròn \"{tieu_de}\"; " + "; ".join(f"{_o(c)}: {HT.vn(p)}%" for p, c in zip(pt, chu)), "hinh")


def DQ(nhan, kim="tam", R=1.0, rong=0.3, ten=""):
    t = _tok(HT.dia(nhan, R=R, kim=kim, ten=ten),
             f"đĩa tròn chia {len(nhan)} hình quạt bằng nhau ghi các số " + ", ".join(_o(c) for c in nhan)
             + (", mũi tên ở tâm" if kim == "tam" else ", mũi kim gắn cố định phía trên"), "hinh")
    RONG[len(_HINH) - 1] = rong
    return t


def BC():
    t = _tok(HT.ban_co(), "bảng 8 × 8 ô vuông tô xen kẽ trắng đen như bàn cờ (32 ô trắng, 32 ô đen)", "hinh")
    RONG[len(_HINH) - 1] = 0.3
    return t


def P2(*tok, rong=0.3, cach="1.5cm"):
    """Hai hình cạnh nhau ở giữa dòng (19/11 Thầy: \\hfill đẩy hình lệch ra hai bên)."""
    ids = [int(re.match(r"⟦H(\d+)⟧", t)[1]) for t in tok]
    return _tok(HT.canh(*[_HINH[i][0] for i in ids], rong=rong, cach=cach), " ; ".join(_HINH[i][1] for i in ids))


def tn(*o):
    """Bốn phương án A–D chia cột đều: ngắn 4 cột, vừa 2 cột, dài 1 cột."""
    dai = max(len(re.sub(r"\\[a-zA-Z]+|[{}$\\]", "", x)) for x in o)
    if dai > 30:   # 19/11 Thầy: phương án dài tràn lề phải ⇒ một cột, không makebox (tự xuống dòng)
        return "".join(rf"[[br]]\hspace*{{1.4em}}{c}. {x}" for c, x in zip("ABCD", o))
    w, moi = ("0.22", 4) if dai <= 9 else ("0.45", 2)
    o = [rf"\makebox[{w}\linewidth][l]{{{c}. {x}}}" for c, x in zip("ABCD", o)]
    return "".join("[[br]]\\hspace*{1.4em}" + "".join(o[i:i + moi]) for i in range(0, 4, moi))


def q(s):
    return r"\textquotedblleft " + s + r"\textquotedblright{}"   # {} giữ dấu cách sau ngoặc đóng


def fr(a, b):
    return rf"$\dfrac{{{a}}}{{{b}}}$"


DS = r"Mỗi khẳng định sau đúng hay sai?"


def y(*ds):
    return BR.join(ds)


def D(nhan, gt, tx, ty, ymax, buoc, tieu_de="", **kw):
    return _tok(HT.doan(nhan, gt, tx, ty, ymax, buoc, tieu_de=tieu_de, **kw),
                f"biểu đồ đoạn thẳng \"{tieu_de}\", trục ngang {_o(tx)}, trục đứng {_o(ty)}; "
                + "; ".join(f"{_o(a)}: {HT.vn(b)}" for a, b in zip(nhan, gt)), "hinh")


def T(nhom, so, chu_thich):
    return _tok(HT.tranh(nhom, so, chu_thich),
                "biểu đồ tranh: " + "; ".join(f"{a}: {b} biểu tượng" for a, b in zip(nhom, so)) + f" ({chu_thich})",
                "hinh")


# ── NGUỒN in sau đề ───────────────────────────────────────────────────────────
DD = r"đề minh họa tuyển sinh lớp 10, Phòng GD\&ĐT Đống Đa, "
N = {
    "tlmt": r"tài liệu Mathtech \textquotedblleft Phép thử ngẫu nhiên và không gian mẫu. Xác suất của biến "
            r"cố\textquotedblright",
    "tlts": r"tài liệu Mathtech \textquotedblleft Bảng tần số và biểu đồ tần số\textquotedblright",
    "tlgn": r"tài liệu Mathtech \textquotedblleft Bảng tần số ghép nhóm\textquotedblright",
    "tlbd": r"tài liệu Mathtech \textquotedblleft Mô tả và biểu diễn dữ liệu\textquotedblright",
    "hbt": r"HK2 Phòng GD\&ĐT Hai Bà Trưng, 2024--2025", "tvg25": r"GK2 THCS Trưng Vương, 2025--2026",
    "tvg24": r"GK2 THCS Trưng Vương, 2024--2025",
    "cg": r"thi thử vào 10 lần 1 THCS Cầu Giấy, 2025--2026", "hv": DD + r"đề 06 (THCS Huy Văn), 2025--2026",
    "ntt": r"đề tham khảo tuyển sinh lớp 10 Trường THCS\&THPT Nguyễn Tất Thành, 2025--2026",
    "tt15": DD + r"đề 15 (THCS Thái Thịnh), 2025--2026", "tll5": r"thi thử vào 10 lần 5 THCS Thọ Lộc, 2025--2026",
    "tll2": r"thi thử vào 10 lần 2 THCS Thọ Lộc, 2025--2026",
    "cvadn": r"HK2 THCS Chu Văn An (Thanh Khê, Đà Nẵng), 2025--2026",
    "ttc": r"HK2 THCS Thái Thịnh (Đống Đa), 2025--2026", "pdg24": r"GK2 THCS Phúc Đồng, 2024--2025",
    "pl24": r"GK2 THCS Phúc Lợi, 2024--2025", "lhp": r"HK2 THCS Lê Hồng Phong (Hà Đông), 2025--2026",
    "cva": r"HK2 THCS Chu Văn An (Tây Hồ), 2024--2025", "bvd": r"HK2 THCS Bế Văn Đàn, 2025--2026",
    "nhtan25": r"GK2 THCS Nhật Tân, 2025--2026", "ntan25": r"GK2 THCS Nghĩa Tân, 2025--2026", "ntanc": r"HK2 THCS Nghĩa Tân, 2025--2026",
    "tmy": r"GK2 THCS Thanh Mỹ, 2024--2025", "pl1": r"HK2 THCS Phúc Lợi (Long Biên), 2024--2025",
    "bm": r"GK2 Ban Mai School, 2025--2026", "tt26": r"thi thử vào 10 THCS Thái Thịnh, 2026--2027",
}


def ng(k):
    return r" \textit{(" + N[k] + ")}"


def sgk(s):
    return r" \textit{(SGK Toán 9 tập hai, " + s + ")}"


def le(*ds):
    """Dòng con thụt vào (liệt kê biến cố)."""
    return BR.join(r"\hspace*{1.4em}" + d for d in ds)


# ── SỐ LIỆU (dùng chung cho hình + kiem) ──────────────────────────────────────
CAO_TT = [90, 73, 88, 93, 101, 104, 111, 95, 78, 95, 81, 97, 96, 92, 95, 83, 90, 101, 103, 117,
          109, 110, 112, 87, 75, 90, 82, 97, 86, 96]
CAO_PD = [156, 157, 161, 158, 166, 160, 162, 157, 163, 160, 163, 164, 158, 159, 166, 162, 161, 165, 163, 163,
          162, 159, 165, 163, 162, 161, 155, 159, 158, 164, 165, 162, 161, 160, 164, 162, 161, 162, 166, 160]
BACH_DAN = [21.2, 19.8, 28.6, 18, 29.8, 27.2, 18.1, 28.4, 18.8, 23.8, 16, 19, 29.6, 18.3, 21.8, 20.6, 25, 27.1,
            23.3, 19.5, 23.2, 17, 17.8, 15.9, 16.8, 18.4, 21.9, 24.3, 27.3, 21, 29.2, 23.5, 29.6, 22.2, 24.4,
            15.4, 23.8, 16.4, 17.2, 23.5]
XANG = [4, 5, 5, 6, 7, 8, 10, 10, 35, 12, 12, 15, 15, 17, 18, 19, 19, 38, 22, 24, 25, 28, 30, 32, 34, 34, 39]
TO_HUU = ["Ngang", "Sắc", "Huyền", "Hỏi", "Ngã", "Nặng"], [12, 10, 4, 1, 1, 5]

XX = r"Gieo đồng thời hai con xúc xắc cân đối và đồng chất I và II."

# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# Tiêu đề: (chữ, chặng, "heading").
# Ví dụ:  (nhãn, chặng, "", "", 0, mã, "", "vi_du", ĐỀ IN (có nguồn), GHI lời giải cho thợ).
# Bài:    (nhãn, chặng, tier, dang_id, level, mã, "", hình thức, ĐỀ IN, GHI đáp số cho thợ).
KHOI = [
    # ───────────── LUYỆN TẬP 1 — NHẬN BIẾT (21 thẻ) ─────────────
    ("Mạch 1. Tần số và tần số tương đối", "practice1", "heading"),
    ("Bài 1.", "practice1", "onclass", "NB1", 1, "ck2-hai-ba-trung-2024-I1", "", "tra_loi_ngan",
     r"Bạn Minh hỏi $40$ bạn học sinh bất kì về môn học mà bạn đó yêu thích nhất. Kết quả thống kê được ghi lại ở "
     r"bảng sau." + ng("hbt")
     + B(("Môn học", "Toán", "Ngữ văn", "Lịch sử", "Thể dục"), ("Số học sinh yêu thích", 11, 8, 9, 12))
     + y(r"a) [NB] Chỉ ra tần số của môn Lịch sử.", r"b) [NB] Tính tần số tương đối của môn Lịch sử."),
     "a) Tần số của môn Lịch sử là 9. b) f = 9/40 · 100% = 22,5%. Mỗi ý 1–2 dòng."),
    ("Bài 2.", "practice1", "onclass", "NB1", 1, "gk2-trung-vuong-2025-I1", "", "tra_loi_ngan",
     r"Kết quả điểm khảo sát tháng 2 môn Toán của học sinh lớp 9G được thống kê trong bảng tần số sau." + ng("tvg25")
     + B(("Điểm số", 3, 4, 5, 6, 7, 8, 9, 10), (r"Tần số ($n$)", 1, 2, 6, 5, 7, 8, 7, 4))
     + y(r"a) [NB] Lớp 9G có bao nhiêu học sinh?", r"b) [NB] Tính tần số tương đối của điểm $9$."),
     "a) 1+2+6+5+7+8+7+4 = 40 học sinh. b) f = 7/40 · 100% = 17,5%."),
    ("Bài 3.", "practice1", "onclass", "NB1", 1, "v10-cau-giay-lan1-2026-I1", "", "tra_loi_ngan",
     r"Thống kê điểm thi học kì I môn Toán 9 của một trường THCS theo nhóm được cho bởi bảng sau (không có học sinh "
     r"bỏ thi)." + ng("cg")
     + B(("Điểm", r"$\le 7$", r"$(7; 8]$", r"$(8; 9]$", r"$(9; 10]$"), ("Số lượng", 33, 60, 189, 168))
     + y(r"a) [NB] Hỏi khối 9 của trường đó có bao nhiêu học sinh?",
         r"b) [NB] Nhóm điểm nào trong bảng có nhiều học sinh nhất và chiếm bao nhiêu phần trăm số học sinh của khối 9?"),
     "a) 33+60+189+168 = 450 học sinh. b) Nhóm (8; 9] có 189 học sinh, nhiều nhất · 189/450 · 100% = 42%."),
    ("Bài 4.", "practice1", "onclass", "NB1", 1, "sgk-b23-hd2 (ý b)", "", "tra_loi_ngan",
     r"Có ba phương án thi đấu tại giải bóng đá khối lớp 9 của một trường. Ban tổ chức đã lấy phiếu khảo sát ý kiến, "
     r"kết quả được biểu diễn bằng biểu đồ sau." + sgk("Bài 23, Hoạt động 2")
     + C(["Phương án 1", "Phương án 2", "Phương án 3"], [28, 61, 11], "Phương án", r"Tỉ lệ (\%)", 80, 20,
         tieu_de="Tỉ lệ ủng hộ các phương án thi đấu", tren=[r"$28\%$", r"$61\%$", r"$11\%$"])
     + r"[NB] Lập bảng tần số tương đối cho kết quả khảo sát ý kiến.",
     "Bảng [[bang: Phương án | Phương án 1 | Phương án 2 | Phương án 3 / Tần số tương đối | $28\\%$ | $61\\%$ | $11\\%$]]. "
     "1 dòng dẫn + bảng."),

    ("Mạch 2. Bảng tần số ghép nhóm, biểu đồ ghép nhóm", "practice1", "heading"),
    ("Bài 5.", "practice1", "onclass", "NB2", 1, "v10-huy-van-2024-I1", "", "tra_loi_ngan",
     r"Sau khi thống kê độ dài (đơn vị: centimét) của $50$ lá dương xỉ trưởng thành, người ta có biểu đồ tần số ghép "
     r"nhóm dưới đây." + ng("hv")
     + C([10, 20, 30, 40, 50], [5, 15, 20, 10], "Độ dài (cm)", r"Tần số ($n$)", 25, 5, sat=True)
     + y(r"a) [NB] Tìm tần số ghép nhóm của nhóm $[30; 40)$.",
         r"b) [NB] Tìm tần số tương đối ghép nhóm của nhóm $[30; 40)$."),
     "a) 20. b) f = 20/50 · 100% = 40%."),
    ("Bài 6.", "practice1", "onclass", "NB2", 1, "gk2-thanh-my-2024-11", "", "tra_loi_ngan",
     r"Sau khi điều tra số tiền điện phải trả của $50$ hộ gia đình trong một tháng (đơn vị: nghìn đồng), người ta có "
     r"biểu đồ tần số ghép nhóm dưới đây." + ng("tmy")
     + C([300, 400, 500, 600, 700], [17, 12, 10, 11], "Số tiền (nghìn đồng)", "Số hộ gia đình", 20, 4, sat=True)
     + y(r"a) [NB] Tìm tần số ghép nhóm của nhóm $[500; 600)$.",
         r"b) [NB] Tìm tần số tương đối ghép nhóm của nhóm $[500; 600)$."),
     "Đề gốc ghi nhầm tên trục ngang ('Số hộ gia đình') — phiếu vẽ đúng. a) 10. b) 10/50 · 100% = 20%."),
    ("Bài 7.", "practice1", "onclass", "NB2", 1, "sgk-7.26", "", "tra_loi_ngan",
     r"Biểu đồ tần số tương đối ghép nhóm sau cho biết tỉ lệ chiều cao của các cây keo giống do một kĩ sư lâm nghiệp "
     r"đã trồng trong nhà kính." + sgk("Bài tập 7{.}26")
     + C([0, 10, 20, 30, 40], [10, 20, 40, 30], "Chiều cao (cm)", r"Tỉ lệ (\%)", 45, 10, sat=True,
         tren=[r"$10\%$", r"$20\%$", r"$40\%$", r"$30\%$"])
     + r"[NB] Lập bảng tần số tương đối ghép nhóm cho dữ liệu được biểu diễn trên biểu đồ.",
     "Bảng [[bang: Chiều cao (cm) | $[0; 10)$ | $[10; 20)$ | $[20; 30)$ | $[30; 40)$ / Tần số tương đối | $10\\%$ | "
     "$20\\%$ | $40\\%$ | $30\\%$]]. 1 dòng dẫn + bảng."),

    ("Mạch 3. Phép thử ngẫu nhiên và không gian mẫu", "practice1", "heading"),
    ("Bài 8.", "practice1", "onclass", "NB3", 1, "tl-ptnn-xsbc-4-tr3", "", "tra_loi_ngan",
     r"Một hộp có $12$ chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, \ldots, 12$, hai thẻ khác nhau "
     r"thì ghi hai số khác nhau. Xét phép thử " + q("Rút ngẫu nhiên một thẻ trong hộp") + "." + ng("tlmt")
     + BR + y(r"a) [NB] Nêu những kết quả có thể xảy ra đối với số xuất hiện trên thẻ được rút ra.",
              r"b) [NB] Viết không gian mẫu của phép thử đó."),
     "a) Các kết quả có thể: 1, 2, 3, …, 12. b) Ω = {1; 2; 3; …; 12}, n(Ω) = 12."),
    ("Bài 9.", "practice1", "onclass", "NB3", 1, "tl-ptnn-xsbc-1-tr1", "", "tra_loi_ngan",
     r"Trên giá sách có $4$ quyển sách thuộc thể loại Văn học, $3$ quyển sách thuộc thể loại Lịch sử, $2$ quyển sách "
     r"thuộc thể loại Khoa học viễn tưởng. Bạn Minh Anh rút ngẫu nhiên một quyển." + ng("tlmt")
     + BR + r"[NB] Có bao nhiêu kết quả có thể xảy ra?",
     "4 + 3 + 2 = 9 kết quả (mỗi quyển sách là một kết quả). 1–2 dòng."),
    ("Bài 10.", "practice1", "onclass", "NB3", 1, "v10-nguyen-tat-thanh-2025-cau3 (ý a, c)", "", "dung_sai",
     r"Gieo đồng thời hai con xúc xắc cân đối, đồng chất loại $6$ mặt. Gieo xong ghi lại số chấm xuất hiện ở mặt trên "
     r"của hai con xúc xắc." + ng("ntt")
     + BR + y(DS, r"a) [NB] Số phần tử của không gian mẫu là $12$.",
              r"b) [NB] Biến cố $B$: " + q(r"Tổng số chấm xuất hiện trên hai con xúc xắc bằng $13$")
              + r" là biến cố không thể."),
     "Ý c) của đề gốc đổi nhãn thành b). a) Sai: mỗi con có 6 kết quả, không gian mẫu có 6·6 = 36 phần tử. "
     "b) Đúng: tổng lớn nhất là 6 + 6 = 12 < 13. Mỗi ý một dòng."),

    ("Mạch 4. Tính xác suất của biến cố", "practice1", "heading"),
    ("Bài 11.", "practice1", "onclass", "NB4", 1, "v10-thai-thinh-2025-I2-md2", "", "tra_loi_ngan",
     r"Trong trò chơi bốc thăm chọn số, người ta đã chuẩn bị một hộp đựng, trong đó có $10$ mảnh giấy giống nhau được "
     r"đánh số từ $1$ đến $10$. Xét phép thử " + q("Bốc ra một tờ giấy từ trong hộp") + " và biến cố $M$: "
     + q(r"Bốc được tờ giấy có ghi số chia hết cho $4$") + "." + ng("tt15")
     + BR + r"[NB] Tính xác suất của biến cố $M$.",
     "n(Ω) = 10, kết quả thuận lợi 4, 8 ⇒ P(M) = 2/10 = 1/5. 2 dòng, không cần Vậy."),
    ("Bài 12.", "practice1", "onclass", "NB4", 1, "v10-tho-loc-l5-2025-I2 (ý a)", "", "tra_loi_ngan",
     r"Trong hộp có chứa $2\,025$ viên bi màu có cùng kích thước và khối lượng (mỗi viên bi chỉ có đúng $1$ màu), trong "
     r"đó có $800$ viên bi màu đỏ, $700$ viên bi màu xanh, $508$ viên bi màu tím và $17$ viên bi còn lại là các viên bi "
     r"màu vàng hoặc màu trắng (mỗi màu có ít nhất $1$ viên). Lấy ngẫu nhiên một viên bi trong hộp." + ng("tll5")
     + BR + r"[NB] Tính xác suất để lấy được viên bi màu đỏ.",
     "Thêm giả thiết 'cùng kích thước và khối lượng' (đồng khả năng). P = 800/2025 = 32/81. 2 dòng."),
    ("Bài 13.", "practice1", "onclass", "NB4", 1, "tl-ptnn-xsbc-68-tr14", "", "tra_loi_ngan",
     r"Phân xưởng H của nhà máy có $2$ kĩ sư, $25$ kĩ thuật viên và $7$ thợ học việc. Người ta chọn ngẫu nhiên một người "
     r"trong số này để phỏng vấn về chế độ đãi ngộ của nhà máy." + ng("tlmt")
     + BR + y(r"a) [NB] Tính xác suất của biến cố " + q("Chọn được một thợ học việc") + ".",
              r"b) [NB] Tính xác suất của biến cố " + q("Chọn được một kĩ sư hoặc kĩ thuật viên") + "."),
     "n(Ω) = 2 + 25 + 7 = 34. a) 7/34. b) 2 + 25 = 27 ⇒ 27/34. Mỗi ý 1–2 dòng."),

    # ───────────── LUYỆN TẬP 2 — THÔNG HIỂU (như đi thi, không câu dẫn, không gợi ý) ─────────────
    ("Mạch 5. Lập bảng tần số tương đối, bảng tần số ghép nhóm", "practice2", "heading"),
    ("Ví dụ 1.", "practice2", "", "", 0, "sgk-7.11", "", "vi_du",
     r"Bảng thống kê sau cho biết số lượng học sinh của lớp 9B theo mức độ cận thị." + sgk("Bài tập 7{.}11")
     + B(("Mức độ", "Không cận thị", "Cận thị nhẹ", "Cận thị vừa", "Cận thị nặng"), ("Số học sinh", 10, 13, 12, 5))
     + y(r"a) Lập bảng tần số tương đối cho bảng thống kê trên.",
         r"b) Đa số học sinh của lớp 9B cận thị hay không cận thị?"),
     "a) Cỡ mẫu n = 10+13+12+5 = 40 · f lần lượt 10/40 = 25%, 13/40 = 32,5%, 12/40 = 30%, 5/40 = 12,5% · bảng tần số "
     "tương đối (dòng Mức độ / Tần số tương đối). b) Tỉ lệ học sinh cận thị: 32,5% + 30% + 12,5% = 75% > 50% · Vậy đa "
     "số học sinh lớp 9B cận thị. 6–7 ô (n, các f trong bảng, 75%, kết luận)."),
    ("Bài 14.", "practice2", "onclass", "TH1", 2, "ck2-chu-van-an-dn-2025-4 (ý a)", "", "tu_luan",
     r"Một cuộc điều tra về thời gian dùng mạng Internet trong ngày của học sinh lớp 9A tại một trường THCS cho kết quả "
     r"như sau." + ng("cvadn")
     + B(("Thời gian (giờ)", r"$[0{,}5; 1)$", r"$[1; 1{,}5)$", r"$[1{,}5; 2)$", r"$[2; 2{,}5]$"),
         ("Số học sinh", 15, 10, 8, 7))
     + r"[TH] Lập bảng tần số tương đối ghép nhóm từ bảng tần số.",
     "Cỡ mẫu n = 15+10+8+7 = 40 · f = 37,5%, 25%, 20%, 17,5% (viết từng phép tính) · bảng · Vậy."),
    ("Ví dụ 2.", "practice2", "", "", 0, "ck2-thai-thinh-2025-I1", "", "vi_du",
     r"Chiều cao (đơn vị: cm) của $30$ học sinh lớp 4 của một trường tiểu học là:" + ng("ttc")
     + L(CAO_TT, 10)
     + y(r"a) Hãy ghép các số liệu trên thành năm nhóm sau: $[70; 80)$, $[80; 90)$, $[90; 100)$, $[100; 110)$, "
         r"$[110; 120)$. Lập bảng tần số ghép nhóm.",
         r"b) Tìm tần số tương đối của nhóm $[90; 100)$."),
     "a) Đếm từng nhóm: [70; 80): 73, 78, 75 → 3 · [80; 90): 88, 81, 83, 87, 82, 86 → 6 · [90; 100): 90, 93, 95, 95, 97, "
     "96, 92, 95, 90, 90, 97, 96 → 12 · [100; 110): 101, 104, 101, 103, 109 → 5 · [110; 120): 111, 117, 110, 112 → 4 · "
     "tổng 30 · bảng tần số ghép nhóm. b) f = 12/30 · 100% = 40% · Vậy. 6–7 ô (các tần số, tổng, 40%)."),
    ("Bài 15.", "practice2", "onclass", "TH1", 2, "gk2-phuc-dong-2024-II", "", "tu_luan",
     r"Đo chiều cao (đơn vị: cm) của học sinh lớp 9/1 cho kết quả như sau:" + ng("pdg24")
     + L(CAO_PD, 10)
     + r"[TH] Lập bảng tần số ghép nhóm và bảng tần số tương đối ghép nhóm cho mẫu số liệu này với các nhóm "
       r"$[155; 158)$, $[158; 161)$, $[161; 164)$, $[164; 167)$.",
     "Cỡ mẫu 40 · tần số 4, 10, 17, 9 · f = 10%, 25%, 42,5%, 22,5% · một bảng gộp hai dòng tần số, tần số tương đối · "
     "Vậy."),

    ("Mạch 6. Đọc bảng, kiểm tra một nhận định", "practice2", "heading"),
    ("Ví dụ 3.", "practice2", "", "", 0, "gk2-phuc-loi-2024-1 (ý 1, 3)", "", "vi_du",
     r"Đánh giá kết quả học tập trong Học kì I của học sinh lớp 8A ở một trường trung học cơ sở được thống kê trong "
     r"bảng dưới đây." + ng("pl24")
     + B(("Mức", "Tốt", "Khá", "Đạt", "Chưa đạt"), ("Số học sinh", 16, 11, 10, 3))
     + y(r"a) Lập bảng tần số tương đối của mẫu số liệu thống kê trên.",
         r"b) Trong buổi sơ kết cuối Học kì I, giáo viên chủ nhiệm lớp 8A thông báo: Tỉ lệ học sinh đạt kết quả học tập "
         r"Học kì I được đánh giá ở mức Tốt và Khá so với cả lớp là trên $67\%$. Thông báo đó của giáo viên chủ nhiệm có "
         r"đúng không?"),
     "Bỏ ý 2) vẽ biểu đồ hình quạt của đề gốc (lớp 9C không dạy vẽ), ý 3) đổi nhãn thành b). a) n = 16+11+10+3 = 40 · "
     "f = 40%, 27,5%, 25%, 7,5% · bảng. b) Tốt và Khá: 40% + 27,5% = 67,5% > 67% · Vậy thông báo đúng. 6 ô."),
    ("Bài 16.", "practice2", "onclass", "TH2", 2, "tl-tanso-23-tr9 (ý b, c)", "", "tu_luan",
     r"Kiểm tra khối lượng một số hộp sữa chua được lấy ngẫu nhiên từ thành phẩm của máy đóng hộp X, nhà máy chế biến "
     r"sữa thu được bảng sau." + ng("tlts")
     + B(("Khối lượng (g)", 92, 96, 100, 105, 110), ("Tần số", 7, 18, 38, 9, 8))
     + y(r"a) [TH] Những hộp cân nặng từ $95$ g đến $105$ g được xem là đạt yêu cầu về khối lượng. Trong $80$ hộp sữa chua "
         r"được kiểm tra có bao nhiêu phần trăm hộp đạt yêu cầu?",
         r"b) [TH] Máy đóng hộp được xem là vận hành tốt nếu trên $90\%$ sản phẩm có chất lượng đạt yêu cầu. Nếu $80$ hộp "
         r"sữa chua này đại diện được cho sản phẩm đóng hộp của máy X thì có thể xem là máy này vận hành tốt hay không?"),
     "Bỏ ý a) của đề gốc (lập bảng tần số tương đối + vẽ quạt), ý b), c) đổi nhãn a), b). a) Đạt yêu cầu: 96 g, 100 g, "
     "105 g ⇒ 18+38+9 = 65 hộp · 65/80 · 100% = 81,25% · Vậy. b) Theo câu a), 81,25% < 90% · Vậy máy không được xem là "
     "vận hành tốt."),

    ("Mạch 7. Xác suất của biến cố trong phép thử một hành động", "practice2", "heading"),
    ("Ví dụ 4.", "practice2", "", "", 0, "ck2-le-hong-phong-2025-I2", "", "vi_du",
     r"Hình bên mô tả một đĩa tròn bằng bìa cứng được chia làm tám phần bằng nhau và ghi các số $1, 2, 3, \ldots, 8$. "
     r"Chiếc kim được gắn cố định vào trục quay ở tâm của đĩa. Xét phép thử " + q("Quay đĩa tròn một lần") + "."
     + DQ(list(range(1, 9)), rong=0.24)
     + r"Tính xác suất của biến cố $A$: " + q("Chiếc kim chỉ vào hình quạt ghi số không phải là số nguyên tố")
     + "." + ng("lhp"),
     "Ω = {1; 2; …; 8}, n(Ω) = 8, đồng khả năng · số nguyên tố 2, 3, 5, 7 ⇒ thuận lợi cho A: 1, 4, 6, 8 (nhắc 1 không "
     "phải số nguyên tố) · n(A) = 4 · P(A) = 4/8 = 1/2 · Vậy. 5–6 ô."),
    ("Bài 17.", "practice2", "onclass", "TH4", 2, "ck2-chu-van-an-2024-I2", "", "tu_luan",
     r"Một hộp có $20$ viên bi với kích thước và khối lượng như nhau. Bạn Nga viết lên các viên bi đó các số "
     r"$1, 2, 3, \ldots, 20$, hai viên bi khác nhau thì viết hai số khác nhau. Xét phép thử "
     + q("Lấy ngẫu nhiên một viên bi trong hộp") + "." + ng("cva")
     + BR + r"[TH] Tính xác suất của biến cố $A$: " + q(r"Số xuất hiện trên viên bi được lấy ra chia $6$ dư $2$") + ".",
     "n(Ω) = 20, đồng khả năng · thuận lợi: 2, 8, 14, 20 (nhớ số 2 = 6·0 + 2) · n(A) = 4 · P(A) = 4/20 = 1/5 · Vậy."),
    ("Ví dụ 5.", "practice2", "", "", 0, "tl-ptnn-xsbc-32-tr8", "", "vi_du",
     r"Viết ngẫu nhiên một số tự nhiên lẻ có hai chữ số." + ng("tlmt")
     + BR + y(r"a) Tìm số phần tử của tập hợp $\Omega$ gồm các kết quả có thể xảy ra đối với số tự nhiên được viết ra.",
              r"b) Tính xác suất của biến cố $E$: " + q(r"Số tự nhiên được viết ra là bội của $9$") + "."),
     "a) Ω = {11; 13; 15; …; 99} · đếm (99 − 11) : 2 + 1 = 45 · n(Ω) = 45. b) Các bội của 9 có hai chữ số: 18, 27, 36, "
     "45, 54, 63, 72, 81, 90, 99 — chọn số lẻ: 27, 45, 63, 81, 99 ⇒ n(E) = 5 · P(E) = 5/45 = 1/9 · Vậy. 6 ô."),
    ("Bài 18.", "practice2", "onclass", "NB3+TH4", 2, "tl-ptnn-xsbc-50-tr12", "", "tu_luan",
     r"Viết ngẫu nhiên một số tự nhiên lớn hơn $499$ và nhỏ hơn $1\,000$." + ng("tlmt")
     + BR + y(r"a) [NB] Có tất cả bao nhiêu kết quả có thể xảy ra trong phép thử trên?",
              r"b) [TH] Tính xác suất của mỗi biến cố sau:",
              le(r"$A$: " + q(r"Số tự nhiên viết ra chia hết cho $100$") + ",",
                 r"$B$: " + q(r"Số tự nhiên viết ra là lập phương của một số tự nhiên") + ".")),
     "a) Ω = {500; 501; …; 999}, 999 − 500 + 1 = 500 kết quả. b) A: 500, 600, 700, 800, 900 ⇒ P(A) = 5/500 = 1/100 · "
     "B: 8³ = 512, 9³ = 729 (7³ = 343 < 500, 10³ = 1000 không nhỏ hơn 1000) ⇒ P(B) = 2/500 = 1/250 · Vậy."),
    ("Ví dụ 6.", "practice2", "", "", 0, "tl-ptnn-xsbc-41-tr10 (ý a, c)", "", "vi_du",
     r"Biểu đồ cột kép sau thống kê số học sinh tham gia câu lạc bộ cờ vua. Lấy ngẫu nhiên một học sinh trong số này. "
     r"Tính xác suất của các biến cố:" + ng("tlmt")
     + K(["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], [3, 8, 6, 9], [4, 5, 4, 7], ("Nam", "Nữ"), "Lớp", "Số học sinh", 10, 5)
     + y(r"a) Lấy được một học sinh nữ lớp 9.", r"b) Lấy được một học sinh nam lớp 7 hoặc lớp 8."),
     "Ý c) của đề gốc đổi nhãn b). Tổng số học sinh: nam 3+8+6+9 = 26, nữ 4+5+4+7 = 20, cộng 46 = n(Ω), đồng khả "
     "năng. a) nữ lớp 9: 7 ⇒ 7/46. b) nam lớp 7 hoặc 8: 8 + 6 = 14 ⇒ 14/46 = 7/23 · Vậy. 6 ô."),
    ("Bài 19.", "practice2", "onclass", "TH5", 2, "tl-ptnn-xsbc-42-tr10 (A, C)", "", "tu_luan",
     r"Biểu đồ cột kép sau biểu diễn số lượng học sinh tham gia giải thi đấu thể thao của một trường trung học cơ sở. "
     r"Chọn ngẫu nhiên một học sinh tham gia giải thi đấu thể thao của trường đó." + ng("tlmt")
     + K(["Khối 6", "Khối 7", "Khối 8", "Khối 9"], [7, 9, 9, 9], [9, 7, 8, 8], ("Nam", "Nữ"), "Khối",
         "Số học sinh", 10, 5)
     + r"[TH] Tính xác suất của mỗi biến cố sau:"
     + BR + le(r"$A$: " + q("Học sinh được chọn là nam") + ",",
               r"$B$: " + q(r"Học sinh được chọn là nữ và không thuộc khối $9$") + "."),
     "Biến cố C của đề gốc đổi tên thành B. n(Ω) = (7+9+9+9) + (9+7+8+8) = 34 + 32 = 66 · P(A) = 34/66 = 17/33 · "
     "nữ không thuộc khối 9: 9 + 7 + 8 = 24 ⇒ P(B) = 24/66 = 4/11 · Vậy."),

    ("Mạch 8. Xác suất của biến cố trong phép thử hai hành động", "practice2", "heading"),
    ("Ví dụ 7.", "practice2", "", "", 0, "sgk-ltc8-vd1 (ý b, c-E, c-G)", "", "vi_du",
     r"Tấm bìa cứng $A$ hình tròn được chia thành $3$ hình quạt có diện tích bằng nhau, đánh số $1, 2, 3$ và tấm bìa "
     r"cứng $B$ hình tròn được chia thành $5$ hình quạt có diện tích bằng nhau, đánh số $1, 2, 3, 4, 5$. Trục quay của "
     r"$A$ và $B$ được gắn mũi tên ở tâm. Bạn Nam quay tấm bìa $A$, bạn Bình quay tấm bìa $B$. Quan sát xem mũi tên "
     r"dừng ở hình quạt nào trên hai tấm bìa." + sgk("Luyện tập chung, Ví dụ")
     + P2(DQ([1, 2, 3], ten="Tấm bìa A"), DQ([1, 2, 3, 4, 5], ten="Tấm bìa B"), rong=0.24)
     + y(r"a) Mô tả không gian mẫu của phép thử.",
         r"b) Tính xác suất của các biến cố $E$: " + q(r"Tích hai số ở hình quạt mà hai mũi tên chỉ vào bằng $6$")
         + r" và $G$: " + q(r"Tích hai số ở hình quạt mà hai mũi tên chỉ vào là số chẵn") + "."),
     "Bỏ ý a) phép thử, biến cố F của SGK. a) Kết quả là cặp (a, b), a là số trên tấm bìa A, b là số trên tấm bìa B · "
     "bảng 3 × 5 [[bang: …]] · n(Ω) = 15, đồng khả năng. b) E: (2, 3), (3, 2) ⇒ P(E) = 2/15 · G: a = 2 (5 cặp), a = 1 hoặc "
     "3 với b = 2, 4 (4 cặp) ⇒ 9 cặp ⇒ P(G) = 9/15 = 3/5 · Vậy. 6–7 ô (có thể khoét trong bảng)."),
    ("Bài 20.", "practice2", "onclass", "TH6", 2, "sgk-8.16 (E, G)", "", "tu_luan",
     XX + r" Tính xác suất của các biến cố sau:" + sgk("Bài tập 8{.}16")
     + BR + le(r"$E$: " + q(r"Tổng số chấm xuất hiện trên hai con xúc xắc bằng $11$") + ",",
               r"$F$: " + q(r"Tổng số chấm xuất hiện trên hai con xúc xắc nhỏ hơn $6$") + ".")
     + BR + r"[TH] Tính xác suất của các biến cố $E$ và $F$.",
     "Biến cố G của SGK đổi tên thành F (bỏ biến cố F gốc). n(Ω) = 36 (bảng 6 × 6 hoặc lập luận 6·6) · E: (5, 6), (6, 5) "
     "⇒ 2/36 = 1/18 · F: tổng 2, 3, 4, 5: (1, 1), (1, 2), (2, 1), (1, 3), (2, 2), (3, 1), (1, 4), (2, 3), (3, 2), (4, 1) "
     "⇒ 10/36 = 5/18 · Vậy."),
    ("Bài 21.", "practice2", "onclass", "NB2+TH4", 2, "ck2-be-van-dan-2025-I1 + I2 (ĐÍCH)", "", "tu_luan",
     r"\textit{(Câu I, " + N["bvd"] + r")}"
     + BR + r"1) Sau khi điều tra cân nặng của $40$ học sinh lớp 9A, người ta có biểu đồ tần số ghép nhóm dưới đây."
     + C([30, 40, 50, 60, 70], [2, 20, 14, 4], "Cân nặng (kg)", r"Tần số ($n$)", 20, 5, sat=True)
     + y(r"a) [NB] Tìm tần số ghép nhóm của nhóm $[30; 40)$.",
         r"b) [NB] Tìm tần số tương đối ghép nhóm của nhóm $[40; 50)$.",
         r"2) Một hộp có $24$ thẻ cùng loại, mỗi thẻ ghi một trong các số $1, 2, 3, \ldots, 24$. Hai thẻ khác nhau thì "
         r"ghi số khác nhau. Rút ngẫu nhiên $1$ thẻ trong hộp.",
         r"[TH] Tính xác suất của biến cố " + q("Số ghi trên thẻ là số chính phương") + "."),
     "ĐÍCH (làm như đi thi). 1a) 2. 1b) f = 20/40 · 100% = 50%. 2) n(Ω) = 24, đồng khả năng · số chính phương 1, 4, 9, 16 "
     "(25 > 24) · n = 4 · P = 4/24 = 1/6 · Vậy."),

    # ───────────── BÀI TẬP VỀ NHÀ (22 NB + 10 TH) ─────────────
    ("Bài 22.", "reflection", "btvn", "NB2", 1, "gk2-nhat-tan-2025-I1", "", "tra_loi_ngan",
     r"Độ dài một cú nhảy ba bước (đơn vị: mét) của $50$ học sinh lớp 9A1 của một trường THCS được ghi lại ở bảng tần "
     r"số ghép nhóm sau." + ng("nhtan25")
     + B(("Độ dài (mét)", r"$[6; 7)$", r"$[7; 8)$", r"$[8; 9)$", r"$[9; 10)$", r"$[10; 11)$"),
         ("Tần số", 23, 10, 9, 6, 2))
     + y(r"a) [NB] Tìm tần số ghép nhóm của nhóm $[9; 10)$.",
         r"b) [NB] Tìm tần số tương đối ghép nhóm của nhóm $[9; 10)$."),
     "a) 6. b) 6/50 · 100% = 12%."),
    ("Bài 23.", "reflection", "btvn", "NB2", 1, "ck2-nghia-tan-2025-I1", "", "tra_loi_ngan",
     r"Sau khi điều tra cân nặng (tính theo kg) của các học sinh trong một lớp, người ta thu được biểu đồ tần số ghép "
     r"nhóm sau." + ng("ntanc")
     + C([35, 40, 45, 50, 55, 60, 65, 70], [3, 5, 9, 15, 10, 5, 3], "Cân nặng (kg)", r"Tần số ($n$)", 16, 4, sat=True)
     + y(r"a) [NB] Xác định tần số của nhóm $[50; 55)$.", r"b) [NB] Xác định tần số tương đối của nhóm $[50; 55)$."),
     "a) 15. b) Cỡ mẫu 3+5+9+15+10+5+3 = 50 · f = 15/50 · 100% = 30%."),
    ("Bài 24.", "reflection", "btvn", "NB2", 1, "gk2-nghia-tan-2025-I1", "", "tra_loi_ngan",
     r"Độ dài một cú nhảy ba bước (đơn vị: mét) của $40$ vận động viên trong lúc tập luyện được ghi lại ở bảng tần số "
     r"ghép nhóm sau." + ng("ntan25")
     + B(("Độ dài (mét)", r"$[10; 11)$", r"$[11; 12)$", r"$[12; 13)$", r"$[13; 14)$", r"$[14; 15)$"),
         ("Tần số", 18, 10, 6, 4, 2))
     + y(r"a) [NB] Xác định tần số của nhóm $[13; 14)$.", r"b) [NB] Xác định tần số tương đối của nhóm $[13; 14)$."),
     "a) 4. b) Cỡ mẫu 18+10+6+4+2 = 40 · f = 4/40 · 100% = 10%."),
    ("Bài 25.", "reflection", "btvn", "NB1", 1, "v10-nguyen-tat-thanh-2025-cau4", "", "tra_loi_ngan",
     r"Bảng sau cho biết trữ lượng đất hiếm (đơn vị: triệu tấn) của các quốc gia trên thế giới (nguồn: Cục Khảo sát "
     r"địa chất Mỹ công bố năm 2022)." + ng("ntt")
     + B(("Quốc gia", "Trung Quốc", "Việt Nam", "Brazil", "Nga", "Các quốc gia còn lại"),
         ("Trữ lượng (triệu tấn)", 44, 22, 21, 21, 12))
     + r"[NB] Tính tỉ số phần trăm trữ lượng đất hiếm của Việt Nam so với tổng trữ lượng đất hiếm của toàn thế giới "
       r"(kết quả làm tròn đến chữ số thập phân thứ nhất).",
     "Tổng 44+22+21+21+12 = 120 · 22/120 · 100% ≈ 18,3%."),
    ("Bài 26.", "reflection", "btvn", "NB2", 1, "ck2-phuc-loi-2024-1-1", "", "tra_loi_ngan",
     r"Một ngân hàng thống kê số tiền (đơn vị: triệu đồng) mà $80$ hộ gia đình vay để phát triển sản xuất. Số liệu được "
     r"ghi lại trong biểu đồ tần số ghép nhóm ở hình dưới đây." + ng("pl1")
     + C([40, 50, 60, 70, 80, 90, 100], [10, 15, 17, 25, 8, 5], "Số tiền (triệu đồng)", r"Tần số ($n$)", 25, 5,
         sat=True)
     + r"[NB] Lập bảng tần số ghép nhóm của mẫu số liệu được ghép nhóm đó.",
     "Bảng [[bang: Số tiền (triệu đồng) | $[40; 50)$ | $[50; 60)$ | $[60; 70)$ | $[70; 80)$ | $[80; 90)$ | $[90; 100)$ "
     "/ Tần số | $10$ | $15$ | $17$ | $25$ | $8$ | $5$]] (cộng 80)."),
    ("Bài 27.", "reflection", "btvn", "NB1", 1, "sgk-7.13", "", "tra_loi_ngan",
     r"Bạn Hoàng khảo sát ý kiến của các bạn trong tổ về chất lượng phục vụ của căng tin trường thu được kết quả sau:"
     + BR + r"\hspace*{1.4em}A, B, C, B, A, A, B, A, B, A,"
     + BR + r"trong đó A là mức Tốt, B là mức Trung bình, C là mức Kém." + sgk("Bài tập 7{.}13")
     + BR + y(r"a) [NB] Lập bảng tần số biểu diễn kết quả bạn Hoàng thu được.",
              r"b) [NB] Lập bảng tần số tương đối biểu diễn kết quả bạn Hoàng thu được."),
     "a) A: 5, B: 4, C: 1 (cỡ mẫu 10) · bảng. b) 50%, 40%, 10% · bảng."),
    ("Bài 28.", "reflection", "btvn", "NB1", 1, "sgk-b23-lt1 (ý a)", "", "tra_loi_ngan",
     r"Quay $50$ lần một tấm bìa hình tròn được chia thành ba hình quạt với các màu xanh, đỏ, vàng. Quan sát và ghi lại "
     r"mũi tên chỉ vào hình quạt có màu nào khi tấm bìa dừng lại. Kết quả thu được: màu xanh $15$ lần, màu đỏ $25$ lần, "
     r"màu vàng $10$ lần." + sgk("Bài 23, Luyện tập 1")
     + BR + r"[NB] Lập bảng tần số tương đối cho kết quả thu được.",
     "f: xanh 15/50 = 30%, đỏ 25/50 = 50%, vàng 10/50 = 20% · bảng."),
    ("Bài 29.", "reflection", "btvn", "NB1", 1, "tl-tanso-6-tr4 (ý a, b)", "", "tra_loi_ngan",
     r"Một địa phương cho trẻ em từ $12$ tháng tuổi trở lên tiêm vắc xin viêm não Nhật Bản. Bảng sau thống kê số mũi "
     r"vắc xin viêm não Nhật Bản mà $50$ trẻ em từ $12$ đến $24$ tháng tuổi tại địa phương này đã tiêm." + ng("tlts")
     + B(("Số mũi tiêm", 0, 1, 2, 3), ("Số trẻ", 7, "?", 26, 14))
     + y(r"a) [NB] Tìm số trẻ đã tiêm $1$ mũi.",
         r"b) [NB] Trẻ từ $12$ đến $24$ tháng tuổi cần hoàn thành $3$ mũi tiêm vắc xin viêm não Nhật Bản. Hỏi trong số "
         r"trẻ được thống kê ở trên, có bao nhiêu trẻ cần phải hoàn thành lộ trình tiêm vắc xin này?"),
     "Ý a) đề gốc 'Hoàn thành bảng tần số' đổi lời (không khung điền). a) 50 − (7 + 26 + 14) = 3. b) chưa đủ 3 mũi: "
     "7 + 3 + 26 = 36 trẻ (hoặc 50 − 14 = 36)."),
    ("Bài 30.", "reflection", "btvn", "NB5", 1, "tl-motabd-15-tr6 (ý a)", "", "tra_loi_ngan",
     r"Ban tổ chức thông báo bán vé trên mạng cho buổi biểu diễn của một nhóm ngôi sao ca nhạc. Biểu đồ sau biểu diễn "
     r"số lượng vé bán ra trong $5$ phút đầu tiên (theo từng phút) kể từ khi bắt đầu bán." + ng("tlbd")
     + D(["Phút 1", "Phút 2", "Phút 3", "Phút 4", "Phút 5"], [90, 75, 140, 100, 120], "Thời điểm", "Số vé", 150, 25,
         tieu_de="Bán vé trực tuyến")
     + r"[NB] Số vé bán được nhiều nhất, ít nhất vào thời điểm nào?",
     "Nhiều nhất phút thứ 3 (140 vé), ít nhất phút thứ 2 (75 vé). 1–2 dòng."),
    ("Bài 31.", "reflection", "btvn", "NB3+NB4", 1, "gk2-phuc-loi-2024-3", "", "tra_loi_ngan",
     r"Xét phép thử " + q("Gieo một con xúc xắc cân đối, đồng chất một lần") + "." + ng("pl24")
     + BR + y(r"a) [NB] Viết không gian mẫu của phép thử đó.",
              r"b) [NB] Tính xác suất của biến cố " + q("Mặt xuất hiện của xúc xắc có số chấm là số nguyên tố") + "."),
     "Thêm 'cân đối, đồng chất'. Ý 1), 2) đổi nhãn a), b). a) Ω = {1; 2; 3; 4; 5; 6}. b) 2, 3, 5 ⇒ 3/6 = 1/2."),
    ("Bài 32.", "reflection", "btvn", "NB4", 1, "v10-tho-loc-l2-2025-I2 (ý a, b)", "", "tra_loi_ngan",
     r"Trong hộp gỗ có $6$ thẻ gỗ cùng loại, được đánh số tương ứng $12, 13, 14, 15, 16, 17$. Bình rút ngẫu nhiên một "
     r"thẻ. Tính xác suất của các biến cố:" + ng("tll2")
     + BR + y(r"a) [NB] $A$: " + q(r"Thẻ rút được có số ghi trên thẻ là ước của $24$") + ".",
              r"b) [NB] $B$: " + q(r"Thẻ rút được có số ghi trên thẻ chia cho $3$ dư $2$") + "."),
     "Bỏ câu hỏi 'lặp lại 120 lần' của đề gốc (ước lượng — ngoài lớp 9C). a) 12 ⇒ 1/6. b) 14, 17 ⇒ 2/6 = 1/3."),
    ("Bài 33.", "reflection", "btvn", "TH1", 2, "sgk-7.7", "", "tu_luan",
     r"Biểu đồ tranh sau đây biểu diễn số lượng học sinh lớp 9B bình chọn phần mềm học trực tuyến được yêu thích nhất."
     + sgk("Bài tập 7{.}7")
     + T(["Skype", "Zoom", "Google Meet"], [3, 11, 6], r"Mỗi biểu tượng biểu diễn $2$ học sinh")
     + r"[TH] Lập bảng tần số tương đối cho dữ liệu được biểu diễn trong biểu đồ tranh trên.",
     "Số học sinh: Skype 3·2 = 6, Zoom 11·2 = 22, Google Meet 6·2 = 12, cỡ mẫu 40 · f = 15%, 55%, 30% · bảng · Vậy."),
    ("Bài 34.", "reflection", "btvn", "NB1+TH1", 2, "gk2-trung-vuong-2024-I1", "", "tu_luan",
     r"Trong bài " + q("Tiếng Việt") + r" của cố nhà văn, nhà soạn kịch kiêm nhà thơ Lưu Quang Vũ, có khổ thơ sau:"
     + BR + r"\hspace*{1.4em}\textit{Trái đất rộng giàu sang bao thứ tiếng}"
     + BR + r"\hspace*{1.4em}\textit{Cao quý thâm trầm rực rỡ vui tươi}"
     + BR + r"\hspace*{1.4em}\textit{Tiếng Việt rung rinh nhịp đập trái tim người}"
     + BR + r"\hspace*{1.4em}\textit{Như tiếng sáo như dây đàn máu nhỏ.}"
     + BR + r"Số lần xuất hiện của mỗi loại dấu (thanh) được ghi lại trong biểu đồ tần số dưới đây." + ng("tvg24")
     + C(TO_HUU[0], TO_HUU[1], "Dấu (thanh)", r"Tần số ($n$)", 14, 4)
     + y(r"a) [NB] Tìm tần số của dấu sắc trong khổ thơ.",
         r"b) [TH] Tần số tương đối của dấu nặng bằng bao nhiêu phần trăm (làm tròn kết quả đến hàng đơn vị)?"),
     "a) 10. b) Cỡ mẫu 12+10+4+1+1+5 = 33 · f = 5/33 · 100% ≈ 15% · Vậy. (Đã đếm lại khổ thơ: khớp biểu đồ.)"),
    ("Bài 35.", "reflection", "btvn", "NB2+TH1", 2, "tl-tsgn-8-tr4", "", "tu_luan",
     r"Trong $1$ giờ, cửa hàng xăng dầu ghi lại số lít xăng mà mỗi khách hàng mua:" + ng("tlgn")
     + L([XANG[i] for i in range(27)], 9)
     + y(r"a) [TH] Hãy lập bảng tần số ghép nhóm gồm $4$ nhóm $[0; 10)$, $[10; 20)$, $[20; 30)$, $[30; 40)$.",
         r"b) [NB] Dựa vào bảng đã lập, cho biết có bao nhiêu khách hàng mua dưới $10$ lít xăng.",
         r"c) [NB] Dựa vào bảng đã lập, cho biết nhóm khách hàng đông nhất là nhóm mua bao nhiêu lít xăng."),
     "Ý b) hai gạch đầu dòng của đề gốc tách thành b), c). a) [0; 10): 4, 5, 5, 6, 7, 8 → 6 · [10; 20): 10 · [20; 30): 4 · "
     "[30; 40): 7 · cộng 27 · bảng · Vậy. b) Theo câu a), 6 khách hàng. c) nhóm [10; 20) (10 khách hàng)."),
    ("Bài 36.", "reflection", "btvn", "TH3", 2, "sgk-7.17 (ý b)", "", "tu_luan",
     r"Một cuộc điều tra về thời gian dùng mạng Internet trong ngày của học sinh lớp 9 tại một thành phố cho kết quả như "
     r"sau." + sgk("Bài tập 7{.}17")
     + B(("Thời gian (giờ)", r"$[0; 0{,}5)$", r"$[0{,}5; 1{,}0)$", r"$[1{,}0; 1{,}5)$", r"$[1{,}5; 2{,}0)$",
          r"$[2{,}0; 2{,}5)$"), ("Tỉ lệ", r"$15\%$", r"$27\%$", r"$23\%$", r"$18\%$", r"$17\%$"))
     + r"[TH] Để thu được bảng thống kê trên, người ta đã lập phiếu điều tra và thu về tổng cộng $2\,000$ phiếu trả "
       r"lời. Lập bảng tần số ghép nhóm cho kết quả thu được.",
     "Tần số = tỉ lệ · 2000: 300, 540, 460, 360, 340 (cộng 2000) · bảng · Vậy."),
    ("Bài 37.", "reflection", "btvn", "TH1", 2, "gk2-phuc-dong-2024-II-md2", "", "tu_luan",
     r"Cô Loan ghi lại chiều cao (đơn vị: cm) của các cây bạch đàn giống vừa được chuyển đến nông trường ở bảng sau." + ng("pdg24")
     + L(BACH_DAN, 10)
     + r"[TH] Hãy chia dữ liệu trên thành $5$ nhóm $[15; 18)$, $[18; 21)$, $[21; 24)$, $[24; 27)$, $[27; 30)$ và lập bảng "
       r"tần số tương đối ghép nhóm tương ứng.",
     "Cỡ mẫu 40 · tần số 8, 9, 11, 3, 9 · f = 20%, 22,5%, 27,5%, 7,5%, 22,5% · bảng · Vậy."),
    ("Bài 38.", "reflection", "btvn", "NB4+TH4", 2, "gk2-ban-mai-2025-7a", "", "tu_luan",
     r"Một hộp có $60$ chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, \ldots, 60$, hai thẻ khác nhau "
     r"thì ghi hai số khác nhau. Rút ngẫu nhiên một thẻ trong hộp. Tính xác suất của mỗi biến cố sau:" + ng("bm")
     + BR + y(r"a) [NB] " + q(r"Số xuất hiện trên thẻ được rút ra là số nhỏ hơn $31$") + ".",
              r"b) [TH] " + q(r"Số xuất hiện trên thẻ được rút ra là số chia cho $8$ dư $5$") + "."),
     "n(Ω) = 60. a) 1, 2, …, 30 ⇒ 30/60 = 1/2. b) 5, 13, 21, 29, 37, 45, 53 ⇒ 7/60 · Vậy."),
    ("Bài 39.", "reflection", "btvn", "TH4", 2, "v10-thai-thinh-2026-I2", "", "tu_luan",
     r"Một hộp có $15$ chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, \ldots, 15$. Hai thẻ khác nhau "
     r"ghi hai số khác nhau. Rút ngẫu nhiên một thẻ trong hộp." + ng("tt26")
     + BR + r"[TH] Tính xác suất của biến cố $A$: " + q("Số xuất hiện trên thẻ được rút ra là số nguyên tố") + ".",
     "n(Ω) = 15 · 2, 3, 5, 7, 11, 13 ⇒ n(A) = 6 · P(A) = 6/15 = 2/5 · Vậy."),
    ("Bài 40.", "reflection", "btvn", "TH4", 2, "gk2-nhat-tan-2025-I2", "", "tu_luan",
     r"Một hộp có $20$ chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, \ldots, 20$, hai thẻ khác nhau "
     r"thì ghi hai số khác nhau. Xét phép thử " + q("Rút một thẻ trong chiếc hộp") + " và biến cố $A$: "
     + q(r"Số xuất hiện trên thẻ là số chia hết cho $3$") + "." + ng("nhtan25")
     + BR + r"[TH] Tính xác suất của biến cố $A$.",
     "n(Ω) = 20 · 3, 6, 9, 12, 15, 18 ⇒ 6/20 = 3/10 · Vậy."),
    ("Bài 41.", "reflection", "btvn", "TH4", 2, "tl-ptnn-xsbc-70-tr14", "", "tu_luan",
     r"Một hộp có chứa $10$ quả cầu màu đen được đánh số từ $1$ đến $10$ và $20$ quả cầu màu vàng được đánh số từ $11$ "
     r"đến $30$, các quả cầu có cùng kích thước và khối lượng. Lấy ngẫu nhiên một quả trong hộp." + ng("tlmt")
     + BR + r"[TH] Tính xác suất của mỗi biến cố sau:"
     + BR + le(r"$A$: " + q(r"Quả cầu được lấy ra có màu đen và ghi số chia cho $3$ dư $1$") + ",",
               r"$B$: " + q(r"Quả cầu được lấy ra có màu vàng hoặc ghi số lẻ lớn hơn $3$") + "."),
     "Thêm 'cùng kích thước và khối lượng'. n(Ω) = 30 · A: 1, 4, 7, 10 ⇒ 4/30 = 2/15 · B: 20 quả vàng (11 đến 30) và "
     "quả đen ghi số lẻ lớn hơn 3: 5, 7, 9 ⇒ 23 ⇒ 23/30 · Vậy."),
    ("Bài 42.", "reflection", "btvn", "TH6", 2, "sgk-8.12", "", "trac_nghiem",
     r"[TH] Gieo đồng thời hai con xúc xắc cân đối, đồng chất. Xác suất để "
     + q(r"Tổng số chấm xuất hiện trên hai con xúc xắc lớn hơn hoặc bằng $10$") + " là" + sgk("Bài tập 8{.}12")
     + tn(fr(7, 36), fr(2, 9), fr(1, 6), fr(5, 36)),
     "36 kết quả · tổng ≥ 10: (4, 6), (6, 4), (5, 5), (5, 6), (6, 5), (6, 6) ⇒ 6/36 = 1/6 · Chọn C."),
]

DAP_TN = {"Bài 42.": "C"}
DAP_DS = {"Bài 10.": "SĐ"}
OPTIONS: dict = {}
NGAN = {f"Bài {i}." for i in range(1, 14)} | {f"Bài {i}." for i in range(22, 33)}
DOI_NHAN_BTVN = {36: 31, 38: 32, 31: 33, 32: 34, 33: 35, 34: 36, 35: 37, 37: 38}   # 19/11 dễ→khó: NB lên trước

THE_MUC = {("NB", "onclass"): 24, ("TH", "onclass"): 9, ("NB", "btvn"): 22, ("TH", "btvn"): 10}


def nt(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def p(tu, mau):
    return F(len(tu) if not isinstance(tu, int) else tu, mau)


def kiem():
    loi = []

    def bang(ten, that, mong):
        if that != mong:
            loi.append(f"{ten}: máy {that} ≠ sơ đồ {mong}")

    r = range
    pc = lambda a, b: F(a * 100, b)  # noqa: E731  phần trăm
    bang("B1", (9, pc(9, 11 + 8 + 9 + 12)), (9, F(45, 2)))
    bang("B2", (sum([1, 2, 6, 5, 7, 8, 7, 4]), pc(7, 40)), (40, F(35, 2)))
    bang("B3", (33 + 60 + 189 + 168, pc(189, 450)), (450, 42))
    bang("B5", pc(20, 50), 40)
    bang("B6", (sum([17, 12, 10, 11]), pc(10, 50)), (50, 20))
    bang("B7", 10 + 20 + 40 + 30, 100)
    bang("B9", 4 + 3 + 2, 9)
    bang("B10", (6 * 6, max(a + b for a in r(1, 7) for b in r(1, 7)) < 13), (36, True))
    bang("B11", p([x for x in r(1, 11) if x % 4 == 0], 10), F(1, 5))
    bang("B12", (800 + 700 + 508 + 17, F(800, 2025)), (2025, F(32, 81)))
    bang("B13", (F(7, 34), F(27, 34)), (F(7, 34), F(27, 34)))
    bang("VD1", [pc(x, 40) for x in (10, 13, 12, 5)] + [pc(30, 40)], [25, F(65, 2), 30, F(25, 2), 75])
    bang("B14", [pc(x, 40) for x in (15, 10, 8, 7)], [F(75, 2), 25, 20, F(35, 2)])
    tt = [sum(a <= x < a + 10 for x in CAO_TT) for a in r(70, 120, 10)]
    bang("VD2", (len(CAO_TT), tt, pc(tt[2], 30)), (30, [3, 6, 12, 5, 4], 40))
    pd = [sum(a <= x < a + 3 for x in CAO_PD) for a in (155, 158, 161, 164)]
    bang("B15", (len(CAO_PD), pd, [pc(x, 40) for x in pd]), (40, [4, 10, 17, 9], [10, 25, F(85, 2), F(45, 2)]))
    bang("VD3", ([pc(x, 40) for x in (16, 11, 10, 3)], pc(27, 40) > 67), ([40, F(55, 2), 25, F(15, 2)], True))
    bang("B16", (7 + 18 + 38 + 9 + 8, pc(18 + 38 + 9, 80), pc(65, 80) > 90), (80, F(325, 4), False))
    bang("VD4", p([x for x in r(1, 9) if not nt(x)], 8), F(1, 2))
    bang("B17", p([x for x in r(1, 21) if x % 6 == 2], 20), F(1, 5))
    le_ = [x for x in r(10, 100) if x % 2]
    bang("VD5", (len(le_), p([x for x in le_ if x % 9 == 0], len(le_))), (45, F(1, 9)))
    s3 = list(r(500, 1000))
    bang("B18", (len(s3), p([x for x in s3 if x % 100 == 0], 500), p([x for x in s3 if round(x ** (1 / 3)) ** 3 == x], 500)),
         (500, F(1, 100), F(1, 250)))
    nam, nu = [3, 8, 6, 9], [4, 5, 4, 7]
    bang("VD6", (sum(nam + nu), F(nu[3], 46), F(nam[1] + nam[2], 46)), (46, F(7, 46), F(7, 23)))
    nam, nu = [7, 9, 9, 9], [9, 7, 8, 8]
    bang("B19", (sum(nam + nu), F(sum(nam), 66), F(sum(nu[:3]), 66)), (66, F(17, 33), F(4, 11)))
    AB = list(itertools.product(r(1, 4), r(1, 6)))
    bang("VD7", (len(AB), p([o for o in AB if o[0] * o[1] == 6], 15), p([o for o in AB if o[0] * o[1] % 2 == 0], 15)),
         (15, F(2, 15), F(3, 5)))
    XX2 = list(itertools.product(r(1, 7), r(1, 7)))
    bang("B20", (p([o for o in XX2 if sum(o) == 11], 36), p([o for o in XX2 if sum(o) < 6], 36)), (F(1, 18), F(5, 18)))
    bang("B21", (sum([2, 20, 14, 4]), pc(20, 40), p([x for x in r(1, 25) if int(x ** 0.5) ** 2 == x], 24)),
         (40, 50, F(1, 6)))
    bang("B22", (sum([23, 10, 9, 6, 2]), pc(6, 50)), (50, 12))
    bang("B23", (sum([3, 5, 9, 15, 10, 5, 3]), pc(15, 50)), (50, 30))
    bang("B24", (sum([18, 10, 6, 4, 2]), pc(4, 40)), (40, 10))
    bang("B25", (sum([44, 22, 21, 21, 12]), round(22 / 120 * 100, 1)), (120, 18.3))
    bang("B26", sum([10, 15, 17, 25, 8, 5]), 80)
    kq = "ABCBAABABA"
    bang("B27", [kq.count(c) for c in "ABC"], [5, 4, 1])
    bang("B28", [pc(x, 50) for x in (15, 25, 10)], [30, 50, 20])
    bang("B29", (50 - 7 - 26 - 14, 50 - 14), (3, 36))
    bang("B31", [pc(2 * x, 40) for x in (3, 11, 6)] + [2 * (3 + 11 + 6)], [15, 55, 30, 40])
    bang("B32", (sum(TO_HUU[1]), round(5 / 33 * 100)), (33, 15))
    xg = [sum(a <= x < a + 10 for x in XANG) for a in (0, 10, 20, 30)]
    bang("B33", (len(XANG), xg), (27, [6, 10, 4, 7]))
    bang("B34", [x * 20 for x in (15, 27, 23, 18, 17)], [300, 540, 460, 360, 340])
    bd = [sum(a <= x < a + 3 for x in BACH_DAN) for a in (15, 18, 21, 24, 27)]
    bang("B35", (len(BACH_DAN), bd, [pc(x, 40) for x in bd]), (40, [8, 9, 11, 3, 9], [20, F(45, 2), F(55, 2), F(15, 2), F(45, 2)]))
    bang("B36", p([x for x in r(1, 7) if nt(x)], 6), F(1, 2))
    bang("B37", (p([x for x in r(1, 61) if x < 31], 60), p([x for x in r(1, 61) if x % 8 == 5], 60)), (F(1, 2), F(7, 60)))
    bang("B38", (p([x for x in r(12, 18) if 24 % x == 0], 6), p([x for x in r(12, 18) if x % 3 == 2], 6)), (F(1, 6), F(1, 3)))
    bang("B39", p([x for x in r(1, 16) if nt(x)], 15), F(2, 5))
    bang("B40", p([x for x in r(1, 21) if x % 3 == 0], 20), F(3, 10))
    bang("B41", (p([x for x in r(1, 11) if x % 3 == 1], 30), p([x for x in r(1, 31) if x > 10 or (x % 2 and x > 3)], 30)),
         (F(2, 15), F(23, 30)))
    bang("B42", p([o for o in XX2 if sum(o) >= 10], 36), F(1, 6))
    return loi


def kiem_trung():
    """Mã câu không được trùng chon-cau ch.VII/VIII, đề KT gộp, nhóm TRUNG / KHONG_BOC của hai script chọn câu."""
    import importlib.util
    import json
    goc = Path(__file__).resolve().parents[2]

    def mod(p, n):
        s = importlib.util.spec_from_file_location(n, goc / p)
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
        return m

    c7, c8 = mod("scripts/chon_cau_ch7_9c.py", "c7"), mod("scripts/chon_cau_ch8_9c.py", "c8")
    G = goc / "inputs/refs/ngan-hang-sheet/lop-9/dai-so"
    da_dung = {r["ma"] for c in ("07", "08") for r in json.loads((G / f"chuong-{c}/chon-cau.json").read_text())}
    kt = (goc / c8.KT_PATH).read_text()
    bank = set()
    for c in ("07", "08"):
        bank |= {r["ma"] for r in json.loads((G / f"chuong-{c}.json").read_text())["rows"]}
    ma = [k[5].split(" ")[0] for k in KHOI if len(k) > 3]
    loi = [f"mã không có trong ngân hàng: {m}" for m in ma if m not in bank]
    loi += [f"trùng mã trong phiếu: {m}" for m, c in collections.Counter(ma).items() if c > 1]
    loi += [f"đã dùng ở phiếu VII/VIII: {m}" for m in ma if m in da_dung]
    loi += [f"nằm trong đề KT gộp: {m}" for m in ma if m in kt]
    loi += [f"mã cấm bốc: {m}" for m in ma if m in set(c7.KHONG_BOC) | set(c8.KHONG_BOC)]
    for g in [set(x) for x in c7.TRUNG] + [set(x) for x in c8.TRUNG]:
        if g & (da_dung | {m for m in bank if m in kt}) and g & set(ma):
            loi.append(f"cùng nhóm trùng với câu đã dùng: {sorted(g & set(ma))}")
        if len(g & set(ma)) > 1:
            loi.append(f"hai câu cùng nhóm trùng: {sorted(g & set(ma))}")
    return loi


def dem_the():
    dem_ = collections.Counter()
    for k in KHOI:
        if len(k) < 9 or k[7] == "vi_du":
            continue
        for t in re.findall(r"\[(NB|TH|VD)\]", k[8]):
            dem_[(t, k[2])] += 1
    loi = [f"{m} {tier}: sơ đồ {dem_[(m, tier)]} thẻ, khung {w}" for (m, tier), w in THE_MUC.items()
           if dem_[(m, tier)] != w]
    return loi, dict(dem_)


if __name__ == "__main__":
    l1 = kiem()
    l2, tong = dem_the()
    l3 = kiem_trung()
    so_vd = sum(1 for k in KHOI if len(k) > 3 and k[7] == "vi_du")
    print("thẻ:", tong, "· ví dụ:", so_vd, "· số hình/bảng:", len(_HINH))
    for x in l1 + l2 + l3:
        print("✗", x)
    print("SẠCH" if not (l1 + l2 + l3) else f"{len(l1 + l2 + l3)} lỗi")
    sys.exit(1 if (l1 + l2 + l3) else 0)
