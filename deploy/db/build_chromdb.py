import chromadb
from load_data import load_datasets
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
        content = " ".join(str(row[field]) for field in text_fields if field in row and str(row[field]) != "nan")
        docs.append(content)

        # Metadata
        meta = {field: str(row[field]) for field in meta_fields if field in row and str(row[field]) != "nan"}
        metadatas.append(meta)

        ids.append(f"{collection_name}_{idx}")
        embeddings.append(embedder.encode(content)[0])

    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Inserted {len(docs)} records into {collection_name}")