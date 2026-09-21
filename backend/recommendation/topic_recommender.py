import sys
from pathlib import Path
import os

import pandas as pd
from neo4j import GraphDatabase
from dotenv import load_dotenv


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# Load environment variables
# Load Neo4j configuration directly from .env
ENV_PATH = PROJECT_ROOT / ".env"

from dotenv import dotenv_values

config = dotenv_values(ENV_PATH)

URI = config.get("NEO4J_URI")
USERNAME = config.get("NEO4J_USERNAME")
PASSWORD = config.get("NEO4J_PASSWORD")

# Create Neo4j driver
driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def recommend_topics(paper_id, top_k=5):

    # Load research paper dataset
    dataset_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "research_papers.csv"
    )

    df = pd.read_csv(dataset_path)

    # Find paper using Paper ID
    paper_matches = df[
        df["paper_id"] == paper_id
    ]

    if paper_matches.empty:

        print("Paper ID not found:", paper_id)

        return []

    paper = paper_matches.iloc[0]

    paper_title = paper["title"]

    query = """
    MATCH (selected:Paper)-[:ABOUT]->(topic:Topic)

    WHERE selected.name = $paper_title

    MATCH (related_paper:Paper)-[:ABOUT]->(related_topic:Topic)

    WHERE related_paper <> selected
      AND NOT (selected)-[:ABOUT]->(related_topic)

    WITH related_topic,
         COUNT(DISTINCT related_paper) AS related_papers

    RETURN
        related_topic.name AS topic,
        related_papers

    ORDER BY related_papers DESC

    LIMIT $top_k
    """

    recommendations = []

    with driver.session() as session:

        result = session.run(
            query,
            paper_title=paper_title,
            top_k=top_k
        )

        for record in result:

            recommendations.append(
                {
                    "topic": record["topic"],
                    "related_papers": record["related_papers"]
                }
            )

    return recommendations


if __name__ == "__main__":

    paper_id = "P004"

    recommendations = recommend_topics(
        paper_id,
        top_k=5
    )

    print("\n" + "=" * 60)
    print("TOPIC RECOMMENDATIONS")
    print("=" * 60)

    print("\nSelected Paper:")
    print(paper_id)

    print("\nRecommended Topics:")

    if not recommendations:

        print("No related topics found.")

    else:

        for rank, recommendation in enumerate(
            recommendations,
            start=1
        ):

            print("\nRank:", rank)

            print(
                "Topic:",
                recommendation["topic"]
            )

            print(
                "Related Papers:",
                recommendation["related_papers"]
            )

    driver.close()