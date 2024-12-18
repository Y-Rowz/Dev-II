import unittest
import pandas as pd
from src.rapport import generer_statistiques

class TestRapport(unittest.TestCase):
    def setUp(self):
        data = {'Nom': ['Pomme', 'Pain'],
                'Quantité': [50, 30],
                'Prix Unitaire (€)': [0.5, 1.2],  # Modifier pour correspondre à la colonne utilisée dans la fonction
                'Catégorie': ['Fruit', 'Boulangerie']}
        self.df = pd.DataFrame(data)

    def test_generer_statistiques(self):
        stats = generer_statistiques(self.df)
        self.assertEqual(stats['Valeur Totale'], 50*0.5 + 30*1.2)
        self.assertEqual(stats['Articles Totaux'], 80)

if __name__ == '__main__':
    unittest.main()