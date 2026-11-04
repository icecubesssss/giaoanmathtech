#!/bin/bash
# build_p.sh <json> : sinh .tex qua src.main build (Tectonic lỗi sandbox), rồi xelatex 3 bản
cd /Users/admin/Documents/thaitd/Code/giaoanMathtech
J=$1
.venv/bin/python -m src.main build "$J" >/dev/null 2>&1
SLUG=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['slug'])" "$J")
O=$(dirname "$J" | sed 's#inputs/seeds#outputs#')/$SLUG
S=${TEXDIR:-$TMPDIR/tex}_$SLUG
mkdir -p $S; export TEXMFVAR=$S TEXMFCACHE=$S
cd "$O"
for T in *.tex; do N=${T%.tex}; r=0
  for i in 1 2; do xelatex -interaction=nonstopmode -halt-on-error -output-directory=$S $T > $S/$N.log$i 2>&1; r=$?; done
  if [ $r = 0 ]; then cp $S/$N.pdf . ; shasum -a 256 $T | cut -d' ' -f1 | tr -d '\n' > $T.sha256; echo "$N: $(pdfinfo $N.pdf | grep Pages)"; else echo "$N LỖI"; grep -m3 "^!" $S/$N.log; fi
done
