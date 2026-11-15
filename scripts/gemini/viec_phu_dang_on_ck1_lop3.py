#!/usr/bin/env python3
"""3 việc Gemini: PHỦ DẠNG cho 3 đề ÔN TẬP CK1 lớp 3 (phu_dang_gate --khoi 3 đang ❌ 12 lỗi).

Claude chốt 13/11/2026 (theo luật cổng phủ dạng Thầy duyệt 12/11, barem đề trung tâm giữ nguyên):
  Mỗi đề ôn có đủ 13 dạng dễ ≥30% đề thật, theo KHUNG Ô cố định:
    Câu 1 a) đọc/viết số            b) tính nhẩm
    Câu 2 a) một phần mấy           b) gấp/giảm một số lần
    Câu 3 a) góc vuông/đếm hình     b) hình tròn
    Câu 4 a) đơn vị đo nhận biết    b) tính toán/đổi đơn vị đo
    Câu 5 biểu thức · Câu 6 phép chia có dư · Câu 7 đặt tính · Câu 8 hai bước
    Câu 9 a) tìm thành phần chưa biết   b) tư duy
  Ngân hàng 13 đề trường đã cạn câu chưa dùng ⇒ bù bằng 2 đề TRUNG TÂM MathTech (KNTT-01, KNTT-02),
  ghi rõ "đề trung tâm" ở nguồn (đã có tiền lệ Ôn 3 câu 3b).
Gemini viết lại khối DE["onN"] (Python) + bản ghi các câu đề trung tâm dùng tới; Claude vá
scripts/de_ck1_lop3.py, chạy cổng, build, soi ảnh.

    .venv/bin/python scripts/gemini/viec_phu_dang_on_ck1_lop3.py
    python3 scripts/gemini/tho.py --mot pd3-on1   (… pd3-on2, pd3-on3; song song)
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HANG_DOI = REPO / "storage/gemini/hang-doi"
TT1 = "inputs/refs/de-thi/lop-3/de-trung-tam/T3 - HKI - KNTT - 01.pdf"
TT2 = "inputs/refs/de-thi/lop-3/de-trung-tam/T3 - HKI - KNTT - 02.pdf"
BG = "inputs/refs/ngan-hang-sheet/tieu-hoc/lop-3/ban-ghi/"

# Kế hoạch ô: (ô, nguồn, ghi chú). "GIỮ" = giữ nguyên Q/ý hiện có trong khối đề đó (được sửa trình bày nếu
# cần cho vừa ô); nguồn "tt-kntt01#.." / "tt-kntt02#.." = câu đề trung tâm (nhãn do Claude đặt, xem NHAN_TT).
KE_HOACH = {
    "on1": [
        ("Câu 1a đọc/viết số", "GIỮ ck1-2526-donghoa#1b", ""),
        ("Câu 1b tính nhẩm", "GIỮ ck1-2526-nguyenvantroi#1a", "đang là Câu 2a, chuyển lên"),
        ("Câu 2a một phần mấy", "ck1-2526-donghoa#2a", "hình 18 quả dứa: vẽ TikZ 18 hình tròn nhỏ xếp 3 hàng × 6 (chỉ cần đếm được)"),
        ("Câu 2b gấp/giảm", "tt-kntt02#2", "con lợn 50 kg, con ngỗng 5 kg, gấp mấy lần"),
        ("Câu 3a đếm hình", "GIỮ ck1-2425-thanhhung2#4", "CHỈ giữ ý đếm tam giác trên hình F_HCN; bỏ ý tứ giác (thanhuyen#4a)"),
        ("Câu 3b hình tròn", "ck1-2425-nguyenbinhkhiem#4", "xem ảnh đề gốc (các trang jpg Nguyễn Bỉnh Khiêm), vẽ lại bằng htron()"),
        ("Câu 4a đơn vị nhận biết", "ck1-2526-donghoa#4a", "nhiệt kế dùng để đo gì"),
        ("Câu 4b đổi/tính đơn vị", "GIỮ ck1-2425-nguyenbinhkhiem#7", "Đ/S còn 2 ý × 0,25 cho đủ 0,5đ của ý b"),
        ("Câu 5 biểu thức", "GIỮ ck1-2425-thanhhung2#8", ""),
        ("Câu 6 phép chia có dư", "tt-kntt02#1b", "số dư của 715 : 7"),
        ("Câu 7 đặt tính", "GIỮ ck1-2425-nguyenbinhkhiem#9", ""),
        ("Câu 8 hai bước", "GIỮ ck1-2425-nguyenbinhkhiem#10", ""),
        ("Câu 9a tư duy", "GIỮ ck1-2526-nguyenvantroi#10b", "điền dấu phép tính"),
        ("Câu 9b tìm thành phần", "ck1-2526-vinhbao#4a", "đang là Câu 6 ($45 : \\square = 5$), chuyển xuống; bỏ dãy số thanhuyen#2a"),
    ],
    "on2": [
        ("Câu 1a đọc/viết số", "tt-kntt01#1", "chọn 2 chỗ: đọc 1 số + viết 1 số (vừa 0,5đ)"),
        ("Câu 1b tính nhẩm", "ck1-2526-phuluong#7", "lấy 4 phép số tròn chục/trăm, điền kết quả"),
        ("Câu 2a một phần mấy", "tt-kntt02#7a", "đã tô màu 1/4 số ô vuông của hình nào: vẽ 4 lưới ô vuông bằng TikZ theo ảnh đề"),
        ("Câu 2b gấp/giảm", "ck1-2526-donghoa#6a", "chuyển từ Ôn 3 Câu 6 sang (gấp một số lên 3 lần được tích của 5 và 9)"),
        ("Câu 3a góc vuông", "GIỮ ck1-2425-nguyenbinhkhiem#5", "hình vuông có mấy góc vuông; bỏ khanhthien#1d"),
        ("Câu 3b hình tròn", "tt-kntt02#5", "Đ/S theo hình O, A, B, M, N, I: chọn 2 ý × 0,25; vẽ lại bằng htron() đúng ảnh đề"),
        ("Câu 4a đơn vị nhận biết", "tt-kntt02#4a", "nhiệt độ ngày nắng nóng"),
        ("Câu 4b đổi/tính đơn vị", "GIỮ ck1-2425-thanhhung2#5", "5 cm = ? mm; bỏ vinhbao#3"),
        ("Câu 5 biểu thức", "GIỮ ck1-2425-nguyenbinhkhiem#8", ""),
        ("Câu 6 phép chia có dư", "GIỮ ck1-2526-donghoa#6b", ""),
        ("Câu 7 đặt tính", "GIỮ ck1-2526-phuluong#5", ""),
        ("Câu 8 hai bước", "GIỮ ck1-2526-khanhthien#8", ""),
        ("Câu 9a tìm thành phần", "GIỮ ck1-2425-nguyenbinhkhiem#1", "đang là Câu 1a (số trừ 36, hiệu 25), chuyển xuống, đổi sang điền kết quả"),
        ("Câu 9b tư duy", "GIỮ ck1-2526-donghoa#10a", "taxi 34 bạn, mỗi xe 5 bạn; bỏ tayhung#TL4, vinhbao#1a, vinhbao#5, thanhhung2#1"),
    ],
    "on3": [
        ("Câu 1a đọc/viết số", "GIỮ ck2-2425-huuthanhb#1", ""),
        ("Câu 1b tính nhẩm", "GIỮ ck1-2425-nguyenbinhkhiem#2", ""),
        ("Câu 2a một phần mấy", "tt-kntt01#2b", "một phần hai số ngôi sao: vẽ đúng số ngôi sao như ảnh đề (TikZ, \\ding{72} của pifont cũng được)"),
        ("Câu 2b gấp/giảm", "GIỮ ck1-2526-donghoa#2b", "sơ đồ SODO; bỏ thanhhung2#6"),
        ("Câu 3a góc vuông", "ck1-2526-nguyenvantroi#5", "hình chữ nhật ghép tam giác vuông: dùng lại hình F_KT1D (đã có), hỏi mấy góc vuông, đáp án 5"),
        ("Câu 3b hình tròn", "GIỮ ck1-2526-thanhuyen#1b", "hình F_TU1B; bỏ ý khối lập phương (tt câu 3a)"),
        ("Câu 4a đơn vị nhận biết", "tt-kntt01#2a", "nhiệt độ cao nhất vào buổi nào"),
        ("Câu 4b đổi/tính đơn vị", "GIỮ ck1-2526-vinhbao#8", "giữ CHỈ 1 phép tính (0,5đ cả ý)"),
        ("Câu 5 biểu thức", "GIỮ ck1-2526-vinhbao#7", ""),
        ("Câu 6 phép chia có dư", "tt-kntt01#5b", "? : 5 = 15 (dư 3)"),
        ("Câu 7 đặt tính", "GIỮ ck1-2526-thanhuyen#5 + ck1-2526-vinhbao#6", ""),
        ("Câu 8 hai bước", "GIỮ ck1-2526-nguyenvantroi#9", ""),
        ("Câu 9a tìm thành phần", "ck1-2526-phuluong#6", "3 × ? = 147; 324 : ? = 6"),
        ("Câu 9b tư duy", "GIỮ ck1-2526-donghoa#8", "CHỈ giữ ý b ($573 + 505 : 5$ so với $630$)"),
    ],
}

NHAN_TT = """Nhãn câu đề trung tâm (dùng ĐÚNG các nhãn này trong ref và trong tt_cau):
  tt-kntt01#1  = Câu 1 (đọc số 725, 508; viết số Ba trăm mười lăm, số gồm 4 trăm 6 đơn vị)
  tt-kntt01#2a = Câu 2a (nhiệt độ 18, 30, 24, 12 °C — cao nhất buổi nào)
  tt-kntt01#2b = Câu 2b (một phần hai số ngôi sao)
  tt-kntt01#5b = Câu 5b (? : 5 = 15 dư 3)
  tt-kntt02#1b = Câu 1b (số dư của 715 : 7)
  tt-kntt02#2  = Câu 2 (lợn 50 kg, ngỗng 5 kg, gấp mấy lần)
  tt-kntt02#4a = Câu 4a (nhiệt độ ngày nắng nóng)
  tt-kntt02#5  = Câu 5 (Đ/S hình tròn O, A, B, M, N, I)
  tt-kntt02#7a = Câu 7a (tô màu 1/4 số ô vuông)"""

