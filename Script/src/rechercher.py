import pandas as pd

def rechercher_produit(df, nom, categorie, prix_min, prix_max):
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
