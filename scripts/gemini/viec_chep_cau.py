#!/usr/bin/env python3
"""Sinh việc "chép nguyên văn + giải" cho thợ Gemini từ danh sách câu đã bốc.

    python3 scripts/gemini/viec_chep_cau.py --bo-cau storage/gemini/bo-cau/l7-ck1.json \
        --ban-ghi inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi

Mỗi đề nguồn ⇒ một việc storage/gemini/hang-doi/chep-<mã đề>.json, chỉ gồm các ý đã bốc.
Kết quả (storage/gemini/xong/chep-*.json) là chữ LaTeX + lời giải theo bước có điểm + hình (TikZ),
Claude soát trước khi đưa vào script dựng đề.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HANG_DOI = REPO / "storage/gemini/hang-doi"

MAU = r"""Bạn là thợ chép đề Toán sang LaTeX. Làm CẨN THẬN, ĐÚNG NGUYÊN VĂN, KHÔNG BỊA.

Thư mục làm việc có một đề kiểm tra cuối học kì I Toán {lop} (Hà Nội), có thể kèm hướng dẫn chấm (HDC):
  - ảnh từng trang trang-1.png, trang-2.png, … (hoặc trang-01.png …): NGUỒN CHÍNH, hãy MỞ XEM ảnh;
  - {txt}: lớp chữ trích tự động, hay mất kí hiệu hoặc rỗng, chỉ để đối chiếu.
KHÔNG chạy lệnh shell (bị cấm). Chỉ dùng công cụ xem/đọc file.

VIỆC: với MỖI ý trong danh sách dưới đây (và CHỈ các ý đó), ghi một phần tử vào mảng "cau":
{ds}

QUY TẮC
1. "cau": đúng nhãn như danh sách.
2. "de_bai": chép NGUYÊN VĂN từ ảnh đề, viết LaTeX: mọi công thức trong $...$; phân số \frac{{a}}{{b}},
   số thập phân dùng dấu phẩy viết {{,}} trong công thức (ví dụ $2{{,}}5$), căn \sqrt{{}}, góc \widehat{{ABC}},
   tam giác \Delta ABC, song song \parallel, vuông góc \perp, độ ^\circ, phần trăm \%.
   KHÔNG viết nhãn "Câu 3." hay "a)" ở đầu; KHÔNG ghi điểm "(1,5 điểm)".
   Trắc nghiệm: de_bai chỉ là phần câu hỏi; 4 phương án vào "phuong_an" (không có "A." "B."...).
3. "loi_dan": ý ĐẦU TIÊN của một bài có lời dẫn chung (bài hình "Cho tam giác…", bài thực tế, đề "Thực
   hiện phép tính", "Tìm x, biết") thì chép lời dẫn đó vào đây (nguyên văn, LaTeX), de_bai chỉ là phần riêng của ý.
4. "dap_an": trắc nghiệm ghi A/B/C/D; tự luận ghi đáp số cuối (LaTeX) hoặc "chứng minh".
5. "loi_giai": lời giải đầy đủ kiểu bài làm của học sinh giỏi, MỖI BƯỚC MỘT PHẦN TỬ, viết LaTeX.
   Có HDC ⇒ bám HDC, ghi "diem" của từng bước đúng như HDC, "nguon_loi_giai": "HDC".
   Không có HDC ⇒ tự giải, chia điểm hợp lí (bội của 0,25) sao cho cộng lại bằng điểm của ý, "nguon_loi_giai": "tu_giai".
   Trắc nghiệm: 1–2 bước giải thích ngắn vì sao chọn, không cần "diem".
   Bài hình chứng minh: viết đủ lập luận "Xét $\Delta ABI$ và $\Delta AKI$ có: … $\Rightarrow$ … (c.g.c)", nêu rõ
   căn cứ (tính chất, dấu hiệu). Không dùng kiến thức ngoài lớp {lop} học kì I.
   Tự kiểm tra lại mọi phép tính; nếu HDC sai thì sửa theo đề in và nói trong "can_soat".
6. "hinh": nếu ý có hình (hình vẽ, biểu đồ) và đây là ý ĐẦU TIÊN của bài có hình:
   "mo_ta" = mô tả hình bằng lời (điểm nào nằm đâu, kí hiệu bằng nhau, số đo ghi trên hình);
   "tikz" = mã TikZ (chỉ phần bên trong \begin{{tikzpicture}}…\end{{tikzpicture}}) vẽ lại hình đúng tỉ lệ hợp lí,
   dùng \coordinate, \draw, \node, đúng nhãn và số đo như đề. Biểu đồ quạt tròn: dùng \draw … arc và ghi
   phần trăm trên từng phần. Bài hình mà đề yêu cầu HS tự vẽ (không có hình trong đề) vẫn ghi tikz của hình
   đúng (dùng cho lời giải).
7. Mọi chỗ không đọc rõ, nghi đề in sai, hay đề và HDC lệch ⇒ ghi rõ vào "can_soat".
8. "de": "{ma}"; "so_trang_da_doc": số ảnh đã mở xem.

Chỉ trả về MỘT đối tượng JSON đúng schema, không thêm lời.
"""


def refs_cua(x):
    if "ref" in x:
        yield x
    for y in x.get("y", []):
        yield y


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bo-cau", required=True)
    ap.add_argument("--ban-ghi", required=True)
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    a = ap.parse_args()
    bo = json.loads((REPO / a.bo_cau).read_text())
    can = collections.defaultdict(dict)
    for de in bo:
        for k, v in de.items():
            for x in (v if isinstance(v, list) else [v] if isinstance(v, dict) else []):
                for y in refs_cua(x):
                    m, c = y["ref"].split("#")
                    can[m][c] = y.get("nd", "")
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    for m, cs in sorted(can.items()):
        bg = json.loads((REPO / a.ban_ghi / f"{m}.json").read_text())
        pdf = Path(bg["thu_muc"]) / bg["pdf"]
        nhan = {q["cau"] for q in bg["cau"]}
        thieu = set(cs) - nhan
        assert not thieu, f"{m}: nhãn không có trong bản ghi {thieu}"
        ds = "\n".join(f"  - {c}: (tóm tắt để nhận ra) {cs[c][:160].replace(chr(10), ' ')}"
                       for c in sorted(cs))
        lop = m.split("-")[0][1:]
        viec = {
            "id": f"chep-{m}", "model": a.model,
            "prompt": MAU.format(lop=lop, txt=pdf.stem + ".txt", ds=ds, ma=m),
            "files": [str(pdf)], "render": True,
            "schema": "scripts/gemini/schema/chep-cau.json", "timeout": "900s",
            "meta": {"loai": "chep", "de": m, "cau": sorted(cs), "bo_cau": a.bo_cau},
        }
        (HANG_DOI / f"chep-{m}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(f"chep-{m}: {len(cs)} ý")
    print(f"{len(can)} việc, {sum(len(v) for v in can.values())} ý")


if __name__ == "__main__":
    main()
