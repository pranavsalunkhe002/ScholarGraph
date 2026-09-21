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
# Load data
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
# Recommendation test cases
# --------------------------------------------------

test_cases = [

    {
        "paper_id": "P004",
        "expected_recommendations": [
            "P007",
            "P009"
        ]
    },

    {
        "paper_id": "P006",
        "expected_recommendations": [
            "P010"
        ]
    },

    {
        "paper_id": "P008",
        "expected_recommendations": [
            "P003"
        ]
    }
]


# --------------------------------------------------
# Evaluate recommendations
# --------------------------------------------------

k = 3

precision_scores = []
recall_scores = []

print("\n" + "=" * 60)
print("RECOMMENDATION QUALITY EVALUATION")
print("=" * 60)


for test in test_cases:

    paper_id = test["paper_id"]

    expected = set(
        test["expected_recommendations"]
    )

    # Find selected paper
    paper_matches = df[
        df["paper_id"] == paper_id
    ]

    if paper_matches.empty:
        print(
            "\nPaper not found:",
            paper_id
        )
        continue

    paper = paper_matches.iloc[0]

    # Create paper text
    text = (
        str(paper["title"])
        + ". "
        + str(paper["abstract"])
    )

    # Generate embedding
    embedding = model.encode(
        [text]
    )

    embedding = np.array(
        embedding
    ).astype("float32")

    # Search
    distances, indices = index.search(
        embedding,
        k + 1
    )

    recommended = []

    for index_id in indices[0]:

        recommended_id = df.iloc[
            index_id
        ]["paper_id"]

        # Remove selected paper
        if recommended_id == paper_id:
            continue

        recommended.append(
            recommended_id
        )

        if len(recommended) >= k:
            break

    recommended_set = set(
        recommended
    )

    relevant_recommendations = (
        recommended_set & expected
    )

    precision = (
        len(relevant_recommendations)
        / len(recommended_set)
        if recommended_set
        else 0
    )

    recall = (
        len(relevant_recommendations)
        / len(expected)
        if expected
        else 0
    )

    precision_scores.append(
        precision
    )

    recall_scores.append(
        recall
    )

    print("\nSelected Paper:")
    print(
        paper_id,
        "-",
        paper["title"]
    )

    print("\nExpected Recommendations:")
    print(
        ", ".join(expected)
    )

    print("\nActual Recommendations:")
    print(
        ", ".join(recommended)
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
# Overall results
# --------------------------------------------------

average_precision = np.mean(
    precision_scores
)

average_recall = np.mean(
    recall_scores
)

print("\n" + "=" * 60)
print("OVERALL RECOMMENDATION RESULTS")
print("=" * 60)

print(
    "\nAverage Precision@3:",
    round(average_precision, 4)
)

print(
    "Average Recall@3:",
    round(average_recall, 4)
)