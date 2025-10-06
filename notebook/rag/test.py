import chromadb
from load_embedding import EmbeddingModel

# Kết nối tới DB
client = chromadb.PersistentClient(path="../chroma_db")
embedder = EmbeddingModel()

def test_search(prompt, collection_name="guide", n_results=3):
    col = client.get_or_create_collection(name=collection_name)

    print(f"Collection: {collection_name}, count={col.count()}")

    # Sinh embedding
    vec = embedder.encode([prompt])
    if hasattr(vec, "tolist"):
        vec = vec.tolist()
    if isinstance(vec, list) and len(vec) > 0 and isinstance(vec[0], (list, tuple)):
        vec = vec[0]

    # Query
    results = col.query(
        query_embeddings=[vec],
        n_results=n_results
    )

    print("==== Raw results ====")
    print("IDs:", results.get("ids", []))
    print("Docs:", results.get("documents", []))
    print("Metas:", results.get("metadatas", []))
    print("Distances:", results.get("distances", []))

if __name__ == "__main__":
    # Ví dụ: test với collection "guide"
    test_search("Bệnh tiểu đường là gì?", collection_name="guide", n_results=2)

    # Bạn có thể test với diagnosis/medical_talk/small_talk
    # test_search("Làm thế nào để phòng ngừa bệnh tim?", collection_name="medical_talk")
    # test_search("Xin chào", collection_name="small_talk")
    # test_search("Triệu chứng của viêm phổi", collection_name="diagnosis")
