"""
MÓDULO: app.py - SISTEMA COMPLETO DE RECOMENDAÇÃO DE GAMES
DESCRIÇÃO: Aplicação Flask com API REST e interface web
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# ================= BANCO DE DADOS SIMPLES =================
class DatabaseManager:
    def __init__(self, db_name='games.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco apenas se a tabela não existir"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Verifica se a tabela já existe
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='games'")
        if c.fetchone():
            print("Tabela já existe")
            conn.close()
            return
        
        # Só cria se não existir
        print("Criando tabela pela primeira vez")

        """Inicializa o banco de dados com tabela e dados de exemplo"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Cria tabela se não existir
        c.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                platform TEXT NOT NULL,
                price REAL,
                rating REAL,
                description TEXT,
                tags TEXT
            )
        ''')
        
        # Dados de exemplo
        sample_games = [
            ('The Witcher 3: Wild Hunt', 'RPG', 'PC, PS4, XBOX', 79.90, 9.7, 
             'RPG de mundo aberto em universo fantástico', '["rpg", "open-world", "fantasy", "story-rich"]'),
            
            ('Counter-Strike 2', 'FPS', 'PC', 0.00, 9.3, 
             'FPS tático multiplayer competitivo', '["fps", "multiplayer", "competitive", "shooter"]'),
            
            ('FIFA 23', 'Sports', 'PC, PS5, XBOX', 249.90, 8.5, 
             'Simulador de futebol com times reais', '["sports", "soccer", "multiplayer", "simulation"]'),
            
            ('Cyberpunk 2077', 'RPG', 'PC, PS5, XBOX', 199.90, 8.9, 
             'RPG de ação em mundo aberto cyberpunk', '["rpg", "open-world", "cyberpunk", "futuristic"]'),
            
            ('Red Dead Redemption 2', 'Action-Adventure', 'PC, PS4, XBOX', 189.90, 9.8, 
             'Aventura no velho oeste americano', '["action", "adventure", "open-world", "western"]'),
            
            ('Minecraft', 'Sandbox', 'Todas as plataformas', 89.90, 9.5, 
             'Jogo sandbox de construção e exploração', '["sandbox", "creative", "multiplayer", "exploration"]'),
            
            ('Grand Theft Auto V', 'Action', 'PC, PS4, XBOX', 129.90, 9.6, 
             'Mundo aberto com história criminal', '["open-world", "action", "crime", "multiplayer"]'),
            
            ('Fortnite', 'Battle Royale', 'Todas as plataformas', 0.00, 8.7, 
             'Battle Royale com construção e elementos únicos', '["battle-royale", "shooter", "multiplayer", "building"]')
        ]
        
        # Insere dados
        c.executemany('''
            INSERT OR IGNORE INTO games (title, genre, platform, price, rating, description, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_games)
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
        print("📊 Dados de exemplo inseridos!")
    
    def get_all_games(self):
        """Retorna todos os jogos do banco"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM games ORDER BY title')
        
        games = []
        for row in c.fetchall():
            games.append({
                'id': row[0],
                'title': row[1],
                'genre': row[2],
                'platform': row[3],
                'price': row[4],
                'rating': row[5],
                'description': row[6],
                'tags': json.loads(row[7]) if row[7] else []
            })
        
        conn.close()
        return games

# ================= SISTEMA DE RECOMENDAÇÃO SIMPLES =================
class SimpleRecommender:
    """Sistema de recomendação simplificado e confiável"""
    
    def __init__(self):
        print("Sistema de recomendação simples inicializado")
        self.games = [
            {
                'title': 'The Witcher 3: Wild Hunt',
                'genre': 'RPG',
                'platform': 'PC, PS4, XBOX',
                'price': 79.90,
                'rating': 9.7,
                'description': 'RPG de mundo aberto em universo fantástico',
                'tags': ['rpg', 'open-world', 'fantasy']
            },
            {
                'title': 'Cyberpunk 2077',
                'genre': 'RPG',
                'platform': 'PC, PS5, XBOX',
                'price': 199.90,
                'rating': 8.9,
                'description': 'RPG de ação em mundo aberto cyberpunk',
                'tags': ['rpg', 'open-world', 'cyberpunk']
            },
            {
                'title': 'Red Dead Redemption 2',
                'genre': 'Action-Adventure',
                'platform': 'PC, PS4, XBOX',
                'price': 189.90,
                'rating': 9.8,
                'description': 'Aventura no velho oeste americano',
                'tags': ['action', 'adventure', 'open-world']
            },
            {
                'title': 'Elden Ring',
                'genre': 'RPG',
                'platform': 'PC, PS4, PS5, XBOX',
                'price': 249.90,
                'rating': 9.5,
                'description': 'RPG de ação em mundo aberto dark fantasy',
                'tags': ['rpg', 'open-world', 'fantasy', 'challenging']
            },
            {
                'title': 'God of War',
                'genre': 'Action-Adventure',
                'platform': 'PC, PS4, PS5',
                'price': 199.90,
                'rating': 9.4,
                'description': 'Aventura épica na mitologia nórdica',
                'tags': ['action', 'adventure', 'story-rich', 'norse']
            }
        ]
    
    def recommend_games(self, game_title, top_n=3):
        """Recomenda jogos baseado no título"""
        try:
            # Simula recomendações baseadas no gênero
            target_game = None
            for game in self.games:
                if game_title.lower() in game['title'].lower():
                    target_game = game
                    break
            
            if not target_game:
                return self.games[:top_n]
            
            # Recomenda jogos do mesmo gênero
            recommendations = []
            for game in self.games:
                if game['title'] != target_game['title'] and game['genre'] == target_game['genre']:
                    recommendations.append(game)
                if len(recommendations) >= top_n:
                    break
            
            return recommendations if recommendations else self.games[:top_n]
            
        except Exception as e:
            print(f"Erro na recomendação simples: {e}")
            return self.games[:top_n]
    
    def recommend_by_features(self, features, top_n=3):
        """Recomenda baseado em features textuais"""
        try:
            # Simples matching de keywords
            features_lower = features.lower()
            recommendations = []
            
            for game in self.games:
                score = 0
                game_text = f"{game['title']} {game['genre']} {game['description']} {' '.join(game['tags'])}".lower()
                
                if any(word in game_text for word in features_lower.split()):
                    score += 1
                
                if score > 0:
                    recommendations.append((game, score))
            
            # Ordena por score e retorna
            recommendations.sort(key=lambda x: x[1], reverse=True)
            return [game for game, score in recommendations[:top_n]]
            
        except Exception as e:
            print(f"Erro na recomendação por features: {e}")
            return self.games[:top_n]

# ================= INICIALIZAÇÃO DA APLICAÇÃO =================
print("🎮" + "="*60)
print("🎮 INICIANDO GAME REC - SISTEMA DE RECOMENDAÇÃO DE GAMES")
print("🎮" + "="*60)

# Inicializa banco de dados
db = DatabaseManager()

# Inicializa sistema de recomendação
try:
    # Tenta importar o sistema avançado
    from recommender import GameRecommender
    recommender = GameRecommender()
    print("Sistema de recomendação avançado carregado")
except ImportError as e:
    print(f"Sistema avançado não disponível: {e}")
    print("Usando sistema de recomendação simples")
    recommender = SimpleRecommender()
except Exception as e:
    print(f"Erro no sistema avançado: {e}")
    print("Usando sistema de recomendação simples...")
    recommender = SimpleRecommender()

# ================= ROTAS DA API =================
@app.route('/')
def index():
    """Página principal com interface web"""
    return render_template('index.html')

@app.route('/api/games', methods=['GET'])
def get_games():
    """API: Retorna todos os jogos"""
    try:
        games = db.get_all_games()
        return jsonify({
            'success': True,
            'count': len(games),
            'games': games
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'games': []
        }), 500

@app.route('/api/recommend/title', methods=['GET'])
def recommend_by_title():
    """API: Recomenda jogos por título"""
    try:
        game_title = request.args.get('title', '').strip()
        top_n = int(request.args.get('n', 3))
        
        if not game_title:
            return jsonify({
                'success': False,
                'error': 'Parâmetro "title" é obrigatório'
            }), 400
        
        recommendations = recommender.recommend_games(game_title, top_n)
        
        return jsonify({
            'success': True,
            'input_game': game_title,
            'count': len(recommendations),
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'recommendations': []
        }), 500

@app.route('/api/recommend/features', methods=['POST'])
def recommend_by_features():
    """API: Recomenda jogos por features textuais"""
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "features" é obrigatório no JSON'
            }), 400
        
        features = data['features'].strip()
        top_n = data.get('n', 3)
        
        if not features:
            return jsonify({
                'success': False,
                'error': 'Campo "features" não pode estar vazio'
            }), 400
        
        recommendations = recommender.recommend_by_features(features, top_n)
        
        return jsonify({
            'success': True,
            'input_features': features,
            'count': len(recommendations),
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'recommendations': []
        }), 500

@app.route('/api/search', methods=['GET'])
def search_games():
    """API: Busca jogos por termo"""
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'Parâmetro "q" é obrigatório'
            }), 400
        
        games = db.get_all_games()
        results = [
            game for game in games 
            if search_term.lower() in game['title'].lower() or 
               search_term.lower() in game['genre'].lower() or
               search_term.lower() in game['description'].lower()
        ]
        
        return jsonify({
            'success': True,
            'search_term': search_term,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        }), 500

# ================= MANIPULADORES DE ERRO =================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint não encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Erro interno do servidor'
    }), 500

# ================= EXECUÇÃO PRINCIPAL =================
if __name__ == '__main__':
    print("\n🌐 SERVIDOR INICIADO")
    print("📍 URL: http://localhost:5000")
    print("📍 API: http://localhost:5000/api/games")
    print("🛑 Use Ctrl+C para parar o servidor")
    print("="*60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:

        print(f"\n❌ Erro ao iniciar servidor: {e}")
