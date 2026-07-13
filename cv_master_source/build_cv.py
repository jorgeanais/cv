#!/usr/bin/env python3
"""
Generador del CV maestro de Jorge Anais Vilchez.

Uso:
    python3 build_cv.py --lang es --version long
    python3 build_cv.py --lang en --version short
    python3 build_cv.py --all          # genera las 4 combinaciones

Lee data/cv_data.yaml + data/sections_meta.yaml, filtra por idioma y
prioridad, renderiza con las plantillas Jinja2 en templates/, y arma un
directorio de compilación completo (fuentes, setup, fields-cv, main.tex)
listo para compilar con xelatex.
"""
import argparse
import re
import shutil
import subprocess
from pathlib import Path

import bibtexparser
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
BASE = ROOT / "base"
BUILD = ROOT / "build"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES)),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


def load_data():
    with open(DATA / "cv_data.yaml", encoding="utf-8") as f:
        cv_data = yaml.safe_load(f)
    with open(DATA / "sections_meta.yaml", encoding="utf-8") as f:
        meta = yaml.safe_load(f)
    return cv_data, meta


def keep(item_priority, version):
    """version 'short' solo conserva priority==1; 'long' lo conserva todo."""
    if version == "long":
        return True
    return item_priority == 1


def render_experience(items, lang, version):
    tpl = env.get_template("experience_item.tex.j2")
    parts = []
    for it in items:
        if not keep(it["priority"], version):
            continue
        parts.append(
            tpl.render(
                dates=it["dates"][lang],
                title=it["title"][lang],
                subtitle=it["subtitle"][lang],
                location=it["location"][lang],
                titlecomment=it["titlecomment"][lang],
            )
        )
    return "\n\\interexpsegmentsep\n\n".join(parts)


def render_labeled_text_section(items, lang, version):
    tpl = env.get_template("labeled_text.tex.j2")
    parts = []
    for it in items:
        if not keep(it["priority"], version):
            continue
        parts.append(tpl.render(label=it["label"][lang], content=it["content"][lang]))
    return "\n\\interlblsegmentsep\n\n".join(parts)


def render_skills(items, lang, version):
    txt_tpl = env.get_template("labeled_text.tex.j2")
    blt_tpl = env.get_template("labeled_bullets.tex.j2")
    parts = []
    for it in items:
        if not keep(it["priority"], version):
            continue
        if it["kind"] == "labeled_text":
            parts.append(txt_tpl.render(label=it["label"][lang], content=it["content"][lang]))
        elif it["kind"] == "labeled_bullets":
            bullets = [b[lang] for b in it["bullets"]]
            parts.append(blt_tpl.render(label=it["label"][lang], bullets=bullets))
    return "\n\\interlblsegmentsep\n\n".join(parts)


def render_bullets_block(section, lang, version):
    if not keep(section["priority"], version):
        return ""
    tpl = env.get_template("bullets_block.tex.j2")
    bullets = [it[lang] for it in section["items"]]
    return tpl.render(bullets=bullets)


JOURNAL_NAMES = {
    "\\apj": "ApJ",
    "\\aap": "A\\&A",
    "\\mnras": "MNRAS",
    "\\pasp": "PASP",
    "\\arxiv": "arXiv",
}

JOURNAL_FALLBACK = {
    "VizieR Online Data Catalog": "VizieR Online Data Catalog",
    "The Astronomer's Telegram": "ATel",
}


def _escape_latex(text):
    for char in r"&%$#_":
        text = text.replace(char, "\\" + char)
    return text


def _clean_author_name(name):
    return re.sub(r"[{}]", "", name)


def _first_author_surname(authors_raw):
    first = authors_raw.split(" and ")[0]
    cleaned = _clean_author_name(first)
    if "," in cleaned:
        return cleaned.split(",")[0]
    parts = cleaned.split()
    return parts[-1] if parts else cleaned


def _format_journal(journal_raw):
    cleaned = _clean_author_name(journal_raw).strip()
    for key, val in JOURNAL_NAMES.items():
        if key in journal_raw:
            return val
    for key, val in JOURNAL_FALLBACK.items():
        if key.lower() == cleaned.lower():
            return val
    return cleaned


def _title_from_bib(title_raw):
    cleaned = _clean_author_name(title_raw)
    cleaned = re.sub(r"^['\"]|['\"]$", "", cleaned)
    return cleaned.strip()


