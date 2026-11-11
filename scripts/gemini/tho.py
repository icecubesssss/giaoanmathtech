#!/usr/bin/env python3
"""Thợ Gemini — chạy hàng đợi việc bằng Antigravity CLI (agy).

Hệ "Claude giám đốc – Gemini thợ" (Thầy giao 11/11/2026):
  Claude ghi việc vào  storage/gemini/hang-doi/<id>.json
  Thầy chạy script này NGOÀI sandbox Claude (Terminal thường):
        python3 scripts/gemini/tho.py              # chạy hết hàng đợi
        python3 scripts/gemini/tho.py --mot <id>   # chạy một việc
        python3 scripts/gemini/tho.py --thu        # chỉ in lệnh, không gọi agy
  Kết quả: storage/gemini/xong/<id>.json  (thô + JSON bóc được)
           storage/gemini/loi/<id>.json   (khi agy lỗi/hết giờ/không ra JSON)
  Claude đọc thư mục xong/ rồi chấm.

Vì sao không để Claude gọi agy trực tiếp: sandbox Claude Code chặn
ghi ~/.gemini/antigravity-cli/ và chặn mở cổng localhost (agy cần cả hai).

Định dạng một việc (JSON):
  {
    "id": "l6-ck1-2425-banmai",
    "model": "gemini-3.8-flash-high",
    "prompt": "...",
    "files": ["inputs/refs/.../de.pdf"],      # chép vào thư mục làm việc riêng
    "schema": "scripts/gemini/schema/....json", # tuỳ chọn, ép JSON đầu ra
    "timeout": "900s",
    "effort": "high"                           # tuỳ chọn
  }
Mỗi việc chạy trong thư mục tạm CHỈ chứa các file được giao ⇒ thợ không đụng repo.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GOC = REPO / "storage" / "gemini"
HANG_DOI, XONG, LOI, LOG = (GOC / d for d in ("hang-doi", "xong", "loi", "log"))
AGY = Path(os.environ.get("AGY", Path.home() / ".gemini" / "bin" / "agy"))


def boc_json(text: str):
    """Lấy JSON kết quả từ stdout của agy (json hoặc text)."""
    text = text.strip()
    if not text:
        return None
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        obj = None
    if isinstance(obj, dict) and "status" in obj and "response" in obj:
        # vỏ của agy --output-format json: {"status","response","denied_actions",…}
        v = obj.get("structured_output") or obj.get("response")
        if isinstance(v, (dict, list)):
            return v
        return boc_json(v) if isinstance(v, str) and v.strip() else None
    if isinstance(obj, dict):
        # --output-format json: kết quả cuối thường nằm ở một trường chuỗi
        for k in ("structured_output", "structuredOutput", "result", "response", "text", "output"):
            v = obj.get(k)
            if isinstance(v, (dict, list)):
                return v
            if isinstance(v, str):
                inner = boc_json(v)
                if inner is not None:
                    return inner
        if "cau" in obj:
            return obj
    if isinstance(obj, list):
        return obj
    # văn bản có khối ```json ... ```
    if "```" in text:
        for khoi in text.split("```")[1::2]:
            khoi = khoi.removeprefix("json").strip()
            try:
                return json.loads(khoi)
            except json.JSONDecodeError:
                pass
    a, b = text.find("{"), text.rfind("}")
    if 0 <= a < b:
        try:
            return json.loads(text[a : b + 1])
        except json.JSONDecodeError:
            pass
    return None


def lenh(viec: dict, wd: Path) -> list[str]:
    cmd = [str(AGY), "-p", viec["prompt"],
           "--model", viec.get("model", "gemini-3.8-flash-high"),
           "--output-format", "json",
           "--add-dir", str(wd),
           "--print-timeout", viec.get("timeout", "900s"),
           "--log-file", str(LOG / f"{viec['id']}.agy.log"),
           "--disable-slash-commands"]
    if viec.get("schema"):
        cmd += ["--json-schema", str(REPO / viec["schema"])]
    if viec.get("effort"):
        cmd += ["--effort", viec["effort"]]
    if viec.get("tu_duyet"):
        cmd += ["--dangerously-skip-permissions"]
    return cmd


def chay(path: Path, thu: bool, tu_duyet: bool) -> bool:
    viec = json.loads(path.read_text())
    if tu_duyet:
        viec["tu_duyet"] = True
    wd = Path(tempfile.mkdtemp(prefix=f"gemini-{viec['id']}-"))
    for f in viec.get("files", []):
        shutil.copy2(REPO / f, wd / Path(f).name)
        if viec.get("render") and f.lower().endswith(".pdf"):
            # thợ không được chạy lệnh (headless tự từ chối) ⇒ dựng sẵn ảnh + text
            goc = Path(f).stem
            pdftoppm = shutil.which("pdftoppm") or "/opt/homebrew/bin/pdftoppm"
            pdftotext = shutil.which("pdftotext") or "/opt/homebrew/bin/pdftotext"
            subprocess.run([pdftoppm, "-r", str(viec.get("dpi", 120)), "-png",
                            str(wd / Path(f).name), str(wd / "trang")], check=True)
            subprocess.run([pdftotext, "-layout", str(wd / Path(f).name), str(wd / f"{goc}.txt")], check=True)
            (wd / Path(f).name).unlink()
    cmd = lenh(viec, wd)
    if thu:
        print(" ".join(repr(c) if " " in c else c for c in cmd[:2]), "<prompt>", *cmd[3:])
        shutil.rmtree(wd, ignore_errors=True)
        return True
    t0 = time.time()
    print(f"→ {viec['id']} ({viec.get('model')}) …", flush=True)
    try:
        r = subprocess.run(cmd, cwd=wd, capture_output=True, text=True,
                           timeout=int(viec.get("timeout", "900s").rstrip("s")) + 120)
        out, err, rc = r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        out, err, rc = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "TIMEOUT", -9
    giay = round(time.time() - t0, 1)
    ket_qua = boc_json(out)
    try:
        vo = json.loads(out)
        bi_chan = vo.get("denied_actions") if isinstance(vo, dict) else None
    except json.JSONDecodeError:
        bi_chan = None
    ban_ghi = {"id": viec["id"], "model": viec.get("model"), "giay": giay, "rc": rc,
               "bi_chan": bi_chan, "ket_qua": ket_qua,
               "stdout": out[-200000:], "stderr": err[-20000:]}
    dich = XONG if (rc == 0 and ket_qua is not None) else LOI
    if bi_chan:
        print(f"   ! thợ bị từ chối quyền: {bi_chan}", flush=True)
    (dich / f"{viec['id']}.json").write_text(json.dumps(ban_ghi, ensure_ascii=False, indent=1))
    path.rename(path.with_suffix(".json.da-chay"))
    shutil.rmtree(wd, ignore_errors=True)
    print(f"   {'OK' if dich is XONG else 'LỖI'} sau {giay}s → {dich.relative_to(REPO)}/{viec['id']}.json", flush=True)
    return dich is XONG


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mot", help="chỉ chạy việc có id này")
    ap.add_argument("--thu", action="store_true", help="in lệnh, không gọi agy")
    ap.add_argument("--tu-duyet", action="store_true",
                    help="thêm --dangerously-skip-permissions (chỉ khi thợ kẹt xin quyền đọc file)")
    ap.add_argument("--gioi-han", type=int, default=0, help="chạy tối đa N việc")
    ap.add_argument("--song-song", type=int, default=1, help="chạy N việc cùng lúc (mỗi việc một agy riêng)")
    a = ap.parse_args()
    for d in (HANG_DOI, XONG, LOI, LOG):
        d.mkdir(parents=True, exist_ok=True)
    if not AGY.exists():
        print(f"Không thấy agy ở {AGY}", file=sys.stderr)
        return 2
    viec = sorted(HANG_DOI.glob("*.json"))
    if a.mot:
        viec = [p for p in viec if p.stem == a.mot]
    if a.gioi_han:
        viec = viec[: a.gioi_han]
    if not viec:
        print("Hàng đợi trống.")
        return 0
    if a.song_song > 1 and not a.thu:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(a.song_song) as ex:
            ok = sum(ex.map(lambda p: chay(p, False, a.tu_duyet), viec))
    else:
        ok = sum(chay(p, a.thu, a.tu_duyet) for p in viec)
    print(f"Xong {ok}/{len(viec)} việc.")
    return 0 if ok == len(viec) else 1


if __name__ == "__main__":
    sys.exit(main())
