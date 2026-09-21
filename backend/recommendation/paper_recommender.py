import sys
from pathlib import Path

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "research_papers.csv"
INDEX_PATH = PROJECT_ROOT / "vector_db" / "index.faiss"

df = pd.read_csv(DATASET_PATH)

index = faiss.read_index(str(INDEX_PATH))

model = SentenceTransformer("all-MiniLM-L6-v2")


def recommend_papers(paper_id, top_k=3):

    # Find selected paper
    paper_matches = df[df["paper_id"] == paper_id]

    if paper_matches.empty:
        print("Paper ID not found:", paper_id)
        return []

    paper = paper_matches.iloc[0]

    # Create text representation
    text = str(paper["title"]) + ". " + str(paper["abstract"])

    # Generate embedding
    embedding = model.encode([text])
    embedding = np.array(embedding).astype("float32")

    # Search for similar papers
    distances, indices = index.search(
        embedding,
        top_k + 1
    )

    print("\n" + "=" * 60)
    print("RELATED PAPER RECOMMENDATIONS")
    print("=" * 60)

    print("\nSelected Paper:")
    print(paper["paper_id"], "-", paper["title"])

    print("\nRecommended Papers:")

    recommendations = []

    for distance, index_id in zip(
        distances[0],
        indices[0]
    ):

        recommended_paper = df.iloc[index_id]

        # Don't recommend the same paper
        if recommended_paper["paper_id"] == paper_id:
            continue

        recommendation = {
            "paper_id": recommended_paper["paper_id"],
            "title": recommended_paper["title"],
            "authors": recommended_paper["authors"],
            "year": int(recommended_paper["year"]),
            "topics": recommended_paper["topics"],
            "distance": round(float(distance), 4)
        }

        recommendations.append(recommendation)

        print("\nRank:", len(recommendations))
        print("Paper ID:", recommendation["paper_id"])
        print("Title:", recommendation["title"])
        print("Topics:", recommendation["topics"])
        print("Similarity Distance:", recommendation["distance"])

        if len(recommendations) >= top_k:
            break

    return recommendations


if __name__ == "__main__":

    recommendations = recommend_papers(
        "P004",
        top_k=3
    )

    print("\nReturned recommendations:", len(recommendations))