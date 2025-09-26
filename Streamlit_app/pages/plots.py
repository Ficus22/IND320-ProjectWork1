# streamlit_app/pages/plots.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configuration de la page
st.set_page_config(layout="wide")
st.title("📈 Visualisations Météo - Janvier 2020")

# Chargement des données (avec cache)
@st.cache_data
def load_data():
    df = pd.read_csv("../data/open-meteo-subset.csv")
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    return df

df = load_data()

# Sidebar pour les filtres
st.sidebar.header("Filtres")
selected_month = st.sidebar.select_slider(
    "Mois",
    options=sorted(df.index.month.unique()),
    value=1  # Janvier par défaut
)

# Filtrer les données par mois
filtered_df = df[df.index.month == selected_month]

# Créer les 4 graphiques
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(12, 12), sharex=True)

# 1. Température
axes[0].plot(filtered_df.index, filtered_df['temperature_2m (°C)'], color='red')
axes[0].set_ylabel("Température (°C)")
axes[0].grid(True)
axes[0].set_title(f"Mois {selected_month}/2020")

# 2. Précipitations
axes[1].bar(filtered_df.index, filtered_df['precipitation (mm)'], color='blue', width=0.05)
axes[1].set_ylabel("Précipitations (mm)")

# 3. Vitesse et rafales de vent
axes[2].plot(filtered_df.index, filtered_df['wind_speed_10m (m/s)'], color='green', label='Vitesse')
axes[2].plot(filtered_df.index, filtered_df['wind_gusts_10m (m/s)'], color='orange', label='Rafales')
axes[2].set_ylabel("Vent (m/s)")
axes[2].legend()
axes[2].grid(True)

# 4. Direction du vent (flèches)
wind_dir_rad = np.deg2rad(filtered_df['wind_direction_10m (°)'])
u = filtered_df['wind_speed_10m (m/s)'] * np.cos(wind_dir_rad)
v = filtered_df['wind_speed_10m (m/s)'] * np.sin(wind_dir_rad)

# Afficher 1 flèche toutes les 12h pour éviter la surcharge
step = 12
axes[3].quiver(
    filtered_df.index[::step],
    np.zeros(len(filtered_df[::step])),
    u[::step], v[::step],
    filtered_df['wind_speed_10m (m/s)'][::step],
    scale=15, cmap='viridis', width=0.005
)
axes[3].set_ylabel("Direction du vent")
axes[3].set_yticks([])

# Ajouter une barre de couleur pour la vitesse
sm = plt.cm.ScalarMappable(cmap='viridis',
                          norm=plt.Normalize(vmin=filtered_df['wind_speed_10m (m/s)'].min(),
                                            vmax=filtered_df['wind_speed_10m (m/s)'].max()))
fig.colorbar(sm, ax=axes[3], label='Vitesse (m/s)')

plt.suptitle(f"Données météo - Mois {selected_month}/2020", y=1.02)
plt.tight_layout()
st.pyplot(fig)

# Afficher les stats du mois sélectionné
st.subheader("Statistiques du mois")
col1, col2, col3 = st.columns(3)
col1.metric("Température moyenne", f"{filtered_df['temperature_2m (°C)'].mean():.1f} °C")
col2.metric("Précipitations totales", f"{filtered_df['precipitation (mm)'].sum():.1f} mm")
col3.metric("Vitesse moyenne du vent", f"{filtered_df['wind_speed_10m (m/s)'].mean():.1f} m/s")
