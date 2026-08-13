"""Soi HÌNH HỌC của TikZ trong phiếu: chỗ nào vẽ ô ký hiệu góc vuông thì hai cạnh
THẬT của góc đó trên hình phải vuông góc với nhau.

Vì sao có test này: 2026-08-13 Thầy bắt được 4 hình ở phiếu A chương V có "góc vuông"
thực tế 98°–114° — đỉnh đặt bằng mắt chứ không tính, nên định lí Thales bị vi phạm
ngay trên bản in (tam giác khai là vuông nhưng vẽ ra thì không). `figure_gate` chỉ soi
đề↔hình có khớp nhau không, KHÔNG đọc toạ độ, nên lỗi lọt qua toàn bộ cổng.

Cách soi: ô ký hiệu góc vuông tự nó luôn vuông (do sinh bằng công thức), nên bằng chứng
nằm ở chỗ khác — **hai cạnh của ô phải nằm dọc theo hai đoạn thẳng THẬT được vẽ từ đỉnh**.
Nếu hình vẽ sai, hai cạnh vuông góc của ô sẽ không tìm được đoạn thẳng nào khớp hướng.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import pytest

SEEDS = Path(__file__).resolve().parents[1] / "inputs" / "seeds"

_NUM = r"-?\d+(?:\.\d+)?"
_PT = rf"\(\s*({_NUM})\s*,\s*({_NUM})\s*\)"
_SQUARE = re.compile(rf"\\draw\[ink\]\s*{_PT}\s*--\s*{_PT}\s*--\s*{_PT}\s*;")
# Đường gấp khúc thường (2 điểm trở lên) — nhận MỌI tuỳ chọn \draw[...], không riêng
# [ink]: phiếu lớp 7 vẽ đường thẳng bằng [brand,line width=…] nên lọc theo "ink" là sót.
_PATH = re.compile(rf"\\draw\[[^\]]*\]\s*((?:{_PT}\s*--\s*)+(?:{_PT}|cycle))")
_PT_ONLY = re.compile(_PT)

TOL_GOC = 2.5      # độ — sai số cho phép giữa hướng cạnh ô và hướng đoạn thẳng thật
TOL_DIEM = 0.04    # đơn vị vẽ — sai số cho phép khi coi hai điểm là trùng nhau


def _tikz_blocks(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    for st in d.get("stages", []):
        for b in st.get("blocks", []):
            for k in ("statement", "text"):
                v = b.get(k)
                if isinstance(v, str) and "tikzpicture" in v:
                    for m in re.finditer(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", v, re.S):
                        hinh = re.search(r"Hình (\d+)", v)
                        yield (b.get("label") or "?"), (hinh.group(1) if hinh else "?"), m.group(0)


def _phieu_files():
    return sorted(SEEDS.rglob("phieu-*.json"))


def _marks(tikz: str):
    """Ô ký hiệu góc vuông: polyline 3 điểm, hai cạnh ngắn và bằng nhau.
    Trả (đỉnh, hướng cạnh 1, hướng cạnh 2, độ lệch khỏi vuông tính bằng độ)."""
    out = []
    for m in _SQUARE.finditer(tikz):
        p1 = (float(m.group(1)), float(m.group(2)))
        p2 = (float(m.group(3)), float(m.group(4)))
        p3 = (float(m.group(5)), float(m.group(6)))
        u = (p2[0] - p1[0], p2[1] - p1[1])
        w = (p3[0] - p2[0], p3[1] - p2[1])
        lu, lw = math.hypot(*u), math.hypot(*w)
        if not (1e-9 < lu <= 0.4 and 1e-9 < lw <= 0.4) or abs(lu - lw) > 0.05:
            continue
        cos = (u[0] * w[0] + u[1] * w[1]) / (lu * lw)
        lech = 90 - math.degrees(math.acos(max(-1.0, min(1.0, abs(cos)))))
        V = (p1[0] - p2[0] + p3[0], p1[1] - p2[1] + p3[1])
        a = ((p1[0] - V[0]) / lw, (p1[1] - V[1]) / lw)
        b = ((p3[0] - V[0]) / lu, (p3[1] - V[1]) / lu)
        out.append((V, a, b, lech, (p1, p2, p3)))
    return out


def _segments(tikz: str):
    """Mọi đoạn thẳng thật của hình (bỏ chính các ô ký hiệu góc vuông)."""
    segs = []
    for m in _PATH.finditer(tikz):
        pts = [(float(x), float(y)) for x, y in _PT_ONLY.findall(m.group(1))]
        if m.group(1).rstrip().endswith("cycle") and len(pts) > 2:
            pts.append(pts[0])          # '-- cycle' đóng kín: cạnh cuối hay bị bỏ sót
        for p, q in zip(pts, pts[1:]):
            if math.dist(p, q) > 0.45:      # ô ký hiệu có cạnh ≤0,4 ⇒ loại ra
                segs.append((p, q))
    return segs


def _huong_tu_dinh(V, segs):
    """Hướng của các đoạn thẳng đi ra từ điểm V (kể cả khi V nằm giữa đoạn)."""
    dirs = []
    for p, q in segs:
        for x, y in ((p, q), (q, p)):
            if math.dist(V, x) <= TOL_DIEM:
                d = math.dist(x, y)
                if d > 1e-9:
                    dirs.append(((y[0] - x[0]) / d, (y[1] - x[1]) / d))
        # V nằm trong lòng đoạn thẳng ⇒ đoạn toả ra hai phía
        dpq = math.dist(p, q)
        if dpq > 1e-9:
            t = ((V[0] - p[0]) * (q[0] - p[0]) + (V[1] - p[1]) * (q[1] - p[1])) / dpq ** 2
            if 0.02 < t < 0.98:
                proj = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
                if math.dist(V, proj) <= TOL_DIEM:
                    u = ((q[0] - p[0]) / dpq, (q[1] - p[1]) / dpq)
                    dirs += [u, (-u[0], -u[1])]
    return dirs


def _khop(d, dirs):
    for e in dirs:
        c = max(-1.0, min(1.0, d[0] * e[0] + d[1] * e[1]))
        if math.degrees(math.acos(c)) <= TOL_GOC:
            return True
    return False


@pytest.mark.parametrize("path", _phieu_files(), ids=lambda p: p.stem[:38])
def test_o_ky_hieu_tu_no_phai_vuong(path: Path):
    """Bản thân ô ký hiệu phải là hình vuông (hai cạnh vuông góc, bằng nhau)."""
    loi = [f"{lab} · Hình {h}: ô góc vuông lệch {lech:.1f}° tại {pts[0]}"
           for lab, h, tikz in _tikz_blocks(path)
           for _V, _a, _b, lech, pts in _marks(tikz) if lech > 1.5]
    assert not loi, path.name + "\n" + "\n".join(loi)


@pytest.mark.parametrize("path", _phieu_files(), ids=lambda p: p.stem[:38])
def test_hai_canh_that_cua_goc_phai_vuong(path: Path):
    """Hai cạnh của ô ký hiệu phải nằm dọc theo hai đoạn thẳng THẬT vẽ từ đỉnh.

    Đây là phép soi bắt được lỗi 2026-08-13: nếu đỉnh đặt sai chỗ thì hai cạnh
    của tam giác tại đó KHÔNG vuông góc, nên ô vuông (vốn luôn vuông) sẽ có ít
    nhất một cạnh không khớp hướng đoạn thẳng nào."""
    loi = []
    for lab, h, tikz in _tikz_blocks(path):
        segs = _segments(tikz)
        for V, a, b, _lech, _pts in _marks(tikz):
            dirs = _huong_tu_dinh(V, segs)
            if not dirs:
                continue                       # đỉnh không nằm trên nét vẽ nào — bỏ qua
            thieu = [n for n, d in (("cạnh 1", a), ("cạnh 2", b)) if not _khop(d, dirs)]
            if thieu:
                loi.append(
                    f"{lab} · Hình {h}: đỉnh {tuple(round(x, 3) for x in V)} — "
                    f"{', '.join(thieu)} của ô góc vuông không nằm dọc cạnh nào của hình "
                    f"⇒ góc tại đỉnh KHÔNG vuông (hình vẽ sai so với đề)")
    assert not loi, path.name + "\n" + "\n".join(loi)
