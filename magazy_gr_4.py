import streamlit as st
from supabase import create_client

# Inicjalizacja połączenia
@st.cache_resource
def init_connection():
    # Pobieramy wartości używając NAZW kluczy z pliku secrets, a nie samych adresów
    url = st.secrets["https://beumgnxpoxgcvvqujcna.supabase.co"]
    key = st.secrets["beumgnxpoxgcvvqujcna"]
    return create_client(url, key)
supabase = init_connection()

st.title("Magazyn z Kategoriami")

# --- POBIERANIE KATEGORII DO SELECTBOXA ---
def get_categories():
    response = supabase.table("kategorie").select("id, nazwa").execute()
    return {item['nazwa']: item['id'] for item in response.data}

categories_dict = get_categories()

# --- DODAWANIE PRODUKTU ---
with st.expander("Dodaj nowy produkt"):
    with st.form("add_product_form"):
        nazwa = st.text_input("Nazwa produktu")
        cena = st.number_input("Cena", min_value=0.0, format="%.2f")
        liczba = st.number_input("Ilość (liczba)", min_value=0, step=1)
        
        # Wybór kategorii z listy pobranej z bazy
        kat_nazwa = st.selectbox("Kategoria", options=list(categories_dict.keys()))
        
        submitted = st.form_submit_button("Dodaj do magazynu")
        
        if submitted:
            new_product = {
                "nazwa": nazwa,
                "cena": cena,
                "liczba": liczba,
                "kategoria_id": categories_dict[kat_nazwa]
            }
            supabase.table("produkty").insert(new_product).execute()
            st.success(f"Dodano: {nazwa}")
            st.rerun()

# --- WYŚWIETLANIE STANU ---
st.subheader("Aktualny stan magazynu")

# Pobieramy produkty razem z nazwami kategorii (join)
response = supabase.table("produkty").select("nazwa, cena, liczba, kategorie(nazwa)").execute()
data = response.data

if data:
    for p in data:
        # kategorie(nazwa) zwraca słownik, bo to relacja
        kat = p.get('kategorie', {}).get('nazwa', 'Brak')
        st.write(f"📦 **{p['nazwa']}** | Cena: {p['cena']} zł | Sztuk: {p['liczba']} | Kat: {kat}")
else:
    st.info("Brak produktów w bazie.")
