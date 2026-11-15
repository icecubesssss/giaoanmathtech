#!/usr/bin/env python3
"""Cổng PHỦ DẠNG cho bộ đề ôn tập (luật Thầy 12/11/2026).

"Đề ôn tập CK phải phủ HẾT các dạng dễ có thể thi — HS C làm được, sót là đáng tiếc."

Luật (mặc định, Thầy giao "làm đi" theo đề xuất 12/11):
  - Dạng DỄ  = trong ngân hàng đề thật, ≥ 50% số ý của dạng ở mức NB/TH.
  - Dạng CÓ THỂ THI = xuất hiện ở ≥ 10% số đề thật và ≥ 2 đề (trong phạm vi kì thi).
  - Mỗi đề ôn phải có mọi dạng dễ xuất hiện ở ≥ 30% số đề      (--nguong-moi-de).
  - Cả bộ đề ôn phải có mọi dạng dễ xuất hiện ở ≥ 10% số đề    (--nguong-ca-bo).
  - Đề chính thức chỉ in bảng để tham khảo, không chặn.

Nguồn:
  - Ngân hàng: bản ghi đọc từng ý (mỗi đề một JSON, mảng "cau" có "dang", "muc").
    Ý gắn "ngoai_pham_vi" hoặc dạng có "ngoai_tap_1" trong khung (trừ khi --lay-ngoai-tap-1) bị bỏ.
    Tiểu học (lớp 3, 4): ý có "cd" thuộc chủ đề "Kì II" của khung SGK bị bỏ (đề trường ra vượt tiến độ).
  - Bộ đề: mỗi đề một danh sách tham chiếu "<mã-đề>#<nhãn-ý>". Lấy từ
      * script dựng đề có bảng DE[...] = ... (lớp 3, 4, 6) — mọi chuỗi "x#y" trong khối của đề;
      * file bo-cau JSON (lớp 7: storage/gemini/bo-cau/l7-ck1.json, có "ref").
    Mã đề viết tắt (vd "cum14") được khớp theo đuôi mã trong ngân hàng.

Ví dụ:
  python3 scripts/phu_dang_gate.py --khoi 6
  python3 scripts/phu_dang_gate.py --khoi 7 --md storage/phu-dang/lop-7-ck1.md
Thoát mã 1 nếu có đề ôn thiếu dạng.
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Cấu hình từng khối: ngân hàng, khung (có thể None), nguồn bộ đề.
KHOI = {
    3: dict(bank="inputs/refs/ngan-hang-sheet/tieu-hoc/lop-3/ban-ghi/l3-ck1-*.json", khung=None,
            tra="inputs/refs/ngan-hang-sheet/tieu-hoc/lop-3/ban-ghi/l3-*.json",
            script="scripts/de_ck1_lop3.py", khung_cd="config/khung-phan-dang/tieu-hoc-lop-3-kntt.json"),
    4: dict(bank="inputs/refs/ngan-hang-sheet/tieu-hoc/lop-4/ban-ghi/l4-ck1-*.json", khung=None,
            tra="inputs/refs/ngan-hang-sheet/tieu-hoc/lop-4/ban-ghi/l4-*.json",
            script="scripts/de_ck1_lop4.py", khung_cd="config/khung-phan-dang/tieu-hoc-lop-4-kntt.json"),
    5: dict(bank="inputs/refs/ngan-hang-sheet/tieu-hoc/lop-5/ban-ghi/l5-ck1-*.json",
            khung="config/khung-phan-dang/tieu-hoc-lop-5-kntt.json",
            tra="inputs/refs/ngan-hang-sheet/tieu-hoc/lop-5/ban-ghi/l5-*.json",
            script="scripts/ck1_lop5_ke_hoach.py", khung_cd="config/khung-phan-dang/tieu-hoc-lop-5-kntt.json"),
    6: dict(bank="inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi/*.json",
            khung="config/khung-phan-dang/lop-6-ck1-kntt.json", script="scripts/de_ck1_lop6.py"),
    7: dict(bank="inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi/*.json",
            khung="config/khung-phan-dang/lop-7-ck1-kntt.json", bo_cau="storage/gemini/bo-cau/l7-ck1.json",
            thay_tu="scripts/de_ck1_lop7.py"),
    8: dict(bank="inputs/refs/ngan-hang-sheet/lop-8/ck1/ban-ghi/*.json",
            khung="config/khung-phan-dang/lop-8-ck1-kntt.json", bo_de="inputs/refs/ngan-hang-sheet/lop-8/ck1/bo-de.json"),
    9: dict(bank="inputs/refs/ngan-hang-sheet/lop-9/ck1/ban-ghi/*.json",
            khung="config/khung-phan-dang/lop-9-ck1-kntt.json", bo_de="inputs/refs/ngan-hang-sheet/lop-9/ck1/bo-de.json"),
}
DE_MAU = re.compile(r'DE\[\s*["\']?(\w+)["\']?\s*\]\s*=')
REF_MAU = re.compile(r'["\']([a-z0-9][a-z0-9-]*#[A-Za-z0-9.]+)["\']')


def doc_ngan_hang(cfg, lay_ngoai):
    khung = json.loads((REPO / cfg["khung"]).read_text()) if cfg.get("khung") else None
    ten = {d["ma"]: d["ten"] for d in khung["dang"]} if khung else {}
    ngoai = {d["ma"] for d in khung["dang"] if d.get("ngoai_tap_1")} if khung and not lay_ngoai else set()
    # Tiểu học: khung theo CHỦ ĐỀ SGK; ý thuộc chủ đề kì II (đề trường ra vượt tiến độ) không tính vào CK1.
    if cfg.get("khung_cd"):
        kcd = json.loads((REPO / cfg["khung_cd"]).read_text())
        ngoai |= {("cd", c["so"]) for c in kcd["chu_de"] if c.get("hoc_ki_sgk") == "Kì II"}
    def doc(mau):
        out = {}
        for f in sorted(glob.glob(str(REPO / mau))):
            d = json.loads(Path(f).read_text())
            out[d.get("de", Path(f).stem)] = d
        return out
    recs = doc(cfg["bank"])
    tra = doc(cfg["tra"]) if cfg.get("tra") else recs  # tra cứu tham chiếu (có thể rộng hơn, vd câu lấy từ đề CK2)
    return recs, tra, ten, ngoai


def ten_dang(c):
    return c.get("dang") or "?"


def thong_ke(recs, ngoai):
    so_de = collections.Counter()
    muc = collections.defaultdict(collections.Counter)
    for d in recs.values():
        co = set()
        for c in d["cau"]:
            dg = ten_dang(c)
            if c.get("ngoai_pham_vi") or dg in ngoai or dg == "D99" or ("cd", c.get("cd")) in ngoai:
                continue
            co.add(dg)
            muc[dg][c.get("muc", "?")] += 1
        so_de.update(co)
    return so_de, muc


def de_cua_script(path):
    src = (REPO / path).read_text()
    pos = [(m.group(1), m.start()) for m in DE_MAU.finditer(src)]
    out = {}
    for i, (k, s) in enumerate(pos):
        e = pos[i + 1][1] if i + 1 < len(pos) else len(src)
        khoi = src[s:e]
        # khối của đề cuối có thể dính cả phần hàm phía sau: cắt ở "def " đầu tiên ở đầu dòng
        m = re.search(r"\n(def |class )", khoi)
        if m:
            khoi = khoi[: m.start()]
        out[str(k)] = REF_MAU.findall(khoi)
    return out


def de_cua_bo_cau(cfg):
    thay = {}
    if cfg.get("thay_tu"):
        src = (REPO / cfg["thay_tu"]).read_text()
        m = re.search(r"THAY\s*=\s*\{(.*?)\}", src, re.S)
        if m:
            thay = dict(re.findall(r'"([^"]+#[^"]+)"\s*:\s*"([^"]+#[^"]+)"', m.group(1)))
    out = {}
    for de in json.loads((REPO / cfg["bo_cau"]).read_text()):
        refs = []

        def di(x):
            if isinstance(x, dict):
                if "ref" in x:
                    refs.append(thay.get(x["ref"], x["ref"]))
                for v in x.values():
                    di(v)
            elif isinstance(x, list):
                for v in x:
                    di(v)
        di(de)
        out[("on" if de.get("loai") == "on" else "ct") + str(de["so"])] = refs
    return out


def tra_ref(ref, recs):
    """'cum14#II.1a' -> (mã đề, câu). Khớp mã tắt theo đuôi; nhãn ý khớp đúng hoặc theo tiền tố."""
    ma, nhan = ref.split("#", 1)
    if ma in recs:
        ung = [ma]
    elif any(k.endswith("-" + ma) for k in recs):  # mã đầy đủ thiếu tiền tố khối, vd "ck1-2526-donghoa"
        # Trường có đề nhiều năm (vd phucdong 2526 + 2425): tên trơn = năm mới nhất (cùng quy ước script đề).
        ung = sorted((k for k in recs if k.endswith("-" + ma)), reverse=True)
    else:
        # Quy ước script đề: tên trường trơn = đề năm mới nhất; hậu tố "24" = đề 2024-2025 trùng tên.
        nam = None
        if re.fullmatch(r"[a-z]+24", ma) and not any(k.split("-")[-1] == ma for k in recs):
            ma, nam = ma[:-2], "2425"
        ung = [k for k in recs if k.split("-")[-1] == ma and (nam is None or f"-{nam}-" in k)]
        ung.sort(reverse=True)  # 2526 trước 2425
    for k in ung:
        cau = recs[k]["cau"]
        cung = [c for c in cau if c["cau"] == nhan]
        if not cung:  # tham chiếu cả bài: 'II.3' ⇒ mọi ý II.3*
            cung = [c for c in cau if c["cau"].startswith(nhan)]
        if cung:
            return k, cung
    return None, []


def la_on(k):
    return str(k).startswith("on")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--khoi", type=int, required=True, choices=sorted(KHOI))
    ap.add_argument("--nguong-moi-de", type=float, default=30)
    ap.add_argument("--nguong-ca-bo", type=float, default=10)
    ap.add_argument("--toi-thieu-de", type=int, default=2, help="dạng phải có ở ít nhất N đề thật mới tính")
    ap.add_argument("--nguong-de", type=float, default=50, help="%% ý NB/TH để coi là dạng dễ")
    ap.add_argument("--lay-ngoai-tap-1", action="store_true")
    ap.add_argument("--md", help="ghi bảng ra file Markdown")
    a = ap.parse_args()
    cfg = KHOI[a.khoi]

    recs, tra, ten, ngoai = doc_ngan_hang(cfg, a.lay_ngoai_tap_1)
    if not recs:
        print(f"Lớp {a.khoi}: chưa có ngân hàng {cfg['bank']}", file=sys.stderr)
        return 2
    if cfg.get("script"):
        bo = de_cua_script(cfg["script"])
    elif cfg.get("bo_cau"):
        bo = de_cua_bo_cau(cfg)
    else:
        p = REPO / cfg["bo_de"]
        if not p.exists():
            print(f"Lớp {a.khoi}: chưa có bộ đề {cfg['bo_de']}", file=sys.stderr)
            return 2
        bo = json.loads(p.read_text())
    n = len(recs)
    so_de, muc = thong_ke(recs, ngoai)

    phu, khong_tra = {}, collections.defaultdict(list)
    for k, refs in bo.items():
        s = set()
        for r in refs:
            if r.startswith("="):  # mã dạng gắn trực tiếp (bộ đề cũ không trỏ về ngân hàng), vd "=D11"
                s.add(r[1:])
                continue
            _, cs = tra_ref(r, tra)
            if not cs:
                khong_tra[k].append(r)
            s.update(ten_dang(c) for c in cs)
        phu[k] = s

    def de(dg):
        m = muc[dg]
        tong = sum(m.values()) or 1
        return 100 * (m["NB"] + m["TH"]) / tong >= a.nguong_de

    cot = sorted(bo, key=lambda k: (not la_on(k), str(k)))
    on = [k for k in cot if la_on(k)]
    dong, loi = [], []
    for dg, v in sorted(so_de.items(), key=lambda x: -x[1]):
        pct = 100 * v / n
        if pct < a.nguong_ca_bo or v < a.toi_thieu_de:
            continue
        mm = " ".join(f"{x}{y}" for x, y in muc[dg].most_common())
        o = ["✓" if dg in phu[k] else "·" for k in cot]
        nhan = "dễ" if de(dg) else "khó"
        dong.append(f"| {dg if ten else ''} | {ten.get(dg, dg)[:60]} | {pct:.0f}% | {mm} | {nhan} | " + " | ".join(o) + " |")
        if not de(dg) or not on:
            continue
        if not any(dg in phu[k] for k in on):
            loi.append(f"CẢ BỘ ôn thiếu {dg} ({pct:.0f}% đề) {ten.get(dg, '')[:50]}")
        elif pct >= a.nguong_moi_de:
            for k in on:
                if dg not in phu[k]:
                    loi.append(f"{k} thiếu {dg} ({pct:.0f}% đề) {ten.get(dg, '')[:50]}")

    tieu_de = (f"# Phủ dạng — lớp {a.khoi} CK1 ({n} đề thật)\n\n"
               f"Dạng dễ: ≥{a.nguong_de:.0f}% ý NB/TH. Mỗi đề ôn phải có dạng dễ ≥{a.nguong_moi_de:.0f}% đề; "
               f"cả bộ ôn phải có dạng dễ ≥{a.nguong_ca_bo:.0f}% đề. Cột ct = đề chính thức (tham khảo).\n\n")
    bang = ("| Mã | Dạng | % đề | Mức (số ý) | Loại | " + " | ".join(map(str, cot)) + " |\n"
            "|---|---|---|---|---|" + "---|" * len(cot) + "\n" + "\n".join(dong) + "\n")
    ket = "\n## Kết luận\n\n" + ("\n".join(f"- ❌ {x}" for x in loi) if loi else "- ✅ Đạt: mọi đề ôn phủ đủ dạng dễ.") + "\n"
    if khong_tra:
        ket += "\n## Tham chiếu không tra được trong ngân hàng\n\n" + "\n".join(
            f"- {k}: {', '.join(v)}" for k, v in khong_tra.items()) + "\n"
    out = tieu_de + bang + ket
    print(out)
    if a.md:
        p = REPO / a.md
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(out)
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
