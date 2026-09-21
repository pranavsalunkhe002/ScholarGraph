import { useState } from "react";
//import { graphRAGSearch, semanticSearch } from "./services/api";
import "./App.css";
import {
  graphRAGSearch,
  semanticSearch,
  recommendPapers,
  recommendResearchers,
  recommendTopics,
} from "./services/api";
function App() {
  const [query, setQuery] = useState("");
  const [topic, setTopic] = useState("Knowledge Graphs");
  const [answer, setAnswer] = useState("");
  const [papers, setPapers] = useState([]);
  const [recommendedPapers, setRecommendedPapers] = useState([]);
  const [recommendedResearchers, setRecommendedResearchers] = useState([]);
  const [recommendedTopics, setRecommendedTopics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError("");
   setAnswer("");
   setPapers([]);
   setRecommendedPapers([]);
   setRecommendedResearchers([]);
   setRecommendedTopics([]);

    try {
      const ragResult = await graphRAGSearch(query, topic);
const searchResult = await semanticSearch(query, 5);

setAnswer(ragResult.answer);
setPapers(searchResult.results);

if (searchResult.results.length > 0) {
  const selectedPaperId =
    searchResult.results[0].paper_id;

  const paperRecommendations =
    await recommendPapers(
      selectedPaperId,
      3
    );

  const topicRecommendations =
    await recommendTopics(
      selectedPaperId,
      5
    );

  setRecommendedPapers(
    paperRecommendations.results
  );

  setRecommendedTopics(
    topicRecommendations.results
  );
}

const researcherMatches = [
  "Alice Brown",
  "John Smith",
  "Maria Garcia",
  "Robert Wilson",
];

const matchedResearcher =
  researcherMatches.find((researcher) =>
    ragResult.answer.includes(researcher)
  );

if (matchedResearcher) {
  const researcherRecommendations =
    await recommendResearchers(
      matchedResearcher,
      3
    );

  setRecommendedResearchers(
    researcherRecommendations.results
  );
}
    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to the ScholarGraph backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      <header className="header">
  <div className="header-content">
    <div>
      <h1>ScholarGraph</h1>
      <p>GraphRAG Research Discovery Platform</p>
    </div>

    <nav className="nav">
      <span>Research</span>
      <span>Knowledge Graph</span>
      <span>Recommendations</span>
    </nav>
  </div>
</header>

      <main className="container">

        <section className="hero">
          <h2>Discover Research Knowledge</h2>

          <p>
            Search research papers, researchers and
            relationships using semantic search and
            knowledge graphs.
          </p>

          <div className="search-box">

            <input
              type="text"
              placeholder="Ask a research question..."
              value={query}
              onChange={(event) =>
                setQuery(event.target.value)
              }
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleSearch();
                }
              }}
            />

            <select
              value={topic}
              onChange={(event) =>
                setTopic(event.target.value)
              }
            >
              <option value="Knowledge Graphs">
                Knowledge Graphs
              </option>

              <option value="Artificial Intelligence">
                Artificial Intelligence
              </option>

              <option value="Machine Learning">
                Machine Learning
              </option>

              <option value="Natural Language Processing">
                Natural Language Processing
              </option>

              <option value="Research Discovery">
                Research Discovery
              </option>

              <option value="Recommendation Systems">
                Recommendation Systems
              </option>
            </select>

            <button
              onClick={handleSearch}
              disabled={loading}
            >
              {loading ? "Searching..." : "Search"}
            </button>

          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>

       {answer && (
  <section className="answer-section">
    <h2>GraphRAG Answer</h2>

    <div className="answer-card">
      <div className="answer-intro">
        <strong>Research Discovery Result</strong>
        <p>
          The following researchers and papers were
          identified from the ScholarGraph knowledge graph.
        </p>
      </div>

      <div className="answer-content">
        {answer.split("\n").map((line, index) => {
          if (!line.trim()) {
            return <div key={index} className="answer-space" />;
          }

          if (
            line.includes("Based on") ||
            line.includes("Researchers working")
          ) {
            return (
              <p key={index} className="answer-heading">
                {line}
              </p>
            );
          }

          if (line.startsWith("- ")) {
            return (
              <div key={index} className="answer-paper">
                📄 {line.substring(2)}
              </div>
            );
          }

          return (
            <p key={index} className="answer-researcher">
              👤 {line}
            </p>
          );
        })}
      </div>
    </div>
  </section>
)}

        {papers.length > 0 && (
          <section className="papers-section">

            <h2>Related Research Papers</h2>

            <div className="paper-grid">

              {papers.map((paper) => (

                <div
                  className="paper-card"
                  key={paper.paper_id}
                >

                  <span className="paper-id">
                    {paper.paper_id}
                  </span>

                  <h3>
                    {paper.title}
                  </h3>

                  <p>
                    <strong>Authors:</strong>{" "}
                    {paper.authors}
                  </p>

                  <p>
                    <strong>Year:</strong>{" "}
                    {paper.year}
                  </p>

                  <p>
                    <strong>Topics:</strong>{" "}
                    {paper.topics}
                  </p>

                  <p className="abstract">
                    {paper.abstract}
                  </p>

                </div>

              ))}

            </div>

          </section>
        )}

        {recommendedPapers.length > 0 && (
  <section className="recommendation-section">
    <h2>Recommended Papers</h2>

    <div className="paper-grid">
      {recommendedPapers.map((paper) => (
        <div
          className="paper-card"
          key={paper.paper_id}
        >
          <span className="paper-id">
            {paper.paper_id}
          </span>

          <h3>{paper.title}</h3>

          <p>
            <strong>Authors:</strong>{" "}
            {paper.authors}
          </p>

          <p>
            <strong>Year:</strong>{" "}
            {paper.year}
          </p>

          <p>
            <strong>Topics:</strong>{" "}
            {paper.topics}
          </p>

         <p className="relevance">
  <strong>Relevance:</strong>{" "}
  {Math.max(
    0,
    Math.round((1 - paper.distance / 2) * 100)
  )}
%
</p>
        </div>
      ))}
    </div>
  </section>
)}


