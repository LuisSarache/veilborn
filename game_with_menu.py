#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from player import Player
from enemy import Enemy
from battle_system_fixed import BattleSystem
from scenes_with_images import SceneManagerWithImages
from visualization import GameVisualizer
from ml_system import DifficultyAdjuster

class VeilbornGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Veilborn RPG")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        
        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg="black", highlightthickness=0)
        self.canvas.pack()
        
        # Paths
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.images_path = os.path.join(base_path, "images")
        self.gifs_path = os.path.join(base_path, "gifs")
        
        self.player = None
        self.scene_manager = None
        self.visualizer = None
        self.difficulty_adjuster = None
        
        self.show_main_menu()
        
    def show_main_menu(self):
        self.canvas.delete("all")
        
        # Carregar imagem de menu
        try:
            menu_path = os.path.join(self.gifs_path, "menu.gif")
            if os.path.exists(menu_path):
                img = Image.open(menu_path)
                img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                self.menu_bg = ImageTk.PhotoImage(img)
                self.canvas.create_image(640, 360, image=self.menu_bg)
        except:
            self.canvas.configure(bg="black")
            self.canvas.create_text(640, 200, text="VEILBORN", fill="white", font=("Arial", 48, "bold"))
        
        # Botões do menu
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.place(relx=0.5, rely=0.6, anchor="center")
        
        tk.Button(btn_frame, text="NOVO JOGO", command=self.new_game, 
                 font=("Arial", 16, "bold"), width=20, bg="#2c2c2c", fg="white").pack(pady=10)
        tk.Button(btn_frame, text="SAIR", command=self.root.quit, 
                 font=("Arial", 16, "bold"), width=20, bg="#2c2c2c", fg="white").pack(pady=10)
        
    def new_game(self):
        # Limpar widgets
        for widget in self.root.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        self.player = self.choose_character_class()
        self.scene_manager = SceneManagerWithImages(self.canvas, self.root, self.player)
        self.visualizer = GameVisualizer(self.player)
        self.difficulty_adjuster = DifficultyAdjuster()
        
        self.create_menu()
        self.connect_scene_events()
        self.scene_manager.setup_scene1()
        
    def choose_character_class(self):
        class_window = tk.Toplevel()
        class_window.title("Escolha sua Classe")
        class_window.geometry("400x350")
        class_window.configure(bg="#1a1a1a")
        class_window.transient(self.root)
        class_window.grab_set()
        
        selected_class = tk.StringVar(value="Guerreiro")
        
        tk.Label(class_window, text="Escolha sua Classe", 
                font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white").pack(pady=20)
        
        classes = [
            ("Guerreiro", "Alto HP e Ataque"),
            ("Mago", "Alto Poder Mágico"),
            ("Ladino", "Balanceado")
        ]
        
        for class_name, description in classes:
            frame = tk.Frame(class_window, bg="#1a1a1a")
            frame.pack(pady=8, padx=20, fill="x")
            
            tk.Radiobutton(frame, text=class_name, variable=selected_class, 
                          value=class_name, font=("Arial", 14, "bold"), 
                          bg="#1a1a1a", fg="white", selectcolor="#2c2c2c").pack(anchor="w")
            tk.Label(frame, text=description, font=("Arial", 10), 
                    bg="#1a1a1a", fg="gray").pack(anchor="w", padx=20)
        
        tk.Button(class_window, text="Confirmar", 
                 command=class_window.destroy, 
                 font=("Arial", 14), bg="#2c2c2c", fg="white", width=15).pack(pady=20)
        
        self.root.wait_window(class_window)
        return Player(player_class=selected_class.get())
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        player_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Jogador", menu=player_menu)
        player_menu.add_command(label="Estatísticas", command=self.show_player_stats)
        player_menu.add_command(label="Inventário", command=self.show_inventory)
        
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Análises", menu=analysis_menu)
        analysis_menu.add_command(label="Gráficos", command=self.visualizer.show_stats_window)
        
    def show_player_stats(self):
        stats = self.player.get_stats()
        stats_text = f"""PERSONAGEM
Classe: {self.player.player_class}
Nível: {stats['level']} | XP: {stats['xp']}/{self.player.xp_to_next_level}

ATRIBUTOS
HP: {stats['hp']}/{stats['max_hp']}
Ataque: {stats['attack']} | Defesa: {stats['defense']}
Magia: {stats['magic']}

BATALHAS
Vitórias: {stats['battles_won']} | Derrotas: {stats['battles_lost']}
Dano Causado: {stats['total_damage_dealt']}
Dano Recebido: {stats['total_damage_taken']}"""
        
        messagebox.showinfo("Estatísticas", stats_text)
        
    def show_inventory(self):
        if not self.player.inventory:
            messagebox.showinfo("Inventário", "Inventário vazio!")
        else:
            items = "\n".join([f"• {item}" for item in self.player.inventory])
            messagebox.showinfo("Inventário", f"Seus itens:\n\n{items}")
            
    def spawn_enemy_scene3(self):
        self.canvas.create_oval(665, 235, 685, 255, fill="red", tags="enemy_spawn")
        self.root.after(500, self.start_battle_scene3)
        
    def start_battle_scene3(self):
        base_stats = self.difficulty_adjuster.get_adjusted_enemy_stats(60, 15)
        enemy = Enemy("Bandido", base_stats["hp"], base_stats["attack"])
        
        battle = BattleSystem(self.canvas, self.root, self.player, enemy, 
                            self.on_battle_end_scene3, self.visualizer)
        battle.start_battle(can_flee=True)
        
    def on_battle_end_scene3(self, victory):
        if victory:
            self.scene_manager.continue_scene3()
        else:
            self.scene_manager.show_defeat()
            
    def spawn_boss(self):
        self.scene_manager.spawn_boss_animation()
        self.root.after(2000, self.start_boss_battle)
        
    def start_boss_battle(self):
        base_stats = self.difficulty_adjuster.get_adjusted_enemy_stats(120, 25)
        boss = Enemy("Boss do Cemitério", base_stats["hp"], base_stats["attack"])
        
        battle = BattleSystem(self.canvas, self.root, self.player, boss, 
                            self.on_boss_battle_end, self.visualizer)
        battle.start_battle(can_flee=False)
        
    def on_boss_battle_end(self, victory):
        if victory:
            self.scene_manager.show_ending()
        else:
            self.scene_manager.show_defeat()
            
    def connect_scene_events(self):
        original_move_scene3 = self.scene_manager.move_player_scene3
        original_move_scene4 = self.scene_manager.move_player_scene4
        original_move_tomb = self.scene_manager.move_to_tomb
        original_move_scene4_key = self.scene_manager.move_to_scene4_key
        
        def enhanced_move_scene3(event):
            result = original_move_scene3(event)
            if result == "spawn_enemy":
                self.spawn_enemy_scene3()
            elif result == "move_to_scene4":
                self.scene_manager.transition_to_scene4()
                
        def enhanced_move_scene4(event):
            result = original_move_scene4(event)
            if result == "show_npc_dialog":
                self.scene_manager.show_npc_dialog()
                
        def enhanced_move_tomb(event):
            result = original_move_tomb(event)
            if result == "spawn_boss":
                self.spawn_boss()
                
        def enhanced_move_scene4_key(event):
            result = original_move_scene4_key(event)
            if result == "move_to_scene4":
                self.scene_manager.transition_to_scene4()
                
        self.scene_manager.move_player_scene3 = enhanced_move_scene3
        self.scene_manager.move_player_scene4 = enhanced_move_scene4
        self.scene_manager.move_to_tomb = enhanced_move_tomb
        self.scene_manager.move_to_scene4_key = enhanced_move_scene4_key
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = VeilbornGame()
    game.run()
