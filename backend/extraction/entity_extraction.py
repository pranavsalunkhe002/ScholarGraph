import pandas as pd
import spacy
from pathlib import Path


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "research_papers.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "entities.csv"


# --------------------------------------------------
# 2. Create processed folder if it doesn't exist
# --------------------------------------------------

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 3. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print("Number of papers:", len(df))


# --------------------------------------------------
# 4. Load spaCy model
# --------------------------------------------------

nlp = spacy.load("en_core_web_sm")

print("spaCy model loaded successfully!")


# --------------------------------------------------
# 5. Entity extraction
# --------------------------------------------------

entities = []


for _, row in df.iterrows():

    paper_id = row["paper_id"]
    title = row["title"]
    abstract = row["abstract"]

    # ----------------------------------------------
    # Paper entity
    # ----------------------------------------------

    entities.append({
        "paper_id": paper_id,
        "entity": title,
        "entity_type": "PAPER",
        "source": "dataset"
    })

    # ----------------------------------------------
    # Researcher entities
    # ----------------------------------------------

    authors = str(row["authors"]).split(";")

    for author in authors:

        author = author.strip()

        if author:
            entities.append({
                "paper_id": paper_id,
                "entity": author,
                "entity_type": "RESEARCHER",
                "source": "dataset"
            })

    # ----------------------------------------------
    # Topic entities
    # ----------------------------------------------

    topics = str(row["topics"]).split(";")

    for topic in topics:

        topic = topic.strip()

        if topic:
            entities.append({
                "paper_id": paper_id,
                "entity": topic,
                "entity_type": "TOPIC",
                "source": "dataset"
            })

    # ----------------------------------------------
    # spaCy NLP entities
    # ----------------------------------------------

    text = title + ". " + abstract

    doc = nlp(text)

    for ent in doc.ents:

        entities.append({
            "paper_id": paper_id,
            "entity": ent.text,
            "entity_type": ent.label_,
            "source": "spacy"
        })


# --------------------------------------------------
# 6. Create DataFrame
# --------------------------------------------------

entities_df = pd.DataFrame(entities)


# --------------------------------------------------
# 7. Remove duplicate entities
# --------------------------------------------------

entities_df = entities_df.drop_duplicates(
    subset=["paper_id", "entity", "entity_type"]
)


# --------------------------------------------------
# 8. Save entities
# --------------------------------------------------

entities_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# 9. Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("ENTITY EXTRACTION COMPLETED")
print("=" * 60)

print("\nTotal extracted entities:", len(entities_df))

print("\nEntity types:")
print(entities_df["entity_type"].value_counts())

print("\nFirst 20 entities:")
print(entities_df.head(20).to_string(index=False))

print("\nEntities saved to:")
print(OUTPUT_PATH)