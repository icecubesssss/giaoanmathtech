#!/usr/bin/env python3
"""Vẽ bảng / biểu đồ thống kê (TikZ thuần) cho phiếu chương VII — số liệu do máy đặt, không giao Gemini vẽ.

18/11: KHÔNG dùng môi trường center — trivlist chèn \@beginparpenalty (−51) ngay trước hình, đè \nopagebreak
⇒ đề nằm cuối trang, hình rơi sang trang sau. Dùng nhóm {\centering … \par}.
Bẫy đã biết ([[phieu-thong-ke-bay-trinh-bay]]): hình đặt THẲNG trong statement bằng
`\\par\\nopagebreak\\smallskip\\begin{center}…\\end{center}\\smallskip`, không [[br]] sát trước/sau khối center,
`\\renewcommand\\arraystretch{…}` không ngoặc. Cột RỜI cho biểu đồ tần số, cột SÁT cho ghép nhóm.
"""
from __future__ import annotations

import re
from fractions import Fraction

CAO = 1.8   # chiều cao trục đứng (cm) — 18/11: 2,6 làm phiếu HS 24 trang
MAU = ["stage1", "stage2", "stage3", "stage4", "stage5", "brand"]


def vn(x) -> str:
    """Số kiểu Việt Nam trong $…$: 12.5 → 12{,}5 ; Fraction → thập phân hữu hạn."""
    if isinstance(x, Fraction):
        x = float(x)
    if isinstance(x, float):
        s = f"{x:.4f}".rstrip("0").rstrip(".")
    else:
        s = str(x)
    return s.replace(".", "{,}")


def _khoi(noi: str, rong: float | None = None) -> str:
    if rong:
        noi = r"\adjustbox{max width=" + f"{rong}" + r"\linewidth}{" + noi + "}"
    return r"\par\nopagebreak\smallskip\nopagebreak{\centering " + noi + r"\par}\smallskip "


def bang(hang: list[list], dam_cot1: bool = True, co: str = r"\footnotesize") -> str:
    """Bảng ngang: hang = [[tiêu đề, ô…], …]; ô là chuỗi LaTeX hoặc số (tự bọc $…$)."""
    k = len(hang[0])
    dong = []
    for h in hang:
        o = []
        for j, c in enumerate(h):
            c = f"${vn(c)}$" if isinstance(c, (int, float, Fraction)) else str(c)
            o.append(r"\textbf{" + c + "}" if (j == 0 and dam_cot1) else c)
        dong.append(" & ".join(o) + r" \\ \hline")
    cot = "|l|" + "c|" * (k - 1) if dam_cot1 else "|" + "c|" * k
    return _khoi(co + r"\renewcommand\arraystretch{1.25}\begin{tabular}{" + cot + r"}\hline " + " ".join(dong)
                 + r"\end{tabular}", rong=0.98)


def luoi(so: list, moi_dong: int, co: str = r"\footnotesize") -> str:
    """Dãy số liệu thô xếp thành lưới (bảng không tiêu đề)."""
    hang = [so[i:i + moi_dong] for i in range(0, len(so), moi_dong)]
    hang[-1] = hang[-1] + [""] * (moi_dong - len(hang[-1]))
    return bang(hang, dam_cot1=False, co=co)


def _tran(gt, ymax: float, buoc: float) -> float:
    """Nới đỉnh trục để số ghi trên cột cao nhất không chạm mép trên (nhan_hinh)."""
    while max(float(v) for v in gt) > 0.85 * ymax:
        ymax += buoc
    return ymax


def _truc(w: float, ymax: float, buoc: float, H: float, tx: str, ty: str, nhan_y=None) -> list[str]:
    """Trục + vạch chia trên trục đứng (không kẻ lưới ngang — lưới đè lên số ghi trên cột)."""
    d = []
    v = 0.0
    while v <= ymax + 1e-9:
        y = v * H / ymax
        d.append(rf"\draw[ink] (-0.06,{y:.2f}) -- (0.06,{y:.2f});")
        d.append(rf"\node[left,font=\scriptsize] at (-0.06,{y:.2f}) {{${vn(v if v % 1 else int(v))}$}};")
        v += buoc
    d.append(rf"\draw[->,ink] (0,0) -- ({w + 0.35:.2f},0);")
    d.append(rf"\node[anchor=south west,font=\scriptsize,align=left] at ({w + 0.3:.2f},0.12) {{{tx}}};")
    d.append(rf"\draw[->,ink] (0,0) -- (0,{H + 0.45:.2f}) node[above,font=\scriptsize]{{{ty}}};")
    return d


