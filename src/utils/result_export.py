import os
import rasterio
import geopandas as gpd
from rasterio.transform import from_origin
from src.utils.logs import log
import rasterio.features

def export_classified_raster(classified, red, results_dir):
    log.info('Exportando raster de classificação...')
    transform = from_origin(red.bounds.left, red.bounds.top, red.res[0], red.res[1])
    new_dataset = rasterio.open(
        os.path.join(results_dir, 'classified_tiff.tif'), 'w',
        driver='GTiff',
        height=classified.shape[0],
        width=classified.shape[1],
        count=1,
        dtype=rasterio.uint8,
        crs=red.crs,
        transform=transform,
    )

    new_dataset.write(classified.astype(rasterio.uint8), 1)
    new_dataset.close()
    log.info('Raster de classificação exportado com sucesso!')

def save_gdf(classified, results_dir):
    log.info('Criando GeoPackage....')
    classified_raster = rasterio.open(os.path.join(results_dir, 'classified_tiff.tif'))
    classified_data = classified_raster.read(1, masked=False)
    mask = classified_data != classified_raster.nodata
    shapes = list(rasterio.features.shapes(classified_data, transform=classified_raster.transform, mask=mask))
    results_gdf = gpd.GeoDataFrame.from_features([
        {"geometry": shape, 
         "properties": {"class": value}} for shape, value in shapes], 
         crs=classified_raster.crs)
    
    results_gdf.to_file(os.path.join(results_dir, 'classification_result.shp'))
    results_gdf.to_file(os.path.join(results_dir, 'classification_result.gpkg'), driver='GPKG')
    log.info('GeoPackage criado com sucesso!')

def save_areas(area_by_class, results_dir):
    log.info('Salvando áreas...')
    results_gdf = gpd.read_file(os.path.join(results_dir, 'classification_result.shp'))
    results_gdf_proj = results_gdf.to_crs('EPSG:4326')
    area_by_class = {}
    for class_value, group in results_gdf_proj.groupby('class'):
        area_sum = group.geometry.to_crs('EPSG:6933').area.sum()
        area_by_class[class_value] = area_sum
    
    with open(os.path.join(results_dir, 'area_by_class.txt'), 'w') as f:
        f.write("Área por classe:\n")
        for class_value, area_sum in area_by_class.items():
            f.write(f"Classe {class_value}: {area_sum} unidades de área\n")
    log.info('Área salva com sucesso!')        
