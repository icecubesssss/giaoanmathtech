#!/usr/bin/env python3
"""Dựng mảng giá trị/công thức cho 3 tab phân dạng theo phương pháp chương X Hình học (khuôn chương VI, VII, VIII).

Đầu vào: inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10/phan-dang-y.json (gom_phan_dang_y.py --chuong 10 --ghi)
         + khung config/khung-phan-dang/lop-9-hinh-hoc-chuong-10.json (danh_muc_dang).
Đầu ra (thư mục OUT, mặc định $TMPDIR/pd10): y.json, ky-thuat.json, dang.json, chinh.json, batch_sheets.json.

    .venv/bin/python scripts/sheets_phan_dang_y_ch10_9.py [--out DIR]
"""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-hinh-hoc-chuong-10.json"
PDY = REPO / "inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10/phan-dang-y.json"
LA_MA = "X"
T_Y = f"Ý Ch.{LA_MA} lớp 9C"
T_KT = f"Kỹ thuật Ch.{LA_MA} lớp 9C"
T_D = f"Dạng Ch.{LA_MA} lớp 9C"
T_CHINH = f"Phân dạng Ch.{LA_MA} lớp 9C"
PHIEU = {"P1": "Phiếu 1 (trụ + nón + cầu, t32)", "P2": "Phiếu 2 (luyện tập + KT chương X, t33)", "ngoài 9C": "ngoài 9C"}

# Đề xuất dựa trên thống kê % đề thật (11 Vào 10 gồm 3 đề Sở, 27 CK2, 8 GK2) — gom 19/11/2026:
DE_XUAT = {
    "C10-01": ("Dạy", "Nền NB buổi mở: gọi tên r, h, l, R; hình khai triển (4% CK2); làm câu trắc nghiệm NB đầu phiếu"),
    "C10-02": ("Dạy", "Trọng tâm số 1: Câu IV.1a cả 3 đề Sở (64% Vào 10, 74% CK2, 88% GK2); bẫy đường kính, chiều cao theo mực nước"),
    "C10-03": ("Thầy xem", "Nón cần Pythagore: 0% mọi kỳ thi (nón 0/3 đề Sở); chỉ 1–2 bài trong phiếu 1, không làm đích"),
    "C10-04": ("Thầy xem", "Tính ngược r, h, R: 0% Vào 10, 7% CK2; dưới ngưỡng 20% ⇒ chỉ dạy trong khung, không làm đích"),
    "C10-05": ("Dạy", "Trọng tâm số 2: bài thực tế một khối, Câu IV.1b đề 2025 (36% Vào 10, 52% CK2, 88% GK2)"),
    "C10-06": ("Dạy", "Đích Câu IV.1b đề 2026 (múc 80% thể tích, làm tròn LÊN 17 xô); 27% Vào 10"),
    "C10-07": ("Dạy", "Đích Câu IV.1b đề minh hoạ (5 viên bi, nước dâng); 27% Vào 10, 19% CK2 — ý tưởng duy nhất ngoài công thức"),
    "C10-08": ("Thầy xem", "Lật ngược chai: 0% đề thi, chỉ 3 bài sách tham khảo; bẫy 'chiều cao theo mực nước' đã nằm trong C10-02, C10-05"),
    "C10-09": ("Dạy", "Ghép / hiệu khối: 18% Vào 10 (thi thử), 11% CK2; Thầy chốt 12/11 chỉ để ở BTVN phiếu 2"),
    "C10-10": ("Không", "Đồng dạng trong hình nón: 0% đề thi, 5 bài sách tham khảo, cần Thales + lập phương tỉ số"),
    "C10-11": ("Không", "Khối nội/ngoại tiếp đa diện theo tham số: 0% đề thi; vượt lớp C"),
    "C10-12": ("Không", "Cực trị, lập hệ theo kích thước, viên phân: chỉ câu V phân loại (7% CK2)"),
}


