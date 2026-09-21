import pandas as pd
from neo4j import GraphDatabase
from pathlib import Path


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENTITIES_PATH = PROJECT_ROOT / "data" / "processed" / "entities.csv"
RELATIONSHIPS_PATH = PROJECT_ROOT / "data" / "processed" / "relationships.csv"


# --------------------------------------------------
# 2. Neo4j configuration
# --------------------------------------------------

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "pranavs002"


# --------------------------------------------------
# 3. Connect to Neo4j
# --------------------------------------------------

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# --------------------------------------------------
# 4. Create entity nodes
# --------------------------------------------------

def create_entity(tx, entity, entity_type):

    if entity_type == "PAPER":

        tx.run(
            """
            MERGE (p:Paper {name: $entity})
            """,
            entity=entity
        )

    elif entity_type == "RESEARCHER":

        tx.run(
            """
            MERGE (r:Researcher {name: $entity})
            """,
            entity=entity
        )

    elif entity_type == "TOPIC":

        tx.run(
            """
            MERGE (t:Topic {name: $entity})
            """,
            entity=entity
        )


# --------------------------------------------------
# 5. Create relationships
# --------------------------------------------------

def create_relationship(
    tx,
    source,
    source_type,
    relationship,
    target,
    target_type
):

    if source_type == "RESEARCHER" and target_type == "PAPER":

        tx.run(
            """
            MATCH (r:Researcher {name: $source})
            MATCH (p:Paper {name: $target})
            MERGE (r)-[:AUTHORED]->(p)
            """,
            source=source,
            target=target
        )

    elif source_type == "PAPER" and target_type == "TOPIC":

        tx.run(
            """
            MATCH (p:Paper {name: $source})
            MATCH (t:Topic {name: $target})
            MERGE (p)-[:ABOUT]->(t)
            """,
            source=source,
            target=target
        )


# --------------------------------------------------
# 6. Build Knowledge Graph
# --------------------------------------------------

def build_graph():

    entities_df = pd.read_csv(ENTITIES_PATH)
    relationships_df = pd.read_csv(RELATIONSHIPS_PATH)

    print("Entities loaded:", len(entities_df))
    print("Relationships loaded:", len(relationships_df))

    with driver.session() as session:

        # Create nodes
        for _, row in entities_df.iterrows():

            session.execute_write(
                create_entity,
                row["entity"],
                row["entity_type"]
            )

        print("Entity nodes created successfully!")

        # Create relationships
        for _, row in relationships_df.iterrows():

            session.execute_write(
                create_relationship,
                row["source"],
                row["source_type"],
                row["relationship"],
                row["target"],
                row["target_type"]
            )

        print("Relationships created successfully!")


# --------------------------------------------------
# 7. Run
# --------------------------------------------------

if __name__ == "__main__":

    try:

        build_graph()

        print("\n" + "=" * 60)
        print("SCHOLARGRAPH KNOWLEDGE GRAPH CREATED!")
        print("=" * 60)

    except Exception as e:

        print("Error while building Knowledge Graph:")
        print(e)

    finally:

        driver.close()