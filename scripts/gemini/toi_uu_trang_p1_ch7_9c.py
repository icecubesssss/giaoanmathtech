#!/usr/bin/env python3
"""Quét lấp trang trắng Phiếu 1 ch.VII 9C (18/11/2026) — Thầy: "soi thấy trắng thì phóng hình cho choán chỗ".

Mỗi lượt: build phiếu HS → đo khoảng trắng đáy từng trang → lấy trang trắng nhất, phóng hình (biểu đồ: xếp dọc,
tăng bề rộng) hoặc bảng (tăng hệ số) của MỘT bài trên trang đó → build lại. Điểm = tổng trắng (trừ trang cuối)
+ 30 × số trang; giảm thì giữ, không thì trả lại và bỏ ứng viên đó. Kết quả ghi scripts/gemini/phong_p1_ch7_9c.json
(so_do_p1_ch7_9c.py tự đọc).

    .venv/bin/python scripts/gemini/toi_uu_trang_p1_ch7_9c.py [--luot 14]
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-07-tan-so-va-tan-so-tuong-doi/phieu-1-bang-tan-so-tan-so-tuong-doi-ghep-nhom.json"
PDF = REPO / ("outputs/lop-9/dai-so/lop-c/chuong-07-tan-so-va-tan-so-tuong-doi/phieu-1-bang-tan-so-tan-so-tuong-doi-ghep-nhom/"
              "Toan9C-Bang-tan-so-tan-so-tuong-doi-ghep-nhom-Phieu-HS.pdf")
FILE = REPO / "scripts/gemini/phong_p1_ch7_9c.json"
PY = str(REPO / ".venv/bin/python")
NGUONG = 2.0   # cm trắng đáy coi là cần lấp
MAC_DINH: dict = {}


def mac_dinh():
    """PHONG đang có trong so_do (bản không kèm file quét) — để bước phóng đi LÊN từ mức hiện tại."""
    code = ("import sys,json,re;sys.path.insert(0,'scripts/gemini');"
            "src=open('scripts/gemini/so_do_p1_ch7_9c.py').read();"
            "print(json.dumps(eval(re.search(r'^PHONG = (\\{.*\\})$',src,re.M)[1])))")
    return json.loads(subprocess.run([PY, "-c", code], cwd=REPO, capture_output=True, text=True, check=True).stdout)


def loai_bai():
    """nhãn bài → 'hinh' | 'bang' (không tính ví dụ: hộp cứng, phóng dễ đẩy cả hộp sang trang)."""
    code = ("import sys,json;sys.path.insert(0,'scripts/gemini');import so_do_p1_ch7_9c as S;"
            "print(json.dumps({k[0]:('hinh' if any(S._LOAI[int(i)]=='hinh' for i in __import__('re').findall(r'⟦H(\\d+)⟧',k[8]))"
            " else 'bang' if '⟦H' in k[8] else '') for k in S.KHOI if len(k)>3 and k[7]!='vi_du'}))")
    return json.loads(subprocess.run([PY, "-c", code], cwd=REPO, capture_output=True, text=True, check=True).stdout)


def build():
    env = dict(os.environ, TECTONIC_BIN=str(REPO / "scripts/tectonic_xelatex.sh"))
    subprocess.run([PY, "scripts/gemini/lap_p1_ch7_9c.py", "--ghi"], cwd=REPO, capture_output=True, check=True)
    r = subprocess.run([PY, "-m", "src.main", "build", SEED, "--only", "handout"], cwd=REPO, env=env,
                       capture_output=True, text=True)
    if r.returncode or not PDF.exists():
        raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])


def do():
    d = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", "40", "-gray", str(PDF), f"{d}/p"], check=True)
    trang = []
    for i, f in enumerate(sorted(glob.glob(f"{d}/p-*.pgm")), 1):
        im = Image.open(f)
        w, h = im.size
        px = im.load()
        cm = h / 29.7
        top, bot = int(4.0 * cm), int(h - 3.9 * cm)
        last = top
        for yy in range(top, bot):
            if sum(1 for x in range(int(w * 0.08), int(w * 0.92), 2) if px[x, yy] < 200) > 3:
                last = yy
        txt = subprocess.run(["pdftotext", "-layout", "-f", str(i), "-l", str(i), str(PDF), "-"],
                             capture_output=True, text=True).stdout
        nhan = re.findall(r"(?m)^\s*(Bài \d+\.)", txt)
        trang.append(((bot - last) / cm, nhan))
    return trang


def diem(trang):
    return sum(t for t, _ in trang[:-1]) + 30 * len(trang)


def main():
    luot = int(sys.argv[sys.argv.index("--luot") + 1]) if "--luot" in sys.argv else 14
    loai = loai_bai()
    global MAC_DINH
    MAC_DINH = mac_dinh()
    st = json.loads(FILE.read_text()) if FILE.exists() else {"hinh": {}, "bang": {}}
    FILE.write_text(json.dumps(st, ensure_ascii=False, indent=1))
    build()
    trang = do()
    best = diem(trang)
    print(f"gốc: {len(trang)} trang, điểm {best:.1f}", flush=True)
    het = set()
    for k in range(luot):
        ung = []
        for t, nhan in sorted(trang, key=lambda x: -x[0]):
            if t < NGUONG:
                break
            ung += [(n, loai.get(n)) for n in nhan if loai.get(n) and (n, loai.get(n)) not in het]
        if not ung:
            print("hết ứng viên")
            break
        n, kieu = ung[0]
        cu = json.loads(json.dumps(st))
        if kieu == "hinh":
            v = round(st["hinh"].get(n, MAC_DINH.get(n, 0.43)) + 0.12, 2)   # bắt đầu từ mức đang dùng
            if v > 1.0:
                het.add((n, kieu))
                continue
            st["hinh"][n] = v
        else:
            v = round(st["bang"].get(n, 1.0) + 0.15, 2)
            if v > 1.6:
                het.add((n, kieu))
                continue
            st["bang"][n] = v
        FILE.write_text(json.dumps(st, ensure_ascii=False, indent=1))
        build()
        tm = do()
        d = diem(tm)
        ok = d < best - 0.3
        print(f"lượt {k + 1}: {n} {kieu}={v} → {len(tm)} trang, điểm {d:.1f} ({'GIỮ' if ok else 'trả lại'})", flush=True)
        if ok:
            best, trang = d, tm
        else:
            st = cu
            het.add((n, kieu))
            FILE.write_text(json.dumps(st, ensure_ascii=False, indent=1))
    build()
    for i, (t, nhan) in enumerate(do(), 1):
        print(f"tr{i:2d} trắng {t:4.1f}cm {' '.join(nhan)}")
    print("chốt:", json.dumps(st, ensure_ascii=False))


if __name__ == "__main__":
    main()
