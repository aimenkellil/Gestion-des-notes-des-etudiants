# Importation des modules nécessaires
import json  # Pour manipuler les fichiers JSON (lecture/écriture)
import os    # Pour gérer les chemins des fichiers de manière portable

# Fonction pour ajouter une note à un étudiant dans une matière
def ajouter_note(id_etudiant, matiere, note):
    # Définir les chemins des fichiers JSON
    etudiants_file = os.path.join("data", "etudiants.json")  # Chemin du fichier des étudiants
    notes_file = os.path.join("data", "notes.json")          # Chemin du fichier des notes

    # Charger la liste des étudiants depuis etudiants.json
    with open(etudiants_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON dans une liste Python

    # Charger les notes existantes depuis notes.json, avec gestion des erreurs
    try:
        with open(notes_file, 'r') as f:
            content = f.read().strip()  # Lire et nettoyer le contenu (supprimer espaces/retours à la ligne)
            notes = json.loads(content) if content else {}  # Parser le JSON ou initialiser un dictionnaire vide si fichier vide
    except FileNotFoundError:
        notes = {}  # Si le fichier n'existe pas, initialiser un dictionnaire vide
        with open(notes_file, 'w') as f:
            json.dump(notes, f)  # Créer le fichier avec un dictionnaire vide
    except json.JSONDecodeError:
        notes = {}  # Si le contenu JSON est invalide, initialiser un dictionnaire vide
        with open(notes_file, 'w') as f:
            json.dump(notes, f)  # Réécrire le fichier avec un dictionnaire vide

    # Vérifier si l'étudiant existe dans la liste des étudiants
    if not any(etudiant["id"] == id_etudiant for etudiant in etudiants):
        print(f"Erreur : L'étudiant avec l'ID {id_etudiant} n'existe pas.")  # Afficher une erreur si l'ID n'existe pas
        return  # Sortir de la fonction

    # Vérifier si la note est valide (entre 0 et 20)
    if not (0 <= note <= 20):
        print("Erreur : La note doit être entre 0 et 20.")  # Afficher une erreur si la note est hors limites
        return  # Sortir de la fonction

    # Ajouter la note si elle n'existe pas déjà
    if str(id_etudiant) not in notes:
        notes[str(id_etudiant)] = {}  # Créer une entrée pour l'étudiant si elle n'existe pas
    if matiere not in notes[str(id_etudiant)]:
        notes[str(id_etudiant)][matiere] = []  # Créer une liste vide pour la matière si elle n'existe pas
    if float(note) not in notes[str(id_etudiant)][matiere]:
        notes[str(id_etudiant)][matiere].append(float(note))  # Ajouter la note si elle n'est pas déjà présente

    # Sauvegarder les modifications dans notes.json
    with open(notes_file, 'w') as f:
        json.dump(notes, f, indent=4)  # Écrire le dictionnaire mis à jour dans le fichier avec indentation

    # Confirmer l'ajout de la note
    print(f"Note {note} ajoutée pour l'étudiant {id_etudiant} en {matiere}.")

# Fonction pour supprimer une note d'un étudiant dans une matière
def supprimer_note(id_etudiant, matiere, note):
    # Définir les chemins des fichiers JSON
    etudiants_file = os.path.join("data", "etudiants.json")  # Chemin du fichier des étudiants
    notes_file = os.path.join("data", "notes.json")          # Chemin du fichier des notes

    # Charger la liste des étudiants depuis etudiants.json
    with open(etudiants_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON dans une liste Python

    # Charger les notes existantes depuis notes.json, avec gestion des erreurs
    try:
        with open(notes_file, 'r') as f:
            content = f.read().strip()  # Lire et nettoyer le contenu
            notes = json.loads(content) if content else {}  # Parser le JSON ou initialiser un dictionnaire vide
    except FileNotFoundError:
        notes = {}  # Si le fichier n'existe pas, initialiser un dictionnaire vide
        with open(notes_file, 'w') as f:
            json.dump(notes, f)  # Créer le fichier
    except json.JSONDecodeError:
        notes = {}  # Si le contenu JSON est invalide, initialiser un dictionnaire vide
        with open(notes_file, 'w') as f:
            json.dump(notes, f)  # Réécrire le fichier

    # Vérifier si l'étudiant existe
    if not any(etudiant["id"] == id_etudiant for etudiant in etudiants):
        print(f"Erreur : L'étudiant avec l'ID {id_etudiant} n'existe pas.")  # Afficher une erreur si l'ID n'existe pas
        return  # Sortir de la fonction

    # Vérifier si l'étudiant a des notes dans cette matière
    if str(id_etudiant) not in notes or matiere not in notes[str(id_etudiant)]:
        print(f"Erreur : Aucune note trouvée pour l'étudiant {id_etudiant} en {matiere}.")  # Afficher une erreur si pas de notes
        return  # Sortir de la fonction

    # Vérifier si la note spécifique existe
    if float(note) not in notes[str(id_etudiant)][matiere]:
        print(f"Erreur : La note {note} n'existe pas pour l'étudiant {id_etudiant} en {matiere}.")  # Afficher une erreur si la note n'existe pas
        return  # Sortir de la fonction

    # Supprimer la note
    notes[str(id_etudiant)][matiere].remove(float(note))  # Retirer la note de la liste

    # Nettoyer la structure si nécessaire
    if not notes[str(id_etudiant)][matiere]:
        del notes[str(id_etudiant)][matiere]  # Supprimer la matière si la liste des notes est vide
        if not notes[str(id_etudiant)]:
            del notes[str(id_etudiant)]  # Supprimer l'étudiant si aucune matière n'a de notes

    # Sauvegarder les modifications dans notes.json
    with open(notes_file, 'w') as f:
        json.dump(notes, f, indent=4)  # Écrire le dictionnaire mis à jour

    # Confirmer la suppression
    print(f"Note {note} supprimée pour l'étudiant {id_etudiant} en {matiere}.")

# Fonction pour afficher les notes d'un étudiant
def afficher_notes(id_etudiant):
    # Définir les chemins des fichiers JSON
    etudiants_file = os.path.join("data", "etudiants.json")  # Chemin du fichier des étudiants
    notes_file = os.path.join("data", "notes.json")          # Chemin du fichier des notes

    # Charger la liste des étudiants depuis etudiants.json
    with open(etudiants_file, 'r') as f:
        etudiants = json.load(f)  # Lecture du contenu JSON

    # Charger les notes existantes depuis notes.json, avec gestion des erreurs
    try:
        with open(notes_file, 'r') as f:
            content = f.read().strip()  # Lire et nettoyer le contenu
            notes = json.loads(content) if content else {}  # Parser le JSON ou initialiser un dictionnaire vide
    except FileNotFoundError:
        notes = {}  # Si le fichier n'existe pas, initialiser un dictionnaire vide
    except json.JSONDecodeError:
        notes = {}  # Si le contenu JSON est invalide, initialiser un dictionnaire vide

    # Vérifier si l'étudiant existe
    if not any(etudiant["id"] == id_etudiant for etudiant in etudiants):
        print(f"Erreur : L'étudiant avec l'ID {id_etudiant} n'existe pas.")  # Afficher une erreur si l'ID n'existe pas
        return  # Sortir de la fonction

    # Vérifier si l'étudiant a des notes
    if str(id_etudiant) not in notes or not notes[str(id_etudiant)]:
        print(f"Aucune note trouvée pour l'étudiant avec l'ID {id_etudiant}.")  # Afficher une erreur si pas de notes
        return  # Sortir de la fonction

    # Afficher les notes de l'étudiant
    print(f"Notes de l'étudiant ID {id_etudiant} :")  # Afficher l'en-tête
    for matiere, notes_liste in notes[str(id_etudiant)].items():
        print(f"{matiere} : {notes_liste}")  # Afficher chaque matière et ses notes