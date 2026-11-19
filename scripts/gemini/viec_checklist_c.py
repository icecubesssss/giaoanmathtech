#!/usr/bin/env python3
"""Sinh việc Gemini: dựng danh sách dòng cho tab checklist duyệt phiếu 4C / 5C / 7C.

Thầy giao 19/11/2026: dựng lại tab "<Tên> - Checklist duyệt phiếu chi tiết <K>C" (sheet
"Bảng theo dõi tiến độ học liệu - Level C", 1ucQH5…) như tab của ThaiTD; danh sách phiếu lấy
theo tab tiến độ bên file "TIẾN ĐỘ C" (1fH7vl…); nhận xét duyệt cũ ở các tab ẩn (Khối 4_QuyenHM,
Khối 5_Bích, Khối 7_AnDV, NHẬN XÉT) chép sang 2 cột cuối.

Gemini CHỈ quyết: danh sách dòng (chương / phiếu / KT) + dòng cũ nào gắn vào dòng mới nào,
trả về MÃ Ô (TD:27, CU:19, NX:12…). Chữ nhận xét do lap_checklist_c.py chép nguyên văn từ ô gốc.

Dữ liệu: storage/gemini/tep/checklist-c/{cu,moi}.json (bóc từ bản xuất xlsx của 2 file Sheets).
Chạy:  python3 scripts/gemini/viec_checklist_c.py   ⇒ ghi 3 việc vào storage/gemini/hang-doi/
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TEP = REPO / "storage" / "gemini" / "tep" / "checklist-c"
HANG_DOI = REPO / "storage" / "gemini" / "hang-doi"
MODEL = "gemini-4-hydrogen-medium"

# khối -> (tab tiến độ, tab link phụ hoặc None, tab cũ, dải dòng NHẬN XÉT, từ chương)
KHOI = {
    "4c": dict(td="Tiến độ 4C", lk="Khối 4C- QuyenHM", cu="Khối 4_QuyenHM", nx=(5, 10), nhom="Chủ đề",
               ten="QuyenHM", lop="Toán 4 (tiểu học)"),
    "5c": dict(td="Tiến độ 5C - 2026 - BichVN", lk="Khối 5 - BíchVN", cu="Khối 5_Bích", nx=(11, 19), nhom="Chủ đề",
               ten="BichVN", lop="Toán 5 (tiểu học)"),
    "7c": dict(td="TIẾN ĐỘ 7C - 2026- AnDV", lk=None, cu="Khối 7_AnDV", nx=(21, 36), nhom="Chương",
               ten="AnDV", lop="Toán 7 (THCS)"),
}
NX_NGUOI = {"E": "KhanhNT", "F": "KhanhNT – giải pháp", "G": "QuyenHM", "H": "QuyenHM – bổ sung",
            "I": "QuyenHM – giải pháp", "J": "AnDV", "K": "AnDV – giải pháp", "L": "ThaiTD",
            "M": "ThaiTD – giải pháp", "N": "BichVN", "O": "BichVN – giải pháp", "P": "ThuyNT3",
            "Q": "ThuyNT3 – giải pháp", "R": "Tổng kết"}


def rut(s, n):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "…"


def dong_tab(rows, ma, bo_dau=1, n=140):
    """In mỗi dòng: MA:row | col:giá trị [LINK] ..."""
    tieu_de = {k: c.get("v", "") for r in rows if r["row"] == 1 for k, c in r["cells"].items()}
    out = []
    for r in rows:
        if r["row"] <= bo_dau:
            continue
        o = []
        for k, c in r["cells"].items():
            v = c.get("v", "")
            if v in ("", None) and "link" not in c:
                continue
            nhan = rut(tieu_de.get(k, k), 25)
            o.append(f"{nhan}: {rut(v, n)}" + (" [LINK]" if "link" in c else ""))
        if o:
            out.append(f"{ma}:{r['row']} | " + " | ".join(o))
    return out


def dong_cu(rows):
    out = []
    for r in rows:
        if r["row"] <= 5:
            continue
        o = []
        for k, c in sorted(r["cells"].items()):
            v = c.get("v", "")
            if isinstance(v, (int, float)) and v < 40:   # 2/4/6 = ô T+2 mẫu, bỏ
                continue
            if v in ("", None) and "link" not in c:
                continue
            o.append(f"{k}: {rut(v, 220)}" + (" [LINK]" if "link" in c else ""))
        if o:
            out.append(f"CU:{r['row']} | " + " | ".join(o))
    return out


def dong_nx(rows, a, b):
    out = []
    for r in rows:
        if not (a <= r["row"] <= b):
            continue
        o = []
        for k, c in sorted(r["cells"].items()):
            v = c.get("v", "")
            if k in ("A", "B", "C", "D"):
                o.append(f"{k}: {rut(v, 80)}" + (" [LINK]" if "link" in c else ""))
            elif v:
                o.append(f"{NX_NGUOI.get(k, k)}: {rut(v, 160)}")
        if o:
            out.append(f"NX:{r['row']} | " + " | ".join(o))
    return out


PROMPT = """Bạn là trợ lý xếp bảng theo dõi duyệt học liệu {lop}, lớp tầng C, người phụ trách {ten}. KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt này.

