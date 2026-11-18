#!/usr/bin/env python3
"""Việc Gemini cho chương VII lớp 9C (18/11/2026), luật giao Gemini lần 3 (16/11):
Claude chốt khung (mã câu, vai, mức, số câu — scripts/chon_cau_ch7_9c.py), thợ viết chữ.

1) cc-ch7-9c        : chấm T1–T7 + lí do chấm + đề xuất (Hay / Cân nhắc / Không hay) + nghi ngờ cho 53 dòng.
2) tm-ch7-9c-chu    : chữ thuyết minh (mô tả từng dòng, kiến thức nền, lý thuyết, ví dụ, lỗi sai, kiến thức NB).

    python3 scripts/gemini/viec_chon_cau_ch7_9c.py
    python3 scripts/gemini/tho.py --mot cc-ch7-9c ; python3 scripts/gemini/tho.py --mot tm-ch7-9c-chu
Sau đó: python3 scripts/chon_cau_ch7_9c.py --ghi && python3 scripts/tm_ch7_9c.py --ghi
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
CHON = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07/chon-cau.json"
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-07.json"
SCHEMA_CC = REPO / "scripts/gemini/schema/cham-chon-cau.json"
SCHEMA_TM = REPO / "scripts/gemini/schema/chu-tm-chuong.json"
MODEL = "gemini-4-hydrogen-medium"

BOI_CANH = r'''## Bối cảnh lớp 9C (đã chốt, KHÔNG bàn lại)
- Lớp C = học lực trung bình – trung bình khá, Hà Nội, ôn thi vào 10. Chương VII (Tần số và tần số tương đối, SGK Toán 9 tập hai Kết nối tri thức, Bài 22, 23, 24) dạy NÉN trong MỘT buổi 180 phút (tuần 31): ví dụ GV làm mẫu ~30 phút, trên lớp 120 phút, BTVN ~86 phút. Kiểm tra chương gộp với chương VIII ở buổi khác.
- Đề vào 10 Hà Nội: Câu I.1 (thống kê) chỉ NB/TH, ma trận Sở mạch Thống kê KHÔNG có VD ⇒ phiếu KHÔNG có câu VD (khuôn 40% NB – 60% TH theo phút).
- Khuôn Câu I.1 đề Sở lặp 3/3 đề: cho bảng/biểu đồ tần số ghép nhóm ⇒ "Xác định tần số và tần số tương đối của nhóm [a; b)" (2026: 50 HS, nhóm [150; 155) tần số 14 ⇒ 28%; 2025: 300 HS, [12; 16) tần số 75 ⇒ 25%; minh họa: 40 lớp, [40; 42) tần số 5 ⇒ 12,5%).
- Tần suất dạng trong đề thật (% đề Vào 10 / CK2 / GK2; 36/32/22 đề): tần số tương đối một nhóm (C7-02) 69/78/86 · lập bảng tần số, cỡ mẫu (C7-01) 25/44/55 · nhóm gộp / đếm theo điều kiện (C7-03) 19/19/18 · ghép nhóm số liệu thô (C7-05) 8/6/18 · kiểm tra nhận định (C7-09) 11/3/9 · tính ngược n = f·N, ước lượng (C7-04) 8/9/0.
- Tổ trưởng chốt 17/11: DẠY C7-01…05, C7-09; C7-10 (biểu đồ lớp 8) chỉ là một câu NB kiến thức cũ; KHÔNG dạy vẽ biểu đồ cột/đoạn thẳng (C7-06), vẽ quạt tròn (C7-07), chọn biểu đồ (C7-08).
- Luật hình thức câu (16/11): NB = MỘT bước (đọc một số, nhắc công thức, một phép chia), 1,5 phút; câu NB là trắc nghiệm, Đúng/Sai hoặc trả lời ngắn. TH = bài gọn có câu hỏi gợi ý bước, 6 phút. "Số câu NB" của dòng TH là số câu nhỏ tách từ chính đề đó. Điền khuyết CHỈ dùng ở vai "Ví dụ". BTVN cùng dạng đã học trên lớp, đề ngắn.
- Mỗi bài gốc chỉ bốc một lần; các cặp trùng số liệu đã được loại bằng máy.
'''

PROMPT_CC = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm dạy lớp C ở Hà Nội, giúp tổ trưởng CHẤM danh sách câu đã bốc cho phiếu chương VII lớp 9C. KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

''' + BOI_CANH + r'''
## Việc của bạn — với TỪNG dòng
1. Chấm 7 tiêu chí, mỗi tiêu chí 0 / 1 / 2 (đúng thứ tự):
   T1 Trọng tâm SGK (đúng kiến thức trọng tâm Bài 22–24) · T2 Ý toán (rèn được một ý toán rõ) · T3 Bối cảnh (bối cảnh thực tế gần gũi, dễ hiểu) · T4 Phân hoá (có ý dễ – ý khó hơn) · T5 Lỗi sai (bắt được lỗi hay gặp) · T6 Số đẹp (phép chia ra số gọn, ít làm tròn) · T7 Dạng đề thi (đúng khuôn đề CK2/GK2/vào 10).
   Câu NB kiến thức cũ chấm T1 theo bài nền nó phục vụ, không chấm 0. Ngưỡng tổ trưởng dùng: NB ≥ 5/10, TH ≥ 6/10 (điểm = Σ Tᵢ·Wᵢ / 26 · 10, W = 3,1,2,1,2,2,2) — đừng nâng điểm cho đủ ngưỡng; câu yếu thật thì chấm thật.
2. "ly_do": TỐI ĐA 25 chữ, nói vì sao câu này đáng dạy ở vai/dạng đó, nêu số liệu then chốt và đáp số bạn TỰ TÍNH (vd "Khuôn I.1 đề Sở 2026: nhóm [150; 155) tần số 14, cỡ mẫu 50 ⇒ 28%."). Không chép lại đề.
3. "de_xuat": Hay | Cân nhắc | Không hay.
   - Hay: đúng dạng, đúng vai, vừa sức lớp C, số đẹp, không gần trùng ý dòng khác cùng vai. Phần lớn dòng nên Hay nếu không có vấn đề thật.
   - Cân nhắc: có MỘT điểm cụ thể tổ trưởng nên nhìn (gần trùng ý dòng khác — ghi mã; số lẻ phải làm tròn; ý bốc lệch dạng; mức có vẻ lệch: "NB" mà cần ≥ 2 bước, "TH" mà chỉ 1 bước; đề cần vẽ biểu đồ).
   - Không hay: sai dạng, cần vẽ biểu đồ (không dạy), trùng hẳn dòng khác, số liệu sai/không khớp.
4. "nghi_ngo": tự giải từng câu; nếu đề có số không khớp (tổng tần số ≠ cỡ mẫu ghi trong đề, % cộng ≠ 100%, nhãn biểu đồ sai), hoặc ý bốc không có trong đề ⇒ ghi ngắn. Không có ⇒ "".

## Dạng (mã C7 ⇒ kỹ thuật con)
{DANG}

## Đầu ra
JSON đúng schema: {"dong": [{"ma", "T", "ly_do", "de_xuat", "nghi_ngo"}], "ghi_chu": ""}. "T" là mảng 7 số nguyên 0–2. Đủ MỌI dòng, đúng "ma", đúng thứ tự.

## Dữ liệu ({SO} dòng, JSON)
'''

PROMPT_TM = r'''Bạn là giáo viên Toán 9, viết CHỮ cho bản THUYẾT MINH chương VII lớp 9C (văn bản tổ trưởng đọc để duyệt khung phiếu). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt. Khung số (dòng nào, bao nhiêu câu, câu nào) ĐÃ CHỐT — bạn chỉ viết chữ.

''' + BOI_CANH + r'''
## Quy ước chữ
- LaTeX trong chuỗi JSON: toán đặt trong $...$ (vd $[150;155)$, $f=\dfrac{m}{N}\cdot 100\%$), dấu phần trăm ngoài toán viết \%, in đậm \textbf{...}. KHÔNG dùng ký tự toán unicode (≤, ≥, ⇒, ·, ×) ngoài $...$ — trong $...$ dùng \le, \ge, \Rightarrow, \cdot. Số thập phân dùng dấu phẩy kiểu Việt Nam trong $...$ viết {,} (vd $12{,}5\%$).
- Văn viết, câu đủ chủ vị, không văn nói, không viết tắt (viết "tần số tương đối", không "TSTĐ"; "học sinh", không "HS"; "giáo viên", không "GV").
- Không bịa số liệu: chỉ dùng số có trong đề được cung cấp; tự tính lại mọi đáp số trước khi ghi.

## Phải viết
1. "d_text": object, mỗi khoá trong danh sách KHOÁ bên dưới ⇒ một câu mô tả dòng thuyết minh (≤ 45 chữ), nói học sinh làm gì ở dòng đó, gom các kiểu đề trong dòng (dựa vào đề các câu được liệt kê). Khoá "…|NB" = câu NB lẻ; "…|TACH" = câu nhỏ tách từ đề TH (bắt đầu bằng "Câu nhỏ tách từ đề …: …"); "…|TH" = bài TH có câu hỏi gợi ý bước; "C7-10|KTC" = câu NB kiến thức cũ — bắt đầu bằng "Ôn lớp 8: …".
2. "kien_thuc_nen": 3–4 gạch đầu dòng, mỗi dòng dạng "\textbf{Tên kiến thức} (Lớp mấy): dùng ở đâu trong phiếu" — vd đọc biểu đồ cột, biểu đồ tranh, biểu đồ hình quạt tròn (lớp 6–8), tỉ số phần trăm (lớp 6–7), làm tròn số thập phân.
3. "lythuyet": 4–5 gạch đầu dòng: \textbf{Mục tiêu chương}; \textbf{Chuẩn đầu ra} (làm trọn Câu I.1 đề vào 10); \textbf{Tần suất dạng trong đề thật} (dùng đúng số % ở trên); \textbf{Hình thức câu hỏi} (luật 16/11, không có câu vận dụng và lí do); \textbf{Không dạy ở lớp 9C} (vẽ biểu đồ cột, đoạn thẳng, hình quạt tròn; chọn loại biểu đồ; kiểm tra chương riêng).
4. "vidu": 1–2 gạch đầu dòng bắt đầu "Buổi 1: …" liệt kê ngắn các ví dụ giáo viên làm mẫu (theo các dòng vai "Ví dụ"), mỗi ví dụ nêu số liệu then chốt.
5. "loisai": 5–7 lỗi sai thường gặp ở lớp C với các dạng này (vd đếm nhầm đầu mút nhóm $[a;b)$ lấy cả $b$; lấy tần số chia cho số nhóm thay vì cỡ mẫu; quên cộng cả bảng ra cỡ mẫu khi đề không ghi; làm tròn sai; "từ … trở lên", "dưới", "ít nhất" lấy thiếu/thừa nhóm; tổng tần số tương đối không bằng $100\%$).
6. "kienthuc_nb": 4–6 dòng KIẾN THỨC THUẦN SGK (định nghĩa, công thức), KHÔNG có mẹo, KHÔNG nói "khuôn đề", "thang điểm", KHÔNG câu hỏi: tần số của một giá trị, bảng tần số, cỡ mẫu; tần số tương đối $f=\dfrac{m}{N}\cdot 100\%$ và bảng tần số tương đối (tổng $100\%$); nhóm số liệu $[a;b)$ gồm các giá trị $x$ với $a\le x<b$, tần số và tần số tương đối ghép nhóm; giá trị đại diện $\dfrac{a+b}{2}$. Mỗi dòng ghi nguồn "(SGK Toán 9 tập hai, Bài 22)" … đúng bài.

## Đầu ra
JSON đúng schema: {"d_text": {khoá: chuỗi}, "kien_thuc_nen": [], "lythuyet": [], "vidu": [], "loisai": [], "kienthuc_nb": [], "ghi_chu": ""}. "d_text" có ĐỦ mọi khoá dưới đây, không thêm khoá lạ.

## KHOÁ và các câu thuộc dòng đó (JSON)
'''


def bang_dang():
    dm = json.loads(KHUNG.read_text())["danh_muc_dang"]["dang"]
    g = {}
    for d in dm:
        g.setdefault(d.get("dang", "?"), []).append(f"{d['ma']} ({d['muc_goc']}) {d['ten']} — cách làm: {d['cach_lam']}")
    return "\n".join(f"- {c}: " + "; ".join(v) for c, v in sorted(g.items()))


def ghi_schema():
    dong = {"type": "object", "required": ["ma", "T", "ly_do", "de_xuat", "nghi_ngo"],
            "properties": {"ma": {"type": "string"},
                           "T": {"type": "array", "items": {"type": "integer"}},
                           "ly_do": {"type": "string"},
                           "de_xuat": {"type": "string", "enum": ["Hay", "Cân nhắc", "Không hay"]},
                           "nghi_ngo": {"type": "string"}}}
    SCHEMA_CC.write_text(json.dumps({"type": "object", "required": ["dong", "ghi_chu"], "properties": {
        "dong": {"type": "array", "items": dong}, "ghi_chu": {"type": "string"}}}, ensure_ascii=False, indent=2) + "\n")
    ds = {"type": "array", "items": {"type": "string"}}
    SCHEMA_TM.write_text(json.dumps({"type": "object",
        "required": ["d_text", "kien_thuc_nen", "lythuyet", "vidu", "loisai", "kienthuc_nb", "ghi_chu"],
        "properties": {"d_text": {"type": "object", "additionalProperties": {"type": "string"}},
                       "kien_thuc_nen": ds, "lythuyet": ds, "vidu": ds, "loisai": ds, "kienthuc_nb": ds,
                       "ghi_chu": {"type": "string"}}}, ensure_ascii=False, indent=2) + "\n")


def main():
    import tm_ch7_9c as tm
    ghi_schema()
    rows = json.loads(CHON.read_text())
    hd = REPO / "storage/gemini/hang-doi"
    data = [{"ma": r["ma"], "vai": r["vai"], "dang": r["dang"], "muc": r["muc"], "so_y_TH": r["so_y"],
             "so_cau_NB": r["so_nb"], "y_boc": r["y"], "loai": r["loai"], "hinh_thuc": r["hinh_thuc"],
             "de": r["de"], "nguon": r["nguon"]} for r in rows]
    vid = "cc-ch7-9c"
    if "--lai" in sys.argv:   # lượt chấm lại các dòng đổi: --lai ma1,ma2 [--ghi-chu "..."]
        chi = sys.argv[sys.argv.index("--lai") + 1].split(",")
        data = [d for d in data if d["ma"] in chi]
        vid = sys.argv[sys.argv.index("--id") + 1] if "--id" in sys.argv else "cc-ch7-9c-b"
        if "--ghi-chu" in sys.argv:
            for d in data:
                d["ghi_chu_to_truong"] = sys.argv[sys.argv.index("--ghi-chu") + 1]
    pr = PROMPT_CC.replace("{DANG}", bang_dang()).replace("{SO}", str(len(data))) + \
        json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    viec = {"id": vid, "model": MODEL, "prompt": pr, "files": [],
            "schema": str(SCHEMA_CC.relative_to(REPO)), "timeout": "1500s",
            "meta": {"loai": "cham-chon-cau", "ma": [d["ma"] for d in data]}}
    if "--thu" not in sys.argv:
        (hd / f"{vid}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print(vid, len(data), "dòng", len(pr), "kí tự")

    if "--lai" in sys.argv:
        return
    khoa = {}
    for (dang, g), items in tm.nhom_dong(rows):
        khoa[f"{dang}|{g}"] = [{"ma": r["ma"], "vai": r["vai"], "y_boc": r["y"], "so_cau": r[f],
                                "de": r["de"][:600]} for r, f in items]
    pr = PROMPT_TM + json.dumps(khoa, ensure_ascii=False, indent=1) + "\n"
    viec = {"id": "tm-ch7-9c-chu", "model": MODEL, "prompt": pr, "files": [],
            "schema": str(SCHEMA_TM.relative_to(REPO)), "timeout": "1200s",
            "meta": {"loai": "chu-tm-chuong", "khoa": list(khoa)}}
    if "--thu" not in sys.argv:
        (hd / "tm-ch7-9c-chu.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("tm-ch7-9c-chu", len(khoa), "khoá", len(pr), "kí tự")


if __name__ == "__main__":
    main()
