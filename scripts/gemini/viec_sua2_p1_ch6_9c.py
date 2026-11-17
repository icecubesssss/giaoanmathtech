#!/usr/bin/env python3
"""Việc Gemini đợt 3 — Phiếu 1 ch.VI 9C bản 2 (16/11/2026): THÊM Ô ĐIỀN cho 7 ví dụ.

Thầy 16/11: "Điền khuyết chắc là cần nhiều hơn để GV định hướng cho HS". Đầu vào = 7 ví dụ trong seed hiện tại
(đã qua SUA_VD đợt 2). lap_p1_ch6_9c.py ưu tiên kết quả việc này cho ví dụ (bỏ qua SUA_VD).

    .venv/bin/python scripts/gemini/viec_sua2_p1_ch6_9c.py
    python3 scripts/gemini/tho.py --mot sua2-p1-ch6-9c
    .venv/bin/python scripts/gemini/lap_p1_ch6_9c.py --ghi
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_dung_p1_ch6_9c import CHUNG, MODEL, SEED  # noqa: E402

VID_SUA2 = "sua2-p1-ch6-9c"


def vi_du_hien_tai():
    f = json.loads((REPO / SEED).read_text())
    out = {}
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("variant") == "example":
                out[re.match(r"\\textbf\{([^}]*)\}", b["text"]).group(1)] = b["text"]
    return out


PROMPT = CHUNG + r'''
## Việc: THÊM Ô ĐIỀN cho 7 ví dụ (giáo viên làm cùng lớp, dùng ô để định hướng học sinh từng bước)
Đầu ra {"sua":[{"label":"Ví dụ N.","statement":"<TOÀN BỘ text mới của ví dụ>","solution":""} × 7],"ghi_chu":"…"}.

Quy tắc:
- GIỮ NGUYÊN đề, thứ tự dòng, câu chữ và mọi ô [[fill:…]] đang có. Chỉ THAY một số chữ/số in sẵn trong phần Lời giải bằng ô [[fill:…]] (đáp án đặt trong ô). Không thêm, không bớt dòng (trừ khi cần tách một dòng có hai bước).
- Mục tiêu số ô: ví dụ một ý khoảng 7–9 ô, ví dụ nhiều ý khoảng 3–4 ô mỗi ý. Ô rơi vào CHỖ GIÁO VIÊN HỎI để định hướng: hệ số $a$, $b$, $c$; công thức "$b^2-4ac$"; giá trị $\Delta$; dấu so sánh với $0$ (ô chứa ">", "<", "="); cụm kết luận ("hai nghiệm phân biệt", "nghiệm kép", "vô nghiệm", "luôn có nghiệm", "trái dấu"); điều kiện của $\Delta$ ("$\Delta>0$"…); biểu thức sau khi khai triển/chuyển vế; nghiệm.
- Không khoét hai ô liền nhau trên cùng một chỗ, không để dòng chỉ còn toàn ô.
- KHÔNG LỘ ĐÁP ÁN: một giá trị đã nằm trong ô thì ở các dòng SAU của CÙNG ý không được in sẵn lại giá trị đó (khoét tiếp hoặc viết bằng chữ). Ngược lại, giá trị đã in sẵn ở dòng trên thì không khoét ô ở dòng dưới.
- Ô trong $…$: đáp án KHÔNG bọc $ (vd "$\Delta=[[fill:61]]>0$", "$\Delta[[fill:>]]0$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong ô (vd "[[fill:$\Delta>0$]]"). KHÔNG đặt ô bên trong \dfrac{…}{…}, \sqrt{…}, \left[…\right] — muốn khoét thì khoét cả biểu thức.
- Không đổi số, không đổi phương trình. Không dấu ";", không ⇔, không "suy ra/do đó".

## 7 ví dụ hiện tại
'''


def main():
    v = {"id": VID_SUA2, "model": MODEL, "prompt": PROMPT + json.dumps(vi_du_hien_tai(), ensure_ascii=False, indent=1) + "\n",
         "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
         "meta": {"loai": "sua2-p1-ch6-9c", "seed": SEED}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID_SUA2}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
