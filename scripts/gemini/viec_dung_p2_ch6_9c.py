#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 2 ch.VI 9C bản 2 (16/11/2026) — 3 việc: lý thuyết, trên lớp, BTVN.

Sơ đồ (đề, thẻ, dang_id, đáp số SymPy) do Claude chốt ở so_do_p2_ch6_9c.py. Gemini chỉ viết chữ.

    .venv/bin/python scripts/gemini/viec_dung_p2_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (hoặc --mot dung-p2-ch6-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p2_ch6_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p2_ch6_9c import KHOI  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
        "phieu-2-dinh-li-viete-bieu-thuc-doi-xung.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p2-ch6-9c-lt", "dung-p2-ch6-9c-lop", "dung-p2-ch6-9c-btvn"
ANH = [f"storage/gemini/tep/p2-ch6-9c/sgk9t2-tr{p}.png" for p in (20, 21, 22, 23, 24, 28)]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = (r"Cho phương trình $x^2+mx-6=0$. a) Chứng minh rằng phương trình luôn có hai nghiệm phân biệt "
           r"$x_1$, $x_2$ với mọi giá trị của $m$. b) Tìm giá trị của $m$ để phương trình có hai nghiệm $x_1$, $x_2$ "
           r"thỏa mãn $x_1^2+x_2^2-x_1x_2=22$.")

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, buổi 2: Bài 20 "Định lí Viète và ứng dụng", SGK Kết nối tri thức với cuộc sống, tập hai) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Buổi 180 phút. Nội dung: định lí Viète (tổng, tích hai nghiệm), điều kiện có nghiệm trước khi dùng Viète, biết một nghiệm tìm nghiệm còn lại, hai nghiệm trái dấu, tính biểu thức ĐỐI XỨNG của hai nghiệm ($x_1^2+x_2^2$, $(x_1-x_2)^2$, $x_1^3+x_2^3$, $\dfrac1{x_1}+\dfrac1{x_2}$, $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$, $\dfrac1{x_1+k}+\dfrac1{x_2+k}$…), tìm $m$ để hai nghiệm thỏa hệ thức đối xứng. Buổi trước (Phiếu 1) học sinh đã học công thức nghiệm, $\Delta$, tìm $m$ theo số nghiệm, "$a$, $c$ trái dấu thì có hai nghiệm phân biệt". KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao).

## Luật cứng (vi phạm bị trả lại)
- KHÔNG dùng công thức nghiệm thu gọn $\Delta'$, $b'$ (đã bỏ khỏi chương). Chỉ $\Delta=b^2-4ac$. Đề SGK có chữ "(hoặc $\Delta'$)" thì bỏ chữ đó.
- KHÔNG dùng dấu $\Leftrightarrow$ ở bất kì đâu: mỗi phép biến đổi xuống một dòng.
- KHÔNG dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX). Tổng, tích viết "$x_1+x_2=7$ và $x_1x_2=5$" hoặc hai dòng.
- CẤM chữ/ý: "khuôn", "dạng đề", "Câu III", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Viết "Viète" (có dấu huyền trên e). Đầu lời giải dùng Viète luôn có MỘT dòng điều kiện có nghiệm: "Ta có $\Delta=…>0$ nên phương trình có hai nghiệm phân biệt $x_1$, $x_2$." hoặc "Vì $a\cdot c=1\cdot(-6)=-6<0$ nên phương trình có hai nghiệm phân biệt $x_1$, $x_2$." rồi dòng "Theo định lí Viète, ta có $x_1+x_2=…$ và $x_1x_2=…$."
- Lời giải theo NHỊP BÀI THI giống SGK: mỗi bước một dòng; dòng con trong lời giải mở đầu "[[br]]\hspace*{1.4em}". Mẫu:
  "Ta có $\Delta=(-7)^2-4\cdot 1\cdot 5=29>0$ nên phương trình có hai nghiệm phân biệt $x_1$, $x_2$.[[br]]\hspace*{1.4em}Theo định lí Viète, ta có $x_1+x_2=7$ và $x_1x_2=5$.[[br]]\hspace*{1.4em}Do đó $A=x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=7^2-2\cdot 5=39$.[[br]]\hspace*{1.4em}Vậy $A=39$."
  Tìm $m$: dòng điều kiện $\Delta$ theo $m$ → dòng Viète theo $m$ → dòng biến đổi hệ thức → dòng giải $m$ → dòng đối chiếu điều kiện → dòng "Vậy $m=…$". Dòng "Vậy" riêng ở cuối.
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy viết $0{,}5$. Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong SƠ ĐỒ đã được máy kiểm (SymPy) — dùng ĐÚNG, không đổi phương trình. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Các chữ trong ngoặc ở sơ đồ (đáp số, lời dặn như "CHỈ ĐỀ", "ý a của đề", "LƯU Ý") là cho người soạn, KHÔNG in vào đề.
'''

KHUON_KHOI = r'''
## Khuôn khối JSON
- Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. …"} (chữ tiêu đề lấy đúng sơ đồ).
- VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết): {"type":"noted","variant":"example","text":"\\textbf{Ví dụ N.} <đề>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …"}
  Ví dụ nhiều ý: đề "a) …[[br]]b) …", lời giải "a) …" rồi các dòng con, "b) …". Ví dụ là bản trình bày mẫu để giáo viên định hướng: khoét NHIỀU ô [[fill:đáp án]] — ví dụ một ý 7–9 ô, ví dụ nhiều ý 3–4 ô mỗi ý — rơi vào chỗ giáo viên hỏi lớp: giá trị $\Delta$ hoặc tích $a\cdot c$, dấu so sánh với $0$, giá trị tổng, giá trị tích, công thức biến đổi (vd "$(x_1+x_2)^2-[[fill:2x_1x_2]]$"), kết quả, điều kiện của $m$, cụm kết luận. Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$\Delta=[[fill:29]]>0$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong (vd "[[fill:$m\\ne-1$]]"). Không để số trong ô lại in sẵn ở dòng ngay sau (lộ đáp án). Ví dụ lấy từ đề thi thì ghi nguồn sau đề: " \\textit{(<nguồn>)}" (ví dụ gộp: nguồn ghi nhỏ sau ý tương ứng).
