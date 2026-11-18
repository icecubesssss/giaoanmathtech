#!/usr/bin/env python3
"""Danh mục dạng ĐÓNG chương VII Đại số 9 (Tần số, tần số tương đối) — phân dạng theo PHƯƠNG PHÁP.

Cùng luật với chương VI (scripts/danh_muc_dang_ch6_9.py, Thầy 16/11/2026): một dạng = một phương pháp
(một chuỗi bước); bối cảnh, số liệu, hình thức = biến thể. Hai cấp: KỸ THUẬT (VII-xx) ⊂ DẠNG (C7-xx);
chỉ tách dạng khi biết làm dạng này vẫn không tự làm được dạng kia.

Đặc điểm chương: ma trận Sở cho mạch Thống kê–Xác suất KHÔNG có câu vận dụng (Câu I.1 = 1,0đ NB);
96 đề Vào 10/CK2/GK2 trong tab chỉ có 2 ý bị chấm VD ⇒ mọi dạng có mức gốc NB/TH, không dạng VD.
Chương VII 9C dạy 1 buổi (t31) ⇒ dạng 9C đều thuộc "P1".

Chạy:  .venv/bin/python scripts/danh_muc_dang_ch7_9.py [--ghi]
       ghi khoá `danh_muc_dang` vào config/khung-phan-dang/lop-9-dai-so-chuong-07.json
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-07.json"

NHOM = {
    "N01": "Bảng tần số (Bài 22)",
    "N02": "Tần số tương đối (Bài 23, cả ghép nhóm)",
    "N03": "Ghép nhóm số liệu (Bài 24)",
    "N04": "Biểu đồ: vẽ, chọn loại",
    "N05": "Nhận xét, so sánh",
    "N06": "Biểu đồ thống kê lớp 8 (không phải tần số)",
}

# (mã, nhóm, cấp 1 ở tab "Danh mục dạng chuẩn", phiếu 9C, mức gốc, tên, cách làm, dấu hiệu)
DANG = [
    # --- N01 ---
    ("VII-01", "N01", "D30", "P1", "NB", "Lập bảng tần số từ dãy số liệu (đếm), kể cả dữ liệu không là số",
     "liệt kê các giá trị khác nhau → đếm số lần xuất hiện → bảng tần số; đọc giá trị có tần số lớn nhất",
     "dãy số liệu thô, bảng kiểm đếm, dữ liệu chữ cái/loại; số giá trị khác nhau"),
    ("VII-02", "N01", "D30", "P1", "NB", "Đọc biểu đồ (tranh, cột, đoạn thẳng; có hoặc không ghép nhóm) ra bảng tần số",
     "đọc từng cột/điểm → ghi tần số tương ứng → bảng tần số (ghép nhóm)",
     "lập bảng tần số (ghép nhóm) từ biểu đồ; giá trị/nhóm có tần số lớn nhất trên biểu đồ"),
    ("VII-03", "N01", "D30", "P1", "NB", "Cỡ mẫu; tìm tần số còn thiếu khi biết cỡ mẫu (cả bảng ghép nhóm)",
     "cỡ mẫu = tổng các tần số; tần số thiếu = cỡ mẫu − tổng các tần số đã biết",
     "tính cỡ mẫu, điền ô trống trong bảng tần số"),
    # --- N02 ---
    ("VII-04", "N02", "D30", "P1", "NB", "Tần số tương đối của MỘT giá trị hoặc MỘT nhóm (khuôn Câu I.1 đề Sở)",
     "đọc tần số của giá trị/nhóm → cỡ mẫu (cộng cả bảng) → f = n/N·100%",
     "xác định tần số và tần số tương đối của nhóm [a; b) — chỉ hỏi một giá trị/một nhóm"),
    ("VII-05", "N02", "D30", "P1", "TH", "Lập CẢ bảng tần số tương đối (có hoặc không ghép nhóm)",
     "cỡ mẫu → chia từng tần số cho cỡ mẫu → bảng tần số tương đối (tổng 100%)",
     "lập bảng tần số tương đối (ghép nhóm) từ dãy số liệu, bảng tần số hoặc biểu đồ"),
    ("VII-06", "N02", "D31", "P1", "NB", "Đọc biểu đồ tần số tương đối (hình quạt tròn, cột, đoạn thẳng) ra bảng tần số tương đối",
     "đọc % trên từng hình quạt/cột → bảng tần số tương đối", "biểu đồ ghi %, đọc tỉ lệ của một loại"),
    ("VII-07", "N02", "D30", "P1", "TH", "Tần số tương đối của NHÓM GỘP / đếm theo điều kiện",
     "xác định các giá trị/nhóm thoả điều kiện (dưới, trên, từ … đến …) → cộng tần số → (chia cỡ mẫu)",
     "bao nhiêu phần trăm … dưới/ít nhất/không quá …; số đối tượng hoàn thành trước …; nhóm gộp [a; c)"),
    ("VII-08", "N02", "D30", "P1", "TH", "Tính ngược từ tần số tương đối: tần số n = f·N, cỡ mẫu N = n/f",
     "đọc f (và N hoặc n) → n = f·N hoặc N = n/f", "biết tỉ lệ % và cỡ mẫu, tìm số đối tượng; biết số đối tượng và %, tìm cỡ mẫu"),
    ("VII-09", "N02", "D30", "P1", "TH", "Ước lượng bằng tần số tương đối: số đối tượng trong mẫu khác, xác suất",
     "tính f của giá trị (nhóm) → giả sử tỉ lệ không đổi: số đối tượng ≈ f·(cỡ mẫu mới); xác suất ≈ f",
     "ước lượng số …, giả sử tỉ lệ không đổi, ước lượng xác suất/khả năng"),
    # --- N03 ---
    ("VII-10", "N03", "D32", "P1", "TH", "Ghép nhóm số liệu thô, lập bảng tần số ghép nhóm",
     "chọn/đọc các nhóm [a; b) (chú ý đầu mút) → xếp từng số liệu vào nhóm → đếm → bảng tần số ghép nhóm",
     "dãy số liệu thô + nhóm cho sẵn hoặc tự chia nhóm; quy đổi dữ liệu phân cấp sang khoảng"),
    ("VII-11", "N03", "D32", "P1", "NB", "Giá trị đại diện của nhóm",
     "giá trị đại diện của [a; b) là (a + b)/2", "giá trị đại diện, trung điểm nhóm"),
    # --- N04 ---
    ("VII-12", "N04", "D31", "P1", "TH", "Vẽ biểu đồ dạng cột hoặc đoạn thẳng (tần số, tần số tương đối, ghép nhóm)",
     "chọn trục và đơn vị → dựng cột/điểm theo bảng (ghép nhóm: cột liền nhau; đoạn thẳng dùng giá trị đại diện)",
     "vẽ biểu đồ cột, biểu đồ đoạn thẳng, biểu đồ tần số tương đối ghép nhóm"),
    ("VII-13", "N04", "D31", "P1", "TH", "Vẽ biểu đồ hình quạt tròn",
     "tần số tương đối fᵢ → số đo góc 360°·fᵢ → vẽ các hình quạt, ghi %", "vẽ biểu đồ hình quạt tròn"),
    ("VII-14", "N04", "D31", "P1", "TH", "Chọn loại biểu đồ phù hợp; nhận biết bảng/biểu đồ tần số (tương đối) hợp lệ",
     "xét mục đích biểu diễn và dữ liệu (tổng % = 100%? dữ liệu theo thời gian?) → chọn/loại",
     "biểu đồ nào phù hợp; bảng này có phải bảng tần số tương đối không"),
    # --- N05 ---
    ("VII-15", "N05", "D33", "P1", "TH", "Nhận xét, so sánh hai mẫu; kiểm tra một nhận định từ bảng/biểu đồ",
     "tính các đại lượng cần so (tần số, tần số tương đối, tổng) → so sánh → kết luận đúng/sai",
     "so sánh hai mẫu, nhận định trên đúng hay sai, nhận xét"),
    # --- N06 ---
    ("VII-16", "N06", "D31", "ngoài 9C", "TH", "Biểu đồ thống kê lớp 8: cột kép, đoạn thẳng theo thời gian, số liệu không phải tần số",
     "đọc/vẽ biểu đồ thống kê, tính tổng, tỉ số phần trăm theo yêu cầu",
     "biểu đồ cột kép; số liệu theo năm/tháng; doanh thu, sản lượng — không đếm số lần xuất hiện"),
]

# (mã dạng, tên dạng, phiếu 9C, [kỹ thuật])
DANG_GOP = [
    ("C7-01", "Lập bảng tần số: đếm từ dãy số liệu, đọc từ biểu đồ, cỡ mẫu, tần số còn thiếu", "P1",
     ["VII-01", "VII-02", "VII-03"]),
    ("C7-02", "Tính tần số tương đối, lập bảng tần số tương đối (có hoặc không ghép nhóm) — khuôn Câu I.1", "P1",
     ["VII-04", "VII-05", "VII-06"]),
    ("C7-03", "Tần số tương đối của nhóm gộp, đếm theo điều kiện", "P1", ["VII-07"]),
    ("C7-04", "Tính ngược từ tần số tương đối; ước lượng số đối tượng, xác suất", "P1", ["VII-08", "VII-09"]),
    ("C7-05", "Ghép nhóm số liệu thô, lập bảng tần số ghép nhóm; giá trị đại diện", "P1", ["VII-10", "VII-11"]),
    ("C7-06", "Vẽ biểu đồ cột, đoạn thẳng (tần số, tần số tương đối, ghép nhóm)", "P1", ["VII-12"]),
    ("C7-07", "Vẽ biểu đồ hình quạt tròn", "P1", ["VII-13"]),
    ("C7-08", "Chọn loại biểu đồ; nhận biết bảng, biểu đồ hợp lệ", "P1", ["VII-14"]),
    ("C7-09", "Nhận xét, so sánh hai mẫu, kiểm tra nhận định", "P1", ["VII-15"]),
    ("C7-10", "Biểu đồ thống kê lớp 8 (không phải tần số)", "ngoài 9C", ["VII-16"]),
]


def danh_muc():
    out = []
    for ma, nhom, cap1, phieu, muc, ten, cach, dau_hieu in DANG:
        assert nhom in NHOM, ma
        out.append({"ma": ma, "nhom": nhom, "ten_nhom": NHOM[nhom], "cap1": cap1, "phieu_9c": phieu,
                    "muc_goc": muc, "ten": ten, "cach_lam": cach, "dau_hieu": dau_hieu})
    mas = [d["ma"] for d in out]
    assert len(mas) == len(set(mas))
    ve = {kt: g[0] for g in DANG_GOP for kt in g[3]}
    assert sorted(ve) == sorted(mas), set(mas) ^ set(ve)  # mỗi kỹ thuật thuộc đúng một dạng
    phieu_dang = {g[0]: g[2] for g in DANG_GOP}
    for d in out:
        d["dang"] = ve[d["ma"]]
        assert (d["phieu_9c"] == "ngoài 9C") == (phieu_dang[d["dang"]] == "ngoài 9C"), d["ma"]
    return out


def main():
    dm = danh_muc()
    khung = json.loads(KHUNG.read_text(encoding="utf-8"))
    khung["danh_muc_dang"] = {
        "_mo_ta": "Phân dạng theo PHƯƠNG PHÁP (luật Thầy 16/11/2026); mỗi ý một mã; sinh bởi scripts/danh_muc_dang_ch7_9.py",
        "nhom": NHOM, "dang": dm,
        "dang_gop": [{"ma": m, "ten": t, "phieu_9c": p, "ky_thuat": k} for m, t, p, k in DANG_GOP],
    }
    print(f"{len(dm)} kỹ thuật / {len(DANG_GOP)} dạng ({sum(g[2] != 'ngoài 9C' for g in DANG_GOP)} dạng 9C) / {len(NHOM)} nhóm")
    if "--ghi" in sys.argv:
        KHUNG.write_text(json.dumps(khung, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Đã ghi", KHUNG.relative_to(REPO))


if __name__ == "__main__":
    main()
