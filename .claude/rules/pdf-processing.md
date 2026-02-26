---
paths:
  - "**/*.pdf"
---

# Robust PDF Processing

When working with PDF files (uploaded papers, reference documents, generated manuscripts), follow this safe processing workflow to avoid token/memory issues.

## The Safe Processing Workflow

### Step 1: Check PDF Properties

Before reading, check size and page count:

```bash
pdfinfo document.pdf | grep "Pages:"
ls -lh document.pdf
```

### Step 2: Read in Chunks

Use the Read tool's `pages` parameter to process PDFs incrementally:

- **Small PDFs (1-10 pages):** Read all at once — no chunking needed
- **Medium PDFs (11-50 pages):** Read in 10-page chunks (`pages: "1-10"`, then `"11-20"`, etc.)
- **Large PDFs (50+ pages):** Read in 5-page chunks, or ask the user which sections matter most

**Maximum 20 pages per Read request.** Exceeding this will fail.

### Step 3: Process Incrementally

- Read chunks one at a time
- Extract key information from each chunk before moving on
- Build understanding progressively
- Do not try to hold all chunks in working memory simultaneously

### Step 4: Selective Deep Reading

After scanning all chunks:
- Identify the most relevant sections
- Re-read only those sections in detail
- Skip appendices, references, or less relevant sections unless specifically needed

## Splitting Large PDFs

When chunked reading is insufficient and you need individual page files:

```bash
# Using Ghostscript — split into 5-page chunks
for i in {0..9}; do
  start=$((i*5 + 1))
  end=$(((i+1)*5))
  gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
     -dFirstPage=$start -dLastPage=$end \
     -sOutputFile="document_p$(printf '%03d' $start)-$(printf '%03d' $end).pdf" \
     document.pdf 2>/dev/null
done
```

Alternative if Ghostscript fails:

```bash
pdftk document.pdf burst output document_%03d.pdf
```

## Error Handling

**If a chunk fails to process:**
1. Note the problematic chunk (e.g., "pages 21-25 failed")
2. Try smaller page ranges (1-2 pages at a time)
3. If still failing, skip and document the gap

**If splitting fails:**
1. Check tool availability: `gs --version` or `pdftk --version`
2. Try the alternative splitting method
3. If all else fails, ask the user to provide specific page ranges

**If token/memory issues persist:**
1. Process only 2-3 chunks per pass
2. Focus on sections the user identifies as most important
3. Summarize earlier chunks before reading new ones
