import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="DCS Monitor - OCP Procédés", layout="wide")

st.markdown("### 🎛️ Système d'Analyse des Boucles de Régulation (SCADA)")
st.caption("Suivi technique de l'alignement Consigne / Retour Mesuré")

st.sidebar.markdown("### 🏭 Atelier OCP Jorf Lasfar")
st.sidebar.markdown("**Analyse Procédé :** Bilal Naji\n**Parcours :** Génie Industriel & Excellence Opérationnelle")

try:
    chemin_excel = 'Data/Donnees_Nettoyees_Calculs_Lignes_Final.xlsx'
    xls = pd.ExcelFile(chemin_excel)
    onglets = [s for s in xls.sheet_names if "Sous-Tableau" in s]
    
    # Sélecteur de bloc stable dans la barre latérale
    selection = st.sidebar.selectbox("Sélectionner un Sous-Tableau de marche :", options=onglets)
    df_active = pd.read_excel(chemin_excel, sheet_name=selection)
    df_active['Time'] = pd.to_datetime(df_active['Time'])

    # Métriques techniques
    ecart_moyen = (df_active['Consigne injection petcock en t/h'] - df_active['Retour de consigne injection petcock en t/h']).abs().mean()
    conso_max = df_active['Conso Petcoke (kg)'].max()

    t1, t2 = st.columns(2)
    t1.metric(label="🎯 Écart Moyen de Régulation", value=f"{ecart_moyen:.3f} t/h")
    t2.metric(label="⚡ Pic de Consommation Instantané", value=f"{conso_max:,.1f} kg/40min")

    st.write("---")

    # Graphique de régulation interactif
    fig_reg = go.Figure()
    fig_reg.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Consigne injection petcock en t/h'], name="Consigne Automate (t/h)", line=dict(color='#2C3E50', width=2.5)))
    fig_reg.add_trace(go.Scatter(x=df_active['Time'], y=df_active['Retour de consigne injection petcock en t/h'], name="Retour Capteur (t/h)", line=dict(color='#E74C3C', width=1.5, dash='dash')))
    
    fig_reg.update_layout(template="plotly_white", margin=dict(l=40, r=40, t=10, b=10), height=400, legend=dict(orientation="h", y=1.1, x=0))
    st.plotly_chart(fig_reg, use_container_width=True)

    # Affichage sécurisé du tableau
    st.markdown("##### 📝 Registre des 10 derniers points de contrôle")
    st.dataframe(df_active[['Time', 'Consigne injection petcock en t/h', 'Retour de consigne injection petcock en t/h', 'Conso Petcoke (kg)']].head(10), use_container_width=True)

except Exception as e:
    st.error(f"Erreur d'accès à la feuille de calcul. Détails : {e}")