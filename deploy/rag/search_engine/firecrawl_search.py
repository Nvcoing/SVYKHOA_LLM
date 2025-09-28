from firecrawl import Firecrawl
import json
import os
from dotenv import load_dotenv
import math
from urllib.parse import urlparse

# Load biến môi trường từ file .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

class FirecrawlWrapper:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        self.client = Firecrawl(api_key=self.api_key)

    def serialize_obj(self, obj):
        """Chuyển toàn bộ object Firecrawl sang dict, bao gồm các trường nested"""
        if hasattr(obj, "__dict__"):
            return {k: self.serialize_obj(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, list):
            return [self.serialize_obj(v) for v in obj]
        else:
            return obj

    def add_custom_fields(self, results):
        """Thêm các trường custom như domain, read_time"""
        if 'web' in results:
            for item in results['web']:
                url = item.get('url')
                content = item.get('content', "")
                # Thêm source_domain
                item['source_domain'] = urlparse(url).netloc if url else None
                # Thêm read_time ước lượng (1 phút ~ 200 từ)
                words = len(content.split())
                item['read_time_minutes'] = math.ceil(words / 200)
        return results

    def search(self, query, limit=5):
        raw_results = self.client.search(query=query, limit=limit)
        results = self.serialize_obj(raw_results)
        results = self.add_custom_fields(results)
        return results

    def pretty_print(self, data):
        print(json.dumps(data, indent=2, ensure_ascii=False))


# # Ví dụ sử dụng
# if __name__ == "__main__":
#     fc = FirecrawlWrapper(api_key="")
#     results = fc.search("Sâu răng là gì?", limit=3)
#     fc.pretty_print(results)
