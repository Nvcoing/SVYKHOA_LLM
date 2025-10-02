from sentence_transformers import SentenceTransformer
import torch

class EmbeddingModel:
    def __init__(self, model_name="Qwen/Qwen3-Embedding-0.6B"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)
