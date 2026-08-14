#!/usr/bin/env python3
"""Tải SÁCH GIÁO VIÊN (SGV) Toán Kết nối tri thức khối 6-12 về inputs/refs/sgv/.

VÌ SAO CÓ SCRIPT NÀY: SGV Toán KNTT không có bản PDF tải thẳng ở đâu cả — toanmath
không có, mấy blog thì link Google Drive chết hoặc đòi đăng nhập, nguồn chính thức
hanhtrangso.nxbgd.vn cần tài khoản giáo viên. Chỗ duy nhất lấy được là
sach.baikiemtra.com, nhưng site đó phục vụ sách dưới dạng ẢNH TỪNG TRANG:

    https://sach.baikiemtra.com/uploads/book/sgv-toan-<N>-ket-noi-tri-thuc/sgv-toan-<N>-kntt-<i>.jpg

Script tải hết ảnh rồi GHÉP thành PDF. Việc ghép viết tay bằng Python thuần vì máy
Thầy không có Pillow / img2pdf / ImageMagick; JPEG được NHÚNG THẲNG vào PDF qua filter
/DCTDecode nên không giải nén–nén lại, không mất chất lượng và chạy rất nhanh.

Lưu ý: PDF ra là ẢNH SCAN, KHÔNG có lớp text (giống SGK trong inputs/refs/sgk/) —
muốn tra nội dung thì phải đọc bằng mắt, `grep`/`pdftotext` vô dụng.

Dùng:
    .venv/bin/python scripts/fetch_sgv.py            # cả khối 6-12
    .venv/bin/python scripts/fetch_sgv.py 7 9        # chỉ vài khối
"""
from __future__ import annotations

import struct
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = ROOT / "inputs" / "refs" / "sgv"
HOST = "https://sach.baikiemtra.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
GRADES = (6, 7, 8, 9, 10, 11, 12)
A4_WIDTH_PT = 595.276          # bề ngang A4; mỗi trang co về đúng khổ này
MAX_MISS = 3                   # 404 liên tiếp bao nhiêu lần thì coi là hết sách


def _url(grade: int, page: int) -> str:
    slug = f"sgv-toan-{grade}-ket-noi-tri-thuc"
    return f"{HOST}/uploads/book/{slug}/sgv-toan-{grade}-kntt-{page}.jpg"


def _get(url: str, timeout: int = 40) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": HOST + "/"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None
    # Site trả trang HTML báo lỗi thay vì 404 trong vài trường hợp
    return data if data[:2] == b"\xff\xd8" else None


def jpeg_size(data: bytes) -> tuple[int, int]:
    """(rộng, cao) tính bằng pixel, đọc từ marker SOF của JPEG."""
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker, seglen = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        # SOF0..SOF15, trừ DHT(C4) / RSTn(C8) / DAC(CC)
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + seglen
    raise ValueError("không đọc được kích thước JPEG")


def jpegs_to_pdf(pages: list[bytes], dest: Path) -> None:
    """Ghép danh sách ảnh JPEG thành PDF, mỗi ảnh một trang, khổ ngang A4.

    Nhúng nguyên bytes JPEG qua /DCTDecode — không đụng vào dữ liệu ảnh."""
    objs: list[bytes] = []          # objs[k] là nội dung object số k+1

    def add(body: bytes) -> int:
        objs.append(body)
        return len(objs)

    root_num, pages_num = 1, 2
    objs.extend([b"", b""])          # giữ chỗ cho Catalog + Pages

    kids = []
    for data in pages:
        w_px, h_px = jpeg_size(data)
        w_pt = A4_WIDTH_PT
        h_pt = h_px * (w_pt / w_px)
        img_num = add(
            b"<< /Type /XObject /Subtype /Image /Width " + str(w_px).encode()
            + b" /Height " + str(h_px).encode()
            + b" /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length "
            + str(len(data)).encode() + b" >>\nstream\n" + data + b"\nendstream")
        content = (f"q {w_pt:.2f} 0 0 {h_pt:.2f} 0 0 cm /I0 Do Q").encode()
        cont_num = add(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n"
                       + content + b"\nendstream")
        page_num = add(
            b"<< /Type /Page /Parent " + str(pages_num).encode() + b" 0 R /MediaBox [0 0 "
            + f"{w_pt:.2f} {h_pt:.2f}".encode() + b"] /Resources << /XObject << /I0 "
            + str(img_num).encode() + b" 0 R >> >> /Contents "
            + str(cont_num).encode() + b" 0 R >>")
        kids.append(page_num)

    objs[root_num - 1] = b"<< /Type /Catalog /Pages " + str(pages_num).encode() + b" 0 R >>"
    objs[pages_num - 1] = (b"<< /Type /Pages /Count " + str(len(kids)).encode() + b" /Kids ["
                           + b" ".join(str(k).encode() + b" 0 R" for k in kids) + b"] >>")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for num, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += str(num).encode() + b" 0 obj\n" + body + b"\nendobj\n"
    xref_at = len(out)
    out += b"xref\n0 " + str(len(objs) + 1).encode() + b"\n0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (b"trailer\n<< /Size " + str(len(objs) + 1).encode() + b" /Root "
            + str(root_num).encode() + b" 0 R >>\nstartxref\n"
            + str(xref_at).encode() + b"\n%%EOF\n")
    dest.write_bytes(bytes(out))


def fetch_grade(grade: int) -> str:
    dest = OUT_ROOT / f"lop-{grade}" / f"sgv-toan-{grade}-kntt.pdf"
    if dest.exists() and dest.stat().st_size > 0:
        return f"SKIP (đã có) {dest.relative_to(ROOT)}"
    dest.parent.mkdir(parents=True, exist_ok=True)

    pages: list[bytes] = []
    page, miss = 0, 0
    while miss < MAX_MISS:
        data = _get(_url(grade, page))
        if data is None:
            miss += 1
        else:
            miss = 0
            pages.append(data)
            if len(pages) % 25 == 0:
                print(f"    lớp {grade}: {len(pages)} trang…", flush=True)
        page += 1
        time.sleep(0.05)           # lịch sự với server

    if not pages:
        return f"FAIL lớp {grade}: không tải được trang nào"
    jpegs_to_pdf(pages, dest)
    mb = dest.stat().st_size / 1e6
    return f"OK   lớp {grade}: {len(pages)} trang, {mb:.1f} MB → {dest.relative_to(ROOT)}"


def main(argv: list[str]) -> int:
    grades = [int(a) for a in argv[1:]] or list(GRADES)
    for g in grades:
        print(f"▶ SGV Toán {g} Kết nối tri thức…", flush=True)
        print("  " + fetch_grade(g), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
