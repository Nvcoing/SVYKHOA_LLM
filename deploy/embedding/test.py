from prompt_classifier import PromptClassifier
from embedding_model import EmbeddingModel
# ----------------- Ví dụ sử dụng -----------------
labels = {
    "diagnosis": "Xác định mã bệnh ICD-10, chuẩn đoán, triệu chứng",
    "guide": "Hướng dẫn, định hướng cho các bác sỹ trẻ học hỏi, tích lũy kinh nghiệm",
    "small talk": "Nói chuyện vui vẻ với các bác sỹ trẻ về chào hỏi, yêu cầu cơ bản, tác vụ chung, có thể không liên quan đến y khoa",
    "medical talk": "Hỏi đáp về các vấn đề y khoa"
}
embedder = EmbeddingModel("Qwen/Qwen3-Embedding-0.6B")
classifier = PromptClassifier(labels, embedder)
label, score = classifier.classify("I love this product, it’s amazing!")
print(f"Predicted label: {label}, similarity: {score:.4f}")