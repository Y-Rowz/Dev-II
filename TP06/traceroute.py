import argparse
import subprocess
import sys
import re
import threading
import queue
import time
import locale
from urllib.parse import urlparse

# Force l'encodage UTF-8 pour stdin, stdout et stderr
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def corriger_encodage(texte):
    """
    Corrige les problèmes d'encodage courants.
    
    PRE:
        texte (str): Texte à corriger
    
    POST:
        str: Texte corrigé
    """
    corrections = {
        '‚': 'é',
        'ÿ': '',
        'Š': 'è'
    }
    for ancien, nouveau in corrections.items():
        texte = texte.replace(ancien, nouveau)
    return texte

def nettoyer_destination(destination):
    """
    Extrait le nom de domaine ou l'adresse IP d'une URL complète.
    PRE:
        destination (str): URL ou adresse IP.
    POST:
        str: Domaine ou adresse IP utilisable pour le tracert.
    """
    try:
        parsed_url = urlparse(destination)
        if parsed_url.netloc:
            return parsed_url.netloc  # Retourne le domaine
        else:
            return destination  # Retourne l'entrée originale si ce n'est pas une URL
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}", file=sys.stderr)
        return destination  # Retourner l'entrée originale en cas d'échec

def extraire_ips(ligne):
    """
    Extrait les adresses IP d'une ligne de traceroute.
    
    PRE:
        ligne (str): Ligne de texte du traceroute
    
    POST:
        list: Liste des adresses IP trouvées dans la ligne
    """
    # Expression régulière pour trouver les adresses IPv4
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    return re.findall(ip_pattern, ligne)

def executer_traceroute(destination, mode_progressif=False, fichier_sortie=None, timeout=30):
    """
    Exécute la commande tracert vers une destination donnée et extrait les IPs.
    
    PRE:
        destination (str): URL ou adresse IP de destination
        mode_progressif (bool): Affichage progressif des résultats
        fichier_sortie (str, optional): Chemin du fichier de sortie
        timeout (int): Temps maximum d'attente en secondes
    """
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        except locale.Error:
            print("Impossible de configurer l'encodage localement.", file=sys.stderr)

    commande = ["tracert", "-h", "30", destination]
    
    try:
        if mode_progressif:
            output_queue = queue.Queue()
            ips_trouvees = set()
            
            def lire_sortie(processus, queue_obj):
                try:
                    for ligne in iter(processus.stdout.readline, ''):
                        ligne = corriger_encodage(ligne.rstrip())
                        queue_obj.put(ligne)
                except Exception as e:
                    print(f"Erreur de lecture : {e}", file=sys.stderr)
                finally:
                    processus.stdout.close()
                    queue_obj.put(None)
            
            fichier = None
            if fichier_sortie:
                try:
                    fichier = open(fichier_sortie, 'w', encoding='utf-8', errors='replace')
                except IOError as erreur_fichier:
                    print(f"Erreur d'ouverture du fichier : {erreur_fichier}", file=sys.stderr)
                    return
            
            processus = subprocess.Popen(
                commande, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                encoding='cp1252',
                errors='replace'
            )
            
            thread_lecture = threading.Thread(target=lire_sortie, args=(processus, output_queue))
            thread_lecture.daemon = True
            thread_lecture.start()
            
            debut = time.time()
            ligne_recue = False
            while True:
                try:
                    ligne = output_queue.get(timeout=1)
                    if ligne is None:
                        break
                    
                    # Extraire les IPs de la ligne
                    ips_ligne = extraire_ips(ligne)
                    for ip in ips_ligne:
                        if ip not in ips_trouvees:
                            ips_trouvees.add(ip)
                            print(ip)
                    
                    # Si fichier de sortie, on écrit toujours la ligne complète
                    if fichier:
                        fichier.write(ligne + '\n')
                    
                    ligne_recue = True
                    debut = time.time()
                except queue.Empty:
                    if not ligne_recue and time.time() - debut > timeout:
                        print(f"\nAucune réponse après {timeout} secondes. Arrêt du tracert.", file=sys.stderr)
                        processus.terminate()
                        break
                    if processus.poll() is not None:
                        break
            
            if fichier:
                fichier.close()
            processus.wait()
        else:
            try:
                resultat = subprocess.run(
                    commande, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True,
                    encoding='cp1252',
                    errors='replace',
                    check=True,
                    timeout=timeout
                )
                ips_trouvees = set()
                for ligne in resultat.stdout.split('\n'):
                    ips_ligne = extraire_ips(ligne)
                    for ip in ips_ligne:
                        if ip not in ips_trouvees:
                            ips_trouvees.add(ip)
                            print(ip)
                
                if fichier_sortie:
                    try:
                        with open(fichier_sortie, 'w', encoding='utf-8', errors='replace') as fichier:
                            fichier.write(resultat.stdout)
                    except IOError as erreur_fichier:
                        print(f"Erreur d'écriture dans le fichier : {erreur_fichier}", file=sys.stderr)
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
    parseur = argparse.ArgumentParser(
        description="Script de tracert réseau pour Windows avec extraction des IPs."
    )
    parseur.add_argument(
        "destination", 
        help="URL ou adresse IP de destination pour le tracert"
    )
    parseur.add_argument(
        "-p", "--progressive", 
        action="store_true", 
        help="Afficher les IPs au fur et à mesure"
    )
    parseur.add_argument(
        "-o", "--output-file", 
        help="Fichier de sortie pour enregistrer les résultats"
    )
    parseur.add_argument(
        "-t", "--timeout", 
        type=int, 
        default=30, 
        help="Temps maximum d'attente en secondes (défaut: 30)"
    )
    args = parseur.parse_args()
    
    destination_nettoyee = nettoyer_destination(args.destination)
    
    try:
        executer_traceroute(
            destination_nettoyee, 
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
