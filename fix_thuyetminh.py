import re

path = '/Users/admin/Documents/thaitd/Code/giaoanMathtech/scripts/build_thuyetminh_tuan10_11.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

new_phieuB = """phieuB = ([
    (r"NHẬN BIẾT — NB ($\\bigstar$)", "stage1", [
        (r"Từ khoá $\\to$ dấu; dịch câu thành BPT (Bài 1 / BTVN 9, 10)", "1", "8′", "1", "10′", "6", "9′", "14", "18′"),
        (r"Viết biểu thức theo ẩn $x$ (Bài 2 / BTVN 11)", "—", "—", "—", "—", "10", "15′", "8", "10′"),
        (r"Xác định chiều làm tròn (Bài 3 / BTVN 12)", "—", "—", "—", "—", "6", "9′", "6", "8′"),
        (r"Ý nhận biết trong toán thực tế (Bài 5, 6, 7 / BTVN 15)", "—", "—", "—", "—", "6", "9′", "1", "1′"),
    ], ("1", "8′", "1", "10′", "28", "42′", "29", "37′")),
    (r"THÔNG HIỂU — TH ($\\bigstar\\bigstar$)", "stage2", [
        (r"Lập BPT từ tình huống — chưa giải (Bài 4 / BTVN 13)", "1", "7′", "1", "10′", "3", "18′", "4", "21′"),
        (r"Ý thông hiểu toán thực tế chẻ câu (Bài 5, 6, 7, 8 / BTVN 14, 15, 16)", "—", "—", "1", "10′", "8", "48′", "3", "16′"),
    ], ("1", "7′", "2", "20′", "11", "66′", "7", "37′")),
    (r"VẬN DỤNG — VD ($\\bigstar\\bigstar\\bigstar$)", "stage3", [
        (r"Kết luận \\& giải BPT trong toán thực tế (Bài 5, 6, 7, 8 / BTVN 14, 16)", "—", "—", "—", "—", "4", "48′", "2", "21′"),
    ], ("—", "—", "—", "—", "4", "48′", "2", "21′")),
], ("2", "15′", "3", "30′", "43", "156′", "38", "95′"))"""

# Replace phieuB
text = re.sub(r'phieuB = \(\[.*?\]\, \("2"\, "15′"\, "3"\, "30′"\, "37"\, "113′"\, "38"\, "94′"\)\)', new_phieuB, text, flags=re.DOTALL)

# Adjust 'canB' time balancing text
text = text.replace(r"Luyện tập 112′ (khung 120′, còn $\approx$8′ GV chữa bài) $=$ \textbf{$\approx$180′} tại lớp", 
                    r"Luyện tập 156′ (tăng cường 2 bài VD) $=$ \textbf{216′} tại lớp (sẽ đẩy bớt 1 bài dễ sang làm mẫu để khớp giờ)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

