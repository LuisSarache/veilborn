import tkinter as tk
from tkinter import messagebox
import random
import time
from enemy import MLEnemyAI
from ml_system import BattleDifficultyClassifier, VictoryPredictor, WeaponRecommender

class BattleSystem:
    def __init__(self, canvas, root, player, enemy, on_battle_end, visualizer=None):
        self.canvas = canvas
        self.root = root
        self.player = player
        self.enemy = enemy
        self.enemy_ai = MLEnemyAI(enemy)
        self.on_battle_end = on_battle_end
        self.visualizer = visualizer
        
        # ML Systems
        self.difficulty_classifier = BattleDifficultyClassifier()
        self.victory_predictor = VictoryPredictor()
        self.weapon_recommender = WeaponRecommender()
        
        # Battle tracking
        self.turn_count = 0
        self.button_frame = None
        self.last_player_action = 0
        self.battle_start_time = None
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        
    def start_battle(self, can_flee=True):
        self.battle_start_time = time.time()
        self.canvas.delete("all")
        
        # Análise ML pré-batalha
        player_stats = self.player.get_stats()
        enemy_stats = {"hp": self.enemy.max_hp, "attack": self.enemy.attack_power}
        
        difficulty = self.difficulty_classifier.predict_difficulty(player_stats, enemy_stats)
        victory_chance = self.victory_predictor.predict_victory(player_stats, enemy_stats)
        recommended_weapon = self.weapon_recommender.recommend_weapon(player_stats, enemy_stats)
        
        # Exibir análise ML
        self.canvas.create_text(400, 100, text="BATALHA!", fill="red", font=("Arial", 24))
        self.canvas.create_text(400, 130, text=f"{self.enemy.name} apareceu!", fill="white", font=("Arial", 16))
        self.canvas.create_text(400, 160, text=f"Dificuldade: {difficulty}", fill="yellow", font=("Arial", 12))
        self.canvas.create_text(400, 180, text=f"Chance de Vitória: {victory_chance*100:.1f}%", fill="cyan", font=("Arial", 12))
        
        if recommended_weapon:
            self.canvas.create_text(400, 200, text=f"Arma Recomendada: {recommended_weapon['name']}", 
                                   fill="gold", font=("Arial", 10))
        
        self.update_battle_display()
        self.create_battle_buttons(can_flee)
        
    def update_battle_display(self):
        # HP do jogador
        self.canvas.create_text(150, 200, text=f"Jogador HP: {self.player.hp}/{self.player.max_hp}", 
                               fill="green", font=("Arial", 12))
        # HP do inimigo
        self.canvas.create_text(650, 200, text=f"{self.enemy.name} HP: {self.enemy.hp}/{self.enemy.max_hp}", 
                               fill="red", font=("Arial", 12))
        
    def create_battle_buttons(self, can_flee):
        if self.button_frame:
            self.button_frame.destroy()
            
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="bottom", pady=20)
        
        tk.Button(self.button_frame, text="Atacar", command=self.attack_menu, width=10).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="Item", command=self.use_item, width=10).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="Persuadir", command=self.persuade, width=10).grid(row=0, column=2, padx=5)
        
        if can_flee:
            tk.Button(self.button_frame, text="Fugir", command=self.flee, width=10).grid(row=0, column=3, padx=5)
            
    def attack_menu(self):
        attack_window = tk.Toplevel(self.root)
        attack_window.title("Escolha o Ataque")
        attack_window.geometry("300x200")
        
        attacks = [
            ("Golpe Rápido", 15),
            ("Ataque Forte", 25),
            ("Combo", 20),
            ("Ataque Especial", 30)
        ]
        
        for attack_name, damage in attacks:
            tk.Button(attack_window, text=attack_name, 
                     command=lambda a=attack_name, d=damage: [attack_window.destroy(), self.execute_attack(a, d)]).pack(pady=5)
                     
    def execute_attack(self, attack_name, base_damage):
        self.last_player_action = 0  # Ataque
        
        # Calcular dano com bônus do jogador
        total_damage = self.player.deal_damage(base_damage)
        if self.player.has_item("Vela Funerária do Esquecido") and attack_name == "Ataque Especial":
            total_damage += 20
            
        self.enemy.take_damage(total_damage)
        self.total_damage_dealt += total_damage
        
        if self.enemy.is_alive():
            messagebox.showinfo("Ataque", f"Você usou {attack_name}!\nCausou {total_damage} de dano!")
            self.enemy_turn()
        else:
            messagebox.showinfo("Vitória", f"Você derrotou {self.enemy.name}!")
            self.player.win_battle()
            self.enemy_ai.learn_from_battle(False)  # Inimigo perdeu
            self.end_battle(True)
            
    def enemy_turn(self):
        self.turn_count += 1
        action = self.enemy_ai.choose_action(self.player.hp, self.turn_count, self.last_player_action)
        damage = self.enemy_ai.get_attack_damage(action)
        message = self.enemy_ai.get_action_message(action)
        
        actual_damage = self.player.take_damage(damage)
        self.total_damage_taken += actual_damage
        
        if self.player.is_alive():
            messagebox.showinfo("Turno do Inimigo", f"{message}\nVocê recebeu {actual_damage} de dano!")
            self.canvas.delete("all")
            self.canvas.create_text(400, 100, text="BATALHA!", fill="red", font=("Arial", 24))
            self.update_battle_display()
        else:
            messagebox.showinfo("Derrota", "Você foi derrotado!")
            self.player.lose_battle()
            self.end_battle(False)
            
    def use_item(self):
        self.last_player_action = 1  # Item
        if not self.player.inventory:
            messagebox.showinfo("Inventário", "Inventário vazio!")
        else:
            item_window = tk.Toplevel(self.root)
            item_window.title("Inventário")
            item_window.geometry("400x300")
            
            for item in self.player.inventory:
                if item == "Vela Funerária do Esquecido":
                    tk.Label(item_window, text=item, font=("Arial", 12, "bold")).pack(pady=5)
                    tk.Label(item_window, text="Aumenta dano do Ataque Especial em 20 pontos", 
                            font=("Arial", 10), fg="gold").pack(pady=2)
                else:
                    tk.Label(item_window, text=item).pack(pady=5)
        self.enemy_turn()
                    
    def persuade(self):
        self.last_player_action = 2  # Persuadir
        
        persuade_dialog = tk.Toplevel(self.root)
        persuade_dialog.title("Tentativa de Persuasão")
        persuade_dialog.geometry("500x300")
        
        tk.Label(persuade_dialog, text="Protagonista:", font=("Arial", 12, "bold"), fg="blue").pack(pady=10)
        tk.Label(persuade_dialog, text="A gente não precisa lutar...\nAinda há algo humano dentro de você!", 
                wraplength=400, justify="center").pack(pady=10)
        
        tk.Label(persuade_dialog, text="Inimigo:", font=("Arial", 12, "bold"), fg="red").pack(pady=10)
        tk.Label(persuade_dialog, text="(grunhidos baixos e distorcidos)", 
                font=("Arial", 10, "italic"), fg="darkred").pack(pady=5)
        
        tk.Label(persuade_dialog, text="Protagonista:", font=("Arial", 12, "bold"), fg="blue").pack(pady=10)
        tk.Label(persuade_dialog, text="Acho que não há mais volta para você...", 
                wraplength=400, justify="center").pack(pady=10)
        
        tk.Button(persuade_dialog, text="Continuar", 
                 command=lambda: [persuade_dialog.destroy(), self.enemy_turn()]).pack(pady=20)
        
    def flee(self):
        self.last_player_action = 3  # Fugir
        if random.random() < 0.25:
            messagebox.showinfo("Fuga", "Você conseguiu fugir!")
            self.end_battle(True)
        else:
            messagebox.showinfo("Fuga", "Não conseguiu fugir!")
            self.enemy_turn()
            
    def end_battle(self, victory):
        if self.button_frame:
            self.button_frame.destroy()
            
        # Registrar batalha para visualização
        if self.visualizer and self.battle_start_time:
            battle_duration = time.time() - self.battle_start_time
            self.visualizer.record_battle(
                self.enemy.name,
                victory,
                self.total_damage_dealt,
                self.total_damage_taken,
                battle_duration
            )
            
        self.on_battle_end(victory)