#!/usr/bin/env python3
"""Đồng bộ toàn bộ Đề ôn tập & Đề kiểm tra Cuối Kì 1 Lớp 8 và Lớp 5 lên Google Drive.
Bao gồm:
- Lớp 8: 3 Đề ôn tập + 3 Đề chính thức + Ma trận & Đáp án chi tiết (36 files PDF)
- Lớp 5: 3 Đề ôn tập + 3 Đề chính thức + Ma trận & Đáp án chi tiết (36 files PDF)
Kiểm tra đối chiếu checksum toàn bộ các file và truy xuất link chia sẻ Drive của 2 folder tổng.
"""
import filecmp
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRIVE_BASE = Path("/Users/admin/Library/CloudStorage/GoogleDrive-thaitd.mathtech@gmail.com/My Drive/giaoanmathtech")

# ────────────────────────── LỚP 8 ──────────────────────────
LOP8_SRC = ROOT / "outputs/lop-8/de-on-tap-cuoi-ki-1"
LOP8_DST = DRIVE_BASE / "Lop 8 2026-2027" / "On tap cuoi ki 1"

LOP8_MAPPING = [
    (
        "1 - De on tap so 1",
        [
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-1/Toan8-De-on-tap-cuoi-ki-1-so-1-Phieu-HS.pdf",
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-1/Toan8-De-on-tap-cuoi-ki-1-so-1-Dap-an-GV.pdf",
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-1/Toan8-De-on-tap-cuoi-ki-1-so-1-Slide.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-1/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-1-Phieu-HS.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-1/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-1-Dap-an-GV.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-1/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-1-Slide.pdf",
        ]
    ),
    (
        "2 - De on tap so 2",
        [
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-2/Toan8-De-on-tap-cuoi-ki-1-so-2-Phieu-HS.pdf",
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-2/Toan8-De-on-tap-cuoi-ki-1-so-2-Dap-an-GV.pdf",
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-2/Toan8-De-on-tap-cuoi-ki-1-so-2-Slide.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-2/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-2-Phieu-HS.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-2/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-2-Dap-an-GV.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-2/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-2-Slide.pdf",
        ]
    ),
    (
        "3 - De on tap so 3",
        [
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-3/Toan8-De-on-tap-cuoi-ki-1-so-3-Phieu-HS.pdf",
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-3/Toan8-De-on-tap-cuoi-ki-1-so-3-Dap-an-GV.pdf",
            LOP8_SRC / "de-on-tap-cuoi-ki-1-so-3/Toan8-De-on-tap-cuoi-ki-1-so-3-Slide.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-3/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-3-Phieu-HS.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-3/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-3-Dap-an-GV.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-on-tap-ck1-so-3/Toan8-Ma-tran-va-dap-an-on-tap-ck1-so-3-Slide.pdf",
        ]
    ),
    (
        "4 - De kiem tra cuoi ki 1 chinh thuc so 1",
        [
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-1-Phieu-HS.pdf",
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-1-Dap-an-GV.pdf",
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-1-Slide.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-1/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-1-Phieu-HS.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-1/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-1-Dap-an-GV.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-1/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-1-Slide.pdf",
        ]
    ),
    (
        "5 - De kiem tra cuoi ki 1 chinh thuc so 2",
        [
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-2-Phieu-HS.pdf",
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-2-Dap-an-GV.pdf",
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-2-Slide.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-2/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-2-Phieu-HS.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-2/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-2-Dap-an-GV.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-2/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-2-Slide.pdf",
        ]
    ),
    (
        "6 - De kiem tra cuoi ki 1 chinh thuc so 3",
        [
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-3-Phieu-HS.pdf",
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-3-Dap-an-GV.pdf",
            LOP8_SRC / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3/Toan8-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-3-Slide.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-3/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-3-Phieu-HS.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-3/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-3-Dap-an-GV.pdf",
            LOP8_SRC / "ma-tran-va-dap-an-ck1-chinh-thuc-so-3/Toan8-Ma-tran-va-dap-an-ck1-chinh-thuc-so-3-Slide.pdf",
        ]
    ),
]

# ────────────────────────── LỚP 5 ──────────────────────────
LOP5_SRC = ROOT / "outputs/lop-5/de-cuoi-ki-1"
LOP5_DST = DRIVE_BASE / "Lop 5 2026-2027" / "On tap cuoi ki 1"

