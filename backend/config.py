import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# Dataset paths
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "research_papers.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed"


# Vector database
VECTOR_DB_PATH = PROJECT_ROOT / "vector_db"
FAISS_INDEX_PATH = VECTOR_DB_PATH / "index.faiss"
METADATA_PATH = VECTOR_DB_PATH / "metadata.pkl"


# Neo4j configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")