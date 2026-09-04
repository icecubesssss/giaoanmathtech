#!/usr/bin/env python3
"""Tải ĐỀ THI Toán HÀ NỘI cho CẢ 4 KHỐI 6-7-8-9 × 4 KỲ (GK1, CK1, GK2, CK2) từ TOANMATH.

Mở rộng `fetch_de_thi.py` (bản cũ chỉ lấy lớp 9 giữa/cuối kì II). Cách lấy vẫn là đọc
sitemap của thcs.toanmath.com — đầy đủ và rẻ hơn dò trang chuyên mục.

Bộ lọc (Thầy chốt 2026-08-30): CHỈ Hà Nội, CHỈ chương trình 2018 (KNTT).
  • slug phải kết thúc '-ha-noi'  → đề Hà Nội
  • năm học ≥ năm khối đó BẮT ĐẦU học chương trình 2018 (lớp 6: 2021, 7: 2022,
    8: 2023, 9: 2024) → loại đề chương trình cũ
  • loại đề HSG / khảo sát / tuyển sinh / chuyên / đề cương ôn tập
Sitemap KHÔNG ghi trường dùng bộ sách nào ⇒ khâu chốt "đúng KNTT" làm ở bước sau
(`screen_kntt.py`) bằng cách soi nội dung PDF, không suy đoán từ slug.

PDF theo quy luật: https://thcs.toanmath.com/thcs-pdf/<slug>.pdf

Dùng:
    .venv/bin/python scripts/fetch_de_thi_khoi.py                 # 20 đề mỗi (khối, kỳ)
    .venv/bin/python scripts/fetch_de_thi_khoi.py --so 35
    .venv/bin/python scripts/fetch_de_thi_khoi.py --lop 6,7 --ky gk1,ck1
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
OUT = ROOT / "inputs" / "refs" / "de-thi"
HOST = "https://thcs.toanmath.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
CACHE = ROOT / "storage" / "cache" / "toanmath_urls.txt"

# Năm học ĐẦU TIÊN mỗi khối học chương trình 2018 (đề trước đó là CT cũ — loại)
NAM_2018 = {"6": 2021, "7": 2022, "8": 2023, "9": 2024}

# Thư mục đích mỗi kỳ. Lớp 9 CK2 giữ tên cũ 'de-cuoi-ki-2' để không đẻ thư mục sinh đôi.
THU_MUC = {"gk1": "giua-ki-1", "ck1": "cuoi-ki-1", "gk2": "giua-ki-2", "ck2": "cuoi-ki-2"}
THU_MUC_RIENG = {("9", "ck2"): "de-cuoi-ki-2"}

# Đề KHÔNG lấy: không phải kiểm tra định kì của trường
_LOAI_TRU = re.compile(
    r"hoc-sinh-gioi|hsg|khao-sat|tuyen-sinh|vao-lop-10|vao-10|chuyen|olympic|"
    r"de-cuong|on-tap|violympic|tuyen-chon|thu-suc|thi-thu"
)
_NAM = re.compile(r"nam-(\d{4})-\d{4}")


def _get(url: str, timeout: int = 60) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": HOST + "/"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None


def quet_sitemap(dung_cache: bool = True) -> list[str]:
    """Danh sách URL bài viết của thcs.toanmath.com (cache ra file cho lần sau)."""
    if dung_cache and CACHE.exists() and CACHE.stat().st_size > 0:
        return CACHE.read_text(encoding="utf-8").splitlines()
    idx = _get(f"{HOST}/sitemap_index.xml") or b""
    maps = [u for u in re.findall(r"<loc>([^<]+)</loc>", idx.decode("utf-8", "ignore"))
            if "post-sitemap" in u]
    urls: list[str] = []
    for m in maps:
        raw = _get(m)
        if raw:
            urls += re.findall(r"<loc>([^<]+)</loc>", raw.decode("utf-8", "ignore"))
        time.sleep(0.05)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text("\n".join(urls), encoding="utf-8")
    return urls


def phan_loai(url: str) -> tuple[str, str, int] | None:
    """(lớp, kỳ, năm) của một URL đề, hoặc None nếu không phải đề định kì Hà Nội hợp lệ.

    Kỳ: gk1/ck1/gk2/ck2. 'giữa kì' nhận ra bằng chữ 'giua'; học kì I/II bằng '-1'/'-2'
    ngay sau 'ki|ky', hoặc 'hk1|hk2'."""
    if not url.endswith("-ha-noi.html"):
        return None
    slug = url.rsplit("/", 1)[-1][: -len(".html")]
    if _LOAI_TRU.search(slug):
        return None
    m = re.search(r"-toan-([6789])-", slug)
    if not m:
        return None
    lop = m.group(1)
    dau = slug[: m.start()]                       # phần trước '-toan-N-' mới nói về kỳ thi
    giua = "giua" in dau
    if re.search(r"(?:ki|ky)-1\b|hk1", dau):
        hoc_ki = 1
    elif re.search(r"(?:ki|ky)-2\b|hk2", dau):
        hoc_ki = 2
    else:
        return None
    mn = _NAM.search(slug)
    if not mn or int(mn.group(1)) < NAM_2018[lop]:
        return None
    ky = f"{'gk' if giua else 'ck'}{hoc_ki}"
    return lop, ky, int(mn.group(1))


def dem_hien_co(lop: str, ky: str) -> int:
    thu_muc = OUT / f"lop-{lop}" / THU_MUC_RIENG.get((lop, ky), THU_MUC[ky])
    if not thu_muc.exists():
        return 0
    return len(list(thu_muc.rglob("*.pdf")))


def tai(urls: list[str], thu_muc: Path, so: int) -> list[str]:
    """Tải tối đa `so` PDF vào thư mục; bỏ qua file đã có."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    ket_qua, dem = [], 0
    for url in urls:
        if dem >= so:
            break
        slug = url.rsplit("/", 1)[-1][: -len(".html")]
        dest = thu_muc / f"{slug}.pdf"
        if dest.exists() and dest.stat().st_size > 0:
            continue
        data = _get(f"{HOST}/thcs-pdf/{slug}.pdf?v=1")
        if not data or data[:4] != b"%PDF":
            ket_qua.append(f"  FAIL {slug}")
            continue
        dest.write_bytes(data)
        ket_qua.append(f"  OK   {len(data)/1e6:>4.1f}MB  {slug}")
        dem += 1
        time.sleep(0.15)
    return ket_qua


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", type=int, default=20, help="số đề MỖI (khối, kỳ) cần có (mặc định 20)")
    ap.add_argument("--lop", default="6,7,8,9")
    ap.add_argument("--ky", default="gk1,ck1,gk2,ck2")
    ap.add_argument("--moi", action="store_true", help="quét lại sitemap, bỏ cache")
    args = ap.parse_args(argv[1:])
    lops = args.lop.split(",")
    kys = args.ky.split(",")

    print("▶ Quét sitemap thcs.toanmath.com…", flush=True)
    urls = quet_sitemap(dung_cache=not args.moi)
    print(f"  {len(urls)} URL bài viết", flush=True)

    kho: dict[tuple[str, str], list[tuple[int, str]]] = {}
    for u in urls:
        pl = phan_loai(u)
        if not pl:
            continue
        lop, ky, nam = pl
        kho.setdefault((lop, ky), []).append((nam, u))

    print("\n▶ Đề Hà Nội, chương trình 2018, có trên sitemap:")
    for lop in lops:
        dong = "  lớp {}: ".format(lop) + "  ".join(
            f"{ky.upper()} {len(kho.get((lop, ky), []))}" for ky in kys)
        print(dong, flush=True)

    for lop in lops:
        for ky in kys:
            co = dem_hien_co(lop, ky)
            thieu = max(0, args.so - co)
            thu_muc = OUT / f"lop-{lop}" / THU_MUC_RIENG.get((lop, ky), THU_MUC[ky])
            print(f"\n▶ lớp {lop} · {ky.upper()} — đang có {co}, cần thêm {thieu} "
                  f"→ {thu_muc.relative_to(ROOT)}", flush=True)
            if not thieu:
                continue
            ds = [u for _, u in sorted(kho.get((lop, ky), []), reverse=True)]
            if not ds:
                print("  (sitemap không có đề nào khớp bộ lọc)", flush=True)
                continue
            for dong in tai(ds, thu_muc, thieu):
                print(dong, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
