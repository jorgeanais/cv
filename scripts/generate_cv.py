#!/usr/bin/env python3
"""Generate localized, full CV LaTeX documents from the master YAML file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "cv_data.yaml"
TEMPLATE_FILE = ROOT / "templates" / "cv_template.tex"
DEFAULT_OUTPUT_DIR = ROOT / "output" / "tex"


def localized(value: Any, language: str) -> str:
    """Return a localized scalar while allowing plain strings in the YAML."""
    if value is None:
        return ""
    if isinstance(value, dict):
        if language not in value:
            raise ValueError(f"Missing '{language}' translation in {value!r}")
        return str(value[language])
    return str(value)


def date_value(value: Any, language: str) -> str:
    text = localized(value, language)
    return re.sub(r"(?<=\d)\s*-\s*(?=\d)", "--", text)


def section_title(data: dict[str, Any], key: str, language: str) -> str:
    titles = data["metadata"]["section_titles"]
    return localized(titles.get(key, key.replace("_", " ").title()), language)


def render_experience(items: list[dict[str, Any]], language: str, macro: str = "workitem") -> str:
    output = []
    for item in items:
        dates = date_value(item.get("dates", ""), language)
        title = localized(item.get("title", ""), language)
        subtitle = localized(item.get("subtitle", ""), language)
        location = localized(item.get("location", ""), language)
        comment = localized(item.get("titlecomment", ""), language)
        third = f"{subtitle}, {location}" if subtitle and location else subtitle or location
        output.append(f"\\{macro}{{{dates}}}{{{title}}}{{{third}}}{{{comment}}}")
    return "\n".join(output)


def render_section(key: str, section: dict[str, Any], data: dict[str, Any], language: str) -> str:
    title = section_title(data, key, language)
    lines = [f"\\section*{{{title}}}"]
    section_type = section.get("type")
    items = section.get("items", [])

    if section_type == "experience":
        macro = "eduitem" if key == "education" else "workitem"
        lines.append(render_experience(items, language, macro))
    elif section_type == "labeled_text":
        for item in items:
            label = localized(item.get("label", ""), language)
            content = localized(item.get("content", ""), language)
            lines.append(f"\\skillitem{{{label}}}{{{content}}}")
    elif section_type == "mixed":
        for item in items:
            kind = item.get("kind")
            label = localized(item.get("label", ""), language)
            if kind == "labeled_text":
                lines.append(f"\\skillitem{{{label}}}{{{localized(item.get('content', ''), language)}}}")
            elif kind == "labeled_bullets":
                lines.append(f"\\skillitem{{{label}}}{{")
                lines.append("\\begin{itemize}")
                lines.extend(f"    \\item {localized(bullet, language)}" for bullet in item.get("bullets", []))
                lines.append("\\end{itemize}}")
            else:
                raise ValueError(f"Unknown mixed item kind '{kind}' in section '{key}'")
    else:
        raise ValueError(f"Unknown section type '{section_type}' for '{key}'")
    return "\n".join(lines)


def render_content(data: dict[str, Any], language: str) -> str:
    metadata = data["metadata"]
    contact_titles = metadata["contact_titles"]
    contact = data["contact-info"]["items"]
    name = metadata["name"]
    lines = [f"{{\\LARGE \\textcolor{{DarkCornflowerBlue}}{{{name}}}}} \\\\", ""]
    lines += ["\\begin{minipage}{\\linewidth}", "\\begin{multicols}{2}"]
    lines.append(f"{localized(contact_titles['nationality'], language)}: {localized(metadata['nationality'], language)}\\\\")
    lines.append(f"{localized(contact_titles['address'], language)}: {localized(metadata['address'], language)}.")
    lines.append("\\vfill\\eject")
    for item in contact:
        label = localized(item.get("label", ""), language)
        content = localized(item.get("content", ""), language)
        if "E-mail" in label or label == "Email":
            lines.append(f"{label}: \\href{{mailto:{content}}}{{{content}}}\\\\")
        else:
            lines.append(f"{label}: {content}\\\\")
    lines += ["\\end{multicols}", "\\end{minipage}", "", "\\hrule", "", "\\vspace{0.3cm}",
              "\\begin{flushright}", "  \\begin{minipage}{15 cm}",
              f"  \\textcolor{{Jet}}{{\\small {localized(metadata['summary'], language)}}}",
              "  \\end{minipage}", "\\end{flushright}", ""]

    for key, section in data.items():
        if key == "metadata" or key == "contact-info":
            continue
        lines.append(render_section(key, section, data, language))
        lines.append("")

    lines += ["\\nocite{*}", "\\printbibliography[heading=none]", "", "\\vspace{1cm}",
              "\\begin{center}", "{\\small \\today\\- \\-\\ Santiago, Chile}\\\\",
              "{\\scriptsize Full Curriculum Vit\\ae}", "\\end{center}"]
    return "\n".join(lines)


def generate(language: str, output: Path) -> None:
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    tex = template.replace("__LANGUAGE__", "spanish" if language == "es" else "english")
    tex = tex.replace("__CONTENT__", render_content(data, language))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(tex, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("language", choices=("es", "en"))
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    output = args.output or DEFAULT_OUTPUT_DIR / f"cv_jorge_anais_{args.language}.tex"
    if not output.is_absolute():
        output = ROOT / output
    generate(args.language, output)
    print(output)


if __name__ == "__main__":
    main()
