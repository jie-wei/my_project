# Compiling the Paper

This directory uses `latexmk` with a local `.latexmkrc`. Read this file before running any LaTeX command.

## Always

- **Run from `paper/`.** The `.latexmkrc` here sets `TEXINPUTS`, the aux directory (`.build/`), and the cleanup command. It only takes effect when `latexmk` is invoked from this directory. Running from the project root dumps aux files in the wrong place and fails to find template classes.
- **Use `latexmk -xelatex`, never raw `xelatex`/`pdflatex`/`bibtex`.** `latexmk` handles multi-pass compilation (bib, refs, toc) automatically. Raw commands leave the bibliography half-built.
- **Recompile after every edit to a `.tex` or `.bib` file.** Don't wait to be asked.

## Two Modes

This paper is split with the `subfiles` package: `main.tex` holds the preamble and a chain of `\subfile{...}` includes; section bodies live in `sections/*.tex` and `appendices/*.tex`. Each section file starts with `\documentclass[../main.tex]{subfiles}` so it can compile either as part of the full paper or on its own.

### Full paper

```
cd paper
latexmk -xelatex main.tex
```

Produces `main.pdf`. Cross-references, citations, and the bibliography only resolve in this mode.

### Single section (e.g., sharing a draft with a coauthor)

```
cd paper
latexmk -xelatex sections/01-introduction.tex
```

Produces `sections/01-introduction.pdf`, using the full preamble but only that section's content. Citations and cross-references to *other* sections won't resolve — that's expected.

## After a Successful Compile

`.latexmkrc`'s `$success_cmd` deletes `.build/` and the root aux files (`.aux`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`, `.out`, `.synctex.gz`, `.toc`) automatically. Verify that only the `.pdf` remains next to the `.tex` source. If aux files linger, something failed mid-run — check the log before rerunning.

## When Compilation Fails

`latexmk` exits non-zero and leaves `.build/` in place so the log survives. To diagnose:

1. Read `.build/<jobname>.log` — search for the first line beginning with `!` (that's the actual error; everything after it is fallout).
2. Common causes: undefined `\cite{...}` (add to `references.bib`), missing package (install via `tlmgr`), typo in a `\subfile{...}` path, missing `\begin{document}`/`\end{document}` in a subfile.
3. Fix, recompile, verify `.build/` is cleaned up.

Don't run raw `xelatex` to "see the error" — the log from `latexmk` has the same information and keeps your build state coherent.

## Adding a New Section

1. Create `sections/NN-name.tex` (or `appendices/L-name.tex`) with:
   ```latex
   \documentclass[../main.tex]{subfiles}
   \begin{document}
   \section{...}
   \end{document}
   ```
2. Add `\subfile{sections/NN-name}` to `main.tex` in the right place in the chain.
3. Recompile the full paper to confirm it's wired in.
