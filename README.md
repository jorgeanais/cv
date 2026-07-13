# CV

Repositorio para generar mi currículum vitae en dos idiomas (español e inglés)
y dos versiones (short y long). El contenido se edita en archivos YAML y se
compila a PDF mediante LaTeX, produciendo 4 documentos listos para enviar.

## Qué contiene

- `PDFs/` — los 4 PDFs ya compilados y listos para usar.
- `cv_master_source/` — el proyecto fuente completo (YAML + plantillas + script).

## Cómo funciona

Todo tu contenido vive en dos archivos YAML dentro de `cv_master_source/data/`:

- `cv_data.yaml` — cada entrada (educación, experiencia, etc.) con su texto en
  español e inglés, y una etiqueta `priority` (1 = aparece en la versión short
  y long, 2 = solo en la long).
- `sections_meta.yaml` — títulos de sección bilingües, orden, y si una sección
  completa es exclusiva de la versión long (`long_only: true`).

Un script (`build_cv.py`) lee esos YAML, filtra por idioma/longitud, y genera
los archivos `.tex` finales reutilizando tus macros LaTeX originales
(`\CVExperienceField`, etc.) sin tocar el diseño.

## Claves de los archivos YAML

### `cv_data.yaml` (contenido)

| Clave | Nivel | Propósito |
|---|---|---|
| `type` | Sección | Cómo renderizar la sección. Opciones: `labeled_text`, `experience`, `mixed`, `bullets_block` |
| `items` | Sección | Lista de entradas de esa sección |
| `es` / `en` | Campos de cada entrada | Texto bilingüe. El script elige según `--lang` |
| `priority` | Cada `item` | `1` = aparece en short y long. `2` = solo en long |
| `kind` | Solo en `skills` | Sub-tipo para secciones mixed: `labeled_text` o `labeled_bullets` |
| `bullets` | Bajo `labeled_bullets` | Lista de puntos (bilingüe) |

### `sections_meta.yaml` (estructura)

| Clave | Propósito |
|---|---|
| `key` | Identificador que enlaza con una sección en `cv_data.yaml` (ej. `education`, `experience`) |
| `title` | Nombre visible de la sección, bilingüe (`es`/`en`) |
| `long_only` | `true`/`false` — si `true`, la sección entera se omite en la versión short |
| `newpage_before` | `true`/`false` — fuerza salto de página antes de esta sección |
| `labels` | Textos reutilizables para la sección de publicaciones (`first_author`, `coauthor`) |

### Cómo interactúan

`build_cv.py` lee `sections_meta.yaml` para saber qué secciones existen y cuáles son `long_only`. El orden de aparición se determina por la posición de cada sección en el archivo. Para cada sección, lee las entradas correspondientes de `cv_data.yaml`, filtradas por `priority` y la versión seleccionada. El campo `type` determina qué plantilla Jinja2 se usa para renderizar cada entrada a LaTeX.

## Cómo editar y compilar

### 1. Configurar el entorno Python (primera vez)

```bash
cd cv_master_source
uv venv
uv sync
source .venv/bin/activate
```

Esto crea un entorno virtual e instala las dependencias (`pyyaml`, `jinja2`).

### 2. Editar el contenido

Modifica **solo** `cv_master_source/data/cv_data.yaml`. Cada entrada tiene:

```yaml
- title: "Mi experiencia"
  es: "Descripción en español"
  en: "Description in English"
  priority: 1   # 1 = short y long, 2 = solo long
```

Para cambiar títulos de sección u orden, edita `data/sections_meta.yaml`.

### 3. Compilar los PDFs

Compilar los 4 PDFs (es/en × short/long):

```bash
cd cv_master_source
source .venv/bin/activate
python3 build_cv.py --all --pdf
```

Compilar una combinación específica:

```bash
python3 build_cv.py --lang es --version long --pdf
```

Los PDFs se generan en `cv_master_source/build/` (este directorio está en
`.gitignore` y no se commitea).

### 4. Copiar los PDFs al repositorio

```bash
cp cv_master_source/build/cv_es_short/main.pdf PDFs/cv_es_short.pdf
cp cv_master_source/build/cv_es_long/main.pdf PDFs/cv_es_long.pdf
cp cv_master_source/build/cv_en_short/main.pdf PDFs/cv_en_short.pdf
cp cv_master_source/build/cv_en_long/main.pdf PDFs/cv_en_long.pdf
```

O copiar los 4 de una vez:

```bash
for f in cv_es_short cv_es_long cv_en_short cv_en_long; do
  cp cv_master_source/build/$f/main.pdf PDFs/${f}.pdf
done
```

### Requisitos

- Python 3.10+ con `uv` para gestionar dependencias
- Distribución TeX con `xelatex`, `biblatex`/`biber`, y los paquetes
  `listofitems`, `enumitem`, `csquotes`, `dirtytalk`, `oplotsymbl`
  (en Ubuntu/Debian: `texlive-full` o `texlive-latex-extra`
  + `texlive-bibtex-extra` + `texlive-science`)

## Nota técnica importante

Tu template usa `\textls` (letterspacing) de `microtype` en el nombre y los
títulos de sección. La versión de `microtype` de este entorno de prueba no
soporta letterspacing bajo XeLaTeX y lanza un error duro. Para poder compilar
y verificar el resultado, neutralizamos esas dos líneas en
`base/fields-cv/name.tex` y `base/fields-cv/section-titles.tex` (dejaron de
espaciar las letras, pero todo lo demás del diseño se mantiene intacto).
Si en tu entorno habitual (ej. Overleaf) esto ya compilaba bien, es probable
que tengas una versión de `microtype` distinta y puedas revertir el cambio
sin problema — solo vuelve a poner `\textls[...]{...}` en esos dos archivos.
