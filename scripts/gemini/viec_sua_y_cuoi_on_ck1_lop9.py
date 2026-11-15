#!/usr/bin/env python3
"""Việc Gemini: sửa 3 lời giải ý cuối bài hình đề ôn CK1 lớp 9 (Claude soát đầu ra phu-dang-l9-on-N, 12/11/2026).

    python3 scripts/gemini/viec_sua_y_cuoi_on_ck1_lop9.py
    python3 scripts/gemini/tho.py --mot sua-l9-on-y-cuoi
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
X = REPO / "storage/gemini/xong"


def da(k, nhan):
    kq = json.loads((X / f"phu-dang-l9-{k}.json").read_text())["ket_qua"]
    return next(a for a in kq["bai4"]["dap_an"] if a.startswith("\\textbf{" + nhan))


PROMPT = r'''Bạn là thợ sửa lời giải đề ôn tập cuối kì 1 Toán 9 (Hà Nội, sách Kết nối tri thức), học sinh tầng C. KHÔNG chạy lệnh, KHÔNG mở file. Sửa đúng 3 ý dưới đây theo SƠ ĐỒ giáo viên đã chốt; giữ nguyên đề (trừ chỗ ghi rõ).

## Luật trình bày
- Mỗi phần tử "buoc" là MỘT dòng, một bước suy luận có lí do. Dòng kết thúc mốc chấm "diem" = 0.25, dòng khác 0. Mỗi ý 0,5 điểm = đúng 2 mốc.
- Không nêu kết luận trước khi chứng minh, không dòng nháp/câu hỏi, không văn nói, không xưng hô, không dùng $\Leftrightarrow$. Dùng "Xét", "Ta có", "Suy ra", "Do đó", "Vậy". Toán trong $…$, \dfrac, \backsim, \widehat{…}. Chuỗi JSON: gạch chéo ngược nhân đôi.
- CẤM dùng: tứ giác nội tiếp, hệ thức lượng $b^2 = ab'$, "đường kính vuông góc với dây thì đi qua trung điểm của dây" (sách Kết nối tri thức không có).
- "ma_tran": mô tả ngắn cho ma trận (≤ 60 kí tự).

## Ý 1 — đề ôn 1, ý 2d (0,5 điểm)
Giả thiết: từ $A$ ngoài $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$; $H = OA \cap BC$; đường kính $BD$. Đề ý d (GIỮ NGUYÊN): "d) \textbf{(0,5 điểm)} Gọi $E$ là chân đường vuông góc kẻ từ $C$ đến $BD$, $K$ là giao điểm của $AD$ và $CE$. Chứng minh rằng $K$ là trung điểm của $CE$."
Lời giải hiện tại (LỖI: còn dòng nháp "Lại có … ? Xét …"; gọi cặp góc đồng vị là "so le trong"):
<<DA1>>
Sơ đồ đúng:
 1. $\widehat{BCD} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn) ⇒ $CD \perp BC$; mà $OA \perp BC$ (ý b) ⇒ $CD \parallel OA$. $AB \perp BD$ (tiếp tuyến), $CE \perp BD$ ⇒ $CE \parallel AB$. Xét $\triangle ABD$ có $EK \parallel AB$ ⇒ $\dfrac{EK}{AB} = \dfrac{DE}{DB}$ (hệ quả định lí Thalès) ⇒ $EK = \dfrac{AB \cdot DE}{2R}$. (mốc 0,25)
 2. Xét $\triangle CED$ và $\triangle ABO$: $\widehat{CED} = \widehat{ABO} = 90^\circ$; $\widehat{CDE} = \widehat{AOB}$ (hai góc đồng vị, $CD \parallel OA$) ⇒ $\triangle CED \backsim \triangle ABO$ (g.g) ⇒ $\dfrac{CE}{AB} = \dfrac{DE}{OB}$ ⇒ $CE = \dfrac{AB \cdot DE}{R}$. Suy ra $CE = 2EK$, vậy $K$ là trung điểm của $CE$. (mốc 0,25)

## Ý 2 — đề ôn 2, ý 2d (0,5 điểm)
Giả thiết: nửa đường tròn $(O)$ đường kính $AB$; $D$ trên nửa đường tròn; tiếp tuyến tại $A$ và tại $D$ cắt nhau ở $C$; $F$ là hình chiếu của $D$ trên $AB$; tia $BC$ cắt nửa đường tròn tại $E$. Ý b đã chứng minh $CA = CD$. Đề ý d (GIỮ NGUYÊN): "d) \textbf{(0,5 điểm)} Gọi $I$ là trung điểm của đoạn thẳng $DF$. Chứng minh ba điểm $B, I, C$ thẳng hàng."
Lời giải hiện tại (LỖI: "tiếp tuyến $Ax$" chưa định nghĩa; dòng $\widehat{AKD} = …$ thừa; hai tỉ số Thalès lấy chung $\dfrac{BF}{AB}$ không có lí do):
<<DA2>>
Sơ đồ đúng:
 1. Gọi $K$ là giao điểm của tia $BD$ và đường thẳng $AC$. $\widehat{ADB} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn) ⇒ $\widehat{ADK} = 90^\circ$. $CA = CD$ ⇒ $\widehat{CAD} = \widehat{CDA}$. Trong $\triangle ADK$ vuông tại $D$: $\widehat{CKD} = 90^\circ - \widehat{CAD}$ và $\widehat{CDK} = 90^\circ - \widehat{CDA}$ ⇒ $\widehat{CKD} = \widehat{CDK}$ ⇒ $CK = CD = CA$. (mốc 0,25)
 2. Gọi $I'$ là giao điểm của $BC$ và $DF$. $DF \perp AB$, $AK \perp AB$ ⇒ $DF \parallel AK$. Xét $\triangle BAC$ có $I'F \parallel AC$ ⇒ $\dfrac{I'F}{AC} = \dfrac{BI'}{BC}$; xét $\triangle BKC$ có $DI' \parallel KC$ ⇒ $\dfrac{DI'}{KC} = \dfrac{BI'}{BC}$ (hệ quả định lí Thalès) ⇒ $\dfrac{I'F}{AC} = \dfrac{DI'}{KC}$, mà $AC = KC$ ⇒ $I'F = I'D$ ⇒ $I'$ là trung điểm của $DF$ ⇒ $I' \equiv I$. Vậy $B, I, C$ thẳng hàng. (mốc 0,25)

## Ý 3 — đề ôn 3, ý 2c (0,5 điểm)
Giả thiết: $(O; R)$ đường kính $AB$; $C$ trên đường tròn, $AC > BC$; đường cao $CH$ của $\triangle ABC$ kéo dài cắt $(O)$ tại $D$; tiếp tuyến tại $A$ và tại $C$ cắt nhau tại $M$; $F = MC \cap AB$. Đề (GIỮ NGUYÊN): "c) \textbf{(0,5 điểm)} Chứng minh đường thẳng $FD$ là tiếp tuyến của $(O; R)$."
Lời giải hiện tại (LỖI: dùng "định lí đường kính vuông góc với dây cung"):
<<DA3>>
Sơ đồ đúng:
 1. $OC = OD = R$ ⇒ $\triangle OCD$ cân tại $O$; $OH \perp CD$ ⇒ $OH$ vừa là đường cao vừa là đường trung tuyến ⇒ $H$ là trung điểm của $CD$ ⇒ $AB$ là đường trung trực của $CD$; $F \in AB$ ⇒ $FC = FD$. (mốc 0,25)
 2. Xét $\triangle FCO$ và $\triangle FDO$: $FC = FD$, $OC = OD$, $FO$ chung ⇒ $\triangle FCO = \triangle FDO$ (c.c.c) ⇒ $\widehat{FDO} = \widehat{FCO} = 90^\circ$ ($FC$ là tiếp tuyến tại $C$) ⇒ $FD \perp OD$ tại $D \in (O)$. Vậy $FD$ là tiếp tuyến của $(O; R)$. (mốc 0,25)

## Đầu ra
JSON: {"y": [{"nhan":"on-1 2d","de":"<đề ý>","buoc":[…],"ma_tran":"…"}, {"nhan":"on-2 2d",…}, {"nhan":"on-3 2c",…}], "ghi_chu":"…"}
'''

p = PROMPT.replace("<<DA1>>", da("on-1", "2d)")).replace("<<DA2>>", da("on-2", "2d)")).replace("<<DA3>>", da("on-3", "2c)"))
viec = {"id": "sua-l9-on-y-cuoi", "model": "gemini-3.8-flash-high", "prompt": p, "files": [],
        "schema": "scripts/gemini/schema/sua-y-de-thi.json", "timeout": "900s", "meta": {"loai": "sua-y-de-thi"}}
(REPO / "storage/gemini/hang-doi/sua-l9-on-y-cuoi.json").write_text(json.dumps(viec, ensure_ascii=False, indent=2))
print("ghi sua-l9-on-y-cuoi")
