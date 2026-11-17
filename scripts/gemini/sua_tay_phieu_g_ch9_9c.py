#!/usr/bin/env python3
"""Sửa tay sau soát đầu ra Gemini — phiếu G ch.IX 9C (mỗi thay thế assert khớp đúng 1 lần)."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lap_phieu_g_ch9_9c import REPO, SEED  # noqa: E402

SUA = [  # (nhãn khối hoặc title, trường, cũ, mới)
    ("1. GÓC NỘI TIẾP", "text",
     "Góc nội tiếp nhỏ hơn hoặc bằng $90^\\circ$ có số đo bằng nửa số đo của góc ở tâm cùng chắn một cung.",
     "Các góc nội tiếp chắn cung nhỏ thì có số đo bằng nửa số đo của góc ở tâm chắn cùng một cung."),
    ("1. GÓC NỘI TIẾP", "text", "\\nhanly{Nhận xét.} Trong một đường tròn:",
     "\\nhanly{Nhận xét.} Đối với các góc nội tiếp của một đường tròn:"),
    ("Ví dụ 2.", "text", "(cùng cách đều trung điểm cạnh huyền)", "(hai đỉnh góc vuông cùng nhìn đoạn $BC$)"),
    ("Ví dụ 2.", "text", "[[fill:$\\widehat{MED}$]]$", "[[fill:\\widehat{MED}]]$"),
    ("Bài 2.", "statement", "[[br]]\\textbf{a)} $DN", "[[br]]$DN"),
    ("Bài 2.", "statement",
     "[[br]]\\textbf{b)} Xét đường tròn đường kính $AD$ (câu a):[[br]]$\\widehat{DNT}$ và $\\widehat{DAT}$ là [[blank:3.2cm]] cùng chắn cung $DT$.[[br]]Vậy $\\widehat{DNT} = \\widehat{DAT}$ ([[blank:3.2cm]]).",
     "[[br]]Xét đường tròn đường kính [[blank:1.1cm]] (câu a):[[br]]$\\widehat{DNT}$ và $\\widehat{DAT}$ là [[blank:3.2cm]] cùng chắn cung [[blank:1.1cm]].[[br]]Vậy $\\widehat{DNT} = \\widehat{DAT}$."),
    ("Bài 2.", "answer", "b) hai góc nội tiếp, hai góc nội tiếp cùng chắn cung $DT$",
     "b) $AD$, hai góc nội tiếp, $DT$"),
    ("Bài 3.", "statement", "[[br]]\\textbf{a)} $AB", "[[br]]$AB"),
    ("Bài 4.", "answer", "$F$ thuộc tia $AC$ (giả thiết)", "$F$ thuộc tia $AC$ (Hình 7)"),
    ("BTVN 4.", "answer", "[[br]]Vậy $\\widehat{ANM} = \\widehat{ABC}$.",
     "[[br]]Vậy $\\widehat{ANM} = \\widehat{ABC}$ ($H$ thuộc cạnh $BC$)."),
    ("Ví dụ 1.", "text", "[[fill:hai góc nội tiếp cùng chắn cung $ED$]]", "[[fill:hai góc nội tiếp cùng chắn một cung]]"),
    ("Ví dụ 1.", "text", "Gọi $O$ là trung điểm của cạnh $AC$. Đường tròn tâm $O$ đường kính $AC$",
     "Đường tròn tâm $O$ đường kính $AC$"),
]

THE2 = ("Đường tròn ngoại tiếp tam giác vuông có tâm là trung điểm của cạnh huyền và bán kính bằng một nửa "
        "cạnh huyền. (SGK Toán 9 tập hai, tr.73)[[br]]"
        "Vì vậy đỉnh góc vuông thuộc đường tròn đường kính là cạnh huyền.[[br]]"
        "Trên hình: $\\triangle ACB$ vuông tại $C$, $\\triangle ADB$ vuông tại $D$[[br]]"
        "$\\Rightarrow A, B, C, D$ cùng thuộc đường tròn đường kính $AB$ (tứ giác $ACDB$ nội tiếp).")


def main():
    p = REPO / SEED
    f = json.loads(p.read_text())
    for nh, k, cu, moi in SUA:
        hit = 0
        for s in f["stages"]:
            for b in s["blocks"]:
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                ten = b.get("label") or b.get("title") or (m.group(1) if m else "")
                if ten.strip() != nh:
                    continue
                n = (b.get(k) or "").count(cu)
                if n:
                    b[k] = b[k].replace(cu, moi)
                    hit += n
        assert hit == 1, f"{nh}/{k}: khớp {hit} lần — {cu[:50]}"
    for s in f["stages"]:              # thẻ 2 viết gọn (bản Gemini lặp ý 3 lần, đẩy trắng nửa trang 2)
        for b in s["blocks"]:
            if b.get("title") == "2. ĐỈNH GÓC VUÔNG VÀ ĐƯỜNG TRÒN ĐƯỜNG KÍNH":
                b["text"] = THE2
            if b.get("title") == "DẠNG 2. BẮC CẦU QUA GÓC THỨ BA":   # luật 15/11: không lặp lại Ví dụ 2 ở thẻ
                i = b["text"].index("[[br]]Minh hoạ theo hình:")
                b["text"] = b["text"][:i] + ("[[br]]Trình bày: mỗi đẳng thức góc một dòng, ghi rõ xét đường tròn nào "
                                             "và hai góc cùng chắn cung nào.")
                b.pop("figure", None)
    p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("đã sửa", len(SUA), "chỗ")


if __name__ == "__main__":
    main()
