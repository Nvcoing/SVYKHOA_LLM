import chromadb
from embedding.load_embedding import EmbeddingModel

# Khởi tạo client và model
client = chromadb.PersistentClient(path="./chroma_db")
embedder = EmbeddingModel()

def search_query(query, collection_name:str="medical_talk", top_k:int=3):
    collection = client.get_collection(name=collection_name)

    query_emb = embedder.encode(query)

    results = collection.query(
        query_embeddings=query_emb,
        n_results=top_k
    )

    # Lấy kết quả
    output = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        if collection_name == "diagnosis":
            output.append({
                "question": doc,
                "symptom": meta.get("symptom", ""),
                "diagnosis": meta.get("diagnosis", "")
            })
        else:
            output.append({
                "question": doc,
                "answer": meta.get("answer", "")
            })
    return output
