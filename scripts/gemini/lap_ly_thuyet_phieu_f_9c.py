#!/usr/bin/env python3
"""Áp việc ly-thuyet-9c-ch6-phieu-f vào phiếu F ch.VI 9C (Thầy 12/11/2026: bỏ hết "khuôn").

    python3 scripts/gemini/lap_ly_thuyet_phieu_f_9c.py          # soát, in tóm tắt
    python3 scripts/gemini/lap_ly_thuyet_phieu_f_9c.py --ghi    # ghi seed

Máy móc (Claude): xoá Bài 1, Bài 9 (trên lớp), Bài 16 (BTVN) — bài "nhận khuôn A/B/C", "đọc thang điểm";
xoá thẻ "Ba tấm bản đồ" ở chặng mở đầu; đánh lại số Bài 1..N + sửa tham chiếu "Bài N" trong chữ.
Gemini: opener, chặng Kiến thức cần nhớ (6 mục lý thuyết cả chương), sơ đồ tư duy, ghi chú GV.
Chạy được trên seed đã sửa một lần (idempotent theo nội dung: chỉ xoá bài còn chữ "khuôn"/"thang điểm").
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_ly_thuyet_phieu_f_9c import SEED, VID  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III(?!\.\d đề)", r"thang điểm", r"\bem\b", r"các em", r"[Hh]ôm nay", r"\bKiểm\b(?! tra)", r"\$S\$", r"\$P\$"]
TIKZ = ("\\begin{tikzpicture}[node distance=4mm and 5mm, font=\\small]\n"
        "  \\node[flownode](a){\\textbf{Bài 19}\\\\Công thức\\\\nghiệm};\n"
        "  \\node[flownode,right=of a](b){\\textbf{Bài 20}\\\\Định lí\\\\Viète};\n"
        "  \\node[flownode,right=of b](c){Phương trình\\\\chứa ẩn\\\\ở mẫu};\n"
        "  \\node[flowkey,right=of c](d){\\textbf{Bài 21}\\\\Lập\\\\phương trình};\n"
        "  \\draw[flowarrow](a)--(b);\n  \\draw[flowarrow](b)--(c);\n  \\draw[flowarrow](c)--(d);\n"
        "\\end{tikzpicture}")


def la_bai_khuon(b):
    s = b.get("statement", "")
    return b.get("type") == "problem" and (s.startswith("Ghi \\textbf{A} (giải phương trình)") or s.startswith("Đọc thang điểm Câu III"))


def main():
    kq = json.loads((REPO / "storage/gemini/xong" / f"{VID}.json").read_text())
    g = kq.get("ket_qua") or kq
    if g.get("ghi_chu"):
        print("ghi_chu Gemini:", g["ghi_chu"])
    p = REPO / SEED
    f = json.loads(p.read_text())
    st = {s["kind"]: s for s in f["stages"]}

    # 1. xoá bài khuôn + thẻ bản đồ
    xoa = [b["label"] for s in f["stages"] for b in s["blocks"] if la_bai_khuon(b)]
    for s in f["stages"]:
        s["blocks"] = [b for b in s["blocks"] if not la_bai_khuon(b)]
    st["review"]["blocks"] = [b for b in st["review"]["blocks"]
                              if not (b.get("type") == "para" and "Ba tấm bản đồ" in b.get("text", ""))
                              and not (b.get("type") == "noted" and b.get("variant") == "note" and "\\textbf{Giải:}" in b.get("text", ""))]
    # 2. đánh lại số
    doi = {}
    n = 0
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem" and re.fullmatch(r"Bài \d+\.", b.get("label", "")):
                n += 1
                doi[int(b["label"][4:-1])] = n
                b["label"] = f"Bài {n}."
    def sua_ref(t):
        return re.sub(r"Bài (\d+)(?!\d)", lambda m: f"Bài {doi.get(int(m.group(1)), m.group(1))}", t)
    # chỉ sửa tham chiếu trong chữ của bài/ví dụ cũ (ghi chú GV do Gemini viết theo số mới)
    for s in f["stages"]:
        for b in s["blocks"]:
            for k in ("statement", "solution", "text", "teacher_note"):
                if isinstance(b.get(k), str) and re.search(r"Bài \d", b[k]):
                    b[k] = sua_ref(b[k])
    # 3. nội dung Gemini
    op = st["review"]["blocks"][0]
    assert op["type"] == "opener"
    op["text"], op["tikz"] = g["opener_text"], TIKZ
    st["concept"]["blocks"] = g["concept_blocks"]
    mm = g["mindmap"]
    mm.setdefault("type", "mindmap")
    rb = st["reflection"]["blocks"]
    assert rb[0]["type"] == "mindmap"
    rb[0] = mm
    for k, v in g["teacher_notes"].items():
        st[k]["teacher_note"] = v

    # soát
    loi = []
    for s in f["stages"]:
        for b in s["blocks"]:
            txt = json.dumps(b, ensure_ascii=False)
            for pat in CAM:
                for m in re.finditer(pat, txt):
                    ctx = txt[max(0, m.start() - 40): m.end() + 40]
                    if "đề chính thức" in ctx or "đề thi thử" in ctx or "đề minh" in ctx:
                        continue  # trích nguồn đề thật — giữ
                    loi.append(f"[{s['kind']}] {b.get('label', b['type'])} /{pat}/: …{ctx}…")
        if re.search(r"[Kk]huôn|Câu III|điểm", s.get("teacher_note", "")):
            loi.append(f"[{s['kind']}] teacher_note còn khuôn/điểm: {s['teacher_note'][:120]}")
    print("xoá:", xoa, "| đổi số:", {k: v for k, v in doi.items() if k != v})
    print("lý thuyết:", [b.get("text", "")[:40] for b in g["concept_blocks"] if b.get("text", "").startswith("\\textbf{")])
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
