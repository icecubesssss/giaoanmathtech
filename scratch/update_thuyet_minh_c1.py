import json
import os

filepath = "/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/chuong-1-he-pt/thuyet-minh-tong-hop-chuong-1.json"

with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. Cập nhật các thông tin tổng hợp ở trang đầu tiên
data["title"] = "Chương I (SGK KNTT): Phương trình \\& hệ hai phương trình bậc nhất hai ẩn — Kế hoạch 4 buổi (12 tiết)"
data["lythuyet"] = [
    "Học sinh lớp C nắm chắc lý thuyết nền tảng: khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn, cách biểu diễn nghiệm bằng đường thẳng và kiểm tra cặp nghiệm.",
    "Thành thạo hai phương pháp giải hệ phương trình cơ bản: phương pháp thế và phương pháp cộng đại số (cân bằng hệ số).",
    "Rèn luyện nhuần nhuyễn quy trình 3 bước giải bài toán bằng cách lập hệ hai phương trình bậc nhất hai ẩn, đặc biệt là bước phân tích đại lượng.",
    "Hạn chế các bài toán hệ phương trình chứa tham số m phức tạp hoặc hệ đối xứng/đẳng cấp khó, tập trung vào kỹ năng tính toán thực hành cơ bản để chuẩn bị thi Giữa kì 1."
]
data["vidu"] = [
    "Ví dụ mẫu: Kiểm tra cặp số có là nghiệm của hệ, rút ẩn thế ẩn cơ bản, nhân hệ số thích hợp để thực hiện phép cộng đại số.",
    "Ví dụ giải hệ phương trình đại số: Sử dụng phương pháp thế và cộng đại số cho các hệ từ cơ bản đến có chứa dấu ngoặc.",
    "Ví dụ thực tế mua bán: Đặt ẩn là số lượng/giá tiền của hai đối tượng thực tế (như bút, vở) để lập hệ phương trình.",
    "Ví dụ bài toán chuyển động hoặc năng suất: Chia nhỏ bước hướng dẫn thiết lập bảng đại lượng và lập hệ phương trình."
]
data["dang_vd"] = [
    "Giải hệ phương trình bậc nhất hai ẩn có chứa dấu ngoặc hoặc quy đồng mẫu số đơn giản.",
    "Giải bài toán thực tế chuyển động hoặc năng suất làm chung - làm riêng bằng cách lập hệ hai phương trình bậc nhất hai ẩn (được chia nhỏ bước)."
]
data["loisai"] = [
    "Nhầm lẫn khi xác định nghiệm của phương trình bậc nhất hai ẩn (vô số nghiệm) với nghiệm của hệ (cặp nghiệm duy nhất).",
    "Sai dấu khi thực hiện phép thế ẩn hoặc cộng/trừ đại số các vế của hệ phương trình.",
    "Lập hệ phương trình thực tế quên đặt điều kiện cho các ẩn (số nguyên dương, vận tốc riêng lớn hơn vận tốc dòng nước).",
    "Sai lầm khi đổi đơn vị thời gian trong bài toán chuyển động (ví dụ đổi 15 phút thành 0,15 giờ thay vì 1/4 giờ)."
]
data["kienthuc_nb"] = [
    "Nhận biết các hệ số a, b, c của phương trình bậc nhất hai ẩn, kiểm tra cặp nghiệm của phương trình/hệ phương trình.",
    "Biết cách rút ẩn và thế ẩn cơ bản, nhân vế với vế hoặc cộng/trừ đại số hai phương trình.",
    "Biết cách chọn ẩn, đặt điều kiện thực tế và biểu diễn mối quan hệ đơn giản giữa hai đại lượng."
]

# 2. Xử lý danh sách phiếu (phieu)
old_phieu = data["phieu"]

# Dịch chuyển và đổi tên các phiếu cũ:
# Buổi 2 (Bài 1) -> Buổi 1 (Tuần 4)
phieu_1 = old_phieu[1]
phieu_1["code"] = "A"
phieu_1["title"] = "Buổi 1 (Tuần 4): Phương trình bậc nhất hai ẩn. Hệ hai phương trình bậc nhất hai ẩn (Bài 1)"

# Buổi 3 (Bài 2) -> Buổi 2 (Tuần 5)
phieu_2 = old_phieu[2]
phieu_2["code"] = "B"
phieu_2["title"] = "Buổi 2 (Tuần 5): Giải hệ hai phương trình bậc nhất hai ẩn (Bài 2)"

# Buổi 4 (Bài 3) -> Buổi 3 (Tuần 6)
phieu_3 = old_phieu[3]
phieu_3["code"] = "C"
phieu_3["title"] = "Buổi 3 (Tuần 6): Giải bài toán bằng cách lập hệ phương trình (Bài 3)"

# Buổi 4 (Tuần 7) mới: Ôn tập & Luyện tập chung
phieu_4 = {
    "code": "D",
    "title": "Buổi 4 (Tuần 7): Ôn tập \\& Luyện tập chung Chương I",
    "rows": [
        {
            "dang": "Xác định các hệ số a, b, c của phương trình bậc nhất hai ẩn",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Kiểm tra cặp số $(x_0; y_0)$ có là nghiệm của hệ phương trình",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Biểu diễn ẩn này theo ẩn kia từ phương trình bậc nhất hai ẩn",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Thực hiện phép thế ẩn đưa hệ về phương trình bậc nhất một ẩn",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Cộng hoặc trừ đại số vế theo vế hai phương trình của hệ",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Nhân hệ số thích hợp vào hai vế của phương trình trong hệ",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Biểu diễn mối quan hệ tổng/hiệu số lượng đối tượng thực tế",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Biểu diễn số tiền mua hàng theo đơn giá và số lượng đối tượng",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Giải hệ hai phương trình bậc nhất hai ẩn bằng phương pháp thế",
            "band": "TH",
            "lythuyet": 1,
            "vidu": 1,
            "onclass": 2,
            "btvn": 2,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Giải hệ phương trình bậc nhất hai ẩn bằng phương pháp cộng đại số",
            "band": "TH",
            "lythuyet": 1,
            "vidu": 2,
            "onclass": 2,
            "btvn": 2,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Lập và giải hệ phương trình cho bài toán mua sắm thực tế",
            "band": "TH",
            "lythuyet": 1,
            "vidu": 1,
            "onclass": 2,
            "btvn": 2,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Lập và giải hệ phương trình cho bài toán hình học tính kích thước",
            "band": "TH",
            "lythuyet": 1,
            "vidu": 1,
            "onclass": 2,
            "btvn": 2,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Giải bài toán thực tế chuyển động bằng cách lập hệ phương trình",
            "band": "VD",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 1,
            "btvn": 1,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Giải bài toán thực tế năng suất bằng cách lập hệ phương trình",
            "band": "VD",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 1,
            "btvn": 1,
            "source_refs": [],
            "decompose": "none"
        }
    ]
}

data["phieu"] = [phieu_1, phieu_2, phieu_3, phieu_4]

# Ghi lại file JSON
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("SUCCESS: Cập nhật thành công thuyet-minh-tong-hop-chuong-1.json")
