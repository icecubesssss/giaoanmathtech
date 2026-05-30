"""Đặt gốc dự án vào sys.path để `from src...` chạy được khi pytest gọi từ ngoài."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
