"""Gọi Mathpix API để bóc tách tệp ảnh hoặc PDF hạt giống sang LaTeX.

Có hỗ trợ chế độ Mock tự động khi thiếu API key để chạy thử nghiệm dễ dàng.
"""
from __future__ import annotations

import json
from pathlib import Path
import requests

from config import settings

MATHPIX_TEXT_URL = "https://api.mathpix.com/v3/text"


class MathpixOCRError(RuntimeError):
    pass


def parse_image_to_latex(image_path: Path) -> str:
    """Gọi Mathpix để dịch 1 tệp ảnh sang LaTeX sạch."""
    if not image_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file ảnh: {image_path}")

    # Chế độ giả lập (Mock) khi thiếu key
    if not settings.MATHPIX_APP_ID or not settings.MATHPIX_APP_KEY:
        # Nếu là file test hoặc demo, trả về mẫu LaTeX giả định
        return (
            r"\section*{Bất đẳng thức xét hiệu}"
            "\nCho hai số thực $a, b$. Chứng minh $a^2 + b^2 \ge 2ab$."
            "\nLời giải: Xét hiệu $a^2 + b^2 - 2ab = (a-b)^2 \ge 0$ với mọi $a, b$."
        )

    headers = {
        "app_id": settings.MATHPIX_APP_ID,
        "app_key": settings.MATHPIX_APP_KEY,
    }
    
    # Chuẩn bị file gửi đi
    with open(image_path, "rb") as f:
        files = {"file": f}
        data = {
            "options_json": json.dumps({
                "math_inline_delimiters": ["$", "$"],
                "math_display_delimiters": ["$$", "$$"],
                "formats": ["text"]
            })
        }
        resp = requests.post(MATHPIX_TEXT_URL, headers=headers, files=files, data=data)
        
    if resp.status_code != 200:
        raise MathpixOCRError(f"Mathpix API báo lỗi ({resp.status_code}): {resp.text}")
        
    result = resp.json()
    if "text" not in result:
        raise MathpixOCRError(f"Phản hồi Mathpix không có text: {result}")
        
    return result["text"]


def process_seed_file(file_path: Path) -> Path:
    """Bóc tách hạt giống và ghi kết quả LaTeX sạch ra thư mục storage."""
    content = parse_image_to_latex(file_path)
    
    out_dir = settings.STORAGE_DIR / "seeds_processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    out_path = out_dir / f"{file_path.stem}_ocr.txt"
    out_path.write_text(content, encoding="utf-8")
    return out_path
