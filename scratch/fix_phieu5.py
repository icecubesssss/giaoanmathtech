import json

path = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-5-luyen-tap-chung.json"
with open(path) as f:
    text = f.read()

# Replace \dfrac{1}{2}(\widehat{AOM} + \widehat{MOB}) with \frac{1}{2}(\widehat{AOM} + \widehat{MOB})
text = text.replace(r"\dfrac{1}{2}(\widehat{AOM} + \widehat{MOB})", r"\frac{1}{2}(\widehat{AOM} + \widehat{MOB})")

# In Vi du 2, fix the final Vay line
old_end = r"\Rightarrow \dfrac{MC}{MO} = [[fill:\dfrac{MO}{MD}|1.3cm]] \Rightarrow MC \cdot MD = [[fill:OM^2]]$."
new_end = r"\Rightarrow \dfrac{MC}{MO} = [[fill:\dfrac{MO}{MD}|1.3cm]] \Rightarrow MC \cdot MD = [[fill:OM^2]]$.[[br]]Vậy $\triangle COD$ vuông tại $O$ và $MC \cdot MD = OM^2$."
if old_end in text:
    text = text.replace(old_end, new_end)

with open(path, "w") as f:
    f.write(text)

print("Updated phieu-5!")
