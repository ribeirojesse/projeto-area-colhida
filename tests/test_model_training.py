import unittest
import numpy as np
from src.utils.model_training import train_classifier
from sklearn.ensemble import RandomForestClassifier

class TestModelTraining(unittest.TestCase):
    
    def setUp(self):
        # Create dummy data
        self.X = np.random.rand(100, 3)
        self.y = np.random.randint(0, 2, 100)
    
    def test_train_classifier(self):
        classifier = train_classifier(self.X, self.y)
        self.assertIsInstance(classifier, RandomForestClassifier)
        self.assertTrue(hasattr(classifier, 'predict'))
    
if __name__ == '__main__':
    unittest.main()
