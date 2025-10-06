import json
from duck_x2go_search import DuckDuckGoSearchEngine as DGS
from firecrawl_search import FirecrawlWrapper as FW
from google_search import GoogleSearch as GS
from tavily_search import TavilySearch as TS
from embedding.load_embedding import EmbeddingModel
from sentence_transformers import util


class SearchEngine:
    def __init__(self):
        self.duck = DGS()
        self.fire = FW(api_key="fc-bcde7168d906417c9e8428486ea2ea6b")
        self.google = GS(api_key="AIzaSyATiZoYWWr-v3syCVMhOy5YSqZPcMNzvmQ", cse_id="c3d8b458cd8fd43ad")
        self.tavily = TS(api_key="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")
        self.embedder = EmbeddingModel()

    def _get_text_from_results(self, engine_name, results):
        texts = []
        if not results:
            return texts

        if engine_name == "duckduckgo":
            for r in results:
                texts.append(r.get("title", "") + " " + r.get("body", ""))
        elif engine_name == "firecrawl":
            if "web" in results:
                for r in results["web"]:
                    texts.append(r.get("title", "") + " " + r.get("content", ""))
        elif engine_name == "google":
            for r in results:
                texts.append(r.get("title", "") + " " + r.get("snippet", "") + " " + r.get("content", ""))
        elif engine_name == "tavily":
            for r in results.get("results", []):
                texts.append(r.get("title", "") + " " + r.get("content", ""))
        return texts

    def search_all(self, query: str, top_k: int = 3):
        jobs = {
            "duckduckgo": (self.duck.search, query, 3),
            "firecrawl": (self.fire.search, query, 3),
            "google": (self.google.search, query, 3),
            "tavily": (self.tavily.search, query, 3),
        }

        engines = {}
        for name, (func, arg1, arg2) in jobs.items():
            try:
                res = func(arg1, arg2)
                engines[name] = res

                # In ra ngay sau khi search
                print(f"\n==== {name.upper()} RESULTS ====")
                texts = self._get_text_from_results(name, res)
                for i, t in enumerate(texts, 1):
                    print(f"[{i}] {t[:200]}...")  # chỉ in 200 ký tự đầu
            except Exception as e:
                print(f"[{name}] error:", e)
                engines[name] = None

        # Embed prompt
        query_emb = self.embedder.encode(query)

        # Gom tất cả kết quả
        candidates = []
        for engine_name, res in engines.items():
            texts = self._get_text_from_results(engine_name, res)
            for txt in texts:
                candidates.append({"engine": engine_name, "text": txt})

        if not candidates:
            return None

        # Embed toàn bộ corpus
        corpus = [c["text"] for c in candidates]
        corpus_emb = self.embedder.encode(corpus, batch_size=16, convert_to_tensor=True)

        # Tính cosine similarity
        scores = util.cos_sim(query_emb, corpus_emb)[0]

        # Chọn top_k
        sorted_idx = scores.argsort(descending=True)[:top_k]
        best_results = []
        for idx in sorted_idx:
            best_results.append({
                "engine": candidates[int(idx)]["engine"],
                "text": candidates[int(idx)]["text"],
                "similarity": float(scores[idx])
            })

        return {
            "query": query,
            "results": best_results
        }


if __name__ == "__main__":
    query = "Sâu răng là gì?"
    engine = SearchEngine()
    result = engine.search_all(query, top_k=1)

    print("\n==== FINAL BEST MATCHES ====")
    print(json.dumps(result, ensure_ascii=False, indent=2))
