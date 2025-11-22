import os
from typing import List, Dict, Any
from fastapi import UploadFile
from backend.utils.file_loader import load_text_from_file
from backend.utils.html_parser import parse_html_structure

async def ingest_files(files: List[UploadFile]) -> Dict[str, Any]:
    """
    Ingest uploaded support documents and HTML file, extract useful info,
    and build a structured knowledge base.
    """
    if not files:
        raise ValueError("No files uploaded for ingestion.")
    
    docs_text = []
    html_content = None

    upload_dir = "backend/data/uploaded_docs"
    os.makedirs(upload_dir, exist_ok=True)

    for file in files:
        content = await file.read()  # Read only once!

        # Save file as uploaded
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)

        # If HTML file, save separately for Selenium
        if file.filename.endswith(".html"):
            html_path = "backend/data/checkout.html"
            with open(html_path, "wb") as f:
                f.write(content)
            html_content = content.decode("utf-8")  # Convert bytes to string

        else:
            text = load_text_from_file(file_path)
            if text:
                docs_text.append(text)

    # Ensure HTML content exists
    if not html_content:
        raise ValueError("⚠ Checkout HTML file is required but missing!")

    # Parse UI elements
    ui_elements = parse_html_structure(html_content)

    # Build structured knowledge base
    knowledge = {
        "requirements": docs_text,
        "ui_elements": ui_elements
    }

    return knowledge
