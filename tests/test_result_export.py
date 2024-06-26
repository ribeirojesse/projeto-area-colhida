import unittest
import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
from src.utils.result_export import export_classified_raster, save_gdf
import geopandas as gpd

class TestResultExport(unittest.TestCase):
    
    def setUp(self):
        self.classified = np.random.randint(0, 2, (10, 10))
        self.red_tiff = 'test_data/images/red.tif'
        self.results_dir = 'test_results'
        os.makedirs(self.results_dir, exist_ok=True)
        self.create_dummy_tiff(self.red_tiff)
    
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

    def test_export_classified_raster(self):
        with rasterio.open(self.red_tiff) as red:
            export_classified_raster(self.classified, red, self.results_dir)
            self.assertTrue(os.path.exists(os.path.join(self.results_dir, 'classified_tiff.tif')))
    
    def test_save_gdf(self):
        with rasterio.open(self.red_tiff) as red:
            save_gdf(self.classified, self.results_dir)
            self.assertTrue(os.path.exists(os.path.join(self.results_dir, 'classification_result.shp')))
            self.assertTrue(os.path.exists(os.path.join(self.results_dir, 'classification_result.gpkg')))
    
    #def tearDown(self):
        #os.remove(self.red_tiff)
        #for file in os.listdir(self.results_dir):
            #os.remove(os.path.join(self.results_dir, file))
       # os.rmdir(self.results_dir)

if __name__ == '__main__':
    unittest.main()
