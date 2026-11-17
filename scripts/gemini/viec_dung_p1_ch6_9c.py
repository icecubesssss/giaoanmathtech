#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 1 ch.VI 9C bản 2 (16/11/2026) — 3 việc: lý thuyết, trên lớp, BTVN.

Sơ đồ (đề, thẻ, dang_id, đáp số SymPy) do Claude chốt ở so_do_p1_ch6_9c.py. Gemini chỉ viết chữ.

    .venv/bin/python scripts/gemini/viec_dung_p1_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (hoặc --mot dung-p1-ch6-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p1_ch6_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch6_9c import KHOI  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
        "phieu-1-phuong-trinh-bac-hai-bien-luan-so-nghiem.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p1-ch6-9c-lt", "dung-p1-ch6-9c-lop", "dung-p1-ch6-9c-btvn"
ANH = [f"storage/gemini/tep/p1-ch6-9c/sgk9t2-tr{p}.png" for p in (10, 11, 12, 13, 14, 15, 16, 22, 23)]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = (r"Cho phương trình $x^2+2(m-3)x-2m+5=0$. a) Giải phương trình với $m=5$. "
           r"b) Chứng minh phương trình luôn có hai nghiệm với mọi $m$.")

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, buổi 1: Bài 19 "Phương trình bậc hai một ẩn", SGK Kết nối tri thức với cuộc sống, tập hai) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Buổi 180 phút. Nội dung: phương trình bậc hai, giải bằng công thức nghiệm, phương trình có tham số $m$: tìm $m$ theo số nghiệm, biết một nghiệm tìm $m$, chứng minh luôn có nghiệm. KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao).

## Luật cứng (vi phạm bị trả lại)
- KHÔNG dùng công thức nghiệm thu gọn $\Delta'$, $b'$ (đã bỏ khỏi chương). Chỉ $\Delta=b^2-4ac$.
- KHÔNG dùng dấu $\Leftrightarrow$ ở bất kì đâu (học sinh không dùng dấu tương đương): mỗi phép biến đổi xuống một dòng.
- KHÔNG dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX). Hai nghiệm viết "$x_1=…$ và $x_2=…$" hoặc "$x=0$ hoặc $x=2$".
- CẤM chữ/ý: "khuôn", "dạng đề", "Câu III", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Lời giải theo NHỊP BÀI THI giống SGK: mỗi bước một dòng; dòng con trong lời giải mở đầu "[[br]]\hspace*{1.4em}". Mẫu:
  "Ta có $\Delta=(-4)^2-4\cdot 3\cdot 5=16-60=-44<0$ nên phương trình vô nghiệm."
  "Ta có $\Delta=7^2-4\cdot 3\cdot(-1)=61>0$ nên phương trình có hai nghiệm phân biệt[[br]]\hspace*{1.4em}$x_1=\dfrac{-7+\sqrt{61}}{6}$ và $x_2=\dfrac{-7-\sqrt{61}}{6}$."
  "Vậy phương trình có hai nghiệm $x_1=…$ và $x_2=…$." (dòng "Vậy" riêng ở cuối).
  Tham số: "Ta có $\Delta=\left[-(2m-1)\right]^2-4\cdot1\cdot(m^2-1)=4m^2-4m+1-4m^2+4=-4m+5$." rồi "Phương trình có hai nghiệm phân biệt khi $\Delta>0$[[br]]\hspace*{1.4em}$-4m+5>0$[[br]]\hspace*{1.4em}$m<\dfrac54$." rồi "Vậy $m<\dfrac54$."
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy viết $0{,}5$. Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong SƠ ĐỒ đã được máy kiểm (SymPy) — dùng ĐÚNG, không đổi phương trình. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Các chữ trong ngoặc ở sơ đồ (đáp số, lời dặn) là cho người soạn, KHÔNG in vào đề.
'''

KHUON_KHOI = r'''
## Khuôn khối JSON
- Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. …"} (chữ tiêu đề lấy đúng sơ đồ).
- VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết): {"type":"noted","variant":"example","text":"\\textbf{Ví dụ N.} <đề>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …"}
  Khoét 3–5 ô [[fill:đáp án]] ở chỗ then chốt (hệ số, giá trị $\Delta$, so sánh với 0, nghiệm, điều kiện của $m$). Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$\Delta=[[fill:61]]>0$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong (vd "[[fill:$m<-\\dfrac73$]]"). Không để số trong ô lại in sẵn ở dòng sau (lộ đáp án). Ví dụ lấy từ đề thi thì ghi nguồn sau đề: " \\textit{(<nguồn>)}".
