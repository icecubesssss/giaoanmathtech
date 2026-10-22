"""Ghi bản Word (.docx) cạnh bản PDF — qua cổng `docx_gate`, có cache theo hash.

Tên file = đúng tên bản PDF (exporters/ten_file.ten_ban_in), đuôi .docx — Thầy mở thư
mục thấy cặp `…-Phieu-HS.pdf` / `…-Phieu-HS.docx` đứng cạnh nhau.

Máy chưa cài pandoc ⇒ trả None + lời nhắc, KHÔNG làm hỏng bản PDF.
"""
from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

from config import settings

# Bật Word MẶC ĐỊNH cho mọi lần build. Để False tới khi Thầy duyệt mẫu (kế hoạch 22/10/2026,
# bước 6); trong lúc đó dùng `build --docx` hoặc `build-docx`.
DOCX_DEFAULT = False

# Đổi số này khi đổi renderer/khuôn ⇒ mọi bản Word build lại.
DOCX_VER = "1"


def _digest(payload: str, template: Path) -> str:
    h = hashlib.sha256()
    h.update(DOCX_VER.encode())
    h.update(payload.encode())
    h.update(template.read_bytes() if template.exists() else b"")
    h.update(Path(settings.DESIGN_TOKENS).read_bytes())
    return h.hexdigest()


def _write(render, payload: str, template: Path, out_dir: Path, filename: str, force: bool,
           branded: bool) -> tuple[Path | None, list[str]]:
    from src.compiler.omml import PandocMissing
    from src.validators.docx_gate import check_docx
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{filename}.docx"
    sha = out_dir / f"{filename}.docx.sha256"
    digest = _digest(payload, template)
    if not force and path.exists() and sha.exists() and sha.read_text().strip() == digest:
        return path, []
    try:
        doc, report = render()
    except PandocMissing as e:
        return None, [f"bỏ qua bản Word: {e}"]
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "x.docx"
        doc.save(tmp)
        errs = list(report.issues) + check_docx(tmp, expect_maths=report.counts.get("maths"),
                                                branded=branded)
        if errs and not force:
            return None, errs
        path.write_bytes(tmp.read_bytes())
    sha.write_text(digest)
    return path, errs


def build_docx(lesson, out_dir: Path, filename: str, lesson_dir: Path | None = None,
               force: bool = False, show_solution: bool = False) -> tuple[Path | None, list[str]]:
    """Phiếu/đề → .docx cạnh PDF. → (đường dẫn | None, lỗi). Có lỗi cổng ⇒ KHÔNG ghi (trừ force)."""
    from src.compiler.docx_renderer import TEMPLATE, render_lesson_docx
    payload = ("GV" if show_solution else "HS") + lesson.model_dump_json()
    return _write(lambda: render_lesson_docx(lesson, lesson_dir, show_solution), payload, TEMPLATE,
                  out_dir, filename, force, branded=True)


def build_thuyetminh_docx(spec, out_dir: Path, filename: str, force: bool = False) -> tuple[Path | None, list[str]]:
    """Thuyết minh → .docx A4 ngang cạnh PDF (không trang trí, y bản PDF)."""
    from src.compiler.thuyetminh_docx import TEMPLATE, render_thuyetminh_docx
    return _write(lambda: render_thuyetminh_docx(spec), "TM" + spec.model_dump_json(), TEMPLATE,
                  out_dir, filename, force, branded=False)
