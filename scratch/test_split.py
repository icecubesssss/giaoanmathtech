with open('outputs/lop-5/de-cuoi-ki-1/de-kiem-tra-cuoi-ki-1-de-1/Toan5-De-kiem-tra-cuoi-ki-1-de-1-Phieu-HS.tex') as f:
    text = f.read()

target = r'\par\vspace{2pt}\noindent\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}'
replacement = r'\newpage' + '\n' + r'\par\vspace{2pt}\noindent\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}'

# Remove the old \newpage after Bài 1
text = text.replace(r'\newpage', '')

# Insert \newpage before PHẦN II
assert target in text, "Target not found!"
text = text.replace(target, replacement)

# Let's adjust sizes of \olyline on Page 2:
# Bài 1: \olyline[3]
# Bài 2: \olyline[2]
# Bài 4: \olyline[4]
# Bài 5: \olyline[2]
text = text.replace(r'\olyline[5]', r'\olyline[3]')
text = text.replace(r'\olyline[3]', r'\olyline[2]') # for Bai 2
text = text.replace(r'\olyline[6]', r'\olyline[4]') # for Bai 4

with open('scratch/test_split_clean.tex', 'w') as f:
    f.write(text)

print("Saved clean tex!")

