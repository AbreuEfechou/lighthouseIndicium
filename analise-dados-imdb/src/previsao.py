# previsao.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

def carregar_dados(caminho_arquivo):
    dados = pd.read_csv(caminho_arquivo)
    return dados

def preparar_dados(dados):
    # Supondo que as colunas relevantes para a previsão da nota do IMDb sejam 'features' e 'nota_imdb'
    X = dados.drop('nota_imdb', axis=1)  # Features
    y = dados['nota_imdb']  # Target
    return X, y

def treinar_modelo(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    return modelo

def prever_nota(modelo, dados_novo):
    return modelo.predict(dados_novo)

def salvar_modelo(modelo, caminho):
    joblib.dump(modelo, caminho)

def carregar_modelo(caminho):
    return joblib.load(caminho)

if __name__ == "__main__":
    caminho_arquivo = '../data/desafio_indicium_imdb.csv'
    dados = carregar_dados(caminho_arquivo)
    X, y = preparar_dados(dados)
    modelo = treinar_modelo(X, y)
    salvar_modelo(modelo, 'modelo_previsao_imdb.pkl')