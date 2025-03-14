import fitz
import os

from util.constants import PROJECT_DIR

def split_pdf_by_page_count(pdf_path, output_dir, pages_per_split=20):
    """Splits a PDF into multiple smaller PDFs with a fixed number of pages each."""
    os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Extract filename without extension
    split_count = (total_pages // pages_per_split) + (1 if total_pages % pages_per_split else 0)

    for i in range(split_count):
        start_page = i * pages_per_split
        end_page = min(start_page + pages_per_split, total_pages)

        new_pdf = fitz.open()
        for page in range(start_page, end_page):
            new_pdf.insert_pdf(doc, from_page=page, to_page=page)

        output_path = os.path.join(output_dir, f"{base_name}_part{i+1}.pdf")
        new_pdf.save(output_path)
        new_pdf.close()
        print(f"Saved: {output_path}")

    doc.close()

split_pdf_by_page_count(os.path.join(PROJECT_DIR, "resources/Gale1pdf.pdf"), os.path.join(PROJECT_DIR, "resources/"), pages_per_split=20)