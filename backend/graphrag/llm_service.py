def generate_answer(context):
    """
    Generate a structured research answer from GraphRAG context.
    """

    lines = context.splitlines()

    researchers = []
    researcher_papers = {}

    in_graph_section = False

    for line in lines:

        line = line.strip()

        if line == "GRAPH RETRIEVAL RESULTS:":
            in_graph_section = True
            continue

        if not in_graph_section:
            continue

        # Read researcher-paper relationships
        if line.startswith("- Researcher-Papers:"):

            relationship = line.replace(
                "- Researcher-Papers:",
                ""
            ).strip()

            if "->" in relationship:

                researcher, papers_text = relationship.split(
                    "->",
                    1
                )

                researcher = researcher.strip()

                papers = [
                    paper.strip()
                    for paper in papers_text.split(",")
                    if paper.strip()
                ]

                if researcher not in researcher_papers:
                    researcher_papers[researcher] = []

                for paper in papers:
                    if paper not in researcher_papers[researcher]:
                        researcher_papers[researcher].append(paper)

                if researcher not in researchers:
                    researchers.append(researcher)

        # Read normal researcher entries
        elif line.startswith("- Researcher:"):

            researcher = line.replace(
                "- Researcher:",
                ""
            ).strip()

            if researcher and researcher not in researchers:
                researchers.append(researcher)

    answer = "Based on the retrieved research information:\n\n"

    if researcher_papers:

        answer += "Researchers working on the selected topic:\n\n"

        for researcher in researchers:

            if researcher in researcher_papers:

                answer += f"{researcher}\n"

                for paper in researcher_papers[researcher]:
                    answer += f"- {paper}\n"

                answer += "\n"

            else:

                answer += f"{researcher}\n\n"

    elif researchers:

        answer += "Researchers working on the selected topic:\n"

        for researcher in researchers:
            answer += f"- {researcher}\n"

        answer += "\n"

    else:

        answer += "No relevant researchers were found.\n"

    return answer