import streamlit as st
from supabase import create_client

# ===== Supabase connection =====
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ===== Helper functions =====
def get_products():
    response = supabase.table("products").select("*").order("name").execute()
    return response.data


def add_product(name, quantity):
    existing = supabase.table("products") \
        .select("*") \
        .eq("name", name) \
        .execute()

    if existing.data:
        new_quantity = existing.data[0]["quantity"] + quantity
        supabase.table("products") \
            .update({"quantity": new_quantity}) \
            .eq("name", name) \
            .execute()
    else:
        supabase.table("products").insert({
            "name": name,
            "quantity": quantity
        }).execute()


def remove_product(name):
    supabase.table("products") \
        .delete() \
        .eq("name", name) \
        .execute()


# ===== UI =====
st.title("📦 Prosta aplikacja magazynowa (Supabase)")

# --- Dodawanie produktu ---
st.subheader("➕ Dodaj produkt")

product_name = st.text_input("Nazwa produktu")
product_quantity = st.number_input(
    "Ilość",
    min_value=1,
    step=1
)

if st.button("Dodaj produkt"):
    if product_name:
        add_product(product_name, product_quantity)
        st.success(f"Dodano produkt: {product_name}")
        st.rerun()
    else:
        st.warning("Podaj nazwę produktu.")

# --- Usuwanie produktu ---
st.subheader("🗑️ Usuń produkt")

product_to_remove = st.text_input("Nazwa produktu do usunięcia")

if st.button("Usuń produkt"):
    if product_to_remove:
        remove_product(product_to_remove)
        st.success(f"Usunięto produkt: {product_to_remove}")
        st.rerun()
    else:
        st.warning("Podaj nazwę produktu.")

# --- Wyświetlanie magazynu ---
st.subheader("📊 Stan magazynu")

products = get_products()

if products:
    for p in products:
        st.write(f"- **{p['name']}**: {p['quantity']} szt.")
else:
    st.info("Magazyn jest pusty.")
