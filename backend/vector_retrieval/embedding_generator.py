import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "research_papers.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "paper_embeddings.npy"


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print("Number of papers:", len(df))


# --------------------------------------------------
# 3. Create text for embedding
# --------------------------------------------------

texts = []

for _, row in df.iterrows():

    text = (
        str(row["title"])
        + ". "
        + str(row["abstract"])
    )

    texts.append(text)


# --------------------------------------------------
# 4. Load embedding model
# --------------------------------------------------

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully!")


# --------------------------------------------------
# 5. Generate embeddings
# --------------------------------------------------

print("\nGenerating paper embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)


# --------------------------------------------------
# 6. Convert to NumPy array
# --------------------------------------------------

embeddings = np.array(embeddings)


# --------------------------------------------------
# 7. Save embeddings
# --------------------------------------------------

np.save(
    OUTPUT_PATH,
    embeddings
)


# --------------------------------------------------
# 8. Display information
# --------------------------------------------------

print("\n" + "=" * 60)
print("EMBEDDING GENERATION COMPLETED")
print("=" * 60)

print("Number of papers:", len(embeddings))
print("Embedding dimensions:", embeddings.shape[1])

print("\nEmbedding shape:", embeddings.shape)

print("\nEmbeddings saved to:")
print(OUTPUT_PATH)