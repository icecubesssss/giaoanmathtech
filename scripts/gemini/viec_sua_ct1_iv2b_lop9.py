#!/usr/bin/env python3
"""Việc Gemini: sửa Bài IV.2b (+ dọn 2c) đề CHÍNH THỨC CK1 lớp 9 số 1.

Lỗi (Gemini phát hiện 12/11/2026 khi gắn dạng): đề in $MC^2 = MH\\cdot MO$ (H là chân đường cao
từ C xuống AB ⇒ SAI); lời giải lại chứng minh $MI\\cdot MO$ với I chưa định nghĩa; 2b nêu kết quả
trước khi chứng minh; 2c "áp dụng Thalès cho KH và CK suy ra" là nhảy bước.
Claude chốt sơ đồ chứng minh, Gemini viết chữ. Kết quả: storage/gemini/xong/sua-l9-ct1-iv2b.json
⇒ Claude vá vào scripts/de_chinh_thuc_ck1_lop9.py (nguồn sự thật của seed).

    python3 scripts/gemini/viec_sua_ct1_iv2b_lop9.py
    python3 scripts/gemini/tho.py --mot sua-l9-ct1-iv2b
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

PROMPT = r'''Bạn là thợ sửa đề kiểm tra cuối kì 1 Toán 9 (Hà Nội, sách Kết nối tri thức) cho học sinh tầng C. Làm CẨN THẬN, CHỈ sửa đúng phạm vi, KHÔNG đổi số liệu, KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Bài IV.2 hiện tại (3,0 điểm)
Cho đường tròn $(O; R)$, đường kính $AB$. Lấy điểm $C$ trên nửa đường tròn sao cho $AC < BC$. Kẻ $CH \perp AB$ tại $H$. Tiếp tuyến tại $A$ và tiếp tuyến tại $C$ của $(O)$ cắt nhau tại điểm $M$.
a) (1,0 điểm) Chứng minh bốn điểm $M, A, O, C$ cùng thuộc một đường tròn.   ← GIỮ NGUYÊN, không trả về
b) (1,0 điểm) Chứng minh $OM \perp AC$ và $MC^2 = MH \cdot MO$.   ← SAI: H là chân đường cao từ C, $MC^2 \ne MH\cdot MO$
c) (1,0 điểm) Đoạn thẳng $MB$ cắt $CH$ tại $K$. Chứng minh rằng $K$ là trung điểm của $CH$.

Lời giải 2b hiện tại (lỗi: dùng điểm I chưa định nghĩa, nêu $MC^2 = MI\cdot MO$ trước rồi mới chứng minh, góc $\widehat{MCI} = \widehat{MOC}$ không có lí do).
Lời giải 2c hiện tại (lỗi: "Chứng minh được $M$ là trung điểm của $AE$" không chứng minh; "Áp dụng định lí Thalès cho $KH$ và $CK$ suy ra $CK = KH$" là nhảy bước).

## Việc của bạn: viết lại đề ý b và lời giải ý b, ý c THEO ĐÚNG SƠ ĐỒ giáo viên đã chốt
Ý b — đề mới (giữ 1,0 điểm): "Gọi $I$ là giao điểm của $OM$ và $AC$. Chứng minh $OM \perp AC$ tại $I$ và $MC^2 = MI \cdot MO$."
Sơ đồ lời giải b (4 mốc, mỗi mốc 0,25):
 1. $MA = MC$ (tính chất hai tiếp tuyến cắt nhau) và $OA = OC = R$ ⇒ $M$, $O$ cùng cách đều $A$ và $C$ ⇒ $OM$ là đường trung trực của đoạn $AC$.
 2. ⇒ $OM \perp AC$ tại $I$.
 3. Xét $\triangle MIC$ và $\triangle MCO$: $\widehat{MIC} = \widehat{MCO} = 90^\circ$ ($OM \perp AC$; $MC$ là tiếp tuyến tại $C$ nên $MC \perp OC$), $\widehat{CMO}$ chung ⇒ $\triangle MIC \backsim \triangle MCO$ (g.g).
 4. ⇒ $\dfrac{MI}{MC} = \dfrac{MC}{MO}$ ⇒ $MC^2 = MI \cdot MO$.
Ý c — giữ đề nguyên văn. Sơ đồ lời giải c (4 mốc, mỗi mốc 0,25):
 1. $MA \perp AB$ (tiếp tuyến) và $CH \perp AB$ ⇒ $CH \parallel MA$. Gọi $E$ là giao điểm của tia $BC$ và đường thẳng $MA$.
 2. $\widehat{ACB} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn) ⇒ $\widehat{ACE} = 90^\circ$. $MA = MC$ ⇒ $\triangle MAC$ cân tại $M$ ⇒ $\widehat{MAC} = \widehat{MCA}$. Trong $\triangle ACE$ vuông tại $C$: $\widehat{MEC} = 90^\circ - \widehat{MAC}$ và $\widehat{MCE} = 90^\circ - \widehat{MCA}$ ⇒ $\widehat{MEC} = \widehat{MCE}$ ⇒ $\triangle MCE$ cân tại $M$ ⇒ $ME = MC = MA$.
 3. $\triangle BME$ có $CK \parallel ME$ ⇒ $\dfrac{CK}{ME} = \dfrac{BK}{BM}$ (hệ quả định lí Thalès). $\triangle BMA$ có $KH \parallel MA$ ⇒ $\dfrac{KH}{MA} = \dfrac{BK}{BM}$.
 4. ⇒ $\dfrac{CK}{ME} = \dfrac{KH}{MA}$, mà $ME = MA$ ⇒ $CK = KH$. Vậy $K$ là trung điểm của $CH$.

## Luật trình bày (vi phạm là bị trả lại)
- Lời giải như bài thi: MỖI dòng một bước suy luận, mỗi phần tử của "buoc" là MỘT dòng; dòng kết thúc một mốc chấm thì "diem" = 0.25, dòng khác "diem" = 0. Tổng "diem" của ý b đúng 1.0, ý c đúng 1.0.
- KHÔNG nêu kết luận trước khi chứng minh. Mỗi suy ra phải có lí do trong ngoặc hoặc dòng trước. Dùng "Xét", "Ta có", "Suy ra", "Do đó", "Vậy". Không văn nói, không xưng hô ("em", "ta thấy rằng dễ dàng"…), không viết tắt.
- KHÔNG dùng dấu $\Leftrightarrow$. Được dùng $\Rightarrow$ trong một dòng ngắn. Không dùng hệ thức lượng $b^2 = ab'$ (sách Kết nối tri thức lớp 9 không có) — phải qua tam giác đồng dạng như sơ đồ.
- Toán trong $…$; phân số \dfrac; đồng dạng \backsim; góc \widehat{…}. Chuỗi JSON: gạch chéo ngược nhân đôi.
- "ma_tran": mô tả ngắn ý đó cho ma trận đề (≤ 60 kí tự), vd "Đường trung trực và hệ thức $MC^2 = MI \cdot MO$ qua đồng dạng".
- TỰ KIỂM từng bước suy luận; thấy sơ đồ có chỗ sai thì ghi vào "ghi_chu", KHÔNG tự đổi.

## Đầu ra
JSON đúng schema: {"y": [{"nhan":"2b","de":"<đề ý b, bắt đầu bằng b) \\textbf{(1,0 điểm)} …>","buoc":[{"text":…,"diem":…},…],"ma_tran":…}, {"nhan":"2c","de":"<đề ý c nguyên văn, bắt đầu c) \\textbf{(1,0 điểm)} …>","buoc":[…],"ma_tran":…}], "ghi_chu": "…"}
'''

viec = {
    "id": "sua-l9-ct1-iv2b",
    "model": "gemini-3.8-flash-high",
    "prompt": PROMPT,
    "files": [],
    "schema": "scripts/gemini/schema/sua-y-de-thi.json",
    "timeout": "900s",
    "meta": {"loai": "sua-y-de-thi", "script": "scripts/de_chinh_thuc_ck1_lop9.py", "de": "ct1", "bai": "Bài IV."},
}
p = REPO / "storage/gemini/hang-doi" / f"{viec['id']}.json"
p.write_text(json.dumps(viec, ensure_ascii=False, indent=2))
print("ghi", p.relative_to(REPO))
