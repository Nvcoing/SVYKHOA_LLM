# rag/search_chromdb.py
import chromadb
from config.config import EMBEDDER

# Kết nối tới ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")


def search_db(prompt: str, label: str = "medical talk", n_results: int = 3):
    """
    Nhận câu hỏi (prompt) và truy vấn vectorDB theo label (collection name).
    Trả ra list intruction + list answer (diagnosis thì có thêm symptom).
    """
    if label == "small talk":
        collection_name = "small_talk"
    if label == "medical talk":
        collection_name = "medical_talk"
    # Lấy collection tương ứng với label
    collection = client.get_or_create_collection(name=collection_name)

    # Sinh embedding cho câu hỏi
    query_emb = EMBEDDER.embed([prompt])

    # Truy vấn collection
    results = collection.query(
        query_embeddings=query_emb,
        n_results=n_results
    )

    # Tách kết quả
    intruction_list, answer_list, symptom_list = [], [], []

    for i, meta in enumerate(results["metadatas"][0]):
        if label == "diagnosis":
            intruction_list.append(meta.get("intruction", ""))
            answer_list.append(meta.get("diagnosis", ""))  # map diagnosis thành answer
            symptom_list.append(meta.get("symptom", ""))
        else:
            intruction_list.append(meta.get("intruction", ""))
            answer_list.append(meta.get("answer", ""))

    # Nếu diagnosis thì trả thêm symptom_list
    if label == "diagnosis":
        return intruction_list, answer_list, symptom_list
    else:
        return intruction_list, answer_list
