"""Sửa thuyết minh chương VI 9C cho KHỚP 6 phiếu A–F đã sửa (12–13/11/2026).

Phiếu đã sửa xong trước, nên TM bám theo phiếu: mỗi dòng TM liệt kê đúng các bài
trong phiếu, số câu trên lớp / BTVN ĐẾM TỪ PHIẾU (cùng luật spec_gate), và ghi
`dang_id` vào từng bài để spec_gate soi được phiếu ↔ TM.

Đồng thời bỏ khỏi TM: tham số m, kí hiệu S và P, chữ "khuôn", điểm số rải trong
dang_vd/loisai, câu "Thầy chốt cắt" (luật không nhắc phần cắt).

Chạy:  .venv/bin/python scripts/sua_tm_chuong6_9c.py          # xem trước
       .venv/bin/python scripts/sua_tm_chuong6_9c.py --ghi    # ghi TM + phiếu
Idempotent: chạy lại cho cùng kết quả.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.schema.lesson_package import LessonPackage  # noqa: E402
from src.validators.spec_gate import _so_cau  # noqa: E402

D = Path("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai")
TM = D / "thuyet-minh.json"
PHIEU = {
    "A": "phieu-a-phuong-trinh-bac-hai-mot-an.json",
    "B": "phieu-b-phuong-trinh-chua-an-o-mau-quy-ve-bac-hai.json",
    "C": "phieu-c-dinh-li-viete-va-ung-dung.json",
    "D": "phieu-d-tinh-gia-tri-bieu-thuc-chua-hai-nghiem.json",
    "E": "phieu-e-giai-bai-toan-bang-cach-lap-phuong-trinh.json",
    "F": "phieu-f-luyen-tap-chung-va-bai-tap-cuoi-chuong-vi.json",
}


def R(band, loai, dang, bai, vidu=0, lythuyet=0, refs=(), gian_giao=""):
    """Một dòng TM. `bai` = số thứ tự bài trong phiếu (trên lớp lẫn BTVN)."""
    return dict(band=band, loai=loai, dang=dang, bai=list(bai), vidu=vidu,
                lythuyet=lythuyet, source_refs=list(refs), gian_giao=gian_giao)


# ───────────────────────── BẢNG DÒNG TỪNG PHIẾU ─────────────────────────
ROWS = {
    "A": dict(title="Buổi 1 — Bài 19: Phương trình bậc hai một ẩn", rows=[
        R("NB", "NB kiến thức cũ",
          "Ôn Lớp 8 (khai triển, thu gọn): đưa phương trình về dạng $ax^2+bx+c=0$ rồi chỉ ra các hệ số $a$, $b$, $c$",
          [1, 11], vidu=1, lythuyet=1, refs=["gk1-nguyen-du-2025-1-3"]),
        R("NB", "NB lẻ LT", "Giải phương trình khuyết $c$: đặt nhân tử chung đưa về $x(ax+b)=0$",
          [2, 12], vidu=1, lythuyet=1, gian_giao="dien-khuyet"),
        R("NB", "NB lẻ LT", "Giải phương trình khuyết $b$: đưa về $x^2=k$ rồi khai căn",
          [3, 13], vidu=1),
        R("NB", "NB tách TH",
          "Hoàn thành bài giải bằng công thức nghiệm: chỉ ra $a$, $b$, $c$, tính $\\Delta$, viết hai nghiệm",
          [4, 14], vidu=1, lythuyet=1, refs=["gk2-dong-anh-2025-12.a", "v10-ly-thuong-kiet-2025-III3"]),
        R("NB", "NB lẻ LT", "Dùng $\\Delta$ cho biết số nghiệm: $\\Delta=0$ có nghiệm kép, $\\Delta<0$ vô nghiệm",
          [5, 15], vidu=1),
        R("NB", "NB tách TH",
          "Hoàn thành bài giải bằng công thức nghiệm thu gọn khi $b=2b'$: tính $\\Delta'$, viết hai nghiệm (chia $a$)",
          [6, 16], vidu=1, lythuyet=1,
          refs=["gk2-dong-anh-2025-12.a", "v10-tu-lap-2026-III3", "v10-cau-giay-lan1-2026-III3"]),
        R("TH", "TH tách VD", "Giải phương trình bậc hai đầy đủ bằng công thức nghiệm hoặc công thức nghiệm thu gọn",
          [7, 17], refs=["gk2-dong-anh-2025-12", "ck2-ba-dinh-2024-II3", "v10-cum-thcs-cong-lap-2026-III3"]),
        R("TH", "TH ghép bài", "Đưa phương trình có dấu ngoặc về dạng $ax^2+bx+c=0$ rồi giải",
          [8, 18], vidu=1, refs=["gk1-giang-vo-2024-Ia", "gk1-thanh-cong-2025-II2"]),
        R("VD", "VD lẻ",
          "Bài toán thực tế cho sẵn ẩn (đội xe chở hàng, ô tô đi nhanh hơn dự định): lập phương trình bậc hai, giải, đối chiếu điều kiện",
          [9, 19], vidu=1, refs=["v10-chuong-my-l4-2025-III2"]),
        R("VD", "VD lẻ",
          "Bài toán hình chữ nhật, tìm hai số: tự đặt ẩn, lập phương trình bậc hai và giải (bài đích: mảnh đất, bộ đề Đống Đa)",
          [10, 20], vidu=1, refs=["ck2-gia-lam-2024-III1", "sgk-b21-vd1"]),
    ]),
    "B": dict(title="Buổi 2 — Luyện tập chung: phương trình chứa ẩn ở mẫu quy về phương trình bậc hai", rows=[
        R("NB", "NB kiến thức cũ",
          "Ôn Lớp 8: phân tích mẫu thành nhân tử, tìm điều kiện xác định của phương trình chứa ẩn ở mẫu",
          [1, 9], vidu=1, lythuyet=1, refs=["gk1-son-dong-2024-1b.a", "gk1-nhat-tan-2025-1b.a"]),
        R("NB", "NB tách TH", "Quy đồng mẫu hai vế, khử mẫu, đưa về phương trình $ax^2+bx+c=0$",
          [2, 10], vidu=1, lythuyet=1, refs=["gk1-dich-vong-hau-2025-I3.a"], gian_giao="dien-khuyet"),
        R("NB", "NB lẻ LT", "Nhẩm nghiệm khi $a+b+c=0$ hoặc $a-b+c=0$ (SGK tập hai Bài 20 tr.22)",
          [3, 11], vidu=1, lythuyet=1),
        R("NB", "NB tách TH",
          "Hoàn thành bài giải phương trình chứa ẩn ở mẫu theo bốn bước, loại nghiệm không thỏa mãn điều kiện xác định",
          [4, 12], vidu=1, refs=["gk1-nguyen-du-2025-1-2.a"]),
        R("TH", "TH tách VD",
          "Giải phương trình chứa ẩn ở mẫu quy về bậc hai (mẫu là tam thức, mẫu đối nhau, có nghiệm bị loại)",
          [5, 6, 13, 14], vidu=1, refs=["gk1-dich-vong-hau-2025-I3", "gk1-nguyen-du-2025-1-2",
                                       "gk1-giang-vo-2025-I3", "ck1-nguyen-truong-to-2025-I2",
                                       "gk1-nguyen-truong-to-2025-I1b", "gk1-ai-mo-2025-Ib",
                                       "gk1-chuyen-my-2025-1b", "gk1-nguyen-huy-tuong-2025-1b"]),
        R("VD", "VD lẻ", "Bài toán chuyển động cho sẵn ẩn dẫn tới phương trình chứa ẩn ở mẫu",
          [7, 16], vidu=1, refs=["v10-chuong-my-l5-2025-III1"]),
        R("VD", "VD lẻ",
          "Bài toán năng suất cho sẵn ẩn dẫn tới phương trình chứa ẩn ở mẫu (bài đích: đề minh họa của Sở, 300 sản phẩm)",
          [8, 15], refs=["so-hn-minhhoa-III2"]),
    ]),
    "C": dict(title="Buổi 3 — Bài 20: Định lí Viète và ứng dụng", rows=[
        R("NB", "NB kiến thức cũ",
          "Nhắc lại Bài 19: kiểm tra phương trình có hai nghiệm ($\\Delta\\ge 0$ hoặc $ac<0$) trước khi dùng định lí Viète",
          [2, 20], vidu=1, refs=["so-hn-2026-III3", "sgk-b20-tl1"]),
        R("NB", "NB lẻ LT", "Viết tổng $x_1+x_2$ và tích $x_1x_2$ theo định lí Viète, kể cả hệ số chứa căn",
          [1, 3, 9, 19, 21, 27], vidu=2, lythuyet=1, gian_giao="dien-khuyet",
          refs=["v10-ung-hoa-lan3-2025-III3", "sgk-6.23", "sgk-b20-vd1"]),
        R("NB", "NB tách TH",
          "Biến đổi rồi tính $x_1^2+x_2^2$, $x_1^3+x_2^3$, $(x_1-x_2)^2$ theo tổng và tích hai nghiệm",
          [4, 6, 7, 10, 18, 22, 24, 25], vidu=3, lythuyet=1,
          refs=["v10-huy-van-2024-III3.a", "sgk-6.48", "ck2-lomonoxop-2025-III3", "ck2-chu-van-an-dn-2025-2",
                "ck2-phuc-loi-2024-3-2", "v10-dong-da-de18-2025-III3"]),
        R("NB", "NB tách TH", "Chứng minh hai nghiệm khác $0$ rồi tính $\\dfrac{1}{x_1}+\\dfrac{1}{x_2}$",
          [5, 23], vidu=1, refs=["v10-cau-giay-lan1-2026-III3.a", "sgk-b20-lt2"]),
        R("NB", "NB lẻ LT", "Biết một nghiệm, tìm nghiệm còn lại bằng tổng hai nghiệm",
          [8, 26], vidu=1, lythuyet=1, refs=["sgk-b20-vd3", "sgk-b20-hd3", "sgk-6.24"]),
        R("NB", "NB lẻ LT", "Xét dấu hai nghiệm từ tích và tổng hai nghiệm, không giải phương trình",
          [11, 28], lythuyet=1, refs=["sgk-6.41"]),
        R("TH", "TH tách VD", "Không giải phương trình, tính tổng bình phương, tổng các lập phương hai nghiệm",
          [12, 14, 29, 31], refs=["v10-cum-thcs-cong-lap-2026-III3", "v10-huy-van-2024-III3"]),
        R("TH", "TH tách VD", "Chứng minh hai nghiệm khác $0$ rồi tính tổng nghịch đảo hai nghiệm",
          [13, 30], refs=["v10-cau-giay-lan1-2026-III3"]),
        R("TH", "TH ghép bài", "Biết một nghiệm chứa căn, tìm nghiệm còn lại và hệ số còn thiếu",
          [15, 32], vidu=1, refs=["so-hn-minhhoa-III3"]),
        R("VD", "VD lẻ", "Tính $\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$ theo tổng và tích hai nghiệm",
          [16, 33], vidu=1, refs=["v10-ly-thuong-kiet-2025-III3", "ck2-ba-dinh-2024-II3"]),
        R("VD", "VD lẻ", "Xét dấu hai nghiệm rồi tính biểu thức chứa $|x_1|$, $|x_2|$",
          [17, 34], vidu=1, refs=["v10-cum-thcs-cong-lap-2026-III3", "v10-tu-lap-2026-III3"]),
    ]),
    "D": dict(title="Buổi 4 — Luyện tập: Tính giá trị biểu thức chứa hai nghiệm", rows=[
        R("NB", "NB kiến thức cũ",
          "Nhắc lại Bài 20: kiểm tra điều kiện có nghiệm rồi viết tổng và tích hai nghiệm",
          [1, 12], vidu=1, lythuyet=1, gian_giao="dien-khuyet", refs=["sgk-6.23"]),
        R("NB", "NB lẻ LT", "Hạ bậc: từ $ax_1^2+bx_1+c=0$ viết $x_1^2$ và $x_1^3$ theo $x_1$",
          [2, 13], vidu=1, lythuyet=1),
        R("NB", "NB tách TH", "Hạ bậc rồi tính giá trị biểu thức của một nghiệm",
          [3, 14], vidu=1, refs=["v10-ung-hoa-lan3-2025-III3.a"]),
        R("NB", "NB tách TH",
          "Hoàn thành bài giải biểu thức không đối xứng: hạ bậc để đưa về tổng và tích hai nghiệm",
          [4, 5, 15, 17], vidu=1, lythuyet=1, refs=["so-hn-2026-III3.a"]),
        R("NB", "NB lẻ LT", "Xét dấu hai nghiệm rồi rút gọn $\\sqrt{x_1^2}=|x_1|$",
          [6, 16], vidu=1, lythuyet=1),
        R("TH", "TH tách VD", "Hạ bậc tính biểu thức bậc ba của một nghiệm",
          [7, 18], vidu=1, refs=["v10-ung-hoa-lan3-2025-III3"]),
        R("TH", "TH tách VD", "Tính biểu thức không đối xứng của hai nghiệm bằng hạ bậc, tổng và tích",
          [8, 19], vidu=1, refs=["so-hn-2026-III3", "ck2-phuc-dong-2025-III2"]),
        R("TH", "TH ghép bài",
          "Biến đổi (quy đồng, khai triển) rồi tính biểu thức đối xứng của hai nghiệm theo tổng và tích",
          [9, 20], refs=["v10-thai-thinh-2025-III3", "v10-quang-trung-2025-III3", "v10-to-vinh-dien-2025-III3",
                         "ck2-thang-long-2025-III3", "v10-thai-thinh-2026-III3", "tl-viete-12-tr3",
                         "tl-viete-13-tr3"]),
        R("VD", "VD lẻ", "Hai nghiệm cùng âm: tính biểu thức chứa căn của nghiệm",
          [10, 21], vidu=1, refs=["v10-tu-lap-2026-III3"]),
        R("VD", "VD lẻ", "Biểu thức phân thức không đối xứng của hai nghiệm (đề chính thức Vào 10 Hà Nội 2026)",
          [11, 22], vidu=1, refs=["so-hn-2026-III3"]),
    ]),
    "E": dict(title="Buổi 5 — Bài 21: Giải bài toán bằng cách lập phương trình", rows=[
        R("NB", "NB kiến thức cũ",
          "Giải phương trình vừa lập (Bài 19, phương trình chứa ẩn ở mẫu), đối chiếu điều kiện và trả lời",
          [5, 10, 15, 29, 32, 35, 36], refs=["sgk-b21-vd1", "sgk-b21-lt1"]),
        R("NB", "NB lẻ LT",
          "Biểu diễn đại lượng chưa biết theo ẩn: năng suất, thời gian $t=\\dfrac{s}{v}$, phần công việc làm trong $1$ giờ",
          [1, 2, 6, 7, 11, 12, 26, 30, 33], vidu=3, lythuyet=2),
        R("NB", "NB tách TH", "Chỉ ra câu văn cho biết quan hệ giữa các đại lượng, lập phương trình",
          [3, 4, 8, 9, 13, 14, 27, 28, 31, 34], lythuyet=1, gian_giao="dien-khuyet",
          refs=["v10-chuong-my-l4-2025-III2.a", "sgk-6.32.a"]),
        R("TH", "TH tách VD", "Giải trọn bài năng suất, số xe (kẻ bảng đại lượng)",
          [16, 17, 18, 37, 38, 39], refs=["v10-chuong-my-l4-2025-III2", "sgk-6.33"]),
        R("TH", "TH tách VD", "Giải trọn bài chuyển động, kể cả xuôi dòng và ngược dòng",
          [19, 20, 21, 40, 41, 42], refs=["sgk-6.32"]),
        R("TH", "TH ghép bài", "Giải trọn bài làm chung, làm riêng", [22, 23, 43, 44],
          refs=["ck2-mai-dich-2025-3-2", "v10-ung-hoa-lan3-2025-III2"]),
        R("VD", "VD lẻ", "Bài năng suất vượt mức, xong sớm hơn kế hoạch", [24, 45], refs=["gk2-dong-anh-2025-31"]),
        R("VD", "VD lẻ", "Bài chuyển động hai chặng với vận tốc khác nhau", [25, 46],
          refs=["v10-tu-lap-2026-III2", "v10-huy-van-2024-III1"]),
    ]),
    "F": dict(title="Buổi 6 — Luyện tập chung và Bài tập cuối chương VI", kiem_tra_phut=45, rows=[
        R("NB", "NB kiến thức cũ",
          "Ôn Lớp 8: điều kiện xác định và chọn nghiệm của phương trình chứa ẩn ở mẫu",
          [5, 18], lythuyet=1, refs=["gk1-phan-dinh-giot-2024-1b.a"]),
        R("NB", "NB lẻ LT", "Chọn công thức nghiệm $\\Delta$ hay $\\Delta'$ cho từng phương trình",
          [1, 14], lythuyet=1, refs=["sgk-b19-lt6"]),
        R("NB", "NB lẻ LT", "Nhẩm nghiệm khi $a+b+c=0$ hoặc $a-b+c=0$", [2, 15], refs=["sgk-b20-lt2", "tl-viete-47-tr8"]),
        R("NB", "NB tách TH",
          "Tính biểu thức của hai nghiệm theo tổng và tích, hạ bậc $x_1^2$ và $x_1^3$",
          [3, 4, 16, 17], vidu=2, lythuyet=1, gian_giao="dien-khuyet", refs=["ck2-ba-dinh-2024-II3.a"]),
        R("NB", "NB lẻ LT", "Đặt ẩn kèm đơn vị và điều kiện cho bài toán lời văn", [6, 19], lythuyet=1,
          refs=["gk2-my-dinh-2-2025-3", "ck2-chu-van-an-dn-2025-3", "v10-nguyen-tat-thanh-2025-cau5", "gk1-thanh-am-2024-V"]),
        R("NB", "NB lẻ LT", "Lập phương trình từ câu văn của đề bài", [7, 20],
          refs=["v10-phuong-mai-2025-III2", "gk1-nguyen-truong-to-2024-II2", "v10-my-dinh-2-2026-III2"]),
        R("TH", "TH ghép bài", "Giải phương trình chứa ẩn ở mẫu quy về bậc hai", [8, 21], vidu=1,
          refs=["gk1-nghia-tan-2024-I2"]),
        R("TH", "TH tách VD",
          "Tính biểu thức của hai nghiệm, biết một nghiệm thì tìm nghiệm còn lại và hệ số còn thiếu",
          [9, 11, 22, 24], vidu=2, refs=["ck2-ba-dinh-2024-II3", "so-hn-minhhoa-III3"]),
        R("TH", "TH ghép bài", "Bài hình chữ nhật: lập phương trình bậc hai và giải", [10, 23], vidu=1,
          refs=["v10-be-van-dan-2025-III2", "ck2-gia-lam-2024-III1", "sgk-6.27"]),
        R("VD", "VD lẻ", "Hạ bậc tính biểu thức không đối xứng của nghiệm", [12, 25], vidu=1,
          refs=["v10-ung-hoa-lan3-2025-III3"]),
        R("VD", "VD lẻ", "Bài toán lời văn dẫn tới phương trình chứa ẩn ở mẫu (năng suất, chuyển động xuôi ngược dòng)",
          [13, 26], refs=["gk2-le-ngoc-han-2024-III1", "v10-to-vinh-dien-2025-III2"]),
    ]),
}

# ───────────────────────── KHỐI ĐẦU THUYẾT MINH ─────────────────────────
THOILUONG = [
    "Buổi 1 (tuần 22 — Bài 19. Phương trình bậc hai một ẩn): 1 ca = 180 phút (PPCT SGV 3 tiết).",
    "Buổi 2 (tuần 23 — Luyện tập chung: phương trình chứa ẩn ở mẫu quy về phương trình bậc hai): 1 ca = 180 phút (PPCT SGV 2 tiết).",
    "Buổi 3 (tuần 24 — Bài 20. Định lí Viète và ứng dụng): 1 ca = 180 phút (PPCT SGV 2 tiết).",
    "Buổi 4 (tuần 25 — Luyện tập: tính giá trị biểu thức chứa hai nghiệm): 1 ca = 180 phút (không thêm tiết SGK).",
    "Buổi 5 (tuần 26 — Bài 21. Giải bài toán bằng cách lập phương trình): 1 ca = 180 phút (PPCT SGV 2 tiết).",
    "Buổi 6 (tuần 27 — Luyện tập chung và Bài tập cuối chương VI): 1 ca = 180 phút (135 phút luyện tập $+$ 45 phút kiểm tra chương, PPCT SGV 4 tiết).",
    "\\textbf{Tổng 6 ca = 1080 phút $\\approx$ 24 tiết} (PPCT SGV chương VI: 16 tiết, trừ 3 tiết Bài 18 còn 13 tiết, trong đó 45 phút là bài kiểm tra chương).",
]

KIEN_THUC_NEN = [
    "\\textbf{Bảy hằng đẳng thức đáng nhớ} (Lớp 8): khai triển để thu gọn phương trình về dạng $ax^2+bx+c=0$, và biến đổi $x_1^2+x_2^2$, $x_1^3+x_2^3$, $(x_1-x_2)^2$ theo tổng và tích hai nghiệm.",
    "\\textbf{Phân tích đa thức thành nhân tử} (Lớp 8): đặt nhân tử chung và dùng $A^2-B^2$ để giải phương trình khuyết $c$, phân tích mẫu thức khi tìm điều kiện xác định.",
    "\\textbf{Quy đồng mẫu thức và điều kiện xác định của phân thức} (Lớp 8, ôn lại ở Bài 4 tuần 7): giải phương trình chứa ẩn ở mẫu quy về bậc hai (buổi 2) và bài toán lời văn có ẩn ở mẫu (buổi 5, 6). Quên điều kiện xác định là giữ lại nghiệm đáng lẽ phải loại.",
    "\\textbf{Căn bậc hai số học và $\\sqrt{A^2}=|A|$} (Chương III): tính $\\sqrt{\\Delta}$, rút gọn nghiệm chứa căn, phương trình có hệ số chứa căn, rút gọn biểu thức chứa căn của nghiệm (buổi 4).",
    "\\textbf{Giải bài toán bằng cách lập phương trình, hệ phương trình} (Chương I, Bài 3): ba bước lập phương trình, giải, đối chiếu điều kiện giữ nguyên, chương VI chỉ đổi khâu giải thành phương trình bậc hai.",
    "\\textbf{Công thức chuyển động, năng suất, diện tích hình chữ nhật} (lớp dưới): $s=v\\cdot t$, khối lượng công việc $=$ năng suất $\\times$ thời gian, $S=$ dài $\\times$ rộng, dùng để biểu diễn đại lượng theo ẩn ở buổi 5.",
    "\\textbf{Giải phương trình bậc nhất một ẩn} (Lớp 8): bước cuối của mọi phương trình tích.",
]

LYTHUYET = [
    "\\textbf{Mục tiêu chương}: học sinh giải được phương trình bậc hai (dạng khuyết, công thức nghiệm, công thức nghiệm thu gọn), phương trình chứa ẩn ở mẫu quy về bậc hai, dùng định lí Viète để tính giá trị biểu thức của hai nghiệm, và giải bài toán bằng cách lập phương trình bậc hai.",
    "Không dùng kí hiệu tắt cho tổng và tích hai nghiệm. Viết thẳng $x_1+x_2$ và $x_1x_2$, gọi đúng tên là \\emph{tổng hai nghiệm} và \\emph{tích hai nghiệm}, như đề thi hỏi bằng lời: \\emph{tổng nghịch đảo hai nghiệm}, \\emph{tổng các lập phương hai nghiệm}.",
    "Công thức nghiệm $\\Delta=b^2-4ac$: $\\Delta>0$ hai nghiệm phân biệt, $\\Delta=0$ nghiệm kép, $\\Delta<0$ vô nghiệm. Công thức thu gọn $\\Delta'=b'^2-ac$ khi $b=2b'$.",
    "Phương trình chứa ẩn ở mẫu: tìm điều kiện xác định, quy đồng mẫu hai vế rồi khử mẫu, giải phương trình vừa nhận được, đối chiếu điều kiện xác định và kết luận (SGK tập một tr.29).",
    "Hệ thức Viète: $x_1+x_2=-\\dfrac{b}{a}$ và $x_1x_2=\\dfrac{c}{a}$. Nhẩm nghiệm khi $a+b+c=0$ và khi $a-b+c=0$. Biết một nghiệm, tìm nghiệm còn lại.",
    "Bốn công thức biến đổi: $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2$, $\\dfrac{1}{x_1}+\\dfrac{1}{x_2}=\\dfrac{x_1+x_2}{x_1x_2}$, $x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)$, $(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2$.",
    "Hạ bậc: $x_1$ là nghiệm nên $ax_1^2+bx_1+c=0$, thay $ax_1^2=-bx_1-c$ để hạ bậc biểu thức trước khi dùng tổng và tích (buổi 4, buổi 6).",
    "Ba bước giải bài toán bằng cách lập phương trình (SGK tập hai tr.25): lập phương trình (chọn ẩn và đặt điều kiện, biểu diễn các đại lượng chưa biết theo ẩn, lập phương trình), giải phương trình, đối chiếu điều kiện và trả lời.",
    "\\textbf{Nguồn bài}: tab phân dạng chương VI (đề Vào 10 chính thức và minh họa của Sở GD\\&ĐT Hà Nội, đề thi thử, đề giữa kì và cuối kì các trường Hà Nội, SGK). Ngân hàng 21 đề GK1/CK1 không phủ chương này vì chương VI học ở kì II. Đáp số mọi bài trong phiếu đã kiểm bằng máy.",
    "\\textbf{Chuẩn đầu ra tầng C}: trình bày trọn bài giải bài toán bằng cách lập phương trình (Câu III.1 đề Vào 10, $1{,}0$ điểm) và câu tính giá trị biểu thức của hai nghiệm (Câu III.3, $0{,}5$ điểm).",
]

VIDU = [
    "Buổi 1: Giải $2x^2-5x+2=0$ bằng công thức nghiệm ($x_1=2$, $x_2=\\dfrac{1}{2}$), $4x^2+6x=0$ khuyết $c$, $2x^2-18=0$ khuyết $b$, $x^2-8x+12=0$ bằng công thức nghiệm thu gọn.",
    "Buổi 2: Giải $\\dfrac{2x}{x+3}+\\dfrac{1}{x-1}=\\dfrac{4}{(x-1)(x+3)}$: điều kiện xác định $x\\ne -3$, $x\\ne 1$, khử mẫu được $2x^2-x-1=0$, nhẩm $a+b+c=0$ được $x=1$ (loại) và $x=-\\dfrac{1}{2}$.",
    "Buổi 3: Phương trình $3x^2-12x+4=0$ có $x_1+x_2=4$, $x_1x_2=\\dfrac{4}{3}$, chứng minh hai nghiệm khác $0$ rồi tính tổng nghịch đảo hai nghiệm bằng $3$.",
    "Buổi 4: Với $x^2-3x-3=0$, hạ bậc $x_1^2=3x_1+3$ nên $x_1^3=12x_1+9$, do đó $H=x_1^3-12x_1+2000=2009$.",
    "Buổi 5: Xưởng may $480$ chiếc áo, thực tế mỗi ngày may ít hơn kế hoạch $8$ chiếc nên chậm $2$ ngày: $\\dfrac{480}{x-8}-\\dfrac{480}{x}=2 \\Rightarrow x=48$ (loại $x=-40$).",
    "Buổi 6: Cho $x^2-5x-8=0$, hạ bậc $x_1^2=5x_1+8$ nên $A=x_1^2+5x_2=5(x_1+x_2)+8=33$.",
]

DANG_VD = [
    "Câu III.1 — bài năng suất dẫn tới phương trình chứa ẩn ở mẫu quy về bậc hai (đề minh họa của Sở, thi thử Chương Mỹ).",
    "Câu III.1 — bài chuyển động chênh lệch thời gian (thi thử Chương Mỹ, Tự Lập).",
    "Câu III.1 — bài diện tích hình chữ nhật biết hiệu hai kích thước (bộ đề Đống Đa).",
    "Câu III.3 — tính biểu thức của hai nghiệm bằng tổng và tích: tổng bình phương, tổng nghịch đảo, tổng các lập phương.",
    "Câu III.3 — hạ bậc để đưa biểu thức không đối xứng về tổng và tích (đề chính thức 2026 cho kết quả $18$, thi thử Ứng Hòa cho kết quả $1995$).",
    "Câu III.3 — biết một nghiệm chứa căn, tìm nghiệm còn lại và hệ số còn thiếu (đề minh họa của Sở).",
    "Câu III.3 — xét dấu hai nghiệm rồi rút gọn biểu thức chứa căn, giá trị tuyệt đối (thi thử cụm THCS công lập, THCS Tự Lập).",
]

LOISAI = [
    "Chưa đưa phương trình về dạng $ax^2+bx+c=0$ đã tính $\\Delta$.",
    "Sai dấu khi $c$ âm: với $c=-6$ thì $-4ac=+24$, hay bị viết thành $-24$.",
    "Dùng $\\Delta'$ khi $b$ lẻ, hoặc dùng đúng $\\Delta'$ nhưng vẫn chia $2a$ thay vì chia $a$.",
    "Dùng tổng và tích hai nghiệm mà chưa kiểm tra phương trình có nghiệm ($\\Delta\\ge 0$ hoặc $ac<0$).",
    "Nhớ nhầm dấu của tổng: viết $x_1+x_2=\\dfrac{b}{a}$ thay vì $-\\dfrac{b}{a}$.",
    "Khai triển sai $x_1^2+x_2^2$ thành $(x_1+x_2)^2$ vì quên trừ $2x_1x_2$.",
    "Tính tổng nghịch đảo mà quên chứng minh hai nghiệm khác $0$.",
    "Giải phương trình chứa ẩn ở mẫu mà quên điều kiện xác định hoặc quên loại nghiệm.",
    "Làm tròn ở bước giữa khi $\\sqrt{\\Delta}$ không chính phương, làm lệch kết quả cuối.",
    "\\textbf{Bài toán lập phương trình}: thiếu câu đặt ẩn kèm đơn vị và điều kiện, giữ lại nghiệm âm, hoặc kết luận không có đơn vị.",
    "\\textbf{Biểu thức của hai nghiệm}: viết ngay tổng và tích mà bỏ câu kiểm tra điều kiện có nghiệm ở đầu bài, và thiếu câu kết luận \\textquotedblleft Vậy giá trị của biểu thức bằng \\dots\\textquotedblright{} ở cuối.",
    "\\textbf{Biểu thức chứa căn của nghiệm}: viết thẳng $\\sqrt{A^2}=A$ mà không xét dấu của nghiệm trước.",
]

KIENTHUC_NB = [
    "Phương trình bậc hai một ẩn là phương trình dạng $ax^2+bx+c=0$ với $a \\ne 0$, trong đó $a$, $b$, $c$ là các hệ số.",
    "Công thức nghiệm: $\\Delta=b^2-4ac$, nếu $\\Delta>0$ thì $x_{1,2}=\\dfrac{-b \\pm \\sqrt{\\Delta}}{2a}$, nếu $\\Delta=0$ thì $x_1=x_2=-\\dfrac{b}{2a}$, nếu $\\Delta<0$ thì phương trình vô nghiệm.",
    "Công thức nghiệm thu gọn khi $b=2b'$: $\\Delta'=b'^2-ac$ và $x_{1,2}=\\dfrac{-b' \\pm \\sqrt{\\Delta'}}{a}$ (chia $a$, không chia $2a$).",
    "Phương trình khuyết $c$ giải bằng đặt nhân tử chung, phương trình khuyết $b$ giải bằng chuyển vế rồi khai căn.",
    "Bốn bước giải phương trình chứa ẩn ở mẫu: điều kiện xác định, quy đồng và khử mẫu, giải, đối chiếu điều kiện.",
    "Hệ thức Viète: $x_1+x_2=-\\dfrac{b}{a}$ và $x_1x_2=\\dfrac{c}{a}$, chỉ dùng sau khi đã kiểm tra phương trình có nghiệm.",
    "Nhẩm nghiệm: $a+b+c=0$ cho $x_1=1$, $x_2=\\dfrac{c}{a}$, còn $a-b+c=0$ cho $x_1=-1$, $x_2=-\\dfrac{c}{a}$.",
    "$ac<0$ thì phương trình luôn có hai nghiệm trái dấu, dùng thay cho việc tính $\\Delta$.",
]


def _num(label: str) -> int:
    return int(label.replace("Bài", "").strip().rstrip("."))


def build(ghi: bool) -> None:
    tm = json.loads(TM.read_text(encoding="utf-8"))
    tm.update(thoiluong=THOILUONG, kien_thuc_nen=KIEN_THUC_NEN, lythuyet=LYTHUYET, vidu=VIDU,
              dang_vd=DANG_VD, loisai=LOISAI, kienthuc_nb=KIENTHUC_NB)
    phieu_moi = []
    for code, spec in ROWS.items():
        path = D / PHIEU[code]
        raw = json.loads(path.read_text(encoding="utf-8"))
        les = LessonPackage.model_validate(raw)
        probs = {_num(b.label): b for st in les.stages for b in st.blocks
                 if getattr(b, "type", "") == "problem"}
        # mã dạng theo thứ tự trong nhóm band — đúng cách spec_gate/renderer đánh số
        dem, ma_bai, rows = {}, {}, []
        for i, r in enumerate(spec["rows"], 1):
            dem[r["band"]] = dem.get(r["band"], 0) + 1
            ma = f"{r['band']}{dem[r['band']]}"
            on = bt = 0
            khung = False
            for n in r["bai"]:
                if n in ma_bai:
                    raise SystemExit(f"phiếu {code}: Bài {n} gán hai dòng ({ma_bai[n]}, {ma})")
                p = probs[n]
                ma_bai[n] = ma
                c = _so_cau(p)
                if p.tier == "onclass":
                    on += c
                else:
                    bt += c
                khung |= "hoàn thành bài giải" in (p.statement or "")
            row = dict(stt=i, dang=r["dang"], band=r["band"], loai=r["loai"],
                       gian_giao=r["gian_giao"], onclass=on, btvn=bt, vidu=r["vidu"],
                       lythuyet=r["lythuyet"], source_refs=r["source_refs"])
            if khung and r["band"] == "NB":
                row["khung"] = True
            rows.append(row)
        thieu = sorted(set(probs) - set(ma_bai))
        if thieu:
            raise SystemExit(f"phiếu {code}: bài chưa gán dòng TM: {thieu}")
        # ghi dang_id vào phiếu (giữ nguyên mọi trường khác của JSON gốc)
        doi = 0
        for st in raw["stages"]:
            for b in st["blocks"]:
                if b.get("type") == "problem":
                    moi = ma_bai[_num(b["label"])]
                    if b.get("dang_id") != moi:
                        b["dang_id"] = moi
                        doi += 1
        p_tm = {"code": code, "title": spec["title"]}
        if spec.get("kiem_tra_phut"):
            p_tm["kiem_tra_phut"] = spec["kiem_tra_phut"]
        p_tm["rows"] = rows
        phieu_moi.append(p_tm)
        tong = {}
        for r in rows:
            for seg in ("onclass", "btvn"):
                tong[(seg, r["band"])] = tong.get((seg, r["band"]), 0) + r[seg]
        print(f"phiếu {code}: {len(rows)} dòng, đổi dang_id {doi} bài | "
              + " ".join(f"{s[:2]}-{b}={n}" for (s, b), n in sorted(tong.items())))
        if ghi:
            path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tm["phieu"] = phieu_moi
    if ghi:
        TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("ĐÃ GHI", TM)


if __name__ == "__main__":
    build("--ghi" in sys.argv)
