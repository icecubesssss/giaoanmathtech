#!/usr/bin/env python3
"""TOẠ ĐỘ hình bài hình học của bộ đề ôn GK1 lớp 8 (scripts/de_on_tap_gk1_lop8.py).

Mỗi hình tính toạ độ bằng hình học giải tích rồi ASSERT đúng các tính chất đề bắt chứng minh
(hình chữ nhật, hình bình hành, trung điểm, thẳng hàng, góc vuông) — hình vẽ phải khớp kết luận.
Chạy riêng để kiểm:  .venv/bin/python scripts/de_on_tap_gk1_lop8_hinh.py
"""
import math


def tru(P, Q):
    return (P[0] - Q[0], P[1] - Q[1])


def tv(P, Q):  # trung điểm
    return ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)


def cham(u, v):
    return u[0] * v[0] + u[1] * v[1]


def chan(P, A, B):
    """chân đường vuông góc từ P xuống đường thẳng AB"""
    d = tru(B, A)
    t = cham(tru(P, A), d) / cham(d, d)
    return (A[0] + t * d[0], A[1] + t * d[1])


def giao(A, B, C, D):
    """giao điểm hai đường thẳng AB, CD"""
    x1, y1 = A; x2, y2 = B; x3, y3 = C; x4, y4 = D
    m = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2; b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / m, (a * (y3 - y4) - (y1 - y2) * b) / m)


def dx(P, Q):
    return math.hypot(*tru(P, Q))


def bang(a, b, e=1e-9):
    return abs(a - b) < e


def vuong_goc(P, Q, R, S):
    return bang(cham(tru(Q, P), tru(S, R)), 0)


def song_song(P, Q, R, S):
    u, v = tru(Q, P), tru(S, R)
    return bang(u[0] * v[1] - u[1] * v[0], 0)


def thang_hang(P, Q, R):
    return song_song(P, Q, P, R)


def hbh(P, Q, R, S):  # PQRS là hình bình hành: hai đường chéo PR, QS cắt nhau tại trung điểm mỗi đường
    a, b = tv(P, R), tv(Q, S)
    return bang(a[0], b[0]) and bang(a[1], b[1])


def hcn(P, Q, R, S):
    return hbh(P, Q, R, S) and vuong_goc(P, Q, Q, R)


def la(P):
    return [round(P[0], 3), round(P[1], 3)]


# ── ĐỀ ÔN 1 — THCS Tam Khương 2024-2025 (Bài 4) ──────────────────────────────
# ΔABC vuông tại A, đường cao AH, trung tuyến AM; HD ⊥ AB, HE ⊥ AC; DE ∩ AH = O, DE ∩ AM = Q;
# E là trung điểm AK.
A = (0.0, 0.0); B = (0.0, 2.6); C = (4.2, 0.0)
H = chan(A, B, C); M = tv(B, C); D = chan(H, A, B); E = chan(H, A, C)
O = giao(D, E, A, H); Q = giao(D, E, A, M); K = (2 * E[0] - A[0], 2 * E[1] - A[1])
assert hcn(A, D, H, E)                                   # a) ADHE là hình chữ nhật
assert hbh(D, H, K, E)                                   # b) DHKE là hình bình hành
assert vuong_goc(A, Q, E, Q)                             # c) ΔAEQ vuông tại Q
ON1 = {k: la(v) for k, v in dict(A=A, B=B, C=C, H=H, M=M, D=D, E=E, O=O, Q=Q, K=K).items()}

# ── ĐỀ ÔN 2 — THCS Nguyễn Du 2025-2026 (Bài 5.2) ─────────────────────────────
# ΔABC vuông tại A (AB < AC), M thuộc BC; MD ⊥ AB, ME ⊥ AC; Ax // DE cắt tia ME tại F;
# D là trung điểm MG; AM ∩ DE = O; AH là đường cao. Tính góc DHE.
A = (0.0, 0.0); B = (0.0, 2.7); C = (4.4, 0.0)
M = (B[0] + 0.62 * (C[0] - B[0]), B[1] + 0.62 * (C[1] - B[1]))
D = chan(M, A, B); E = chan(M, A, C)
F = giao(A, (A[0] + E[0] - D[0], A[1] + E[1] - D[1]), M, E)
G = (2 * D[0] - M[0], 2 * D[1] - M[1]); O = giao(A, M, D, E); H = chan(A, B, C)
assert hcn(A, D, M, E)                                   # a)
assert hbh(A, D, E, F)                                   # b) ADEF là hình bình hành
assert bang(tv(G, F)[0], A[0]) and bang(tv(G, F)[1], A[1])   # b) A là trung điểm GF
assert vuong_goc(D, H, E, H)                             # c) góc DHE = 90°
assert dx(A, B) < dx(A, C)
ON2 = {k: la(v) for k, v in dict(A=A, B=B, C=C, M=M, D=D, E=E, F=F, G=G, O=O, H=H).items()}

# ── ĐỀ ÔN 3 — THCS Nguyễn Huy Tưởng 2025-2026 (Câu 4) ────────────────────────
# ΔABC vuông cân tại A, M trung điểm BC; D trên tia đối của tia MA; DE ⊥ AB, DF ⊥ AC;
# EN ⊥ MF tại N. CM AEDF là hình vuông, EF // BC, góc AND = 90°.
A = (0.0, 0.0); B = (0.0, 3.0); C = (3.0, 0.0)
M = tv(B, C); D = (2.2, 2.2)
E = chan(D, A, B); F = chan(D, A, C); N = chan(E, M, F); I = tv(A, D)
assert thang_hang(A, M, D) and dx(A, D) > dx(A, M)      # D trên tia đối của tia MA
assert hcn(A, E, D, F) and bang(dx(A, E), dx(A, F))      # a) hình vuông
assert song_song(E, F, B, C)                             # b)
assert vuong_goc(A, N, D, N)                             # c)
ON3 = {k: la(v) for k, v in dict(A=A, B=B, C=C, M=M, D=D, E=E, F=F, N=N, I=I).items()}

