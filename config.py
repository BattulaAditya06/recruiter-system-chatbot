from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# API Keys
# -----------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# -----------------------
# Models
# -----------------------

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "models/gemini-embedding-001"
)

# -----------------------
# Paths
# -----------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

JD_DIR = DATA_DIR / "jd"

RESUME_DIR = DATA_DIR / "resumes" / "raw"

CHROMA_DB_PATH = DATA_DIR / "chroma_store"

LOG_DIR = BASE_DIR / "logs"

# Create folders automatically
LOG_DIR.mkdir(exist_ok=True)
CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

# -----------------------
# Retrieval
# -----------------------

TOP_K = 5

MAX_SHORTLIST = 3

MAX_INTERVIEW_QUESTIONS = 5