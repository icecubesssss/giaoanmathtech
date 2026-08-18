#!/usr/bin/env python3
"""Tải ĐỀ THI Toán 9 HÀ NỘI (giữa kì II / cuối kì II) từ TOANMATH về inputs/refs/de-thi/.

Cách lấy: đọc sitemap của thcs.toanmath.com (post-sitemap*.xml) — đầy đủ và rẻ hơn
nhiều so với dò trang chuyên mục (mấy slug chuyên mục bị 301 về một bài lẻ).
Lọc slug theo 3 điều kiện, KHÔNG lấy bừa:
  • là đề Toán 9 giữa kì 2 / cuối kì 2   • có đuôi '-ha-noi'   • năm học 2024-2025 trở đi

VÌ SAO chặn năm ≥ 2024-2025: từ 2024-2025 lớp 9 Hà Nội mới học chương trình 2018
(Kết nối tri thức); đề các năm trước là chương trình cũ, lấy vào là sai chuẩn.
Lưu ý sitemap KHÔNG nói trường đó dùng bộ sách nào — cùng lắm chỉ chắc được "đề Hà Nội,
chương trình 2018". Trường nào dùng bộ khác thì phải soi từng đề mới biết.

PDF theo quy luật: https://thcs.toanmath.com/thcs-pdf/<slug>.pdf

Dùng:
    .venv/bin/python scripts/fetch_de_thi.py            # 20 đề mỗi loại
    .venv/bin/python scripts/fetch_de_thi.py --so 30
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "inputs" / "refs" / "de-thi" / "lop-9"
HOST = "https://thcs.toanmath.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# Năm học tối thiểu (chương trình 2018 cho lớp 9)
NAM_TOI_THIEU = 2024
# 'ki'/'ky', có/không 'hoc' — toanmath đặt slug không thống nhất
_GK = re.compile(r"/de-giua-(?:hoc-)?(?:ki|ky)-2-toan-9-nam-(\d{4})-\d{4}-(.+?)\.html$")
_CK = re.compile(r"/de-(?:cuoi-)?(?:hoc-)?(?:ki|ky)-2-toan-9-nam-(\d{4})-\d{4}-(.+?)\.html$")


def _get(url: str, timeout: int = 60) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": HOST + "/"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None


def thu_thap() -> tuple[list[str], list[str]]:
    """Quét sitemap → (danh sách slug giữa kì 2, danh sách slug cuối kì 2)."""
    idx = _get(f"{HOST}/sitemap_index.xml") or b""
    maps = [u for u in re.findall(r"<loc>([^<]+)</loc>", idx.decode("utf-8", "ignore"))
            if "post-sitemap" in u]
    gk, ck = [], []
    for m in maps:
        raw = _get(m)
        if not raw:
            continue
        for url in re.findall(r"<loc>([^<]+)</loc>", raw.decode("utf-8", "ignore")):
            if "toan-9" not in url or not url.endswith("-ha-noi.html"):
                continue
            for pat, bucket in ((_GK, gk), (_CK, ck)):
                mm = pat.search(url)
                if mm and int(mm.group(1)) >= NAM_TOI_THIEU:
                    bucket.append(url)
                    break
        time.sleep(0.05)
    # 'de-giua-...' cũng khớp _CK (vì 'cuoi-' là tuỳ chọn) ⇒ loại chéo cho sạch
    gk_set = set(gk)
    ck = [u for u in ck if u not in gk_set and "-giua-" not in u]
    # mới nhất trước (slug có năm trong đường dẫn /YYYY/MM/)
    return sorted(set(gk), reverse=True), sorted(set(ck), reverse=True)


def tai(urls: list[str], thu_muc: Path, so: int) -> list[str]:
    thu_muc.mkdir(parents=True, exist_ok=True)
    ket_qua, dem = [], 0
    for url in urls:
        if dem >= so:
            break
        slug = url.rsplit("/", 1)[-1][: -len(".html")]
        dest = thu_muc / f"{slug}.pdf"
        if dest.exists() and dest.stat().st_size > 0:
            ket_qua.append(f"SKIP {slug}")
            dem += 1
            continue
        data = _get(f"{HOST}/thcs-pdf/{slug}.pdf?v=1")
        if not data or data[:4] != b"%PDF":
            ket_qua.append(f"FAIL {slug}")
            continue
        dest.write_bytes(data)
        ket_qua.append(f"OK   {len(data)/1e6:.1f}MB  {slug}")
        dem += 1
        time.sleep(0.15)
    return ket_qua


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", type=int, default=20, help="số đề mỗi loại (mặc định 20)")
    args = ap.parse_args(argv[1:])

    print("▶ Quét sitemap thcs.toanmath.com…", flush=True)
    gk, ck = thu_thap()
    print(f"  tìm được {len(gk)} đề GIỮA KÌ 2 và {len(ck)} đề CUỐI KÌ 2 (Hà Nội, "
          f"từ năm học {NAM_TOI_THIEU}-{NAM_TOI_THIEU+1})", flush=True)

    for ten, urls, thu_muc in (("GIỮA KÌ 2", gk, OUT / "giua-ki-2"),
                               ("CUỐI KÌ 2", ck, OUT / "de-cuoi-ki-2")):
        print(f"\n▶ {ten} → {thu_muc.relative_to(ROOT)}", flush=True)
        for dong in tai(urls, thu_muc, args.so):
            print("  " + dong, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
