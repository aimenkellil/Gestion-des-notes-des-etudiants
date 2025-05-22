import tkinter as tk
from tkinter import messagebox, simpledialog
import json

# --- Matières fixes ---
MATIERES = ["Mathematique", "Physique", "Informatique", "Francais", "Anglais"]

# Dictionnaires pour stocker les étudiants et leurs notes
etudiants = {}  # {id: (nom, prénom)}
notes = {}      # {id: {matière: [note1, note2, ...]}}



# --- Fonctions pour la gestion des étudiants ---

def ajouter_etudiant_gui():
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
        notes[identifiant] = {m: [] for m in MATIERES}
        messagebox.showinfo("Succès", f"Étudiant {prenom} {nom} ajouté.")
    else:
        messagebox.showerror("Erreur", "Champs incomplets.")

def supprimer_etudiant_gui():
    identifiant = simpledialog.askstring("ID Étudiant", "ID à supprimer :")
    if identifiant in etudiants:
        if messagebox.askyesno("Confirmation", f"Supprimer {etudiants[identifiant][1]} {etudiants[identifiant][0]} ?"):
            etudiants.pop(identifiant)
            notes.pop(identifiant, None)
            messagebox.showinfo("Succès", "Étudiant supprimé.")
    else:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")

def afficher_etudiants_gui():
    if not etudiants:
        messagebox.showinfo("Étudiants", "Aucun étudiant enregistré.")
        return
    liste = "\n".join([f"ID: {id} - {prenom} {nom}" for id, (nom, prenom) in etudiants.items()])
    messagebox.showinfo("Liste des étudiants", liste)

# --- Fonctions pour la gestion des notes ---

def ajouter_note_gui():
    identifiant = simpledialog.askstring("ID Étudiant", "ID de l'étudiant :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return

    matiere = choisir_matiere_gui()
    if not matiere:
        return

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
    messagebox.showinfo("Succès", f"Note ajoutée en {matiere}.")

def supprimer_note_gui():
    identifiant = simpledialog.askstring("ID Étudiant", "ID de l'étudiant :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return

    matiere = choisir_matiere_gui()
    if not matiere:
        return

    if matiere not in notes.get(identifiant, {}):
        messagebox.showerror("Erreur", "Matière non trouvée.")
        return
    if not notes[identifiant][matiere]:
        messagebox.showerror("Erreur", "Aucune note à supprimer.")
        return

    note_supprimee = notes[identifiant][matiere].pop()
    messagebox.showinfo("Succès", f"Note {note_supprimee} supprimée de {matiere}.")

def afficher_notes_gui():
    identifiant = simpledialog.askstring("ID Étudiant", "ID :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return
    texte = f"Notes de {etudiants[identifiant][1]} {etudiants[identifiant][0]} :\n"
    for matiere in MATIERES:
        texte += f"{matiere}: {notes[identifiant][matiere]}\n"
    messagebox.showinfo("Notes", texte)

# --- Fonctions pour les moyennes et le bulletin ---

def moyenne_matiere(identifiant, matiere):
    if notes[identifiant][matiere]:
        return sum(notes[identifiant][matiere]) / len(notes[identifiant][matiere])
    return None

def moyenne_generale(identifiant):
    total, count = 0, 0
    for matiere in MATIERES:
        n = notes[identifiant][matiere]
        total += sum(n)
        count += len(n)
    return total / count if count else None

def afficher_bulletin_gui():
    identifiant = simpledialog.askstring("ID Étudiant", "ID :")
    if identifiant not in etudiants:
        messagebox.showerror("Erreur", "Étudiant non trouvé.")
        return
    nom, prenom = etudiants[identifiant]
    texte = f"Bulletin de {prenom} {nom} (ID: {identifiant})\n\n"
    for matiere in MATIERES:
        moy = moyenne_matiere(identifiant, matiere)
        texte += f"{matiere}: {notes[identifiant][matiere]} | Moyenne: {moy:.2f}\n" if moy is not None else f"{matiere}: Aucune note\n"
    moy_gen = moyenne_generale(identifiant)
    if moy_gen is not None:
        texte += f"\nMoyenne générale : {moy_gen:.2f}"
    else:
        texte += "\nMoyenne générale : N/A"
    messagebox.showinfo("Bulletin", texte)

# --- Classement ---

def classement_etudiants_gui():
    lignes = [(moyenne_generale(id), id) for id in etudiants if moyenne_generale(id) is not None]
    if not lignes:
        messagebox.showinfo("Classement", "Aucune donnée disponible.")
        return
    lignes.sort(reverse=True)
    classement = "\n".join([f"{i+1}. {etudiants[id][1]} {etudiants[id][0]} - Moyenne: {moy:.2f}" for i, (moy, id) in enumerate(lignes)])
    messagebox.showinfo("Classement", classement)

# --- Interface graphique principale ---
def choisir_matiere_gui():
    """Fenêtre popup pour choisir une matière dans la liste"""
    popup = tk.Toplevel()
    popup.title("Choisir une matière")

    var = tk.StringVar(popup)
    var.set(MATIERES[0])  # Matière sélectionnée par défaut

    tk.Label(popup, text="Choisissez une matière :").pack(pady=5)
    option_menu = tk.OptionMenu(popup, var, *MATIERES)
    option_menu.pack(pady=5)

    result = {}

    def confirmer():
        result["matiere"] = var.get()
        popup.destroy()

    tk.Button(popup, text="Valider", command=confirmer).pack(pady=5)
    popup.wait_window()  # Attendre que l'utilisateur ferme la fenêtre
    return result.get("matiere")

# --- Fonctions pour charger et sauvegarder les données ---

def charger_donnees():
    global etudiants, notes
    try:
        with open("etudiants.json", "r") as f:
            etudiants.update(json.load(f))
        with open("notes.json", "r") as f:
            notes.update(json.load(f))
    except FileNotFoundError:
        pass

def sauvegarder_donnees():
    with open("etudiants.json", "w") as f:
        json.dump(etudiants, f, indent=4)
    with open("notes.json", "w") as f:
        json.dump(notes, f, indent=4)

def lancer_interface_graphique():
    charger_donnees()
    fenetre = tk.Tk()
    fenetre.title("Gestion des Notes Étudiants")

    tk.Button(fenetre, text="Ajouter un étudiant", width=30, command=ajouter_etudiant_gui).pack(pady=5)
    tk.Button(fenetre, text="Supprimer un étudiant", width=30, command=supprimer_etudiant_gui).pack(pady=5)
    tk.Button(fenetre, text="Afficher les étudiants", width=30, command=afficher_etudiants_gui).pack(pady=5)
    tk.Button(fenetre, text="Ajouter une note", width=30, command=ajouter_note_gui).pack(pady=5)
    tk.Button(fenetre, text="Supprimer une note", width=30, command=supprimer_note_gui).pack(pady=5)
    tk.Button(fenetre, text="Afficher les notes", width=30, command=afficher_notes_gui).pack(pady=5)
    tk.Button(fenetre, text="Afficher le bulletin", width=30, command=afficher_bulletin_gui).pack(pady=5)
    tk.Button(fenetre, text="Classement des étudiants", width=30, command=classement_etudiants_gui).pack(pady=5)
    tk.Button(fenetre, text="Sauvegarder et quitter", width=30, command=lambda: (sauvegarder_donnees(), fenetre.destroy())).pack(pady=10)

    fenetre.mainloop()

# Lancement
if __name__ == "__main__":
    lancer_interface_graphique()