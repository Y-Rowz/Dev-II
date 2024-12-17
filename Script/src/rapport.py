import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF

def generer_statistiques(df: pd.DataFrame) -> dict:
    valeur_totale = (df['Quantité'] * df['Prix Unitaire (€)']).sum()
    articles_totaux = df['Quantité'].sum()
    return {"Valeur Totale": valeur_totale, "Articles Totaux": articles_totaux}

def generer_graphique(df: pd.DataFrame, chemin: str) -> None:
    if not chemin.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError("Le chemin de l'image doit avoir une extension valide (.png, .jpg, .jpeg)")
    
    stats = df.groupby('Catégorie')['Quantité'].sum()
    plt.figure(figsize=(10, 6))
    stats.plot(kind='bar', title='Quantité par Catégorie')
    plt.xlabel('Catégorie')
    plt.ylabel('Quantité')
    plt.tight_layout()  # Ajuste les marges pour que les légendes soient visibles
    plt.savefig(chemin)
    plt.close()

def generer_rapport_pdf(df: pd.DataFrame, chemin_pdf: str, chemin_graphique: str) -> None:
    if not os.path.exists(chemin_graphique):
        raise FileNotFoundError(f"L'image spécifiée n'existe pas : {chemin_graphique}")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Ajout de la police DejaVuSans avec encodage UTF-8
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    
    # Titre
    pdf.cell(200, 10, txt="Rapport d'Inventaire", ln=True, align='C')
    pdf.ln(10)  # Ajouter un espace après le titre
    
    # Section Statistiques
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Statistiques", ln=True)
    pdf.set_font('DejaVu', '', 10)
    stats = generer_statistiques(df)
    for k, v in stats.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True, border=1)
    pdf.ln(10)  # Ajouter un espace après les statistiques
    
    # Section Détails des articles
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Détails des articles", ln=True)
    pdf.set_font('DejaVu', '', 8)
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"Article: {row['Nom']} | Catégorie: {row['Catégorie']} | Quantité: {row['Quantité']} | Prix Unitaire (€): {row['Prix Unitaire (€)']}", ln=True, border=1)
    pdf.ln(10)  # Ajouter un espace après les détails des articles
    
    # Section Graphique
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Graphique", ln=True)
    pdf.image(chemin_graphique, x=10, y=pdf.get_y() + 10, w=190)
    
    # Sauvegarde du PDF
    pdf.output(chemin_pdf)

def ajouter_extension_si_absente(nom_fichier, extension):
    if not nom_fichier.lower().endswith(extension):
        nom_fichier += extension
    return nom_fichier