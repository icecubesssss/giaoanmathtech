"""Cấu trúc tích hợp cả 5 chặng của buổi học — khóa cứng giữa AI và template Jinja2.

AI chỉ tạo ra dữ liệu theo schema này (đề + lời giải + bố cục khối nội dung),
TUYỆT ĐỐI không tạo mã LaTeX giao diện. Khối nội dung được dựng từ các Block
nguyên thủy; chỗ trống cho HS điền dùng token [[blank]] / [[mblank:W]] trong text,
do renderer dịch sang lệnh LaTeX an toàn (xem src/compiler/jinja_renderer.py).
"""
from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import BaseModel, Field

# ----- Các Block nội dung nguyên thủy (discriminated union theo 'type') -----


class ParaBlock(BaseModel):
    type: Literal["para"] = "para"
    text: str = Field(..., description="Đoạn văn; cho phép $...$ và token [[blank]]")
    # TIÊU ĐỀ MỤC trong khối lý thuyết ("1. Đường tròn", "2. Vị trí của một điểm…").
    # Trước 22/09/2026 chỉ gõ `\textbf{1. Đường tròn}` nên tiêu đề CHÌM vào thân bài:
    # cùng cỡ chữ, cùng màu, không có khoảng thở phía trên ⇒ cả khối lý thuyết đọc
    # thành một mảng chữ đặc (Thầy chê: "lý thuyết quá khó nhìn"). Variant này cho
    # tiêu đề màu brand, chữ sans, và khoảng cách rõ phía trên.
    variant: Literal["", "heading"] = Field(
        "", description="'heading' = tiêu đề mục trong khối lý thuyết; rỗng = đoạn văn thường"
    )


class MathBlock(BaseModel):
    type: Literal["math"] = "math"
    latex: str = Field(..., description="Công thức hiển thị giữa dòng (không kèm $$)")


class DefItem(BaseModel):
    """MỘT mục của danh sách định nghĩa: thuật ngữ + phần giải thích."""
    term: str = Field(..., description="Thuật ngữ / vế trái, vd 'Bán kính' hoặc '$OM < R \\Rightarrow$'")
    desc: str = Field(..., description="Phần giải thích; cho phép $...$ và [[blank]]")


class DefListBlock(BaseModel):
    """DANH SÁCH ĐỊNH NGHĨA — mỗi mục MỘT DÒNG RIÊNG, thuật ngữ nổi bật, phần giải
    thích thụt vào cho thẳng hàng.

    Vì sao có block này (Thầy chốt 22/09/2026 — "lý thuyết quá khó nhìn, cần xuống
    dòng hãy cứ xuống"): khối lý thuyết trước đây gõ tay cấu trúc vào giữa `para`:

        "$\\bullet$ \\textbf{Bán kính}: … \\quad $\\bullet$ \\textbf{Dây cung}: …"

    Hai định nghĩa bị `\\quad` dán vào CÙNG một dòng rồi tự ngắt dòng ở chỗ ngẫu
    nhiên, nên mắt không tách được đâu là mục mới. Y hệt bệnh trộn bố cục vào nội
    dung ở `ProblemBlock.statement`. Khai thành `items` thì template tự xuống dòng,
    tự canh thụt đầu dòng — người soạn khỏi nhẩm `\\quad` hay `\\hspace`.

    Dùng cho cả danh sách TRƯỜNG HỢP (viết dấu suy ra vào cuối `term`):
        term = "$OM < R \\Rightarrow$" · desc = "$M$ nằm \\textbf{trong} đường tròn"
    """
    type: Literal["deflist"] = "deflist"
    items: list[DefItem] = Field(default_factory=list, description="Các mục, mỗi mục một dòng")


