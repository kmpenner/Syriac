#!/bin/bash
# Rebuild lesson PDFs and Syriac_Textbook.pdf from the Markdown sources.
# Also writes the web pages (<lesson>.html, syriac_web_premium.css).
# pandoc (MD -> HTML with syriac_print.css) -> headless Chrome (HTML -> PDF) -> pdfunite.
# Usage: ./build.sh            all lessons
#        ./build.sh Lesson_03  lessons matching a prefix
set -e
cd "$(dirname "$0")"
# Validate markdown tables before building
python3 -c '
import glob, sys
error = False
for md in sorted(glob.glob("Lesson_[0-9][0-9]_*.md") + glob.glob("Appendix_*.md")):
    in_table, col_count, start_line = False, 0, 0
    for idx, line in enumerate(open(md, encoding="utf-8"), 1):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.split("|")[1:-1]]
            if not in_table:
                in_table, col_count, start_line = True, len(cells), idx
            elif len(cells) != col_count:
                print(f"Error: {md}:{idx} has {len(cells)} cells, expected {col_count} (table at line {start_line})", file=sys.stderr)
                error = True
        else:
            in_table = False
if error:
    sys.exit(1)
' && echo "✓ Table cell lint passed"

prof=$(mktemp -d)
for md in ${1:-Lesson_}*.md $( [ -z "$1" ] && ls Appendix_*.md ); do
  b=${md%.md}
  pandoc "$md" --standalone --no-highlight -t html5 \
    --metadata title="The Acts of Mar Yukhannan" --css syriac_print.css -o "${b}_print.html"
  pandoc "$md" --standalone --no-highlight -t html5 \
    --metadata title="The Acts of Mar Yukhannan" --css syriac_web_premium.css -o "$b.html"
  pandoc "$md" -o "$b.docx"
  google-chrome --headless=new --disable-gpu --no-pdf-header-footer --user-data-dir="$prof" \
    --print-to-pdf="$b.pdf" "file://$PWD/${b}_print.html" 2>/dev/null
  echo "✓ $b.pdf"
done
rm -rf "$prof"
pdfunite Lesson_[0-9][0-9]_*.pdf Appendix_*.pdf Syriac_Textbook.pdf && echo "✓ Syriac_Textbook.pdf ($(pdfinfo Syriac_Textbook.pdf | awk '/Pages/{print $2}') pages)"

