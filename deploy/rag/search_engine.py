import os
import json
from tavily import TavilyClient as TV
from google_search import GoogleSearch as GS


class SearchEngine:
    def __init__(self, engine: str = "google"):
        """
        engine: 'google' hoặc 'tavily'
        """
        self.engine = engine

        if engine == "google":
            self.client = GS()
        elif engine == "tavily":
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                raise ValueError("Thiếu TAVILY_API_KEY trong .env")
            self.client = TV(api_key=api_key)
        else:
            raise ValueError("Engine không hợp lệ. Chọn 'google' hoặc 'tavily'.")

    def search(self, query: str, n: int = 5, fetch_content: bool = True):
        if self.engine == "google":
            return self.client.search(query, n)
        elif self.engine == "tavily":
            return self.client.search(
                query=query,
                max_results=n,
                include_raw_content=fetch_content
            )

    def get_result(self, results, index: int, field: str):
        if self.engine == "google":
            return self.client.get_result(results, index, field)
        elif self.engine == "tavily":
            try:
                return results["results"][index].get(field)
            except (IndexError, KeyError):
                return None

    def pretty_print(self, data):
        print(json.dumps(data, indent=2, ensure_ascii=False))


# if __name__ == "__main__":
#     # Google
#     gs = SearchEngine(engine="google")
#     g_results = gs.search("DFT technology JSC là công ty gì", n=5)
#     gs.pretty_print(g_results)
#     print("\n🏷️ Tiêu đề đầu tiên:", gs.get_result(g_results, 0, "title"))

#     # Tavily
#     ts = SearchEngine(engine="tavily")
#     t_results = ts.search("Tôi bị ợ chua và đau bụng", n=5, fetch_content=True)
#     ts.pretty_print(t_results)
