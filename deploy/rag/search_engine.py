import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import các search engine có sẵn
from search_engine.duck_x2go_search import DuckDuckGoSearchEngine as DGS
from search_engine.firecrawl_search import FirecrawlWrapper as FW
from search_engine.google_search import GoogleSearch as GS
from search_engine.tavily_search import TavilySearch as TS
from rag.search_chromdb import search_db as search
from config.config import EMBEDDER, TAVILY_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID, FIRECRAWLER_API_KEY

# Dùng sentence-transformers để embedding và so sánh
from sentence_transformers import util


class SearchEngine:
    def __init__(self):
        self.duck = DGS()
        self.fire = FW(api_key=FIRECRAWLER_API_KEY)
        self.google = GS(api_key=GOOGLE_API_KEY, cse_id=GOOGLE_CSE_ID)
        self.tavily = TS(api_key=TAVILY_API_KEY)
        self.embedder = EMBEDDER

    def _get_text_from_results(self, engine_name, results):
        """Trích xuất text chính từ kết quả search"""
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

    def search_all(self, query: str, top_k: int = 1):
        jobs = {
            "duckduckgo": (self.duck.search, query, 5),
            "firecrawl": (self.fire.search, query, 5),
            "google": (self.google.search, query, 5),
            "tavily": (self.tavily.search, query, 5),
        }

        engines = {}
        with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
            futures = {
                executor.submit(func, arg1, arg2): name
                for name, (func, arg1, arg2) in jobs.items()
            }
            for future in as_completed(futures):
                engine_name = futures[future]
                try:
                    res = future.result()
                    engines[engine_name] = res
                except Exception as e:
                    print(f"[{engine_name}] error:", e)
                    engines[engine_name] = None

        # Tạo embedding
        query_emb = self.embedder.encode(query)
        candidates = []
        for engine_name, res in engines.items():
            texts = self._get_text_from_results(engine_name, res)
            for txt in texts:
                candidates.append({"engine": engine_name, "text": txt})

        if not candidates:
            return None

        corpus = [c["text"] for c in candidates]
        corpus_emb = self.embedder.encode(corpus)

        scores = util.cos_sim(query_emb, corpus_emb)[0]
        best_idx = int(scores.argmax())
        best_score = float(scores[best_idx])
        best_result = candidates[best_idx]

        return {
            "query": query,
            "best_engine": best_result["engine"],
            "best_text": best_result["text"],
            "similarity": best_score
        }


# if __name__ == "__main__":
#     query = "Sâu răng là gì?"
#     engine = SearchEngine()
#     result = engine.search_all(query)
#     print(json.dumps(result, ensure_ascii=False, indent=2))
