import json
import torch
from sentence_transformers import util
from embedding.load_embedding import EmbeddingModel
from duckduckgo_search import DDGS
from googleapiclient.discovery import build


class SearchEngine:
    def __init__(self, engine="duckduckgo", top_k=3):
        self.engine = engine
        self.top_k = top_k
        self.embedder = EmbeddingModel()

    def _search_duckduckgo(self, query):
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=5))

    def _search_google(self, query):
        service = build("customsearch", "v1", developerKey="YOUR_API_KEY")
        res = (
            service.cse()
            .list(q=query, cx="YOUR_SEARCH_ENGINE_ID", num=5)
            .execute()
        )
        return res.get("items", [])

    def search(self, query):
        engines = {}

        if self.engine in ["duckduckgo", "all"]:
            engines["duckduckgo"] = self._search_duckduckgo(query)
        if self.engine in ["google", "all"]:
            engines["google"] = self._search_google(query)

        # Embed query
        query_emb = self.embedder.encode(query)

        candidates = []
        for engine_name, res in engines.items():
            texts = self._get_text_from_results(engine_name, res)
            for txt in texts:
                candidates.append({"engine": engine_name, "text": txt})

        if not candidates:
            return None

        # Embed corpus (không batch_size)
        corpus = [c["text"] for c in candidates]
        corpus_emb = self.embedder.encode(corpus)

        # Convert sang tensor nếu chưa phải
        if not torch.is_tensor(query_emb):
            query_emb = torch.tensor(query_emb)
        if not torch.is_tensor(corpus_emb):
            corpus_emb = torch.tensor(corpus_emb)

        # Tính cosine similarity
        scores = util.cos_sim(query_emb, corpus_emb)[0]

        best_idx = torch.argmax(scores).item()
        best_candidate = candidates[best_idx]
        best_candidate["score"] = scores[best_idx].item()

        return best_candidate

    def _get_text_from_results(self, engine_name, results):
        if engine_name == "duckduckgo":
            return [r.get("body") or r.get("title") or "" for r in results]
        elif engine_name == "google":
            return [r.get("snippet", "") for r in results]
        return []


if __name__ == "__main__":
    se = SearchEngine(engine="all", top_k=3)
    query = "Sâu răng là gì"
    result = se.search(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