def cot(nhan: list, gt: list, tx: str, ty: str, ymax: float, buoc: float, sat: bool = False,
        tren: list | None = None, tieu_de: str = "", mau: str = "stage2", rong: float = 0.62,
        bw: float = 0.9, gap: float = 0.6, nhan_rong: float | None = None) -> str:
    """Biểu đồ cột. sat=True: biểu đồ ghép nhóm, `nhan` là các MỐC (len = len(gt)+1), cột sát nhau.
    tren: chữ ghi trên cột (mặc định = giá trị)."""
    H = CAO
    ymax = _tran(gt, ymax, buoc)
    n = len(gt)
    if sat:
        x0, step = 0.4, bw
        w = x0 + n * bw + 0.3
    else:
        x0, step = gap, bw + gap
        w = gap + n * (bw + gap)
    d = [r"\begin{tikzpicture}[font=\small,line width=0.6pt]"] + _truc(w, ymax, buoc, H, tx, ty)
    for i, v in enumerate(gt):
        a = x0 + i * step
        h = float(v) * H / ymax
        d.append(rf"\fill[{mau}!25] ({a:.2f},0) rectangle ({a + bw:.2f},{h:.2f});")
        d.append(rf"\draw[{mau}] ({a:.2f},0) rectangle ({a + bw:.2f},{h:.2f});")
        t = tren[i] if tren else f"${vn(v)}$"
        d.append(rf"\node[above,font=\scriptsize,inner sep=1.5pt] at ({a + bw / 2:.2f},{h:.2f}) {{{t}}};")
        if not sat:
            tw = nhan_rong or (bw + gap * 0.8)
            d.append(rf"\node[below,font=\scriptsize,align=center,text width={tw:.2f}cm] at ({a + bw / 2:.2f},0) "
                     rf"{{{nhan[i]}}};")
    if sat:
        for i, mo in enumerate(nhan):
            d.append(rf"\node[below,font=\scriptsize] at ({x0 + i * bw:.2f},0) {{${vn(mo)}$}};")
    if tieu_de:
        d.append(rf"\node[font=\scriptsize\bfseries,align=center] at ({w / 2:.2f},{H + 1.15:.2f}) {{{tieu_de}}};")
    d.append(r"\end{tikzpicture}")
    return _khoi("".join(d), rong=rong)


def doan(nhan: list, gt: list, tx: str, ty: str, ymax: float, buoc: float, tieu_de: str = "",
         mau: str = "stage3", rong: float = 0.62, step: float = 1.4, nhan_rong: float = 1.3) -> str:
    """Biểu đồ đoạn thẳng."""
    H = CAO
    ymax = _tran(gt, ymax, buoc)
    n = len(gt)
    w = step * (n + 0.5)
    d = [r"\begin{tikzpicture}[font=\small,line width=0.6pt]"] + _truc(w, ymax, buoc, H, tx, ty)
    pts = [(step * (i + 0.75), float(v) * H / ymax) for i, v in enumerate(gt)]
    d.append(rf"\draw[{mau},line width=0.9pt] " + " -- ".join(f"({a:.2f},{b:.2f})" for a, b in pts) + ";")
    for i, ((a, b), v, t) in enumerate(zip(pts, gt, nhan)):
        truoc = pts[i - 1][1] if i else None
        sau = pts[i + 1][1] if i + 1 < len(pts) else None
        cao = [z for z in (truoc, sau) if z is not None and z > b]
        if not cao:
            vt = "above"                     # đỉnh: đường nối đi xuống hai bên
        elif len(cao) == 2 or (truoc is None or sau is None):
            vt = "below right" if (sau is not None and sau > b) else "below left"
        else:
            vt = "above left" if (sau is not None and sau > b) else "above right"
        if vt.startswith("below") and b < 0.35:
            vt = "left" if (sau is not None and sau > b) else "right"
        d.append(rf"\fill[{mau}] ({a:.2f},{b:.2f}) circle (1.6pt);")
        d.append(rf"\node[{vt},font=\scriptsize,inner sep=2.5pt] at ({a:.2f},{b:.2f}) {{${vn(v)}$}};")
        d.append(rf"\node[below,font=\scriptsize,align=center,text width={nhan_rong:.2f}cm] at ({a:.2f},0) {{{t}}};")
    if tieu_de:
        d.append(rf"\node[font=\scriptsize\bfseries,align=center] at ({w / 2:.2f},{H + 1.15:.2f}) {{{tieu_de}}};")
    d.append(r"\end{tikzpicture}")
    return _khoi("".join(d), rong=rong)


