#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 4 ch.VI 9C bản 2 (17/11/2026) — 3 việc: lý thuyết, trên lớp, BTVN.

Sơ đồ (ĐỀ nguyên văn, thẻ, dang_id, đáp số SymPy) do Claude chốt ở so_do_p4_ch6_9c.py. Gemini chỉ viết LỜI GIẢI,
ví dụ điền khuyết và phần lý thuyết. Luật đợt 2–3 của Phiếu 2, 3 đưa thẳng vào prompt đợt 1.

    .venv/bin/python scripts/gemini/viec_dung_p4_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (dung-p4-ch6-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p4_ch6_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p4_ch6_9c import KHOI  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
        "phieu-4-giai-bai-toan-bang-cach-lap-phuong-trinh.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p4-ch6-9c-lt", "dung-p4-ch6-9c-lop", "dung-p4-ch6-9c-btvn"
TEP = "storage/gemini/tep/p4-ch6-9c"
ANH_LT = [f"{TEP}/{f}.png" for f in ("sgk9t1-tr28", "sgk9t1-tr29", "sgk9t2-tr25", "sgk9t2-tr26")]
ANH_LOP = [f"{TEP}/{f}.png" for f in ("sgk9t1-tr29", "sgk9t2-tr25", "sgk9t2-tr26")]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = next(k[8] for k in KHOI if k[0] == "Bài 11.").split("[[br]]")[0]

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, buổi 4: phương trình chứa ẩn ở mẫu và Bài 21 "Giải bài toán bằng cách lập phương trình", SGK Kết nối tri thức với cuộc sống) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Buổi 180 phút. Nội dung: (1) giải phương trình chứa ẩn ở mẫu quy về phương trình bậc hai theo 4 bước SGK (tìm ĐKXĐ → quy đồng mẫu hai vế rồi khử mẫu → giải phương trình vừa tìm được → kết luận, loại giá trị không thỏa mãn ĐKXĐ); (2) giải bài toán bằng cách lập phương trình theo 3 bước SGK (lập phương trình: chọn ẩn và điều kiện, biểu diễn đại lượng chưa biết theo ẩn, lập phương trình → giải phương trình → trả lời: kiểm tra nghiệm nào thỏa mãn điều kiện của ẩn rồi kết luận), các loại: hình chữ nhật, năng suất, chuyển động (có xuôi ngược dòng), làm chung – làm riêng, bài hai giai đoạn. Học sinh đã học công thức nghiệm của phương trình bậc hai ($\Delta=b^2-4ac$) ở Phiếu 1 và đã giải bài toán bằng cách lập hệ phương trình ở Chương I. KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao).

