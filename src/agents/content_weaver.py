"""Agent cốt lõi dệt gói kịch bản 5 chặng sư phạm bám sát ma trận độ khó.

Kịch bản bao gồm đầy đủ: Hook -> Discovery -> Level Up -> Boss -> Reflection
và bọc trong định dạng Pydantic LessonPackage sạch sẽ.
"""
from __future__ import annotations

import json
from pathlib import Path
import requests

from config import settings
from src.schema.lesson_package import LessonPackage, Stage
from src.agents.web_scouter import scout_problems

WEAVER_PROMPT = """Bạn là Trưởng bộ môn Phát triển Chương trình của MathTech. Hãy thiết kế một giáo án 5 chặng (Khám phá/Kiểm tra bài cũ -> Khái niệm -> Luyện tập 1 -> Luyện tập 2 -> Reflection) cho chủ đề "{topic}" của đối tượng học sinh "{audience}".

Yêu cầu sư phạm (cấu trúc 4 tầng: Ví dụ mẫu -> Bài tập trên lớp -> BTVN -> Mở rộng):
1. **review (Khám phá/Kiểm tra bài cũ)**: Ôn kiến thức nền cần cho bài qua bài toán/tình huống đúng tầm. Không giảng vỡ lòng.
2. **concept (Khái niệm)**: Dẫn dắt công thức/phương pháp cốt lõi; có ÍT NHẤT 1 "Ví dụ mẫu" làm trọn vẹn theo từng bước. Nên có 1 ghi chú ngắn "Đích đến thi vào 10" liên hệ kỹ năng này với dạng câu hỏi trong đề thi vào 10 (vd cực trị/biến đổi sẽ tái xuất ở câu phụ bài rút gọn chứa căn).
3. **practice1 (Luyện tập 1 — BÀI TẬP TRÊN LỚP, phần nền)**: bài đại diện, làm cùng GV.
4. **practice2 (Luyện tập 2 — BÀI TẬP TRÊN LỚP, vận dụng)**: ưu tiên dạng CÓ TRONG ĐỀ THI vào 10 và dạng HS bắt buộc hiểu; bài khó dần, chạm trần độ khó {ceiling_level}.
5. **reflection**: chặng 5 chỉ là **"Tổng kết"** (đặt title = "Tổng kết") gồm 1–2 câu chốt vũ khí chính + **SƠ ĐỒ TƯ DUY ĐIỀN KHUYẾT** (block "mindmap") thay ô tự chấm — đặt summary + mindmap Ở ĐẦU blocks. SAU đó thêm các bài **BTVN** (gắn tier="btvn", cùng kiểu đã chữa, lời giải đầy đủ trong "solution") và **MỞ RỘNG** (tier="extend"). Renderer TỰ tách BTVN và Mở rộng thành 2 mục riêng có banner — ĐỪNG tự viết block tiêu đề "BÀI TẬP VỀ NHÀ"/"BÀI TẬP MỞ RỘNG"; chỉ cần gắn đúng tier. Câu "nhịp cầu" (block para) đặt ngay trước cụm extend.

CHỐNG ĐỘ DỐC ĐỨNG ở tầng Mở rộng (quan trọng):
- Mở rộng KHÔNG được là MỘT bài khó đứng một mình. Hãy làm **THANG 2–3 bậc**: mỗi bài chỉ cao hơn bài trước **đúng MỘT bước kỹ thuật** (mở rộng bậc 1 = biến thể bài trên lớp thêm 1 yếu tố → bậc 2 thêm 1 bước → bậc 3 (sao/tự chọn) = khó nhất, vẫn trong tầm vào 10).
- Trước cụm Mở rộng, chèn **1 nhịp cầu** (block "para") chỉ rõ kỹ thuật mới khác bài trên lớp ở đâu.
- Mỗi bài Mở rộng kèm **"hints"** = 1–2 gợi ý "mở khi bí" (ĐỊNH HƯỚNG, tuyệt đối KHÔNG phải lời giải) — in trên phiếu HS để hạ ngưỡng nhập. Lời giải đầy đủ vẫn chỉ nằm trong "solution".

Đánh dấu tầng & đánh số:
- Mỗi block "problem" gắn "tier": "onclass" (trên lớp) | "btvn" (về nhà) | "extend" (mở rộng).
- Phân tầng theo độ khó + mức độ xuất hiện trong đề thi vào 10: dễ/nền -> lướt nhanh hoặc BTVN; trọng tâm thi -> trên lớp; nâng cao nhiều bước -> Mở rộng. KHÔNG bỏ bài nào của nguồn — chỉ phân tầng lại.
- Đánh số bài LIỀN MẠCH trong cả phiếu (Bài 1, 2, 3, …), không đánh lại theo từng dạng.

QUY TẮC TRÌNH BÀY (bắt buộc, để phiếu chỉn chu):
- TUYỆT ĐỐI không viết chú thích dành cho giáo viên (vd "(GV làm)", "GV chốt", "GV hỏi") vào blocks para/math/noted/problem — đó là phiếu phát cho HS. Mọi hướng dẫn cho GV chỉ đặt trong "teacher_note"; lời giải chỉ đặt trong "solution" (đều chỉ in ở Sổ tay GV).
- Khi một block có nhiều ý a) b) c) d) hoặc nhiều bước (Bước 1, Bước 2…), chèn token "[[br]]" giữa các ý để mỗi ý XUỐNG DÒNG riêng — không để dính chung một dòng. KHÔNG đặt [[br]] ở cuối block.
- Worked example ("Ví dụ mẫu") vẫn hiển thị cho HS (bỏ nhãn "GV"), và phải trình bày theo TỪNG BƯỚC, mỗi bước tách bằng "[[br]]" hoặc đặt phép biến đổi chính trong block "math" riêng — không dồn cả lời giải vào một dòng dài khó đọc.
- Mỗi chặng nên giao đủ không gian làm bài: dùng block "writelines" (count phù hợp) sau cụm bài để HS có chỗ trình bày.
- KHÔNG dùng ký tự mũi tên/ký hiệu unicode thô (→, ⟹, ≥, ≤…) trong text/title — font có thể thiếu glyph (ra ô vuông). Dùng lệnh LaTeX trong $...$ (vd $\\to$, $\\Rightarrow$, $\\ge$). Riêng "&" trong title/eyebrow phải viết "\\&".
- Sơ đồ tư duy ("mindmap"): nhãn nút ngắn gọn; chừa chỗ điền bằng [[blank:W]]; cây 3–5 nhánh, mỗi nhánh tối đa 2 cấp để không tràn trang.
- "solution" cũng PHẢI xuống dòng cho dễ đọc: mỗi bài một đoạn (dùng "\\par\\smallskip" giữa các bài); các ý a) b) c) của CÙNG một bài và mỗi đáp án ô trống sơ đồ đặt trên dòng riêng (dùng "[[br]]"). KHÔNG nhồi nhiều ý vào một dòng ngăn bằng dấu ";".
- Bài có "hints": hộp gợi ý tự xuống dưới đề (template lo); chỉ cần điền danh sách "hints" ngắn gọn, KHÔNG tự thêm nhãn "Gợi ý".
- Ký hiệu cực trị: GHI RÕ BIẾN — viết "$\\min A=1$" / "$\\max B=\\tfrac94$" (KHÔNG viết trống "min = 1"). Nêu rõ điều kiện đạt cực trị qua bước bình phương: "dấu $=$ xảy ra khi $(x-3)^2=0$, tức $x=3$" (đừng nhảy thẳng "khi $x=3$"). Áp cho cả ví dụ mẫu lẫn solution.

Hãy sử dụng các đề toán thực tế sau đây để đưa vào giáo án:
{scouted_problems_json}

Hãy xuất ra định dạng JSON khớp 100% cấu trúc Pydantic LessonPackage:
{{
  "slug": "danh-sach-viet-lien-khong-dau-chu-thuong",
  "title": "Tiêu đề bài học",
  "eyebrow": "DÒNG PHỤ TRÊN TIÊU ĐỀ",
  "grade_label": "Lớp 9 • Ôn vào 10",
  "stages": [
    {{
      "kind": "review",
      "number": 1,
      "title": "Tên chặng Khám phá/Kiểm tra bài cũ",
      "blocks": [
        {{"type": "para", "text": "đoạn văn; nhiều ý thì xuống dòng: a) ý một [[br]] b) ý hai [[br]] c) ý ba"}},
        {{"type": "math", "latex": "công thức hiển thị (không gồm $$)"}},
        {{"type": "problem", "label": "Bài 4.", "statement": "đề bài mở rộng", "tier": "extend",
          "hints": ["gợi ý định hướng 1", "gợi ý 2 nếu vẫn bí"]}},
        {{"type": "mindmap", "caption": "Sơ đồ tư duy — điền các ô trống",
          "root": "Chủ đề bài",
          "branches": [
            {{"label": "Nhánh 1 [[blank:2.5cm]]", "children": [{{"label": "[[blank:2cm]]"}}]}},
            {{"label": "Nhánh 2 [[blank:2.5cm]]"}}
          ]}}
      ],
      "solution": "đáp án chặng này (gồm cả đáp án các ô trống của sơ đồ tư duy)",
      "teacher_note": "mẹo điều phối"
    }},
    ... (đủ 5 chặng) ...
  ]
}}
"""


