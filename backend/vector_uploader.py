import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# 🔹 Ayarlar
dosya_yolu = "urunler_yeni.csv"
collection_name = "urun_tfidf_vektorleri"

# 🔹 Veriyi oku
df = pd.read_csv(dosya_yolu)

# 🔹 TF-IDF vektörleri
aciklamalar = df["description"].astype(str).tolist()
isimler = df["title"].astype(str).tolist()

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(aciklamalar)
tfidf_vectors = X.toarray()
vector_dim = tfidf_vectors.shape[1]
print(f"📐 Vektör boyutu: {vector_dim}")

# 🔹 TF-IDF vektörizerini kaydet
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
print("💾 TF-IDF vektörizer kaydedildi.")

# 🔹 Qdrant Client
client = QdrantClient(host="localhost", port=6333)

# 🔹 Eski koleksiyon silinsin
client.delete_collection(collection_name=collection_name)
print(f"🗑️ Eski koleksiyon silindi: {collection_name}")

# 🔹 Yeni koleksiyon oluştur
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE)
)
print(f"✅ Yeni koleksiyon oluşturuldu: {collection_name}")

# 🔹 Veriyi Qdrant'a yükle
points = [
    PointStruct(
        id=i,
        vector=vec,
        payload={
            "isim": isimler[i],
            "aciklama": aciklamalar[i],
            "price": float(df.loc[i, "price"]),
            "rating": float(df.loc[i, "rating"])
        }
    )
    for i, vec in enumerate(tfidf_vectors)
]

client.upsert(collection_name=collection_name, points=points)
print("✅ Vektörler başarıyla Qdrant'a yüklendi.")
