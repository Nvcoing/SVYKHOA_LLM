# main.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from agent_server.load_model import load_model_tokenizer
from agent_server.generate import generate_stream
from embedding.classifier import PromptClassifier 
from embedding.load_embedding import EmbeddingModel
from config.constants import MODEL, EMBEDDING


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi domain gọi (bạn có thể thay bằng domain cụ thể)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("config/classifier.json", "r", encoding="utf-8") as f:
    labels = json.load(f)

model, tokenizer, device = load_model_tokenizer(MODEL)
embedder = EmbeddingModel(EMBEDDING)
classifier = PromptClassifier(labels, embedder)
class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 1024

@app.post("/model/generate/")
async def generate_text(req: PromptRequest):
    label, score = classifier.classify(req.prompt)
    print(f"Predicted label: {label}, similarity: {score:.4f}")
    return StreamingResponse(generate_stream(model, tokenizer, device, req.prompt,label), media_type="text/plain")