{recommendedResearchers.length > 0 && (
  <section className="recommendation-section">
    <h2>Recommended Researchers</h2>

    <div className="researcher-list">
      {recommendedResearchers.map(
        (researcher, index) => (
          <div
            className="researcher-card"
            key={researcher.researcher}
          >
            <span className="researcher-rank">
              #{index + 1}
            </span>

            <div>
              <h3>
                {researcher.researcher}
              </h3>

              <p>
                Shared Topics:{" "}
                {researcher.shared_topics}
              </p>
            </div>
          </div>
        )
      )}
    </div>
  </section>
)}


{recommendedTopics.length > 0 && (
  <section className="recommendation-section">
    <h2>Recommended Topics</h2>

    <div className="topic-list">
      {recommendedTopics.map(
        (topic, index) => (
          <div
            className="topic-card"
            key={topic.topic}
          >
            <span className="topic-rank">
              #{index + 1}
            </span>

            <div>
              <h3>{topic.topic}</h3>

              <p>
                Related Papers:{" "}
                {topic.related_papers}
              </p>
            </div>
          </div>
        )
      )}
    </div>
  </section>
)}
<section className="graph-section">
  <h2>Knowledge Graph</h2>

  <div className="graph-card">
    <div className="graph-node researcher-node">
      <span>👤</span>
      <strong>John Smith</strong>
      <small>Researcher</small>
    </div>

    <div className="graph-arrow">
      ↓
      <span>AUTHORED</span>
    </div>

    <div className="graph-node paper-node">
      <span>📄</span>
      <strong>Knowledge Graphs for Scientific Research</strong>
      <small>Paper</small>
    </div>

    <div className="graph-arrow">
      ↓
      <span>ABOUT</span>
    </div>

    <div className="graph-node topic-node">
      <span>🔗</span>
      <strong>Knowledge Graphs</strong>
      <small>Topic</small>
    </div>
  </div>
</section>
      </main>

    </div>
  );
}

export default App;