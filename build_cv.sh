#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

command -v xelatex >/dev/null || { echo "Error: xelatex no está instalado." >&2; exit 1; }
command -v biber >/dev/null || { echo "Error: biber no está instalado." >&2; exit 1; }

for language in es en; do
    tex="output/tex/cv_jorge_anais_${language}.tex"
    build_dir="build/${language}"
    mkdir -p "$build_dir" output/pdf

    python3 scripts/generate_cv.py "$language" --output "$tex"
    xelatex -interaction=nonstopmode -halt-on-error \
        -output-directory="$build_dir" "$tex"
    biber --input-directory="$build_dir" --output-directory="$build_dir" \
        "cv_jorge_anais_${language}"
    xelatex -interaction=nonstopmode -halt-on-error \
        -output-directory="$build_dir" "$tex"
    xelatex -interaction=nonstopmode -halt-on-error \
        -output-directory="$build_dir" "$tex"
    cp "$build_dir/cv_jorge_anais_${language}.pdf" \
        "output/pdf/cv_jorge_anais_${language}.pdf"
done
