import unittest
import pandas as pd
import os
import tempfile
import shutil

from src.rapport import (
    generer_statistiques, 
    generer_graphique, 
    generer_rapport_pdf, 
    rechercher_produit, 
    importer_csv, 
    ajouter_extension_si_absente
)

class TestRapport(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
        data = {
            'Nom': ['Pommes', 'Pâtes', 'Eau', 'Télévision', 'Ordinateur Portable', 'Casque Audio'],
            'Quantité': [50, 100, 200, 10, 5, 20],
            'Prix Unitaire (€)': [2.0, 1.5, 0.8, 500, 1200, 150],
            'Catégorie': ['Alimentation', 'Alimentation', 'Alimentation', 'Électronique', 'Électronique', 'Électronique']
        }
        self.df = pd.DataFrame(data)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_generer_statistiques(self):
        stats = generer_statistiques(self.df)
        
        expected_total_value = (
            (50 * 2.0) + 
            (100 * 1.5) + 
            (200 * 0.8) + 
            (10 * 500) + 
            (5 * 1200) + 
            (20 * 150)
        )
        
        self.assertAlmostEqual(stats['Valeur Totale'], expected_total_value)
        self.assertEqual(stats['Articles Totaux'], 385)

    def test_generer_graphique(self):
        graph_path = os.path.join(self.test_dir, 'test_graph.png')
        
        generer_graphique(self.df, graph_path)
        
        self.assertTrue(os.path.exists(graph_path))

    def test_generer_graphique_invalid_path(self):
        with self.assertRaises(ValueError):
            generer_graphique(self.df, os.path.join(self.test_dir, 'test_graph.txt'))
        
        with self.assertRaises(ValueError):
            generer_graphique(self.df, '')

    def test_generer_rapport_pdf(self):
        graph_path = os.path.join(self.test_dir, 'test_graph.png')
        generer_graphique(self.df, graph_path)
        
        pdf_path = os.path.join(self.test_dir, 'test_rapport.pdf')
        
        generer_rapport_pdf(self.df, pdf_path, graph_path)
        
        self.assertTrue(os.path.exists(pdf_path))

    def test_generer_rapport_pdf_missing_graph(self):
        pdf_path = os.path.join(self.test_dir, 'test_rapport.pdf')
        non_existent_graph = os.path.join(self.test_dir, 'non_existent.png')
        
        with self.assertRaises(FileNotFoundError):
            generer_rapport_pdf(self.df, pdf_path, non_existent_graph)

    def test_rechercher_produit(self):
        results = rechercher_produit(self.df, 'Pommes', '', None, None)
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]['Nom'], 'Pommes')
        
        results = rechercher_produit(self.df, '', 'Électronique', None, None)
        self.assertEqual(len(results), 3)
        
        results = rechercher_produit(self.df, '', '', 100, 600)
        self.assertEqual(len(results), 2)

    def test_importer_csv(self):
        csv_data1 = pd.DataFrame({
            'Nom': ['Pommes', 'Pâtes'],
            'Quantité': [50, 100],
            'Prix Unitaire (€)': [2.0, 1.5],
            'Catégorie': ['Alimentation', 'Alimentation']
        })
        csv_data2 = pd.DataFrame({
            'Nom': ['Télévision', 'Casque Audio'],
            'Quantité': [10, 20],
            'Prix Unitaire (€)': [500, 150],
            'Catégorie': ['Électronique', 'Électronique']
        })
        
        csv_path1 = os.path.join(self.test_dir, 'inventory1.csv')
        csv_path2 = os.path.join(self.test_dir, 'inventory2.csv')
        csv_data1.to_csv(csv_path1, index=False)
        csv_data2.to_csv(csv_path2, index=False)
        
        combined_df = importer_csv(self.test_dir)
        
        self.assertEqual(len(combined_df), 4)
        
    def test_ajouter_extension_si_absente(self):
        self.assertEqual(ajouter_extension_si_absente('', '.png'), ' .png')
        
        self.assertEqual(ajouter_extension_si_absente('test', '.png'), 'test.png')
        
        self.assertEqual(ajouter_extension_si_absente('test.png', '.png'), 'test.png')

if __name__ == '__main__':
    unittest.main()