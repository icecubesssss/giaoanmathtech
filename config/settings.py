"""Cấu hình tập trung — đọc biến môi trường từ .env (KHÔNG hardcode key)."""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv chưa cài thì vẫn chạy được với env sẵn có
    pass

# Gốc dự án (config/ nằm ngay dưới gốc)
ROOT = Path(__file__).resolve().parent.parent

# Thư mục chuẩn
CONFIG_DIR = ROOT / "config"
TEMPLATES_DIR = ROOT / "templates"
OUTPUTS_DIR = ROOT / "outputs"
STORAGE_DIR = ROOT / "storage"
ASSETS_FONTS_DIR = ROOT / "assets" / "fonts"

# Khóa thiết kế
DESIGN_TOKENS = CONFIG_DIR / "design_tokens.json"

# Engine biên dịch — Tectonic (XeLaTeX, không cần root). TUYỆT ĐỐI không bật -shell-escape.
TECTONIC_BIN = os.path.expanduser(os.getenv("TECTONIC_BIN", "~/bin/tectonic"))

# API keys (rỗng nếu chưa cấu hình — các tầng AI sẽ báo lỗi rõ ràng khi cần)
MATHPIX_APP_ID = os.getenv("MATHPIX_APP_ID", "")
MATHPIX_APP_KEY = os.getenv("MATHPIX_APP_KEY", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