class ProblemFigure(BaseModel):
    """HÌNH ĐI KÈM MỘT BÀI — tách khỏi `statement` để template tự canh chỗ.

    `pos` là Ý ĐỊNH của người soạn, không phải lệnh cứng: renderer vẫn hạ hình xuống
    dưới nếu đề quá dài để đứng cạnh hình (xem `fig_side` trong jinja_renderer).
      • right = treo bên phải đề (mặc định, kiểu SGK)
      • below = đặt dưới đề, căn giữa
      • none  = KHÔNG vẽ ở bản in; bài chỉ TRỎ sang hình của bài trước qua `ref`

    `ref` cho bài dùng lại hình của bài khác ("Vẫn trên Hình 6"). Bản in A4 khỏi vẽ
    lại vì hình nằm ngay trên, nhưng SLIDE thì PHẢI vẽ lại — mỗi bài một slide riêng,
    không có hình thì HS nhìn vào câu hỏi trỏ tới một hình không tồn tại."""
    tikz: str = Field("", description="Mã TikZ đầy đủ \\begin{tikzpicture}…\\end{tikzpicture}")
    image: str = Field("", description="Đường dẫn ảnh TƯƠNG ĐỐI folder phiếu; để trống nếu dùng tikz")
    caption: str = Field("", description="Nhãn hình, vd 'Hình 6'")
    pos: Literal["right", "below", "none"] = Field("right", description="Chỗ đặt hình so với đề")
    ref: str = Field("", description="Nhãn hình của bài khác mà bài này dùng lại, vd 'Hình 6'")


class NotedBlock(BaseModel):
    type: Literal["noted"] = "noted"
    text: str = Field(..., description="Nội dung trong hộp nền xám (vd ô điền khuyết)")
    text_slide: str = Field("", description="Nội dung riêng cho Slide (nếu khác text bản in)")
    # Thẻ callout có nhãn màu + icon. "" = hộp xám trung tính như cũ (tương thích ngược).
    #   trap   = "BẪY ĐIỂM" (đỏ, cảnh báo lỗi hay mất điểm)
    #   target = "ĐÍCH THI VÀO 10" (vàng, chốt mục tiêu thi)
    #   tip    = "MẸO" (tím, mẹo nhanh)
    #   example= "VÍ DỤ MẪU" (xanh dương)
    variant: Literal["", "note", "trap", "target", "tip", "example"] = Field(
        "", description="Kiểu thẻ callout; rỗng = hộp xám trung tính như cũ"
    )
    # Hình đi kèm hộp (ví dụ mẫu / mở màn có hình). Trước 22/09/2026 phải gõ tay hai
    # `\begin{minipage}[t]{0.58\linewidth}` cạnh nhau ngay trong `text` — cùng bệnh
    # trộn bố cục vào nội dung như `ProblemBlock.statement`, và minipage thì KHÔNG cắt
    # trang được nên hộp rơi sát đáy là nhảy nguyên khối sang trang sau.
    figure: Optional["ProblemFigure"] = Field(
        None, description="Hình đi kèm hộp; None = hộp chỉ có chữ"
    )

    @property
    def layout_moi(self) -> bool:
        return self.figure is not None


class WriteLinesBlock(BaseModel):
    type: Literal["writelines"] = "writelines"
    count: int = Field(2, ge=0, le=12, description="Số dòng kẻ trống cho HS viết (0 = chỉ chừa 1 dòng trắng, KHÔNG kẻ — lớp HS trình bày vào vở)")
    variant: Optional[str] = Field(
        None,
        description="Variant của block: 'oly' = lưới ô ly tiểu học; "
                    "'draw' = KHUNG TRỐNG cho HS tự vẽ hình (count = chiều cao cm); "
                    "None = dòng kẻ chấm để viết",
    )


# ----- Đáp án MÁY-ĐỌC để validate tự soi bằng SymPy (tùy chọn, KHÔNG in ra phiếu) -----


class SolvesetCheck(BaseModel):
    """Kiểm nghiệm phương trình một ẩn (→ sympy_solver.check_solution_set)."""
    kind: Literal["solveset"] = "solveset"
    equation: str = Field(..., description="PT dạng 'lhs = rhs' hoặc 'expr = 0' (LaTeX/text)")
    answer: list[Union[str, int, float]] = Field(..., description="Tập nghiệm người tuyên bố, vd [2, 3]")
    symbol: str = Field("x", description="Tên ẩn (mặc định x)")


class IdentityCheck(BaseModel):
    """Kiểm đẳng thức hai vế (→ sympy_solver.verify_identity)."""
    kind: Literal["identity"] = "identity"
    lhs: str = Field(..., description="Vế trái")
    rhs: str = Field(..., description="Vế phải")


