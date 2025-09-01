"""
MÓDULO: database.py
DESCRIÇÃO: Gerencia o banco de dados SQLite para armazenar jogos e usuários
HABILIDADES: SQL, SQLite, CRUD Operations, Data Modeling
"""

import sqlite3
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_name='games.db'):
        """
        Inicializa o gerenciador do banco de dados
        db_name: nome do arquivo do banco de dados SQLite
        """
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com tabelas necessárias"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Tabela de jogos
        c.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                platform TEXT NOT NULL,
                price REAL,
                rating REAL,
                description TEXT,
                tags TEXT  -- Armazena tags como JSON string
            )
        ''')
        
        # Tabela de usuários (para histórico de buscas)
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                search_history TEXT  -- Armazena histórico como JSON
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Banco de dados inicializado com sucesso")
    
    def insert_sample_data(self):
        """Insere dados de exemplo de jogos"""
        sample_games = [
            {
                'title': 'The Witcher 3: Wild Hunt',
                'genre': 'RPG',
                'platform': 'PC, PS4, XBOX',
                'price': 79.90,
                'rating': 9.7,
                'description': 'RPG de mundo aberto em um universo fantástico',
                'tags': json.dumps(['rpg', 'open-world', 'fantasy', 'story-rich'])
            },
            {
                'title': 'Counter-Strike 2',
                'genre': 'FPS',
                'platform': 'PC',
                'price': 0.00,
                'rating': 9.3,
                'description': 'FPS tático multiplayer competitivo',
                'tags': json.dumps(['fps', 'multiplayer', 'competitive', 'shooter'])
            },
            {
                'title': 'FIFA 23',
                'genre': 'Sports',
                'platform': 'PC, PS5, XBOX',
                'price': 249.90,
                'rating': 8.5,
                'description': 'Simulador de futebol com times e ligas reais',
                'tags': json.dumps(['sports', 'soccer', 'multiplayer', 'simulation'])
            },
            {
                'title': 'The Legend of Zelda: Breath of the Wild',
                'genre': 'Adventure',
                'platform': 'Nintendo Switch',
                'price': 299.90,
                'rating': 9.8,
                'description': 'Aventura épica em mundo aberto',
                'tags': json.dumps(['adventure', 'open-world', 'puzzle', 'action'])
            },
            {
                'title': 'Call of Duty: Warzone',
                'genre': 'FPS',
                'platform': 'PC, PS4, XBOX',
                'price': 0.00,
                'rating': 8.9,
                'description': 'Battle Royale gratuito da série Call of Duty',
                'tags': json.dumps(['fps', 'battle-royale', 'multiplayer', 'shooter'])
            },
            {
                'title': 'Minecraft',
                'genre': 'Sandbox',
                'platform': 'Todas as plataformas',
                'price': 89.90,
                'rating': 9.5,
                'description': 'Jogo sandbox de construção e exploração',
                'tags': json.dumps(['sandbox', 'creative', 'multiplayer', 'exploration'])
            },
            {
                'title': 'Grand Theft Auto V',
                'genre': 'Action',
                'platform': 'PC, PS4, XBOX',
                'price': 129.90,
                'rating': 9.6,
                'description': 'Mundo aberto com história criminal',
                'tags': json.dumps(['open-world', 'action', 'crime', 'multiplayer'])
            },
            {
                'title': 'Fortnite',
                'genre': 'Battle Royale',
                'platform': 'Todas as plataformas',
                'price': 0.00,
                'rating': 8.7,
                'description': 'Battle Royale com construção e elementos únicos',
                'tags': json.dumps(['battle-royale', 'shooter', 'multiplayer', 'building'])
            }
        ]
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        for game in sample_games:
            c.execute('''
                INSERT OR IGNORE INTO games (title, genre, platform, price, rating, description, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                game['title'], game['genre'], game['platform'], game['price'],
                game['rating'], game['description'], game['tags']
            ))
        
        conn.commit()
        conn.close()
        print("Dados de exemplo inseridos com sucesso")
    
    def get_all_games(self):
        """Retorna todos os jogos do banco SEM DUPLICATAS"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # GROUP BY title para evitar duplicatas
        c.execute('''
            SELECT *, MIN(id) as min_id 
            FROM games 
            GROUP BY title 
            ORDER BY title
        ''')
        
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

    def get_game_by_title(self, title):
        """Busca jogo pelo título (case insensitive)"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM games WHERE LOWER(title) LIKE LOWER(?)', (f'%{title}%',))
        
        columns = [description[0] for description in c.description]
        games = []
        
        for row in c.fetchall():
            game = dict(zip(columns, row))
            game['tags'] = json.loads(game['tags'])
            games.append(game)
        
        conn.close()
        return games

# Teste do módulo
if __name__ == '__main__':
    db = DatabaseManager()
    db.insert_sample_data()

    print("Jogos no banco:", len(db.get_all_games()))
