"""drive_sync — chép PDF thành phẩm từ `outputs/` sang Google Drive đã đồng bộ trên máy.

Thầy dựng sẵn cây thư mục trên Drive theo **khối → tầng lớp → chương**, khác cây
trong repo (repo chia theo `hinh-hoc` / `dai-so`). Module này dịch đường dẫn giữa hai cây:

    outputs/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-a-mo-dau-ve-duong-tron/ca-01-handout.pdf
      →  <DRIVE>/giaoanmathtech/lop9/C/Chuong 5/Ca-01 - Mo dau ve duong tron/ca-01-handout.pdf

    outputs/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/thuyet-minh-…/thuyet-minh-….pdf
      →  <DRIVE>/giaoanmathtech/lop9/C/Chuong 5/Thuyet-minh-chuong-V/thuyet-minh-….pdf

Quy ước giữ nguyên như chương IV Thầy đã chép tay: tên folder tiếng Việt KHÔNG DẤU,
file giữ NGUYÊN tên build ra (chép lại là ghi đè, không sinh bản trùng).

Thư mục thiếu thì TẠO MỚI. Thư mục đã có mà chỉ khác hoa/thường hay khoảng trắng
("Chuong5" vs "Chuong 5") thì DÙNG LẠI cái sẵn có — tránh đẻ folder song sinh cạnh
folder Thầy tự tạo.
"""
from __future__ import annotations

import os
import re
import shutil
import unicodedata
from dataclasses import dataclass
from pathlib import Path

# Drive đồng bộ trên máy Thầy; đổi bằng biến môi trường MATHTECH_DRIVE_ROOT nếu máy khác.
_DEFAULT_DRIVE = (
    "~/Library/CloudStorage/GoogleDrive-thaitd.mathtech@gmail.com/My Drive/giaoanmathtech"
)

_ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
          8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}


def drive_root() -> Path:
    return Path(os.environ.get("MATHTECH_DRIVE_ROOT", _DEFAULT_DRIVE)).expanduser()


_TEX = re.compile(r"\\[A-Za-z]+\s*|[$\\{}]")


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


def _norm(name: str) -> str:
    """Khoá so khớp thư mục: bỏ dấu, bỏ khoảng trắng, thường hoá ⇒ 'Chuong5' == 'Chuong 5'."""
    return re.sub(r"[\s_-]+", "", bo_dau(name)).lower()


def ensure_khoi(root: Path, name: str, tao: bool = True) -> Path:
    """Thư mục KHỐI ('lop9') — khớp RỘNG TAY hơn `ensure_dir`: nhận cả tên có đuôi.

    Thầy đặt tên khối kèm năm học ("Lop 9 2026-2027"). `ensure_dir` so khớp CHÍNH XÁC
    nên không nhận ra, đẻ ra 'lop9' nằm cạnh — hai cây song sinh, mỗi cây một nửa bài
    (Thầy phát hiện 15/08/2026). Nay khớp theo TIỀN TỐ: 'lop920262027' bắt đầu bằng
    'lop9' ⇒ dùng lại. Nhiều thư mục cùng khớp thì lấy cái ĐANG CHỨA NHIỀU PDF NHẤT
    (cây Thầy thật sự dùng). Đặt MATHTECH_DRIVE_KHOI để chỉ định thẳng, khỏi đoán.
    """
    chi_dinh = os.environ.get("MATHTECH_DRIVE_KHOI")
    if chi_dinh:
        return ensure_dir(root, chi_dinh, tao)
    if root.is_dir():
        want = _norm(name)
        hop = [d for d in sorted(root.iterdir())
               if d.is_dir() and _norm(d.name).startswith(want)]
        if hop:
            return max(hop, key=lambda d: len(list(d.rglob("*.pdf"))))
    out = root / name
    if tao:
        out.mkdir(parents=True, exist_ok=True)
    return out


def ensure_dir(parent: Path, name: str, tao: bool = True) -> Path:
    """Trả thư mục con `name` dưới `parent`, dùng lại thư mục đã có nếu chỉ khác
    hoa/thường hay khoảng trắng; không có thì tạo mới (`tao=False` = chỉ tra đường)."""
    if parent.is_dir():
        want = _norm(name)
        for child in sorted(parent.iterdir()):
            if child.is_dir() and _norm(child.name) == want:
                return child
    out = parent / name
    if tao:
        out.mkdir(parents=True, exist_ok=True)
    return out