class NonnegCheck(BaseModel):
    """Kiểm 'biểu thức bậc hai >= 0 với mọi biến thực' (→ sympy_solver.prove_quadratic_nonneg)."""
    kind: Literal["nonneg"] = "nonneg"
    expr: str = Field(..., description="Biểu thức bậc hai thuần nhất, vd 'a**2+b**2-2*a*b'")
    symbols: list[str] = Field(..., description="Danh sách biến, vd ['a','b']")


AnswerCheck = Union[SolvesetCheck, IdentityCheck, NonnegCheck]


class ProblemBlock(BaseModel):
    type: Literal["problem"] = "problem"
    label: str = Field(..., description="Nhãn, vd 'Bài 1.' / 'Bài toán.'")
    statement: str = Field(..., description="Đề bài (LaTeX inline cho phép)")
    statement_slide: str = Field(
        "", description="Đề bài riêng cho Slide (nếu khác statement bản in, vd bài điền khuyết rút gọn còn đề)"
    )
    # Tầng bài = NƠI LÀM (đặt mục + gradient gate): "" | onclass | btvn | extend.
    tier: Literal["", "onclass", "btvn", "extend"] = Field(
        "", description="onclass=trên lớp, btvn=về nhà, extend=mở rộng/nâng cao"
    )
    # MỨC ĐỘ NHẬN THỨC (Bloom) → SỐ SAO in trên phiếu. ĐỘC LẬP với `tier` (nơi làm):
    # một bài btvn vẫn có thể là mức Vận dụng (3 sao). Định nghĩa CHỐT:
    #   1 = Nhận biết   (★☆☆, vàng)  : 1 bước, nhận ra / áp dụng TRỰC TIẾP 1 công thức,
    #                                   định nghĩa, quy tắc — "nhìn phát thấy ngay".
    #   2 = Thông hiểu  (★★☆, vàng)  : 1–2 bước, phải hiểu quan hệ rồi mới suy ra
    #                                   (giải thích, so sánh, biến đổi/tính toán cơ bản).
    #   3 = Vận dụng    (★★★, vàng)  : 2–4 bước, ghép nhiều ý cùng chủ đề / bài thực tế
    #                                   ĐƠN GIẢN (lãi suất, lập kế hoạch, %, đo đạc).
    #   4 = Vận dụng cao (◆◆◆◆, MÀU KIM CƯƠNG): đa tầng, không giải "rập khuôn"
    #                                   (chứng minh BĐT, tìm cực trị, đổi biến phức tạp…).
    #   0 = chưa chấm → renderer tự suy sao từ `tier` (tương thích ngược file cũ);
    #       visual_linter sẽ nhắc gắn level.
    level: Literal[0, 1, 2, 3, 4] = Field(
        0, description="Mức nhận thức→số sao: 1 NB, 2 TH, 3 VD, 4 VD cao (kim cương); 0=chưa chấm"
    )
    # Gợi ý phân tầng "mở khi bí" — IN TRÊN PHIẾU HS (định hướng, KHÔNG phải lời
    # giải). Hạ ngưỡng nhập cho bài khó mà không lộ đáp án (lời giải vẫn ở solution).
    hints: list[str] = Field(
        default_factory=list, description="Gợi ý mở dần, mỗi phần tử một gợi ý; cho phép $...$ và [[blank]]"
    )
    # QUY TRÌNH GIẢI BÀI — Thầy chốt 30/08/2026: mọi bài VẬN DỤNG (level 3) của phiếu
    # tầng B phải in sẵn các bước giải NGAY TẠI BÀI, không để HS mò. Khác `hints`
    # (gợi ý mở khi bí): quy trình LUÔN hiện trên phiếu HS và là khuôn để HS bám.
    quy_trinh: list[str] = Field(
        default_factory=list,
        description="Các BƯỚC của quy trình giải, vd ['Bước 1 — vẽ hình…', 'Bước 2 — …']",
    )
    # LỜI GIẢI của RIÊNG bài này — CHỈ in ở Sổ tay GV (`show_solution=True` trong
    # `_blocks.j2`), tuyệt đối không lọt sang phiếu HS / slide. Trước 2026-08-12 field
    # này KHÔNG tồn tại: seed viết `solution` cho từng bài thì pydantic lặng lẽ vứt đi
    # và guide.pdf ra trắng đáp án. Dùng [[br]] tách từng bước cho dễ đọc.
    solution: str = Field(
        "", description="Lời giải đầy đủ của bài (chỉ hiện ở Sổ tay GV); dùng [[br]] xuống dòng"
    )
    # ĐÁP ÁN GỌN một dòng ('B' / '$R = 5$ cm') — cũng CHỈ in ở Sổ tay GV. Khác `solution`
    # (lời giải đầy đủ từng bước): dùng cho câu trắc nghiệm và câu hỏi đáp nhanh, nơi
    # viết cả bài giải là thừa.
    # ⚠️ LẦN THỨ BA repo dính đúng một họ lỗi: trước 22/09/2026 field này KHÔNG tồn tại,
    # nhưng 43 bài chương V lớp 9C vẫn khai "answer": … ⇒ pydantic ÂM THẦM vứt đi, và 32
    # bài trong số đó không có `solution` nên guide.pdf in ra TRẮNG ĐÁP ÁN. Y hệt vụ
    # `solution` (12/08/2026, xem trên) và `writelines` (15/08/2026, xem dưới). Cả ba lần
    # đều không cổng nào kêu vì pydantic mặc định BỎ QUA khoá lạ — nay `schema_validator`
    # có cảnh báo "JSON có khoá lạ" để chặn hẳn họ lỗi này.
    answer: str = Field(
        "", description="Đáp án gọn một dòng (chỉ hiện ở Sổ tay GV); dùng cho trắc nghiệm / hỏi đáp nhanh"
    )
    # ── BỐ CỤC CÓ CẤU TRÚC (22/09/2026) — nội dung ở TRƯỜNG, LaTeX bố cục do template sinh ──
    # Trước đây ba thứ dưới đây được gõ tay bằng LaTeX ngay trong `statement`:
    #   • phương án trắc nghiệm bằng \parbox[t]{0.30\linewidth} × 4 → chỉ dùng 60% bề
    #     ngang, phí 40%, lại phải chèn \par\vspace{6pt} giữa hai hàng;
    #   • hộp hình bằng \makebox[0pt][l]{\hspace{0.62\linewidth}\smash{\raisebox{-1.75cm}…;
    #   • \vspace{1.63cm} cuối đề để né hình — con số AI phải NHẨM TAY cho từng bài
    #     (nhẩm dư ⇒ khoảng trắng chết, nhẩm thiếu ⇒ chữ đè hình).
    # Khai vào trường thì template biết chiều cao hộp hình THẬT nên tự canh, khỏi nhẩm.
    # Block CŨ (statement còn [[wrap]]/\makebox) vẫn render y như trước — xem `layout_moi`.
    options: list[str] = Field(
        default_factory=list,
        description="Phương án trắc nghiệm theo thứ tự A,B,C,D…; nhãn do template đánh. Rỗng = bài tự luận",
    )
    figure: Optional["ProblemFigure"] = Field(
        None, description="Hình đi kèm bài; None = bài không hình"
    )

    @property
    def layout_moi(self) -> bool:
        """True = bài đã tách nội dung khỏi bố cục ⇒ dùng đường render MỚI.

        Nhận biết bằng SỰ CÓ MẶT của trường mới, KHÔNG soi chuỗi `statement`: soi chuỗi
        thì một bài mới mà đề lỡ có `\\textbf` sẽ bị hiểu nhầm là bài cũ."""
        return bool(self.options or self.figure)

    def noi_dung_day_du(self) -> str:
        """TOÀN BỘ chữ HS đọc được của bài, gộp từ mọi trường — dùng cho CÁC CỔNG.

        Cổng nào đếm câu/soi chữ mà chỉ đọc `.statement` thì sau khi tách trường sẽ
        đếm hụt (vd `duration_gate` mất hết thẻ [NB] nằm trong phương án)."""
        phan = [self.statement, self.answer, *self.options]
        if self.figure is not None:
            phan += [self.figure.tikz, self.figure.caption, self.figure.ref]
        return " ".join(p for p in phan if p)
    # Đặc sản "QR video lời giải": URL video Thầy giải bài. Có giá trị → in QR nhỏ ở
    # lề phải bài (cầu nối giấy → điện thoại). Rỗng = không in QR (tương thích ngược).
    video: str = Field("", description="URL video lời giải; có → in QR cạnh bài")
    # Bài HÌNH mà HS phải TỰ VẼ HÌNH (đề không cho sẵn hình) — tốn thêm thời gian.
    # Thầy chốt 2026-07-26: mỗi bài như vậy cộng `draw_minutes` (5′) vào quỹ giờ,
    # tính MỘT LẦN cho cả bài (vẽ 1 hình dùng cho mọi ý a,b,c…). Chỉ là dữ liệu
    # tính giờ cho duration_gate — KHÔNG in gì thêm ra phiếu, nên đề bài vẫn phải
    # tự nói "Vẽ hình, ghi giả thiết – kết luận".
    draw: bool = Field(False, description="HS phải tự vẽ hình cho bài này → +draw_minutes vào quỹ giờ")
    # NGƯỢC LẠI với `draw`: bài HÌNH đã VẼ SẴN hình, HS chỉ đọc hình rồi chọn đáp án /
    # điền chỗ chấm (trắc nghiệm, điền khuyết). Thầy chốt 2026-07-27: "vẽ luôn hình để
    # trừ các khâu vẽ hình" — 1,5 tiếng chỉ chữa nổi 1–2 bài hình hẳn hoi, phần còn lại
    # dồn về trắc nghiệm / điền khuyết có hình sẵn. Rate hình ×2 (đọc đề, dựng hình,
    # trình bày) KHÔNG áp cho những bài này ⇒ phút/câu về lại mức đại số (×0,5).
    figure_given: bool = Field(
        False, description="Đề đã vẽ sẵn hình, HS chỉ đọc hình (trắc nghiệm/điền khuyết) → phút/câu ×0,5"
    )
    # MÃ DẠNG trỏ về đúng dòng của thuyet-minh.json cạnh bên: 'NB5', 'TH2', 'VD1'…
    # (đánh số theo THỨ TỰ TRONG NHÓM BAND của phiếu tương ứng, y như bảng thuyết minh in ra).
    # Thầy chốt 14/08/2026: "phiếu thật PHẢI TƯƠNG ỨNG THẬT RÕ phiếu thuyết minh" —
    # trước đây spec_gate chỉ so TỔNG số câu theo band nên phiếu lệch hẳn dạng mà cổng vẫn im.
    dang_id: str = Field(
        "", description="Mã dạng trong thuyet-minh.json, vd 'NB5' / 'TH2' / 'VD1'"
    )
    # (TÙY CHỌN) Đáp án MÁY-ĐỌC để `validate` tự soi bằng SymPy. None = bỏ qua (như cũ).
    # KHÔNG in ra phiếu — chỉ phục vụ answer_gate. Phân biệt loại bằng khóa "kind".
    check: Optional[AnswerCheck] = Field(
        None, description="Đáp án máy-đọc cho answer_gate; KHÔNG hiển thị trên phiếu"
    )
    # CHỖ VIẾT ngay dưới đề — tương đương một WriteLinesBlock đặt sau bài, nhưng khai
    # thẳng trên bài cho gọn. 0 = không chừa gì (bài trắc nghiệm, hoặc đề đã tự chừa
    # bằng \vspace ở cuối statement).
    # ⚠️ Trước 15/08/2026 field này KHÔNG tồn tại: 666 bài ở 30 phiếu khai "writelines": N
    # thì pydantic ÂM THẦM vứt đi ⇒ phiếu in ra HS KHÔNG có dòng nào để viết, bài nọ
    # dính vào bài kia. Y hệt vụ `solution` bị vứt làm guide.pdf trắng đáp án.
    writelines: int = Field(
        0, ge=0, le=12, description="Số dòng kẻ trống chừa ngay dưới đề (0 = không chừa)"
    )


