"""Cổng NHÃN HÌNH BỊ NÉT VẼ ĐÈ — góp ý chương V lớp 9C (26/09/2026).

Người chấm: *"Tránh để tên điểm bị đường thẳng đè qua"*. Mắt người dò lỗi này trên
bản in thì sót (chương V có hơn 150 hình), mà `figure_gate`/`test_tikz_goc_vuong`
chỉ soi quan hệ hình học, không soi chữ. Cổng này đọc mã TikZ, ước lượng HỘP CHỮ của
từng nhãn (`\\node[...] at (…) {$A$}` hoặc `… node[...]{$A$}` đi sau một điểm) rồi dò
xem có đoạn thẳng / đường tròn / cung nào cắt ngang hộp đó không.

Chỉ hiểu những lối viết đang dùng trong kho: toạ độ số `(x,y)`, toạ độ cực `(a:r)`,
tên điểm khai bằng `\\coordinate`, `--`, `-- cycle`, `circle (r)`, `arc (a:b:r)`.
Gặp thứ không đọc được (`\\foreach`, `calc`, `pic`…) thì BỎ QUA nét đó chứ không đoán —
cổng chỉ CẢNH BÁO, thà sót còn hơn kêu oan.
"""
from __future__ import annotations

import math
import re

from src.schema import LessonPackage

# Cỡ chữ nhãn trong đơn vị TikZ (cm) — đo trên bản in (nền 12pt nên \small ≈ 11pt): một
# chữ cái in nghiêng cỡ \small rộng ≈ 0,26 cm, cao ≈ 0,3 cm; nhãn nhiều ký tự ("4 m",
# "30 cm") mỗi ký tự ≈ 0,22 cm kể cả dấu cách. \scriptsize nhỏ hơn ~25 %.
_W_CHU = {"tiny": 0.15, "scriptsize": 0.19, "footnotesize": 0.22, "small": 0.26, "normalsize": 0.28}
_H_CHU = {"tiny": 0.19, "scriptsize": 0.23, "footnotesize": 0.27, "small": 0.3, "normalsize": 0.33}
_INNER_SEP = 0.1176        # 0.3333em ở cỡ \small ≈ 3.33pt ≈ 0.1176 cm
_PT = 0.03515               # 1pt theo cm
_CO = 0.025                 # co hộp chữ vào một chút: nét chỉ LƯỚT mép thì không tính

_SO = r"-?\d*\.?\d+"
_TIKZ = re.compile(r"\\begin\{tikzpicture\}(\[[^\]]*\])?(.*?)\\end\{tikzpicture\}", re.S)
_COORD_DEF = re.compile(r"\\coordinate\s*\((\w+)\)\s*at\s*\(([^()]*)\)\s*;")
_DIEM = re.compile(r"\(\s*(" + _SO + r")\s*,\s*(" + _SO + r")\s*\)|\(\s*(" + _SO + r")\s*:\s*(" + _SO
                   + r")\s*\)|\(\s*([A-Za-z]\w*'?)\s*\)")


def _font(opts: str, mac_dinh: str) -> str:
    m = re.search(r"font\s*=\s*\\(tiny|scriptsize|footnotesize|small|normalsize)", opts or "")
    return m.group(1) if m else mac_dinh


def _doc_diem(tok: re.Match, ten: dict) -> tuple[float, float] | None:
    if tok.group(1) is not None:
        return float(tok.group(1)), float(tok.group(2))
    if tok.group(3) is not None:
        a, r = math.radians(float(tok.group(3))), float(tok.group(4))
        return r * math.cos(a), r * math.sin(a)
    return ten.get(tok.group(5))


def _chu_hien(txt: str) -> str:
    """Chữ thực sự in ra của nhãn (bỏ $, lệnh, ngoặc) để ước bề rộng."""
    s = re.sub(r"\\(?:text|mathrm|textit|textbf)\{([^{}]*)\}", r"\1", txt)
    s = re.sub(r"\\[a-zA-Z]+", "x", s)
    # Khoảng trắng giữa số và đơn vị ("2 m") vẫn chiếm chỗ trên bản in — giữ lại một ký tự.
    s = re.sub(r"\s+", " ", s.strip())
    return re.sub(r"[${}^_]", "", s)


