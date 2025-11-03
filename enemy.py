import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        
    def is_alive(self):
        return self.hp > 0
        
    def attack(self):
        return random.randint(self.attack_power - 5, self.attack_power + 5)

class MLEnemyAI:
    def __init__(self, enemy):
        self.enemy = enemy
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.scaler = StandardScaler()
        self.training_data = []
        self.training_labels = []
        self.is_trained = False
        self.action_history = []
        
        # Dados iniciais para treinar o modelo
        self._initialize_training_data()
        
    def _initialize_training_data(self):
        # Dados sintéticos iniciais baseados em estratégias básicas
        initial_data = [
            [100, 80, 1, 0],  # player_hp, enemy_hp, turn, last_player_action -> normal_attack
            [30, 60, 3, 1],   # HP baixo -> aggressive_attack
            [50, 40, 6, 2],   # Batalha longa -> special_attack
            [80, 90, 2, 3],   # Início -> defensive_attack
            [20, 30, 4, 0],   # Ambos com HP baixo -> aggressive_attack
        ]
        
        initial_labels = [0, 1, 2, 3, 1]  # 0=normal, 1=aggressive, 2=special, 3=defensive
        
        self.training_data.extend(initial_data)
        self.training_labels.extend(initial_labels)
        self._train_model()
        
    def _train_model(self):
        if len(self.training_data) >= 5:
            X = np.array(self.training_data)
            y = np.array(self.training_labels)
            
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.is_trained = True
            
    def choose_action(self, player_hp, turn_count, last_player_action=0):
        # Codificar ação do jogador: 0=ataque, 1=item, 2=persuadir, 3=fugir
        features = [player_hp, self.enemy.hp, turn_count, last_player_action]
        
        if self.is_trained:
            try:
                features_scaled = self.scaler.transform([features])
                prediction = self.model.predict(features_scaled)[0]
                
                # Adicionar um pouco de aleatoriedade
                if random.random() < 0.2:
                    prediction = random.randint(0, 3)
                    
                actions = ["normal_attack", "aggressive_attack", "special_attack", "defensive_attack"]
                chosen_action = actions[prediction]
                
                # Armazenar dados para aprendizado futuro
                self.action_history.append((features, prediction))
                
                return chosen_action
            except:
                # Fallback para IA simples se ML falhar
                return self._simple_ai_fallback(player_hp, turn_count)
        else:
            return self._simple_ai_fallback(player_hp, turn_count)
            
    def _simple_ai_fallback(self, player_hp, turn_count):
        if player_hp < 30:
            return "aggressive_attack"
        elif turn_count > 5:
            return "special_attack"
        elif random.random() < 0.3:
            return "defensive_attack"
        else:
            return "normal_attack"
            
    def learn_from_battle(self, battle_result):
        # Aprende com o resultado da batalha
        if self.action_history:
            # Se o inimigo perdeu, ajusta estratégia
            for features, action in self.action_history[-3:]:  # Últimas 3 ações
                if not battle_result:  # Inimigo perdeu
                    # Tenta uma estratégia diferente
                    new_action = (action + 1) % 4
                    self.training_data.append(features)
                    self.training_labels.append(new_action)
                    
            self._train_model()
            
    def get_attack_damage(self, action):
        base_damage = self.enemy.attack_power
        
        multipliers = {
            "normal_attack": 1.0,
            "aggressive_attack": 1.5,
            "special_attack": 1.3,
            "defensive_attack": 0.8
        }
        
        return int(base_damage * multipliers.get(action, 1.0))
            
    def get_action_message(self, action):
        messages = {
            "aggressive_attack": f"{self.enemy.name} ataca ferozmente!",
            "special_attack": f"{self.enemy.name} usa um ataque especial!",
            "defensive_attack": f"{self.enemy.name} ataca cautelosamente!",
            "normal_attack": f"{self.enemy.name} ataca!"
        }
        return messages.get(action, f"{self.enemy.name} ataca!")

# Alias para compatibilidade
EnemyAI = MLEnemyAI