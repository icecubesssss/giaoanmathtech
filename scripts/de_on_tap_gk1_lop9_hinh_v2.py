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
# Ôn 1 — Văn Yên (Hà Đông): A vuông, AB=9, tanC=3/4 ⇒ AC=12 (tỉ lệ 0.25); M, N hình chiếu của H;
# K = (đường qua A song song MN) ∩ (đường qua C song song AH); I = AH ∩ BK
s1=0.25; A=(0,0);B=(0,9*s1);C=(12*s1,0);H=foot(A,B,C);M=(0,H[1]);N=(H[0],0)
K=inter(A,(N[0]-M[0],N[1]-M[1]),C,(C[0]+H[0],C[1]+H[1]));I=inter(A,H,B,K)
assert abs(cross(M,I,N))<1e-9 and abs(dist(K,A)-dist(K,C))<1e-9 and dist(I,(H[0]/2,H[1]/2))<1e-9
assert abs(dist(H,N)*dist(A,C)-dist(H,A)*dist(H,C))<1e-9 and abs(dist(H,N)-9*s1*(12/15)**2)<1e-9
print("Ôn1 M,I,N thẳng hàng; KA=KC; I trung điểm AH; HN·AC=HA·HC; HN=AB sin²B: OK")
out["on1"]=dict(A=A,B=B,C=C,H=H,M=M,N=N,K=K,I=I)
# Ôn 2 — Bát Tràng: A vuông, AB=6, góc B=53°
AC=6*tan(radians(53))/2; A=(0,0);B=(0,3);C=(AC,0);H=foot(A,B,C)
# phân giác góc B cắt AC tại D: AD/DC=AB/BC
BC=dist(B,C); D=(AC*3/(3+BC),0); K=inter(B,D,A,H); M=foot(C,B,D); I=inter(M,(M[0],M[1]+1),B,C)
print("Ôn2 BC=ABcosB+ACcosC:",abs(BC-(3*cos(radians(53))+AC*cos(radians(37))))<1e-9,
      "KH=AK sinC:",abs(dist(K,H)-dist(A,K)*sin(radians(37)))<1e-9, "I trung điểm BC:",dist(I,((B[0]+C[0])/2,(B[1]+C[1])/2))<1e-9)
out["on2"]=dict(A=A,B=B,C=C,H=H,D=D,K=K,M=M,I=I)
# Ôn 3 — Đền Lừ (Hoàng Mai): A vuông, B=60°, AC=7 (tỉ lệ 0.5); M trung điểm AC; AD ⊥ BM;
# N hình chiếu của M trên BC; E = tia AD ∩ đường qua C vuông góc AC
s3=0.5; AB3=7/sqrt(3); A=(0,0);B=(0,AB3*s3);C=(7*s3,0);M=(3.5*s3,0);H=foot(A,B,C);D=foot(A,B,M);N=foot(M,B,C)
E=inter(A,D,C,(C[0],C[1]+1)); O=(0,AB3*s3/2); r=AB3*s3/2
assert all(abs(dist(P,O)-r)<1e-9 for P in (A,B,H,D)) and abs(cross(M,N,E))<1e-9
assert abs((dist(A,M)/dist(B,M))**2-dist(D,M)/dist(B,M))<1e-12
print("Ôn3 A,B,H,D cùng đường tròn; sin²ABM=DM/BM; M,N,E thẳng hàng: OK")
out["on3"]=dict(A=A,B=B,C=C,M=M,H=H,D=D,N=N,E=E,O=O,r=r)
# GK — Cổ Nhuế: M vuông, MN=6, MP=8; H; E F; Q trên MP; I chân vuông góc từ M xuống NQ
Mv=(0,0);Nv=(0,3);P=(4,0);H=foot(Mv,Nv,P);E=(0,H[1]);F=(H[0],0);Q=(2.4,0);I=foot(Mv,Nv,Q)
lhs=(dist(Mv,Nv)/dist(Nv,Q))*(dist(Mv,Nv)/dist(Nv,P)); rhs=dist(H,I)/dist(Q,P)
print("GK ME·MN=MF·MP:",abs(dist(Mv,E)*3-dist(Mv,F)*4)<1e-9,"góc MEF=MPN:",abs(ang(Mv,E,F)-ang(Mv,P,Nv))<1e-9,
      "sin(MQN)cos(MNP)=HI/QP:",abs(lhs-rhs)<1e-12, "NI·NQ=NH·NP:",abs(dist(Nv,I)*dist(Nv,Q)-dist(Nv,H)*dist(Nv,P))<1e-9)
out["gk"]=dict(M=Mv,N=Nv,P=P,H=H,E=E,F=F,Q=Q,I=I)
TOA_DO = out
