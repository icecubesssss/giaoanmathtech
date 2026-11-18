#!/usr/bin/env python3
"""Đợt sửa 1 Phiếu 1 ch.VII 9C (18/11/2026) — theo cảnh báo vi_du_gate sau lượt dựng:
gợi ý (hints) cho 4 bài TH BTVN không có câu dẫn [NB]; kết luận ví dụ có ô điền; số trong ô bị in lại phía dưới.

    .venv/bin/python scripts/gemini/viec_sua_p1_ch7_9c.py && python3 scripts/gemini/tho.py --mot sua-p1-ch7-9c
    (lap_p1_ch7_9c.py đè kết quả theo nhãn qua VID_SUA)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch7_9c import KHOI, cho_tho  # noqa: E402
from viec_dung_p1_ch7_9c import CHUNG, LUAT_VI_DU, MODEL  # noqa: E402

VID = "sua-p1-ch7-9c"
xong = {}
for v in ("lop", "btvn"):
    d = json.loads((REPO / f"storage/gemini/xong/dung-p1-ch7-9c-{v}.json").read_text())
    xong.update({x["label"]: x for x in (d.get("ket_qua") or d)["sua"]})
de = {k[0]: cho_tho(k[8]) for k in KHOI if len(k) > 3}

VIEC_VD = {
    "Ví dụ 1.": "Dòng kết luận của ý b) đang in sẵn \"Vậy bảng tần số … là bảng trên\" — viết lại dòng Vậy có ô: "
                "\"Vậy Mai đi xe buýt [[fill:9]] ngày, xe máy [[fill:5]] ngày, xe đạp [[fill:8]] ngày.\" và bỏ các "
                "ô trong bảng ý b) (bảng ý b) in số thường) để không trùng ô.",
    "Ví dụ 5.": "Kết luận đang in sẵn \"Vậy bảng tần số tương đối ghép nhóm … \". Viết lại dòng Vậy của mỗi ý có ô ở "
                "giá trị kết luận (vd ý a) mức có tần số tương đối lớn nhất, ý b) cỡ mẫu và nhóm có tần số tương đối lớn "
                "nhất). Kiểm tra: số 20 đã là ô ở trên thì phía dưới không in sẵn số 20 ngoài ô (đổi cách viết hoặc khoét).",
    "Ví dụ 9.": "Kết luận đang in sẵn \"Vậy bảng … là bảng trên\". Viết lại: \"Vậy nhóm [[fill:$[161; 164)$]] có "
                "nhiều học sinh nhất, chiếm [[fill:37{,}5]]\\%.\" — chú ý quy tắc ô ngoài $ phải viết $[[fill:…]]$; ô "
                "chứa nửa khoảng thì viết \"nhóm $[[fill:[161; 164)]]$\" (KHÔNG có dấu ]]] — đổi sang "
                "\"nhóm từ [[fill:161]] cm đến dưới [[fill:164]] cm\").",
    "Ví dụ 10.": "Kết luận đang in sẵn \"Vậy nhận định … là đúng\" — khoét chữ \"đúng\" thành [[fill:đúng]]. Các số 15 và "
                 "70 đã là ô ở trên thì phía dưới không in sẵn ngoài ô.",
}
VIEC_BAI = ["Bài 35.", "Bài 36.", "Bài 41.", "Bài 43."]

pr = CHUNG + LUAT_VI_DU + r'''
## Việc: sửa nhỏ sau cổng kiểm tra
Đầu ra {"sua":[…],"ghi_chu":"…"} — mỗi phần tử một nhãn dưới đây, giữ nguyên mọi chỗ không nói tới.

### A. Ví dụ — trả "statement" = TOÀN BỘ phần lời giải đã sửa (mở bằng {\sffamily\bfseries\color{brand}Lời giải}), "solution":"".
''' + "\n".join(f"- {n}\n    ĐỀ: {de[n]}\n    YÊU CẦU: {y}\n    LỜI GIẢI HIỆN TẠI: {xong[n]['statement']}"
                for n, y in VIEC_VD.items()) + r'''

### B. Bài TH ở bài tập về nhà không có câu dẫn — thêm "hints": đúng MỘT gợi ý ngắn (một câu, định hướng bước đầu, KHÔNG lộ số đáp án), "statement":"", "solution" = giữ NGUYÊN lời giải hiện tại.
''' + "\n".join(f"- {n}\n    ĐỀ: {de[n]}\n    LỜI GIẢI HIỆN TẠI: {xong[n]['solution']}" for n in VIEC_BAI) + "\n"

v = {"id": VID, "model": MODEL, "prompt": pr, "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json",
     "timeout": "900s", "meta": {"loai": "sua-p1-ch7-9c"}}
(REPO / "storage/gemini/hang-doi" / f"{VID}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
print(VID, len(pr) // 1000, "k ký tự")
