# análise_filmes.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analisar_filmes(caminho_csv):
    df = pd.read_csv(caminho_csv)
    df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce').fillna(0)
    
    print("Informações gerais:")
    print(f"Total de filmes: {len(df)}")
    print(f"Período: {df['Released_Year'].min()} - {df['Released_Year'].max()}")
    print(f"Bilheteria total: ${df['Gross'].sum():,.0f}")
    print(f"Bilheteria média por filme: ${df['Gross'].mean():,.0f}")
    
    # Separar gêneros (um filme pode ter múltiplos gêneros)
    genres_list = df['Genre'].str.split(', ').explode()
    genre_stats = genres_list.value_counts()

    plt.figure(figsize=(12, 6))
    genre_stats.head(10).plot(kind='bar')
    plt.title('Filmes por Gênero')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.show()

    # Análise de rentabilidade por gênero
    genre_profit = df.assign(Genre=df['Genre'].str.split(', ')).explode('Genre')
    genre_profit_analysis = genre_profit.groupby('Genre').agg({
        'Gross': ['mean', 'median', 'sum', 'count'],
        'Meta_score': 'mean'
    }).round(2)

    print("Rentabilidade por Gênero:")
    print(genre_profit_analysis.sort_values(('Gross', 'mean'), ascending=False))
    
    # Tendências ao longo dos anos
    yearly_stats = df.groupby('Released_Year').agg({
        'Gross': ['mean', 'sum', 'count'],
        'Meta_score': 'mean',
        'Runtime': 'mean'
    })

    plt.figure(figsize=(14, 8))
    plt.subplot(2, 2, 1)
    yearly_stats[('Gross', 'mean')].plot()
    plt.title('Bilheteria Média por Ano')

    plt.subplot(2, 2, 2)
    yearly_stats[('Gross', 'count')].plot()
    plt.title('Número de Filmes por Ano')

    plt.subplot(2, 2, 3)
    yearly_stats[('Meta_score', 'mean')].plot()
    plt.title('Nota Média por Ano')

    plt.subplot(2, 2, 4)
    yearly_stats[('Runtime', 'mean')].plot()
    plt.title('Duração Média por Ano')

    plt.tight_layout()
    plt.show()

    director_analysis = df.groupby('Director').agg({
        'Gross': ['mean', 'sum', 'count'],
        'Meta_score': 'mean'
    }).sort_values(('Gross', 'mean'), ascending=False)

    print("Top 10 Diretores por Rentabilidade:")
    print(director_analysis.head(10))

    # Análise das estrelas
    stars = pd.concat([df['Star1'], df['Star2'], df['Star3'], df['Star4']])
    star_stats = stars.value_counts()

    # Rentabilidade por ator
    def analyze_star_performance(star_column):
        star_performance = df.groupby(star_column).agg({
            'Gross': ['mean', 'sum'],
            'Meta_score': 'mean'
        }).sort_values(('Gross', 'mean'), ascending=False)
        return star_performance

    star1_perf = analyze_star_performance('Star1')
    print("Top 10 Atores Principais por Rentabilidade:")
    print(star1_perf.head(10))

    # Matriz de correlação
    correlation_matrix = df[['Runtime', 'Meta_score', 'No_of_Votes', 'Gross']].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Matriz de Correlação')
    plt.show()

    # Relação entre nota crítica e bilheteria
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Meta_score'], df['Gross'], alpha=0.5)
    plt.xlabel('Nota Crítica (Meta_score)')
    plt.ylabel('Bilheteria (Gross)')
    plt.title('Relação entre Nota Crítica e Bilheteria')
    plt.show()

    # Filmes mais bem sucedidos (alta bilheteria + boa crítica)
    df['Success_Score'] = (df['Gross'] / df['Gross'].max() * 0.7 + 
                      df['Meta_score'] / 100 * 0.3)

    top_successful = df.nlargest(10, 'Success_Score')[['Series_Title', 'Genre', 'Director', 
                                                 'Gross', 'Meta_score', 'Success_Score']]

    print("Top 10 Filmes Mais Bem Sucedidos:")
    print(top_successful)

    # Identificar padrões dos filmes de maior sucesso
    successful_patterns = df[df['Success_Score'] > 0.7]
    successful_genres = successful_patterns['Genre'].str.split(', ').explode().value_counts()
    successful_directors = successful_patterns['Director'].value_counts()

    print("="*60)
    print("RECOMENDAÇÕES PARA PRÓXIMO FILME")
    print("="*60)

    # Gêneros em crescimento nos últimos 5 anos
    recent_years = df['Released_Year'] >= (df['Released_Year'].max() - 5)
    recent_genres = df[recent_years]['Genre'].str.split(', ').explode().value_counts()
    yearly_trend_analysis = recent_genres.index[:3].tolist()

    print("\n1. GÊNEROS MAIS PROMISSORES:")
    print(f"- Top gêneros rentáveis: {genre_profit_analysis.index[:3].tolist()}")
    print(f"- Gêneros em crescimento: {yearly_trend_analysis}")

    print("\n2. DIRETORES RECOMENDADOS:")
    print(f"- Diretores com melhor custo-benefício: {director_analysis.index[:3].tolist()}")

    runtime_analysis = successful_patterns.groupby('Runtime').size()

    certificate_analysis = successful_patterns['Certificate'].value_counts()

    ideal_specs = {
        'duração_ideal': runtime_analysis.idxmax() if not runtime_analysis.empty else None,
        'classificação_indicativa': certificate_analysis.index[0] if not certificate_analysis.empty else None
    }

    print("\n3. CARACTERÍSTICAS TÉCNICAS IDEIAS:")
    print(f"- Duração ideal: {runtime_analysis.idxmax()[0]}")
    print(f"- Classificação indicativa: {certificate_analysis.index[0]}")

    print("\n4. ELENCO SUGERIDO:")
    print(f"- Atores principais comprovados: {star1_perf.index[:3].tolist()}")

    print("\n5. ESTRATÉGIA TEMPORAL:")
    release_strategy = datetime.now().year + 1
    print(f"- Lançamento ideal: {release_strategy} (baseado em tendências)")

    # Cálculo das variáveis finais
    top_genres = genre_profit_analysis.sort_values(('Gross', 'mean'), ascending=False).index[:3].tolist()
    top_directors = director_analysis.sort_values(('Gross', 'mean'), ascending=False).index[:3].tolist()
    top_stars = star1_perf.sort_values(('Gross', 'mean'), ascending=False).index[:3].tolist()
    ideal_runtime = runtime_analysis.idxmax() if not runtime_analysis.empty else None
    ideal_certificate = certificate_analysis.idxmax() if not certificate_analysis.empty else None

    # Análise de combinações de gêneros (muito importante!)
    df['Genre_List'] = df['Genre'].str.split(', ')
    genre_combinations = df['Genre_List'].apply(lambda x: tuple(sorted(x)) if isinstance(x, list) else (x,))
    combo_stats = genre_combinations.value_counts().head(10)

    print("\nCombinações de Gêneros Mais Comuns:")
    for combo, count in combo_stats.items():
        combo_films = df[df['Genre_List'].apply(lambda x: tuple(sorted(x)) if isinstance(x, list) else (x,)) == combo]
        avg_gross = combo_films['Gross'].mean()
        print(f"{combo}: {count} filmes, Bilheteria média: ${avg_gross:,.0f}")

    # Análise de diretor-ator parcerias de sucesso
    df['Director_Star1'] = df['Director'] + " + " + df['Star1']
    director_star_combo = df.groupby('Director_Star1').agg({
        'Gross': 'mean',
        'Meta_score': 'mean',
        'Series_Title': 'count'
    }).sort_values('Gross', ascending=False)

    print("\nTop Parcerias Diretor-Ator:")
    print(director_star_combo.head(5))

    return {
        'melhores_generos': top_genres,
        'melhores_diretores': top_directors,
        'melhores_atores': top_stars,
        'duracao_ideal': ideal_runtime,
        'certificacao_ideal': ideal_certificate,
        'dados_analise': {
            'total_filmes': len(df),
            'bilheteria_total': df['Gross'].sum(),
            'media_bilheteria': df['Gross'].mean()
        }
    }

# Executar análise
if __name__ == "__main__":
    resultados = analisar_filmes('desafio_indicium_imdb.csv')

    print("Resultados da Análise:")
    for key, value in resultados.items():
        if key != 'dados_analise':
            print(f"{key.replace('_', ' ').title()}: {value}")

    print(f"\nMétricas Gerais:")
    for key, value in resultados['dados_analise'].items():
        print(f"{key.replace('_', ' ').title()}: {value:,.0f}")