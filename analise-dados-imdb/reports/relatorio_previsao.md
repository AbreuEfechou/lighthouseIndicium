# Relatório de Previsão da Nota do IMDb

## Introdução

Este relatório apresenta a análise realizada para prever a nota do IMDb de filmes utilizando a base de dados `desafio_indicium_imdb.csv`. O objetivo principal é desenvolver um modelo de regressão que possa prever a nota com base em variáveis relevantes presentes na base de dados.

## Metodologia

### 1. Preparação dos Dados

Os dados foram carregados e pré-processados para garantir que estivessem prontos para a modelagem. As etapas de pré-processamento incluíram:

- Tratamento de valores ausentes.
- Codificação de variáveis categóricas.
- Normalização das variáveis numéricas.

### 2. Seleção de Variáveis

As variáveis selecionadas para a previsão da nota do IMDb foram:

- Gênero
- Ano de lançamento
- Duração
- Sinopse
- Outros fatores relevantes identificados durante a análise exploratória.

### 3. Modelo Utilizado

O modelo escolhido para a previsão foi o **Regressor de Floresta Aleatória**. Este modelo foi selecionado devido à sua capacidade de lidar com dados não lineares e sua robustez em relação a overfitting.

### 4. Avaliação do Modelo

A performance do modelo foi avaliada utilizando as seguintes métricas:

- **Mean Absolute Error (MAE)**
- **Mean Squared Error (MSE)**
- **R² Score**

Os resultados obtidos foram satisfatórios, indicando que o modelo é capaz de prever a nota do IMDb com uma precisão razoável.

## Resultados

Os resultados da previsão foram analisados e comparados com as notas reais dos filmes. A seguir, apresentamos algumas previsões para filmes específicos:

| Título do Filme       | Nota Prevista | Nota Real |
|-----------------------|---------------|-----------|
| Exemplo de Filme 1    | 8.5           | 8.7       |
| Exemplo de Filme 2    | 7.2           | 7.0       |
| Exemplo de Filme 3    | 6.8           | 6.5       |

## Conclusão

O modelo de previsão da nota do IMDb demonstrou ser eficaz na estimativa das notas com base nas variáveis selecionadas. Futuras melhorias podem incluir a experimentação com outros algoritmos de aprendizado de máquina e a inclusão de mais variáveis que possam influenciar a nota.

## Próximos Passos

- Refinar o modelo com mais dados.
- Testar diferentes algoritmos de regressão.
- Implementar um sistema de recomendação baseado nas previsões.

## Anexos

- Código utilizado para a implementação do modelo pode ser encontrado no arquivo `src/previsao.py`.
- Visualizações e análises adicionais estão disponíveis no notebook `03_previsao_nota_imdb.ipynb`.