## Luật cứng (vi phạm bị trả lại)
- KHÔNG dùng $\Delta'$, $b'$. Chỉ $\Delta=b^2-4ac$. KHÔNG dấu $\Leftrightarrow$, $\Rightarrow$: mỗi phép biến đổi xuống một dòng.
- KHÔNG dấu chấm phẩy ";". Hai nghiệm viết "$x_1=30$, $x_2=-60$" hoặc "$x=30$ hoặc $x=-60$".
- CẤM chữ: "khuôn", "dạng đề", "Câu III", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy", "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy", "TMĐK", "(TM)", "(L)". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn. (Chữ "Do đó" có sẵn trong vài ĐỀ gốc — đề giữ nguyên, chỉ lời giải mới cấm.)
- Lời giải theo NHỊP BÀI THI giống SGK: mỗi bước một dòng; dòng con mở đầu "[[br]]\hspace*{1.4em}" ("\hspace*" chỉ đứng ĐẦU dòng); nối bằng "nên" trong cùng câu, hoặc mở dòng bằng "Ta có …", "Khi đó …", "Theo câu …". Dòng "Vậy …" riêng ở cuối mỗi bài.
- Bài lập phương trình viết như SGK: "Gọi $x$ (km/h) là … Điều kiện: $x>0$." · "… là $\dfrac{100}{x}$ (giờ)." · "Theo đề bài, ta có phương trình $…$" · "Quy đồng mẫu hai vế rồi khử mẫu, ta được $…$" · "$\Delta=…$, $\sqrt\Delta=…$" · "Phương trình có hai nghiệm $x_1=…$, $x_2=…$." · "Giá trị $x_1=…$ thỏa mãn điều kiện, $x_2=…$ không thỏa mãn điều kiện." · "Vậy …" (trả lời đúng câu hỏi của đề, có đơn vị). Điều kiện số tự nhiên viết $x\in\mathbb N^*$ (hoặc $x\in\mathbb N$, $x>2$).
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy $0{,}5$, số lớn $1\,800$, đơn vị diện tích "$280\ \text{m}^2$". Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong GHI CHÚ của sơ đồ đã được máy kiểm (SymPy) — dùng ĐÚNG. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Chữ trong ghi chú (như "chỉ đề", "BÀI ĐÍCH", "7–9 ô", "ĐỌC ẢNH") là cho người soạn, KHÔNG in.
'''

LUAT_LOI_GIAI = r'''
## Luật lời giải của BÀI (đề đã chốt — chép NGUYÊN "statement" như sơ đồ, không đổi một chữ)
- Mỗi ý trả lời ĐÚNG cái được hỏi, không thêm việc khác: "Tìm điều kiện xác định" ⇒ một dòng "$x\ne…$ và $x\ne…$". "Viết … theo $x$" ⇒ một dòng biểu thức kèm đơn vị. "Nêu điều kiện của $x$" ⇒ một dòng. "Đổi … ra giờ" ⇒ một dòng. "Khử mẫu, viết phương trình nhận được" ⇒ một dòng phương trình CHƯA thu gọn.
- Ý cuối ([TH]/[VD]) làm nốt bài, mở đầu "Theo câu b) và c), ta có phương trình …" (hoặc câu tương ứng), KHÔNG chép lại các dòng của ý trước. Ý cuối làm đủ: lập phương trình, quy đồng khử mẫu, thu gọn về $ax^2+bx+c=0$, tính $\Delta$, hai nghiệm, đối chiếu điều kiện (hoặc ĐKXĐ), dòng "Vậy …".
- Trắc nghiệm (Bài 1): solution 1–2 dòng, kết "Chọn C."
- Đầu ra mỗi bài: {"label":"Bài N.","statement":<chép nguyên đề sơ đồ>,"solution":"a) …[[br]]b) …[[br]]d) Theo câu …[[br]]\hspace*{1.4em}…"}.
'''

LUAT_VI_DU = r'''
## Luật VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết)
- Đầu ra: {"label":"Ví dụ N.","statement":"\\textbf{Ví dụ N.} <ĐỀ như sơ đồ, giữ nguồn>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …","solution":""}.
- Riêng Ví dụ 3 (ví dụ mở đầu ba bước): giữa đề và "Lời giải" chèn khối "{\\sffamily\\bfseries\\color{brand}Phân tích}" gồm 3 dòng câu hỏi dẫn, mỗi dòng có ô trả lời: "Đề hỏi gì? [[fill:chiều dài và chiều rộng]]" · "Chọn ẩn: gọi chiều rộng là $x$ (m), chiều dài là [[fill:$x+30$]] (m)" · "Câu nào cho phương trình? [[fill:diện tích bằng $1\,800\ \text{m}^2$]]".
- Ví dụ giải phương trình chứa ẩn ở mẫu (Ví dụ 1, 2): đi đúng 4 bước SGK, mỗi bước mở đầu bằng chữ nghiêng "\textit{Bước 1.}" … "\textit{Bước 4.}" như SGK tập một tr.29.
- Ví dụ lập phương trình (Ví dụ 3–9): đi theo 3 bước SGK, mỗi bước mở đầu "\textit{Bước 1.}", "\textit{Bước 2.}", "\textit{Bước 3.}" (Bước 1 nhiều dòng: chọn ẩn + điều kiện, mỗi đại lượng biểu diễn theo ẩn một dòng, dòng phương trình).
- Đi đúng các bước trong ghi chú, mỗi bước một dòng.
- Khoét 7–9 ô [[fill:đáp án]] ở chỗ giáo viên hỏi lớp: điều kiện của ẩn / ĐKXĐ, đại lượng biểu diễn theo ẩn, phút đổi ra giờ, phương trình lập được, phương trình sau khử mẫu, $\Delta$, nghiệm, nghiệm bị loại, kết luận.
- Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$\Delta=[[fill:8100]]$", "$x\ne[[fill:2]]$"). Ô ngoài $…$ chứa công thức mới bọc $ bên trong. Ô chứa phân số viết "$t=[[fill:\dfrac{100}{x}]]$" — đếm đủ dấu ngoặc, ô kết thúc bằng đúng hai dấu "]]" (KHÔNG BAO GIỜ ba dấu "]]]").
- Một số đã nằm trong ô thì KHÔNG in sẵn (ngoài ô) ở bất kì dòng nào phía DƯỚI ô đó trong cùng ví dụ (nếu cần nhắc lại thì khoét lần nữa hoặc viết "giá trị trên"). Kiểm tra lại từng ví dụ trước khi trả.
- Kết bằng dòng riêng "Vậy …" và giá trị kết luận là ô (vd "Vậy chiều rộng là [[fill:30]] m, chiều dài là [[fill:60]] m.").
- Ví dụ không có thẻ [NB]/[TH]/[VD].
'''


def so_do(chang):
    dong = []
    for k in KHOI:
        if k[1] not in chang:
            continue
        if len(k) == 3:
            dong.append(f"- [TIÊU ĐỀ MẠCH — người lắp tự chèn] {k[0]}")
            continue
        nhan, _, tier, dang, level, ma, _, ht, de, ghi = k
        dau = f"- {nhan} " + ("(VÍ DỤ)" if ht == "vi_du" else f"tier={tier} dang_id={dang} level={level} hình thức={ht}")
        dong.append(f"{dau} mã={ma}\n    ĐỀ: {de}\n    GHI CHÚ: {ghi}")
    return "\n".join(dong)


PROMPT_LT = CHUNG + r'''
## Việc A: phần mở đầu, nhắc lại, kiến thức cần nhớ, ghi chú giáo viên
Được giao ảnh SGK: sgk9t1-tr28.png, sgk9t1-tr29.png (tập một tr.28–29, mục 2 "Phương trình chứa ẩn ở mẫu": điều kiện xác định, cách giải 4 bước), sgk9t2-tr25.png, sgk9t2-tr26.png (tập hai tr.25–26, Bài 21: "Nhận xét. Các bước giải một bài toán bằng cách lập phương trình", Ví dụ 1, Ví dụ 2 có vận tốc xuôi dòng, ngược dòng). ĐỌC ẢNH để chép đúng chữ SGK.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}. ("mindmap" trả {} — người lắp tự dựng.)

