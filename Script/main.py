import os
import pandas as pd
from src.rapport import generer_statistiques, generer_graphique, generer_rapport_pdf, ajouter_extension_si_absente
from src.rechercher import rechercher_produit
from src.importer import importer_csv

def afficher_menu():
    print("""
    ==== Gestion des Stocks ====
    1. Charger et combiner les fichiers CSV
    2. Effectuer une recherche de produit
    3. Créer un rapport complet
    4. Quitter le programme
    """)

def main():
    df = None

    while True:
        afficher_menu()
        choix = input("Faites votre choix : ")

        if choix == "1":
            dossier = "./data"
            if os.path.isdir(dossier):
                df = importer_csv(dossier)
                print("Les fichiers CSV ont été chargés et fusionnés avec succès.")
                print("Colonnes disponibles dans le tableau :", df.columns)
            else:
                print("Le dossier spécifié est introuvable.")
        elif choix == "2":
            if df is not None:
                nom = input("Saisissez le nom du produit : ")
                categorie = input("Saisissez la catégorie : ")
                prix_min_input = input("Prix minimum souhaité (laisser vide si non applicable) : ")
                prix_min = float(prix_min_input) if prix_min_input else None
                
                prix_max_input = input("Prix maximum souhaité (laisser vide si non applicable) : ")
                prix_max = float(prix_max_input) if prix_max_input else None
                resultats = rechercher_produit(df, nom, categorie, prix_min, prix_max)
                print("Résultats de la recherche :")
                print(resultats)
            else:
                print("Veuillez d'abord charger les fichiers CSV.")
        elif choix == "3":
            if df is not None:
                chemin_graphique = input("Nom du fichier pour sauvegarder le graphique (sans extension) : ")
                chemin_graphique = ajouter_extension_si_absente(chemin_graphique, ".png")
                try:
                    generer_graphique(df, chemin_graphique)
                except ValueError as e:
                    print(f"Erreur : {e}")
                    continue
                
                chemin_pdf = input("Nom du fichier pour sauvegarder le rapport PDF (sans extension) : ")
                chemin_pdf = ajouter_extension_si_absente(chemin_pdf, ".pdf")
                try:
                    generer_rapport_pdf(df, chemin_pdf, chemin_graphique)
                    print(f"Le rapport PDF a été créé avec succès : {os.path.abspath(chemin_pdf)}")
                except FileNotFoundError as e:
                    print(f"Erreur : {e}")
            else:
                print("Aucun fichier CSV n'a encore été importé.")
        elif choix == "4":
            print("Programme stoppé.")
            break
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()