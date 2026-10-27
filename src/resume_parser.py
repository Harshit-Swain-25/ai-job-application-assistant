from pathlib import Path

from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_resume_text(file_path: str) -> str:
    path = Path(file_path)
    
    if not path.is_file():
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    
    suffix = path.suffix.lower()
    try:
        if suffix == ".pdf":
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif suffix == ".docx":
            document = Document(str(path))
            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        else:
            raise ValueError("Unsupported file type. Please use PDF or DOCX.")
    
    except (PdfReadError, PackageNotFoundError, OSError) as error:
        raise ValueError("Could not read the resume. Please check that the file is a valid, uncorrupted PDF or DOCX document.") from error
    
    text = text.strip()
    if not text:
        raise ValueError("No readable text found. The document may be empty or scanned.")
    
    return text
