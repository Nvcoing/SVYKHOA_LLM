import json
from sentence_transformers import util
from config.config import EMBEDDER

class EmbeddingSelector:
    def __init__(self, model = EMBEDDER):
        # Load model embedding
        self.model = model

    def select_best(self, query, search_results, top_k=3, return_json=True):
        candidates = []
        for engine_name, results in search_results.items():
            if not results:
                continue

            if engine_name == "duckduckgo":
                for r in results:
                    candidates.append({
                        "engine": engine_name,
                        "title": r.get("title"),
                        "snippet": r.get("body"),
                        "content": r.get("body"),
                        "highlight": r.get("body"),
                    })

            elif engine_name == "firecrawl" and "web" in results:
                for r in results["web"]:
                    candidates.append({
                        "engine": engine_name,
                        "title": r.get("title"),
                        "snippet": r.get("description"),
                        "content": r.get("content"),
                        "highlight": r.get("content") or r.get("description"),
                    })

            elif engine_name == "google":
                for r in results:
                    candidates.append({
                        "engine": engine_name,
                        "title": r.get("title"),
                        "snippet": r.get("snippet"),
                        "content": r.get("content"),
                        "highlight": r.get("content") or r.get("snippet"),
                    })

            elif engine_name == "tavily" and "results" in results:
                for r in results["results"]:
                    candidates.append({
                        "engine": engine_name,
                        "title": r.get("title"),
                        "snippet": r.get("content"),
                        "content": r.get("raw_content") if "raw_content" in r else r.get("content"),
                        "highlight": r.get("raw_content") or r.get("content"),
                    })

        if not candidates:
            return None

        # Encode query
        query_emb = self.model.encode(query)

        # Encode kết hợp snippet + content + highlight
        corpus = [
            f"{c['snippet'] or ''} {c['content'] or ''} {c['highlight'] or ''}"
            for c in candidates
        ]
        corpus_emb = self.model.encode(corpus)

        # Cosine similarity
        scores = util.cos_sim(query_emb, corpus_emb)[0]

        # Lấy top_k
        sorted_idx = scores.argsort(descending=True)[:top_k]
        best = []
        for idx in sorted_idx:
            c = candidates[int(idx)]
            best.append({
                "engine": c["engine"],
                "title": c["title"],
                "snippet": c["snippet"],
                "content": c["content"],
                "highlight": (c["highlight"] or "")[:300],
                "similarity": float(scores[idx])
            })

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
