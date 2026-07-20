import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="OCP Jorf Lasfar - Master Dashboard", layout="wide", page_icon="🏭")

# ================================================================================
# MOTEUR DE CHARGEMENT DES DONNÉES (CORRIGÉ & SÉCURISÉ)
# ================================================================================
@st.cache_data
def load_master_data():
    chemin_excel = 'Data/Donnees_Nettoyees_Calculs_Lignes_Final.xlsx'
    if not os.path.exists(chemin_excel):
        return {}, pd.DataFrame(), []
        
    xls = pd.ExcelFile(chemin_excel)
    onglets = [sheet for sheet in xls.sheet_names if "Sous-Tableau" in sheet]
    
    dict_blocs = {}
    liste_dfs = []
    
    for sheet in onglets:
        df_sheet = pd.read_excel(chemin_excel, sheet_name=sheet)
        df_sheet['Time'] = pd.to_datetime(df_sheet['Time'])
        df_sheet['Nom_Bloc'] = sheet
        dict_blocs[sheet] = df_sheet
        liste_dfs.append(df_sheet)
        
    df_global = pd.concat(liste_dfs, ignore_index=True) if liste_dfs else pd.DataFrame()
    return dict_blocs, df_global, onglets

# ⚠️ LA LIGNE CLÉ CRUCIALE ICI : On s'assure d'assigner explicitement les 3 variables globales
dict_blocs, df_global, onglets_sous_tab = load_master_data()

# Sécurité si le fichier Excel v2 n'est pas trouvé
if df_global is None or df_global.empty:
    st.error("🚨 Le fichier Excel est introuvable dans 'Data/'. Veuillez vérifier son emplacement.")
    st.stop()

# ================================================================================
# 3. INTERFACE LATÉRALE (SIDEBAR) : CONFIGURATION DU PROJET & DES CRÉDITS
# ================================================================================
st.sidebar.markdown("### 🎓 Cadre du Projet d'Ingénierie")

# Cartouche officiel de présentation (Texte brut ultra-stable pour éviter l'écran blanc)
st.sidebar.markdown("""
**📍 PROJET DE FIN D'ANNÉE**
*Ateliers de Cuisson — OCP Jorf Lasfar*

👥 **Réalisé par :**
*   **Sara El Masmoudy**
*   **Mohamed Gorfti**

👨‍🏫 **Encadré par :**
*   **M. Akram Malyadi**

*Établissement : ENSAM Meknès*
---
""")

# 🎛️ CHOIX DU TEMPLATE GRAPHIQUE (L'élément créatif demandé)
st.sidebar.markdown("### 🎨 Thème & Template Visuel")
template_choisi = st.sidebar.selectbox(
    "Choisir l'ambiance du Dashboard :",
    options=[
        "1. OCP Corporate Gold (Épuré & Institutionnel)",
        "2. SCADA Cyber Industrial (Sombre & Haute Technologie)",
        "3. Steel & Mint Eco-Cuisson (Métallique & Moderne)"
    ]
)

# 🕹️ SÉLECTION DES FILTRES DE PRODUCTION
st.sidebar.markdown("### 🔍 Périmètre d'Analyse")
scope_marche = st.sidebar.selectbox(
    "Sélectionner l'échelle des données :",
    options=["Vue Consolidée (Usine Globale)"] + onglets_sous_tab
)

# Filtrage dynamique des données selon le scope
df_active = df_global if scope_marche == "Vue Consolidée (Usine Globale)" else dict_blocs[scope_marche]

# ================================================================================
# 4. CONFIGURATION DYNAMIQUE DES PALETTES EN FONCTION DU TEMPLATE CHOISI
# ================================================================================
if "1. OCP Corporate Gold" in template_choisi:
    theme_plotly = "plotly_white"
    color_main = "#1E4620"      # Vert profond OCP
    color_accent = "#D4AF37"    # Or Éclatant
    color_bg_card = "#F8F9FA"   # Gris très clair
    color_text = "#2C3E50"
    seq_couleurs = ['#1E4620', '#D4AF37', '#2C3E50']
    banner_style = "background: linear-gradient(135deg, #1E4620 0%, #2C3E50 100%); color: white;"

elif "2. SCADA Cyber Industrial" in template_choisi:
    theme_plotly = "plotly_dark"
    color_main = "#00F0FF"      # Cyan Néon
    color_accent = "#FF0055"    # Rubis Cyber
    color_bg_card = "#111827"   # Gris Anthracite foncé
    color_text = "#E5E7EB"
    seq_couleurs = ['#00F0FF', '#FF0055', '#9333EA']
    banner_style = "background: #111827; border: 2px solid #00F0FF; color: #00F0FF;"

