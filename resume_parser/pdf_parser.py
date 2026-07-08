import fitz  # PyMuPDF

def extract_pdf_text(file_path):
    """
    Extract text from a PDF resume.
    """
    text = ""

    try:
        document = fitz.open(file_path)

        for page in document:
            text += page.get_text()

        document.close()

    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")

    return text.strip()