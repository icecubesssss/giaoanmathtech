#!/usr/bin/env python3
"""Ráp 2 kết quả Gemini (kt-9c-ch6-de + kt-9c-ch6-dap-an) → đề kiểm tra chương VI 9C.

    python3 scripts/gemini/lap_kt_chuong_6_9c.py          # chỉ soát, in lỗi
    python3 scripts/gemini/lap_kt_chuong_6_9c.py --ghi    # soát + ghi 3 file

Ghi: kiem-tra-chuong/{de-kiem-tra-chuong-vi, ma-tran-va-dap-an-kiem-tra-chuong-vi}.json (theme de_thi)
     + de-kiem-tra.json (thay đề 1 tiết bằng KT-VI, sửa 15-13 Câu 4 và 15-14 Câu 1).
Ma trận sinh từ SO_DO của viec_kt_chuong_6_9c.py (một nguồn số liệu).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_kt_chuong_6_9c import D, SO_DO  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
KT = REPO / D / "kiem-tra-chuong"
DUNG = {"Câu 1.": "C", "Câu 2.": "A", "Câu 3.": "D", "Câu 4.": "B"}
DIEM_Y = {"5a": 1.0, "5b": 1.0, "6": 1.5, "7": 2.5, "8a": 0.5, "8b": 1.5}
CAM = [r"\bem\b", r"các em", r"[Hh]ôm nay", r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\$S\$", r"\$P\$", r"\bS\s*=", r"\bP\s*="]


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    data = kq.get("ket_qua") or kq
    if data.get("ghi_chu"):
        print(f"[{vid}] ghi_chu Gemini: {data['ghi_chu']}")
    return data["stages"]


def so(x):
    return f"{x:g}".replace(".", "{,}")


def bang_ma_tran():
    bang = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.15}\n"
            "\\begin{tabular}{|c|p{8.6cm}|c|c|c|}\n\\hline\n"
            "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} \\\\ \\hline\n"
            + "".join(f"{c.replace('Câu ', '')} & {nd} & {m} & ${so(d)}$ & ${so(ph)}$ \\\\ \\hline\n"
                      for c, nd, m, d, ph, _h, _a in SO_DO)
            + "\\end{tabular}\\end{center}")
    tong = {}
    for _c, _n, m, d, ph, _h, _a in SO_DO:
        a = tong.setdefault(m, [0, 0]); a[0] += d; a[1] += ph
    bt = ("\\begin{center}\\footnotesize\n\\begin{tabular}{|l|c|c|c|c|}\n\\hline\n"
          "\\textbf{Mức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{Tổng} \\\\ \\hline\n"
          f"Điểm & ${so(tong['NB'][0])}$ & ${so(tong['TH'][0])}$ & ${so(tong['VD'][0])}$ & \\textbf{{10}} \\\\ \\hline\n"
          f"Phút & ${so(tong['NB'][1])}$ & ${so(tong['TH'][1])}$ & ${so(tong['VD'][1])}$ & "
          f"\\textbf{{{so(sum(v[1] for v in tong.values()))}}} \\\\ \\hline\n\\end{{tabular}}\\end{{center}}")
    return bang, bt, tong


def soat(de_st, da_st):
    loi = []
    assert abs(sum(r[3] for r in SO_DO) - 10) < 1e-9 and sum(r[4] for r in SO_DO) <= 45
    if [s["kind"] for s in de_st] != ["review", "concept", "practice1", "practice2", "reflection"]:
        loi.append(f"tờ đề sai thứ tự chặng: {[s['kind'] for s in de_st]}")
    if [s["kind"] for s in da_st] != ["concept", "practice1", "practice2", "reflection"]:
        loi.append(f"đáp án sai thứ tự chặng: {[s['kind'] for s in da_st]}")
    nhan = []
    for s in de_st:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                nhan.append(b.get("label"))
                if b["label"] in DUNG:
                    if len(b.get("options", [])) != 4:
                        loi.append(f"{b['label']} không đủ 4 phương án")
                    if b.get("answer") != DUNG[b["label"]]:
                        loi.append(f"{b['label']} answer={b.get('answer')} ≠ {DUNG[b['label']]}")
                if "solution" in b:
                    loi.append(f"{b['label']} tờ đề có solution")
    if nhan != [f"Câu {i}." for i in range(1, 9)]:
        loi.append(f"nhãn câu lệch: {nhan}")
    # chữ cái trong đáp án Phần I
    t1 = da_st[0]["blocks"][0]["text"]
    for k, v in DUNG.items():
        if not re.search(rf"{k[4]}\s*[–-]\s*{v}\b", t1):
            loi.append(f"đáp án Phần I thiếu '{k[4]} – {v}'")
    # tổng barem từng ý
    toan = " [[br]] ".join(b.get("text", "") for s in da_st[:3] for b in s["blocks"])
    for cau in ("5", "6", "7", "8"):
        m = re.search(rf"\\textbf{{Câu {cau}\b.*?(?=\\textbf{{Câu {int(cau) + 1}\b|$)", toan, re.S)
        if not m:
            loi.append(f"không thấy đáp án Câu {cau}"); continue
        khoi = m.group(0)
        phan = re.split(r"\[\[br\]\]\s*(?=[ab]\))", khoi) if cau in ("5", "8") else [khoi]
        for i, p in enumerate(phan[1:] if cau in ("5", "8") else phan):
            y = cau + ("ab"[i] if cau in ("5", "8") else "")
            tong = sum(float(x.replace(",", ".")) for x in re.findall(r"\((\d+(?:,\d+)?)đ\)", p))
            if abs(tong - DIEM_Y.get(y, -1)) > 1e-9:
                loi.append(f"barem ý {y}: cộng {tong} ≠ {DIEM_Y.get(y)}")
    # từ cấm + chấm phẩy giữa hai công thức
    for s in de_st + da_st:
        for b in s["blocks"]:
            for k in ("statement", "text"):
                v = b.get(k) or ""
                for pat in CAM:
                    if re.search(pat, v):
                        loi.append(f"từ cấm /{pat}/ ở {b.get('label') or v[:30]}")
                if re.search(r"\$\s*;\s*\$", v):
                    loi.append(f"chấm phẩy nối công thức ở {b.get('label') or v[:30]}")
    return loi


def main():
    de_st, da_st = lay("kt-9c-ch6-de"), lay("kt-9c-ch6-dap-an")
    loi = soat(de_st, da_st)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} lỗi")
    if "--ghi" not in sys.argv:
        return
    for s in de_st:
        s["title"] = ""
        s.pop("teacher_note", None)
        # phương án ngắn ⇒ mcq_cols xếp 4 cột một hàng (tờ đề vừa khít, ý b Câu 8 không rơi trang)
        for b in s["blocks"]:
            if b.get("label") == "Câu 1.":
                b["statement"] = "Số nghiệm của phương trình $x^2 - 5x + 7 = 0$ là:"
                b["options"] = ["$1$", "$2$", "$0$", "vô số"]
            if b.get("label") == "Câu 3.":
                b["statement"] = "Hai nghiệm của phương trình $5x^2 - 8x + 3 = 0$ là:"
                b["options"] = ["$-1$ và $-\\dfrac{3}{5}$", "$1$ và $-\\dfrac{3}{5}$", "$-1$ và $\\dfrac{3}{5}$", "$1$ và $\\dfrac{3}{5}$"]
    # dòng hai nghiệm dài gãy giữa công thức ⇒ tách nghiệm thứ hai xuống dòng
    for s in da_st:
        for b in s["blocks"]:
            if isinstance(b.get("text"), str):
                b["text"] = b["text"].replace(" và $x_2 = \\dfrac", "[[br]]$x_2 = \\dfrac")
    bang, bt, tong = bang_ma_tran()
    head = {"kind": "review", "number": 1, "title": "Ma trận đề", "blocks": [
        {"type": "para", "text": "\\textbf{ĐỀ KIỂM TRA CHƯƠNG VI — PHƯƠNG TRÌNH BẬC HAI MỘT ẨN (LỚP 9C)} ($45$ phút, thang điểm $10$). "
         "\\textbf{Phạm vi:} cả chương — giải phương trình bậc hai, định lí Viète và nhẩm nghiệm, phương trình chứa ẩn ở mẫu, "
         "giải bài toán bằng cách lập phương trình. Câu 7 bám Câu III.1, Câu 8 bám Câu III.3 đề vào 10 Hà Nội. "
         "Không phương trình nào trùng phiếu A–F; không tham số $m$, không kí hiệu tắt cho tổng, tích hai nghiệm."},
        {"type": "para", "text": bang}, {"type": "para", "text": bt}]}
    for s in da_st:
        s.pop("teacher_note", None)
    base = {"grade_label": "Lớp 9 • Đại số", "class_tier": "C", "theme": "de_thi"}
    de = {"slug": "de-kiem-tra-chuong-vi-lop-9c",
          "title": "Đề kiểm tra Chương VI — Phương trình bậc hai một ẩn (45 phút)",
          "eyebrow": "LỚP 9C • KIỂM TRA CHƯƠNG VI", **base, "stages": de_st}
    mt = {"slug": "ma-tran-va-dap-an-kiem-tra-chuong-vi-lop-9c",
          "title": "Ma trận và đáp án — Kiểm tra Chương VI",
          "eyebrow": "TÀI LIỆU GIÁO VIÊN • LỚP 9C • KIỂM TRA CHƯƠNG VI", **base, "stages": [head] + da_st}
    KT.mkdir(exist_ok=True)
    (KT / "de-kiem-tra-chuong-vi.json").write_text(json.dumps(de, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (KT / "ma-tran-va-dap-an-kiem-tra-chuong-vi.json").write_text(json.dumps(mt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    sp_path = REPO / D / "de-kiem-tra.json"
    sp = json.loads(sp_path.read_text(encoding="utf-8"))
    for d in sp["de"]:
        if d["ma"] == "15-13":
            d["pham_vi"] = d["pham_vi"].replace("lập phương trình khi biết hai nghiệm", "biết một nghiệm, tìm nghiệm còn lại và hệ số")
            for c in d["cau"]:
                if c["ma"] == "Câu 4":
                    c.update(dang="Phương trình $x^2-7x+c=0$ có một nghiệm bằng $2$: tìm nghiệm còn lại và hệ số $c$",
                             dap_an="tổng hai nghiệm $=7$ nên nghiệm còn lại $=5$; $c=2\\cdot 5=10$")
        if d["ma"] == "15-14":
            for c in d["cau"]:
                c["dang"] = c["dang"].replace("Kiểm $\\Delta$", "Xét $\\Delta$")
            d["pham_vi"] = d["pham_vi"].replace("kiểm $\\Delta$", "xét $\\Delta$").replace("Ba bước của khuôn Câu III.3", "Ba bước tính biểu thức của hai nghiệm (Câu III.3)")
            d["ten"] = d["ten"].replace("Câu III.3: khuôn Viète (biểu thức của hai nghiệm)", "Định lí Viète: biểu thức của hai nghiệm")
    sp["de"] = [d for d in sp["de"] if d["ma"] not in ("1tiet-VI", "KT-VI")] + [{
        "ma": "KT-VI", "ten": "Đề kiểm tra Chương VI — Phương trình bậc hai một ẩn (45 phút)",
        "tuan": 27, "phut": 45, "diem_toi_da": 10.0,
        "pham_vi": "Cả chương VI: giải phương trình bậc hai, định lí Viète, phương trình chứa ẩn ở mẫu, giải bài toán bằng cách lập phương trình. "
                   "Phần I trắc nghiệm 2 điểm; tự luận bám Câu III đề vào 10 (III.1 lập phương trình, III.3 Viète có hạ bậc).",
        "cau": [{"ma": c, "dang": nd, "band": m, "diem": d, "phut": ph, "hinh_thuc": h, "dap_an": a}
                for c, nd, m, d, ph, h, a in SO_DO]}]
    sp_path.write_text(json.dumps(sp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ghi 3 file", {k: v for k, v in tong.items()})


if __name__ == "__main__":
    main()
