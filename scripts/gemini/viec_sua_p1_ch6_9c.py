#!/usr/bin/env python3
"""Việc Gemini đợt 2 — Phiếu 1 ch.VI 9C bản 2 (16/11/2026): viết lại 7 ví dụ theo sơ đồ đã gộp + sửa Bài 9, 10, 24.

Lí do (validate lượt 1): ví dụ đứng liền nhau không đi cùng bài (gộp 2+3, 4+5, 6+7 cũ), thiếu "Vậy",
còn "suy ra", ví dụ ít ô, kết luận ví dụ 9 cũ in sẵn; Bài 24 BTVN giống Ví dụ 4 cũ 90%.

    .venv/bin/python scripts/gemini/viec_sua_p1_ch6_9c.py
    python3 scripts/gemini/tho.py --mot sua-p1-ch6-9c
    .venv/bin/python scripts/gemini/lap_p1_ch6_9c.py [--ghi]      (lap tự đọc kết quả việc này)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_dung_p1_ch6_9c import CHUNG, KHUON_KHOI, MODEL, SEED, VID_BTVN, VID_LOP, so_do  # noqa: E402

VID_SUA = "sua-p1-ch6-9c"


def ban_cu():
    out = {}
    for vid in (VID_LOP, VID_BTVN):
        kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
        kq = kq.get("ket_qua") or kq.get("json") or kq
        for s in kq["stages"]:
            for b in s["blocks"]:
                if b.get("variant") == "example":
                    out[b["text"].split("}", 1)[0].replace("\\textbf{", "") + " (CŨ)"] = b["text"]
                elif b.get("label") in ("Bài 9.", "Bài 10.", "Bài 24."):
                    out[b["label"]] = {"statement": b["statement"], "solution": b["solution"]}
    return json.dumps(out, ensure_ascii=False, indent=1)


PROMPT = CHUNG + KHUON_KHOI + r'''
## Việc: sửa đợt 2 (sau khi máy soát lượt 1)
Đầu ra {"sua":[…],"ghi_chu":"…"}. Mỗi phần tử {"label","statement","solution"}:
- VÍ DỤ: "label":"Ví dụ N." (số MỚI), "statement" = TOÀN BỘ chuỗi text của khối ví dụ (bắt đầu "\\textbf{Ví dụ N.} …", có Lời giải và ô [[fill:]]), "solution":"".
- BÀI: "label":"Bài N.", "statement" và "solution" đầy đủ (thay hẳn bản cũ).

### 1. Viết lại ĐỦ 7 ví dụ theo SƠ ĐỒ MỚI dưới đây (Ví dụ 1–7; các ví dụ cũ 2+3, 4+5, 6+7 đã GỘP; cũ 8, 9, 10 nay là 5, 6, 7)
Yêu cầu chung cho mọi ví dụ:
- Ví dụ nhiều ý: đề "Giải các phương trình sau: a) …, b) …, c) …." rồi Lời giải theo từng ý, mỗi ý KẾT bằng dòng riêng "\\hspace*{1.4em}Vậy …".
- Ví dụ một ý cũng kết bằng dòng riêng "Vậy …". Không dùng "suy ra", "do đó", "Do đó": viết "nên" hoặc xuống dòng.
- Số ô [[fill:]]: ví dụ một ý 3–4 ô, ví dụ nhiều ý 5–7 ô, rơi vào chỗ phải suy ra (hệ số, giá trị $\Delta$, so sánh với 0, nghiệm, điều kiện của $m$, chữ kết luận như "vô nghiệm", "nghiệm kép"). Số nào đã nằm trong ô thì KHÔNG in sẵn lại ở dòng sau (dòng "Vậy" cũng khoét ô hoặc viết lại bằng chữ không lộ số). Câu "Vậy …" của Ví dụ 6 ý b) phải có ô (kết luận là chỗ học sinh điền).
- Ví dụ 5: đề viết lại "Cho phương trình $x^2-2(m+3)x+m^2-5=0$ ($m$ là tham số). Tìm điều kiện của $m$ để phương trình[[br]]a) có hai nghiệm phân biệt[[br]]b) có nghiệm kép[[br]]c) vô nghiệm." Lời giải: tính $\Delta$ một lần, rồi a) b) c) mỗi ý: "Phương trình … khi $\Delta>0$" / dòng bất phương trình / dòng kết quả / "Vậy …".
- Ví dụ 1: đề viết "Trong hai phương trình sau, phương trình nào là phương trình bậc hai ẩn $x$? …[[br]]a) $2x^2-3x+1=0$[[br]]b) $\left(\dfrac{1}{x}\right)^2+3\cdot\dfrac{1}{x}+2=0$" (đánh lại a, b — bản cũ ghi a, c), thêm dòng "Vậy …".
- Ví dụ 7: giữ ý tham số tên $a$ trùng tên hệ số — lời giải nói rõ "hệ số của $x^2$ là $1$, hệ số tự do là $-1$"; bỏ "Cách khác" (chỉ một cách: tích hai hệ số trái dấu); thêm dòng "Vậy …".
- Ví dụ lấy từ đề thi: nguồn " \\textit{(…)}" sau đề (Ví dụ 4: nguồn ghi sau từng ý). Ví dụ SGK: " \\textit{(SGK …)}".

### 2. Sửa ba bài
- Bài 9.: giữ đề, lời giải ý c) thêm dòng riêng "Vậy phương trình vô nghiệm." (ý c hiện chỉ có một câu "Vì … nên …").
- Bài 10.: bỏ chữ "Suy ra" ở ý a) (viết "$\sqrt{\Delta}=\sqrt{92}=2\sqrt{23}$." thành dòng riêng). Giữ phần còn lại.
- Bài 24. (bài tập về nhà): câu dẫn a) đổi thành "a) [NB] Tính $\Delta$." (đúng sơ đồ), lời giải a) chỉ tính $\Delta$ (có thể ghi hệ số ở dòng đầu). Giữ ý b).

## Sơ đồ mới của các ví dụ
''' + "\n".join(l for l in so_do({"practice1", "practice2"}).split("\n- ") if l.startswith("Ví dụ")) + r'''

## Bản cũ (đầu ra lượt 1 — sửa từ đây, giữ nguyên các dòng đã đúng)
'''


def main():
    v = {"id": VID_SUA, "model": MODEL, "prompt": PROMPT + ban_cu() + "\n", "files": [],
         "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
         "meta": {"loai": "sua-p1-ch6-9c", "seed": SEED}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID_SUA}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