DANG = ["Đọc, viết số", "Tính nhẩm (bảng nhân chia, số tròn chục/trăm)", "Một phần mấy", "Gấp, giảm một số lần",
        "Góc vuông, góc không vuông; đếm hình", "Hình tròn: tâm, bán kính, đường kính",
        "Đơn vị đo (mm, g, ml, °C): nhận biết, ước lượng", "Tính toán, đổi đơn vị đo (mm, g, ml)",
        "Phép chia có dư", "Tìm thành phần chưa biết của phép tính"]

MAU = r"""Bạn là giáo viên Toán tiểu học, sửa ĐỀ ÔN TẬP cuối học kì I Toán 3 (Kết nối tri thức).

Thư mục làm việc có:
- de_ck1_lop3.py: script Python sinh 6 đề. Đọc kĩ các hàm Q(), y(), ops(), fig(), ds(), htron(), tugiac(),
  dat_tinh(), dt_sol(), giai(), ng() và hằng hình F_*, SODO. Khối cần viết lại: DE["{k}"] = (...).
- l3-*.json: bản ghi từng câu của các đề trường (trường "nd" là nội dung đã chép, "dap_an", "muc", "cd", "bai").
- Ảnh/text đề trung tâm (T3 - HKI - KNTT - 01/02 …-trang-N.png, .txt) và ảnh đề khác nếu cần xem hình.
Bạn KHÔNG được chạy lệnh; chỉ đọc file rồi trả JSON theo schema.

VIỆC: viết lại TOÀN BỘ khối DE["{k}"] theo KẾ HOẠCH Ô dưới đây (ĐÚNG thứ tự, đúng nguồn):
{kh}

{nhan_tt}

LUẬT CỨNG:
1. Barem giữ nguyên: Câu 1–4 mỗi câu "1" điểm gồm 2 ý a), b) × 0,5 (viết bằng y("a", …) + y("b", …));
   Câu 5, 6 mỗi câu "0,5"; Câu 7 "2"; Câu 8 "2"; Câu 9 "1" (2 ý × 0,5). Tổng đúng 10.
   Mức (tham số level): Câu 1–4 theo mức ý khó hơn; Câu 7 mức 1, Câu 8 mức 2, Câu 9 mức 3.
2. Ý "GIỮ" = chép lại đúng chữ, đúng số đang có trong khối hiện tại (chỉ được cắt bớt ý cho vừa 0,5đ như ghi chú).
   Ý mới = CHÉP NGUYÊN VĂN số liệu của câu nguồn (từ "nd" của bản ghi hoặc ảnh đề trung tâm). Không bịa số.
   Câu nguồn trắc nghiệm giữ đủ phương án, đúng thứ tự in. Có thể đổi trắc nghiệm ⇄ điền kết quả cho vừa ô,
   ghi điều đó vào note của ng(..., "…").
3. Mỗi Q có meta = (nội dung ngắn, [DANH SÁCH REF của cả câu, ý a trước], mức, phút). Phút: Câu 1–4 = 3,
   Câu 5–6 = 2, Câu 7 = 7, Câu 8 = 8, Câu 9 = 6. Nguồn (src) ghép như các câu hiện có:
   "a) " + ng("<ref ý a>") + "; b) " + ng("<ref ý b>"). Ref đề trung tâm cũng viết qua ng("tt-kntt0N#…").
   KHÔNG dùng NGUON["tt"] nữa.
4. Chỗ điền: \\makebox[3.2cm]{{\\dotfill}} (số/từ ngắn), câu viết chữ (đọc số) xuống dòng [[br]] \\dotfill\\mbox{{}}.
   CẤM \\dots\\dots làm chỗ điền. Mọi số, phép tính trong $...$; số 4 chữ số viết $1\\,000$. Không unicode toán
   ngoài $...$ (dùng $\\times$, $:$, $^\\circ$C). Trong chuỗi Python nhớ nhân đôi dấu \\.
5. Hình: dùng hằng có sẵn khi kế hoạch nói vậy; hình mới định nghĩa thành hằng F_<TÊN> = ... (dùng htron(),
   tugiac() hoặc tikzpicture ngắn) đặt TRONG code trả về, TRƯỚC dòng DE["{k}"] =. Hình phải khớp đề gốc
   (đúng điểm nào nằm trên đường tròn, đoạn nào qua tâm). Câu có hình: fig(text, F_…, 0.58) như câu hiện có.
   Trang 1 chứa Câu 1–3 ⇒ tối đa MỘT hình cạnh chữ ở mỗi câu, hình nhỏ (scale ≤ 0.85).
6. answer ngắn ("a) B – b) 5"); solution ghi lời giải ngắn từng ý + điểm, tự tính lại mọi đáp số.
   Đề gốc sai/mơ hồ ⇒ ghi vào ghi_chu, không tự ý đổi đề.
7. Phần cuối tuple giữ dòng phiếu tự kiểm tra hiện có (có thể sửa chữ cho khớp câu mới).

TRẢ VỀ JSON:
- "code": đoạn Python hoàn chỉnh (các hằng F_ mới nếu có + DE["{k}"] = ("…", [ … ], "…")), chạy được khi
  dán thay khối cũ.
- "tt_cau": mỗi câu đề trung tâm đã dùng một phần tử: de ("tt-kntt01"/"tt-kntt02"), cau (nhãn như trên),
  nd (chép nguyên văn ngắn gọn, tả hình), ht ("TN"/"Điền"/"Đ/S"), diem (điểm trong đề trung tâm),
  dap_an, muc ("NB"/"TH"/"VD"), cd, bai (số chủ đề, số bài KNTT ghi trong khung ở docstring hoặc suy từ nội dung:
  CĐ1 bài 1 đọc viết số; CĐ2 bài 14 một phần mấy; CĐ3 bài 17 hình tròn; CĐ4 bài 25 chia có dư;
  CĐ5 bài 33 nhiệt độ; CĐ6 bài 39 so sánh số lớn gấp mấy lần số bé), dang (CHỌN ĐÚNG MỘT trong danh sách:
  {dang}).
- "ghi_chu": nghi ngờ, chỗ cắt ý, chỗ đổi hình thức.
"""


