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
- `manual/`: manually maintained application-specific CV versions.

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

## Manual Short CV

For applications that need a shorter, customized version, edit
`manual/short_cv.tex` directly. It uses the shared fonts and bibliography from
the repository. See `manual/README.md` for the compilation commands.

The `priority` fields in the YAML are intentionally ignored. Both generated
documents contain the complete CV.
