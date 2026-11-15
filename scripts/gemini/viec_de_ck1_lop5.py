#!/usr/bin/env python3
"""6 việc Gemini: chép câu nguồn + viết lời giải cho 6 đề CK1 Toán 5 theo scripts/ck1_lop5_ke_hoach.py.

    python3 scripts/gemini/viec_de_ck1_lop5.py
    python3 scripts/gemini/tho.py --tien-to de5- --song-song 3
Kết quả storage/gemini/xong/de5-<k>.json ⇒ scripts/de_ck1_lop5.py gom vào scripts/ck1_lop5_de.json rồi dựng seed.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
from ck1_lop5_ke_hoach import DE, DIEM  # noqa: E402

HANG_DOI = REPO / "storage/gemini/hang-doi"
BG = REPO / "inputs/refs/ngan-hang-sheet/tieu-hoc/lop-5/ban-ghi"
VIEC_BOC = {p.stem.replace(".json", ""): p for p in HANG_DOI.glob("l5-*.json*")}

MAU = r"""Bạn là giáo viên Toán lớp 5 (sách Kết nối tri thức). Việc: soạn nội dung MỘT đề kiểm tra cuối học kì I
Toán 5 ({ten}) bằng cách CHÉP NGUYÊN VĂN các câu đề trường đã chỉ định, rồi viết đáp án + lời giải.

Thư mục làm việc có:
- l5-*.json: bản ghi từng ý của đề trường ("cau" = nhãn ý, "nd" = nội dung đã chép, "dap_an", "co_hinh").
- Ảnh đề gốc (…-trang-N.png) của các trường được dùng — MỞ XEM khi câu có hình hoặc khi "nd" có vẻ thiếu/sai.
Tham chiếu "ck1-2526-vinhbao#1a" = file l5-ck1-2526-vinhbao.json, phần tử có "cau" = "1a".
Bạn KHÔNG được chạy lệnh; chỉ đọc file rồi trả JSON theo schema.

KẾ HOẠCH Ô (đúng thứ tự, mỗi ô một phần tử "o_cau", "o" = mã ô):
{kh}

Ý NGHĨA Ô VÀ HÌNH THỨC
- C1…C8: Phần I, mỗi câu 0,5 điểm. Mặc định TRẮC NGHIỆM 4 phương án ("hinh_thuc":"TN", "phuong_an" đủ 4 chuỗi
  KHÔNG có chữ "A."; giữ đúng thứ tự phương án của đề gốc). Câu gốc là điền/tự luận ⇒ theo ghi chú trong kế hoạch;
  không có ghi chú thì được giữ "Điền". Câu 2 ý Đúng/Sai: "hinh_thuc":"Đ-S", các mệnh đề đặt trong "y".
- B1 (2đ) "Đặt tính rồi tính": "hinh_thuc":"TL", "de_bai":"Đặt tính rồi tính:", "y" = 4 phép tính chỉ là biểu thức
  toán (vd "29{{,}}62 + 74{{,}}35"), "dap_an" = 4 kết quả cách nhau "; ".
- B2 (1đ) viết số thích hợp vào chỗ chấm: "y" = 4 dòng, mỗi dòng một chỗ điền (vd "$48$ m $9$ dm $=$ \makebox[2.6cm]{{\dotfill}} m").
- B3 (1đ): "y" = 2 ý a), b) (KHÔNG ghi chữ "a)" trong chuỗi), "de_bai" = lời dẫn chung (vd "Tính giá trị của biểu thức / tìm $x$:").
  Hai ý khác yêu cầu thì đưa yêu cầu vào từng ý.
- B4 (1,5đ) bài toán có lời văn: "de_bai" = đầy đủ lời đề; nếu đề có 2 câu hỏi thì câu hỏi để trong "y".
- B5 (0,5đ): câu tư duy, "de_bai" đầy đủ.

LUẬT CỨNG
1. CHÉP NGUYÊN VĂN số liệu, đơn vị, lời văn của câu nguồn (sửa lỗi chính tả hiển nhiên thì nói trong "doi_so_voi_goc").
   Không bịa câu mới. Chỉ được thêm phương án nhiễu khi kế hoạch cho phép; mọi thay đổi ghi vào "doi_so_voi_goc".
