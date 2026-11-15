#!/usr/bin/env python3
"""Việc Gemini: phiếu F ch.VI 9C — bỏ hết "khuôn", Kiến thức cần nhớ = tổng hợp lý thuyết cả chương.

Thầy (12/11/2026): "Các phần lý thuyết nó chỉ là lý thuyết thôi, tổng hợp lại lý thuyết của cả chương
để HS nhìn lại … Bỏ hết đi" + "Mấy câu nhận biết khuôn bỏ đi".
Claude: xoá khối/bài (máy móc, lap_ly_thuyet_phieu_f_9c.py). Gemini: viết lý thuyết, opener, sơ đồ, ghi chú GV.

    python3 scripts/gemini/viec_ly_thuyet_phieu_f_9c.py
    python3 scripts/gemini/tho.py --mot ly-thuyet-9c-ch6-phieu-f
    python3 scripts/gemini/lap_ly_thuyet_phieu_f_9c.py [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
SEED = f"{D}/phieu-f-luyen-tap-chung-va-bai-tap-cuoi-chuong-vi.json"
MAU = f"{D}/phieu-c-dinh-li-viete-va-ung-dung.json"
VID = "ly-thuyet-9c-ch6-phieu-f"

PROMPT = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI: phương trình bậc hai một ẩn) cho học sinh lớp 9 TẦNG C. Phiếu F là buổi luyện tập chung cuối chương (sau đó học sinh làm bài kiểm tra chương 45 phút).
KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm cuối prompt.

## Giáo viên vừa chốt (vi phạm là bị trả lại)
- BỎ HẾT chữ và ý "khuôn" (khuôn giải, khuôn tổng và tích, khuôn lập phương trình, nhận khuôn…), BỎ HẾT chuyện cấu trúc đề, thang điểm Câu III, "bảng điểm", "mất 0,25 điểm", "tầng C lấy chắc". Không bịa thêm mẹo, sơ đồ, mục tiêu hay thứ gì linh tinh.
- Phần "Kiến thức cần nhớ" CHỈ LÀ LÝ THUYẾT: tổng hợp lại lý thuyết của CẢ chương VI (đúng như SGK Toán 9 Kết nối tri thức, Bài 19, Bài 20, Bài 21 và phương trình quy về bậc hai) để học sinh nhìn lại. Không có thẻ bẫy, thẻ mục tiêu.
- Các bài nhận biết "ghi A/B/C khuôn nào" và bài "đọc thang điểm Câu III" đã bị XOÁ (giáo viên tự xoá) — bạn KHÔNG nhắc tới chúng.
- Không kí hiệu $S$, $P$ cho tổng, tích hai nghiệm; không tham số $m$. Không văn nói, không xưng hô ("em", "các em", "hôm nay", "ta đi qua", "Kiểm", "Soi"). Không dùng dấu chấm phẩy ";" nối hai công thức (xuống dòng [[br]] hoặc dùng chữ "và").
- Toán trong $…$; phân số \dfrac; JSON hợp lệ (gạch chéo ngược nhân đôi trong chuỗi).

## Việc 1 — "concept_blocks": khối của chặng "Kiến thức cần nhớ"
Khuôn trình bày y như chặng Kiến thức cần nhớ của phiếu C đã duyệt (xem "Mẫu lý thuyết phiếu C"): cặp {"type":"para","text":"\\textbf{N. Tên mục}"} rồi {"type":"para","text": nội dung, xuống dòng [[br]], gạch đầu dòng "$\\bullet$\\; "}. Đúng 6 mục, theo thứ tự:
1. Phương trình bậc hai một ẩn: dạng $ax^2+bx+c=0$ ($a \ne 0$). Trường hợp khuyết $c$ (đặt nhân tử chung $x(ax+b)=0$) và khuyết $b$ (đưa về $x^2=-\dfrac{c}{a}$).
2. Công thức nghiệm: $\Delta=b^2-4ac$. $\Delta>0$: hai nghiệm phân biệt $x_1=\dfrac{-b+\sqrt\Delta}{2a}$, $x_2=\dfrac{-b-\sqrt\Delta}{2a}$. $\Delta=0$: nghiệm kép $x_1=x_2=-\dfrac{b}{2a}$. $\Delta<0$: vô nghiệm. Nếu $ac<0$ thì phương trình có hai nghiệm phân biệt.
3. Công thức nghiệm thu gọn: $b=2b'$, $\Delta'=b'^2-ac$, ba trường hợp tương ứng với $x_{1,2}=\dfrac{-b'\pm\sqrt{\Delta'}}{a}$, nghiệm kép $-\dfrac{b'}{a}$.
4. Định lí Viète: có hai nghiệm thì $x_1+x_2=-\dfrac{b}{a}$, $x_1x_2=\dfrac{c}{a}$ (viết dạng hệ $\begin{cases}…\end{cases}$ như mẫu). Bốn công thức biến đổi: $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2$; $\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{x_1+x_2}{x_1x_2}$; $x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)$; $(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2$ (mỗi công thức một dòng). Nhẩm nghiệm: $a+b+c=0$ thì $x_1=1$, $x_2=\dfrac{c}{a}$; $a-b+c=0$ thì $x_1=-1$, $x_2=-\dfrac{c}{a}$. Biết một nghiệm $x_1$ thì nghiệm còn lại $x_2=-\dfrac{b}{a}-x_1$. Tìm hai số biết tổng $u+v$ và tích $uv$: hai số là nghiệm của $x^2-(u+v)x+uv=0$ (điều kiện $(u+v)^2-4uv \ge 0$).
5. Phương trình chứa ẩn ở mẫu (quy về bậc hai) — 4 bước: tìm điều kiện xác định; quy đồng mẫu hai vế rồi khử mẫu; giải phương trình nhận được; đối chiếu điều kiện xác định rồi kết luận.
6. Giải bài toán bằng cách lập phương trình — 3 bước SGK: lập phương trình (chọn ẩn, đơn vị và điều kiện cho ẩn; biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết; lập phương trình biểu thị mối quan hệ); giải phương trình; trả lời (kiểm tra nghiệm nào thỏa mãn điều kiện của ẩn rồi kết luận).

## Việc 2 — "opener_text"
Đoạn mở màn 2–3 câu, không xưng hô, không "khuôn", không điểm số: buổi luyện tập chung ôn lại toàn bộ chương VI gồm giải phương trình bậc hai, định lí Viète, phương trình chứa ẩn ở mẫu và giải bài toán bằng cách lập phương trình, trước bài kiểm tra chương.

## Việc 3 — "mindmap"
Sơ đồ tư duy điền khuyết tổng kết LÝ THUYẾT chương (thay bản cũ có "Khuôn 1/2/3" và "Điểm trong đề"). Khuôn JSON như bản cũ: {"type":"mindmap","caption":"Điền các ô trống để tự tổng kết cả chương VI","root":"Chương VI — Phương trình bậc hai","branches":[{"label":…,"children":[{"label":…}]}]}. Đúng 4 nhánh: "Công thức nghiệm", "Định lí Viète", "Ẩn ở mẫu", "Lập phương trình"; mỗi nhánh 2–3 con, mỗi con NGẮN (dưới 35 kí tự hiển thị), chỉ khoét phần công thức/từ khoá bằng [[blank:1cm]] (độ dài 0.8cm–1.6cm). Nhánh "Lập phương trình" con thứ nhất phải là "Chọn ẩn, đơn vị, [[blank:1.4cm]]".

## Việc 4 — "teacher_notes" (ghi chú giáo viên, viết lại bỏ hết chữ "khuôn", "Câu III", điểm số)
Số bài MỚI sau khi xoá: trên lớp Luyện tập 1 là Bài 1–Bài 7 (Δ hay Δ′, nhẩm nghiệm, Viète điền, hạ bậc, ẩn ở mẫu, đặt ẩn, lập phương trình từ cụm chữ); Luyện tập 2 là Bài 8–Bài 13 (Bài 12 biểu thức có hạ bậc, Bài 13 bài toán chở hàng). Giữ nhịp thời gian như bản cũ (Luyện tập 1 khoảng 35 phút, Luyện tập 2 khoảng 60 phút).
- "review": 1–2 câu (mở màn khoảng 5 phút).
- "concept": 1–2 câu (học sinh đọc lại lý thuyết, giáo viên hỏi nhanh vài công thức).
- "practice1": viết lại bản cũ, câu hỏi miệng mở đầu đổi "thuộc khuôn nào" thành "dùng định lí Viète tính tổng và tích hai nghiệm".
- "practice2": viết lại bản cũ, nói Bài 12 và Bài 13 là hai bài khó nhất, dành 25 phút cuối, chấm chéo từng bước trình bày.

## Đầu ra
JSON đúng schema: {"opener_text", "concept_blocks", "mindmap", "teacher_notes": {"review","concept","practice1","practice2"}, "ghi_chu"}.
'''


def main():
    f = json.loads((REPO / SEED).read_text())
    c = json.loads((REPO / MAU).read_text())
    st = {s["kind"]: s for s in f["stages"]}
    mau_c = [b for s in c["stages"] if s["kind"] == "concept" for b in s["blocks"] if b["type"] == "para"]
    du_lieu = ("\n## Mẫu lý thuyết phiếu C (đã duyệt — chỉ xem khuôn trình bày)\n" + json.dumps(mau_c, ensure_ascii=False)
               + "\n\n## Bản cũ phiếu F — chặng Kiến thức cần nhớ (BỎ, chỉ để biết đã có gì)\n" + json.dumps(st["concept"], ensure_ascii=False)
               + "\n\n## Bản cũ — opener, sơ đồ, ghi chú giáo viên\n"
               + json.dumps({"opener": st["review"]["blocks"][0]["text"], "mindmap": st["reflection"]["blocks"][0],
                             "teacher_notes": {k: st[k].get("teacher_note", "") for k in ("review", "concept", "practice1", "practice2")}},
                            ensure_ascii=False) + "\n")
    viec = {"id": VID, "model": "gemini-3.8-flash-high", "prompt": PROMPT + du_lieu, "files": [],
            "schema": "scripts/gemini/schema/ly-thuyet-phieu.json", "timeout": "1200s",
            "meta": {"loai": "ly-thuyet-phieu", "seed": SEED}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(viec['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
