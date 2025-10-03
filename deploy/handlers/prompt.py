import json

def build_prompt(prompt: str, labels: str = "",auguments_local=None, auguments_online=None):
    if isinstance(auguments_online, str):
        auguments_online = json.loads(auguments_online)  # parse nếu bị string
    tavily_snippets = [r["snippet"] for r in auguments_online if r["engine"] == "tavily"]
        # best_result = auguments_online["results"][0]
        # snippet = best_result["snippet"]
        # content = best_result["content"]
        # highlight = best_result["highlight"]
    print("Tavily snippets:", tavily_snippets)
    if labels == "diagnosis":
        Intruction = auguments_local["Intruction"]
        Diagnosis = auguments_local["Diagnosis"]
        Symptom = auguments_local["Symptom"]
        prompts = (
                # f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}\nHãy trình bày câu hỏi theo dạng dưới đây nhưng không được lấy theo nội dung:\n**Chuẩn đoán:**{Diagnosis}\n**Triệu chứng:**{Symptom}\n<label>{labels.strip()}</label>\n"
                f"<|begin_of_text|>\n{Intruction}\nHãy trả lời câu hỏi **{prompt.strip()}** dựa vào nội dung sau:\n* **Chuẩn đoán**:\n{Diagnosis}\n* **Triệu chứng**:\n{Symptom} *\nLưu ý: Bạn không được trả lời theo nội dung trên mà phải dựa vào kiến thức y khoa của bạn để trả lời đúng nội dung câu hỏi.\n<label>{labels.strip()}</label>\n",
        )
    else:
        Intruction = auguments_local["Intruction"]
        Answer = auguments_local["Answer"]
        prompts = (
                # f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}\nHãy trình bày câu hỏi theo dạng dưới đây nhưng không được lấy theo nội dung:\n{Answer}\n<label>{labels.strip()}</label>\n"
                                f"<|begin_of_text|>\n{Intruction}\nHãy trả lời câu hỏi **{prompt.strip()}** dựa vào nội dung sau:\n* **Câu trả lời**:\n{Answer}\nLưu ý: Bạn không được trả lời theo nội dung trên mà phải dựa vào kiến thức y khoa của bạn để trả lời đúng nội dung câu hỏi.\n<label>{labels.strip()}</label>\n",
        )
    print("Generated Prompt:", prompts)
    return prompts