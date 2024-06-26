from sklearn.metrics import confusion_matrix, classification_report
from src.utils.logs import log
import numpy as np

def validate_classification(classified, red, pontos_valid):
    log.info('Validando classificação...')
    valid_geometries = pontos_valid.geometry
    valid_labels = pontos_valid['LULC'].values
    predicted_labels = []

    for geom in valid_geometries:
        coords = [(geom.xy[0][0], geom.xy[1][0])]
        row, col = red.index(coords[0][0], coords[0][1])
        predicted_labels.append(classified[row, col])

    conf_matrix = confusion_matrix(valid_labels, predicted_labels)
    report = classification_report(valid_labels, predicted_labels, target_names=[str(c) for c in np.unique(valid_labels)])
    log.info('Classificação validada com sucesso!')
    return conf_matrix, report
    

