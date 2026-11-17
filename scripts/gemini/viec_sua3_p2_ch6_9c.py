#!/usr/bin/env python3
"""Việc Gemini đợt 3 — Phiếu 2 ch.VI 9C bản 2 (17/11/2026): mỗi câu [NB] chỉ MỘT bước.

Thầy 17/11: "Bài 3 là NB ấy hả? Bạn đếm xem mấy bước?" — SGK 6.43 (tính x₁²+x₂²) đi 4 bước (điều kiện, Viète,
biến đổi, thay số) = TH. Claude soát lại mọi câu [NB]: Bài 3, 9, 13a, 14a, 15a, 17ab, 18 (bỏ ý giải m=2),
26b, 32a, 33a gộp 2–3 bước ⇒ tách còn một bước, phần còn lại dồn vào ý [TH]/[VD]. Sơ đồ mới ở so_do_p2_ch6_9c.

    .venv/bin/python scripts/gemini/viec_sua3_p2_ch6_9c.py
    python3 scripts/gemini/tho.py --mot sua3-p2-ch6-9c
    .venv/bin/python scripts/gemini/lap_p2_ch6_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p2_ch6_9c import KHOI  # noqa: E402
from viec_dung_p2_ch6_9c import CHUNG, KHUON_KHOI, MODEL, SEED  # noqa: E402
from viec_sua_p2_ch6_9c import LUAT_SUA  # noqa: E402

VID = "sua3-p2-ch6-9c"
NHAN = ["Bài 3.", "Bài 9.", "Bài 13.", "Bài 14.", "Bài 15.", "Bài 17.", "Bài 18.", "Bài 26.", "Bài 32.", "Bài 33."]


def so_do_moi():
    out = []
    for k in KHOI:
        if len(k) > 3 and k[0] in NHAN:
            nhan, _, tier, dang, level, ma, nguon, ht, noi = k
            out.append(f"- {nhan} tier={tier} dang_id={dang} level={level} hình thức={ht} mã={ma}"
                       + (f" nguồn in=\"{nguon}\"" if nguon else "") + "\n    " + noi)
    return "\n".join(out)


def ban_cu():
    f = json.loads((REPO / SEED).read_text())
    out = {}
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("label") in NHAN:
                out[b["label"]] = {k: b[k] for k in ("statement", "solution", "options") if b.get(k)}
    return json.dumps(out, ensure_ascii=False, indent=1)


PROMPT = CHUNG + KHUON_KHOI + LUAT_SUA + r'''
### Việc đợt 3: MỖI CÂU [NB] CHỈ MỘT BƯỚC
Giáo viên duyệt: câu [NB] là câu nhỏ nhắc MỘT công thức/điều kiện/MỘT phép tính (1,5 phút). Câu nào phải đi từ 2 bước trở lên (vd: kiểm tra điều kiện + Viète + biến đổi + thay số) là bài TH, không được gắn [NB]. Viết lại ĐÚNG 10 bài dưới đây theo SƠ ĐỒ MỚI:
- Câu [NB] hỏi đúng một việc như sơ đồ (không thêm "và cho biết…", "vì sao…" khi sơ đồ không có). Lời giải câu [NB] một hai dòng.
- Phần bị bỏ khỏi câu [NB] (dòng điều kiện $a\cdot c<0$ hoặc $\Delta\ge0$, giải bất phương trình điều kiện, khai triển mẫu, đối chiếu điều kiện) DỒN VÀO lời giải ý cuối [TH]/[VD], đủ nhịp bài thi. Ý cuối mở đầu "Theo câu a) và b), …" như đợt 2.
- Bài 3 là trắc nghiệm, "options" 4 phương án như sơ đồ (không chữ A. B.), lời giải "Chọn A." + một dòng lí do. Nguồn in sau đề: " \textit{(tách từ SGK 6{.}43)}".
- Bài 18: đề BỎ ý "Giải phương trình với $m=2$"; đề gốc giữ phần "Cho phương trình … ($m$ là tham số)." và nguồn.
- Giữ nguyên các chỗ khác của bài (đề gốc, nguồn, số liệu). KHÔNG chữ "Do đó", "Suy ra", "suy ra".
Đầu ra {"sua":[10 phần tử {"label","statement","solution","options"(chỉ Bài 3)}],"ghi_chu":"…"}.

## Sơ đồ mới của 10 bài
''' + so_do_moi() + r'''

## Bản hiện tại (sửa từ đây)
'''


def main():
    v = {"id": VID, "model": MODEL, "prompt": PROMPT + ban_cu() + "\n", "files": [],
         "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
         "meta": {"loai": "sua3-p2-ch6-9c", "seed": SEED}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
