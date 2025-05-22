import tkinter as tk
from tkinter import ttk, messagebox
from functions.gestion_etudiants import ajouter_etudiant, supprimer_etudiant, afficher_etudiants
from functions.gestion_notes import ajouter_note, supprimer_note, afficher_notes
from functions.analyse_notes import calculer_moyenne_matiere, calculer_moyenne_generale, afficher_bulletin, trier_etudiants_par_moyenne
import sys
from io import StringIO

class GestionEtudiantsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion des Étudiants et Notes")
        self.root.geometry("1200x800")
        self.root.configure(bg="#E8ECEF")  # Soft gray background

        # Configurer le style moderne avec palette Contemplative Tech
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Arial", 12), foreground="#2E3A46")
        self.style.configure("TEntry", font=("Arial", 12), padding=5)
        self.style.configure("TFrame", background="#D3D8DC")

        # Styles des boutons avec palette Contemplative Tech
        self.style.configure("Ajouter.TButton", font=("Arial", 12, "bold"), padding=8, background="#26A69A", foreground="white")
        self.style.map("Ajouter.TButton", background=[("active", "#1E7E6D")], foreground=[("active", "#FFFFFF")])
        self.style.configure("Supprimer.TButton", font=("Arial", 12, "bold"), padding=8, background="#EF5350", foreground="white")
        self.style.map("Supprimer.TButton", background=[("active", "#D32F2F")], foreground=[("active", "#FFFFFF")])
        self.style.configure("Afficher.TButton", font=("Arial", 12, "bold"), padding=8, background="#1976D2", foreground="white")
        self.style.map("Afficher.TButton", background=[("active", "#155FA0")], foreground=[("active", "#FFFFFF")])
        self.style.configure("Calculer.TButton", font=("Arial", 12, "bold"), padding=8, background="#66BB6A", foreground="white")
        self.style.map("Calculer.TButton", background=[("active", "#43A047")], foreground=[("active", "#FFFFFF")])
        self.style.configure("Trier.TButton", font=("Arial", 12, "bold"), padding=8, background="#AB47BC", foreground="white")
        self.style.map("Trier.TButton", background=[("active", "#8E24AA")], foreground=[("active", "#FFFFFF")])

        # Style pour la table
        self.style.configure("Treeview", font=("Arial", 11), rowheight=30, background="#D3D8DC", fieldbackground="#D3D8DC", foreground="#2E3A46")
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#1976D2", foreground="white")
        self.style.map("Treeview", background=[("selected", "#B0C4DE")])

        # Cadre principal avec disposition horizontale
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Cadre Kanban (70% de la fenêtre)
        self.kanban_frame = ttk.Frame(self.main_frame, width=800, style="TFrame")
        self.kanban_frame.pack(side="left", fill="both", expand=False)

        # Créer les colonnes du Kanban et le cadre pour les opérations
        self.create_kanban_columns()

        # Cadre pour les opérations (en dessous des colonnes Kanban)
        self.operation_frame = ttk.Frame(self.kanban_frame, style="TFrame")
        self.operation_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Cadre pour les entrées (à droite, 30% de la fenêtre)
        self.input_frame = ttk.Frame(self.main_frame, width=400, style="TFrame")
        self.input_frame.pack(side="right", fill="y", padx=(10, 0))
        self.create_input_fields()

        # Cadre pour les résultats (tableau en bas, agrandi)
        self.result_frame = ttk.Frame(self.root, style="TFrame")
        self.result_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.create_result_table()

        # Cadre pour afficher les interfaces dynamiquement
        self.current_operation_frame = None

    def create_input_fields(self):
        input_label = ttk.Label(self.input_frame, text="Entrées", font=("Arial", 14, "bold"), foreground="#1976D2")
        input_label.pack(pady=10)

        ttk.Label(self.input_frame, text="ID Étudiant:").pack(anchor="w", padx=10, pady=5)
        self.id_entry = ttk.Entry(self.input_frame)
        self.id_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.input_frame, text="Nom:").pack(anchor="w", padx=10, pady=5)
        self.nom_entry = ttk.Entry(self.input_frame)
        self.nom_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.input_frame, text="Prénom:").pack(anchor="w", padx=10, pady=5)
        self.prenom_entry = ttk.Entry(self.input_frame)
        self.prenom_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.input_frame, text="Matière:").pack(anchor="w", padx=10, pady=5)
        self.matiere_entry = ttk.Entry(self.input_frame)
        self.matiere_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.input_frame, text="Note (0-20):").pack(anchor="w", padx=10, pady=5)
        self.note_entry = ttk.Entry(self.input_frame)
        self.note_entry.pack(fill="x", padx=10, pady=5)

    def create_result_table(self):
        table_container = ttk.Frame(self.result_frame)
        table_container.pack(fill="both", expand=True)

        columns = ("Operation", "Details", "Status")
        self.result_table = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        self.result_table.heading("Operation", text="Opération")
        self.result_table.heading("Details", text="Détails")
        self.result_table.heading("Status", text="Statut")
        self.result_table.column("Operation", width=250, anchor="center")
        self.result_table.column("Details", width=650, anchor="w")
        self.result_table.column("Status", width=200, anchor="center")

        scrollbar_y = ttk.Scrollbar(table_container, orient="vertical", command=self.result_table.yview)
        self.result_table.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.result_table.xview)
        self.result_table.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")

        self.result_table.pack(fill="both", expand=True, padx=5, pady=5)

    def create_kanban_columns(self):
        kanban_container = ttk.Frame(self.kanban_frame, style="TFrame")
        kanban_container.pack(fill="both", expand=False, padx=10, pady=10)

        # Colonne 1 : Gestion des Étudiants
        col1_frame = ttk.Frame(kanban_container, style="TFrame", borderwidth=2, relief="groove")
        col1_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)
        ttk.Label(col1_frame, text="Gestion des Étudiants", font=("Arial", 12, "bold"), foreground="#1976D2").pack(pady=5)
        ttk.Button(col1_frame, text="Ajouter Étudiant", style="Ajouter.TButton", command=self.show_ajouter_etudiant).pack(fill="x", pady=5)
        ttk.Button(col1_frame, text="Supprimer Étudiant", style="Supprimer.TButton", command=self.show_supprimer_etudiant).pack(fill="x", pady=5)
        ttk.Button(col1_frame, text="Afficher Étudiants", style="Afficher.TButton", command=self.show_afficher_etudiants).pack(fill="x", pady=5)

        # Colonne 2 : Gestion des Notes
        col2_frame = ttk.Frame(kanban_container, style="TFrame", borderwidth=2, relief="groove")
        col2_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(col2_frame, text="Gestion des Notes", font=("Arial", 12, "bold"), foreground="#1976D2").pack(pady=5)
        ttk.Button(col2_frame, text="Ajouter Note", style="Ajouter.TButton", command=self.show_ajouter_note).pack(fill="x", pady=5)
        ttk.Button(col2_frame, text="Supprimer Note", style="Supprimer.TButton", command=self.show_supprimer_note).pack(fill="x", pady=5)
        ttk.Button(col2_frame, text="Afficher Notes", style="Afficher.TButton", command=self.show_afficher_notes).pack(fill="x", pady=5)

        # Colonne 3 : Analyse et Visualisation
        col3_frame = ttk.Frame(kanban_container, style="TFrame", borderwidth=2, relief="groove")
        col3_frame.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        ttk.Label(col3_frame, text="Analyse et Visualisation", font=("Arial", 12, "bold"), foreground="#1976D2").pack(pady=5)
        ttk.Button(col3_frame, text="Moyenne Matière", style="Calculer.TButton", command=self.show_moyenne_matiere).pack(fill="x", pady=5)
        ttk.Button(col3_frame, text="Moyenne Générale", style="Calculer.TButton", command=self.show_moyenne_generale).pack(fill="x", pady=5)
        ttk.Button(col3_frame, text="Bulletin Complet", style="Afficher.TButton", command=self.show_bulletin).pack(fill="x", pady=5)
        ttk.Button(col3_frame, text="Trier par Moyenne", style="Trier.TButton", command=self.show_trier_moyenne).pack(fill="x", pady=5)

    def clear_operation_frame(self):
        if self.current_operation_frame:
            self.current_operation_frame.destroy()
        self.current_operation_frame = ttk.Frame(self.operation_frame, style="TFrame")
        self.current_operation_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_table(self):
        for item in self.result_table.get_children():
            self.result_table.delete(item)

    def show_ajouter_etudiant(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Ajouter", style="Ajouter.TButton", command=self.ajouter_etudiant_action).grid(row=0, column=0, pady=20)

    def ajouter_etudiant_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            nom = self.nom_entry.get()
            prenom = self.prenom_entry.get()
            if not nom or not prenom:
                messagebox.showerror("Erreur", "Le nom et le prénom ne peuvent pas être vides.")
                return
            stdout = sys.stdout
            sys.stdout = StringIO()
            ajouter_etudiant(id_etudiant, nom, prenom)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            self.clear_table()
            self.result_table.insert("", "end", values=("Ajouter Étudiant", output.strip(), "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Ajouter Étudiant", "L'ID doit être un nombre.", "Erreur"))

    def show_supprimer_etudiant(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Supprimer", style="Supprimer.TButton", command=self.supprimer_etudiant_action).grid(row=0, column=0, pady=20)

    def supprimer_etudiant_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            stdout = sys.stdout
            sys.stdout = StringIO()
            supprimer_etudiant(id_etudiant)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            self.clear_table()
            self.result_table.insert("", "end", values=("Supprimer Étudiant", output.strip(), "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Supprimer Étudiant", "L'ID doit être un nombre.", "Erreur"))

    def show_afficher_etudiants(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Afficher", style="Afficher.TButton", command=self.afficher_etudiants_action).grid(row=0, column=0, pady=20)

    def afficher_etudiants_action(self):
        stdout = sys.stdout
        sys.stdout = StringIO()
        afficher_etudiants()
        output = sys.stdout.getvalue()
        sys.stdout = stdout
        self.clear_table()
        self.result_table.insert("", "end", values=("Afficher Étudiants", output.strip(), "Succès"))

    def show_ajouter_note(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Ajouter", style="Ajouter.TButton", command=self.ajouter_note_action).grid(row=0, column=0, pady=20)

    def ajouter_note_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            matiere = self.matiere_entry.get()
            note = float(self.note_entry.get())
            if not matiere:
                messagebox.showerror("Erreur", "La matière ne peut pas être vide.")
                return
            stdout = sys.stdout
            sys.stdout = StringIO()
            ajouter_note(id_etudiant, matiere, note)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            self.clear_table()
            self.result_table.insert("", "end", values=("Ajouter Note", output.strip(), "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Ajouter Note", "L'ID et la note doivent être des nombres.", "Erreur"))

    def show_supprimer_note(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Supprimer", style="Supprimer.TButton", command=self.supprimer_note_action).grid(row=0, column=0, pady=20)

    def supprimer_note_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            matiere = self.matiere_entry.get()
            note = float(self.note_entry.get())
            if not matiere:
                messagebox.showerror("Erreur", "La matière ne peut pas être vide.")
                return
            stdout = sys.stdout
            sys.stdout = StringIO()
            supprimer_note(id_etudiant, matiere, note)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            self.clear_table()
            self.result_table.insert("", "end", values=("Supprimer Note", output.strip(), "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Supprimer Note", "L'ID et la note doivent être des nombres.", "Erreur"))

    def show_afficher_notes(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Afficher", style="Afficher.TButton", command=self.afficher_notes_action).grid(row=0, column=0, pady=20)

    def afficher_notes_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            stdout = sys.stdout
            sys.stdout = StringIO()
            afficher_notes(id_etudiant)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            self.clear_table()
            self.result_table.insert("", "end", values=("Afficher Notes", output.strip(), "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Afficher Notes", "L'ID doit être un nombre.", "Erreur"))

    def show_moyenne_matiere(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Calculer", style="Calculer.TButton", command=self.moyenne_matiere_action).grid(row=0, column=0, pady=20)

    def moyenne_matiere_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            matiere = self.matiere_entry.get()
            if not matiere:
                messagebox.showerror("Erreur", "La matière ne peut pas être vide.")
                return
            moyenne = calculer_moyenne_matiere(id_etudiant, matiere)
            self.clear_table()
            self.result_table.insert("", "end", values=("Moyenne Matière", f"Moyenne en {matiere} : {moyenne:.2f}", "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Moyenne Matière", "L'ID doit être un nombre.", "Erreur"))

    def show_moyenne_generale(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Calculer", style="Calculer.TButton", command=self.moyenne_generale_action).grid(row=0, column=0, pady=20)

    def moyenne_generale_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            moyenne = calculer_moyenne_generale(id_etudiant)
            self.clear_table()
            self.result_table.insert("", "end", values=("Moyenne Générale", f"Moyenne générale : {moyenne:.2f}", "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Moyenne Générale", "L'ID doit être un nombre.", "Erreur"))

    def show_bulletin(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Afficher", style="Afficher.TButton", command=self.bulletin_action).grid(row=0, column=0, pady=20)

    def bulletin_action(self):
        try:
            id_etudiant = int(self.id_entry.get())
            stdout = sys.stdout
            sys.stdout = StringIO()
            afficher_bulletin(id_etudiant)
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            self.clear_table()
            self.result_table.insert("", "end", values=("Bulletin Complet", output.strip(), "Succès"))
        except ValueError:
            self.clear_table()
            self.result_table.insert("", "end", values=("Bulletin Complet", "L'ID doit être un nombre.", "Erreur"))

    def show_trier_moyenne(self):
        self.clear_operation_frame()
        self.current_operation_frame.configure(style="TFrame", borderwidth=2, relief="groove")
        ttk.Button(self.current_operation_frame, text="Trier", style="Trier.TButton", command=self.trier_moyenne_action).grid(row=0, column=0, pady=20)

    def trier_moyenne_action(self):
        stdout = sys.stdout
        sys.stdout = StringIO()
        trier_etudiants_par_moyenne()
        output = sys.stdout.getvalue()
        sys.stdout = stdout
        self.clear_table()
        self.result_table.insert("", "end", values=("Trier par Moyenne", output.strip(), "Succès"))

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionEtudiantsApp(root)
    root.mainloop()