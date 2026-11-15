#!/usr/bin/env python3
"""BỐC CÂU bộ đề CUỐI HỌC KÌ I TOÁN 7 (KNTT, Hà Nội) — BẢN 2 (12/11/2026, Thầy giao lại):

  - 3 ĐỀ ÔN TẬP: mỗi đề PHỦ ĐỦ mọi dạng có thể ra (D01–D22 trong phạm vi), riêng VDC chỉ ôn
    1–2 dạng tỉ lệ ra cao nhất (D27 63% đề, D26 20% đề; D25 6% bỏ).
  - 3 ĐỀ CHÍNH THỨC: mỗi câu chỉ lấy từ 1–3 dạng hay ra nhất ở đúng vị trí đó (thống kê 30 đề),
    VDC cũng chỉ D27/D26.
Bản 1 (khung chung cho cả 6 đề) lưu ở storage/gemini/bo-cau/l7-ck1-ban1.*.

Ngân hàng: 30 đề CK1 lớp 7 HN 2024-2026 (inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi/),
câu `ngoai_pham_vi` không bốc. Ưu tiên câu ĐÃ CHÉP (storage/gemini/xong/chep-*.json) để thợ
Gemini chỉ phải chép phần mới.

KHUNG ĐỀ ÔN (10đ, 90′): TN 12 câu × 0,25 = 3,0 (D01 D03 D07 D08 D11 D12 D14 D15 D18 D19 D20 D21)
  · B1 tính 2 ý 1,0 (D02, D04) · B2 tìm x 3 ý 1,5 (D05, D06, D09) · B3 bài thực tế 0,75 (D10; đề nào
  thiếu D21 ở TN thì B3 là bài biểu đồ D21 và TN lấy D10) · B4 chia theo tỉ lệ 1,0 (D22)
  · B5 song song 1,0 (D11–D13, phải có D13) · B6 tam giác 1,25 (D16 + D17, ưu tiên có D18) · B7 VDC 0,5.
KHUNG ĐỀ CHÍNH THỨC (10đ, 90′, chốt từ 30 đề): TN 8 × 0,25 · B1 tính 3 ý 1,5 · B2 tìm x 3 ý 1,5
  · B3 chia theo tỉ lệ 1,5 · B4 song song 1,5 · B5 tam giác bằng nhau 1,5 · B6 VDC 0,5.

    python3 scripts/bo_cau_ck1_lop7.py   → storage/gemini/bo-cau/l7-ck1.json + .md
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BG = ROOT / "inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi"
RA = ROOT / "storage/gemini/bo-cau"
CHEP = ROOT / "storage/gemini/xong"

DE = {f.stem: json.loads(f.read_text()) for f in sorted(BG.glob("l7-ck1-*.json"))}
DA_CHEP: set[str] = set()
for f in CHEP.glob("chep-l7-ck1-*.json"):
    for c in (json.loads(f.read_text()).get("ket_qua") or {}).get("cau", []):
        DA_CHEP.add(f"{f.stem[5:]}#{c['cau']}")

PHAM_VI = [f"D{i:02d}" for i in range(1, 23)]          # dạng phải phủ ở đề ôn
# câu sai/khó dùng phát hiện khi soát bản 1 — không bốc lại
CAM = {"l7-ck1-2526-lyson#II.1.1", "l7-ck1-2526-hatmon#I.5",
       "l7-ck1-2526-donganh#5a", "l7-ck1-2526-donganh#5b"}   # Đông Anh 25-26 Bài 5 chép nguyên Phan Đình Giót 24-25

# ---------------------------------------------------------------- khung
# TN: mỗi slot = danh sách dạng theo thứ tự ưu tiên
TN_ON = [["D01"], ["D03"], ["D07"], ["D08"], ["D11"], ["D12"], ["D14"], ["D15"], ["D18", "D09", "D22"],
         ["D19"], ["D20"], ["D21"]]
TN_CT = [["D08"], ["D08", "D01"], ["D07"], ["D09"], ["D11"], ["D12"], ["D22"], ["D15", "D14"]]


def key(de, q):
    return f"{de}#{q['cau']}"


def ok(q, de):
    return (not q.get("ngoai_pham_vi") and "chọn 1 trong 2" not in str(q.get("can_soat", ""))
            and key(de, q) not in CAM)


def sach(q):
    return not re.search(r"lệch|nhầm|sai|theo đề in", str(q.get("can_soat", "")))


DUNG: set[str] = set()
ND_DUNG: list[str] = []
DE_DUNG: Counter = Counter()


def chuan(nd):
    nd = re.sub(r"^.*?(biết|tính|phép tính)[^:]*:\s*", "", nd, flags=re.I)
    return re.sub(r"20\d\d|\s|\$|\\", "", nd.lower())[:160]


def na_na(q):
    c = chuan(q.get("nd", ""))
    return any(SequenceMatcher(None, c, x).ratio() >= 0.8 for x in ND_DUNG)


def la_tim_x(q):
    nd = q.get("nd", "")
    return bool(re.search(r"tìm\s*\$?x|=", nd, re.I)) and "x" in nd and not re.search(r"lớp|học sinh|cây|quyển|sách", nd)


def la_tinh(q):
    nd = q.get("nd", "")
    return not (re.search(r"tìm\s*\$?x", nd, re.I) or (re.search(r"(?<![A-Za-z])\d*x(?![A-Za-z])", nd) and "=" in nd))


def mo_ta(de, q):
    return {"ref": key(de, q), "dang": q["dang"], "ht": q["ht"], "muc": q["muc"], "diem_goc": q["diem"],
            "nd": q["nd"], "dap_an": q["dap_an"], "da_chep": key(de, q) in DA_CHEP,
            **({"can_soat": q["can_soat"]} if q.get("can_soat") else {})}


def nhan(de, q):
    DUNG.add(key(de, q)); ND_DUNG.append(chuan(q["nd"]))


def chon_y(dang_list, ht_ok, loc=lambda q: True):
    """Một ý lẻ theo dạng (ưu tiên dạng đứng trước); trong dạng: câu sạch, đã chép, đề nguồn ít dùng."""
    for dang in dang_list:
        ung = []
        for de, d in DE.items():
            for q in d["cau"]:
                if (q["dang"] == dang and q["ht"] in ht_ok and ok(q, de) and loc(q)
                        and key(de, q) not in DUNG and not na_na(q)):
                    ung.append((not sach(q), key(de, q) not in DA_CHEP, DE_DUNG[de], q.get("diem_uoc", False), de, q))
        if ung:
            ung.sort(key=lambda x: x[:5])
            de, q = ung[0][4], ung[0][5]
            nhan(de, q); DE_DUNG[de] += 1
            return mo_ta(de, q)
    return None


def nhom_bai(d, cap1=False):
    """Gom ý theo bài: 'II.4a' → 'II.4'; 'II.4.2a' → 'II.4.2' (cap1: → 'II.4', gộp cả bài lớn)."""
    g = defaultdict(list)
    for q in d["cau"]:
        if q["ht"] != "TL":
            continue
        m = re.match(r"^((?:[IVX]+\.)?\d+)" if cap1 else r"^((?:[IVX]+\.)?\d+(?:\.\d+)?)", q["cau"])
        g[m.group(1) if m else q["cau"]].append(q)
    return g


def chon_bai(nhom_dang, dmin, dmax, can_co=(), uu_tien=(), muc_tieu=1.5, cap1=False):
    """Nguyên một bài tự luận của một đề: mọi ý thuộc nhom_dang, có đủ các dạng can_co."""
    ung = []
    for de, d in DE.items():
        for b, ys in nhom_bai(d, cap1).items():
            if not all(ok(q, de) and q["dang"] in nhom_dang for q in ys):
                continue
            if any(key(de, q) in DUNG or na_na(q) for q in ys):
                continue
            ds = {q["dang"] for q in ys}
            if not set(can_co) <= ds:
                continue
            t = sum(q["diem"] for q in ys)
            if dmin <= t <= dmax:
                # dạng ưu tiên (để PHỦ dạng) xếp trên cả "câu sạch": ghi chú lệch điểm HDC không hại vì điểm chia lại
                ung.append((-len(set(uu_tien) & ds), not all(sach(q) for q in ys),
                            not all(key(de, q) in DA_CHEP for q in ys), DE_DUNG[de], abs(t - muc_tieu), de, b, ys))
    if not ung:
        return None
    ung.sort(key=lambda x: x[:7])
    de, b, ys = ung[0][5], ung[0][6], ung[0][7]
    for q in ys:
        nhan(de, q)
    DE_DUNG[de] += 1
    return {"nguon": f"{de}#{b}", "y": [mo_ta(de, q) for q in ys]}


def chon_vdc(dang_list):
    """VDC: nguyên bài (bài 5a, 5b lấy cả), dạng theo thứ tự ưu tiên."""
    for dg in dang_list:
        b = chon_bai({dg}, 0.25, 1.0, muc_tieu=0.5)
        if b:
            return b
    return None


def bai(k, ten, loai, tong, items):
    return {"key": k, "ten": ten, "loai": loai, "tong": tong, "items": items}


# ---------------------------------------------------------------- dựng
def de_on(so, vdc):
    # bài tam giác bốc TRƯỚC: ưu tiên bài có cả D17 lẫn D18; dạng nào bài không có thì slot TN 9 bù
    b6 = chon_bai({"D14", "D15", "D16", "D17", "D18", "D13"}, 1.5, 3.5, can_co=("D16",), uu_tien=("D18", "D17"))
    ds6 = {y["dang"] for y in b6["y"]} if b6 else set()
    bu = [x for x in ("D18", "D17") if x not in ds6]
    tn = [chon_y((bu + ["D09", "D22"]) if s == ["D18", "D09", "D22"] else s, {"TN"}) for s in TN_ON]
    co = {c["dang"] for c in tn if c}
    b3 = None
    hut = [x for x in ("D20", "D21") if x not in co]
    if hut:  # hết câu TN biểu đồ ⇒ B3 là bài biểu đồ (gộp cả bài lớn nếu thiếu cả hai), TN slot trống lấy D10
        b3 = chon_bai({"D19", "D20", "D21"}, 0.5, 3.0, can_co=tuple(hut), muc_tieu=1.0, cap1=len(hut) > 1)
        for x, thay in zip(hut, (["D10", "D14"], ["D08", "D14"])):
            i = next(i for i, s in enumerate(TN_ON) if s == [x])
            tn[i] = chon_y(thay, {"TN"})
    if b3 is None:
        b3 = chon_bai({"D10"}, 0.5, 1.5, muc_tieu=1.0)
    b1 = [chon_y([x], {"TL"}, loc=la_tinh) for x in ("D02", "D04")]
    b2 = [chon_y([x], {"TL"}, loc=la_tim_x) for x in ("D05", "D06", "D09")]
    b4 = chon_bai({"D22"}, 1.0, 2.25, muc_tieu=1.5)
    b5 = chon_bai({"D11", "D12", "D13"}, 1.0, 3.0, can_co=("D13",), uu_tien=("D12",))
    b7 = chon_vdc(vdc)
    return {"ten": f"Đề ôn tập {so}", "loai": "on", "so": so, "TN": tn, "bai": [
        bai("tinh", "Thực hiện phép tính", "le", 1.0, b1),
        bai("timx", "Tìm x", "le", 1.5, b2),
        bai("thucte", "Bài toán thực tế" if b3 and b3["y"][0]["dang"] == "D10" else "Biểu đồ", "nguyen", 0.75, b3),
        bai("tile", "Bài toán chia theo tỉ lệ", "nguyen", 1.0, b4),
        bai("songsong", "Hai đường thẳng song song", "nguyen", 1.0, b5),
        bai("tamgiac", "Tam giác bằng nhau", "nguyen", 1.25, b6),
        bai("vdc", "Vận dụng cao", "nguyen", 0.5, b7)]}


def de_ct(so, vdc):
    tn = [chon_y(s, {"TN"}) for s in TN_CT]
    b1 = [chon_y(s, {"TL"}, loc=la_tinh) for s in (["D02"], ["D04"], ["D04", "D02"])]
    b2 = [chon_y(s, {"TL"}, loc=la_tim_x) for s in (["D05"], ["D09"], ["D05", "D09"])]
    b3 = chon_bai({"D22"}, 1.0, 2.25, muc_tieu=1.5)
    b4 = chon_bai({"D11", "D12", "D13"}, 1.5, 3.0, can_co=("D13",))
    b5 = chon_bai({"D14", "D15", "D16", "D17", "D18", "D13"}, 1.5, 3.5, can_co=("D16", "D17"))
    b6 = chon_vdc(vdc)
    return {"ten": f"Đề chính thức {so}", "loai": "ct", "so": so, "TN": tn, "bai": [
        bai("tinh", "Thực hiện phép tính", "le", 1.5, b1),
        bai("timx", "Tìm x", "le", 1.5, b2),
        bai("tile", "Bài toán chia theo tỉ lệ", "nguyen", 1.5, b3),
        bai("songsong", "Hai đường thẳng song song", "nguyen", 1.5, b4),
        bai("tamgiac", "Tam giác bằng nhau", "nguyen", 1.5, b5),
        bai("vdc", "Vận dụng cao", "nguyen", 0.5, b6)]}


def refs(D):
    for c in D["TN"]:
        if c:
            yield c
    for b in D["bai"]:
        it = b["items"]
        if isinstance(it, list):
            yield from (c for c in it if c)
        elif it and "y" in it:
            yield from it["y"]
        elif it:
            yield it


def main():
    RA.mkdir(parents=True, exist_ok=True)
    # đề ôn bốc TRƯỚC (cần câu dạng hiếm + bài tam giác có D18), rồi đề chính thức
    bo = [de_on(1, ["D27"]), de_on(2, ["D26", "D27"]), de_on(3, ["D27"]),
          de_ct(1, ["D27"]), de_ct(2, ["D26", "D27"]), de_ct(3, ["D27"])]
    (RA / "l7-ck1.json").write_text(json.dumps(bo, ensure_ascii=False, indent=1))
    md = ["# Bốc câu CK1 Toán 7 — bản 2 (ôn phủ đủ dạng · chính thức top dạng)", ""]
    thieu = 0
    for D in bo:
        md += [f"## {D['ten']}", ""]
        for i, c in enumerate(D["TN"], 1):
            md.append(f"- TN{i}: " + (f"{c['ref']} [{c['dang']} {c['muc']}]{'' if c['da_chep'] else ' (mới)'} {c['nd'][:70]}" if c else "**THIẾU**"))
            thieu += c is None
        for b in D["bai"]:
            it = b["items"]
            if b["loai"] == "le":
                for i, c in enumerate(it, 1):
                    md.append(f"- {b['ten']} {i}: " + (f"{c['ref']} [{c['dang']}]{'' if c['da_chep'] else ' (mới)'} {c['nd'][:70]}" if c else "**THIẾU**"))
                    thieu += c is None
            elif it and "y" in it:
                moi = "" if all(y["da_chep"] for y in it["y"]) else " (mới)"
                md.append(f"- {b['ten']} ({b['tong']}đ): {it['nguon']} {[y['dang'] for y in it['y']]}{moi} {it['y'][0]['nd'][:70]}")
            elif it:
                md.append(f"- {b['ten']} ({b['tong']}đ): {it['ref']} [{it['dang']}]{'' if it['da_chep'] else ' (mới)'} {it['nd'][:70]}")
            else:
                md.append(f"- {b['ten']}: **THIẾU**"); thieu += 1
        if D["loai"] == "on":
            co = {c["dang"] for c in refs(D)}
            hut = [x for x in PHAM_VI if x not in co]
            md.append(f"- **Phủ dạng:** {len(set(PHAM_VI) & co)}/22" + (f" — THIẾU {hut}" if hut else " ✓"))
            thieu += len(hut)
        md.append("")
    tat = [c for D in bo for c in refs(D)]
    moi = [c["ref"] for c in tat if not c["da_chep"]]
    nguon = Counter(c["ref"].split("#")[0] for c in tat)
    md += [f"Tổng ý: {len(tat)} · đã chép sẵn: {len(tat) - len(moi)} · CẦN CHÉP MỚI: {len(moi)} · ô thiếu: {thieu} · "
           f"đề nguồn dùng: {len(nguon)}/30 · nhiều nhất: {nguon.most_common(3)}"]
    (RA / "l7-ck1.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
