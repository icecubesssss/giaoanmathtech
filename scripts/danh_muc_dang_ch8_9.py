#!/usr/bin/env python3
"""Danh mục dạng ĐÓNG chương VIII Đại số 9 (Xác suất của biến cố) — phân dạng theo PHƯƠNG PHÁP.

Cùng luật với chương VI & VII (Thầy 16/11/2026): một dạng = một phương pháp (một chuỗi bước);
bối cảnh, số liệu, hình thức = biến thể. Hai cấp: KỸ THUẬT (VIII-xx) ⊂ DẠNG (C8-xx).
Chương VIII 9C (Thầy chốt 18/11/2026): gộp 1 buổi 180′ (t32), dạy cả một hành động và hai hành động
(bảng hai chiều), cắt dạng lấy lần lượt không trả lại.

Chạy:  .venv/bin/python scripts/danh_muc_dang_ch8_9.py [--ghi]
       ghi khoá `danh_muc_dang` vào config/khung-phan-dang/lop-9-dai-so-chuong-08.json
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-08.json"

NHOM = {
    "N01": "Phép thử, không gian mẫu và kết quả thuận lợi (Bài 25, đầu Bài 26)",
    "N02": "Xác suất phép thử một hành động (Bài 26 — khuôn Câu I.2)",
    "N03": "Xác suất phép thử hai hành động độc lập / có hoàn lại (Bài 26)",
    "N04": "Xác suất chọn đồng thời, xếp thứ tự, lấy không hoàn lại",
    "N05": "Bài toán ngược, đếm nâng cao và xác suất thực nghiệm",
}

# (mã, nhóm, cấp 1 ở tab "Danh mục dạng chuẩn", phiếu 9C, mức gốc, tên, cách làm, dấu hiệu)
DANG = [
    # --- N01 ---
    ("VIII-01", "N01", "D34", "P1", "NB",
     "Nhận biết phép thử ngẫu nhiên, kết quả, tính đồng khả năng, biến cố xảy ra hay không",
     "xét kết quả có biết trước không và có liệt kê hết được không; kiểm các kết quả có cùng khả năng không; thay kết quả cụ thể kiểm tra biến cố",
     "hoạt động nào là phép thử ngẫu nhiên; phép thử là gì; có đồng khả năng không; biến cố nào xảy ra"),
    ("VIII-02", "N01", "D34", "P1", "NB",
     "Viết không gian mẫu Ω và đếm n(Ω) — phép thử một hành động (tập nền cho sẵn)",
     "đọc tất cả kết quả có thể từ thẻ, bi, hình quạt, xúc xắc, danh sách cho sẵn → viết Ω = {…} và đếm n(Ω)",
     "viết không gian mẫu / tập hợp kết quả; hỏi n(Ω) của phép thử một hành động cho sẵn tập nền"),
    ("VIII-03", "N01", "D34", "P1", "NB",
     "Tự liệt kê không gian mẫu Ω từ mô tả điều kiện số (phép thử một hành động)",
     "đọc điều kiện của số cần viết/chọn (hai chữ số, lẻ, nhỏ hơn k, chính phương…) → liệt kê đủ từ nhỏ nhất đến lớn nhất → đếm n(Ω)",
     "viết/chọn ngẫu nhiên số tự nhiên có điều kiện rồi yêu cầu viết Ω hoặc tìm n(Ω)"),
    ("VIII-04", "N01", "D34", "P1", "NB",
     "Liệt kê và đếm kết quả thuận lợi n(E) của biến cố (chưa tính xác suất)",
     "đọc điều kiện biến cố E → lọc các phần tử thoả điều kiện từ Ω (hoặc đọc từ bảng) → đếm n(E)",
     "mô tả / xác định các kết quả thuận lợi / số kết quả thuận lợi của biến cố"),
    ("VIII-05", "N01", "D34", "P1", "TH",
     "Mô tả không gian mẫu hai hành động độc lập / có hoàn lại (bảng hai chiều hoặc sơ đồ cây)",
     "xác định kết quả hành động 1 (hàng), hành động 2 (cột) → lập bảng m × n (hoặc sơ đồ cây) các cặp (a; b) → n(Ω) = m·n",
     "chỉ hỏi mô tả không gian mẫu / đếm n(Ω) của phép thử hai hành động độc lập hoặc có hoàn lại"),
    # --- N02 ---
    ("VIII-06", "N02", "D35", "P1", "TH",
     "Tính xác suất phép thử một hành động — tập nền cho sẵn (khuôn Câu I.2)",
     "nêu Ω và n(Ω) → khẳng định đồng khả năng → liệt kê kết quả thuận lợi n(E) → P(E) = n(E)/n(Ω) rút gọn tối giản",
     "quay đĩa, rút 1 thẻ/bi/bóng, gieo 1 xúc xắc, chọn 1 người/sách (chia hết, chia dư, nguyên tố, chính phương, màu, biến cố 'không')"),
    ("VIII-07", "N02", "D35", "P1", "TH",
     "Tính xác suất phép thử một hành động khi phải tự liệt kê không gian mẫu từ điều kiện số",
     "tự liệt kê Ω các số thoả mô tả → đếm n(Ω) → khẳng định đồng khả năng → lọc kết quả thuận lợi n(E) → P(E) = n(E)/n(Ω)",
     "viết/chọn ngẫu nhiên số tự nhiên (hai chữ số, lẻ, nhỏ hơn k…) rồi tính xác suất (kể cả khi ý a đã viết Ω)"),
    ("VIII-08", "N02", "D35", "P1", "TH",
     "Tính xác suất chọn một đối tượng từ bảng thống kê, biểu đồ hoặc tỉ lệ phần trăm",
     "đọc tần số các nhóm từ bảng / biểu đồ cột, cột kép, quạt tròn → cộng tổng n(Ω) → cộng tần số thoả biến cố n(E) → P(E) = n(E)/n(Ω)",
     "cho bảng thống kê, bảng ghép nhóm, biểu đồ cột/cột kép/quạt tròn, hoặc tỉ lệ % → chọn ngẫu nhiên 1 đối tượng, tính xác suất"),
    # --- N03 ---
    ("VIII-09", "N03", "D35", "P1", "TH",
     "Tính xác suất phép thử hai hành động độc lập / có hoàn lại (bảng hai chiều / sơ đồ cây)",
     "lập bảng hai chiều m × n (hoặc sơ đồ cây) tìm n(Ω) → đồng khả năng → đánh dấu ô thoả điều kiện (tổng, tích, hiệu, ghép số, so sánh, ít nhất một…) tìm n(E) → P(E)",
     "hai xúc xắc, hai túi thẻ, đồng xu + thẻ/xúc xắc, quay đĩa hai lần, hai bạn chọn ngày/quán, sinh hai con, lai gene, tung đồng xu 2 lần"),
    # --- N04 ---
    ("VIII-10", "N04", "D35", "P1", "TH",
     "Mô tả không gian mẫu và tính xác suất khi lấy ĐỒNG THỜI 2 vật (tập con không phân biệt thứ tự)",
     "gán kí hiệu phân biệt từng vật → liệt kê các cặp {A; B} không phân biệt thứ tự → n(Ω) → lọc cặp thoả biến cố → P(E)",
     "lấy đồng thời / cùng một lúc / chọn ngẫu nhiên 2 vật (bi, thẻ, hoa, bạn) từ một hộp/nhóm"),
    ("VIII-11", "N04", "D35", "P1", "TH",
     "Mô tả không gian mẫu và tính xác suất bài toán xếp thứ tự / hoán vị 3–4 đối tượng",
     "liệt kê các thứ tự theo sơ đồ cây hoặc chia trường hợp phần tử đầu → n(Ω) → lọc thứ tự thoả biến cố → P(E)",
     "xếp ngẫu nhiên 3–4 bạn ngồi hàng ghế, thứ tự giải 3 bài, xếp hàng thanh toán, lấy lần lượt hết 3 viên bi"),
    ("VIII-12", "N04", "D35", "ngoài 9C", "VD",
     "Mô tả không gian mẫu và tính xác suất phép thử lấy lần lượt KHÔNG hoàn lại (cặp có thứ tự, a ≠ b)",
     "lập bảng gạch bỏ đường chéo chính (hoặc sơ đồ cây giảm nhánh) → n(Ω) = n(n − 1) → lọc cặp (a; b) thoả biến cố → P(E)",
     "lấy lần lượt từng thẻ/bi/phiếu, viên đầu không trả lại vào hộp (hoặc hai người lần lượt rút từ cùng một hộp)"),
    # --- N05 ---
    ("VIII-13", "N05", "D35", "P1", "VD",
     "Bài toán ngược: biết xác suất (hoặc tỉ lệ xác suất), lập phương trình tìm số phần tử / số vật",
     "đặt ẩn x là số vật chưa biết (hoặc tổng m) → biểu diễn n(Ω), n(E) theo x → lập phương trình n(E)/n(Ω) = p (hoặc P(A) = k·P(B)) → giải, đối chiếu điều kiện",
     "biết xác suất (0,18; 0,4; 0,6) hoặc biết P(đỏ) = 2·P(xanh), tìm tổng số thẻ hoặc số bi mỗi màu"),
    ("VIII-14", "N05", "D35", "ngoài 9C", "VD",
     "Phép thử nhiều hơn hai hành động / quy tắc nhân / bài toán đếm tổ hợp–hình học nâng cao",
     "liệt kê sơ đồ cây ≥ 3 tầng (tung đồng xu 3 lần) hoặc phân tích quy tắc nhân / chẵn lẻ / bất đẳng thức tam giác / điểm nguyên Oxy",
     "tung đồng xu 3 lần, rút từ 3 hộp thẻ, vé 4 chữ số, chọn 3 đoạn thẳng lập tam giác, điểm nguyên trong HCN Oxy, bài toán chia dư nâng cao"),
    ("VIII-15", "N05", "D36", "ngoài 9C", "TH",
     "Xác suất thực nghiệm và ước lượng từ số liệu thực nghiệm (Toán 8)",
     "tính tần số tương đối thực nghiệm k/N → ước lượng xác suất hoặc số đối tượng x ≈ (k/N)·M",
     "lặp lại thử nghiệm N lần thấy k lần xảy ra, tính xác suất thực nghiệm hoặc ước lượng số bi (lưu ý: hỏi số lần khi lặp N lần từ xác suất lý thuyết vẫn là VIII-06)"),
    ("VIII-16", "N05", "D35", "ngoài 9C", "TH",
     "So sánh khả năng xảy ra của các biến cố",
     "tính xác suất (hoặc đếm kết quả thuận lợi cùng Ω) của từng biến cố → so sánh hai phân số → kết luận",
     "biến cố nào có khả năng xảy ra cao hơn; so sánh khả năng xảy ra của các biến cố"),
]

# (mã dạng, tên dạng, phiếu 9C, [kỹ thuật])
DANG_GOP = [
    ("C8-01", "Nhận biết phép thử ngẫu nhiên, tính đồng khả năng, biến cố xảy ra hay không", "P1", ["VIII-01"]),
    ("C8-02", "Mô tả không gian mẫu Ω, đếm n(Ω) và kết quả thuận lợi (một hành động)", "P1",
     ["VIII-02", "VIII-03", "VIII-04"]),
    ("C8-03", "Tính xác suất một hành động — tập nền cho sẵn (khuôn Câu I.2 đề Sở)", "P1", ["VIII-06"]),
    ("C8-04", "Tính xác suất một hành động khi tự liệt kê không gian mẫu từ điều kiện số", "P1", ["VIII-07"]),
    ("C8-05", "Tính xác suất chọn một đối tượng từ bảng thống kê, biểu đồ hoặc tỉ lệ phần trăm", "P1", ["VIII-08"]),
    ("C8-06", "Phép thử hai hành động độc lập / có hoàn lại (bảng hai chiều, sơ đồ cây): mô tả Ω và tính xác suất", "P1",
     ["VIII-05", "VIII-09"]),
    ("C8-07", "Lấy đồng thời 2 vật (tập con không phân biệt thứ tự)", "P1", ["VIII-10"]),
    ("C8-08", "Xếp thứ tự / hoán vị 3–4 đối tượng", "P1", ["VIII-11"]),
    ("C8-09", "Bài toán ngược: biết xác suất (hoặc tỉ lệ xác suất), tìm số phần tử / số vật", "P1", ["VIII-13"]),
    ("C8-10", "Phép thử lấy lần lượt không hoàn lại (Thầy cắt ở 9C)", "ngoài 9C", ["VIII-12"]),
    ("C8-11", "Phép thử ≥ 3 hành động / quy tắc nhân / bài toán đếm nâng cao", "ngoài 9C", ["VIII-14"]),
    ("C8-12", "Xác suất thực nghiệm và ước lượng (Toán 8)", "ngoài 9C", ["VIII-15"]),
    ("C8-13", "So sánh khả năng xảy ra của các biến cố", "ngoài 9C", ["VIII-16"]),
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
    assert sorted(ve) == sorted(mas), set(mas) ^ set(ve)
    phieu_dang = {g[0]: g[2] for g in DANG_GOP}
    for d in out:
        d["dang"] = ve[d["ma"]]
        assert (d["phieu_9c"] == "ngoài 9C") == (phieu_dang[d["dang"]] == "ngoài 9C"), d["ma"]
    return out


def main():
    dm = danh_muc()
    khung = json.loads(KHUNG.read_text(encoding="utf-8"))
    khung["danh_muc_dang"] = {
        "_mo_ta": "Phân dạng theo PHƯƠNG PHÁP (luật Thầy 16/11/2026); mỗi ý một mã; sinh bởi scripts/danh_muc_dang_ch8_9.py",
        "nhom": NHOM, "dang": dm,
        "dang_gop": [{"ma": m, "ten": t, "phieu_9c": p, "ky_thuat": k} for m, t, p, k in DANG_GOP],
    }
    print(f"{len(dm)} kỹ thuật / {len(DANG_GOP)} dạng ({sum(g[2] != 'ngoài 9C' for g in DANG_GOP)} dạng P1) / {len(NHOM)} nhóm")
    if "--ghi" in sys.argv:
        KHUNG.write_text(json.dumps(khung, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Đã ghi", KHUNG.relative_to(REPO))


if __name__ == "__main__":
    main()
