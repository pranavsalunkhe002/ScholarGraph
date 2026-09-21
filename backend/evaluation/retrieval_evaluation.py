import sys
from pathlib import Path

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

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
# Load dataset and vector index
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

index = faiss.read_index(
    str(INDEX_PATH)
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Dataset loaded successfully!")
print("FAISS index loaded successfully!")


# --------------------------------------------------
# Evaluation queries
# --------------------------------------------------

test_queries = [

    {
        "query": "knowledge graphs for scientific research",
        "relevant_papers": [
            "P004",
            "P007",
            "P009"
        ]
    },

    {
        "query": "semantic search and vector embeddings for academic documents",
        "relevant_papers": [
            "P008"
        ]
    },

    {
        "query": "recommendation of researchers and research papers",
        "relevant_papers": [
            "P006",
            "P010"
        ]
    }
]


# --------------------------------------------------
# Evaluate retrieval
# --------------------------------------------------

k = 3

precision_scores = []
recall_scores = []

print("\n" + "=" * 60)
print("RETRIEVAL RELEVANCE EVALUATION")
print("=" * 60)


for test in test_queries:

    query = test["query"]
    relevant_papers = set(
        test["relevant_papers"]
    )

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        k
    )

    retrieved_papers = []

    for index_id in indices[0]:

        paper_id = df.iloc[
            index_id
        ]["paper_id"]

        retrieved_papers.append(
            paper_id
        )

    retrieved_set = set(
        retrieved_papers
    )

    relevant_retrieved = (
        retrieved_set
        & relevant_papers
    )

    precision = (
        len(relevant_retrieved)
        / len(retrieved_set)
        if retrieved_set
        else 0
    )

    recall = (
        len(relevant_retrieved)
        / len(relevant_papers)
        if relevant_papers
        else 0
    )

    precision_scores.append(
        precision
    )

    recall_scores.append(
        recall
    )

    print("\nQuery:")
    print(query)

    print("\nExpected Relevant Papers:")
    print(
        ", ".join(
            relevant_papers
        )
    )

    print("\nRetrieved Papers:")
    print(
        ", ".join(
            retrieved_papers
        )
    )

    print(
        "\nPrecision@3:",
        round(precision, 4)
    )

    print(
        "Recall@3:",
        round(recall, 4)
    )


# --------------------------------------------------
# Average results
# --------------------------------------------------

average_precision = np.mean(
    precision_scores
)

average_recall = np.mean(
    recall_scores
)

print("\n" + "=" * 60)
print("OVERALL RETRIEVAL RESULTS")
print("=" * 60)

print(
    "\nAverage Precision@3:",
    round(average_precision, 4)
)

print(
    "Average Recall@3:",
    round(average_recall, 4)
)
