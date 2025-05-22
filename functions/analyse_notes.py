# Importation des modules nécessaires
import json  # Pour manipuler les fichiers JSON (lecture/écriture)
import os    # Pour gérer les chemins des fichiers de manière portable

# Fonction pour calculer la moyenne d'une matière pour un étudiant
def calculer_moyenne_matiere(id_etudiant, matiere):
    # Définir le chemin du fichier des notes
    notes_file = os.path.join("data", "notes.json")  # Chemin du fichier notes.json

    # Charger les notes avec gestion des erreurs
    try:
        with open(notes_file, 'r') as f:
            content = f.read().strip()  # Lire et nettoyer le contenu du fichier
            notes = json.loads(content) if content else {}  # Parser le JSON ou initialiser un dictionnaire vide si vide
    except FileNotFoundError:
        return 0.0  # Retourner 0.0 si le fichier n'existe pas
    except json.JSONDecodeError:
        return 0.0  # Retourner 0.0 si le contenu JSON est invalide

    # Vérifier si l'étudiant ou la matière existe dans les notes
    if str(id_etudiant) not in notes or matiere not in notes[str(id_etudiant)]:
        return 0.0  # Retourner 0.0 si aucune note n'est trouvée pour cette matière

    # Récupérer la liste des notes pour la matière
    notes_liste = notes[str(id_etudiant)][matiere]
    # Calculer et retourner la moyenne, ou 0.0 si la liste est vide
    return sum(notes_liste) / len(notes_liste) if notes_liste else 0.0

# Fonction pour calculer la moyenne générale d'un étudiant
def calculer_moyenne_generale(id_etudiant):
    # Définir le chemin du fichier des notes
    notes_file = os.path.join("data", "notes.json")  # Chemin du fichier notes.json

    # Charger les notes avec gestion des erreurs
    try:
        with open(notes_file, 'r') as f:
            content = f.read().strip()  # Lire et nettoyer le contenu
            notes = json.loads(content) if content else {}  # Parser le JSON ou initialiser un dictionnaire vide
    except FileNotFoundError:
        return 0.0  # Retourner 0.0 si le fichier n'existe pas
    except json.JSONDecodeError:
        return 0.0  # Retourner 0.0 si le contenu JSON est invalide

    # Vérifier si l'étudiant a des notes
    if str(id_etudiant) not in notes or not notes[str(id_etudiant)]:
        return 0.0  # Retourner 0.0 si aucune note n'est trouvée

    # Récupérer toutes les notes de toutes les matières
    total_notes = []
    for matiere_notes in notes[str(id_etudiant)].values():
        total_notes.extend(matiere_notes)  # Ajouter les notes de chaque matière à la liste totale
    # Calculer et retourner la moyenne générale, ou 0.0 si aucune note
    return sum(total_notes) / len(total_notes) if total_notes else 0.0

# Fonction pour afficher le bulletin complet d'un étudiant
def afficher_bulletin(id_etudiant):
    # Définir les chemins des fichiers des étudiants et des notes
    notes_file = os.path.join("data", "etudiants.json")   # Chemin du fichier etudiants.json
    notes_data_file = os.path.join("data", "notes.json")  # Chemin du fichier notes.json

    # Charger la liste des étudiants
    with open(notes_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON dans une liste

    # Charger les notes avec gestion des erreurs
    try:
        with open(notes_data_file, 'r') as f:
            content = f.read().strip()  # Lire et nettoyer le contenu
            notes = json.loads(content) if content else {}  # Parser le JSON ou initialiser un dictionnaire vide
    except FileNotFoundError:
        notes = {}  # Initialiser un dictionnaire vide si le fichier n'existe pas
    except json.JSONDecodeError:
        notes = {}  # Initialiser un dictionnaire vide si le contenu JSON est invalide

    # Trouver l'étudiant correspondant à l'ID
    etudiant = next((e for e in etudiants if e["id"] == id_etudiant), None)
    if not etudiant:
        print(f"Erreur : L'étudiant avec l'ID {id_etudiant} n'existe pas.")  # Afficher une erreur si l'étudiant n'existe pas
        return  # Sortir de la fonction

    # Afficher l'en-tête du bulletin
    print(f"\nBulletin de {etudiant['prenom']} {etudiant['nom']} (ID: {id_etudiant})")

    # Vérifier si l'étudiant a des notes
    if str(id_etudiant) not in notes or not notes[str(id_etudiant)]:
        print("Aucune note enregistrée.")  # Afficher un message si pas de notes
        return  # Sortir de la fonction

    # Afficher les notes et moyennes par matière
    for matiere, notes_liste in notes[str(id_etudiant)].items():
        moyenne = calculer_moyenne_matiere(id_etudiant, matiere)  # Calculer la moyenne de la matière
        print(f"{matiere} : Notes = {notes_liste}, Moyenne = {moyenne:.2f}")  # Afficher matière, notes et moyenne

    # Calculer et afficher la moyenne générale
    moyenne_generale = calculer_moyenne_generale(id_etudiant)
    print(f"Moyenne générale : {moyenne_generale:.2f}")

# Fonction pour trier et afficher les étudiants par moyenne générale
def trier_etudiants_par_moyenne():
    # Définir les chemins des fichiers des étudiants et des notes
    etudiants_file = os.path.join("data", "etudiants.json")  # Chemin du fichier etudiants.json
    notes_file = os.path.join("data", "notes.json")          # Chemin du fichier notes.json

    # Charger la liste des étudiants
    with open(etudiants_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON

    # Charger les notes avec gestion des erreurs
    try:
        with open(notes_file, 'r') as f:
            content = f.read().strip()  # Lire et nettoyer le contenu
            notes = json.loads(content) if content else {}  # Parser le JSON ou initialiser un dictionnaire vide
    except FileNotFoundError:
        notes = {}  # Initialiser un dictionnaire vide si le fichier n'existe pas
    except json.JSONDecodeError:
        notes = {}  # Initialiser un dictionnaire vide si le contenu JSON est invalide

    # Calculer la moyenne générale pour chaque étudiant
    etudiants_avec_moyennes = []
    for etudiant in etudiants:
        id_etudiant = etudiant["id"]  # Récupérer l'ID de l'étudiant
        moyenne = calculer_moyenne_generale(id_etudiant)  # Calculer sa moyenne générale
        etudiants_avec_moyennes.append((etudiant["prenom"], etudiant["nom"], moyenne))  # Ajouter un tuple (prenom, nom, moyenne)

    # Trier les étudiants par moyenne générale (ordre décroissant)
    etudiants_avec_moyennes.sort(key=lambda x: x[2], reverse=True)  # Trier selon la moyenne (index 2)

    # Afficher le classement
    print("\nClassement des étudiants par moyenne générale :")  # En-tête du classement
    for prenom, nom, moyenne in etudiants_avec_moyennes:
        print(f"{prenom} {nom} : Moyenne = {moyenne:.2f}")  # Afficher chaque étudiant avec sa moyenne