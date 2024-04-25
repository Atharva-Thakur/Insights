import sys
import os
import numpy as np


# sys.path.append("..")

import unittest
import pandas as pd
from Modules.data_transformer import DataTransformer


class TestDataTransformer(unittest.TestCase):

    def setUp(self):
        # Initialize DataTransformer object with sample data
        data = {
            'A': [1, 2, 3, None, 5],
            'B': [4, 5, None, 7, 8],
            'C': ['X', 'Y', 'Z', 'X', 'Y'],
            'D': ['M', 'N', 'O', 'N', 'P'],
            'E': [10.1, 20.2, None, 40.4, 50.5],
            'F': [10.1, 20.2, None, 40.4, None],
            'G': [None, 20.2, None, 40.4, 50.5]
        }
        self.sample_data = pd.DataFrame(data)
        self.sample_data.to_csv("data.csv", index=False)
        self.transformer = DataTransformer(self.sample_data.copy())

    def test_handle_null_remove(self):
        # Test removing rows with null values
        self.transformer.handle_null_remove(['G'])
        self.assertNotIn(None, self.transformer.data['G'])
        # self.assertTrue(pd.read_csv("data.csv").equals(self.transformer.data))

    def test_remove_columns_func(self):
        # Test removing columns
        self.transformer.remove_columns_func(['D'])
        self.assertNotIn('D', self.transformer.data.columns)

    def test_handle_null_impute(self):
        # Test imputing null values with mean
        self.transformer.handle_null_impute('A', 'mean')
        self.assertFalse(self.transformer.data['A'].isnull().any())
        self.assertTrue(pd.read_csv("data.csv").equals(self.transformer.data))

        # Test imputing null values with mode
        self.transformer.handle_null_impute('F', 'mode')
        self.assertFalse(self.transformer.data['F'].isnull().any())
        self.assertTrue(pd.read_csv("data.csv").equals(self.transformer.data))

        # Test imputing null values with 0
        self.transformer.handle_null_impute('G', '0')
        self.assertFalse(self.transformer.data['G'].isnull().any())
        self.assertTrue(pd.read_csv("data.csv").equals(self.transformer.data))

    def test_categorical_to_numerical_func(self):
        # Test converting categorical columns to numerical
        self.transformer.categorical_to_numerical_func(['C'])
        self.assertTrue(any(col.startswith('C_') for col in self.transformer.data.columns))
        self.assertTrue(pd.read_csv("data.csv").equals(self.transformer.data))

    def tearDown(self):
        # Clean up temporary files generated during tests
        import os
        os.remove("data.csv")

if __name__ == '__main__':
    unittest.main()
