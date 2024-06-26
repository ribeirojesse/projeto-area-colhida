import unittest
import os
import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from src.utils.image_processing import extract_samples

class TestImageProcessing(unittest.TestCase):
    
    def setUp(self):
        self.red_tiff = 'test_data/images/red.tif'
        self.green_tiff = 'test_data/images/green.tif'
        self.blue_tiff = 'test_data/images/blue.tif'
        self.create_dummy_tiff(self.red_tiff)
        self.create_dummy_tiff(self.green_tiff)
        self.create_dummy_tiff(self.blue_tiff)
        
        # Create a dummy shapefile for training samples within the raster bounds
        data = {'LULC': [1, 2], 'geometry': [Point(1, 1), Point(5, 5)]}
        self.amostras_treino = gpd.GeoDataFrame(data, crs='EPSG:4326')
    
    def create_dummy_tiff(self, path):
        data = np.zeros((10, 10), dtype=rasterio.uint8)
        transform = rasterio.transform.from_origin(0, 10, 1, 1)
        with rasterio.open(
            path, 'w', driver='GTiff',
            height=data.shape[0], width=data.shape[1],
            count=1, dtype=data.dtype,
            transform=transform
        ) as dst:
            dst.write(data, 1)

if __name__ == '__main__':
    unittest.main()
