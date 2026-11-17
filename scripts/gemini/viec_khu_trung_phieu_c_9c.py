#!/usr/bin/env python3
"""Sinh việc Gemini: KHỬ TRÙNG ĐỀ phiếu C (Viète) ch.VI 9C — 15/11/2026.

Soát 15/11: trùng đề TRONG phiếu (4a = 10 = 12a, 4b = 12b, 5a = 13a, 6a = 14a = 18, 19a = 21a,
22 = 29, 23a = 30a, 23b = 13b, 24 = 31), $x^2-3x+1$ (= đích phiếu D) ở 7 ý, và phương trình lặp
phiếu D. Claude chốt bảng thay (SymPy: scripts/gemini/so_do_phieu_c_9c_khu_trung.py), Gemini
viết lại chữ của đúng các ý đó.

    .venv/bin/python scripts/gemini/so_do_phieu_c_9c_khu_trung.py     (kiểm sơ đồ)
    python3 scripts/gemini/viec_khu_trung_phieu_c_9c.py
    python3 scripts/gemini/tho.py --mot khu-trung-9c-ch6-phieu-c
    python3 scripts/gemini/ap_sua_phieu.py khu-trung-9c-ch6-phieu-c [--ghi]
Đợt 2 (Bài 8a, 26c lặp đề 15 phút số 13):  ... viec_khu_trung_phieu_c_9c.py --dot2  → id khu-trung-9c-ch6-phieu-c-2
Đợt 3 (câu THẬT từ ngân hàng + bỏ x^2+x-6):  ... --dot3  → id khu-trung-9c-ch6-phieu-c-3
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from so_do_phieu_c_9c_khu_trung import THAY, THAY2, tex, kiem_dot3  # noqa: E402
import sympy as sp  # noqa: E402

SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-c-dinh-li-viete-va-ung-dung.json"
VID = "khu-trung-9c-ch6-phieu-c"
LABELS = ["Bài 1.", "Bài 3.", "Bài 4.", "Bài 5.", "Bài 6.", "Bài 7.", "Bài 10.", "Bài 11.",
          "Bài 18.", "Bài 21.", "Bài 22.", "Bài 23.", "Bài 24.", "Bài 30.", "Ví dụ 4.", "Ví dụ 10."]
TEN = {"SP": "tổng và tích", "SQ": "$x_1^2+x_2^2$", "INV": "$\\dfrac{1}{x_1}+\\dfrac{1}{x_2}$",
       "CUBE": "$x_1^3+x_2^3$", "DIFF2": "$(x_1-x_2)^2$", "SIGN": "dấu hai nghiệm",
       "RATIO": "$\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$"}

PROMPT = r'''Bạn là thợ sửa phiếu học tập Toán 9 (định lí Viète, học sinh lớp 9 tầng C — học lực trung bình). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề.

KHÔNG chạy lệnh, KHÔNG mở file: toàn bộ dữ liệu nằm ở mục "Dữ liệu gốc" cuối prompt (trích từ seed phiếu). Mỗi khối có "label", "statement", "solution" (riêng "Ví dụ N." chỉ có "statement" = toàn bộ chữ ví dụ kèm lời giải mẫu). Xuống dòng trong chuỗi là [[br]]. Toán viết LaTeX trong $...$; giữ escape \& (ví dụ "GD\&ĐT").

## Vì sao phải sửa
Phiếu bị TRÙNG ĐỀ: nhiều ý dùng lại đúng phương trình VÀ đúng câu hỏi của ý khác trong phiếu (hoặc của phiếu khác cùng chương). Giáo viên đã chọn phương trình MỚI cho từng ý (bảng dưới, số liệu đã kiểm bằng máy). Việc của bạn: thay phương trình ở đúng các ý đó và viết lại các con số đi kèm (dòng điều kiện $\Delta$/$\Delta'$/$ac$, tổng, tích, phép tính, đáp số) trong statement và solution. MỌI CHỮ KHÁC GIỮ NGUYÊN Y HỆT (câu dẫn, khung chỗ chấm \ldots\ldots, thẻ [NB]/[TH], cách xuống dòng [[br]]\hspace*{1.4em}, các ý KHÔNG có trong bảng).

## Bảng thay (bất di bất dịch — không đổi số)
{BANG}

## Dặn riêng từng chỗ
1. Dòng điều kiện giữ ĐÚNG KIỂU của ý cũ trong statement (ý cũ là "Ta có $\Delta=\ldots\ldots>0$" thì giữ $\Delta$; là "$ac=\ldots\ldots<0$" thì giữ $ac$). Trong solution viết đủ phép tính như bản cũ, ví dụ "Ta có $\Delta=(-7)^2-4\cdot1\cdot7=21>0$ nên phương trình có hai nghiệm phân biệt." hoặc "Ta có $ac=1\cdot(-7)=-7<0$ nên phương trình có hai nghiệm phân biệt.". Ví dụ 4 và Ví dụ 10 dùng $\Delta'$ như bản cũ: "$\Delta'=(-6)^2-3\cdot 4=24>0$", "$\Delta'=(-4)^2-1\cdot 2=14>0$".
2. Bài 5 ý a): BỎ chú thích nguồn "\;(thi thử Vào 10 lần 1, THCS Cầu Giấy)" (phương trình mới không phải đề Cầu Giấy).
3. Bài 10: đổi phương trình trong câu dẫn thành $x^2-5x+5=0$ và BỎ "(đề minh họa Vào 10, Sở GD\&ĐT Hà Nội)" ở cuối câu dẫn (câu dẫn kết thúc bằng "tính $x_1^2+x_2^2$."). Ý a) thành "$\Delta=(-5)^2-4\cdot 1\cdot 5=\ldots\ldots$"; dòng "Vì $\Delta\ldots 0$ nên phương trình có hai nghiệm." sửa thành "Vì $\Delta\ldots 0$ nên phương trình có hai nghiệm phân biệt." (khớp lời giải). Lời giải: a) $\Delta=25-20=5$ ... b) $x_1+x_2=5$, $x_1x_2=5$ (giữ hai dòng như cũ) c) $x_1^2+x_2^2=5^2-2\cdot 5=15$.
4. Bài 11 ý b): BỎ chú thích nguồn "\;(thi thử Vào 10, THCS Tự Lập)". Kết luận vẫn là "cùng âm" (tổng $-7<0$, tích $3>0$).
5. Bài 18: đổi phương trình trong câu dẫn thành $x^2-4x-4=0$ và BỎ "(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)". Giữ nguyên khung chỗ chấm. Lời giải: a) $ac=-4<0$ nên phương trình có hai nghiệm phân biệt / $x_1+x_2=4$ / $x_1x_2=-4$. b) $x_1^3+x_2^3=4^3-3\cdot(-4)\cdot 4=64+48=112$.
6. Bài 30 chỉ đổi ý b); ý a) giữ nguyên từng chữ (kể cả nguồn Đống Đa). Bài 22, Bài 23, Bài 24 đổi CẢ hai ý a), b). Bài 21 chỉ đổi ý a), ý b) giữ nguyên.
7. Lời giải các bài BTVN (Bài 21–24, 30) viết đủ 4 bước như các ý khác của chính bài đó: dòng điều kiện → "Theo định lí Viète, ta có $\begin{cases} x_1+x_2=…\\ x_1x_2=…\end{cases}$" (KHÔNG chấm sau cases) → biến đổi (có dòng "Vì $x_1x_2=…\ne 0$ nên $x_1\ne 0$ và $x_2\ne 0$." ở dạng nghịch đảo) → "Vậy …".
8. Ví dụ 4 (dạng $\dfrac{1}{x_1}+\dfrac{1}{x_2}$) và Ví dụ 10 (dạng $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$): chỉ thay phương trình và các con số; giữ nguyên câu đề, tiêu đề "Lời giải", các bước. Trả về trong "statement" TOÀN BỘ chữ ví dụ mới; "solution" để chuỗi rỗng "".
9. Không văn nói, không xưng hô ("em", "hôm nay", "Kiểm", "Soi"), không kí hiệu $S$, $P$, không dấu chấm phẩy ";" nối công thức. Phân số dùng \dfrac (phân số lồng trong phân số dùng \frac như bản cũ). Số âm trong phép tính đặt trong ngoặc: $(-7)^2$, $2\cdot(-3)$.

## Kiểm lại trước khi nộp
- Tự tính lại MỌI con số của các ý đã đổi (Viète: $x_1+x_2=-\frac{b}{a}$, $x_1x_2=\frac{c}{a}$) và so với cột "đáp số" trong bảng; lệch thì ghi vào "ghi_chu", KHÔNG tự đổi phương trình.
- Không đổi "label", không thêm/bớt bài, không đổi số ý, không đụng ý không có trong bảng.
- LaTeX hợp lệ: ngoặc { } cân, $ đủ cặp (đặc biệt $ đóng ở cuối dòng).

## Đầu ra
JSON đúng schema: {"sua": [16 phần tử {"label","statement","solution"}, đủ: {NHAN}], "ghi_chu": "điểm nghi ngờ hoặc chuỗi rỗng"}.
"statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ (kể cả phần không đổi).
'''


def bang() -> str:
    dong = ["| ý | phương trình MỚI | câu hỏi | Δ / ac | tổng | tích | đáp số |", "|---|---|---|---|---|---|---|"]
    for lab, (a, b, c), loai, dk, _ly in THAY:
        S, P = sp.Rational(-b, a), sp.Rational(c, a)
        val = {"SP": "tổng $%s$, tích $%s$" % (sp.latex(S), sp.latex(P)), "SQ": S**2 - 2 * P, "INV": S / P,
               "CUBE": S**3 - 3 * P * S, "DIFF2": S**2 - 4 * P, "SIGN": "hai nghiệm cùng âm",
               "RATIO": (S**2 - 2 * P) / P}[loai]
        if not isinstance(val, str):
            val = "$%s$" % sp.latex(val).replace("\\frac", "\\dfrac")
        dk_s = {"Delta": f"$\\Delta={b*b-4*a*c}$", "ac": f"$ac={a*c}$",
                "Delta'": f"$\\Delta'={(b//2)**2-a*c}$"}[dk]
        dong.append(f"| {lab} | ${tex(a, b, c)}$ | {TEN[loai]} | {dk_s} | ${sp.latex(S)}$ | ${sp.latex(P)}$ | {val} |")
    return "\n".join(dong)


PROMPT2 = r'''Bạn là thợ sửa phiếu học tập Toán 9 (định lí Viète, học sinh lớp 9 tầng C). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề.

KHÔNG chạy lệnh, KHÔNG mở file: dữ liệu nằm ở mục "Dữ liệu gốc" cuối prompt. Xuống dòng là [[br]]. Toán trong $...$.

## Việc
Hai ý dưới đây trùng đề kiểm tra 15 phút nên giáo viên đổi phương trình (đã kiểm bằng máy). Thay phương trình và viết lại các con số đi kèm trong statement và solution; MỌI CHỮ KHÁC GIỮ Y HỆT (khung chỗ chấm, thẻ [NB], các ý khác).
- Bài 8 ý a): $x^2-7x+12=0$, nghiệm $x_1=3$  →  $x^2-11x+24=0$, nghiệm $x_1=3$. Lời giải: $x_1+x_2=11$, $x_2=11-3=8$, "Vậy nghiệm còn lại là $x_2=8$."
- Bài 26 ý c): $3x^2-5x+2=0$, nghiệm $x_1=1$  →  $3x^2-7x+4=0$, nghiệm $x_1=1$. Lời giải: $x_1+x_2=\dfrac{7}{3}$, $x_2=\dfrac{7}{3}-1=\dfrac{4}{3}$, "Vậy nghiệm còn lại là $x_2=\dfrac{4}{3}$."
Bài 8 ý b), c) và Bài 26 ý a), b) giữ nguyên từng chữ. Tự tính lại; lệch thì ghi "ghi_chu".

## Đầu ra
JSON đúng schema: {"sua": [2 phần tử {"label","statement","solution"} cho "Bài 8." và "Bài 26."], "ghi_chu": ""}. "statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ.
'''


def dot2():
    labels = ["Bài 8.", "Bài 26."]
    seed = json.loads((REPO / SEED).read_text())
    goc = [{k: b[k] for k in ("label", "statement", "solution")} for s in seed["stages"]
           for b in s.get("blocks", []) if b.get("type") == "problem" and b["label"] in labels]
    assert len(goc) == 2 and len(THAY2) == 2
    vid = VID + "-2"
    viec = {"id": vid, "model": "gemini-4-hydrogen-medium",
            "prompt": PROMPT2 + "\n## Dữ liệu gốc (JSON)\n" + json.dumps(goc, ensure_ascii=False, indent=1) + "\n",
            "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "600s",
            "meta": {"loai": "sua-phieu", "seed": SEED, "labels": labels}}
    out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO))


PROMPT3 = r'''Bạn là thợ sửa phiếu học tập Toán 9 (định lí Viète, học sinh lớp 9 tầng C — học lực trung bình). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề.

KHÔNG chạy lệnh, KHÔNG mở file: dữ liệu nằm ở mục "Dữ liệu gốc" cuối prompt. Mỗi khối có "label", "statement", "solution". Xuống dòng là [[br]]. Toán viết LaTeX trong $...$; giữ escape \& ("GD\&ĐT").

## Việc
Giáo viên thay phương trình ở các ý trong bảng bằng phương trình lấy từ ĐỀ THI THẬT / SGK (đã kiểm đáp số bằng máy). Thay phương trình, viết lại các con số đi kèm (dòng điều kiện, tổng, tích, phép tính, đáp số) trong statement và solution. MỌI CHỮ KHÁC GIỮ Y HỆT: câu dẫn, khung chỗ chấm \ldots\ldots, thẻ [NB]/[TH], cách xuống dòng [[br]]\hspace*{1.4em}, các ý KHÔNG có trong bảng (kể cả chú thích nguồn của chúng).

## Bảng thay (bất di bất dịch)
{BANG}

Cột "nguồn in trên đề": nếu khác rỗng thì đặt ngay sau phương trình của ý đó, đúng kiểu sẵn có trong phiếu: "a) [NB] $x^2+8x-6=0$ \;(đề chính thức Vào 10 Hà Nội 2025)". Nếu rỗng thì KHÔNG ghi nguồn và xoá chú thích nguồn cũ của ý đó (nếu có).

## Dặn riêng
1. Dòng điều kiện trong statement giữ ĐÚNG KIỂU của ý cũ ($\Delta$ hay $ac$ — bảng đã chọn khớp). Solution viết đủ phép tính, ví dụ "Ta có $\Delta=(-12)^2-4\cdot1\cdot8=112>0$ nên phương trình có hai nghiệm phân biệt.", "Ta có $ac=4\cdot(-15)=-60<0$ nên phương trình có hai nghiệm phân biệt.", "Ta có $\Delta=(-4\sqrt3)^2-4\cdot1\cdot8=16>0$ …". Phương trình chứa căn viết như phiếu: $x^2-4\sqrt3\,x+8=0$.
2. Bài 8 ý a): phương trình $2x^2-7x+5=0$, nghiệm cho sẵn $x_1=1$ (khung đổi "3" thành "1": "Vì phương trình có nghiệm $x_1=1$ nên …", "Suy ra $x_2=\ldots\ldots-1=\ldots\ldots$"). Lời giải: $x_1+x_2=\dfrac{7}{2}$, $x_2=\dfrac{7}{2}-1=\dfrac{5}{2}$.
3. Bài 26 ý c): $7x^2-15x+2=0$, nghiệm $x_1=2$. Lời giải: $x_1+x_2=\dfrac{15}{7}$, $x_2=\dfrac{15}{7}-2=\dfrac{1}{7}$.
4. Bài 10: câu dẫn thành "Điền vào chỗ chấm để hoàn thành bài giải: cho $3x^2-5x+1=0$ có hai nghiệm $x_1$, $x_2$, tính $x_1^2+x_2^2$ (bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)." Ý a) "$\Delta=(-5)^2-4\cdot 3\cdot 1=\ldots\ldots$". Lời giải: a) $\Delta=25-12=13$ / Vì $\Delta>0$ nên phương trình có hai nghiệm phân biệt. b) $x_1+x_2=\dfrac{5}{3}$ / $x_1x_2=\dfrac{1}{3}$. c) $x_1^2+x_2^2=\left(\dfrac{5}{3}\right)^2-2\cdot\dfrac{1}{3}=\dfrac{19}{9}$.
5. Bài 18: câu dẫn đổi phương trình thành $x^2-3x-40=0$ (không nguồn). Lời giải: a) $ac=-40<0$ nên phương trình có hai nghiệm phân biệt / $x_1+x_2=3$ / $x_1x_2=-40$. b) $x_1^3+x_2^3=3^3-3\cdot(-40)\cdot 3=27+360=387$.
6. Bài 20: đổi ý a) thành $2x^2+7x+5=0$. Viết LẠI CẢ lời giải Bài 20 theo văn toán, mỗi ý: dòng tính $\Delta$ (hoặc $ac$) → kết luận số nghiệm → "Vậy phương trình … dùng được định lí Viète." / "Vậy … không dùng được định lí Viète." KHÔNG gạch ngang "—", KHÔNG chữ IN HOA ("KHÔNG"). Đáp: a) $\Delta=49-40=9>0$, dùng được; b) $\Delta=16-16=0$, nghiệm kép, dùng được; c) $\Delta=1-4=-3<0$, vô nghiệm, không dùng được.
7. Bài 28 ý a): $x^2-3x-2025=0$ — trái dấu vì $x_1x_2=-2025<0$.
8. Bài 4 đổi cả ba ý; Bài 6 đổi cả ba ý; Bài 1 đổi a) và c); Bài 3, 5, 21, 22, 28 chỉ đổi a); Bài 7 đổi b) và c); Bài 11 chỉ đổi b); Bài 23, 24 đổi a) (Bài 23 cả a) và b)), Bài 24 chỉ a). Theo đúng bảng.
9. Không văn nói, không xưng hô, không kí hiệu $S$, $P$, không dấu chấm phẩy ";" nối công thức, không chấm sau \end{cases}. Phân số \dfrac (lồng trong phân số dùng \frac như bản cũ). Số âm đặt trong ngoặc khi nhân/luỹ thừa.

## Kiểm lại trước khi nộp
Tự tính lại mọi con số các ý đã đổi và so với bảng; lệch thì ghi "ghi_chu", KHÔNG tự đổi phương trình. Không đổi "label", không thêm/bớt bài/ý. LaTeX hợp lệ: { } cân, $ đủ cặp.

## Đầu ra
JSON đúng schema: {"sua": [{N} phần tử {"label","statement","solution"}, đủ: {NHAN}], "ghi_chu": ""}. "statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ.
'''

TEN3 = dict(TEN, COND="có dùng được định lí Viète không", ROOT="nghiệm còn lại")


def dot3():
    bang = kiem_dot3()
    dong = ["| ý | phương trình MỚI | câu hỏi | Δ | tổng | tích | đáp số | nguồn in trên đề |", "|---|---|---|---|---|---|---|---|"]
    for lab, e, loai, dk, Dl, S, P, val, x1, ma, nguon in bang:
        q = TEN3[loai] + (f" (cho $x_1={x1}$)" if x1 is not None else "")
        dong.append(f"| {lab} | ${e}$ | {q} | ${Dl}$ | ${S}$ | ${P}$ | ${val}$ | {nguon} |".replace("$trái dấu$", "trái dấu").replace("$cùng âm$", "cùng âm").replace("$dùng được$", "dùng được"))
    labels = sorted({b[0].split()[0] + " " + "".join(ch for ch in b[0].split()[1] if ch.isdigit()) + "." for b in bang},
                    key=lambda t: int(t.split()[1][:-1]))
    seed = json.loads((REPO / SEED).read_text())
    goc = [{k: b[k] for k in ("label", "statement", "solution")} for s in seed["stages"]
           for b in s.get("blocks", []) if b.get("type") == "problem" and b["label"] in labels]
    assert len(goc) == len(labels), (labels, [g["label"] for g in goc])
    vid = VID + "-3"
    prompt = PROMPT3.replace("{BANG}", "\n".join(dong)).replace("{NHAN}", ", ".join(labels)).replace("{N}", str(len(labels)))
    viec = {"id": vid, "model": "gemini-4-hydrogen-medium",
            "prompt": prompt + "\n## Dữ liệu gốc (JSON)\n" + json.dumps(goc, ensure_ascii=False, indent=1) + "\n",
            "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
            "meta": {"loai": "sua-phieu", "seed": SEED, "labels": labels}}
    out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), labels)
    print("\n".join(dong))


def main():
    if "--dot3" in sys.argv:
        return dot3()
    if "--dot2" in sys.argv:
        return dot2()
    seed = json.loads((REPO / SEED).read_text())
    goc = []
    for s in seed["stages"]:
        for b in s.get("blocks", []):
            if b.get("type") == "problem" and b["label"] in LABELS:
                goc.append({k: b[k] for k in ("label", "statement", "solution")})
            elif b.get("type") == "noted":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                if m and m.group(1) in LABELS:
                    goc.append({"label": m.group(1), "statement": b["text"]})
    assert sorted(x["label"] for x in goc) == sorted(LABELS), [x["label"] for x in goc]
    prompt = PROMPT.replace("{BANG}", bang()).replace("{NHAN}", ", ".join(LABELS))
    viec = {
        "id": VID, "model": "gemini-4-hydrogen-medium",
        "prompt": prompt + "\n## Dữ liệu gốc (16 khối, JSON)\n" + json.dumps(goc, ensure_ascii=False, indent=1) + "\n",
        "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
        "meta": {"loai": "sua-phieu", "seed": SEED, "labels": LABELS},
    }
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO))
    if "--in" in sys.argv:
        print(bang())


if __name__ == "__main__":
    main()