class TableBlock(BaseModel):
    """Bảng (vd bảng đại lượng $s=v\\cdot t$) — IN RA BẢNG THẬT cho HS điền.

    QUY TẮC: hễ đề/ghi chú nhắc 'lập bảng / kẻ bảng' thì PHẢI có block này, không
    được nói suông. Mỗi ô cho phép $...$ và token [[blank:W]] để chừa chỗ HS điền.
    Số cột lấy theo `headers` (hoặc hàng đầu nếu không có headers)."""
    type: Literal["table"] = "table"
    caption: str = Field("", description="Chú thích nhỏ phía trên bảng")
    headers: list[str] = Field(default_factory=list, description="Hàng tiêu đề cột (in đậm)")
    rows: list[list[str]] = Field(default_factory=list, description="Các hàng; mỗi ô cho phép $...$ và [[blank:W]]")


class FigureBlock(BaseModel):
    """Hình minh hoạ hình học — VECTOR TikZ (ưu tiên) hoặc ảnh cắt từ phiếu gốc.

    Dùng cho mọi hình trong phiếu Hình học (tam giác, sơ đồ đo đạc…). Chọn MỘT
    trong hai nguồn:
      • `tikz`  : mã TikZ ĐẦY ĐỦ `\\begin{tikzpicture}...\\end{tikzpicture}`.
                  Ưu tiên dùng (sắc nét, sửa được, đồng bộ phong cách phiếu).
      • `image` : đường dẫn ảnh TƯƠNG ĐỐI so với folder phiếu (vd 'fig/thang.png'),
                  chỉ dùng khi không dựng lại chính xác bằng TikZ (ảnh thực tế).
    Renderer tự căn giữa và co cho vừa bề ngang (không tràn trang)."""
    type: Literal["figure"] = "figure"
    tikz: str = Field("", description="Mã TikZ đầy đủ \\begin{tikzpicture}...\\end{tikzpicture}; để trống nếu dùng ảnh")
    image: str = Field("", description="Đường dẫn ảnh tương đối folder phiếu (vd 'fig/x.png'); để trống nếu dùng tikz")
    caption: str = Field("", description="Chú thích nhỏ dưới hình; cho phép $...$")
    width: str = Field("", description="Bề rộng tối đa, vd '0.6\\linewidth'. Trống = tự co vừa khung")