- BÀI NB trả lời ngắn: {"type":"problem","label":"Bài N.","level":1,"tier":…,"dang_id":…,"statement":"<một câu yêu cầu chung>[[br]]a) [NB] …[[br]]b) [NB] …","solution":"a) …[[br]]b) …","hints":[]}. Bài một câu: "statement":"[NB] <câu hỏi>". Không chỗ chấm, không ô điền, không khung "hoàn thành bài giải".
- BÀI NB trắc nghiệm: thêm "options":["…","…","…","…"] (4 phương án theo thứ tự A–D, KHÔNG ghi chữ A. B. trong chuỗi); "statement":"[NB] <câu hỏi>"; "solution":"Chọn A. <lí do một dòng>".
- BÀI NB Đúng/Sai: "dung_sai":["<khẳng định>"]; "statement":"[NB] Khẳng định sau đúng hay sai? Vì sao?"; "solution":"Sai. <lí do>".
- BÀI TH (hình thức th_dan, tự trình bày vào vở): {"type":"problem","label":"Bài N.","level":2,"tier":…,"dang_id":…,"statement":"<đề gọn> \\textit{(<nguồn>)}[[br]]a) [NB] <câu hỏi dẫn ngắn>[[br]]b) [TH] <yêu cầu chính>","solution":"a) <trả lời>[[br]]b) <lời giải đủ theo nhịp bài thi>","hints":[]}
  Câu hỏi dẫn [NB] là CÂU HỎI (nhắc công thức, điều kiện, bước làm đầu tiên), không phải chỗ chấm. Ý [TH] là yêu cầu của đề gốc. Đề gốc chép trung thành (yêu cầu của đề gốc chuyển vào ý [TH], phần "Cho phương trình …" giữ ở đầu).
