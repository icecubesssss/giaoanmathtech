#!/usr/bin/env python3
"""Toạ độ giải tích chính xác 100% cho 3 bài hình ĐỀ KIỂM TRA CHÍNH THỨC CK1 LỚP 9."""
import math

def build_hinh_ct1():
    # O=(0,0), R=2. A=(-2,0), B=(2,0). C=(1, sqrt(3)), H=(1,0)
    # M=(-2, 2*sqrt(3)). K=(1, sqrt(3)/2).
    # scale để vừa khung 0.62\linewidth
    s = 1.25
    O = (0.0, 0.0)
    A = (-2.0, 0.0)
    B = (2.0, 0.0)
    C = (1.0, math.sqrt(3))
    H = (1.0, 0.0)
    M = (-2.0, 2 * math.sqrt(3))
    K = (1.0, math.sqrt(3) / 2)
    return {
        "O": O, "A": A, "B": B, "C": C, "H": H, "M": M, "K": K
    }

def build_hinh_ct2():
    # O=(0,0), R=2. A=(-4,0). B=(-1, sqrt(3)), C=(-1, -sqrt(3)). H=(-1,0). I=(-2,0).
    # D=(1, -sqrt(3)). K là hình chiếu C trên BD.
    # BD qua B(-1, sqrt(3)) và O(0,0) -> y = -sqrt(3)*x.
    # C=(-1, -sqrt(3)). Hình chiếu K trên BD:
    # CK vuông góc BD -> K=(0.5, -0.5*sqrt(3))
    O = (0.0, 0.0)
    A = (-4.0, 0.0)
    B = (-1.0, math.sqrt(3))
    C = (-1.0, -math.sqrt(3))
    H = (-1.0, 0.0)
    I = (-2.0, 0.0)
    D = (1.0, -math.sqrt(3))
    K = (0.5, -0.5 * math.sqrt(3))
    return {
        "O": O, "A": A, "B": B, "C": C, "H": H, "I": I, "D": D, "K": K
    }

def build_hinh_ct3():
    # O=(0,0), R=2. A=(-4,0). B=(-1, sqrt(3)), C=(-1, -sqrt(3)).
    # D=(1, -sqrt(3)). E=(-2,0). M=(-2.5, 0.5*sqrt(3)).
    O = (0.0, 0.0)
    A = (-4.0, 0.0)
    B = (-1.0, math.sqrt(3))
    C = (-1.0, -math.sqrt(3))
    D = (1.0, -math.sqrt(3))
    E = (-2.0, 0.0)
    M = (-2.5, 0.5 * math.sqrt(3))
    H = (-1.0, 0.0)
    return {
        "O": O, "A": A, "B": B, "C": C, "D": D, "E": E, "M": M, "H": H
    }

TOA_DO = {
    "ct1": build_hinh_ct1(),
    "ct2": build_hinh_ct2(),
    "ct3": build_hinh_ct3(),
}

if __name__ == "__main__":
    for k, v in TOA_DO.items():
        print(f"=== {k} ===")
        for pt, coord in v.items():
            print(f"  {pt}: ({coord[0]:.3f}, {coord[1]:.3f})")
