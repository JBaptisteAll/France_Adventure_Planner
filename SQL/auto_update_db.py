import sqlite3
import pandas as pd
import os

# 📍 Chemin vers ta base SQLite
db_path = "chemin/vers/ta/database.sqlite"

# 📍 Dictionnaire avec les fichiers CSV et leurs tables correspondantes
csv_files = {
    "chemin/vers/fichier1.csv": "table1",
    "chemin/vers/fichier2.csv": "table2",
    "chemin/vers/fichier3.csv": "table3",
    "chemin/vers/fichier4.csv": "table4",
    "chemin/vers/fichier5.csv": "table5"
}

# 🔗 Connexion à SQLite
conn = sqlite3.connect(db_path)

for csv_file, table_name in csv_files.items():
    if os.path.exists(csv_file):  # Vérifier que le fichier existe
        print(f"🔄 Mise à jour de la table '{table_name}' depuis '{csv_file}'...")
        
        # Charger le CSV en DataFrame pandas
        df = pd.read_csv(csv_file)

        # Insérer ou remplacer les données dans la base
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"✅ Table '{table_name}' mise à jour avec succès !")
    else:
        print(f"⚠️ Fichier non trouvé : {csv_file}")

# ✅ Fermer la connexion
conn.commit()
conn.close()

print("🎉 Mise à jour complète de la base de données !")
