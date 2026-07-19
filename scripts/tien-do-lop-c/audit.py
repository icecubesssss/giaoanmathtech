# -*- coding: utf-8 -*-
"""Soi lỗi logic tiến độ tầng C — CHẠY TRƯỚC KHI XUẤT FILE cho Thầy.

    cd scripts/tien-do-lop-c && python3 audit.py && python3 gen_xlsx.py

Sinh ra sau khi Thầy bắt được loạt lỗi 2026-07-16 (ngày ghi dạng chuỗi bị Excel
parse sai thành 2028/2029; nhãn "Trọng tâm vào 10" gắn nhầm lên bài không thi).
"""
import re
import collections
import _data as D

SGV = {'I': 12, 'II': 12, 'III': 13, 'IV': 11, 'V': 15,
       'VI': 16, 'VII': 10, 'VIII': 8, 'IX': 12, 'X': 7}
CHNAME = {'I': 'PT & hệ PT', 'II': 'BĐT–BPT', 'III': 'Căn thức', 'IV': 'Tỉ số lượng giác',
          'V': 'Đường tròn', 'VI': 'Hàm số y=ax², PT bậc hai', 'VII': 'Tần số',
          'VIII': 'Xác suất', 'IX': 'Đ.tròn ngoại/nội tiếp', 'X': 'Hình khối'}
# Các bài KHÔNG có trong 3/3 đề vào 10 — không được gắn nhãn "Trọng tâm vào 10".
# Danh sách này ĐÃ SAI 2 LẦN, Thầy sửa cả 2:
#  - Bài 5 (BĐT) + Bài 6 (BPT): Câu II ý 3 của 3/3 đề đều cần → BỎ khỏi danh sách.
#  - Bài 15 (cung, quạt, vành khuyên): CÓ trong đề thi thử và CÓ THỂ THAY hình khối
#    ở Câu IV.1 (cùng là ý đo lường) → BỎ khỏi danh sách.
KHONG_THI = ('18', '30', '17', '11', '12')

# Bài nào thuộc chương nào — để đếm tiết đúng kể cả khi bài bị dời sang buổi ôn tập
BAI2CH = {}
for _lo, _hi, _ch in ((1, 3, 'I'), (4, 6, 'II'), (7, 10, 'III'), (11, 12, 'IV'), (13, 17, 'V'),
                      (18, 21, 'VI'), (22, 24, 'VII'), (25, 26, 'VIII'), (27, 30, 'IX'), (31, 32, 'X')):
    for _b in range(_lo, _hi + 1):
        BAI2CH[str(_b)] = _ch

loi = []
def add(k, s): loi.append((k, s))

def muc_day(r):
    if not isinstance(r[2], int) or not r[2]:
        return ""
    return r[10] if len(r) > 10 else "Đầy đủ"

def ch_of(nd):
    for k in sorted(SGV, key=len, reverse=True):
        if nd.startswith('CHƯƠNG ' + k + '.'):
            return k
    return None

for src, mon, budget in ((D.DAI_SO, 'ĐS', 165), (D.HINH_HOC, 'HH', 90)):
    taught, t15n = {}, collections.Counter()
    for w in sorted(src):
        for r in src[w]:
            for m in re.findall(r'Bài (\d+)', r[1] or ''):
                taught.setdefault(m, w)
    for w in sorted(src):
        tot = sum(r[3] for r in src[w] if isinstance(r[3], int))
        if tot != budget:
            add('QUỸ PHÚT', f'{mon} tuần {w}: {tot}′ ≠ {budget}′')
        for r in src[w]:
            td, bai, tiet, phut, hm, lkt, ut, cau, nd, gc = r[:10]
            if lkt == '15 phút':
                m = re.search(r'Đề 15′ số (\d+)', nd)
                if m:
                    t15n[int(m.group(1))] += 1
                for b in re.findall(r'Bài (\d+)', td):
                    if b in taught and taught[b] > w:
                        add('KT15 SOI BÀI CHƯA DẠY',
                            f'{mon} tuần {w}: "{td[:46]}" — Bài {b} mãi tuần {taught[b]} mới dạy')
            if ut == D.A:
                for b in re.findall(r'Bài (\d+)', str(bai)):
                    if b in KHONG_THI:
                        add('NHÃN ƯU TIÊN NÓI DỐI',
                            f'{mon} tuần {w}: gắn A + "{cau}" nhưng dòng chứa Bài {b} (không có trong đề) — {bai}')
            for fld in (td, bai, gc):
                if '^' in str(fld):
                    add('KÍ HIỆU TOÁN THÔ', f'{mon} tuần {w}: "{str(fld)[:44]}" — dùng ² thay ^2')
    dup = [n for n, c in t15n.items() if c > 1]
    if dup:
        add('ĐỀ 15′ TRÙNG SỐ', f'{mon}: {dup}')
    if t15n:
        gap = [n for n in range(1, max(t15n) + 1) if n not in t15n]
        if gap:
            add('ĐỀ 15′ THIẾU SỐ', f'{mon}: {gap}')