- BÀI VD (hình thức vd_de): như bài TH nhưng "level":3 và ý cuối là "[VD] <yêu cầu của đề gốc, chép nguyên văn>". Ý [VD] CHỈ LÀ ĐỀ: không gợi ý, không "Hướng dẫn", không "Gợi ý", "hints":[]. Các ý [NB] đứng trước là câu nhỏ như sơ đồ. Lời giải ý [VD] đầy đủ nhịp bài thi (điều kiện → Viète → biến đổi → giải → đối chiếu → Vậy).
- Mọi bài có "dang_id", "level", "tier" ĐÚNG như sơ đồ.
'''


def so_do(chang):
    dong = []
    for k in KHOI:
        if k[1] not in chang:
            continue
        if len(k) == 3:
            dong.append(f"- [TIÊU ĐỀ MẠCH] {k[0]}")
            continue
        nhan, _, tier, dang, level, ma, nguon, ht, noi = k
        dau = f"- {nhan} vai={'Ví dụ' if ht == 'vi_du' else 'Bài'}"
        if ht != "vi_du":
            dau += f" tier={tier} dang_id={dang} level={level}"
        dau += f" hình thức={ht} mã={ma}" + (f" nguồn in=\"{nguon}\"" if nguon else "")
        dong.append(dau + "\n    " + noi)
    return "\n".join(dong)


PROMPT_LT = CHUNG + r'''
## Việc A: phần mở đầu, nhắc lại, kiến thức cần nhớ, ghi chú giáo viên
Được giao ảnh các trang SGK Toán 9 tập hai: sgk9t2-tr20.png … tr24.png (Bài 20 Định lí Viète), tr28.png (Luyện tập chung, Ví dụ 1). Tên file = số trang IN. ĐỌC ẢNH để chép đúng chữ SGK.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}. ("mindmap" trả {} — người lắp tự dựng.)

1. "opener_text" (chặng Khám phá, 4–6 dòng nối bằng [[br]]): chép đề đích (Bài 19 cuối Luyện tập 2, đề kiểm tra học kì II THCS\&THPT M.V. Lômônôxốp 2024--2025) trong \emph{\textquotedblleft…\textquotedblright}, rồi nêu: ý a) cần nhận ra $a$, $c$ trái dấu (đã học ở Phiếu 1), ý b) cần viết $x_1+x_2$, $x_1x_2$ theo $m$ bằng định lí Viète rồi đưa $x_1^2+x_2^2-x_1x_2$ về tổng và tích. Kết: đó là nội dung buổi học, đề này là Bài 19. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (khối Nhắc lại — chỉ kiến thức ĐÃ HỌC, dùng trong buổi này), mỗi mục một dòng "$\bullet$\; …" nối [[br]]:
   hằng đẳng thức $(A+B)^2=A^2+2AB+B^2$, $(A-B)^2=A^2-2AB+B^2$, $(A+B)^3=A^3+3A^2B+3AB^2+B^3$ (Toán 8) · quy đồng mẫu hai phân thức: $\dfrac{A}{B}+\dfrac{C}{D}=\dfrac{AD+BC}{BD}$ (Toán 8) · công thức $\Delta=b^2-4ac$ và: $\Delta>0$ thì phương trình có hai nghiệm phân biệt, $\Delta\ge 0$ thì có nghiệm, $a$ và $c$ trái dấu thì có hai nghiệm phân biệt (Phiếu 1, Bài 19).
3. "concept_blocks" (chặng Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT, mỗi mục là hai khối: {"type":"para","variant":"heading","text":"N. Tên"} rồi {"type":"para","text":"<nội dung>"}; cuối nội dung ghi nguồn trong \textit{(…)}. 4 mục:
   1. Định lí Viète — chép khung SGK tr.21 (Nếu $x_1$, $x_2$ là hai nghiệm của phương trình $ax^2+bx+c=0$ ($a\ne0$) thì $x_1+x_2=-\dfrac ba$ và $x_1x_2=\dfrac ca$). Thêm một câu: định lí chỉ dùng khi phương trình có nghiệm, nên trước hết tính $\Delta$ để kiểm tra điều kiện có nghiệm (như SGK Ví dụ 1 tr.21). \textit{(SGK Toán 9 tập hai, tr.21)}
   2. Biết một nghiệm, tìm nghiệm còn lại — theo SGK Ví dụ 3 tr.23: biết $x_1$ thì $x_2=\dfrac{c}{a\,x_1}$ (từ tích, khi $x_1\ne0$) hoặc $x_2=-\dfrac ba-x_1$ (từ tổng). \textit{(SGK Toán 9 tập hai, tr.23)}
   3. Hai nghiệm trái dấu: nếu $a$ và $c$ trái dấu thì $ac<0$, phương trình có hai nghiệm phân biệt và $x_1x_2=\dfrac ca<0$, nên hai nghiệm trái dấu. \textit{(suy ra từ định lí Viète)}
   4. Biểu thức đối xứng của hai nghiệm viết theo tổng và tích (mỗi công thức một dòng [[br]], viết đủ bước biến đổi từ hằng đẳng thức):
      $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2$ \textit{(SGK tr.28, Ví dụ 1)}
      $(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2$
      $x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)$
      $\dfrac1{x_1}+\dfrac1{x_2}=\dfrac{x_1+x_2}{x_1x_2}$ (với $x_1x_2\ne0$)
      $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}=\dfrac{x_1^2+x_2^2}{x_1x_2}$ (với $x_1x_2\ne0$)
      Kết mục: \textit{(biến đổi bằng hằng đẳng thức đáng nhớ, Toán 8)}.
   KHÔNG đưa phần tìm hai số khi biết tổng và tích, KHÔNG nhẩm nghiệm (đã học ở Phiếu 1), KHÔNG $\Delta'$. KHÔNG thêm mẹo, các bước làm bài, lỗi hay gặp, cấu trúc đề thi. Mỗi mục xuống dòng bằng [[br]] khi có nhiều ý, không dùng ";".
4. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số/"khuôn"):
   review: 10 phút — nhắc lại hằng đẳng thức, quy đồng mẫu, điều kiện có nghiệm, đọc đề đích, chưa giải.
   concept: 20 phút — mục 1 và mục 4 là trọng tâm, cho học sinh tự viết lại $x_1^2+x_2^2$ theo tổng, tích ngay khi giảng.
   practice1: khoảng 20 phút — câu nhỏ Đúng/Sai, trắc nghiệm, trả lời ngắn, gọi nhiều học sinh trả lời miệng, chữa nhanh. Ví dụ 1 giáo viên làm cùng lớp, học sinh điền ô.
   practice2: khoảng 100 phút — mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm bài ngay sau, câu hỏi dẫn trả lời miệng, ý chính tự trình bày vào vở. Bài 18, Bài 19 ý cuối học sinh tự làm như đi thi, không gợi ý thêm. Bài 19 (đề đích) làm cá nhân rồi gọi lên bảng.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 20–33 in thành phiếu riêng. Buổi sau chữa Bài 32, Bài 33 trước.
'''

PROMPT_LOP = CHUNG + KHUON_KHOI + r'''
## Việc B: dựng 2 chặng LUYỆN TẬP trên lớp
Đầu ra JSON {"stages":[{"kind":"practice1","number":3,"title":"Luyện tập 1 — Nhận biết","teacher_note":"","blocks":[…]},{"kind":"practice2","number":4,"title":"Luyện tập 2 — Thông hiểu và vận dụng","teacher_note":"","blocks":[…]}],"ghi_chu":"…"}.
- Khối ĐẦU TIÊN của practice1: {"type":"para","text":"\\textbf{Đích của buổi học:} Bài 19 — đề kiểm tra học kì II THCS\\&THPT M.V. Lômônôxốp: chứng minh phương trình luôn có hai nghiệm phân biệt và tìm $m$ để hai nghiệm thỏa mãn một hệ thức. Mạch 1–3 chuẩn bị cho ý a) và cách viết tổng, tích, Mạch 4–8 chuẩn bị cho ý b)."}
- Sau đó các khối ĐÚNG THỨ TỰ sơ đồ dưới đây. Mục ghi "Đích + Mạch 4…" chỉ in tiêu đề "Mạch 4. Tổng các bình phương".
- Bài 14 dùng lại kết quả quy đồng của Bài 9 (lời giải được nhắc "theo Bài 9").
- Bài 16: tham số trong đề tên là $a$, trùng tên hệ số. Lời giải không gọi "$a$" là hệ số của $x^2$.

## Sơ đồ (đúng thứ tự khối)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + KHUON_KHOI + r'''
## Việc C: phần BÀI TẬP VỀ NHÀ (mọi bài "tier":"btvn", Bài 20. đến Bài 33.)
Không ví dụ, không tiêu đề mạch. Trả về {"stages":[{"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":"","blocks":[14 bài]}],"ghi_chu":"…"}.
Thứ tự: các bài NB (20–23), rồi các bài có ý [TH] (24–31), rồi các bài có ý [VD] (32, 33), đúng sơ đồ. Đề gọn: một câu yêu cầu chung + các ý. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở, không ghi điểm từng bài.

## Sơ đồ (đúng thứ tự khối)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", ANH),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/dung-chang-phieu.json", []),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/dung-chang-phieu.json", [])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p2-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
