#!/usr/bin/env python3
"""Việc Gemini đợt 4 — Phiếu 2 ch.VI 9C bản 2 (17/11/2026): CLEAN câu hỏi (bỏ lời thừa, rõ mục tiêu → output).

Thầy 17/11: "clean là clean lại những lời thừa … Bài 3 có nhất thiết phải cho phương trình không? … Bài 4 cho thêm
dữ kiện các phương trình đều có 2 nghiệm phân biệt … Mục đích của việc ra đề là hướng tới việc gì? HS tương tác và
ra được outputs ntn?" Claude CHỐT ĐỀ từng bài (DE_MOI: thân = đề gốc, ý = câu ngắn một output); Gemini viết lại
LỜI GIẢI cho khớp đề mới (chỉ trả lời đúng cái được hỏi, ý cuối "Theo câu …").

    .venv/bin/python scripts/gemini/viec_clean_p2_ch6_9c.py
    python3 scripts/gemini/tho.py --song-song 2      (clean-p2-ch6-9c-lop, clean-p2-ch6-9c-btvn)
    .venv/bin/python scripts/gemini/lap_p2_ch6_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_dung_p2_ch6_9c import CHUNG, MODEL, SEED  # noqa: E402

VID_LOP, VID_BTVN = "clean-p2-ch6-9c-lop", "clean-p2-ch6-9c-btvn"
BR = "[[br]]"


def y(*ds):
    return BR + BR.join(ds)


# Đề mới (Claude chốt). Bài Đúng/Sai: (câu dẫn, khẳng định). Trắc nghiệm: (đề, 4 phương án).
DE_MOI = {
    "Bài 1.": ("[NB] Khẳng định sau đúng hay sai? Vì sao?",
               ["Tổng và tích hai nghiệm của phương trình $x^2-x+1=0$ đều bằng $1$."]),
    "Bài 2.": ("[NB] Biểu thức $x_1^2+x_2^2$ viết theo $x_1+x_2$ và $x_1x_2$ là",
               ["$(x_1+x_2)^2-2x_1x_2$", "$(x_1+x_2)^2+2x_1x_2$", "$(x_1+x_2)^2-x_1x_2$", "$(x_1+x_2)^2-4x_1x_2$"]),
    "Bài 3.": "[NB] Phương trình $x^2+x+1=0$ có tổng và tích các nghiệm là hai số đối nhau không? Vì sao?",
    "Bài 4.": ("Các phương trình sau đều có hai nghiệm phân biệt. Tính tổng và tích các nghiệm của mỗi phương trình. "
               r"\textit{(SGK 6{.}23)}" + y("a) [NB] $x^2-12x+8=0$", "b) [NB] $2x^2+11x-5=0$", "c) [NB] $3x^2-10=0$")),
    "Bài 5.": (r"Cho phương trình $x^2+3x-5=0$. Chứng minh rằng phương trình có hai nghiệm phân biệt $x_1$, $x_2$. Tính "
               r"$x_1+x_2-x_1x_2$. \textit{(HK2 Phòng GD\&ĐT Gia Lâm, 2024--2025)}"
               + y("a) [NB] Vì sao phương trình có hai nghiệm phân biệt?", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
                   "c) [NB] Tính $x_1+x_2-x_1x_2$.")),
    "Bài 6.": ("[NB] Khẳng định sau đúng hay sai? Vì sao?",
               ["Phương trình $x^2-2x+m=0$ có hai nghiệm trái dấu khi $m<0$."]),
    "Bài 7.": r"[NB] Biết phương trình $x^2+2\sqrt2\,x+2=0$ có một nghiệm $x_1=-\sqrt2$. Dùng tích hai nghiệm, tìm nghiệm còn lại.",
    "Bài 8.": "[NB] Tìm $m$ để phương trình $x^2+4x+m=0$ có hai nghiệm trái dấu.",
    "Bài 9.": r"[NB] Quy đồng mẫu rồi cộng: $\dfrac{1}{x_1+3}+\dfrac{1}{x_2+3}$ (với $x_1\ne-3$, $x_2\ne-3$).",
    "Bài 10.": (r"Cho phương trình $x^2-5x+2=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, "
                r"hãy tính giá trị biểu thức $A=x_1^2+x_2^2$. \textit{(GK2 THCS Cổ Đông, 2024--2025)}"
                + y(r"a) [NB] Tính $\Delta$.", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "c) [TH] Tính $A$.")),
    "Bài 11.": (r"Cho phương trình $x^2-7x-1=0$ có hai nghiệm là $x_1$, $x_2$. Không giải phương trình, hãy tính giá trị "
                r"của biểu thức $A=x_1^2+x_2^2-x_1x_2$. \textit{(HK2 THCS Thăng Long, 2025--2026)}"
                + y(r"a) [NB] Tính $\Delta$.", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
                    "c) [NB] Viết $A$ theo $x_1+x_2$ và $x_1x_2$.", "d) [TH] Tính $A$.")),
    "Bài 12.": (r"Biết phương trình bậc hai $2x^2-4x+1=0$ có hai nghiệm $x_1$ và $x_2$. Chứng minh $x_1$, $x_2$ khác $0$ và "
                r"tính tổng nghịch đảo hai nghiệm. \textit{(thi thử vào 10 lần 1, THCS Cầu Giấy, 2025--2026)}"
                + y(r"a) [NB] Tính $\Delta$.", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
                    r"c) [NB] Viết $\dfrac{1}{x_1}+\dfrac{1}{x_2}$ theo $x_1+x_2$ và $x_1x_2$.",
                    "d) [TH] Chứng minh $x_1$, $x_2$ khác $0$ và tính tổng nghịch đảo hai nghiệm.")),
    "Bài 13.": (r"Gọi $x_1$, $x_2$ là hai nghiệm của phương trình $2x^2-x-5=0$. Không giải phương trình, hãy tính giá trị "
                r"biểu thức $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$. \textit{(HK2 Phòng GD\&ĐT Ba Đình, 2024--2025)}"
                + y(r"a) [NB] Tính $\Delta$.", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
                    r"c) [NB] Quy đồng $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$.", "d) [TH] Tính giá trị biểu thức.")),
    "Bài 14.": (r"Cho phương trình $x^2+4x-6=0$, gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Tính giá trị của biểu thức "
                r"$A=\dfrac{1}{x_1+3}+\dfrac{1}{x_2+3}$. \textit{(đề minh hoạ tuyển sinh 10, THCS Thái Thịnh, 2025--2026)}"
                + y(r"a) [NB] Tính $\Delta$.", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "c) [TH] Tính $A$.")),
    "Bài 15.": (r"Cho phương trình $x^2+5x-1=0$. Tính tổng lập phương hai nghiệm của phương trình. "
                r"\textit{(đề minh hoạ tuyển sinh 10, THCS Thái Thịnh, 2025--2026)}"
                + y(r"a) [NB] Tính $\Delta$.", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "c) [TH] Tính $x_1^3+x_2^3$.")),
    "Bài 16.": (r"Biết rằng phương trình bậc hai $x^2-3x+a=0$ có một nghiệm là $x=\dfrac{3-\sqrt5}{2}$. Tìm tổng bình phương "
                r"hai nghiệm của phương trình trên. \textit{(đề minh hoạ tuyển sinh 10, Sở GD\&ĐT Hà Nội)}"
                + y("a) [NB] Thay nghiệm đã cho vào phương trình, tìm $a$.", r"b) [NB] Với $a$ vừa tìm, tính $\Delta$.",
                    "c) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "d) [TH] Tính tổng bình phương hai nghiệm.")),
    "Bài 17.": (r"Cho phương trình $x^2+3x+m=0$ ($m$ là tham số). Tìm các giá trị của $m$ để phương trình có hai nghiệm thỏa "
                r"mãn $x_1^2+x_2^2=2025$. \textit{(HK2 THCS Thái Thịnh, 2025--2026)}"
                + y(r"a) [NB] Tính $\Delta$ theo $m$.", "b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
                    "c) [TH] Tìm $m$.")),
    "Bài 18.": (r"Cho phương trình $x^2-(m+2)x+2m=0$ ($m$ là tham số). Tìm $m$ để phương trình có hai nghiệm $x_1$, $x_2$ "
                r"thỏa mãn $x_1^2+x_2^2=7+x_1x_2$. \textit{(HK2 Phòng GD\&ĐT Hoài Đức, 2024--2025)}"
                + y(r"a) [NB] Tính $\Delta$ theo $m$.", "b) [NB] Phương trình có nghiệm với mọi $m$ không? Vì sao?",
                    "c) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.", "d) [VD] Tìm $m$.")),
    "Bài 19.": (r"Cho phương trình $x^2+mx-6=0$. \textit{(HK2 THCS\&THPT M.V. Lômônôxốp, 2024--2025)}"
                + y(r"a) [NB] Chứng minh rằng phương trình luôn có hai nghiệm phân biệt $x_1$, $x_2$ với mọi giá trị của $m$.",
                    "b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
                    r"c) [VD] Tìm giá trị của $m$ để phương trình có hai nghiệm $x_1$, $x_2$ thỏa mãn $x_1^2+x_2^2-x_1x_2=22$.")),
    "Bài 20.": ("Các phương trình sau đều có nghiệm. Tính tổng và tích các nghiệm của mỗi phương trình."
                + y("a) [NB] $2x^2-7x+3=0$", "b) [NB] $25x^2-20x+4=0$", r"c) [NB] $2\sqrt2\,x^2-4=0$")),
    "Bài 21.": ("Cho phương trình $2x^2-7x+6=0$."
                + y("a) [NB] Chứng minh phương trình có hai nghiệm phân biệt.", "b) [NB] Tính tổng và tích các nghiệm.")),
    "Bài 22.": ("Tính nhẩm nghiệm của các phương trình sau:"
                + y(r"a) [NB] $\sqrt2\,x^2-(\sqrt2+1)x+1=0$", r"b) [NB] $2x^2+(\sqrt3-1)x-3+\sqrt3=0$")),
    "Bài 23.": "[NB] Tìm $m$ để phương trình $x^2-2(m-1)x+m+1=0$ có hai nghiệm trái dấu.",
    "Bài 24.": (r"Gọi $x_1$, $x_2$ là hai nghiệm của phương trình $x^2-4\sqrt3\,x+8=0$. Không giải phương trình, hãy tính "
                r"$Q=x_1^3+x_2^3$. \textit{(HK2 THCS Chu Văn An, Đà Nẵng, 2025--2026)}"
                + y(r"a) [NB] Tính $\Delta$.", "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "c) [TH] Tính $Q$.")),
    "Bài 25.": (r"Cho phương trình $x^2-2x-9=0$ có hai nghiệm $x_1$, $x_2$ khác $0$. Không giải phương trình, hãy tính "
                r"$A=\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$. \textit{(thi thử vào 10, THCS Thái Thịnh, 2026--2027)}"
                + y("a) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "b) [NB] Quy đồng $A$.", "c) [TH] Tính $A$.")),
    "Bài 26.": (r"Cho phương trình $x^2-5x-3=0$. Biết phương trình có hai nghiệm $x_1$, $x_2$. Không giải phương trình, hãy "
                r"tính $A=\dfrac{1}{x_1-1}+\dfrac{1}{x_2-1}$. \textit{(GK2 THCS Nguyễn Du, 2024--2025)}"
                + y("a) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "b) [NB] Quy đồng mẫu $A$.", "c) [TH] Tính $A$.")),
    "Bài 27.": (r"Cho phương trình $2x^2-13x-6=0$. Với $x_1$, $x_2$ là nghiệm của phương trình, không giải phương trình, hãy "
                r"tính $A=(x_1+x_2)(x_1+2x_2)-x_2^2$. \textit{(đề minh hoạ tuyển sinh 10, THCS Tô Vĩnh Diện, 2025--2026)}"
                + y("a) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "b) [NB] Khai triển và rút gọn $A$.", "c) [TH] Tính $A$.")),
    "Bài 28.": (r"Cho phương trình $x^2+5x-7=0$. \textit{(HK2 THCS Phúc Lợi, 2024--2025)}"
                + y("a) [NB] Chứng minh phương trình có hai nghiệm phân biệt $x_1$, $x_2$.",
                    "b) [NB] Tính $x_1+x_2$ và $x_1x_2$.", "c) [TH] Tính $A=x_1^2+x_2^2-2x_1x_2$.")),
    "Bài 29.": (r"Cho phương trình $x^2+5x+m=0$, biết một nghiệm là $\dfrac{-\sqrt{13}-5}{2}$. Tìm tổng bình phương hai "
                r"nghiệm của phương trình. \textit{(thi thử vào 10 lần 3, THCS Thọ Lộc, 2025--2026)}"
                + y("a) [NB] Tính tổng hai nghiệm.", "b) [NB] Tìm nghiệm còn lại.",
                    "c) [TH] Tính tổng bình phương hai nghiệm.")),
    "Bài 30.": (r"Cho phương trình $x^2-x+m=0$ có hai nghiệm $x_1$, $x_2$ và $x_1=\dfrac{1+\sqrt{13}}{2}$. Tính giá trị của "
                r"biểu thức $A=3x_1^2x_2+3x_1x_2^2$. \textit{(HK2 THCS Đại Áng, 2025--2026)}"
                + y("a) [NB] Tìm $x_2$.", "b) [TH] Tính $A$.")),
    "Bài 31.": (r"Cho phương trình $x^2+4x+m=0$ có hai nghiệm phân biệt $x_1$, $x_2$, trong đó có một nghiệm là "
                r"$x_1=-\sqrt3$. Tính tổng nghịch đảo hai nghiệm của phương trình. \textit{(GK2 xã Đông Anh, 2025--2026)}"
                + y("a) [NB] Tìm $x_2$.", "b) [TH] Tính tổng nghịch đảo hai nghiệm.")),
    "Bài 32.": (r"Cho phương trình $x^2-6x-2m+3=0$. Tìm $m$ để phương trình có hai nghiệm phân biệt $x_1$, $x_2$ thỏa mãn "
                r"$x_1^2+x_2^2=20$. \textit{(GK2 THCS Mai Dịch, 2024--2025)}"
                + y(r"a) [NB] Tính $\Delta$ theo $m$.", "b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.", "c) [VD] Tìm $m$.")),
    "Bài 33.": (r"Tìm tất cả các giá trị của tham số $m$ để phương trình $x^2-2mx+4m-4=0$ có hai nghiệm $x_1$, $x_2$ thỏa "
                r"mãn $x_1^2+x_2^2-8=0$. \textit{(thi thử vào 10 lần 2, Phòng GD\&ĐT Thanh Oai, 2025--2026)}"
                + y(r"a) [NB] Tính $\Delta$ theo $m$.", "b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.", "c) [VD] Tìm $m$.")),
}
DUNG_SAI = {"Bài 1.", "Bài 6."}
TRAC_NGHIEM = {"Bài 2."}


def khoi_moi(nhan):
    v = DE_MOI[nhan]
    if nhan in DUNG_SAI:
        return {"statement": v[0], "dung_sai": v[1]}
    if nhan in TRAC_NGHIEM:
        return {"statement": v[0], "options": v[1]}
    return {"statement": v}


def ban_cu(nhans):
    f = json.loads((REPO / SEED).read_text())
    out = {}
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("label") in nhans:
                out[b["label"]] = {"de_moi": khoi_moi(b["label"]), "loi_giai_cu": b.get("solution", "")}
    return json.dumps(out, ensure_ascii=False, indent=1)


PROMPT = CHUNG + r'''
## Việc: viết lại LỜI GIẢI cho khớp ĐỀ MỚI (giáo viên đã chốt đề — KHÔNG sửa đề)
Giáo viên duyệt: mỗi câu hỏi chỉ hỏi MỘT việc, có một output rõ. Đề mới đã bỏ lời thừa. Lời giải cũng phải sạch:
- Mỗi ý trả lời ĐÚNG cái được hỏi, không thêm việc khác. "Tính $x_1+x_2$ và $x_1x_2$" ⇒ chỉ một dòng "Theo định lí Viète, ta có $x_1+x_2=…$ và $x_1x_2=…$." (KHÔNG thêm dòng $\Delta$ hay $a\cdot c$, đề đã cho có nghiệm hoặc ý khác đã lo). "Tính $\Delta$" ⇒ chỉ dòng tính $\Delta$ và so sánh với $0$. "Tính $\Delta$ theo $m$" ⇒ chỉ tính, rút gọn. "Viết … theo $x_1+x_2$ và $x_1x_2$", "Quy đồng" ⇒ chỉ một chuỗi biến đổi.
- Ý cuối ([TH]/[VD]) làm nốt bài theo nhịp bài thi, mở đầu "Theo câu a) và b), …" (hoặc câu tương ứng), KHÔNG chép lại các dòng ý trước. Việc mà các ý trước chưa làm thì ý cuối phải làm đủ: điều kiện có nghiệm theo $m$ ($\Delta\ge0$ hoặc $\Delta>0$, giải ra điều kiện), khai triển mẫu, kiểm tra mẫu khác $0$, đối chiếu điều kiện. Kết bằng dòng "Vậy …" riêng.
- Bài 15: đề không khẳng định có nghiệm ⇒ ý b) có dòng "Vì $a\cdot c=-1<0$ nên phương trình có hai nghiệm phân biệt." trước khi tính. Bài 5 c), Bài 7: một hai dòng.
- Bài trắc nghiệm: "Chọn A." + một dòng lí do. Bài Đúng/Sai: "Sai." hoặc "Đúng." + lí do một hai dòng.
- Đáp số giữ đúng như lời giải cũ (đã kiểm bằng máy). KHÔNG "Do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy". Dòng con "[[br]]\hspace*{1.4em}", ý mới "[[br]]a) …".
Đầu ra {"sua":[{"label","statement","solution"}…],"ghi_chu":"…"}: "statement" CHÉP NGUYÊN "de_moi.statement" (không đổi một chữ), "solution" là lời giải mới. Trả về MỌI bài có dưới đây.

## Đề mới + lời giải cũ
'''


def main():
    lop = [f"Bài {i}." for i in range(1, 20)]
    btvn = [f"Bài {i}." for i in range(20, 34)]
    for vid, nh in ((VID_LOP, lop), (VID_BTVN, btvn)):
        v = {"id": vid, "model": MODEL, "prompt": PROMPT + ban_cu(set(nh)) + "\n", "files": [],
             "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
             "meta": {"loai": "clean-p2-ch6-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
