import streamlit as st
import requests

st.set_page_config(page_title="Ürün Arama", layout="wide")

st.title("🔍 Akıllı Ürün Arama")

query = st.text_input("Ürün ara...", placeholder="örn. kulaklık, su şişesi, bluetooth hoparlör")

col1, col2, col3 = st.columns(3)
with col1:
    min_rating = st.slider("Minimum Puan", 0.0, 5.0, 0.0, 0.5)
with col2:
    min_price = st.number_input("Minimum Fiyat", min_value=0.0, value=0.0)
with col3:
    max_price = st.number_input("Maksimum Fiyat", min_value=0.0, value=10000.0)

if query:
    with st.spinner("Aranıyor..."):
        response = requests.get("http://localhost:8000/oner/",

            params={
                "query": query,
                "min_rating": min_rating,
                "min_price": min_price,
                "max_price": max_price,
                "limit": 10
            }
        )

        if response.status_code == 200:
            results = response.json()
            if results:
                for i, item in enumerate(results):
                    with st.container():
                        st.markdown(f"### {item['isim']}")
                        st.markdown(f"{item['aciklama']}")
                        st.markdown(f"💰 **{item['price']} TL**")
                        st.markdown(f"⭐ {item['rating']} puan")
                        st.markdown("---")
            else:
                st.warning("❌ Sonuç bulunamadı.")
        else:
            st.error("⚠️ Arama sırasında hata oluştu.")
