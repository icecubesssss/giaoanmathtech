"""Vẽ các mảnh LaTeX đồ hoạ (TikZ, sơ đồ forest, badge chặng, thanh hành trình…) ra PNG
để chèn vào bản Word.

Bài học từ tex2gdoc / latex2docx-converter (Thầy 22/10/2026):
  • Dùng LẠI preamble thật của bản PDF (`preamble/_fonts,_colors,_macros`) — cùng font
    STIX, cùng macro \\rightanglemark, flownode… ⇒ hình Word giống hệt hình PDF.
    (latex2docx-converter dùng preamble cứng ⇒ hình lệch font/macro.)
  • `\\linewidth` = đúng bề ngang cột chữ của phiếu (6,77in) ⇒ hình dùng \\linewidth
    co giãn y như bản PDF (tex2gdoc: đo sai bề ngang làm chữ trên hình lệch 17%).
  • CACHE theo hash (mã hình + preamble) — cả hai repo kia vẽ lại mọi hình mỗi lần chạy.
  • Gộp mọi hình MỘT phiếu vào MỘT file standalone nhiều trang (multi=mtfig) ⇒ một lần
    Tectonic. Lô lỗi thì vẽ lại TỪNG hình để chỉ đúng hình hỏng, các hình khác vẫn ra.
  • PNG < 2KB coi là hỏng (tex2gdoc).
  • `pdftocairo -transp`: nền TRONG SUỐT như hình PDF (watermark nhìn xuyên qua được).
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from config import settings

CACHE_DIR = Path(settings.ROOT) / "storage" / "cache" / "tikz"
DPI = 300
TEXT_WIDTH_IN = 6.77          # A4 − 2×0,75in: bề ngang cột chữ phiếu (base_handout)


class FigureError(RuntimeError):
    pass


@dataclass
class Raster:
    png: Path
    w_in: float               # kích thước TỰ NHIÊN của hình (trước khi co theo khung)
    h_in: float


@lru_cache(maxsize=1)
def _preamble() -> str:
    from src.compiler.jinja_renderer import _env, load_tokens
    env = _env(False)
    tok = load_tokens()
    parts = [env.get_template(f"preamble/{n}.tex.j2").render(**tok)
             for n in ("_fonts", "_colors", "_macros")]
    return "\n".join(parts)


@lru_cache(maxsize=1)
def _preamble_hash() -> str:
    return hashlib.sha1(_preamble().encode()).hexdigest()[:12]


def _doc(snippets: list[str]) -> str:
    body = "\n".join(f"\\begin{{mtfig}}{s}\\end{{mtfig}}" for s in snippets)
    return (
        "\\documentclass[multi=mtfig,border=1.5pt,12pt]{standalone}\n"
        "\\usepackage{graphicx}\n"
        f"{_preamble()}\n"
        f"\\setlength{{\\textwidth}}{{{TEXT_WIDTH_IN}in}}\\setlength{{\\linewidth}}{{\\textwidth}}"
        f"\\setlength{{\\hsize}}{{\\textwidth}}\\setlength{{\\columnwidth}}{{\\textwidth}}\n"
        "\\newenvironment{mtfig}{}{}\n"
        "\\begin{document}\n"
        f"{body}\n"
        "\\end{document}\n"
    )


def key(snippet: str) -> str:
    return hashlib.sha1(f"{_preamble_hash()}\0{snippet}".encode()).hexdigest()


def _cached(snippet: str) -> Path | None:
    p = CACHE_DIR / f"{key(snippet)}.png"
    return p if p.exists() and p.stat().st_size > 0 else None


def _compile(snippets: list[str]) -> list[Path]:
    """Một lần Tectonic cho cả lô; trả PNG theo đúng thứ tự `snippets`."""
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        tex = tdp / "figs.tex"
        tex.write_text(_doc(snippets), encoding="utf-8")
        r = subprocess.run([settings.TECTONIC_BIN, "-X", "compile", str(tex), "--outdir", td],
                           capture_output=True, text=True)
        pdf = tdp / "figs.pdf"
        if r.returncode != 0 or not pdf.exists():
            err = [ln for ln in (r.stderr or "").splitlines() if "error" in ln.lower()]
            raise FigureError("; ".join(err[-3:]) or "Tectonic lỗi")
        subprocess.run(["pdftocairo", "-png", "-transp", "-r", str(DPI), str(pdf), str(tdp / "p")],
                       check=True, capture_output=True)
        pngs = sorted(tdp.glob("p-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
        if len(pngs) != len(snippets):
            raise FigureError(f"ra {len(pngs)} trang cho {len(snippets)} hình")
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        out = []
        for s, png in zip(snippets, pngs):
            if png.stat().st_size < 2000 and "tikz" in s:
                raise FigureError("hình rỗng (PNG < 2KB)")
            dst = CACHE_DIR / f"{key(s)}.png"
            shutil.copyfile(png, dst)
            out.append(dst)
        return out


def _size(png: Path) -> tuple[float, float]:
    from PIL import Image
    with Image.open(png) as im:
        return im.width / DPI, im.height / DPI


def render_many(snippets: list[str]) -> dict[str, Raster | FigureError]:
    """{mã LaTeX: Raster | FigureError}. Hình hỏng KHÔNG kéo đổ cả phiếu — cổng
    docx_gate sẽ chặn ghi file và chỉ đúng hình hỏng."""
    res: dict[str, Raster | FigureError] = {}
    todo = []
    for s in dict.fromkeys(snippets):
        hit = _cached(s)
        if hit:
            res[s] = Raster(hit, *_size(hit))
        else:
            todo.append(s)
    if todo:
        try:
            for s, p in zip(todo, _compile(todo)):
                res[s] = Raster(p, *_size(p))
        except FigureError:
            for s in todo:          # dò từng hình để khoanh đúng hình hỏng
                try:
                    p = _compile([s])[0]
                    res[s] = Raster(p, *_size(p))
                except FigureError as e:
                    res[s] = e
    return res
