#!/usr/bin/env python3
"""Toạ độ và kiểm tra hình học cho Bộ Đề ôn Cuối kì 1 (CK1) Toán 9."""
import math

TOA_DO = {
    # ── Đề ôn 1 ──
    # (O; R=2), A=(-4, 0), B=(-1, sqrt(3)), C=(-1, -sqrt(3)), D=(1, -sqrt(3))
    # E=(0.5, -sqrt(3)/2), K=(-0.25, -3*sqrt(3)/4), H=(-1, 0), M=(-2, 0), N=(2, 0)
    "on1": {
        "O": (0.0, 0.0), "r": 2.0,
        "A": (-4.0, 0.0),
        "B": (-1.0, math.sqrt(3)),
        "C": (-1.0, -math.sqrt(3)),
        "D": (1.0, -math.sqrt(3)),
        "H": (-1.0, 0.0),
        "E": (0.5, -math.sqrt(3) / 2),
        "K": (-0.25, -1.299038),
        "M": (-2.0, 0.0),
        "N": (2.0, 0.0),
    },

    # ── Đề ôn 2 ──
    # Nửa đường tròn (O; R=2.5), A=(-2.5, 0), B=(2.5, 0)
    # D ở góc 60°: D = (1.25, 2.5*sqrt(3)/2)
    # Tiếp tuyến tại A và D cắt nhau tại C = (-2.5, 2.5*sqrt(3))
    # F = (1.25, 0), I = (1.25, 1.25*sqrt(3)/2)
    # E = BC cắt (O): E = (-0.357, 2.474)
    "on2": {
        "O": (0.0, 0.0), "r": 2.5,
        "A": (-2.5, 0.0),
        "B": (2.5, 0.0),
        "D": (1.25, 2.5 * math.sqrt(3) / 2),
        "C": (-2.5, 2.5 * math.sqrt(3)),
        "F": (1.25, 0.0),
        "I": (1.25, 1.25 * math.sqrt(3) / 2),
        "E": (-0.357143, 2.474358),
    },

    # ── Đề ôn 3 ──
    # Đường tròn (O; R=2.5), A=(-2.5, 0), B=(2.5, 0)
    # C ở góc 45°: C = (2.5*cos(pi/4), 2.5*sin(pi/4)) = (1.768, 1.768)
    # H = (1.768, 0), D = (1.768, -1.768)
    # Tiếp tuyến tại A và C cắt nhau tại M = (-2.5, 6.036)
    # I = trung điểm AC = (-0.366, 0.884)
    # F = MC cắt AB: F = (3.536, 0.0)
    "on3": {
        "O": (0.0, 0.0), "r": 2.5,
        "A": (-2.5, 0.0),
        "B": (2.5, 0.0),
        "C": (2.5 * math.cos(math.pi / 4), 2.5 * math.sin(math.pi / 4)),
        "H": (2.5 * math.cos(math.pi / 4), 0.0),
        "D": (2.5 * math.cos(math.pi / 4), -2.5 * math.sin(math.pi / 4)),
        "M": (-2.5, 6.035534),
        "I": (-0.366117, 0.883883),
        "F": (3.535534, 0.0),
    },
}


if __name__ == "__main__":
    print("Kiểm tra toạ độ hình học:")
    t1 = TOA_DO["on1"]
    # Kiểm tra K là trung điểm CE
    cy = (t1["C"][1] + t1["E"][1]) / 2
    assert abs(t1["K"][1] - cy) < 1e-4, f"K y diff: {t1['K'][1]} vs {cy}"
    print("✓ Đề ôn 1: K là trung điểm CE chuẩn xác.")

    t2 = TOA_DO["on2"]
    # Kiểm tra B, I, C thẳng hàng
    dx1 = t2["C"][0] - t2["B"][0]
    dy1 = t2["C"][1] - t2["B"][1]
    dx2 = t2["I"][0] - t2["B"][0]
    dy2 = t2["I"][1] - t2["B"][1]
    det2 = dx1 * dy2 - dy1 * dx2
    assert abs(det2) < 1e-4, f"B, I, C det: {det2}"
    print("✓ Đề ôn 2: B, I, C thẳng hàng chuẩn xác.")

    t3 = TOA_DO["on3"]
    # Kiểm tra FD vuông góc OD
    v_FD = (t3["F"][0] - t3["D"][0], t3["F"][1] - t3["D"][1])
    v_OD = t3["D"]
    dot3 = v_FD[0] * v_OD[0] + v_FD[1] * v_OD[1]
    assert abs(dot3) < 1e-4, f"FD . OD dot: {dot3}"
    print("✓ Đề ôn 3: FD tiếp tuyến (vuông góc OD) chuẩn xác.")

