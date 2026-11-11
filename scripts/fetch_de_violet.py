#!/usr/bin/env python3
"""Thêm đề TIỂU HỌC lấy từ thư viện Violet (dethi.violet.vn) vào kho + manifest tieu-hoc-nguon-tai.json.

Violet không cho tải file khi chưa đăng nhập, nhưng mỗi tài liệu có ẢNH XEM TRƯỚC từng trang công khai
(`lecture_player.init(..., "<base>/images", N)` ⇒ `<base>/images/SlideK.JPG`). Đó là ảnh đề gốc ⇒ đọc được.
TLS: chuỗi chứng chỉ Violet cần root "GlobalSign Root R46" (thiếu trong bộ CA của curl macOS) ⇒ truyền
`--cacert` gồm bộ CA hệ thống + root đó (KHÔNG dùng -k). Máy chủ hay cắt cụt trang ⇒ thử lại tới khi có </html>.

Danh sách đề đã XÁC MINH bằng mắt (tên trường + năm học 2025-2026 in trên đề) ở DS bên dưới.
    .venv/bin/python scripts/fetch_de_violet.py --ca /path/ca-plus.pem
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "inputs/refs/de-thi/tieu-hoc-nguon-tai.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
# (entry_id, url, lớp, kỳ, trường, tỉnh, mã đề trong bản ghi)
DS = [
    (14868107, "https://dethi.violet.vn/present/de-kt-cuoi-hk1-co-ma-tran-va-dap-an-chi-tiet-14868107.html", "4", "ck1", "Tiểu học Minh Khôi", "", "l4-ck1-2526-minhkhoi"),
    (14825239, "https://dethi.violet.vn/present/cuoi-hki-14825239.html", "4", "ck1", "Tiểu học Từ Thiện", "xã Phước Dinh", "l4-ck1-2526-tuthien"),
    (15103229, "https://dethi.violet.vn/present/cuoi-ki-1-15103229.html", "4", "ck1", "Tiểu học Liên Bảo", "", "l4-ck1-2526-lienbao"),
    (14861719, "https://dethi.violet.vn/present/de-ktchk1-lop-4-kntt-14861719.html", "4", "ck1", "TH Trần Quốc Toản", "xã Eadrông", "l4-ck1-2526-tranquoctoan"),
    (14829821, "https://dethi.violet.vn/present/de-ktdk-cuoi-hk1-bo-sach-canh-dieu-14829821.html", "4", "ck1", "Tiểu học Đồng Cấm", "Hải Phòng", "l4-ck1-2526-dongcam"),
    (14820528, "https://giaoan.violet.vn/present/de-thi-toan-4-cuoi-ki-i-14820528.html", "4", "ck1", "Tiểu học Tiên Phú", "", "l4-ck1-2526-tienphu"),
    (15052669, "https://dethi.violet.vn/present/de-kiem-tra-toan-hki-15052669.html", "4", "ck1", "Tiểu học Minh Tâm", "xã Minh Tâm", "l4-ck1-2526-minhtam"),
    (14806800, "https://dethi.violet.vn/present/de-thi-hoc-ki-1-14806800.html", "4", "ck1", "TH Tân Thuận 1", "xã Tân Thành", "l4-ck1-2526-tanthuan1"),
    (14898343, "https://dethi.violet.vn/present/kiem-tra-cuoi-ky-i-mon-toan-14898343.html", "3", "ck1", "TH&THCS Khánh Thiện", "xã Lâm Thượng", "l3-ck1-2526-khanhthien"),
    # năm học 2024-2025 (Thầy nới 10/11/2026)
    (14357238, "https://dethi.violet.vn/present/de-kiem-tra-hk-1-toan-lop-3-14357238.html", "3", "ck1", "TH&THCS Nguyễn Bỉnh Khiêm", "", "l3-ck1-2425-nguyenbinhkhiem"),
    (14327531, "https://dethi.violet.vn/present/kiem-tra-cuoi-ki-i-kntt-14327531.html", "3", "ck1", "TH Thạnh Hưng 2", "", "l3-ck1-2425-thanhhung2"),
    (14321322, "https://dethi.violet.vn/present/de-thi-hoc-ki-1-14321322.html", "4", "ck1", "TH&THCS Chu Văn An", "Ea Súp", "l4-ck1-2425-chuvanan-easup"),
    (14320626, "https://dethi.violet.vn/present/de-thi-cuoi-hoc-ky-1-14320626.html", "4", "ck1", "Tiểu học Đông Quang", "xã Đông Quang", "l4-ck1-2425-dongquang"),
    (14320603, "https://dethi.violet.vn/present/de-kiem-tra-cuoi-ki-i-14320603.html", "4", "ck1", "Tiểu học Thị trấn Lộc Hà (đề A)", "Hà Tĩnh", "l4-ck1-2425-lochatt"),
    (14320591, "https://dethi.violet.vn/present/de-thi-cuoi-ki-i-14320591.html", "4", "ck1", "Tiểu học Thị trấn Lộc Hà (đề B)", "Hà Tĩnh", "l4-ck1-2425-lochatt"),
    (14299392, "https://dethi.violet.vn/present/de-thi-hoc-ki-1-14299392.html", "4", "ck1", "Tiểu học Tân Liễu (đề A)", "Yên Dũng", "l4-ck1-2425-tanlieu"),
    (14289130, "https://dethi.violet.vn/present/cuoi-hki-14289130.html", "4", "ck1", "Tiểu học Tân Liễu (đề B)", "Yên Dũng", "l4-ck1-2425-tanlieu"),
]
THU_MUC = {"ck1": "cuoi-ki-1"}


def get(url: str, ca: str, binary: bool = False, tries: int = 40) -> bytes:
    for _ in range(tries):
        r = subprocess.run(["curl", "-s", "-L", "-m", "90", "--cacert", ca, "-A", UA, url], capture_output=True)
        if binary and r.returncode == 0 and len(r.stdout) > 2000:
            return r.stdout
        if not binary and b"</html>" in r.stdout:
            return r.stdout
    return b""


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--ca", required=True); a = ap.parse_args()
    from PIL import Image
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    man = [m for m in man if m.get("nguon") != "violet"]
    for eid, url, lop, ky, truong, tinh, ma in DS:
        t = get(url, a.ca).decode("utf-8", "ignore")
        m = re.search(r'lecture_player\.init\([^,]+,\s*"([^"]+)",\s*(\d+)\)', t)
        if not m:
            print(f"✗ {eid}: không thấy ảnh xem trước"); continue
        base, n = m.group(1), int(m.group(2))
        anh = [f"{base}/Slide{i}.JPG" for i in range(1, n + 1)]
        d = ROOT / f"inputs/refs/de-thi/lop-{lop}/{THU_MUC[ky]}/anh/{ma}-{eid}"
        d.mkdir(parents=True, exist_ok=True)
        trang = []
        for i, u in enumerate(anh, 1):
            f = d / f"trang-{i}.jpg"
            if not f.exists() or f.stat().st_size < 2000:
                f.write_bytes(get(u, a.ca, binary=True))
            if f.stat().st_size > 2000:
                trang.append(Image.open(f).convert("RGB"))
        pdf = d.parent.parent / f"{ma}-{eid}-violet.pdf"
        if trang:
            trang[0].save(pdf, save_all=True, append_images=trang[1:], resolution=72)
        nam = 2000 + int(ma.split("-")[2][:2])
        man.append({"nguon": "violet", "ky": ky, "lop": lop, "nam_hoc": f"{nam}-{nam + 1}", "nam_dau": nam,
                    "truong": truong, "tinh": tinh, "ten": f"{truong} – cuối HK1 Toán {lop} {nam}-{nam + 1} (Violet)",
                    "url_trang": url, "url_anh": anh, "ma": ma, "so_trang_anh": len(trang),
                    "file": str(pdf.relative_to(ROOT)), "nguon_file": "anh-xem-truoc (violet)"})
        print(f"✓ {ma}: {len(trang)}/{n} trang")
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
