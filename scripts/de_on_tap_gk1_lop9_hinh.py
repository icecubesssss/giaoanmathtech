"""Toạ độ hình của bộ đề ôn GK1 lớp 9 — TÍNH và KIỂM bằng giải tích (tính chất cần chứng minh
phải đúng trên chính hình vẽ). Import bởi scripts/de_on_tap_gk1_lop9.py."""
from math import *
import json
def foot(P,A,B):
    ax,ay=A; bx,by=B; px,py=P; dx,dy=bx-ax,by-ay; t=((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy); return (ax+t*dx,ay+t*dy)
def inter(P1,P2,P3,P4):
    x1,y1=P1;x2,y2=P2;x3,y3=P3;x4,y4=P4
    d=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    a=x1*y2-y1*x2; b=x3*y4-y3*x4
    return ((a*(x3-x4)-(x1-x2)*b)/d,(a*(y3-y4)-(y1-y2)*b)/d)
dist=lambda P,Q: hypot(P[0]-Q[0],P[1]-Q[1])
cross=lambda O,A,B:(A[0]-O[0])*(B[1]-O[1])-(A[1]-O[1])*(B[0]-O[0])
def ang(A,O,B):
    a=atan2(A[1]-O[1],A[0]-O[0]); b=atan2(B[1]-O[1],B[0]-O[0]); d=abs(degrees(a-b))%360; return min(d,360-d)
out={}
# Ôn 1 — Nguyễn Du: A vuông, AB=6, AC=8 (tỉ lệ 0.5)
A=(0,0);B=(0,3);C=(4,0);M=(2,0);H=foot(A,B,M);I=foot(M,B,C);K=inter(M,I,C,(4,1))
print("Ôn1 A,H,K thẳng hàng:",abs(cross(A,H,K))<1e-9, "cos²AMB=HM/BM:",abs((dist(A,M)/dist(B,M))**2-dist(H,M)/dist(B,M))<1e-12, "K",K)
out["on1"]=dict(A=A,B=B,C=C,M=M,H=H,I=I,K=K)
# Ôn 2 — Bát Tràng: A vuông, AB=6, góc B=53°
AC=6*tan(radians(53))/2; A=(0,0);B=(0,3);C=(AC,0);H=foot(A,B,C)
# phân giác góc B cắt AC tại D: AD/DC=AB/BC
BC=dist(B,C); D=(AC*3/(3+BC),0); K=inter(B,D,A,H); M=foot(C,B,D); I=inter(M,(M[0],M[1]+1),B,C)
print("Ôn2 BC=ABcosB+ACcosC:",abs(BC-(3*cos(radians(53))+AC*cos(radians(37))))<1e-9,
      "KH=AK sinC:",abs(dist(K,H)-dist(A,K)*sin(radians(37)))<1e-9, "I trung điểm BC:",dist(I,((B[0]+C[0])/2,(B[1]+C[1])/2))<1e-9)
out["on2"]=dict(A=A,B=B,C=C,H=H,D=D,K=K,M=M,I=I)
# Ôn 3 — Trưng Vương: A vuông, AB<AC, AH, M N hình chiếu của H
A=(0,0);B=(0,3);C=(4.6,0);H=foot(A,B,C);Mm=(0,H[1]);N=(H[0],0)
O=(H[0]/2,H[1]/2); r=dist(A,H)/2
print("Ôn3 4 điểm:",[round(dist(P,O)-r,12) for P in (A,Mm,H,N)],"HN=AB sin²B:",abs(dist(H,N)-3*(dist(A,C)/dist(B,C))**2)<1e-9,
      "AMN~ACB:",abs(dist(A,Mm)/dist(A,C)-dist(A,N)/dist(A,B))<1e-12)
out["on3"]=dict(A=A,B=B,C=C,H=H,M=Mm,N=N,O=O,r=r)
# GK — Cổ Nhuế: M vuông, MN=6, MP=8; H; E F; Q trên MP; I chân vuông góc từ M xuống NQ
Mv=(0,0);Nv=(0,3);P=(4,0);H=foot(Mv,Nv,P);E=(0,H[1]);F=(H[0],0);Q=(2.4,0);I=foot(Mv,Nv,Q)
lhs=(dist(Mv,Nv)/dist(Nv,Q))*(dist(Mv,Nv)/dist(Nv,P)); rhs=dist(H,I)/dist(Q,P)
print("GK ME·MN=MF·MP:",abs(dist(Mv,E)*3-dist(Mv,F)*4)<1e-9,"góc MEF=MPN:",abs(ang(Mv,E,F)-ang(Mv,P,Nv))<1e-9,
      "sin(MQN)cos(MNP)=HI/QP:",abs(lhs-rhs)<1e-12, "NI·NQ=NH·NP:",abs(dist(Nv,I)*dist(Nv,Q)-dist(Nv,H)*dist(Nv,P))<1e-9)
out["gk"]=dict(M=Mv,N=Nv,P=P,H=H,E=E,F=F,Q=Q,I=I)
TOA_DO = out
