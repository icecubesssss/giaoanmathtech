import json

with open("config/tier_spec.json", "r") as f:
    data = json.load(f)

data["grades"]["lop-6"] = {
    "dai-so": {
        "session_minutes": 90,
        "break_minutes": 15,
        "budgets": {"vidu": 30.0, "onclass": 45.0, "btvn": 60.0},
        "budget_tol": 0.10,
        "ratio_tol": 10.0,
        "spec_count_tol": 2,
        "tiers": {
            "C": {"ratio": {"NB": 40, "TH": 40, "VD": 20, "VDC": 0}, "max_level": 3, "allow_extend": False, "_note": "Lớp 6 Tầng C"}
        }
    }
}

with open("config/tier_spec.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
