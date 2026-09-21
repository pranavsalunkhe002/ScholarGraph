from pathlib import Path
import sys


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from backend.vector_retrieval.vector_search import search_papers


def test_vector_search_returns_results():

    results = search_papers(
        "knowledge graphs",
        top_k=3
    )

    assert len(results) == 3


def test_vector_search_contains_required_fields():

    results = search_papers(
        "knowledge graphs",
        top_k=3
    )

    required_fields = {
        "rank",
        "paper_id",
        "title",
        "authors",
        "abstract",
        "year",
        "topics",
        "distance"
    }

    assert required_fields.issubset(
        set(results[0].keys())
    )


def test_vector_search_returns_valid_paper_ids():

    results = search_papers(
        "knowledge graphs",
        top_k=3
    )

    for result in results:

        assert result["paper_id"].startswith("P")


def test_vector_search_ranking_is_valid():

    results = search_papers(
        "knowledge graphs",
        top_k=3
    )

    distances = [
        result["distance"]
        for result in results
    ]

    assert distances == sorted(distances)