def di_toi(root: Path, parts: list[str], tao: bool = True) -> Path:
    """Lần theo `parts` từ gốc Drive. Khúc ĐẦU (khối) khớp rộng tay, các khúc sau khớp chặt.

    `tao=False` dùng cho --dry-run: chỉ TRA đường, không tạo thư mục rỗng — và quan
    trọng hơn là in ra ĐÚNG chỗ sẽ chép (bản cũ ghép chuỗi thô nên --dry-run báo
    'lop9/…' còn bản chép thật lại vào chỗ khác).
    """
    dest = root
    for i, seg in enumerate(parts):
        dest = ensure_khoi(dest, seg, tao) if i == 0 else ensure_dir(dest, seg, tao)
    return dest


@dataclass
class DriveTarget:
    """Chỗ đến trên Drive của một thư mục output."""
    parts: list[str]          # vd ['lop9', 'C', 'Chuong 5', 'Ca-01 - Mo dau ve duong tron']
    ly_do: str = ""


def _chuong_so(seg: str) -> int | None:
    m = re.match(r"chuong-0*(\d+)", seg)
    return int(m.group(1)) if m else None


def plan_target(out_dir: Path, outputs_root: Path, tieu_de: str | None = None) -> DriveTarget | None:
    """Dịch một thư mục trong `outputs/` sang danh sách thư mục trên Drive.

    Trả None khi đường dẫn không nằm trong `outputs/` hoặc thiếu lớp/chương để xếp chỗ."""
    try:
        rel = out_dir.resolve().relative_to(outputs_root.resolve())
    except ValueError:
        return None
    segs = rel.parts
    if len(segs) < 2:
        return None

    lop = next((s for s in segs if re.fullmatch(r"lop-\d+", s)), None)
    tier = next((re.fullmatch(r"lop-([a-x])", s).group(1).upper()
                 for s in segs if re.fullmatch(r"lop-[a-x]", s)), None)
    chuong = next((_chuong_so(s) for s in segs if _chuong_so(s) is not None), None)
    if not lop or not tier or chuong is None:
        return None

    parts = [lop.replace("-", ""), tier, f"Chuong {chuong}"]
    slug = segs[-1]

    if slug.startswith("thuyet-minh"):
        parts.append(f"Thuyet-minh-chuong-{_ROMAN.get(chuong, chuong)}")
        return DriveTarget(parts, "phiếu thuyết minh")

    # Phiếu học tập: lấy số Ca từ tiền tố file ca-NN-, tên lấy từ title của phiếu.
    ca = ""
    for pdf in sorted(out_dir.glob("ca-*-handout.pdf")):
        m = re.match(r"(ca-\d+)-", pdf.name)
        if m:
            ca = m.group(1).capitalize()      # 'ca-01' → 'Ca-01'
            break
    ten = bo_dau(tieu_de) if tieu_de else bo_dau(re.sub(r"^phieu-[a-z]-", "", slug).replace("-", " ")).capitalize()
    parts.append(f"{ca} - {ten}" if ca else ten)
    return DriveTarget(parts, "phiếu học tập")


def sync_dir(out_dir: Path, outputs_root: Path, tieu_de: str | None = None,
             dry_run: bool = False, root: Path | None = None) -> tuple[Path | None, list[str]]:
    """Chép mọi PDF trong `out_dir` sang đúng chỗ trên Drive. Trả (thư mục đích, tên file đã chép)."""
    target = plan_target(out_dir, outputs_root, tieu_de)
    if target is None:
        return None, []
    # Bộ build ghi SONG SONG hai tên cho cùng một bản ('handout.pdf' và 'ca-01-handout.pdf').
    # Drive chỉ nhận bộ có tiền tố Ca — đúng quy ước Thầy đã chép tay ở chương IV.
    pdfs = sorted(out_dir.glob("ca-*.pdf")) or sorted(out_dir.glob("*.pdf"))
    if not pdfs:
        return None, []

    goc = root if root is not None else drive_root()
    if dry_run:
        return di_toi(goc, target.parts, tao=False), [p.name for p in pdfs]

    goc.mkdir(parents=True, exist_ok=True)
    dest = di_toi(goc, target.parts)
    for p in pdfs:
        shutil.copy2(p, dest / p.name)      # ghi đè bản cũ, không sinh bản trùng
    return dest, [p.name for p in pdfs]
