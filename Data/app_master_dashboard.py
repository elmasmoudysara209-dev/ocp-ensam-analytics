import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="OCP Jorf Lasfar - Performance Energetique", layout="wide")

# Fonction robuste pour injecter les images de fond (Backgrounds)
def injecter_image_fond(nom_base_fichier):
    variantes = [nom_base_fichier, nom_base_fichier.replace("backgroud", "background")]
    trouve = False
    
    for var in variantes:
        for ext in ['.png', '.jpg', '.jpeg']:
            chemin_complet = f"Assets/{var}{ext}"
            if os.path.exists(chemin_complet):
                with open(chemin_complet, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                
                st.markdown(f"""
                    <style>
                    [data-testid="stAppViewContainer"], .stApp {{
                        background-image: url("data:image/{ext[1:]};base64,{encoded}") !important;
                        background-size: cover !important;
                        background-position: center !important;
                        background-repeat: no-repeat !important;
                        background-attachment: fixed !important;
                    }}
                    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], .main {{
                        background-color: transparent !important;
                    }}
                    </style>
                """, unsafe_allow_html=True)
                trouve = True
                break
        if trouve:
            break
    if not trouve:
        st.sidebar.warning(f"Fichier '{nom_base_fichier}' introuvable dans Assets/")

# 2. MOTEUR DE CHARGEMENT DES DONNÉES
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

dict_blocs, df_global, onglets_sous_tab = load_master_data()

if df_global is None or df_global.empty:
    st.error("Le fichier Excel dans 'Data/' est introuvable ou vide.")
    st.stop()

# ================================================================================
# 3. INTERFACE LATÉRALE (SIDEBAR) & FILTRES
# ================================================================================
st.sidebar.markdown("### Cadre du Projet d'Ingenierie")
st.sidebar.markdown("""
**PROJET DE FIN D'ANNÉE**  
*Ateliers de Cuisson — OCP Jorf Lasfar*

**Realise par :**  
*   **Sara El Masmoudy**  
*   **Mohamed Gorfti**  

**Encadre par :**  
*   **M. Akram Malyadi**  

*Etablissement : ENSAM Meknes*  
---
""")

st.sidebar.markdown("### Configuration Visuelle")
template_choisi = st.sidebar.selectbox(
    "Theme de l'interface :",
    options=[
        "Corporate Gold (Epure & Institutionnel)",
        "SCADA Cyber Industrial (Sombre & Haute Technologie)",
        "Steel & Mint Eco-Cuisson (Metallique & Moderne)"
    ]
)

st.sidebar.markdown("### Perimetre d'Analyse")
scope_marche = st.sidebar.selectbox(
    "Echelle des donnees :",
    options=["Vue Consolidee (Usine Globale)"] + onglets_sous_tab
)

df_active = df_global if scope_marche == "Vue Consolidee (Usine Globale)" else dict_blocs[scope_marche]

# ================================================================================
# 4. CONFIGURATION ET HARMONISATION DES ADAPTATIONS COULEURS (SIDEBAR INCLUSE)
# ================================================================================
if "Corporate Gold" in template_choisi:
    injecter_image_fond("backgroud1")
    theme_plotly = "plotly_white"
    color_main = "#1E4620"      
    color_accent = "#D4AF37"    
    color_bg_card = "rgba(255, 255, 255, 0.96)"   
    color_text = "#1A252C" 
    color_sidebar_bg = "rgba(248, 249, 250, 0.96)" # Fond clair pour la sidebar
    color_sidebar_text = "#1A252C"
    seq_couleurs = ['#1E4620', '#D4AF37', '#2C3E50']
    banner_style = "background: linear-gradient(135deg, #1E4620 0%, #2C3E50 100%); color: white;"
    chart_paper_bg = "rgba(255, 255, 255, 0.94)"
    chart_plot_bg = "rgba(245, 247, 250, 0.6)"

elif "SCADA Cyber Industrial" in template_choisi:
    injecter_image_fond("backgroud2")
    theme_plotly = "plotly_dark"
    color_main = "#00F0FF"      
    color_accent = "#FF0055"    
    color_bg_card = "rgba(15, 23, 42, 0.94)"   
    color_text = "#FFFFFF" 
    color_sidebar_bg = "rgba(15, 23, 42, 0.96)" # 🛠️ Fond sombre pour la barre à gauche
    color_sidebar_text = "#FFFFFF"               # 🛠️ Texte blanc pour un contraste maximal
    seq_couleurs = ['#00F0FF', '#FF0055', '#9333EA']
    banner_style = "background: #0F172A; border: 2px solid #00F0FF; color: #00F0FF;"
    chart_paper_bg = "rgba(30, 41, 59, 0.94)"
    chart_plot_bg = "rgba(15, 23, 42, 0.7)"

else:
    injecter_image_fond("backgroud3")
    theme_plotly = "ggplot2"
    color_main = "#059669"      
    color_accent = "#EA580C"    
    color_bg_card = "rgba(248, 250, 252, 0.96)"   
    color_text = "#0F172A"
    color_sidebar_bg = "rgba(241, 245, 249, 0.96)" 
    color_sidebar_text = "#0F172A"
    seq_couleurs = ['#059669', '#EA580C', '#475569']
    banner_style = "background: linear-gradient(135deg, #475569 0%, #059669 100%); color: white;"
    chart_paper_bg = "rgba(255, 255, 255, 0.94)"
    chart_plot_bg = "rgba(241, 245, 249, 0.6)"

# Injection CSS globale appliquée à la zone centrale ET à la sidebar
st.markdown(f"""
    <style>
    /* Zone principale */
    html, body, [data-testid="stAppViewContainer"] {{
        color: {color_text} !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans serif !important;
    }}
    h1, h2, h3, h4, h5, h6, p, span, label, small, li {{
        color: {color_text} !important;
    }}
    
    /* 🛠️ AJUSTEMENT TECHNIQUE FORCE SUR LA BARRE LATÉRALE (SIDEBAR) */
    [data-testid="stSidebar"] {{
        background-color: {color_sidebar_bg} !important;
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li, [data-testid="stSidebar"] small, [data-testid="stSidebar"] strong {{
        color: {color_sidebar_text} !important;
    }}
    
    /* Harmonisation visuelle des listes de sélection de la sidebar */
    [data-testid="stSidebar"] div[data-baseweb="select"] div {{
        color: {color_sidebar_text} !important;
    }}
    
    /* Correction de la couleur des onglets de navigation (Tabs) */
    button[data-baseweb="tab"] p {{
        color: {color_text} !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }}
    
    /* Style unifié des cartes d'information */
    .custom-card {{
        background-color: {color_bg_card} !important;
        padding: 20px;
        border-radius: 6px;
        text-align: center;
        border-top: 4px solid {color_main} !important;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .custom-card-title {{ font-size: 11px; color: #64748B !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
    .custom-card-val {{ font-size: 24px; font-weight: 700; margin-top: 5px; }}
    
    /* Panneau d'analyse de texte */
    .analysis-pane {{
        background-color: {color_bg_card} !important;
        padding: 22px;
        border-radius: 6px;
        border-left: 4px solid {color_accent} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        height: 100%;
    }}
    </style>
""", unsafe_allow_html=True)

# ================================================================================
# 5. EN-TÊTE ET LOGOS
# ================================================================================
col_l1, col_titre_centre, col_l2 = st.columns([2, 5, 1.8])
with col_l1:
    if os.path.exists("Assets/logo_ensam.png"): st.image("Assets/logo_ensam.png", width=190)
with col_l2:
    if os.path.exists("Assets/logo_ocp.png"): st.image("Assets/logo_ocp.png", width=110)

with col_titre_centre:
    st.markdown(f"""
    <div style="{banner_style} padding: 18px; border-radius: 6px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
        <h2 style='margin:0; font-weight:700; letter-spacing: 0.5px; color: white !important;'>DASHBOARD CENTRAL : INTEGRATION ENERGETIQUE</h2>
        <p style='margin:4px 0 0 0; font-size:13px; opacity:0.95; color: white !important;'>Perimetre : {scope_marche} | Configuration active : {template_choisi}</p>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# ================================================================================
# 6. BANDEAU DES INDICATEURS DE RENDEMENT CUMULÉS
# ================================================================================
calc_petcoke = df_active['Conso Petcoke (kg)'].sum()
calc_fuel = df_active['Conso Fuel P1 (kg)'].sum() + df_active['Conso Fuel P2 (kg)'].sum()
calc_prod = df_active['Prod RS3 (t)'].sum() + df_active['Prod RS4 (t)'].sum()
ratio_indus = (calc_petcoke + calc_fuel) / max(calc_prod, 1.0)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="custom-card"><div class="custom-card-title">Production Totale Realisee</div><div class="custom-card-val">{calc_prod:,.1f} t</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="custom-card"><div class="custom-card-title">Consommation Petcoke</div><div class="custom-card-val">{calc_petcoke:,.0f} kg</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="custom-card"><div class="custom-card-title">Consommation Fuels (P1+P2)</div><div class="custom-card-val">{calc_fuel:,.0f} kg</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="custom-card" style="border-top-color:{color_accent} !important;"><div class="custom-card-title">Indice d\'Efficience Thermique</div><div class="custom-card-val" style="color:{color_accent} !important;">{ratio_indus:.2f} kg/t</div></div>', unsafe_allow_html=True)

# ================================================================================
# 7. STRUCTURE DE NAVIGATION TECHNIQUE INTER-DOMAINES
# ================================================================================
st.write("---")
st.markdown("### Navigation Metier Inter-Domaines")
domaine_actif = st.tabs(["1. Pilotage Managerial & Performance", "2. Ingenierie Procede & Boucles DCS", "3. Logistique Matieres & Cinetique Silos"])

# --------------------------------------------------------------------------------
# DOMAINE 1 : PILOTAGE MANAGÉRIAL
# --------------------------------------------------------------------------------
with domaine_actif[0]:
    st.write("\n")
    c_graph1, c_text1 = st.columns([3, 1])
    
    with c_graph1:
        st.markdown("##### Bilan de Consommation Energetique par Periode Stable")
        fig_macro = px.bar(
            df_active, x='Nom_Bloc' if scope_marche == "Vue Consolidee (Usine Globale)" else 'Time',
            y=['Conso Petcoke (kg)', 'Conso Fuel P1 (kg)', 'Conso Fuel P2 (kg)'],
            labels={'value': 'Quantite thermique injectee', 'variable': 'Vecteur energetique'},
            color_discrete_sequence=seq_couleurs, template=theme_plotly
        )
        fig_macro.update_layout(
            margin=dict(t=15, b=20, l=20, r=20), height=380,
            paper_bgcolor=chart_paper_bg, plot_bgcolor=chart_plot_bg
        )
        st.plotly_chart(fig_macro, use_container_width=True)
    
    with c_text1:
        st.markdown(f"""
        <div class="analysis-pane">
            <h5 style="margin-top:0;">Analyse d'Exploitation</h5>
            <p>Ce module consolide la performance globale des ateliers de cuisson.</p>
            <ul>
                <li><b>Stabilite du flux :</b> Conforme aux specifications process.</li>
                <li><b>Vecteurs energetiques :</b> Base sur les extractions differentielles fiabilisees.</li>
            </ul>
            <br>
            <small style="color:#64748B;">Volume echantillonne</small>
            <h3 style="margin:0;">{len(df_active)} lignes</h3>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# DOMAINE 2 : INGENIERIE PROCÉDÉ
# --------------------------------------------------------------------------------
with domaine_actif[1]:
    st.write("\n")
    g_scada1, g_scada2 = st.columns(2)
    
    with g_scada1:
        st.markdown("##### Suivi temporel de la Boucle de Cuisson (Consigne vs Retour)")
        fig_scada = go.Figure()
        fig_scada.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Consigne injection petcock en t/h'], name="SP : Consigne (t/h)", line=dict(color=color_main, width=2.5)))
        fig_scada.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Retour de consigne injection petcock en t/h'], name="PV : Retour (t/h)", line=dict(color=color_accent, dash='dash', width=1.5)))
        fig_scada.update_layout(
            template=theme_plotly, margin=dict(t=20, b=20, l=20, r=20), height=350,
            legend=dict(orientation="h", y=1.12, x=0),
            paper_bgcolor=chart_paper_bg, plot_bgcolor=chart_plot_bg
        )
        st.plotly_chart(fig_scada, use_container_width=True)
        
    with g_scada2:
        st.markdown("##### Superposition Cuisson vs Production Horaire")
        fig_double = go.Figure()
        fig_double.add_trace(go.Bar(x=df_active['Time'], y=df_active['Prod RS3 (t)'] + df_active['Prod RS4 (t)'], name="Production RS3+RS4 (t)", marker_color=color_main, opacity=0.7))
        fig_double.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Conso Petcoke (kg)'], name="Delta Petcoke (kg)", line=dict(color=color_accent, width=2), yaxis="y2"))
        
        fig_double.update_layout(
            template=theme_plotly, height=350,
            margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", y=1.12, x=0),
            yaxis=dict(title="Production Totale (t)"),
            yaxis2=dict(title="Consommation Coke (kg)", overlaying="y", side="right", showgrid=False),
            paper_bgcolor=chart_paper_bg, plot_bgcolor=chart_plot_bg
        )
        st.plotly_chart(fig_double, use_container_width=True)

# --------------------------------------------------------------------------------
# DOMAINE 3 : LOGISTIQUE MATIÈRES
# --------------------------------------------------------------------------------
with domaine_actif[2]:
    st.write("\n")
    c_silo_graph, c_silo_data = st.columns([2, 1])
    with c_silo_graph:
        st.markdown("##### Alimentation continue et Autonomie des Stocks Silos")
        fig_silo = px.area(
            df_active, x='Time', y=['Niveau de silot Brute en t', 'Niveau de silot Broyé en t'],
            labels={'value': 'Quantite en stock (t)', 'variable': 'Affectation Silo'},
            color_discrete_sequence=[seq_couleurs[2], seq_couleurs[1]], template=theme_plotly
        )
        fig_silo.update_layout(
            margin=dict(t=15, b=20, l=20, r=20), height=350,
            legend=dict(orientation="h", y=1.12, x=0),
            paper_bgcolor=chart_paper_bg, plot_bgcolor=chart_plot_bg
        )
        st.plotly_chart(fig_silo, use_container_width=True)
        
    with c_silo_data:
        st.markdown("##### Extraction des bilans matieres")
        st.write("Registre courant pret pour audit :")
        st.dataframe(df_active[['Time', 'Niveau de silot Brute en t', 'Niveau de silot Broyé en t', 'Conso Petcoke (kg)']].head(5), use_container_width=True)
        
        csv_bytes = df_active.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exporter les donnees en CSV",
            data=csv_bytes,
            file_name=f"Synthese_Matiere_{scope_marche.replace(' ', '_')}.csv",
            mime='text/csv'
        )