#!/usr/bin/env python3
"""Sinh 2 việc Gemini cho buổi 2 chương X lớp 9C (12/11/2026).

Thầy: "làm qua Gemini cho đỡ tốn TOKEN … giao việc cho nó sửa phiếu và soát 2 đầu".
  sua-9c-ch10-phieu-c : Gemini SỬA + TỰ SOÁT phiếu C (mọi bài, ví dụ, BTVN) — trả đủ mọi nhãn.
  soat-9c-ch10-kt     : Gemini SOÁT CHÉO đề KT chương X + ma trận–đáp án (chỉ báo lỗi, không sửa).

    python3 scripts/gemini/viec_sua_phieu_c_ch10_9c.py
    python3 scripts/gemini/tho.py --mot sua-9c-ch10-phieu-c      (và --mot soat-9c-ch10-kt)
    python3 scripts/gemini/ap_sua_phieu.py sua-9c-ch10-phieu-c [--ghi]
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DIR = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien"
SEED = f"{DIR}/phieu-c-luyen-tap-chung-va-bai-tap-cuoi-chuong-x.json"
KT_DE = f"{DIR}/kiem-tra-chuong/de-kiem-tra-chuong-x.json"
KT_DA = f"{DIR}/kiem-tra-chuong/ma-tran-va-dap-an-kiem-tra-chuong-x.json"

CHUNG = r'''KHÔNG chạy lệnh, KHÔNG mở file: toàn bộ dữ liệu nằm ở mục "Dữ liệu gốc" cuối prompt. Xuống dòng trong chuỗi là [[br]]. Toán viết LaTeX trong $...$, số thập phân kiểu Việt Nam $3{,}14$, nghìn cách bằng \, ($11\,304$). Giữ escape \% \& (ví dụ "$80\%$", "GD\&ĐT"). Lấy $\pi \approx 3{,}14$ trừ khi đề ghi kết quả theo $\pi$.
Học sinh lớp 9 tầng C (học lực trung bình yếu). Chương X: hình trụ $S_{xq}=2\pi rh$, $V=\pi r^2h$; hình nón $S_{xq}=\pi rl$, $V=\frac13\pi r^2h$, $l^2=r^2+h^2$; hình cầu $S=4\pi R^2$, $V=\frac43\pi R^3$. $1$ lít $=1$ dm$^3=1000$ cm$^3$, $1$ m$^3=1000$ lít.
'''

PROMPT_SUA = r'''Bạn là thợ sửa phiếu học tập Toán 9 (chương X — hình trụ, hình nón, hình cầu). Làm CẨN THẬN, CHỈ sửa đúng phạm vi, KHÔNG bịa đề, KHÔNG đổi số liệu đề (đề lấy từ đề thi thật).
''' + CHUNG + r'''
Mỗi phần tử dữ liệu có "label" ("Bài 3.", "BTVN 4.", "Ví dụ 1."), "statement", "solution". Với "Ví dụ N." thì "statement" là TOÀN BỘ hộp ví dụ (đề + "Lời giải" mẫu có ô [[fill:đáp án]]), "solution" để chuỗi rỗng.

## Việc 1 — rút gọn câu dẫn của 4 bài điền khuyết (đề dài làm slide co chữ không đọc được)
Bài 3., Bài 4., BTVN 3., BTVN 4.: phần đề TRƯỚC khung điền (trước dấu ":" + [[br]] đầu tiên) viết lại còn tối đa khoảng 35 chữ, vẫn đủ số liệu và đủ yêu cầu ("Điền vào chỗ trống để …"). PHẢI giữ dấu ":" ngay trước [[br]] đầu tiên (máy dựa vào đó để đặt hình giữa đề và khung). Khung điền phía sau giữ NGUYÊN số ô [[blank:…]] và vị trí ô, chỉ được sửa chữ cho gọn. BTVN 4. giữ yêu cầu vẽ phác vào khung.

## Việc 2 — soát và sửa lời giải theo nhịp bài thi (mọi bài có solution, kể cả BTVN)
- Mỗi bước một dòng ([[br]]); căn cứ trước kết quả ("Theo công thức thể tích hình trụ, …", "Xét …"); dòng kết luận "Vậy …" riêng, có đơn vị; làm tròn một lần ở bước cuối, từ chỗ xấp xỉ dùng $\approx$.
- Chú ý BTVN 8.: mỗi ý phải mở bằng căn cứ rõ ràng (máy soát đang báo thiếu).
- Bài trắc nghiệm: lời giải kết thúc "Vậy chọn X." với X đúng trường đáp án hiện có (không đổi phương án).

## Việc 3 — tự soát toàn phiếu (bắt buộc)
- TỰ TÍNH LẠI mọi đáp số (bài, ví dụ, ô [[fill:…]], đáp án trắc nghiệm). Sai thì sửa solution/ô fill cho đúng và GHI vào ghi_chu ("Bài N: cũ … → đúng …").
- Câu chữ: không văn nói, không từ tắt, không xưng "em", chính tả đúng; giữ thẻ [NB]/[TH]/[VD] đầu đề, giữ "(Hình N)", giữ \textbf{(nguồn đề)}.
- Ví dụ: KHÔNG để ô [[fill:x]] ở trên rồi dòng dưới lại in sẵn đúng số x (lộ đáp án) — nếu gặp thì khoét luôn chỗ dưới thành [[fill:x]].
- Không thêm/bớt bài, không đổi label, không đổi số ý, không đổi hình.

## Đầu ra
JSON đúng schema: {"sua": [ĐỦ MỌI phần tử của Dữ liệu gốc, mỗi phần tử {"label","statement","solution"} là chuỗi HOÀN CHỈNH — phần tử không cần sửa thì trả nguyên văn], "ghi_chu": "liệt kê từng chỗ đã sửa đáp số / nghi ngờ; chuỗi rỗng nếu không có"}.
'''

PROMPT_SOAT = r'''Bạn là giáo viên soát đề kiểm tra Toán 9 chương X (45 phút, lớp 9 tầng C). CHỈ SOÁT, KHÔNG viết lại đề.
''' + CHUNG + r'''
Dữ liệu: (1) tờ đề học sinh — các câu có "label", "statement", "options" (trắc nghiệm A–D theo thứ tự); (2) ma trận + đáp án giáo viên (đoạn văn LaTeX).

Soát và báo:
1. Từng câu: TỰ GIẢI LẠI, so với đáp án GV (chữ cái trắc nghiệm, số, đơn vị, làm tròn). Mọi chỗ lệch ⇒ báo.
2. Trắc nghiệm: có đúng MỘT phương án đúng không; phương án nhiễu có trùng nhau không.
3. Tổng điểm 10; điểm từng ý trong đề khớp biểu điểm; barem từng dòng (0,25đ) cộng đúng điểm ý.
4. Đề có đủ dữ kiện, không mơ hồ (đơn vị, làm tròn đến đâu, $\pi$ lấy bao nhiêu); lời giải đáp án có bước nào nhảy cóc / dùng kiến thức ngoài chương.
5. Chính tả, văn nói.

Đầu ra JSON đúng schema: "sua" = [] (mảng rỗng), "ghi_chu" = danh sách lỗi, mỗi lỗi một dòng bắt đầu "- Câu N: …" (ghi cả cách sửa đề xuất); nếu không thấy lỗi ghi "KHÔNG THẤY LỖI" kèm đáp số bạn tự tính cho từng câu.
'''


def _problems_and_examples(seed):
    out = []
    for s in seed["stages"]:
        for b in s.get("blocks", []):
            if b.get("type") == "problem":
                out.append({"label": b["label"], "statement": b["statement"], "solution": b.get("solution", ""),
                            **({"options": b["options"], "answer": b.get("answer", "")} if b.get("options") else {})})
            elif b.get("type") == "noted" and b.get("variant") == "example":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b["text"])
                out.append({"label": m.group(1), "statement": b["text"], "solution": ""})
    return out


def ghi(vid, prompt, du_lieu, labels, seed):
    viec = {
        "id": vid, "model": "gemini-3.8-flash-high",
        "prompt": prompt + "\n## Dữ liệu gốc (JSON)\n" + json.dumps(du_lieu, ensure_ascii=False, indent=1) + "\n",
        "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
        "meta": {"loai": "sua-phieu", "seed": seed, "labels": labels},
    }
    out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), "—", len(labels), "nhãn")


def main():
    seed = json.loads((REPO / SEED).read_text())
    goc = _problems_and_examples(seed)
    ghi("sua-9c-ch10-phieu-c", PROMPT_SUA, goc, [x["label"] for x in goc], SEED)

    de = json.loads((REPO / KT_DE).read_text())
    da = json.loads((REPO / KT_DA).read_text())
    du = {"to_de": [{"label": b["label"], "statement": b["statement"], "options": b.get("options", [])}
                    for s in de["stages"] for b in s["blocks"] if b.get("type") == "problem"],
          "ma_tran_dap_an": [b["text"] for s in da["stages"] for b in s["blocks"] if b.get("type") == "para"]}
    ghi("soat-9c-ch10-kt", PROMPT_SOAT, du, [], KT_DE)


if __name__ == "__main__":
    main()
