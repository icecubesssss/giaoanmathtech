#!/usr/bin/env python3
"""THỐNG KÊ DẠNG BÀI trong đề kiểm tra Toán Hà Nội, khối 6-9 × 4 kỳ → 4 file Excel.

Nguồn: kho đề `inputs/refs/de-thi/lop-N/{giua-ki-1,cuoi-ki-1,giua-ki-2,cuoi-ki-2}` (đề lệch KNTT
đã tách sang `de-thi-lech-kntt/` ngày 30/09/2026 nên KHÔNG được tính).
Text lấy ở `storage/cache/de-txt-all/` — lớp text của PDF, hoặc OCR tiếng Việt (tesseract `vie`)
cho đề scan; dòng đầu mỗi file ghi `#NGUON:text|ocr`.

Cách làm:
  1. Cắt lấy KHỐI ĐỀ đầu tiên của file (bỏ ma trận / bản đặc tả / hướng dẫn chấm / mã đề thứ hai).
  2. Tách khối đề thành từng Câu/Bài; nhận phần trắc nghiệm hay tự luận.
  3. Gắn dạng cho mỗi câu bằng từ khoá theo bộ mã từng khối (bám thứ tự chương KNTT).
     Một câu có thể mang nhiều dạng (bài tự luận nhiều ý).
  4. Đếm: số ĐỀ có dạng (tần suất), số lượt câu, trắc nghiệm/tự luận — theo từng kỳ.

Đây là phân loại TỰ ĐỘNG theo từ khoá ⇒ đúng ở mức "dạng này có trong đề hay không", không
thay được việc đọc đề. Đề OCR sai công thức nhưng giữ được chữ nên vẫn nhận dạng được.

Dùng:
    .venv/bin/python scripts/thong_ke_dang_de.py            # 4 file ở outputs/thong-ke-dang-de/
    .venv/bin/python scripts/thong_ke_dang_de.py --lop 8
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DE = ROOT / "inputs" / "refs" / "de-thi"
TXT = ROOT / "storage" / "cache" / "de-txt-all"
OUT = ROOT / "outputs" / "thong-ke-dang-de"

KY_DIR = {"giua-ki-1": "GK1", "cuoi-ki-1": "CK1", "giua-ki-2": "GK2", "cuoi-ki-2": "CK2",
          "de-cuoi-ki-2": "CK2"}
KY_THU_TU = ["GK1", "CK1", "GK2", "CK2"]

# ─────────────────────────── BỘ MÃ DẠNG THEO KHỐI ───────────────────────────
# (chương KNTT, tên dạng, regex trên text đã chuẩn hoá chữ thường)
# Dạng chung ("thực hiện phép tính", "tìm x"…) để chương "Chung" — chương cụ thể do KỲ quyết định.
_TINH = r"kết quả (của )?(phép tính|biểu thức)|^\s*(câu|bài)[^\n]{0,25}\btính\b|thực hiện phép tính|tính hợp l[íý]|tính nhanh|tính giá trị (của )?(các )?biểu thức|tính một cách hợp"
_TIMX = r"(số (tự nhiên |nguyên )?)?x thoả mãn|x thỏa mãn|giá trị (nào )?của x|tìm (số (tự nhiên|nguyên) )?x\b|tìm x[,:;. ]|tìm x biết|tìm các số (tự nhiên|nguyên) x"
_CM_HINH = r"chứng minh|chứng tỏ"
_THUC_TE = ("Chung", "Toán thực tế có lời văn (mua bán, giá tiền, đo lường)",
            r"\d ?(nghìn |ngàn )?đồng\b|triệu đồng|giá (tiền|bán|niêm yết|gốc)|giảm giá|khuyến mãi|tiền lãi|lãi suất|\bmua\b")

# Câu NÂNG CAO cuối đề (lớp 6-7) — nhận theo hình thức, dùng chung.
_NC = [
    ("Nâng cao", "Tổng dãy có quy luật (tính, so sánh, chứng minh)", r"(\+|\.|−|-)\s*(\.\s?\.\s?\.|…)\s*(\+|−|-|\.)"),
    ("Nâng cao", "Chứng minh chia hết / số nguyên tố cùng nhau", r"chứng (minh|tỏ).{0,120}(chia hết|nguyên tố cùng nhau|tối giản)"),
    ("Nâng cao", "Giá trị lớn nhất / nhỏ nhất", r"(giá trị )?(lớn|nhỏ) nhất của"),
    ("Nâng cao", "Chứng minh đẳng thức / tỉ lệ thức", r"chứng minh (rằng )?:?[^\n]{0,60}= ?[^\n]{0,30}="),
    ("Nâng cao", "Tìm số nguyên / tự nhiên thoả điều kiện (x, y, n)", r"tìm (các )?(cặp )?số (tự nhiên|nguyên) ?(x ?, ?y|n|a ?, ?b)|tìm x ?, ?y|tìm n\b"),
]

DANG: dict[str, list[tuple[str, str, str]]] = {
    "6": [
        ("Chung", "Thực hiện phép tính / tính hợp lí", _TINH),
        ("Chung", "Tìm x", _TIMX),
        ("Chung", "So sánh, sắp xếp thứ tự các số", r"so sánh|sắp xếp|thứ tự (tăng|giảm)|lớn nhất|nhỏ nhất"),
        ("I. Số tự nhiên", "Tập hợp, phần tử, cách viết tập hợp", r"tập hợp [a-z]\b|phần tử|liệt kê|chỉ ra tính chất đặc trưng|∈|∉"),
        ("I. Số tự nhiên", "Ghi số, số La Mã, giá trị chữ số", r"la mã|chữ số hàng|giá trị (của )?chữ số|số liền (trước|sau)"),
        ("I. Số tự nhiên", "Luỹ thừa", r"lu[ỹỹ] thừa|dạng (một )?lu[ỹỹ]"),
        ("I. Số tự nhiên", "Thứ tự thực hiện phép tính", r"thứ tự thực hiện"),
        ("II. Chia hết", "Dấu hiệu chia hết cho 2, 3, 5, 9", r"chia hết cho|⋮|dấu hiệu chia hết|phép chia hết|thay (dấu )?\*|chữ số \* "),
        ("II. Chia hết", "Tính chất chia hết của tổng/hiệu", r"(tổng|hiệu) .{0,40}(có )?(không )?chia hết|chia hết cho [a-z0-9]+ không"),
        ("II. Chia hết", "Ước và bội", r"ước của|bội của|tập hợp (các )?(ước|bội)|ư\(\d|b\(\d"),
        ("II. Chia hết", "Số nguyên tố, phân tích ra thừa số nguyên tố", r"số nguy[eê]n t[ốổ]|hợp số|thừa số nguyên tố"),
        ("II. Chia hết", "ƯC, ƯCLN", r"ước chung|ưcln"),
        ("II. Chia hết", "BC, BCNN", r"bội chung|bcnn"),
        ("II. Chia hết", "Bài toán thực tế ƯCLN/BCNN", r"vừa đủ|đều (thừa|thiếu)|sao cho .{0,120}(như nhau|bằng nhau)|chia .{0,150}(đĩa|túi|phần quà|phần thưởng)|(chia đều|xếp (thành )?hàng|chia (thành|được)|số phần thưởng|nhiều nhất|ít nhất).{0,200}(tổ|nhóm|hàng|phần|học sinh|quyển|bó|túi)|(tổ|nhóm|hàng|phần|học sinh|quyển).{0,200}(chia đều|nhiều nhất|ít nhất)"),
        ("III. Số nguyên", "Số nguyên âm, số đối, trục số, so sánh", r"số nguyên âm|số đối(?! của phân số)|trục số|tập hợp (các )?số nguyên(?! tố)|mực nước biển|nhiệt độ|dưới 0|âm độ"),
        ("III. Số nguyên", "Quy tắc dấu ngoặc, chuyển vế", r"dấu ngoặc|bỏ ngoặc|chuyển vế"),
        ("IV. Hình phẳng", "Nhận biết tam giác đều, hình vuông, lục giác đều, HCN, hình thoi, HBH, hình thang cân",
         r"(hình nào|là hình gì|đặc điểm|khẳng định|tính chất|đường chéo|các góc|cạnh (đối|bên)|bằng nhau|trục đối xứng|vẽ).{0,100}(tam giác đều|lục giác đều|hình thoi|hình bình hành|hình thang cân|hình vuông|hình chữ nhật)|(tam giác đều|lục giác đều|hình thoi|hình bình hành|hình thang cân|hình vuông|hình chữ nhật).{0,100}(hình nào|là hình gì|đặc điểm|khẳng định|tính chất|đường chéo|các góc|cạnh (đối|bên)|bằng nhau|trục đối xứng|vẽ)"),
        ("IV. Hình phẳng", "Chu vi, diện tích hình phẳng", r"chu vi|diện tích"),
        ("IV. Hình phẳng", "Vẽ hình (thước, compa)", r"vẽ (một )?(hình|tam giác|lục giác)"),
        ("V. Đối xứng", "Trục đối xứng, tâm đối xứng", r"đối xứng"),
        ("VI. Phân số", "Phân số bằng nhau, rút gọn, tối giản, hỗn số", r"phân số (bằng nhau|tối giản|nào)|mẫu (số )?chung|rút gọn phân số|hỗn số|quy đồng|số nghịch đảo|phân số đối"),
        ("VI. Phân số", "So sánh, sắp xếp phân số", r"(so sánh|sắp xếp).{0,60}phân số|phân số.{0,60}(lớn nhất|nhỏ nhất|tăng dần|giảm dần)"),
        ("VI. Phân số", "Hai bài toán về phân số (giá trị phân số của một số…)", r"của (một )?số [a-z]\b|của số đó|\d+/\d+ (số|tổng|quãng)|phân số của|của nó bằng|tìm một số biết|số trang|số học sinh (lớp|cả|khối)"),
        ("VII. Số thập phân", "Số thập phân, làm tròn, ước lượng", r"số thập phân|làm tròn|ước lượng"),
        ("VII. Số thập phân", "Tỉ số, tỉ số phần trăm", r"tỉ số|phần trăm|%"),
        ("VIII. Hình cơ bản", "Điểm, đường thẳng, ba điểm thẳng hàng", r"thẳng hàng|nằm giữa|giao điểm|điểm .{0,20}(thuộc|không thuộc)|đường thẳng"),
        ("VIII. Hình cơ bản", "Tia, tia đối, tia trùng nhau", r"\btia\b"),
        ("VIII. Hình cơ bản", "Đoạn thẳng, độ dài, trung điểm", r"trung điểm|độ dài đoạn|đoạn thẳng"),
        ("VIII. Hình cơ bản", "Góc, số đo góc, các loại góc", r"\bgóc\b"),
        ("IX. Dữ liệu – XS", "Thu thập, bảng dữ liệu, dữ liệu không hợp lí", r"thống kê|dữ liệu|bảng thống kê|kiểm đếm|thu thập"),
        ("IX. Dữ liệu – XS", "Biểu đồ tranh, biểu đồ cột (kép)", r"biểu đồ"),
        ("IX. Dữ liệu – XS", "Xác suất thực nghiệm", r"xác suất|tung (một )?đồng xu|gieo (một )?(con )?xúc xắc|lấy ngẫu nhiên|kết quả có thể"),
    ],
    "7": [
        ("Chung", "Thực hiện phép tính / tính hợp lí", _TINH),
        ("Chung", "Tìm x", _TIMX + r"|tìm x, ?y"),
        ("I. Số hữu tỉ", "Số hữu tỉ, số đối, biểu diễn trên trục số, so sánh", r"số hữu tỉ|trục số|số đối|ℚ"),
        ("I. Số hữu tỉ", "Luỹ thừa của số hữu tỉ", r"lu[ỹỹ] thừa"),
        ("I. Số hữu tỉ", "Quy tắc dấu ngoặc, chuyển vế", r"dấu ngoặc|chuyển vế"),
        ("II. Số thực", "Căn bậc hai số học", r"căn bậc hai|√"),
        ("II. Số thực", "Số vô tỉ, số thực, số thập phân vô hạn", r"vô tỉ|số thực|vô hạn|tuần hoàn|ℝ|\bi\b ?∈"),
        ("II. Số thực", "Giá trị tuyệt đối", r"giá trị tuyệt đối|\|x"),
        ("II. Số thực", "Làm tròn, ước lượng", r"làm tròn|ước lượng|độ chính xác"),
        ("III. Góc – song song", "Góc đối đỉnh, hai góc kề bù, tính số đo góc", r"đối đỉnh|kề bù|kề nhau"),
        ("III. Góc – song song", "Tia phân giác (cả khi dùng trong bài hình tam giác)", r"phân giác"),
        ("III. Góc – song song", "Dấu hiệu, tính chất hai đường thẳng song song, tiên đề Euclid",
         r"song song|so le trong|đồng vị|trong cùng phía|euclid|ơ-?clít"),
        ("III. Góc – song song", "Định lí, giả thiết – kết luận", r"định lí|giả thiết|gt ?- ?kl|ghi gt"),
        ("IV. Tam giác bằng nhau", "Tổng ba góc, góc ngoài tam giác", r"tổng (ba|3|các) góc|góc ngoài|180 ?°|\b1800\b"),
        ("IV. Tam giác bằng nhau", "Bài hình tổng hợp: cho tam giác … chứng minh", r"(△|∆|\\baabc\\b|tam giác).{0,400}chứng (minh|tỏ)"),
        ("IV. Tam giác bằng nhau", "Hai tam giác bằng nhau (c.c.c, c.g.c, g.c.g, tam giác vuông)", r"bằng nhau|c\.?c\.?c|c\.?g\.?c|g\.?c\.?g|cạnh huyền"),
        ("IV. Tam giác bằng nhau", "Tam giác cân, tam giác đều", r"tam giác .{0,10}cân|cân tại|tam giác đều"),
        ("IV. Tam giác bằng nhau", "Đường trung trực của đoạn thẳng", r"trung trực"),
        ("V. Dữ liệu", "Thu thập, phân loại dữ liệu", r"thống kê|dữ liệu|thu thập|số liệu"),
        ("V. Dữ liệu", "Biểu đồ hình quạt tròn, biểu đồ đoạn thẳng", r"biểu đồ"),
        ("VI. Tỉ lệ thức", "Tỉ lệ thức, dãy tỉ số bằng nhau", r"tỉ lệ thức|dãy tỉ số|tính chất (của )?dãy"),
        ("VI. Tỉ lệ thức", "Đại lượng tỉ lệ thuận / nghịch", r"tỉ lệ thuận|tỉ lệ nghịch|hệ số tỉ lệ"),
        ("VI. Tỉ lệ thức", "Bài toán chia tỉ lệ (thực tế)", r"(công nhân|máy|người|đội|tổ).{0,120}(hoàn thành|làm xong|cày|gặt)|năng suất|hoàn thành .{0,60}trong \d+ (ngày|giờ)|trong \d+ (lít|kg)|tỉ lệ (với|thuận|nghịch).{0,200}(số|cây|học sinh|máy|người|ngày|công nhân|tiền|sách)"),
        ("VII. Đa thức", "Biểu thức đại số, giá trị biểu thức", r"bi[ểê]u thức đại s[ốô]|đơn thức|biểu thức (biểu thị|số)|giá trị (của )?biểu thức|viết biểu thức"),
        ("VII. Đa thức", "Đa thức một biến: thu gọn, sắp xếp, bậc, hệ số", r"đa thức|bậc của|hệ số (cao nhất|tự do)|thu gọn"),
        ("VII. Đa thức", "Cộng, trừ, nhân, chia đa thức", r"(tổng|hiệu|tích|thương|cộng|trừ|nhân|chia).{0,30}đa thức|đa thức.{0,40}(cộng|trừ|nhân|chia)|p\(x\) ?[+−-] ?q\(x\)|phép chia"),
        ("VII. Đa thức", "Nghiệm của đa thức", r"nghiệm"),
        ("VIII. Biến cố – XS", "Biến cố chắc chắn / không thể / ngẫu nhiên", r"biến cố|chắc chắn|không thể"),
        ("VIII. Biến cố – XS", "Xác suất của biến cố", r"xác suất"),
        ("IX. Quan hệ trong tam giác", "Quan hệ góc – cạnh đối diện", r"cạnh (lớn|nhỏ) nhất|góc (lớn|nhỏ) nhất|so sánh (các )?(góc|cạnh)|đối diện"),
        ("IX. Quan hệ trong tam giác", "Đường vuông góc, đường xiên", r"đường xiên|đường vuông góc|hình chiếu|khoảng cách"),
        ("IX. Quan hệ trong tam giác", "Bất đẳng thức tam giác", r"bất đẳng thức tam giác|độ dài (ba|3) cạnh|ba cạnh của (một )?tam giác"),
        ("IX. Quan hệ trong tam giác", "Trung tuyến, phân giác, đường cao, trọng tâm, đồng quy", r"trọng tâm|trung tuyến|trực tâm|đồng quy|đường cao"),
        ("X. Hình khối", "Hình hộp chữ nhật, hình lập phương", r"hình hộp|lập phương"),
        ("X. Hình khối", "Hình lăng trụ đứng", r"lăng trụ"),
        ("X. Hình khối", "Diện tích xung quanh, thể tích", r"thể tích|diện tích xung quanh"),
    ],
    "8": [
        ("Chung", "Tìm x", _TIMX),
        ("I. Đa thức", "Đơn thức, đơn thức đồng dạng", r"đơn thức"),
        ("I. Đa thức", "Đa thức: thu gọn, bậc, giá trị", r"đa thức|thu gọn|bậc của|giá trị (của )?đa thức"),
        ("I. Đa thức", "Nhân đa thức", r"nhân (đơn thức|đa thức)|thực hiện phép (tính|nhân)|khai triển"),
        ("I. Đa thức", "Chia đa thức cho đơn thức", r"chia (đa thức|đơn thức)|phép chia"),
        ("II. Hằng đẳng thức", "Hằng đẳng thức đáng nhớ", r"(chọn|khẳng định|thích hợp).{0,15}đ[ẳă]ng thức|biểu thức thích hợp|hằng đẳng thức|bình phương (của )?(một )?(tổng|hiệu)|lập phương|hiệu hai bình phương|tổng hai lập"),
        ("II. Hằng đẳng thức", "Phân tích đa thức thành nhân tử", r"nhân tử"),
        ("II. Hằng đẳng thức", "Rút gọn biểu thức, tính nhanh", r"rút gọn|tính nhanh|tính hợp l[íý]"),
        ("II. Hằng đẳng thức", "Chứng minh biểu thức không phụ thuộc biến / đẳng thức", r"không phụ thuộc|chứng minh (đẳng thức|rằng)"),
        ("II. Hằng đẳng thức", "Giá trị lớn nhất / nhỏ nhất", r"(giá trị )?(lớn|nhỏ) nhất"),
        ("III. Tứ giác", "Tứ giác, tổng các góc", r"tổng (các|4|bốn) góc|tứ giác lồi|tứ giác \w{4} có [^.\n]{0,40}(=|°)"),
        ("III. Tứ giác", "Hình thang, hình thang cân", r"hình thang"),
        ("III. Tứ giác", "Hình bình hành", r"bình hành"),
        ("III. Tứ giác", "Hình chữ nhật", r"hình chữ nhật"),
        ("III. Tứ giác", "Hình thoi", r"hình thoi"),
        ("III. Tứ giác", "Hình vuông", r"hình vuông"),
        ("IV. Thalès", "Định lí Thalès (thuận, đảo, hệ quả)", r"thal|ta-?lét|ta lét|(//|∥|song song với).{0,100}(tỉ số|độ dài|tính)"),
        ("IV. Thalès", "Đường trung bình của tam giác", r"đường trung bình"),
        ("IV. Thalès", "Tính chất đường phân giác", r"phân giác"),
        ("V. Dữ liệu", "Thu thập, phân loại dữ liệu (định tính/định lượng)", r"thống kê|phân (loại|nhóm)|dữ liệu|định tính|định lượng|thu thập"),
        ("V. Dữ liệu", "Biểu đồ (cột, cột kép, quạt, đoạn thẳng)", r"biểu đồ"),
        ("VI. Phân thức", "Phân thức: điều kiện xác định, giá trị", r"phân thức|điều kiện xác định|xác định khi|đkxđ"),
        ("VI. Phân thức", "Cộng, trừ, nhân, chia, rút gọn phân thức", r"(cộng|trừ|nhân|chia|rút gọn).{0,30}phân thức|(rút gọn|cho (hai )?biểu thức).{0,160}(≠|khác 0|điều kiện)"),
        ("VI. Phân thức", "Câu phụ: tìm x nguyên để biểu thức nguyên / thoả điều kiện", r"giá trị nguyên|x nguyên|số nguyên x|tìm (giá trị )?(của )?x để"),
        ("VII. PT & hàm số", "Giải phương trình bậc nhất một ẩn", r"phương trình"),
        ("VII. PT & hàm số", "Giải bài toán bằng cách lập phương trình", r"lập phương trình"),
        ("VII. PT & hàm số", "Hàm số, đồ thị, hệ số góc", r"f ?\(x\)|hàm số|đồ thị|hệ số góc|mặt phẳng tọa độ|mặt phẳng toạ độ"),
        ("VIII. Xác suất", "Xác suất của biến cố (lí thuyết, thực nghiệm)", r"xác suất|biến cố|kết quả thuận lợi"),
        ("IX. Đồng dạng", "Tam giác đồng dạng (các trường hợp)", r"đồng dạng|∽|∾|\b\w{3,4} ?[~øω] ?\w{3,4}\b"),
        ("IX. Đồng dạng", "Định lí Pythagore", r"(là|không là|không phải là) tam giác vuông|pythag|pi-?ta-?go|py-?ta-?go|pytago"),
        ("IX. Đồng dạng", "Ứng dụng đồng dạng đo đạc thực tế", r"(bóng|cây|tòa nhà|toà nhà|cột|chiều cao).{0,200}(đồng dạng|tỉ lệ)|(đồng dạng).{0,200}(bóng|cây|cột|chiều cao)"),
        ("X. Hình chóp", "Hình chóp tam giác đều, tứ giác đều", r"hình chóp|kim tự tháp"),
    ],
    "9": [
        ("Chung", "Tính giá trị biểu thức / thực hiện phép tính", _TINH),
        ("I. PT & hệ PT", "Phương trình bậc nhất hai ẩn, nghiệm", r"phương trình bậc nhất hai ẩn|cặp số .{0,40}nghiệm"),
        ("I. PT & hệ PT", "Giải hệ phương trình", r"hệ phương trình|giải hệ"),
        ("I. PT & hệ PT", "Giải bài toán bằng cách lập hệ phương trình", r"lập hệ|hoặc hệ phương trình"),
        ("II. BĐT – BPT", "Phương trình quy về bậc nhất (tích, chứa ẩn ở mẫu)", r"phương trình tích|chứa ẩn ở mẫu|điều kiện xác định|giải (các )?phương trình"),
        ("II. BĐT – BPT", "Bất đẳng thức, so sánh", r"\bcho [a-z] ?[<>≤≥] ?[a-z]\b|bất đẳng thức|chứng minh .{0,30}(≥|≤|>|<)"),
        ("II. BĐT – BPT", "Giải bất phương trình bậc nhất một ẩn", r"bất phương trình"),
        ("II. BĐT – BPT", "Toán thực tế lập bất phương trình", r"(ít nhất|nhiều nhất|tối đa|tối thiểu).{0,200}(bất phương trình|mua|tháng|ngày|câu|sản phẩm)"),
        ("III. Căn thức", "Căn bậc hai, căn bậc ba: tính, điều kiện xác định", r"\bv\d|\bvx\b|\d ?v\d|căn bậc (hai|ba)|√|∛|căn thức|có nghĩa|xác định khi"),
        ("III. Căn thức", "Rút gọn biểu thức chứa căn", r"rút gọn|cho (hai )?biểu thức|với x ?(≥|>)"),
        ("III. Căn thức", "Câu phụ của bài rút gọn (tìm x, so sánh, giá trị nguyên)", r"tìm (giá trị )?(của )?x để|giá trị nguyên|so sánh [a-z] với"),
        ("IV. Hệ thức lượng", "Tỉ số lượng giác của góc nhọn", r"tỉ số lượng giác|\b(sin|cos|tan|cot|cotg|tg)(?![a-zăâđêôơưàáảãạ])"),
        ("IV. Hệ thức lượng", "Giải tam giác vuông, hệ thức cạnh – góc", r"giải tam giác vuông|tam giác .{0,20}vuông"),
        ("IV. Hệ thức lượng", "Ứng dụng thực tế (đo chiều cao, khoảng cách, góc nghiêng)", r"góc (nâng|nghiêng|tạo bởi)|chiều cao|tia nắng|bóng|cột cờ|thang|máy bay|con diều|tòa nhà|toà nhà|ngọn|đỉnh tháp|dốc"),
        ("V. Đường tròn", "Đường tròn, dây, vị trí tương đối", r"đường tròn|dây cung|bán kính"),
        ("V. Đường tròn", "Chứng minh 3–4 điểm cùng thuộc một đường tròn", r"cùng (thuộc|nằm trên) (một )?đường tròn"),
        ("V. Đường tròn", "Tiếp tuyến", r"tiếp tuyến"),
        ("V. Đường tròn", "Độ dài cung, diện tích hình quạt, hình vành khuyên", r"độ dài (cung|đường tròn)|hình quạt|vành khuyên|diện tích hình tròn|chu vi (hình|đường) tròn"),
        ("VI. y = ax², PT bậc hai", "Hàm số y = ax², đồ thị parabol", r"parabol|y ?= ?ax|hàm số y"),
        ("VI. y = ax², PT bậc hai", "Giải phương trình bậc hai", r"phương trình bậc hai|biệt thức|Δ|delta"),
        ("VI. y = ax², PT bậc hai", "Định lí Viète", r"vi-?ét|viète|viet|x₁|x1 ?\+ ?x2"),
        ("Chung", "Giải bài toán bằng cách lập phương trình (bậc nhất ở kỳ I, bậc hai ở kỳ II)", r"lập phương trình"),
        ("VII. Tần số", "Bảng tần số, tần số tương đối, biểu đồ", r"tần số|mẫu số liệu|biểu đồ|ghép nhóm"),
        ("VIII. Xác suất", "Phép thử, không gian mẫu, xác suất của biến cố", r"xác suất|không gian mẫu|phép thử|biến cố"),
        ("IX. Nội tiếp", "Góc nội tiếp, tứ giác nội tiếp, đường tròn ngoại/nội tiếp", r"nội tiếp|ngoại tiếp"),
        ("IX. Nội tiếp", "Đa giác đều, phép quay", r"đa giác đều|phép quay|lục giác đều|ngũ giác đều"),
        ("X. Hình khối", "Hình trụ, hình nón, hình cầu", r"hình trụ|hình nón|hình cầu|khối cầu|bồn|thùng"),
        ("Chung", "Giá trị lớn nhất / nhỏ nhất, bài toán tối ưu thực tế", r"(giá trị )?(lớn|nhỏ) nhất|cao nhất|tối đa|tối thiểu|lợi nhuận"),
    ],
}

# Kết luận phải chứng minh trong BÀI HÌNH (lớp 7-9) — thống kê riêng.
KET_LUAN = [
    ("Hai tam giác bằng nhau", r"(△|∆|δ|tam giác) ?\w{3} ?= ?(△|∆|δ|tam giác)|hai tam giác .{0,30}bằng nhau"),
    ("Hai tam giác đồng dạng", r"đồng dạng|∽|∾"),
    ("Hai đoạn / hai góc bằng nhau", r"chứng minh:? ?[a-zđ]{2} ?= ?[a-zđ]{2}\b|góc .{0,20}bằng|\w{2} ?= ?\w{2}\b"),
    ("Song song", r"song song|//|∥"),
    ("Vuông góc", r"vuông góc|⊥"),
    ("Thẳng hàng", r"thẳng hàng"),
    ("Tam giác / tứ giác đặc biệt", r"là (hình|tam giác) ?(thang|bình hành|chữ nhật|thoi|vuông|cân|đều)|tam giác .{0,12}(cân|đều|vuông)"),
    ("Trung điểm", r"trung điểm"),
    ("Tia phân giác", r"phân giác"),
    ("Cùng thuộc một đường tròn", r"cùng (thuộc|nằm trên)"),
    ("Tiếp tuyến", r"tiếp tuyến"),
    ("Hệ thức (tích đoạn thẳng)", r"\w{2} ?[.·] ?\w{2} ?= ?\w{2} ?[.·] ?\w{2}|\w{2}\s?2 ?= ?\w{2} ?[.·]"),
    ("Đồng quy", r"đồng quy"),
]

# ─────────────────── TOÁN LỜI VĂN: tách theo BỐI CẢNH (dùng chung 6-9) ───────────────────
# Một bài được coi là "lời văn" khi khớp ít nhất một bối cảnh dưới đây. Thứ tự = thứ tự in ra.
LOI_VAN: list[tuple[str, str]] = [
    ("Chuyển động: vận tốc – quãng đường – thời gian",
     r"vận tốc|km ?/ ?h|km ?/ ?giờ|quãng đường|khởi hành|tốc độ|đi từ [a-z] đến [a-z]|gặp nhau"),
    ("Chuyển động trên dòng nước (ca nô, xuôi – ngược dòng)",
     r"xuôi dòng|ngược dòng|dòng nước|ca ?nô|nước yên lặng|bến sông"),
    ("Làm chung – làm riêng (hai đội, hai vòi nước)",
     r"làm chung|làm riêng|cùng làm|làm một mình|một mình .{0,40}(xong|hoàn thành)|vòi nước|hai vòi|chảy (vào|đầy)|đầy bể|(hoàn thành|làm xong) (xong )?công việc"),
    ("Năng suất – kế hoạch (dự định/thực tế, vượt mức, cải tiến kĩ thuật)",
     r"năng suất|theo kế hoạch|(?<!phong trào )(?<!phong trào \")kế hoạch(?! nhỏ)|vượt (mức|kế hoạch)|cải tiến (kĩ|kỹ) thuật|mỗi (ngày|giờ) (làm|sản xuất|may|dệt|đóng|trồng)|chi tiết máy|xưởng|phân xưởng|xí nghiệp"),
    ("Mua bán: giá niêm yết, khuyến mãi, giảm giá %",
     r"giá niêm yết|khuyến m[ãạ]i|giảm giá|chiết khấu|giảm \d+(,\d+)? ?%|giá (gốc|bìa)|ưu đãi"),
    ("Mua bán: tính tiền, số lượng hàng mua được (không %)",
     r"\d ?(nghìn |ngàn )?đồng|triệu đồng|thanh toán|hóa đơn|hoá đơn|\bmua\b|giá (bán|tiền|vé|mỗi)"),
    ("Lợi nhuận: giá nhập – giá bán, lãi/lỗ",
     r"giá nhập|giá vốn|lợi nhuận|doanh thu|lãi \d+(,\d+)? ?%|bán lỗ|\blỗ\b|tiền lời"),
    ("Lãi suất ngân hàng, gửi tiết kiệm, đầu tư",
     r"lãi suất|tiết kiệm|gửi (vào )?ngân hàng|kì hạn|kỳ hạn|đầu tư|cả gốc (lẫn|và) lãi"),
    ("Tăng – giảm phần trăm theo thời gian (dân số, sản lượng năm ngoái/năm nay)",
     r"năm (ngoái|nay|trước)|dân số|tăng (thêm )?\d+(,\d+)? ?%|vượt \d+(,\d+)? ?%|so với (năm|tháng|kì|kỳ) (trước|ngoái)"),
    ("Hình học thực tế: vườn, ruộng, sân, phòng (chu vi – diện tích – kích thước)",
     r"mảnh (vườn|đất|ruộng)|khu (vườn|đất)|thửa ruộng|miếng đất|sân (trường|chơi|vận động|bóng)|căn phòng|nền nhà|lát (gạch|nền)|hàng rào|bồn hoa|chiều dài.{0,60}chiều rộng|chiều rộng.{0,60}chiều dài"),
    ("Hình khối thực tế: bể, thùng, hộp, lều, cốc (thể tích – diện tích xung quanh)",
     r"(bể|thùng|hộp|lều|cốc|\blon\b|bồn|bình|chậu|téc|bồn chứa).{0,160}(thể tích|dung tích|diện tích xung quanh|\blít\b|m3|cm3|dm3|m³|cm³)"
     r"|(thể tích|dung tích|diện tích xung quanh).{0,120}(bể|thùng|hộp|lều|cốc|lon|bồn|bình)|kim tự tháp|lều trại"),
    ("Đo đạc gián tiếp: bóng cây, góc nâng, thang dựa tường, chiều cao tháp",
     r"bóng (của )?(cây|cột|tòa|toà|người|tháp)|tia nắng|góc (nâng|nghiêng|tạo bởi)|cột cờ|ngọn (cây|hải đăng|tháp|núi)|con diều|thang (dựa|tựa|nghiêng)|chiều cao (của )?(cây|tòa|toà|tháp|cột|ngôi nhà)|máy bay|khinh khí cầu|con dốc"),
    ("Bài toán hai loại (xe lớn/nhỏ, vé loại I/II, hai loại hàng)",
     r"(hai|2) loại|loại (i|1)\b.{0,120}loại (ii|2)\b|xe (cỡ )?(lớn|nhỏ)|\d+ chỗ( ngồi)?\b"),
    ("Tìm số (chữ số, hai số, tổng – hiệu – tỉ số)",
     r"chữ số hàng|số có hai chữ số|tổng (của )?hai số|hiệu (của )?hai số|tỉ số (của )?hai số|hai số tự nhiên"),
    ("Chia theo tỉ lệ (tỉ lệ thuận/nghịch: máy cày, công nhân, chia tiền thưởng)",
     r"tỉ lệ (với|thuận|nghịch).{0,200}(máy|người|thợ|công nhân|đội|lớp|học sinh|cây|tiền|sách|ngày|giờ|kg|lít)"
     r"|theo tỉ lệ|máy cày|cánh đồng|(năng suất|công suất) (các|mỗi) máy"),
    ("Phân số/phần trăm của một số (số trang sách, học sinh các khối)",
     r"(đọc|còn lại|đã đọc).{0,40}số trang|số trang .{0,20}(còn lại|đã đọc)|ngày thứ (nhất|hai|ba) .{0,60}(đọc|làm|được|bán)|số (sách|trang|học sinh) còn lại|(khối|lớp) (6|7|8|9)[a-z]? .{0,50}(bằng|chiếm)|chiếm \d+(,\d+)? ?% (tổng|số)"),
    ("Chia đều, xếp hàng (ƯCLN – BCNN)",
     r"xếp (thành )?(các )?hàng|chia đều|vừa đủ|đều (thừa|thiếu)|không (thừa|dư) (ai|người|bạn)|(nhiều|ít) nhất .{0,80}(nhóm|tổ|phần|đĩa|túi|hàng|khay)|(nhóm|tổ|phần|đĩa|túi|khay) .{0,80}(nhiều|ít) nhất"),
    ("Điểm thi: trả lời đúng/sai (cộng – trừ điểm), điểm trung bình hệ số",
     r"(số câu|bao nhiêu câu).{0,80}(trả lời )?(đúng|sai)|(đúng|sai) .{0,40}(bị trừ|được cộng)|bị trừ \d|hệ số (2|3|hai|ba)|điểm trung bình (môn|cả năm|của)"),
    ("Nhiệt độ, độ cao – độ sâu so với mực nước biển (số nguyên)",
     r"nhiệt độ|°c|độ c\b|mực nước biển|dưới (mặt|mực) nước|tầng hầm|độ sâu"),
    ("Cước phí, tiền điện – nước, taxi (tính theo bậc/km)",
     r"taxi|cước|tiền điện|tiền nước|số điện|kwh|kw ?h|bậc (1|i|thang)|gói cước|km đầu tiên"),
    ("Hoá – lý: dung dịch, nồng độ, khối lượng riêng, hợp kim",
     r"dung dịch|nồng độ|khối lượng riêng|nhiệt lượng|hợp kim|axit|gam muối|lít nước biển"),
    ("Tính tuổi", r"\b\d+ tuổi\b|(bố|mẹ|ông|bà|anh|chị|em|con|cha) .{0,40}\btuổi\b(?! đời)"),
]
# Gắn THÊM (không tự thành bài lời văn): bài lời văn có hỏi lớn nhất/nhỏ nhất.
TOI_UU_LV = ("(kèm) Tối ưu: hỏi lớn nhất / nhỏ nhất / nhiều nhất / ít nhất",
             r"(lớn|nhỏ|cao|thấp) nhất|tối (đa|thiểu)|nhiều nhất|ít nhất")

# ─────────────────── TIỂU DẠNG của một số dạng lớn (theo TÊN dạng cha) ───────────────────
# Chỉ xét trên câu đã mang dạng cha. Câu không khớp tiểu dạng nào rơi vào "(chưa rõ tiểu dạng)".
_SUB_TIMX = [
    ("theo điều kiện ước – bội – chia hết", r"ước|bội|chia hết|⋮|ưcln|bcnn"),
    ("có giá trị tuyệt đối", r"\||giá trị tuyệt đối"),
    ("dạng tích bằng 0", r"\)\s*\.?\s*\(.{0,40}= ?0\b|tích .{0,20}bằng 0"),
    ("trong tỉ lệ thức / dãy tỉ số", r"tỉ lệ thức|dãy tỉ số|x ?: ?\d+ ?= ?y|x ?/ ?\d+ ?= ?y"),
    ("tìm x, y (hai ẩn) / tìm cặp số", r"tìm (các )?(cặp )?(số )?(nguyên |tự nhiên )?x ?, ?y"),
    ("có luỹ thừa / căn bậc hai", r"lu[ỹỹ] thừa|√|căn|x ?\^|\^ ?x"),
]
SUB: dict[str, list[tuple[str, str]]] = {
    "Tìm x": _SUB_TIMX,
    "Thực hiện phép tính / tính hợp lí": [
        ("tính hợp lí / tính nhanh (giao hoán, kết hợp, phân phối)", r"hợp l[íý]|tính nhanh|một cách hợp"),
        ("biểu thức nhiều tầng ngoặc, thứ tự thực hiện", r"\[|\{|thứ tự thực hiện"),
    ],
    "Rút gọn biểu thức chứa căn": [
        ("tính giá trị biểu thức tại x = …", r"tính giá trị (của )?(biểu thức )?[a-z]\b.{0,15}(khi|tại) x"),
        ("rút gọn / chứng minh P = …", r"rút gọn|chứng minh (rằng )?[a-z] ?="),
        ("tìm x để P = số", r"tìm (giá trị (của )?|các giá trị (của )?)?x để [a-z] ?="),
        ("tìm x để P < / > số (bất phương trình)", r"(tìm (giá trị (của )?|các giá trị (của )?)?x để [a-z] ?[<>≤≥])|để [a-z] (âm|dương|< ?0|> ?0)"),
        ("so sánh P với một số", r"so sánh [a-z] (với|và)"),
        ("tìm x nguyên để P nguyên", r"giá trị nguyên|x nguyên|số nguyên x|nhận giá trị nguyên"),
        ("GTLN / GTNN của P", r"(giá trị )?(lớn|nhỏ) nhất"),
    ],
    "Câu phụ của bài rút gọn (tìm x, so sánh, giá trị nguyên)": [
        ("tìm x để P = số", r"x để [a-z] ?="),
        ("tìm x để P < / > số", r"x để [a-z] ?[<>≤≥]|để [a-z] (âm|dương)"),
        ("so sánh P với một số", r"so sánh"),
        ("giá trị nguyên", r"nguyên"),
    ],
    "Câu phụ: tìm x nguyên để biểu thức nguyên / thoả điều kiện": [
        ("tìm x nguyên để biểu thức nhận giá trị nguyên", r"giá trị nguyên|x nguyên|số nguyên x"),
        ("tìm x để biểu thức = / < / > số", r"x để [a-z] ?[=<>≤≥]|để [a-z] (âm|dương|có giá trị)"),
        ("tính giá trị biểu thức tại x = …", r"tính giá trị .{0,30}(khi|tại) x"),
    ],
    "Giá trị lớn nhất / nhỏ nhất, bài toán tối ưu thực tế": [
        ("tối ưu trong bài thực tế (lợi nhuận, diện tích, chi phí…)",
         r"lợi nhuận|chi phí|doanh thu|đồng|mảnh|diện tích|thể tích|sản phẩm|khách|phòng|\bvé\b|mét|\bm2\b|m²|tiền"),
        ("GTLN / GTNN của biểu thức đại số", r"(giá trị )?(lớn|nhỏ) nhất của (biểu thức|[a-z]\b)"),
        ("chứng minh bất đẳng thức", r"chứng minh .{0,60}(≥|≤|>|<)"),
    ],
    "Giá trị lớn nhất / nhỏ nhất": [
        ("GTLN / GTNN của biểu thức đại số", r"(lớn|nhỏ) nhất của"),
        ("tối ưu trong bài thực tế", r"lợi nhuận|chi phí|diện tích|đồng|tiền|sản phẩm"),
    ],
    "Phân tích đa thức thành nhân tử": [
        ("dùng để tìm x / giải phương trình", r"tìm x|= ?0"),
        ("dùng để tính nhanh / tính giá trị", r"tính (nhanh|giá trị|hợp l)"),
    ],
}
CHUA_RO = "(chưa rõ tiểu dạng)"

# ── Tiểu dạng LỚP 9 (01/10/2026, Thầy: "tách dạng sâu hơn") ──
SUB.update({
    "Giải hệ phương trình": [
        ("hệ hai PT bậc nhất hai ẩn (thế / cộng đại số)", r"giải (các )?hệ|hệ phương trình sau"),
        ("hệ quy về bậc nhất (khai triển có xy, đặt ẩn phụ 1/x…)", r"đặt ẩn|ẩn phụ|1 ?/ ?\(?x|√|\bvx\b|\bxy\b"),
        ("nằm trong bài lập hệ (lời văn)", r"lập hệ|hoặc hệ phương trình"),
        ("có tham số m", r"\bm\b|tham số"),
    ],
    "Phương trình quy về bậc nhất (tích, chứa ẩn ở mẫu)": [
        ("phương trình tích", r"\)\s*\.?\s*\(|phương trình tích"),
        ("phương trình chứa ẩn ở mẫu", r"ẩn ở mẫu|điều kiện xác định|đkxđ|x ?≠"),
        ("phương trình bậc nhất một ẩn (khai triển, chuyển vế)", r"^(?![\s\S]*(\)\s*\.?\s*\(|ẩn ở mẫu|x ?≠|phương trình tích))[\s\S]*giải (các )?phương trình"),
    ],
    "Giải bất phương trình bậc nhất một ẩn": [
        ("biểu diễn tập nghiệm trên trục số", r"trục số|biểu diễn (tập )?nghiệm"),
        ("tìm nghiệm nguyên lớn nhất / nhỏ nhất", r"nghiệm nguyên|số nguyên (lớn|nhỏ) nhất|giá trị nguyên"),
        ("giải BPT (có mẫu, khai triển ngoặc)", r"giải (các )?bất phương trình"),
    ],
    "Tỉ số lượng giác của góc nhọn": [
        ("tính tỉ số lượng giác, so sánh / sắp xếp", r"tính (các )?tỉ số lượng giác|so sánh|sắp xếp|giá trị (của )?(sin|cos|tan|cot)"),
        ("tính cạnh, góc (giải tam giác vuông)", r"tính (độ dài|cạnh|góc|số đo)|giải tam giác"),
        ("tính / rút gọn biểu thức lượng giác", r"(sin|cos) ?\^? ?2|(sin|cos)2|biểu thức"),
        ("chứng minh hệ thức lượng giác", r"chứng minh[^.\n]{0,80}\b(sin|cos|tan|cot)(?![a-zăâđêôơư])"),
    ],
    "Đường tròn, dây, vị trí tương đối": [
        ("vị trí tương đối (điểm, đường thẳng, hai đường tròn)", r"vị trí tương đối|tiếp xúc|không giao|cắt nhau tại hai"),
        ("dây và khoảng cách từ tâm đến dây", r"\bdây\b|khoảng cách từ (tâm|o)"),
        ("bài hình tổng hợp có chứng minh", r"chứng minh"),
    ],
    "Tiếp tuyến": [
        ("chứng minh một đường thẳng là tiếp tuyến", r"chứng minh .{0,60}tiếp tuyến"),
        ("tính chất hai tiếp tuyến cắt nhau", r"hai tiếp tuyến|các tiếp tuyến"),
        ("tính độ dài đoạn tiếp tuyến / góc", r"tính .{0,60}(độ dài|góc|tiếp tuyến)"),
    ],
    "Độ dài cung, diện tích hình quạt, hình vành khuyên": [
        ("độ dài cung, chu vi đường tròn", r"độ dài (cung|đường tròn)|chu vi"),
        ("diện tích hình tròn, hình quạt", r"hình quạt|diện tích hình tròn"),
        ("hình vành khuyên", r"vành khuyên"),
    ],
    "Giải phương trình bậc hai": [
        ("giải PT bậc hai (công thức nghiệm, nhẩm nghiệm)", r"giải (các )?phương trình"),
        ("tham số m (có nghiệm, hai nghiệm phân biệt…)", r"\bm\b|tham số"),
    ],
    "Định lí Viète": [
        ("không giải PT, tính biểu thức của hai nghiệm", r"không giải|x ?1|x₁|biểu thức"),
        ("tìm hai số biết tổng và tích", r"hai số .{0,40}tổng|tổng .{0,30}tích"),
        ("có tham số m", r"\bm\b|tham số"),
    ],
    "Bảng tần số, tần số tương đối, biểu đồ": [
        ("lập bảng tần số / tần số tương đối", r"lập bảng|bảng tần số"),
        ("đọc bảng, tính tần số tương đối, tỉ lệ %", r"tần số tương đối|tỉ lệ|phần trăm|%"),
        ("bảng / biểu đồ tần số ghép nhóm", r"ghép nhóm|\[\s*\d+\s*;\s*\d+\s*\)"),
        ("vẽ / đọc biểu đồ", r"biểu đồ"),
    ],
    "Phép thử, không gian mẫu, xác suất của biến cố": [
        ("liệt kê không gian mẫu, kết quả thuận lợi", r"không gian mẫu|kết quả có thể|liệt kê|thuận lợi"),
        ("một hành động: xúc xắc, rút thẻ, lấy bóng", r"xúc xắc|thẻ|quả bóng|viên bi|đồng xu|rút ngẫu nhiên|lấy ngẫu nhiên"),
        ("hai hành động / chọn hai đối tượng", r"hai (lần|đồng xu|con xúc xắc|bạn|học sinh)|lần lượt|2 lần|đồng thời|liên tiếp"),
    ],
    "Góc nội tiếp, tứ giác nội tiếp, đường tròn ngoại/nội tiếp": [
        ("chứng minh tứ giác nội tiếp / 4 điểm cùng thuộc đường tròn", r"tứ giác .{0,40}nội tiếp|cùng (thuộc|nằm trên)"),
        ("góc nội tiếp, tính số đo góc", r"góc nội tiếp|số đo"),
        ("đường tròn ngoại/nội tiếp tam giác, tính bán kính", r"(ngoại|nội) tiếp (tam giác|∆|△)|bán kính"),
    ],
    "Hình trụ, hình nón, hình cầu": [
        ("hình trụ", r"hình trụ|\btrụ\b"),
        ("hình nón", r"hình nón|\bnón\b"),
        ("hình cầu", r"hình cầu|khối cầu|quả bóng|quả cầu"),
    ],
    "Căn bậc hai, căn bậc ba: tính, điều kiện xác định": [
        ("tính, rút gọn biểu thức số có căn", r"tính|rút gọn|thực hiện"),
        ("điều kiện xác định của căn", r"xác định|có nghĩa"),
        ("căn bậc ba", r"căn bậc ba|∛"),
        ("giải phương trình chứa căn", r"phương trình"),
    ],
})


def _bo_ma(lop: str) -> list[tuple[str, str, str]]:
    """Bộ mã đầy đủ của khối: dạng theo chương + câu nâng cao (6-8) + toán thực tế (6-7).
    Lớp 8 đã có dạng GTLN/GTNN ở chương II nên không lấy lại mục đó ở phần nâng cao."""
    ma = list(DANG[lop])
    if lop in "678":
        ma += [x for x in _NC if not (lop == "8" and "lớn nhất" in x[1])]
    if lop in "67":
        ma.append(_THUC_TE)
    return ma


# ─────────────────────────── TÁCH KHỐI ĐỀ & CÂU ───────────────────────────
_CAU = re.compile(r"^\s{0,8}(?:câu|bài)\s*(\d{1,2}|[ivx]{1,4})\b\s*[.:)(/-]?", re.I | re.M)
_CAU_DAU = re.compile(r"^\s{0,8}(?:câu|bài)\s*(?:1|i)\b\s*[.:)(/-]?\s*\S", re.I)
_HET = re.compile(r"^[\s\-–—_.*=]*h[ếe]t[\s\-–—_.*=!]*$", re.I)
_DUNG = re.compile(r"hướng dẫn chấm|đáp án|biểu điểm|\bhdc\b|hướng dẫn giải|lời giải", re.I)
# tiêu đề phần chấm viết thường / OCR sai dấu — dừng khối đề cả khi dòng KHÔNG in hoa
# đầu đề thứ hai (mã đề khác) dính ngay sau câu cuối khi file thiếu dòng "Hết"
_DE_MOI = re.compile(r"đ[ềèệ] ki[ểếề]m tra (giữa|cuối|học)|mã đ[ềệè] \d{3}|^\s*ubnd\b|^\s*phòng (gd|giáo dục)", re.I)
_DUNG_MO = re.compile(r"hướng d[ẫaáã]n ch[ấaảá]m|biểu đi[ểe]m|đáp án (và|&|-) ?(biểu|hướng)|^\s*đáp án\s*[:.]?\s*$|^\s*(i|1)\.\s*đáp án", re.I)
_BO_QUA = re.compile(r"ma trận|bản đặc tả|khung ma trận|đặc tả", re.I)
_TN = re.compile(r"trắc nghiệm", re.I)
# bảng đáp án trắc nghiệm ("Câu | 1 2 3 4 …" / "Đáp án A C B …") — đề thiếu dòng "Hết" thì đây là mốc dừng
_BANG_DA = re.compile(r"^\s*(câu|đáp án)\s*[|:]?\s*1\s+\|?\s*2\s+\|?\s*3\b|^\s*đáp án\s*[|:]?\s*[abcd]\s+[abcd]\s", re.I)
_TL = re.compile(r"tự luận", re.I)


# Font Symbol (MathType) nằm ở vùng riêng U+F020–F0FF: nửa dưới trùng ASCII, nửa trên theo bảng Symbol.
_KI_HIEU = {0xCE: "∈", 0xCF: "∉", 0xA3: "≤", 0xB3: "≥", 0xB9: "≠", 0xB4: "×", 0xB8: "÷", 0xB0: "°",
            0xD7: "·", 0xA5: "ℕ", 0xDE: "⇒", 0xDB: "⇔", 0xD0: "∠", 0xB1: "±", 0xBA: "≡", 0xE6: "(", 0xF6: ")"}
_PUA = {c: (chr(c - 0xF000) if c - 0xF000 < 0x7F else _KI_HIEU.get(c - 0xF000, " "))
        for c in range(0xF020, 0xF100)}


def chuan(t: str) -> str:
    """Chữ thường, gộp khoảng trắng; đưa chữ toán nghiêng 𝑥 → x (pdftotext hay nhân đôi 𝑥𝑥) và
    kí hiệu font Symbol vùng riêng (\\uf0ce…) về kí tự thật."""
    t = unicodedata.normalize("NFKC", t)
    t = t.translate(_PUA)
    t = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", t)     # kí tự điều khiển — Excel không nhận
    t = re.sub(r"\b([xyz])\1\b", r"\1", t)
    return re.sub(r"[ \t]+", " ", t.lower())


def khoi_de(text: str) -> list[tuple[str, str]]:
    """[(phan, dòng)] của KHỐI ĐỀ đầu tiên; phan = 'TN' | 'TL' | '?'."""
    ra: list[tuple[str, str]] = []
    trong = False
    bo = False            # đang ở ma trận / đặc tả
    phan = "?"
    for dong in text.splitlines():
        d = dong.strip()
        hoa = d.upper() == d and len(d) > 6
        if not trong:
            if hoa and _BO_QUA.search(d):
                bo = True
            if _TN.search(d) and len(d) < 120:
                phan, bo = "TN", False
            elif _TL.search(d) and len(d) < 120 and not bo:
                phan = "TL"
            if _CAU_DAU.match(dong) and not bo:
                trong = True
            elif _CAU_DAU.match(dong) and bo and len(d) > 25:
                trong, bo = True, False           # đề đặt ngay sau ma trận, không tiêu đề
            else:
                continue
        # đang trong đề
        if (_HET.match(d) or (hoa and _DUNG.search(d)) or (hoa and _BO_QUA.search(d)) or _BANG_DA.match(dong)
                or (len(d) < 90 and _DUNG_MO.search(d)) or (len(ra) > 20 and _DE_MOI.search(d))):
            break
        if _TN.search(d) and len(d) < 120:
            phan = "TN"
        elif _TL.search(d) and len(d) < 120:
            phan = "TL"
        ra.append((phan, dong))
    return ra


def tach_cau(dong_de: list[tuple[str, str]]) -> list[dict]:
    cau: list[dict] = []
    for phan, dong in dong_de:
        m = _CAU.match(dong)
        if m or not cau:
            cau.append({"so": m.group(1) if m else "?", "phan": phan, "text": dong})
        else:
            cau[-1]["text"] += "\n" + dong
    for c in cau:
        c["text"] = chuan(c["text"])
        if c["phan"] == "?":
            c["phan"] = "TN" if re.search(r"\ba\s*[.)].{0,200}\bb\s*[.)].{0,200}\bc\s*[.)]", c["text"], re.S) else "TL"
        # điểm ghi ngay ở đầu câu/bài — KHÔNG lấy "(7,0 điểm)" của tiêu đề phần tự luận dính vào
        m = re.search(r"\(\s*(\d+(?:[,.]\d+)?)\s*(?:điểm|đ)\s*\)", c["text"].split("\n")[0][:80])
        c["diem"] = float(m.group(1).replace(",", ".")) if m else None
    return cau


# ─────────────────────────── ĐỌC KHO ───────────────────────────
_TRUONG = re.compile(r"(?:truong|phong-gddt|phong|cum)-(.+?)-ha-noi$")


def ten_de(stem: str) -> tuple[str, str]:
    m = re.search(r"nam-(\d{4})-(\d{4})", stem)
    nam = f"{m.group(1)}-{m.group(2)}" if m else "?"
    t = _TRUONG.search(stem)
    return nam, (t.group(1).replace("-", " ").title() if t else stem[:60])


def doc_kho(lop: str) -> list[dict]:
    de = []
    for f in sorted((TXT / f"lop-{lop}").rglob("*.txt")):
        rel = f.relative_to(TXT)
        ky = next((KY_DIR[p] for p in rel.parts if p in KY_DIR), None)
        pdf = DE / rel.with_suffix(".pdf")
        if not ky or not pdf.exists():          # đề đã tách sang de-thi-lech-kntt ⇒ bỏ
            continue
        raw = f.read_text(encoding="utf-8", errors="ignore")
        nguon = "ocr" if raw.startswith("#NGUON:ocr") else "text"
        cau = tach_cau(khoi_de(raw))
        nam, truong = ten_de(f.stem)
        # Không tách được khối đề (OCR vỡ / bố cục lạ) ⇒ KHÔNG đưa vào thống kê, chỉ liệt kê
        # (dùng cả file thì dính ma trận + đáp án, làm phồng tần suất).
        de.append({"file": str(pdf.relative_to(ROOT)), "ky": ky, "nam": nam, "truong": truong,
                   "nguon": nguon, "cau": cau if len(cau) >= 3 else [], "loi": len(cau) < 3})
    return de


def gan_dang(lop: str, de: list[dict]) -> None:
    rx = [(ch, ten, re.compile(p, re.I)) for ch, ten, p in _bo_ma(lop)]
    kl = [(ten, re.compile(p, re.I)) for ten, p in KET_LUAN]
    lv = [(ten, re.compile(p, re.I)) for ten, p in LOI_VAN]
    tu = re.compile(TOI_UU_LV[1], re.I)
    sub = {cha: [(t, re.compile(p, re.I)) for t, p in ds] for cha, ds in SUB.items()}
    for d in de:
        for c in d["cau"]:
            c["dang"] = [(ch, ten) for ch, ten, r in rx if r.search(c["text"])]
            c["loi_van"] = [ten for ten, r in lv if r.search(c["text"])]
            if (any(t.startswith("Hình khối") for t in c["loi_van"])
                    and not re.search(r"mảnh|khu (vườn|đất)|thửa|sân|căn phòng|nền nhà|rào", c["text"])):
                c["loi_van"] = [t for t in c["loi_van"] if not t.startswith("Hình học thực tế")]
            if c["loi_van"] and tu.search(c["text"]):
                c["loi_van"].append(TOI_UU_LV[0])
            c["sub"] = {}
            for _, ten in c["dang"]:
                if ten in sub:
                    c["sub"][ten] = [t for t, r in sub[ten] if r.search(c["text"])] or [CHUA_RO]
            c["ket_luan"] = []
            if lop != "6" and re.search(_CM_HINH, c["text"]) and re.search(
                    r"tam giác|tứ giác|hình (thang|bình hành|chữ nhật|thoi|vuông)|đường tròn|△|∆|đường thẳng|\btia\b|\bgóc\b",
                    c["text"]):
                for cm in re.findall(r"chứng (?:minh|tỏ)[^\n]{0,120}", c["text"]):
                    c["ket_luan"] += [ten for ten, r in kl if r.search(cm)]


# ─────────────────────────── XUẤT EXCEL ───────────────────────────
def xuat(lop: str, de: list[dict], dest: Path) -> dict:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    dam = Font(bold=True)
    nen = PatternFill("solid", fgColor="DDEBF7")
    nen_ch = PatternFill("solid", fgColor="F2F2F2")
    vien = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
    gon = Alignment(wrap_text=True, vertical="top")

    def bang(ws, hang0, tieu_de, rows, rong):
        for j, h in enumerate(tieu_de, 1):
            c = ws.cell(hang0, j, h); c.font = dam; c.fill = nen; c.alignment = gon; c.border = vien
        for i, r in enumerate(rows, hang0 + 1):
            for j, v in enumerate(r, 1):
                c = ws.cell(i, j, v); c.alignment = gon; c.border = vien
        for j, w in enumerate(rong, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
        ws.freeze_panes = ws.cell(hang0 + 1, 1)

    theo_ky = {k: [d for d in de if d["ky"] == k and not d["loi"]] for k in KY_THU_TU}
    loi_ky = Counter(d["ky"] for d in de if d["loi"])
    thu_tu_dang = [(ch, ten) for ch, ten, _ in _bo_ma(lop)]

    # ── Tổng quan
    ws = wb.active; ws.title = "Tổng quan"
    ws["A1"] = f"THỐNG KÊ DẠNG BÀI TRONG ĐỀ KIỂM TRA TOÁN {lop} — HÀ NỘI, KNTT"; ws["A1"].font = Font(bold=True, size=14)
    ghi = [
        "Nguồn: đề thi toanmath.com (Hà Nội, chương trình 2018), đã BỎ các đề lệch tiến độ/bộ sách KNTT.",
        "Mỗi câu/bài trong đề được gắn dạng TỰ ĐỘNG theo từ khoá; một bài tự luận nhiều ý có thể mang nhiều dạng.",
        "\"% số đề\" = tỉ lệ đề của kỳ đó có ít nhất một câu thuộc dạng — con số chính để biết dạng nào hay ra.",
        "Đề scan được đọc bằng OCR tiếng Việt: chữ đúng, công thức hay vỡ ⇒ dạng chỉ nhận ra qua lời đề có thể bị sót.",
        "Chương \"Chung\" (tính hợp lí, tìm x…) thuộc chương đang học của kỳ đó.",
        "ĐỘ TIN CẬY (soát tay 01/10/2026, 60 cặp câu–dạng chọn ngẫu nhiên, 15 cặp/khối): ~52/60 đúng (~87%). "
        "Lỗi hay gặp: bài tự luận nhiều ý mang cả dạng của ý khác; câu OCR vỡ chữ bị sót dạng. "
        "Con số % là để so dạng NHIỀU/ÍT, không dùng như số đếm chính xác.",
        "TIỂU DẠNG (dòng ↳) và TOÁN LỜI VĂN theo bối cảnh: soát tay 24 cặp ngẫu nhiên, ~21/24 đúng (~87%). "
        "Tiểu dạng của \"Tìm x\" phần lớn rơi vào \"(chưa rõ tiểu dạng)\" vì công thức trong đề bị vỡ khi đọc máy — "
        "không đoán bừa.",
    ]
    for i, g in enumerate(ghi, 3):
        ws.cell(i, 1, "• " + g).alignment = Alignment(wrap_text=True)
    rows = []
    for k in KY_THU_TU:
        ds = theo_ky[k]
        rows.append([k, len(ds), sum(d["nguon"] == "text" for d in ds), sum(d["nguon"] == "ocr" for d in ds),
                     sum(len(d["cau"]) for d in ds), loi_ky[k],
                     ", ".join(f"{n}: {c}" for n, c in sorted(Counter(d["nam"] for d in ds).items()))])
    bang(ws, 12, ["Kỳ", "Số đề dùng thống kê", "Có lớp chữ", "OCR (scan)", "Số câu/bài tách được",
                  "Đề KHÔNG tách được (bỏ ra)", "Theo năm học"], rows, [10, 11, 12, 12, 14, 14, 60])
    ws.column_dimensions["A"].width = 12
    for i in range(3, 10):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)
        ws.row_dimensions[i].height = 30

    xanh = PatternFill("solid", fgColor="C6EFCE")
    vang = PatternFill("solid", fgColor="FFF2CC")
    nhat = Font(italic=True, color="555555")

    def pt(n, ds):
        return round(100 * n / len(ds)) if ds else None

    def so_de(ds, dk):
        """Số đề có ít nhất một câu thoả dk(câu)."""
        return sum(any(dk(c) for c in d["cau"]) for d in ds)

    def vi_du(cau, uu_tien_it_dang=True):
        vd = sorted(cau, key=lambda x: (x[0]["nguon"] != "text",
                                        len(x[1]["dang"]) if uu_tien_it_dang else 0,
                                        abs(len(x[1]["text"]) - 240)))
        if not vd:
            return ""
        d0, c0 = vd[0]
        return f"[{d0['truong']} {d0['nam']}] " + re.sub(r"\s+", " ", c0["text"])[:280]

    def to_mau(ws, hang, cot_tu, cot_den):
        for j in range(cot_tu, cot_den + 1):
            v = ws.cell(hang, j).value
            if isinstance(v, (int, float)) and v >= 50:
                ws.cell(hang, j).font = dam; ws.cell(hang, j).fill = xanh
            elif isinstance(v, (int, float)) and v >= 20:
                ws.cell(hang, j).fill = vang

    def ds_sub(ten):
        return [t for t, _ in SUB.get(ten, [])] + ([CHUA_RO] if ten in SUB else [])

    # ── Cả năm: dạng × kỳ (tiểu dạng ngay dưới dạng cha)
    ws = wb.create_sheet("Cả năm")
    rows, la_sub = [], []
    for ch, ten in thu_tu_dang:
        rows.append([ch, ten] + [pt(so_de(theo_ky[k], lambda c: (ch, ten) in c["dang"]), theo_ky[k]) for k in KY_THU_TU])
        la_sub.append(False)
        for st in ds_sub(ten):
            r = ["", "      ↳ " + st] + [pt(so_de(theo_ky[k], lambda c, st=st: st in c["sub"].get(ten, [])), theo_ky[k])
                                        for k in KY_THU_TU]
            if any(r[2:]):
                rows.append(r); la_sub.append(True)
    bang(ws, 1, ["Chương KNTT", "Dạng  (↳ = tiểu dạng; % tính trên TOÀN BỘ đề của kỳ)", "% đề GK1", "% đề CK1",
                 "% đề GK2", "% đề CK2"], rows, [22, 66, 10, 10, 10, 10])
    for i, sb in enumerate(la_sub, 2):
        to_mau(ws, i, 3, 6)
        if sb:
            ws.cell(i, 2).font = nhat

    # ── Từng kỳ
    tom_tat = {}
    thu_tu_ch = [ch for ch, _ in thu_tu_dang]
    for k in KY_THU_TU:
        ds = theo_ky[k]
        if not ds:
            continue
        ws = wb.create_sheet(k)
        nhom = []
        for ch, ten in thu_tu_dang:
            cau = [(d, c) for d in ds for c in d["cau"] if (ch, ten) in c["dang"]]
            if not cau:
                continue
            n = so_de(ds, lambda c: (ch, ten) in c["dang"])
            diem = [c["diem"] for _, c in cau if c["diem"] is not None and c["phan"] == "TL" and len(c["dang"]) == 1]
            cha = [ch, ten, n, pt(n, ds), sum(c["phan"] == "TN" for _, c in cau),
                   sum(c["phan"] == "TL" for _, c in cau), round(sum(diem) / len(diem), 2) if diem else None,
                   vi_du(cau)]
            con = []
            for st in ds_sub(ten):
                cs = [(d, c) for d, c in cau if st in c["sub"].get(ten, [])]
                if not cs:
                    continue
                m = len({id(d) for d, _ in cs})
                con.append(["", "      ↳ " + st, m, pt(m, ds), sum(c["phan"] == "TN" for _, c in cs),
                            sum(c["phan"] == "TL" for _, c in cs), None,
                            "" if st == CHUA_RO else vi_du(cs, False)])
            con.sort(key=lambda r: (r[1].endswith(CHUA_RO), -r[3]))
            nhom.append((cha, con))
        nhom.sort(key=lambda g: (thu_tu_ch.index(g[0][0]), -g[0][3]))
        rows, la_sub = [], []
        for cha, con in nhom:
            rows.append(cha); la_sub.append(False)
            rows += con; la_sub += [True] * len(con)
        ws["A1"] = f"{k} — {len(ds)} đề"; ws["A1"].font = Font(bold=True, size=13)
        ws["A2"] = "↳ = tiểu dạng của dòng trên; % tính trên TOÀN BỘ đề của kỳ. Toán lời văn tách theo bối cảnh ở cuối trang."
        ws["A2"].font = nhat
        bang(ws, 3, ["Chương KNTT", "Dạng", "Số đề có", "% số đề", "Lượt câu TN", "Lượt câu/bài TL",
                     "Điểm TB bài TL (chỉ bài 1 dạng)", "Ví dụ trích đề"], rows, [20, 56, 9, 9, 10, 10, 13, 90])
        for i, sb in enumerate(la_sub, 4):
            to_mau(ws, i, 4, 4)
            if sb:
                ws.cell(i, 2).font = nhat
        # khối TOÁN LỜI VĂN của kỳ
        h = 4 + len(rows) + 2
        co_lv = so_de(ds, lambda c: bool(c["loi_van"]))
        tb = sum(sum(1 for c in d["cau"] if c["loi_van"]) for d in ds) / len(ds)
        ws.cell(h, 1, f"TOÁN LỜI VĂN — {k}: {pt(co_lv, ds)}% đề có ít nhất 1 bài lời văn · trung bình {tb:.1f} bài/đề").font = Font(bold=True, size=12)
        rows_lv = []
        for ten, _ in LOI_VAN + [TOI_UU_LV]:
            cs = [(d, c) for d in ds for c in d["cau"] if ten in c["loi_van"]]
            if not cs:
                continue
            m = len({id(d) for d, _ in cs})
            rows_lv.append(["Lời văn", ten, m, pt(m, ds), sum(c["phan"] == "TN" for _, c in cs),
                            sum(c["phan"] == "TL" for _, c in cs), None, vi_du(cs, False)])
        rows_lv.sort(key=lambda r: (r[1].startswith("(kèm)"), -r[3]))
        bang(ws, h + 1, ["", "Bối cảnh bài lời văn", "Số đề có", "% số đề", "Lượt câu TN", "Lượt câu/bài TL", "",
                         "Ví dụ trích đề"], rows_lv, [20, 56, 9, 9, 10, 10, 13, 90])
        for i in range(len(rows_lv)):
            to_mau(ws, h + 2 + i, 4, 4)
        ws.freeze_panes = ws.cell(4, 1)
        tom_tat[k] = sorted(((r[3], r[1]) for r in rows if not r[1].startswith(" ")), reverse=True)[:6]

    # ── Toán lời văn: bối cảnh × kỳ
    ws = wb.create_sheet("Toán lời văn")
    ws["A1"] = f"TOÁN LỜI VĂN — Toán {lop}: tách theo BỐI CẢNH"; ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Một bài có thể mang nhiều bối cảnh (VD: chuyển động + tối ưu). \"Hay giải bằng\" = các dạng "
                "(công cụ) hay đi cùng bối cảnh đó trong cùng một bài.")
    ws["A2"].font = nhat
    tong = ["", "Có ít nhất 1 bài lời văn"] + [pt(so_de(theo_ky[k], lambda c: bool(c["loi_van"])), theo_ky[k])
                                              for k in KY_THU_TU] + ["", "", ""]
    rows = [tong]
    tat_ca = [(d, c) for k in KY_THU_TU for d in theo_ky[k] for c in d["cau"]]
    for ten, _ in LOI_VAN + [TOI_UU_LV]:
        cs = [(d, c) for d, c in tat_ca if ten in c["loi_van"]]
        if not cs:
            continue
        cung = Counter(t for _, c in cs for ch, t in c["dang"]
                       if ch != "Chung" or "lập" in t or "thực tế" in t)
        rows.append(["", ten] + [pt(so_de(theo_ky[k], lambda c, ten=ten: ten in c["loi_van"]), theo_ky[k])
                                 for k in KY_THU_TU]
                    + [len(cs), "; ".join(f"{t} ({n})" for t, n in cung.most_common(3)), vi_du(cs, False)])
    rows[1:] = sorted(rows[1:], key=lambda r: (r[1].startswith("(kèm)"), -sum(x or 0 for x in r[2:6])))
    bang(ws, 3, ["", "Bối cảnh", "% đề GK1", "% đề CK1", "% đề GK2", "% đề CK2", "Tổng lượt (4 kỳ)",
                 "Hay giải bằng (dạng đi cùng)", "Ví dụ trích đề"], rows, [3, 58, 9, 9, 9, 9, 10, 48, 90])
    ws.cell(4, 2).font = dam
    for i in range(len(rows)):
        to_mau(ws, 4 + i, 3, 6)
    ws.column_dimensions["A"].width = 3

    # ── Bài hình: kết luận hay gặp (lớp 7-9)
    if lop != "6":
        ws = wb.create_sheet("Bài hình – kết luận")
        rows = []
        for ten, _ in KET_LUAN:
            r = [ten]
            for k in KY_THU_TU:
                ds = theo_ky[k]
                n = sum(any(ten in c["ket_luan"] for c in d["cau"]) for d in ds)
                r.append(round(100 * n / len(ds)) if ds else None)
            rows.append(r)
        bang(ws, 1, ["Điều phải chứng minh", "% đề GK1", "% đề CK1", "% đề GK2", "% đề CK2"], rows, [36, 10, 10, 10, 10])

    # ── Danh sách đề
    ws = wb.create_sheet("Danh sách đề")
    rows = []
    for d in sorted(de, key=lambda d: (KY_THU_TU.index(d["ky"]), d["nam"], d["truong"])):
        dang = Counter(ten for c in d["cau"] for _, ten in c["dang"])
        rows.append([d["ky"], d["nam"], d["truong"], "OCR" if d["nguon"] == "ocr" else "chữ",
                     "KHÔNG tách được — không tính" if d["loi"] else len(d["cau"]), "; ".join(dang), d["file"]])
    bang(ws, 1, ["Kỳ", "Năm học", "Trường", "Nguồn", "Số câu", "Các dạng có trong đề", "File"], rows,
         [7, 11, 26, 7, 8, 90, 50])

    dest.parent.mkdir(parents=True, exist_ok=True)
    wb.save(dest)
    return tom_tat


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", default="6,7,8,9")
    ap.add_argument("--json", action="store_true", help="ghi thêm bản phân loại từng câu (để soát)")
    a = ap.parse_args(argv[1:])
    for lop in a.lop.split(","):
        de = doc_kho(lop)
        gan_dang(lop, de)
        dest = OUT / f"Thong-ke-dang-de-Toan{lop}-Ha-Noi.xlsx"
        tt = xuat(lop, de, dest)
        khong_dang = sum(1 for d in de for c in d["cau"] if not c["dang"])
        print(f"   bỏ {sum(d['loi'] for d in de)} đề không tách được khối đề")
        tong = sum(len(d["cau"]) for d in de)
        print(f"lớp {lop}: {len(de)} đề, {tong} câu, {khong_dang} câu không nhận ra dạng "
              f"({100 * khong_dang / max(tong, 1):.0f}%) → {dest.relative_to(ROOT)}")
        for k, top in tt.items():
            print(f"   {k}: " + " · ".join(f"{t} {p}%" for p, t in top[:4]))
        if a.json:
            (OUT / f"phan-loai-lop-{lop}.json").write_text(json.dumps(de, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
