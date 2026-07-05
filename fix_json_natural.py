import json
import re

file_path = "/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/chuong-2-bdt-bpt/thuyet-minh-tong-hop-chuong-2.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Update the top level sections
data["vidu"] = [
    "Ví dụ mồi: Cho học sinh giải song song hai BPT $2x-6 > 0$ và $-2x-4 > 0$ để tự nhận ra điểm khác biệt cốt lõi là bước đổi chiều.",
    "Ví dụ thực tế: Đưa bài toán mua sắm ngân sách giới hạn để học sinh tự suy luận từ khóa 'tối đa' tương đương với dấu $\\le$.",
    "Hướng dẫn ghép bước: Yêu cầu học sinh làm riêng biệt bước tìm ĐKXĐ và bước quy đồng trước, sau đó mới ráp chúng lại thành bước mở đầu để giải phương trình chứa ẩn ở mẫu."
]

data["dang_vd"] = [
    "Giải phương trình chứa ẩn ở mẫu cần quy đồng mẫu thức chung phức tạp hoặc phải đổi dấu.",
    "Chứng minh các bất đẳng thức cơ bản bằng cách phối hợp linh hoạt tính chất cộng và nhân.",
    "Giải các bài toán thực tế mang tính lựa chọn phương án tối ưu (ví dụ chọn gói cước tiết kiệm hơn) bằng cách lập BPT."
]

data["loisai"] = [
    "Quên đặt điều kiện xác định hoặc làm xong quên đối chiếu lại điều kiện.",
    "Không chịu đổi chiều bất phương trình khi nhân hay chia cả hai vế cho số âm.",
    "Nhầm dấu khi phá ngoặc hoặc khi chuyển vế.",
    "Làm toán thực tế hay quên đặt điều kiện cho ẩn, thiếu đơn vị hoặc làm tròn kết quả sai yêu cầu."
]

data["kienthuc_nb"] = [
    "Nhận diện được đâu là phương trình tích, đâu là phương trình chứa ẩn ở mẫu.",
    "Nhận biết và đọc đúng các kí hiệu bất đẳng thức $>, <, \\ge, \\le$.",
    "Nắm được quy tắc cộng cùng một số vào hai vế của bất đẳng thức.",
    "Nắm chắc quy tắc nhân hai vế: nhân số dương thì giữ nguyên chiều, nhân số âm bắt buộc phải đổi chiều."
]