1. "opener_text" (chặng Khám phá, 4–6 dòng nối bằng [[br]]): chép đề đích (Bài 11 cuối Luyện tập 2, đề thi thử vào 10 THCS Tự Lập 2025--2026) trong \emph{\textquotedblleft…\textquotedblright}, rồi nêu: bài có hai giai đoạn (3 km đầu đi như thường ngày, dừng 3 phút, rồi tăng tốc), thời gian mỗi đoạn là quãng đường chia vận tốc nên khi gọi vận tốc là $x$ thì phương trình lập được có ẩn ở mẫu. Muốn giải được cần hai việc: giải phương trình chứa ẩn ở mẫu (Luyện tập 1) và biết chọn ẩn, biểu diễn đại lượng, lập phương trình (Luyện tập 2). Kết: đề này là Bài 11. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (khối Nhắc lại — chỉ kiến thức ĐÃ HỌC), mỗi mục một dòng "$\bullet$\; …" nối [[br]]:
   phân tích mẫu thành nhân tử: $x^2-a^2=(x-a)(x+a)$ (hằng đẳng thức, lớp 8) · quy đồng mẫu nhiều phân thức: tìm mẫu thức chung rồi nhân tử và mẫu với nhân tử phụ (lớp 8) · công thức nghiệm của phương trình $ax^2+bx+c=0$ ($a\ne0$): $\Delta=b^2-4ac$, $\Delta>0$ có hai nghiệm phân biệt $x_{1,2}=\dfrac{-b\pm\sqrt\Delta}{2a}$ (Phiếu 1) · quãng đường $=$ vận tốc $\times$ thời gian, khối lượng công việc $=$ năng suất $\times$ thời gian (Toán 5) · đổi phút ra giờ: $1$ phút $=\dfrac1{60}$ giờ (Toán 5).
