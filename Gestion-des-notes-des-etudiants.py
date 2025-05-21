# Import des bibliothèques nécessaires
import tkinter as tk
from tkinter import messagebox, simpledialog
import json

# Dictionnaires pour stocker les étudiants et leurs notes
etudiants = {}  # {id: (nom, prénom)}
notes = {}      # {id: {matière: [note1, note2, ...]}}

# --- Fonctions pour charger et sauvegarder les données ---

def charger_donnees():
    """Charge les données des fichiers JSON si existants"""
    global etudiants, notes
    try:
        with open("etudiants.json", "r") as f:
            etudiants.update(json.load(f))
        with open("notes.json", "r") as f:
            notes.update(json.load(f))
    except FileNotFoundError:
        # Fichiers inexistants = première utilisation
        pass

def sauvegarder_donnees():
    """Sauvegarde les données dans les fichiers JSON"""
    with open("etudiants.json", "w") as f:
        json.dump(etudiants, f, indent=4)
    with open("notes.json", "w") as f:
        json.dump(notes, f, indent=4)

# --- Fonctions pour la gestion des étudiants ---

def ajouter_etudiant_gui():
    """Ajoute un étudiant via une interface de dialogue"""
    identifiant = simpledialog.askstring("Identifiant", "ID de l'étudiant :")
    if not identifiant:
        return
    if identifiant in etudiants:
        messagebox.showerror("Erreur", "ID déjà existant.")
        return
    nom = simpledialog.askstring("Nom", "Nom :")
    prenom = simpledialog.askstring("Prénom", "Prénom :")
    if nom and prenom:
        etudiants[identifiant] = (nom, prenom)
        notes[identifiant] = {}
        messagebox.showinfo("Succès", f"Étudiant {prenom} {nom} ajouté.")
    else:
        messagebox.showerror("Erreur", "Champs incomplets.")

def supprimer_etudiant_gui():
    """Supprime un étudiant existant"""
    identifiant = simpledialog.askstring("Supprimer étudiant", "ID de l'étudiant à supprimer :")
    if identifiant in etudiants:
        confirm = messagebox.askyesno("Confirmation", f"Supprimer l'étudiant {etudiants[identifiant][1]} {etudiants[identifiant][0]} ?")
        if confirm:
            etudiants.pop(identifiant)
            notes.pop(identifiant, None)
            messagebox.showinfo("Succès", "Étudiant supprimé.")
    else:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")

def afficher_etudiants_gui():
    """Affiche la liste des étudiants enregistrés"""
    if not etudiants:
        messagebox.showinfo("Étudiants", "Aucun étudiant enregistré.")
        return
    liste = ""
    for identifiant, (nom, prenom) in etudiants.items():
        liste += f"ID: {identifiant} - {prenom} {nom}\n"
    messagebox.showinfo("Liste des étudiants", liste)

# --- Fonctions pour la gestion des notes ---

