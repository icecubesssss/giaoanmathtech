#!/usr/bin/env python3
"""12/11/2026 — Thầy: Ch.X 9C gộp trụ + nón + cầu vào 1 buổi, buổi 2 = luyện tập 45′ + KT 45′.
Sửa thuyet-minh.json: phiếu A (gộp, 90′) thay A+B cũ; phiếu C (luyện tập + KT) giữ mã C
(để khớp seed phieu-c-… cũ), sửa lỗi chữ hỏng ($ phút, 68409, {xq}$). Chạy từ gốc repo."""
import json
from pathlib import Path
P = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/thuyet-minh.json")
tm = json.loads(P.read_text())
old = {p["code"]: p for p in tm["phieu"]}

tm["tuan"] = "32-33"
tm["thoiluong"][0] = ("Buổi 1 (tuần 32 — Bài 31 $+$ Bài 32 GỘP: hình trụ, hình nón, hình cầu): 1 ca $=$ 90 phút "
                      "(PPCT SGV: 4 tiết). Thầy chốt 12/11/2026: dạy đủ sáu công thức trong một buổi.")
tm["thoiluong"][1] = ("Buổi 2 (tuần 33 — Luyện tập chung $+$ Bài tập cuối chương X): 1 ca $=$ 90 phút "
                      "(45 phút luyện tập $+$ 45 phút kiểm tra chương).")
tm["thoiluong"][2] = ("\\textbf{Tổng 2 ca $=$ 180 phút $=$ 4 tiết} trên PPCT 7 tiết — chương DẠY NÉN, còn $57\\%$ "
                      "thời lượng sách; Chuyên đề 1 (Câu IV.1) cũ gộp vào buổi 2.")
tm["thoiluong"][3] = tm["thoiluong"][3]  # vì sao nén được — giữ
tm["thoiluong"][4] = ("\\textbf{Chỗ nén}: hình trụ dạy kĩ (3/3 đề Vào 10), hình cầu vừa đủ cho khuôn mực nước (đề minh họa), "
                      "hình nón chỉ nhận biết $+$ thay số (0/3 đề Vào 10). Buổi 1 không luyện diện tích vật liệu, "
                      "chiều ngược, hiệu hai khối — để buổi 2.")
tm["thoiluong"][5] = ("\\textbf{Chương X là chương SGK CUỐI CÙNG của mạch hình học} — hết chương trình ở tuần 33 "
                      "(31/01/2027, buổi cuối trước Tết), cùng tuần hết đại số.")
tm["vidu"] = [v.replace("Buổi 2:", "Buổi 1:").replace("Buổi 2 (", "Buổi 1 (")
               .replace("Buổi 3:", "Buổi 2:").replace("Buổi 3 (", "Buổi 2 (") for v in tm["vidu"]]

def row(band, dang, loai, lt, vd, oc, bt, refs, **kw):
    r = {"band": band, "dang": dang, "loai": loai, "lythuyet": lt, "vidu": vd,
         "onclass": oc, "btvn": bt, "source_refs": refs, "decompose": "none"}
    r.update(kw); return r