def q(t):
    return "'" + t.replace("'", "''") + "'"


def main():
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else Path(os.environ.get("TMPDIR", "/tmp")) / "pd10"
    out.mkdir(parents=True, exist_ok=True)
    dm = json.loads(KHUNG.read_text())["danh_muc_dang"]
    ys = json.loads(PDY.read_text())["y"]
    Y, KT, D = q(T_Y), q(T_KT), q(T_D)
    n_kt, n_d = len(dm["dang"]), len(dm["dang_gop"])
    kt_end, d_end = 4 + n_kt, 4 + n_d

    # --- tab Ý ---
    rows = [["Mã câu", "Ý", "Tóm tắt ý", "Mã kỹ thuật", "Mức", "Biến thể", "Lý do đổi mức", "Tên kỹ thuật", "Nhóm",
             "Phiếu 9C", "Kỳ thi", "Đề thi", "Hạng mức (1 NB, 2 TH, 3 VD, 4 VDC)", "Mã dạng", "Tên dạng"]]
    for i, y in enumerate(ys, 2):
        r = str(i)
        l_co_dinh = y["de_id"] if y["ma_cau"].startswith("so-hn") else None
        rows.append([
            y["ma_cau"], ("'" + y["nhan"]) if y["nhan"] else "", y["tom_tat"], y["ma_dang"], y["muc"], y["bien_the"],
            y["ly_do_muc"],
            f'=IF($D{r}="NGOAI","Ngoài chương {LA_MA}",IFERROR(XLOOKUP($D{r},{KT}!$A$5:$A${kt_end},{KT}!$E$5:$E${kt_end}),"MÃ LẠ"))',
            f'=IF($D{r}="NGOAI","Ngoài chương {LA_MA}",IFERROR(XLOOKUP($D{r},{KT}!$A$5:$A${kt_end},{KT}!$C$5:$C${kt_end}),"MÃ LẠ"))',
            f'=IF($D{r}="NGOAI","",IFERROR(XLOOKUP($D{r},{KT}!$A$5:$A${kt_end},{KT}!$I$5:$I${kt_end}),"MÃ LẠ"))',
            f'=IF(REGEXMATCH($A{r},"^(so-hn|v10)"),"Vào 10",IF(REGEXMATCH($A{r},"^ck2"),"CK2",IF(REGEXMATCH($A{r},"^gk2"),"GK2",IF(REGEXMATCH($A{r},"^ck1"),"CK1",IF(REGEXMATCH($A{r},"^gk1"),"GK1",IF(REGEXMATCH($A{r},"^sgk"),"SGK","Sách tham khảo"))))))',
            l_co_dinh or f'=IF(OR($K{r}="SGK",$K{r}="Sách tham khảo"),"",IFERROR(TRIM(REGEXEXTRACT(XLOOKUP($A{r},{q(T_CHINH)}!$M:$M,{q(T_CHINH)}!$B:$B,""),"^[^,]*")),""))',
            f'=IFERROR(MATCH($E{r},{{"NB","TH","VD","VDC"}},0),0)',
            f'=IF($D{r}="NGOAI","NGOAI",IFERROR(XLOOKUP($D{r},{KT}!$A$5:$A${kt_end},{KT}!$B$5:$B${kt_end}),"MÃ LẠ"))',
            f'=IF($N{r}="NGOAI","Ngoài chương {LA_MA}",IFERROR(XLOOKUP($N{r},{D}!$A$5:$A${d_end},{D}!$B$5:$B${d_end}),"MÃ LẠ"))',
        ])
    (out / "y.json").write_text(json.dumps({"range": f"{q(T_Y)}!A1", "values": rows}, ensure_ascii=False))

    def pct(col_ma, ky_cell, tong_cell, r):
        return (f"=IFERROR(ROWS(UNIQUE(FILTER({Y}!$L$2:$L,{Y}!${col_ma}$2:${col_ma}=$A{r},{Y}!$K$2:$K={ky_cell})))"
                f"/{tong_cell},0)")

    def tong(ky_cell):
        return f"=IFERROR(ROWS(UNIQUE(FILTER({Y}!$L$2:$L,{Y}!$K$2:$K={ky_cell}))),0)"

    # --- tab Kỹ thuật ---
    kt = [[f"Kỹ thuật chương {LA_MA} (cấp chi tiết dưới Dạng): mỗi ý trong tab {T_Y} mang đúng một mã kỹ thuật"],
          ["Một dạng là một phương pháp giải (một chuỗi bước). Bối cảnh, số liệu, hình thức ghi ở cột Biến thể của tab Ý, không tạo dạng mới.",
           *[""] * 12, f"Số đề có câu chương {LA_MA}", tong("O$3"), tong("P$3"), tong("Q$3")],
          [f"% đề = số đề có ít nhất một ý thuộc kỹ thuật chia cho số đề có câu chương {LA_MA} cùng kỳ thi.",
           *[""] * 12, "Kỳ thi", "Vào 10", "CK2", "GK2"],
          ["Mã kỹ thuật", "Mã dạng", "Nhóm", "Dạng chuẩn (cấp 1)", "Tên kỹ thuật", "Cách làm (chuỗi bước)",
           "Dấu hiệu nhận diện", "Mức gốc", "Phiếu 9C", "Số ý", "NB", "TH", "VD", "VDC", "% đề Vào 10", "% đề CK2",
           "% đề GK2", "Dạy 9C (theo tab Dạng)"]]
    for i, d in enumerate(dm["dang"], 5):
        r = str(i)
        kt.append([d["ma"], d["dang"], d["ten_nhom"], d["cap1"], d["ten"], d["cach_lam"], d["dau_hieu"], d["muc_goc"],
                   PHIEU[d["phieu_9c"]], f"=COUNTIF({Y}!$D$2:$D,$A{r})",
                   *[f"=COUNTIFS({Y}!$D$2:$D,$A{r},{Y}!$E$2:$E,{c}$4)" for c in "KLMN"],
                   pct("D", "O$3", "O$2", r), pct("D", "P$3", "P$2", r), pct("D", "Q$3", "Q$2", r),
                   f"=XLOOKUP($B{r},{D}!$A$5:$A${d_end},{D}!$M$5:$M${d_end},FALSE)"])
    (out / "ky-thuat.json").write_text(json.dumps({"range": f"{q(T_KT)}!A1", "values": kt}, ensure_ascii=False))

    # --- tab Dạng ---
    dg = [[f"Dạng chương {LA_MA} (cấp dạy): mỗi dạng gồm một hoặc vài kỹ thuật ở tab {T_KT}"],
          ["Chỉ tách hai dạng khi biết làm dạng này vẫn không tự làm được dạng kia; khác công thức cần nhớ thì cùng dạng.",
           *[""] * 7, f"Số đề có câu chương {LA_MA}", tong("J$3"), tong("K$3"), tong("L$3")],
          [f"% đề = số đề có ít nhất một ý thuộc dạng chia cho số đề có câu chương {LA_MA} cùng kỳ thi. Câu IV.1 đề Sở (1 điểm) là bài thực tế hình khối.",
           *[""] * 7, "Kỳ thi", "Vào 10", "CK2", "GK2"],
          ["Mã dạng", "Tên dạng", "Phiếu 9C", "Gồm kỹ thuật", "Số ý", "NB", "TH", "VD", "VDC", "% đề Vào 10",
           "% đề CK2", "% đề GK2", "Dạy 9C (Thầy chốt)", "Đề xuất (Claude)", "Lý do đề xuất", "Ghi chú"]]
    for i, g in enumerate(dm["dang_gop"], 5):
        r = str(i)
        dx, ld = DE_XUAT.get(g["ma"], ("", ""))
        dg.append([g["ma"], g["ten"], PHIEU[g["phieu_9c"]], ", ".join(g["ky_thuat"]), f"=COUNTIF({Y}!$N$2:$N,$A{r})",
                   *[f"=COUNTIFS({Y}!$N$2:$N,$A{r},{Y}!$E$2:$E,{c}$4)" for c in "FGHI"],
                   pct("N", "J$3", "J$2", r), pct("N", "K$3", "K$2", r), pct("N", "L$3", "L$2", r),
                   False, dx, ld, ""])
    (out / "dang.json").write_text(json.dumps({"range": f"{q(T_D)}!A1", "values": dg}, ensure_ascii=False))

    # --- tab chính: C, D, F, J (công thức đọc tab Ý) + P, Q mới ---
    so_dong = len({y["ma_cau"] for y in ys})
    def loc(col):
        return (f'=IFERROR(TEXTJOIN(" · ",TRUE,ARRAYFORMULA(FILTER(IF({Y}!$B$2:$B="","",REGEXREPLACE({Y}!$B$2:$B&"","[).]+$","")&") ")&{Y}!${col}$2:${col},'
                f'{Y}!$A$2:$A=$M{{r}}))),"")')
    cdfj = []
    pq = []
    for i in range(2, so_dong + 2):
        r = str(i)
        cdfj.append([
            f'=IFERROR(INDEX({{"NB","TH","VD","VDC"}},MAX(FILTER({Y}!$M$2:$M,{Y}!$A$2:$A=$M{r}))),"")',
            f'=IFERROR(LET(k,SORTN(FILTER({{{Y}!$N$2:$N,{Y}!$O$2:$O,{Y}!$M$2:$M}},{Y}!$A$2:$A=$M{r}),1,0,3,FALSE),INDEX(k,1,1)&" · "&INDEX(k,1,2)),"")',
        ])
        pq.append([loc("N").replace("{r}", r), loc("D").replace("{r}", r)])
    batch_ops = [
        {"op": "write", "range": f"{q(T_D)}!A1", "data": dg},
        {"op": "write", "range": f"{q(T_KT)}!A1", "data": kt},
        {"op": "write", "range": f"{q(T_Y)}!A1", "data": rows},
        {"op": "write", "range": f"{q(T_CHINH)}!C1:D1", "data": [[
            "Mức độ (cao nhất trong bài; VD lên trước để lựa chọn)",
            f"Dạng bài (dạng chính = ý có mức cao nhất; tự tính từ tab {T_Y})",
        ]]},
        {"op": "write", "range": f"{q(T_CHINH)}!F1", "data": [[f"Phân loại vào phiếu nào? (tự tính từ tab {T_Y})"]]},
        {"op": "write", "range": f"{q(T_CHINH)}!J1", "data": [["Mức độ từng ý"]]},
        {"op": "write", "range": f"{q(T_CHINH)}!C2", "data": cdfj},
        {"op": "write", "range": f"{q(T_CHINH)}!F2", "data": [[f'=IFERROR(TEXTJOIN("; ",TRUE,UNIQUE(FILTER({Y}!$J$2:$J,{Y}!$A$2:$A=$M{i},{Y}!$J$2:$J<>""))),"")'] for i in range(2, so_dong + 2)]},
        {"op": "write", "range": f"{q(T_CHINH)}!J2", "data": [[loc("E").replace("{r}", str(i))] for i in range(2, so_dong + 2)]},
        {"op": "write", "range": f"{q(T_CHINH)}!P1", "data": [[f"Mã dạng từng ý (từ tab {T_Y})", "Mã kỹ thuật từng ý"]] + pq},
    ]
    (out / "batch_sheets.json").write_text(json.dumps(batch_ops, ensure_ascii=False))
    print(f"Ý {len(rows) - 1} dòng · kỹ thuật {n_kt} · dạng {n_d} · tab chính {so_dong} dòng → {out}")


if __name__ == "__main__":
    main()
