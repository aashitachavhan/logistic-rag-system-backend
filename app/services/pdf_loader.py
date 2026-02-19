from pypdf import PdfReader
import tempfile

async def load_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        reader = PdfReader(tmp.name)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