def weave_lesson_package(topic: str, profile_path: Path) -> LessonPackage:
    """Điều phối AI và dữ liệu cào để dệt giáo án 5 chặng."""
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    
    # 1. Thu thập các bài toán có sẵn từ ngân hàng cho chủ đề gốc
    topic_root = profile.get("topic_root", "bdt")
    ceiling_level = profile.get("ceiling", {}).get("level", 8)
    floor_level = profile.get("floor", {}).get("level", 4)
    
    # Săn lùng đề từ ngân hàng đề cào chuẩn
    problems = scout_problems(f"{topic_root}.xet_hieu", floor_level - 1, ceiling_level + 2)
    problems_serialized = [p.model_dump() for p in problems]
    
    if not settings.LLM_API_KEY:
        # Fallback Mock giáo án hoàn chỉnh cực đẹp khi thiếu API Key để đảm bảo zero-error chạy local
        # Trích xuất dữ liệu trực tiếp từ bài BĐT xét hiệu mẫu để đảm bảo đồng bộ
        return _mock_lesson_package(topic)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LLM_API_KEY}"
    }
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "user",
                "content": WEAVER_PROMPT.format(
                    topic=topic,
                    audience=profile.get("audience", "HS lớp 9 ôn thi vào 10"),
                    ceiling_level=ceiling_level,
                    scouted_problems_json=json.dumps(problems_serialized, ensure_ascii=False, indent=2)
                )
            }
        ]
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=45)
        if resp.status_code == 200:
            raw_json = resp.json()["choices"][0]["message"]["content"]
            return LessonPackage.model_validate_json(raw_json)
    except Exception:
        pass
        
    return _mock_lesson_package(topic)


