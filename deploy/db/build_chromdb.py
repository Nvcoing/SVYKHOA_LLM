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


# Diagnosis
insert_dataframe(
    datasets["diagnosis"],
    collection_name="diagnosis",
    text_fields=["intruction", "question", "symptom", "diagnosis"],
    meta_fields=['icd_10','icd_10/title','document/title','document/description','cme/title','cme/description']
)

# Guide
insert_dataframe(
    datasets["guide"],
    collection_name="guide",
    text_fields=["intruction", "question", "answer"],
    meta_fields=['document/title','document/tool','document/description','cme/title','cme/tool','cme/description']
)

# Medical Talk
insert_dataframe(
    datasets["medical_talk"],
    collection_name="medical_talk",
    text_fields=["intruction", "question", "answer"],
    meta_fields=[]
)

# Small Talk
insert_dataframe(
    datasets["small_talk"],
    collection_name="small_talk",
    text_fields=["intruction", "question", "answer"],
    meta_fields=[]
)
