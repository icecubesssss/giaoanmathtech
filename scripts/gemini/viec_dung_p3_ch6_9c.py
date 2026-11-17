#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 3 ch.VI 9C bản 2 (17/11/2026) — 3 việc: lý thuyết, trên lớp, BTVN + làm thêm.

Sơ đồ (ĐỀ nguyên văn, thẻ, dang_id, đáp số SymPy) do Claude chốt ở so_do_p3_ch6_9c.py. Gemini chỉ viết LỜI GIẢI,
ví dụ điền khuyết và phần lý thuyết. Luật đợt 2–3 của Phiếu 2 (bỏ Do đó/Suy ra, "Theo câu …", Vậy là ô, trả lời
đúng cái được hỏi) đưa thẳng vào prompt đợt 1.

    .venv/bin/python scripts/gemini/viec_dung_p3_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (dung-p3-ch6-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p3_ch6_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p3_ch6_9c import KHOI  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
        "phieu-3-viete-bieu-thuc-khong-doi-xung.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p3-ch6-9c-lt", "dung-p3-ch6-9c-lop", "dung-p3-ch6-9c-btvn"
ANH = [f"storage/gemini/tep/p3-ch6-9c/{f}.png" for f in ("sgk9t2-tr21", "sgk9t1-tr47")]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = next(k[8] for k in KHOI if k[0] == "Bài 11.").split("[[br]]")[0]

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, buổi 3: Bài 20 "Định lí Viète và ứng dụng" (tiếp), SGK Kết nối tri thức với cuộc sống, tập hai) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Buổi 180 phút. Nội dung: biểu thức KHÔNG ĐỐI XỨNG của hai nghiệm — (1) hệ thức bậc nhất giữa hai nghiệm ($x_1-2x_2=6$, $x_1=3x_2$…): kết hợp với $x_1+x_2$ thành hệ, giải ra $x_1$, $x_2$, thay vào tích tìm $m$; (2) hạ bậc: $x_1$ là nghiệm của $ax^2+bx+c=0$ nên $ax_1^2+bx_1+c=0$, thay $x_1^2$ (và $x_1^3$) bằng biểu thức bậc nhất của $x_1$ rồi đưa về tổng, tích; (3) biểu thức chứa căn, giá trị tuyệt đối của nghiệm: xét dấu hai nghiệm, dùng $\sqrt{A^2}=|A|$; (4) tìm $m$ theo hệ thức không đối xứng bằng hạ bậc. Buổi trước (Phiếu 2) học sinh đã học định lí Viète và biểu thức đối xứng ($x_1^2+x_2^2$, $(x_1-x_2)^2$, $x_1^3+x_2^3$, $\dfrac1{x_1}+\dfrac1{x_2}$…), tìm $m$ theo hệ thức đối xứng. KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao).

