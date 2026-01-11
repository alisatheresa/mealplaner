import streamlit as st # Streamlit importieren, um UI-Elemente zu erstellen
import random


st.title("Persönlicher Kochplaner 🍽️")  # Titel der App im Browser anzeigen

# --------------------
# DATEN: Gerichte
# --------------------

GERICHTE = [
    {
        "name": "Linsen Bolognese",
        "typ": "fix",  # fix = feste Zutaten
        "kategorie": ["ganzjährig"],  # Saison / Kategorie
        "zutaten": {
            "Linsen": ("g", 80),
            "Passierte Tomaten": ("ml", 200),
            "Zwiebel": ("Stk", 0.5),
            "Knoblauch": ("Zehe", 1),
            "Spaghetti": ("g", 100)
        }
    },
    {
        "name": "Wraps",
        "typ": "modular",
        "kategorie": ["ganzjährig", "sommer"],
        "module": {
            "Basis": {"Wrap": ("Stk", 2)},
            "Protein": {"Falafel": ("g", 100), "Hähnchen": ("g", 120), "Tofu": ("g", 100)},
            "Gemüse": {"Paprika": ("Stk", 0.5), "Salat": ("g", 50), "Gurke": ("Stk", 0.25)},
            "Sauce": {"Hummus": ("g", 40), "Joghurt-Sauce": ("ml", 50)}
        }
    },
    {
        "name": "Asia Nudelpfanne",
        "typ": "modular",
        "kategorie": ["ganzjährig", "winter"],
        "module": {
            "Basis": {"Reisnudeln": ("g", 100)},
            "Protein": {"Tofu": ("g", 120), "Huhn": ("g", 120)},
            "Gemüse": {"Brokkoli": ("g", 100), "Karotten": ("g", 80)},
            "Sauce": {"Sojasauce": ("ml", 30), "Erdnusssauce": ("ml", 30)}
        }
    }
]

# --------------------
# UI: Personenanzahl
# --------------------
personen = st.slider("👥 Für wie viele Personen?", 1, 6, 2)

# Optional: Kategorie-Auswahl (z. B. Sommer, Winter)
selected_kategorie = st.multiselect(
    "Kategorie wählen (optional, leer = alle):",
    options=["ganzjährig", "sommer", "winter"]
)

# --------------------
# Funktion: Zutat zur Einkaufsliste hinzufügen
# --------------------
einkaufsliste = {}

def add_zutat(name, einheit, menge):
    if name in einkaufsliste:
        einkaufsliste[name][1] += menge  # Menge addieren, falls schon drin
    else:
        einkaufsliste[name] = [einheit, menge]

# --------------------
# FILTERN: nur Gerichte nach Kategorie
# --------------------
if selected_kategorie:
    filtered_gerichte = [g for g in GERICHTE if any(k in g["kategorie"] for k in selected_kategorie)]
else:
    filtered_gerichte = GERICHTE

# --------------------
# ZUFÄLLIGES GERICHT AUSWÄHLEN
# --------------------
gericht = random.choice(filtered_gerichte)
st.subheader(f"🥘 Vorgeschlagenes Gericht: {gericht['name']}")

# --------------------
# MENGE BERECHNEN & EINKAUFSLISTE ERSTELLEN
# --------------------
if gericht["typ"] == "fix":
    # feste Zutaten immer hinzufügen
    for zutat, (einheit, menge_pp) in gericht["zutaten"].items():
        add_zutat(zutat, einheit, menge_pp * personen)
else:
    st.write("Zutaten für dieses modulare Gericht (zufällig ausgewählt):")
    
    # feste Zutaten immer hinzufügen, falls vorhanden
    for zutat, (einheit, menge_pp) in gericht.get("feste_zutaten", {}).items():
        add_zutat(zutat, einheit, menge_pp * personen)
    
    # variable Zutaten: intelligente Zufallsauswahl
    for kategorie, zutaten in gericht.get("variable_zutaten", {}).items():
        # Anzahl der auszuwählenden Zutaten pro Kategorie festlegen
        if kategorie == "Protein":
            anzahl = 1  # 1 Protein
        elif kategorie == "Gemüse":
            anzahl = min(2, len(zutaten))  # max 2 Gemüse
        elif kategorie == "Sauce":
            anzahl = 1  # 1 Sauce
        else:
            anzahl = 1  # Default
        
        # zufällige Auswahl treffen (nur, wenn genug Zutaten vorhanden)
        if len(zutaten) <= anzahl:
            auswahl = list(zutaten.keys())
        else:
            auswahl = random.sample(list(zutaten.keys()), k=anzahl)
        
        # ausgewählte Zutaten hinzufügen
        for zutat in auswahl:
            einheit, menge_pp = zutaten[zutat]
            add_zutat(zutat, einheit, menge_pp * personen)
        
        # Anzeige der ausgewählten Zutaten
        st.write(f"{kategorie}: {', '.join(auswahl)}")
        
# --------------------
# AUSGABE: Einkaufsliste
# --------------------
st.subheader("🛒 Einkaufsliste")
for zutat, (einheit, menge) in einkaufsliste.items():
    st.write(f"- {zutat}: {round(menge,2)} {einheit}")
