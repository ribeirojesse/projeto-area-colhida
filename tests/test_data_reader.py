import unittest
import os
import numpy as np
import rasterio
from shapely.geometry import Point
from src.utils.data_reader import read_rasters, read_shapefile
import geopandas as gpd

class TestDataReader(unittest.TestCase):
    
    def setUp(self):
        # Paths to sample TIFF files
        self.red_tiff = 'test_data/images/red.tif'
        self.green_tiff = 'test_data/images/green.tif'
        self.blue_tiff = 'test_data/images/blue.tif'
        self.shapefile_path = 'test_data/shapefile/amostras_treino.shp'
        
        # Create dummy TIFF files for testing
        self.create_dummy_tiff(self.red_tiff)
        self.create_dummy_tiff(self.green_tiff)
        self.create_dummy_tiff(self.blue_tiff)
        
        # Create a dummy shapefile for testing
        self.create_dummy_shapefile(self.shapefile_path)
    
    def create_dummy_tiff(self, path):
        data = np.zeros((10, 10), dtype=rasterio.uint8)
        with rasterio.open(
            path, 'w', driver='GTiff',
            height=data.shape[0], width=data.shape[1],
            count=1, dtype=data.dtype
        ) as dst:
            dst.write(data, 1)
    
    def create_dummy_shapefile(self, path):
        data = {'LULC': [1, 2], 'geometry': [Point(1, 1), Point(2, 2)]}
        gdf = gpd.GeoDataFrame(data, crs='EPSG:4326')
        gdf.to_file(path)
    
    def test_read_rasters(self):
        red, green, blue = read_rasters(self.red_tiff, self.green_tiff, self.blue_tiff)
        self.assertIsInstance(red, rasterio.io.DatasetReader)
        self.assertIsInstance(green, rasterio.io.DatasetReader)
        self.assertIsInstance(blue, rasterio.io.DatasetReader)

    def test_read_shapefile(self):
        gdf = read_shapefile(self.shapefile_path)
        self.assertIsInstance(gdf, gpd.GeoDataFrame)
    
    #def tearDown(self):
        # Clean up dummy TIFF files and shapefile
        #os.remove(self.red_tiff)
        #os.remove(self.green_tiff)
        #os.remove(self.blue_tiff)
        #os.remove(self.shapefile_path)

if __name__ == '__main__':
    unittest.main()
