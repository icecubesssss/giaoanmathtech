import json

base_dir = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"

with open(f"{base_dir}/phieu-1-do-dai-cung-dien-tich-quat-vanh-khuyen.json") as f:
    d1 = json.load(f)

# Vi du 1
v1_text_1 = (
    r"\textbf{Ví dụ 1.} Trên Hình 2, góc ở tâm $\widehat{AOB} = 70^\circ$.[[br]]"
    r"a) Tính số đo cung nhỏ $AB$.[[br]]"
    r"b) Tính số đo cung lớn $AB$.[[br]]"
    r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
    r"a) Góc ở tâm $\widehat{AOB}$ chắn cung nhỏ $AB \Rightarrow$ số đo cung nhỏ $AB = [[fill:70^\circ]]$.[[br]]"
    r"b) Số đo cung lớn $AB = [[fill:360^\circ - 70^\circ]] = [[fill:290^\circ]]$.[[br]]"
    r"Vậy cung nhỏ $AB$ có số đo $[[fill:70^\circ]]$, cung lớn $AB$ có số đo $[[fill:290^\circ]]$."
)
d1["stages"][2]["blocks"][1]["text"] = v1_text_1

# Vi du 3
v3_text_1 = (
    r"\textbf{Ví dụ 3.} Hình quạt tô màu ở Hình 5 có bán kính $4$ cm, góc ở tâm $90^\circ$ (lấy $\pi \approx 3{,}14$).[[br]]"
    r"a) Tính độ dài cung của hình quạt.[[br]]"
    r"b) Tính diện tích của hình quạt.[[br]]"
    r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
    r"a) $l = \dfrac{n}{360} \cdot 2\pi R = [[fill:\dfrac{90}{360} \cdot 2\pi \cdot 4]] = [[fill:2\pi]] \approx [[fill:6{,}28]]$ (cm).[[br]]"
    r"b) $S_q = \dfrac{n}{360} \cdot \pi R^2 = [[fill:\dfrac{90}{360} \cdot \pi \cdot 4^2]] = [[fill:4\pi]] \approx [[fill:12{,}56]]$ (cm$^2$).[[br]]"
    r"Vậy cung dài khoảng [[fill:6{,}28]] cm, hình quạt có diện tích khoảng [[fill:12{,}56]] cm$^2$."
)
d1["stages"][2]["blocks"][8]["text"] = v3_text_1

with open(f"{base_dir}/phieu-1-do-dai-cung-dien-tich-quat-vanh-khuyen.json", "w") as f:
    json.dump(d1, f, ensure_ascii=False, indent=2)

print("Updated phieu-1 Vi du 1 & 3!")
