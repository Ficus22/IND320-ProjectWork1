# streamlit_app/pages/data_Table.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode

@st.cache_data
def load_data():
    df = pd.read_csv("../data/open-meteo-subset.csv")
    df['time'] = pd.to_datetime(df['time'])
    return df

st.title("📊 Tableau des données météo")
df = load_data()

# Tableau interactif avec AgGrid
AgGrid(
    df,
    height=500,
    enableEnterpriseModules=True,
    updateMode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=True
)

# Graphique de la température du premier mois
st.subheader("Température du premier mois")
first_month = df[df['time'].dt.month == 1]
st.line_chart(first_month.set_index('time')['temperature_2m (°C)'])
