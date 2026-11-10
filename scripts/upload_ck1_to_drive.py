#!/usr/bin/env python3
"""Đồng bộ toàn bộ Đề ôn tập & Đề kiểm tra Cuối Kì 1 lên Google Drive.
Bao gồm:
- 3 Đề ôn tập cuối kì 1 (Đề HS, Đáp án GV, Slide, Ma trận)
- 3 Đề kiểm tra cuối kì 1 chính thức (Đề HS, Đáp án GV, Slide, Ma trận)
- Báo cáo thống kê lưới dạng & cơ sở sư phạm bốc câu (.md & .xlsx)
Kiểm tra đối chiếu checksum toàn bộ các file.
"""
import filecmp
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRIVE_ROOT = Path("/Users/admin/Library/CloudStorage/GoogleDrive-thaitd.mathtech@gmail.com/My Drive/giaoanmathtech/Lop 9 2026-2027/On tap cuoi ki 1")
OUTPUTS = ROOT / "outputs/lop-9/de-on-tap-cuoi-ki-1"

MAPPING = [
    (
        "1 - De on tap so 1",
        [
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-1/Toan9-De-on-tap-cuoi-ki-1-so-1-Phieu-HS.pdf",
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-1/Toan9-De-on-tap-cuoi-ki-1-so-1-Dap-an-GV.pdf",
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-1/Toan9-De-on-tap-cuoi-ki-1-so-1-Slide.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-1/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-1-Phieu-HS.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-1/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-1-Dap-an-GV.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-1/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-1-Slide.pdf",
        ],
    ),
    (
        "2 - De on tap so 2",
        [
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-2/Toan9-De-on-tap-cuoi-ki-1-so-2-Phieu-HS.pdf",
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-2/Toan9-De-on-tap-cuoi-ki-1-so-2-Dap-an-GV.pdf",
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-2/Toan9-De-on-tap-cuoi-ki-1-so-2-Slide.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-2/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-2-Phieu-HS.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-2/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-2-Dap-an-GV.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-2/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-2-Slide.pdf",
        ],
    ),
    (
        "3 - De on tap so 3",
        [
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-3/Toan9-De-on-tap-cuoi-ki-1-so-3-Phieu-HS.pdf",
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-3/Toan9-De-on-tap-cuoi-ki-1-so-3-Dap-an-GV.pdf",
            OUTPUTS / "de-on-tap-cuoi-ki-1-so-3/Toan9-De-on-tap-cuoi-ki-1-so-3-Slide.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-3/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-3-Phieu-HS.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-3/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-3-Dap-an-GV.pdf",
            OUTPUTS / "ma-tran-va-dap-an-on-tap-ck1-so-3/Toan9-Ma-tran-va-dap-an-on-tap-ck1-so-3-Slide.pdf",
        ],
    ),
    (
        "4 - De kiem tra cuoi ki 1 chinh thuc so 1",
        [
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-1-Phieu-HS.pdf",
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-1-Dap-an-GV.pdf",
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-1-Slide.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-1/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-1-Phieu-HS.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-1/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-1-Dap-an-GV.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-1/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-1-Slide.pdf",
        ],
    ),
    (
        "5 - De kiem tra cuoi ki 1 chinh thuc so 2",
        [
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-2-Phieu-HS.pdf",
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-2-Dap-an-GV.pdf",
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-2-Slide.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-2/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-2-Phieu-HS.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-2/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-2-Dap-an-GV.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-2/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-2-Slide.pdf",
        ],
    ),
    (
        "6 - De kiem tra cuoi ki 1 chinh thuc so 3",
        [
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-3-Phieu-HS.pdf",
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-3-Dap-an-GV.pdf",
            OUTPUTS / "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3/Toan9-De-kiem-tra-cuoi-ki-1-chinh-thuc-so-3-Slide.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-3/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-3-Phieu-HS.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-3/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-3-Dap-an-GV.pdf",
            OUTPUTS / "ma-tran-va-dap-an-ck1-chinh-thuc-so-3/Toan9-Ma-tran-va-dap-an-ck1-chinh-thuc-so-3-Slide.pdf",
        ],
    ),
]

DOCS = [
    ROOT / "outputs/thong-ke-dang-de/Thong-ke-dang-CK1-Toan9-luoi-tay.md",
    ROOT / "outputs/thong-ke-dang-de/Thong-ke-dang-CK1-Toan9-luoi-tay.xlsx",
]


def main():
    print(f"Bắt đầu đồng bộ lên Google Drive: {DRIVE_ROOT}")
    DRIVE_ROOT.mkdir(parents=True, exist_ok=True)

    # 1. Đồng bộ các file tài liệu thống kê
    print("\n1. Đồng bộ báo cáo thống kê & lý do bốc câu:")
    for doc in DOCS:
        assert doc.exists(), f"Không tìm thấy file: {doc}"
        dst = DRIVE_ROOT / doc.name
        shutil.copy2(doc, dst)
        assert filecmp.cmp(doc, dst, shallow=False), f"Lỗi checksum file: {doc.name}"
        print(f"  ✓ {doc.name} (khớp checksum)")

    # 2. Đồng bộ các thư mục đề
    total_files = 0
    print("\n2. Đồng bộ 6 thư mục đề thi:")
    for folder_name, files in MAPPING:
        dst_folder = DRIVE_ROOT / folder_name
        dst_folder.mkdir(parents=True, exist_ok=True)
        print(f"\n  📁 {folder_name}:")
        for src in files:
            assert src.exists(), f"Không tìm thấy file PDF: {src}"
            dst = dst_folder / src.name
            shutil.copy2(src, dst)
            assert filecmp.cmp(src, dst, shallow=False), f"Lỗi checksum: {src.name}"
            size_kb = dst.stat().st_size / 1024
            print(f"    ✓ {src.name} ({size_kb:.1f} KB - khớp checksum)")
            total_files += 1

    print(f"\n============================================================")
    print(f"✓ ĐỒNG BỘ THÀNH CÔNG TRỌN VẸN {total_files} FILE PDF VÀ 2 FILE BÁO CÁO LÊN DRIVE!")
    print(f"  Đường dẫn: {DRIVE_ROOT}")


if __name__ == "__main__":
    main()

