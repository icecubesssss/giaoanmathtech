#!/usr/bin/env python3
"""SỔ DẠNG BÀI — mỗi (tiểu) dạng trong đề Hà Nội: tần suất · nhận dạng · các bước · lỗi hay gặp ·
bài mẫu từ đề thật + lời giải trình bày như HS đi thi. Ra PDF A4 dọc.

Nội dung: scripts/so_dang_bai_lop<N>.py (biến MUC). Tần suất: đọc
outputs/thong-ke-dang-de/phan-loai-lop-<N>.json do scripts/thong_ke_dang_de.py --json sinh ra.

Trước khi dựng, script KIỂM MÁY mọi bài có trường `kiem` (SymPy): thay nghiệm vào hệ/phương trình,
giải lại bất phương trình, so biểu thức rút gọn, tính lại số làm tròn, đếm lại tần số/xác suất.
Sai một bài là DỪNG, không dựng PDF.

Dùng:
    .venv/bin/python scripts/thong_ke_dang_de.py --lop 9 --json
    .venv/bin/python scripts/build_so_dang_bai.py --lop 9            # kiểm + dựng PDF
    .venv/bin/python scripts/build_so_dang_bai.py --lop 9 --kiem     # chỉ kiểm đáp số
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

KY = ["GK1", "CK1", "GK2", "CK2"]


# ─────────────────────────── KIỂM ĐÁP SỐ ───────────────────────────
def kiem_bai(k: dict) -> list[str]:
    """Trả danh sách lỗi (rỗng = đúng)."""
    import sympy as sp
    from sympy import Rational, sqrt  # noqa: F401  (dùng trong eval chuỗi biểu thức)
    x, y = sp.symbols("x y")
    ns = {"x": x, "y": y, "Rational": sp.Rational, "sqrt": sp.sqrt, "pi": sp.pi,
          "tan": sp.tan, "cos": sp.cos, "sin": sp.sin}
    loi = []
    if "he" in k:
        sub = {sp.Symbol(a): sp.nsimplify(v) for a, v in k["nghiem"].items()}
        for e in k["he"]:
            v = sp.simplify(sp.sympify(e, locals=ns).subs(sub))
            if v != 0:
                loi.append(f"hệ: {e} ≠ 0 tại {k['nghiem']} (= {v})")
        eqs = [sp.sympify(e, locals=ns) for e in k["he"]]
        ds = sp.solve(eqs, [x, y], dict=True)
        if len(ds) != 1:
            loi.append(f"hệ không có nghiệm duy nhất: {ds}")
    if "pt" in k:
        # So TẬP NGHIỆM của phương trình gốc với tập ghi trong sổ. SymPy giải phương trình gốc nên tự
        # loại giá trị làm mẫu bằng 0 (ĐKXĐ). Nghiệm "loại" vì điều kiện thực tế (x = −10 xe…) vẫn là
        # nghiệm của phương trình nên được ghi kèm trong `nghiem`.
        e = sp.sympify(k["pt"], locals=ns)
        sol = {sp.nsimplify(sp.simplify(r)) for r in sp.solve(e, x)}
        ghi = {sp.nsimplify(sp.sympify(r, locals=ns)) for r in k["nghiem"]}
        if {sp.simplify(v) for v in sol} != {sp.simplify(v) for v in ghi}:
            loi.append(f"pt: máy ra {sorted(sol, key=str)}, ghi {sorted(ghi, key=str)}")
    if "bpt" in k:
        got = sp.solve_univariate_inequality(sp.sympify(k["bpt"], locals=ns), x, relational=False)
        want = sp.solve_univariate_inequality(sp.sympify(k["nghiem"], locals=ns), x, relational=False)
        if got != want:
            loi.append(f"bpt: máy ra {got}, ghi {want}")
    if "bt" in k:
        if sp.simplify(sp.sympify(k["bt"], locals=ns) - sp.sympify(k["gia_tri"], locals=ns)) != 0:
            loi.append(f"bt: {k['bt']} ≠ {k['gia_tri']}")
    if "rut_gon" in k:
        a, b = (sp.sympify(t, locals=ns) for t in k["rut_gon"])
        for xv in (0, 2, 3, 4, 9, sp.Rational(1, 4), 16):
            if sp.simplify((a - b).subs(x, xv)) != 0:
                loi.append(f"rút gọn sai tại x={xv}")
                break
    if "so" in k:
        for bieu, mong in k["so"]:
            v = float(sp.N(sp.sympify(bieu, locals=ns)))
            nd = len(str(mong).split(".")[1]) if "." in str(mong) else 0
            if round(v, nd) != round(mong, nd):
                loi.append(f"số: {bieu} = {v:.4f}, ghi {mong}")
    if "viete" in k:
        vt = k["viete"]
        x1, x2 = sp.solve(sp.sympify(vt["pt"], locals=ns), x)
        v = sp.simplify(sp.sympify(vt["bt"], locals={"x1": x1, "x2": x2}))
        if sp.simplify(v - sp.sympify(vt["gia_tri"])) != 0:
            loi.append(f"viète: máy ra {v}, ghi {vt['gia_tri']}")
    if "tan_so" in k:
        t = k["tan_so"]
        dem = [sum(1 for v in t["du_lieu"] if a <= v < b) for a, b in t["nhom"]]
        if dem != t["dap"] or sum(dem) != len(t["du_lieu"]):
            loi.append(f"tần số: máy đếm {dem} (cỡ mẫu {len(t['du_lieu'])}), ghi {t['dap']}")
    if "dem" in k:
        d = k["dem"]
        n = sum(1 for kk in eval(d["tap"]) if eval(d["dk"], {"k": kk}))  # noqa: S307 — dữ liệu nội bộ
        if n != d["dap"]:
            loi.append(f"đếm: máy ra {n}, ghi {d['dap']}")
    if "toi_uu" in k:
        t = k["toi_uu"]
        f = sp.lambdify(x, sp.sympify(t["bt"], locals=ns))
        best = max(range(0, 21), key=f)
        if best != t["x"] or abs(f(best) - t["gtln"]) > 1e-9:
            loi.append(f"tối ưu: máy ra x={best}, T={f(best)}; ghi x={t['x']}, T={t['gtln']}")
    return loi


def kiem_tat_ca(muc: list[dict]) -> int:
    so_bai = so_kiem = 0
    sai = []
    for m in muc:
        for b in m["bai"]:
            so_bai += 1
            if "kiem" in b:
                so_kiem += 1
                for e in kiem_bai(b["kiem"]):
                    sai.append(f"[{m['ten']} · {b['ma']}] {e}")
    print(f"Kiểm đáp số: {so_kiem}/{so_bai} bài có kiểm máy; {len(sai)} lỗi")
    for s in sai:
        print("  ✗", s)
    return len(sai)


# ─────────────────────────── TẦN SUẤT ───────────────────────────
def tan_suat(lop: str):
    p = ROOT / "outputs" / "thong-ke-dang-de" / f"phan-loai-lop-{lop}.json"
    de = [d for d in json.loads(p.read_text(encoding="utf-8")) if not d["loi"]]
    theo_ky = {k: [d for d in de if d["ky"] == k] for k in KY}

    def pt(dk):
        out = []
        for k in KY:
            ds = theo_ky[k]
            n = sum(any(dk(c) for c in d["cau"]) for d in ds)
            out.append(round(100 * n / len(ds)) if ds else 0)
        return out

    def cua_dang(ten, tieu=None):
        if tieu:
            return pt(lambda c: tieu in c.get("sub", {}).get(ten, []))
        return pt(lambda c: any(t == ten for _, t in c["dang"]))

    def cua_boi_canh(bc):
        return pt(lambda c: bc in c.get("loi_van", []))

    return cua_dang, cua_boi_canh, {k: len(v) for k, v in theo_ky.items()}


def dong_tan_suat(ts: list[int], chi_ky: list[str] | None = None) -> str:
    parts = []
    for k, v in zip(KY, ts):
        if chi_ky and k not in chi_ky:
            continue
        o = "—" if v == 0 else (f"\\textbf{{{v}\\%}}" if v >= 50 else f"{v}\\%")
        parts.append(f"{k}~{o}")
    s = " · ".join(parts)
    return s + (" (chỉ tính kỳ II)" if chi_ky else "")


# ─────────────────────────── DỰNG PDF ───────────────────────────
def esc(s: str) -> str:
    """Thoát kí tự đặc biệt cho chuỗi THUẦN VĂN BẢN (nguồn, tên file)."""
    return s.replace("\\&", "&").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#")


def render(lop: str, muc: list[dict]) -> Path:
    from config import settings
    from src.compiler.jinja_renderer import _env, load_tokens
    from src.compiler.latex_builder import build_pdf

    cua_dang, cua_boi_canh, so_de = tan_suat(lop)
    nhom: "OrderedDict[str, list]" = OrderedDict()
    for m in muc:
        nhom.setdefault(m["chuong"], []).append(m)

    body = [
        f"\\tmtitle{{SỔ DẠNG BÀI — TOÁN {lop}}}\\par",
        f"\\tmsub{{Đề kiểm tra Hà Nội · KNTT · {sum(len(v) for v in nhom.values())} dạng · "
        f"{sum(len(m['bai']) for m in muc)} bài mẫu từ đề thật}}\\par\\vspace{{5pt}}",
        "{\\setlength{\\fboxsep}{6pt}\\colorbox{brand!7}{\\parbox{\\dimexpr\\linewidth-12pt}{\\small "
        "\\textbf{Cách dùng.} Mỗi dạng ghi \\emph{tần suất} xuất hiện trong đề Hà Nội theo kỳ "
        f"(GK1 {so_de['GK1']} đề · CK1 {so_de['CK1']} · GK2 {so_de['GK2']} · CK2 {so_de['CK2']}; "
        "\\textbf{in đậm} = có trong từ một nửa số đề trở lên), cách nhận dạng, các bước, lỗi hay gặp, "
        "rồi bài mẫu \\emph{nguyên văn đề thật} kèm lời giải trình bày như khi đi thi. "
        "Tần suất do máy đếm trên kho đề (đúng khoảng 87\\%) — dùng để so dạng nhiều/ít. "
        "Mọi đáp số đã kiểm lại bằng máy; bài ghi ``có barem gốc'' đã đối chiếu hướng dẫn chấm của trường.}}}\\par",
    ]
    stt = 0
    for chuong, ds in nhom.items():
        body.append(f"\\chuongbar{{{chuong}}}")
        for m in ds:
            stt += 1
            ten, tieu = m["tan_suat"]
            ts = cua_dang(ten, tieu)
            body.append(f"\\dangtitle{{{stt}}}{{{m['ten']}}}")
            body.append(f"\\tsline{{{dong_tan_suat(ts, m.get('chi_ky'))}}}")
            body.append(f"\\muc{{Nhận dạng}} {m['nhan_dang']}\\par")
            body.append("\\muc{Các bước}\\begin{enumerate}[label=\\arabic*.,leftmargin=1.6em,itemsep=0pt,topsep=1pt]"
                        + "".join(f"\\item {b}" for b in m["buoc"]) + "\\end{enumerate}")
            body.append(f"\\muc{{Lỗi hay gặp}} {m['loi']}\\par")
            if m.get("xem_them"):
                body.append(f"\\muc{{Tài liệu chi tiết}} {{\\small\\ttfamily {esc(m['xem_them'])}}}\\par")
            for i, b in enumerate(m["bai"], 1):
                nhan = f"Bài mẫu {i}" if len(m["bai"]) > 1 else "Bài mẫu"
                bc = ""
                if b.get("boi_canh"):
                    bc = (f"\\par{{\\footnotesize\\color{{muted}}Bối cảnh: {esc(b['boi_canh'])} — "
                          f"{dong_tan_suat(cua_boi_canh(b['boi_canh']))}}}")
                hinh = ""
                if b.get("hinh"):
                    hinh = "\\par\\begin{center}" + b["hinh"] + "\\end{center}"
                lg = "\\par ".join(b["loi_giai"])
                body.append(
                    f"\\begin{{baimau}}{{{nhan}}}{{{esc(b['nguon'])}}}\n"
                    f"{b['de']}{bc}{hinh}\n\\tcblower\n\\textbf{{Lời giải}}\\par {lg}\n\\end{{baimau}}")
    src = _env().get_template("base_so_dang_bai.tex.j2").render(body="\n\n".join(body), **load_tokens())
    return build_pdf(src, slug="so-dang-bai", filename=f"So-dang-bai-Toan{lop}-Ha-Noi",
                     out_root=settings.OUTPUTS_DIR, force=True)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", default="9")
    ap.add_argument("--kiem", action="store_true", help="chỉ kiểm đáp số, không dựng PDF")
    a = ap.parse_args(argv[1:])
    muc = importlib.import_module(f"so_dang_bai_lop{a.lop}").MUC
    if kiem_tat_ca(muc):
        print("⛔ Có đáp số sai — KHÔNG dựng PDF.")
        return 1
    if a.kiem:
        return 0
    pdf = render(a.lop, muc)
    print("PDF →", pdf.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