def render_publications(meta, lang):
    tpl = env.get_template("publications.tex.j2")

    with open(BASE / "bibliography.bib", encoding="utf-8") as f:
        bib = bibtexparser.load(f)

    entries = []
    for e in bib.entries:
        author_str = e.get("author", "")
        authors = author_str.split(" and ")
        first_clean = _clean_author_name(authors[0])
        is_first = "Anais" in first_clean or "Jorge" in first_clean
        has_anais = any(
            "Anais" in _clean_author_name(a) or "Jorge" in _clean_author_name(a)
            for a in authors
        )
        if not has_anais:
            continue

        year = e.get("year", "?")
        title = _title_from_bib(e.get("title", ""))
        first_surname = _first_author_surname(author_str)
        journal = _format_journal(e.get("journal", "")) if e.get("journal") else ""
        volume = e.get("volume", "")
        pages = e.get("pages", e.get("eid", ""))
        doi = e.get("doi", "")
        note = e.get("note", "")

        if is_first:
            coauthors = ", ".join(
                _clean_author_name(a).split(",")[0]
                for a in authors[1:]
            )
            line = (
                f"\\item {{Anais, J., {coauthors}, et. al "
                f"\\textit{{{title}}}. {note or year}}} "
            )
        else:
            parts = [f"{first_surname}, et al., including \\textbf{{Anais, J.}}"]
            parts.append(f"\\textit{{{title}}}")
            parts.append(str(year))
            if journal:
                parts.append(journal)
            if volume:
                parts.append(volume)
            if pages:
                parts.append(pages)
            if doi:
                parts.append(f"doi:{doi}")
            line = "\\item {" + ", ".join(parts) + "}"

        entries.append((int(year) if year.isdigit() else 0, line))

    entries.sort(key=lambda x: -x[0])
    body = "\n    ".join(line for _, line in entries)

    return tpl.render(body=body)


def build(lang, version, outdir=None):
    cv_data, meta = load_data()
    target = outdir or (BUILD / f"cv_{lang}_{version}")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    # copy static assets
    for sub in ["fonts", "setup", "fields-cv"]:
        shutil.copytree(BASE / sub, target / sub)
    (target / "EDITABLE-sections").mkdir()
    (target / "EDITABLE-setup").mkdir()
    shutil.copy(BASE / "setup_editable.tex", target / "EDITABLE-setup" / "setup.tex")
    shutil.copy(BASE / "bibliography.bib", target / "EDITABLE-sections" / "bibliography.bib")

    included_sections = []
    for sec in meta["sections"]:
        key = sec["key"]
        if sec.get("long_only") and version == "short":
            continue

        if key == "publications":
            content = render_publications(meta, lang)
        else:
            block = cv_data[key]
            btype = block["type"]
            if btype == "experience":
                content = render_experience(block["items"], lang, version)
            elif btype == "labeled_text":
                content = render_labeled_text_section(block["items"], lang, version)
            elif btype == "mixed":
                content = render_skills(block["items"], lang, version)
            elif btype == "bullets_block":
                content = render_bullets_block(block, lang, version)
            else:
                raise ValueError(f"Tipo desconocido: {btype} en {key}")

        if not content.strip():
            continue  # sección vacía tras filtrar -> se omite

        (target / "EDITABLE-sections" / f"{key}.tex").write_text(content, encoding="utf-8")
        included_sections.append(sec)

    # 0-all.tex
    lines = []
    for i, sec in enumerate(included_sections):
        if sec.get("newpage_before"):
            lines.append("\\newpage")
        lines.append(f"\\cvsection{{{sec['title'][lang]}}}{{{sec['key']}}}")
        if i != len(included_sections) - 1:
            lines.append("\\intersectionsep")
    (target / "EDITABLE-sections" / "0-all.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # main.tex (idéntico al original, sin la línea de postulación específica)
    main_tex = r"""\input{setup/packages.tex}

\begin{document}
    \input{fields-cv/all.tex}
    \nametitle{\topname}{\bottomname}
    \input{EDITABLE-sections/0-all.tex}
\end{document}
"""
    (target / "main.tex").write_text(main_tex, encoding="utf-8")

    print(f"[ok] Generado: {target}")
    return target


def compile_pdf(target: Path):
    cmd = ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    for _ in range(2):  # 2 pasadas por si hay referencias
        result = subprocess.run(cmd, cwd=target, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-3000:])
        print(result.stderr[-2000:])
        raise RuntimeError(f"Fallo la compilación de {target}")
    print(f"[ok] PDF: {target / 'main.pdf'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["es", "en"])
    ap.add_argument("--version", choices=["long", "short"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--pdf", action="store_true", help="Compilar a PDF con xelatex")
    args = ap.parse_args()

    combos = [(l, v) for l in ["es", "en"] for v in ["long", "short"]] if args.all else [(args.lang, args.version)]

    for lang, version in combos:
        target = build(lang, version)
        if args.pdf:
            compile_pdf(target)


if __name__ == "__main__":
    main()
