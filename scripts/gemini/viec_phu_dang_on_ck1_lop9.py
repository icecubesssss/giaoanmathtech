#!/usr/bin/env python3
"""3 việc Gemini: PHỦ DẠNG cho 3 đề ÔN TẬP CK1 lớp 9 (phu_dang_gate --khoi 9 đang ❌).

Thầy chốt 12/11/2026:
  - Bài III (2,5đ) thành 6 ý: 4 ý × 0,5 + 2 ý một bước × 0,25 (PT tích, căn dạng số).
  - Bài IV.1 thành 1,0đ: a) lượng giác 0,5 (giữ) + b) cung/quạt/vành khuyên 0,5 (đề thật).
    Bài hình IV.2 còn 2,5đ.
Claude chốt sơ đồ + chọn câu thật (ngân hàng 41 đề, ban-ghi), Gemini chép nguyên văn từ PDF,
viết lời giải/barem, tự tính lại. Kết quả ⇒ scripts/ck1_lop9_phu_dang.py (Claude vá, kiểm).

    python3 scripts/gemini/viec_phu_dang_on_ck1_lop9.py
    python3 scripts/gemini/tho.py --mot phu-dang-l9-on-1   (… on-2, on-3; song song)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PDF = "inputs/refs/de-thi/lop-9/cuoi-ki-1/"


def nap_de():
    """DE của de_on_tap_ck1_lop9.py SAU khi vá căn bổ sung (đúng như seed hiện hành)."""
    sys.path.insert(0, str(REPO / "scripts"))
    path = REPO / "scripts/de_on_tap_ck1_lop9.py"
    src = path.read_text()
    g = {"__file__": str(path), "__name__": "nap"}
    exec(compile(src[: src.index('\nif __name__ == "__main__":')], str(path), "exec"), g)
    from ck1_lop9_can_bo_sung import QUAN_MOI, ap_dung
    g["QUAN"].update(QUAN_MOI)
    ap_dung(g["DE"], g["y"], g["BR"])
    return g["DE"]


# (tên trường dùng ở cột nguồn, file PDF, vị trí câu trong đề gốc, nội dung bóc sẵn, đáp số đã kiểm)
CAU = {
    "ngosilien": ("THCS Ngô Sĩ Liên (2025–2026)", "de-cuoi-hoc-ki-1-toan-9-nam-2025-2026-truong-thcs-ngo-si-lien-ha-noi.pdf",
                  "Bài 1 ý b", "B = 14/(3 + √2) + √((1 - 2√2)²)", "$B = 5$"),
    "chuvanan": ("THCS Chu Văn An (2025–2026)", "de-hoc-ky-1-toan-9-nam-2025-2026-truong-thcs-chu-van-an-ha-noi.pdf",
                 "Bài IV.1 ý a (CHỈ ý a)", "Chiếc quạt giấy xòe hết cỡ là nửa hình tròn bán kính 2,2 dm; cung tròn lớn nhất dài bao nhiêu dm (π ≈ 3,14, làm tròn chữ số thập phân thứ nhất)", "$\\approx 6{,}9$ dm"),
    "dongda": ("THCS Đống Đa (2025–2026)", "de-cuoi-hk1-toan-9-nam-2025-2026-truong-thcs-dong-da-ha-noi.pdf",
               "Bài I.1", "Giải phương trình (x + 1)(2x - 3) = 0", "$x = -1$; $x = \\dfrac{3}{2}$"),
    "nguyendu": ("THCS Nguyễn Du (2025–2026)", "de-hoc-ki-1-toan-9-nam-2025-2026-truong-thcs-nguyen-du-ha-noi.pdf",
                 "Bài IV.1 ý a (CHỈ ý a)", "Quạt giấy xòe ra dạng hình quạt tròn bán kính 25 cm, góc giữa hai nan ngoài cùng 150°, π ≈ 3,14; tính diện tích chiếc quạt (làm tròn đến hàng đơn vị)", "$\\approx 818$ cm$^2$"),
    "lyson": ("THCS Lý Sơn (2025–2026)", "de-cuoi-ki-1-toan-9-nam-2025-2026-truong-thcs-ly-son-ha-noi.pdf",
              "Bài I.2 ý a", "Giải phương trình (x - 5)(5x - 1) = 0", "$x = 5$; $x = \\dfrac{1}{5}$"),
    "quocoai": ("Phòng GD\\&ĐT Quốc Oai (2024–2025)", "de-cuoi-ki-1-toan-9-nam-2024-2025-phong-gddt-quoc-oai-ha-noi.pdf",
                "Bài II.1 ý a", "Rút gọn biểu thức 2√8 - 3√18 + 4√50", "$15\\sqrt{2}$"),
    "phucdong": ("THCS Phúc Đồng (2025–2026)", "de-cuoi-hoc-ki-1-toan-9-nam-2025-2026-truong-thcs-phuc-dong-ha-noi.pdf",
                 "Bài IV.1", "Mặt đĩa CD dạng hình vành khuyên giới hạn bởi hai đường tròn bán kính 1,5 cm và 6 cm, π ≈ 3,14; diện tích hình vành khuyên (làm tròn đến hàng đơn vị)", "$\\approx 106$ cm$^2$"),
}

KE_HOACH = {
    "on-1": dict(
        cau=["ngosilien", "chuvanan"],
        bai3="""Bài III mới (2,5 điểm), 6 ý, thứ tự và điểm:
 1) (0,5) hệ phương trình — GIỮ NGUYÊN ý 1 hiện tại.
 2) (0,25) phương trình tích $x(x - 7) + x - 7 = 0$ — GIỮ đề, rút lời giải còn MỘT mốc 0,25 ở dòng kết luận.
 3) (0,5) bất phương trình — GIỮ NGUYÊN ý 3 hiện tại.
 4) (0,25) tính biểu thức số $\\dfrac{2}{3}\\sqrt{9} - \\dfrac{3}{2}\\sqrt{(-6)^2} + 7$ — GIỮ đề, rút lời giải còn MỘT mốc 0,25.
 5) (0,5) MỚI — trục căn thức ở mẫu: chép NGUYÊN VĂN ý b Bài 1 đề THCS Ngô Sĩ Liên 2025–2026 (xem PDF). Câu dẫn trong đề mới: "Tính giá trị của biểu thức: $B = …$". Đáp số đã kiểm: $B = 5$. Hai mốc 0,25.
 6) (0,5) phương trình chứa căn — GIỮ NGUYÊN ý 5 hiện tại.""",
        bai4="""Bài IV mới (3,5 điểm):
 1) (1,0 điểm) gồm a) và b):
   a) (0,5) GIỮ NGUYÊN câu lượng giác (toà tháp) hiện tại.
   b) (0,5) MỚI — độ dài cung: chép NGUYÊN VĂN câu quạt giấy (CHỈ ý a: cung tròn lớn nhất) Bài IV.1 đề THCS Chu Văn An 2025–2026 (PDF). Đáp số đã kiểm: $\\pi \\cdot 2{,}2 \\approx 6{,}9$ dm. Lời giải: công thức độ dài cung $l = \\dfrac{\\pi R n}{180}$ với $n = 180^\\circ$ (0,25) → thay số, làm tròn, "Vậy …" (0,25).
 2) (2,5 điểm) GIỮ phần giả thiết NHƯNG BỎ câu "Kẻ cát tuyến $AMN$ qua tâm $O$ …" và bỏ đoạn chứng minh $AM \\cdot AN$. Chia lại 4 ý:
   a) (1,0) bốn điểm $A, B, O, C$ — GIỮ NGUYÊN.
   b) (0,5) "Chứng minh $OA \\perp BC$ tại $H$." — lời giải lấy từ phần đầu 2b hiện tại (tính chất hai tiếp tuyến cắt nhau ⇒ đường trung trực), 2 mốc 0,25.
   c) (0,5) "Chứng minh $AH \\cdot AO = AB^2$." — lời giải lấy từ 2b hiện tại (đồng dạng g.g), 2 mốc 0,25.
   d) (0,5) đề và lời giải = 2c hiện tại ($K$ là trung điểm của $CE$), gộp barem còn 2 mốc 0,25 (giữ đủ các dòng suy luận).""",
    ),
    "on-2": dict(
        cau=["dongda", "nguyendu"],
        bai3="""Bài III mới (2,5 điểm), 6 ý, thứ tự và điểm:
 1) (0,5) hệ phương trình — GIỮ NGUYÊN ý 1 hiện tại.
 2) (0,25) MỚI — phương trình tích: chép NGUYÊN VĂN Bài I.1 đề THCS Đống Đa 2025–2026 (PDF): $(x + 1)(2x - 3) = 0$. Đáp số: $x = -1$; $x = \\dfrac{3}{2}$. Một mốc 0,25 ở dòng kết luận.
 3) (0,5) phương trình chứa ẩn ở mẫu — GIỮ NGUYÊN ý 2 hiện tại.
 4) (0,5) bất phương trình — GIỮ NGUYÊN ý 3 hiện tại.
 5) (0,25) tính $\\sqrt{98} - \\sqrt{32} + \\sqrt{2}\\left(\\sqrt{8} - 3\\right)$ — GIỮ đề ý 4 hiện tại, rút lời giải còn MỘT mốc 0,25.
 6) (0,5) phương trình chứa căn — GIỮ NGUYÊN ý 5 hiện tại.
