import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Test", page_icon="🤦‍♂️", layout="wide")

# Fonction pour charger les données et les regrouper
@st.cache_data
def load_and_aggregate_data():
    # Charger le fichier CSV
    df = pd.read_csv("final_results.csv")
    
    # Regrouper les données par Ville, Date et Moment_Journee
    df_agg = df.groupby(["Ville", "Date", "Day_Time"], as_index=False).agg({
        "Temp_Max": "mean",
        "Temp_Min": "mean",
        "Temp_Avg": "mean",
        "Humidity": "mean",
        "Rain_Probability": "mean",
        "Weather": lambda x: x.mode()[0]  # Prendre la météo la plus fréquente
    })
    
    # Arrondir les valeurs numériques pour plus de lisibilité
    df_agg["Temp_Max"] = df_agg["Temp_Max"].round(1)
    df_agg["Temp_Min"] = df_agg["Temp_Min"].round(1)
    df_agg["Temp_Avg"] = df_agg["Temp_Avg"].round(1)
    df_agg["Humidity"] = df_agg["Humidity"].round(1)
    df_agg["Rain_Probability"] = df_agg["Rain_Probability"].round(2)
    
    return df_agg

# Charger les données
df_agg = load_and_aggregate_data()

# Exemple de treks
treks = {
    "Les Ecrins": ["Bourg d'Oisans", "Vallouise"],
    "Mont-Blanc": []
}

# Titre de la page
st.markdown("## Test")
st.markdown("Explorez les prévisions météo.")

# Sélection de l'itinéraire
chosen_trek = st.selectbox("Choisir un itinéraire :", list(treks.keys()))

# Sélectionner les villes associées à cet itinéraire
selected_cities = treks[chosen_trek]
st.markdown(f"**Itinéraire sélectionné :** {chosen_trek}")
st.markdown(f"**Villes impliquées :** {', '.join(selected_cities)}")

# Filtrer les données pour les villes sélectionnées
df_filtered = df_agg[df_agg["Ville"].isin(selected_cities)]

# Affichage des données consolidées par moment de la journée
st.markdown("### Prévisions météo consolidées")
for moment in ["Morning", "Afternoon", "Evening", "Night"]:
    st.markdown(f"#### {moment}")
    df_moment = df_filtered[df_filtered["Day_Time"] == moment]
    
    if not df_moment.empty:
        st.dataframe(df_moment[["Ville", "Date", "Temp_Max", "Temp_Min", "Temp_Avg", "Humidity", "Rain_Probability", "Weather"]])
    else:
        st.write(f"Aucune donnée disponible pour {moment}.")

# Footer
st.markdown("**Bon trek et profitez des montagnes !** 🥾")
