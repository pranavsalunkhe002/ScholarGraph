import pandas as pd
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, f1_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "research_papers.csv"
)

RELATIONSHIPS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "relationships.csv"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)
relationships_df = pd.read_csv(RELATIONSHIPS_PATH)

print("Dataset loaded successfully!")
print("Extracted relationships loaded successfully!")


# --------------------------------------------------
# Create ground-truth relationships
# --------------------------------------------------

ground_truth = set()

for _, row in df.iterrows():

    paper_title = row["title"]

    # Researcher -> AUTHORED -> Paper
    authors = str(row["authors"]).split(";")

    for author in authors:

        author = author.strip()

        if author:

            ground_truth.add(
                (
                    author,
                    "AUTHORED",
                    paper_title
                )
            )

    # Paper -> ABOUT -> Topic
    topics = str(row["topics"]).split(";")

    for topic in topics:

        topic = topic.strip()

        if topic:

            ground_truth.add(
                (
                    paper_title,
                    "ABOUT",
                    topic
                )
            )


# --------------------------------------------------
# Create predicted relationships
# --------------------------------------------------

predicted = set()

for _, row in relationships_df.iterrows():

    predicted.add(
        (
            row["source"],
            row["relationship"],
            row["target"]
        )
    )


# --------------------------------------------------
# Compare relationships
# --------------------------------------------------

all_relationships = sorted(
    ground_truth | predicted
)

y_true = []
y_pred = []

for relationship in all_relationships:

    if relationship in ground_truth:
        y_true.append(1)
    else:
        y_true.append(0)

    if relationship in predicted:
        y_pred.append(1)
    else:
        y_pred.append(0)


# --------------------------------------------------
# Calculate metrics
# --------------------------------------------------

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("RELATIONSHIP EXTRACTION EVALUATION")
print("=" * 60)

print("\nGround-truth relationships:", len(ground_truth))
print("Predicted relationships:", len(predicted))

print("\nPrecision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1-score:", round(f1, 4))


# --------------------------------------------------
# Relationship type counts
# --------------------------------------------------

print("\nRelationship Type Counts:")

print(
    relationships_df[
        "relationship"
    ].value_counts()
)