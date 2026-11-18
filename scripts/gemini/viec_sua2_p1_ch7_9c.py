#!/usr/bin/env python3
"""Đợt sửa 2 Phiếu 1 ch.VII 9C (18/11/2026) — Thầy duyệt phương án (a): câu NB đổi hình thức
(trắc nghiệm A–D / Đúng–Sai / trả lời ngắn chỉ ghi số) để bớt thời gian trình bày. Đề do Claude chốt
(so_do_p1_ch7_9c.py), Gemini viết lại lời giải ngắn cho các bài đổi.

    .venv/bin/python scripts/gemini/viec_sua2_p1_ch7_9c.py && python3 scripts/gemini/tho.py --mot sua2-p1-ch7-9c
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch7_9c import KHOI, OPTIONS, cho_tho  # noqa: E402
from viec_dung_p1_ch7_9c import CHUNG, MODEL  # noqa: E402

VID = "sua2-p1-ch7-9c"
DOI = ["Bài 2.", "Bài 3.", "Bài 4.", "Bài 5.", "Bài 6.", "Bài 7.", "Bài 8.", "Bài 9.", "Bài 11.", "Bài 12.",
       "Bài 25.", "Bài 27.", "Bài 28.", "Bài 29.", "Bài 30.", "Bài 31.", "Bài 32.", "Bài 33.", "Bài 34."]
xong = {}
for v in ("lop", "btvn"):
    d = json.loads((REPO / f"storage/gemini/xong/dung-p1-ch7-9c-{v}.json").read_text())
    xong.update({x["label"]: x for x in (d.get("ket_qua") or d)["sua"]})
k = {x[0]: x for x in KHOI if len(x) > 3}


def mot(n):
    o = OPTIONS.get(n)
    them = ("\n    PHƯƠNG ÁN: " + " | ".join(f"{c}. {t}" for c, t in zip("ABCD", o))) if o else ""
    return (f"- {n}\n    ĐỀ MỚI: {cho_tho(k[n][8])}{them}\n    GHI CHÚ: {k[n][9]}\n"
            f"    LỜI GIẢI CŨ (đề cũ là tự luận — chỉ dùng để tham khảo số liệu): {xong[n]['solution']}")


pr = CHUNG + r'''
## Việc: viết lại LỜI GIẢI cho các bài vừa đổi hình thức (đề đã chốt, người lắp tự in đề)
Các câu nhận biết đã đổi sang hình thức ngắn để học sinh không phải trình bày dài:
- Ý trắc nghiệm (có A. B. C. D.): lời giải MỘT dòng, dạng "b) Chọn C vì $f=\frac{14}{50}\cdot 100\%=28\%$." Có thể thêm nửa câu chỉ ra phương án sai hay gặp nếu ghi chú có nói.
- Ý Đúng/Sai: "a) Đúng vì $9+14+5+3=31$." / "b) Sai vì xe $7$ chỗ có tần số lớn nhất ($14$)." Bài 2: "Sai vì …" rồi một dòng bảng đúng "[[bang: …]]".
- Ý "là bao nhiêu?": MỘT dòng chỉ ghi kết quả kèm phép tính ngắn nếu có, ví dụ "a) Tần số của nhóm $[150; 155)$ là $14$."
- Bài 8 ý a) GIỮ NGUYÊN lời giải cũ (lập bảng tự luận), chỉ viết lại ý b) theo dạng trắc nghiệm.
- Không cần dòng "Vậy" cho ý trắc nghiệm / Đúng–Sai / trả lời ngắn (bài toàn câu ngắn). Bài có nhiều ý: mỗi ý một dòng.
Đầu ra {"sua":[{"label":"Bài N.","statement":"","solution":"…"} cho đúng 19 bài dưới đây theo thứ tự],"ghi_chu":"…"}. Tự đếm, tính lại; thấy phương án đúng lệch ghi chú thì ghi vào "ghi_chu".

## Các bài
''' + "\n".join(mot(n) for n in DOI) + "\n"
v = {"id": VID, "model": MODEL, "prompt": pr, "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json",
     "timeout": "900s", "meta": {"loai": "sua2-p1-ch7-9c"}}
(REPO / "storage/gemini/hang-doi" / f"{VID}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
print(VID, len(pr) // 1000, "k ký tự")
