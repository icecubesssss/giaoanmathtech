#!/usr/bin/env python3
"""Việc Gemini nhỏ — Phiếu 3 ch.VI 9C (17/11/2026): lời giải Bài 15 thay câu.

Thầy 17/11: Bài 15 (luyện đề 19) trùng phương trình đề đích ⇒ "chọn lại" ⇒ đề thi HK2 Ngọc Lâm T901 (C6-11).
Đề do Claude chốt trong so_do_p3_ch6_9c.KHOI; Gemini chỉ viết lời giải.

    .venv/bin/python scripts/gemini/viec_sua_p3_ch6_9c.py
    python3 scripts/gemini/tho.py --mot sua2-p3-ch6-9c      (chạy riêng một việc: thêm id sau lệnh)
    .venv/bin/python scripts/gemini/lap_p3_ch6_9c.py [--ghi]      (lap tự đè kết quả việc này)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_dung_p3_ch6_9c import CHUNG, LUAT_LOI_GIAI, MODEL, SEED, so_do  # noqa: E402

# (id, nhãn, chặng, dặn riêng) — mỗi việc đè lời giải theo nhãn trong lap_p3_ch6_9c (VID_SUA)
VIEC = [
    ("sua-p3-ch6-9c-b15", {"Bài 15."}, {"reflection"},
     "- Chữ $k$ là tham số. Ý d) mở đầu \"Theo câu a) và b), …\", giải phương trình ẩn $k$, loại nghiệm theo $k>0$, "
     "kiểm tra $\\Delta>0$ với $k$ tìm được, rồi tính $B$ theo câu c). Dòng \"Vậy\" riêng.\n- Ý a), b), c) mỗi ý một dòng."),
    # 17/11 Thầy "ôn giải hpt làm chi" ⇒ bỏ bài giải hệ; Bài 2 (Mai Dịch) thêm câu dẫn lập hệ; Bài 4 mới √(A²)=|A|;
    # Bài 7 bớt câu dẫn bỏ căn (chuyển sang Bài 4).
    ("sua2-p3-ch6-9c", {"Bài 2.", "Bài 4.", "Bài 7."}, {"practice1", "practice2"},
     "- Bài 2 ý d): giải hệ ở câu c) ngay trong lời giải (thế hoặc cộng đại số, hai ba dòng), KHÔNG nhắc bài nào khác.\n"
     "- Bài 4 là trắc nghiệm, phương án theo thứ tự A. $3-x$ · B. $x-3$ · C. $x+3$ · D. $-x-3$: lời giải \"Chọn A.\" rồi "
     "một dòng lí do theo $\\sqrt{A^2}=|A|$ và dấu của $x-3$.\n"
     "- Bài 7 ý c) làm đủ: dùng câu b) viết căn thành $|x_1-3|$, bỏ dấu giá trị tuyệt đối vì $x_1<0$, rồi Viète, tính $A$."),
]


def main():
    for vid, nhan, chang, dan in VIEC:
        if len(sys.argv) > 1 and vid not in sys.argv[1:]:
            continue
        dong = [d for d in so_do(chang).split("\n- ") if any(d.lstrip("- ").startswith(n + " ") for n in nhan)]
        assert len(dong) == len(nhan), (vid, len(dong))
        prompt = CHUNG + LUAT_LOI_GIAI + r'''
## Việc: lời giải các bài dưới đây (đề mới, giáo viên đã chốt — chép NGUYÊN đề vào "statement")
Đầu ra {"sua":[{"label","statement","solution"}…],"ghi_chu":"…"} — đủ mọi bài dưới đây, đúng nhãn.
''' + dan + "\n\n## Sơ đồ\n- " + "\n- ".join(dong) + "\n"
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": [],
             "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
             "meta": {"loai": "sua-p3-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự)")

if __name__ == "__main__":
    main()
