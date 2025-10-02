import torch
from sentence_transformers import util
from embedding.load_embedding import EmbeddingModel

class PromptClassifier:
    def __init__(self, labels_descriptions, embedding_model=None):
        """
        labels_descriptions: dict, ví dụ {"Positive": "text description", ...}
        embedding_model: instance của EmbeddingModel
        """
        self.labels = labels_descriptions
        self.label_texts = list(labels_descriptions.values())
        self.label_keys = list(labels_descriptions.keys())
        self.embedding_model = embedding_model or EmbeddingModel()
        self.label_embeddings = self.embedding_model.encode(self.label_texts)

    def classify(self, prompt):
        # Đếm số từ trong prompt
        word_count = len(prompt.strip().split())

        # Nếu số từ < 5 thì loại diagnosis
        if word_count < 5 and "diagnosis" in self.labels:
            active_keys = [k for k in self.label_keys if k != "diagnosis"]
        else:
            active_keys = self.label_keys

        # Encode lại chỉ các nhãn đang active
        active_texts = [self.labels[k] for k in active_keys]
        active_embeddings = self.embedding_model.encode(active_texts)

        # Encode prompt
        prompt_emb = self.embedding_model.encode(prompt)

        # Tính cosine similarity
        sims = util.cos_sim(prompt_emb, active_embeddings)[0]
        best_idx = torch.argmax(sims).item()

        return active_keys[best_idx], sims[best_idx].item()
