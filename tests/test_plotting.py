import unittest
import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
from src.utils.plotting import plot_results, plot_confusion_matrix, plot_classification_report
import matplotlib.pyplot as plt

class TestPlotting(unittest.TestCase):
    
    def setUp(self):
        self.results_dir = 'test_results'
        os.makedirs(self.results_dir, exist_ok=True)
        self.classified = np.random.randint(0, 2, (10, 10))
        self.conf_matrix = np.array([[5, 2], [1, 7]])
        self.class_names = ['Class 0', 'Class 1']
        self.report = 'Classification Report\n\n              precision    recall  f1-score   support\n\n     Class 0       0.83      0.71      0.77         7\n     Class 1       0.78      0.88      0.82         8\n\n    accuracy                           0.80        15\n   macro avg       0.81      0.79      0.79        15\nweighted avg       0.80      0.80      0.80        15'

        # Create dummy tiff file to simulate classified raster
        self.classified_tiff_path = os.path.join(self.results_dir, 'classified_tiff.tif')
        self.create_dummy_tiff(self.classified_tiff_path)
    
    def create_dummy_tiff(self, path):
        data = np.zeros((10, 10), dtype=rasterio.uint8)
        transform = from_origin(0, 10, 1, 1)
        with rasterio.open(
            path, 'w', driver='GTiff',
            height=data.shape[0], width=data.shape[1],
            count=1, dtype=data.dtype,
            transform=transform
        ) as dst:
            dst.write(data, 1)

    def test_plot_classification_report(self):
        plot_classification_report(self.report, self.results_dir)
        self.assertTrue(os.path.exists(os.path.join(self.results_dir, 'classification_report.png')))

    
    #def tearDown(self):
        #for file in os.listdir(self.results_dir):
            #os.remove(os.path.join(self.results_dir, file))
        #os.rmdir(self.results_dir)

if __name__ == '__main__':
    unittest.main()
