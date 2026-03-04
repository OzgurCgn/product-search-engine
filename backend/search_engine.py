from qdrant_client import QdrantClient
import joblib



# 🔹 TF-IDF vektörizer dosyasını yükle
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# 🔹 Kullanıcıdan ürün açıklaması al
sorgu = input("🔍 Aramak istediğiniz ürün açıklamasını yazın: ")
sorgu_vektoru = vectorizer.transform([sorgu]).toarray()[0]

# 🔹 Qdrant istemcisi
client = QdrantClient(host="localhost", port=6333)
koleksiyon_adi = "urun_tfidf_vektorleri"

# 🔹 Qdrant'ta arama yap
response = client.search(
    collection_name=koleksiyon_adi,
    query_vector=sorgu_vektoru.tolist(),
    limit=3
)


# 🔹 Sonuçları yazdır
print("🔍 En benzer sonuçlar:")
for sonuc in response:
    skor: float = sonuc.score
    isim: str = sonuc.payload.get("isim", "Bilinmiyor")
    aciklama: str = sonuc.payload.get("aciklama", "Yok")
    print(f"🔹 Skor: {skor:.4f} | Ürün: {isim} | Açıklama: {aciklama}")
