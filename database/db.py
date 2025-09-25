import chromadb

client = chromadb.PersistentClient(path="../deploy/chroma_db")

# Xem các collection đang có
print(client.list_collections())

# Lấy collection và xem số lượng document
col = client.get_or_create_collection("medical_talk")
print("Diagnosis count:", col.count())

# Thử lấy vài document mẫu
res = col.get(limit=3)
print(res)