class OpenerBlock(BaseModel):
    """Thẻ "MỞ MÀN THỰC TẾ" — hook đời thực mở đầu phiếu (đặc sản nhận diện).

    Thay câu mở khô khan bằng một tình huống/bài toán thực tế kéo HS vào bài
    (vd hai vòi nước → ẩn ở mẫu). Đặt ở ĐẦU chặng 'review'. Cho phép kèm ảnh
    minh hoạ (đường dẫn tương đối folder phiếu) ở cột phải."""
    type: Literal["opener"] = "opener"
    text: str = Field(..., description="Nội dung hook; cho phép $...$, [[br]], [[blank]]")
    image: str = Field("", description="Ảnh minh hoạ (đường dẫn tương đối folder phiếu); trống = chỉ chữ")
    tikz: str = Field("", description="Hình minh hoạ NÉT VẼ TikZ (\\begin{tikzpicture}…) ở cột phải — ưu tiên dùng cái này thay ảnh để in đen trắng sắc nét")


class MindmapNode(BaseModel):
    """Một nút trong sơ đồ tư duy điền khuyết. label có thể chứa [[blank:W]] để HS điền."""
    label: str = Field(..., description="Nhãn nút; cho phép $...$ và token [[blank]] để chừa chỗ điền")
    children: list["MindmapNode"] = Field(default_factory=list)


