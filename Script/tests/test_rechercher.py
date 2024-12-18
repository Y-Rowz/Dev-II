import unittest
import pandas as pd
from src.rechercher import rechercher_produit

class TestRechercher(unittest.TestCase):
    def setUp(self):
        data = {
            'Nom': ['Pommes', 'Pâtes', 'Eau', 'Télévision', 'Ordinateur Portable', 'Casque Audio'],
            'Quantité': [50, 100, 200, 10, 5, 20],
            'Prix Unitaire (€)': [2.0, 1.5, 0.8, 500, 1200, 150],
            'Catégorie': ['Alimentation', 'Alimentation', 'Alimentation', 'Électronique', 'Électronique', 'Électronique']
        }
        self.df = pd.DataFrame(data)

    def test_rechercher_nom(self):
        result = rechercher_produit(self.df, nom='Pommes', categorie='', prix_min=None, prix_max=None)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['Nom'], 'Pommes')

    def test_rechercher_categorie(self):
        result = rechercher_produit(self.df, nom='', categorie='Électronique', prix_min=None, prix_max=None)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(result['Catégorie'] == 'Électronique'))

    def test_rechercher_prix(self):
        result = rechercher_produit(self.df, nom='', categorie='', prix_min=100, prix_max=600)
        self.assertEqual(len(result), 2)
        self.assertTrue(all((result['Prix Unitaire (€)'] >= 100) & (result['Prix Unitaire (€)'] <= 600)))

    def test_rechercher_multiple_criteres(self):
        result = rechercher_produit(self.df, nom='Télévision', categorie='Électronique', prix_min=None, prix_max=None)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['Nom'], 'Télévision')

if __name__ == '__main__':
    unittest.main()