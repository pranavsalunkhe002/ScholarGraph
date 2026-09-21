import sys
from pathlib import Path

from neo4j import GraphDatabase

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "pranavs002"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def recommend_researchers(researcher_name, top_k=5):

    query = """
    MATCH (r:Researcher {name: $researcher_name})
          -[:AUTHORED]->(p:Paper)
          -[:ABOUT]->(t:Topic)
          <-[:ABOUT]-(related_p:Paper)
          <-[:AUTHORED]-(recommended:Researcher)

    WHERE recommended.name <> $researcher_name

    WITH recommended,
         COUNT(DISTINCT t) AS shared_topics

    RETURN recommended.name AS researcher,
           shared_topics
    ORDER BY shared_topics DESC
    LIMIT $top_k
    """

    with driver.session() as session:

        result = session.run(
            query,
            researcher_name=researcher_name,
            top_k=top_k
        )

        recommendations = [
            {
                "researcher": record["researcher"],
                "shared_topics": record["shared_topics"]
            }
            for record in result
        ]

    return recommendations


if __name__ == "__main__":

    researcher = "John Smith"

    recommendations = recommend_researchers(
        researcher,
        top_k=5
    )

    print("\n" + "=" * 60)
    print("RESEARCHER RECOMMENDATIONS")
    print("=" * 60)

    print("\nSelected Researcher:")
    print(researcher)

    print("\nRecommended Researchers:")

    if not recommendations:
        print("No related researchers found.")

    else:

        for rank, recommendation in enumerate(
            recommendations,
            start=1
        ):

            print("\nRank:", rank)
            print(
                "Researcher:",
                recommendation["researcher"]
            )
            print(
                "Shared Topics:",
                recommendation["shared_topics"]
            )

    driver.close()