import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GameVisualizer:
    def __init__(self, player):
        self.player = player
        self.battle_history = []
        
    def record_battle(self, enemy_name, victory, damage_dealt, damage_taken, duration):
        self.battle_history.append({
            "enemy": enemy_name,
            "victory": victory,
            "damage_dealt": damage_dealt,
            "damage_taken": damage_taken,
            "duration": duration,
            "player_level": self.player.level,
            "player_xp": self.player.xp
        })
        
    def show_stats_window(self):
        stats_window = tk.Toplevel()
        stats_window.title("Estatísticas do Jogador")
        stats_window.geometry("800x600")
        
        # Criar notebook para abas
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba 1: Gráficos
        self._create_charts_tab(notebook)
        
        # Aba 2: Tabela de batalhas
        self._create_battles_tab(notebook)
        
        # Aba 3: Estatísticas gerais
        self._create_general_stats_tab(notebook)
        
    def _create_charts_tab(self, notebook):
        chart_frame = ttk.Frame(notebook)
        notebook.add(chart_frame, text="Gráficos")
        
        # Criar figura com subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        # Gráfico 1: Evolução do XP
        if self.battle_history:
            xp_data = [b["player_xp"] for b in self.battle_history]
            ax1.plot(range(len(xp_data)), xp_data, 'b-o')
            ax1.set_title("Evolução do XP")
            ax1.set_xlabel("Batalhas")
            ax1.set_ylabel("XP")
            
        # Gráfico 2: Taxa de vitórias
        if self.battle_history:
            victories = [b["victory"] for b in self.battle_history]
            win_rate = [sum(victories[:i+1])/(i+1) for i in range(len(victories))]
            ax2.plot(range(len(win_rate)), win_rate, 'g-o')
            ax2.set_title("Taxa de Vitórias")
            ax2.set_xlabel("Batalhas")
            ax2.set_ylabel("Taxa de Vitória")
            ax2.set_ylim(0, 1)
            
        # Gráfico 3: Dano por batalha
        if self.battle_history:
            damage_dealt = [b["damage_dealt"] for b in self.battle_history]
            damage_taken = [b["damage_taken"] for b in self.battle_history]
            x = range(len(damage_dealt))
            ax3.bar([i-0.2 for i in x], damage_dealt, 0.4, label="Dano Causado", color='red', alpha=0.7)
            ax3.bar([i+0.2 for i in x], damage_taken, 0.4, label="Dano Recebido", color='blue', alpha=0.7)
            ax3.set_title("Dano por Batalha")
            ax3.set_xlabel("Batalhas")
            ax3.set_ylabel("Dano")
            ax3.legend()
            
        # Gráfico 4: Distribuição de inimigos
        if self.battle_history:
            enemies = [b["enemy"] for b in self.battle_history]
            enemy_counts = pd.Series(enemies).value_counts()
            ax4.pie(enemy_counts.values, labels=enemy_counts.index, autopct='%1.1f%%')
            ax4.set_title("Inimigos Enfrentados")
            
        plt.tight_layout()
        
        # Adicionar gráfico ao tkinter
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def _create_battles_tab(self, notebook):
        battles_frame = ttk.Frame(notebook)
        notebook.add(battles_frame, text="Histórico de Batalhas")
        
        # Criar Treeview para tabela
        columns = ("Inimigo", "Resultado", "Dano Causado", "Dano Recebido", "Duração", "Nível")
        tree = ttk.Treeview(battles_frame, columns=columns, show="headings")
        
        # Configurar cabeçalhos
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
            
        # Adicionar dados
        for i, battle in enumerate(self.battle_history):
            result = "Vitória" if battle["victory"] else "Derrota"
            tree.insert("", "end", values=(
                battle["enemy"],
                result,
                battle["damage_dealt"],
                battle["damage_taken"],
                f"{battle['duration']:.1f}s",
                battle["player_level"]
            ))
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(battles_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def _create_general_stats_tab(self, notebook):
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Estatísticas Gerais")
        
        stats = self.player.get_stats()
        
        # Criar labels com estatísticas
        info_text = f"""
INFORMAÇÕES DO PERSONAGEM
Classe: {self.player.player_class}
Nível: {stats['level']}
XP: {stats['xp']} / {self.player.xp_to_next_level}

ATRIBUTOS
HP: {stats['hp']} / {stats['max_hp']}
Ataque: {stats['attack']}
Defesa: {stats['defense']}
Poder Mágico: {stats['magic']}

ESTATÍSTICAS DE COMBATE
Batalhas Vencidas: {stats['battles_won']}
Batalhas Perdidas: {stats['battles_lost']}
Taxa de Vitória: {stats['battles_won']/(stats['battles_won']+stats['battles_lost'])*100:.1f}% (se houver batalhas)
Dano Total Causado: {stats['total_damage_dealt']}
Dano Total Recebido: {stats['total_damage_taken']}

INVENTÁRIO
Itens: {len(self.player.inventory)}
        """
        
        text_widget = tk.Text(stats_frame, wrap="word", font=("Courier", 12))
        text_widget.insert("1.0", info_text)
        text_widget.config(state="disabled")
        
        scrollbar_text = ttk.Scrollbar(stats_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_text.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar_text.pack(side="right", fill="y")
        
    def generate_ml_report(self, difficulty_classifier, victory_predictor):
        """Gera relatório com insights do ML"""
        if not self.battle_history:
            return "Nenhuma batalha registrada ainda."
            
        df = pd.DataFrame(self.battle_history)
        
        report = f"""
RELATÓRIO DE MACHINE LEARNING

ANÁLISE DE DESEMPENHO:
- Total de batalhas: {len(self.battle_history)}
- Taxa de vitória: {df['victory'].mean()*100:.1f}%
- Dano médio causado: {df['damage_dealt'].mean():.1f}
- Dano médio recebido: {df['damage_taken'].mean():.1f}
- Duração média das batalhas: {df['duration'].mean():.1f}s

INSIGHTS DO MODELO:
- Inimigo mais enfrentado: {df['enemy'].mode().iloc[0] if not df.empty else 'N/A'}
- Melhor performance contra: {df[df['victory']==True]['enemy'].mode().iloc[0] if df['victory'].any() else 'N/A'}
- Pior performance contra: {df[df['victory']==False]['enemy'].mode().iloc[0] if not df['victory'].all() else 'N/A'}

RECOMENDAÇÕES:
- Continue treinando para melhorar a taxa de vitória
- Foque em aumentar o dano causado por batalha
- Considere equipar itens melhores se disponíveis
        """
        
        return report