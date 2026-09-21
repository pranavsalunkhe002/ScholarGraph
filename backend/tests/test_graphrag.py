from pathlib import Path
import sys


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from backend.graphrag.graphrag_pipeline import run_graphrag


def test_graphrag_returns_answer():

    answer = run_graphrag(
        "Who are the researchers working on Knowledge Graphs?",
        "Knowledge Graphs"
    )

    assert answer is not None
    assert len(answer.strip()) > 0


def test_graphrag_answer_contains_researchers():

    answer = run_graphrag(
        "Who are the researchers working on Knowledge Graphs?",
        "Knowledge Graphs"
    )

    expected_researchers = [
        "Alice Brown",
        "John Smith",
        "Maria Garcia",
        "Robert Wilson"
    ]

    for researcher in expected_researchers:

        assert researcher in answer


def test_graphrag_answer_contains_papers():

    answer = run_graphrag(
        "Who are the researchers working on Knowledge Graphs?",
        "Knowledge Graphs"
    )

    expected_papers = [
        "Knowledge Graphs for Scientific Research",
        "GraphRAG for Scientific Question Answering",
        "AI Based Patent Analysis"
    ]

    for paper in expected_papers:

        assert paper in answer


def test_graphrag_answer_does_not_contain_database_typo():

    answer = run_graphrag(
        "Who are the researchers working on Knowledge Graphs?",
        "Knowledge Graphs"
    )

    assert "ScientificQuestion" not in answer