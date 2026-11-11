#!/usr/bin/env python3
"""BỐC CÂU cho bộ đề CUỐI HỌC KÌ I TOÁN 7 (KNTT, Hà Nội): 3 đề ôn + 3 đề chính thức.

Ngân hàng: 30 đề CK1 lớp 7 HN 2024-2026, Gemini bóc + Claude soát
(inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi/). Câu có `ngoai_pham_vi` KHÔNG được bốc
(phạm vi chốt ở config/khung-phan-dang/lop-7-ck1-kntt.json → pham_vi_ck1).

KHUNG (chốt 11/11/2026 từ thống kê 30 đề — xem storage/gemini/soat/7-ck1-thong-ke.md):
  Phần I  Trắc nghiệm 8 câu × 0,25 = 2,0đ
  Bài 1   Thực hiện phép tính 3 ý = 1,5đ   (29/30 đề có; D02, D04, D08/D09)
  Bài 2   Tìm x 3 ý = 1,5đ                  (30/30; D05, D09, D06/D22)
  Bài 3   Bài toán chia theo tỉ lệ 1,5đ     (20/30; D22 dãy tỉ số)
  Bài 4   Hình: song song – tính góc 1,5đ   (25/30; D11–D13, nguyên bài một đề)
  Bài 5   Hình: tam giác bằng nhau 1,5đ     (13/30; tiến độ Thầy tuần 21 nhắm bài này; D14–D18)
  Bài 6   Vận dụng cao 0,5đ                 (27/30; D25–D27, nội dung trong phạm vi)
Đề ôn 1–2: dạng tần suất cao; đề ôn 3: dạng tần suất nhì; đề chính thức 1–3: câu chưa dùng.

    python3 scripts/bo_cau_ck1_lop7.py   → storage/gemini/bo-cau/l7-ck1.json + .md
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BG = ROOT / "inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi"
RA = ROOT / "storage/gemini/bo-cau"

DE = {f.stem: json.loads(f.read_text()) for f in sorted(BG.glob("l7-ck1-*.json"))}

# Slot trắc nghiệm: (dạng ưu tiên cho đề ôn 1-2, dạng cho đề ôn 3 / dự phòng)
TN_SLOT = [("D08", "D01"), ("D09", "D07"), ("D07", "D01"), ("D22", "D22"),
           ("D11", "D12"), ("D12", "D11"), ("D15", "D14"), ("D20", "D21", "D19")]
B1 = [("D02", "D02"), ("D04", "D04"), ("D08", "D09", "D04", "D02")]
B2 = [("D05", "D05"), ("D09", "D06"), ("D22", "D05")]


def key(de, q):
    return f"{de}#{q['cau']}"


def ok(q):
    return not q.get("ngoai_pham_vi") and "chọn 1 trong 2" not in str(q.get("can_soat", ""))


def sach(q):  # câu không có ghi chú nghi vấn đáp án
    return not re.search(r"lệch|nhầm|sai|theo đề in", str(q.get("can_soat", "")))


DUNG: set[str] = set()
ND_DUNG: list[str] = []


def chuan(nd):
    nd = re.sub(r"^.*?(biết|tính|phép tính)[^:]*:\s*", "", nd, flags=re.I)
    return re.sub(r"20\d\d|\s|\$|\\", "", nd.lower())[:160]


def na_na(q):
    from difflib import SequenceMatcher
    c = chuan(q.get("nd", ""))
    return any(SequenceMatcher(None, c, x).ratio() >= 0.8 for x in ND_DUNG)
DE_DUNG: Counter = Counter()


def la_tim_x(q):
    nd = q.get("nd", "")
    return bool(re.search(r"tìm\s*\$?x|=", nd, re.I)) and "x" in nd and not re.search(r"lớp|học sinh|cây|quyển|sách", nd)


def chon_y(dang_list, ht_ok, n_bo=0, tranh=(), loc=lambda q: True):
    """Chọn MỘT ý lẻ (TN hoặc ý tính/tìm x) theo dạng; ưu tiên câu sạch, đề nguồn ít dùng."""
    for dang in dang_list:
        ung = []
        for de, d in DE.items():
            if de in tranh:
                continue
            for q in d["cau"]:
                if q["dang"] == dang and q["ht"] in ht_ok and ok(q) and loc(q) and key(de, q) not in DUNG and not na_na(q):
                    ung.append((not sach(q), DE_DUNG[de], q.get("diem_uoc", False), de, q))
        if ung:
            ung.sort(key=lambda x: x[:4])
            _, _, _, de, q = ung[min(n_bo, len(ung) - 1)]
            DUNG.add(key(de, q)); DE_DUNG[de] += 1; ND_DUNG.append(chuan(q["nd"]))
            return {"ref": key(de, q), "dang": q["dang"], "ht": q["ht"], "muc": q["muc"],
                    "diem_goc": q["diem"], "nd": q["nd"], "dap_an": q["dap_an"],
                    **({"can_soat": q["can_soat"]} if q.get("can_soat") else {})}
    return None


def nhom_bai(d):
    """Gom ý tự luận theo bài: 'II.4a','II.4b' → 'II.4'; 'II.4.2a' → 'II.4.2'."""
    g = defaultdict(list)
    for q in d["cau"]:
        if q["ht"] != "TL":
            continue
        m = re.match(r"^((?:[IVX]+\.)?\d+(?:\.\d+)?)", q["cau"])
        g[m.group(1) if m else q["cau"]].append(q)
    return g


def chon_bai(nhom_dang, diem_min, diem_max, tranh_de=(), can_co=None):
    ung = []
    for de, d in DE.items():
        if de in tranh_de:
            continue
        for b, ys in nhom_bai(d).items():
            if not all(ok(q) and q["dang"] in nhom_dang for q in ys):
                continue
            if any(key(de, q) in DUNG or na_na(q) for q in ys):
                continue
            if can_co and not any(q["dang"] in can_co for q in ys):
                continue
            t = sum(q["diem"] for q in ys)
            if diem_min <= t <= diem_max:
                ung.append((not all(sach(q) for q in ys), DE_DUNG[de], abs(t - 1.5), de, b, ys))
    if not ung:
        return None
    ung.sort(key=lambda x: x[:5])
    _, _, _, de, b, ys = ung[0]
    for q in ys:
        DUNG.add(key(de, q)); ND_DUNG.append(chuan(q["nd"]))
    DE_DUNG[de] += 1
    return {"nguon": f"{de}#{b}", "y": [{"ref": key(de, q), "dang": q["dang"], "muc": q["muc"],
                                       "diem_goc": q["diem"], "nd": q["nd"], "dap_an": q["dap_an"],
                                       **({"can_soat": q["can_soat"]} if q.get("can_soat") else {})}
                                      for q in ys]}


def dung_de(ten, cot):
    """cot = 0 (dạng tần suất cao) | 1 (dạng tần suất nhì)."""
    tn = [chon_y([s[cot], s[1 - cot], *s[2:]], {"TN"}) for s in TN_SLOT]
    b1 = [chon_y([s[cot], s[1 - cot], *s[2:]], {"TL"}, loc=lambda q: not (re.search(r"tìm\s*\$?x", q.get("nd", ""), re.I) or (re.search(r"(?<![A-Za-z])\d*x(?![A-Za-z])", q.get("nd", "")) and "=" in q.get("nd", "")))) for s in B1]
    b2 = [chon_y([s[cot], s[1 - cot]], {"TL"}, loc=la_tim_x) for s in B2]
    b3 = chon_bai({"D22"}, 1.0, 2.25)
    b4 = chon_bai({"D11", "D12", "D13"}, 1.5, 3.0, can_co={"D13"})
    b5 = chon_bai({"D14", "D15", "D16", "D17", "D18", "D13"}, 1.5, 3.5, can_co={"D16"})
    b6 = chon_y(["D27", "D26", "D25"], {"TL"})
    return {"ten": ten, "TN": tn, "Bai1": b1, "Bai2": b2, "Bai3": b3, "Bai4": b4, "Bai5": b5, "Bai6": b6}


def main():
    RA.mkdir(parents=True, exist_ok=True)
    bo = [dung_de("Đề ôn tập 1", 0), dung_de("Đề ôn tập 2", 0), dung_de("Đề ôn tập 3", 1),
          dung_de("Đề chính thức 1", 0), dung_de("Đề chính thức 2", 0), dung_de("Đề chính thức 3", 1)]
    (RA / "l7-ck1.json").write_text(json.dumps(bo, ensure_ascii=False, indent=1))
    md = ["# Bốc câu CK1 Toán 7 — 3 đề ôn + 3 đề chính thức", ""]
    thieu = 0
    for D in bo:
        md += [f"## {D['ten']}", ""]
        for i, c in enumerate(D["TN"], 1):
            md.append(f"- TN{i}: " + (f"{c['ref']} [{c['dang']} {c['muc']}] {c['nd'][:80]}" if c else "**THIẾU**"))
            thieu += c is None
        for bn in ("Bai1", "Bai2"):
            for i, c in enumerate(D[bn], 1):
                md.append(f"- {bn}.{i}: " + (f"{c['ref']} [{c['dang']}] {c['nd'][:80]}" if c else "**THIẾU**"))
                thieu += c is None
        for bn in ("Bai3", "Bai4", "Bai5"):
            b = D[bn]
            md.append(f"- {bn}: " + (f"{b['nguon']} ({len(b['y'])} ý, {sum(y['diem_goc'] for y in b['y'])}đ gốc) "
                                     f"{b['y'][0]['nd'][:80]}" if b else "**THIẾU**"))
            thieu += b is None
        c = D["Bai6"]
        md.append("- Bai6 VDC: " + (f"{c['ref']} [{c['dang']}] {c['nd'][:80]}" if c else "**THIẾU**"))
        thieu += c is None
        md.append("")
    nguon = Counter(r.split("#")[0] for r in DUNG)
    md += [f"Tổng ý đã bốc: {len(DUNG)} · ô thiếu: {thieu} · số đề nguồn dùng: {len(nguon)}/30 · "
           f"nhiều nhất: {nguon.most_common(3)}"]
    (RA / "l7-ck1.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