# tiết/chương vs PPCT — quy tiết về chương THEO SỐ BÀI (kể cả bài đã dời sang buổi ôn tập)
tot = collections.Counter()      # tổng tiết PPCT được nhắc tới
bo = collections.Counter()       # tiết của bài đánh dấu "Bỏ – chỉ nhắc"
for src in (D.DAI_SO, D.HINH_HOC):
    for w, rows in src.items():
        for r in rows:
            if not isinstance(r[2], int):
                continue
            bais = re.findall(r'Bài (\d+)', str(r[1]))
            ch = BAI2CH.get(bais[0]) if bais else ch_of(r[8])
            if ch:
                tot[ch] += r[2]
                if muc_day(r).startswith('Bỏ'):
                    bo[ch] += r[2]
for k, v in SGV.items():
    if tot[k] != v:
        add('TIẾT ≠ PPCT', f'Chương {k}: xếp {tot[k]} / PPCT {v} — có bài bị bỏ sót khỏi tiến độ')

# phủ đề vào 10
need = {D.Q_I1, D.Q_I2, D.Q_II, D.Q_III1, D.Q_III2, D.Q_III3, D.Q_IV1, D.Q_IV2}
cov = {q: 0 for q in need}
for src in (D.DAI_SO, D.HINH_HOC):
    for w, rows in src.items():
        for r in rows:
            if r[7] in cov:
                cov[r[7]] += 1
for q, n in cov.items():
    if not n:
        add('CÂU TRONG ĐỀ KHÔNG ĐƯỢC PHỦ', q)

print('=' * 74)
print(f'AUDIT TIẾN ĐỘ TẦNG C — {len(loi)} lỗi')
print('=' * 74)
for k in sorted({k for k, _ in loi}):
    rs = [s for kk, s in loi if kk == k]
    print(f'\n■ {k}  ({len(rs)})')
    for s in rs:
        print(f'   - {s}')
if not loi:
    print('\n✓ SẠCH — không phát hiện lỗi logic.')

# bảng mật độ dạy theo chương (thông tin, không phải lỗi)
phut = collections.Counter()
for src in (D.DAI_SO, D.HINH_HOC):
    for w, rows in src.items():
        chs = [ch_of(r[8]) for r in rows if ch_of(r[8])]
        main = collections.Counter(chs).most_common(1)[0][0] if chs else None
        for r in rows:
            k = ch_of(r[8]) or (main if r[5] in ('1 tiết', '') and main else None)
            if k and isinstance(r[3], int) and r[5] != '15 phút':
                phut[k] += r[3]
print('\n' + '=' * 84)
print('MẬT ĐỘ DẠY THEO CHƯƠNG (gồm buổi KT 1 tiết + chữa; KHÔNG gồm buổi luyện đề sau Tết)')
print('=' * 84)
print(f'{"Ch":5s} {"Nội dung":26s} {"PPCT":>4s} {"bỏ":>3s} {"dạy":>4s} {"cần′":>5s} {"có′":>5s} {"×":>5s}')
for k in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']:
    day = SGV[k] - bo[k]              # tiết thực dạy = PPCT trừ bài đã bỏ
    can = day * 45
    ratio = phut[k] / can if can else 0
    print(f'{k:5s} {CHNAME[k]:26s} {SGV[k]:4d} {bo[k]:3d} {day:4d} {can:5d} {phut[k]:5d} {ratio:5.2f}'
          + ('  ← MỎNG, Thầy rà lại' if ratio < 0.7 else ''))
print('\n"bỏ" = tiết của bài Thầy chốt cắt hẳn (chỉ nhắc khi ôn thi trường). "×" tính trên tiết THỰC DẠY.')
