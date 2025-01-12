import subprocess

def run_command(command):
    """
    Exécute une commande shell et affiche la sortie ou les erreurs.
    """
    try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {e.stderr}")

# Commandes prédéfinies
def automate_github_workflow():
    """
    Exécute un workflow GitHub prédéfini.
    """
    
    # Ajouter fichiers
    print("Ajout des fichiers au staging area...")
    run_command(["git", "add", "."])

    # Créer un commit
    print("Création d'un commit...")
    commit_message = "Mise à jour automatique via script Python"
    run_command(["git", "commit", "-m", commit_message])

    # Pousser les changements
    print("Push des changements vers GitHub...")
    run_command(["git", "push", "-u", "origin", "main"])

if __name__ == "__main__":
    automate_github_workflow()