LOP5_MAPPING = [
    (
        "1 - De on tap so 1",
        [
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-1/Toan5-De-on-tap-cuoi-ki-1-so-1-Phieu-HS.pdf",
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-1/Toan5-De-on-tap-cuoi-ki-1-so-1-Dap-an-GV.pdf",
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-1/Toan5-De-on-tap-cuoi-ki-1-so-1-Slide.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-1/Toan5-Ma-tran-va-dap-an-on-tap-so-1-Phieu-HS.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-1/Toan5-Ma-tran-va-dap-an-on-tap-so-1-Dap-an-GV.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-1/Toan5-Ma-tran-va-dap-an-on-tap-so-1-Slide.pdf",
        ]
    ),
    (
        "2 - De on tap so 2",
        [
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-2/Toan5-De-on-tap-cuoi-ki-1-so-2-Phieu-HS.pdf",
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-2/Toan5-De-on-tap-cuoi-ki-1-so-2-Dap-an-GV.pdf",
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-2/Toan5-De-on-tap-cuoi-ki-1-so-2-Slide.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-2/Toan5-Ma-tran-va-dap-an-on-tap-so-2-Phieu-HS.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-2/Toan5-Ma-tran-va-dap-an-on-tap-so-2-Dap-an-GV.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-2/Toan5-Ma-tran-va-dap-an-on-tap-so-2-Slide.pdf",
        ]
    ),
    (
        "3 - De on tap so 3",
        [
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-3/Toan5-De-on-tap-cuoi-ki-1-so-3-Phieu-HS.pdf",
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-3/Toan5-De-on-tap-cuoi-ki-1-so-3-Dap-an-GV.pdf",
            LOP5_SRC / "de-on-tap-cuoi-ki-1-so-3/Toan5-De-on-tap-cuoi-ki-1-so-3-Slide.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-3/Toan5-Ma-tran-va-dap-an-on-tap-so-3-Phieu-HS.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-3/Toan5-Ma-tran-va-dap-an-on-tap-so-3-Dap-an-GV.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-on-tap-so-3/Toan5-Ma-tran-va-dap-an-on-tap-so-3-Slide.pdf",
        ]
    ),
    (
        "4 - De kiem tra cuoi ki 1 chinh thuc so 1",
        [
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-1/Toan5-De-kiem-tra-cuoi-ki-1-de-1-Phieu-HS.pdf",
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-1/Toan5-De-kiem-tra-cuoi-ki-1-de-1-Dap-an-GV.pdf",
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-1/Toan5-De-kiem-tra-cuoi-ki-1-de-1-Slide.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-1/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-1-Phieu-HS.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-1/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-1-Dap-an-GV.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-1/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-1-Slide.pdf",
        ]
    ),
    (
        "5 - De kiem tra cuoi ki 1 chinh thuc so 2",
        [
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-2/Toan5-De-kiem-tra-cuoi-ki-1-de-2-Phieu-HS.pdf",
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-2/Toan5-De-kiem-tra-cuoi-ki-1-de-2-Dap-an-GV.pdf",
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-2/Toan5-De-kiem-tra-cuoi-ki-1-de-2-Slide.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-2/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-2-Phieu-HS.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-2/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-2-Dap-an-GV.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-2/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-2-Slide.pdf",
        ]
    ),
    (
        "6 - De kiem tra cuoi ki 1 chinh thuc so 3",
        [
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-3/Toan5-De-kiem-tra-cuoi-ki-1-de-3-Phieu-HS.pdf",
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-3/Toan5-De-kiem-tra-cuoi-ki-1-de-3-Dap-an-GV.pdf",
            LOP5_SRC / "de-kiem-tra-cuoi-ki-1-de-3/Toan5-De-kiem-tra-cuoi-ki-1-de-3-Slide.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-3/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-3-Phieu-HS.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-3/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-3-Dap-an-GV.pdf",
            LOP5_SRC / "ma-tran-va-dap-an-cuoi-ki-1-de-3/Toan5-Ma-tran-va-dap-an-cuoi-ki-1-de-3-Slide.pdf",
        ]
    ),
]


def sync_collection(title: str, dst_root: Path, mapping: list):
    print(f"\n============================================================")
    print(f"▶ ĐỒNG BỘ: {title.upper()}")
    print(f"  Thư mục đích: {dst_root}")
    dst_root.mkdir(parents=True, exist_ok=True)

    total_files = 0
    for folder_name, files in mapping:
        dst_folder = dst_root / folder_name
        dst_folder.mkdir(parents=True, exist_ok=True)
        print(f"\n  📁 {folder_name}:")
        for src in files:
            assert src.exists(), f"Không tìm thấy file nguồn: {src}"
            dst = dst_folder / src.name
            shutil.copy2(src, dst)
            assert filecmp.cmp(src, dst, shallow=False), f"Lỗi checksum không khớp: {src.name}"
            size_kb = dst.stat().st_size / 1024
            print(f"    ✓ {src.name} ({size_kb:.1f} KB - khớp checksum)")
            total_files += 1

    print(f"\n✓ Hoàn thành đồng bộ {total_files} file cho {title}!")
    return total_files


def get_drive_link(path: Path) -> str:
    try:
        res = subprocess.run(['xattr', '-p', 'com.google.drivefs.item-id#S', str(path)],
                             capture_output=True, text=True, check=True)
        item_id = res.stdout.strip()
        if item_id:
            return f"https://drive.google.com/drive/folders/{item_id}"
    except Exception:
        pass
    return ""


def main():
    sync_collection("Toán 8 - Cuối Kì 1", LOP8_DST, LOP8_MAPPING)
    sync_collection("Toán 5 - Cuối Kì 1", LOP5_DST, LOP5_MAPPING)

    print("\n============================================================")
    print("Đang truy vấn liên kết Google Drive trực tiếp...")
    
    # Cho DriveFS vài giây để đồng bộ metadata nếu folder mới tạo
    for _ in range(10):
        link8 = get_drive_link(LOP8_DST)
        link5 = get_drive_link(LOP5_DST)
        if link8 and link5:
            break
        time.sleep(1)

    print(f"\nLink Folder Lớp 8: {link8 or 'Đang đồng bộ...'}")
    print(f"Link Folder Lớp 5: {link5 or 'Đang đồng bộ...'}")


if __name__ == "__main__":
    main()

