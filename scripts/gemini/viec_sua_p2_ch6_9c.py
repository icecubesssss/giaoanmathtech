#!/usr/bin/env python3
"""Việc Gemini đợt 2 — Phiếu 2 ch.VI 9C bản 2 (16/11/2026): sửa theo validate lượt 1.

Lỗi lượt 1: 3 bài Đúng/Sai cùng câu dẫn (figure_gate CHẶN "đề chép lại 3 lần"); lời giải dùng "Do đó/Suy ra"
(trinh_bay nhịp đi thi); ý [TH]/[VD] chép lại dòng điều kiện + Viète đã có ở câu dẫn a), b); ví dụ: Vậy in sẵn
đáp số, số đã khoét ô lại in sẵn ở dòng dưới, Ví dụ 7 ô bọc $ trong $…$, Ví dụ 1 thiếu "Vậy".

    .venv/bin/python scripts/gemini/viec_sua_p2_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 2      (sua-p2-ch6-9c-lop, sua-p2-ch6-9c-btvn)
    .venv/bin/python scripts/gemini/lap_p2_ch6_9c.py [--ghi]      (lap tự đọc kết quả hai việc này)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_dung_p2_ch6_9c import CHUNG, KHUON_KHOI, MODEL, SEED, VID_BTVN, VID_LOP  # noqa: E402

VID_SUA_LOP, VID_SUA_BTVN = "sua-p2-ch6-9c-lop", "sua-p2-ch6-9c-btvn"
BAI_LOP = {"Bài 1.", "Bài 2.", "Bài 6."} | {f"Bài {i}." for i in range(10, 20)}
BAI_BTVN = {f"Bài {i}." for i in range(24, 34)}


def ban_cu(vid, nhan):
    out = {}
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    kq = kq.get("ket_qua") or kq.get("json") or kq
    for s in kq["stages"]:
        for b in s["blocks"]:
            if b.get("variant") == "example":
                out[b["text"].split("}", 1)[0].replace("\\textbf{", "")] = b["text"]
            elif b.get("label") in nhan:
                out[b["label"]] = {k: b[k] for k in ("statement", "solution", "dung_sai") if b.get(k)}
    return json.dumps(out, ensure_ascii=False, indent=1)


LUAT_SUA = r'''
## Việc: sửa đợt 2 (sau khi máy soát lượt 1) — GIỮ NGUYÊN mọi số, phương trình, thẻ [NB]/[TH]/[VD], nguồn
Đầu ra {"sua":[…],"ghi_chu":"…"}. Mỗi phần tử {"label","statement","solution"}:
- VÍ DỤ: "label":"Ví dụ N.", "statement" = TOÀN BỘ chuỗi text của khối ví dụ (bắt đầu "\\textbf{Ví dụ N.} …", có Lời giải và ô [[fill:]]), "solution":"".
- BÀI: "label":"Bài N.", "statement" và "solution" đầy đủ (thay hẳn bản cũ). Bài Đúng/Sai thêm "dung_sai":[…] giữ nguyên khẳng định.
Trả về MỌI mục có trong "Bản cũ" bên dưới (kể cả mục chỉ đổi ít).

### Luật sửa
1. CẤM các chữ "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy" ở mọi lời giải và ví dụ. Thay bằng "nên" trong cùng câu, hoặc mở dòng mới bằng "Ta có …", "Khi đó …", "Thay vào, ta được …". Mỗi bước vẫn một dòng; dòng con mở đầu "[[br]]\hspace*{1.4em}"; "\hspace*" chỉ đứng ĐẦU dòng.
2. Bài có câu dẫn a) [NB], b) [NB] đã nêu điều kiện có nghiệm và tổng, tích: lời giải ý cuối ([TH] hoặc [VD]) KHÔNG chép lại các dòng đó. Mở đầu ý cuối bằng "Theo câu a) và b), …" (hoặc "Theo câu b), …") rồi đi tiếp các bước còn lại (biến đổi biểu thức → thay số → kết quả → dòng "Vậy" riêng). Lời giải các ý dẫn giữ ngắn gọn như bản cũ.
3. VÍ DỤ (ô [[fill:]]):
   - Mỗi ý kết bằng dòng riêng "Vậy …", và giá trị kết luận trong dòng "Vậy" PHẢI là ô (vd "Vậy $A=[[fill:39]]$." , "Vậy $m=[[fill:2]]$ hoặc $m=[[fill:-2]]$.").
   - Một số đã nằm trong ô thì KHÔNG được in sẵn (ngoài ô) ở bất kì dòng nào phía DƯỚI ô đó trong cùng ví dụ. Muốn hỏi giá trị tổng, tích thì khoét ở dòng THAY SỐ cuối cùng (hoặc khoét mọi lần nó xuất hiện), còn dòng "Theo định lí Viète" có thể in sẵn. Kiểm tra lại từng ví dụ theo luật này trước khi trả.
   - Ô nằm trong $…$ thì đáp án KHÔNG có dấu $ (vd "$m\ne[[fill:-1]]$", "$\Delta=[[fill:(m+1)^2]]$"). Ô ngoài $…$ mới được bọc $ bên trong.
   - Giữ số ô khoảng 3–4 ô mỗi ý (ví dụ một ý 7–9 ô), ô ở chỗ giáo viên hỏi lớp.
   - Ví dụ 1 thêm dòng "Vậy …" cho mỗi ý.
'''

PROMPT_LOP = CHUNG + KHUON_KHOI + LUAT_SUA + r'''4. Ba bài Đúng/Sai (Bài 1, Bài 2, Bài 6) đang có câu dẫn giống hệt nhau ⇒ mỗi bài một câu dẫn riêng, giữ thẻ [NB] đầu câu, giữ khẳng định trong "dung_sai":
   Bài 1.: "[NB] Bạn An nói: \textquotedblleft Không cần giải, tổng và tích hai nghiệm của phương trình $x^2-x+1=0$ đều bằng $1$.\textquotedblright\ Bạn An nói đúng hay sai? Vì sao?"  (dung_sai giữ khẳng định cũ)
   Bài 2.: "[NB] Có bạn cho rằng phương trình $x^2+x+1=0$ có tổng và tích các nghiệm là hai số đối nhau. Ý kiến đó đúng hay sai? Vì sao?"
   Bài 6.: "[NB] Xét phương trình $x^2-2x+m=0$ ($m$ là tham số). Khẳng định sau đúng hay sai? Vì sao?"
   Lời giải ba bài giữ như cũ (bỏ "do đó").

## Bản cũ (đầu ra lượt 1 — sửa từ đây, giữ nguyên các dòng đã đúng)
'''

PROMPT_BTVN = CHUNG + KHUON_KHOI + LUAT_SUA + r'''
## Bản cũ (đầu ra lượt 1, phần bài tập về nhà — sửa từ đây, giữ nguyên các dòng đã đúng)
'''


def main():
    for vid, prompt, nguon, nhan in ((VID_SUA_LOP, PROMPT_LOP, VID_LOP, BAI_LOP),
                                     (VID_SUA_BTVN, PROMPT_BTVN, VID_BTVN, BAI_BTVN)):
        v = {"id": vid, "model": MODEL, "prompt": prompt + ban_cu(nguon, nhan) + "\n", "files": [],
             "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
             "meta": {"loai": "sua-p2-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
