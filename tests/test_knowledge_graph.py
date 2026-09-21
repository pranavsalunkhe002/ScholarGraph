from pathlib import Path
import sys


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from backend.knowledge_graph.neo4j_connection import driver


def test_neo4j_connection():

    with driver.session() as session:

        result = session.run(
            "RETURN 1 AS value"
        )

        record = result.single()

        assert record["value"] == 1


def test_paper_nodes_exist():

    with driver.session() as session:

        result = session.run(
            "MATCH (p:Paper) RETURN count(p) AS count"
        )

        record = result.single()

        assert record["count"] > 0


def test_researcher_nodes_exist():

    with driver.session() as session:

        result = session.run(
            "MATCH (r:Researcher) RETURN count(r) AS count"
        )

        record = result.single()

        assert record["count"] > 0


def test_topic_nodes_exist():

    with driver.session() as session:

        result = session.run(
            "MATCH (t:Topic) RETURN count(t) AS count"
        )

        record = result.single()

        assert record["count"] > 0


def test_authored_relationships_exist():

    with driver.session() as session:

        result = session.run(
            """
            MATCH (:Researcher)-[r:AUTHORED]->(:Paper)
            RETURN count(r) AS count
            """
        )

        record = result.single()

        assert record["count"] > 0


def test_about_relationships_exist():

    with driver.session() as session:

        result = session.run(
            """
            MATCH (:Paper)-[r:ABOUT]->(:Topic)
            RETURN count(r) AS count
            """
        )

        record = result.single()

        assert record["count"] > 0