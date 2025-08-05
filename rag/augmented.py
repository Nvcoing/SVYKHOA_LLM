from llm.call_gemini import call_gemini
from vectordb_rag import run_keybert_qa
def augmented(query,context, model_name="models/gemini-1.5-flash-latest"):
    prompt = f"""
Hãy trả lời câu hỏi sau: "{query}"

- Nếu thông tin truy xuất bên dưới có liên quan, hãy ưu tiên sử dụng để trả lời.
- Nếu thông tin không đủ hoặc không liên quan, hãy sử dụng tri thức sẵn có của bạn để trả lời đầy đủ và chính xác nhất có thể.
- Trả lời trực tiếp, đúng trọng tâm và dễ hiểu. Không cần nhắc lại phần truy vấn hay thông tin truy xuất.

**Thông tin truy xuất:**  
{context}
"""


    summary = call_gemini(prompt, model_name=model_name)
    return summary

# if __name__ == "__main__":
#     query = "Bệnh bạch cầu là gì? Triệu chứng và cách điều trị?"
#     summary = augmented(query,run_keybert_qa(query))
#     print("📝 Tóm tắt từ Gemini:\n", summary)
