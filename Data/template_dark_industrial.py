import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="DCS Monitor - OCP", layout="wide", page_icon="🎛️")

# Injection de CSS pour passer l'application en mode sombre technique
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #E2E8F0; }
    header, footer { label { color: white !important; } }
    .stSelectbox div[data-baseweb="select"] { background-color: #1E293B !important; color: white !important; }
    div[data-testid="stSidebar"] { background-color: #1E293B !important; }
    .dcs-card {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 6px;
        border: 1px solid #334155;
        text-align: center;
    }
    h1, h2, h3, h4, h5, p { color: #E2E8F0 !important; }
    </style>
""", unsafe_allow_html=True)

# En-tête d'identification projet
st.sidebar.markdown("<h3 style='color:#38BDF8;'>🎛️ DCS SCADA MONITOR</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="background-color: #0F172A; padding: 12px; border-radius: 6px; border: 1px solid #334155;">
    <p style='margin-bottom:4px; font-size:12px; color:#94A3B8;'>ORGANISME</p>
    <p style='margin-top:0; font-weight:bold; font-size:14px;'>OCP Jorf Lasfar / ENSAM</p>
    <p style='margin-bottom:4px; font-size:12px; color:#94A3B8;'>INGÉNIEUR PROJET</p>
    <p style='margin-top:0; font-weight:bold; font-size:14px; color:#38BDF8;'>Bilal Naji</p>
    <p style='margin-bottom:4px; font-size:12px; color:#94A3B8;'>ENCADRANT DE STAGE</p>
    <p style='margin-top:0; font-weight:bold; font-size:14px;'>[Nom de l'encadrant]</p>
</div>
""", unsafe_allow_html=True)

st.title("🎛️ Interface Temps Réel - Lignes de Cuisson Ciment")
st.write("---")

try:
    df = pd.read_excel('data/Donnees_Nettoyees_v4.xlsx')
    df['Time'] = pd.to_datetime(df['Time'])
    df['Conso_Petcoke'] = df['Totaliseur injection coke en kg'].diff().fillna(0)
    df['Conso_Fuel'] = df['Totaliseur fuel P1 en kg'].diff().fillna(0) + df['Totaliseur fuel P2 en kg'].diff().fillna(0)
    df['Prod_Totale'] = df['Totaliseur de production RS3 en t'].diff().fillna(0) + df['Totaliseur de production RS4 en t'].diff().fillna(0)

    # Section de 3 KPIs style automate industriel
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='dcs-card'><span style='color:#94A3B8;font-size:13px;'>🎚️ DEBIT INJECTION MOYEN</span><br><h2 style='color:#38BDF8 !important;margin:5px;'>{df['Retour de consigne injection petcock en t/h'].mean():.2f} t/h</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='dcs-card'><span style='color:#94A3B8;font-size:13px;'>⚡ PRODUCTION RS3 + RS4</span><br><h2 style='color:#34D399 !important;margin:5px;'>{df['Prod_Totale'].sum():,.1f} t</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='dcs-card'><span style='color:#94A3B8;font-size:13px;'>🔥 APPORT THERMIQUE COKE</span><br><h2 style='color:#F87171 !important;margin:5px;'>{df['Conso_Petcoke'].sum():,.0f} kg</h2></div>", unsafe_allow_html=True)

    st.write("\n")

    # Graphique pleine largeur : Analyse des corrélations Rendement/Combustibles
    st.markdown("##### 📊 Analyse de Performance : Production de Ciment vs Apports Thermiques")
    
    fig_dcs = go.Figure()
    fig_dcs.add_trace(go.Bar(x=df['Time'], y=df['Prod_Totale'], name="Production (t)", marker_color='#34D399'))
    fig_dcs.add_trace(go.Scatter(x=df['Time'], y=df['Conso_Petcoke'], name="Conso Petcoke (kg)", yaxis="y2", line=dict(color='#F87171', width=1.5)))
    
    fig_dcs.update_layout(
        template="plotly_dark",
        paper_bgcolor='#1E293B',
        plot_bgcolor='#1E293B',
        margin=dict(l=40, r=40, t=20, b=20),
        height=400,
        legend=dict(orientation="h", y=1.1, x=0),
        yaxis=dict(title="Production Ciment (t)", title Clifford=dict(color='#34D399')),
        yaxis2=dict(title="Consommation Petcoke (kg)", title_font=dict(color='#F87171'), overlaying="y", side="right")
    )
    st.plotly_chart(fig_dcs, use_container_width=True)

except Exception as e:
    st.error(f"Fichier de données introuvable. Erreur : {e}")