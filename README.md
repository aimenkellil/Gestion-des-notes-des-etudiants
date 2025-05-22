# Gestion des notes des etudiants
Ce projet a pour but de développer une application Python permettant de gérer des étudiants et leurs notes, 
avec une interface graphique utilisant **Tkinter**. L'application permet d'ajouter, supprimer, modifier et afficher des étudiants et leurs notes, 
ainsi que de faire des analyses telles que le calcul de moyennes, la génération de bulletins et le classement général.


---

## Structure du projet
```
Gestion-des-notes-des-etudiants/
├── .idea/                    # Configuration de l'IDE (VS Code, PyCharm, etc.)
├── etudiants.json            # Données des étudiants (ID, nom, etc.)
├── notes.json                # Notes des étudiants par matière
├── main.py                   # Fichier principal pour exécuter l'application
├── README.md                 # Documentation du projet

```

## Fonctionnalités

### Gestion des étudiants
- Ajouter un nouvel étudiant
- Supprimer un étudiant existant
- Afficher la liste des étudiants

### Gestion des notes
- Ajouter une note à un étudiant
- Supprimer une note
- Afficher les notes par étudiant ou par matière

### Analyse des notes
- Calcul de la moyenne d’un étudiant
- Génération du bulletin
- Classement général de la classe

---

## Lancement de l'application

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/Tp1_gestion_notes.git
```


### 2. Lancer l'application
```bash
python main.py
```


**Exemple de données**

```bash
etudiants.json :
[
  {
    "id": "1",
    "nom": "Dupont",
    "prenom": "Jean"
  }
]
notes.json :

[
  {
    "id_etudiant": "1",
    "matiere": "Math",
    "note": 18
  }
]
```

### Technologies utilisées
```bash
Python 3.13
```
```bash
JSON (stockage des données)
```




# Auteurs
### Groupe 1-Npower-2025
### Groupe 2-Npower-2025
### Groupe 3-Npower-2025


Ce projet a été réalisé dans le cadre du cours AD à Npower.
