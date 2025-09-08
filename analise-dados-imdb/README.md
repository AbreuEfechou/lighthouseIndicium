# Análise de Dados IMDB

Este projeto tem como objetivo realizar uma análise de dados utilizando a base de dados `desafio_indicium_imdb.csv`, que contém informações sobre filmes, como título, ano de lançamento, gênero, sinopse, entre outros. O projeto inclui uma análise exploratória dos dados (EDA), recomendações de filmes e previsão da nota do IMDb.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- **data/**: Contém a base de dados utilizada para a análise.
  - `desafio_indicium_imdb.csv`: Base de dados com informações sobre filmes.

- **notebooks/**: Contém notebooks Jupyter para realizar as análises.
  - `01_eda.ipynb`: Análise exploratória dos dados (EDA).
  - `02_recomendacoes_filmes.ipynb`: Recomendações de filmes.
  - `03_previsao_nota_imdb.ipynb`: Previsão da nota do IMDb.

- **src/**: Contém os scripts Python utilizados nas análises.
  - `eda.py`: Funções e classes para análise exploratória dos dados.
  - `recomendacoes.py`: Lógica para gerar recomendações de filmes.
  - `previsao.py`: Implementação do modelo de previsão da nota do IMDb.
  - `utils.py`: Funções utilitárias para carregamento de dados e pré-processamento.

- **reports/**: Contém relatórios das análises realizadas.
  - `relatorio_eda.md`: Relatório da análise exploratória dos dados.
  - `relatorio_recomendacoes.md`: Relatório sobre as recomendações de filmes.
  - `relatorio_previsao.md`: Relatório sobre a previsão da nota do IMDb.

- **requirements.txt**: Lista de pacotes utilizados no projeto.

- **.gitignore**: Arquivo que especifica quais arquivos ou pastas devem ser ignorados pelo sistema de controle de versão.

## Como Executar o Projeto

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd analise-dados-imdb
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute os notebooks para realizar as análises:
   ```
   jupyter notebook notebooks/
   ```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.