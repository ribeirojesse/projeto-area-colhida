from sklearn.ensemble import RandomForestClassifier
from src.utils.logs import log

def train_classifier(X, y):
    log.info('Treiando classificador...')
    classifier = RandomForestClassifier(n_estimators=500, random_state=42)
    classifier.fit(X, y)
    return classifier
    log.info('Processo de treinamento realizado com sucesso!')