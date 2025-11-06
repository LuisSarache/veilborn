import random

try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    
try:
    from .asset_manager import AssetManager
except ImportError:
    from asset_manager import AssetManager

class BattleDifficultyClassifier:
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
            enemy_hp = random.randint(30, 150)
            enemy_attack = random.randint(8, 40)
            
            player_power = player_level * 10 + player_hp * 0.5 + player_attack * 2
            enemy_power = enemy_hp * 0.7 + enemy_attack * 2.5
            
            power_ratio = enemy_power / player_power if player_power > 0 else 0
            
            if power_ratio < 0.7:
                difficulty = 0
            elif power_ratio < 1.3:
                difficulty = 1
            else:
                difficulty = 2
                
            data.append([player_level, player_hp, player_attack, enemy_hp, enemy_attack])
            labels.append(difficulty)
            
        self.X_train = np.array(data)
        self.y_train = np.array(labels)
        self._train_model()
        
    def _train_model(self):
        if not ML_AVAILABLE:
            return
        X_scaled = self.scaler.fit_transform(self.X_train)
        self.model.fit(X_scaled, self.y_train)
        self.is_trained = True
        
    def predict_difficulty(self, player_stats, enemy_stats):
        if not ML_AVAILABLE or not self.is_trained:
            return self._simple_difficulty(player_stats, enemy_stats)
            
        required_keys = ['level', 'hp', 'attack']
        for key in required_keys:
            if key not in player_stats:
                return self._simple_difficulty(player_stats, enemy_stats)
        if 'hp' not in enemy_stats or 'attack' not in enemy_stats:
            return self._simple_difficulty(player_stats, enemy_stats)
            
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
    
    def _simple_difficulty(self, player_stats, enemy_stats):
        player_power = player_stats.get('hp', 100) * 0.5 + player_stats.get('attack', 20) * 2 + player_stats.get('level', 1) * 10
        enemy_power = enemy_stats.get('hp', 80) * 0.7 + enemy_stats.get('attack', 15) * 2.5
        
        if player_power == 0:
            return "Médio"
        
        power_ratio = enemy_power / player_power
        
        if power_ratio < 0.7:
            return "Fácil"
        elif power_ratio < 1.3:
            return "Médio"
        else:
            return "Difícil"

class VictoryPredictor:
    def __init__(self):
        self.is_trained = False
        if not ML_AVAILABLE:
            return
        self.model = LogisticRegression(random_state=42)
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
        
    def predict_victory(self, player_stats, enemy_stats):
        if not ML_AVAILABLE or not self.is_trained:
            return self._simple_victory(player_stats, enemy_stats)
            
        required_keys = ['level', 'hp', 'attack', 'defense']
        for key in required_keys:
            if key not in player_stats:
                return self._simple_victory(player_stats, enemy_stats)
        if 'hp' not in enemy_stats or 'attack' not in enemy_stats:
            return self._simple_victory(player_stats, enemy_stats)
            
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
    
    def _simple_victory(self, player_stats, enemy_stats):
        player_power = (player_stats.get('level', 1) * 15 + 
                       player_stats.get('hp', 100) * 0.3 + 
                       player_stats.get('attack', 20) * 3 + 
                       player_stats.get('defense', 5) * 2)
        enemy_power = enemy_stats.get('hp', 80) * 0.8 + enemy_stats.get('attack', 15) * 3
        
        total_power = player_power + enemy_power
        if total_power == 0:
            return 0.5
        
        return player_power / total_power

class WeaponRecommender:
    def __init__(self):
        try:
            self.asset_manager = AssetManager()
        except:
            self.asset_manager = None
            
        self.weapons = [
            {"name": "Espada de Ferro", "damage": 15, "required_level": 1, "type": "físico", "character": "carrasco"},
            {"name": "Cajado Arcano", "damage": 25, "required_level": 3, "type": "mágico", "character": "arcano"},
            {"name": "Adaga do Assaltante", "damage": 20, "required_level": 2, "type": "físico", "character": "assaltante"},
            {"name": "Foice do Coveiro", "damage": 18, "required_level": 2, "type": "necromancia", "character": "coveiro"},
            {"name": "Poder Renascido", "damage": 30, "required_level": 5, "type": "divino", "character": "renascido"}
        ]
        
        if self.asset_manager:
            for weapon in self.weapons:
                weapon["asset"] = self.asset_manager.get_character_asset(weapon["character"])
        
    def recommend_weapon(self, player_stats, enemy_stats):
        if not isinstance(player_stats, dict):
            return self.weapons[0] if self.weapons else None
            
        player_level = player_stats.get("level", 1)
        available_weapons = [w for w in self.weapons if w["required_level"] <= player_level]
        
        if not available_weapons:
            return self.weapons[0] if self.weapons else None
            
        player_magic = player_stats.get("magic", 0)
        player_attack = player_stats.get("attack", 0)
        
        if player_magic > player_attack:
            magic_weapons = [w for w in available_weapons if w["type"] == "mágico"]
            if magic_weapons:
                return max(magic_weapons, key=lambda x: x["damage"])
                
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
