import rasterio
import geopandas as gpd
from src.utils.logs import log

def read_rasters(red_tiff, green_tiff, blue_tiff):
    log.info('Lendo rasters...')
    red = rasterio.open(red_tiff)
    green = rasterio.open(green_tiff)
    blue = rasterio.open(blue_tiff)
    return red, green, blue
    log.info('Processo de leitura dos rasters finalizado!')

def read_shapefile(shapefile_path):
    log.info('Lendo shapefile...')
    return gpd.read_file(shapefile_path)
    log.info('Processo de leitura do shapefile finalizado!')
