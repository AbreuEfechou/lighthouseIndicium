import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Carregar os dados
df = pd.read_csv('desafio_indicium_imdb.csv')

# Verificar dados faltantes
print("Dados faltantes por coluna:")
print(df.isnull().sum())

# Tratar dados faltantes
df['Gross'].fillna(0, inplace=True)
df['Meta_score'].fillna(df['Meta_score'].median(), inplace=True)

# Converter tipos de dados
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
df['Gross'] = df['Gross'].astype(float)