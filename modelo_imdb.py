import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle
import re

def preprocessar_dados(df):
    """Pré-processamento dos dados"""
    df_clean = df.copy()
    
    if 'Unnamed: 0' in df_clean.columns:
        df_clean = df_clean.drop(columns=['Unnamed: 0'])
    
    def limpar_gross(valor):
        if pd.isna(valor):
            return 0
        if isinstance(valor, str):
            valor_limpo = ''.join(c for c in valor if c.isdigit() or c == '.')
            return float(valor_limpo) if valor_limpo else 0
        return float(valor)
    
    df_clean['Gross'] = df_clean['Gross'].apply(limpar_gross)
    
    def limpar_runtime(valor):
        if pd.isna(valor):
            return np.nan
        if isinstance(valor, str):
            numeros = re.findall(r'\d+', valor)
            return int(numeros[0]) if numeros else np.nan
        return valor
    
    df_clean['Runtime'] = df_clean['Runtime'].apply(limpar_runtime)
    
    df_clean['Meta_score'] = df_clean['Meta_score'].fillna(df_clean['Meta_score'].median())
    df_clean['Runtime'] = df_clean['Runtime'].fillna(df_clean['Runtime'].median())
    df_clean['IMDB_Rating'] = df_clean['IMDB_Rating'].fillna(df_clean['IMDB_Rating'].median())
    df_clean['No_of_Votes'] = df_clean['No_of_Votes'].fillna(df_clean['No_of_Votes'].median())
    
    def padronizar_certificados(certificado):
        if pd.isna(certificado):
            return 'Unknown'
        certificado = str(certificado).strip().upper()
        if certificado in ['UA', 'U/A', 'TV-14']:
            return 'PG-13'
        elif certificado in ['TV-PG']:
            return 'PG'
        elif certificado in ['U']:
            return 'G'
        elif certificado in ['A', 'TV-MA']:
            return 'R'
        else:
            return certificado
    
    df_clean['Certificate'] = df_clean['Certificate'].apply(padronizar_certificados)
    df_clean['Certificate'] = df_clean['Certificate'].fillna('Unknown')
    
    return df_clean

def treinar_modelo(df, salvar_modelo=True):
    """Treinar modelo de previsão de nota IMDB"""
    
    df_clean = preprocessar_dados(df)
    
    features = ['Gross', 'Runtime', 'Meta_score', 'No_of_Votes', 'Certificate', 'Genre']
    target = 'IMDB_Rating'
    
    df_model = df_clean[features + [target]].dropna()
    
    categorical_cols = ['Certificate', 'Genre']
    label_encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col].astype(str))
        label_encoders[col] = le
    
    X = df_model[features]
    y = df_model[target]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['Gross', 'Runtime', 'Meta_score', 'No_of_Votes']),
            ('cat', 'passthrough', ['Certificate', 'Genre'])
        ]
    )
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print("📊 Avaliação do Modelo:")
    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R²: {r2:.3f}")
    
    if salvar_modelo:
        modelo_data = {
            'pipeline': pipeline,
            'label_encoders': label_encoders,
            'features': features,
            'metrics': {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        }
        
        with open('modelo_imdb.pkl', 'wb') as f:
            pickle.dump(modelo_data, f)
        
        print("✅ Modelo salvo como 'modelo_imdb.pkl'")
    
    return pipeline, label_encoders, features, {'MAE': mae, 'RMSE': rmse, 'R2': r2}

def carregar_modelo(caminho='modelo_imdb.pkl'):
    """Carregar modelo treinado"""
    with open(caminho, 'rb') as f:
        modelo_data = pickle.load(f)
    return modelo_data

def prever_nota_imdb(modelo_data, gross, runtime, meta_score, num_votes, certificate, genre):
    """
    Prever nota IMDB para novos dados
    """
    pipeline = modelo_data['pipeline']
    label_encoders = modelo_data['label_encoders']
    features = modelo_data['features']
    
    input_data = pd.DataFrame({
        'Gross': [gross],
        'Runtime': [runtime],
        'Meta_score': [meta_score],
        'No_of_Votes': [num_votes],
        'Certificate': [certificate],
        'Genre': [genre]
    })
    
    for col in ['Certificate', 'Genre']:
        le = label_encoders[col]
        input_data[col] = input_data[col].apply(
            lambda x: le.transform([x])[0] if x in le.classes_ else -1
        )
    
    predicao = pipeline.predict(input_data)[0]
    
    return predicao

if __name__ == "__main__":
    print("📂 Carregando dados...")
    df = pd.read_csv('desafio_indicium_imdb.csv')
    
    print("🤖 Treinando modelo...")
    pipeline, label_encoders, features, metrics = treinar_modelo(df, salvar_modelo=True)
    
    print("\n🎯 Exemplo de previsão:")
    exemplo_pred = prever_nota_imdb(
        {'pipeline': pipeline, 'label_encoders': label_encoders, 'features': features},
        gross=100000000, 
        runtime=120,
        meta_score=70,
        num_votes=500000,
        certificate='PG-13',
        genre='Action, Adventure'
    )
    
    print(f"Nota IMDB prevista: {exemplo_pred:.2f}")