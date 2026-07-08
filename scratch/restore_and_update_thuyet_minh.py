import json

filepath = "/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/chuong-1-he-pt/thuyet-minh-tong-hop-chuong-1.json"

with open(filepath, "r", encoding="utf-8") as f:
    current_data = json.load(f)

# Lấy các phiếu còn đúng trên đĩa
# phieu[0] hiện tại chính là Bài 1 (cũ là index 1)
phieu_1 = current_data["phieu"][0]
phieu_1["code"] = "A"
phieu_1["title"] = "Buổi 1 (Tuần 4): Phương trình bậc nhất hai ẩn. Hệ hai phương trình bậc nhất hai ẩn (Bài 1)"

# phieu[1] hiện tại chính là Bài 2 (cũ là index 2)
phieu_2 = current_data["phieu"][1]
phieu_2["code"] = "B"
phieu_2["title"] = "Buổi 2 (Tuần 5): Giải hệ hai phương trình bậc nhất hai ẩn (Bài 2)"

# Reconstruct Bài 3 (cũ là index 3) từ transcript hội thoại
phieu_3 = {
  "code": "C",
  "title": "Buổi 3 (Tuần 6): Giải bài toán bằng cách lập hệ phương trình (Bài 3)",
  "rows": [
    {
      "dang": "Chọn hai ẩn số cho đại lượng thực tế và đặt điều kiện",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 2,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn tổng hoặc hiệu số lượng đối tượng thực tế qua hai ẩn",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 2,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn tổng số tiền qua đơn giá và hai ẩn số tương ứng",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn thời gian chuyển động theo quãng đường và vận tốc",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn vận tốc chuyển động xuôi dòng của vật thể",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn vận tốc chuyển động ngược dòng của vật thể",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn số lượng đối tượng phân chia đều theo các nhóm/xe",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn số tiền được giảm giá theo phần trăm ưu đãi",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn chu vi hình học theo kích thước của ẩn",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn diện tích hình học theo kích thước của ẩn",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Thiết lập phương trình thứ nhất từ mối liên hệ số lượng",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Thiết lập phương trình thứ hai từ mối liên hệ giá trị, chi phí",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Viết hệ phương trình hoàn chỉnh biểu diễn bài toán thực tế",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 1,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn chiều dài và rộng mới của hình chữ nhật sau tăng/giảm",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 1,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn số đối tượng thừa hoặc thiếu khi phân chia vào các nhóm",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 1,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Biểu diễn quãng đường chuyển động theo vận tốc và thời gian",
      "band": "NB",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 2,
      "btvn": 1,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Bài toán thực tế tìm hai số biết tổng hiệu hoặc tỉ số",
      "band": "TH",
      "lythuyet": 1,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Bài toán thực tế mua sắm (sticker, sách vở) tính số lượng, giá tiền",
      "band": "TH",
      "lythuyet": 1,
      "vidu": 1,
      "onclass": 2,
      "btvn": 1,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Bài toán thực tế hình chữ nhật khi thay đổi kích thước",
      "band": "TH",
      "lythuyet": 1,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [
        "ck1-dich-vong-III"
      ],
      "decompose": "none"
    },
    {
      "dang": "Bài toán thực tế chia tổ, chia xe vận chuyển hàng hóa",
      "band": "TH",
      "lythuyet": 1,
      "vidu": 1,
      "onclass": 2,
      "btvn": 2,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Bài toán thực tế chuyển động đường bộ (cùng hoặc ngược chiều)",
      "band": "VD",
      "lythuyet": 0,
      "vidu": 1,
      "onclass": 1,
      "btvn": 1,
      "source_refs": [],
      "decompose": "none"
    },
    {
      "dang": "Bài toán thực tế chuyển động xuôi dòng, ngược dòng trên nước",
      "band": "VD",
      "lythuyet": 0,
      "vidu": 0,
      "onclass": 1,
      "btvn": 1,
      "source_refs": [],
      "decompose": "none"
    }
  ]
}

# Buổi 4 (Tuần 7) ôn tập có vidu được điều chỉnh để khớp 44 phút (budget 45 phút)
phieu_4 = {
    "code": "D",
    "title": "Buổi 4 (Tuần 7): Ôn tập \\& Luyện tập chung Chương I",
    "rows": [
        {
            "dang": "Tìm điều kiện xác định (ĐKXĐ) của hệ phương trình chứa ẩn ở mẫu thức",
            "band": "NB",
            "lythuyet": 0,
            "vidu": 1,
            "onclass": 4,
            "btvn": 3,
            "source_refs": [],
            "decompose": "none"
        },
        {
            "dang": "Xác định ẩn phụ thích hợp để đưa hệ phương trình về dạng cơ bản",
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

current_data["phieu"] = [phieu_1, phieu_2, phieu_3, phieu_4]

# Ghi lại file JSON
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(current_data, f, ensure_ascii=False, indent=2)

print("SUCCESS: Đã khôi phục và cập nhật thuyet-minh-tong-hop-chuong-1.json thành công")
