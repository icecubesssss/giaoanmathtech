#!/usr/bin/env python3
"""Danh mục dạng ĐÓNG chương X Hình học 9 (Một số hình khối trong thực tiễn) — phân dạng theo PHƯƠNG PHÁP.

Cùng luật với chương VI, VII, VIII (Thầy 16/11/2026): một dạng = một phương pháp (một chuỗi bước);
bối cảnh, số liệu, hình thức = biến thể. Hai cấp: KỸ THUẬT (X-xx) ⊂ DẠNG (C10-xx).
Kỹ thuật tách theo KHỐI (trụ / nón / cầu) để thống kê được tỉ lệ từng khối trong đề thật;
dạng gộp lại theo phương pháp (khác công thức cần nhớ = cùng dạng).
Chương X 9C (Thầy chốt 19/11/2026): làm lại theo quy trình mới, GIỮ 2 buổi —
P1 = t32 gộp trụ + nón + cầu (90′), P2 = t33 luyện tập 45′ + KT chương X 45′.

Chạy:  .venv/bin/python scripts/danh_muc_dang_ch10_9.py [--ghi]
       ghi khoá `danh_muc_dang` vào config/khung-phan-dang/lop-9-hinh-hoc-chuong-10.json
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-hinh-hoc-chuong-10.json"

NHOM = {
    "N01": "Nhận biết yếu tố và áp công thức trực tiếp (Bài 31, Bài 32)",
    "N02": "Tính qua bước trung gian trên một khối (Pythagore, tính ngược, khai triển)",
    "N03": "Bài toán thực tế một khối (khuôn Câu IV.1 đề Sở)",
    "N04": "Thể tích nước: vật thả chìm, chiều cao theo phần nước",
    "N05": "Vật thể ghép và phần còn lại (cộng / trừ khối)",
    "N06": "Nâng cao: đồng dạng hình nón, khối nội/ngoại tiếp, cực trị",
}

# (mã, nhóm, cấp 1 ở tab "Danh mục dạng chuẩn", phiếu 9C, mức gốc, tên, cách làm, dấu hiệu)
DANG = [
    # --- N01 ---
    ("X-01", "N01", "D40/D41/D42", "P1", "NB",
     "Nhận biết yếu tố của hình trụ, hình nón, hình cầu (bán kính đáy, chiều cao, đường sinh, đỉnh, tâm, bán kính mặt cầu)",
     "đọc hình / mô tả → chỉ ra yếu tố được hỏi; với hình tạo bởi khi quay hình chữ nhật, tam giác vuông: cạnh nằm trên trục quay là chiều cao, cạnh vuông góc trục là bán kính đáy",
     "chỉ hỏi gọi tên / chỉ ra bán kính đáy, chiều cao, đường sinh, tâm, bán kính; quay hình chữ nhật/tam giác vuông quanh một cạnh rồi hỏi r, h (chưa tính diện tích, thể tích)"),
    ("X-02", "N01", "D40", "P1", "NB",
     "Áp công thức hình trụ trực tiếp: S_xq = 2πrh, S_đáy = πr², S_tp, V = πr²h (biết r hoặc đường kính d, biết h)",
     "đọc r, h (đề cho đường kính thì chia đôi) → thay vào công thức → tính, làm tròn theo yêu cầu",
     "cho sẵn r (hoặc d) và h của một hình trụ, hỏi diện tích xung quanh / toàn phần / thể tích; bảng điền S_xq, V"),
    ("X-03", "N01", "D41", "P1", "NB",
     "Áp công thức hình nón trực tiếp: S_xq = πrl (đã cho l), V = ⅓πr²h (đã cho h)",
     "đọc r và l (hoặc h) cho sẵn → thay vào công thức → tính",
     "cho sẵn đủ r, l hoặc r, h của hình nón, hỏi S_xq hoặc V không cần Pythagore"),
    ("X-04", "N01", "D42", "P1", "NB",
     "Áp công thức hình cầu trực tiếp: S = 4πR², V = ⁴⁄₃πR³ (biết R hoặc đường kính d)",
     "đọc R (đề cho đường kính thì chia đôi) → thay vào công thức → tính",
     "cho bán kính hoặc đường kính hình cầu / quả bóng / viên bi, hỏi diện tích mặt cầu hoặc thể tích (kể cả nhân số viên)"),
    # --- N02 ---
    ("X-05", "N02", "D41", "P1", "TH",
     "Hình nón cần định lí Pythagore liên hệ r, h, l rồi tính S_xq, S_tp hoặc V",
     "vẽ tam giác vuông (h, r, l) → l² = r² + h² tìm cạnh còn thiếu → thay công thức S_xq = πrl hoặc V = ⅓πr²h",
     "hình nón (kể cả tạo bởi quay tam giác vuông quanh cạnh góc vuông) biết r và h mà hỏi S_xq, hoặc biết r và l mà hỏi V"),
    ("X-06", "N02", "D40/D42", "P1", "TH",
     "Tính ngược: biết diện tích / thể tích / chu vi đường tròn lớn / diện tích mặt cắt qua tâm / quan hệ h = k·r → tìm r, h, R rồi tính tiếp",
     "viết công thức với ẩn r (hoặc h, R) → thay giá trị đã biết → giải phương trình (r², R³ hoặc bậc nhất) → tính đại lượng được hỏi",
     "biết V và h tìm r (hoặc diện tích đáy); biết S mặt cầu / V tìm R; biết chu vi đường tròn lớn; bảng điền ngược R, h; hình trụ có h = 2r biết V"),
    ("X-07", "N02", "D40/D41", "P1", "TH",
     "Hình khai triển: chu vi đáy = chiều dài hình chữ nhật (trụ) / độ dài cung hình quạt (nón)",
     "nhận ra mép tấm phẳng cuộn thành đường tròn đáy → 2πr = độ dài mép → tìm r → tính S hoặc V",
     "cuộn tấm tôn / tờ giấy hình chữ nhật thành hình trụ; cuộn hình quạt / nửa hình tròn thành hình nón; hoạt động dẫn tới công thức S_xq"),
    # --- N03 ---
    ("X-08", "N03", "D40", "P1", "TH",
     "Thực tế hình trụ — DIỆN TÍCH: chọn đúng phần bề mặt (S_xq, S_xq + 1 đáy, S_tp, nửa trụ, lăn n vòng) rồi tính chi phí / vật liệu",
     "xác định vật có mấy đáy / phần nào được sơn, may, lăn → chọn công thức đúng → tính → đổi đơn vị diện tích → nhân đơn giá, cộng % hao hụt",
     "trục lăn sơn, hộp chè, vỏ hộp sữa, thùng không nắp, nhà kính nửa hình trụ, cột sơn, chi phí làm vỏ"),
    ("X-09", "N03", "D40", "P1", "TH",
     "Thực tế hình trụ — THỂ TÍCH: tính V rồi đổi đơn vị (lít, ml, m³, khối lượng riêng) và trả lời câu hỏi thực tế",
     "đọc r, h (bẫy đường kính) → V = πr²h → đổi cm³ ↔ lít ↔ m³ (hoặc nhân khối lượng riêng) → nhân giá / phần trăm / số lượng",
     "bồn nước, bình nước, khúc gỗ, lon nước, thùng dầu, bể trụ: hỏi chứa bao nhiêu lít, nặng bao nhiêu kg, bao nhiêu tiền"),
    ("X-10", "N03", "D41", "P1", "TH",
     "Thực tế hình nón: diện tích xung quanh hoặc thể tích vật hình nón",
     "đọc r, h, l (bẫy đường kính; thiếu l thì Pythagore) → S_xq = πrl hoặc V = ⅓πr²h → đổi đơn vị, nhân số lượng / giá",
     "nón lá, mũ sinh nhật, kem ốc quế, đống cát, đồng hồ cát, mái nhà hình nón, phễu, đài phun nước hình nón"),
    ("X-11", "N03", "D42", "P1", "TH",
     "Thực tế hình cầu: diện tích mặt cầu hoặc thể tích vật hình cầu / nửa hình cầu",
     "đọc R (bẫy đường kính) → S = 4πR² hoặc V = ⁴⁄₃πR³ (nửa cầu chia đôi) → đổi đơn vị, nhân số lượng / phần trăm",
     "quả bóng, bể nước hình cầu, viên kem, Trái Đất, bình cầu ngập nửa, số miếng da khâu bóng"),
    ("X-12", "N03", "D40/D43", "P1", "TH",
     "Chia / so sánh thể tích giữa hai vật chứa: số cốc rót được, số lần đổ đầy, có tràn không, đúc lại thể tích không đổi",
     "tính thể tích hai vật (chú ý phần trăm đổ đầy) → chia hoặc so sánh → làm tròn XUỐNG khi hỏi số cốc đầy, làm tròn LÊN khi hỏi số lần / số xô cần dùng",
     "rót nước từ bình sang cốc / ly, đổ xô vào bể, so sánh hai lọ, đổ sang có bị tràn không, nấu chảy rồi đúc thành khối khác"),
    # --- N04 ---
    ("X-13", "N04", "D43", "P1", "TH",
     "Thả vật chìm vào bình hình trụ: thể tích vật = thể tích nước dâng thêm / tràn ra",
     "V vật = S_đáy bình × độ dâng (hoặc = V nước tràn) → suy ra mực nước dâng, thể tích vật, hoặc bán kính bi (giải R³)",
     "thả bi / quả cầu / hòn đá / quả trứng vào cốc, ly, bình hình trụ; nước dâng lên bao nhiêu; tìm bán kính viên bi; nước tràn ra"),
    ("X-14", "N04", "D40", "P2", "VD",
     "Chiều cao theo phần nước / lật ngược bình: V bình = V nước + V phần trống; mực nước còn lại sau khi tháo, dùng",
     "xác định phần nào là nước, phần nào trống theo từng tư thế → lập thể tích từng phần theo chiều cao mực nước → cộng / trừ → tìm đại lượng",
     "chai lật ngược, bồn tháo bớt nước, thể tích nước đã dùng, mực nước hiện tại khác chiều cao bình"),
    # --- N05 ---
    ("X-15", "N05", "D43", "P2", "TH",
     "Vật thể ghép: tách thành khối cơ bản rồi CỘNG thể tích / diện tích bề mặt lộ ra",
     "nhận ra các khối thành phần (trụ, nón, nửa cầu, vành khuyên) và kích thước chung → tính từng khối → cộng (bỏ mặt tiếp giáp khi tính diện tích)",
     "trụ + nón (quả dọi, thùng có nắp nón), trụ + nửa cầu (viên thuốc, đinh tán), nón + nửa cầu (kem ốc quế), mũ = S_xq nón + vành, quay tam giác quanh cạnh huyền ra hai nón chung đáy"),
    ("X-16", "N05", "D43", "P2", "TH",
     "Phần còn lại: TRỪ thể tích (hiệu hai khối, vỏ, ống, phần trống khi chứa khít các quả cầu)",
     "tính thể tích khối ngoài và khối bên trong (cùng đơn vị) → trừ; khi chứa khít: suy r = R, h = n·2R rồi trừ",
     "thể tích vật liệu làm cốc / ống / vỏ cầu, trụ khoét nón hoặc cầu, hộp chứa khít 3 quả bóng, nước còn lại sau khi đặt khối vào"),
    # --- N06 ---
    ("X-17", "N06", "D41", "ngoài 9C", "VD",
     "Tỉ số đồng dạng trong hình nón: mặt nước trong phễu / cốc nón, r tỉ lệ h, tỉ số thể tích bằng lập phương tỉ số chiều cao",
     "mặt nước cắt nón thành nón nhỏ đồng dạng → r'/r = h'/h (Thales) → V'/V = (h'/h)³ → suy đại lượng",
     "cốc / phễu hình nón chứa nước đến một phần chiều cao, lật ngược phễu, nước chảy giữa hai phễu, bi thả vào cốc hình nón"),
    ("X-18", "N06", "D43", "ngoài 9C", "VD",
     "Khối tròn xoay nội tiếp / ngoại tiếp đa diện hoặc đa giác, tính theo tham số a",
     "từ hình lập phương / chóp / tam giác đều / hình vuông suy bán kính, chiều cao theo a (đường chéo, bán kính đường tròn ngoại tiếp) → thay công thức → rút gọn hoặc lập tỉ số",
     "mặt cầu ngoại tiếp hình lập phương, hình cầu nội tiếp bể lập phương, hình nón nội tiếp lập phương, đáy nón ngoại tiếp tam giác đều / hình vuông, cầu trong nón"),
    ("X-19", "N06", "D43", "ngoài 9C", "VDC",
     "Nâng cao: cực trị, lập phương trình / hệ theo quan hệ kích thước, phần trụ nằm ngang có hình viên phân",
     "đặt ẩn kích thước → lập phương trình / hệ từ điều kiện (chu vi, diện tích, hiệu bán kính, tổng diện tích) hoặc bất đẳng thức Cô-si; hoặc tính diện tích viên phân (quạt trừ tam giác) rồi nhân chiều dài",
     "thể tích lớn nhất, diện tích toàn phần nhỏ nhất, hai hình cầu biết hiệu bán kính và hiệu thể tích, quay hình chữ nhật biết chu vi và diện tích, bồn dầu nằm ngang rút một phần"),
]

# (mã dạng, tên dạng, phiếu 9C, [kỹ thuật])
DANG_GOP = [
    ("C10-01", "Nhận biết yếu tố hình trụ, hình nón, hình cầu; hình khai triển", "P1", ["X-01", "X-07"]),
    ("C10-02", "Áp sáu công thức trực tiếp (trụ, nón, cầu) — bẫy đường kính", "P1", ["X-02", "X-03", "X-04"]),
    ("C10-03", "Hình nón cần định lí Pythagore tìm h hoặc l", "P1", ["X-05"]),
    ("C10-04", "Tính ngược: biết diện tích / thể tích / chu vi, tìm bán kính, chiều cao", "P1", ["X-06"]),
    ("C10-05", "Bài toán thực tế một khối: diện tích, thể tích, đổi đơn vị, chi phí (khuôn Câu IV.1)", "P1",
     ["X-08", "X-09", "X-10", "X-11"]),
    ("C10-06", "Chia / so sánh thể tích hai vật chứa — làm tròn lên / xuống", "P1", ["X-12"]),
    ("C10-07", "Thả vật chìm: thể tích vật = thể tích nước dâng / tràn", "P1", ["X-13"]),
    ("C10-08", "Chiều cao theo phần nước / lật ngược bình", "P2", ["X-14"]),
    ("C10-09", "Vật thể ghép và phần còn lại (cộng / trừ khối)", "P2", ["X-15", "X-16"]),
    ("C10-10", "Tỉ số đồng dạng trong hình nón (mặt nước trong phễu)", "ngoài 9C", ["X-17"]),
    ("C10-11", "Khối nội / ngoại tiếp đa diện, tính theo tham số", "ngoài 9C", ["X-18"]),
    ("C10-12", "Nâng cao: cực trị, lập phương trình theo kích thước, viên phân", "ngoài 9C", ["X-19"]),
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
        "_mo_ta": "Phân dạng theo PHƯƠNG PHÁP (luật Thầy 16/11/2026); mỗi ý một mã; sinh bởi scripts/danh_muc_dang_ch10_9.py",
        "nhom": NHOM, "dang": dm,
        "dang_gop": [{"ma": m, "ten": t, "phieu_9c": p, "ky_thuat": k} for m, t, p, k in DANG_GOP],
    }
    n9 = sum(g[2] != "ngoài 9C" for g in DANG_GOP)
    print(f"{len(dm)} kỹ thuật / {len(DANG_GOP)} dạng ({n9} dạng 9C) / {len(NHOM)} nhóm")
    if "--ghi" in sys.argv:
        KHUNG.write_text(json.dumps(khung, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Đã ghi", KHUNG.relative_to(REPO))


if __name__ == "__main__":
    main()
