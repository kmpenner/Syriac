#!/bin/bash
# Rebuild lesson PDFs and Syriac_Textbook.pdf from the Markdown sources.
# Also writes the web pages (<lesson>.html, syriac_web_premium.css).
# pandoc (MD -> HTML with syriac_print.css) -> headless Chrome (HTML -> PDF) -> pdfunite.
# Usage: ./build.sh            all lessons
#        ./build.sh Lesson_03  lessons matching a prefix
set -e
cd "$(dirname "$0")"
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
