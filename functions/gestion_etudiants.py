# Importation des modules nécessaires
import json  # Pour manipuler les fichiers JSON (lecture/écriture)
import os    # Pour gérer les chemins des fichiers de manière portable

# Fonction pour ajouter un nouvel étudiant
def ajouter_etudiant(id_etudiant, nom, prenom):
    # Définir le chemin du fichier des étudiants
    etudiants_file = os.path.join("data", "etudiants.json")  # Chemin du fichier etudiants.json

    # Charger la liste actuelle des étudiants depuis le fichier JSON
    with open(etudiants_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON dans une liste Python

    # Vérifier si l'ID existe déjà dans la liste des étudiants
    if any(etudiant["id"] == id_etudiant for etudiant in etudiants):
        print(f"Erreur : L'ID {id_etudiant} est déjà utilisé.")  # Afficher une erreur si l'ID est déjà pris
        return  # Sortir de la fonction

    # Créer un dictionnaire pour le nouvel étudiant
    nouvel_etudiant = {"id": id_etudiant, "nom": nom, "prenom": prenom}  # Structurer les données de l'étudiant
    etudiants.append(nouvel_etudiant)  # Ajouter le nouvel étudiant à la liste

    # Sauvegarder les modifications dans etudiants.json
    with open(etudiants_file, 'w') as f:
        json.dump(etudiants, f, indent=4)  # Écrire la liste mise à jour dans le fichier avec indentation
    print(f"Étudiant {nom} {prenom} (ID: {id_etudiant}) ajouté avec succès.")  # Confirmer l'ajout

# Fonction pour supprimer un étudiant
def supprimer_etudiant(id_etudiant):
    # Définir le chemin du fichier des étudiants
    etudiants_file = os.path.join("data", "etudiants.json")  # Chemin du fichier etudiants.json

    # Charger la liste actuelle des étudiants depuis le fichier JSON
    with open(etudiants_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON dans une liste Python

    # Rechercher l'étudiant correspondant à l'ID
    etudiant_a_supprimer = next((etudiant for etudiant in etudiants if etudiant["id"] == id_etudiant), None)
    if etudiant_a_supprimer is None:
        print(f"Erreur : L'étudiant avec l'ID {id_etudiant} n'existe pas.")  # Afficher une erreur si l'étudiant n'existe pas
        return  # Sortir de la fonction

    # Supprimer l'étudiant de la liste
    etudiants.remove(etudiant_a_supprimer)  # Retirer l'étudiant trouvé de la liste

    # Sauvegarder les modifications dans etudiants.json
    with open(etudiants_file, 'w') as f:
        json.dump(etudiants, f, indent=4)  # Écrire la liste mise à jour dans le fichier
    print(f"Étudiant avec l'ID {id_etudiant} supprimé avec succès.")  # Confirmer la suppression

# Fonction pour afficher tous les étudiants
def afficher_etudiants():
    # Définir le chemin du fichier des étudiants
    etudiants_file = os.path.join("data", "etudiants.json")  # Chemin du fichier etudiants.json

    # Charger la liste des étudiants depuis le fichier JSON
    with open(etudiants_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON dans une liste Python

    # Vérifier si la liste des étudiants est vide
    if not etudiants:
        print("Aucun étudiant trouvé.")  # Afficher un message si la liste est vide
    else:
        # Afficher les informations de chaque étudiant
        for etudiant in etudiants:
            print(f"ID: {etudiant['id']}, Nom: {etudiant['nom']}, Prénom: {etudiant['prenom']}")  # Afficher les détails de l'étudiant