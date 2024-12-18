import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF


def importer_csv(dossier):
    """
    Importe et fusionne tous les fichiers CSV d'un dossier.

    PRE:
        dossier (str): Le chemin du dossier contenant les fichiers CSV.

    POST:
        pd.DataFrame: Un DataFrame combinant tous les fichiers CSV.
    """
    all_files = [
        os.path.join(dossier, f) for f in os.listdir(dossier) if f.endswith('.csv')
    ]
    df_list = [pd.read_csv(file) for file in all_files]
    df = pd.concat(df_list, ignore_index=True)
    return df


def generer_statistiques(df: pd.DataFrame) -> dict:
    """
    Calcule les statistiques principales pour un DataFrame de données d'inventaire.

    PRE:
        df (pd.DataFrame): Le DataFrame contenant les données d'inventaire.

    POST:
        dict: Un dictionnaire contenant les statistiques (valeur totale, articles totaux).
    """
    valeur_totale = (df['Quantité'] * df['Prix Unitaire (€)']).sum()
    articles_totaux = df['Quantité'].sum()
    return {"Valeur Totale": valeur_totale, "Articles Totaux": articles_totaux}


def generer_graphique(df: pd.DataFrame, chemin: str) -> None:
    """
    Génère un graphique à barres de la quantité par catégorie et l'enregistre dans un fichier.

    PRE:
        df (pd.DataFrame): Le DataFrame contenant les données d'inventaire.
        chemin (str): Le chemin du fichier où sauvegarder le graphique (avec extension .png, .jpg ou .jpeg).

    Raises:
        ValueError: Si le chemin du fichier est vide ou n'a pas une extension valide.
    """
    if not chemin or chemin.strip() == '':
        raise ValueError(
            "Un nom de fichier est requis pour sauvegarder le graphique. "
            "Veuillez fournir un nom de fichier valide."
        )

    if not chemin.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError(
            f"Le chemin de l'image '{chemin}' doit avoir une extension valide "
            f"(.png, .jpg, .jpeg)"
        )

    stats = df.groupby('Catégorie')['Quantité'].sum()
    plt.figure(figsize=(10, 6))
    stats.plot(kind='bar', title='Quantité par Catégorie')
    plt.xlabel('Catégorie')
    plt.ylabel('Quantité')
    plt.tight_layout()
    plt.savefig(chemin)
    plt.close()


def generer_rapport_pdf(df: pd.DataFrame, chemin_pdf: str, chemin_graphique: str) -> None:
    """
    Génère un rapport PDF détaillé avec les statistiques et les données d'inventaire, ainsi qu'un graphique.

    PRE:
        df (pd.DataFrame): Le DataFrame contenant les données d'inventaire.
        chemin_pdf (str): Le chemin du fichier PDF où sauvegarder le rapport (avec extension .pdf).
        chemin_graphique (str): Le chemin du fichier contenant le graphique à inclure dans le rapport.

    Raises:
        FileNotFoundError: Si le fichier graphique spécifié n'existe pas.
    """
    if not os.path.exists(chemin_graphique):
        raise FileNotFoundError(
            f"Le fichier graphique spécifié '{chemin_graphique}' n'existe pas"
        )

    pdf = FPDF()
    pdf.add_page()

    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    pdf.cell(200, 10, txt="Rapport d'Inventaire", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Statistiques", ln=True)
    pdf.set_font('DejaVu', '', 10)
    stats = generer_statistiques(df)
    for k, v in stats.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True, border=1)
    pdf.ln(10)

    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Détails des articles", ln=True)
    pdf.set_font('DejaVu', '', 8)
    for _, row in df.iterrows():
        pdf.cell(
            200,
            10,
            txt=f"Article: {row['Nom']} | Catégorie: {row['Catégorie']} | "
                f"Quantité: {row['Quantité']} | Prix Unitaire (€): {row['Prix Unitaire (€)']}",
            ln=True,
            border=1,
        )
    pdf.ln(10)

    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Graphique", ln=True)
    pdf.image(chemin_graphique, x=10, y=pdf.get_y() + 10, w=190)

    pdf.output(chemin_pdf)


def rechercher_produit(df, nom, categorie, prix_min, prix_max):
    """
    Recherche des produits dans un DataFrame en fonction de différents critères.

    PRE:
        df (pd.DataFrame): Le DataFrame contenant les données d'inventaire.
        nom (str): Le nom du produit à rechercher.
        categorie (str): La catégorie du produit à rechercher.
        prix_min (float): Le prix minimum souhaité (None si non applicable).
        prix_max (float): Le prix maximum souhaité (None si non applicable).

    POST:
        pd.DataFrame: Un DataFrame contenant les résultats de la recherche.
    """
    masque = pd.Series([True] * len(df))

    if nom:
        masque &= df['Nom'].str.contains(nom, case=False)

    if categorie:
        masque &= df['Catégorie'].str.contains(categorie, case=False)

    if prix_min is not None:
        masque &= df['Prix Unitaire (€)'] >= prix_min

    if prix_max is not None:
        masque &= df['Prix Unitaire (€)'] <= prix_max

    return df[masque].sort_values('Quantité', ascending=False)

def ajouter_extension_si_absente(nom_fichier, extension):
    """
    Ajoute une extension à un nom de fichier si elle est absente.
    
    PRE:
        nom_fichier (str): Le nom du fichier.
        extension (str): L'extension à ajouter (avec le point, ex: ".png").
    
    POST:
        str: Le nom du fichier avec l'extension ajoutée si nécessaire.
    """
    if not nom_fichier.lower().endswith(extension):
        if nom_fichier == "":
            nom_fichier = " "
            nom_fichier += extension
        else:
            nom_fichier += extension
    return nom_fichier
