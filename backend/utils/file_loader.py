import os

def load_text_from_file(file_path: str) -> str:
    """
    Loads text from supported document formats.
    Currently supports .txt, .md; PDFs can be added later using PyPDF2 or pdfplumber.

    You can expand this based on what formats you plan to use.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        # For unsupported formats, just ignore for now
        print(f"[Warning] Unsupported file format: {ext} ({file_path})")
        return ""
