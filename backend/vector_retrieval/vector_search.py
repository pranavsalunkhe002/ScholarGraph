import pandas as pd
import numpy as np
import faiss

from pathlib import Path
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "research_papers.csv"
)

INDEX_PATH = (
    PROJECT_ROOT
    / "vector_db"
    / "index.faiss"
)


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

print("Research paper dataset loaded.")


# --------------------------------------------------
# 3. Load FAISS index
# --------------------------------------------------

index = faiss.read_index(
    str(INDEX_PATH)
)

print("FAISS index loaded.")

print(
    "Number of indexed papers:",
    index.ntotal
)


# --------------------------------------------------
# 4. Load embedding model
# --------------------------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# --------------------------------------------------
# 5. Search function
# --------------------------------------------------

def search_papers(query, top_k=3):

    # Convert query into embedding
    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for rank, (distance, index_id) in enumerate(
        zip(distances[0], indices[0]),
        start=1
    ):

        paper = df.iloc[index_id]

        results.append({
            "rank": rank,
            "paper_id": paper["paper_id"],
            "title": paper["title"],
            "authors": paper["authors"],
            "abstract": paper["abstract"],
            "year": int(paper["year"]),
            "topics": paper["topics"],
            "distance": round(float(distance), 4)
        })

    return results


# --------------------------------------------------
# 6. Test searches
# --------------------------------------------------

if __name__ == "__main__":

    results = search_papers(
        "artificial intelligence for scientific research",
        top_k=3
    )

    print("\n" + "=" * 60)
    print("VECTOR SEARCH RESULTS")
    print("=" * 60)

    for result in results:
        print("\nRank:", result["rank"])
        print("Paper ID:", result["paper_id"])
        print("Title:", result["title"])
        print("Distance:", result["distance"])
        print("Topics:", result["topics"])


    results = search_papers(
        "finding researchers who can collaborate",
        top_k=3
    )

    print("\n" + "=" * 60)
    print("VECTOR SEARCH RESULTS")
    print("=" * 60)

    for result in results:
        print("\nRank:", result["rank"])
        print("Paper ID:", result["paper_id"])
        print("Title:", result["title"])
        print("Distance:", result["distance"])
        print("Topics:", result["topics"])


    results = search_papers(
        "semantic search of academic documents",
        top_k=3
    )

    print("\n" + "=" * 60)
    print("VECTOR SEARCH RESULTS")
    print("=" * 60)

    for result in results:
        print("\nRank:", result["rank"])
        print("Paper ID:", result["paper_id"])
        print("Title:", result["title"])
        print("Distance:", result["distance"])
        print("Topics:", result["topics"])