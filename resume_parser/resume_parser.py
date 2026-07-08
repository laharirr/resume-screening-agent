import os

from resume_parser.pdf_parser import extract_pdf_text
from resume_parser.docx_parser import extract_docx_text


def parse_resume(file_path):
    """
    Detect the file type and extract text.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")


def parse_resume_folder(folder_path):
    """
    Parse all PDF and DOCX resumes in a folder.
    """
    resumes = {}

    for filename in os.listdir(folder_path):

        if not filename.endswith((".pdf", ".docx")):
            continue

        file_path = os.path.join(folder_path, filename)

        try:
            text = parse_resume(file_path)
            resumes[filename] = text
            print(f"✅ Parsed: {filename}")

        except Exception as e:
            print(f"❌ Failed to parse {filename}: {e}")

    return resumes