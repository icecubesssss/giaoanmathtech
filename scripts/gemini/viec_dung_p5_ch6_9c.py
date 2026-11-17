#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 5 ch.VI 9C bản 2 (17/11/2026) — 3 việc: mở đầu + ghi chú GV, trên lớp, BTVN.

Sơ đồ (ĐỀ nguyên văn, thẻ, dang_id, đáp số SymPy) do Claude chốt ở so_do_p5_ch6_9c.py. Gemini chỉ viết LỜI GIẢI,
ví dụ điền khuyết, mở đầu / nhắc lại / ghi chú giáo viên. Kiến thức cần nhớ = các khối lý thuyết đã qua cổng của
Phiếu 1, 2, 4 (lap_p5_ch6_9c.py chép lại, không giao viết).

    .venv/bin/python scripts/gemini/viec_dung_p5_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (dung-p5-ch6-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p5_ch6_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p5_ch6_9c import KHOI  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
        "phieu-5-luyen-tap-chung-bai-tap-cuoi-chuong-vi.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p5-ch6-9c-lt", "dung-p5-ch6-9c-lop", "dung-p5-ch6-9c-btvn"
ANH_LOP = ["storage/gemini/tep/p4-ch6-9c/sgk9t2-tr25.png", "storage/gemini/tep/p4-ch6-9c/sgk9t2-tr26.png"]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = next(k[8] for k in KHOI if k[0] == "Bài 10.").split("[[br]]")[0]

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI "Phương trình bậc hai một ẩn", buổi 5: LUYỆN TẬP CHUNG và bài tập cuối chương, SGK Kết nối tri thức với cuộc sống) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Học sinh đã học đủ chương ở 4 buổi trước: công thức nghiệm ($\Delta=b^2-4ac$), nhận xét $a$, $c$ trái dấu, định lí Viète, biểu thức đối xứng của hai nghiệm, tìm $m$ theo hệ thức, giải bài toán bằng cách lập phương trình. Buổi này ôn và luyện lại theo đề kiểm tra; cuối buổi (phần riêng, không thuộc phiếu này) có bài kiểm tra chương. KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao).

