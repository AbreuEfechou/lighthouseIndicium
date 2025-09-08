# analise-dados-imdb/src/eda.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def carregar_dados(caminho):
    """Carrega os dados a partir de um arquivo CSV."""
    dados = pd.read_csv(caminho)
    return dados

def resumo_dados(dados):
    """Gera um resumo estatístico dos dados."""
    return dados.describe()

def visualizar_distribuicao(dados, coluna):
    """Visualiza a distribuição de uma coluna específica."""
    plt.figure(figsize=(10, 6))
    sns.histplot(dados[coluna], bins=30, kde=True)
    plt.title(f'Distribuição de {coluna}')
    plt.xlabel(coluna)
    plt.ylabel('Frequência')
    plt.grid()
    plt.show()

def correlacao(dados):
    """Calcula e plota a matriz de correlação."""
    plt.figure(figsize=(12, 8))
    correlacao = dados.corr()
    sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de Correlação')
    plt.show()

def visualizar_categoria(dados, coluna):
    """Visualiza a contagem de categorias em uma coluna específica."""
    plt.figure(figsize=(12, 6))
    sns.countplot(data=dados, x=coluna, order=dados[coluna].value_counts().index)
    plt.title(f'Contagem de {coluna}')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()