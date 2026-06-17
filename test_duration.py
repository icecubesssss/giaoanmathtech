from src.schema.lesson_package import LessonPackage
from src.validators.duration_gate import check_duration

def test():
    lesson_json = {
        "slug": "test",
        "title": "test",
        "eyebrow": "test",
        "grade_label": "Lớp 8",
        "class_tier": "C", 
        "stages": [
            {
                "kind": "practice1",
                "number": 3,
                "title": "Luyện tập 1",
                "blocks": [
                    {
                        "type": "problem", "level": 1, "tier": "onclass", "label": "B1",
                        "statement": "a) b) c) d) e) f) g) h) i) j)"
                    },
                    {
                        "type": "problem", "level": 1, "tier": "onclass", "label": "B2",
                        "statement": "a) b) c) d) e) f) g) h) i) j)"
                    },
                    {
                        "type": "problem", "level": 1, "tier": "onclass", "label": "B3",
                        "statement": "a) b) c) d) e) f) g) h)"
                    },
                    {
                        "type": "problem", "level": 2, "tier": "onclass", "label": "B4",
                        "statement": "a) b) c)"
                    },
                    {
                        "type": "problem", "level": 2, "tier": "onclass", "label": "B5",
                        "statement": "a) b) c)"
                    },
                    {
                        "type": "problem", "level": 3, "tier": "onclass", "label": "B6",
                        "statement": "a) [NB] 1 \n b) [TH] 2 \n c) [VD] 3"
                    },
                    {
                        "type": "problem", "level": 3, "tier": "onclass", "label": "B7",
                        "statement": "a) [NB] 1 \n b) [TH] 2 \n c) [VD] 3"
                    }
                ]
            },
            {
                "kind": "reflection",
                "number": 5,
                "title": "Tổng kết",
                "blocks": [
                    {
                        "type": "problem", "level": 1, "tier": "btvn", "label": "B8",
                        "statement": "a) b) c) d) e) f) g) h) i) j)"
                    },
                    {
                        "type": "problem", "level": 1, "tier": "btvn", "label": "B9",
                        "statement": "a) b) c) d) e) f) g) h) i) j)"
                    },
                    {
                        "type": "problem", "level": 1, "tier": "btvn", "label": "B10",
                        "statement": "a) b) c) d) e) f)"
                    },
                    {
                        "type": "problem", "level": 2, "tier": "btvn", "label": "B11",
                        "statement": "a) b) c)"
                    },
                    {
                        "type": "problem", "level": 2, "tier": "btvn", "label": "B12",
                        "statement": "a) b) c)"
                    },
                    {
                        "type": "problem", "level": 3, "tier": "btvn", "label": "B13",
                        "statement": "a) [NB] \n b) [TH] \n c) [VD]"
                    },
                    {
                        "type": "problem", "level": 3, "tier": "btvn", "label": "B14",
                        "statement": "a) [TH] \n b) [VD]"
                    }
                ]
            }
        ]
    }
    lesson = LessonPackage.model_validate(lesson_json)
    warns = check_duration(lesson)
    for w in warns:
        print(w)
    if not warns:
        print("Perfect timing!")

if __name__ == '__main__':
    test()
