import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# CSV dosyasını oku (aynı klasörde olduğunu varsayıyoruz)
df = pd.read_csv("urunler_yeni.csv")

# TF-IDF vektörizer oluştur
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["description"])

# Vektörizeri kaydet
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# TF-IDF matrisini kaydet
with open("tfidf_matrix.pkl", "wb") as f:
    pickle.dump(X, f)

# Ürün listesini dict formatında kaydet
with open("urunler.pkl", "wb") as f:
    pickle.dump(df.to_dict(orient="records"), f)

print("✅ Veriler başarıyla işlendi ve kaydedildi.")