# Manual replacements for 'dang' in phieu
replacements = {
    "Nhận diện phương trình tích và phương trình chứa ẩn ở mẫu (NB mồi)": "Mở đầu: Nhận diện phương trình tích và phương trình chứa ẩn ở mẫu",
    "Giải phương trình tích dạng cơ bản (đã phân tích sẵn thành nhân tử)": "Giải phương trình tích cơ bản dạng phân tích sẵn",
    "Kĩ năng phụ: Đặt nhân tử chung / HĐT để đưa đa thức về dạng tích": "Đặt nhân tử chung hoặc dùng hằng đẳng thức để đưa đa thức về dạng tích",
    "Tìm ĐKXĐ của phương trình chứa ẩn ở mẫu và quy đồng": "Tìm ĐKXĐ và quy đồng các phân thức",
    "Giải phương trình đưa về dạng tích (Kết nối kĩ năng NB thành TH)": "Giải phương trình bằng phương pháp đưa về phương trình tích",
    "Giải phương trình chứa ẩn ở mẫu cơ bản (Ghép ĐKXĐ và quy đồng thành TH)": "Giải phương trình chứa ẩn ở mẫu cơ bản",
    "Giải phương trình chứa ẩn ở mẫu phức tạp hơn (Mở rộng từ TH)": "Giải phương trình chứa ẩn ở mẫu nâng cao",
    "Nhận biết các kí hiệu $>, <, \\ge, \\le$ và kiểm tra tính đúng sai của BĐT cụ thể": "Nhận biết các kí hiệu $>, <, \\ge, \\le$ và kiểm tra tính đúng sai của BĐT",
    "Viết bất đẳng thức mô tả tình huống thực tế (tốc độ tối đa, cân nặng tối thiểu)": "Viết bất đẳng thức mô tả các tình huống thực tế cơ bản",
    "Tính chất cộng cùng một số vào hai vế của BĐT (giữ nguyên chiều)": "Thực hành tính chất cộng cùng một số vào hai vế của BĐT",
    "Tính chất nhân hai vế với số DƯƠNG (giữ nguyên chiều)": "Thực hành tính chất nhân hai vế của BĐT với số dương",
    "Tính chất nhân hai vế với số ÂM (ĐỔI CHIỀU BĐT)": "Thực hành tính chất nhân hai vế của BĐT với số âm",
    "Ghép tính chất nhân và cộng: So sánh biểu thức hỗn hợp (Kết nối NB thành TH)": "Sử dụng phối hợp tính chất nhân và cộng để so sánh biểu thức",
    "Chứng minh bất đẳng thức đơn giản bằng cách dùng phối hợp các tính chất": "Chứng minh bất đẳng thức đơn giản bằng cách phối hợp các tính chất",
    "Nhận diện BPT bậc nhất một ẩn; kiểm tra $x=a$ có là nghiệm không": "Nhận diện BPT bậc nhất một ẩn và kiểm tra nghiệm",
    "Giải BPT bằng quy tắc chuyển vế (áp dụng tính chất cộng)": "Sử dụng quy tắc chuyển vế để giải BPT",
    "Giải BPT bằng quy tắc nhân với số DƯƠNG (giữ nguyên chiều)": "Sử dụng quy tắc nhân số dương để giải BPT",
    "Giải BPT bằng quy tắc nhân với số ÂM (đổi chiều BĐT)": "Sử dụng quy tắc nhân số âm để giải BPT",
    "Giải BPT bậc nhất $ax + b > 0$ trọn vẹn (Kết nối chuyển vế và nhân)": "Giải hoàn chỉnh BPT bậc nhất một ẩn",
    "Giải BPT chứa ngoặc đơn giản (Nhân phá ngoặc rồi đưa về dạng TH chuẩn)": "Giải BPT bậc nhất có chứa dấu ngoặc",
    "BPT thu gọn về dạng đặc biệt $0x > c$ (bẫy vô nghiệm hoặc đúng với mọi x)": "Xử lý BPT thu về dạng đặc biệt vô nghiệm hoặc luôn đúng",
    "Chuyển ngữ thực tế: Chọn ẩn và đặt điều kiện cho ẩn từ đề bài": "Chọn ẩn số và đặt điều kiện cho ẩn từ đề bài toán thực tế",
    "Dịch từ khóa 'ít nhất/tối đa' sang dấu BPT tương ứng": "Chuyển đổi các từ khóa thực tế sang dấu BPT tương ứng",
    "Lập bảng phân tích và biểu diễn đại lượng chưa biết": "Lập bảng phân tích và biểu diễn các đại lượng chưa biết",
    "Viết phương trình/bất phương trình từ các đại lượng đã biểu diễn": "Thiết lập phương trình hoặc bất phương trình từ bảng phân tích",
    "Giải toán thực tế bằng cách lập PT (Kết nối NB thành TH)": "Giải trọn vẹn bài toán thực tế bằng phương trình",
    "Giải toán thực tế bằng cách lập BPT (Kết nối NB thành TH)": "Giải trọn vẹn bài toán thực tế bằng bất phương trình",
    "Toán thực tế lựa chọn phương án tối ưu: so sánh hai gói cước bằng BPT": "Giải bài toán thực tế lựa chọn phương án tối ưu"
}

for p in data["phieu"]:
    for row in p["rows"]:
        if row["dang"] in replacements:
            row["dang"] = replacements[row["dang"]]

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done")
