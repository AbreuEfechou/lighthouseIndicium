def carregar_dados(caminho_arquivo):
    import pandas as pd
    return pd.read_csv(caminho_arquivo)

def preprocessar_dados(df):
    # Exemplo de pré-processamento: remover colunas desnecessárias e lidar com valores ausentes
    df = df.drop(columns=['coluna_desnecessaria'], errors='ignore')
    df = df.fillna({'coluna_exemplo': 'valor_padrao'})
    return df

def salvar_dados(df, caminho_arquivo):
    df.to_csv(caminho_arquivo, index=False)

def visualizar_dados(df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='genero')
    plt.title('Distribuição de Gêneros')
    plt.xticks(rotation=45)
    plt.show()