import random

try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

class DifficultyAdjuster:
    def __init__(self):
        self.performance_history = []
        self.adjustment_factor = 1.0
        
    def record_battle(self, victory, battle_duration=0, damage_ratio=1.0):
        self.performance_history.append({
            "victory": victory,
            "duration": battle_duration,
            "damage_ratio": damage_ratio
        })
        
        if len(self.performance_history) > 10:
            self.performance_history.pop(0)
            
        self._adjust_difficulty()
        
    def _adjust_difficulty(self):
        if len(self.performance_history) < 3:
            return
            
        recent_battles = self.performance_history[-5:]
        wins = sum(1 for b in recent_battles if b["victory"])
        
        if len(recent_battles) == 0:
            return
            
        win_rate = wins / len(recent_battles)
        
        if win_rate > 0.8:
            self.adjustment_factor = min(1.5, self.adjustment_factor + 0.1)
        elif win_rate < 0.3:
            self.adjustment_factor = max(0.5, self.adjustment_factor - 0.1)
        else:
            self.adjustment_factor = max(0.9, min(1.1, self.adjustment_factor))
            
    def get_adjusted_enemy_stats(self, base_hp, base_attack):
        return {
            "hp": int(base_hp * self.adjustment_factor),
            "attack": int(base_attack * self.adjustment_factor)
        }

class BattlePredictor:
    def __init__(self):
        self.is_trained = False
        if not ML_AVAILABLE:
            return
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self._generate_training_data()
        
    def _generate_training_data(self):
        if not ML_AVAILABLE:
            return
        data = []
        labels = []
        
        for _ in range(1000):
            player_level = random.randint(1, 10)
            player_hp = random.randint(50, 200)
            player_attack = random.randint(10, 50)
            player_defense = random.randint(2, 15)
            enemy_hp = random.randint(30, 150)
            enemy_attack = random.randint(8, 40)
            
            player_power = player_level * 15 + player_hp * 0.3 + player_attack * 3 + player_defense * 2
            enemy_power = enemy_hp * 0.8 + enemy_attack * 3
            
            player_power *= random.uniform(0.8, 1.2)
            enemy_power *= random.uniform(0.8, 1.2)
            
            victory = 1 if player_power > enemy_power else 0
            
            data.append([player_level, player_hp, player_attack, player_defense, enemy_hp, enemy_attack])
            labels.append(victory)
            
        self.X_train = np.array(data)
        self.y_train = np.array(labels)
        self._train_model()
        
    def _train_model(self):
        if not ML_AVAILABLE:
            return
        X_scaled = self.scaler.fit_transform(self.X_train)
        self.model.fit(X_scaled, self.y_train)
        self.is_trained = True
        
    def predict_victory_chance(self, player, enemy):
        if not ML_AVAILABLE or not self.is_trained:
            return self._simple_prediction(player, enemy)
            
        features = [
            player.level,
            player.hp,
            player.attack,
            player.defense,
            enemy.hp,
            enemy.attack
        ]
        
        features_scaled = self.scaler.transform([features])
        probability = self.model.predict_proba(features_scaled)[0][1]
        return probability * 100
    
    def _simple_prediction(self, player, enemy):
        player_power = (player.level * 15 + player.hp * 0.3 + 
                       player.attack * 3 + player.defense * 2)
        enemy_power = enemy.hp * 0.8 + enemy.attack * 3
        
        total_power = player_power + enemy_power
        if total_power == 0:
            return 50.0
        
        return (player_power / total_power) * 100
