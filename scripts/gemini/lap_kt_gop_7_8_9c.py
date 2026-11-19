#!/usr/bin/env python3
"""Ráp 2 kết quả Gemini (kt-9c-ch78-de + kt-9c-ch78-dap-an) → đề kiểm tra gộp chương VII + VIII 9C.

    python3 scripts/gemini/lap_kt_gop_7_8_9c.py          # chỉ soát, in lỗi
    python3 scripts/gemini/lap_kt_gop_7_8_9c.py --ghi    # soát + ghi 2 file

Ghi: <ch.VIII>/kiem-tra-chuong/{de-kiem-tra-chuong-vii-viii, ma-tran-va-dap-an-kiem-tra-chuong-vii-viii}.json
Ma trận sinh từ SO_DO + NGUON của viec_kt_gop_7_8_9c.py (một nguồn số liệu).
KHÔNG đụng de-kiem-tra.json / thuyet-minh.json (chương VIII chưa có DeSpec).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_kt_gop_7_8_9c import D, DIEM_Y, DUNG, NGUON, SO_DO  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
KT = REPO / D / "kiem-tra-chuong"
CAM = [r"\bem\b", r"các em", r"[Tt]heo em", r"[Hh]ôm nay", r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\\times", r"\\smallskip"]


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
    tong = {"NB": [0, 0], "TH": [0, 0], "VD": [0, 0]}   # 19/11: không còn câu VD ⇒ cột VD ghi 0
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
        phan = re.split(r"\[\[br\]\]\s*(?=[abc]\))", m.group(0))[1:]
        y_can = sorted(k for k in DIEM_Y if k[0] == cau)
        if len(phan) != len(y_can):
            loi.append(f"Câu {cau}: tách được {len(phan)} ý, cần {len(y_can)}"); continue
        for y, p in zip(y_can, phan):
            tong = sum(float(x.replace(",", ".")) for x in re.findall(r"\((\d+(?:,\d+)?)đ\)", p))
            if abs(tong - DIEM_Y[y]) > 1e-9:
                loi.append(f"barem ý {y}: cộng {tong} ≠ {DIEM_Y[y]}")
    for s in de_st + da_st:
        for b in s["blocks"]:
            for k in ("statement", "text"):
                v = b.get(k) or ""
                for pat in CAM:
                    if re.search(pat, v):
                        loi.append(f"từ cấm /{pat}/ ở {b.get('label') or v[:30]}")
                # chấm phẩy nối hai CÔNG THỨC (dãy số $4$; $8$ thì được)
                for a_, b_ in re.findall(r"\$([^$]*)\$\s*;\s*\$([^$]*)\$", v):
                    if not (re.fullmatch(r"[\d{},\\ldots.]+", a_.strip()) and re.fullmatch(r"[\d{},\\ldots.]+", b_.strip())):
                        loi.append(f"chấm phẩy nối công thức ở {b.get('label') or v[:30]}: ${a_}$; ${b_}$")
    return loi


def main():
    de_st, da_st = lay("kt-9c-ch78-de"), lay("kt-9c-ch78-dap-an")
    loi = soat(de_st, da_st)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} lỗi")
    if "--ghi" not in sys.argv:
        return
    for s in de_st:
        s["title"] = ""
        s.pop("teacher_note", None)
    for s in da_st:
        s.pop("teacher_note", None)
        # Câu 7a: gộp 2 dòng dẫn trước bảng (trang 3 vừa khít ⇒ vạch ngăn chặng rơi sang trang trắng)
        for b in s["blocks"]:
            if isinstance(b.get("text"), str):
                b["text"] = b["text"].replace("lần lượt là ngày đăng ký của Bách và Chi.[[br]]Bảng mô tả không gian mẫu:",
                                              "lần lượt là ngày đăng ký của Bách và Chi. Bảng mô tả không gian mẫu:")
    # 19/11/2026: ý 8b bài toán ngược (C8-09, ngoài lớp 9C, 0 đề Sở) ⇒ biến cố chia cho 7 dư 1 trên cùng hộp bóng.
    # Đè lên bản Gemini (kt-9c-ch78-de / -dap-an) — chạy lại việc Gemini thì sơ đồ trong viec_kt_gop đã là ý mới.
    de_8b = (r"b) \textbf{(1,0 điểm)} Tính xác suất của biến cố $D$: \textquotedblleft Số ghi trên quả bóng được lấy "
             r"ra chia cho $7$ dư $1$\textquotedblright.")
    da_8b = (r"b) Các kết quả thuận lợi cho biến cố $D$ là các số chia cho $7$ dư $1$:[[br]]$1$; $8$; $15$; $22$; $29$; $36$. "
             r"\hfill \textit{(0,5đ)}[[br]]Do đó, số kết quả thuận lợi cho biến cố $D$ là $n(D) = 6$.[[br]]Xác suất của biến "
             r"cố $D$ là $P(D) = \dfrac{n(D)}{n(\Omega)} = \dfrac{6}{36} = \dfrac{1}{6}$. \hfill \textit{(0,25đ)}[[br]]"
             r"Vậy $P(D) = \dfrac{1}{6}$. \hfill \textit{(0,25đ)}")
    for s in de_st:
        for b in s["blocks"]:
            if b.get("label") == "Câu 8." and "gấp $2$ lần" in b["statement"]:
                b["statement"] = re.sub(r"\[\[br\]\]b\) .*$", lambda _m: "[[br]]" + de_8b, b["statement"], flags=re.S)
                b["level"], b["dang_id"] = 2, "TH5"
    for s in da_st:
        for b in s["blocks"]:
            t = b.get("text", "")
            if t.startswith(r"\textbf{Câu 8 (2,0 điểm).}") and "Gọi số quả bóng" in t:
                b["text"] = re.sub(r"\[\[br\]\]b\) Gọi số quả bóng.*$", lambda _m: "[[br]]" + da_8b, t, flags=re.S)
            elif "Câu 8b không đối chiếu điều kiện của ẩn" in t:
                b["text"] = t.replace(r"Câu 8b không đối chiếu điều kiện của ẩn trừ $0{,}25$đ",
                                      r"Câu 8b bỏ sót số $1$ trừ $0{,}25$đ")
    bang, bt, tong = bang_ma_tran()
    nguon = "[[br]]".join(f"\\textbf{{{c}:}} {n}." for c, n in NGUON.items())
    head = {"kind": "review", "number": 1, "title": "Ma trận đề", "blocks": [
        {"type": "para", "text": "\\textbf{ĐỀ KIỂM TRA GỘP CHƯƠNG VII VÀ VIII — TẦN SỐ, TẦN SỐ TƯƠNG ĐỐI VÀ XÁC SUẤT (LỚP 9C)} "
         "($45$ phút, thang điểm $10$, cuối buổi $31/01/2027$ sau phiếu luyện tập chương VIII). "
         "\\textbf{Phạm vi:} chương VII — bảng tần số, tần số tương đối, bảng tần số ghép nhóm và tần số tương đối ghép nhóm; "
         "chương VIII — không gian mẫu, xác suất của biến cố với phép thử một hành động và hai hành động (bảng). "
         "Không có lấy đồng thời, không có lần lượt không trả lại. Câu 5a bám Câu I.1, Câu 6b, 8a, 8b bám Câu I.2 đề vào 10 Hà Nội. Không có câu vận dụng. "
         "Mọi câu lấy từ đề kiểm tra thật, không trùng đề hay số liệu nào của phiếu chương VII, VIII lớp 9C."},
        {"type": "para", "text": bang}, {"type": "para", "text": bt}]}
    # nguồn đề để cuối tài liệu (đặt ở trang 1 thì tiêu đề mồ côi cuối trang)
    da_st[-1]["blocks"].append({"type": "para", "text": "\\textbf{Nguồn đề} (ngân hàng \\texttt{inputs/refs/ngan-hang-sheet/lop-9/dai-so}).[[br]]" + nguon})
    base = {"grade_label": "Lớp 9 • Đại số", "class_tier": "C", "theme": "de_thi"}
    de = {"slug": "de-kiem-tra-chuong-vii-viii-lop-9c",
          "title": "Đề kiểm tra Chương VII và VIII — Thống kê và Xác suất (45 phút)",
          "eyebrow": "LỚP 9C • KIỂM TRA CHƯƠNG VII + VIII", **base, "stages": de_st}
    mt = {"slug": "ma-tran-va-dap-an-kiem-tra-chuong-vii-viii-lop-9c",
          "title": "Ma trận và đáp án — Kiểm tra Chương VII và VIII",
          "eyebrow": "TÀI LIỆU GIÁO VIÊN • LỚP 9C • KIỂM TRA CHƯƠNG VII + VIII", **base, "stages": [head] + da_st}
    KT.mkdir(exist_ok=True)
    (KT / "de-kiem-tra-chuong-vii-viii.json").write_text(json.dumps(de, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (KT / "ma-tran-va-dap-an-kiem-tra-chuong-vii-viii.json").write_text(json.dumps(mt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("ghi 2 file", {k: v for k, v in tong.items()})


if __name__ == "__main__":
    main()
