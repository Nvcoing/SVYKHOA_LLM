import json
from ddgs import DDGS

class DuckDuckGoSearchEngine:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 5):
        results = list(self.ddgs.text(query, max_results=max_results))
        return results

    def search_json(self, query: str, max_results: int = 5, pretty: bool = True):
        results = self.search(query, max_results)
        if pretty:
            return json.dumps(results, ensure_ascii=False, indent=2)
        return json.dumps(results, ensure_ascii=False)

# if __name__ == "__main__":
#     engine = DuckDuckGoSearchEngine()
#     query = "Tôi bị ợ chua và đau bụng"
    
#     # In ra JSON
#     print(engine.search_json(query, max_results=5))
