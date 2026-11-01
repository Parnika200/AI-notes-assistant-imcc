from io import BytesIO
from pathlib import Path

import pymupdf
from charset_normalizer import from_bytes
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


class NoTextExtractedError(Exception):
    """Raised when a document has no extractable text."""


def _extract_pdf(file_bytes):
    page_texts = []

    with pymupdf.open(stream=file_bytes, filetype="pdf") as pdf:
        for page in pdf:
            text = page.get_text(sort=True).strip()
            if text:
                page_texts.append(text)

    return "\n\n".join(page_texts)


def _extract_docx(file_bytes):
    document = Document(BytesIO(file_bytes))
    content = []

    # iter_inner_content keeps top-level paragraphs and tables in document order.
    for block in document.iter_inner_content():
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if text:
                content.append(text)

        elif isinstance(block, Table):
            for row in block.rows:
                cells = [
                    cell.text.strip().replace("\n", " ")
                    for cell in row.cells
                ]
                row_text = " | ".join(value for value in cells if value)
                if row_text:
                    content.append(row_text)

    return "\n".join(content)


def _extract_txt(file_bytes):
    match = from_bytes(file_bytes).best()

    if match is None:
        # Fallback if the detector cannot choose an encoding.
        return file_bytes.decode("utf-8", errors="replace")

    return match.output().decode("utf-8")


def extract_text_from_material(material):
    """Read an uploaded PDF, DOCX, or TXT file and return its text."""
    extension = Path(material.file_path.name).suffix.lower()

    with material.file_path.open("rb") as uploaded_file:
        file_bytes = uploaded_file.read()

    if extension == ".pdf":
        text = _extract_pdf(file_bytes)
    elif extension == ".docx":
        text = _extract_docx(file_bytes)
    elif extension == ".txt":
        text = _extract_txt(file_bytes)
    else:
        raise ValueError("This file type is not supported for text extraction.")

    text = text.strip()

    if not text:
        raise NoTextExtractedError(
            "No selectable text was found. Scanned PDFs may need OCR."
        )

    return text