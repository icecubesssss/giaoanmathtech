#!/usr/bin/env python3
"""Đợt sửa 3 Phiếu 1 ch.VII 9C (18/11/2026) — rút gọn lời giải Ví dụ 2 (hộp ví dụ cao gần 1 trang, không ngắt trang
được ⇒ trang 5 trắng). Chạy: .venv/bin/python scripts/gemini/viec_sua3_p1_ch7_9c.py && python3 scripts/gemini/tho.py --mot sua3-p1-ch7-9c
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch7_9c import KHOI, cho_tho  # noqa: E402
from viec_dung_p1_ch7_9c import CHUNG, LUAT_VI_DU, MODEL  # noqa: E402

VID = "sua3-p1-ch7-9c"
d = json.loads((REPO / "storage/gemini/xong/dung-p1-ch7-9c-lop.json").read_text())
cu = [x for x in (d.get("ket_qua") or d)["sua"] if x["label"] == "Ví dụ 2."][0]["statement"]
de = cho_tho(next(k[8] for k in KHOI if k[0] == "Ví dụ 2."))
pr = CHUNG + LUAT_VI_DU + r'''
## Việc: RÚT GỌN lời giải Ví dụ 2 (hộp ví dụ đang quá cao, làm trang trước bỏ trắng)
- Ý a) chỉ còn HAI dòng ngắn, mỗi biểu đồ một dòng, đọc MỘT cột / MỘT điểm làm mẫu, không liệt kê hết:
  "a) Biểu đồ A (dạng cột): cột ở điểm $8$ cao $[[fill:12]]$ nghĩa là có $12$ học sinh được điểm $8$." và
  "\hspace*{1.4em}Biểu đồ B (dạng đoạn thẳng): điểm $(9; 6)$ nghĩa là có $[[fill:6]]$ học sinh được điểm $9$." (được sửa câu chữ cho tự nhiên, giữ ý).
  Lưu ý: số trong ô không in lại ngoài ô ở dòng sau — viết lại câu cho đúng luật.
- Ý b) giữ bảng có ô, gộp hai dòng cuối thành MỘT dòng Vậy: "Vậy hai biểu đồ cùng biểu diễn một dữ liệu, bảng thu được là bảng tần số với cỡ mẫu $n=[[fill:33]]$." Bỏ dòng "Bảng thống kê trên cho biết …".
Đầu ra {"sua":[{"label":"Ví dụ 2.","statement":"<toàn bộ phần Lời giải mới>","solution":""}],"ghi_chu":""}.

ĐỀ: ''' + de + "\nLỜI GIẢI HIỆN TẠI: " + cu + "\n"
v = {"id": VID, "model": MODEL, "prompt": pr, "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json",
     "timeout": "600s", "meta": {"loai": VID}}
(REPO / "storage/gemini/hang-doi" / f"{VID}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
print(VID)
