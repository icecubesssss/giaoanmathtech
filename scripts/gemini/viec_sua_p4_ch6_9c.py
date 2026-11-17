#!/usr/bin/env python3
"""Việc sửa Phiếu 4 ch.VI 9C (17/11/2026, lượt 3) — bỏ hẳn phần phương trình chứa ẩn ở mẫu.

Thầy: "phương trình chứa ẩn ở mẫu HS đã học ở lớp 8 … ôn xong mấy câu dưới có dùng k?" ⇒ bỏ Mạch 1 cũ, kiến thức cũ
chỉ còn bước khử mẫu (Bài 1). Hai việc:
  sua-p4-ch6-9c-lt   : viết lại opener, nhắc lại, lý thuyết (chỉ 3 bước SGK), ghi chú giáo viên
  sua-p4-ch6-9c-bai  : lời giải 5 bài mới (Bài 1, 7, 9, 14, 19)
Bài còn lại giữ lời giải bản dựng đầu (lap_p4_ch6_9c.py đổi nhãn qua NHAN_CU).

    .venv/bin/python scripts/gemini/viec_sua_p4_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 2
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p4_ch6_9c import KHOI  # noqa: E402
from viec_dung_p4_ch6_9c import CHUNG, LUAT_LOI_GIAI, MODEL, SEED, TEP  # noqa: E402

VID_LT2, VID_BAI2 = "sua-p4-ch6-9c-lt", "sua-p4-ch6-9c-bai"
BAI_MOI = ("Bài 1.", "Bài 7.", "Bài 9.", "Bài 14.", "Bài 19.")

# Bối cảnh chung của lượt dựng đầu nói tới phương trình chứa ẩn ở mẫu — thay bằng bối cảnh mới.
CHUNG2 = CHUNG.replace(
    "Nội dung: (1) giải phương trình chứa ẩn ở mẫu quy về phương trình bậc hai theo 4 bước SGK (tìm ĐKXĐ → quy đồng "
    "mẫu hai vế rồi khử mẫu → giải phương trình vừa tìm được → kết luận, loại giá trị không thỏa mãn ĐKXĐ); (2) giải "
    "bài toán bằng cách lập phương trình",
    "Nội dung: giải bài toán bằng cách lập phương trình BẬC HAI (phương trình lập được có ẩn ở mẫu thì nhân hai vế với "
    "mẫu chung, đưa về phương trình bậc hai rồi giải bằng công thức nghiệm $\\Delta=b^2-4ac$ ở Phiếu 1). KHÔNG dạy lại "
    "cách giải phương trình chứa ẩn ở mẫu (học sinh đã thạo từ lớp 8), KHÔNG nói tới điều kiện xác định — chỉ có điều "
    "kiện của ẩn. Bài toán lập phương trình")
assert CHUNG2 != CHUNG


def so_do(nhan):
    dong = []
    for k in KHOI:
        if len(k) == 3 or k[0] not in nhan:
            continue
        nh, _, tier, dang, level, ma, _, ht, de, ghi = k
        dong.append(f"- {nh} tier={tier} dang_id={dang} level={level} hình thức={ht} mã={ma}\n    ĐỀ: {de}\n    GHI CHÚ: {ghi}")
    return "\n".join(dong)


DE_DICH = next(k[8] for k in KHOI if k[0] == "Bài 11.").split("[[br]]")[0]

PROMPT_LT2 = CHUNG2 + r'''
## Việc: viết lại phần mở đầu, nhắc lại, kiến thức cần nhớ, ghi chú giáo viên
Được giao ảnh SGK sgk9t2-tr25.png (tập hai tr.25, Bài 21: "Nhận xét. Các bước giải một bài toán bằng cách lập phương trình"). ĐỌC ẢNH để chép đúng chữ SGK.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}.

Cấu trúc phiếu (đã chốt): Luyện tập 1 = Bài 1 (ôn bước khử mẫu) + Mạch 1 hình chữ nhật (Ví dụ 1, Bài 2) + Mạch 2 năng suất (Ví dụ 2, Bài 3, Ví dụ 3, Bài 4). Luyện tập 2 = Mạch 3 chuyển động (Ví dụ 4, Bài 5, Bài 6, Ví dụ 5, Bài 7, Bài 8) + Mạch 4 làm chung, làm riêng (Ví dụ 6, Bài 9, Bài 10) + Mạch 5 hai giai đoạn (Ví dụ 7, Bài 11 = đề đích). Bài tập về nhà Bài 12–21.

1. "opener_text" (4–5 dòng nối [[br]]): chép đề đích trong \emph{\textquotedblleft…\textquotedblright} kèm nguồn \textit{(thi thử vào 10, THCS Tự Lập, 2025--2026)}, rồi nêu: chọn ẩn là vận tốc thường ngày $x$, thời gian mỗi đoạn bằng quãng đường chia vận tốc nên phương trình có ẩn ở mẫu; nhân hai vế với mẫu chung thì được một phương trình bậc hai, giải bằng công thức nghiệm đã học ở Phiếu 1. Việc chính của buổi học là ba bước SGK: chọn ẩn và biểu diễn các đại lượng, lập phương trình, giải rồi đối chiếu điều kiện để trả lời. Kết: đề này là Bài 11. Không nói "phương trình chứa ẩn ở mẫu" như một nội dung cần học, không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (khối Nhắc lại — chỉ kiến thức ĐÃ HỌC và CÓ DÙNG trong các bài), mỗi mục một dòng "$\bullet$\; …" nối [[br]], đúng 4 mục:
   công thức nghiệm của phương trình $ax^2+bx+c=0$ ($a\ne0$): $\Delta=b^2-4ac$, $\Delta>0$ thì có hai nghiệm phân biệt $x_{1,2}=\dfrac{-b\pm\sqrt\Delta}{2a}$ (Phiếu 1) · khử mẫu: nhân hai vế của phương trình với mẫu chung (lớp 8) · quãng đường $=$ vận tốc $\times$ thời gian, khối lượng công việc $=$ năng suất $\times$ thời gian (Toán 5) · đổi đơn vị: $1$ phút $=\dfrac{1}{60}$ giờ (Toán 5).
3. "concept_blocks" — CHỈ MỘT mục, hai khối: {"type":"para","variant":"heading","text":"Các bước giải bài toán bằng cách lập phương trình"} rồi {"type":"para","text":"<chép Nhận xét SGK tr.25: \textit{Bước 1.} Lập phương trình: rồi ba dòng gạch đầu dòng \"--\" (chọn ẩn số và đặt điều kiện thích hợp cho ẩn số · biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết · lập phương trình biểu thị mối quan hệ giữa các đại lượng), \textit{Bước 2.} Giải phương trình., \textit{Bước 3.} Trả lời: …; mỗi ý một dòng [[br]]> \textit{(SGK Toán 9 tập hai, tr.25)}"}. KHÔNG thêm mục điều kiện xác định, cách giải phương trình chứa ẩn ở mẫu, mẹo, lỗi hay gặp.
4. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 10 phút — nhắc lại công thức nghiệm, khử mẫu, các công thức chuyển động và năng suất, đổi phút ra giờ, đọc đề đích, chưa giải.
   concept: 5 phút — đọc to ba bước SGK, nhấn Bước 3 đối chiếu nghiệm với điều kiện của ẩn.
   practice1: khoảng 45 phút — Bài 1 hỏi nhanh cả lớp. Ví dụ 1 làm chậm, đủ đoạn phân tích. Mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm bài ngay sau, câu hỏi dẫn trả lời miệng, ý cuối tự trình bày vào vở. Giáo viên kẻ bảng đại lượng (dự định, thực tế) trên bảng cho các bài năng suất.
   practice2: khoảng 90 phút — tương tự, kẻ bảng quãng đường, vận tốc, thời gian cho bài chuyển động. Bài 10, Bài 11 ý cuối học sinh tự làm như đi thi, không gợi ý thêm. Bài 11 (đề đích) làm cá nhân rồi gọi lên bảng.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 12--21 in thành phiếu riêng. Buổi sau chữa Bài 20, Bài 21 trước.
'''

PROMPT_BAI2 = CHUNG2 + LUAT_LOI_GIAI + r'''
## Việc: lời giải 5 bài (đề đã chốt — chép nguyên)
Đầu ra {"sua":[5 bài theo đúng thứ tự],"ghi_chu":"…"}. Bài 1 là trắc nghiệm (phương án A là $240(x+10)-240x=2x(x+10)$): lời giải 1–2 dòng "Mẫu chung là $x(x+10)$. Nhân hai vế với $x(x+10)$, ta được …" rồi "Chọn A.", không giải tiếp.

## Sơ đồ
''' + so_do(BAI_MOI) + "\n"


def main():
    viec = [(VID_LT2, PROMPT_LT2, "scripts/gemini/schema/ly-thuyet-phieu.json", [f"{TEP}/sgk9t2-tr25.png"]),
            (VID_BAI2, PROMPT_BAI2, "scripts/gemini/schema/sua-bai-phieu.json", [])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "sua-p4-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
