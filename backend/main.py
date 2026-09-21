from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.data.dataset_loader import load_dataset
from backend.graphrag.graphrag_pipeline import run_graphrag
from backend.recommendation.researcher_recommender import recommend_researchers
from backend.knowledge_graph.graph_queries import (
    find_papers_by_topic,
    find_researchers_by_topic
)
from backend.recommendation.paper_recommender import recommend_papers
from backend.recommendation.topic_recommender import recommend_topics
from backend.vector_retrieval.vector_search import search_papers as vector_search_papers

app = FastAPI(
    title="ScholarGraph API",
    description="Research Discovery Platform using GraphRAG",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "ScholarGraph API is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ScholarGraph API"
    }


@app.get("/papers")
def get_papers():
    df = load_dataset()

    papers = df.to_dict(orient="records")

    return {
        "count": len(papers),
        "papers": papers
    }


@app.get("/search")
def search_papers(query: str):
    df = load_dataset()

    query = query.lower().strip()

    if not query:
        return {
            "query": query,
            "count": 0,
            "results": []
        }

    mask = (
        df["title"].str.lower().str.contains(query, na=False)
        | df["abstract"].str.lower().str.contains(query, na=False)
        | df["topics"].str.lower().str.contains(query, na=False)
        | df["authors"].str.lower().str.contains(query, na=False)
    )

    results = df[mask].to_dict(orient="records")

    return {
        "query": query,
        "count": len(results),
        "results": results
    }


@app.get("/semantic-search")
def semantic_search(query: str, top_k: int = 3):
    results = vector_search_papers(
        query=query,
        top_k=top_k
    )

    return {
        "query": query,
        "count": len(results),
        "results": results
    }
@app.get("/graphrag")
def graphrag_search(
    query: str,
    topic: str = "Knowledge Graphs"
):
    answer = run_graphrag(
        query=query,
        topic=topic
    )

    return {
        "query": query,
        "topic": topic,
        "answer": answer
    }
@app.get("/recommend/papers/{paper_id}")
def paper_recommendations(
    paper_id: str,
    top_k: int = 3
):
    results = recommend_papers(
        paper_id,
        top_k=top_k
    )

    return {
        "paper_id": paper_id,
        "results": results
    }
@app.get("/recommend/researchers/{researcher_name}")
def researcher_recommendations(
    researcher_name: str,
    top_k: int = 3
):
    results = recommend_researchers(
        researcher_name,
        top_k=top_k
    )

    return {
        "researcher": researcher_name,
        "results": results
    }
@app.get("/recommend/topics/{paper_id}")
def topic_recommendations(
    paper_id: str,
    top_k: int = 5
):
    results = recommend_topics(
        paper_id,
        top_k=top_k
    )

    return {
        "paper_id": paper_id,
        "results": results
    }

@app.get("/knowledge-graph/{topic}")
def knowledge_graph(topic: str):
    researchers = find_researchers_by_topic(topic)
    papers = find_papers_by_topic(topic)

    return {
        "topic": topic,
        "researchers": researchers,
        "papers": papers
    }