def ajouter_note_gui():
    """Ajoute une note pour un étudiant et une matière donnée"""
    identifiant = simpledialog.askstring("ID Étudiant", "ID de l'étudiant :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return
    matiere = simpledialog.askstring("Matière", "Nom de la matière :")
    try:
        note = float(simpledialog.askstring("Note", "Note (0-20) :"))
        if not 0 <= note <= 20:
            raise ValueError
    except:
        messagebox.showerror("Erreur", "Note invalide.")
        return
    if matiere not in notes[identifiant]:
        notes[identifiant][matiere] = []
    notes[identifiant][matiere].append(note)
    messagebox.showinfo("Succès", "Note ajoutée.")

def supprimer_note_gui():
    """Supprime la dernière note ajoutée d'une matière"""
    identifiant = simpledialog.askstring("ID Étudiant", "ID de l'étudiant :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return
    matiere = simpledialog.askstring("Matière", "Nom de la matière :")
    if matiere not in notes.get(identifiant, {}):
        messagebox.showerror("Erreur", "Matière non trouvée.")
        return
    if not notes[identifiant][matiere]:
        messagebox.showerror("Erreur", "Aucune note à supprimer.")
        return
    note_supprimee = notes[identifiant][matiere].pop()
    messagebox.showinfo("Succès", f"Note {note_supprimee} supprimée de {matiere}.")

def afficher_notes_gui():
    """Affiche toutes les notes d'un étudiant"""
    identifiant = simpledialog.askstring("ID Étudiant", "ID de l'étudiant :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return
    if not notes.get(identifiant):
        messagebox.showinfo("Notes", "Aucune note enregistrée.")
        return
    texte = f"Notes pour {etudiants[identifiant][1]} {etudiants[identifiant][0]} (ID: {identifiant}) :\n\n"
    for matiere, liste_notes in notes[identifiant].items():
        texte += f"{matiere} : {liste_notes}\n"
    messagebox.showinfo("Notes", texte)

# --- Fonctions pour calculs et bulletin ---

def moyenne_matiere(identifiant, matiere):
    """Calcule la moyenne d'une matière pour un étudiant"""
    if identifiant not in notes or matiere not in notes[identifiant]:
        return None
    return sum(notes[identifiant][matiere]) / len(notes[identifiant][matiere])

def moyenne_generale(identifiant):
    """Calcule la moyenne générale d'un étudiant"""
    if identifiant not in notes or not notes[identifiant]:
        return None
    total, nb = 0, 0
    for matiere in notes[identifiant]:
        total += sum(notes[identifiant][matiere])
        nb += len(notes[identifiant][matiere])
    return total / nb if nb > 0 else None

def afficher_bulletin_gui():
    """Affiche le bulletin complet d'un étudiant avec moyennes"""
    identifiant = simpledialog.askstring("ID Étudiant", "ID de l'étudiant :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return
    nom, prenom = etudiants[identifiant]
    bulletin = f"Bulletin de {prenom} {nom} (ID: {identifiant})\n\n"
    if not notes[identifiant]:
        bulletin += "Aucune note enregistrée."
    else:
        for matiere, liste_notes in notes[identifiant].items():
            moy = moyenne_matiere(identifiant, matiere)
            bulletin += f"{matiere} : {liste_notes} | Moyenne = {moy:.2f}\n"
        moy_gen = moyenne_generale(identifiant)
        bulletin += f"\nMoyenne générale : {moy_gen:.2f}"
    messagebox.showinfo("Bulletin", bulletin)

# --- Classement des étudiants par moyenne ---

def classement_etudiants_gui():
    """Affiche le classement des étudiants selon leur moyenne générale"""
    lignes = []
    for identifiant in etudiants:
        moy = moyenne_generale(identifiant)
        if moy is not None:
            lignes.append((moy, identifiant))
    if not lignes:
        messagebox.showinfo("Classement", "Aucune donnée disponible.")
        return
    lignes.sort(reverse=True)  # Tri décroissant
    classement = ""
    for i, (moy, identifiant) in enumerate(lignes, start=1):
        nom, prenom = etudiants[identifiant]
        classement += f"{i}. {prenom} {nom} (ID: {identifiant}) - Moyenne : {moy:.2f}\n"
    messagebox.showinfo("Classement", classement)

# --- Interface graphique principale ---

def lancer_interface_graphique():
    """Lance la fenêtre principale avec les boutons"""
    charger_donnees()
    fenetre = tk.Tk()
    fenetre.title("Gestion des Notes Étudiants")

    # Création des boutons et leurs actions
    tk.Button(fenetre, text="Ajouter un étudiant", width=30, command=ajouter_etudiant_gui).pack(pady=5)
    tk.Button(fenetre, text="Supprimer un étudiant", width=30, command=supprimer_etudiant_gui).pack(pady=5)
    tk.Button(fenetre, text="Afficher la liste des étudiants", width=30, command=afficher_etudiants_gui).pack(pady=5)

    tk.Button(fenetre, text="Ajouter une note", width=30, command=ajouter_note_gui).pack(pady=5)
    tk.Button(fenetre, text="Supprimer une note", width=30, command=supprimer_note_gui).pack(pady=5)
    tk.Button(fenetre, text="Afficher les notes d'un étudiant", width=30, command=afficher_notes_gui).pack(pady=5)

    tk.Button(fenetre, text="Afficher le bulletin", width=30, command=afficher_bulletin_gui).pack(pady=5)
    tk.Button(fenetre, text="Classement des étudiants", width=30, command=classement_etudiants_gui).pack(pady=5)

    tk.Button(fenetre, text="Sauvegarder", width=30, command=lambda: (sauvegarder_donnees(), messagebox.showinfo("Info", "Données sauvegardées."))).pack(pady=5)

    # Boucle principale de l'application
    fenetre.mainloop()

# --- Lancement de l'application ---
if __name__ == "__main__":
    lancer_interface_graphique()
