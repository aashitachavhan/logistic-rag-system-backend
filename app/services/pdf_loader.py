from pypdf import PdfReader
import tempfile
import os

async def load_pdf_from_bytes(file_bytes):
    """Extract all text from PDF bytes."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        tmp_path = tmp.name
    
    try:
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


async def extract_first_page_text_from_bytes(file_bytes):
    """Extract text from the first page of PDF bytes."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        tmp_path = tmp.name
    
    try:
        reader = PdfReader(tmp_path)
        if len(reader.pages) > 0:
            return reader.pages[0].extract_text()
        return ""
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


async def load_pdf(file):
    """Extract all text from a PDF file."""
    file_bytes = await file.read()
    return await load_pdf_from_bytes(file_bytes)


async def extract_first_page_text(file):
    """Extract text from the first page of a PDF file."""
    file_bytes = await file.read()
    return await extract_first_page_text_from_bytes(file_bytes)
