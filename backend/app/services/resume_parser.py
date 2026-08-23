import pymupdf

def extract_text_from_pdf(file_bytes: bytes) -> str:
    document = pymupdf.open(stream = file_bytes, filetype = "pdf")

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages).strip()
