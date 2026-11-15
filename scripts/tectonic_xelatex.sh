#!/bin/bash
# Bọc tạm: tectonic -X compile <tex> --outdir <dir>  ⇒  xelatex 2 lượt (sandbox chặn Tectonic khởi tạo mạng)
# Dùng khi Tectonic panic "Attempted to create a NULL object" (sandbox Claude Code chặn SystemConfiguration):
#   TECTONIC_BIN=$PWD/scripts/tectonic_xelatex.sh .venv/bin/python -m src.main build <seed.json>
tex=""; out="."
while [ $# -gt 0 ]; do case "$1" in -X|compile) shift;; --outdir) out="$2"; shift 2;; *) tex="$1"; shift;; esac; done
cd "$(dirname "$tex")" || exit 1
for i in 1 2; do
  /Library/TeX/texbin/xelatex -interaction=nonstopmode -halt-on-error -output-directory="$out" "$(basename "$tex")" > "$out/.xelatex.log" 2>&1 || { tail -40 "$out/.xelatex.log" >&2; exit 1; }
done