- BÀI NB trả lời ngắn: {"type":"problem","label":"Bài N.","level":1,"tier":…,"dang_id":…,"statement":"<một câu yêu cầu chung>[[br]]a) [NB] …[[br]]b) [NB] …","solution":"a) …[[br]]b) …","hints":[]}. Không chỗ chấm, không ô điền, không khung "hoàn thành bài giải".
- BÀI NB trắc nghiệm: thêm "options":["…","…","…","…"] (4 phương án theo thứ tự A–D, KHÔNG ghi chữ A. B. trong chuỗi); "statement":"[NB] <câu hỏi>"; "solution":"Chọn C. <lí do một dòng>".
- BÀI NB Đúng/Sai: "dung_sai":["<khẳng định>"]; "statement":"[NB] <câu dẫn, vd: Khẳng định sau đúng hay sai? Vì sao?>"; "solution":"Sai. <lí do>".
- BÀI TH (tự trình bày vào vở): {"type":"problem","label":"Bài N.","level":2,"tier":…,"dang_id":…,"statement":"<đề gọn> \\textit{(<nguồn>)}[[br]]a) [NB] <câu hỏi dẫn ngắn>[[br]]b) [TH] <yêu cầu chính>","solution":"a) <trả lời>[[br]]b) <lời giải đủ theo nhịp bài thi>","hints":[]}
  Câu hỏi dẫn [NB] là CÂU HỎI (nhắc công thức, điều kiện, bước làm đầu tiên), không phải chỗ chấm. Ý [TH] là yêu cầu của đề gốc. Đề gốc chép trung thành (được đổi "phương trình (1)" thành câu dẫn gọn), không thêm "biết phương trình có hai nghiệm" khi đề không có.
- Mọi bài có "dang_id" ĐÚNG như sơ đồ. "level": NB 1, bài có ý [TH] 2.
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
## Việc A: phần mở đầu, nhắc lại, kiến thức cần nhớ, sơ đồ tư duy, ghi chú giáo viên
Được giao ảnh các trang SGK Toán 9 tập hai: sgk9t2-tr10.png … tr16.png (Bài 19), tr22.png, tr23.png (Bài 20, phần nhẩm nghiệm). Tên file = số trang IN. ĐỌC ẢNH để chép đúng chữ SGK.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap","teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}.

1. "opener_text" (chặng Khám phá, 4–6 dòng nối bằng [[br]]): chép đề đích (Bài 19 cuối Luyện tập 2, đề giữa kì II THCS Nguyễn Trường Tộ 2025--2026) trong \emph{\textquotedblleft…\textquotedblright}, rồi nêu: ý a) cần giải phương trình bậc hai bằng công thức nghiệm, ý b) cần tính $\Delta$ theo $m$ và xét dấu. Kết: hai việc đó là nội dung buổi học, đề này là Bài 19. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (khối Nhắc lại — chỉ kiến thức ĐÃ HỌC ở lớp dưới, dùng trong buổi này), mỗi mục một dòng "$\bullet$\; …" nối [[br]]:
   hằng đẳng thức $(A+B)^2=A^2+2AB+B^2$, $(A-B)^2=A^2-2AB+B^2$, $A^2-B^2=(A-B)(A+B)$ (Toán 8) · chuyển một hạng tử từ vế này sang vế kia thì đổi dấu hạng tử đó · phương trình tích: $A\cdot B=0$ khi $A=0$ hoặc $B=0$ (Toán 9 tập một, Chương II) · $x^2=k$ với $k>0$ thì $x=\sqrt k$ hoặc $x=-\sqrt k$ (căn bậc hai, Toán 9 tập một, Chương III).
