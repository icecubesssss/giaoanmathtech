#!/usr/bin/env python3
"""Dựng mảng giá trị/công thức cho 3 tab phân dạng theo phương pháp chương VII (khuôn chương VI 16/11/2026).

Đầu vào: inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07/phan-dang-y.json (gom_phan_dang_y.py --chuong 07 --ghi)
         + khung config/khung-phan-dang/lop-9-dai-so-chuong-07.json (danh_muc_dang).
Đầu ra (thư mục OUT, mặc định $TMPDIR/pd7): y.json, ky-thuat.json, dang.json, chinh.json — mỗi file là
{"range": A1, "values": [[...]]} để ghi bằng update_formulas. Đề xuất (Claude) của tab Dạng ở DE_XUAT.

    .venv/bin/python scripts/sheets_phan_dang_y_ch7_9.py [--out DIR]
"""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-07.json"
PDY = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07/phan-dang-y.json"
LA_MA = "VII"
T_Y = f"Ý Ch.{LA_MA} lớp 9C"
T_KT = f"Kỹ thuật Ch.{LA_MA} lớp 9C"
T_D = f"Dạng Ch.{LA_MA} lớp 9C"
T_CHINH = f"Phân dạng Ch.{LA_MA} lớp 9C"
PHIEU = {"P1": "Phiếu 1 (tần số, tần số tương đối, ghép nhóm)", "ngoài 9C": "ngoài 9C"}

# Đề xuất của Claude cho cột N/O tab Dạng (sửa sau khi có số %): mã dạng → (đề xuất, lý do)
DE_XUAT = {
    "C7-01": ("Dạy", "NB nền của Câu I.1: đọc bảng, biểu đồ, cỡ mẫu; GK2 55%, CK2 44%"),
    "C7-02": ("Dạy", "Trọng tâm: khuôn Câu I.1 đề Sở (1,0đ); Vào 10 69%, CK2 78%, GK2 86%"),
    "C7-03": ("Dạy", "TH đi kèm Câu I.1 (đếm theo điều kiện, nhóm gộp); 18-19% mỗi kỳ"),
    "C7-04": ("Dạy", "Ít câu, chỉ một phép nhân n = f·N; cần khi đề cho biểu đồ tần số tương đối"),
    "C7-05": ("Dạy", "Kiến thức chính Bài 24; GK2 18%, có ở đề thi thử"),
    "C7-06": ("Thầy xem", "Đề thi ít hỏi vẽ (3-14%), tốn giờ: chỉ vẽ cột ghép nhóm, giao BTVN"),
    "C7-07": ("Thầy xem", "0% Vào 10 và CK2: nêu cách vẽ ở Kiến thức, đọc biểu đồ quạt đã thuộc C7-02"),
    "C7-08": ("Thầy xem", "Gần 0% đề: chỉ 1-2 câu NB trắc nghiệm"),
    "C7-09": ("Dạy", "Kiểm tra nhận định có ở đề thi thử 2026 (11% Vào 10); lồng vào ý cuối"),
    "C7-10": ("Không", "Kiến thức lớp 8; chỉ dùng làm NB kiến thức cũ nếu cần"),
}


def q(t):
    return "'" + t.replace("'", "''") + "'"


def main():
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else Path(os.environ.get("TMPDIR", "/tmp")) / "pd7"
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
          ["Một dạng là một phương pháp giải (một chuỗi bước). Bối cảnh, số liệu, có hay không ghép nhóm, hình thức ghi ở cột Biến thể của tab Ý, không tạo dạng mới.",
           *[None] * 12, f"Số đề có câu chương {LA_MA}", tong("O$3"), tong("P$3"), tong("Q$3")],
          [f"% đề = số đề có ít nhất một ý thuộc kỹ thuật chia cho số đề có câu chương {LA_MA} cùng kỳ thi.",
           *[None] * 12, "Kỳ thi", "Vào 10", "CK2", "GK2"],
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
           *[None] * 7, f"Số đề có câu chương {LA_MA}", tong("J$3"), tong("K$3"), tong("L$3")],
          [f"% đề = số đề có ít nhất một ý thuộc dạng chia cho số đề có câu chương {LA_MA} cùng kỳ thi. Ma trận Sở: mạch Thống kê không có câu vận dụng.",
           *[None] * 7, "Kỳ thi", "Vào 10", "CK2", "GK2"],
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
    def loc(col, sep=" · "):
        return (f'=IFERROR(TEXTJOIN("{sep}",TRUE,ARRAYFORMULA(FILTER(IF({Y}!$B$2:$B="","",{Y}!$B$2:$B&") ")&{Y}!${col}$2:${col},'
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
    chinh = {
        "C_D": {"range": f"{q(T_CHINH)}!C2", "values": cdfj},
        "F": {"range": f"{q(T_CHINH)}!F2", "values": [[f'=IFERROR(TEXTJOIN("; ",TRUE,UNIQUE(FILTER({Y}!$J$2:$J,{Y}!$A$2:$A=$M{i},{Y}!$J$2:$J<>""))),"")'] for i in range(2, so_dong + 2)]},
        "J": {"range": f"{q(T_CHINH)}!J2", "values": [[loc("E").replace("{r}", str(i))] for i in range(2, so_dong + 2)]},
        "P_Q": {"range": f"{q(T_CHINH)}!P1", "values": [[f"Mã dạng từng ý (từ tab {T_Y})", "Mã kỹ thuật từng ý"]] + pq},
        "tieu_de": {"range": f"{q(T_CHINH)}!C1", "values": [[
            "Mức độ (cao nhất trong bài; VD lên trước để lựa chọn)",
            f"Dạng bài (dạng chính = ý có mức cao nhất; tự tính từ tab {T_Y})", None,
            f"Phân loại vào phiếu nào? (tự tính từ tab {T_Y})", None, None, None, "Mức độ từng ý"]]},
    }
    (out / "chinh.json").write_text(json.dumps(chinh, ensure_ascii=False))
    print(f"Ý {len(rows) - 1} dòng · kỹ thuật {n_kt} · dạng {n_d} · tab chính {so_dong} dòng → {out}")


if __name__ == "__main__":
    main()
