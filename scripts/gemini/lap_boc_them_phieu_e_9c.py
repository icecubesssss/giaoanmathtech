#!/usr/bin/env python3
"""Áp 2 việc boc-them-9c-ch6-phieu-e-{lop,btvn}: kiểm SymPy, xếp bài theo mạch, đánh lại số.

    python3 scripts/gemini/lap_boc_them_phieu_e_9c.py [--ghi]

Thứ tự trong mạch (LT1, BTVN NB): NB-a → NB-b → NB-c. TH xếp năng suất → chuyển động → làm chung, rồi VD.
Kiểm: pt_goc (còn mẫu) giải bằng SymPy phải ra nghiệm dương trong check.answer; check.equation phải có đúng nghiệm answer.
"""
import json
import re
import sys
from pathlib import Path

from sympy import Eq, S, simplify, solve, symbols, sympify

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_boc_them_phieu_e_9c import SEED, VID_BTVN, VID_LOP  # noqa: E402

X = symbols("x")
MACH = ["nang-suat", "chuyen-dong", "lam-chung"]
CAM = [r"[Kk]huôn", r"Câu III", r"chưa cần giải", r"\bem\b", r"[Hh]ôm nay", r"Do đó", r"[Ss]uy ra", r"mathbb"]


def kieu_nb(b):
    s = b["statement"]
    return "c" if "Biết phương trình" in s else ("b" if "Chỉ ra câu văn" in s else "a")


def mach_cu(b):
    s = b["statement"].split("[[br]]")[0]
    if "hình chữ nhật" in s:
        return "hcn"
    if re.search(r"vòi|cùng làm|làm chung|làm riêng", s):
        return "lam-chung"
    if re.search(r"km|vận tốc|ca nô", s):
        return "chuyen-dong"
    return "nang-suat"


def nghiem(eq):
    l, r = eq.split("=")
    return solve(Eq(sympify(l.replace("x", "X"), locals={"X": X}), sympify(r.replace("x", "X"), locals={"X": X})), X)


def kiem(b):
    loi = []
    c, pg = b.get("check"), b.get("pt_goc")
    if not c or not pg:
        return ["thiếu check/pt_goc"]
    try:
        ans = sorted(S(a) for a in c["answer"])
        n1 = sorted(nghiem(c["equation"]))
        n2 = nghiem(pg)
        if [simplify(a - b) for a, b in zip(n1, ans)] != [0] * len(ans) or len(n1) != len(ans):
            loi.append(f"check.equation {c['equation']} có nghiệm {n1} ≠ answer {ans}")
        duong = [r for r in n2 if r.is_positive]
        if not duong or not any(simplify(duong[0] - a) == 0 for a in ans):
            loi.append(f"pt_goc {pg} có nghiệm {n2} không khớp answer {ans}")
    except Exception as e:  # noqa: BLE001
        loi.append(f"không parse được: {e}")
    return loi


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    g = kq.get("ket_qua") or kq.get("json") or kq
    print(f"ghi_chu {vid}:", g.get("ghi_chu", "")[:600])
    return [b for s in g["stages"] for b in s["blocks"] if b.get("type") == "problem"]


