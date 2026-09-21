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

ENTITIES_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "entities.csv"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)
entities_df = pd.read_csv(ENTITIES_PATH)

print("Dataset loaded successfully!")
print("Extracted entities loaded successfully!")


# --------------------------------------------------
# Create ground-truth entities
# --------------------------------------------------

ground_truth = set()

for _, row in df.iterrows():

    paper_id = row["paper_id"]

    # Paper
    ground_truth.add(
        (
            paper_id,
            row["title"],
            "PAPER"
        )
    )

    # Researchers
    authors = str(row["authors"]).split(";")

    for author in authors:

        author = author.strip()

        if author:
            ground_truth.add(
                (
                    paper_id,
                    author,
                    "RESEARCHER"
                )
            )

    # Topics
    topics = str(row["topics"]).split(";")

    for topic in topics:

        topic = topic.strip()

        if topic:
            ground_truth.add(
                (
                    paper_id,
                    topic,
                    "TOPIC"
                )
            )


# --------------------------------------------------
# Create predicted entities
# --------------------------------------------------

predicted = set()

for _, row in entities_df.iterrows():

    entity_type = row["entity_type"]

    # Evaluate only our structured entity types
    if entity_type in [
        "PAPER",
        "RESEARCHER",
        "TOPIC"
    ]:

        predicted.add(
            (
                row["paper_id"],
                row["entity"],
                entity_type
            )
        )


# --------------------------------------------------
# Calculate entity-level results
# --------------------------------------------------

all_entities = sorted(
    ground_truth | predicted
)

y_true = []
y_pred = []

for entity in all_entities:

    if entity in ground_truth:
        y_true.append(1)
    else:
        y_true.append(0)

    if entity in predicted:
        y_pred.append(1)
    else:
        y_pred.append(0)


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
print("ENTITY EXTRACTION EVALUATION")
print("=" * 60)

print("\nGround-truth entities:", len(ground_truth))
print("Predicted entities:", len(predicted))

print("\nPrecision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1-score:", round(f1, 4))


# --------------------------------------------------
# Entity type statistics
# --------------------------------------------------

print("\nEntity Type Counts:")

print(
    entities_df[
        entities_df["entity_type"].isin(
            ["PAPER", "RESEARCHER", "TOPIC"]
        )
    ]["entity_type"].value_counts()
)