VIỆC: dựng DANH SÁCH DÒNG cho tab mới "{ten} - Checklist duyệt phiếu chi tiết {K}" (mỗi dòng = một học liệu cần duyệt) và GẮN các dòng nhận xét duyệt cũ vào đúng dòng mới. Bạn chỉ trả về MÃ Ô (ví dụ TD:27, CU:19, NX:12), không chép chữ nhận xét — máy sẽ tự chép nguyên văn.

MẪU THAM KHẢO (tab của ThaiTD, lớp 9C) — các cột A, B, C như sau:
  A="Chương 6", B="Thuyết minh", C="Thuyết minh chương VI – Phương trình bậc hai"   (loai=chuong)
  A="",          B="Phiếu 6.1",  C="Phương trình bậc hai, biện luận số nghiệm"          (loai=phieu)
  A=" KT C6",    B="KT chương VI", C="Kiểm tra chương VI (90′)"                          (loai=kiem_tra)

LUẬT DỰNG DÒNG
1. Thứ tự dòng = thứ tự dạy trong bảng TIẾN ĐỘ (mã TD). Mỗi {nhom} mở đầu bằng MỘT dòng loai=chuong: cot_A="{nhom} N" (N là số Ả Rập), cot_B="Thuyết minh", ten="Thuyết minh {nhom_thuong} N – <tên {nhom_thuong} viết hoa chữ đầu, có dấu đầy đủ>".
2. Sau đó mỗi buổi dạy có học liệu riêng = MỘT dòng loai=phieu: cot_A="", cot_B="Phiếu N.k" (N = số {nhom_thuong}, k = 1, 2, 3… theo thứ tự buổi trong {nhom_thuong}; nếu bảng tiến độ đã ghi sẵn "Phiếu bài N.k" thì dùng đúng số đó), ten = tên bài ngắn gọn theo cột "Bài cụ thể"/"Tên Bài học" (bỏ chữ "Bài 22:" đứng đầu nếu có; giữ "Luyện tập chung", "Ôn tập…").
   Buổi "Nghỉ" thì bỏ. Buổi dạy tiếp CÙNG một phiếu đã có dòng (ví dụ lớp 4 tuần 48 "Bài 34: Ôn tập phép cộng, phép trừ" lặp lại) thì không tạo dòng mới.
