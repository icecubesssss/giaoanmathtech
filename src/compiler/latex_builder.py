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


# Dấu hiệu dòng lỗi LaTeX/Tectonic đáng nổi lên đầu (thay vì lội 3000 ký tự log thô).
_ERROR_MARKERS = (
    "error:",                    # Tectonic
    "! LaTeX Error",
    "! Undefined control sequence",
    "! Package",
    "! Misplaced",
    "! Missing",
    "! Extra ",
    "! Paragraph ended",
    "! Dimension too large",
    "! Emergency stop",
    "Runaway argument",
    "l.",                        # "l.123 ..." — số dòng .tex nơi lỗi
)


def _summarize_tex_log(log: str, tex_path: Path) -> str:
    """Trích các dòng lỗi cốt lõi từ log Tectonic để dễ truy dòng .tex bị sai.

    Tectonic in lỗi ra stderr; ta nhặt riêng các dòng khớp `_ERROR_MARKERS`
    (kèm tên file .tex tạm) rồi mới đính kèm đuôi log thô làm dự phòng."""
    hits = [ln for ln in log.splitlines() if any(m in ln for m in _ERROR_MARKERS)]
    parts = [f"  Tệp .tex: {tex_path}"]
    if hits:
        parts.append("  Dòng lỗi cốt lõi:")
        parts.extend(f"    {ln.strip()}" for ln in hits[-15:])
    parts.append("  --- đuôi log thô ---")
    parts.append(log[-1500:])
    return "\n".join(parts)


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
        log = (proc.stderr or "") + ("\n" + proc.stdout if proc.stdout else "")
        raise LatexBuildError(
            f"Tectonic thất bại (mã {proc.returncode}).\n"
            + _summarize_tex_log(log, tex_path)
        )

    pdf_path = out_dir / f"{filename}.pdf"
    if not pdf_path.exists():
        raise LatexBuildError("Compile xong nhưng không thấy PDF.")
    return pdf_path