3. "concept_blocks" (chặng Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT ĐÚNG CHỮ SGK, mỗi mục là hai khối: {"type":"para","variant":"heading","text":"N. Tên"} rồi {"type":"para","text":"<nội dung>"}; cuối nội dung ghi trang "\textit{(SGK Toán 9 tập hai, tr.N)}" theo tên file ảnh. 6 mục:
   1. Định nghĩa phương trình bậc hai một ẩn (chép định nghĩa trong khung SGK, nhấn $a\ne 0$).
   2. Giải phương trình bậc hai khuyết $c$ ($ax^2+bx=0$: đặt nhân tử chung) và khuyết $b$ (đưa về $x^2=k$ hoặc $(x+p)^2=k$) — viết theo cách SGK trình bày ở Ví dụ 2, Ví dụ 3.
   3. Công thức nghiệm của phương trình bậc hai: biệt thức $\Delta=b^2-4ac$ và ba trường hợp (chép khung SGK tr.13).
   4. Nhận xét: nếu $a$ và $c$ trái dấu thì $ac<0$, nên $\Delta=b^2-4ac>0$, phương trình có hai nghiệm phân biệt (trả lời "Thử thách nhỏ" tr.14 — viết đủ lí do như trên).
   5. Tính nhẩm nghiệm (chép khung SGK Bài 20 trường hợp $a+b+c=0$ và $a-b+c=0$, tr.22–23). Thêm một câu: dùng để kiểm tra nhanh nghiệm vừa tìm.
   6. Số nghiệm của phương trình có tham số: từ công thức nghiệm, phương trình $ax^2+bx+c=0$ ($a\ne0$) có hai nghiệm phân biệt khi $\Delta>0$, có nghiệm kép khi $\Delta=0$, vô nghiệm khi $\Delta<0$, có nghiệm khi $\Delta\ge 0$. Số $x_0$ là nghiệm của phương trình khi $ax_0^2+bx_0+c=0$. (Mục này không ghi trang, ghi "\textit{(suy ra từ công thức nghiệm)}".)
   KHÔNG đưa "Chú ý" về $\Delta'$ / công thức nghiệm thu gọn. KHÔNG thêm mẹo, các bước làm bài, lỗi hay gặp, cấu trúc đề thi. Mỗi mục xuống dòng bằng [[br]] khi có nhiều ý, không dùng ";".
4. "mindmap": {"type":"mindmap","caption":"Điền các ô trống để tự tóm tắt buổi học","root":"Phương trình bậc hai $ax^2+bx+c=0$ ($a\\ne0$)","branches":[4 nhánh: "Khuyết $b$, khuyết $c$" (con: $ax^2+bx=0$: đặt [[blank:2cm]] chung, $x^2=k$ ($k>0$): $x=[[blank:1.6cm]]$), "Công thức nghiệm" (con: $\Delta=[[blank:2cm]]$, $\Delta>0$: [[blank:2.4cm]], $\Delta=0$: [[blank:2.4cm]], $\Delta<0$: [[blank:2.4cm]]), "Tìm $m$" (con: hai nghiệm phân biệt: $\Delta[[blank:0.8cm]]0$, có nghiệm: $\Delta[[blank:0.8cm]]0$, biết nghiệm $x_0$: thay $x=x_0$ vào [[blank:2cm]]), "Luôn có nghiệm" (con: $\Delta=(\ldots)^2[[blank:0.8cm]]0$, $a$, $c$ [[blank:1.6cm]] dấu)]}. Mỗi nhánh {"label":…,"children":[{"label":…}]}.
5. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số/"khuôn"):
   review: 10 phút — nhắc lại hằng đẳng thức, chuyển vế, phương trình tích, đọc đề đích, chưa giải.
   concept: 20 phút — mục 3 và mục 6 là trọng tâm, cho học sinh tự tính $\Delta$ một phương trình ngay khi giảng.
   practice1: khoảng 25 phút — câu nhỏ trắc nghiệm, Đúng/Sai, trả lời ngắn, gọi nhiều học sinh trả lời miệng, chữa nhanh. Ví dụ 1–3 giáo viên làm cùng lớp, học sinh điền ô.
   practice2: khoảng 105 phút — mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm bài ngay sau, câu hỏi dẫn trả lời miệng, ý chính tự trình bày vào vở. Bài 19 (đề đích) làm cá nhân rồi gọi lên bảng.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 20–33 in thành phiếu riêng, khoảng 85 phút. Buổi sau chữa Bài 30, Bài 31 trước.
