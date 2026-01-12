import streamlit as st
from supabase import create_client

# --- Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("Prosta aplikacja magazynowa (Supabase)")

# --- Dodawanie produktu ---
st.subheader("Dodaj produkt")

product_name = st.text_input("Nazwa produktu")
product_quantity = st.number_input(
    "Ilość",
    min_value=1,
    step=1
)

if st.button("Dodaj produkt"):
    if product_name:
        existing = supabase.table("products") \
            .select("*") \
            .eq("name", product_name) \
            .execute()

        if existing.data:
            supabase.table("products") \
                .update({
                    "quantity": existing.data[0]["quantity"] + product_quantity
                }) \
                .eq("name", product_name) \
                .execute()
        else:
            supabase.table("products") \
                .insert({
                    "name": product_name,
                    "quantity": product_quantity
                }) \
                .execute()

        st.success(f"Dodano produkt: {product_name}")
        st.rerun()
    else:
        st.warning("Podaj nazwę produktu.")

# --- Usuwanie produktu ---
st.subheader("Usuń produkt")

product_to_remove = st.text_input("Nazwa produktu do usunięcia")

if st.button("Usuń produkt"):
    supabase.table("products") \
        .delete() \
        .eq("name", product_to_remove) \
        .execute()

    st.success(f"Usunięto produkt: {product_to_remove}")
    st.rerun()

# --- Wyświetlanie magazynu ---
st.subheader("Stan magazynu")

data = supabase.table("products").select("*").execute()

if data.data:
    for item in data.data:
        st.write(f"- *{item['name']}*: {item['quantity']} szt.")
else:
    st.info("Magazyn jest pusty.")
