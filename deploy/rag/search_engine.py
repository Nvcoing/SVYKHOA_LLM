import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

# Import các search engine có sẵn
from search_engine.duck_x2go_search import DuckDuckGoSearchEngine as DGS
from search_engine.firecrawl_search import FirecrawlWrapper as FW
from search_engine.google_search import GoogleSearch as GS
from search_engine.tavily_search import TavilySearch as TS
from rag.search_chromdb import search_db as search
from config.config import EMBEDDER,TAVILY_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID, TAVILY_API_KEY, FIRECRAWLER_API_KEY
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

    async def search_all(self, query: str, top_k: int = 1):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            tasks = [
                loop.run_in_executor(pool, self.duck.search, query, 5),
                loop.run_in_executor(pool, self.fire.search, query, 5),
                loop.run_in_executor(pool, self.google.search, query, 5),
                loop.run_in_executor(pool, self.tavily.search, query, 5),
            ]
            duck_res, fire_res, google_res, tavily_res = await asyncio.gather(*tasks)

        # Gom dữ liệu
        engines = {
            "duckduckgo": duck_res,
            "firecrawl": fire_res,
            "google": google_res,
            "tavily": tavily_res,
        }

        # Tạo embedding
        query_emb = self.embedder.encode(query, convert_to_tensor=True)
        candidates = []
        for engine_name, res in engines.items():
            texts = self._get_text_from_results(engine_name, res)
            for txt in texts:
                candidates.append({"engine": engine_name, "text": txt})

        if not candidates:
            return None

        corpus = [c["text"] for c in candidates]
        corpus_emb = self.embedder.encode(corpus, convert_to_tensor=True)

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


if __name__ == "__main__":
    query = "Sâu răng là gì?"
    engine = SearchEngine()
    result = asyncio.run(engine.search_all(query))
    print(json.dumps(result, ensure_ascii=False, indent=2))
