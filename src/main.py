import numpy as np
from datetime import date
from utils.logs import log
from utils.data_reader import read_rasters, read_shapefile
from utils.image_processing import extract_samples, classify_image
from utils.model_training import train_classifier
from utils.validation import validate_classification
from utils.result_export import export_classified_raster, save_gdf, save_areas
from utils.plotting import plot_results, plot_confusion_matrix, plot_classification_report
from api.crud import create_image
from api.schemas import ProcessedImageBase
from api.database import SessionLocal

def main():
    log.info('Iniciando o processo de classificação...')
    # Caminhos dos arquivos
    red_tiff = 'data/images/red.tif'
    green_tiff = 'data/images/green.tif'
    blue_tiff = 'data/images/blue.tif'
    amostras_treino_shp = 'data/shapefile/amostras_treino.shp'
    pontos_valid_shp = 'data/shapefile/pontos_valid.shp'
    results_dir = 'results'
    
    log.info('Leitura dos dados...')
    # Leitura dos dados
    red, green, blue = read_rasters(red_tiff, 
                                    green_tiff,     
                                    blue_tiff)
    amostras_treino = read_shapefile(amostras_treino_shp)
    pontos_valid = read_shapefile(pontos_valid_shp)
    log.info('Processo de leitura dos dados finalizado!')

    log.info('Extração de amostras e treinamento...')
    # Extração de amostras e treinamento
    X, y = extract_samples(amostras_treino, 
                           red, 
                           green, 
                           blue)
    classifier = train_classifier(X, y)
    log.info('Processo de treinamento concluído!')

    log.info('Classificando e validando imagem...')
    classified = classify_image(classifier, 
                                red, 
                                green, 
                                blue)
    conf_matrix, report = validate_classification(classified, 
                                                  red, 
                                                  pontos_valid)
    log.info('Processo de classificação e validação concluído!')

    log.info('Plotagem iniciada...')
    plot_classification_report(report, 
                               results_dir)
    class_names = [str(c) for c in np.unique(y)]
    plot_confusion_matrix(conf_matrix, 
                          class_names,  
                          results_dir)
    export_classified_raster(classified, 
                             red, 
                             results_dir)
    save_gdf(classified, 
             results_dir)
    plot_results(classified, 
                 results_dir)
    log.info('Plotagem concluída!')

    log.info('Processo concluído com sucesso!')

if __name__ == "__main__":
    main()

