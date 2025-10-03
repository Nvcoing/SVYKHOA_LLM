import json
from sentence_transformers import util
from config.config import EMBEDDER

class EmbeddingSelector:
    def __init__(self, model=EMBEDDER):
        self.model = model

    def _parse_results(self, search_results, top_k=None):
        candidates = []
        for engine, results in search_results.items():
            if not results:
                continue
            if engine == "duckduckgo":
                for r in results[:top_k]:
                    candidates.append({
                        "engine": engine,
                        "title": r.get("title"),
                        "snippet": r.get("body"),
                        "content": r.get("body"),
                        "highlight": r.get("body"),
                    })
            elif engine == "firecrawl" and "web" in results:
                for r in results["web"][:top_k]:
                    candidates.append({
                        "engine": engine,
                        "title": r.get("title"),
                        "snippet": r.get("description"),
                        "content": r.get("content"),
                        "highlight": r.get("content") or r.get("description"),
                    })
            elif engine == "google":
                for r in results[:top_k]:
                    candidates.append({
                        "engine": engine,
                        "title": r.get("title"),
                        "snippet": r.get("snippet"),
                        "content": r.get("content"),
                        "highlight": r.get("content") or r.get("snippet"),
                    })
            elif engine == "tavily" and "results" in results:
                for r in results["results"][:top_k]:
                    candidates.append({
                        "engine": engine,
                        "title": r.get("title"),
                        "snippet": r.get("content"),
                        "content": r.get("raw_content") if "raw_content" in r else r.get("content"),
                        "highlight": r.get("raw_content") or r.get("content"),
                    })
        return candidates

    def search_no_embed(self, search_results, top_k=3, return_json=True):
        candidates = self._parse_results(search_results, top_k)
        return json.dumps(candidates, ensure_ascii=False, indent=2) if return_json else candidates

    def search_with_embed(self, query, search_results, top_k=3, return_json=True):
        candidates = self._parse_results(search_results)
        if not candidates:
            return None
        query_emb = self.model.encode(query)
        corpus = [c["content"] or "" for c in candidates]
        corpus_emb = self.model.encode(corpus)
        scores = util.cos_sim(query_emb, corpus_emb)[0]
        sorted_idx = scores.argsort(descending=True)[:top_k]
        best = [{
            "engine": candidates[int(i)]["engine"],
            "title": candidates[int(i)]["title"],
            "snippet": candidates[int(i)]["snippet"],
            "content": candidates[int(i)]["content"],
            "highlight": (candidates[int(i)]["highlight"] or "")[:300],
            "similarity": float(scores[i])
        } for i in sorted_idx]
        result = {"query": query, "results": best}
        return json.dumps(result, ensure_ascii=False, indent=2) if return_json else result



# if __name__ == "__main__":
#     query = input("Nhập prompt: ")
#     top_k = int(input("Nhập top_k: "))

#     engine = SearchEngine()
#     all_results = engine.search_all(query, top_k=top_k)

#     selector = EmbeddingSelector()
#     best = selector.select_best(query, all_results["raw_results"], top_k=top_k, return_json=False)

#     print("\n==== BEST MATCHES ====")
#     print(json.dumps(best, ensure_ascii=False, indent=2))

#     # Truy cập trực tiếp
#     print("\nTitle tốt nhất:", best["results"][0]["title"])
#     print("Snippet:", best["results"][0]["snippet"])
#     print("Content:", best["results"][0]["content"])
#     print("Highlight:", best["results"][0]["highlight"])
