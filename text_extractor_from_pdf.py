"""
Simple PDF text extractor.
Extracts text from a PDF and saves it to a .txt file for easy reading.

Usage:
    python text_extractor_from_pdf.py <path_to_pdf>
    python text_extractor_from_pdf.py <path_to_pdf> --output <output_txt>
"""

import sys
import argparse
from pathlib import Path

import pymupdf  # pip install pymupdf


def extract_text(pdf_path: str, output_path: str | None = None) -> str:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = pymupdf.open(str(pdf_path))
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text()
        pages.append(f"--- Page {i} ---\n{text}")
    doc.close()

    full_text = "\n".join(pages)

    if output_path is None:
        output_path = pdf_path.with_suffix(".txt")
    else:
        output_path = Path(output_path)

    output_path.write_text(full_text, encoding="utf-8")
    print(f"Extracted {len(pages)} page(s) → {output_path}")
    return str(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf", help="Path to the input PDF file")
    parser.add_argument("--output", "-o", default=None,
                        help="Path for the output .txt file (default: same name as PDF)")
    args = parser.parse_args()

    extract_text(args.pdf, args.output)
