import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const healthCheck = async () => {
  const response = await api.get("/health");
  return response.data;
};

export const semanticSearch = async (query, topK = 3) => {
  const response = await api.get("/semantic-search", {
    params: {
      query: query,
      top_k: topK,
    },
  });

  return response.data;
};

export const graphRAGSearch = async (
  query,
  topic = "Knowledge Graphs"
) => {
  const response = await api.get("/graphrag", {
    params: {
      query: query,
      topic: topic,
    },
  });

  return response.data;
};
export const recommendPapers = async (
  paperId,
  topK = 3
) => {
  const response = await api.get(
    `/recommend/papers/${paperId}`,
    {
      params: {
        top_k: topK,
      },
    }
  );

  return response.data;
};


export const recommendResearchers = async (
  researcherName,
  topK = 3
) => {
  const response = await api.get(
    `/recommend/researchers/${encodeURIComponent(
      researcherName
    )}`,
    {
      params: {
        top_k: topK,
      },
    }
  );

  return response.data;
};


export const recommendTopics = async (
  paperId,
  topK = 5
) => {
  const response = await api.get(
    `/recommend/topics/${paperId}`,
    {
      params: {
        top_k: topK,
      },
    }
  );

  return response.data;
};
export default api;