def build_context(query, vector_results, graph_results):
    context = []

    context.append("USER QUERY:")
    context.append(query)

    context.append("\nVECTOR RETRIEVAL RESULTS:")

    for result in vector_results:
        context.append(
            f"- {result}"
        )

    context.append("\nGRAPH RETRIEVAL RESULTS:")

    for result in graph_results:
        context.append(
            f"- {result}"
        )

    return "\n".join(context)


if __name__ == "__main__":

    query = "Who are the researchers working on Knowledge Graphs?"

    vector_results = [
        "Knowledge Graphs for Scientific Research",
        "GraphRAG for Scientific Question Answering"
    ]

    graph_results = [
        "Maria Garcia",
        "John Smith"
    ]

    context = build_context(
        query,
        vector_results,
        graph_results
    )

    print("\n" + "=" * 60)
    print("GRAPHRAG CONTEXT BUILDER")
    print("=" * 60)

    print("\n" + context)