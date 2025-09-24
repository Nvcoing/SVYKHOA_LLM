from embedding.load_embedding import EmbeddingModel
from config.constants import EMBEDDING, MODEL
from agent_server.load_model import load_model_tokenizer

LLM, TOKENIZER, DEVICE = load_model_tokenizer(MODEL)
EMBEDDER = EmbeddingModel(EMBEDDING)