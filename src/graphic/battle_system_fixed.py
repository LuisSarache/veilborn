import tkinter as tk
from tkinter import messagebox
import random
import time
import os
from PIL import Image, ImageTk
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
        
        # Assets
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.images_path = os.path.join(base_path, "assets_game", "images")
        self.gifs_path = os.path.join(base_path, "assets_game", "gifs")
        self.battle_bg = None
        self.player_frames = []
        self.enemy_frames = []
        self.load_battle_assets()
        
    def load_battle_assets(self):
        try:
            bg_path = os.path.join(self.images_path, "menu-batalha.png")
            if os.path.exists(bg_path):
                img = Image.open(bg_path)
                img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                self.battle_bg = ImageTk.PhotoImage(img)
                
            player_gif_path = os.path.join(self.gifs_path, "carrasco-parado.gif")
            if os.path.exists(player_gif_path):
                player_gif = Image.open(player_gif_path)
                try:
                    while True:
                        frame = player_gif.copy().resize((250, 250), Image.Resampling.LANCZOS)
                        self.player_frames.append(ImageTk.PhotoImage(frame))
                        player_gif.seek(len(self.player_frames))
                except EOFError:
                    pass
                    
            enemy_gif_path = os.path.join(self.gifs_path, "finalboss.gif")
            if os.path.exists(enemy_gif_path):
                enemy_gif = Image.open(enemy_gif_path)
                try:
                    while True:
                        frame = enemy_gif.copy().resize((250, 250), Image.Resampling.LANCZOS)
                        self.enemy_frames.append(ImageTk.PhotoImage(frame))
                        enemy_gif.seek(len(self.enemy_frames))
                except EOFError:
                    pass
        except:
            pass
        
    def start_battle(self, can_flee=True):
        self.battle_start_time = time.time()
        self.canvas.delete("all")
        
        # Fundo de batalha
        if self.battle_bg:
            self.canvas.create_image(400, 300, image=self.battle_bg)
        else:
            self.canvas.configure(bg="#1a1a1a")
        
        # Análise ML
        player_stats = self.player.get_stats()
        enemy_stats = {"hp": self.enemy.max_hp, "attack": self.enemy.attack_power}
        
        difficulty = self.difficulty_classifier.predict_difficulty(player_stats, enemy_stats)
        victory_chance = self.victory_predictor.predict_victory(player_stats, enemy_stats)
        
        # UI de batalha
        self.canvas.create_text(400, 50, text=f"BATALHA: {self.enemy.name}", 
                               fill="red", font=("Arial", 24, "bold"))
        
        self.canvas.create_text(200, 100, text=f"Dificuldade: {difficulty}", 
                               fill="yellow", font=("Arial", 12))
        self.canvas.create_text(600, 100, text=f"Vitória: {victory_chance*100:.0f}%", 
                               fill="cyan", font=("Arial", 12))
        
        # Sprites
        if self.player_frames:
            self.player_sprite = self.canvas.create_image(175, 275, image=self.player_frames[0], tags="player")
            self.player_frame_index = 0
            self.animate_player()
        else:
            self.canvas.create_oval(150, 250, 200, 300, fill="blue", outline="white", width=2, tags="player")
        self.canvas.create_text(175, 350, text="Você", fill="white", font=("Arial", 12))
        
        if self.enemy_frames:
            self.enemy_sprite = self.canvas.create_image(1050, 275, image=self.enemy_frames[0], tags="enemy")
            self.enemy_frame_index = 0
            self.animate_enemy()
        else:
            self.canvas.create_oval(1025, 250, 1075, 300, fill="red", outline="white", width=2, tags="enemy")
        self.canvas.create_text(1050, 350, text=self.enemy.name, fill="white", font=("Arial", 12))
        
        self.update_battle_display()
        self.create_battle_buttons(can_flee)
        
    def animate_player(self):
        if self.player_frames:
            self.canvas.itemconfig(self.player_sprite, image=self.player_frames[self.player_frame_index])
            self.player_frame_index = (self.player_frame_index + 1) % len(self.player_frames)
            self.player_anim_id = self.root.after(100, self.animate_player)
            
    def animate_enemy(self):
        if self.enemy_frames:
            self.canvas.itemconfig(self.enemy_sprite, image=self.enemy_frames[self.enemy_frame_index])
            self.enemy_frame_index = (self.enemy_frame_index + 1) % len(self.enemy_frames)
            self.enemy_anim_id = self.root.after(100, self.animate_enemy)
    
    def update_battle_display(self):
        # Barras de HP
        # Jogador
        player_hp_percent = self.player.hp / self.player.max_hp
        self.canvas.create_rectangle(50, 450, 350, 470, fill="gray", outline="white")
        self.canvas.create_rectangle(50, 450, 50 + (300 * player_hp_percent), 470, 
                                     fill="green", outline="white")
        self.canvas.create_text(200, 460, text=f"HP: {self.player.hp}/{self.player.max_hp}", 
                               fill="white", font=("Arial", 10, "bold"))
        
        # Inimigo
        enemy_hp_percent = self.enemy.hp / self.enemy.max_hp
        self.canvas.create_rectangle(930, 450, 1230, 470, fill="gray", outline="white")
        self.canvas.create_rectangle(930, 450, 930 + (300 * enemy_hp_percent), 470, 
                                     fill="red", outline="white")
        self.canvas.create_text(1080, 460, text=f"HP: {self.enemy.hp}/{self.enemy.max_hp}", 
                               fill="white", font=("Arial", 10, "bold"))
        
    def create_battle_buttons(self, can_flee):
        if self.button_frame:
            self.button_frame.destroy()
            
        self.button_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.button_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        btn_style = {"font": ("Arial", 12, "bold"), "width": 12, "bg": "#2c2c2c", "fg": "white"}
        
        tk.Button(self.button_frame, text="⚔ Atacar", command=self.attack_menu, **btn_style).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="🎒 Item", command=self.use_item, **btn_style).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="💬 Persuadir", command=self.persuade, **btn_style).grid(row=0, column=2, padx=5)
        
        if can_flee:
            tk.Button(self.button_frame, text="🏃 Fugir", command=self.flee, **btn_style).grid(row=0, column=3, padx=5)
            
    def attack_menu(self):
        attack_window = tk.Toplevel(self.root)
        attack_window.title("Escolha o Ataque")
        attack_window.geometry("350x250")
        attack_window.configure(bg="#1a1a1a")
        
        tk.Label(attack_window, text="Escolha seu Ataque", 
                font=("Arial", 14, "bold"), bg="#1a1a1a", fg="white").pack(pady=15)
        
        attacks = [
            ("⚡ Golpe Rápido", 15),
            ("💥 Ataque Forte", 25),
            ("🌀 Combo", 20),
            ("✨ Ataque Especial", 30)
        ]
        
        for attack_name, damage in attacks:
            tk.Button(attack_window, text=f"{attack_name} ({damage} dano)", 
                     command=lambda a=attack_name, d=damage: [attack_window.destroy(), self.execute_attack(a, d)],
                     font=("Arial", 11), bg="#2c2c2c", fg="white", width=25).pack(pady=5)
                     
    def execute_attack(self, attack_name, base_damage):
        self.last_player_action = 0
        
        total_damage = self.player.deal_damage(base_damage)
        if self.player.has_item("Vela Funerária do Esquecido") and "Especial" in attack_name:
            total_damage += 20
            
        self.enemy.take_damage(total_damage)
        self.total_damage_dealt += total_damage
        
        # Animação de ataque
        self.canvas.create_text(400, 250, text=f"-{total_damage}", 
                               fill="orange", font=("Arial", 24, "bold"), tags="damage")
        self.root.after(500, lambda: self.canvas.delete("damage"))
        
        if self.enemy.is_alive():
            messagebox.showinfo("Ataque", f"{attack_name}!\nCausou {total_damage} de dano!")
            self.canvas.delete("all")
            if self.battle_bg:
                self.canvas.create_image(640, 360, image=self.battle_bg)
            self.canvas.create_text(640, 50, text=f"BATALHA: {self.enemy.name}", 
                                   fill="red", font=("Arial", 24, "bold"))
            if self.player_frames:
                self.player_sprite = self.canvas.create_image(175, 275, image=self.player_frames[0])
                self.animate_player()
            else:
                self.canvas.create_oval(150, 250, 200, 300, fill="blue", outline="white", width=2)
            if self.enemy_frames:
                self.enemy_sprite = self.canvas.create_image(1050, 275, image=self.enemy_frames[0])
                self.animate_enemy()
            else:
                self.canvas.create_oval(1025, 250, 1075, 300, fill="red", outline="white", width=2)
            self.update_battle_display()
            self.enemy_turn()
        else:
            messagebox.showinfo("Vitória", f"Você derrotou {self.enemy.name}!")
            self.player.win_battle()
            self.enemy_ai.learn_from_battle(False)
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
            if self.battle_bg:
                self.canvas.create_image(640, 360, image=self.battle_bg)
            self.canvas.create_text(640, 50, text=f"BATALHA: {self.enemy.name}", 
                                   fill="red", font=("Arial", 24, "bold"))
            if self.player_frames:
                self.player_sprite = self.canvas.create_image(175, 275, image=self.player_frames[0])
                self.animate_player()
            else:
                self.canvas.create_oval(150, 250, 200, 300, fill="blue", outline="white", width=2)
            if self.enemy_frames:
                self.enemy_sprite = self.canvas.create_image(1050, 275, image=self.enemy_frames[0])
                self.animate_enemy()
            else:
                self.canvas.create_oval(1025, 250, 1075, 300, fill="red", outline="white", width=2)
            self.update_battle_display()
        else:
            messagebox.showinfo("Derrota", "Você foi derrotado!")
            self.player.lose_battle()
            self.end_battle(False)
            
    def use_item(self):
        self.last_player_action = 1
        if not self.player.inventory:
            messagebox.showinfo("Inventário", "Inventário vazio!")
            self.enemy_turn()
        else:
            items = "\n".join([f"• {item}" for item in self.player.inventory])
            messagebox.showinfo("Inventário", f"Seus itens:\n\n{items}")
            self.enemy_turn()
                    
    def persuade(self):
        self.last_player_action = 2
        messagebox.showinfo("Persuasão", 
                           "Você: A gente não precisa lutar...\n\n" +
                           f"{self.enemy.name}: (grunhidos)\n\n" +
                           "Você: Acho que não há mais volta...")
        self.enemy_turn()
        
    def flee(self):
        self.last_player_action = 3
        if random.random() < 0.25:
            messagebox.showinfo("Fuga", "Você conseguiu fugir!")
            self.end_battle(True)
        else:
            messagebox.showinfo("Fuga", "Não conseguiu fugir!")
            self.enemy_turn()
            
    def end_battle(self, victory):
        if self.button_frame:
            self.button_frame.destroy()
            
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
