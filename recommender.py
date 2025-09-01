"""
MÓDULO: recommender.py - VERSÃO SIMPLIFICADA E FUNCIONAL
DESCRIÇÃO: Sistema de recomendação de games
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

class GameRecommender:  # ← NOME EXATO DA CLASSE
    def __init__(self):
        """
        Inicializa o sistema de recomendação
        """
        print("✅ Inicializando GameRecommender...")
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.games_data = self._get_sample_data()
        
        # Prepara dados para ML
        self._prepare_features()
    
    def _get_sample_data(self):
        """Retorna dados de exemplo"""
        return [
            {
                'id': 1,
                'title': 'The Witcher 3: Wild Hunt',
                'genre': 'RPG',
                'platform': 'PC, PS4, XBOX',
                'price': 79.90,
                'rating': 9.7,
                'description': 'RPG de mundo aberto em universo fantástico',
                'tags': ['rpg', 'open-world', 'fantasy']
            },
            {
                'id': 2,
                'title': 'Counter-Strike 2',
                'genre': 'FPS', 
                'platform': 'PC',
                'price': 0.00,
                'rating': 9.3,
                'description': 'FPS tático multiplayer competitivo',
                'tags': ['fps', 'multiplayer', 'competitive']
            },
            {
                'id': 3,
                'title': 'FIFA 23',
                'genre': 'Sports',
                'platform': 'PC, PS5, XBOX',
                'price': 249.90,
                'rating': 8.5,
                'description': 'Simulador de futebol com times reais',
                'tags': ['sports', 'soccer', 'multiplayer']
            },
            {
                'id': 4,
                'title': 'Cyberpunk 2077',
                'genre': 'RPG',
                'platform': 'PC, PS5, XBOX',
                'price': 199.90,
                'rating': 8.9,
                'description': 'RPG de ação em mundo aberto cyberpunk',
                'tags': ['rpg', 'open-world', 'cyberpunk']
            },
            {
                'id': 5,
                'title': 'Red Dead Redemption 2',
                'genre': 'Action-Adventure',
                'platform': 'PC, PS4, XBOX',
                'price': 189.90,
                'rating': 9.8,
                'description': 'Aventura no velho oeste americano',
                'tags': ['action', 'adventure', 'open-world']
            }
        ]
    
    def _prepare_features(self):
        """Prepara os dados para o modelo ML"""
        # Combina todas as features textuais
        for game in self.games_data:
            game['combined_features'] = (
                f"{game['title']} {game['genre']} {game['platform']} "
                f"{game['description']} {' '.join(game['tags'])}"
            )
        
        # Cria matriz TF-IDF
        texts = [game['combined_features'] for game in self.games_data]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
    
    def recommend_games(self, game_title, top_n=3):
        """
        Recomenda jogos similares baseado no título
        """
        try:
            # Encontra o jogo
            game_index = None
            for i, game in enumerate(self.games_data):
                if game_title.lower() in game['title'].lower():
                    game_index = i
                    break
            
            if game_index is None:
                return self.games_data[:top_n]  # Fallback
            
            # Calcula similaridade
            cosine_sim = cosine_similarity(
                self.tfidf_matrix[game_index], 
                self.tfidf_matrix
            )
            
            # Pega os mais similares
            sim_scores = list(enumerate(cosine_sim[0]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Retorna recomendações (excluindo o próprio jogo)
            recommendations = []
            for i, (idx, score) in enumerate(sim_scores):
                if idx != game_index:  # Não recomenda o mesmo jogo
                    rec_game = self.games_data[idx].copy()
                    rec_game['similarity_score'] = float(score)
                    recommendations.append(rec_game)
                if len(recommendations) >= top_n:
                    break
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Erro na recomendação: {e}")
            return self.games_data[:top_n]  # Fallback
    
    def recommend_by_features(self, features, top_n=3):
        """
        Recomenda baseado em features textuais
        """
        try:
            features_vector = self.vectorizer.transform([features])
            cosine_sim = cosine_similarity(features_vector, self.tfidf_matrix)
            
            sim_scores = list(enumerate(cosine_sim[0]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for i, (idx, score) in enumerate(sim_scores):
                if i >= top_n:
                    break
                rec_game = self.games_data[idx].copy()
                rec_game['similarity_score'] = float(score)
                recommendations.append(rec_game)
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Erro na recomendação por features: {e}")
            return self.games_data[:top_n]

# Teste do módulo
if __name__ == '__main__':
    print("🧪 Testando GameRecommender...")
    recommender = GameRecommender()
    recommendations = recommender.recommend_games("The Witcher 3")
    print("✅ Recomendações:", [r['title'] for r in recommendations])rue)