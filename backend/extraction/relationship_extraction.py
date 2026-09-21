import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "research_papers.csv"
ENTITIES_PATH = PROJECT_ROOT / "data" / "processed" / "entities.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "relationships.csv"


# --------------------------------------------------
# 2. Load files
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)
entities_df = pd.read_csv(ENTITIES_PATH)

print("Dataset loaded successfully!")
print("Entities loaded successfully!")


# --------------------------------------------------
# 3. Create relationship list
# --------------------------------------------------

relationships = []


# --------------------------------------------------
# 4. Extract relationships from dataset
# --------------------------------------------------

for _, row in df.iterrows():

    paper_id = row["paper_id"]
    paper_title = row["title"]

    # ----------------------------------------------
    # Researcher → AUTHORED → Paper
    # ----------------------------------------------

    authors = str(row["authors"]).split(";")

    for author in authors:

        author = author.strip()

        if author:

            relationships.append({
                "source": author,
                "source_type": "RESEARCHER",
                "relationship": "AUTHORED",
                "target": paper_title,
                "target_type": "PAPER",
                "paper_id": paper_id
            })

    # ----------------------------------------------
    # Paper → ABOUT → Topic
    # ----------------------------------------------

    topics = str(row["topics"]).split(";")

    for topic in topics:

        topic = topic.strip()

        if topic:

            relationships.append({
                "source": paper_title,
                "source_type": "PAPER",
                "relationship": "ABOUT",
                "target": topic,
                "target_type": "TOPIC",
                "paper_id": paper_id
            })


# --------------------------------------------------
# 5. Create DataFrame
# --------------------------------------------------

relationships_df = pd.DataFrame(relationships)


# --------------------------------------------------
# 6. Remove duplicates
# --------------------------------------------------

relationships_df = relationships_df.drop_duplicates(
    subset=[
        "source",
        "source_type",
        "relationship",
        "target",
        "target_type"
    ]
)


# --------------------------------------------------
# 7. Save relationships
# --------------------------------------------------

relationships_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("RELATIONSHIP EXTRACTION COMPLETED")
print("=" * 60)

print("\nTotal relationships:", len(relationships_df))

print("\nRelationship types:")
print(
    relationships_df["relationship"].value_counts()
)

print("\nFirst 20 relationships:")

print(
    relationships_df.head(20).to_string(index=False)
)

print("\nRelationships saved to:")
print(OUTPUT_PATH)