def main():
    moi_lop, moi_bt = lay(VID_LOP), lay(VID_BTVN)
    loi = []
    for b in moi_lop + moi_bt:
        b["level"] = int(b.get("level", 1))
        if b["level"] == 2 or (b["level"] == 1 and kieu_nb(b) == "c"):
            loi += [f"{b['mach']} {b['statement'][:50]}…: {e}" for e in kiem(b)]
    p = REPO / SEED
    f = json.loads(p.read_text())
    st = {s["kind"]: s for s in f["stages"]}

    # ── LT1: chèn NB mới vào mạch ──
    out, mi = [], -1
    them = {m: sorted([b for b in moi_lop if b["level"] == 1 and b["mach"] == m], key=kieu_nb) for m in MACH}
    seg = {}
    for b in st["practice1"]["blocks"]:
        if b.get("type") == "para" and b.get("variant") == "heading":
            mi += 1
        if b.get("type") == "problem":
            seg.setdefault(mi, []).append(b)
        else:
            out.append(b)
            continue
    p1 = []
    mi = -1
    for b in st["practice1"]["blocks"]:
        if b.get("type") == "problem":
            continue
        if b.get("type") == "para" and b.get("variant") == "heading" and mi >= 0:
            p1 += sorted(seg[mi] + them[MACH[mi]], key=kieu_nb)
        if b.get("type") == "para" and b.get("variant") == "heading":
            mi += 1
        p1.append(b)
    p1 += sorted(seg[mi] + them[MACH[mi]], key=kieu_nb)
    st["practice1"]["blocks"] = p1

    # ── LT2: TH theo mạch rồi VD ──
    p2 = st["practice2"]["blocks"]
    th = [b for b in p2 if b.get("level") == 2] + [b for b in moi_lop if b["level"] == 2]
    vd = [b for b in p2 if b.get("level") == 3]
    st["practice2"]["blocks"] = sorted(th, key=lambda b: MACH.index(b.get("mach") or mach_cu(b))) + vd

    # ── BTVN ──
    rf = st["reflection"]["blocks"]
    dau = [b for b in rf if b.get("type") != "problem"]
    cu = [b for b in rf if b.get("type") == "problem"]
    thu_tu = MACH + ["hcn"]
    nb = [b for b in cu if b["level"] == 1] + [b for b in moi_bt if b["level"] == 1]
    nb = sorted(nb, key=lambda b: (thu_tu.index(b.get("mach") or mach_cu(b)), kieu_nb(b)))
    thb = [b for b in cu if b["level"] == 2] + [b for b in moi_bt if b["level"] == 2]
    thb = sorted(thb, key=lambda b: MACH.index(b.get("mach") or mach_cu(b)))
    st["reflection"]["blocks"] = dau + nb + thb + [b for b in cu if b["level"] == 3]

    # ── chuẩn hoá, đánh số ──
    n = 0
    ds = {}
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                n += 1
                b["label"] = f"Bài {n}."
                b.pop("pt_goc", None)
                b.pop("mach", None)
                b["tier"] = "btvn" if s["kind"] == "reflection" else "onclass"
                ds.setdefault((s["kind"], b["level"]), []).append(n)
                t = b["statement"] + b.get("solution", "")
                loi += [f"{b['label']} /{c}/" for c in CAM if re.search(c, t)]
                if re.search(r"(?<!\\);", t):
                    loi.append(f"{b['label']} có ';'")
    th2, vd2 = ds[("practice2", 2)], ds[("practice2", 3)]
    bt = [x for k, v in ds.items() if k[0] == "reflection" for x in v]
    st["practice1"]["teacher_note"] = ("Khoảng 60 phút. Mỗi mạch giáo viên làm ví dụ cùng lớp, rồi học sinh làm các bài NB "
                                       "ngắn theo thứ tự biểu diễn → lập phương trình → giải và trả lời, chữa nhanh từng bài.")
    st["practice2"]["teacher_note"] = (f"Khoảng 60 phút. Bài {th2[0]}–{th2[-1]} học sinh tự kẻ bảng và trình bày đủ 3 bước, "
                                       f"giáo viên chấm khâu bảng và phương trình trước. Bài {vd2[0]}, {vd2[1]} là bài vận dụng; "
                                       f"Bài {vd2[1]} đề hỏi vận tốc lúc tăng tốc $x+6$ và câu hỏi phụ về giới hạn tốc độ.")
    st["reflection"]["teacher_note"] = (f"Sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà là Bài {min(bt)} đến Bài {max(bt)}, "
                                        f"in thành phiếu riêng. Buổi sau chữa Bài {ds[('reflection', 3)][0]} và "
                                        f"Bài {ds[('reflection', 3)][1]} trước.")
    print("bài:", {f"{k[0]}/L{k[1]}": v for k, v in ds.items()})
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ")
    if "--ghi" in sys.argv and not loi:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi")
    elif "--ghi" in sys.argv:
        print("KHÔNG ghi vì còn lỗi")


if __name__ == "__main__":
    main()
