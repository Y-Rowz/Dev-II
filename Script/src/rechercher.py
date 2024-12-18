import pandas as pd

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
    filtre = pd.Series([True] * len(df))
    if nom:
        filtre &= df['Nom'].str.contains(nom, case=False, na=False)
    if categorie:
        filtre &= df['Catégorie'].str.contains(categorie, case=False, na=False)
    if prix_min is not None:
        filtre &= df['Prix Unitaire (€)'] >= prix_min
    if prix_max is not None:
        filtre &= df['Prix Unitaire (€)'] <= prix_max
    return df[filtre]
