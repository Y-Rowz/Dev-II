import os
import pandas as pd
from src.rapport import generer_statistiques, generer_graphique, generer_rapport_pdf, ajouter_extension_si_absente
from src.rechercher import rechercher_produit
from src.importer import importer_csv

def afficher_menu():
    print("""
    ===== Menu Gestion d'Inventaire =====
    1. Importer et fusionner les fichiers CSV
    2. Rechercher un produit
    3. Générer un rapport
    4. Quitter
    """)

def main():
    df = None

    while True:
        afficher_menu()
        choix = input("Entrez votre choix : ")

        if choix == "1":
            dossier = "./data"
            if os.path.exists(dossier):
                df = importer_csv(dossier)
                print("Fichiers importés et fusionnés avec succès !")
                print("Colonnes du DataFrame:", df.columns)  # Debug print to check columns
            else:
                print("Le dossier spécifié n'existe pas.")
        elif choix == "2":
            if df is not None:
                nom = input("Entrez le nom du produit : ")
                categorie = input("Entrez la catégorie du produit : ")
                prix_min_input = input("Entrez le prix minimum : ")
                prix_min = float(prix_min_input) if prix_min_input else None
                
                prix_max_input = input("Entrez le prix maximum : ")
                prix_max = float(prix_max_input) if prix_max_input else None
                resultats = rechercher_produit(df, nom, categorie, prix_min, prix_max)
                print(resultats)
            else:
                print("Veuillez d'abord importer les fichiers CSV.")
        elif choix == "3":
            if df is not None:
                chemin_graphique = input("Entrez le nom du fichier pour sauvegarder le graphique (sans extension) : ")
                chemin_graphique = ajouter_extension_si_absente(chemin_graphique, ".png")
                try:
                    generer_graphique(df, chemin_graphique)
                except ValueError as e:
                    print(e)
                    continue
                
                chemin_pdf = input("Entrez le nom du fichier pour sauvegarder le rapport PDF (sans extension) : ")
                chemin_pdf = ajouter_extension_si_absente(chemin_pdf, ".pdf")
                try:
                    generer_rapport_pdf(df, chemin_pdf, chemin_graphique)
                    print(f"Rapport PDF généré : {os.path.abspath(chemin_pdf)}")
                except FileNotFoundError as e:
                    print(e)
            else:
                print("Veuillez d'abord importer les fichiers CSV.")
        elif choix == "4":
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()