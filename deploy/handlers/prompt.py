import json
from rag.augment import augment_prompt as aug
def build_prompt(prompt: str, labels: str = "",auguments_local=None, auguments_online=None,augment_answer=None):

    if labels == "diagnosis":
        Intruction = auguments_local["Intruction"]
        icd = aug(prompt, "icd10", n_results=1)
        id = icd["MÃ BỆNH"]
        name = icd["TÊN BỆNH"]
        dec = icd["mô tả"]
        prompts = (
                # f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}\nHãy trình bày câu hỏi theo dạng dưới đây nhưng không được lấy theo nội dung:\n**Chuẩn đoán:**{Diagnosis}\n**Triệu chứng:**{Symptom}\n<label>{labels.strip()}</label>\n"
                f"<|begin_of_text|>\n{Intruction}\nMã ICD-10:{id}\n Bệnh: {name}\n Triệu chứng:{dec}\n Hãy trả lời câu hỏi **{prompt.strip()}** dựa vào nội dung sau:\n{augment_answer}\nLưu ý: Bạn không được trả lời theo nội dung trên mà phải dựa vào kiến thức y khoa của bạn để trả lời đúng nội dung câu hỏi.\n<label>{labels.strip()}</label>\n",
        )
    elif labels == "small talk":
        Intruction = auguments_local["Intruction"]
        Answer = auguments_local["Answer"]
        prompts = (
                f"<|begin_of_text|>\n{Intruction}\nHãy trả lời lời như sau:{Answer}\n<label>{labels.strip()}</label>\n",
        )
    else:
        Intruction = auguments_local["Intruction"]
        prompts = (
                # f"<|begin_of_text|>\n{Intruction}\nCâu hỏi cần trả lời:{prompt.strip()}\nHãy trình bày câu hỏi dựa vào nội dung sau:\n**Đoạn trích ngắn**:{snippet}\n**Nội dung chính**:{highlight}\nHãy trình bày câu hỏi theo dạng dưới đây nhưng không được lấy theo nội dung:\n{Answer}\n<label>{labels.strip()}</label>\n"
                                f"<|begin_of_text|>\n{Intruction}\nHãy trả lời câu hỏi **{prompt.strip()}** dựa vào nội dung sau:\n{augment_answer}\nLưu ý: Bạn không được trả lời theo nội dung trên mà phải dựa vào kiến thức y khoa của bạn để trả lời đúng nội dung câu hỏi.\n<label>{labels.strip()}</label>\n",
        )
    print("Generated Prompt:", prompts)
    return prompts

def prompt_summary(prompt: str, labels: str = "medical talk",auguments_local=None, auguments_online=None):
    if isinstance(auguments_online, str):
        auguments_online = json.loads(auguments_online)  # parse nếu bị string
    tavily_snippets = " ".join([r["snippet"] for r in auguments_online if r["engine"] == "tavily"])
    tavily_highlight = " ".join([r["highlight"] for r in auguments_online if r["engine"] == "tavily"])
    google_snippets = " ".join([r["snippet"] for r in auguments_online if r["engine"] == "google"])
    google_highlight = " ".join([r["highlight"] for r in auguments_online if r["engine"] == "google"])
    if labels == "diagnosis":
        icd = aug(prompt, "icd10", n_results=1)
        id = icd["MÃ BỆNH"]
        name = icd["TÊN BỆNH"]
        dec = icd["mô tả"]
        Diagnosis = auguments_local["Diagnosis"]
        Symptom = auguments_local["Symptom"]
        prompts = (
            f"<|begin_of_text|>\nHãy là chatbot y khoa và tóm tắt nội dung sau để trả lời câu hỏi **{prompt.strip()}** biết có Mã ICD-10:{id}\n Bệnh: {name}\n Triệu chứng:{dec}\n. Dựa vào nội dung sau để trả lời câu hỏi:\n* **Nội dung chính 1**:\n{tavily_highlight}\n* **Nội dung chính 2**:\n{google_highlight}\n<label>{labels}</label>\n"
        )
    elif labels == "medical talk":
        Answer = auguments_local["Answer"]
        prompts = (
            f"<|begin_of_text|>\nHãy là chatbot y khoa và tóm tắt nội dung sau để trả lời câu hỏi **{prompt.strip()}** dựa vào nội dung sau:\n* **Nội dung chính 1**:\n{tavily_highlight}\n* **Nội dung chính 2**:\n{google_highlight}\n<label>{labels}</label>\n"
        )
    elif labels == "guide":
        Answer = auguments_local["Answer"]
        prompts = (
            f"<|begin_of_text|>\nHãy là chatbot y khoa và tóm tắt nội dung sau để trả lời câu hỏi **{prompt.strip()}** dựa vào nội dung sau:\n* **Nội dung chính 1**:\n{tavily_highlight}\n* **Nội dung chính 2**:\n{google_highlight}\n<label>{labels}</label>\n"
        )
    elif labels == "small talk":
        Answer = auguments_local["Answer"]
        prompts = (
            f"<|begin_of_text|>\nHãy là chatbot y khoa và tóm tắt nội dung sau để trả lời lời như sau:{Answer}\n<label>{labels}</label>\n",
        )

    return prompts