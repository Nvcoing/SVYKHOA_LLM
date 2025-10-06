import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from search_engine.duck_x2go_search import DuckDuckGoSearchEngine as DGS
from search_engine.firecrawl_search import FirecrawlWrapper as FW
from search_engine.google_search import GoogleSearch as GS
from search_engine.tavily_search import TavilySearch as TS
from config.config import TAVILY_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID, FIRECRAWLER_API_KEY

class SearchEngine:
    def __init__(self):
        self.duck = DGS()
        self.fire = FW(api_key=FIRECRAWLER_API_KEY)
        self.google = GS(
            api_key=GOOGLE_API_KEY,
            cse_id=GOOGLE_CSE_ID
        )
        self.tavily = TS(api_key=TAVILY_API_KEY)

    def _normalize_results(self, engine_name, results):
        """Chuẩn hóa dữ liệu raw từ mỗi engine thành dict thống nhất"""
        items = []

        if not results:
            return items

        if engine_name == "duckduckgo":
            for r in results:
                items.append({
                    "engine": engine_name,
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body"),
                    "content": r.get("body"),
                    "highlight": r.get("body")
                })

        elif engine_name == "firecrawl":
            if "web" in results:
                for r in results["web"]:
                    items.append({
                        "engine": engine_name,
                        "title": r.get("title"),
                        "link": r.get("url"),
                        "snippet": r.get("description"),
                        "content": r.get("content"),
                        "source_domain": r.get("source_domain"),
                        "read_time": r.get("read_time_minutes"),
                        "highlight": r.get("content") or r.get("description")
                    })

        elif engine_name == "google":
            for r in results:
                items.append({
                    "engine": engine_name,
                    "title": r.get("title"),
                    "link": r.get("link"),
                    "snippet": r.get("snippet"),
                    "thumbnail": r.get("thumbnail"),
                    "content": r.get("content"),
                    "highlight": r.get("content") or r.get("snippet")
                })

        elif engine_name == "tavily":
            for r in results.get("results", []):
                items.append({
                    "engine": engine_name,
                    "title": r.get("title"),
                    "link": r.get("url"),
                    "snippet": r.get("content"),
                    "content": r.get("raw_content") if "raw_content" in r else r.get("content"),
                    "highlight": r.get("raw_content") or r.get("content")
                })

        return items

    def search_all(self, query: str, top_k: int = 3):
        jobs = {
            "duckduckgo": (self.duck.search, query, top_k),
            "firecrawl": (self.fire.search, query, top_k),
            "google": (self.google.search, query, top_k),
            "tavily": (self.tavily.search, query, top_k),
        }

        raw_results = {}
        unified_results = []
        start = time.time()

        # chạy song song
        with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
            future_to_name = {
                executor.submit(func, arg1, arg2): name
                for name, (func, arg1, arg2) in jobs.items()
            }
            for future in as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    res = future.result()
                    raw_results[name] = res
                    normalized = self._normalize_results(name, res)
                    unified_results.extend(normalized)

                    print(f"\n==== {name.upper()} RESULTS ====")
                    for i, item in enumerate(normalized, 1):
                        print(f"[{i}] {item['title']} -> {item['highlight'][:200]}...")
                except Exception as e:
                    print(f"[{name}] error:", e)
                    raw_results[name] = None

        end = time.time()
        print(f"\nThời gian thực hiện: {end - start:.2f} giây")

        return {"raw_results": raw_results, "unified_results": unified_results}


