import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Thresholds de qualidade mínima para o modelo
ACCURACY_THRESHOLD = 0.85
PRECISION_THRESHOLD = 0.85
RECALL_THRESHOLD = 0.80
F1_THRESHOLD = 0.825

def test_model_performance():
    # Carregar modelo salvo
    with open('../BEST_model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Carregar os dados
    url = "https://raw.githubusercontent.com/FernandoMBresolin/Heart_Atack_ML/refs/heads/main/heart.csv"
    dataset = pd.read_csv(url)

    # Limpeza (igual ao treino!)
    dataset = dataset[(dataset['Cholesterol'] != 0) & (dataset['RestingBP'] != 0)]

    X = dataset.drop('HeartDisease', axis=1)
    y = dataset['HeartDisease']

    # Divisão treino/teste com mesma semente
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=7, stratify=y
    )

    # Predição
    y_pred = model.predict(X_test)

    # Cálculo das métricas
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Impressão (opcional)
    print(f"Acurácia: {acc:.3f}, Precisão: {prec:.3f}, Recall: {rec:.3f}, F1-score: {f1:.3f}")

    # Testes de verificação com assertions
    assert acc >= ACCURACY_THRESHOLD, f"Acurácia abaixo do esperado: {acc:.3f}"
    assert prec >= PRECISION_THRESHOLD, f"Precisão abaixo do esperado: {prec:.3f}"
    assert rec >= RECALL_THRESHOLD, f"Recall abaixo do esperado: {rec:.3f}"
    assert f1 >= F1_THRESHOLD, f"F1-score abaixo do esperado: {f1:.3f}"