class MindmapBlock(BaseModel):
    """Sơ đồ tư duy điền khuyết — khung kiến thức bài học, HS điền các nút trống.

    AI/Thầy chỉ khai báo cây (root + branches), renderer dựng TikZ/forest.
    Dùng trong reflection thay cho ô tự chấm nhàm. size='large' cho phiếu tổng kết
    cả chương (Phase 2)."""
    type: Literal["mindmap"] = "mindmap"
    root: str = Field(..., description="Nhãn nút gốc (trung tâm sơ đồ)")
    branches: list[MindmapNode] = Field(default_factory=list)
    caption: str = Field("", description="Chú thích nhỏ phía trên sơ đồ, vd 'Điền các ô trống'")
    size: Literal["small", "large"] = Field("small", description="small=trong phiếu; large=phiếu tổng kết chương")


MindmapNode.model_rebuild()

Block = Union[ParaBlock, MathBlock, NotedBlock, WriteLinesBlock, ProblemBlock, MindmapBlock, TableBlock, FigureBlock, OpenerBlock, DefListBlock]

# ----- Chặng & gói bài học -----

StageKind = Literal["review", "concept", "practice1", "practice2", "reflection"]


class Stage(BaseModel):
    kind: StageKind
    number: int = Field(..., ge=1, le=5)
    title: str
    blocks: list[Block] = Field(default_factory=list)
    # Hai field dưới chỉ in trong Sổ tay GV (guide.pdf). Mặc định rỗng để
    # tương thích ngược với JSON cũ — handout/slide bỏ qua hoàn toàn.
    solution: str = Field("", description="Lời giải đầy đủ của chặng (chỉ hiện ở Guide, đỏ trầm)")
    teacher_note: str = Field("", description="Mẹo sư phạm điều phối chặng (chỉ hiện ở Guide)")