2. LaTeX: mọi số và phép tính trong $...$; dấu phẩy thập phân viết {{,}} (vd $29{{,}}62$); số ≥ 10 000 tách nghìn bằng \,
   (vd $18\,261$); nhân $\times$, chia $:$; đơn vị diện tích m$^2$, km$^2$, dm$^2$ (mũ trong $...$); phân số $\dfrac{{a}}{{b}}$;
   hỗn số $5\dfrac{{34}}{{1000}}$. KHÔNG dùng kí tự unicode toán (×, ÷, ², ≤, −) ngoài $...$. Không dùng \dots làm chỗ điền:
   chỗ điền ngắn \makebox[2.6cm]{{\dotfill}}, dài \makebox[4.5cm]{{\dotfill}}. Escape \% nếu có.
   Không xưng "em" trong đề. Câu hỏi giữ ngôi như đề gốc.
3. "dap_an" ngắn (TN: một chữ cái A/B/C/D; Đ-S: "a) Đ – b) S"; điền/tự luận: kết quả).
   "loi_giai": lời giải như HS lớp 5 trình bày, mỗi bước một dòng nối bằng " [[br]] ", có điểm thành phần
   dạng \hfill \textit{{(0,25đ)}} cho Phần II; tổng điểm thành phần mỗi ô đúng bằng điểm ô ({diem}).
   Bài toán có lời văn: câu lời giải + phép tính + "Đáp số: …". TỰ TÍNH LẠI mọi đáp số (đề gốc/HDC có thể sai —
   đề gốc sai dữ kiện thì nói trong "ghi_chu", giữ đề, ghi đáp án đúng theo đề in). Trắc nghiệm: giải ngắn vì sao chọn,
   nêu bẫy hay gặp (\textit{{Bẫy: …}}).
4. "tikz": câu cần hình (đề gốc có hình hoặc ghi chú yêu cầu) ⇒ một tikzpicture hoàn chỉnh, nhỏ (rộng ≤ 5 cm,
   [scale=…] hợp lí), nhãn đỉnh $A$…, độ dài ghi bằng node \small; vẽ ĐÚNG số liệu và quan hệ trong đề (đường cao vuông góc,
   kí hiệu góc vuông, điểm nằm đúng chỗ). Không cần hình ⇒ "".
5. Trả về đủ 13 ô C1…C8, B1…B5.

"ghi_chu": nghi ngờ, chỗ đề gốc sai/mơ hồ, chỗ đổi hình thức.
"""


def main():
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    ten = {"on1": "Đề ôn tập số 1", "on2": "Đề ôn tập số 2", "on3": "Đề ôn tập số 3",
           "ct1": "Đề chính thức 1", "ct2": "Đề chính thức 2", "ct3": "Đề chính thức 3"}
    for k, ds in DE.items():
        kh, nguon = [], set()
        for o, refs, g in ds:
            kh.append(f"  {o} ({str(DIEM[o]).replace('.', ',')}đ) ← {', '.join(refs)}" + (f"  [{g}]" if g else ""))
            nguon |= {r.split("#")[0] for r in refs}
        files = [str((BG / f"l5-{n}.json").relative_to(REPO)) for n in sorted(nguon)]
        for n in sorted(nguon):  # PDF đề gốc lấy từ meta của việc bóc
            v = VIEC_BOC.get(f"l5-{n}")
            if v:
                files.append(json.loads(v.read_text())["meta"]["pdf"])
        viec = {"id": f"de5-{k}", "model": "gemini-3.8-flash-high",
                "prompt": MAU.format(ten=ten[k], kh="\n".join(kh), diem="C: 0,5; B1: 2; B2: 1; B3: 1; B4: 1,5; B5: 0,5"),
                "files": files, "render": True, "schema": "scripts/gemini/schema/de-ck1-lop5.json",
                "timeout": "1800s", "meta": {"loai": "de-ck1-lop5", "de": k}}
        (HANG_DOI / f"{viec['id']}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(f"ghi {viec['id']}: {len(files)} file")


if __name__ == "__main__":
    main()
