#!/usr/bin/env python3
"""Sinh việc Gemini: GẮN MÃ DẠNG (khung mới) cho từng ý của các đề ĐÃ DỰNG (seed JSON) — để cổng phủ dạng
đo được bộ đề cũ không trỏ về ngân hàng từng ý (lớp 5, 8, 9).

    python3 scripts/gemini/viec_gan_dang_bo_de.py --lop 9 --ky ck1 \
        --khung config/khung-phan-dang/lop-9-ck1-kntt.json \
        --seed inputs/seeds/lop-9/de-on-tap-cuoi-ki-1/de-on-tap-cuoi-ki-1-so-{1,2,3}.json \
               inputs/seeds/lop-9/de-on-tap-cuoi-ki-1/de-kiem-tra-cuoi-ki-1-chinh-thuc-so-{1,2,3}.json

Kết quả (storage/gemini/xong/gan-dang-l<lop>-<ky>-<seed>.json, mỗi đề một việc) → scripts/gemini/lap_bo_de_tu_gan_dang.py
⇒ inputs/refs/ngan-hang-sheet/lop-<lop>/<ky>/bo-de.json cho scripts/phu_dang_gate.py.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HANG_DOI = REPO / "storage/gemini/hang-doi"

MAU = """Bạn là giáo viên Toán {lop} soát ma trận đề. Làm CẨN THẬN, ĐỦ, KHÔNG BỊA.
KHÔNG chạy lệnh shell (bị cấm). Chỉ dùng công cụ đọc file.

Trong thư mục làm việc có {n} file JSON, mỗi file là MỘT đề kiểm tra/ôn tập đã soạn
(trường "stages" → "blocks"; mỗi block "problem" có "label" và "statement" bằng LaTeX, đôi khi có "parts").
Danh sách file: {ds}

VIỆC: với TỪNG file, liệt kê MỌI Ý CHẤM ĐIỂM của đề (mỗi câu trắc nghiệm, mỗi ý 1), 2), a), b) là một ý riêng)
và gắn:
  - "nhan": nhãn ý theo đề, ví dụ "TN3", "I.1", "II.2b", "IV.3".
  - "dang": ĐÚNG MỘT mã trong khung dưới đây. Ý thuộc bài thực tế ⇒ mã thực tế của chủ đề đó.
    Câu khó cuối đề ⇒ mã VDC. Không khớp ⇒ "D99" và ghi lí do vào "can_soat".
    LƯU Ý căn thức: biểu thức KHÔNG có ẩn (chỉ có số) ⇒ D10/D11/D12, không phải D14/D15.
  - "muc": NB / TH / VD / VDC (không nâng mức).
  - "diem": điểm của ý nếu đề ghi.
  - "nd": tóm tắt nội dung ý (≤ 20 chữ).
Trả "de": mỗi phần tử {{"file": "<tên file>", "y": [...]}}, đúng thứ tự file ở trên.

KHUNG DẠNG (mã — chương — tên dạng; [ngoài tập 1] = nội dung học kì II):
{khung}

Chỉ trả về MỘT đối tượng JSON đúng schema, không thêm lời.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", type=int, required=True)
    ap.add_argument("--ky", required=True)
    ap.add_argument("--khung", required=True)
    ap.add_argument("--seed", nargs="+", required=True)
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    a = ap.parse_args()
    khung = json.loads((REPO / a.khung).read_text())
    dong = "\n".join(f"{d['ma']} — CĐ{d['cd']} — {d['ten']}" + (" [ngoài tập 1]" if d.get("ngoai_tap_1") else "")
                     for d in khung["dang"])
    seeds = [str(Path(s).resolve().relative_to(REPO)) for s in a.seed]
    for s in seeds:
        assert (REPO / s).exists(), s
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    # MỘT việc / đề: gộp 6 đề một việc bị quá 15 phút (12/11/2026)
    for s in seeds:
        ma = f"gan-dang-l{a.lop}-{a.ky}-{Path(s).stem}"
        viec = {
            "id": ma, "model": a.model,
            "prompt": MAU.format(lop=a.lop, n=1, ds=Path(s).name, khung=dong),
            "files": [s], "schema": "scripts/gemini/schema/gan-dang-bo-de.json", "timeout": "900s",
            "meta": {"lop": a.lop, "ky": a.ky, "khung": a.khung, "seed": s},
        }
        (HANG_DOI / f"{ma}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("Đã ghi việc", ma)

if __name__ == "__main__":
    main()