## Luật cứng (vi phạm bị trả lại)
- KHÔNG dùng $\Delta'$, $b'$. Chỉ $\Delta=b^2-4ac$. KHÔNG dấu $\Leftrightarrow$, $\Rightarrow$: mỗi phép biến đổi xuống một dòng.
- KHÔNG dấu chấm phẩy ";". Hai nghiệm viết "$x_1=80$, $x_2=-100$".
- CẤM chữ: "khuôn", "dạng đề", "Câu III", "Bài III", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy", "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy", "TMĐK", "(TM)", "(L)", "ĐKXĐ", "chứa ẩn ở mẫu". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Lời giải theo NHỊP BÀI THI giống SGK: mỗi bước một dòng; dòng con mở đầu "[[br]]\hspace*{1.4em}" ("\hspace*" chỉ đứng ĐẦU dòng); nối bằng "nên" trong cùng câu, hoặc mở dòng bằng "Ta có …", "Khi đó …", "Theo câu …", "Theo định lí Viète, …". Dòng "Vậy …" riêng ở cuối mỗi bài.
- Bài lập phương trình viết như SGK: "Gọi $x$ (km/h) là … Điều kiện: $x>0$." · "… là $\dfrac{90}{x}$ (giờ)." · "Theo đề bài, ta có phương trình $…$" · "Quy đồng mẫu hai vế rồi khử mẫu, ta được $…$" · "$\Delta=…$, $\sqrt\Delta=…$" · "Phương trình có hai nghiệm $x_1=…$, $x_2=…$." · "Giá trị $x_1=…$ thỏa mãn điều kiện, $x_2=…$ không thỏa mãn điều kiện." · "Vậy …" (trả lời đúng câu hỏi của đề, có đơn vị).
- Bài có tham số viết như SGK: "Ta có $\Delta=…$" · "Phương trình có hai nghiệm phân biệt khi $\Delta>0$, tức là …" · "Theo định lí Viète, ta có $x_1+x_2=…$, $x_1x_2=…$." · đối chiếu điều kiện của $m$ ở cuối.
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy $0{,}09$, số lớn $1\,100$, phần trăm "$9\%$". Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong GHI CHÚ của sơ đồ đã được máy kiểm (SymPy) — dùng ĐÚNG. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Chữ trong ghi chú (như "chỉ đề", "BÀI ĐÍCH", "7–9 ô", "MỘT bước", "ĐỌC ẢNH", "KHÔNG ghi vào lời giải") là cho người soạn, KHÔNG in.
'''

LUAT_LOI_GIAI = r'''
## Luật lời giải của BÀI (đề đã chốt — chép NGUYÊN "statement" như sơ đồ, không đổi một chữ)
- Mỗi ý trả lời ĐÚNG cái được hỏi, không thêm việc khác: "Viết … theo $x$" ⇒ một dòng biểu thức kèm đơn vị. "Đổi … ra giờ" ⇒ một dòng. "Tính $\Delta$" ⇒ một dòng. "Viết $x_1+x_2$ và $x_1x_2$" ⇒ một dòng Viète. "Tính tích $ac$ rồi kết luận" ⇒ một hai dòng.
- Ý cuối ([TH]/[VD]) làm nốt bài, mở đầu "Theo câu …, …" khi dùng kết quả ý trước, KHÔNG chép lại các dòng của ý trước. Ý cuối làm đủ: lập phương trình, khử mẫu, thu gọn về $ax^2+bx+c=0$, tính $\Delta$, hai nghiệm, đối chiếu điều kiện, dòng "Vậy …".
- Trắc nghiệm (Bài 2, 3, 6, 7, 8): solution 1–2 dòng, kết "Chọn …".
- Đầu ra mỗi bài: {"label":"Bài N.","statement":<chép nguyên đề sơ đồ>,"solution":"a) …[[br]]b) …[[br]]d) Theo câu …[[br]]\hspace*{1.4em}…"}.
'''

LUAT_VI_DU = r'''
## Luật VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết)
- Đầu ra: {"label":"Ví dụ N.","statement":"\\textbf{Ví dụ N.} <ĐỀ như sơ đồ, giữ nguồn>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …","solution":""}.
- Ví dụ lập phương trình (Ví dụ 2, 3, 4): đi theo 3 bước SGK, mỗi bước mở đầu "\textit{Bước 1.}", "\textit{Bước 2.}", "\textit{Bước 3.}" (Bước 1 nhiều dòng: chọn ẩn + điều kiện, mỗi đại lượng biểu diễn theo ẩn một dòng, dòng phương trình).
- Ví dụ 5 có hai ý: viết "a) …" rồi "b) …" mỗi ý bắt đầu dòng mới, mỗi ý 3–4 ô.
- Đi đúng các bước trong ghi chú, mỗi bước một dòng.
- Khoét 7–9 ô [[fill:đáp án]] ở chỗ giáo viên hỏi lớp: hệ số, $\Delta$, dấu so sánh với $0$, tổng và tích theo Viète, biểu thức đổi theo tổng tích, điều kiện của ẩn / của $m$, đại lượng biểu diễn theo ẩn, phương trình lập được, nghiệm, nghiệm bị loại, kết luận.
- Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$\Delta=[[fill:13]]$", "$x_1+x_2=[[fill:\dfrac53]]$"). Ô ngoài $…$ chứa công thức thì viết "$[[fill:x+20]]$" (dấu $ bọc NGOÀI ô, không bao giờ "[[fill:$…$]]"). Ô kết thúc bằng đúng hai dấu "]]" (KHÔNG BAO GIỜ ba dấu "]]]" — ô chứa ngoặc vuông thì đổi sang ngoặc tròn).
- Một số đã nằm trong ô thì KHÔNG in sẵn (ngoài ô) ở bất kì dòng nào phía DƯỚI ô đó trong cùng ví dụ (nếu cần nhắc lại thì khoét lần nữa hoặc viết "giá trị trên"). Kiểm tra lại từng ví dụ trước khi trả.
- Kết bằng dòng riêng "Vậy …" và giá trị kết luận là ô (vd "Vậy $M=[[fill:\dfrac19]]$.").
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
## Việc A: phần mở đầu, nhắc lại, ghi chú giáo viên
Đầu ra JSON: {"opener_text","review_note","concept_blocks":[],"mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}. ("concept_blocks" trả [] và "mindmap" trả {} — người lắp tự dựng.)

1. "opener_text" (chặng Khám phá, 4–6 dòng nối bằng [[br]]): chép đề đích (Bài 10 cuối Luyện tập 2, đề kiểm tra học kì II Phòng GD\&ĐT Hà Đông 2024--2025) trong \emph{\textquotedblleft…\textquotedblright}, rồi nêu: bài có hai việc — chứng tỏ phương trình luôn có hai nghiệm phân biệt (nhìn dấu của $ac$), rồi tìm $m$ từ một hệ thức giữa hai nghiệm (đưa hệ thức về tổng và tích, dùng định lí Viète). Buổi luyện tập đi lại các kĩ năng của cả chương theo thứ tự: giải phương trình và định lí Viète (Luyện tập 1), giải bài toán bằng cách lập phương trình rồi tìm $m$ theo hệ thức (Luyện tập 2). Kết: đề này là Bài 10. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (khối Nhắc lại — chỉ kiến thức ĐÃ HỌC ở lớp dưới mà các bài của buổi dùng), mỗi mục một dòng "$\bullet$\; …" nối [[br]]:
   hằng đẳng thức $(a+b)^2=a^2+2ab+b^2$, $(a-b)^2=a^2-2ab+b^2$ (Toán 8) · quy đồng mẫu hai phân thức $\dfrac{1}{A}+\dfrac{1}{B}=\dfrac{A+B}{AB}$ (Toán 8) · đổi phút ra giờ: $1$ phút $=\dfrac1{60}$ giờ (Toán 5) · gửi $a$ đồng với lãi suất $x$ một kì (viết dưới dạng số thập phân) thì sau một kì nhận được $a+a\cdot x=a(1+x)$ đồng cả vốn lẫn lãi (Toán 7, tỉ số phần trăm).
3. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 5 phút — đọc đề đích, chỉ ra hai việc của bài, chưa giải. Nhắc nhanh các mục Nhắc lại.
   concept: 5 phút — học sinh đọc to bảng kiến thức của chương, giáo viên hỏi nhanh: khi nào phương trình có hai nghiệm phân biệt, định lí Viète dùng khi nào, ba bước giải bài toán bằng cách lập phương trình.
   practice1: khoảng 30 phút — Bài 1, 2, 3 hỏi nhanh cả lớp. Ví dụ 1 giáo viên làm cùng lớp, học sinh điền ô. Bài 4, Bài 5 câu hỏi dẫn trả lời miệng, ý cuối tự trình bày vào vở.
   practice2: khoảng 50 phút — mỗi ví dụ giáo viên làm cùng lớp rồi học sinh làm ngay bài sau. Bài 6, 7, 8 trắc nghiệm hỏi nhanh. Bài 9 kẻ bảng hai sổ tiết kiệm (số tiền gửi, thời gian gửi, số tiền nhận). Bài 10 (đề đích) ý c) học sinh tự làm như đi thi, không gợi ý thêm, gọi lên bảng chữa.
   reflection: sơ đồ tư duy 5 phút trước giờ kiểm tra. Bài tập về nhà Bài 11--20 in thành phiếu riêng. Buổi sau chữa Bài 19, Bài 20 trước.
