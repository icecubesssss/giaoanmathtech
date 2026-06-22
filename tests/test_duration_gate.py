"""duration_gate — đếm "câu" theo ý nhỏ/thẻ mức và soi quỹ phút + tỉ lệ 40-40-20
từng phiếu tầng C (Thầy chốt 2026-06-11)."""
from src.schema import LessonPackage
from src.validators.duration_gate import _count_items, check_duration


def test_count_items_letters_and_bullets():
    # 3 ý chữ, trong đó b) và c) mỗi ý liệt kê 3 bullet → 1 + 3 + 3 = 7 câu.
    text = (r"a) Trong các số $-2; 0; 5$ ... "
            r"b) Kiểm tra: $\bullet$ A $\bullet$ B $\bullet$ C "
            r"c) Số nào: $\bullet$ D $\bullet$ E $\bullet$ F")
    assert _count_items(text) == 7


def test_count_items_ignores_vietnamese_and_math_parens():
    # "chữa)" và "(2x-1)" không phải đầu ý; i)/j) phải được đếm.
    assert _count_items("(KHÔNG cần giải — tiết sau chữa): a) X b) $(x+1)(2x-1)$") == 2
    assert _count_items("a) A b) B c) C d) D e) E f) F g) G h) H i) I j) J") == 10


def test_count_items_skips_letters_inside_math_groups():
    # "(a+b)", "(a-b)" KHÔNG được tính là ý — chỉ a) và b) ở vị trí liệt kê = 2.
    assert _count_items(r"a) Chứng minh $(a+b)^2-(a-b)^2=4ab$ [[br]] b) Tìm GTNN") == 2


def _lesson(problems):
    """Dựng phiếu C tối giản: 1 chặng practice1 chứa các problem cho trước."""
    return LessonPackage(slug="t", title="t", class_tier="C", stages=[{
        "kind": "practice1", "number": 3, "title": "LT",
        "blocks": [{"type": "problem", "label": f"Bài {i+1}.", "tier": t,
                    "level": lv, "statement": s} for i, (t, lv, s) in enumerate(problems)],
    }])


def test_balanced_onclass_passes():
    # 32 NB (48′) + 8 TH (48′) + 2 VD (24′) = 120′, đúng 40-40-20.
    nb = " ".join(f"{c}) x" for c in "abcdefgh")
    lesson = _lesson(
        [("onclass", 1, nb)] * 4            # 4 bài × 8 ý NB = 32 NB
        + [("onclass", 2, "a) x b) x c) x d) x")] * 2   # 8 TH
        + [("onclass", 3, "a) x b) x")]      # 2 VD
    )
    assert check_duration(lesson) == []


def test_skewed_ratio_warns():
    # Toàn TH → lệch 40-40-20, phải có cảnh báo tỉ lệ.
    lesson = _lesson([("onclass", 2, " ".join(f"{c}) x" for c in "abcdefghij"))] * 2)
    warns = check_duration(lesson)
    assert any("tỉ lệ" in w for w in warns)


def test_tags_override_level():
    # Bài VD đã tách thẻ: đếm 1 NB + 2 TH + 1 VD chứ không phải 4 VD.
    lesson = _lesson([("onclass", 3, "a) [NB] x b) [TH] x c) [TH] x d) [VD] x")])
    warns = check_duration(lesson)
    # 1,5 + 12 + 12 = 25,5′ → cảnh báo quỹ (quá ít) nhưng kiểm được phân mức qua message.
    assert any("NB 1 câu" in w and "TH 2 câu" in w and "VD 1 câu" in w for w in warns)


def test_btvn_only_budget_no_ratio():
    # BTVN: 40-40-20 KHÔNG áp (Thầy chốt — đó là tỉ lệ giờ TRÊN LỚP);
    # toàn TH nhưng đủ ~90′ thì sạch. 17 câu TH × 5,2′ = 88,4′.
    lesson = _lesson([("btvn", 2, " ".join(f"{c}) x" for c in "abcdefghi")),
                      ("btvn", 2, " ".join(f"{c}) x" for c in "abcdefgh"))])
    assert check_duration(lesson) == []


def test_non_tier_c_skipped():
    lesson = _lesson([("onclass", 2, "a) x")])
    lesson.class_tier = ""
    assert check_duration(lesson) == []


def test_tier_b_now_checked_with_vdc_band():
    # Sau refactor đọc tier_spec: tầng B lớp 9 (trước bị bỏ) NAY được soi;
    # level 4 → band VDC (trước gộp vào VD).
    lesson = _lesson([("onclass", 4, "a) x")])
    lesson.class_tier = "B"
    lesson.grade_label = "Lớp 9 • Ôn vào 10"
    warns = check_duration(lesson)
    assert warns and any("VDC" in w for w in warns)


def test_tier_x_not_gated():
    # X (chuyên) chưa chốt tỉ lệ trong tier_spec → không gate.
    lesson = _lesson([("onclass", 2, "a) x b) x")])
    lesson.class_tier = "X"
    lesson.grade_label = "Lớp 9 • Ôn vào 10"
    assert check_duration(lesson) == []
