"""Gọi Tectonic (engine XeLaTeX) biên dịch mã LaTeX → PDF.

CHỐT BẢO MẬT: Tectonic mặc định KHÔNG bật shell-escape; ở đây cũng tuyệt đối
không truyền cờ shell-escape. Mọi LaTeX cào mạng phải đi qua latex_sanitizer (S2)
trước khi tới bước này.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from config import settings


class LatexBuildError(RuntimeError):
    pass


def build_pdf(tex_source: str, slug: str, filename: str = "handout", out_root: Path | None = None) -> Path:
    """Ghi .tex vào <out_root>/<slug>/ rồi compile ra PDF. Trả về đường dẫn PDF.

    `out_root` mặc định là OUTPUTS_DIR; truyền vào để output mirror theo cây
    inputs/seeds (vd outputs/dai-so/tuan09-bat-dang-thuc/<slug>/).
    """
    base = out_root if out_root is not None else settings.OUTPUTS_DIR
    out_dir = base / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = out_dir / f"{filename}.tex"
    tex_path.write_text(tex_source, encoding="utf-8")

    cmd = [settings.TECTONIC_BIN, "-X", "compile", str(tex_path), "--outdir", str(out_dir)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise LatexBuildError(
            f"Tectonic thất bại (mã {proc.returncode}).\n--- stderr ---\n{proc.stderr[-3000:]}"
        )

    pdf_path = out_dir / f"{filename}.pdf"
    if not pdf_path.exists():
        raise LatexBuildError("Compile xong nhưng không thấy PDF.")
    return pdf_path