3. Buổi kiểm tra / ôn tập kì / làm đề (Kiểm tra lần n, Ôn tập giữa kì, Kiểm tra cuối chủ đề, Làm đề, Test, Đề 1/2/3…): loai=kiem_tra, đặt đúng vị trí thời gian, cot_A là nhãn ngắn có dấu cách đầu như " KT GK1", " Ôn GK1", " KT CĐ1+2", " KT CK1", " Ôn CK1"…; cot_B là "Đề 1", "Đề 2", "Đề KT"…; ten = mô tả như trong tiến độ. Không tạo dòng thuyết minh cho các nhóm này.
4. link_tu = MÃ dòng có ô [LINK] dẫn tới học liệu của dòng đó: ưu tiên link riêng của phiếu (bảng LINK hoặc bảng CŨ cột D), nếu không có thì link thư mục của {nhom_thuong} ở bảng TIẾN ĐỘ/LINK; dòng thuyết minh lấy link thuyết minh (bảng CŨ dòng "Phiếu thuyết minh…" hoặc bảng LINK). Không có link nào thì để "". Chỉ được dùng mã dòng THỰC SỰ có [LINK].
5. gan_cu: gắn các dòng bảng CŨ (CU:n) và bảng NHẬN XÉT (NX:n) vào dòng mới có CÙNG NỘI DUNG. So theo NỘI DUNG/TÊN BÀI, KHÔNG theo số thứ tự — đánh số phiếu cũ và mới có chỗ lệch (ví dụ phiếu cũ "Ca-04-Phép nhân — Tính chất…" có thể ứng với phiếu mới số khác).
   - Dòng CU nào có nhận xét/kết quả duyệt (có chữ ở cột G trở đi) và dòng NX nào có nhận xét thì PHẢI được gắn ĐÚNG MỘT lần.
   - Dòng NX không có cột D (dòng tiếp nối) thì gắn cùng dòng mới với dòng NX ngay trên có cột D, trừ khi nội dung nói rõ phiếu khác; nhận xét chung cho cả chương thì gắn vào dòng thuyết minh của chương đó.
   - Dòng CU/NX "Phiếu thuyết minh" gắn vào dòng loai=chuong của {nhom_thuong} đó.
   - Phiếu cũ không còn trong tiến độ mới (đã bỏ/gộp): gắn vào dòng phiếu mới đã gộp nội dung đó; nếu không có thì gắn vào dòng thuyết minh của {nhom_thuong} đó.
   - Dòng CU/NX không có nhận xét/kết quả thì KHÔNG cần gắn.
6. ghi_chu: liệt kê ngắn các chỗ bạn không chắc (gắn theo phán đoán, phiếu cũ không khớp, buổi khó xếp), mỗi ý một dòng. Không có thì để "".

BẢNG TIẾN ĐỘ (mã TD) — tab "{td}" bên file TIẾN ĐỘ C:
{bang_td}
{khoi_lk}
BẢNG CŨ (mã CU) — tab ẩn "{cu}". Dòng 4 là tiêu đề cột: {tieu_de_cu}
{bang_cu}

BẢNG NHẬN XÉT (mã NX) — tab ẩn "NHẬN XÉT", phần của khối này (A/B = khối/chương, C = link, D = tên phiếu, các cột khác = nhận xét theo người):
{bang_nx}

Trả về JSON đúng schema: {{"dong": [{{"loai","cot_A","cot_B","ten","link_tu","gan_cu"}}...], "ghi_chu": "..."}}.
"""


def main():
    cu = json.loads((TEP / "cu.json").read_text())
    moi = json.loads((TEP / "moi.json").read_text())
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    for k, cfg in KHOI.items():
        bang_td = dong_tab(moi[cfg["td"]], "TD")
        khoi_lk = ""
        if cfg["lk"]:
            bo = 1
            khoi_lk = (f"\nBẢNG LINK (mã LK) — tab \"{cfg['lk']}\" bên file TIẾN ĐỘ C (chứa link học liệu):\n"
                       + "\n".join(dong_tab(moi[cfg["lk"]], "LK", bo_dau=bo)) + "\n")
        tde = next((r for r in cu[cfg["cu"]] if r["row"] == 4), {"cells": {}})
        tieu_de_cu = "; ".join(f"{c}={v.get('v','')}" for c, v in sorted(tde["cells"].items()))
        prompt = PROMPT.format(
            lop=cfg["lop"], ten=cfg["ten"], K=k.upper(), nhom=cfg["nhom"], nhom_thuong=cfg["nhom"].lower(),
            td=cfg["td"], bang_td="\n".join(bang_td), khoi_lk=khoi_lk, cu=cfg["cu"], tieu_de_cu=tieu_de_cu,
            bang_cu="\n".join(dong_cu(cu[cfg["cu"]])), bang_nx="\n".join(dong_nx(cu["NHẬN XÉT"], *cfg["nx"])),
        )
        viec = {"id": f"checklist-{k}", "model": MODEL, "prompt": prompt, "files": [],
                "schema": "scripts/gemini/schema/checklist-duyet-c.json", "timeout": "1200s",
                "meta": {"loai": "checklist-c", "khoi": k}}
        p = HANG_DOI / f"checklist-{k}.json"
        p.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(p.relative_to(REPO), len(prompt), "ký tự")


if __name__ == "__main__":
    main()