def quat(pt: list, chu: list, tieu_de: str = "", rong: float = 0.42) -> str:
    """Biểu đồ hình quạt tròn: pt = phần trăm (tổng 100), chu = chú thích từng quạt."""
    assert abs(sum(pt) - 100) < 1e-9, pt
    R = 1.5
    d = [r"\begin{tikzpicture}[font=\small,line width=0.6pt]"]
    goc = 90.0
    for i, (p, c) in enumerate(zip(pt, chu)):
        g2 = goc - 3.6 * p
        m = MAU[i % len(MAU)]
        d.append(rf"\fill[{m}!35] (0,0) -- ({goc:.1f}:{R}) arc ({goc:.1f}:{g2:.1f}:{R}) -- cycle;")
        d.append(rf"\node[font=\scriptsize] at ({(goc + g2) / 2:.1f}:{R * 0.66:.2f}) {{${vn(p)}\%$}};")
        y = 0.9 - i * 0.45
        d.append(rf"\fill[{m}!35] (2.3,{y - 0.12:.2f}) rectangle (2.55,{y + 0.12:.2f});")
        d.append(rf"\node[right,font=\scriptsize] at (2.6,{y:.2f}) {{{c}}};")
        goc = g2
    d.append(rf"\draw[ink!60] (0,0) circle ({R});")
    if tieu_de:
        d.append(rf"\node[font=\scriptsize\bfseries,align=center] at (0.9,{R + 0.4:.2f}) {{{tieu_de}}};")
    d.append(r"\end{tikzpicture}")
    return _khoi("".join(d), rong=rong)


def tranh(nhom: list, so: list, chu_thich: str, rong: float | None = None) -> str:
    """Biểu đồ tranh: mỗi biểu tượng người = 1 đơn vị."""
    d = [r"\begin{tikzpicture}[font=\small,line width=0.5pt]"]
    for i, (t, k) in enumerate(zip(nhom, so)):
        y = -i * 0.6
        d.append(rf"\node[left,font=\scriptsize,text width=3.4cm,align=right] at (3.5,{y:.2f}) {{{t}}};")
        d.append(rf"\draw[ink!40] (3.6,{y - 0.3:.2f}) -- (3.6,{y + 0.3:.2f});")
        for j in range(k):
            x = 3.9 + j * 0.42
            d.append(rf"\fill[stage2] ({x:.2f},{y + 0.12:.2f}) circle (0.07);")
            d.append(rf"\fill[stage2,rounded corners=1pt] ({x - 0.09:.2f},{y - 0.2:.2f}) rectangle "
                     rf"({x + 0.09:.2f},{y + 0.03:.2f});")
    yb = -len(nhom) * 0.6 + 0.05
    d.append(rf"\node[font=\scriptsize,anchor=west] at (0.2,{yb:.2f}) {{{chu_thich}}};")
    d.append(r"\end{tikzpicture}")
    return _khoi("".join(d), rong=rong)


def canh(*khoi: str, rong: float = 0.47) -> str:
    """Đặt nhiều hình (kết quả cot/doan/…) cạnh nhau trong một khối center."""
    dau, cuoi = r"\par\nopagebreak\smallskip\nopagebreak{\centering ", r"\par}\smallskip "
    noi = []
    for k in khoi:
        assert k.startswith(dau) and k.endswith(cuoi), k[:60]
        t = k[len(dau):-len(cuoi)]
        t = re.sub(r"^\\adjustbox\{max width=[0-9.]+\\linewidth\}\{(.*)\}$", r"\1", t, flags=re.S)
        noi.append(r"\adjustbox{max width=" + f"{rong}" + r"\linewidth}{" + t + "}")
    return dau + r"\hfill".join(noi) + cuoi


def ruot(k: str) -> str:
    """Bỏ vỏ center + adjustbox của một khối hình, trả về TikZ trần."""
    dau, cuoi = r"\par\nopagebreak\smallskip\nopagebreak{\centering ", r"\par}\smallskip "
    assert k.startswith(dau) and k.endswith(cuoi), k[:60]
    t = k[len(dau):-len(cuoi)]
    return re.sub(r"^\\adjustbox\{max width=[0-9.]+\\linewidth\}\{(.*)\}$", r"\1", t, flags=re.S)


def ben_phai(trai: str, hinh: str, rong_hinh: float = 0.41) -> str:
    """Câu hỏi bên trái, hình bên phải (18/11: hình chiếm trọn ngang trang làm phiếu nhiều khoảng trắng)."""
    rt = 0.97 - rong_hinh
    return (r"\par\smallskip\noindent\begin{minipage}[t]{" + f"{rt:.2f}" + r"\linewidth}\vspace{0pt}" + trai
            + r"\end{minipage}\hfill\begin{minipage}[t]{" + f"{rong_hinh:.2f}" + r"\linewidth}\vspace{0pt}\centering"
            + r"\adjustbox{max width=\linewidth}{" + ruot(hinh) + r"}\end{minipage}\par\smallskip ")
