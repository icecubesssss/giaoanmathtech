import json

data = {
  "slug": "thuyet-minh-tong-hop-chuong-2",
  "title": "Chương II (SGK KNTT): Phương trình \\& bất phương trình bậc nhất một ẩn — kế hoạch 4 buổi (12 tiết)",
  "grade": "lop-9",
  "subject": "dai-so",
  "tier": "C",
  "tuan": "09-12",
  "lythuyet": [
    "Tuân thủ ĐÚNG thứ tự chương trình SGK KNTT (12 tiết): Bài 4 (PT quy về bậc nhất) $\\rightarrow$ Bài 5 (Bất đẳng thức) $\\rightarrow$ Bài 6 (Bất phương trình) $\\rightarrow$ Luyện tập chung.",
    "Chiến lược tầng C: Tăng cường chẻ nhỏ các bước ở mức độ Nhận biết (NB). Giảm số lượng câu hỏi lặp lại ở mỗi dạng để tránh nhàm chán và dư thừa thời gian.",
    "Tuyệt đối KHÔNG đưa dạng 'biểu diễn nghiệm trên trục số' vào vì không phù hợp với định hướng thi và yêu cầu.",
    "Kết nối kiến thức (theo tinh thần SGV Toán 9 KNTT): Các dạng NB là bước chuẩn bị trực tiếp (viên gạch) để lắp ráp thành bài toán Thông hiểu (TH) và Vận dụng (VD). Bài toán VD phải là sự tổng hợp tự nhiên của các kĩ năng NB và TH trước đó."
  ],
  "vidu": [
    "Ví dụ mồi kết nối NB-TH: Giải hai BPT song song $2x-6 > 0$ và $-2x-4 > 0$ để làm nổi bật duy nhất bước đổi chiều (kết nối từ NB tính chất sang TH giải BPT).",
    "Ví dụ thực tế: Bài toán mua sắm với ngân sách giới hạn để học sinh tự luận ra từ khóa 'tối đa' tương ứng với dấu $\\le$.",
    "Ghép kĩ năng: Từ bài toán tìm ĐKXĐ (NB) và Quy đồng (NB), ghép lại thành bước đầu của Giải PT chứa ẩn ở mẫu (TH)."
  ],
  "dang_vd": [
    "Giải phương trình chứa ẩn ở mẫu có mẫu thức chung phức tạp hoặc cần đổi dấu.",
    "Chứng minh bất đẳng thức đơn giản dựa vào tính chất cộng/nhân.",
    "Toán thực tế lựa chọn phương án tối ưu (ví dụ: so sánh hai gói cước) bằng cách lập BPT."
  ],
  "loisai": [
    "Quên ĐKXĐ khi giải phương trình chứa ẩn ở mẫu.",
    "Quên đổi chiều bất phương trình khi nhân/chia với số âm.",
    "Lỗi dấu khi phá ngoặc hoặc chuyển vế.",
    "Toán thực tế: Thiếu điều kiện cho ẩn, quên làm tròn đúng yêu cầu hoặc quên đơn vị."
  ],
  "kienthuc_nb": [
    "Nhận diện phương trình tích và phương trình chứa ẩn ở mẫu.",
    "Nhận biết các kí hiệu bất đẳng thức $>, <, \\ge, \\le$.",
    "Hiểu tính chất cộng cùng một số vào hai vế của BĐT.",
    "Hiểu tính chất nhân hai vế với số dương (giữ chiều) và số âm (đổi chiều)."
  ],
  "phieu": [
    {
      "code": "A",
      "title": "Buổi 1 (Tuần 9): Phương trình quy về phương trình bậc nhất một ẩn (Bài 4)",
      "rows": [
        {
          "dang": "Nhận diện phương trình tích và phương trình chứa ẩn ở mẫu (NB mồi)",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Giải phương trình tích dạng cơ bản (đã phân tích sẵn thành nhân tử)",
          "band": "NB", "lythuyet": 0, "vidu": 3, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Kĩ năng phụ: Đặt nhân tử chung / HĐT để đưa đa thức về dạng tích",
          "band": "NB", "lythuyet": 1, "vidu": 4, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Tìm ĐKXĐ của phương trình chứa ẩn ở mẫu và quy đồng",
          "band": "NB", "lythuyet": 1, "vidu": 4, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Giải phương trình đưa về dạng tích (Kết nối kĩ năng NB thành TH)",
          "band": "TH", "lythuyet": 1, "vidu": 1, "onclass": 4, "btvn": 4,
          "source_refs": ["gk1-bat-trang-2a"], "decompose": "none"
        },
        {
          "dang": "Giải phương trình chứa ẩn ở mẫu cơ bản (Ghép ĐKXĐ và quy đồng thành TH)",
          "band": "TH", "lythuyet": 1, "vidu": 1, "onclass": 4, "btvn": 4,
          "source_refs": ["gk1-co-nhue-2-1a"], "decompose": "none"
        },
        {
          "dang": "Giải phương trình chứa ẩn ở mẫu phức tạp hơn (Mở rộng từ TH)",
          "band": "VD", "lythuyet": 0, "vidu": 1, "onclass": 2, "btvn": 2,
          "source_refs": [], "decompose": "vd"
        }
      ]
    },
    {
      "code": "B",
      "title": "Buổi 2 (Tuần 10): Bất đẳng thức và tính chất (Bài 5)",
      "rows": [
        {
          "dang": "Nhận biết các kí hiệu $>, <, \\ge, \\le$ và kiểm tra tính đúng sai của BĐT cụ thể",
          "band": "NB", "lythuyet": 1, "vidu": 2, "onclass": 6, "btvn": 6,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Viết bất đẳng thức mô tả tình huống thực tế (tốc độ tối đa, cân nặng tối thiểu)",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 6, "btvn": 6,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Tính chất cộng cùng một số vào hai vế của BĐT (giữ nguyên chiều)",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 6, "btvn": 6,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Tính chất nhân hai vế với số DƯƠNG (giữ nguyên chiều)",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 7, "btvn": 7,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Tính chất nhân hai vế với số ÂM (ĐỔI CHIỀU BĐT)",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 7, "btvn": 7,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Ghép tính chất nhân và cộng: So sánh biểu thức hỗn hợp (Kết nối NB thành TH)",
          "band": "TH", "lythuyet": 1, "vidu": 2, "onclass": 8, "btvn": 8,
          "source_refs": ["gk1-nbk-3-1"], "decompose": "none"
        },
        {
          "dang": "Chứng minh bất đẳng thức đơn giản bằng cách dùng phối hợp các tính chất",
          "band": "VD", "lythuyet": 0, "vidu": 1, "onclass": 2, "btvn": 2,
          "source_refs": [], "decompose": "vd"
        }
      ]
    },
    {
      "code": "C",
      "title": "Buổi 3 (Tuần 11): Bất phương trình bậc nhất một ẩn (Bài 6)",
      "rows": [
        {
          "dang": "Nhận diện BPT bậc nhất một ẩn; kiểm tra $x=a$ có là nghiệm không",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Giải BPT bằng quy tắc chuyển vế (áp dụng tính chất cộng)",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Giải BPT bằng quy tắc nhân với số DƯƠNG (giữ nguyên chiều)",
          "band": "NB", "lythuyet": 1, "vidu": 4, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Giải BPT bằng quy tắc nhân với số ÂM (đổi chiều BĐT)",
          "band": "NB", "lythuyet": 1, "vidu": 4, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Giải BPT bậc nhất $ax + b > 0$ trọn vẹn (Kết nối chuyển vế và nhân)",
          "band": "TH", "lythuyet": 1, "vidu": 1, "onclass": 4, "btvn": 4,
          "source_refs": ["gk1-bat-trang-2c"], "decompose": "none"
        },
        {
          "dang": "Giải BPT chứa ngoặc đơn giản (Nhân phá ngoặc rồi đưa về dạng TH chuẩn)",
          "band": "TH", "lythuyet": 1, "vidu": 1, "onclass": 4, "btvn": 4,
          "source_refs": ["ck1-tan-trieu-12"], "decompose": "none"
        },
        {
          "dang": "BPT thu gọn về dạng đặc biệt $0x > c$ (bẫy vô nghiệm hoặc đúng với mọi x)",
          "band": "VD", "lythuyet": 0, "vidu": 1, "onclass": 2, "btvn": 2,
          "source_refs": [], "decompose": "vd"
        }
      ]
    },
    {
      "code": "D",
      "title": "Buổi 4 (Tuần 12): Giải toán lập PT/BPT thực tế \\& Luyện tập chung",
      "rows": [
        {
          "dang": "Chuyển ngữ thực tế: Chọn ẩn và đặt điều kiện cho ẩn từ đề bài",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Dịch từ khóa 'ít nhất/tối đa' sang dấu BPT tương ứng",
          "band": "NB", "lythuyet": 1, "vidu": 3, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Lập bảng phân tích và biểu diễn đại lượng chưa biết",
          "band": "NB", "lythuyet": 1, "vidu": 4, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Viết phương trình/bất phương trình từ các đại lượng đã biểu diễn",
          "band": "NB", "lythuyet": 0, "vidu": 4, "onclass": 8, "btvn": 8,
          "source_refs": [], "decompose": "none"
        },
        {
          "dang": "Giải toán thực tế bằng cách lập PT (Kết nối NB thành TH)",
          "band": "TH", "lythuyet": 1, "vidu": 1, "onclass": 4, "btvn": 4,
          "source_refs": ["gk1-bat-trang-3-2"], "decompose": "none"
        },
        {
          "dang": "Giải toán thực tế bằng cách lập BPT (Kết nối NB thành TH)",
          "band": "TH", "lythuyet": 1, "vidu": 1, "onclass": 4, "btvn": 4,
          "source_refs": ["gk1-co-nhue-2-2-2"], "decompose": "none"
        },
        {
          "dang": "Toán thực tế lựa chọn phương án tối ưu: so sánh hai gói cước bằng BPT",
          "band": "VD", "lythuyet": 0, "vidu": 1, "onclass": 2, "btvn": 2,
          "source_refs": ["ck1-cau-dien-5"], "decompose": "vd"
        }
      ]
    }
  ]
}

with open("/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/chuong-2-bdt-bpt/thuyet-minh-tong-hop-chuong-2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