A = {"code": "A", "title": "Buổi 1 — Bài 31 $+$ Bài 32 (gộp): Hình trụ, hình nón, hình cầu", "so_ca": 1,
     "dich": "Câu IV.1 đề minh họa Vào 10 của Sở (ly nước hình trụ, thả 5 viên bi hình cầu)",
     "rows": [
  row("NB", "Đọc hình vẽ sẵn của HÌNH TRỤ và đổi ĐƯỜNG KÍNH sang BÁN KÍNH ($r=d:2$) trước khi thay số — chống bẫy số một của cả chương",
      "NB kiến thức cũ", 1, 1, 2, 2, ["tl-cthn2526-4-tr2.b", "ck2-mai-dich-2025-4.1"], hinh_san=True),
  row("NB", "Thay số vào $S_{xq}=2\\pi rh$ và $V=\\pi r^2 h$ của hình trụ, ghi đúng đơn vị cm$^2$ / cm$^3$",
      "NB tách TH", 1, 0, 2, 2, ["tl-cthn2627-4-tr2.a", "gk2-ban-mai-2025-4.1"], hinh_san=True),
  row("NB", "HÌNH NÓN (trắc nghiệm): từ $r$, $h$ tìm đường sinh $l$ (Pythagore) rồi thay số $S_{xq}=\\pi r l$ — phân biệt $h$ với $l$",
      "NB lẻ LT", 1, 0, 1, 1, ["sgk-10.23"], hinh_san=True),
  row("NB", "HÌNH CẦU: thay số vào $S=4\\pi R^2$ và $V=\\dfrac{4}{3}\\pi R^3$ (đề cho đường kính thì chia đôi; nhớ mũ BA ở thể tích)",
      "NB lẻ LT", 1, 0, 2, 2, ["ck2-chu-van-an-2024-IV1", "ck2-trung-vuong-2025-IV1"], hinh_san=True),
  row("NB", "Ôn Lớp 5--6: đổi cm$^3$ $\\leftrightarrow$ lít $\\leftrightarrow$ m$^3$ — bước bắt buộc của bài thực tế",
      "NB kiến thức cũ", 0, 0, 1, 1, ["sgk-10.7"]),
  row("NB", "Giàn giáo VẼ HÌNH — khuôn MỰC NƯỚC: vẽ phác ly hình trụ, ghi $r$, mực nước cũ và mới; thể tích vật thả chìm $=$ thể tích nước DÂNG THÊM; chiều cao lấy theo phần nước dâng",
      "NB ghép bài", 1, 0, 1, 1, ["tl-mhhn2018-4-tr3.b"], gian_giao="ve-hinh", ve_hinh={"onclass": 1, "btvn": 0}),
  row("NB", "Giàn giáo ĐIỀN KHUYẾT: hoàn thành bài giải mẫu một ý Câu IV.1 (bán kính, công thức, thay số, đơn vị, câu kết luận) — trên lớp quả bóng hình cầu, về nhà ly nước hình trụ",
      "NB ghép bài", 0, 0, 1, 1, ["ck2-trung-vuong-2025-IV1"], hinh_san=True, gian_giao="dien-khuyet", khung=True),
  row("TH", "Tính thể tích của một vật hình trụ có thật (thùng tôn, thùng phuy), số liệu cho bằng ĐƯỜNG KÍNH, rồi đổi ra lít; ví dụ mẫu tính cả $S_{xq}$ và $V$ (đề 2026)",
      "TH lẻ LT", 0, 1, 1, 1, ["gk2-ban-mai-2025-4.1", "tl-cthn2627-4-tr2.a"]),
  row("VD", "Trọn Câu IV.1 đề minh họa Vào 10: ly nước hình trụ (đề cho đường kính), ý a thể tích nước, ý b thả 5 viên bi — chấm theo thang 0,5 $+$ 0,5; ví dụ mẫu khuôn nước tràn (Chu Văn An); về nhà trọn Câu IV.1 đề 2025",
      "VD lẻ", 0, 1, 1, 1, ["tl-mhhn2018-4-tr3.b", "ck2-chu-van-an-2024-IV1", "tl-cthn2526-4-tr2.b"]),
]}
C = old["C"]
C["title"] = "Buổi 2 — Luyện tập chung (45 phút) $+$ Kiểm tra chương X (45 phút)"
fix = {0: "Điền lại BẢNG SÁU CÔNG THỨC của cả chương (trụ: $S_{xq}$, $V$; nón: $S_{xq}$, $V$; cầu: $S$, $V$) rồi đối chiếu với SGK",
       6: "Khuôn ĐẾM SỐ LẦN: mỗi lần múc $80\\%$ thể tích xô để đổ đầy bể — chia rồi làm tròn LÊN (Câu IV.1b đề Vào 10 năm 2026)",
       7: "Khuôn HIỆU HAI KHỐI TRỤ: tính thể tích bê tông của bể $=$ khối trụ ngoài trừ lòng bể, rồi so sánh với số tiền có"}
for i, s in fix.items():
    C["rows"][i]["dang"] = s
tm["phieu"] = [A, C]
P.write_text(json.dumps(tm, ensure_ascii=False, indent=2) + "\n")
print("ok")
