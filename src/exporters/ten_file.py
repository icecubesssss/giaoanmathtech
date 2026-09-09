"""ten_file — đặt TÊN PDF thành phẩm tự nói ra mình là bài gì.

Thầy phản hồi 06/09/2026: gửi hàng loạt PDF vào Zalo thì "mọi người vẫn không
biết là file bài gì nếu không gửi cả folder". Nguyên nhân: mọi thư mục trong kho
đều build ra đúng ba cái tên `ca-01-handout.pdf` / `ca-01-guide.pdf` /
`ca-01-slide.pdf` — thông tin phân biệt nằm HẾT ở tên thư mục, mà Zalo thì chỉ
hiện tên file.

Tên mới gói đủ bốn thứ người nhận cần đọc trong một dòng::

    Toan8B-Tuan10-On-tap-hinh-binh-hanh-hinh-chu-nhat-Phieu-HS.pdf
    └─┬──┘ └─┬───┘ └──────────┬─────────────────────┘ └──┬────┘
     khối    tuần            tên bài                    bản nào
     +tầng  (sắp xếp)      (lấy từ slug phiếu)

Quy ước chữ: KHÔNG DẤU, y như tên thư mục Drive Thầy đang chép tay (xem
`drive_sync`) — khỏi lệch NFC/NFD giữa macOS, Windows và Zalo.

Thiếu mảnh nào (seed nằm ngoài cây `inputs/seeds`, thư mục không có số tuần…)
thì lùi về tên cũ `ca-NN-<bản>` chứ không đoán bừa.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

# Tên 'bản in' theo cách Thầy gọi, không phải theo tên kỹ thuật của template.
BAN_IN = {"handout": "Phieu-HS", "guide": "Dap-an-GV", "slide": "Slide"}

_TEX = re.compile(r"\\[A-Za-z]+\s*|[$\\{}]")
_TUAN = re.compile(r"^(?:\[[A-Za-z]\])?tuan(\d+(?:-\d+)*)", re.IGNORECASE)


def bo_dau(s: str) -> str:
    """'Mở đầu về đường tròn' → 'Mo dau ve duong tron' (Drive/Finder dễ đọc, khỏi lệch NFC/NFD).

    Bóc luôn LaTeX: tiêu đề phiếu có thể chứa `$AH$`, `\\textbf{…}` — không bóc thì tên
    thư mục Drive lòi ra 'Ca-03 - He thuc luong (duong cao $AH$)'.
    """
    s = _TEX.sub("", s)
    s = s.replace("Đ", "D").replace("đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip()


def _khoi_tang(json_path: Path, lesson) -> str:
    """'lop-8' + tầng 'B' → 'Toan8B'. Tầng lấy từ phiếu trước, rồi mới tới đường dẫn."""
    segs = json_path.parts
    m = next((re.fullmatch(r"lop-(\d+)", s) for s in segs
              if re.fullmatch(r"lop-\d+", s)), None)
    if not m:
        gl = getattr(lesson, "grade_label", "") or ""
        m = re.search(r"L[ớo]p\s*(\d+)", gl)
    if not m:
        return ""
    tang = (getattr(lesson, "class_tier", "") or "").strip().upper()
    if not tang:
        tang = next((re.fullmatch(r"lop-([a-x])", s).group(1).upper() for s in segs
                     if re.fullmatch(r"lop-[a-x]", s)), "")
    return f"Toan{m.group(1)}{tang}"


def _tuan(json_path: Path) -> str:
    """Thư mục 'tuan10-…' / '[C]tuan10-11-…' → 'Tuan10' / 'Tuan10-11'."""
    for seg in reversed(json_path.parts):
        m = _TUAN.match(seg)
        if m:
            return "Tuan" + m.group(1)
    return ""


def _ten_bai(lesson) -> str:
    """Chủ đề của CHÍNH phiếu này, lấy từ slug: 'phieu-a-on-tap-hbh-hcn' → 'On-tap-hbh-hcn'.

    Dùng slug chứ không dùng `title` vì slug đã là chuỗi không dấu Thầy tự đặt, và
    hai phiếu cùng thư mục luôn khác slug — tên file vì thế không bao giờ đụng nhau.
    """
    slug = (getattr(lesson, "slug", "") or "").strip()
    slug = re.sub(r"^phieu-[a-z]-", "", slug)
    slug = bo_dau(slug.replace(" ", "-"))
    slug = re.sub(r"[^A-Za-z0-9-]+", "-", slug).strip("-")
    return slug[:1].upper() + slug[1:] if slug else ""


def ten_ban_in(lesson, json_path: Path | str | None, kind: str, ca_pre: str = "") -> str:
    """Tên file (không đuôi) cho một bản in. Lùi về '{ca_pre}{kind}' khi thiếu dữ kiện."""
    lui = f"{ca_pre}{kind}"
    if json_path is None:
        return lui
    p = Path(json_path).resolve()
    phan = [_khoi_tang(p, lesson), _tuan(p), _ten_bai(lesson), BAN_IN.get(kind, kind)]
    if not all(phan):
        return lui
    return "-".join(phan)