## Luật cứng (vi phạm bị trả lại)
- KHÔNG dùng $\Delta'$, $b'$. Chỉ $\Delta=b^2-4ac$. KHÔNG dấu $\Leftrightarrow$: mỗi phép biến đổi xuống một dòng.
- KHÔNG dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX và tọa độ điểm viết "$(1;\,2)$"). Tổng, tích viết "$x_1+x_2=7$ và $x_1x_2=5$". Nghiệm của hệ viết "$x_1=1$, $x_2=2$".
- CẤM chữ: "khuôn", "dạng đề", "Câu III", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy", "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Viết "Viète". Lời giải theo NHỊP BÀI THI giống SGK: mỗi bước một dòng; dòng con mở đầu "[[br]]\hspace*{1.4em}" ("\hspace*" chỉ đứng ĐẦU dòng); nối bằng "nên" trong cùng câu, hoặc mở dòng bằng "Ta có …", "Khi đó …", "Thay vào, ta được …", "Theo câu …". Dòng "Vậy …" riêng ở cuối mỗi bài, mỗi ý cuối.
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy $0{,}5$. Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong GHI CHÚ của sơ đồ đã được máy kiểm (SymPy) — dùng ĐÚNG. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Chữ trong ghi chú (như "chỉ đề", "BÀI ĐÍCH", "7–9 ô") là cho người soạn, KHÔNG in.
'''

LUAT_LOI_GIAI = r'''
## Luật lời giải của BÀI (đề đã chốt — chép NGUYÊN "statement" như sơ đồ, không đổi một chữ)
- Mỗi ý trả lời ĐÚNG cái được hỏi, không thêm việc khác. "Tính $x_1+x_2$ và $x_1x_2$" ⇒ một dòng "Theo định lí Viète, ta có …" (thêm MỘT dòng điều kiện có nghiệm $a\cdot c<0$ hoặc $\Delta>0$ trước đó chỉ khi đề KHÔNG cho sẵn "có hai nghiệm" và không có ý nào khác lo điều kiện). "Tính $\Delta$ theo $m$" ⇒ chỉ tính, rút gọn (có thể viết dạng bình phương). "Viết … theo …" ⇒ một chuỗi biến đổi. "Lập hệ" ⇒ viết hệ bằng \begin{cases}…\end{cases}, không giải.
- Ý cuối ([TH]/[VD]) làm nốt bài, mở đầu "Theo câu a) và b), …" (hoặc câu tương ứng), KHÔNG chép lại các dòng của ý trước. Việc ý trước chưa làm thì ý cuối làm đủ: điều kiện có nghiệm theo $m$ (giải ra điều kiện), giải hệ, thay vào tích, giải phương trình ẩn $m$, đối chiếu điều kiện, kết "Vậy …".
- Bài không có ý a), b) (một câu): lời giải đủ các bước như bài thi.
- Bài làm thêm (Bài 22–24) không có thẻ mức: lời giải bình thường theo ý a), b).
- Đầu ra mỗi bài: {"label":"Bài N.","statement":<chép nguyên đề sơ đồ>,"solution":"a) …[[br]]\hspace*{1.4em}…[[br]]b) …"}.
'''

LUAT_VI_DU = r'''
## Luật VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết)
- Đầu ra: {"label":"Ví dụ N.","statement":"\\textbf{Ví dụ N.} <ĐỀ như sơ đồ, giữ nguồn>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …","solution":""}. Ví dụ nhiều ý: lời giải "a) …" rồi các dòng con, "[[br]]b) …".
- Đi đúng các bước trong ghi chú, mỗi bước một dòng.
- Khoét NHIỀU ô [[fill:đáp án]] ở chỗ giáo viên hỏi lớp: ví dụ một ý 7–9 ô, ví dụ nhiều ý 3–4 ô mỗi ý (giá trị $\Delta$ / tích $a\cdot c$, dấu so sánh, tổng, tích, $x_1^2$ viết theo $x_1$, hệ phương trình, giá trị $x_1$, $x_2$, kết quả, điều kiện của $m$).
- Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$\Delta=[[fill:29]]>0$", "$m\ne[[fill:2]]$"). Ô ngoài $…$ chứa công thức mới bọc $ bên trong.
- Một số đã nằm trong ô thì KHÔNG in sẵn (ngoài ô) ở bất kì dòng nào phía DƯỚI ô đó trong cùng ví dụ (dòng "Theo định lí Viète" có thể in sẵn tổng, tích nếu ô hỏi ở dòng sau thì khoét mọi lần xuất hiện). Kiểm tra lại từng ví dụ trước khi trả.
- Mỗi ý kết bằng dòng riêng "Vậy …" và giá trị kết luận là ô (vd "Vậy $m=[[fill:0]]$.").
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
Được giao ảnh SGK: sgk9t2-tr21.png (tập hai tr.21, định lí Viète), sgk9t1-tr47.png (tập một tr.47, hằng đẳng thức $\sqrt{A^2}=|A|$ và Ví dụ 5). ĐỌC ẢNH để chép đúng chữ SGK.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}. ("mindmap" trả {} — người lắp tự dựng.)

1. "opener_text" (chặng Khám phá, 4–6 dòng nối bằng [[br]]): chép đề đích (Bài 11 cuối Luyện tập 2, đề tuyển sinh lớp 10 THPT Hà Nội 2026--2027) trong \emph{\textquotedblleft…\textquotedblright}, rồi nêu: biểu thức $Q$ không đối xứng (đổi chỗ $x_1$, $x_2$ thì $Q$ thay đổi), nên chưa viết ngay được theo tổng và tích như Phiếu 2. Cần một cách mới: dùng $x_2$ là nghiệm để thay $3x_2-1$ bằng $x_2^2$ (hạ bậc, đổi biểu thức), rồi quy đồng về tổng và tích. Kết: đó là nội dung buổi học, đề này là Bài 11. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (khối Nhắc lại — chỉ kiến thức ĐÃ HỌC), mỗi mục một dòng "$\bullet$\; …" nối [[br]]:
   giải hệ hai phương trình bậc nhất hai ẩn bằng phương pháp thế hoặc cộng đại số (Chương I) · định lí Viète $x_1+x_2=-\dfrac ba$, $x_1x_2=\dfrac ca$ và điều kiện có nghiệm $\Delta\ge0$ (hoặc $a\cdot c<0$ thì có hai nghiệm phân biệt) (Phiếu 1, Phiếu 2) · các biểu thức đối xứng $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2$, $x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)$, $\dfrac1{x_1}+\dfrac1{x_2}=\dfrac{x_1+x_2}{x_1x_2}$ (Phiếu 2) · giá trị tuyệt đối: $|A|=A$ khi $A\ge0$, $|A|=-A$ khi $A<0$ (Toán 7).