Hiện ý 1 và ý 2 in chung một dòng ("\\qquad"); bản mới cho ý 1 (hệ) một dòng riêng, ý 2 và ý 3 chung một dòng bằng " \\qquad ".""",
        bai4="""Bài IV mới (3,5 điểm):
 1) (1,0 điểm) gồm a) và b):
   a) (0,5) GIỮ NGUYÊN câu tàu ngầm hiện tại.
   b) (0,5) MỚI — diện tích hình quạt: chép NGUYÊN VĂN câu quạt giấy (CHỈ ý a: diện tích chiếc quạt) Bài IV.1 đề THCS Nguyễn Du 2025–2026 (PDF). Đáp số đã kiểm: $\\dfrac{\\pi \\cdot 25^2 \\cdot 150}{360} \\approx 818$ cm$^2$. Lời giải: công thức $S = \\dfrac{\\pi R^2 n}{360}$ (0,25) → thay số, làm tròn, "Vậy …" (0,25).
 2) (2,5 điểm) GIỮ phần giả thiết. Chia lại 4 ý:
   a) (1,0) $\\triangle AEB$ vuông tại $E$ — GIỮ NGUYÊN.
   b) (0,5) MỚI (tính chất hai tiếp tuyến cắt nhau): "Chứng minh $OC \\perp AD$." Sơ đồ: $CA = CD$ (tính chất hai tiếp tuyến cắt nhau), $OA = OD$ ⇒ $OC$ là đường trung trực của $AD$ (0,25) ⇒ $OC \\perp AD$ (0,25).
   c) (0,5) "Chứng minh $CE \\cdot CB = CA^2$." — lời giải lấy từ 2b hiện tại, 2 mốc 0,25. BỎ vế "$\\widehat{CDE} = \\widehat{CBD}$" KHỎI ĐỀ, TRỪ KHI lời giải ý d hiện tại cần dùng nó: khi đó giữ nó trong đề ý c và ghi lí do vào ghi_chu.
   d) (0,5) đề và lời giải = 2c hiện tại ($B, I, C$ thẳng hàng), gộp barem còn 2 mốc 0,25 (giữ đủ các dòng suy luận).""",
    ),
    "on-3": dict(
        cau=["lyson", "quocoai", "phucdong"],
        bai3="""Bài III mới (2,5 điểm), 6 ý, thứ tự và điểm:
 1) (0,5) hệ phương trình — GIỮ NGUYÊN ý 1 hiện tại.
 2) (0,25) MỚI — phương trình tích: chép NGUYÊN VĂN Bài I.2 ý a đề THCS Lý Sơn 2025–2026 (PDF): $(x - 5)(5x - 1) = 0$. Đáp số: $x = 5$; $x = \\dfrac{1}{5}$. Một mốc 0,25 ở dòng kết luận.
 3) (0,5) phương trình chứa ẩn ở mẫu — GIỮ NGUYÊN ý 2 hiện tại.
 4) (0,5) bất phương trình — GIỮ NGUYÊN ý 3 hiện tại.
 5) (0,25) MỚI — thay ý 4 hiện tại (biểu thức $M$ có trục căn, BỎ hẳn): chép NGUYÊN VĂN Bài II.1 ý a đề Phòng GD\\&ĐT Quốc Oai 2024–2025 (PDF): "Rút gọn biểu thức: $2\\sqrt{8} - 3\\sqrt{18} + 4\\sqrt{50}$". Đáp số: $15\\sqrt{2}$. Một mốc 0,25.
 6) (0,5) phương trình chứa căn — GIỮ NGUYÊN ý 5 hiện tại.""",
        bai4="""Bài IV mới (3,5 điểm):
 1) (1,0 điểm) gồm a) và b):
   a) (0,5) GIỮ NGUYÊN câu chiếc thang hiện tại.
   b) (0,5) MỚI — hình vành khuyên: chép NGUYÊN VĂN Bài IV.1 đề THCS Phúc Đồng 2025–2026 (PDF), BỎ chữ "(hình 1)" vì đề ôn không in hình. Đáp số đã kiểm: $\\pi(6^2 - 1{,}5^2) = 33{,}75\\pi \\approx 106$ cm$^2$. Lời giải: công thức $S = \\pi(R^2 - r^2)$ (0,25) → thay số, làm tròn, "Vậy …" (0,25).
 2) (2,5 điểm) GIỮ phần giả thiết. Chia lại 3 ý:
   a) (1,0) — GIỮ NGUYÊN.
   b) (1,0) — GIỮ NGUYÊN.
   c) (0,5) CHỈ còn "Chứng minh đường thẳng $FD$ là tiếp tuyến của $(O; R)$." (BỎ vế $AF \\cdot BH = BF \\cdot AH$ ở cả đề lẫn lời giải), 2 mốc 0,25.""",
    ),
}

LUAT = r'''## Luật trình bày (giáo viên đã chốt — vi phạm là bị trả lại)
- "GIỮ NGUYÊN" nghĩa là chép lại Y HỆT chuỗi hiện tại (chỉ đổi số thứ tự ý và điểm ghi trên đầu nếu thay đổi). Không "làm đẹp" ý giữ nguyên.
- Câu MỚI: chép NGUYÊN VĂN từ ảnh PDF đề gốc (ảnh <tên-pdf>-trang-N.png, text <tên-pdf>.txt). Nội dung bóc sẵn bên dưới chỉ để tìm câu; ảnh PDF là chuẩn. Đề gốc và bản bóc lệch nhau ⇒ theo ảnh và ghi vào ghi_chu.
- Đề: mỗi ý mở đầu "N) \\textbf{(0,5 điểm)} …"; ý con của IV.1 là "a) \\textbf{(0,5 điểm)} …"; nối các ý bằng " [[br]] ". Phần mở đầu "\\textbf{(2,5 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:" của Bài III giữ nguyên (có thể thêm ", tính giá trị biểu thức" nếu cần). Bài IV mở đầu "\\textbf{(3,5 điểm)} [[br]] 1) \\textbf{(1,0 điểm)} [[br]] a) …".
- Lời giải: mỗi phần tử "dap_an" là MỘT ý, dạng "\\textbf{1) (0,5đ)} [[br]] dòng [[br]] dòng \\hfill \\textit{(0,25đ)} [[br]] …" — y như các chuỗi hiện tại. Nhãn: Bài III "1)"…"6)"; Bài IV "1a)", "1b)", "2a)", "2b)"…. Mốc chấm là " \\hfill \\textit{(0,25đ)}" cuối dòng; TỔNG các mốc trong một ý PHẢI bằng đúng điểm ý.
- Mỗi dòng một bước, dừng đúng chỗ, như bài thi. Không nêu kết luận trước khi chứng minh. Không dùng $\Leftrightarrow$. Không văn nói, không xưng hô ("em", "ta thấy dễ dàng"…), không viết tắt (trừ ĐKXĐ, g.g). Toán trong $…$, số thập phân $0{,}5$, phân số \dfrac, đồng dạng \backsim. Giữ escape \% \& \#.
- Bài hình: KHÔNG dùng hệ thức lượng $b^2 = ab'$ hay tứ giác nội tiếp (chưa học ở học kì 1, sách Kết nối tri thức) — qua tam giác đồng dạng.
- "mt": mỗi ý một dòng ma trận {"ma","nd","chu_de","muc","diem","phut","nguon"}. Mã: Bài III "IIIa"…"IIIf"; Bài IV "IVa" (lượng giác), "IVa2" (cung/quạt/vành khuyên), "IVb1"…; chu_de: hệ/PT "ĐS I", BPT "ĐS II", căn "ĐS III", lượng giác "HH IV", đường tròn + cung/quạt "HH V". muc ∈ NB/TH/VD/VDC. Ý giữ nguyên ⇒ chép dòng ma trận hiện tại (chỉ sửa ma, diem, phut nếu đổi). nguon: ý giữ nguyên ⇒ y như hiện tại; ý mới ⇒ đúng chuỗi tên trường cho bên dưới.
- "phut" (phút học sinh tầng C làm): ý 0,25 một bước 2–3; trục căn 0,5 khoảng 5; cung/quạt/vành khuyên 0,5 khoảng 4; ý hình bị rút điểm ⇒ giảm phút tương ứng. MỤC TIÊU: tổng phút Bài III + Bài IV mới KHÔNG vượt tổng hiện tại.
- "note": ghi chú giáo viên của bài (giữ ý cũ, thêm một câu cho phần mới nếu cần).
- "bay": thay TOÀN BỘ các dòng bẫy có vị trí bắt đầu "Bài III" hoặc "Bài IV" bằng danh sách mới (đánh lại vị trí theo số ý mới; bỏ dòng của ý đã bỏ; thêm tối đa 1 dòng cho câu mới nếu có bẫy thật). Mỗi dòng {"vi_tri","noi_dung","loi","cach"}.
- TỰ TÍNH LẠI mọi đáp số câu mới; lệch với "đáp số đã kiểm" ⇒ ghi ghi_chu, KHÔNG tự đổi số.
- Chuỗi JSON: gạch chéo ngược nhân đôi.
'''


def mo_ta_bai(b):
    mt = "\n".join(f"   {r}" for r in b["mt"])
    da = "\n".join(f"   [{i}] {a}" for i, a in enumerate(b["dap_an"]))
    return (f"### {b['label']}\nstatement:\n   {b['statement']}\ndap_an (mỗi phần tử một ý):\n{da}\n"
            f"mt (ma, nội dung, chủ đề, mức, điểm, phút, nguồn):\n{mt}\nnote: {b.get('note', '')}\n")


def main():
    DE = nap_de()
    for k, kh in KE_HOACH.items():
        D = DE[k]
        b3, b4 = D["bai"][2], D["bai"][3]
        assert (b3["label"], b4["label"]) == ("Bài III.", "Bài IV."), k
        phut = sum(r[5] for b in (b3, b4) for r in b["mt"])
        bay = [x for x in D["bay"] if x[0].startswith(("Bài III", "Bài IV"))]
        cau = "\n".join(f"- {CAU[c][0]} — file {CAU[c][1]} — {CAU[c][2]}: «{CAU[c][3]}» ⇒ đáp số đã kiểm {CAU[c][4]}"
                        for c in kh["cau"])
        prompt = f'''Bạn là thợ sửa ĐỀ ÔN TẬP CUỐI KÌ 1 Toán 9 (Hà Nội, sách Kết nối tri thức) cho học sinh tầng C. Đây là {D["ten"]}. Làm CẨN THẬN, CHỈ sửa đúng phạm vi, KHÔNG bịa đề. KHÔNG chạy lệnh: dữ liệu nằm trong prompt và các file ảnh/text đề gốc trong thư mục làm việc.

## Vì sao sửa
Thống kê 41 đề cuối kì 1 thật ở Hà Nội cho thấy đề ôn này thiếu các dạng dễ học sinh tầng C làm được (phương trình tích, căn dạng số, trục căn, độ dài cung/diện tích quạt/vành khuyên, tính chất hai tiếp tuyến). Giáo viên đã chốt khung mới: Bài III 6 ý (4 ý 0,5 + 2 ý 0,25), Bài IV.1 thành 1,0 điểm (lượng giác + cung/quạt), bài hình còn 2,5 điểm. Bài I, II, V không đụng. Tổng phút hiện tại của Bài III + Bài IV: {phut}.

## Kế hoạch (bất di bất dịch)
{kh["bai3"]}

{kh["bai4"]}

## Câu mới lấy từ đề thật
{cau}

{LUAT}
## Bài III và Bài IV HIỆN TẠI
{mo_ta_bai(b3)}
{mo_ta_bai(b4)}
### Các dòng bẫy hiện tại của Bài III, Bài IV (vi_tri, noi_dung, loi, cach)
{json.dumps(bay, ensure_ascii=False, indent=1)}

## Đầu ra
JSON đúng schema: {{"bai3": {{"statement", "dap_an": [6 chuỗi], "mt": [6 dòng], "note"}}, "bai4": {{"statement", "dap_an": [...], "mt": [...], "note"}}, "bay": [...], "ghi_chu": "chỗ nghi ngờ, chỗ đề gốc lệch bản bóc, hoặc chuỗi rỗng"}}
'''
        viec = {
            "id": f"phu-dang-l9-{k}",
            "model": "gemini-3.8-flash-high",
            "prompt": prompt,
            "files": [PDF + CAU[c][1] for c in kh["cau"]],
            "render": True,
            "schema": "scripts/gemini/schema/phu-dang-de-on.json",
            "timeout": "1500s",
            "meta": {"loai": "phu-dang-de-on", "de": k, "nguon": {CAU[c][0]: c for c in kh["cau"]}},
        }
        p = REPO / "storage/gemini/hang-doi" / f"{viec['id']}.json"
        p.write_text(json.dumps(viec, ensure_ascii=False, indent=2))
        print("ghi", p.relative_to(REPO), "| phút III+IV hiện tại", phut, "| prompt", len(prompt), "kí tự")


if __name__ == "__main__":
    main()
