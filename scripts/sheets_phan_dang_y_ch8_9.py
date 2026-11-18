#!/usr/bin/env python3
"""Dựng mảng giá trị/công thức cho 3 tab phân dạng theo phương pháp chương VIII (khuôn chương VI & VII).

Đầu vào: inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-08/phan-dang-y.json (gom_phan_dang_y.py --chuong 08 --ghi)
         + khung config/khung-phan-dang/lop-9-dai-so-chuong-08.json (danh_muc_dang).
Đầu ra (thư mục OUT, mặc định $TMPDIR/pd8): y.json, ky-thuat.json, dang.json, chinh.json, batch_sheets.json.

    .venv/bin/python scripts/sheets_phan_dang_y_ch8_9.py [--out DIR]
"""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-08.json"
PDY = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-08/phan-dang-y.json"
LA_MA = "VIII"
T_Y = f"Ý Ch.{LA_MA} lớp 9C"
T_KT = f"Kỹ thuật Ch.{LA_MA} lớp 9C"
T_D = f"Dạng Ch.{LA_MA} lớp 9C"
T_CHINH = f"Phân dạng Ch.{LA_MA} lớp 9C"
PHIEU = {"P1": "Phiếu 1 (gộp một hành động & hai hành động)", "ngoài 9C": "ngoài 9C"}

# Đề xuất dựa trên thống kê % đề thật (38 Vào 10, 24 CK2, 20 GK2) + chốt 18/11:
DE_XUAT = {
    "C8-01": ("Dạy", "Nền Bài 25: nhận biết phép thử ngẫu nhiên, đồng khả năng (5% Vào 10, 4% CK2); làm câu NB Khám phá"),
    "C8-02": ("Dạy", "Nền Bài 25–26: viết không gian mẫu Ω, đếm n(Ω) và n(E) (13% Vào 10, 12% CK2, 15% GK2)"),
    "C8-03": ("Dạy", "Trọng tâm số 1: khuôn Câu I.2 đề Sở (61% Vào 10, 71% CK2, 70% GK2)"),
    "C8-04": ("Dạy", "Câu I.2 dạng trường tự liệt kê Ω từ mô tả số (5% Vào 10, 12% CK2, 5% GK2); HS C hay sót đầu/cuối"),
    "C8-05": ("Thầy xem", "Liên môn bảng/biểu đồ thống kê chương VII (0% Vào 10, 4% CK2, 10% GK2); có thể ghép buổi ôn VII+VIII"),
    "C8-06": ("Dạy", "Trọng tâm 2 hành động (16% Vào 10, 8% CK2); Thầy chốt 18/11 giữ bảng hai chiều trong phiếu gộp 180′"),
    "C8-07": ("Thầy xem", "Lấy đồng thời 2 vật (3% Vào 10, 4% CK2, 20% GK2); cần cân quỹ 180′ gộp cùng hai hành động"),
    "C8-08": ("Thầy xem", "Xếp thứ tự / hoán vị 3–4 đối tượng (3% Vào 10, 0% CK2/GK2; SGK Ví dụ 2 + Bài 8.4)"),
    "C8-09": ("Thầy xem", "Bài toán ngược tìm số vật từ xác suất (3% Vào 10, 4% CK2, 5% GK2); mức VD (ma trận Sở TK–XS = 0đ VD)"),
    "C8-10": ("Không", "Lấy lần lượt không hoàn lại (5% Vào 10, 5% GK2); Thầy đã chốt cắt ở lớp 9C"),
    "C8-11": ("Không", "Phép thử ≥ 3 hành động / quy tắc nhân / đếm nâng cao (5% Vào 10); vượt khuôn 1–2 hành động lớp C"),
    "C8-12": ("Không", "Xác suất thực nghiệm và ước lượng của Toán 8 (5% Vào 10); ngoài chương trình lớp 9"),
    "C8-13": ("Không", "So sánh khả năng xảy ra của các biến cố (0% đề thi; chỉ có 2 bài sách tham khảo)"),
}


def q(t):
    return "'" + t.replace("'", "''") + "'"


def main():
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else Path(os.environ.get("TMPDIR", "/tmp")) / "pd8"
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
        rows.append([
            y["ma_cau"], ("'" + y["nhan"]) if y["nhan"] else "", y["tom_tat"], y["ma_dang"], y["muc"], y["bien_the"],
            y["ly_do_muc"],
            f'=IF($D{r}="NGOAI","Ngoài chương {LA_MA}",IFERROR(XLOOKUP($D{r},{KT}!$A$5:$A${kt_end},{KT}!$E$5:$E${kt_end}),"MÃ LẠ"))',
            f'=IF($D{r}="NGOAI","Ngoài chương {LA_MA}",IFERROR(XLOOKUP($D{r},{KT}!$A$5:$A${kt_end},{KT}!$C$5:$C${kt_end}),"MÃ LẠ"))',
            f'=IF($D{r}="NGOAI","",IFERROR(XLOOKUP($D{r},{KT}!$A$5:$A${kt_end},{KT}!$I$5:$I${kt_end}),"MÃ LẠ"))',
            f'=IF(REGEXMATCH($A{r},"^(so-hn|v10)"),"Vào 10",IF(REGEXMATCH($A{r},"^ck2"),"CK2",IF(REGEXMATCH($A{r},"^gk2"),"GK2",IF(REGEXMATCH($A{r},"^ck1"),"CK1",IF(REGEXMATCH($A{r},"^gk1"),"GK1",IF(REGEXMATCH($A{r},"^sgk"),"SGK","Sách tham khảo"))))))',
            f'=IF(OR($K{r}="SGK",$K{r}="Sách tham khảo"),"",IFERROR(TRIM(REGEXEXTRACT(XLOOKUP($A{r},{q(T_CHINH)}!$M:$M,{q(T_CHINH)}!$B:$B,""),"^[^,]*")),""))',
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
          [f"% đề = số đề có ít nhất một ý thuộc dạng chia cho số đề có câu chương {LA_MA} cùng kỳ thi. Ma trận Sở: mạch Thống kê – Xác suất có 0 điểm vận dụng.",
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