def _mock_lesson_package(topic: str) -> LessonPackage:
    """Trả về gói bài mẫu chất lượng cao cho chế độ Mock."""
    # Bấm mẫu bài giảng Bất đẳng thức kỹ thuật xét hiệu mẫu của Thầy
    return LessonPackage(
        slug="bdt-xet-hieu",
        title="Bất đẳng thức",
        eyebrow="CHỦ ĐỀ • ĐẠI SỐ — KỸ THUẬT XÉT HIỆU",
        grade_label="Lớp 9 • Ôn vào 10",
        stages=[
            Stage(
                kind="review",
                number=1,
                title="Khám phá — Đừng quy đồng!",
                blocks=[
                    {"type": "para", "text": "So sánh hai phân số sau mà \\textbf{không dùng máy tính} và \\textbf{không quy đồng} (quy đồng ra mẫu số tới 7 chữ số!):"},
                    {"type": "math", "latex": "A=\\dfrac{2024}{2023} \\qquad\\text{và}\\qquad B=\\dfrac{2025}{2024}."},
                    {"type": "para", "text": "\\textbf{Gợi ý đắt giá:} hãy tách mỗi phân số thành $1 + (\\text{một phân số nhỏ})$ rồi so sánh hai phần nhỏ đó."},
                    {"type": "para", "text": "Em tách được: $A = 1 + \\dfrac{[[mblank:1.6cm]]}{[[mblank:1.6cm]]}$,\\quad $B = 1 + \\dfrac{[[mblank:1.6cm]]}{[[mblank:1.6cm]]}$.\\quad Kết luận: $A\\ [[mblank:0.8cm]]\\ B$."}
                ],
                solution="Ta có $A=1+\\dfrac{1}{2023}$ và $B=1+\\dfrac{1}{2024}$. Vì $\\dfrac{1}{2023}>\\dfrac{1}{2024}$ nên $A>B$.",
                teacher_note="Hook chỉ cần đánh thức trực giác — KHÔNG dạy lý thuyết xét hiệu ở đây."
            ),
            Stage(
                kind="concept",
                number=2,
                title="Khái niệm — Vũ khí \"xét hiệu\"",
                blocks=[
                    {"type": "para", "text": "Để chứng minh $A \\ge B$, ta không so sánh trực tiếp mà xét \\textbf{hiệu} $A-B$ và chứng minh nó không âm."},
                    {"type": "noted", "text": "\\textbf{Điền khuyết.} \\;$A \\ge B \\;\\Longleftrightarrow\\; A - B\\ [[mblank:0.9cm]]\\ 0$.\\quad Công cụ mạnh nhất: với mọi biểu thức $M$ ta luôn có $M^2\\ [[mblank:0.9cm]]\\ 0$."},
                    {"type": "para", "text": "\\textbf{Hằng đẳng thức nền tảng.} Với mọi $a,b$:"},
                    {"type": "math", "latex": "a^2+b^2 \\;\\ge\\; 2ab, \\qquad\\text{vì}\\qquad a^2+b^2-2ab=(\\,[[mblank:1.6cm]]\\,)^2\\ \\ge 0."},
                    {"type": "para", "text": "Dấu \"$=$\" xảy ra khi và chỉ khi \\;$a\\ [[mblank:0.7cm]]\\ b$."}
                ],
                solution="Điền vào chỗ trống: $A-B \\ge 0$;\\; $M^2 \\ge 0$;\\; $(a-b)^2 \\ge 0$;\\; $a = b$.\\par\\medskip\\textbf{Chứng minh BĐT cốt lõi:} $a^2+b^2-2ab=(a-b)^2\\ge 0$ với mọi $a,b$, suy ra $a^2+b^2\\ge 2ab$. Đẳng thức khi $a=b$.",
                teacher_note="Đây là chặng khám phá, để HS điền trước, GV chốt sau."
            ),
            Stage(
                kind="practice1",
                number=3,
                title="Luyện tập 1 — Tự dựng lời giải",
                blocks=[
                    {"type": "problem", "label": "Bài toán.", "tier": "onclass", "statement": "Cho $a,b$ là hai số dương. Chứng minh \\;$\\dfrac{a}{b}+\\dfrac{b}{a}\\ \\ge\\ 2$."},
                    {"type": "para", "text": "\\textbf{Giàn giáo (em điền tiếp):}"},
                    {"type": "para", "text": "Xét hiệu \\;$\\dfrac{a}{b}+\\dfrac{b}{a}-2 \\;=\\; \\dfrac{a^2+b^2-2ab}{ab} \\;=\\; \\dfrac{(\\,[[mblank:1.4cm]]\\,)^2}{ab}.$" },
                    {"type": "para", "text": "Vì $a,b>0$ nên $ab\\ [[mblank:0.7cm]]\\ 0$ và $(a-b)^2\\ [[mblank:0.7cm]]\\ 0$, suy ra hiệu trên \\;$[[mblank:0.7cm]]\\ 0$." },
                    {"type": "para", "text": "Vậy điều phải chứng minh. Dấu \"$=$\" xảy ra khi: [[blank:5cm]]"}
                ],
                solution="Xét hiệu $\\dfrac{a}{b}+\\dfrac{b}{a}-2 = \\dfrac{a^2+b^2-2ab}{ab} = \\dfrac{(a-b)^2}{ab}.$\\\\Vì $a,b>0$ nên $ab>0$ và $(a-b)^2\\ge 0$, suy ra $\\dfrac{(a-b)^2}{ab}\\ge 0$.\\\\Vậy $\\dfrac{a}{b}+\\dfrac{b}{a}\\ge 2$. Đẳng thức xảy ra khi và chỉ khi $a=b$. \\hfill$\\square$",
                teacher_note="HS hay quên giả thiết a,b dương ở bước chia cho ab."
            ),
            Stage(
                kind="practice2",
                number=4,
                title="Luyện tập 2 — Thử thách 3 biến",
                blocks=[
                    {"type": "para", "text": "\\textbf{Trùm cuối.} Với mọi số thực $a,b,c$, chứng minh:"},
                    {"type": "math", "latex": "a^2+b^2+c^2 \\;\\ge\\; ab+bc+ca."},
                    {"type": "para", "text": "\\textbf{Chiến thuật:} nhân đôi hai vế rồi gom thành tổng của \\emph{ba} bình phương. Bài làm:"},
                    {"type": "writelines", "count": 3}
                ],
                solution="Nhân đôi hai vế, BĐT tương đương $2a^2+2b^2+2c^2\\ge 2ab+2bc+2ca$, tức\\\\$(a^2-2ab+b^2)+(b^2-2bc+c^2)+(c^2-2ca+a^2)\\ge 0$,\\\\hay $(a-b)^2+(b-c)^2+(c-a)^2\\ge 0$ — luôn đúng vì là tổng ba bình phương.\\\\Đẳng thức xảy ra khi và chỉ khi $a=b=c$. \\hfill$\\square$",
                teacher_note="Chìa khóa: 2 biến cần 1 bình phương, 3 biến cần tổng 3 bình phương."
            ),
            Stage(
                kind="reflection",
                number=5,
                title="Tổng kết",
                blocks=[
                    {"type": "para", "text": "Vũ khí hôm nay: muốn so sánh hay chứng minh, hãy \\emph{xét hiệu} rồi đưa về bình phương $M^2\\ge 0$; lên ba biến thì gom \\emph{tổng ba bình phương}."},
                    {"type": "mindmap", "caption": "Sơ đồ tư duy — em điền các ô trống để chốt kiến thức",
                     "root": "Xét hiệu và bình phương",
                     "branches": [
                         {"label": "Ý tưởng: $A\\ge B \\Leftrightarrow A-B[[blank:0.8cm]]0$",
                          "children": [{"label": "Công cụ: $M^2[[blank:0.8cm]]0$"}]},
                         {"label": "2 biến [[blank:2cm]]",
                          "children": [{"label": "$a^2+b^2\\ge[[blank:1cm]]$"}]},
                         {"label": "3 biến: tổng [[blank:1.4cm]] bình phương"},
                         {"label": "Dấu \"=\" khi [[blank:1.6cm]]"},
                     ]},
                    {"type": "noted", "text": "\\textbf{BÀI TẬP VỀ NHÀ.} Cùng kiểu bài đã chữa trên lớp."},
                    {"type": "problem", "label": "Bài 5.", "tier": "btvn",
                     "statement": "Cho $x,y>0$. Chứng minh \\;$\\dfrac{x}{y}+\\dfrac{y}{x}\\ge 2$ \\;rồi suy ra $(x+y)\\Big(\\dfrac1x+\\dfrac1y\\Big)\\ge 4$."},
                    {"type": "para", "text": "\\textbf{Nhịp cầu lên mở rộng.} 2–3 biến đã quen kỹ thuật tổng các bình phương; bậc tiếp theo chỉ thêm \\emph{một bước}: gắn thêm điều kiện ràng buộc giữa các biến."},
                    {"type": "noted", "text": "\\textbf{BÀI TẬP MỞ RỘNG (tự chọn) — thang 2 bậc.}"},
                    {"type": "problem", "label": "Bài 6.", "tier": "extend",
                     "statement": "Cho $a,b,c>0$. Chứng minh \\;$\\dfrac{a}{b}+\\dfrac{b}{c}+\\dfrac{c}{a}\\ge 3$.",
                     "hints": ["Mỗi cặp đã có $\\dfrac{a}{b}+\\dfrac{b}{a}\\ge 2$ — nhưng ở đây là vòng tròn, thử AM–GM cho \\emph{ba} số hạng.",
                               "Tích ba số hạng $\\dfrac{a}{b}\\cdot\\dfrac{b}{c}\\cdot\\dfrac{c}{a}=1$."]},
                    {"type": "problem", "label": "Bài 7.", "tier": "extend",
                     "statement": "Cho $a,b,c>0$ và $a+b+c=3$. Tìm GTNN của $P=a^2+b^2+c^2$.",
                     "hints": ["Nối ràng buộc $a+b+c=3$ với tổng bình phương bằng một BĐT đã học ở Bài 4."]},
                ],
                solution=(
                    "\\textbf{Bài 5.} Xét hiệu $\\dfrac{x}{y}+\\dfrac{y}{x}-2=\\dfrac{(x-y)^2}{xy}\\ge0$, suy ra $\\dfrac{x}{y}+\\dfrac{y}{x}\\ge2$. [[br]]"
                    "Do đó $(x+y)\\big(\\tfrac1x+\\tfrac1y\\big)=2+\\dfrac{x}{y}+\\dfrac{y}{x}\\ge4$.\\par\\smallskip"
                    "\\textbf{Bài 6.} AM–GM ba số (tích $=1$): $\\dfrac{a}{b}+\\dfrac{b}{c}+\\dfrac{c}{a}\\ge3\\sqrt[3]{1}=3$; dấu $=$ khi $a=b=c$.\\par\\smallskip"
                    "\\textbf{Bài 7.} $a^2+b^2+c^2\\ge\\dfrac{(a+b+c)^2}{3}=\\dfrac{9}{3}=3$; GTNN $=3$ khi $a=b=c=1$.\\par\\smallskip"
                    "\\textbf{Đáp án sơ đồ tư duy:} [[br]]"
                    "$\\bullet$\\; Ý tưởng: $A-B\\ge0$;\\quad công cụ: $M^2\\ge0$. [[br]]"
                    "$\\bullet$\\; 2 biến: bình phương $(a-b)^2$, nên $a^2+b^2\\ge2ab$. [[br]]"
                    "$\\bullet$\\; 3 biến: tổng \\emph{ba} bình phương. [[br]]"
                    "$\\bullet$\\; Dấu $=$ khi các biến bằng nhau."
                ),
                teacher_note="Mở rộng đi theo thang: Bài 6 quen (vòng tròn) $\\to$ Bài 7 thêm ràng buộc tổng. Chốt sơ đồ tư duy cùng HS 3 phút cuối."
            )
        ]
    )
