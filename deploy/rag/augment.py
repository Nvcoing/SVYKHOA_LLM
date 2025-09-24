from rag.search_chromdb import search_db as search

def augment_prompt(prompt: str, label: str = "medical talk", n_results: int = 1):
    """
    Nhận câu hỏi (prompt) và truy vấn vectorDB theo label (collection name).
    Trả ra dict chứa nội dung augment.
    """
    res = search(prompt, label=label, n_results=n_results)
    if label == "diagnosis":
        intruction_list, answer_list, symptom_list = res
        result = {
            "Intruction": intruction_list[0] if intruction_list else "",
            "Question": prompt,
            "Diagnosis": answer_list[0] if answer_list else "",
            "Symptom": symptom_list[0] if symptom_list else ""
        }
    else:
        intruction_list, answer_list = res
        result = {
            "Intruction": intruction_list[0] if intruction_list else "",
            "Question": prompt,
            "Answer": answer_list[0] if answer_list else ""
        }
    return result


# # Ví dụ sử dụng
# q1 = "Bệnh tiểu đường là gì?"
# aug_q1 = augment_prompt(q1, label="diagnosis")
# print(aug_q1["Diagnosis"])   # Lấy thẳng Diagnosis

# q2 = "Làm thế nào để phòng ngừa bệnh tim?"
# aug_q2 = augment_prompt(q2, label="guide")
# print(aug_q2["Answer"])      # Lấy thẳng Answer
