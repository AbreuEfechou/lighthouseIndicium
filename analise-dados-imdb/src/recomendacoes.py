# recomendacoes.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class Recommender:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.data['Overview'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_recommendations(self, title, num_recommendations=5):
        if title not in self.data['Title'].values:
            return "Título não encontrado na base de dados."

        idx = self.data.index[self.data['Title'] == title].tolist()[0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations + 1]
        movie_indices = [i[0] for i in sim_scores]

        return self.data['Title'].iloc[movie_indices].tolist()

# Exemplo de uso:
# recommender = Recommender('data/desafio_indicium_imdb.csv')
# print(recommender.get_recommendations('Título do Filme Exemplo'))