import streamlit as st

# Ustawienie konfiguracji strony (opcjonalne, ale poprawia wygląd)
st.set_page_config(
    page_title="Prosty Magazyn",
    page_icon="📦",
    layout="centered"
)

# --- NAGŁÓWEK Z OBRAZKIEM ---
# Tworzymy dwie kolumny.
# Kolumna 1 (lewa) będzie szersza (proporcja 3) i zawierać tytuł.
# Kolumna 2 (prawa) będzie węższa (proporcja 1) i zawierać obrazek.
col1, col2 = st.columns([3, 1])

with col1:
    # Tytuł aplikacji w lewej kolumnie
    st.title("Prosty Magazyn 📦")
    st.write("Zarządzaj listą produktów w pamięci podręcznej.")

with col2:
    # Obrazek paczki w prawej kolumnie.
    # Używamy URL do darmowej ikony (flaticon).
    # Możesz zmienić width (szerokość), aby dopasować rozmiar.
    image_url = "https://cdn-icons-png.flaticon.com/512/679/679720.png"
    st.image(image_url, width=120, caption="Stan: W toku")


st.divider() # Linia oddzielająca nagłówek

# --- LOGIKA APLIKACJI (bez zmian) ---

# 1. Inicjalizacja stanu (Session State)
if 'produkty' not in st.session_state:
    st.session_state.produkty = []

# --- SEKCJA DODAWANIA ---
st.subheader("Dodaj nowy produkt")
# Używamy formularza, aby enter zatwierdzał dodanie (lepsze UX)
with st.form(key='add_form', clear_on_submit=True):
    nowy_produkt_input = st.text_input("Nazwa produktu:")
    submit_button = st.form_submit_button(label='Dodaj produkt')

    if submit_button:
        if nowy_produkt_input:
            # Sprawdzenie czy produkt już istnieje (ignorując wielkość liter)
            if not any(p.lower() == nowy_produkt_input.lower() for p in st.session_state.produkty):
                st.session_state.produkty.append(nowy_produkt_input)
                st.success(f"Dodano: {nowy_produkt_input}")
            else:
                st.warning("Ten produkt jest już na liście!")
        else:
            st.error("Wpisz nazwę produktu.")

# --- SEKCJA USUWANIA ---
st.subheader("Usuń produkt")

if st.session_state.produkty:
    col_del1, col_del2 = st.columns([3, 1])
    with col_del1:
        produkt_do_usuniecia = st.selectbox(
            "Wybierz produkt:", 
            st.session_state.produkty,
            label_visibility="collapsed"
        )
    with col_del2:
        # Przycisk usuwania obok selectboxa
        if st.button("Usuń 🗑️"):
            st.session_state.produkty.remove(produkt_do_usuniecia)
            st.rerun()
else:
    st.info("Brak produktów do usunięcia.")

st.divider()

# --- SEKCJA WYŚWIETLANIA ---
st.subheader(f"Stan magazynu ({len(st.session_state.produkty)} poz.)")

if st.session_state.produkty:
    # Wyświetlanie w ładniejszej formie (np. jako schludna lista)
    for i, produkt in enumerate(st.session_state.produkty, 1):
        st.markdown(f"{i}. {produkt}")
else:
    st.write("Magazyn jest pusty.")
