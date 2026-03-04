from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)

collection_name = "tfidf_product_vectors"

if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=100, distance=Distance.COSINE)
    )
    print(f"✅ Koleksiyon oluşturuldu: {collection_name}")
else:
    print(f"ℹ️ Koleksiyon zaten mevcut: {collection_name}")


status = client.get_collection(collection_name).status
print(f"📦 Koleksiyon durumu: {status}")