3. "concept_blocks" (chặng Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT SGK, mỗi mục là hai khối: {"type":"para","variant":"heading","text":"N. Tên"} rồi {"type":"para","text":"<nội dung>"}; cuối nội dung ghi nguồn trong \textit{(…)}. 3 mục:
   1. Điều kiện xác định của phương trình — chép khung SGK tập một tr.28 (đặt điều kiện cho ẩn để tất cả các mẫu thức trong phương trình đều khác 0, gọi là điều kiện xác định, viết tắt ĐKXĐ). \textit{(SGK Toán 9 tập một, tr.28)}
   2. Cách giải phương trình chứa ẩn ở mẫu — chép 4 bước SGK tập một tr.29 (Bước 1 … Bước 4), mỗi bước một dòng [[br]], "\textit{Bước 1.}" nghiêng như SGK. \textit{(SGK Toán 9 tập một, tr.29)}
   3. Các bước giải bài toán bằng cách lập phương trình — chép "Nhận xét" SGK tập hai tr.25: Bước 1 (ba gạch đầu dòng: chọn ẩn số và đặt điều kiện thích hợp cho ẩn số · biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết · lập phương trình biểu thị mối quan hệ giữa các đại lượng), Bước 2, Bước 3; mỗi ý một dòng [[br]], gạch đầu dòng viết "--". \textit{(SGK Toán 9 tập hai, tr.25)}
   KHÔNG thêm mẹo, lỗi hay gặp, cấu trúc đề thi, công thức chuyển động/năng suất (đã ở Nhắc lại). Không dùng ";".
4. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 10 phút — nhắc lại phân tích mẫu, quy đồng, công thức nghiệm, đổi phút ra giờ, đọc đề đích, chỉ ra phương trình lập được có ẩn ở mẫu, chưa giải.
   concept: 10 phút — mục 2 và mục 3 là trọng tâm, cho học sinh đọc to từng bước, nhấn bước đối chiếu điều kiện ở cuối cả hai quy trình.
   practice1: khoảng 35 phút — Bài 1 hỏi nhanh cả lớp. Ví dụ 1, Ví dụ 2 giáo viên làm cùng lớp, học sinh điền ô, nhấn bước loại nghiệm không thỏa mãn ĐKXĐ. Bài 2, Bài 3 câu hỏi dẫn trả lời miệng, ý cuối tự trình bày vào vở.
   practice2: khoảng 110 phút — mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm bài ngay sau. Ví dụ 3 làm chậm, đủ đoạn phân tích, giáo viên kẻ bảng đại lượng trên bảng (các đại lượng, dự định, thực tế) cho các bài năng suất, chuyển động. Bài 10, Bài 11 ý cuối học sinh tự làm như đi thi, không gợi ý thêm. Bài 11 (đề đích) làm cá nhân rồi gọi lên bảng.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 12--21 in thành phiếu riêng. Buổi sau chữa Bài 20, Bài 21 trước.
'''

PROMPT_LOP = CHUNG + LUAT_LOI_GIAI + LUAT_VI_DU + r'''
## Việc B: lời giải các bài và ví dụ của 2 chặng LUYỆN TẬP trên lớp
Được giao ảnh SGK sgk9t1-tr29.png (cách giải 4 bước, Ví dụ 4 SGK làm mẫu trình bày), sgk9t2-tr25.png, sgk9t2-tr26.png (Bài 21, Ví dụ 1, Ví dụ 2 — làm mẫu trình bày lập phương trình). Theo nhịp trình bày SGK.
Đầu ra {"sua":[…mọi Ví dụ và Bài theo đúng thứ tự sơ đồ…],"ghi_chu":"…"}. Không trả tiêu đề mạch.

## Sơ đồ (đúng thứ tự)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + LUAT_LOI_GIAI + r'''
## Việc C: lời giải BÀI TẬP VỀ NHÀ (Bài 12–21)
Đầu ra {"sua":[10 bài theo đúng thứ tự],"ghi_chu":"…"}. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở.
- Bài 14: ẩn là $t$ (giây), không đổi sang $x$. Giá trị $t=0$ là thời điểm bắt đầu phóng (không phải lúc rơi trở lại).
- Bài 15: phương trình có $x$ ở mẫu ($\dfrac{360}{x}$) — nhân hai vế với $x$ ($x>0$) rồi thu gọn.

## Sơ đồ (đúng thứ tự)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", ANH_LT),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/sua-bai-phieu.json", ANH_LOP),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/sua-bai-phieu.json", [])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p4-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
