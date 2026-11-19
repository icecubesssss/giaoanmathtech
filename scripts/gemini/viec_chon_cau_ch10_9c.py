#!/usr/bin/env python3
"""Việc Gemini cho chương X lớp 9C (19/11/2026), luật giao Gemini lần 3 (16/11):
Claude chốt khung (mã câu, vai, mức, số câu — scripts/chon_cau_ch10_9c.py), thợ viết chữ.

1) cc-ch10-9c       : chấm T1–T7 + lí do chấm + đề xuất (Hay / Cân nhắc / Không hay) + nghi ngờ cho 31 dòng.
2) tm-ch10-9c-chu   : chữ thuyết minh (mô tả từng dòng, kiến thức nền, lý thuyết, ví dụ, dạng VD, lỗi sai, kiến thức NB).

    python3 scripts/gemini/viec_chon_cau_ch10_9c.py
    python3 scripts/gemini/tho.py --mot cc-ch10-9c ; python3 scripts/gemini/tho.py --mot tm-ch10-9c-chu
Sau đó: python3 scripts/chon_cau_ch10_9c.py --ghi && python3 scripts/tm_ch10_9c.py --ghi
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
CHON = REPO / "inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10/chon-cau.json"
KHUNG = REPO / "config/khung-phan-dang/lop-9-hinh-hoc-chuong-10.json"
SCHEMA_CC = REPO / "scripts/gemini/schema/cham-chon-cau.json"
SCHEMA_TM = REPO / "scripts/gemini/schema/chu-tm-chuong-vd.json"
MODEL = "gemini-4-hydrogen-medium"

BOI_CANH = r'''## Bối cảnh lớp 9C (đã chốt, KHÔNG bàn lại)
- Lớp C = học lực trung bình – trung bình khá, Hà Nội, ôn thi vào 10. Chương X (Một số hình khối trong thực tiễn, SGK Toán 9 tập hai Kết nối tri thức, Bài 31 Hình trụ và hình nón, Bài 32 Hình cầu) dạy NÉN trong HAI buổi 90 phút:
  • Phiếu 1 (tuần 32): đủ sáu công thức trụ – nón – cầu. Quỹ: giáo viên giảng ~25 phút (lý thuyết + ví dụ mẫu), luyện tập trên lớp ~55 phút, bài tập về nhà ~40 phút. Đích = Bài 5 đề CK2 THCS Đoàn Thị Điểm (ly hình trụ đường kính 5 cm, nước cao 10 cm, thả 5 viên bi làm nước dâng tới miệng ly 15 cm, ý b hỏi BÁN KÍNH mỗi viên bi) — cùng khuôn Câu IV.1 đề minh họa của Sở.
  • Phiếu 2 (tuần 33): luyện tập 45 phút + kiểm tra chương 45 phút. Đích = Câu IV.1 đề chính thức vào 10 Hà Nội 2026 (xô hình trụ cao 25 cm, bán kính đáy 12 cm; ý b đếm số xô ít nhất đổ đầy bể 150 lít, làm tròn LÊN).
- Khuôn Câu IV.1 đề Sở (1,0 điểm) lặp 3/3 đề: ý a = diện tích xung quanh / thể tích hình trụ cho sẵn số đo; ý b = bài thực tế (minh họa: 5 viên bi làm nước dâng; 2025: thùng r = 50 cm, h = 150 cm, mực nước hạ 40 cm ⇒ số lít đã dùng; 2026: số xô).
- Tần suất dạng trong đề thật (% đề Vào 10 / CK2 / GK2; 11/27/8 đề): công thức trực tiếp C10-02 64/74/88 · thực tế một khối C10-05 36/52/88 · chia/so sánh hai vật chứa, làm tròn C10-06 27/7/0 · vật chìm = nước dâng C10-07 27/19/0 · ghép/hiệu khối C10-09 18/11/0 · nón Pythagore C10-03 0/0/0 · tính ngược C10-04 0/7/0 · lật ngược chai C10-08 0.
- Tổ trưởng chốt 19/11: DẠY C10-01 … C10-09; C10-03, C10-04, C10-08 dạy trong khung (không làm đích, không làm câu vận dụng); KHÔNG dạy C10-10, 11, 12 (tỉ số đồng dạng nón, khối nội/ngoại tiếp, cực trị).
- Luật hình thức câu (16/11): NB = MỘT bước (đọc số đo, đổi đường kính ra bán kính, thay vào MỘT công thức), câu NB là trắc nghiệm hoặc trả lời ngắn. TH = bài gọn có câu hỏi gợi ý bước. VD = chỉ đề, học sinh tự giải. "Số câu NB" của dòng TH/VD là số câu nhỏ tách từ chính đề đó (thường là ý a). Điền khuyết CHỈ dùng ở vai "Ví dụ". Dòng có ghi "CHỈ bước đầu" / "CHỈ bước tách khối" nghĩa là phiếu chỉ hỏi bước đầu của bài gốc nhiều bước.
- Ba bẫy của chương: (1) đề cho ĐƯỜNG KÍNH; (2) chiều cao lấy theo MỰC NƯỚC, không phải chiều cao bình; (3) đổi đơn vị 1 dm³ = 1 lít, 1 m³ = 1000 lít, 1 cm³ = 1 ml. Ý tưởng duy nhất ngoài công thức: thể tích vật chìm = thể tích nước dâng thêm / tràn ra.
- Mỗi bài gốc chỉ bốc một lần; các nhóm trùng số liệu đã được loại bằng tay.
'''

PROMPT_CC = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm dạy lớp C ở Hà Nội, giúp tổ trưởng CHẤM danh sách câu đã bốc cho hai phiếu chương X lớp 9C. KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

''' + BOI_CANH + r'''
## Việc của bạn — với TỪNG dòng
1. Chấm 7 tiêu chí, mỗi tiêu chí 0 / 1 / 2 (đúng thứ tự):
   T1 Trọng tâm SGK (đúng kiến thức trọng tâm Bài 31–32) · T2 Ý toán (rèn được một ý toán rõ) · T3 Bối cảnh (thực tế gần gũi, dễ hiểu) · T4 Phân hoá (có ý dễ – ý khó hơn) · T5 Lỗi sai (bắt được bẫy hay gặp: đường kính, mực nước, đổi đơn vị, làm tròn lên) · T6 Số đẹp (số gọn, ít làm tròn rối) · T7 Dạng đề thi (đúng khuôn Câu IV.1 / đề CK2 / GK2).
   Câu NB kiến thức cũ chấm T1 theo bài nền nó phục vụ, không chấm 0. Ngưỡng tổ trưởng dùng: NB ≥ 5/10, TH ≥ 6/10, VD ≥ 7/10 (điểm = Σ Tᵢ·Wᵢ / 26 · 10, W = 3,1,2,1,2,2,2) — đừng nâng điểm cho đủ ngưỡng; câu yếu thật thì chấm thật.
2. "ly_do": TỐI ĐA 30 chữ, nói vì sao câu này đáng dạy ở vai/dạng đó, nêu số đo then chốt và ĐÁP SỐ bạn TỰ TÍNH (lấy π ≈ 3,14 nếu đề bảo, giữ π nếu đề không bảo; vd "Khuôn IV.1 Sở 2025: r = 50, h = 150, mực hạ 40 ⇒ 314 000 cm³ = 314 lít."). Không chép lại đề.
3. "de_xuat": Hay | Cân nhắc | Không hay.
   - Hay: đúng dạng, đúng vai, đúng mức, vừa sức lớp C, không gần trùng dòng khác. Phần lớn dòng nên Hay nếu không có vấn đề thật.
   - Cân nhắc: có MỘT điểm cụ thể tổ trưởng nên nhìn (gần trùng ý dòng khác — ghi mã; số lẻ khó; mức có vẻ lệch: "NB" mà cần ≥ 2 bước, "TH" mà chỉ 1 bước, "VD" mà quá dễ; đề cần hình mà đề chữ thiếu số đo).
   - Không hay: sai dạng, thuộc dạng không dạy, trùng hẳn dòng khác, số liệu sai/không khớp, không giải được.
   ĐỪNG cho "Hay" nếu chính bạn ghi nghi ngờ về số liệu hay mức.
4. "nghi_ngo": tự giải từng câu; nếu đề có số không khớp, thiếu dữ kiện (vd cần hình mà không có số đo), đáp án đề cho sai, hoặc ý bốc không có trong đề ⇒ ghi ngắn. Không có ⇒ "".

## Dạng (mã C10 ⇒ kỹ thuật con)
{DANG}

## Đầu ra
JSON đúng schema: {"dong": [{"ma", "T", "ly_do", "de_xuat", "nghi_ngo"}], "ghi_chu": ""}. "T" là mảng 7 số nguyên 0–2. Đủ MỌI dòng, đúng "ma", đúng thứ tự. "ghi_chu": nhận xét chung (≤ 60 chữ) — cặp dòng nào gần trùng nhau, phiếu nào thiếu dạng.

## Dữ liệu ({SO} dòng, JSON)
'''

PROMPT_TM = r'''Bạn là giáo viên Toán 9, viết CHỮ cho bản THUYẾT MINH chương X lớp 9C (văn bản tổ trưởng đọc để duyệt khung phiếu). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt. Khung số (dòng nào, bao nhiêu câu, câu nào) ĐÃ CHỐT — bạn chỉ viết chữ.

''' + BOI_CANH + r'''
## Quy ước chữ
- LaTeX trong chuỗi JSON: toán đặt trong $...$ (vd $S_{xq}=2\pi rh$, $V=\dfrac{1}{3}\pi r^2h$, $V=\dfrac{4}{3}\pi R^3$), đơn vị mũ viết cm$^3$, m$^2$; dấu phần trăm ngoài toán viết \%, in đậm \textbf{...}. KHÔNG dùng ký tự toán unicode (≤, ≥, ⇒, ·, ×, π, ³, ²) ngoài $...$ — trong $...$ dùng \le, \Rightarrow, \cdot, \pi. Số thập phân trong $...$ viết {,} (vd $3{,}14$).
- Văn viết, câu đủ chủ vị, không văn nói, không viết tắt (viết "học sinh", "giáo viên", "diện tích xung quanh" — ký hiệu $S_{xq}$ được dùng trong công thức).
- Không bịa số liệu: chỉ dùng số có trong đề được cung cấp; tự tính lại mọi đáp số trước khi ghi.

## Phải viết
1. "d_text": object, mỗi khoá trong danh sách KHOÁ bên dưới ⇒ một câu mô tả dòng thuyết minh (≤ 45 chữ), nói học sinh làm gì ở dòng đó, gom các kiểu đề trong dòng (dựa vào đề các câu được liệt kê). Khoá "…|NB" = câu NB lẻ; "…|TACH" = câu nhỏ tách từ đề TH/VD (bắt đầu bằng "Câu nhỏ tách từ đề …: …"); "…|TH" = bài TH có câu hỏi gợi ý bước; "…|VD" = bài vận dụng chỉ có đề; "…|KTC" = câu NB kiến thức cũ — bắt đầu bằng "Ôn lớp 8: …" hoặc "Ôn lớp 7: …" đúng lớp của kiến thức.
2. "kien_thuc_nen": 4–5 gạch đầu dòng, mỗi dòng dạng "\textbf{Tên kiến thức} (Lớp mấy): dùng ở đâu trong phiếu" — diện tích hình tròn, chu vi đường tròn; quan hệ đường kính – bán kính; định lí Pythagore (Lớp 8); thể tích hình hộp chữ nhật (Lớp 7); đổi đơn vị thể tích, tỉ số phần trăm, làm tròn số.
3. "lythuyet": 5–6 gạch đầu dòng: \textbf{Mục tiêu chương}; \textbf{Chuẩn đầu ra} (làm trọn Câu IV.1 đề vào 10, 1,0 điểm); \textbf{Sáu công thức} (trụ, nón, cầu — viết đủ công thức); \textbf{Tần suất dạng trong đề thật} (dùng đúng số % ở trên); \textbf{Hình thức câu hỏi} (luật 16/11); \textbf{Không dạy ở lớp 9C} (C10-10, C10-11, C10-12 và lí do).
4. "vidu": 2 gạch đầu dòng bắt đầu "Buổi 1: …" và "Buổi 2: …" liệt kê ngắn các ví dụ giáo viên làm mẫu (theo các dòng vai "Ví dụ"), mỗi ví dụ nêu số đo then chốt và đáp số.
5. "dang_vd": 2–3 gạch đầu dòng, mỗi dạng vận dụng (dòng "…|VD") một gạch: "\textbf{Tên dạng} (mã, phiếu): đề …, các bước giải …, đáp số …" — gồm đích Phiếu 1 (bán kính bi), đích Phiếu 2 (số xô, làm tròn lên) và bài vận dụng ở bài tập về nhà Phiếu 2 (lật ngược chai).
6. "loisai": 6–8 lỗi sai thường gặp ở lớp C với các dạng này (thay đường kính như bán kính; lẫn $S_{xq}$ với $V$; lấy chiều cao bình thay mực nước; quên $\dfrac{1}{3}$ ở thể tích nón; đổi đơn vị sai; làm tròn xuống khi đếm số xô; nhầm đường sinh với chiều cao nón; lấy căn bậc hai thay căn bậc ba khi tìm bán kính bi).
7. "kienthuc_nb": 5–7 dòng KIẾN THỨC THUẦN SGK (định nghĩa, công thức), KHÔNG có mẹo, KHÔNG nói "khuôn đề", KHÔNG câu hỏi: yếu tố hình trụ, hình nón, hình cầu; $S_{xq}$ và $V$ hình trụ; $S_{xq}$ và $V$ hình nón; diện tích mặt cầu và thể tích hình cầu. Mỗi dòng ghi nguồn "(SGK Toán 9 tập hai, Bài 31)" hoặc "(… Bài 32)" đúng bài.

## Đầu ra
JSON đúng schema: {"d_text": {khoá: chuỗi}, "kien_thuc_nen": [], "lythuyet": [], "vidu": [], "dang_vd": [], "loisai": [], "kienthuc_nb": [], "ghi_chu": ""}. "d_text" có ĐỦ mọi khoá dưới đây, không thêm khoá lạ.

## KHOÁ và các câu thuộc dòng đó (JSON)
'''


def bang_dang():
    dm = json.loads(KHUNG.read_text())["danh_muc_dang"]
    ky = {d["ma"]: d for d in dm["dang"]}
    out = []
    for g in dm["dang_gop"]:
        if g["ma"] in ("C10-10", "C10-11", "C10-12"):
            continue
        con = "; ".join(f"{k} ({ky[k]['muc_goc']}) {ky[k]['ten']} — cách làm: {ky[k].get('cach_lam', '')}"
                        for k in g["ky_thuat"])
        out.append(f"- {g['ma']} {g['ten']}: {con}")
    return "\n".join(out)


def ghi_schema():
    ds = {"type": "array", "items": {"type": "string"}}
    SCHEMA_TM.write_text(json.dumps({"type": "object",
        "required": ["d_text", "kien_thuc_nen", "lythuyet", "vidu", "dang_vd", "loisai", "kienthuc_nb", "ghi_chu"],
        "properties": {"d_text": {"type": "object", "additionalProperties": {"type": "string"}},
                       "kien_thuc_nen": ds, "lythuyet": ds, "vidu": ds, "dang_vd": ds, "loisai": ds,
                       "kienthuc_nb": ds, "ghi_chu": {"type": "string"}}}, ensure_ascii=False, indent=2) + "\n")


def main():
    import tm_ch10_9c as tm
    ghi_schema()
    rows = json.loads(CHON.read_text())
    hd = REPO / "storage/gemini/hang-doi"
    data = [{"ma": r["ma"], "phieu": r["phieu"], "vai": r["vai"], "dang": r["dang"], "muc": r["muc"],
             "so_y_TH_VD": r["so_y"], "so_cau_NB": r["so_nb"], "y_boc": r["y"], "loai": r["loai"],
             "hinh_thuc": r["hinh_thuc"], "de": r["de"], "nguon": r["nguon"]} for r in rows]
    for d in data:   # hai dòng chỉ hỏi bước đầu của bài gốc nhiều bước
        if d["ma"] == "tl-tcnc-20-tr8":
            d["y_boc"] = "CHỈ bước đầu (lật ngược chai ⇒ phần không chứa nước là hình trụ cao 8 cm)"
        if d["ma"] == "sgk-10.18":
            d["y_boc"] = "CHỈ bước Pythagore (tính AC; phiếu đổi thành câu trả lời ngắn)"
        if d["ma"] == "v10-my-dinh-2-2026-IV1":
            d["y_boc"] = "a — CHỈ bước tách khối (ly = hình trụ cao 3 cm + nửa hình cầu bán kính 3 cm)"
    vid = "cc-ch10-9c"
    if "--lai" in sys.argv:   # lượt chấm lại các dòng đổi: --lai ma1,ma2 [--id ...]
        chi = sys.argv[sys.argv.index("--lai") + 1].split(",")
        data = [d for d in data if d["ma"] in chi]
        vid = sys.argv[sys.argv.index("--id") + 1] if "--id" in sys.argv else "cc-ch10-9c-b"
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
    for p in ("P1", "P2"):
        for (dang, g), items in tm.nhom_dong([r for r in rows if r["phieu"] == p]):
            khoa[f"{dang}|{g}"] = [{"phieu": p, "ma": r["ma"], "vai": r["vai"], "y_boc": r["y"], "so_cau": r[f],
                                    "de": r["de"][:700]} for r, f in items]
    pr = PROMPT_TM + json.dumps(khoa, ensure_ascii=False, indent=1) + "\n"
    viec = {"id": "tm-ch10-9c-chu", "model": MODEL, "prompt": pr, "files": [],
            "schema": str(SCHEMA_TM.relative_to(REPO)), "timeout": "1500s",
            "meta": {"loai": "chu-tm-chuong", "khoa": list(khoa)}}
    if "--thu" not in sys.argv:
        (hd / "tm-ch10-9c-chu.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("tm-ch10-9c-chu", len(khoa), "khoá", len(pr), "kí tự")


if __name__ == "__main__":
    main()
