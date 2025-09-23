import chromadb
from db.load_data import load_datasets
from embedding.load_embedding import EmbeddingModel

# Khởi tạo DB
client = chromadb.PersistentClient(path="./chroma_db")

# Tải dữ liệu
datasets = load_datasets()

# Load embedding model
embedder = EmbeddingModel()

def insert_dataframe(df, collection_name, text_fields, meta_fields, batch_size=5000):
    collection = client.get_or_create_collection(name=collection_name)

    total = len(df)
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        docs, metadatas, ids, embeddings = [], [], [], []

        for idx, row in df[start:end].iterrows():
            content = " ".join(
                str(row[field]) for field in text_fields
                if field in row and str(row[field]) != "nan"
            )
            docs.append(content)

            meta = {
                field: str(row[field])
                for field in meta_fields
                if field in row and str(row[field]) != "nan"
            }
            metadatas.append(meta)

            ids.append(f"{collection_name}_{idx}")

            vec = embedder.encode(content)
            if hasattr(vec, "tolist"):
                vec = vec.tolist()
            if isinstance(vec, list) and len(vec) > 0 and isinstance(vec[0], (list, tuple)):
                vec = vec[0]

            embeddings.append(vec)

        collection.add(
            documents=docs,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Inserted batch {start}-{end} into {collection_name}")