# ── GK1 CHÍNH THỨC — THCS Phan Đình Giót 2023-2024 (Bài 4) ────────────────────
# ΔABC vuông tại A (AB < AC), đường cao AH; HM ⊥ AB, HN ⊥ AC; I trung điểm HC;
# tia MH cắt tia AI tại K; MN ∩ AH = O; CO ∩ AK = G. CM AK = 3AG.
A = (0.0, 0.0); B = (0.0, 2.8); C = (4.6, 0.0)
H = chan(A, B, C); M = chan(H, A, B); N = chan(H, A, C); I = tv(H, C)
K = giao(M, H, A, I); O = giao(M, N, A, H); G = giao(C, O, A, K)
assert hcn(A, M, H, N)                                   # a)
assert hbh(A, H, K, C)                                   # b)
assert bang(dx(A, K), 3 * dx(A, G))                      # c)
assert dx(A, B) < dx(A, C)
GK = {k: la(v) for k, v in dict(A=A, B=B, C=C, H=H, M=M, N=N, I=I, K=K, O=O, G=G).items()}

# ══ CHƯƠNG IV (bổ sung 15/10/2026 — tiến độ mới dạy Thalès, đường trung bình, phân giác tuần 11–13) ══
def goc(P, Q, R):
    """số đo góc PQR (độ)"""
    u, v = tru(P, Q), tru(R, Q)
    return math.degrees(math.acos(cham(u, v) / (dx(P, Q) * dx(R, Q))))


# ── ĐỀ ÔN 2 · Bài 5.1 — THCS Lê Lợi 2023-2024 (Câu 16a): M, N trung điểm AB, AC; MN = 3,5 cm ──
A = (1.3, 2.6); B = (0.0, 0.0); C = (4.2, 0.0)
M = tv(A, B); N = tv(A, C)
assert song_song(M, N, B, C) and bang(dx(B, C), 2 * dx(M, N))     # MN // BC, BC = 2MN ⇒ BMNC là hình thang
C4_LE_LOI = {k: la(v) for k, v in dict(A=A, B=B, C=C, M=M, N=N).items()}

# ── ĐỀ ÔN 1 · Bài 5.1 — THCS Văn Yên 2025-2026 (Bài IV.1): D, E trung điểm AB, AC; BC = 5 cm;
#    góc ADE = 70°, góc DAE = 60° (đề cho hình) ⇒ DE = 2,5 cm; góc ABC = 70°, góc ACB = 50°.
B = (0.0, 0.0); C = (5.0, 0.0)
A = giao(B, (math.cos(math.radians(70)), math.sin(math.radians(70))),
         C, (C[0] + math.cos(math.radians(130)), math.sin(math.radians(130))))
D = tv(A, B); E = tv(A, C)
assert bang(goc(B, A, C), 60, 1e-7) and bang(goc(A, D, E), 70, 1e-7)    # đúng số đo đề cho
assert bang(dx(D, E), 2.5) and bang(goc(A, B, C), 70, 1e-7) and bang(goc(A, C, B), 50, 1e-7)
C4_VAN_YEN = {k: la(v) for k, v in dict(A=A, B=B, C=C, D=D, E=E).items()}

# ── ĐỀ ÔN 3 · Bài 5.1 — THCS Văn Khê 2025-2026 (Bài IV.1): ao cá, MA = AN = 9 m, MB = BP = 16 m,
#    NP = 29 m ⇒ AB = 14,5 m. Toạ độ theo MÉT (vẽ theo tỉ lệ, scale trong TikZ).
N = (0.0, 0.0); P = (29.0, 0.0)
_x = (18 ** 2 - 32 ** 2 + 29 ** 2) / (2 * 29); M = (_x, math.sqrt(18 ** 2 - _x ** 2))
A = tv(M, N); B = tv(M, P)
assert bang(dx(M, A), 9) and bang(dx(A, N), 9) and bang(dx(M, B), 16) and bang(dx(B, P), 16)
assert bang(dx(A, B), 14.5) and song_song(A, B, N, P)
C4_VAN_KHE = {k: la(v) for k, v in dict(M=M, N=N, P=P, A=A, B=B).items()}

# ── GK1 · Bài 5.1 — THCS Nguyễn Trãi 2025-2026 (Bài 4.1): D, E trung điểm AB, AC (hình đánh dấu);
#    DE = 35 m ⇒ BC = 70 m. Hình minh hoạ (không theo tỉ lệ mét).
A = (1.6, 0.0); B = (0.0, 3.0); C = (4.4, 3.7)
D = tv(A, B); E = tv(A, C)
assert song_song(D, E, B, C) and bang(dx(B, C), 2 * dx(D, E))
C4_NGUYEN_TRAI = {k: la(v) for k, v in dict(A=A, B=B, C=C, D=D, E=E).items()}

TOA_DO = {"on1": ON1, "on2": ON2, "on3": ON3, "gk": GK,
          "c4_le_loi": C4_LE_LOI, "c4_van_yen": C4_VAN_YEN, "c4_van_khe": C4_VAN_KHE, "c4_nguyen_trai": C4_NGUYEN_TRAI}

if __name__ == "__main__":
    for k, v in TOA_DO.items():
        print(k, v)
