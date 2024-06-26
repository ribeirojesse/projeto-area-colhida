import os
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.utils.logs import log

def calculate_and_save_class_areas(results_gdf, results_dir):
    log.info('Calculando e salvando as área de cada classe...')
    """Calcula e salva as áreas de cada classe em um arquivo CSV."""
    results_gdf['area'] = results_gdf.geometry.area / 10**6  # Convertendo de m² para km², se necessário
    class_areas = results_gdf.groupby('class')['area'].sum().reset_index()
    class_areas.to_csv(os.path.join(results_dir, 'class_areas.csv'), index=False)
    log.info('Áreas calculadas e salvas com sucesso!')

def plot_results(classified, results_dir):
    log.info('Plotando classificação...')
    classified_raster = rasterio.open(os.path.join(results_dir, 'classified_tiff.tif'))
    classified_data = classified_raster.read(1, masked=False)
    mask = classified_data != classified_raster.nodata
    shapes = list(rasterio.features.shapes(classified_data, transform=classified_raster.transform, mask=mask))
    results_gdf = gpd.GeoDataFrame.from_features([
        {"geometry": shape, 
         "properties": {"class": value}} for shape, value in shapes], 
         crs=classified_raster.crs)
    
    # Chamar a função para calcular e salvar as áreas das classes
    calculate_and_save_class_areas(results_gdf, results_dir)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    results_gdf.plot(column='class', ax=ax, legend=True, cmap='viridis')
    plt.title('Classificação de Uso do Solo')
    plt.savefig(os.path.join(results_dir, 'plot_map.png'))
    plt.close(fig)
    log.info('Classificação plotada com sucesso!')

def plot_confusion_matrix(conf_matrix, class_names, results_dir):
    log.info('Plotando Matriz de Confusão...')
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap='viridis', ax=ax, xticklabels=class_names, yticklabels=class_names)
    ax.set_xlabel('Valores Preditos')
    ax.set_ylabel('Valores Reais')
    ax.set_title('Matriz de Confusão')
    plt.savefig(os.path.join(results_dir, 'confusion_matrix.png'))
    plt.close(fig)
    log.info('Matriz de Confusão plotada com sucesso!')

def plot_classification_report(report, results_dir):
    log.info('Plotando relatório de classificação...')
    report_data = []
    lines = report.split('\n')
    for line in lines[2:-3]:
        row_data = line.split()
        if len(row_data) == 5:
            report_data.append(row_data)
        elif len(row_data) == 6:
            report_data.append(row_data[1:])
    
    metrics = ['precision', 'recall', 'f1-score', 'support']
    classes = [row[0] for row in report_data]
    data = np.array([row[1:] for row in report_data]).astype(float)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(data, annot=True, fmt=".2f", cmap='viridis', xticklabels=metrics, yticklabels=classes, ax=ax)
    ax.set_xlabel('Métricas')
    ax.set_ylabel('Classes')
    ax.set_title('Relatório de Classificação')
    plt.savefig(os.path.join(results_dir, 'classification_report.png'))
    plt.close(fig)
    log.info('Relatório de Classificação plotado com sucesso!')
