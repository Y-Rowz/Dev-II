import pandas as pd
import os

def importer_csv(dossier):
    """
    Importe et fusionne tous les fichiers CSV d'un dossier.
    
    PRE:
        dossier (str): Le chemin du dossier contenant les fichiers CSV.
    
    Post:
        pd.DataFrame: Un DataFrame combinant tous les fichiers CSV.
    """
    all_files = [os.path.join(dossier, f) for f in os.listdir(dossier) if f.endswith('.csv')]
    df_list = [pd.read_csv(file) for file in all_files]
    df = pd.concat(df_list, ignore_index=True)
    return df