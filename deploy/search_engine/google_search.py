import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build


class GoogleSearch:
    def __init__(self, api_key=None, cse_id=None):

        self.api_key = api_key
        self.cse_id = cse_id

    def _get_page_content(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = "\n".join([p.get_text() for p in paragraphs])
            return content.strip()
        except:
            return ""

    def search(self, query, num_results=10):
        if not self.api_key or not self.cse_id:
            print("Thiếu API_KEY hoặc CSE_ID")
            return []

        try:
            service = build("customsearch", "v1", developerKey=self.api_key)
            res = service.cse().list(q=query, cx=self.cse_id, num=num_results).execute()

            results = []
            if 'items' in res:
                for item in res['items']:
                    link = item.get('link')
                    # Lấy thumbnail nếu có
                    thumbnail = None
                    if "pagemap" in item and "cse_image" in item["pagemap"]:
                        thumbnail = item["pagemap"]["cse_image"][0].get("src")

                    content = self._get_page_content(link)

                    results.append({
                        'title': item.get('title'),
                        'link': link,
                        'displayLink': item.get('displayLink'),
                        'snippet': item.get('snippet'),
                        'mime': item.get('mime'),
                        'thumbnail': thumbnail,
                        'content': content
                    })
            return results
        except:
            return []

    def get_result(self, results, index, field):
        try:
            return results[index][field]
        except:
            return None


# # --- Ví dụ sử dụng ---
# if __name__ == "__main__":
#     gs = GoogleSearch()
#     query = "DFT technology JSC là công ty gì"
#     search_results = gs.search(query)

#     # Xuất JSON đầy đủ
#     print(json.dumps(search_results, ensure_ascii=False, indent=2))

#     # Lấy theo vị trí cụ thể
#     print("\n🏷️ Tiêu đề đầu tiên:", gs.get_result(search_results, 0, "title"))
#     print("🔗 Link kết quả thứ 2:", gs.get_result(search_results, 1, "link"))
#     print("🖼️ Thumbnail kết quả thứ 1:", gs.get_result(search_results, 0, "thumbnail"))
#     print("📄 Nội dung tóm tắt kết quả thứ 3:", gs.get_result(search_results, 2, "content")[:300] if gs.get_result(search_results, 2, "content") else None)
