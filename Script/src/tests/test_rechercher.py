import unittest
import pandas as pd
from src.rechercher import rechercher_produit

class TestRechercher(unittest.TestCase):
    def setUp(self):
        data = {'Nom': ['Pomme', 'Pain', 'Téléphone'],
                'Quantité': [50, 30, 10],
                'Prix Unitaire (€)': [0.5, 1.2, 500],  # Modifier pour correspondre à la colonne utilisée dans la fonction
                'Catégorie': ['Fruit', 'Boulangerie', 'Électronique']}
        self.df = pd.DataFrame(data)

    def test_rechercher_nom(self):
        result = rechercher_produit(self.df, nom='Pomme', categorie='', prix_min=None, prix_max=None)
        self.assertEqual(len(result), 1)

    def test_rechercher_categorie(self):
        result = rechercher_produit(self.df, nom='', categorie='Électronique', prix_min=None, prix_max=None)
        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()