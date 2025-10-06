from config.config import CHROMADB, EMBEDDER


def search_db(prompt: str, label: str = "medical talk", n_results: int = 3):
    """
    Truy vấn vectorDB theo label (collection name).
    """
    # Map nhãn → collection
    if label == "small talk":
        collection_name = "small_talk"
    elif label == "medical talk":
        collection_name = "medical_talk"
    elif label == "guide":
        collection_name = "guide"
    elif label == "diagnosis":
        collection_name = "diagnosis"
    else:
        raise ValueError(f"Unknown label: {label}")

    collection = CHROMADB.get_or_create_collection(name=collection_name)

    # Sinh embedding cho câu hỏi
    query_emb = EMBEDDER.encode(prompt)
    if hasattr(query_emb, "tolist"):
        query_emb = query_emb.tolist()
    if isinstance(query_emb[0], (list, tuple)):
        query_emb = query_emb[0]

    # Truy vấn
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=n_results
    )

    # Debug xem có kết quả ko
    print("Raw results:", results)

    intruction_list, answer_list, symptom_list = [], [], []
    for meta in results.get("metadatas", [[]])[0]:
        if label == "diagnosis":
            intruction_list.append(meta.get("intruction", ""))
            answer_list.append(meta.get("diagnosis", ""))
            symptom_list.append(meta.get("symptom", ""))
        else:
            intruction_list.append(meta.get("intruction", ""))
            answer_list.append(meta.get("answer", ""))

    if label == "diagnosis":
        return intruction_list, answer_list, symptom_list
    return intruction_list, answer_list
