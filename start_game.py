#!/usr/bin/env python3
"""
Script de inicialização do jogo Veilborn
Corrige paths e importações antes de iniciar
"""

import sys
import os

# Adicionar diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Verificar arquivos necessários
required_files = [
    'player.py',
    'enemy.py',
    'battle_system.py',
    'scenes.py',
    'visualization.py',
    'ml_system.py'
]

print("=== VEILBORN RPG - INICIANDO ===\n")
print("Verificando arquivos...")

missing_files = []
for file in required_files:
    file_path = os.path.join(current_dir, file)
    if os.path.exists(file_path):
        print(f"[OK] {file}")
    else:
        print(f"[ERRO] {file} não encontrado!")
        missing_files.append(file)

if missing_files:
    print(f"\nERRO: Arquivos faltando: {', '.join(missing_files)}")
    print("Certifique-se de estar na pasta correta.")
    input("Pressione Enter para sair...")
    sys.exit(1)

print("\nTodos os arquivos encontrados!")
print("Iniciando o jogo...\n")

# Importar e iniciar o jogo
try:
    import tkinter as tk
    from tkinter import messagebox
    from player import Player
    from enemy import Enemy
    from battle_system import BattleSystem
    from scenes_with_images import SceneManagerWithImages as SceneManager
    from visualization import GameVisualizer
    from ml_system import DifficultyAdjuster

    class RPGGame:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Veilborn RPG")
            self.root.geometry("800x600")
            self.root.configure(bg="black")
            
            self.canvas = tk.Canvas(self.root, width=800, height=600, bg="darkgreen")
            self.canvas.pack()
            
            self.player = self.choose_character_class()
            self.scene_manager = SceneManager(self.canvas, self.root, self.player)
            self.visualizer = GameVisualizer(self.player)
            self.difficulty_adjuster = DifficultyAdjuster()
            
            self.create_menu()
            self.start_game()
            
        def start_game(self):
            self.scene_manager.setup_scene1()
            
        def choose_character_class(self):
            class_window = tk.Toplevel()
            class_window.title("Escolha sua Classe")
            class_window.geometry("400x300")
            class_window.transient(self.root)
            class_window.grab_set()
            
            selected_class = tk.StringVar(value="Guerreiro")
            
            tk.Label(class_window, text="Escolha sua classe:", font=("Arial", 16, "bold")).pack(pady=20)
            
            classes = [
                ("Guerreiro", "Alto HP e Ataque, Defesa média"),
                ("Mago", "Alto Poder Mágico, HP baixo"),
                ("Ladino", "Ataque e Defesa equilibrados")
            ]
            
            for class_name, description in classes:
                frame = tk.Frame(class_window)
                frame.pack(pady=5, padx=20, fill="x")
                
                tk.Radiobutton(frame, text=class_name, variable=selected_class, 
                              value=class_name, font=("Arial", 12, "bold")).pack(anchor="w")
                tk.Label(frame, text=description, font=("Arial", 10)).pack(anchor="w", padx=20)
                
            def confirm_class():
                class_window.destroy()
                
            tk.Button(class_window, text="Confirmar", command=confirm_class, 
                     font=("Arial", 12)).pack(pady=20)
                     
            self.root.wait_window(class_window)
            return Player(player_class=selected_class.get())
            
        def create_menu(self):
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            player_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Jogador", menu=player_menu)
            player_menu.add_command(label="Ver Estatísticas", command=self.show_player_stats)
            player_menu.add_command(label="Inventário", command=self.show_inventory)
            
            analysis_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Análises", menu=analysis_menu)
            analysis_menu.add_command(label="Gráficos e Estatísticas", command=self.visualizer.show_stats_window)
            
        def show_player_stats(self):
            stats = self.player.get_stats()
            stats_text = f"""INFORMAÇÕES DO PERSONAGEM
Classe: {self.player.player_class}
Nível: {stats['level']}
XP: {stats['xp']} / {self.player.xp_to_next_level}

ATRIBUTOS
HP: {stats['hp']} / {stats['max_hp']}
Ataque: {stats['attack']}
Defesa: {stats['defense']}
Poder Mágico: {stats['magic']}

ESTATÍSTICAS
Batalhas Vencidas: {stats['battles_won']}
Batalhas Perdidas: {stats['battles_lost']}
Dano Total Causado: {stats['total_damage_dealt']}
Dano Total Recebido: {stats['total_damage_taken']}"""
            
            messagebox.showinfo("Estatísticas do Jogador", stats_text)
            
        def show_inventory(self):
            if not self.player.inventory:
                messagebox.showinfo("Inventário", "Inventário vazio!")
            else:
                items_text = "\n".join([f"- {item}" for item in self.player.inventory])
                messagebox.showinfo("Inventário", f"Seus itens:\n{items_text}")
                
        def start_battle_scene3(self):
            base_stats = self.difficulty_adjuster.get_adjusted_enemy_stats(60, 15)
            enemy = Enemy("Bandido", base_stats["hp"], base_stats["attack"])
            
            battle = BattleSystem(self.canvas, self.root, self.player, enemy, 
                                self.on_battle_end_scene3, self.visualizer)
            battle.start_battle(can_flee=True)
            
        def on_battle_end_scene3(self, victory):
            damage_ratio = self.player.total_damage_dealt / max(1, self.player.total_damage_taken)
            self.difficulty_adjuster.record_battle(victory, 30, damage_ratio)
            
            if victory:
                self.scene_manager.continue_scene3()
                
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
                
        def run(self):
            self.connect_scene_events()
            self.root.mainloop()
            
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
            
        def spawn_enemy_scene3(self):
            enemy_sprite = self.canvas.create_oval(675-10, 245-10, 675+10, 245+10, fill="red")
            self.root.after(500, lambda: self.start_battle_scene3())

    # Iniciar o jogo
    game = RPGGame()
    game.run()
    
except Exception as e:
    print(f"\nERRO ao iniciar o jogo: {e}")
    import traceback
    traceback.print_exc()
    print("\nTentando instalar Pillow...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("Pillow instalado! Tente executar o jogo novamente.")
    except:
        print("Erro ao instalar Pillow. Execute: pip install Pillow")
    input("\nPressione Enter para sair...")
    sys.exit(1)
