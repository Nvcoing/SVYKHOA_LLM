import chromadb
from db.load_data import load_datasets
from embedding.load_embedding import EmbeddingModel

# Khởi tạo DB
client = chromadb.PersistentClient(path="./chroma_db")

# Tải dữ liệu
datasets = load_datasets()

# Load embedding model
embedder = EmbeddingModel()

def insert_dataframe(df, collection_name, text_fields, meta_fields):
    collection = client.get_or_create_collection(name=collection_name)

    docs, metadatas, ids, embeddings = [], [], [], []

    for idx, row in df.iterrows():
        # Tạo văn bản để embedding
        content = " ".join(
            str(row[field]) for field in text_fields
            if field in row and str(row[field]) != "nan"
        )
        docs.append(content)

        # Metadata
        meta = {
            field: str(row[field])
            for field in meta_fields
            if field in row and str(row[field]) != "nan"
        }
        metadatas.append(meta)

        ids.append(f"{collection_name}_{idx}")

        # Sinh embedding
        vec = embedder.encode(content)

        # Nếu là tensor hoặc numpy -> convert sang list
        if hasattr(vec, "tolist"):
            vec = vec.tolist()

        # Nếu encode ra 2D (vd [[...]]), thì lấy hàng đầu tiên
        if isinstance(vec, list) and len(vec) > 0 and isinstance(vec[0], (list, tuple)):
            vec = vec[0]

        embeddings.append(vec)

    # Insert vào collection
    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Inserted {len(docs)} records into {collection_name}")
