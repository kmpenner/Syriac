#!/bin/bash
# Rebuild all Syriac curriculum PDFs using pandoc and weasyprint

DIR="/home/kubuntu/GoogleDrive/RELS/Syriac"
cd "$DIR" || exit

for md in Lesson_*.md; do
  # Skip files that aren't actual lessons if any
  [[ "$md" == *"dump"* ]] && continue
  
  base="${md%.md}"
  # Extract a clean title 
  title=$(grep -m 1 "^### " "$md" | sed 's/^### //')
  if [ -z "$title" ]; then
    title=$(grep -m 1 "^## " "$md" | sed 's/^## //')
  fi
  if [ -z "$title" ]; then
    title=$(grep -oP '(?<=<span class="lesson-title-text">).*?(?=</span>)' "$md" | head -1)
  fi
  if [ -z "$title" ]; then
    title="${base//_/ }"
  fi
  
  echo -n "Building ${base}.pdf... "
  
  # Run pandoc and weasyprint
  # Capture ALL output to show if there's a problem, but only flag on non-zero exit code
  output=$(pandoc "$md" --standalone --no-highlight -t html5 --metadata title="$title" | \
    weasyprint --stylesheet syriac_print.css --base-url . - "${base}.pdf" 2>&1)
  
  if [ $? -eq 0 ]; then
    echo "✓ Success"
  else
    echo "✗ Failed"
    echo "$output" | grep -i "error\|fatal\|warning"
  fi
done

echo "Batch PDF regeneration complete."
