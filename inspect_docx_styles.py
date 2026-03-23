import docx
from docx.enum.style import WD_STYLE_TYPE

def extract_styles(file_path):
    doc = docx.Document(file_path)
    # Check styles
    print(f"--- Styles in {file_path} ---")
    
    # Common elements we want to map to CSS
    # 1. Normal text (p)
    # 2. Headings (h1, h2, h3)
    # 3. Tables (table, th, td) - Syriac tables are important
    # 4. Bold/Italic formatting
    # 5. Syriac script specific fonts/alignment
    
    styles = doc.styles
    for style in styles:
        if style.type == WD_STYLE_TYPE.PARAGRAPH:
            # We only care about common ones
            if any(x in style.name.lower() for x in ['heading', 'normal', 'list']):
                print(f"Style Name: {style.name}")
                if style.font.name: print(f"  Font: {style.font.name}")
                if style.font.size: print(f"  Size: {style.font.size.pt}")
                if style.font.color and style.font.color.rgb: print(f"  Color: {style.font.color.rgb}")
                if style.font.bold: print(f"  Bold: {style.font.bold}")
                if style.paragraph_format.alignment: print(f"  Alignment: {style.paragraph_format.alignment}")

    # Inspect paragraphs directly to find ad-hoc formatting (often the case in Word)
    print("\n--- Ad-hoc Paragraph Formatting ---")
    for i, para in enumerate(doc.paragraphs[:20]): # look at first 20
        if para.text.strip():
            print(f"P{i}: '{para.text[:50]}...'")
            if para.style: print(f"  Style: {para.style.name}")
            if para.paragraph_format.alignment: print(f"  Alignment: {para.paragraph_format.alignment}")
            # Check runs for font
            for run in para.runs[:1]: # just first run
                if run.font.name: print(f"  Run Font: {run.font.name}")
                if run.font.size: print(f"  Run Size: {run.font.size.pt}")

if __name__ == "__main__":
    extract_styles("G:/My Drive/RELS/Syriac/backups/Lesson_05_Aphel_Stem.docx")