3. "concept_blocks" (chặng Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT, mỗi mục là hai khối: {"type":"para","variant":"heading","text":"N. Tên"} rồi {"type":"para","text":"<nội dung>"}; cuối nội dung ghi nguồn trong \textit{(…)}. 4 mục:
   1. Nghiệm của phương trình bậc hai — nếu $x_1$ là nghiệm của phương trình $ax^2+bx+c=0$ ($a\ne0$) thì thay $x=x_1$ vào phương trình ta được đẳng thức đúng $ax_1^2+bx_1+c=0$, nên $ax_1^2=-bx_1-c$. Một dòng ví dụ ĐÚNG phương trình này (không đổi): $x_1$ là nghiệm của $x^2-5x+2=0$ thì $x_1^2=5x_1-2$. \textit{(định nghĩa nghiệm của phương trình)}
   2. Định lí Viète — chép khung SGK tr.21, kèm câu: định lí dùng khi phương trình có nghiệm. \textit{(SGK Toán 9 tập hai, tr.21)}
   3. Dấu của hai nghiệm (hệ quả của định lí Viète, mỗi ý một dòng [[br]], có câu giải thích ngắn từ $x_1x_2=\dfrac ca$, $x_1+x_2=-\dfrac ba$): $a\cdot c<0$ thì hai nghiệm trái dấu · $x_1x_2>0$ và $x_1+x_2<0$ thì hai nghiệm cùng âm · $x_1x_2>0$ và $x_1+x_2>0$ thì hai nghiệm cùng dương. \textit{(hệ quả của định lí Viète)}
   4. Hằng đẳng thức $\sqrt{A^2}=|A|$ — chép khung SGK tập một tr.47 (với $A$ là một biểu thức, $\sqrt{A^2}=|A|$), thêm dòng $|A|=A$ khi $A\ge0$, $|A|=-A$ khi $A<0$. \textit{(SGK Toán 9 tập một, tr.47)}
   KHÔNG thêm mẹo, các bước làm bài, lỗi hay gặp, cấu trúc đề thi, KHÔNG gọi tên "hạ bậc" trong lý thuyết. Mỗi mục xuống dòng bằng [[br]] khi có nhiều ý, không dùng ";".
4. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 10 phút — nhắc lại giải hệ, Viète, biểu thức đối xứng, giá trị tuyệt đối, đọc đề đích, chỉ ra vì sao chưa viết được theo tổng và tích, chưa giải.
   concept: 15 phút — mục 1 là trọng tâm: cho học sinh tự viết $x_1^2$ theo $x_1$ với vài phương trình trên bảng; mục 4 dùng cho Mạch 4.
   practice1: khoảng 40 phút — Bài 1 gọi một học sinh lên bảng giải hệ. Ví dụ 1 giáo viên làm cùng lớp, học sinh điền ô, nhấn bốn bước: điều kiện, Viète, lập hệ, thay vào tích. Bài 2–4 câu hỏi dẫn trả lời miệng, ý cuối tự trình bày vào vở.
   practice2: khoảng 100 phút — mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm bài ngay sau. Mạch 3, Mạch 5 nhấn câu hỏi \textquotedblleft $x_1$ là nghiệm thì $x_1^2$ bằng gì\textquotedblright. Bài 10, Bài 11 ý cuối học sinh tự làm như đi thi, không gợi ý thêm. Bài 11 (đề đích) làm cá nhân rồi gọi lên bảng.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 12–21 in thành phiếu riêng, Bài 22–24 là bài làm thêm cho học sinh khá (không bắt buộc). Buổi sau chữa Bài 20, Bài 21 trước.
'''

PROMPT_LOP = CHUNG + LUAT_LOI_GIAI + LUAT_VI_DU + r'''
## Việc B: lời giải các bài và ví dụ của 2 chặng LUYỆN TẬP trên lớp
Đầu ra {"sua":[…mọi Ví dụ và Bài theo đúng thứ tự sơ đồ…],"ghi_chu":"…"}. Không trả tiêu đề mạch.
- Bài 3 dùng lại nghiệm của hệ ở Bài 1 (lời giải ý c) ghi "Theo Bài 1, hệ … có nghiệm $x_1=1$, $x_2=2$").
- Bài 4 ý d): phương trình ẩn $m$ $6m^2+31m+35=0$ gọi biệt thức là $\Delta_1$ để khỏi trùng $\Delta$ của phương trình ban đầu.

## Sơ đồ (đúng thứ tự)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + LUAT_LOI_GIAI + r'''
## Việc C: lời giải BÀI TẬP VỀ NHÀ (Bài 12–21) và BÀI LÀM THÊM (Bài 22–24)
Đầu ra {"sua":[13 bài theo đúng thứ tự],"ghi_chu":"…"}. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở.
- Bài 17: chữ $a$ trong đề là THAM SỐ, lời giải không gọi $a$ là hệ số của $x$.

## Sơ đồ (đúng thứ tự)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", ANH),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/sua-bai-phieu.json", []),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/sua-bai-phieu.json", [])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p3-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
