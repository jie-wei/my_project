---
name: compile-latex
description: Multi-pass LaTeX compilation with structured result reporting
disable-model-invocation: true
argument-hint: "[filename without .tex extension, default: main]"
allowed-tools: ["Read", "Bash", "Glob"]
---

# Compile LaTeX Document

Compile a LaTeX document using XeLaTeX with full citation resolution.

**Input:** `$ARGUMENTS` — filename without `.tex` extension. Defaults to `main` if not provided.

---

## Steps

1. **Check the target file exists:**

```bash
ls paper/$ARGUMENTS.tex
```

If the file is empty or does not exist, report and stop.

2. **Compile with 3-pass sequence** (all in one command to preserve the .log for parsing before the latex-cleanup hook fires):

```bash
cd paper && \
TEXINPUTS=../docs/preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex && \
BIBINPUTS=.:$BIBINPUTS bibtex $ARGUMENTS && \
TEXINPUTS=../docs/preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex && \
TEXINPUTS=../docs/preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex && \
echo "=== PARSE LOG ===" && \
grep -cE "^(LaTeX|Package|Class) .*Warning" $ARGUMENTS.log 2>/dev/null || echo "0" && \
grep -c "^! " $ARGUMENTS.log 2>/dev/null || echo "0" && \
grep "Citation.*undefined" $ARGUMENTS.log 2>/dev/null || echo "none" && \
grep -c "Overfull" $ARGUMENTS.log 2>/dev/null || echo "0" && \
pdfinfo $ARGUMENTS.pdf 2>/dev/null | grep Pages || echo "Pages: unknown"
```

**Alternative (latexmk):**
```bash
cd paper && \
TEXINPUTS=../docs/preambles:$TEXINPUTS BIBINPUTS=.:$BIBINPUTS latexmk -xelatex -interaction=nonstopmode $ARGUMENTS.tex && \
echo "=== PARSE LOG ===" && \
grep -cE "^(LaTeX|Package|Class) .*Warning" $ARGUMENTS.log 2>/dev/null || echo "0" && \
grep -c "^! " $ARGUMENTS.log 2>/dev/null || echo "0" && \
grep "Citation.*undefined" $ARGUMENTS.log 2>/dev/null || echo "none" && \
grep -c "Overfull" $ARGUMENTS.log 2>/dev/null || echo "0" && \
pdfinfo $ARGUMENTS.pdf 2>/dev/null | grep Pages || echo "Pages: unknown"
```

3. **Open the PDF** for visual verification:
```bash
open paper/$ARGUMENTS.pdf
```

4. **Report results** using the structured output format below.

---

## Structured Output

After compilation, emit this block for agent consumption:

```
--- COMPILATION RESULT ---
STATUS: SUCCESS | FAILURE
WARNINGS: [total warning count]
ERRORS: [total error count]
PAGES: [page count]
UNDEFINED_CITATIONS: [comma-separated list or "none"]
OVERFULL_HBOX: [count]
--- END COMPILATION RESULT ---
```

Parse from the compilation log:
- STATUS: SUCCESS if PDF created and no fatal errors; FAILURE otherwise
- PAGES: from `pdfinfo` output
- UNDEFINED_CITATIONS: from `grep "Citation.*undefined"` in the .log
- OVERFULL_HBOX: from `grep -c "Overfull"` in the .log
- WARNINGS: count lines matching `^(LaTeX|Package|Class) .*Warning` in the .log
- ERRORS: count all "! " lines in the .log (LaTeX error marker)

---

## Why 3 passes?

1. First xelatex: creates `.aux` file with citation keys
2. bibtex: reads `.aux`, generates `.bbl` with formatted references
3. Second xelatex: incorporates bibliography
4. Third xelatex: resolves all cross-references with final page numbers

---

## Important

- **Parse the log BEFORE the cleanup hook fires.** The `latex-cleanup` hook deletes `.aux`, `.log`, `.bbl` files after each Bash command containing LaTeX commands. All log parsing must happen in the same Bash invocation as the compilation (compound command with `&&`).
- **Use XeLaTeX by default.** If the document requires pdflatex (e.g., uses eps figures or packages incompatible with XeLaTeX), fall back to pdflatex.
- **TEXINPUTS** is required if custom preamble files (`.sty`, `.cls`) are in `docs/preambles/`.
- **BIBINPUTS** points to `paper/` where `references.bib` lives.
- **Handle empty stubs gracefully.** If `paper/main.tex` is empty (0 bytes), report "Cannot compile: file is empty" instead of cryptic LaTeX errors.
