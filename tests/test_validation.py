import unittest
import numpy as np
import os
import geopandas as gpd
from shapely.geometry import Point
from src.utils.validation import validate_classification
import rasterio
from rasterio.transform import from_origin

class TestValidation(unittest.TestCase):
    
    def setUp(self):
        self.classified = np.random.randint(0, 2, (10, 10))
        
        # Create dummy TIFF for red band
        self.red_tiff = 'test_data/images/red.tif'
        self.create_dummy_tiff(self.red_tiff)
        
        # Create a dummy shapefile for validation points
        data = {'LULC': [1, 0], 'geometry': [Point(1, 1), Point(2, 2)]}
        self.pontos_valid = gpd.GeoDataFrame(data, crs='EPSG:4326')
    
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

    def test_validate_classification(self):
        with rasterio.open(self.red_tiff) as red:
            conf_matrix, report = validate_classification(self.classified, red, self.pontos_valid)
            self.assertIsInstance(conf_matrix, np.ndarray)
            self.assertIsInstance(report, str)

    #def tearDown(self):
        #os.remove(self.red_tiff)

if __name__ == '__main__':
    unittest.main()
