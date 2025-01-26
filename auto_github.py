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
    
    
    # Ajouter fichiers
    run_command(["git", "add", "."])

    # Créer un commit
    commit_message = "Automatic push using Python script"
    run_command(["git", "commit", "-m", commit_message])

    # Pousser les changements
    run_command(["git", "push", "-u", "origin", "main"])

if __name__ == "__main__":
    automate_github_workflow()
