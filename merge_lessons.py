import os
from pypdf import PdfWriter

def merge_pdfs(directory, output_filename):
    writer = PdfWriter()
    
    # Filter for lesson PDFs and sort them
    pdf_files = [f for f in os.listdir(directory) if f.startswith("Lesson_") and f.endswith(".pdf")]
    pdf_files.sort()
    
    print(f"Merging the following files in order:")
    for pdf in pdf_files:
        print(f" - {pdf}")
        file_path = os.path.join(directory, pdf)
        writer.append(file_path)
    
    with open(output_filename, "wb") as output_file:
        writer.write(output_file)
    
    print(f"\nSuccessfully created: {output_filename}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    merge_pdfs(current_dir, "Syriac_Textbook.pdf")
