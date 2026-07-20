import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="OCP - Flux Silos", layout="wide", page_icon="🛢️")

st.markdown("""
    <style>
    .silo-container {
        background-color: #FFFDF9;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E5D8C3;
    }
    </style>
""", unsafe_allow_html=True)

# Logos
col_l, col_r = st.columns([5, 1])
with col_r:
    if os.path.exists("Assets/logo_ocp.png"): st.image("Assets/logo_ocp.png", width=110)

st.title("🛢️ Gestion de Stockage & Cinétique des Silos")
st.markdown("##### *Travail d'Optimisation — Bilal Naji (ENSAM Meknès)*")
st.write("---")

try:
    chemin = 'Data/Donnees_Nettoyees_Calculs_Lignes_Final.xlsx'
    xls = pd.ExcelFile(chemin)
    onglets = [s for s in xls.sheet_names if "Sous-Tableau" in s]
    
    selected = st.selectbox("Sélectionner la période de chargement :", options=onglets)
    df_silo = pd.read_excel(chemin, sheet_name=selected)

    # Graphique d'évolution des stocks
    fig_area = px.area(df_silo, x='Time', y=['Niveau de silot Brute en t', 'Niveau de silot Broyé en t'],
                       title=f"Cinétique de transfert de matière au sein du {selected}",
                       color_discrete_map={'Niveau de silot Brute en t': '#2C3E50', 'Niveau de silot Broyé en t': '#D35400'},
                       template="plotly_white")
    fig_area.update_layout(height=400, legend=dict(orientation="h", y=1.08, x=0))
    st.plotly_chart(fig_area, use_container_width=True)

    st.write("---")
    
    # Extraction de données pour vérification rapide
    st.markdown("##### 📋 Extrait des Relevés de Niveaux de Matières")
    st.dataframe(df_silo[['Time', 'Niveau de silot Brute en t', 'Niveau de silot Broyé en t', 'Prod RS3 (t)', 'Prod RS4 (t)']].head(10), use_container_width=True)

except Exception as e:
    st.error(f"Erreur de chargement. Vérifiez les dossiers. Détails : {e}")