class LessonPackage(BaseModel):
    slug: str = Field(..., description="Định danh không dấu, dùng đặt tên thư mục outputs/")
    title: str
    eyebrow: str = Field("", description="Dòng nhỏ trên tiêu đề, vd 'ĐẠI SỐ — KỸ THUẬT XÉT HIỆU'")
    grade_label: str = Field("", description="vd 'Lớp 9 • Ôn vào 10'")
    class_tier: str = Field("", description="Tầng lớp phân hoá: ''=chuẩn | 'A' | 'B' | 'C' | 'X' (HS chuyên)")
    # CHƯƠNG — cần cho tầng B (Thầy chốt 30/08/2026): tỉ lệ NB-TH-VD của tầng B chọn
    # theo chương (chương có bài VD/VDC trong đề thi hay không — config/ban_do_vd_vdc.json).
    # Để trống thì `duration_gate` không soi được tỉ lệ của phiếu tầng B.
    chuong: str = Field("", description="Chương trong ban_do_vd_vdc.json, vd 'chuong-04-he-thuc-luong-tam-giac-vuong'")
    # SỐ CA (buổi) mà phiếu này trải ra — mặc định 1 = một phiếu dạy gọn trong một
    # buổi. Thầy chốt 16/08/2026: có phiếu cố ý gộp nhiều buổi vào MỘT file (chương III
    # lớp 9 tầng B gộp tuần 16+17). Khai `so_ca` để `duration_gate` nhân quỹ phút lên,
    # thay vì kêu oan "lệch quỹ 120′" ở mọi phiếu nhiều ca. Khớp `SpecPhieu.so_ca`.
    so_ca: int = Field(1, ge=1, le=6, description="Số ca (buổi) phiếu này trải ra; quỹ giờ ×so_ca")
    theme: str = Field("", description="Giao diện (vd: 'thay_thai' cho giao diện mới, để trống cho mặc định)")
    stages: list[Stage] = Field(default_factory=list)


class ChapterSummary(BaseModel):
    """Phiếu TỔNG KẾT CHƯƠNG (1 trang) — gom nhiều phiếu của một chương/tuần thành
    MỘT sơ đồ tư duy to (size large) cho HS điền. Là artifact riêng, sinh sau khi
    các phiếu thành viên đã có. Render bằng base_summary.tex.j2 (xem renderer)."""
    slug: str = Field(..., description="Định danh không dấu, đặt tên thư mục outputs/")
    title: str
    eyebrow: str = Field("", description="Dòng nhỏ trên tiêu đề, vd 'ĐẠI SỐ — TỔNG KẾT CHƯƠNG'")
    grade_label: str = Field("", description="vd 'Lớp 9 • Ôn vào 10'")
    grade: str = Field("", description="Mã khối lớp, ví dụ 'lop-9', 'lop-10'")
    intro: str = Field("", description="1–2 câu dẫn; cho phép $...$ và [[br]]")
    lessons: list[str] = Field(default_factory=list, description="slug các phiếu thành viên (tham chiếu)")
    mindmap: MindmapBlock = Field(..., description="Sơ đồ tư duy to gom cả chương (size='large')")
    solution: str = Field("", description="Đáp án các ô trống — CHỈ in ở bản GV")
