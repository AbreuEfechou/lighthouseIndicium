import pickle
import pandas as pd

def formatar_numero(valor):
    """Formatar número para legibilidade"""
    if valor >= 1_000_000_000:
        return f"${valor/1_000_000_000:.2f}B"
    elif valor >= 1_000_000:
        return f"${valor/1_000_000:.2f}M"
    elif valor >= 1_000:
        return f"${valor/1_000:.1f}K"
    else:
        return f"${valor:,.0f}"

def limpar_valor_monetario(valor):
    """Limpar valor monetário da coluna Gross"""
    if pd.isna(valor):
        return 0
    if isinstance(valor, str):
        valor_limpo = ''.join(c for c in valor if c.isdigit() or c == '.')
        return float(valor_limpo) if valor_limpo else 0
    return float(valor)

def limpar_runtime(valor):
    """Extrair minutos da coluna Runtime"""
    if pd.isna(valor):
        return 0
    if isinstance(valor, str):
        # Extrair números da string (ex: "142 min" -> 142)
        import re
        numeros = re.findall(r'\d+', valor)
        return int(numeros[0]) if numeros else 0
    return valor

def padronizar_certificados(certificado):
    """Padronizar classificações indicativas"""
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

print("📦 Carregando modelo...")
try:
    with open('modelo_imdb.pkl', 'rb') as f:
        modelo = pickle.load(f)
    print("✅ Modelo carregado com sucesso!")
    print(f"📊 Métricas do modelo: MAE={modelo['metrics']['MAE']:.3f}, R²={modelo['metrics']['R2']:.3f}")
    
except FileNotFoundError:
    print("❌ Arquivo modelo_imdb.pkl não encontrado!")
    print("⚠️ Execute primeiro: python modelo_imdb.py")
    exit()

shawshank_data = {
    'Series_Title': 'The Shawshank Redemption',
    'Released_Year': '1994',
    'Certificate': 'A',
    'Runtime': '142 min',
    'Genre': 'Drama',
    'Overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
    'Meta_score': 80.0,
    'Director': 'Frank Darabont',
    'Star1': 'Tim Robbins',
    'Star2': 'Morgan Freeman',
    'Star3': 'Bob Gunton',
    'Star4': 'William Sadler',
    'No_of_Votes': 2343110,
    'Gross': '28,341,469'
}

print("\n🎬 PREPARANDO DADOS DO FILME:")
print("=" * 40)

gross = limpar_valor_monetario(shawshank_data['Gross'])
runtime = limpar_runtime(shawshank_data['Runtime'])
meta_score = shawshank_data['Meta_score']
num_votes = shawshank_data['No_of_Votes']
certificate = padronizar_certificados(shawshank_data['Certificate'])
genre = shawshank_data['Genre']

print(f"📝 Título: {shawshank_data['Series_Title']}")
print(f"📅 Ano: {shawshank_data['Released_Year']}")
print(f"💰 Bilheteria: {formatar_numero(gross)} (original: {shawshank_data['Gross']})")
print(f"⏰ Duração: {runtime} min (original: {shawshank_data['Runtime']})")
print(f"⭐ Meta Score: {meta_score}")
print(f"🗳️ Número de Votos: {num_votes:,}")
print(f"📋 Certificado: {certificate} (original: {shawshank_data['Certificate']})")
print(f"🎭 Gênero: {genre}")

def prever_nota_imdb(modelo_data, gross, runtime, meta_score, num_votes, certificate, genre):
    """Fazer previsão de nota IMDB"""
    pipeline = modelo_data['pipeline']
    label_encoders = modelo_data['label_encoders']
    
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
        if certificate in le.classes_:
            input_data[col] = le.transform([certificate])[0]
        else:
            input_data[col] = -1
    
    
    predicao = pipeline.predict(input_data)[0]
    
    return predicao


print("\n🤖 FAZENDO PREVISÃO:")
print("=" * 40)

nota_prevista = prever_nota_imdb(modelo, gross, runtime, meta_score, num_votes, certificate, genre)

print(f"🎯 Nota IMDB Prevista: {nota_prevista:.2f}/10")

# Nota real do filme (para comparação)
# The Shawshank Redemption tem 9.3 no IMDB
nota_real = 9.3
diferenca = abs(nota_prevista - nota_real)

print(f"⭐ Nota IMDB Real: {nota_real}/10")
print(f"📊 Diferença: {diferenca:.2f} pontos")

if diferenca <= 0.5:
    print("✅ Previsão EXCELENTE! (diferença ≤ 0.5)")
elif diferenca <= 1.0:
    print("⚠️ Previsão BOA! (diferença ≤ 1.0)")
elif diferenca <= 1.5:
    print("📉 Previsão RAZOÁVEL! (diferença ≤ 1.5)")
else:
    print("❌ Previsão precisa ser melhorada")

