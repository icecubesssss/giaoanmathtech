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
        ("IV. Hệ thức lượng", "Tỉ số lượng giác của góc nhọn", r"tỉ số lượng giác|\bsin|\bcos|\btan|\bcot"),
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
        if _HET.match(d) or (hoa and _DUNG.search(d)) or (hoa and _BO_QUA.search(d)) or _BANG_DA.match(dong):
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
    for d in de:
        for c in d["cau"]:
            c["dang"] = [(ch, ten) for ch, ten, r in rx if r.search(c["text"])]
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
    ]
    for i, g in enumerate(ghi, 3):
        ws.cell(i, 1, "• " + g).alignment = Alignment(wrap_text=True)
    rows = []
    for k in KY_THU_TU:
        ds = theo_ky[k]
        rows.append([k, len(ds), sum(d["nguon"] == "text" for d in ds), sum(d["nguon"] == "ocr" for d in ds),
                     sum(len(d["cau"]) for d in ds), loi_ky[k],
                     ", ".join(f"{n}: {c}" for n, c in sorted(Counter(d["nam"] for d in ds).items()))])
    bang(ws, 11, ["Kỳ", "Số đề dùng thống kê", "Có lớp chữ", "OCR (scan)", "Số câu/bài tách được",
                  "Đề KHÔNG tách được (bỏ ra)", "Theo năm học"], rows, [10, 11, 12, 12, 14, 14, 60])
    ws.column_dimensions["A"].width = 12
    for i in range(3, 9):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)
        ws.row_dimensions[i].height = 30

    # ── Cả năm: dạng × kỳ
    ws = wb.create_sheet("Cả năm")
    rows = []
    for ch, ten in thu_tu_dang:
        r = [ch, ten]
        for k in KY_THU_TU:
            ds = theo_ky[k]
            n = sum(any((ch, ten) in c["dang"] for c in d["cau"]) for d in ds)
            r.append(round(100 * n / len(ds)) if ds else None)
        rows.append(r)
    bang(ws, 1, ["Chương KNTT", "Dạng", "% đề GK1", "% đề CK1", "% đề GK2", "% đề CK2"], rows, [22, 58, 10, 10, 10, 10])
    for i, r in enumerate(rows, 2):
        for j in range(3, 7):
            v = r[j - 1]
            if v is not None and v >= 50:
                ws.cell(i, j).font = dam
                ws.cell(i, j).fill = PatternFill("solid", fgColor="C6EFCE")
            elif v:
                ws.cell(i, j).fill = PatternFill("solid", fgColor="FFF2CC") if v >= 20 else nen_ch

    # ── Từng kỳ
    tom_tat = {}
    for k in KY_THU_TU:
        ds = theo_ky[k]
        if not ds:
            continue
        ws = wb.create_sheet(k)
        rows = []
        for ch, ten in thu_tu_dang:
            co = [d for d in ds if any((ch, ten) in c["dang"] for c in d["cau"])]
            cau = [(d, c) for d in ds for c in d["cau"] if (ch, ten) in c["dang"]]
            if not co:
                continue
            diem = [c["diem"] for _, c in cau if c["diem"] is not None and c["phan"] == "TL" and len(c["dang"]) == 1]
            # ví dụ: ưu tiên câu có lớp chữ, ngắn, chỉ mang MỘT dạng
            vd = sorted(cau, key=lambda x: (x[0]["nguon"] != "text", len(x[1]["dang"]), abs(len(x[1]["text"]) - 220)))
            vi_du = ""
            if vd:
                d0, c0 = vd[0]
                vi_du = f"[{d0['truong']} {d0['nam']}] " + re.sub(r"\s+", " ", c0["text"])[:260]
            rows.append([ch, ten, len(co), round(100 * len(co) / len(ds)),
                         sum(c["phan"] == "TN" for _, c in cau), sum(c["phan"] == "TL" for _, c in cau),
                         round(sum(diem) / len(diem), 2) if diem else None, vi_du])
        rows.sort(key=lambda r: (thu_tu_dang.index((r[0], r[1])) if r[0] == "Chung" else 0, -r[3]))
        rows.sort(key=lambda r: [ch for ch, _ in thu_tu_dang].index(r[0]))
        ws["A1"] = f"{k} — {len(ds)} đề"; ws["A1"].font = Font(bold=True, size=13)
        bang(ws, 3, ["Chương KNTT", "Dạng", "Số đề có", "% số đề", "Lượt câu TN", "Lượt câu/bài TL",
                     "Điểm TB bài TL (chỉ bài 1 dạng)", "Ví dụ trích đề"], rows, [20, 50, 9, 9, 10, 10, 13, 90])
        for i, r in enumerate(rows, 4):
            if r[3] >= 50:
                ws.cell(i, 4).font = dam; ws.cell(i, 4).fill = PatternFill("solid", fgColor="C6EFCE")
        tom_tat[k] = sorted(((r[3], r[1]) for r in rows), reverse=True)[:6]

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