def _hop_chu(p, opts: str, txt: str, font: str):
    """Hộp chữ (x0, y0, x1, y1) của một node đặt tại điểm `p` với tuỳ chọn `opts`."""
    font = _font(opts, font)
    n = max(1, len(_chu_hien(txt)))
    h = _H_CHU[font]
    w = _W_CHU[font] if n == 1 else _W_CHU[font] * 0.85 * n + 0.04
    sep = 0.0 if re.search(r"inner\s*sep\s*=\s*0", opts) else _INNER_SEP
    dx = dy = 0.0
    # "above=3pt" → khoảng cách THÊM so với mặc định.
    def _them(k: str) -> float:
        m = re.search(k + r"\s*=\s*(" + _SO + r")\s*(pt|cm|mm)?", opts)
        if not m:
            return 0.0
        v, u = float(m.group(1)), (m.group(2) or "cm")
        return v * {"pt": _PT, "cm": 1.0, "mm": 0.1}[u]
    tren = re.search(r"\babove\b", opts)
    duoi = re.search(r"\bbelow\b", opts)
    trai = re.search(r"\bleft\b", opts)
    phai = re.search(r"\bright\b", opts)
    x, y = p
    if tren:
        dy = sep + h / 2 + _them("above")
    elif duoi:
        dy = -(sep + h / 2 + _them("below"))
    if trai:
        dx = -(sep + w / 2 + _them("left"))
    elif phai:
        dx = sep + w / 2 + _them("right")
    cx, cy = x + dx, y + dy
    return (cx - w / 2 + _CO, cy - h / 2 + _CO, cx + w / 2 - _CO, cy + h / 2 - _CO)


def _cat_doan(hop, a, b) -> bool:
    """Đoạn a–b có cắt hộp chữ không (Liang–Barsky)."""
    x0, y0, x1, y1 = hop
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return False
    return True


def _cat_tron(hop, c, r) -> bool:
    x0, y0, x1, y1 = hop
    gan = math.hypot(min(max(c[0], x0), x1) - c[0], min(max(c[1], y0), y1) - c[1])
    xa = max(math.hypot(x - c[0], y - c[1]) for x in (x0, x1) for y in (y0, y1))
    return gan < r < xa


def _net_ve(body: str, ten: dict):
    """Các đoạn (a, b) và đường tròn (c, r) của mọi lệnh \\draw (bỏ lệnh không đọc được)."""
    doan, tron = [], []
    for m in re.finditer(r"\\(draw|filldraw)\s*(\[[^\]]*\])?(.*?);", body, re.S):
        than = m.group(3)
        if "foreach" in than or "$" in re.sub(r"\{[^{}]*\}", "", than) or "pic" in than:
            continue
        than = re.sub(r"node\s*(\[[^\]]*\])?\s*\{[^{}]*\}", " ", than)
        truoc, dau, cuoi_cycle = None, None, False
        pos = 0
        while pos < len(than):
            mc = re.match(r"\s*circle\s*\(\s*(" + _SO + r")\s*(pt|cm)?\s*\)", than[pos:])
            if mc:
                r = float(mc.group(1)) * (_PT if mc.group(2) == "pt" else 1.0)
                if truoc and r > 0.08:
                    tron.append((truoc, r))
                pos += mc.end()
                continue
            ma = re.match(r"\s*arc\s*\(\s*(" + _SO + r")\s*:\s*(" + _SO + r")\s*:\s*(" + _SO + r")\s*\)", than[pos:])
            if ma and truoc:
                a0, a1, r = (float(ma.group(i)) for i in (1, 2, 3))
                cx = truoc[0] - r * math.cos(math.radians(a0))
                cy = truoc[1] - r * math.sin(math.radians(a0))
                k = max(4, int(abs(a1 - a0) / 8))
                pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / k)),
                        cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / k))) for i in range(k + 1)]
                doan += list(zip(pts, pts[1:]))
                truoc = pts[-1]
                pos += ma.end()
                continue
            mcy = re.match(r"\s*--\s*cycle", than[pos:])
            if mcy:
                if truoc and dau:
                    doan.append((truoc, dau))
                pos += mcy.end()
                continue
            md = re.match(r"\s*(--|-\||\|-)?\s*", than[pos:])
            noi = md.group(1) if md else None
            pos += md.end() if md else 0
            mp = _DIEM.match(than, pos)
            if not mp:
                pos += 1
                continue
            p = _doc_diem(mp, ten)
            pos = mp.end()
            if p is None:
                truoc = None
                continue
            if noi == "--" and truoc:
                doan.append((truoc, p))
            elif noi in ("-|", "|-") and truoc:
                goc = (p[0], truoc[1]) if noi == "-|" else (truoc[0], p[1])
                doan += [(truoc, goc), (goc, p)]
            if noi is None or dau is None:
                dau = p if noi is None else dau
            truoc = p
    return doan, tron


