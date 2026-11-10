import re
import json
from pathlib import Path

p = Path("inputs/seeds/lop-5/de-cuoi-ki-1/de-kiem-tra-cuoi-ki-1-de-1.json")
data = json.loads(p.read_text(encoding="utf-8"))

# Điều chỉnh Bài 1: 2.0cm
b1 = data["stages"][1]["blocks"][1]
b1["statement"] = re.sub(r"grid \(\\linewidth, [0-9.]+\)", lambda m: r"grid (\linewidth, 2.0)", b1["statement"])

# Điều chỉnh Bài 2: 1.5cm
b2 = data["stages"][2]["blocks"][0]
b2["statement"] = re.sub(r"grid \(\\linewidth, [0-9.]+\)", lambda m: r"grid (\linewidth, 1.5)", b2["statement"])

# Bài 4: count = 3
data["stages"][3]["blocks"][1]["count"] = 3

# Bài 5: count = 2
data["stages"][4]["blocks"][1]["count"] = 2

p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Adjusted to 2.0 and 1.5!")
