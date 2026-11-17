#!/usr/bin/env python3
"""Sinh việc Gemini (Thầy 16/11/2026, sau Phiên 1 ch.VI 9C bản 2):

1) CỘT ĐỀ XUẤT cho tab "Chọn câu Ch.VI lớp 9C": Thầy "nhiều quá đọc không hết" ⇒ thợ đọc
   từng dòng, đề xuất Hay / Cân nhắc / Không hay + lí do ngắn, để Thầy chỉ đọc các dòng
   Cân nhắc / Không hay. Một việc mỗi phiếu (dx-ch6-9c-P1 … P5).
2) BỎ Δ′ (Thầy 16/11: "cái Delta' thì bỏ đi, không dạy cũng được"):
   - lí do chấm nhắc Δ′ / b′ ⇒ thợ viết lại bằng Δ = b² − 4ac (trường ly_do_cham_moi);
   - chữ thuyết minh nhắc Δ′ / b′ / công thức nghiệm thu gọn ⇒ việc tm-ch6-9c-bo-delta-phay.

    python3 scripts/gemini/viec_de_xuat_chon_cau_ch6_9c.py
    python3 scripts/gemini/tho.py --tien-to dx-ch6-9c- --song-song 3
    python3 scripts/gemini/tho.py --mot tm-ch6-9c-bo-delta-phay
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
CHON = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06/chon-cau.json"
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-06.json"
SCHEMA_DX = REPO / "scripts/gemini/schema/de-xuat-chon-cau.json"
SCHEMA_TM = REPO / "scripts/gemini/schema/sua-chu-tm.json"
MODEL = "gemini-4-hydrogen-medium"
PHAY = re.compile(r"Δ['′]|Delta'|b['′]|nghiệm thu gọn")

PHIEU = {
    "P1": "PT bậc hai + biện luận nghiệm theo Δ (có m). 32 NB + 12 TH trên lớp, KHÔNG có VD. Chưa học Viète.",
    "P2": "Viète + biểu thức ĐỐI XỨNG + tìm m theo hệ thức đối xứng. 32 NB + 8 TH + 2 VD trên lớp (120′).",
    "P3": "Viète + biểu thức KHÔNG đối xứng (hạ bậc, |x|/căn, hệ thức bậc nhất) + các dạng VD khác. 32 NB + 8 TH + 2 VD. C6-28 parabol–đường thẳng = bài làm thêm, không tính giờ.",
    "P4": "PT chứa ẩn ở mẫu quy về bậc hai + giải bài toán bằng cách lập PT (HS đã luyện lập hệ ở chương I, chỉ nhắc công thức). 32 NB + 8 TH + 2 VD.",
    "P5": "Luyện tập chung ~90′ (chữa mẫu Bài III đề thi) + đề kiểm tra chương 90′ (vai 'KT chương' chỉ là câu đề xuất cho đề).",
}

PROMPT = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm dạy lớp C (học lực trung bình – trung bình khá) ở Hà Nội, đang giúp tổ trưởng DUYỆT danh sách câu đã bốc cho một phiếu học tập chương VI (phương trình bậc hai, Viète, lập phương trình). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

Tổ trưởng có quá nhiều dòng để đọc. Việc của bạn: đọc TỪNG dòng và ĐỀ XUẤT một trong ba mức, để tổ trưởng chỉ cần đọc kỹ các dòng "Cân nhắc" và "Không hay".

## Phiếu đang duyệt: {PHIEU} — {MO_TA}

## Luật hình thức câu (đã chốt 16/11/2026)
- NB = câu NHỎ gắn với đề (nhắc công thức, điều kiện, bước làm) dạng trắc nghiệm, Đúng/Sai, trả lời ngắn. "Số câu NB" của dòng TH/VD là số câu nhỏ tách từ chính đề đó.
- TH = bài gọn + câu hỏi gợi ý bước. VD = chỉ đề, học sinh tự giải. Lớp C KHÔNG làm VDC.
- Điền khuyết CHỈ dùng ở vai "Ví dụ" (giáo viên chữa mẫu). Ví dụ phải là bài mẫu chuẩn, đi trước và cùng dạng với bài trên lớp.
- BTVN: đề ngắn gọn, cùng dạng đã học trên lớp, không có dạng mới.
- Mỗi bài gốc chỉ được bốc một lần trong cả chương; hai bài khác mã nhưng cùng phương trình/cùng số liệu coi là trùng.
- Ưu tiên nghiệm đẹp; tránh số liệu quá to, phân số nhiều tầng ở lớp C.
- KHÔNG DẠY Δ′ (công thức nghiệm thu gọn) ở lớp 9C — tổ trưởng vừa bỏ ngày 16/11. Mọi bài chỉ dùng Δ = b² − 4ac. Đề gốc yêu cầu "công thức nghiệm thu gọn" / "tính Δ′" mà không đổi được sang Δ một cách tự nhiên ⇒ Không hay. Đề gốc ghi "Δ (hoặc Δ′)" hay "tính Δ′" mà chỉ cần đổi chữ thành Δ ⇒ vẫn có thể Hay/Cân nhắc, ghi rõ "phiếu đổi Δ′ thành Δ".
- Tham số m CÓ dạy. Nhẩm nghiệm x = ±1 chỉ là nhận xét nhanh, không thành dạng bài. Không dạy: đồ thị y = ax², tìm hai số biết tổng và tích, hệ thức không phụ thuộc m, VDC.

## Tiêu chí đề xuất
- "Hay": đúng dạng ghi ở dòng, đúng vai (ví dụ / trên lớp / BTVN / KT), vừa sức lớp C, số liệu đẹp, không trùng ý với dòng khác CÙNG vai trong phiếu, hình thức đúng luật trên. Phần lớn các dòng nên ở mức này nếu không có vấn đề thật.
- "Cân nhắc": có MỘT điểm tổ trưởng nên nhìn: gần trùng ý với dòng khác (ghi mã dòng kia); nghiệm/số liệu hơi xấu; đề dài hoặc nhiều ý so với vai; mức (NB/TH/VD) có vẻ lệch; đề gốc dùng Δ′ cần đổi chữ; dùng kiến thức của phiếu sau (vd Viète trong P1); lí do chấm có chỗ bạn thấy chưa đúng.
- "Không hay": sai dạng hoặc sai phiếu; quá khó (VDC) với lớp C; trùng hẳn một dòng khác; đáp số trong lí do chấm sai mà không sửa được; bắt buộc dùng Δ′.
- Đừng chấm "Cân nhắc" chỉ cho an toàn — mỗi "Cân nhắc" phải nêu được vấn đề cụ thể.

## Cách ghi
- "de_xuat": Hay | Cân nhắc | Không hay.
- "ly_do": TỐI ĐA 20 chữ, nói thẳng vấn đề hoặc điểm mạnh chính (vd "Mẫu chuẩn biện luận 3 trường hợp, nghiệm đẹp." / "Gần trùng ck2-thang-long-2025-III3: cùng x₁² + x₂² − x₁x₂."). Không chép lại đề.
- "ly_do_cham_moi": CHỈ điền khi "Lí do chấm" cũ nhắc Δ′ hoặc b′ — viết lại cả câu lí do chấm, giữ ý cũ, thay mọi Δ′ bằng Δ = b² − 4ac và TÍNH LẠI giá trị Δ (Δ = 4Δ′ khi b chẵn; tự tính lại từ đề, không nhân bừa). Dòng khác ⇒ "".
- "nghi_ngo": nếu bạn tự giải và thấy đáp số trong "Lí do chấm" sai, hoặc ý bốc không khớp đề, ghi ngắn ở đây (vd "Δ = 4m² + 8, không phải 4m² + 9"). Không có ⇒ "".
- Tự giải nhanh mọi bài có số liệu trong lí do chấm để kiểm.

## Dạng (mã C6 của tab ⇒ các dạng phương pháp con)
{DANG}

## Đầu ra
JSON đúng schema: {"dong": [{"ma", "de_xuat", "ly_do", "ly_do_cham_moi", "nghi_ngo"}], "ghi_chu": ""}. Đủ MỌI dòng dữ liệu, đúng "ma", đúng thứ tự.

## Dữ liệu phiếu {PHIEU} ({SO} dòng, JSON)
'''

PROMPT_TM = r'''Bạn là giáo viên Toán 9, sửa chữ một bản THUYẾT MINH chương VI (phương trình bậc hai) cho lớp 9C. KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

Tổ trưởng vừa chốt (16/11/2026): BỎ công thức nghiệm thu gọn Δ′ ở lớp 9C — không dạy, mọi bài chỉ dùng Δ = b² − 4ac.

Dưới đây là các đoạn chữ (LaTeX, giữ nguyên cú pháp: $...$, \\dfrac, \\textbf, \\textit, \\%) có nhắc Δ′, b′ hoặc "công thức nghiệm thu gọn". Viết lại TỪNG đoạn sao cho:
- Không còn Δ′, b′, "công thức nghiệm thu gọn"; giữ nguyên mọi ý khác, câu chữ khác giữ y nguyên càng nhiều càng tốt.
- Đoạn chỉ nói về công thức thu gọn (không còn ý gì khi bỏ) ⇒ "moi" = "" (xoá cả đoạn).
- Lỗi sai "dùng Δ′ mà vẫn chia cho 2a" ⇒ bỏ vế đó; nếu câu còn lại vẫn đủ nghĩa thì giữ.
- "Biện luận theo Δ′" ⇒ "biện luận theo Δ".
- Đoạn "Không dạy ở lớp C" (nếu có trong dữ liệu) KHÔNG phải sửa; nhưng bạn đề xuất thêm vào "them_khong_day" một cụm ngắn để chèn vào danh sách đó, vd "công thức nghiệm thu gọn $\\Delta'$ (Thầy bỏ 16/11/2026)".
- Không thêm kiến thức mới, không đổi số liệu.

## Đầu ra
JSON đúng schema: {"sua": [{"khoa", "cu", "moi"}], "them_khong_day": "", "ghi_chu": ""}. "khoa" và "cu" chép đúng từ dữ liệu.

## Dữ liệu (JSON)
'''


def bang_dang():
    dm = json.loads(KHUNG.read_text())["danh_muc_dang"]["dang"]
    g = {}
    for d in dm:
        g.setdefault(d.get("dang", "?"), []).append(f"{d['ma']} ({d['muc_goc']}) {d['ten']}")
    return "\n".join(f"- {c}: " + "; ".join(v) for c, v in sorted(g.items()))


def ghi_schema():
    dong = {"type": "object", "required": ["ma", "de_xuat", "ly_do", "ly_do_cham_moi", "nghi_ngo"],
            "properties": {"ma": {"type": "string"},
                           "de_xuat": {"type": "string", "enum": ["Hay", "Cân nhắc", "Không hay"]},
                           "ly_do": {"type": "string"}, "ly_do_cham_moi": {"type": "string"},
                           "nghi_ngo": {"type": "string"}}}
    SCHEMA_DX.write_text(json.dumps({"type": "object", "required": ["dong", "ghi_chu"], "properties": {
        "dong": {"type": "array", "items": dong}, "ghi_chu": {"type": "string"}}}, ensure_ascii=False, indent=2) + "\n")
    sua = {"type": "object", "required": ["khoa", "cu", "moi"],
           "properties": {k: {"type": "string"} for k in ("khoa", "cu", "moi")}}
    SCHEMA_TM.write_text(json.dumps({"type": "object", "required": ["sua", "them_khong_day", "ghi_chu"], "properties": {
        "sua": {"type": "array", "items": sua}, "them_khong_day": {"type": "string"},
        "ghi_chu": {"type": "string"}}}, ensure_ascii=False, indent=2) + "\n")


def doan_tm():
    """Các đoạn chữ TM (trong scripts/tm_ch6_9c_ban2.py) nhắc Δ′ / b′ / thu gọn."""
    import tm_ch6_9c_ban2 as tm
    out = []
    for ten in ("LYTHUYET", "VIDU", "LOISAI", "KIENTHUC_NB", "KIEN_THUC_NEN", "DANG_VD"):
        for i, s in enumerate(getattr(tm, ten, [])):
            if PHAY.search(s) or ("Không dạy ở lớp C" in s):
                out.append({"khoa": f"{ten}[{i}]", "cu": s})
    for k, s in tm.D_TEXT.items():
        if PHAY.search(s) or "thu gọn" in s:
            out.append({"khoa": "D_TEXT" + json.dumps(list(k), ensure_ascii=False), "cu": s})
    return out


def main():
    ghi_schema()
    rows = json.loads(CHON.read_text())
    dang = bang_dang()
    hd = REPO / "storage/gemini/hang-doi"
    for p, mo in PHIEU.items():
        data = [{"ma": r["ma"], "vai": r["vai"], "dang": r["dang"], "muc": r["muc"], "so_y": r["so_y"],
                 "so_nb": r["so_nb"], "y_boc": r["y"], "hinh_thuc": r["hinh_thuc"], "de": r["de"],
                 "nguon": r["nguon"], "diem_may": r["diem"], "ly_do_cham": r["ly_do"]}
                for r in rows if r["phieu"] == p]
        vid = f"dx-ch6-9c-{p}"
        pr = (PROMPT.replace("{PHIEU}", p).replace("{MO_TA}", mo).replace("{DANG}", dang)
              .replace("{SO}", str(len(data))) + json.dumps(data, ensure_ascii=False, indent=1) + "\n")
        viec = {"id": vid, "model": MODEL, "prompt": pr, "files": [],
                "schema": str(SCHEMA_DX.relative_to(REPO)), "timeout": "1200s",
                "meta": {"loai": "de-xuat-chon-cau", "phieu": p, "ma": [d["ma"] for d in data]}}
        if "--thu" not in sys.argv:
            (hd / f"{vid}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(vid, len(data), "dòng", len(pr), "kí tự")
    dt = doan_tm()
    vid = "tm-ch6-9c-bo-delta-phay"
    viec = {"id": vid, "model": MODEL, "prompt": PROMPT_TM + json.dumps(dt, ensure_ascii=False, indent=1) + "\n",
            "files": [], "schema": str(SCHEMA_TM.relative_to(REPO)), "timeout": "600s",
            "meta": {"loai": "sua-chu-tm", "khoa": [d["khoa"] for d in dt]}}
    if "--thu" not in sys.argv:
        (hd / f"{vid}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print(vid, len(dt), "đoạn:", [d["khoa"] for d in dt])


if __name__ == "__main__":
    main()
