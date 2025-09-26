# streamlit_app/app.py
import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard Météo")
st.title("🌦️ Dashboard Météo - IND320")
st.markdown("""
Bienvenue sur le dashboard d'analyse des données météorologiques de 2020.

**Fonctionnalités :**
- Visualisation des températures, précipitations et vents
- Analyse des directions du vent avec flèches vectorielles
- Filtres par mois pour une analyse ciblée
""")

st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="Accueil")
st.sidebar.page_link("pages/1_📊_Data_Table.py", label="Tableau de données")
st.sidebar.page_link("pages/2_📈_Plots.py", label="Visualisations")
st.sidebar.page_link("pages/4_🔍_About.py", label="À propos")

st.image("https://i.imgur.com/JQJgD2m.png", width=300) 
