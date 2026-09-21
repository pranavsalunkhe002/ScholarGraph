import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.knowledge_graph.neo4j_connection import driver


def find_papers_by_topic(topic):
    """
    Find research papers related to a specific topic.
    """

    query = """
    MATCH (p:Paper)-[:ABOUT]->(t:Topic)
    WHERE toLower(t.name) CONTAINS toLower($topic)
    RETURN p.name AS paper
    ORDER BY p.name
    """

    with driver.session() as session:
        result = session.run(query, topic=topic)
        papers = [record["paper"] for record in result]

    return papers


def find_researchers_by_topic(topic):
    """
    Find researchers working on a specific topic.
    """

    query = """
    MATCH (r:Researcher)-[:AUTHORED]->(p:Paper)-[:ABOUT]->(t:Topic)
    WHERE toLower(t.name) CONTAINS toLower($topic)
    RETURN DISTINCT r.name AS researcher
    ORDER BY r.name
    """

    with driver.session() as session:
        result = session.run(query, topic=topic)
        researchers = [record["researcher"] for record in result]

    return researchers


def find_papers_by_researcher(researcher):
    """
    Find papers authored by a specific researcher.
    """

    query = """
    MATCH (r:Researcher)-[:AUTHORED]->(p:Paper)
    WHERE toLower(r.name) CONTAINS toLower($researcher)
    RETURN p.name AS paper
    ORDER BY p.name
    """

    with driver.session() as session:
        result = session.run(query, researcher=researcher)
        papers = [record["paper"] for record in result]

    return papers


def find_topics_by_paper(paper):
    """
    Find topics associated with a specific paper.
    """

    query = """
    MATCH (p:Paper)-[:ABOUT]->(t:Topic)
    WHERE toLower(p.name) CONTAINS toLower($paper)
    RETURN t.name AS topic
    ORDER BY t.name
    """

    with driver.session() as session:
        result = session.run(query, paper=paper)
        topics = [record["topic"] for record in result]

    return topics


if __name__ == "__main__":

    print("Testing ScholarGraph graph queries...")

    print("\nPapers related to 'Knowledge Graphs':")
    print(find_papers_by_topic("Knowledge Graphs"))

    print("\nResearchers related to 'Knowledge Graphs':")
    print(find_researchers_by_topic("Knowledge Graphs"))

    print("\nPapers by 'John Smith':")
    print(find_papers_by_researcher("John Smith"))

    print("\nTopics of 'Knowledge Graphs for Scientific Research':")
    print(find_topics_by_paper("Knowledge Graphs for Scientific Research"))

    print("\nGraph queries working successfully!")

    driver.close()