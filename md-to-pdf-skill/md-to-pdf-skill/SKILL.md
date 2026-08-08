---
name: md-to-pdf
description: >
  Convert Markdown files to well-formatted PDFs using pandoc + weasyprint with a
  print-optimized CSS stylesheet. Use this skill whenever the user wants to generate
  PDFs from Markdown files — whether a single file or a whole folder of them.
  Trigger on phrases like: "make PDFs from the MD files", "generate PDFs from my
  lessons", "convert markdown to PDF", "export as PDF", "turn these into PDFs",
  "build PDFs from markdown", or any request where .md files are the input and .pdf
  files are the desired output. Also trigger when the user asks to regenerate or
  rebuild existing PDFs from source Markdown. This skill handles dependency
  installation automatically, so trigger it even if weasyprint isn't yet installed.
---

# MD → PDF Skill

Convert Markdown files into polished, print-ready PDFs using **pandoc** (MD → HTML)
piped into **weasyprint** (HTML → PDF) with a custom print CSS stylesheet.

This pipeline produces better typographic results than pandoc's built-in PDF output
(which relies on LaTeX), and gives full CSS control over the layout including:
page size, margins, running headers, page numbers, fonts, table styling, and
right-to-left script support.

---

## Dependencies

Check for both tools before starting, and install weasyprint if missing:

```bash
# Check pandoc (system tool — should already be present)
which pandoc || echo "pandoc not found — install via system package manager"

# Check / install weasyprint
python3 -c "import weasyprint" 2>/dev/null || \
  pip install weasyprint --break-system-packages
```

weasyprint's executable lands in `~/.local/bin/` on some systems — always invoke it
as `python3 -m weasyprint` to avoid PATH issues.

---

## The Core Command

For a single file:

```bash
pandoc input.md --standalone --no-highlight -t html5 \
  --metadata title="Document Title" | \
  python3 -m weasyprint --stylesheet print.css - output.pdf
```

Key flags:
- `--standalone`: generates a complete HTML document (with `<head>`, `<body>`)
- `--no-highlight`: disables pandoc's syntax highlighting (avoids inline style conflicts)
- `-t html5`: targets HTML5 output
- `--metadata title="..."`: sets the `<title>` (suppresses pandoc's "empty title" warning)
- `-` (stdin) and `-` (stdout): weasyprint reads from stdin when given `-` as input

---

## Batch Conversion

To convert all `.md` files in a directory:

```bash
cd /path/to/md/files

for md in *.md; do
  base="${md%.md}"
  title=$(head -1 "$md" | sed 's/^# //')
  pandoc "$md" --standalone --no-highlight -t html5 \
    --metadata title="$title" | \
    python3 -m weasyprint --stylesheet print.css - "${base}.pdf" \
    2>&1 | grep -i "error\|fatal" | head -3
  echo "✓ ${base}.pdf"
done
```

The `grep -i "error\|fatal"` suppresses weasyprint's many harmless warnings (e.g.,
`box-shadow` not supported) while still surfacing real failures.

---

## CSS Stylesheet

The CSS file is what drives the PDF's appearance. If the user already has a CSS file
(e.g., `syriac_print.css`, `print.css`), use it. If not, generate a sensible default.

### Choosing / creating the CSS

1. **Use an existing file** if the user points to one or if one is present in the
   same directory as the MD files.
2. **Adapt the web CSS** if the user has a `.css` file for HTML viewing — strip out
   `box-shadow`, `@media` queries, and webkit-specific selectors, which weasyprint
   doesn't support.
3. **Generate a default** if there's nothing to work from — see the template below.

### WeasyPrint CSS compatibility notes

weasyprint does NOT support these properties (suppress in print CSS to avoid noise):
- `box-shadow`
- `overflow-x: auto`
- `transition`
- `@media (max-width: ...)` responsive breakpoints
- `-webkit-*` prefixed selectors
- `print-color-adjust` (use `-weasyprint-color-adjust: exact` instead)
- `unicode-bidi: embed`

weasyprint DOES support:
- `@page` rules (size, margins, `@top-*`, `@bottom-*` for running headers/footers)
- `string-set` for running headers
- `page-break-inside: avoid` / `break-inside: avoid`
- CSS custom properties (`--var`)
- Google Fonts via `@import url(...)`

### Default print CSS template

Use this as a starting point when generating CSS from scratch:

```css
@page {
  size: letter;
  margin: 2.2cm 2.5cm 2.5cm 2.5cm;
  @bottom-center {
    content: counter(page);
    font-size: 9pt;
    color: #888;
  }
}

html { font-size: 11pt; }

body {
  font-family: Georgia, serif;
  color: #1e1e1e;
  line-height: 1.7;
  margin: 0;
  padding: 0;
}

h1 { font-size: 22pt; border-bottom: 1pt solid #ccc; padding-bottom: 6pt; }
h2 { font-size: 16pt; margin-top: 18pt; }
h3 { font-size: 13pt; margin-top: 14pt; }
h4 { font-size: 10pt; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 16pt; }

table { width: 100%; border-collapse: collapse; margin: 10pt 0; }
th { background: #2a5c6a; color: white; padding: 6pt 10pt; font-size: 8pt;
     text-transform: uppercase; -weasyprint-color-adjust: exact; }
td { padding: 5pt 10pt; border-bottom: 0.5pt solid #ccc; }
tbody tr:nth-child(even) td { background: #f5f3ef; -weasyprint-color-adjust: exact; }

blockquote { border-left: 3pt solid #2a5c6a; padding: 6pt 12pt;
             background: #e6f2f4; margin: 10pt 0; font-style: italic; }

h1, h2, h3, h4 { page-break-after: avoid; }
table, blockquote { page-break-inside: avoid; }
tr { page-break-inside: avoid; }
```

For multilingual documents with right-to-left script (Arabic, Hebrew, Syriac):

```css
.syriac, [lang="syc"], [lang="syr"] {
  font-family: 'Noto Sans Syriac', serif;
  font-size: 1.3em;
  direction: rtl;
  line-height: 1.5;
}
```

---

## Workflow

1. **Confirm the source files** — which MD files, which directory, all of them or a subset?
2. **Confirm or create the CSS** — existing file, adapt from web CSS, or generate default?
3. **Install dependencies** if needed
4. **Run the conversion** — single file or batch loop
5. **Report results** — list each output file with its size; flag any that produced errors

Keep the output tidy: redirect weasyprint's warnings to `grep -i "error\|fatal"` so
the user sees a clean checklist of `✓ filename.pdf` lines, not a wall of warnings.

---

## Regenerating PDFs

When the user edits an MD file and wants to rebuild its PDF:

```bash
md="Lesson_01.md"
base="${md%.md}"
title=$(head -1 "$md" | sed 's/^# //')
pandoc "$md" --standalone --no-highlight -t html5 --metadata title="$title" | \
  python3 -m weasyprint --stylesheet print.css - "${base}.pdf" 2>&1 | grep -i "error\|fatal"
echo "✓ Rebuilt ${base}.pdf"
```

If the user wants to rebuild all PDFs at once (e.g., after editing the CSS), run the
full batch loop.
