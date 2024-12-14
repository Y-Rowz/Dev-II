#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de traceroute pour Windows avec options de progression et de sortie fichier.

Ce script permet de tracer la route réseau entre votre machine 
et une destination spécifiée, avec des options flexibles.
"""

import argparse
import subprocess
import sys
import os

def executer_traceroute(destination, mode_progressif=False, fichier_sortie=None):
    """
    Exécute la commande tracert vers une destination donnée.
    
    Args:
        destination (str): URL ou adresse IP de destination
        mode_progressif (bool): Affichage progressif des résultats
        fichier_sortie (str, optional): Chemin du fichier de sortie
    """
    # Commande tracert pour Windows
    commande = ["tracert", destination]
    
    try:
        # Mode progressif utilisant Popen
        if mode_progressif:
            # Ouverture du processus
            processus = subprocess.Popen(
                commande, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                universal_newlines=True
            )
            
            # Préparation du fichier de sortie si spécifié
            fichier = None
            if fichier_sortie:
                try:
                    fichier = open(fichier_sortie, 'w', encoding='utf-8')
                except IOError as erreur_fichier:
                    print(f"Erreur d'ouverture du fichier : {erreur_fichier}", file=sys.stderr)
                    return
            
            # Lecture et affichage progressif des résultats
            try:
                for ligne in iter(processus.stdout.readline, ''):
                    ligne = ligne.rstrip()
                    print(ligne)
                    if fichier:
                        fichier.write(ligne + '\n')
            except Exception as erreur_lecture:
                print(f"Erreur lors de la lecture : {erreur_lecture}", file=sys.stderr)
            finally:
                # Fermeture propre des ressources
                processus.stdout.close()
                if fichier:
                    fichier.close()
        
        # Mode standard utilisant run()
        else:
            # Exécution du tracert
            resultat = subprocess.run(
                commande, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                check=True
            )
            
            # Gestion de la sortie
            if fichier_sortie:
                try:
                    with open(fichier_sortie, 'w', encoding='utf-8') as fichier:
                        fichier.write(resultat.stdout)
                except IOError as erreur_fichier:
                    print(f"Erreur d'écriture dans le fichier : {erreur_fichier}", file=sys.stderr)
            else:
                print(resultat.stdout)
    
    except subprocess.CalledProcessError as erreur_subprocess:
        print(f"Erreur lors de l'exécution de tracert : {erreur_subprocess}", file=sys.stderr)
        print(f"Erreur détaillée : {erreur_subprocess.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print("La commande tracert n'est pas disponible. Vérifiez votre installation Windows.", file=sys.stderr)
    except PermissionError:
        print("Permission refusée pour exécuter tracert ou écrire dans le fichier.", file=sys.stderr)
    except Exception as erreur:
        print(f"Une erreur inattendue s'est produite : {erreur}", file=sys.stderr)

def main():
    """
    Fonction principale pour parser les arguments et lancer le traceroute.
    """
    # Configuration de l'analyseur d'arguments
    parseur = argparse.ArgumentParser(
        description="Script de tracert réseau pour Windows avec options avancées."
    )
    
    # Argument de destination (obligatoire)
    parseur.add_argument(
        "destination", 
        help="URL ou adresse IP de destination pour le tracert"
    )
    
    # Option de mode progressif
    parseur.add_argument(
        "-p", "--progressive", 
        action="store_true", 
        help="Afficher les résultats au fur et à mesure"
    )
    
    # Option de fichier de sortie
    parseur.add_argument(
        "-o", "--output-file", 
        help="Fichier de sortie pour enregistrer les résultats"
    )
    
    # Récupération des arguments
    args = parseur.parse_args()
    
    try:
        # Exécution du tracert avec les arguments fournis
        executer_traceroute(
            args.destination, 
            mode_progressif=args.progressive, 
            fichier_sortie=args.output_file
        )
    except KeyboardInterrupt:
        print("\nOpération interrompue par l'utilisateur.", file=sys.stderr)
        sys.exit(1)
    except Exception as erreur:
        print(f"Erreur lors de l'exécution : {erreur}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()