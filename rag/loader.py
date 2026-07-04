"""
loader.py

Loads Job Descriptions and Resume files.

Responsibilities
----------------
✔ Load Resume PDFs
✔ Load Job Description TXT
✔ Return raw text

Does NOT
---------
✘ Chunk
✘ Embed
✘ Store
✘ Retrieve
"""
from config import JD_DIR, RESUME_DIR
from pathlib import Path
from typing import List, Dict
import sys
import fitz

from config import JD_DIR, RESUME_DIR
from utils.logger import logger


# -------------------------------------------------------
# PDF Loader
# -------------------------------------------------------

def load_pdf(file_path: Path) -> str:
    """Read a PDF and return extracted text."""

    try:

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        logger.info(f"Loaded Resume : {file_path.name}")

        return text.strip()

    except Exception as e:

        logger.error(f"Error reading {file_path.name}")

        logger.error(e)

        return ""


# -------------------------------------------------------
# Text Loader
# -------------------------------------------------------

def load_text_file(file_path: Path) -> str:
    """Read a text file."""

    try:

        text = file_path.read_text(encoding="utf-8")

        logger.info(f"Loaded JD : {file_path.name}")

        return text.strip()

    except Exception as e:

        logger.error(e)

        return ""


# -------------------------------------------------------
# Load Job Description
# -------------------------------------------------------

def load_job_description(filename: str) -> str:

    jd_file = JD_DIR / filename

    if not jd_file.exists():

        raise FileNotFoundError(
            f"{filename} not found."
        )

    return load_text_file(jd_file)


# -------------------------------------------------------
# Load All Resume PDFs
# -------------------------------------------------------

def load_all_resumes() -> List[Dict]:

    resumes = []

    pdf_files = sorted(
        RESUME_DIR.glob("*.pdf")
    )

    logger.info(f"{len(pdf_files)} resumes found.")

    for pdf in pdf_files:

        text = load_pdf(pdf)

        if text:

            resumes.append({

                "candidate_name": pdf.stem,

                "resume_file": pdf.name,

                "text": text

            })

    logger.info(
        f"{len(resumes)} resumes successfully loaded."
    )

    return resumes


# -------------------------------------------------------
# Test
# -------------------------------------------------------

if __name__ == "__main__":

    resumes = load_all_resumes()

    print()

    print("=" * 60)

    print(f"Total Resumes : {len(resumes)}")

    print("=" * 60)

    if resumes:

        print()

        print(resumes[0]["candidate_name"])

        print()

        print(resumes[0]["text"][:1000])