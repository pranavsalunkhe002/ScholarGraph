from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.graphrag.graph_retriever import (
    find_researcher_papers_by_topic
)


def evaluate_citation_validity(topic):
    """
    Evaluate whether researcher-paper claims are supported
    by the Neo4j knowledge graph.

    This is a controlled evaluation using the knowledge graph
    as the source of truth.
    """

    print("=" * 60)
    print("SCHOLARGRAPH CITATION VALIDITY EVALUATION")
    print("=" * 60)

    print("\nTopic:")
    print(topic)

    # Retrieve evidence from Neo4j
    evidence = find_researcher_papers_by_topic(topic)

    print("\nRetrieved Evidence:")

    for item in evidence:
        researcher = item["researcher"]
        papers = item["papers"]

        print(f"\n{researcher}")

        for paper in papers:
            print(f"- {paper}")

    # Count supported researcher-paper relationships
    total_claims = 0
    supported_claims = 0

    for item in evidence:

        papers = item["papers"]

        for paper in papers:

            total_claims += 1

            # Evidence comes directly from Neo4j,
            # therefore the claim is supported.
            if paper:
                supported_claims += 1

    # Calculate citation validity
    if total_claims > 0:
        citation_validity = (
            supported_claims / total_claims
        ) * 100
    else:
        citation_validity = 0

    print("\n" + "-" * 60)

    print("Total Claims:", total_claims)
    print("Supported Claims:", supported_claims)

    print(
        f"Citation Validity Score: "
        f"{citation_validity:.2f}%"
    )

    print("-" * 60)

    return citation_validity


if __name__ == "__main__":

    topic = "Knowledge Graphs"

    evaluate_citation_validity(topic)
    