'''

PROMPT_LOP = CHUNG + KHUON_KHOI + r'''
## Việc B: dựng 2 chặng LUYỆN TẬP trên lớp
Đầu ra JSON {"stages":[{"kind":"practice1","number":3,"title":"Luyện tập 1 — Nhận biết","teacher_note":"","blocks":[…]},{"kind":"practice2","number":4,"title":"Luyện tập 2 — Thông hiểu","teacher_note":"","blocks":[…]}],"ghi_chu":"…"}.
- Khối ĐẦU TIÊN của practice1: {"type":"para","text":"\\textbf{Đích của buổi học:} Bài 19 — đề giữa kì II THCS Nguyễn Trường Tộ: giải phương trình khi cho giá trị của $m$ và chứng minh phương trình luôn có nghiệm. Mạch 1–4 chuẩn bị cho ý a), Mạch 5–7 chuẩn bị cho ý b)."}
- Sau đó các khối ĐÚNG THỨ TỰ sơ đồ dưới đây. Mục ghi "Đích + Mạch 4…" chỉ in tiêu đề "Mạch 4. Giải phương trình bằng công thức nghiệm".
- Bài 19 là bài đích: đề chép nguyên văn (hai ý của đề gốc) rồi tách thành các câu a)–e) như sơ đồ. Lời giải ý e) kết luận đúng: $\Delta=4(m-2)^2\ge 0$ với mọi $m$ nên phương trình luôn có nghiệm với mọi $m$ (khi $m=2$ thì $\Delta=0$, hai nghiệm trùng nhau).
- Ví dụ 10: tham số trong đề tên là $a$, trùng tên hệ số. Lời giải ghi rõ "Phương trình có hệ số của $x^2$ là $1$, hệ số tự do là $-1$" rồi xét tích hai hệ số đó.

## Sơ đồ (đúng thứ tự khối)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + KHUON_KHOI + r'''
## Việc C: phần BÀI TẬP VỀ NHÀ (mọi bài "tier":"btvn", Bài 20. đến Bài 33.)
Không ví dụ, không tiêu đề mạch. Trả về {"stages":[{"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":"","blocks":[14 bài]}],"ghi_chu":"…"}.
Thứ tự: các bài NB (20–23) rồi các bài có ý [TH] (24–33), đúng sơ đồ. Bài NB nhiều ý: một câu yêu cầu chung + các ý a) [NB] …. Bài 20 hỏi "Trong các phương trình sau, phương trình nào là phương trình bậc hai ẩn $x$? Với phương trình bậc hai, chỉ rõ các hệ số $a$, $b$, $c$." Lời giải đầy đủ như trên lớp. Học sinh làm vào vở, không ghi điểm từng bài.

## Sơ đồ (đúng thứ tự khối)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", ANH),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/dung-chang-phieu.json", []),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/dung-chang-phieu.json", [])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p1-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
