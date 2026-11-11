#!/usr/bin/env python3
"""Tải ĐỀ THI Toán TIỂU HỌC (lớp 3, 4) — đề CHÍNH THỨC của trường/phòng, năm học 2025-2026+.

Luật lấy đề (Thầy chốt 10/11/2026, khác THCS):
  • tỉnh nào cũng được, bộ sách nào cũng được — nhưng phải là đề CÓ TÊN TRƯỜNG/PHÒNG
    (đề "Bộ 10/15/20 đề…", "Đề số N" tự soạn của trang tổng hợp ⇒ LOẠI: ma trận dễ sai)
  • năm học 2024-2025 trở đi (Thầy nới 10/11/2026 vì thiếu đề Hà Nội và đề lớp 3; ban đầu chỉ 2025-2026)
  • lưu LINK NGUỒN từng đề để Thầy kiểm chứng chất lượng nguồn

Nguồn (dò 10/11/2026): hệ VietJack là nơi duy nhất trên mạng mở gom đề trường thật lớp 3-4:
  1. vietjack.com/de-kiem-tra-…/<slug>.jsp — có ẢNH CHỤP ĐỀ GỐC từng trang (images1/<slug>-N.PNG)
  2. khoahoc.vietjack.com/thi-online/<bộ>/<id> — bản gõ lại từng câu + "Đáp án đúng là"
     (chỉ để đối chiếu — đề phải chép từ ẢNH, không từ bản gõ)
  3. khoahoc.vietjack.com/chi-tiet-de-thi/<id> — PDF gốc
Đã soát và LOẠI: hoatieu.vn / vndoc / download.vn / dethi.edu.vn (đề tự soạn hoặc bán file),
Violet (cần đăng nhập + JS), tieuhoc.toanmath.com (không tồn tại).

Ra: inputs/refs/de-thi/lop-N/<kỳ>/<slug>.pdf (+ thư mục ảnh) và
    inputs/refs/de-thi/tieu-hoc-nguon-tai.json (manifest: tên, trường, tỉnh, kỳ, link).

Dùng:
    .venv/bin/python scripts/fetch_de_thi_tieu_hoc.py            # tải hết
    .venv/bin/python scripts/fetch_de_thi_tieu_hoc.py --chi-in   # chỉ in danh sách
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "inputs" / "refs" / "de-thi"
MANIFEST = OUT / "tieu-hoc-nguon-tai.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
VJ = "https://vietjack.com"
KH = "https://khoahoc.vietjack.com"

THU_MUC = {"gk1": "giua-ki-1", "ck1": "cuoi-ki-1", "gk2": "giua-ki-2", "ck2": "cuoi-ki-2"}
NAM_TOI_THIEU = 2024

# Trang mục lục .jsp chứa danh sách đề các trường (mỗi lớp × kỳ)
MUC_LUC_JSP = [
    "de-kiem-tra-lop-3/de-kiem-tra-toan-lop-3-hoc-ki-1.jsp",
    "de-kiem-tra-lop-3/de-kiem-tra-toan-3-cuoi-ki-1.jsp",
    "de-kiem-tra-lop-3/de-kiem-tra-toan-3-giua-ki-1.jsp",
    "de-kiem-tra-lop-3/de-kiem-tra-toan-3-giua-ki-2.jsp",
    "de-kiem-tra-lop-3/de-kiem-tra-toan-3-cuoi-ki-2.jsp",
    "de-kiem-tra-toan-lop-4/de-kiem-tra-toan-4-giua-ki-1.jsp",
    "de-kiem-tra-toan-lop-4/de-kiem-tra-toan-4-cuoi-ki-1.jsp",
    "de-kiem-tra-toan-lop-4/de-kiem-tra-toan-4-giua-ki-2.jsp",
    "de-kiem-tra-toan-lop-4/de-kiem-tra-toan-4-cuoi-ki-2.jsp",
]
# Trang danh sách bộ đề thi online (bản gõ + đáp án)
MUC_LUC_ONLINE = [f"{KH}/trac-nghiem/Lop-{l}/mon-Toan?type=test&book={b}"
                  for l in (3, 4) for b in (1, 2, 3)]
# Trang danh mục đề các trường (PDF gốc)
MUC_LUC_CHI_TIET = [f"{KH}/dap-an-de-thi/Toan/Lop-{l}/{k}" for l in (3, 4)
                    for k in ("de-thi-giua-ki-1", "de-thi-cuoi-ki-1",
                              "de-thi-giua-ki-2", "de-thi-cuoi-ki-2")]


def get(url: str, timeout: int = 60) -> bytes:
    r = subprocess.run(["curl", "-s", "-L", "-m", str(timeout), "-A", UA, url],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else b""


def text(url: str) -> str:
    return get(url).decode("utf-8", "ignore")


def sach(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def khong_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def phan_tich_ten(ten: str) -> dict | None:
    """'Đề thi Học kì 1 Toán lớp 4 năm 2025-2026 trường Tiểu học Đồng Hòa (Hải Phòng)'."""
    m = re.search(r"(Giữa kì|Học kì|Cuối kì|giữa kì|học kì|cuối kì)\s*([12]).*?lớp\s*([345]).*?"
                  r"(20\d\d)\s*[-–]\s*(20\d\d)", ten)
    if not m:
        return None
    loai, so, lop, nam = m.group(1).lower(), m.group(2), m.group(3), int(m.group(4))
    ky = ("gk" if "giữa" in loai else "ck") + so
    sau = ten[m.end():]
    tinh = (re.findall(r"\(([^()]+)\)", sau) or [""])[-1].strip()
    truong = re.sub(r"\([^()]*\)|có đáp án|\s+", " ", sau).strip(" -")
    truong = re.sub(r"^(trường|Trường)\s+", "", truong).strip()
    return {"ky": ky, "lop": lop, "nam_hoc": f"{nam}-{nam + 1}", "nam_dau": nam,
            "truong": truong, "tinh": tinh}


def khoa(lop: str, ky: str, truong: str) -> str:
    t = khong_dau(truong)
    t = re.sub(r"^(truong\s+)?(pho thong dtbt\s+)?(tieu hoc|th&thcs|th & thcs|th)\s+", "", t)
    t = re.sub(r"\s*-\s*.*$", "", t)  # "Đồng Hòa - Kiến An" ⇒ "dong hoa"
    t = re.sub(r"\bi\b", "1", t)       # "Nguyễn Thái Học I" = "… 1"
    return f"{lop}|{ky}|{re.sub(r'[^a-z0-9]', '', t)}"


def quet_jsp() -> dict[str, dict]:
    links: set[str] = set()
    for u in MUC_LUC_JSP:
        t = text(f"{VJ}/{u}")
        for h in re.findall(r'href="([^"]*20\d\d-20\d\d\.jsp)"', t):
            h = re.sub(r"^\.\./", "", h)
            links.add(h if h.startswith("http") else f"{VJ}/{h}")
    out = {}
    for u in sorted(links):
        t = text(u)
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        ten = sach(h1[0]) if h1 else ""
        p = phan_tich_ten(ten)
        if not p or "Toán" not in ten or p["nam_dau"] < NAM_TOI_THIEU:
            continue
        slug = u.rsplit("/", 1)[1][:-4]
        base = u.rsplit("/", 1)[0]
        anh = []
        for s in re.findall(r'<img[^>]+src="([^"]+)"', t):
            # ảnh đề gốc nằm ở thư mục images1/ (tên ảnh có khi lệch slug: "…dong-thai-2025…")
            if "/images1/" in s and re.search(r"-\d+\.(png|jpe?g)$", s, re.I):
                s = re.sub(r"^\.\./", "", s)
                full = s if s.startswith("http") else (f"{VJ}/{s}" if "/" in s.split("images")[0]
                                                      else f"{base}/{s}")
                if full not in anh:
                    anh.append(full)
        out[khoa(p["lop"], p["ky"], p["truong"])] = {**p, "ten": ten, "slug": slug,
                                                     "url_trang": u, "url_anh": anh}
    return out


def quet_online() -> dict[str, dict]:
    bo: set[str] = set()
    for u in MUC_LUC_ONLINE:
        bo.update(re.findall(r"thi-online/([^\"/]*de-thi[^\"/]*20\d\d-20\d\d[^\"/]*)", text(u)))
    out = {}
    for b in sorted(bo):
        t = text(f"{KH}/thi-online/{b}")
        ids = sorted(set(re.findall(rf"thi-online/{re.escape(b)}/(\d+)", t)))
        for i in ids:
            u = f"{KH}/thi-online/{b}/{i}"
            h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", text(u), re.S)
            ten = sach(h1[0]) if h1 else ""
            p = phan_tich_ten(ten)
            if p and p["nam_dau"] >= NAM_TOI_THIEU and re.search(r"(?i)trường|phường|xã|phòng", ten):
                out[khoa(p["lop"], p["ky"], p["truong"])] = {**p, "ten": ten, "url_thi_online": u}
    return out


def quet_chi_tiet() -> dict[str, dict]:
    out = {}
    for u in MUC_LUC_CHI_TIET:
        for h, a in re.findall(r'href="(https://khoahoc\.vietjack\.com/chi-tiet-de-thi/[^"]+)"[^>]*>(.*?)</a>',
                               text(u), re.S):
            ten = sach(a)
            p = phan_tich_ten(ten)
            if not p or "Toán" not in ten or p["nam_dau"] < NAM_TOI_THIEU:
                continue
            pdf = re.findall(r"https://video\.vietjack\.com/upload/documents/[^\"'&]+\.pdf", text(h))
            out[khoa(p["lop"], p["ky"], p["truong"])] = {**p, "ten": ten, "url_chi_tiet": h,
                                                         "url_pdf": pdf[0] if pdf else ""}
    return out


# Đề đã soi ảnh thấy SAI NHÃN ở nguồn ⇒ loại (khoá lớp|kỳ|trường)
LOAI = {"3|ck2|thanhuyen": "VietJack gắn nhãn CK2 nhưng nội dung trùng gần hết đề CK1 Thanh Uyên (đã bóc) — loại",
        "4|gk1|anhai": "Trùng đề TH Đồng Thái (UBND phường An Hải) — giữ bản Đồng Thái có ảnh gốc",
        "4|ck1|khanhthuy": "VietJack xếp lớp 4 nhưng ảnh đề là KTĐK cuối HK1 LỚP 5 (số thập phân, hình thang)"}


def gop(*nguon: dict[str, dict]) -> list[dict]:
    tat: dict[str, dict] = {}
    for n in nguon:
        for k, v in n.items():
            cu = tat.setdefault(k, {})
            for kk, vv in v.items():
                if vv and not cu.get(kk):
                    cu[kk] = vv
    return [dict(v, khoa=k) for k, v in sorted(tat.items()) if k not in LOAI]


def ten_file(d: dict) -> str:
    t = khong_dau(f"de-{THU_MUC[d['ky']]}-toan-{d['lop']}-nam-{d['nam_hoc']}-{d['truong']}-{d['tinh']}")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t)).strip("-")


def tai(d: dict) -> None:
    from PIL import Image
    thu_muc = OUT / f"lop-{d['lop']}" / THU_MUC[d["ky"]]
    thu_muc.mkdir(parents=True, exist_ok=True)
    ten = ten_file(d)
    pdf = thu_muc / f"{ten}.pdf"
    d["file"] = str(pdf.relative_to(ROOT))
    if d.get("url_anh"):
        anh_dir = thu_muc / "anh" / ten
        anh_dir.mkdir(parents=True, exist_ok=True)
        trang = []
        for i, u in enumerate(d["url_anh"], 1):
            f = anh_dir / f"trang-{i}{Path(u).suffix.lower() or '.png'}"
            if not f.exists() or f.stat().st_size == 0:
                f.write_bytes(get(u))
            try:
                im = Image.open(f)
            except Exception:
                print(f"   ⚠ ảnh hỏng: {u}")
                continue
            # Ảnh đầu trang .jsp thường là HÌNH MINH HOẠ cắt nhỏ (lặp lại hình trong đề) — không
            # phải trang đề; chỉ ghép ảnh rộng ≥ 600px (trang chụp đầy đủ / phần cuối trang).
            if im.width >= 600:
                trang.append(im.convert("RGB"))
        d["so_trang_anh"] = len(trang)
        if trang:
            trang[0].save(pdf, save_all=True, append_images=trang[1:], resolution=150)
        d["nguon_file"] = "anh-chup-de-goc (jsp)"
    elif d.get("url_pdf"):
        if not pdf.exists():
            pdf.write_bytes(get(d["url_pdf"], 120))
        d["nguon_file"] = "pdf-goc (chi-tiet-de-thi)"
    else:
        d["file"] = ""
        d["nguon_file"] = "chi-co-ban-go (thi-online) — CẦN ẢNH GỐC"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chi-in", action="store_true")
    a = ap.parse_args()
    ds = gop(quet_jsp(), quet_chi_tiet(), quet_online())
    for d in ds:
        if not a.chi_in:
            tai(d)
        print(f"lớp {d['lop']} {d['ky'].upper()} {d['nam_hoc']} | {d['truong']} ({d['tinh']}) | "
              f"ảnh {len(d.get('url_anh', []))} | {d.get('nguon_file', '')}")
    if not a.chi_in:
        # giữ các đề nguồn khác (Violet…) do script riêng ghi vào cùng manifest
        cu = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else []
        ds += [m for m in cu if m.get("nguon") and m.get("nguon") != "vietjack"]  # violet, drive-thay…
        MANIFEST.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n✓ {len(ds)} đề → {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