def _nhan(body: str, ten: dict, font: str):
    """[(chữ, hộp)] cho mọi nhãn chữ đặt tại một điểm đọc được."""
    out = []
    for m in re.finditer(r"\\node\s*(\[[^\]]*\])?\s*at\s*(\([^()]*\))\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", body):
        mp = _DIEM.match(m.group(2))
        p = _doc_diem(mp, ten) if mp else None
        # Nhãn có NỀN TRẮNG (số trên mặt đồng hồ…) vẽ đè lên nét nên vẫn đọc được — bỏ qua.
        if p is not None and m.group(3).strip() and "fill=white" not in (m.group(1) or "").replace(" ", ""):
            out.append((m.group(3), _hop_chu(p, m.group(1) or "", m.group(3), font)))
    for m in re.finditer(r"(\([^()]*\))\s*(?:circle\s*\([^()]*\)\s*)?node\s*(\[[^\]]*\])\s*\{([^{}]*)\}", body):
        mp = _DIEM.match(m.group(1))
        p = _doc_diem(mp, ten) if mp else None
        if p is not None and m.group(3).strip():
            out.append((m.group(3), _hop_chu(p, m.group(2) or "", m.group(3), font)))
    return out


def nhan_bi_de(tikz: str) -> list[str]:
    """Danh sách nhãn (chữ) bị nét vẽ cắt ngang trong một hình TikZ."""
    out: list[str] = []
    for m in _TIKZ.finditer(tikz or ""):
        font = _font(m.group(1) or "", "small")
        body = m.group(2)
        ten = {}
        for c in _COORD_DEF.finditer(body):
            mp = _DIEM.match("(" + c.group(2) + ")")
            p = _doc_diem(mp, ten) if mp else None
            if p is not None:
                ten[c.group(1)] = p
        doan, tron = _net_ve(body, ten)
        for chu, hop in _nhan(body, ten, font):
            if any(_cat_doan(hop, a, b) for a, b in doan) or any(_cat_tron(hop, c, r) for c, r in tron):
                out.append(chu.strip())
    return out


def _hinh_cua(b):
    """(nhãn khối, mã tikz) của mọi hình trong một block."""
    ten = getattr(b, "label", "") or (getattr(b, "text", "") or "")[:30]
    fig = getattr(b, "figure", None)
    if fig is not None and getattr(fig, "tikz", ""):
        yield ten, fig.tikz
    if getattr(b, "type", "") == "figure" and getattr(b, "tikz", ""):
        yield (getattr(b, "caption", "") or "hình lý thuyết")[:40], b.tikz
    for attr in ("statement", "text", "solution", "answer"):
        s = getattr(b, attr, "") or ""
        if "tikzpicture" in s:
            yield ten, s


def check_nhan_hinh(lesson: LessonPackage) -> list[str]:
    """Cảnh báo nhãn điểm bị đoạn thẳng / đường tròn cắt ngang."""
    out: list[str] = []
    for st in lesson.stages:
        for b in st.blocks:
            for ten, tikz in _hinh_cua(b):
                bi = nhan_bi_de(tikz)
                if bi:
                    ten = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", ten).strip()
                    out.append(f"nhan_hinh: {ten} — nhãn {', '.join(dict.fromkeys(bi))} bị nét vẽ "
                               f"đè qua. Dời nhãn ra góc trống (đổi hướng/khoảng cách), đừng đổi toạ độ điểm.")
    return out
