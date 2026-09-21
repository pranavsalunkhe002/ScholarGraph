import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.vector_retrieval.vector_search import search_papers
from backend.graphrag.graph_retriever import (
    find_papers_by_topic,
    find_researchers_by_topic,
    find_researcher_papers_by_topic
)
from backend.graphrag.context_builder import build_context
from backend.graphrag.llm_service import generate_answer


def run_graphrag(query, topic):

    print("\n" + "=" * 60)
    print("SCHOLARGRAPH GRAPHRAG PIPELINE")
    print("=" * 60)

    print("\nUser Query:")
    print(query)

    # --------------------------------------------------
    # 1. Vector Retrieval
    # --------------------------------------------------

    print("\n[1] Running Vector Retrieval...")

    vector_search_results = search_papers(
        query,
        top_k=3
    )

    vector_results = []

    for result in vector_search_results:
        vector_results.append(
            "Paper: "
            + result["title"]
            + " | Authors: "
            + result["authors"]
            + " | Topics: "
            + result["topics"]
        )

    print("\nVector Results:")

    for result in vector_search_results:
        print(
            result["rank"],
            result["paper_id"],
            result["title"]
        )

    # --------------------------------------------------
    # 2. Graph Retrieval
    # --------------------------------------------------

    print("\n[2] Running Graph Retrieval...")

    graph_papers = find_papers_by_topic(topic)
    researchers = find_researchers_by_topic(topic)
    researcher_papers = find_researcher_papers_by_topic(topic)

    graph_results = []

    for paper in graph_papers:
        graph_results.append(
            "Paper: " + paper
        )

    for researcher in researchers:
        graph_results.append(
            "Researcher: " + researcher
        )

    # print("\nDEBUG - Researcher-Paper Results:")
    # print(researcher_papers)

    for item in researcher_papers:

        researcher = item["researcher"]
        papers = item["papers"]

        formatted_papers = [
            paper.replace(
                "ScientificQuestion",
                "Scientific Question"
            )
            for paper in papers
        ]

        graph_results.append(
            "Researcher-Papers: "
            + researcher
            + " -> "
            + ", ".join(formatted_papers)
        )

    print("\nGraph Results:")

    for result in graph_results:
        print(result)

    # --------------------------------------------------
    # 3. Context Builder
    # --------------------------------------------------

    print("\n[3] Building Combined Context...")

    context = build_context(
        query,
        vector_results,
        graph_results
    )

    print("\nCombined Context:")
    print(context)

    # --------------------------------------------------
    # 4. LLM Service
    # --------------------------------------------------

    print("\n[4] Generating Answer...")

    answer = generate_answer(context)

    print("\nFinal Answer:")
    print(answer)

    return answer


# --------------------------------------------------
# Test GraphRAG Pipeline
# --------------------------------------------------

if __name__ == "__main__":

    query = (
        "Who are the researchers working on Knowledge Graphs "
        "and what papers have they published?"
    )

    topic = "Knowledge Graphs"

    run_graphrag(
        query,
        topic
    )