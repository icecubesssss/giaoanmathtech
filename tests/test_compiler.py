"""Smoke test khung biên dịch + chốt bảo mật -shell-escape."""
import os
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ["base_handout.tex.j2"]  # base_slide/base_guide là việc của S3
COMPONENTS = ["review", "concept", "practice1", "practice2", "reflection"]


def test_handout_template_and_five_components_exist():
    for t in TEMPLATES:
        assert (ROOT / "templates" / t).exists(), f"Thiếu template {t}"
    for c in COMPONENTS:
        assert (ROOT / "templates" / "components" / f"{c}.tex.j2").exists(), f"Thiếu chặng {c}"


def test_pydantic_schema_importable():
    from src.schema.lesson_package import LessonPackage  # noqa: F401


def test_jinja_renders_without_error():
    env = Environment(
        loader=FileSystemLoader(str(ROOT / "templates")),
        block_start_string="((*", block_end_string="*))",
        variable_start_string="(((", variable_end_string=")))",
        comment_start_string="((=", comment_end_string="=))",
    )
    # Renderer thật được test riêng (build-handout); ở đây chỉ smoke parse cú pháp Jinja.
    tpl = env.get_template("base_handout.tex.j2")
    assert tpl is not None


def test_no_shell_escape_in_build():
    """Chốt bảo mật: latex_builder TUYỆT ĐỐI không được bật -shell-escape."""
    src = (ROOT / "src" / "compiler" / "latex_builder.py").read_text(encoding="utf-8")
    assert "-shell-escape" not in src, "Phát hiện -shell-escape: nguy cơ thực thi mã!"
