# Manual CV Versions

`short_cv.tex` is a manually maintained English short CV for applications that
need a reduced version of the full generated CV.

The source uses the shared fonts in `../assets/fonts/` and the bibliography in
`../data/publications.bib`. Compile it from the `manual/` directory:

```bash
cd manual
xelatex short_cv.tex
biber short_cv
xelatex short_cv.tex
xelatex short_cv.tex
```

The resulting PDF is `manual/short_cv.pdf`. Edit `short_cv.tex` directly when a
specific application needs a customized version.
