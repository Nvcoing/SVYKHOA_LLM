import torch
from sentence_transformers import util
from embedding_model import EmbeddingModel

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
        prompt_emb = self.embedding_model.encode(prompt)
        sims = util.cos_sim(prompt_emb, self.label_embeddings)[0]
        best_idx = torch.argmax(sims).item()
        return self.label_keys[best_idx], sims[best_idx].item()