'''

PROMPT_LOP = CHUNG + LUAT_LOI_GIAI + LUAT_VI_DU + r'''
## Việc B: lời giải các bài và ví dụ của 2 chặng LUYỆN TẬP trên lớp
Được giao ảnh SGK sgk9t2-tr25.png, sgk9t2-tr26.png (tập hai tr.25–26, Bài 21: tình huống mở đầu bác Lan gửi tiết kiệm, HĐ1–HĐ3, các bước giải bài toán bằng cách lập phương trình, Ví dụ 1, 2) — ĐỌC ẢNH để Ví dụ 4 trình bày đúng như SGK (HĐ1: sau kì thứ nhất $100+100x=100(1+x)$, HĐ2: sau kì thứ hai $100(1+x)^2$, HĐ3: phương trình $100(1+x)^2=118{,}81$).
Đầu ra {"sua":[…mọi Ví dụ và Bài theo đúng thứ tự sơ đồ…],"ghi_chu":"…"}. Không trả tiêu đề mạch.

## Sơ đồ (đúng thứ tự)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + LUAT_LOI_GIAI + r'''
## Việc C: lời giải BÀI TẬP VỀ NHÀ (Bài 11–20)
Đầu ra {"sua":[10 bài theo đúng thứ tự],"ghi_chu":"…"}. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở.
- Bài 12: chữ $a$ trong đề là tham số, KHÔNG gọi hệ số là $a$, $b$, $c$ trong lời giải; tổng hai nghiệm tính trực tiếp từ phương trình $2x^2-2x+2-a=0$ ($x_1+x_2=\dfrac{2}{2}=1$). Không cần tìm giá trị của tham số.
- Bài 13: chữ $a$ trong đề cũng là tham số, chỉ dùng tích $x_1x_2=3$.

## Sơ đồ (đúng thứ tự)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", []),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/sua-bai-phieu.json", ANH_LOP),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/sua-bai-phieu.json", [])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p5-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
