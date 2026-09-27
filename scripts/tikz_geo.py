"""Sinh TikZ hình học có TOẠ ĐỘ TÍNH + NHÃN TỰ ĐẶT vào góc trống (không bị nét đè).

Dựng lại chương V lớp 9C (26/09/2026) sau góp ý "tránh để tên điểm bị đường thẳng đè qua".
Mọi hình xuất ra đều chạy qua `src.validators.nhan_hinh_gate.nhan_bi_de` để tự kiểm, ô góc
vuông tự kiểm 90°. Dùng:

    from scripts.tikz_geo import Fig, polar, tangent_points
    f = Fig(); f.circle((0, 0), 1.5); f.pt("O", (0, 0)); f.pt("A", polar(60, 1.5)); f.seg("O", "A")
    tikz = f.tikz()          # nhãn O, A tự đặt ra chỗ trống; nhãn bị đè thì báo lỗi ngay
"""
from __future__ import annotations

import math
import re

from src.validators.nhan_hinh_gate import _cat_doan, _cat_tron, nhan_bi_de

W1, H1 = 0.26, 0.3           # hộp một chữ cỡ \small (cm), nền 12pt


def polar(deg, r, c=(0.0, 0.0)):
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def f4(p):
    return f"({p[0]:.4f},{p[1]:.4f})"


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def norm(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def foot(p, a, b):
    """Chân đường vuông góc từ p xuống đường thẳng ab."""
    d = sub(b, a)
    t = ((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / (d[0] ** 2 + d[1] ** 2)
    return (a[0] + t * d[0], a[1] + t * d[1])


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def tangent_points(o, r, a):
    """Hai tiếp điểm từ điểm a ngoài (o, r)."""
    d = dist(o, a)
    base = math.degrees(math.atan2(a[1] - o[1], a[0] - o[0]))
    phi = math.degrees(math.acos(r / d))
    return polar(base + phi, r, o), polar(base - phi, r, o)


class Fig:
    def __init__(self, font="\\small", lw="0.8pt"):
        self.font, self.lw = font, lw
        self.P: dict[str, tuple] = {}
        self.cmds: list[str] = []
        self.segs: list[tuple] = []        # (a, b)
        self.circles: list[tuple] = []     # (c, r)
        self.boxes: list[tuple] = []       # hộp chữ đã đặt
        self.labels: list[tuple] = []      # (tên, chữ, hướng ép, khoảng)
        self.dots: list[str] = []
        self.free: list[tuple] = []        # nhãn tự do (chữ, điểm neo, hướng gợi ý)

    # ── điểm & nét ─────────────────────────────────────────────────────────
    def pt(self, name, xy, label=None, dot=True, where=None, d=None):
        self.P[name] = (float(xy[0]), float(xy[1]))
        if dot:
            self.dots.append(name)
        if label is not False:
            self.labels.append((name, label or f"${name}$", where, d))
        return self.P[name]

    def _p(self, x):
        return self.P[x] if isinstance(x, str) else x

    def seg(self, a, b, style="ink"):
        pa, pb = self._p(a), self._p(b)
        self.segs.append((pa, pb))
        self.cmds.append(f"  \\draw[{style}] {f4(pa)} -- {f4(pb)};")

    def line(self, a, b, ext=0.4, style="ink"):
        """Đường thẳng qua a, b kéo dài hai phía thêm `ext`."""
        pa, pb = self._p(a), self._p(b)
        u = norm(sub(pb, pa))
        self.seg(add(pa, mul(u, -ext)), add(pb, mul(u, ext)), style)

    def poly(self, *names, cycle=True, style="ink"):
        pts = [self._p(n) for n in names]
        for a, b in zip(pts, pts[1:] + ([pts[0]] if cycle else [])):
            self.segs.append((a, b))
        body = " -- ".join(f4(p) for p in pts) + (" -- cycle" if cycle else "")
        self.cmds.append(f"  \\draw[{style}] {body};")

    def circle(self, c, r, style="ink"):
        pc = self._p(c)
        self.circles.append((pc, r))
        self.cmds.append(f"  \\draw[{style}] {f4(pc)} circle ({r:.4f});")

    def arc(self, c, r, a0, a1, style="ink"):
        pc = self._p(c)
        s = polar(a0, r, pc)
        k = max(4, int(abs(a1 - a0) / 8))
        pts = [polar(a0 + (a1 - a0) * i / k, r, pc) for i in range(k + 1)]
        self.segs += list(zip(pts, pts[1:]))
        self.cmds.append(f"  \\draw[{style}] {f4(s)} arc ({a0:.4f}:{a1:.4f}:{r:.4f});")

    def fill_sector(self, c, r, a0, a1, style="brand!18"):
        pc = self._p(c)
        s = polar(a0, r, pc)
        self.cmds.insert(0, f"  \\fill[{style}] {f4(pc)} -- {f4(s)} arc ({a0:.4f}:{a1:.4f}:{r:.4f}) -- cycle;")

    def fill_raw(self, tikz):
        self.cmds.insert(0, "  " + tikz)

    def right(self, v, a, b, s=0.16):
        """Ô góc vuông tại v, hai cạnh dọc va, vb (kiểm 90°)."""
        pv, pa, pb = self._p(v), self._p(a), self._p(b)
        ua, ub = norm(sub(pa, pv)), norm(sub(pb, pv))
        assert abs(ua[0] * ub[0] + ua[1] * ub[1]) < 1e-3, f"góc tại {v} không vuông"
        p1, p3 = add(pv, mul(ua, s)), add(pv, mul(ub, s))
        p2 = add(p1, mul(ub, s))
        self.segs += [(p1, p2), (p2, p3)]
        self.cmds.append(f"  \\draw[ink] {f4(p1)} -- {f4(p2)} -- {f4(p3)};")

    def angle(self, v, a, b, r=0.35, text=None, style="brand"):
        """Cung đánh dấu góc a-v-b (ngược chiều kim đồng hồ từ va tới vb)."""
        pv, pa, pb = self._p(v), self._p(a), self._p(b)
        t0 = math.degrees(math.atan2(pa[1] - pv[1], pa[0] - pv[0]))
        t1 = math.degrees(math.atan2(pb[1] - pv[1], pb[0] - pv[0]))
        while t1 <= t0:
            t1 += 360
        if t1 - t0 > 180:
            t0, t1 = t1, t0 + 360
        self.arc(pv, r, t0, t1, style)
        if text:
            m = polar((t0 + t1) / 2, r + 0.28, pv)
            self.free.append((text, m, None, 0.0))

    def tick(self, a, b, n=1, style="ink"):
        """Dấu gạch bằng nhau ở giữa đoạn ab."""
        pa, pb = self._p(a), self._p(b)
        m, u = lerp(pa, pb, 0.5), norm(sub(pb, pa))
        nrm = (-u[1], u[0])
        for i in range(n):
            c = add(m, mul(u, (i - (n - 1) / 2) * 0.07))
            self.segs.append((add(c, mul(nrm, 0.08)), add(c, mul(nrm, -0.08))))
            self.cmds.append(f"  \\draw[{style}] {f4(add(c, mul(nrm, 0.08)))} -- {f4(add(c, mul(nrm, -0.08)))};")

    def text(self, xy, s, near=None):
        """Nhãn chữ tự do (số đo, tên đường thẳng…) đặt gần `xy`; near = hướng ưu tiên (độ)."""
        self.free.append((s, self._p(xy), near, None))

    def seglabel(self, a, b, s, t=0.5):
        pa, pb = self._p(a), self._p(b)
        self.free.append((s, lerp(pa, pb, t), None, None))

    # ── đặt nhãn ───────────────────────────────────────────────────────────
    def _box(self, c, s):
        n = max(1, len(_chu(s)))
        w = W1 if n == 1 else W1 * 0.85 * n + 0.04
        return (c[0] - w / 2, c[1] - H1 / 2, c[0] + w / 2, c[1] + H1 / 2), w

    def _ok(self, box):
        co = (box[0] + 0.015, box[1] + 0.015, box[2] - 0.015, box[3] - 0.015)
        if any(_cat_doan(co, a, b) for a, b in self.segs):
            return False
        if any(_cat_tron(co, c, r) for c, r in self.circles):
            return False
        for b2 in self.boxes:
            if not (box[2] < b2[0] or b2[2] < box[0] or box[3] < b2[1] or b2[3] < box[1]):
                return False
        return True

    def _huong_net(self, p):
        """Hướng (độ) các nét đi ra từ điểm p (đầu mút hoặc điểm giữa đoạn, tiếp tuyến tròn)."""
        hs = []
        for a, b in self.segs:
            for x, y in ((a, b), (b, a)):
                if dist(x, p) < 1e-6 and dist(y, p) > 1e-6:
                    hs.append(math.degrees(math.atan2(y[1] - p[1], y[0] - p[0])))
            ab = dist(a, b)
            if ab > 1e-6 and dist(a, p) > 1e-6 and dist(b, p) > 1e-6 and abs(dist(a, p) + dist(p, b) - ab) < 1e-6:
                hs += [math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])),
                       math.degrees(math.atan2(a[1] - b[1], a[0] - b[0]))]
        for c, r in self.circles:
            if abs(dist(c, p) - r) < 1e-4:
                t = math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
                hs += [t + 90, t - 90]
        return hs

    def _place(self, s, p, pref=None, d0=None, radial_from=None):
        hs = self._huong_net(p)
        best = None
        tren_tron = any(abs(dist(c, p) - r) < 1e-4 for c, r in self.circles)
        buoc = [0.3, 0.36, 0.44, 0.54, 0.66, 0.8] if tren_tron else [0.24, 0.3, 0.38, 0.48, 0.6, 0.75, 0.9]
        for d in ([d0] if d0 else buoc):
            _, w = self._box(p, s)
            for k in range(36):
                th = k * 10
                # chữ rộng: đẩy xa thêm theo trục ngang cho khỏi đè lên điểm
                extra = max(0.0, w / 2 - W1 / 2) * abs(math.cos(math.radians(th)))
                c = add(p, ((d + extra) * math.cos(math.radians(th)), d * math.sin(math.radians(th))))
                box, _ = self._box(c, s)
                if not self._ok(box):
                    continue
                gap = min([abs((th - h + 180) % 360 - 180) for h in hs] or [180])
                score = gap - 40 * (d - 0.24)
                if pref is not None:
                    score -= 0.5 * abs((th - pref + 180) % 360 - 180)
                if radial_from is not None:
                    rad = math.degrees(math.atan2(p[1] - radial_from[1], p[0] - radial_from[0]))
                    score -= 0.25 * abs((th - rad + 180) % 360 - 180)
                if best is None or score > best[0]:
                    best = (score, c, box)
            if best:
                break
        if best is None:
            raise RuntimeError(f"không đặt được nhãn {s}")
        self.boxes.append(best[2])
        return best[1]

    def tikz(self, extra_opts=""):
        out = [f"\\begin{{tikzpicture}}[line width={self.lw}, font={self.font}{extra_opts}]"]
        out += self.cmds
        for n in self.dots:
            out.append(f"  \\fill[ink] {f4(self.P[n])} circle (1.3pt);")
        # tâm đường tròn gần nhất để ưu tiên đặt nhãn điểm trên đường tròn ra NGOÀI
        for name, s, where, d in self.labels:
            p = self.P[name]
            rad = None
            for c, r in self.circles:
                if abs(dist(c, p) - r) < 1e-4:
                    rad = c
            c = self._place(s, p, where, d, rad)
            out.append(f"  \\node[inner sep=0pt] at {f4(c)} {{{s}}};")
        for s, p, near, d in self.free:
            c = self._place(s, p, near, d if d else None)
            fs = ""
            out.append(f"  \\node[inner sep=0pt{fs}] at {f4(c)} {{{s}}};")
        out.append("\\end{tikzpicture}")
        tz = "\n".join(out)
        bi = nhan_bi_de(tz)
        assert not bi, f"nhãn bị đè: {bi}"
        return tz


def _chu(s):
    s = re.sub(r"\\(?:text|mathrm)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+", "x", s)
    s = re.sub(r"\s+", " ", s.strip())
    return re.sub(r"[${}^_]", "", s)
