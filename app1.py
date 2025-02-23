import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Webscraping Project: Amazon Analytics Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5em !important;
        color: #FF9900 !important;
        text-shadow: 2px 2px 4px #000000;
        padding: 20px;
        background: linear-gradient(90deg, #232F3E 0%, #FF9900 100%);
        border-radius: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #232F3E !important;
    }
    .metric-box {
        background-color: #37475A !important;
        padding: 15px !important;
        border-radius: 10px !important;
        margin: 10px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("amazon_products.csv", parse_dates=["Date"])

df = load_data()

# Création de la colonne Marque
df['Marque'] = df['Titre'].str.split().str[0].str.strip()

# En-tête avec logo et titre
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)  # Remplacez par votre logo
with col2:
    st.markdown('<div class="main-title">📈 Amazon Analytics Dashboard Pro</div>', unsafe_allow_html=True)

# Sidebar stylisée
with st.sidebar:
    st.image("logo_small.png", width=100)  # Logo réduit pour la sidebar
    st.markdown("## 🔍 Filtres Intelligents")
    
    marques = st.multiselect(
        "**Sélection des marques**",
        options=df['Titre'].str.split().str[0].unique(),
        format_func=lambda x: f"🏷️ {x}"
    )
    
    date_range = st.date_input(
        "**Période d'analyse**",
        [df['Date'].min(), df['Date'].max()],
        help="Sélectionnez une plage de dates pour filtrer les données"
    )
    
    st.markdown("---")
    st.markdown("ℹ️ **Aide rapide**")
    st.info("Utilisez les filtres pour affiner l'analyse. Les graphiques s'ajustent en temps réel.")

# Contenu principal
st.divider()

# Section des KPI
st.subheader("📉 Informations globales")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Produits Suivis", df['Titre'].nunique(), help="Nombre total de produits uniques")
with kpi2:
    st.metric("Prix Moyen", f"{df['Prix'].mean():.2f} €")
with kpi3:
    st.metric("Note Moyenne", f"{df['Evaluation'].mean():.2f}/5")
with kpi4:
    st.metric("Total Avis", df['Nombre_d_evaluations'].sum())

filtered_df = df[
    (df['Titre'].str.split().str[0].isin(marques if marques else df['Titre'].str.split().str[0].unique())) &
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1]))
]

st.title("📊 Tendances Clées")
col1, col2, col3 = st.columns(3)
col1.metric("Produits uniques", filtered_df['Titre'].nunique())
col2.metric("Prix moyen", f"{filtered_df['Prix'].mean():.2f} €")
col3.metric("Note moyenne", f"{filtered_df['Evaluation'].mean():.2f}/5")

st.subheader("Évolution des prix")
fig = px.line(filtered_df, x="Date", y="Prix", color="Titre", markers=True)
st.plotly_chart(fig, use_container_width=True)


# Graphique principal
st.subheader("📅 Évolution des Prix")
tab1, tab2 = st.tabs(["Vue Globale", "Analyse Comparative Par Marque"])

with tab1:
   # Création d'une colonne simplifiée pour les noms
    df['Nom_Produit'] = df['Titre'].str[:20] + '...'


    # Création du graphique
    fig = px.line(
        df,
        x='Date',
        y='Prix',
        color='Nom_Produit',
        markers=True,
        title='Évolution des prix des produits',
        labels={'Prix': 'Prix (€)', 'Date': 'Date'},
        hover_data=['Titre']
    )

    # Personnalisation
    fig.update_layout(
        legend=dict(
            title='Produits',
            orientation='v',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=1.02,
            itemwidth=40,
            itemsizing='constant',
            font=dict(size=10),
            bgcolor='rgba(245,245,245,0.8)'
        ),
        margin=dict(l=50, r=150, t=50, b=50),
        xaxis=dict(tickangle=45),
        hoverdistance=20
    )
    # Affichage dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    fig2 = px.area(df.groupby(['Date', 'Marque'])['Prix'].mean().reset_index(),
                  x="Date", y="Prix", color="Marque",
                  title="Répartition par Marque")
    st.plotly_chart(fig2, use_container_width=True)

# Tableau interactif
st.subheader("🔎 Données Brutes")
with st.expander("Explorer les données détaillées", expanded=False):
    st.dataframe(
        df.sort_values('Date', ascending=False),
        use_container_width=True,
        column_config={
            "Image": st.column_config.ImageColumn("Aperçu Produit"),
            "Prix": st.column_config.NumberColumn(format="%.2f €"),
            "Evaluation": st.column_config.ProgressColumn(
                format="%.1f ⭐",
                min_value=0,
                max_value=5
            )
        },
        hide_index=True
    )

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666;">
        🚀 Dashboard développé par [Groupe2: Dometi, Mpolah & Tchunbu] - 
        Mise à jour du {date} - 
        Source: Données Amazon
    </div>
    """.format(date=datetime.now().strftime("%d/%m/%Y")), 
    unsafe_allow_html=True)