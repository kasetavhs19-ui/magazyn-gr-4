import streamlit as st
setx API_KEY beumgnxpoxgcvvqujcna
st.title("Prosta aplikacja magazynowa")

# Inicjalizacja magazynu w session_state
if "products" not in st.session_state:
    st.session_state.products = {}

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
        if product_name in st.session_state.products:
            st.session_state.products[product_name] += product_quantity
        else:
            st.session_state.products[product_name] = product_quantity

        st.success(
            f"Dodano produkt: {product_name} (ilość: {product_quantity})"
        )
    else:
        st.warning("Podaj nazwę produktu.")

# --- Usuwanie produktu ---
st.subheader("Usuń produkt")

product_to_remove = st.text_input("Nazwa produktu do usunięcia")

if st.button("Usuń produkt"):
    if product_to_remove in st.session_state.products:
        del st.session_state.products[product_to_remove]
        st.success(f"Usunięto produkt: {product_to_remove}")
    else:
        st.warning("Taki produkt nie istnieje.")

# --- Wyświetlanie magazynu ---
st.subheader("Stan magazynu")

if st.session_state.products:
    for name, quantity in st.session_state.products.items():
        st.write(f"- **{name}**: {quantity} szt.")
else:
    st.info("Magazyn jest pusty.")

