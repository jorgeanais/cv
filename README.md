# CV Generator

The CV content lives in `data/cv_data.yaml`. The Python generator renders it
into the reusable `templates/cv_template.tex` template in Spanish and English.

## Structure

- `data/`: YAML data and bibliography.
- `templates/`: LaTeX template.
- `scripts/`: Python generator.
- `assets/fonts/`: CV fonts.
- `output/tex/`: generated LaTeX sources.
- `output/pdf/`: generated PDF files.
- `build/`: LaTeX auxiliary files.
- `archive/`: original LaTeX document.

## Requirements

- Python 3
- PyYAML
- XeLaTeX
- Biber

## Generate LaTeX

```bash
python3 scripts/generate_cv.py es
python3 scripts/generate_cv.py en
```

## Generate PDFs

```bash
./build_cv.sh
```

The `priority` fields in the YAML are intentionally ignored. Both generated
documents contain the complete CV.
