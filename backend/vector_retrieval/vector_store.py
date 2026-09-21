import numpy as np
import faiss
import pickle
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EMBEDDINGS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "paper_embeddings.npy"
)

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "research_papers.csv"
)

VECTOR_DB_PATH = PROJECT_ROOT / "vector_db"

INDEX_PATH = VECTOR_DB_PATH / "index.faiss"

METADATA_PATH = VECTOR_DB_PATH / "metadata.pkl"


# --------------------------------------------------
# 2. Create vector_db folder
# --------------------------------------------------

VECTOR_DB_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 3. Load embeddings
# --------------------------------------------------

embeddings = np.load(
    EMBEDDINGS_PATH
)

print("Embeddings loaded successfully!")

print(
    "Embedding shape:",
    embeddings.shape
)


# --------------------------------------------------
# 4. Convert to float32
# --------------------------------------------------

embeddings = embeddings.astype(
    "float32"
)


# --------------------------------------------------
# 5. Create FAISS index
# --------------------------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)


# --------------------------------------------------
# 6. Add embeddings to index
# --------------------------------------------------

index.add(
    embeddings
)


# --------------------------------------------------
# 7. Save FAISS index
# --------------------------------------------------

faiss.write_index(
    index,
    str(INDEX_PATH)
)


# --------------------------------------------------
# 8. Load paper metadata
# --------------------------------------------------

df = pd.read_csv(
    DATASET_PATH
)


# --------------------------------------------------
# 9. Create metadata
# --------------------------------------------------

metadata = []

for _, row in df.iterrows():

    metadata.append(
        {
            "paper_id": row["paper_id"],
            "title": row["title"],
            "authors": row["authors"],
            "year": row["year"],
            "topics": row["topics"]
        }
    )


# --------------------------------------------------
# 10. Save metadata
# --------------------------------------------------

with open(
    METADATA_PATH,
    "wb"
) as file:

    pickle.dump(
        metadata,
        file
    )


# --------------------------------------------------
# 11. Display information
# --------------------------------------------------

print("\n" + "=" * 60)
print("FAISS VECTOR INDEX CREATED")
print("=" * 60)

print("Vector dimension:", dimension)
print("Number of vectors:", index.ntotal)

print("\nMetadata records:", len(metadata))

print("\nIndex saved to:")
print(INDEX_PATH)

print("\nMetadata saved to:")
print(METADATA_PATH)