def main() -> None:
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    bg = sorted(str(p.relative_to(REPO)) for p in (REPO / BG).glob("l3-*.json"))
    nbk = sorted(str(p.relative_to(REPO)) for p in
                 (REPO / "inputs/refs/de-thi/lop-3/cuoi-ki-1/anh/l3-ck1-2425-nguyenbinhkhiem-14357238").glob("*.jpg"))
    for k, kh in KE_HOACH.items():
        txt = "\n".join(f"  {i + 1:2}. {o:28} ← {n}" + (f"  ({g})" if g else "") for i, (o, n, g) in enumerate(kh))
        files = ["scripts/de_ck1_lop3.py", TT1, TT2] + bg + (nbk if k == "on1" else [])
        viec = {"id": f"pd3-{k}", "model": "gemini-3.8-flash-high",
                "prompt": MAU.format(k=k, kh=txt, nhan_tt=NHAN_TT, dang="; ".join(f'"{d}"' for d in DANG)),
                "files": files, "render": True, "schema": "scripts/gemini/schema/de-on-lop3.json",
                "timeout": "1800s", "meta": {"loai": "phu-dang-l3", "de": k}}
        (HANG_DOI / f"{viec['id']}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(f"ghi {viec['id']}: {len(kh)} ô, {len(files)} file")


if __name__ == "__main__":
    main()
