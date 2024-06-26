import numpy as np
from rasterio.mask import mask
from src.utils.logs import log

def extract_raster_values(raster, shapes):
    log.info('Extração de valores de raster...')
    out_image, out_transform = mask(raster, shapes, crop=True)
    out_image = out_image[0]  # Acessa a primeira (e única) banda
    return out_image[out_image != raster.nodata]
    log.info('Processo de extração de valores de raster realizado com sucesso!')

def extract_samples(amostras_treino, red, green, blue):
    log.info('Extração de amostras de treinamento...')
    classes = amostras_treino['LULC'].unique()
    X, y = [], []
    for c in classes:
        geometries = amostras_treino[amostras_treino['LULC'] == c].geometry
        red_values = extract_raster_values(red, geometries)
        green_values = extract_raster_values(green, geometries)
        blue_values = extract_raster_values(blue, geometries)
        
        # Empilhar os valores de R, G, B
        samples = np.vstack([red_values, green_values, blue_values]).T
        labels = np.full(samples.shape[0], c)
        
        X.append(samples)
        y.append(labels)
    
    # Converter para arrays numpy
    X = np.vstack(X)
    y = np.concatenate(y)
    return X, y
    log.info('Processo de treinamento realizado com sucesso!')

def classify_image(classifier, red, green, blue):
    log.info('Classificação da imagem...')
    red_data = red.read(1)
    green_data = green.read(1)
    blue_data = blue.read(1)

    # Empilhar os dados dos rasters
    stacked_data = np.dstack([red_data, green_data, blue_data])
    rows, cols, bands = stacked_data.shape
    flat_data = stacked_data.reshape(rows * cols, bands)

    # Predizer a classificação
    predictions = classifier.predict(flat_data)
    classified = predictions.reshape(rows, cols)
    return classified
    log.info('Processo de classificação realizado com sucesso!')