else: # 3. Steel & Mint Eco-Cuisson
    theme_plotly = "ggplot2"
    color_main = "#059669"      # Vert Menthe Éco
    color_accent = "#EA580C"    # Orange Sécurité
    color_bg_card = "#F1F5F9"   # Gris Acier Métallique
    color_text = "#0F172A"
    seq_couleurs = ['#059669', '#EA580C', '#475569']
    banner_style = "background: linear-gradient(135deg, #475569 0%, #059669 100%); color: white;"

# Injection locale sécurisée pour les petits blocs d'info
st.markdown(f"""
    <style>
    .custom-card {{
        background-color: {color_bg_card};
        padding: 18px;
        border-radius: 8px;
        text-align: center;
        border-top: 4px solid {color_main};
        margin-bottom: 15px;
    }}
    .custom-card-title {{ font-size: 12px; color: #7F8C8D; font-weight: 600; text-transform: uppercase; }}
    .custom-card-val {{ font-size: 22px; color: {color_text}; font-weight: 700; margin-top: 5px; }}
    </style>
""", unsafe_allow_html=True)

# ================================================================================
# 5. BANNIÈRE EN-TÊTE DYNAMIQUE
# ================================================================================
col_l1, col_titre_centre, col_l2 = st.columns([1, 4, 1])
with col_l1:
    if os.path.exists("Assets/logo_ensam.png"): st.image("Assets/logo_ensam.png", width=120)
with col_l2:
    if os.path.exists("Assets/logo_ocp.png"): st.image("Assets/logo_ocp.png", width=110)

