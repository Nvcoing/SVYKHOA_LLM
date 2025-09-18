from sentence_transformers import SentenceTransformer, util
import torch

class PromptClassifier:
    def __init__(self, labels_descriptions, model_name="Qwen/Qwen3-Embedding-0.6B"):
        """
        labels_descriptions: dict, ví dụ {"Positive": "text description", ...}
        model_name: tên model GEMMA hoặc tương tự
        """
        self.labels = labels_descriptions
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)
        # Tạo embedding cho tất cả nhãn
        self.label_texts = list(labels_descriptions.values())
        self.label_keys = list(labels_descriptions.keys())
        self.label_embeddings = self.model.encode(self.label_texts, convert_to_tensor=True)

    def classify(self, prompt):
        """
        Trả về nhãn và điểm similarity cao nhất
        """
        prompt_emb = self.model.encode(prompt, convert_to_tensor=True)
        sims = util.cos_sim(prompt_emb, self.label_embeddings)[0]
        best_idx = torch.argmax(sims).item()
        best_label = self.label_keys[best_idx]
        best_score = sims[best_idx].item()
        return best_label, best_score
# # ----------------- Ví dụ sử dụng -----------------
# if __name__ == "__main__":
#     labels = {
#         "diagnosis": "Xác định mã bệnh ICD-10, chuẩn đoán, triệu chứng",
#         "guide": "Hướng dẫn, định hướng cho các bác sỹ trẻ học hỏi, tích lũy kinh nghiệm",
#         "small talk": "Nói chuyện vui vẻ với các bác sỹ trẻ về chào hỏi, yêu cầu cơ bản, tác vụ chung, có thể không liên quan đến y khoa",
#         "medical talk": "Hỏi đáp về các vấn đề y khoa"
#     }

#     classifier = PromptClassifier(labels)
#     prompt = "Xác định mã bệnh ICD 10 sau: Tôi bị đau bụng và ợ chua"
#     label, score = classifier.classify(prompt)
#     print(f"Predicted label: {label}, similarity: {score:.4f}")

