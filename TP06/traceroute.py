import argparse
import subprocess
import sys
import threading
import queue
import time

def executer_traceroute(destination, mode_progressif=False, fichier_sortie=None, timeout=30):
    """
    Exécute la commande tracert vers une destination donnée.
    
    Args:
        destination (str): URL ou adresse IP de destination
        mode_progressif (bool): Affichage progressif des résultats
        fichier_sortie (str, optional): Chemin du fichier de sortie
        timeout (int): Temps maximum d'attente en secondes
    """
    # Commande tracert pour Windows
    commande = ["tracert", "-h", "30", destination]  # Limite de 30 sauts
    
    try:
        # Mode progressif amélioré avec gestion de file d'attente et timeout
        if mode_progressif:
            # File d'attente pour stocker la sortie
            output_queue = queue.Queue()
            
            # Fonction pour lire la sortie
            def lire_sortie(processus, queue_obj):
                try:
                    for ligne in iter(processus.stdout.readline, ''):
                        ligne = ligne.rstrip()
                        queue_obj.put(ligne)
                except Exception:
                    pass
                finally:
                    processus.stdout.close()
                    queue_obj.put(None)  # Signal de fin
            
            # Préparation du fichier de sortie si spécifié
            fichier = None
            if fichier_sortie:
                try:
                    fichier = open(fichier_sortie, 'w', encoding='utf-8')
                except IOError as erreur_fichier:
                    print(f"Erreur d'ouverture du fichier : {erreur_fichier}", file=sys.stderr)
                    return
            
            # Lancement du processus
            processus = subprocess.Popen(
                commande, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                universal_newlines=True
            )
            
            # Lancement du thread de lecture
            thread_lecture = threading.Thread(target=lire_sortie, args=(processus, output_queue))
            thread_lecture.daemon = True
            thread_lecture.start()
            
            # Gestion du timeout et de l'affichage
            debut = time.time()
            ligne_recue = False
            while True:
                try:
                    # Attente avec timeout
                    ligne = output_queue.get(timeout=1)
                    
                    # Fin de la lecture
                    if ligne is None:
                        break
                    
                    # Affichage et écriture
                    print(ligne)
                    ligne_recue = True
                    if fichier:
                        fichier.write(ligne + '\n')
                    
                    # Réinitialiser le temps si une ligne est reçue
                    debut = time.time()
                
                except queue.Empty:
                    # Vérifier le timeout
                    if not ligne_recue and time.time() - debut > timeout:
                        print(f"\nAucune réponse après {timeout} secondes. Arrêt du tracert.", file=sys.stderr)
                        processus.terminate()
                        break
                    
                    # Vérifier si le processus est toujours actif
                    if processus.poll() is not None:
                        break
            
            # Nettoyage
            if fichier:
                fichier.close()
            processus.wait()
        
        # Mode standard avec timeout
        else:
            # Exécution du tracert avec timeout
            try:
                resultat = subprocess.run(
                    commande, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True,
                    check=True,
                    timeout=timeout
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
            
            except subprocess.TimeoutExpired:
                print(f"\nLe tracert a dépassé le temps limite de {timeout} secondes.", file=sys.stderr)
    
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
    
    # Option de timeout personnalisé
    parseur.add_argument(
        "-t", "--timeout", 
        type=int, 
        default=30, 
        help="Temps maximum d'attente en secondes (défaut: 30)"
    )
    
    # Récupération des arguments
    args = parseur.parse_args()
    
    try:
        # Exécution du tracert avec les arguments fournis
        executer_traceroute(
            args.destination, 
            mode_progressif=args.progressive, 
            fichier_sortie=args.output_file,
            timeout=args.timeout
        )
    except KeyboardInterrupt:
        print("\nOpération interrompue par l'utilisateur.", file=sys.stderr)
        sys.exit(1)
    except Exception as erreur:
        print(f"Erreur lors de l'exécution : {erreur}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()