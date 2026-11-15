#!/bin/bash
# Đẩy phiếu C Viète (ch.VI 9C) bản 12/11/2026 lên Drive — Thầy chạy ở Terminal (sandbox Claude chặn ghi CloudStorage).
# Chép vào ĐÚNG thư mục cũ "Ca-03 - …" (sync-drive sẽ đẻ thư mục sinh đôi "Bai 20. …" vì slug phieu-c- không có số ca).
# Bản cũ ca-03-*.pdf (10/09) được chuyển vào _ban-cu/ chứ không xoá.
set -e
cd "$(dirname "$0")/.."
G="$HOME/Library/CloudStorage/GoogleDrive-thaitd.mathtech@gmail.com/My Drive/giaoanmathtech/Lop 9 2026-2027/C/Chuong 6"
O=outputs/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai
CA="$G/Ca-03 - Bai 20. Dinh li Viete va ung dung"
[ -d "$CA" ] || { echo "Không thấy thư mục $CA"; exit 1; }
mkdir -p "$CA/_ban-cu"
for f in "$CA"/ca-03-*.pdf; do [ -e "$f" ] && mv "$f" "$CA/_ban-cu/"; done
cp -v "$O"/phieu-c-dinh-li-viete-va-ung-dung/Toan9C-Dinh-li-viete-va-ung-dung-{Phieu-HS,Phieu-BTVN,Dap-an-GV,Slide}.pdf "$CA/"
cp -v "$O"/thuyet-minh-lop-9c-chuong-06-pt-bac-hai/thuyet-minh-lop-9c-chuong-06-pt-bac-hai.pdf "$G/Thuyet-minh-chuong-VI/"
echo "Xong."
