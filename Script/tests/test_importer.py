import unittest
import pandas as pd
from src.importer import importer_csv

class TestImporter(unittest.TestCase):
    def test_importer_csv(self):
        df = importer_csv('data/')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn('Nom', df.columns)

if __name__ == '__main__':
    unittest.main()
