#!/usr/bin/env python3
"""Ráp seed phiếu G ch.IX 9C (buổi 9.6) từ kết quả Gemini + hình tính toạ độ.

    python3 scripts/gemini/lap_phieu_g_ch9_9c.py          # soát (không ghi)
    python3 scripts/gemini/lap_phieu_g_ch9_9c.py --ghi    # ghi seed

Sau khi ghi, seed là nguồn sự thật — sửa tay/Gemini trên seed, ĐỪNG chạy lại --ghi.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hinh_phieu_h_ch9_9c import tat_ca  # noqa: E402
from viec_phieu_h_ch9_9c import VID  # noqa: E402

SEED = ("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-09-duong-tron-ngoai-tiep-va-noi-tiep/"
        "phieu-h-chung-minh-he-thuc-tich-bang-tam-giac-dong-dang-dua-vao-goc-noi-tiep.json")
SLUG = Path(SEED).stem

META = {  # nhãn: (level, tier, dang_id, cờ thêm)
    "Bài 1.": (1, "onclass", "NB1", {"figure_given": True}),
    "Bài 2.": (2, "onclass", "NB2+TH1", {"figure_given": True, "ve_tiep": 2}),
    "Bài 3.": (2, "onclass", "NB2+TH2", {"figure_given": False, "ve_tiep": 3}),
    "Bài 4.": (3, "onclass", "TH3+VD1", {"figure_given": False, "draw": True}),
    "BTVN 1.": (2, "btvn", "TH1", {"draw": True}),
    "BTVN 2.": (2, "btvn", "TH3+TH1", {"draw": True}),
    "BTVN 3.": (2, "btvn", "TH1", {"draw": True}),
    "BTVN 4.": (3, "btvn", "VD1", {"draw": True}),
}
FIG_W = {"Bài 1.": "0.28", "Bài 2.": "0.30", "Bài 3.": "0.30", "Ví dụ 1.": "0.30", "Ví dụ 2.": "0.32"}
CAM = [r"[Kk]huôn", r"Câu IV(?!\.\d)", r"thang điểm", r"\bem\b", r"các em", r"[Hh]ôm nay", r"ở lớp",
       r"Do đó", r"[Ss]uy ra", r"Như vậy", r"Mặt khác", r"Ta thấy", r"tiếp tuyến và dây", r"bóc tách", r"vừa sức", r"trọn bộ", r"Đích của buổi học.*đích"]


def lay():
    kq = json.loads((REPO / "storage/gemini/xong" / f"{VID}.json").read_text())
    return kq.get("ket_qua") or kq


def main():
    g = lay()
    if g.get("ghi_chu"):
        print("ghi_chu:", g["ghi_chu"][:3000])
    hinh = tat_ca()
    loi = []
    for s in g["stages"]:
        for b in s["blocks"]:
            k = b.get("figure")
            if isinstance(k, str):
                if k not in hinh:
                    loi.append(f"khoá hình lạ: {k}")
                    b.pop("figure")
                else:
                    b["figure"] = {kk: v for kk, v in hinh[k].items() if not kk.startswith("_")}
                    if k in FIG_W:
                        b["figure"]["width"] = FIG_W[k]
            if b.get("type") == "problem":
                nh = b.get("label")
                if nh not in META:
                    loi.append(f"bài lạ: {nh}")
                    continue
                lv, tier, dang, co = META[nh]
                b["level"], b["tier"], b["dang_id"] = lv, tier, dang
                b.update(co)
                b.pop("solution", None) if b.get("solution") == b.get("answer") else None
    kinds = [s["kind"] for s in g["stages"]]
    if kinds != ["review", "concept", "practice1", "practice2", "reflection"]:
        loi.append(f"thứ tự chặng: {kinds}")
    f = {
        "slug": SLUG,
        "title": "Chứng minh hệ thức tích bằng tam giác đồng dạng dựa vào góc nội tiếp",
        "eyebrow": "PHIẾU H • HÌNH HỌC 9 · CHƯƠNG IX — LUYỆN TẬP GÓC NỘI TIẾP",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "chuong": "Chương IX. Đường tròn ngoại tiếp và đường tròn nội tiếp",
        "so_ca": 1,
        "khuon": "chung_minh",
        "btvn_phieu_rieng": True,
        "stages": g["stages"],
    }
    # ── soát chữ ──
    nhan = []
    for s in f["stages"]:
        for b in s["blocks"]:
            nh = b.get("label") or (re.match(r"\\textbf\{([^}]*)\}", b.get("text", "")) or [0, b.get("type")])[1]
            if b.get("type") == "problem":
                nhan.append((nh, b.get("level"), b.get("tier"), b.get("dang_id")))
                if b.get("level", 0) >= 2 and not b.get("hints"):
                    loi.append(f"{nh}: thiếu hints")
                if b.get("options") and len(b["options"]) != 4:
                    loi.append(f"{nh}: options ≠ 4")
            if b.get("type") == "noted" and b.get("variant") == "example":
                n = b["text"].count("[[fill:")
                if n < 6:
                    loi.append(f"{nh}: ví dụ chỉ {n} ô fill")
                if not re.search(r"Vậy[^\[]*\[\[fill:", b["text"]):
                    loi.append(f"{nh}: câu Vậy không có ô fill")
            txt = json.dumps({k: v for k, v in b.items() if k != "figure"}, ensure_ascii=False)
            for pat in CAM:
                for m in re.finditer(pat, txt):
                    loi.append(f"[{s['kind']}] {nh} /{pat}/: …{txt[max(0, m.start() - 50): m.end() + 30]}…")
            for k in ("statement", "answer", "text"):
                c = len(re.findall(r"(?<!\\);", b.get(k) or ""))
                if c:
                    loi.append(f"[{s['kind']}] {nh} {k}: {c} dấu ';'")
            for k in ("statement", "answer", "text"):
                for ln in (b.get(k) or "").split("[[br]]"):
                    if ln.count("\\Rightarrow") > 1:
                        loi.append(f"{nh} {k}: dòng có >1 ⇒: {ln[:90]}")
    print("bài:", nhan)
    for x in loi:
        print("✗", x)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        p = REPO / SEED
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
