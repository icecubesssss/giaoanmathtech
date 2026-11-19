#!/usr/bin/env python3
"""Việc sửa nhỏ Phiếu 1 ch.X 9C (19/11/2026, Thầy duyệt lượt 1): lời giải Bài 15 mới (tl-tcnc-23-tr9 thay sgk-10.23).

    .venv/bin/python scripts/gemini/viec_sua_p1_ch10_9c.py
    python3 scripts/gemini/tho.py --mot sua-p1-ch10-9c
    .venv/bin/python scripts/gemini/lap_p1_ch10_9c.py --ghi      (đè theo nhãn qua VID_SUA)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch10_9c import cho_tho, danh_so_hinh, khoi_bai  # noqa: E402
from viec_dung_p1_ch10_9c import CHUNG, LUAT_LOI_GIAI, MODEL, SEED, TEP  # noqa: E402

VID = "sua-p1-ch10-9c"
NHAN = ["Bài 15."]


def main():
    so = danh_so_hinh()
    dong = []
    for k in khoi_bai():
        if k["nhan"] in NHAN:
            dong.append(f"- {k['nhan']} tier={k['tier']} dang_id={k['dang']} level={k['level']} hình thức={k['ht']} "
                        f"mã={k['ma']}\n    ĐỀ: {cho_tho(k, so)}\n    GHI CHÚ: {k['ghi']}")
    prompt = CHUNG + LUAT_LOI_GIAI + r'''
## Việc: lời giải bài tập về nhà đổi đề (đọc ảnh sgk9t2-tr99 để theo nhịp lời giải SGK Ví dụ 4)
- Dòng tính theo định lí Pythagore phải nêu căn cứ ngay dòng trên: "Tam giác $ABC$ vuông tại $A$ nên theo định lí Pythagore ta có" rồi dòng "$AC^2=BC^2-AB^2=…$", KHÔNG tách thành nhiều dòng phương trình.
Đầu ra {"sua":[''' + str(len(NHAN)) + r''' bài],"ghi_chu":"…"}.

## Sơ đồ
''' + "\n".join(dong) + "\n"
    v = {"id": VID, "model": MODEL, "prompt": prompt, "files": [f"{TEP}/sgk9t2-tr99.png"],
         "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
         "meta": {"loai": "sua-p1-ch10-9c", "seed": SEED}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
