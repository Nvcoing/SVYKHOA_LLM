from embedding.load_embedding import EmbeddingModel
from config.constants import EMBEDDING, MODEL, ENV
from agent_server.load_model import load_model_tokenizer
from dotenv import load_dotenv

import os
import chromadb

load_dotenv(ENV)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
FIRECRAWLER_API_KEY = os.getenv("FIRECRAWLER_API_KEY")
CHROMADB = chromadb.PersistentClient(path="./chroma_db")
LLM, TOKENIZER, DEVICE = load_model_tokenizer(MODEL)
EMBEDDER = EmbeddingModel(EMBEDDING)