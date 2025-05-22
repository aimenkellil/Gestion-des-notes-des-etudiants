# Importation des fonctions nécessaires depuis les modules
from functions.gestion_etudiants import ajouter_etudiant, supprimer_etudiant, afficher_etudiants  # Fonctions pour gérer les étudiants
from functions.gestion_notes import ajouter_note, supprimer_note, afficher_notes  # Fonctions pour gérer les notes
from functions.analyse_notes import calculer_moyenne_matiere, calculer_moyenne_generale, afficher_bulletin, trier_etudiants_par_moyenne  # Fonctions pour analyser les notes

# Fonction pour afficher le menu interactif
def afficher_menu():
    print("\n=== Système de Gestion des Étudiants et Notes ===")  # Afficher l'en-tête du menu
    print("1. Ajouter un étudiant")  # Option 1
    print("2. Supprimer un étudiant")  # Option 2
    print("3. Afficher tous les étudiants")  # Option 3
    print("4. Ajouter une note")  # Option 4
    print("5. Supprimer une note")  # Option 5
    print("6. Afficher les notes d'un étudiant")  # Option 6
    print("7. Calculer la moyenne d'une matière")  # Option 7
    print("8. Calculer la moyenne générale")  # Option 8
    print("9. Afficher le bulletin complet")  # Option 9
    print("10. Trier les étudiants par moyenne générale")  # Option 10
    print("11. Quitter")  # Option 11
    return input("Choisissez une option (1-11) : ")  # Demander à l'utilisateur de choisir une option

# Fonction principale pour exécuter le programme
def main():
    while True:  # Boucle infinie pour afficher le menu jusqu'à ce que l'utilisateur quitte
        choix = afficher_menu()  # Afficher le menu et récupérer le choix de l'utilisateur

        # Option 1 : Ajouter un étudiant
        if choix == "1":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant : "))  # Demander l'ID de l'étudiant
                nom = input("Entrez le nom : ")  # Demander le nom
                prenom = input("Entrez le prénom : ")  # Demander le prénom
                ajouter_etudiant(id_etudiant, nom, prenom)  # Appeler la fonction pour ajouter l'étudiant
            except ValueError:
                print("Erreur : L'ID doit être un nombre.")  # Gérer les erreurs si l'ID n'est pas un nombre

        # Option 2 : Supprimer un étudiant
        elif choix == "2":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant à supprimer : "))  # Demander l'ID de l'étudiant à supprimer
                supprimer_etudiant(id_etudiant)  # Appeler la fonction pour supprimer l'étudiant
            except ValueError:
                print("Erreur : L'ID doit être un nombre.")  # Gérer les erreurs si l'ID n'est pas un nombre

        # Option 3 : Afficher tous les étudiants
        elif choix == "3":
            afficher_etudiants()  # Appeler la fonction pour afficher la liste des étudiants

        # Option 4 : Ajouter une note
        elif choix == "4":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant : "))  # Demander l'ID de l'étudiant
                matiere = input("Entrez la matière : ")  # Demander la matière
                note = float(input("Entrez la note (0-20) : "))  # Demander la note
                ajouter_note(id_etudiant, matiere, note)  # Appeler la fonction pour ajouter la note
            except ValueError:
                print("Erreur : Veuillez entrer des valeurs valides (ID et note doivent être des nombres).")  # Gérer les erreurs si les entrées ne sont pas valides

        # Option 5 : Supprimer une note
        elif choix == "5":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant : "))  # Demander l'ID de l'étudiant
                matiere = input("Entrez la matière : ")  # Demander la matière
                note = float(input("Entrez la note à supprimer : "))  # Demander la note à supprimer
                supprimer_note(id_etudiant, matiere, note)  # Appeler la fonction pour supprimer la note
            except ValueError:
                print("Erreur : Veuillez entrer des valeurs valides (ID et note doivent être des nombres).")  # Gérer les erreurs si les entrées ne sont pas valides

        # Option 6 : Afficher les notes d'un étudiant
        elif choix == "6":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant : "))  # Demander l'ID de l'étudiant
                afficher_notes(id_etudiant)  # Appeler la fonction pour afficher les notes
            except ValueError:
                print("Erreur : L'ID doit être un nombre.")  # Gérer les erreurs si l'ID n'est pas un nombre

        # Option 7 : Calculer la moyenne d'une matière
        elif choix == "7":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant : "))  # Demander l'ID de l'étudiant
                matiere = input("Entrez la matière : ")  # Demander la matière
                moyenne = calculer_moyenne_matiere(id_etudiant, matiere)  # Calculer la moyenne pour la matière
                print(f"Moyenne en {matiere} : {moyenne:.2f}")  # Afficher la moyenne avec 2 décimales
            except ValueError:
                print("Erreur : L'ID doit être un nombre.")  # Gérer les erreurs si l'ID n'est pas un nombre

        # Option 8 : Calculer la moyenne générale
        elif choix == "8":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant : "))  # Demander l'ID de l'étudiant
                moyenne = calculer_moyenne_generale(id_etudiant)  # Calculer la moyenne générale
                print(f"Moyenne générale : {moyenne:.2f}")  # Afficher la moyenne avec 2 décimales
            except ValueError:
                print("Erreur : L'ID doit être un nombre.")  # Gérer les erreurs si l'ID n'est pas un nombre

        # Option 9 : Afficher le bulletin complet
        elif choix == "9":
            try:
                id_etudiant = int(input("Entrez l'ID de l'étudiant : "))  # Demander l'ID de l'étudiant
                afficher_bulletin(id_etudiant)  # Appeler la fonction pour afficher le bulletin
            except ValueError:
                print("Erreur : L'ID doit être un nombre.")  # Gérer les erreurs si l'ID n'est pas un nombre

        # Option 10 : Trier les étudiants par moyenne générale
        elif choix == "10":
            trier_etudiants_par_moyenne()  # Appeler la fonction pour trier et afficher les étudiants par moyenne

        # Option 11 : Quitter le programme
        elif choix == "11":
            print("Programme terminé.")  # Afficher un message de fin
            break  # Sortir de la boucle pour arrêter le programme

        # Gestion des options invalides
        else:
            print("Option invalide. Veuillez choisir une option entre 1 et 10.")  # Afficher un message si l'option n'est pas reconnue

# Point d'entrée du programme
if __name__ == "__main__":
    main()  # Lancer la fonction principale pour démarrer le programme