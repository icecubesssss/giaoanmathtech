"""Cổng gác ĐỀ ↔ HÌNH — chặn hai lỗi đã lọt tới Thầy ở phiếu B/C chương III lớp 7.

Ra đời sau phản hồi 2026-07-28 của Thầy An (phiếu B: "lỗi tia Ot", "lỗi tia Od",
"thừa bài 5,6,9"; phiếu C: "AI k hiểu được nội dung dạng câu, nhiều lỗi kí hiệu").
Cả hai đều là lỗi CƠ HỌC, soi bằng code được — không cần LLM đọc lại:

  1. `check_figure_symbols` — HÌNH KHÔNG ĐỠ NỔI ĐỀ:
     a) Đề (kể cả 4 phương án A/B/C/D) nhắc góc $\\widehat{A_2}$ mà hình chỉ vẽ
        $\\widehat{A_1}$ → HS không có căn cứ để chọn. Đây chính là phiếu C: 24 bài
        hỏi về $A_1,A_2,B_1,B_2$ nhưng hình chỉ dán 2 nhãn.
     b) Hình dán nhãn ĐẦU TIA kiểu `$Ot$` trong khi các tia còn lại dán `$m$`, `$n$`.
        Quy ước vẽ: nhãn đặt ở đầu mút tia là CHỮ CÁI ĐÓ (`t`), không phải cả tên
        tia (`Ot`) — Thầy gọi là "lỗi tia".

  2. `check_clone_problems` — BÀI NHÂN BẢN:
     Bỏ hình + bỏ chỉ số đi rồi mà hai đề vẫn trùng chữ thì là một bài chép nhiều
     lần để lấp chỗ (phiếu C: bài 1–24 thực chất chỉ là 2 bài × 12 bản sao, đáp án
     đều là A). Thầy gạch chéo nguyên 4 trang vì lỗi này.

Cả hai đều trả VI PHẠM CHẶN (không phải cảnh báo): phiếu dính là phải dệt lại.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

from src.schema import LessonPackage

__all__ = [
    "FigureViolation",
    "check_figure_symbols",
    "check_clone_problems",
    "check_figures",
]

# --- Bóc hình khỏi đề -------------------------------------------------------
_TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
# Nhãn dán trong hình: node[...]{$x$} / node{$\widehat{A_1}$}
_NODE_LABEL = re.compile(r"\\node[^{]*\{\$(.+?)\$\}|node\[[^\]]*\]\{\$(.+?)\$\}")
# Góc có chỉ số: \widehat{A_1}, \widehat{B_2}
_INDEXED_ANGLE = re.compile(r"\\widehat\{([A-Za-z])_\{?(\d+)\}?\}")
# Nhãn đầu tia viết cả tên tia: $Ot$, $Oz$, $Od$ (gốc O + 1 chữ thường)
_RAY_AS_PAIR = re.compile(r"^([A-Z])([a-z])$")
# Caption dưới hình do compiler tự đánh số: 'Hình 1', 'Hình 12'
_FIG_CAPTION = re.compile(r"H[ìi]nh\s*\d+", re.IGNORECASE)
# Đề TRỎ tới một hình có sẵn ("cho hình vẽ", "quan sát hình", "hình vẽ có…") →
# BẮT BUỘC phải kèm hình, nếu không HS không có gì để nhìn.
#   Lưu ý thứ tự chữ: "hình vẽ" (danh từ, trỏ hình có sẵn) KHÁC "vẽ hình" (bảo HS vẽ).
_TRO_HINH = re.compile(
    r"h[ìi]nh\s*v[ẽe]|"
    r"(?:cho|quan\s*sát|xem|theo|dựa\s*vào)\s+h[ìi]nh",
    re.IGNORECASE)
# Đề BẮT HS TỰ VẼ ("vẽ hình", "hãy vẽ…") → phải bật draw=True để cấp giờ + chừa khung.
_BAT_VE = re.compile(
    r"\bv[ẽe]\s+h[ìi]nh\b|\bhãy\s+v[ẽe]\b|\bv[ẽe]\s+(?:đường\s*thẳng|tia|góc|tam\s*giác|cung)",
    re.IGNORECASE)


@dataclass
class FigureViolation:
    label: str
    reason: str

    def __str__(self) -> str:  # để in thẳng ra CLI
        return f"{self.label} {self.reason}"


def _iter_problems(lesson: LessonPackage):
    """Duyệt mọi block `problem` kèm tên chặng, theo đúng thứ tự in ra phiếu."""
    for stage in lesson.stages:
        for block in stage.blocks:
            if getattr(block, "type", "") == "problem":
                yield stage, block


def _iter_co_hinh(lesson: LessonPackage):
    """Duyệt MỌI block có thể chứa hình — kể cả lý thuyết (para/noted).

    Hình ở chặng Khám phá / Khái niệm cũng phải đúng quy ước nhãn: Thầy đọc phiếu
    từ trang đầu, sai ở phần lý thuyết còn lộ hơn sai trong bài tập.
    """
    for stage in lesson.stages:
        for i, block in enumerate(stage.blocks, 1):
            kind = getattr(block, "type", "")
            if kind == "problem":
                yield block.label, block.statement
            elif kind in ("para", "noted", "opener"):
                yield f"[{stage.title} · khối {i}]", getattr(block, "text", "")


def _split_figure(statement: str) -> tuple[str, str]:
    """Tách đề thành (phần chữ, phần hình TikZ gộp)."""
    figures = "\n".join(_TIKZ.findall(statement))
    text = _TIKZ.sub(" ", statement)
    return text, figures


def _labels_in_figure(figure: str) -> set[str]:
    """Tập nhãn đã DÁN trong hình (nội dung mỗi $...$ của node)."""
    out: set[str] = set()
    for a, b in _NODE_LABEL.findall(figure):
        lab = (a or b).strip()
        if lab:
            out.add(lab)
    return out


# --- 1. Hình có đỡ nổi đề không? -------------------------------------------
def check_figure_symbols(lesson: LessonPackage) -> list[FigureViolation]:
    """Đề nhắc ký hiệu nào thì hình phải dán đủ ký hiệu đó."""
    out: list[FigureViolation] = []

    for nhan, raw in _iter_co_hinh(lesson):
        text, figure = _split_figure(raw)
        if not figure:
            continue  # khối chữ thuần — không thuộc phạm vi cổng này

        labels = _labels_in_figure(figure)

        # (a) Góc có chỉ số: đề hỏi $\widehat{A_2}$ thì hình phải chỉ ra được góc đó.
        # Chấp nhận HAI cách vẽ:
        #   • dán thẳng nhãn '\widehat{A_2}' (rõ nhưng chiếm chỗ), HOẶC
        #   • cách SGK/Thầy vẫn vẽ tay: ghi tên đỉnh 'A' rồi rắc CHỮ SỐ TRẦN 1,2,3,4
        #     quanh đỉnh — gọn hơn hẳn khi hình bị co nhỏ.
        drawn = {(n, i) for n, i in _INDEXED_ANGLE.findall("|".join(labels))}
        dinh = {x for x in labels if len(x) == 1 and x.isalpha() and x.isupper()}
        so = {x for x in labels if x.isdigit()}
        drawn |= {(v, s) for v in dinh for s in so}

        asked = {(n, i) for n, i in _INDEXED_ANGLE.findall(text)}
        missing = sorted(asked - drawn)
        if missing:
            names = ", ".join(f"$\\widehat{{{n}_{i}}}$" for n, i in missing)
            out.append(
                FigureViolation(
                    nhan,
                    f"đề/phương án nhắc {names} nhưng HÌNH KHÔNG DÁN nhãn đó "
                    f"(hình chỉ có {sorted(labels) or 'không nhãn nào'}) — HS không có căn cứ để trả lời.",
                )
            )

        # (b) Nhãn đầu tia viết cả tên tia ('Ot') giữa các nhãn 1 chữ ('m','n').
        pair_labels = sorted(x for x in labels if _RAY_AS_PAIR.match(x))
        single = {x for x in labels if len(x) == 1 and x.isalpha()}
        if pair_labels and single:
            for bad in pair_labels:
                out.append(
                    FigureViolation(
                        nhan,
                        f"hình dán nhãn đầu tia '${bad}$' trong khi các tia khác dán "
                        f"'{'/'.join(sorted(single))}' — đầu mút tia phải ghi '${bad[1]}$', "
                        f"không ghi cả tên tia.",
                    )
                )

    return out


# --- 2. Bài nhân bản --------------------------------------------------------
def _fingerprint(statement: str) -> str:
    """Vân tay ĐỀ: bỏ hình + caption 'Hình N' + chỉ số góc, ép khoảng trắng — hai đề
    chỉ khác nhau ở chỉ số/số hiệu hình sẽ ra cùng một vân tay.

    CỐ Ý GIỮ các số đo trong đề ($60^\\circ$, $110^\\circ$…): hai bài cùng lời văn
    nhưng khác số đo là bài luyện tập hợp lệ, KHÔNG phải bản sao.
    """
    text, _ = _split_figure(statement)
    text = _FIG_CAPTION.sub(" ", text)            # bỏ 'Hình 1' / 'Hình 12' (đánh số tự động)
    text = _INDEXED_ANGLE.sub(r"\\widehat{\1_#}", text)
    text = re.sub(r"\\[a-zA-Z]+", " ", text)      # bỏ lệnh LaTeX trình bày
    text = re.sub(r"[^\w\sÀ-ỹ]", " ", text)       # bỏ dấu câu/ngoặc
    return re.sub(r"\s+", " ", text).strip().lower()


def check_clone_problems(lesson: LessonPackage, max_clones: int = 2) -> list[FigureViolation]:
    """Cùng một đề chép quá `max_clones` lần → lấp chỗ, phải dệt lại."""
    groups: dict[str, list[str]] = defaultdict(list)
    for _stage, prob in _iter_problems(lesson):
        fp = _fingerprint(prob.statement)
        if len(fp) < 30:
            continue  # đề quá ngắn, vân tay không đáng tin
        groups[fp].append(prob.label)

    out: list[FigureViolation] = []
    for labels in groups.values():
        if len(labels) > max_clones:
            out.append(
                FigureViolation(
                    labels[0],
                    f"đề này bị CHÉP LẠI {len(labels)} lần ({', '.join(labels)}) — "
                    f"khác nhau mỗi chỉ số/hình. Giữ tối đa {max_clones} bản, phần còn lại "
                    f"phải đổi thành dạng khác.",
                )
            )
    return out


# --- 3. Đề trỏ tới hình mà không có hình / bắt vẽ mà không chừa chỗ ---------
def check_hinh_thieu(lesson: LessonPackage) -> list[FigureViolation]:
    """Hai lỗi Thầy đã bắt ở phiếu B, còn sót ở phiếu E:

      a) Đề viết "Hình vẽ ... minh họa cho định lý nào?" nhưng KHÔNG kèm hình nào
         → HS không có gì để nhìn mà trả lời.
      b) Đề bắt "Vẽ hình và ghi GT, KL" nhưng `draw` vẫn False → không được cấp
         `draw_minutes` vào quỹ giờ và không có khung trống để HS vẽ vào phiếu
         (Thầy: "tạo thêm chỗ cho hs vẽ vào đề").
    """
    out: list[FigureViolation] = []
    for _stage, prob in _iter_problems(lesson):
        text, figure = _split_figure(prob.statement)

        if _TRO_HINH.search(text) and not figure:
            out.append(FigureViolation(
                prob.label,
                "đề trỏ tới một hình có sẵn nhưng KHÔNG kèm hình nào — HS không có gì "
                "để nhìn. Thêm hình, hoặc sửa đề thành yêu cầu HS tự vẽ."))

        # Chỉ tính là "HS phải tự vẽ" khi đề KHÔNG kèm hình sẵn. Bài đã có hình mà đề
        # viết "vẽ tia Ot là tia phân giác…" thì tia đó đã vẽ sẵn trên hình rồi.
        if not figure and _BAT_VE.search(text) and not getattr(prob, "draw", False):
            out.append(FigureViolation(
                prob.label,
                "đề bắt HS TỰ VẼ HÌNH nhưng chưa bật `draw: true` — thiếu khung trống "
                "để vẽ vào phiếu và thiếu phút vẽ trong quỹ giờ."))
    return out


def check_figures(lesson: LessonPackage) -> list[str]:
    """VI PHẠM CHẶN — hai lỗi đã có bằng chứng Thầy trả phiếu, kho hiện sạch nên
    chặn cứng được ngay."""
    return [str(v) for v in check_figure_symbols(lesson) + check_clone_problems(lesson)]


def warn_figures(lesson: LessonPackage) -> list[str]:
    """CẢNH BÁO (chưa chặn) — `check_hinh_thieu` bắt đúng nhưng đang dính ~60 chỗ ở
    18 phiếu cũ khắp kho; chặn cứng ngay sẽ làm vỡ build hàng loạt việc không liên
    quan. Dọn hết nợ cũ rồi mới nâng lên chặn."""
    return [str(v) for v in check_hinh_thieu(lesson)]
