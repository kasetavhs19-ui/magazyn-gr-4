import streamlit as st

# Inicjalizacja listy produktów (będzie przechowywać nazwy produktów)
product_list = []

# Funkcja do dodawania produktu
def add_product(product_name):
    if product_name:
        product_list.append(product_name)
        st.success(f"Produkt '{product_name}' został dodany.")
    else:
        st.warning("Proszę podać nazwę produktu.")

# Funkcja do usuwania produktu
def remove_product(product_name):
    if product_name in product_list:
        product_list.remove(product_name)
        st.success(f"Produkt '{product_name}' został usunięty.")
    else:
        st.warning(f"Produkt '{product_name}' nie znajduje się na liście.")

# Nagłówek
st.title('Prosta aplikacja magazynowa')

# Pole do dodawania produktu
add_product_name = st.text_input('Wpisz nazwę produktu do dodania:')
if st.button('Dodaj produkt'):
    add_product(add_product_name)

# Pole do usuwania produktu
remove_product_name = st.text_input('Wpisz nazwę produktu do usunięcia:')
if st.button('Usuń produkt'):
    remove_product(remove_product_name)

# Wyświetlenie aktualnej listy produktów
st.subheader('Aktualna lista produktów w magazynie:')
st.write(product_list)
