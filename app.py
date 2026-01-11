import streamlit as st  # Streamlit importieren, um UI-Elemente zu erstellen

st.title("Persönlicher Kochplaner 🍽️")  # Titel der App im Browser anzeigen

# --------------------
# DATEN: Feste & modulare Gerichte
# --------------------
FIXE_GERICHTE = {
    "Linsen Bolognese": {  # Gerichtname
        "Linsen": ("g", 80),  # Zutat: Einheit + Menge pro Person
        "Passierte Tomaten": ("ml", 200),
        "Zwiebel": ("Stk", 0.5),
        "Knoblauch": ("Zehe", 1),
        "Spaghetti": ("g", 100),
    }
}

MODULARE_GERICHTE = {
    "Wraps": {  # Gericht mit wählbaren Modulen
        "Basis": {"Wrap": ("Stk", 2)},  # Modul: Basis
        "Protein": {"Falafel": ("g", 100), "Tofu": ("g", 100)},  # Modul Protein
        "Gemüse": {"Paprika": ("Stk", 0.5), "Salat": ("g", 50), "Gurke": ("Stk", 0.25)},  # Modul Gemüse
        "Sauce": {"Hummus": ("g", 40), "Joghurt-Sauce": ("ml", 50)}  # Modul Sauce
    }
}

# --------------------
# UI: Personenanzahl & Gerichtstyp
# --------------------
personen = st.slider("👥 Personen", 1, 6, 2)  # Slider: wähle Anzahl der Personen (1-6), Standard=2

gericht_typ = st.radio("Gerichtstyp", ["Fixes Gericht", "Modulares Gericht"])  
# Radio-Button: wähle zwischen festen und modularen Gerichten

einkaufsliste = {}  # leeres Dictionary, in dem alle Zutaten mit Menge gesammelt werden

# --------------------
# FUNKTION: Zutat hinzufügen
# --------------------
def add_zutat(name, einheit, menge):  # Funktion zum Hinzufügen einer Zutat
    if name in einkaufsliste:  # Wenn Zutat schon drin
        einkaufsliste[name][1] += menge  # Menge addieren
    else:
        einkaufsliste[name] = [einheit, menge]  # Neu hinzufügen

# --------------------
# FIXE GERICHTE
# --------------------
if gericht_typ == "Fixes Gericht":  # Wenn Nutzer feste Gerichte wählt
    gericht = st.selectbox("Gericht wählen", FIXE_GERICHTE.keys())  # Dropdown mit festen Gerichten
    for zutat, (einheit, menge_pp) in FIXE_GERICHTE[gericht].items():  # Jede Zutat durchlaufen
        add_zutat(zutat, einheit, menge_pp * personen)  # Menge anpassen für Anzahl Personen

# --------------------
# MODULARE GERICHTE
# --------------------
else:  # Wenn Nutzer modulare Gerichte wählt
    gericht = st.selectbox("Gericht wählen", MODULARE_GERICHTE.keys())  # Dropdown mit modularen Gerichten
    module = MODULARE_GERICHTE[gericht]  # alle Module des Gerichts holen

    for kategorie, zutaten in module.items():  # Jede Kategorie (Basis, Protein, Gemüse, Sauce)
        auswahl = st.multiselect(kategorie, zutaten.keys())  # Auswahlfeld: mehrere Zutaten wählbar
        for zutat in auswahl:  # Jede gewählte Zutat
            einheit, menge_pp = zutaten[zutat]  # Menge pro Person
            add_zutat(zutat, einheit, menge_pp * personen)  # Menge anpassen und zur Einkaufsliste hinzufügen

# --------------------
# AUSGABE: Einkaufsliste
# --------------------
st.subheader("🛒 Einkaufsliste")  # Untertitel
for zutat, (einheit, menge) in einkaufsliste.items():  # Durch alle Zutaten iterieren
    st.write(f"- {zutat}: {round(menge, 2)} {einheit}")  # Zutat + Menge anzeigen, auf 2 Dezimalstellen gerundet
