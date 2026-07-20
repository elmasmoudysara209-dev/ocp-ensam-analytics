import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. Configuration de la page
st.set_page_config(page_title="Dashboard OCP - ENSAM", layout="wide", page_icon="🏭")

# Custom CSS pour peaufiner l'esthétique des métriques et des encadrés
st.markdown("""
    <style>
    .kpi-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #1E4620;
    }
    .project-card {
        background-color: #1E4620;
        color: white;
        padding: 22px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Gestion des Logos et En-tête de page
col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
    # Charge le logo local ou affiche un espaceur si absent
    if os.path.exists("assets/logo_ensam.png"):
        st.image("assets/logo_ensam.png", width=120)
    else:
        st.markdown("**[ENSAM MEKNÈS]**")

with col_logo2:
    if os.path.exists("assets/logo_ocp.png"):
        st.image("assets/logo_ocp.png", width=120)
    else:
        st.markdown("**[OCP GROUP]**")

with col_title:
    st.markdown("<h2 style='text-align: center; color: #2C3E50; margin-top: 10px;'>Direction du Site Industriel Jorf Lasfar</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #7F8C8D; font-weight: normal;'>Plateforme d'Analyse Énergétique & Optimisation Procédés</h4>", unsafe_allow_html=True)

st.write("---")

# 3. Sidebar : Bloc d'identification et Filtres
st.sidebar.markdown("### 🎓 Cadre du Projet")
st.sidebar.markdown("""
<div style="background-color: #ffffff; padding: 15px; border-radius: 6px; border: 1px solid #E0E0E0; margin-bottom: 20px;">
    <p style='margin-bottom: 5px;'><strong>🎓 Établissement :</strong><br>ENSAM Meknès</p>
    <p style='margin-bottom: 5px;'><strong>🏢 Entreprise :</strong><br>OCP Jorf Lasfar</p>
    <p style='margin-bottom: 5px;'><strong>👨‍💻 Réalisé par :</strong><br>Bilal Naji</p>
    <p style='margin-bottom: 0px;'><strong>👨‍🏫 Encadré par :</strong><br>[Nom de l'encadrant]</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.markdown("### 🕹️ Sélection des Campagnes")

# Chargement et calcul des données
@st.cache_data
def load_and_process_data():
    df = pd.read_excel('data/Donnees_Nettoyees_v4.xlsx')
    df['Time'] = pd.to_datetime(df['Time'])
    # Re-génération des 9 sous-tableaux sur changement S1/S2
    df['S1_change'] = df['Totaliseur fuel S1 en kg'].diff().fillna(0) != 0
    df['S2_change'] = df['Totaliseur fuel S2 en kg'].diff().fillna(0) != 0
    df['subtable_id'] = (df['S1_change'] | df['S2_change']).cumsum() + 1
    
    # Déductions des consommations par ligne
    df['Conso_Petcoke'] = df['Totaliseur injection coke en kg'].diff().fillna(0)
    df['Conso_Fuel'] = df['Totaliseur fuel P1 en kg'].diff().fillna(0) + df['Totaliseur fuel P2 en kg'].diff().fillna(0)
    df['Prod_Totale'] = df['Totaliseur de production RS3 en t'].diff().fillna(0) + df['Totaliseur de production RS4 en t'].diff().fillna(0)
    return df

try:
    df = load_and_process_data()
    
    # Sélecteur de bloc dans la sidebar
    liste_blocs = ["Vue Globale (Tous les blocs)"] + [f"Sous-Tableau {i}" for i in sorted(df['subtable_id'].unique())]
    choix_bloc = st.sidebar.selectbox("Filtrer par sous-tableau :", options=liste_blocs)
    
    if choix_bloc != "Vue Globale (Tous les blocs)":
        id_bloc = int(choix_bloc.split()[-1])
        df_display = df[df['subtable_id'] == id_bloc]
    else:
        df_display = df

    # Bannière d'introduction de la section centrale
    st.markdown(f"""
    <div class="project-card">
        <h3 style='margin: 0;'>Analyse Dynamique : {choix_bloc}</h3>
        <p style='margin: 5px 0 0 0; opacity: 0.9;'>Suivi en temps réel des consommations spécifiques de Petcoke et de Fuel par rapport aux rendements des lignes de production RS3 / RS4.</p>
    </div>
    """, unsafe_allow_html=True)

    # 4. Bloc d'indicateurs clés (KPIs)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"<div class='kpi-box'><small style='color:#7F8C8D;'>PROD. TOTALE</small><h3 style='margin:0;color:#2C3E50;'>{df_display['Prod_Totale'].sum():,.1f} t</h3></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"<div class='kpi-box'><small style='color:#7F8C8D;'>CONSO. PETCOKE</small><h3 style='margin:0;color:#1E4620;'>{df_display['Conso_Petcoke'].sum():,.1f} kg</h3></div>", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"<div class='kpi-box'><small style='color:#7F8C8D;'>CONSO. FUEL TOTAL</small><h3 style='margin:0;color:#D35400;'>{df_display['Conso_Fuel'].sum():,.1f} kg</h3></div>", unsafe_allow_html=True)
    with kpi4:
        ratio = (df_display['Conso_Petcoke'].sum() + df_display['Conso_Fuel'].sum()) / max(df_display['Prod_Totale'].sum(), 1)
        st.markdown(f"<div class='kpi-box'><small style='color:#7F8C8D;'>RATIO ÉNERGÉTIQUE</small><h3 style='margin:0;color:#2980B9;'>{ratio:.2f} kg/t</h3></div>", unsafe_allow_html=True)

    st.write("\n")

    # 5. Graphiques principaux
    g1, g2 = st.columns(2)
    
    with g1:
        st.markdown("##### 📈 Profil Temporel : Débit de Consigne vs Retour d'Injection")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df_display['Time'], y=df_display['Consigne injection petcock en t/h'], name="Consigne", line=dict(color='#1E4620', width=2)))
        fig1.add_trace(go.Scatter(x=df_display['Time'], y=df_display['Retour de consigne injection petcock en t/h'], name="Retour Réel", line=dict(color='#E74C3C', width=1.5, dash='dot')))
        fig1.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=20, b=20), height=350, legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        st.markdown("##### 📊 Suivi des Niveaux de Stockage : Silos")
        fig2 = px.line(df_display, x='Time', y=['Niveau de silot Brute en t', 'Niveau de silot Broyé en t'],
                        color_discrete_map={'Niveau de silot Brute en t': '#2C3E50', 'Niveau de silot Broyé en t': '#E67E22'}, template="plotly_white")
        fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350, legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(fig2, use_container_width=True)

    # 6. Section de données brutes
    st.write("---")
    st.markdown("##### 📋 Registre d'Acquisition des Données Filtrées (Pas de 40 min)")
    st.dataframe(df_display[['Time', 'Consigne injection petcock en t/h', 'Conso_Petcoke', 'Conso_Fuel', 'Niveau de silot Brute en t', 'Prod_Totale']], use_container_width=True)

except Exception as e:
    st.warning(f"Veuillez vérifier l'emplacement du fichier 'Donnees_Nettoyees_v4.xlsx' dans le sous-dossier 'data/'. Détails : {e}")