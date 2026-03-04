from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from qdrant_client import QdrantClient
from typing import List

# 🔹 TF-IDF vektörizer dosyasını yükle
with open("backend/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# 🔹 Qdrant ayarları
client = QdrantClient(host="localhost", port=6333)
collection_name = "urun_tfidf_vektorleri"

# 🔹 FastAPI başlat
app = FastAPI()

# 🔹 CORS (Frontend bağlantısı için gerekli)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Dönüş modeli
class Urun(BaseModel):
    isim: str
    aciklama: str
    price: float
    rating: float
    skoru: float

# 🔹 Arama endpoint'i
@app.get("/oner", response_model=List[Urun])
def search(
    query: str = Query(..., min_length=1),
    min_rating: float = 0.0,
    min_price: float = 0.0,
    max_price: float = 10000.0,
    limit: int = 10
):
    # Sorguyu TF-IDF vektörüne dönüştür
    vec = vectorizer.transform([query]).toarray()[0]

    # Qdrant üzerinden en yakın vektörleri bul
    sonuc = client.search(
        collection_name=collection_name,
        query_vector=vec.tolist(),
        limit=limit
    )

    # Sonuçları filtrele
    urunler = []
    for eslesme in sonuc:
        payload = eslesme.payload
        skor = eslesme.score

        try:
            fiyat = float(payload.get("price", 0.0))
            puan = float(payload.get("rating", 0.0))
        except ValueError:
            continue

        if fiyat < min_price or fiyat > max_price:
            continue
        if puan < min_rating:
            continue

        urunler.append(Urun(
            isim=payload.get("isim", ""),
            aciklama=payload.get("aciklama", ""),
            price=fiyat,
            rating=puan,
            skoru=skor
        ))

    return urunler
