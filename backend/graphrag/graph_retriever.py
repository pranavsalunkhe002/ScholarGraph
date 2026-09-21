from backend.knowledge_graph.graph_queries import (
    find_papers_by_topic,
    find_researchers_by_topic
)
from backend.knowledge_graph.neo4j_connection import driver


def find_researcher_papers_by_topic(topic):
    query = """
    MATCH (researcher:Researcher)-[:AUTHORED]->(paper:Paper)
          -[:ABOUT]->(topic_node:Topic)

    WHERE toLower(topic_node.name) = toLower($topic)

    RETURN
        researcher.name AS researcher,
        collect(DISTINCT paper.name) AS papers

    ORDER BY researcher
    """

    results = []

    with driver.session() as session:

        records = session.run(
            query,
            topic=topic
        )

        for record in records:

            researcher = record["researcher"]
            papers = record["papers"]

            results.append({
                "researcher": researcher,
                "papers": papers
            })

    return results
def get_graph_results(topic):

    """
    Retrieve papers, researchers and researcher-paper
    relationships for a topic.
    """

    papers = find_papers_by_topic(topic)

    researchers = find_researchers_by_topic(topic)

    researcher_papers = find_researcher_papers_by_topic(topic)

    return {
        "papers": papers,
        "researchers": researchers,
        "researcher_papers": researcher_papers
    }