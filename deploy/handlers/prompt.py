import json

def build_prompt(prompt: str, labels: str = "",auguments_local=None, auguments_online=None):
    if isinstance(auguments_online, str):
        auguments_online = json.loads(auguments_online)  # parse nếu bị string

        best_result = auguments_online["results"][0]
        snippet = best_result["snippet"]
        content = best_result["content"]
        highlight = best_result["highlight"]
    #     print("\nTitle tốt nhất:", best["results"][0]["title"])
#     print("Snippet:", best["results"][0]["snippet"])
#     print("Content:", best["results"][0]["content"])
#     print("Highlight:", best["results"][0]["highlight"])
    if labels == "diagnosis":
        Intruction = auguments_local["Intruction"]
        Diagnosis = auguments_local["Diagnosis"]
        Symptom = auguments_local["Symptom"]
        prompts = (
                # f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}\nHãy trình bày câu hỏi theo dạng dưới đây nhưng không được lấy theo nội dung:\n**Chuẩn đoán:**{Diagnosis}\n**Triệu chứng:**{Symptom}\n<label>{labels.strip()}</label>\n"
                f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}\n<label>{labels.strip()}</label>\n"
        )
    else:
        Intruction = auguments_local["Intruction"]
        Answer = auguments_local["Answer"]
        prompts = (
                # f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}\nHãy trình bày câu hỏi theo dạng dưới đây nhưng không được lấy theo nội dung:\n{Answer}\n<label>{labels.strip()}</label>\n"
                                f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}<label>{labels.strip()}</label>\n"
        )
    print("Generated Prompt:", prompts)
    return prompts