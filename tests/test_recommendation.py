from pathlib import Path
import sys


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from backend.recommendation.paper_recommender import recommend_papers
from backend.recommendation.researcher_recommender import (
    recommend_researchers
)
from backend.recommendation.topic_recommender import (
    recommend_topics
)


def test_paper_recommendation_returns_results():

    results = recommend_papers(
        "P004",
        top_k=3
    )

    assert len(results) > 0


def test_paper_recommendation_contains_required_fields():

    results = recommend_papers(
        "P004",
        top_k=3
    )

    required_fields = {
        "paper_id",
        "title",
        "distance"
    }

    assert required_fields.issubset(
        set(results[0].keys())
    )


def test_researcher_recommendation_returns_results():

    results = recommend_researchers(
        "John Smith",
        top_k=3
    )

    assert len(results) > 0


def test_topic_recommendation_returns_results():

    results = recommend_topics(
        "P004",
        top_k=3
    )

    assert len(results) > 0