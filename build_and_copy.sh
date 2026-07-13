#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[1/2] Building all CV variants with PDF compilation..."
python cv_master_source/build_cv.py --all --pdf

echo "[2/2] Copying PDFs to PDFs/..."
mkdir -p pdfs
cp cv_master_source/build/cv_es_long/main.pdf   PDFs/cv_es_long.pdf
cp cv_master_source/build/cv_es_short/main.pdf  PDFs/cv_es_short.pdf
cp cv_master_source/build/cv_en_long/main.pdf   PDFs/cv_en_long.pdf
cp cv_master_source/build/cv_en_short/main.pdf  PDFs/cv_en_short.pdf

echo "[ok] Done. PDFs in pdfs/:"
ls -lh PDFs/*.pdf
