from tavily import TavilyClient
import json

class TavilySearch:
    def __init__(self, api_key=None):

        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, n: int = 5, fetch_content: bool = True):
        """
        Tìm kiếm với Tavily.
        - query: câu truy vấn
        - n: số kết quả trả về
        - fetch_content: True nếu muốn có cả content (snippet hoặc raw_content nếu có)
        """
        response = self.client.search(
            query=query,
            max_results=n,
            include_raw_content=fetch_content
        )
        return response

    def pretty_print(self, data):
        print(json.dumps(data, indent=2, ensure_ascii=False))


# if __name__ == "__main__":
#     tavily = TavilySearch()
#     results = tavily.search("Tôi bị ợ chua và đau bụng", n=5, fetch_content=True)
#     tavily.pretty_print(results)
