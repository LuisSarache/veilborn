import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import random

class BattleDifficultyClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self._generate_training_data()
        
    def _generate_training_data(self):
        # Gerar dados simulados para treinamento
        data = []
        labels = []
        
        for _ in range(1000):
            player_level = random.randint(1, 10)
            player_hp = random.randint(50, 200)
            player_attack = random.randint(10, 50)
            enemy_hp = random.randint(30, 150)
            enemy_attack = random.randint(8, 40)
            
            # Calcular dificuldade baseada na diferença de poder
            player_power = player_level * 10 + player_hp * 0.5 + player_attack * 2
            enemy_power = enemy_hp * 0.7 + enemy_attack * 2.5
            
            power_ratio = enemy_power / player_power
            
            if power_ratio < 0.7:
                difficulty = 0  # Fácil
            elif power_ratio < 1.3:
                difficulty = 1  # Médio
            else:
                difficulty = 2  # Difícil
                
            data.append([player_level, player_hp, player_attack, enemy_hp, enemy_attack])
            labels.append(difficulty)
            
        self.X_train = np.array(data)
        self.y_train = np.array(labels)
        self._train_model()
        
    def _train_model(self):
        X_scaled = self.scaler.fit_transform(self.X_train)
        self.model.fit(X_scaled, self.y_train)
        self.is_trained = True
        
    def predict_difficulty(self, player_stats, enemy_stats):
        if not self.is_trained:
            return 1  # Médio como padrão
            
        features = [
            player_stats['level'],
            player_stats['hp'],
            player_stats['attack'],
            enemy_stats['hp'],
            enemy_stats['attack']
        ]
        
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        
        difficulty_names = ["Fácil", "Médio", "Difícil"]
        return difficulty_names[prediction]

class VictoryPredictor:
    def __init__(self):
        self.model = LogisticRegression(random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self._generate_training_data()
        
    def _generate_training_data(self):
        data = []
        labels = []
        
        for _ in range(1000):
            player_level = random.randint(1, 10)
            player_hp = random.randint(50, 200)
            player_attack = random.randint(10, 50)
            player_defense = random.randint(2, 15)
            enemy_hp = random.randint(30, 150)
            enemy_attack = random.randint(8, 40)
            
            # Simular resultado da batalha
            player_power = player_level * 15 + player_hp * 0.3 + player_attack * 3 + player_defense * 2
            enemy_power = enemy_hp * 0.8 + enemy_attack * 3
            
            # Adicionar aleatoriedade
            player_power *= random.uniform(0.8, 1.2)
            enemy_power *= random.uniform(0.8, 1.2)
            
            victory = 1 if player_power > enemy_power else 0
            
            data.append([player_level, player_hp, player_attack, player_defense, enemy_hp, enemy_attack])
            labels.append(victory)
            
        self.X_train = np.array(data)
        self.y_train = np.array(labels)
        self._train_model()
        
    def _train_model(self):
        X_scaled = self.scaler.fit_transform(self.X_train)
        self.model.fit(X_scaled, self.y_train)
        self.is_trained = True
        
    def predict_victory(self, player_stats, enemy_stats):
        if not self.is_trained:
            return 0.5  # 50% como padrão
            
        features = [
            player_stats['level'],
            player_stats['hp'],
            player_stats['attack'],
            player_stats['defense'],
            enemy_stats['hp'],
            enemy_stats['attack']
        ]
        
        features_scaled = self.scaler.transform([features])
        probability = self.model.predict_proba(features_scaled)[0][1]
        return probability

class WeaponRecommender:
    def __init__(self):
        self.weapons = [
            {"name": "Espada de Ferro", "damage": 15, "required_level": 1, "type": "físico"},
            {"name": "Espada Élfica", "damage": 25, "required_level": 3, "type": "físico"},
            {"name": "Cajado Mágico", "damage": 20, "required_level": 2, "type": "mágico"},
            {"name": "Adaga Venenosa", "damage": 18, "required_level": 2, "type": "físico"},
            {"name": "Martelo de Guerra", "damage": 30, "required_level": 5, "type": "físico"}
        ]
        
    def recommend_weapon(self, player_stats, enemy_stats):
        available_weapons = [w for w in self.weapons if w["required_level"] <= player_stats["level"]]
        
        if not available_weapons:
            return None
            
        # Recomendar baseado no tipo de inimigo e stats do jogador
        if player_stats["magic"] > player_stats["attack"]:
            # Jogador mágico - preferir armas mágicas
            magic_weapons = [w for w in available_weapons if w["type"] == "mágico"]
            if magic_weapons:
                return max(magic_weapons, key=lambda x: x["damage"])
                
        # Recomendar arma com maior dano disponível
        return max(available_weapons, key=lambda x: x["damage"])

class DifficultyAdjuster:
    def __init__(self):
        self.performance_history = []
        self.adjustment_factor = 1.0
        
    def record_battle(self, victory, battle_duration, damage_ratio):
        self.performance_history.append({
            "victory": victory,
            "duration": battle_duration,
            "damage_ratio": damage_ratio
        })
        
        # Manter apenas os últimos 10 resultados
        if len(self.performance_history) > 10:
            self.performance_history.pop(0)
            
        self._adjust_difficulty()
        
    def _adjust_difficulty(self):
        if len(self.performance_history) < 3:
            return
            
        recent_battles = self.performance_history[-5:]
        win_rate = sum(1 for b in recent_battles if b["victory"]) / len(recent_battles)
        
        if win_rate > 0.8:  # Muito fácil
            self.adjustment_factor = min(1.5, self.adjustment_factor + 0.1)
        elif win_rate < 0.3:  # Muito difícil
            self.adjustment_factor = max(0.5, self.adjustment_factor - 0.1)
        else:  # Balanceado
            self.adjustment_factor = max(0.9, min(1.1, self.adjustment_factor))
            
    def get_adjusted_enemy_stats(self, base_hp, base_attack):
        return {
            "hp": int(base_hp * self.adjustment_factor),
            "attack": int(base_attack * self.adjustment_factor)
        }