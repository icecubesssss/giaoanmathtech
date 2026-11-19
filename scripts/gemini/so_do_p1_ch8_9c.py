#!/usr/bin/env python3
"""Sơ đồ Phiếu 1 ch.VIII 9C (19/11/2026) — "Phép thử ngẫu nhiên, không gian mẫu và xác suất của biến cố (Bài 25–26)".

Một phiếu 180′ trọn buổi, khuôn `khong_vd`, cờ `luat_16_11`. Mã câu = chon-cau.json (Thầy duyệt tab 9084 ngày 19/11:
64 "Hay" + ghi chú cột AC — bổ sung giả thiết cùng loại / kích thước (16-tr5, 36-tr9, Ngọc Thụy), Hà Đông "biến cố A",
27-tr7 "đồng chất", SGK B26 LT1 + VD1 bốc cả ý a).
dang_id ↔ dòng TM phiếu 1 (đánh số theo band): NB1 kiến thức cũ · NB2 C8-01 · NB3 C8-02 · NB4 C8-03 · NB5 tách TH C8-03 ·
NB6 tách TH C8-04 · NB7 C8-05 · NB8 tách TH C8-05 · NB9 C8-06 · NB10 tách TH C8-06 ·
TH1 C8-03 · TH2 C8-04 · TH3 C8-05 · TH4 C8-06 · TH5 C8-06 ghép bài.

Claude CHỐT ĐỀ (nguyên văn đề gốc, tách ý theo luật 16/11 + 17/11), thẻ, đáp số (máy đếm ở kiem()).
Hình (đĩa quay, bàn cờ, biểu đồ) vẽ bằng máy (hinh_thong_ke.py). Gemini viết lời giải, ví dụ điền khuyết, mở đầu, lý thuyết.

    .venv/bin/python scripts/gemini/so_do_p1_ch8_9c.py      # kiểm đáp số + đếm thẻ theo dang_id
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
_TU_DO = Path(__file__).with_name("phong_p1_ch8_9c.json")
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
    return r"\textquotedblleft " + s + r"\textquotedblright"


def fr(a, b):
    return rf"$\dfrac{{{a}}}{{{b}}}$"


DS = r"Mỗi khẳng định sau đúng hay sai?"


def y(*ds):
    return BR.join(ds)


# ── NGUỒN in sau đề ───────────────────────────────────────────────────────────
DD = r"đề minh họa tuyển sinh lớp 10, Phòng GD\&ĐT Đống Đa, "
N = {
    "tlmt": r"tài liệu Mathtech \textquotedblleft Phép thử ngẫu nhiên và không gian mẫu. Xác suất của biến "
            r"cố\textquotedblright",
    "pdp": r"HK2 THCS Phan Đình Phùng (Thanh Khê, Đà Nẵng), 2025--2026",
    "cva": r"HK2 THCS Chu Văn An (Thanh Khê, Đà Nẵng), 2025--2026",
    "dtd": r"HK2 THCS Đoàn Thị Điểm (TP. Hồ Chí Minh), 2025--2026",
    "gl": r"HK2 Phòng GD\&ĐT Gia Lâm, 2024--2025", "tt": r"HK2 Phòng GD\&ĐT Thạch Thất, 2024--2025",
    "hn26": r"đề tuyển sinh lớp 10 Hà Nội, 2026--2027", "hn25": r"đề tuyển sinh lớp 10 Hà Nội, 2025--2026",
    "cm4": r"thi thử vào 10 lần 4 Phòng GD\&ĐT Chương Mỹ, 2025--2026",
    "ntan25": r"GK2 THCS Nghĩa Tân, 2025--2026", "kk": r"GK2 THCS Kiêu Kỵ, 2025--2026",
    "pd25": r"HK2 THCS Phúc Đồng (Long Biên), 2025--2026", "pd24": r"HK2 THCS Phúc Đồng (Long Biên), 2024--2025",
    "nthuy": r"HK2 THCS Ngọc Thụy (Long Biên), 2024--2025", "ngt": r"HK2 THCS Ngô Gia Tự (Việt Hưng), 2025--2026",
    "hd": r"khảo sát lớp 9 Phòng GD\&ĐT Hà Đông, 2025--2026", "pl": r"HK2 THCS Phúc Lợi (Long Biên), 2024--2025",
    "tl": r"thi thử vào 10 THCS Tự Lập, 2025--2026", "ntl": r"GK2 THCS Nam Từ Liêm, 2025--2026",
    "tll3": r"thi thử vào 10 lần 3 THCS Thọ Lộc, 2025--2026", "tll3b": r"thi thử vào 10 lần 3 THCS Thọ Lộc, 2026--2027",
    "cd25": r"GK2 THCS Chương Dương, 2025--2026", "cd24": r"GK2 THCS Chương Dương, 2024--2025",
    "nbk": r"GK2 THCS Nguyễn Bỉnh Khiêm, 2024--2025", "lt": DD + r"đề 08 (THCS Láng Thượng), 2025--2026",
    "bd": r"HK2 Phòng GD\&ĐT Ba Đình, 2024--2025", "hbt": r"HK2 Phòng GD\&ĐT Hai Bà Trưng, 2024--2025",
    "lmns": r"HK2 THCS\&THPT M.V. Lômônôxốp, 2024--2025", "nl": r"HK2 THCS Ngọc Lâm (Long Biên), 2024--2025",
    "nhtan": r"GK2 THCS Nhật Tân, 2024--2025", "bvd2": DD + r"đề 02 (THCS Bế Văn Đàn), 2025--2026",
    "tvg": r"GK2 THCS Trưng Vương, 2025--2026", "tvc": r"HK2 THCS Trưng Vương, 2025--2026",
    "kt": DD + r"đề 07 (THCS Khương Thượng), 2025--2026", "cg": r"thi thử vào 10 lần 1 THCS Cầu Giấy, 2025--2026",
}


def ng(k):
    return r" \textit{(" + N[k] + ")}"


def sgk(s):
    return r" \textit{(SGK Toán 9 tập hai, " + s + ")}"


# ── SỐ LIỆU (dùng chung cho hình + kiem) ──────────────────────────────────────
CAO_CD = [158, 164, 148, 150, 160, 151, 155, 152, 152, 163, 153, 154, 154, 154, 155, 155, 168, 157, 155, 156,
          156, 156, 156, 157, 157, 151, 158, 150, 162, 163, 163, 163, 152, 163, 148, 165, 167, 168, 158, 170]
DIA_PL = [1, 12, 18, 22, 27, 69, 96, 99]

# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# Tiêu đề: (chữ, chặng, "heading").
# Ví dụ:  (nhãn, chặng, "", "", 0, mã, "", "vi_du", ĐỀ IN (có nguồn), GHI lời giải cho thợ).
# Bài:    (nhãn, chặng, tier, dang_id, level, mã, "", hình thức, ĐỀ IN, GHI đáp số cho thợ).
XX = r"Gieo đồng thời hai con xúc xắc cân đối và đồng chất I và II."
KHOI = [
    # ───────────── LUYỆN TẬP 1 — chỉ NB (18 thẻ) ─────────────
    ("Mạch 1. Phép thử ngẫu nhiên, biến cố xảy ra hay không", "practice1", "heading"),
    ("Ví dụ 1.", "practice1", "", "", 0, "sgk-b26-hd1", "", "vi_du",
     y(r"Bạn Tùng gieo một con xúc xắc liên tiếp hai lần. Xét các biến cố sau:",
       r"\hspace*{1.4em}$E$: " + q(r"Cả hai lần gieo con xúc xắc đều xuất hiện mặt có số chấm là số nguyên tố") + ",",
       r"\hspace*{1.4em}$F$: " + q(r"Cả hai lần gieo con xúc xắc đều không xuất hiện mặt có số chấm là số chẵn") + ".",
       r"a) Phép thử là gì?",
       r"b) Giả sử số chấm xuất hiện trên con xúc xắc trong lần gieo thứ nhất, thứ hai tương ứng là $2$ và $5$ chấm. "
       r"Khi đó, biến cố nào xảy ra? Biến cố nào không xảy ra?" + sgk("Bài 26, Hoạt động")),
     "a) Phép thử là gieo một con xúc xắc liên tiếp hai lần (quan sát số chấm xuất hiện mỗi lần). b) Kết quả (2; 5): "
     "2 và 5 đều là số nguyên tố nên E xảy ra · lần thứ nhất xuất hiện mặt 2 chấm (số chẵn) nên F không xảy ra. "
     "Nhắc: 2 là số nguyên tố chẵn duy nhất. 5–6 ô (tên phép thử, 2 và 5 nguyên tố, E xảy ra, mặt 2 chẵn, F không)."),
    ("Bài 1.", "practice1", "onclass", "NB2", 1, "ck2-phan-dinh-phung-2025-TN8", "", "trac_nghiem",
     r"[NB] Trong các thí nghiệm sau, thí nghiệm nào không phải là phép thử ngẫu nhiên?" + ng("pdp")
     + tn(r"Gieo một con xúc xắc cân đối, đồng chất và xem mặt xuất hiện là số chẵn hay số lẻ.",
          r"Tung một đồng xu để quyết định xem nhóm mình hay nhóm bạn sẽ được thuyết trình trước.",
          r"Cô giáo bỏ tên của $30$ bạn trong lớp vào một chiếc hộp rồi bốc thăm xem ai là người nhận quà.",
          r"Đo và tính tổng số đo ba góc trong một tam giác bất kì."),
     "Chọn D: tổng ba góc của mọi tam giác luôn bằng 180° (biết trước kết quả) nên không phải phép thử ngẫu nhiên. "
     "Lời giải 1–2 dòng."),
    ("Bài 2.", "practice1", "onclass", "NB2", 1, "sgk-8.3 (ý a)", "", "tra_loi_ngan",
     r"Có hai nhóm học sinh: Nhóm I có ba học sinh nam là Huy, Sơn, Tùng. Nhóm II có ba học sinh nữ là Hồng, Phương, "
     r"Linh. Giáo viên chọn ngẫu nhiên một học sinh từ mỗi nhóm." + sgk("Bài tập 8{.}3")
     + BR + r"[NB] Phép thử và kết quả của phép thử là gì?",
     "Phép thử: giáo viên chọn ngẫu nhiên một học sinh nam từ nhóm I và một học sinh nữ từ nhóm II. Kết quả của phép "
     "thử là cặp (a; b), a là học sinh được chọn ở nhóm I, b là học sinh được chọn ở nhóm II. KHÔNG mô tả không gian "
     "mẫu (ý b của SGK không hỏi). 2 dòng."),
    ("Bài 3.", "practice1", "onclass", "NB2", 1, "tl-ptnn-xsbc-27-tr7", "", "dung_sai",
     r"Cho phép thử gieo hai con xúc xắc cân đối và đồng chất. Giả sử kết quả của phép thử là con xúc xắc thứ nhất "
     r"xuất hiện mặt $1$ chấm, con xúc xắc thứ hai xuất hiện mặt $6$ chấm. Xét các biến cố" + ng("tlmt")
     + BR + r"\hspace*{1.4em}$A$: " + q("Tích số chấm xuất hiện là số chẵn") + ","
     + BR + r"\hspace*{1.4em}$B$: " + q("Hai mặt xuất hiện có cùng số chấm") + "."
     + BR + y(DS, r"a) [NB] Biến cố $A$ xảy ra.", r"b) [NB] Biến cố $B$ xảy ra."),
     "Thầy 19/11: sửa 'đồng nhất' → 'đồng chất'; bốc 2 biến cố (bỏ 'tổng lớn hơn 1' quá hiển nhiên). a) Đúng: "
     "1·6=6 là số chẵn. b) Sai: 1 khác 6. Mỗi ý một dòng \"a) Đúng. …\"."),
    ("Mạch 2. Không gian mẫu và kết quả thuận lợi", "practice1", "heading"),
    ("Ví dụ 2.", "practice1", "", "", 0, "tl-ptnn-xsbc-12-tr4 + tl-ptnn-xsbc-22-tr6", "", "vi_du",
     y(r"a) Xét phép thử quay bánh xe ở Hình 1 để quan sát xem khi bánh xe dừng thì mũi kim (gắn cố định) chỉ vào ô "
       r"ghi số mấy. Hãy liệt kê các phần tử của không gian mẫu.",
       r"b) Bánh xe ở Hình 2 được chia thành $16$ hình quạt bằng nhau, đánh số thứ tự từ $1$ đến $16$. Quay bánh xe và "
       r"quan sát xem khi nó dừng thì mũi kim (được gắn cố định) chỉ vào hình quạt số mấy. Hãy liệt kê các kết quả "
       r"thuận lợi cho mỗi biến cố sau:",
       r"\hspace*{1.4em}$A$: " + q("Kim chỉ vào số là bội của $5$") + ",",
       r"\hspace*{1.4em}$B$: " + q("Kim chỉ vào số là ước của $14$") + "." + ng("tlmt"))
     + P2(DQ(list(range(1, 11)), kim="tren", ten="Hình 1"), DQ(list(range(1, 17)), kim="tren", R=1.25, ten="Hình 2"),
          rong=0.3),
     "a) Ω = {1; 2; 3; 4; 5; 6; 7; 8; 9; 10}, n(Ω)=10 (viết tập hợp trong $…$ bằng \\{ \\}, các phần tử cách nhau "
     "dấu chấm phẩy như SGK — trong $…$ được phép). b) Các kết quả thuận lợi cho A là 5, 10, 15 · cho B là 1, 2, 7, 14 "
     "(nhớ ước gồm cả 1 và chính 14). 6–8 ô."),
    ("Bài 4.", "practice1", "onclass", "NB3", 1, "ck2-gia-lam-2024-I2 (ý a)", "", "tra_loi_ngan",
     r"Gieo một con xúc xắc cân đối, đồng chất một lần." + ng("gl")
     + BR + r"[NB] Viết tập hợp các kết quả có thể xảy ra đối với số chấm trên mặt xuất hiện của xúc xắc. Tập hợp đó "
       r"có bao nhiêu phần tử?",
     "Ω = {1; 2; 3; 4; 5; 6}, có 6 phần tử. 1–2 dòng."),
    ("Mạch 3. Không gian mẫu của phép thử hai hành động", "practice1", "heading"),
    ("Ví dụ 3.", "practice1", "", "", 0, "sgk-b25-vd1", "", "vi_du",
     y(r"Bạn Lan gieo một con xúc xắc và bạn Hoà gieo một đồng xu. Quan sát số chấm xuất hiện trên con xúc xắc và mặt "
       r"xuất hiện của đồng xu.",
       r"a) Phép thử và kết quả của phép thử là gì?",
       r"b) Mô tả không gian mẫu của phép thử. Không gian mẫu có bao nhiêu phần tử?" + sgk("Bài 25, Ví dụ 1")),
     "ĐỌC ẢNH sgk9t2-tr57, tr58 để theo đúng lời giải SGK. a) Phép thử: Lan gieo xúc xắc, Hoà gieo đồng xu. Kết quả là "
     "cặp (a, b) với a là số chấm, b là mặt đồng xu (S: sấp, N: ngửa). b) Lập bảng hai chiều 2 hàng (S, N) × 6 cột "
     "(1 … 6) bằng [[bang: …]], vài ô là [[fill:]] · không gian mẫu có 2·6 = 12 phần tử. 6–8 ô."),
    ("Bài 5.", "practice1", "onclass", "NB9", 1, "ck2-phan-dinh-phung-2025-TN11", "", "trac_nghiem",
     r"[NB] Bạn Minh gieo một đồng xu và bạn Hải lấy ngẫu nhiên một quả bóng từ một hộp chứa $4$ quả bóng với các "
     r"màu xanh, đỏ, tím, vàng. Không gian mẫu của phép thử trên có số phần tử là" + ng("pdp")
     + tn("$8$", "$9$", "$12$", "$7$"),
     "Chọn A: mỗi mặt đồng xu (2 mặt) ghép với một trong 4 màu bóng ⇒ 2·4 = 8. Lời giải 1 dòng."),
    ("Bài 6.", "practice1", "onclass", "NB3", 1, "sgk-b26-lt1", "", "tra_loi_ngan",
     r"Bạn Hoàng lấy ngẫu nhiên một quả cầu từ một túi đựng $2$ quả cầu gồm một quả màu đen và một quả màu trắng, có "
     r"cùng khối lượng và kích thước. Bạn Hải rút ngẫu nhiên một tấm thẻ từ một hộp đựng $3$ tấm thẻ $A$, $B$, $C$. "
     r"Xét các biến cố sau:" + sgk("Bài 26, Luyện tập 1")
     + BR + r"\hspace*{1.4em}$E$: " + q("Bạn Hoàng lấy được quả cầu màu đen") + ","
     + BR + r"\hspace*{1.4em}$F$: " + q("Bạn Hoàng lấy được quả cầu màu trắng và bạn Hải không rút được tấm thẻ $A$")
     + "."
     + BR + y(r"a) [NB] Mô tả không gian mẫu của phép thử.",
              r"b) [NB] Mô tả các kết quả thuận lợi cho biến cố $E$.",
              r"c) [NB] Mô tả các kết quả thuận lợi cho biến cố $F$."),
     "Thầy 19/11: bốc cả ý a. Kí hiệu Đ: đen, T: trắng. a) Ω = {(Đ, A); (Đ, B); (Đ, C); (T, A); (T, B); (T, C)}, 6 phần "
     "tử. b) (Đ, A), (Đ, B), (Đ, C). c) (T, B), (T, C). Mỗi ý 1–2 dòng."),
    ("Bài 7.", "practice1", "onclass", "NB3", 1, "sgk-b26-vd1", "", "tra_loi_ngan",
     r"Một tấm bìa cứng hình tròn được chia làm bốn hình quạt bằng nhau, đánh số $1$, $2$, $3$, $4$ và được gắn vào "
     r"trục quay có mũi tên ở tâm (hình bên). Bạn Tuấn quay tấm bìa hai lần, quan sát và ghi lại số của hình quạt mà "
     r"mũi tên chỉ vào." + sgk("Bài 26, Ví dụ 1")
     + DQ([1, 2, 3, 4], rong=0.22)
     + y(r"a) [NB] Phép thử là gì? Hãy mô tả không gian mẫu của phép thử.",
         r"b) [NB] Xét biến cố $E$: " + q("Tổng hai số ghi trên hai hình quạt ở hai lần quay bằng $5$")
         + ". Mô tả các kết quả thuận lợi cho biến cố $E$.",
         r"c) [NB] Xét biến cố $F$: " + q("Tích hai số ghi trên hai hình quạt ở hai lần quay bằng $4$")
         + ". Mô tả các kết quả thuận lợi cho biến cố $F$."),
     "Thầy 19/11: bốc cả ý a. ĐỌC ẢNH sgk9t2-tr60, tr61 theo đúng lời giải SGK. a) Phép thử: quay tấm bìa hai lần. "
     "Kết quả là cặp (i, j), i, j lần lượt là số ở lần quay thứ nhất, thứ hai · bảng 4×4 [[bang: …]] · 16 phần tử. "
     "b) (1, 4), (2, 3), (3, 2), (4, 1). c) (1, 4), (2, 2), (4, 1)."),
    ("Mạch 4. Tính xác suất bằng công thức", "practice1", "heading"),
    ("Ví dụ 4.", "practice1", "", "", 0, "tl-ptnn-xsbc-16-tr5 (ý a, c)", "", "vi_du",
     y(r"Các kết quả của mỗi phép thử sau có đồng khả năng không? Tại sao?",
       r"a) Gieo một đồng xu cân đối và đồng chất.",
       r"b) Lấy ngẫu nhiên $1$ tấm thẻ từ một hộp chứa $2$ tấm thẻ ghi số $5$ và $5$ tấm thẻ ghi số $2$ (các tấm thẻ "
       r"cùng loại) và xem số ghi trên thẻ." + ng("tlmt")),
     "Thầy 19/11: bổ sung 'các tấm thẻ cùng loại'. a) Đồng xu cân đối, đồng chất nên hai kết quả S, N có cùng khả năng "
     "xảy ra · đồng khả năng. b) Có 7 tấm thẻ, trong đó số 2 ghi trên 5 thẻ, số 5 chỉ ghi trên 2 thẻ nên kết quả "
     "\"số 2\" có khả năng xảy ra cao hơn · không đồng khả năng. Kết dòng Vậy: chỉ khi các kết quả đồng khả năng mới "
     "dùng công thức P(A) = n(A)/n(Ω). 4–6 ô."),
    ("Ví dụ 5.", "practice1", "", "", 0, "tl-ptnn-xsbc-36-tr9 (ý a) + gk2-nghia-tan-2025-I2 (ý a)", "", "vi_du",
     y(r"a) Túi kẹo trái cây có $60$ viên kẹo có cùng kích thước và khối lượng, trong đó có $20$ viên kẹo vị sầu "
       r"riêng, $15$ viên kẹo vị cam, $7$ viên kẹo vị dâu, $10$ viên kẹo vị chanh, $8$ viên kẹo vị mít. Bạn Toàn lấy "
       r"ngẫu nhiên một viên kẹo trong túi. Tính xác suất của biến cố $E$: " + q("Bạn Toàn lấy được kẹo vị sầu riêng")
       + "." + ng("tlmt"),
       r"b) Một hộp có $52$ chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, \ldots, 52$, hai thẻ khác "
       r"nhau thì ghi hai số khác nhau. Rút ngẫu nhiên một thẻ trong hộp. Tính xác suất của biến cố "
       + q("Số xuất hiện trên thẻ được rút ra là số nhỏ hơn $27$") + "." + ng("ntan25")),
     "Thầy 19/11: bổ sung 'cùng kích thước và khối lượng'. Nhịp SGK: số kết quả có thể n(Ω) · các kết quả đồng khả "
     "năng · số kết quả thuận lợi n(E) · P(E) = n(E)/n(Ω) (công thức \\dfrac dòng riêng) · Vậy. a) n(Ω)=60, n(E)=20, "
     "P=20/60=1/3. b) n(Ω)=52, các số nhỏ hơn 27 là 1, 2, …, 26 nên có 26 kết quả thuận lợi, P=26/52=1/2. "
     "Đặt tên biến cố ý b là A trong lời giải. 3–4 ô mỗi ý."),
    ("Bài 8.", "practice1", "onclass", "NB4", 1, "so-hn-2026-I2", "", "trac_nghiem",
     r"[NB] Một hộp đựng $6$ quả bóng cùng loại, mỗi quả bóng ghi một trong các số $1, 2, 3, 4, 5, 6$, hai quả bóng "
     r"khác nhau được ghi hai số khác nhau. Lấy ngẫu nhiên một quả bóng trong hộp. Xác suất của biến cố $A$: "
     + q("Số ghi trên quả bóng lấy được là số chẵn") + " là" + ng("hn26")
     + tn(r"$\dfrac{1}{3}$", r"$\dfrac{1}{2}$", r"$\dfrac{1}{6}$", r"$\dfrac{2}{3}$"),
     "Chọn B: A gồm 2, 4, 6 ⇒ P(A)=3/6=1/2. Lời giải 1–2 dòng."),
    ("Bài 9.", "practice1", "onclass", "NB4", 1, "ck2-thach-that-2024-1-2", "", "trac_nghiem",
     r"[NB] Hình bên mô tả một đĩa tròn bằng bìa cứng được chia làm tám phần bằng nhau và ghi các số "
     r"$1, 2, 3, \ldots, 8$. Chiếc kim được gắn cố định vào trục quay ở tâm của đĩa. Quay đĩa tròn một lần. Xác suất "
     r"của biến cố $A$: " + q("Chiếc kim chỉ vào hình quạt ghi số lớn hơn $3$") + " là" + ng("tt")
     + DQ(list(range(1, 9)), rong=0.24)
     + tn(r"$\dfrac{3}{8}$", r"$\dfrac{1}{2}$", r"$\dfrac{5}{8}$", r"$\dfrac{3}{4}$"),
     "Chọn C: A gồm 4, 5, 6, 7, 8 (không lấy 3) ⇒ 5/8. Phương án 3/4 là lỗi lấy cả số 3."),
    ("Ví dụ 6.", "practice1", "", "", 0, "gk2-kieu-ky-2025-I2", "", "vi_du",
     r"Một túi đựng $30$ viên bi có kích thước và khối lượng như nhau, trong đó có $5$ viên bi đỏ, $6$ viên bi xanh, "
     r"$7$ viên bi vàng, còn lại là bi trắng. Lấy ngẫu nhiên một viên bi trong túi. Tính xác suất của biến cố $A$: "
     + q("Lấy được viên bi màu trắng") + "." + ng("kk"),
     "Số bi trắng là 30 − (5 + 6 + 7) = 12 · n(Ω)=30, đồng khả năng · n(A)=12 · P(A)=12/30=2/5 · Vậy. 6–8 ô."),
    ("Bài 10.", "practice1", "onclass", "NB4", 1, "v10-chuong-my-l4-2025-I2", "", "trac_nghiem",
     r"[NB] Một chiếc túi có $20$ tấm thẻ có cùng hình dạng và kích thước gồm $3$ màu, trong đó có $8$ tấm thẻ màu đỏ, "
     r"$5$ tấm thẻ màu vàng và $7$ tấm thẻ màu trắng. Lấy ngẫu nhiên $1$ tấm thẻ từ túi. Xác suất của biến cố $E$: "
     + q("Không lấy được tấm thẻ màu vàng") + " là" + ng("cm4")
     + tn(r"$\dfrac{1}{4}$", r"$\dfrac{7}{20}$", r"$\dfrac{2}{5}$", r"$\dfrac{3}{4}$"),
     "Chọn D: không vàng = 8 + 7 = 15 thẻ ⇒ 15/20 = 3/4. Phương án 1/4 là lỗi quên chữ \"Không\"."),
    ("Mạch 5. Xác suất từ tỉ lệ phần trăm, bảng số liệu", "practice1", "heading"),
    ("Bài 11.", "practice1", "onclass", "NB1", 1, "ck2-doan-thi-diem-2025-3 (ý a)", "", "tra_loi_ngan",
     r"Thống kê điểm kiểm tra giữa kì II môn Toán của các học sinh lớp 9A được biểu diễn bởi biểu đồ sau." + ng("dtd")
     + C([5, 6, 7, 8, 9, 10], [3, 7, 9, 10, 6, 1], "Điểm số", "Số học sinh", 12, 3,
         tieu_de="Số lượng học sinh theo điểm đạt được", bw=0.7, gap=0.5)
     + y(r"a) [NB] Lớp 9A có tổng cộng bao nhiêu học sinh?",
         r"b) [NB] Tần số tương đối của số học sinh có điểm kiểm tra là $7$ bằng"
         + tn(r"$9\%$", r"$25\%$", r"$36\%$", r"$0{,}25\%$")),
     "Kiến thức cũ (chương VII). a) 3+7+9+10+6+1 = 36 học sinh. b) 9/36·100% = 25%. Chọn B."),
    ("Ví dụ 7.", "practice1", "", "", 0, "tl-ptnn-xsbc-74-tr15", "", "vi_du",
     r"Trong một kì thi học sinh giỏi Toán, tỉ lệ học sinh đạt giải là $35\%$. Chọn ngẫu nhiên một học sinh đã tham "
     r"gia kì thi đó. Tính xác suất của biến cố " + q("Học sinh được chọn đạt giải") + "." + ng("tlmt"),
     "Gọi số học sinh dự thi là n thì số học sinh đạt giải là 35%·n · P(A) = (35%·n)/n = 35% = 35/100 = 7/20 · Vậy. "
     "Ý: tỉ lệ phần trăm của một nhóm chính là xác suất chọn được đối tượng thuộc nhóm đó (nối với tần số tương đối "
     "ở Bài 11). 4–6 ô."),
    ("Bài 12.", "practice1", "onclass", "NB7", 1, "tl-ptnn-xsbc-43-tr10 (ý a)", "", "tra_loi_ngan",
     r"Nhà máy đã kiểm tra chất lượng sản phẩm do hai dây chuyền $Y$, $Z$ sản xuất và thống kê số sản phẩm đạt, không "
     r"đạt chất lượng trong bảng sau." + ng("tlmt")
     + B(["Chất lượng sản phẩm", "Đạt", "Không đạt", "Tổng"], ["Dây chuyền $Y$", 250, 14, 264],
         ["Dây chuyền $Z$", 270, 18, 288], ["Tổng", 520, 32, 552])
     + r"[NB] Lấy ngẫu nhiên một sản phẩm trong số những sản phẩm này. Tính xác suất của biến cố $C$: "
     + q("Lấy được một phế phẩm (sản phẩm không đạt chất lượng)") + ".",
     "n(Ω)=552 (ô Tổng–Tổng), n(C)=32 ⇒ P(C)=32/552=4/69. 2 dòng."),
    # ───────────── LUYỆN TẬP 2 — TH có câu dẫn NB (12 TH + 14 NB) ─────────────
    ("Mạch 6. Xác suất từ biểu đồ", "practice2", "heading"),
    ("Ví dụ 8.", "practice2", "", "", 0, "tl-ptnn-xsbc-31-tr8", "", "vi_du",
     r"Mỗi công nhân của một đội xây dựng làm việc ở một trong năm bộ phận của đội đó: Lợp mái, Ốp gạch bếp, Lát nền, "
     r"Trát tường, Xây tường. Biểu đồ hình quạt tròn dưới đây thống kê tỉ lệ công nhân thuộc mỗi bộ phận. Chọn ngẫu "
     r"nhiên một công nhân của đội. Tính xác suất của mỗi biến cố sau:" + ng("tlmt")
     + Q([20, 10, 25, 15, 30], ["Lợp mái", "Ốp gạch bếp", "Lát nền", "Trát tường", "Xây tường"])
     + y(r"a) $A$: " + q("Công nhân được chọn thuộc bộ phận Trát tường") + ",",
         r"b) $B$: " + q("Công nhân được chọn không thuộc bộ phận Lát nền hay Lợp mái") + "."),
     "a) P(A)=15%=3/20. b) Tỉ lệ công nhân thuộc Lát nền hoặc Lợp mái là 25%+20%=45% · không thuộc hai bộ phận đó: "
     "100%−45%=55% · P(B)=55%=11/20. 3–4 ô mỗi ý."),
    ("Bài 13.", "practice2", "onclass", "NB8+TH3", 2, "gk2-chuong-duong-2025-I2", "", "th_dan",
     r"Cho biểu đồ tần số ghép nhóm biểu diễn thời gian hoàn thành một bài kiểm tra của toàn bộ học sinh lớp 9A như "
     r"sau." + ng("cd25")
     + C([90, 95, 100, 105, 110, 115, 120], [3, 5, 6, 7, 9, 10], "Thời gian (phút)", "Tần số", 12, 3, sat=True,
         tieu_de="Thời gian hoàn thành bài kiểm tra của lớp 9A", bw=0.75)
     + y(r"a) [NB] Lớp 9A có bao nhiêu học sinh?",
         r"b) [TH] Chọn một học sinh bất kì trong số các học sinh trên của lớp 9A. Tính xác suất để chọn được học sinh "
         r"có thời gian làm bài dưới $100$ phút."),
     "a) 3+5+6+7+9+10 = 40. b) Theo câu a), n(Ω)=40 · dưới 100 phút gồm hai nhóm [90; 95) và [95; 100) nên có "
     "3+5 = 8 học sinh · P = 8/40 = 1/5 · Vậy."),
    ("Bài 14.", "practice2", "onclass", "NB8+TH3", 2, "tl-ptnn-xsbc-45-tr11 (ý a, c)", "", "th_dan",
     r"Thầy Nam điều tra sở thích chơi thể thao của học sinh lớp 9A do thầy phụ trách (mỗi học sinh chỉ nêu một môn "
     r"thể thao yêu thích nhất). Biểu đồ cột kép dưới đây biểu diễn số học sinh nam và số học sinh nữ của lớp 9A có "
     r"sở thích chơi một số môn thể thao mà thầy Nam đã điều tra. Chọn ngẫu nhiên một học sinh của lớp 9A tham gia "
     r"điều tra." + ng("tlmt")
     + K(["Bóng đá", "Bóng rổ", "Bóng bàn"], [12, 4, 5], [10, 5, 6], ("Nam", "Nữ"), "Môn", "Số học sinh", 15, 5)
     + y(r"a) [NB] Có bao nhiêu học sinh lớp 9A tham gia điều tra?",
         r"b) [TH] Tính xác suất của mỗi biến cố $A$: " + q("Học sinh được chọn là nam") + " và $B$: "
         + q("Học sinh được chọn là nam và yêu thích môn Bóng bàn hoặc Bóng rổ") + "."),
     "a) 12+4+5+10+5+6 = 42. b) Theo câu a), n(Ω)=42 · số học sinh nam 12+4+5=21 ⇒ P(A)=21/42=1/2 · nam thích Bóng "
     "bàn hoặc Bóng rổ: 5+4=9 ⇒ P(B)=9/42=3/14 · Vậy."),
    ("Mạch 7. Phép thử hai hành động", "practice2", "heading"),
    ("Bài 15.", "practice2", "onclass", "NB10+TH4", 2, "sgk-b25-lt1", "", "th_dan",
     r"Một tấm bìa cứng hình tròn được chia làm ba hình quạt bằng nhau, đánh số $1$, $2$, $3$ và được gắn vào trục "
     r"quay có mũi tên cố định ở tâm (hình bên). Bạn Hiền quay tấm bìa liên tiếp hai lần và quan sát xem mũi tên chỉ "
     r"vào hình quạt nào khi tấm bìa dừng lại." + sgk("Bài 25, Luyện tập 1")
     + DQ([1, 2, 3], rong=0.22)
     + y(r"a) [NB] Phép thử và kết quả của phép thử là gì?",
         r"b) [TH] Mô tả không gian mẫu của phép thử. Không gian mẫu có bao nhiêu phần tử?"),
     "hints: SGK gợi ý lập bảng (hàng Lần 1, cột Lần 2). a) Phép thử: quay tấm bìa liên tiếp hai lần. Kết quả là cặp "
     "(i, j), i là số ở lần quay thứ nhất, j là số ở lần quay thứ hai. b) Bảng 3×3 [[bang: …]] đủ 9 cặp · Ω gồm 9 "
     "cặp, viết dạng tập hợp · n(Ω)=9 · Vậy."),
    ("Ví dụ 9.", "practice2", "", "", 0, "sgk-8.15 (A, D)", "", "vi_du",
     y(r"Có hai túi I và II. Túi I chứa $3$ tấm thẻ, đánh số $2$, $3$, $4$. Túi II chứa $2$ tấm thẻ, đánh số $5$, $6$. "
       r"Từ mỗi túi I và II, rút ngẫu nhiên một tấm thẻ. Tính xác suất của các biến cố sau:" + sgk("Bài tập 8{.}15"),
       r"\hspace*{1.4em}$A$: " + q("Hai số ghi trên hai tấm thẻ chênh nhau $2$ đơn vị") + ",",
       r"\hspace*{1.4em}$B$: " + q("Tổng hai số ghi trên hai tấm thẻ là một số nguyên tố") + "."),
     "Biến cố D của SGK đổi tên thành B. Bảng 3 hàng (2, 3, 4) × 2 cột (5, 6) [[bang: …]] · n(Ω)=6, đồng khả năng · "
     "A: (3, 5), (4, 6) ⇒ P(A)=2/6=1/3 · tổng các cặp: 7, 8, 8, 9, 9, 10, chỉ 7 là số nguyên tố ⇒ B: (2, 5) ⇒ "
     "P(B)=1/6 · Vậy. 7–9 ô."),
    ("Bài 16.", "practice2", "onclass", "NB10+TH4", 2, "sgk-8.6 (E, F)", "", "th_dan",
     XX + r" Xét các biến cố" + sgk("Bài tập 8{.}6")
     + BR + r"\hspace*{1.4em}$E$: " + q("Có đúng một con xúc xắc xuất hiện mặt $6$ chấm") + ","
     + BR + r"\hspace*{1.4em}$F$: " + q("Có ít nhất một con xúc xắc xuất hiện mặt $6$ chấm") + "."
     + BR + y(r"a) [NB] Không gian mẫu của phép thử có bao nhiêu phần tử?",
              r"b) [TH] Tính xác suất của các biến cố $E$ và $F$."),
     "a) 6·6 = 36. b) Theo câu a), n(Ω)=36 · E: (6, 1), …, (6, 5), (1, 6), …, (5, 6) — liệt kê đủ 10 cặp ⇒ "
     "P(E)=10/36=5/18 · F gồm các kết quả của E và (6, 6) nên có 11 cặp ⇒ P(F)=11/36 · Vậy."),
    ("Bài 17.", "practice2", "onclass", "NB10+TH4", 2, "sgk-8.7 (F, G)", "", "th_dan",
     r"Bạn An gieo một đồng xu cân đối và bạn Bình rút ngẫu nhiên một tấm thẻ từ hộp chứa $5$ tấm thẻ ghi các số "
     r"$1$, $2$, $3$, $4$, $5$. Xét các biến cố" + sgk("Bài tập 8{.}7")
     + BR + r"\hspace*{1.4em}$A$: " + q("Rút được tấm thẻ ghi số chẵn và đồng xu xuất hiện mặt sấp") + ","
     + BR + r"\hspace*{1.4em}$B$: " + q("Rút được tấm thẻ ghi số $5$ hoặc đồng xu xuất hiện mặt ngửa") + "."
     + BR + y(r"a) [NB] Không gian mẫu của phép thử có bao nhiêu phần tử?",
              r"b) [TH] Tính xác suất của các biến cố $A$ và $B$."),
     "Biến cố F, G của SGK đổi tên thành A, B. a) 2·5 = 10. b) Theo câu a), n(Ω)=10 · A: (S, 2), (S, 4) ⇒ "
     "P(A)=2/10=1/5 · B: (N, 1), (N, 2), (N, 3), (N, 4), (N, 5), (S, 5) — 6 cặp, (N, 5) chỉ đếm một lần ⇒ "
     "P(B)=6/10=3/5 · Vậy."),
    ("Ví dụ 10.", "practice2", "", "", 0, "v10-ha-dong-2025-I2", "", "vi_du",
     r"Cho hai túi I và II, mỗi túi chứa $3$ tấm thẻ cùng loại được ghi các số $2$, $3$, $7$. Rút ngẫu nhiên từ mỗi túi "
     r"ra một tấm thẻ và ghép thành số có hai chữ số với chữ số trên tấm thẻ rút từ túi I là chữ số hàng chục. Tính "
     r"xác suất của biến cố $A$: " + q("Số tạo thành là số nguyên tố") + "." + ng("hd"),
     "Thầy 19/11: đề sửa thành 'biến cố A', thêm 'cùng loại'. Bảng 3×3 các số tạo thành [[bang: …]]: 22, 23, 27, 32, "
     "33, 37, 72, 73, 77 · n(Ω)=9 · số nguyên tố: 23, 37, 73 (27=3·9, 33=3·11, 77=7·11 là hợp số) · P(A)=3/9=1/3 · "
     "Vậy. 7–9 ô."),
    ("Bài 18.", "practice2", "onclass", "NB10+TH5", 2, "ck2-chu-van-an-dn-2025-5", "", "th_dan",
     r"Cho hai túi $A$ và $B$, mỗi túi chứa $3$ tấm thẻ cùng loại được ghi các số $1$, $5$, $9$. Rút ngẫu nhiên từ mỗi "
     r"túi ra một tấm thẻ và ghép thành số có hai chữ số với chữ số trên tấm thẻ rút ra từ túi $A$ là chữ số hàng chục. "
     r"Xét các biến cố $M$: " + q("Số tạo thành chia hết cho $5$") + " và $N$: " + q("Số tạo thành là số nguyên tố")
     + "." + ng("cva")
     + BR + y(r"a) [NB] Mô tả không gian mẫu của phép thử. Không gian mẫu có bao nhiêu phần tử?",
              r"b) [NB] Trong các số tạo thành, những số nào chia hết cho $5$?",
              r"c) [TH] Tính xác suất của mỗi biến cố $M$ và $N$."),
     "a) Ω = {11; 15; 19; 51; 55; 59; 91; 95; 99}, 9 phần tử (có thể kèm bảng). b) 15, 55, 95. c) Theo câu b), "
     "P(M)=3/9=1/3 · số nguyên tố: 11, 19, 59 (51=3·17, 91=7·13, 99=9·11 là hợp số) ⇒ P(N)=3/9=1/3 · Vậy."),
    ("Bài 19.", "practice2", "onclass", "NB10+TH5", 2, "ck2-phan-dinh-phung-2025-TL4", "", "th_dan",
     r"Trong ngày hội \textquotedblleft Sống xanh\textquotedblright, một trường THCS tổ chức ba khu vực tình nguyện: "
     r"Khu $A$ (Trồng cây), Khu $B$ (Phân loại rác tái chế) và Khu $C$ (Tặng sách cũ cho trẻ em nghèo). Hai bạn Giang "
     r"và Ngân cùng đăng kí tham gia tình nguyện. Mỗi bạn chọn ngẫu nhiên một khu vực để tham gia. Xét các biến cố"
     + ng("pdp")
     + BR + r"\hspace*{1.4em}$M$: " + q("Cả hai bạn cùng tham gia vào một hoạt động để hỗ trợ nhau") + ","
     + BR + r"\hspace*{1.4em}$N$: " + q("Có ít nhất một bạn tham gia vào hoạt động trồng cây") + "."
     + BR + y(r"a) [NB] Phép thử là gì?", r"b) [NB] Mô tả không gian mẫu của phép thử.",
              r"c) [TH] Tính xác suất của các biến cố $M$ và $N$."),
     "a) Phép thử: Giang và Ngân, mỗi bạn chọn ngẫu nhiên một khu vực. b) Kết quả là cặp (x, y), x là khu Giang chọn, "
     "y là khu Ngân chọn · bảng 3×3 [[bang: …]] · Ω có 9 phần tử. c) M: (A, A), (B, B), (C, C) ⇒ P(M)=3/9=1/3 · N: "
     "(A, A), (A, B), (A, C), (B, A), (C, A) ⇒ P(N)=5/9 · Vậy. Bỏ cụm 'để góp phần phủ xanh môi trường' của đề gốc "
     "(lời thừa)."),
    ("Mạch 8. Tự viết không gian mẫu rồi tính xác suất", "practice2", "heading"),
    ("Ví dụ 11.", "practice2", "", "", 0, "ck2-ngo-gia-tu-2025-d1-2", "", "vi_du",
     y(r"Viết ngẫu nhiên một số tự nhiên có hai chữ số nhỏ hơn $30$." + ng("ngt"),
       r"a) Viết tập hợp $\Omega$ tất cả các kết quả có thể xảy ra đối với số tự nhiên được viết ra.",
       r"b) Tính xác suất của biến cố $A$: " + q("Số tự nhiên được viết ra chia hết cho $6$") + "."),
     "a) Ω = {10; 11; 12; …; 29} · n(Ω) = 29 − 10 + 1 = 20 (nhắc số có hai chữ số nhỏ nhất là 10). b) A: 12, 18, 24 "
     "· P(A)=3/20 · Vậy. 6–8 ô."),
    ("Bài 20.", "practice2", "onclass", "NB6+TH2", 2, "gk2-nam-tu-liem-2025-I2", "", "th_dan",
     r"Viết ngẫu nhiên một số tự nhiên có hai chữ số lớn hơn $84$." + ng("ntl")
     + BR + y(r"a) [NB] Viết tập hợp $\Omega$ gồm các kết quả có thể xảy ra đối với số tự nhiên được viết ra.",
              r"b) [TH] Tính xác suất của biến cố $A$: " + q("Số tự nhiên được viết ra chia hết cho cả $2$ và $3$")
              + "."),
     "a) Ω = {85; 86; …; 99}, n(Ω)=15. b) Theo câu a) · số chia hết cho cả 2 và 3 là số chia hết cho 6: 90, 96 · "
     "P(A)=2/15 · Vậy."),
    ("Bài 21.", "practice2", "onclass", "NB6+TH2", 2, "v10-tho-loc-l3-2025-I2 (M, ý b)", "", "th_dan",
     r"Viết ngẫu nhiên một số tự nhiên có hai chữ số lớn hơn $40$." + ng("tll3")
     + BR + y(r"a) [NB] Tìm số phần tử của tập hợp $M$ gồm các kết quả có thể xảy ra đối với số tự nhiên được viết ra.",
              r"b) [TH] Tính xác suất của biến cố $A$: " + q("Số tự nhiên được viết ra là tổng của hai số tự nhiên "
                                                               r"liên tiếp") + "."),
     "hints: một câu hỏi gợi ý \"Tổng của hai số tự nhiên liên tiếp $n$ và $n+1$ là số chẵn hay số lẻ?\". a) M = {41; 42; "
     "…; 99}, n(M) = 99 − 41 + 1 = 59. b) n + (n + 1) = 2n + 1 là số lẻ, ngược lại mỗi số lẻ 2n+1 là tổng của n và n+1 "
     "· các số lẻ từ 41 đến 99: (99 − 41) : 2 + 1 = 30 số · P(A)=30/59 · Vậy."),
    ("Mạch 9. Xác suất với điều kiện số học — đề thi vào 10", "practice2", "heading"),
    ("Ví dụ 12.", "practice2", "", "", 0, "ck2-phuc-dong-2025-I2", "", "vi_du",
     r"Một hộp có $20$ viên bi với kích thước và khối lượng như nhau. Bạn Ngân viết lên các viên bi đó các số "
     r"$1, 2, 3, \ldots, 20$, hai viên bi khác nhau thì viết hai số khác nhau. Xét phép thử " + q("Lấy ngẫu nhiên một "
     r"viên bi trong hộp") + ". Tính xác suất của biến cố $A$: " + q("Số xuất hiện trên viên bi được lấy ra chia $7$ "
                                                                   r"dư $1$") + "." + ng("pd25"),
     "n(Ω)=20, đồng khả năng · số chia 7 dư 1 có dạng 7k+1: 1, 8, 15 (k = 0, 1, 2 — nhắc số 1 = 7·0 + 1 hay bị sót) "
     "· n(A)=3 · P(A)=3/20 · Vậy. 6–8 ô."),
    ("Bài 22.", "practice2", "onclass", "NB5+TH1", 2, "ck2-phuc-loi-2024-1-2", "", "th_dan",
     r"Hình bên mô tả một đĩa tròn bằng bìa cứng được chia làm $8$ phần bằng nhau và ghi các số $1$, $12$, $18$, "
     r"$22$, $27$, $69$, $96$, $99$, chiếc kim được gắn cố định vào trục quay ở tâm của đĩa. Xét phép thử "
     + q("Quay đĩa tròn một lần") + " và biến cố $M$: " + q("Chiếc kim chỉ vào hình quạt ghi số chia cho $5$ dư $2$")
     + "." + ng("pl")
     + DQ(DIA_PL, rong=0.24)
     + y(r"a) [NB] Số chia cho $5$ dư $2$ có chữ số tận cùng là những chữ số nào?",
         r"b) [TH] Tính xác suất của biến cố $M$."),
     "a) 2 hoặc 7. b) Theo câu a), các số chia cho 5 dư 2 trên đĩa là 12, 22, 27 · n(Ω)=8 · P(M)=3/8 · Vậy."),
    ("Bài 23.", "practice2", "onclass", "NB5+TH1", 2, "v10-tu-lap-2026-I2", "", "th_dan",
     r"Một hộp đựng $50$ cái thẻ cùng loại, mỗi thẻ được ghi một trong các số $50, 51, 52, \ldots, 98, 99$ (hai thẻ "
     r"khác nhau ghi hai số khác nhau). Rút ngẫu nhiên một thẻ từ hộp. Xét biến cố $A$: "
     + q("Số ghi trên thẻ rút được là một số chia cho $7$ dư $1$") + "." + ng("tl")
     + BR + y(r"a) [NB] Số $50$ chia cho $7$ dư bao nhiêu?", r"b) [TH] Tính xác suất của biến cố $A$."),
     "a) 50 = 7·7 + 1 nên dư 1. b) Theo câu a), 50 thuộc A, các số tiếp theo cách nhau 7: 50, 57, 64, 71, 78, 85, 92, "
     "99 · n(A)=8, n(Ω)=50 · P(A)=8/50=4/25 · Vậy."),
    ("Ví dụ 13.", "practice2", "", "", 0, "ck2-ngoc-thuy-2024-I2", "", "vi_du",
     r"Trong một hộp đựng $15$ tấm thẻ cùng loại đánh số từ $1$ đến $15$ và không có hai tấm thẻ nào đánh số trùng "
     r"nhau. An rút ngẫu nhiên một tấm thẻ trong hộp. Tính xác suất của biến cố $A$: " + q("An rút được tấm thẻ đánh "
     r"số chia hết cho $3$ và không vượt quá $10$") + "." + ng("nthuy"),
     "Thầy 19/11: thêm 'cùng loại'. n(Ω)=15 · số chia hết cho 3: 3, 6, 9, 12, 15 · trong đó không vượt quá 10 "
     "(≤ 10): 3, 6, 9 · P(A)=3/15=1/5 · Vậy. 6–8 ô."),
    ("Bài 24.", "practice2", "onclass", "NB5+TH1", 2, "so-hn-2025-I2 — ĐÍCH", "", "th_dan",
     r"Một hộp có $8$ chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, 4, 5, 6, 7, 8$, hai thẻ khác "
     r"nhau được ghi hai số khác nhau. Rút ngẫu nhiên một thẻ trong hộp. Xét biến cố $A$: "
     + q("Số ghi trên thẻ rút được là một số chia hết cho $3$") + "." + ng("hn25")
     + BR + y(r"a) [NB] Không gian mẫu của phép thử có bao nhiêu phần tử?", r"b) [TH] Tính xác suất của biến cố $A$."),
     "ĐÍCH (Câu I.2 đề vào 10 Hà Nội 2025). a) 8. b) Theo câu a), n(Ω)=8, các kết quả đồng khả năng · A gồm 3, 6 · "
     "P(A)=2/8=1/4 · Vậy. Trình bày đủ như bài thi."),
    # ───────────── BTVN — NB rồi TH (28 NB + 10 TH) ─────────────
    ("Bài 25.", "reflection", "btvn", "NB2", 1, "sgk-8.1 (ý a)", "", "tra_loi_ngan",
     r"[NB] Chọn ngẫu nhiên một gia đình có hai con và quan sát giới tính của hai người con đó. Phép thử và kết quả "
     r"của phép thử là gì?" + sgk("Bài tập 8{.}1"),
     "Phép thử: chọn ngẫu nhiên một gia đình có hai con, quan sát giới tính của hai người con. Kết quả là cặp (a, b), "
     "a là giới tính người con thứ nhất, b là giới tính người con thứ hai (mỗi người là trai hoặc gái)."),
    ("Bài 26.", "reflection", "btvn", "NB2", 1, "tl-ptnn-xsbc-17-tr5 (ý a, c)", "", "dung_sai",
     y(r"Mỗi khẳng định sau đúng hay sai? Giải thích." + ng("tlmt"),
       r"a) [NB] Rút ngẫu nhiên $1$ tấm thẻ từ $10$ tấm thẻ cùng loại được đánh số lần lượt từ $1$ đến $10$. Các kết quả "
       r"của phép thử là đồng khả năng.",
       r"b) [NB] Lấy ra ngẫu nhiên $1$ viên bi từ một hộp chứa $1$ viên bi xanh, $1$ viên bi đỏ và $8$ viên bi trắng có "
       r"cùng kích thước và khối lượng rồi quan sát màu của nó. Các kết quả của phép thử là đồng khả năng."),
     "a) Đúng: 10 thẻ cùng loại, mỗi số ghi trên đúng một thẻ. b) Sai: màu trắng có 8 viên, xanh và đỏ chỉ 1 viên "
     "nên khả năng lấy được bi trắng cao hơn."),
    ("Bài 27.", "reflection", "btvn", "NB3", 1, "gk2-nguyen-binh-khiem-2024-I2 (ý a)", "", "tra_loi_ngan",
     r"[NB] Một hộp có $12$ tấm thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, \ldots, 12$, hai thẻ khác "
     r"nhau thì ghi hai số khác nhau. Xét phép thử " + q("Rút ngẫu nhiên một thẻ trong hộp") + ". Viết không gian mẫu "
     r"của phép thử." + ng("nbk"),
     "Ω = {1; 2; 3; …; 12} (viết đủ 12 số), n(Ω)=12."),
    ("Bài 28.", "reflection", "btvn", "NB3", 1, "v10-lang-thuong-2025-II2 (ý a)", "", "tra_loi_ngan",
     r"[NB] Nhóm học sinh tình nguyện khối 9 của một trường trung học cơ sở có $6$ bạn, trong đó có $3$ bạn nam là "
     r"Trung (lớp 9A), Quý (lớp 9A), Việt (lớp 9C) và $3$ bạn nữ là An (lớp 9A), Châu (lớp 9B), Hương (lớp 9D). Chọn "
     r"ngẫu nhiên một bạn trong nhóm đó để tham gia hoạt động tình nguyện của trường. Liệt kê tất cả các kết quả có "
     r"thể xảy ra trong phép thử trên. Có tất cả bao nhiêu kết quả có thể xảy ra?" + ng("lt"),
     "Ω = {Trung; Quý; Việt; An; Châu; Hương}, có 6 kết quả."),
    ("Bài 29.", "reflection", "btvn", "NB3", 1, "tl-ptnn-xsbc-21-tr6 (M, N)", "", "tra_loi_ngan",
     r"Bảng sau biểu diễn kết quả thống kê của một bệnh viện về cân nặng của một số trẻ sơ sinh." + ng("tlmt")
     + B(["Cân nặng (g)", "$[2800; 3000)$", "$[3000; 3200)$", "$[3200; 3400)$", "$[3400; 3600)$", "Tổng số"],
         ["Bé gái", 4, 17, 10, 5, 36], ["Bé trai", 3, 18, 8, 3, 32])
     + r"Chọn ngẫu nhiên một trẻ sơ sinh trong số này."
     + BR + y(r"a) [NB] Có bao nhiêu kết quả thuận lợi cho biến cố $M$: "
              + q(r"Chọn được một bé gái có cân nặng thuộc nhóm $[3200; 3400)$ (g)") + "?",
              r"b) [NB] Có bao nhiêu kết quả thuận lợi cho biến cố $N$: "
              + q(r"Chọn được một bé có cân nặng dưới $3000$ g") + "?"),
     "a) 10. b) Nhóm [2800; 3000) của bé gái và bé trai: 4 + 3 = 7."),
    ("Bài 30.", "reflection", "btvn", "NB4", 1, "v10-tho-loc-l3-2026-I2 (ý a)", "", "trac_nghiem",
     r"[NB] Bạn An ném ngẫu nhiên một viên bi vào bảng gồm các ô vuông như hình bên. Biết rằng mỗi lần ném, viên bi "
     r"chỉ có thể nằm gọn vào một ô vuông màu trắng hoặc một ô vuông màu đen và việc viên bi nằm trong mỗi ô vuông là "
     r"đồng khả năng. Xác suất để trong $1$ lần ném, viên bi nằm trong ô vuông màu đen là" + ng("tll3b")
     + BC()
     + tn(r"$\dfrac{1}{64}$", r"$\dfrac{1}{2}$", r"$\dfrac{1}{32}$", r"$\dfrac{1}{4}$"),
     "Chọn B: 64 ô, 32 ô đen ⇒ 32/64 = 1/2. Chỉ bốc ý a. Đề gốc \"việc viên bi nằm trong ô trắng hay ô đen là đồng "
     "khả năng\" — sơ đồ viết lại \"nằm trong mỗi ô vuông là đồng khả năng\" cho đúng phép thử 64 kết quả."),
    ("Bài 31.", "reflection", "btvn", "NB4", 1, "ck2-ba-dinh-2024-I2", "", "tra_loi_ngan",
     r"[NB] Trên bàn học của An có $3$ quyển sách Toán, $3$ quyển sách Văn và $2$ quyển sách Tiếng Anh. An chọn ngẫu "
     r"nhiên $1$ quyển sách trên bàn đó để đọc (mỗi quyển sách đều có khả năng được chọn như nhau). Tính xác suất của "
     r"biến cố " + q("An chọn được sách Toán") + "." + ng("bd"),
     "n(Ω)=3+3+2=8, n=3 ⇒ P=3/8."),
    ("Bài 32.", "reflection", "btvn", "NB4", 1, "ck2-hai-ba-trung-2024-I2", "", "tra_loi_ngan",
     r"[NB] Trong một hộp có $20$ chiếc thẻ cùng loại, được ghi số từ $1$ đến $20$. Hai thẻ khác nhau ghi số khác nhau. "
     r"Bạn Hà rút ngẫu nhiên một thẻ trong hộp rồi ghi lại số. Tính xác suất của biến cố $A$: "
     + q("Số ghi trên thẻ là số lớn hơn $15$") + "." + ng("hbt"),
     "A: 16, 17, 18, 19, 20 ⇒ P(A)=5/20=1/4."),
    ("Bài 33.", "reflection", "btvn", "NB4", 1, "ck2-lomonoxop-2024-I2", "", "tra_loi_ngan",
     r"[NB] Một hộp có $18$ viên bi cùng loại được ghi số $1, 2, \ldots, 18$, hai viên bi khác nhau ghi hai số khác "
     r"nhau. Lấy ngẫu nhiên một viên bi trong hộp. Tìm xác suất của biến cố $M$: "
     + q("Viên bi được lấy có ghi số có hai chữ số") + "." + ng("lmns"),
     "M: 10, 11, …, 18 — 9 số ⇒ P(M)=9/18=1/2."),
    ("Bài 34.", "reflection", "btvn", "NB4", 1, "ck2-ngoc-lam-2024-T901-I2", "", "tra_loi_ngan",
     r"[NB] Một hộp có $20$ quả bóng được ghi số lần lượt từ $1$ đến $20$. Biết các quả bóng có cùng màu sắc, khối "
     r"lượng và kích thước. Bạn Nam lấy ngẫu nhiên một quả bóng trong hộp. Tính xác suất của biến cố "
     + q("Bạn Nam lấy được quả bóng có ghi số chia hết cho $4$") + "." + ng("nl"),
     "4, 8, 12, 16, 20 ⇒ 5/20 = 1/4."),
    ("Bài 35.", "reflection", "btvn", "NB4", 1, "ck2-phuc-dong-2024-902-I2", "", "tra_loi_ngan",
     r"[NB] Một bình đựng $20$ quả cầu có kích thước và khối lượng như nhau, được đánh số từ $1$ đến $20$ (không có hai "
     r"quả cầu nào đánh cùng một số). Chọn ngẫu nhiên một quả cầu. Tính xác suất của biến cố $A$: "
     + q("Chọn được quả cầu trên đó có ghi số chính phương") + "." + ng("pd24"),
     "1, 4, 9, 16 (1 = 1² là số chính phương) ⇒ P(A)=4/20=1/5."),
    ("Bài 36.", "reflection", "btvn", "NB4", 1, "gk2-nhat-tan-2024-I2", "", "tra_loi_ngan",
     r"[NB] Trong túi có $6$ quả bóng bàn được làm bằng cùng chất liệu, có kích thước và khối lượng như nhau, gồm hai "
     r"quả màu đỏ được đánh số $1$, $2$, hai quả màu trắng được đánh số $3$, $4$, hai quả màu xanh được đánh số $5$, "
     r"$6$. Lấy ngẫu nhiên một quả bóng từ trong túi. Tính xác suất của biến cố $A$: "
     + q("Không lấy được quả bóng màu đỏ") + "." + ng("nhtan"),
     "Không đỏ: 3, 4, 5, 6 ⇒ P(A)=4/6=2/3."),
    ("Bài 37.", "reflection", "btvn", "NB4", 1, "tl-ptnn-xsbc-38-tr9 (ý a)", "", "tra_loi_ngan",
     r"[NB] Một hộp chứa $15$ quả cầu màu xanh được đánh số từ $1$ đến $15$ và $5$ quả cầu màu đỏ được đánh số từ $16$ "
     r"đến $20$, các quả cầu có cùng kích thước và khối lượng. Lấy ngẫu nhiên một quả trong hộp. Tính xác suất của "
     r"biến cố " + q("Quả cầu được lấy ra có màu xanh") + "." + ng("tlmt"),
     "n(Ω)=20, 15 quả xanh ⇒ 15/20 = 3/4."),
    ("Bài 38.", "reflection", "btvn", "NB7", 1, "tl-ptnn-xsbc-76-tr15", "", "trac_nghiem",
     r"[NB] Một đoàn khách quốc tế tham quan vịnh Hạ Long có tỉ lệ khách người châu Âu là $27\%$. Chọn ngẫu nhiên một "
     r"hành khách trong đoàn khách đó. Xác suất của biến cố " + q("Hành khách được chọn là người châu Âu") + " là"
     + ng("tlmt") + tn("$27$", r"$\dfrac{73}{100}$", "$0{,}27$", r"$\dfrac{1}{27}$"),
     "Chọn C: P = 27% = 0,27."),
    ("Bài 39.", "reflection", "btvn", "NB9", 1, "v10-be-van-dan-2025-I2-md2 (ý a, b)", "", "tra_loi_ngan",
     r"Tung một đồng xu cân đối, đồng chất $2$ lần. Xét các biến cố $A$: " + q("Xuất hiện $2$ lần mặt ngửa")
     + " và $B$: " + q("Xuất hiện $1$ lần mặt sấp, $1$ lần mặt ngửa") + "." + ng("bvd2")
     + BR + y(r"a) [NB] Mô tả không gian mẫu.", r"b) [NB] Xác định các kết quả thuận lợi cho mỗi biến cố $A$ và $B$."),
     "a) Ω = {SS; SN; NS; NN} (hoặc cặp (S, S) …), 4 phần tử. b) A: NN · B: SN, NS."),
    ("Bài 40.", "reflection", "btvn", "NB5+TH1", 2, "gk2-trung-vuong-2025-I2", "", "th_dan",
     r"Một tấm bìa cứng hình tròn được chia thành $20$ hình quạt như nhau, đánh số $1, 2, 3, \ldots, 20$ và được gắn "
     r"vào trục quay có mũi tên cố định ở tâm (hình bên). Xét phép thử " + q("Quay đĩa tròn một lần") + " và biến cố "
     r"$A$: " + q("Số trên hình quạt mà mũi tên chỉ vào không phải là số nguyên tố") + "." + ng("tvg")
     + DQ(list(range(1, 21)), R=1.3, rong=0.26)
     + y(r"a) [NB] Từ $1$ đến $20$ có bao nhiêu số nguyên tố?", r"b) [TH] Tính xác suất của biến cố $A$."),
     "a) 2, 3, 5, 7, 11, 13, 17, 19 — 8 số. b) Theo câu a), số không phải số nguyên tố: 20 − 8 = 12 (kể cả số 1) · "
     "P(A)=12/20=3/5 · Vậy."),
    ("Bài 41.", "reflection", "btvn", "NB5+TH1", 2, "v10-khuong-thuong-2025-I2", "", "th_dan",
     r"Một hộp có $20$ chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1, 2, 3, \ldots, 20$, hai thẻ khác nhau "
     r"ghi hai số khác nhau. Rút ngẫu nhiên một thẻ trong hộp. Xét biến cố $A$: " + q("Số xuất hiện trên thẻ được rút "
     r"ra là số lẻ và chia hết cho $3$") + "." + ng("kt")
     + BR + y(r"a) [NB] Viết các số chia hết cho $3$ trong các số từ $1$ đến $20$.",
              r"b) [TH] Tính xác suất của biến cố $A$."),
     "a) 3, 6, 9, 12, 15, 18. b) Theo câu a), các số lẻ trong đó: 3, 9, 15 · P(A)=3/20 · Vậy."),
    ("Bài 42.", "reflection", "btvn", "NB5+TH1", 2, "v10-cau-giay-lan1-2026-I2", "", "th_dan",
     r"Trong hộp có $13$ quả bóng đỏ, $10$ quả bóng vàng và $80$ quả bóng trắng, các quả bóng có kích thước và khối "
     r"lượng như nhau. Lấy ngẫu nhiên một quả trong hộp. Xét biến cố $A$: " + q("Quả bóng lấy được không phải là màu "
     r"trắng") + "." + ng("cg")
     + BR + y(r"a) [NB] Trong hộp có tất cả bao nhiêu quả bóng?",
              r"b) [TH] Tính xác suất của biến cố $A$ (làm tròn kết quả đến hàng phần trăm)."),
     "a) 13+10+80 = 103. b) Theo câu a), không trắng: 13+10 = 23 · P(A)=23/103 ≈ 0,22 · Vậy."),
    ("Bài 43.", "reflection", "btvn", "NB6+TH2", 2, "ck2-trung-vuong-2025-I2", "", "th_dan",
     r"Viết ngẫu nhiên một số tự nhiên lẻ có hai chữ số và nhỏ hơn $40$. Xét biến cố $M$: "
     + q("Số tự nhiên được viết ra là bội của $3$") + "." + ng("tvc")
     + BR + y(r"a) [NB] Viết tập hợp $\Omega$ gồm các kết quả có thể xảy ra.", r"b) [TH] Tính xác suất của biến cố $M$."),
     "a) Ω = {11; 13; 15; …; 39}, n(Ω)=15. b) Theo câu a), M: 15, 21, 27, 33, 39 · P(M)=5/15=1/3 · Vậy."),
    ("Bài 44.", "reflection", "btvn", "NB6+TH2", 2, "tl-ptnn-xsbc-51-tr12 (ý a, B)", "", "th_dan",
     r"Viết ngẫu nhiên một số tự nhiên có hai chữ số không nhỏ hơn $80$. Xét biến cố $A$: "
     + q("Số tự nhiên được viết ra có chữ số hàng chục gấp hai hoặc gấp ba lần chữ số hàng đơn vị") + "." + ng("tlmt")
     + BR + y(r"a) [NB] Viết tập hợp $\Omega$ gồm các kết quả có thể xảy ra.", r"b) [TH] Tính xác suất của biến cố $A$."),
     "Biến cố B của đề gốc đổi tên thành A. a) Ω = {80; 81; …; 99}, n(Ω)=20 (không nhỏ hơn 80 ⇒ lấy cả 80). "
     "b) Gấp hai: 84 · gấp ba: 93 (80 có hàng đơn vị 0, không tính; 90 cũng vậy) · P(A)=2/20=1/10 · Vậy."),
    ("Bài 45.", "reflection", "btvn", "NB8+TH3", 2, "gk2-chuong-duong-2024-I2", "", "th_dan",
     r"Kết quả đo chiều cao của $40$ học sinh (đơn vị: cm) được thống kê trong bảng sau." + ng("cd24")
     + L(CAO_CD, 10)
     + y(r"a) [NB] Có bao nhiêu học sinh có chiều cao từ $158$ cm trở lên?",
         r"b) [TH] Chọn một học sinh bất kì trong $40$ học sinh trên. Tính xác suất để chọn được học sinh có chiều cao "
         r"từ $1$ m $58$ trở lên."),
     "a) Đếm theo từng giá trị: 158 (3), 160 (1), 162 (1), 163 (5), 164 (1), 165 (1), 167 (1), 168 (2), 170 (1) ⇒ 16. "
     "b) Theo câu a), 1 m 58 = 158 cm · P = 16/40 = 2/5 · Vậy."),
    ("Bài 46.", "reflection", "btvn", "NB10+TH4", 2, "sgk-8.8", "", "th_dan",
     r"Có hai túi I và II, mỗi túi chứa $4$ tấm thẻ được đánh số $1$, $2$, $3$, $4$. Rút ngẫu nhiên từ mỗi túi ra một "
     r"tấm thẻ và nhân hai số ghi trên hai tấm thẻ với nhau. Xét các biến cố $A$: " + q("Kết quả là một số lẻ")
     + " và $B$: " + q("Kết quả là $1$ hoặc một số nguyên tố") + "." + sgk("Bài tập 8{.}8")
     + BR + y(r"a) [NB] Không gian mẫu của phép thử có bao nhiêu phần tử?",
              r"b) [TH] Tính xác suất của các biến cố $A$ và $B$."),
     "a) 4·4 = 16. b) Bảng tích 4×4 [[bang: …]] · A: (1, 1), (1, 3), (3, 1), (3, 3) ⇒ P(A)=4/16=1/4 · B: tích 1, 2, 3: "
     "(1, 1), (1, 2), (2, 1), (1, 3), (3, 1) ⇒ P(B)=5/16 · Vậy."),
    ("Bài 47.", "reflection", "btvn", "NB10+TH4", 2, "sgk-8.9", "", "th_dan",
     r"Có hai túi đựng các tấm thẻ. Túi I đựng $4$ tấm thẻ ghi các chữ cái TT, TH, HT và HH. Túi II đựng $2$ tấm thẻ "
     r"ghi các chữ cái T và H. Từ mỗi túi rút ngẫu nhiên ra một tấm thẻ rồi ghép hai thẻ lại với nhau để được ba chữ "
     r"cái, trong đó thẻ hai chữ cái đặt trước, chẳng hạn tấm thẻ TT ghép với tấm thẻ H được ba chữ cái TTH. Xét các "
     r"biến cố $E$: " + q("Trong ba chữ cái, có hai chữ H và một chữ T") + " và $F$: "
     + q("Trong ba chữ cái, có nhiều nhất hai chữ T") + "." + sgk("Bài tập 8{.}9")
     + BR + y(r"a) [NB] Viết tất cả các kết quả có thể của phép thử.",
              r"b) [TH] Tính xác suất của các biến cố $E$ và $F$."),
     "a) TTT, TTH, THT, THH, HTT, HTH, HHT, HHH — 8 kết quả. b) E: THH, HTH, HHT ⇒ P(E)=3/8 · F: mọi kết quả trừ TTT "
     "⇒ 7 kết quả ⇒ P(F)=7/8 · Vậy."),
    ("Bài 48.", "reflection", "btvn", "NB10+TH4", 2, "sgk-8.10 (H, K)", "", "th_dan",
     XX + r" Xét các biến cố $A$: " + q("Số chấm xuất hiện trên con xúc xắc I là số lẻ và số chấm xuất hiện trên con "
                                         r"xúc xắc II lớn hơn $4$") + " và $B$: "
     + q("Số chấm xuất hiện trên cả hai con xúc xắc lớn hơn $2$") + "." + sgk("Bài tập 8{.}10")
     + BR + y(r"a) [NB] Không gian mẫu của phép thử có bao nhiêu phần tử?",
              r"b) [TH] Tính xác suất của các biến cố $A$ và $B$."),
     "Biến cố H, K của SGK đổi tên thành A, B. a) 36. b) A: con I ∈ {1, 3, 5}, con II ∈ {5, 6} ⇒ 3·2 = 6 cặp, liệt kê "
     "⇒ P(A)=6/36=1/6 · B: mỗi con ∈ {3, 4, 5, 6} ⇒ 4·4 = 16 cặp ⇒ P(B)=16/36=4/9 · Vậy."),
    ("Bài 49.", "reflection", "btvn", "NB10+TH4", 2, "tl-ptnn-xsbc-67-tr14 (ý a, P, Q)", "", "th_dan",
     r"Trên mặt phẳng cho năm điểm phân biệt $A$, $B$, $C$, $D$, $E$, trong đó không có ba điểm nào thẳng hàng. Hai "
     r"điểm $A$, $B$ được tô màu đỏ, ba điểm $C$, $D$, $E$ được tô màu xanh. Bạn Châu chọn ra ngẫu nhiên một điểm tô màu "
     r"đỏ và một điểm tô màu xanh để nối thành một đoạn thẳng. Xét các biến cố $M$: "
     + q("Trong hai điểm chọn ra, có điểm $A$") + " và $N$: " + q("Trong hai điểm chọn ra, không có điểm $C$") + "."
     + ng("tlmt")
     + BR + y(r"a) [NB] Liệt kê các cách chọn mà bạn Châu thực hiện.",
              r"b) [TH] Tính xác suất của các biến cố $M$ và $N$."),
     "Biến cố P, Q của đề gốc đổi tên thành M, N (tránh viết P(P)). a) AC, AD, AE, BC, BD, BE — 6 cách. b) M: AC, AD, "
     "AE ⇒ P(M)=3/6=1/2 · N: AD, AE, BD, BE ⇒ P(N)=4/6=2/3 · Vậy."),
]

DAP_TN = {"Bài 1.": "D", "Bài 5.": "A", "Bài 8.": "B", "Bài 9.": "C", "Bài 10.": "D", "Bài 11.": "B",
          "Bài 30.": "B", "Bài 38.": "C"}
DAP_DS = {"Bài 3.": "ĐS", "Bài 26.": "ĐS"}
OPTIONS: dict = {}
NGAN = {"Bài 2.", "Bài 4.", "Bài 6.", "Bài 7.", "Bài 12.", "Bài 25.", "Bài 27.", "Bài 28.", "Bài 29.", "Bài 39.",
        "Bài 31.", "Bài 32.", "Bài 33.", "Bài 34.", "Bài 35.", "Bài 36.", "Bài 37."}

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu 1 (19/11)
    "NB1": (2, 0), "NB2": (4, 3), "NB3": (7, 4), "NB4": (3, 8), "NB5": (3, 3), "NB6": (2, 2), "NB7": (1, 1),
    "NB8": (2, 1), "NB9": (1, 2), "NB10": (7, 4),
    "TH1": (3, 3), "TH2": (2, 2), "TH3": (2, 1), "TH4": (3, 4), "TH5": (2, 0),
}


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
    bang("VD2 bội 5", [x for x in r(1, 17) if x % 5 == 0], [5, 10, 15])
    bang("VD2 ước 14", [x for x in r(1, 17) if 14 % x == 0], [1, 2, 7, 14])
    bang("VD5", (F(20, 60), F(len([x for x in r(1, 53) if x < 27]), 52)), (F(1, 3), F(1, 2)))
    bang("B8", p([x for x in r(1, 7) if x % 2 == 0], 6), F(1, 2))
    bang("B9", p([x for x in r(1, 9) if x > 3], 8), F(5, 8))
    bang("VD6", F(30 - 18, 30), F(2, 5))
    bang("B10", F(15, 20), F(3, 4))
    bang("B11", (3 + 7 + 9 + 10 + 6 + 1, F(9, 36) * 100), (36, 25))
    bang("B12", F(32, 552), F(4, 69))
    bang("VD8", (F(15, 100), F(100 - 45, 100)), (F(3, 20), F(11, 20)))
    bang("B13", F(3 + 5, sum([3, 5, 6, 7, 9, 10])), F(1, 5))
    bang("B14", (F(21, 42), F(9, 42), sum([12, 4, 5, 10, 5, 6])), (F(1, 2), F(3, 14), 42))
    O = list(itertools.product(r(1, 4), r(1, 4)))
    bang("B15", len(O), 9)
    bang("VD9", (p([1 for a in (2, 3, 4) for b in (5, 6) if abs(a - b) == 2], 6),
                 p([1 for a in (2, 3, 4) for b in (5, 6) if nt(a + b)], 6)), (F(1, 3), F(1, 6)))
    XX2 = list(itertools.product(r(1, 7), r(1, 7)))
    bang("B16", (p([o for o in XX2 if o.count(6) == 1], 36), p([o for o in XX2 if 6 in o], 36)), (F(5, 18), F(11, 36)))
    DX = list(itertools.product("SN", r(1, 6)))
    bang("B17", (p([o for o in DX if o[0] == "S" and o[1] % 2 == 0], 10),
                 p([o for o in DX if o[1] == 5 or o[0] == "N"], 10)), (F(1, 5), F(3, 5)))
    so = [10 * a + b for a in (2, 3, 7) for b in (2, 3, 7)]
    bang("VD10", p([x for x in so if nt(x)], 9), F(1, 3))
    so = [10 * a + b for a in (1, 5, 9) for b in (1, 5, 9)]
    bang("B18", ([x for x in so if x % 5 == 0], p([x for x in so if nt(x)], 9)), ([15, 55, 95], F(1, 3)))
    KV = list(itertools.product("ABC", "ABC"))
    bang("B19", (p([o for o in KV if o[0] == o[1]], 9), p([o for o in KV if "A" in o], 9)), (F(1, 3), F(5, 9)))
    bang("VD11", (len(r(10, 30)), p([x for x in r(10, 30) if x % 6 == 0], 20)), (20, F(3, 20)))
    bang("B20", (len(r(85, 100)), p([x for x in r(85, 100) if x % 6 == 0], 15)), (15, F(2, 15)))
    bang("B21", (len(r(41, 100)), p([x for x in r(41, 100) if x % 2], 59)), (59, F(30, 59)))
    bang("VD12", p([x for x in r(1, 21) if x % 7 == 1], 20), F(3, 20))
    bang("B22", p([x for x in DIA_PL if x % 5 == 2], 8), F(3, 8))
    bang("B23", (50 % 7, p([x for x in r(50, 100) if x % 7 == 1], 50)), (1, F(4, 25)))
    bang("VD13", p([x for x in r(1, 16) if x % 3 == 0 and x <= 10], 15), F(1, 5))
    bang("B24", p([x for x in r(1, 9) if x % 3 == 0], 8), F(1, 4))
    bang("B29", (10, 4 + 3), (10, 7))
    bang("B31-37", [F(3, 8), p([x for x in r(1, 21) if x > 15], 20), p([x for x in r(1, 19) if x >= 10], 18),
                    p([x for x in r(1, 21) if x % 4 == 0], 20), p([x for x in r(1, 21) if int(x ** 0.5) ** 2 == x], 20),
                    F(4, 6), F(15, 20)],
         [F(3, 8), F(1, 4), F(1, 2), F(1, 4), F(1, 5), F(2, 3), F(3, 4)])
    bang("B40", (len([x for x in r(1, 21) if nt(x)]), p([x for x in r(1, 21) if not nt(x)], 20)), (8, F(3, 5)))
    bang("B41", p([x for x in r(1, 21) if x % 2 and x % 3 == 0], 20), F(3, 20))
    bang("B42", round(23 / 103, 2), 0.22)
    bang("B43", (len(r(11, 40, 2)), p([x for x in r(11, 40, 2) if x % 3 == 0], 15)), (15, F(1, 3)))
    bang("B44", p([x for x in r(80, 100) if x % 10 and (x // 10 in (2 * (x % 10), 3 * (x % 10)))], 20), F(1, 10))
    bang("B45", (len(CAO_CD), sum(1 for v in CAO_CD if v >= 158)), (40, 16))
    T4 = list(itertools.product(r(1, 5), r(1, 5)))
    bang("B46", (p([o for o in T4 if o[0] * o[1] % 2], 16), p([o for o in T4 if o[0] * o[1] == 1 or nt(o[0] * o[1])], 16)),
         (F(1, 4), F(5, 16)))
    BA = [a + b for a in ("TT", "TH", "HT", "HH") for b in "TH"]
    bang("B47", (p([s for s in BA if s.count("H") == 2], 8), p([s for s in BA if s.count("T") <= 2], 8)), (F(3, 8), F(7, 8)))
    bang("B48", (p([o for o in XX2 if o[0] % 2 and o[1] > 4], 36), p([o for o in XX2 if min(o) > 2], 36)), (F(1, 6), F(4, 9)))
    CH = list(itertools.product("AB", "CDE"))
    bang("B49", (p([o for o in CH if "A" in o], 6), p([o for o in CH if "C" not in o], 6)), (F(1, 2), F(2, 3)))
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
        tong[(re.match(r"[A-Z]+", d)[0], tier)] += n
    return loi, dict(tong)


if __name__ == "__main__":
    l1 = kiem()
    l2, tong = dem_the()
    print("thẻ:", tong, "· số hình/bảng:", len(_HINH))
    for l in l1 + l2:
        print("✗", l)
    print("SẠCH" if not (l1 + l2) else f"{len(l1 + l2)} lỗi")
    sys.exit(1 if (l1 + l2) else 0)