with col_titre_centre:
    st.markdown(f"""
    <div style="{banner_style} padding: 15px; border-radius: 8px; text-align: center;">
        <h2 style='margin:0; font-weight:700;'>🎯 CENTRAL DASHBOARD : EXCELLENCE ÉNÉRGÉTIQUE</h2>
        <p style='margin:4px 0 0 0; font-size:14px; opacity:0.9;'>Périmètre actuel : {scope_marche} | Design actif : {template_choisi.split('.')[1]}</p>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# ================================================================================
# 6. BLOC GENERAL DES KPI MACRO-PROCÉDÉS
# ================================================================================
calc_petcoke = df_active['Conso Petcoke (kg)'].sum()
calc_fuel = df_active['Conso Fuel P1 (kg)'].sum() + df_active['Conso Fuel P2 (kg)'].sum()
calc_prod = df_active['Prod RS3 (t)'].sum() + df_active['Prod RS4 (t)'].sum()
ratio_indus = (calc_petcoke + calc_fuel) / max(calc_prod, 1.0)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="custom-card"><div class="custom-card-title">🏗️ Production Totale</div><div class="custom-card-val">{calc_prod:,.1f} t</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="custom-card"><div class="custom-card-title">🔥 Consommation Coke</div><div class="custom-card-val">{calc_petcoke:,.0f} kg</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="custom-card"><div class="custom-card-title">🛢️ Consommation Fuels</div><div class="custom-card-val">{calc_fuel:,.0f} kg</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="custom-card" style="border-top-color:{color_accent};"><div class="custom-card-title">📉 Indice d\'Efficience</div><div class="custom-card-val">{ratio_indus:.2f} kg/t</div></div>', unsafe_allow_html=True)

# ================================================================================
# 7. NAVIGATION PAR BOUTONS/ONGLETS INTERNES (LES 3 DOMAINES CLÉS COUPLÉS)
# ================================================================================
st.write("---")
st.markdown("### 🗂️ Navigation Métier Inter-Domaines")
domaine_actif = st.tabs(["🌐 1. Pilotage Managérial & Performance", "🎛️ 2. Ingénierie Procédé & Boucles DCS", "🛢️ 3. Logistique Matières & Cinétique Silos"])

# --------------------------------------------------------------------------------
# DOMAINE 1 : PILOTAGE MANAGÉRIAL (VUE DIRECTION)
# --------------------------------------------------------------------------------
with domaine_actif[0]:
    st.markdown("#### 📈 Synthèse d'Exploitation Globale (Macro)")
    
    c_graph1, c_text1 = st.columns([3, 1])
    with c_graph1:
        # Graphique d'analyse énergétique par bloc
        fig_macro = px.bar(
            df_active, x='Nom_Bloc' if scope_marche == "Vue Consolidée (Usine Globale)" else 'Time',
            y=['Conso Petcoke (kg)', 'Conso Fuel P1 (kg)', 'Conso Fuel P2 (kg)'],
            title="Consommation cumulée d'énergie thermique sur la période",
            color_discrete_sequence=seq_couleurs, template=theme_plotly
        )
        st.plotly_chart(fig_macro, use_container_width=True)
    
    with c_text1:
        st.markdown(f"""
        **📋 Note de Performance :**
        Ce module permet aux responsables d'exploitation de valider les campagnes de marche stables.
        
        *   **Stabilité Courante :** Parfaitement alignée sur les critères industriels.
        *   **Énergie Dominante :** Relevée sur les colonnes de calculs différentiels de la V2.
        """)
        st.metric("Nombre total d'enregistrements", len(df_active))

# --------------------------------------------------------------------------------
# DOMAINE 2 : INGENIERIE PROCÉDÉ (BOUCLES SCADA)
# --------------------------------------------------------------------------------
with domaine_actif[1]:
    st.markdown("#### 🎮 Régulation Thermique & Stabilité des Automatismes")
    
    g_scada1, g_scada2 = st.columns(2)
    with g_scada1:
        # Évolution temporelle consigne/retour
        fig_scada = go.Figure()
        fig_scada.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Consigne injection petcock en t/h'], name="SP : Consigne (t/h)", line=dict(color=color_main, width=2.5)))
        fig_scada.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Retour de consigne injection petcock en t/h'], name="PV : Retour (t/h)", line=dict(color=color_accent, dash='dash', width=1.5)))
        fig_scada.update_layout(template=theme_plotly, title="Suivi temporel de la Boucle de Cuisson Injection", margin=dict(t=40, b=20), height=350, legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig_scada, use_container_width=True)
        
    with g_scada2:
        # Corrélation double axe
        fig_double = go.Figure()
        fig_double.add_trace(go.Bar(x=df_active['Time'], y=df_active['Prod RS3 (t)'] + df_active['Prod RS4 (t)'], name="Production (t)", marker_color=color_main, opacity=0.7))
        fig_double.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Conso Petcoke (kg)'], name="Delta Petcoke (kg)", line=dict(color=color_accent, width=2), yaxis="y2"))
        fig_double.update_layout(
            template=theme_plotly, title="Superposition Cuisson vs Production horaire", height=350,
            margin=dict(t=40, b=20), legend=dict(orientation="h", y=1.12),
            yaxis=dict(title="Production Totale (t)"),
            yaxis2=dict(title="Consommation Coke (kg)", overlaying="y", side="right")
        )
        st.plotly_chart(fig_double, use_container_width=True)

# --------------------------------------------------------------------------------
# DOMAINE 3 : LOGISTIQUE MATIÈRES (STOCKS SILOS)
# --------------------------------------------------------------------------------
with domaine_actif[2]:
    st.markdown("#### 🛢️ Cinétique de Remplissage & Autonomie des Stocks")
    
    c_silo_graph, c_silo_data = st.columns([2, 1])
    with c_silo_graph:
        # Profil d'aire des silos
        fig_silo = px.area(
            df_active, x='Time', y=['Niveau de silot Brute en t', 'Niveau de silot Broyé en t'],
            title="Courbe d'alimentation des Silos Brut & Broyé (Capacités en t)",
            color_discrete_sequence=[seq_couleurs[2], seq_couleurs[1]], template=theme_plotly
        )
        fig_silo.update_layout(margin=dict(t=40, b=20), height=350, legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig_silo, use_container_width=True)
        
    with c_silo_data:
        st.markdown("##### 📥 Exportation des rapports de poste")
        st.write("Visualisez un extrait des lignes chronologiques filtrées prêtes pour extraction :")
        st.dataframe(df_active[['Time', 'Niveau de silot Brute en t', 'Niveau de silot Broyé en t', 'Conso Petcoke (kg)']].head(8), use_container_width=True)
        
        # Téléchargement dynamique
        csv_bytes = df_active.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger le registre courant (.csv)",
            data=csv_bytes,
            file_name=f"Rapport_OCP_Scope_{scope_marche.replace(' ', '_')}.csv",
            mime='text/csv'
        )

print("Master application with multi-template rendering completed successfully.")
