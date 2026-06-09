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


class MathBlock(BaseModel):
    type: Literal["math"] = "math"
    latex: str = Field(..., description="Công thức hiển thị giữa dòng (không kèm $$)")


class NotedBlock(BaseModel):
    type: Literal["noted"] = "noted"
    text: str = Field(..., description="Nội dung trong hộp nền xám (vd ô điền khuyết)")
    # Thẻ callout có nhãn màu + icon. "" = hộp xám trung tính như cũ (tương thích ngược).
    #   trap   = "BẪY ĐIỂM" (đỏ, cảnh báo lỗi hay mất điểm)
    #   target = "ĐÍCH THI VÀO 10" (vàng, chốt mục tiêu thi)
    #   tip    = "MẸO" (tím, mẹo nhanh)
    #   example= "VÍ DỤ MẪU" (xanh dương)
    variant: Literal["", "note", "trap", "target", "tip", "example"] = Field(
        "", description="Kiểu thẻ callout; rỗng = hộp xám trung tính như cũ"
    )


class WriteLinesBlock(BaseModel):
    type: Literal["writelines"] = "writelines"
    count: int = Field(2, ge=0, le=12, description="Số dòng kẻ trống cho HS viết (0 = chỉ chừa 1 dòng trắng, KHÔNG kẻ — lớp HS trình bày vào vở)")


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
    # Đặc sản "QR video lời giải": URL video Thầy giải bài. Có giá trị → in QR nhỏ ở
    # lề phải bài (cầu nối giấy → điện thoại). Rỗng = không in QR (tương thích ngược).
    video: str = Field("", description="URL video lời giải; có → in QR cạnh bài")
    # (TÙY CHỌN) Đáp án MÁY-ĐỌC để `validate` tự soi bằng SymPy. None = bỏ qua (như cũ).
    # KHÔNG in ra phiếu — chỉ phục vụ answer_gate. Phân biệt loại bằng khóa "kind".
    check: Optional[AnswerCheck] = Field(
        None, description="Đáp án máy-đọc cho answer_gate; KHÔNG hiển thị trên phiếu"
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

Block = Union[ParaBlock, MathBlock, NotedBlock, WriteLinesBlock, ProblemBlock, MindmapBlock, TableBlock, FigureBlock, OpenerBlock]

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
    stages: list[Stage] = Field(default_factory=list)


class ChapterSummary(BaseModel):
    """Phiếu TỔNG KẾT CHƯƠNG (1 trang) — gom nhiều phiếu của một chương/tuần thành
    MỘT sơ đồ tư duy to (size large) cho HS điền. Là artifact riêng, sinh sau khi
    các phiếu thành viên đã có. Render bằng base_summary.tex.j2 (xem renderer)."""
    slug: str = Field(..., description="Định danh không dấu, đặt tên thư mục outputs/")
    title: str
    eyebrow: str = Field("", description="Dòng nhỏ trên tiêu đề, vd 'ĐẠI SỐ — TỔNG KẾT CHƯƠNG'")
    grade_label: str = Field("", description="vd 'Lớp 9 • Ôn vào 10'")
    intro: str = Field("", description="1–2 câu dẫn; cho phép $...$ và [[br]]")
    lessons: list[str] = Field(default_factory=list, description="slug các phiếu thành viên (tham chiếu)")
    mindmap: MindmapBlock = Field(..., description="Sơ đồ tư duy to gom cả chương (size='large')")
    solution: str = Field("", description="Đáp án các ô trống — CHỈ in ở bản GV")
