import tkinter as tk
from tkinter import messagebox

class SceneManager:
    def __init__(self, canvas, root, player):
        self.canvas = canvas
        self.root = root
        self.player = player
        self.current_scene = 1
        
    def show_loading(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 300, text="Carregando...", fill="white", font=("Arial", 20))
        
    def setup_scene1(self):
        self.canvas.delete("all")
        # Porta
        self.canvas.create_rectangle(350, 200, 450, 400, fill="brown", outline="black", width=3)
        self.canvas.create_text(400, 100, text="Cenário 1 - Guilda", fill="white", font=("Arial", 16))
        
        # Protagonista sai da porta
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.after(1000, self.show_guild_dialog)
        
    def show_guild_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Líder da Guilda")
        dialog.geometry("500x400")
        tk.Label(dialog, text="Líder da Guilda:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Sua missão é simples: siga pelas estradas ao leste\ne investigue os desaparecimentos.\nNão volte sem respostas.", 
                wraplength=450, justify="center").pack(pady=10)
        
        tk.Label(dialog, text="Escolha sua resposta:", font=("Arial", 11, "bold")).pack(pady=(20,10))
        
        responses = [
            "Missão simples... Isso sempre acaba em morte.",
            "Entendido... Voltarei, com respostas ou talvez com ainda mais perguntas.",
            "Voltarei quando o silêncio for seguro novamente.",
            "..."
        ]
        
        for i, response in enumerate(responses):
            tk.Button(dialog, text=f"{i+1} - {response}", wraplength=400,
                     command=lambda r=i+1: [dialog.destroy(), self.handle_guild_response(r)]).pack(pady=5, fill="x", padx=20)
                     
    def handle_guild_response(self, response):
        responses_dict = {
            1: "Então morra tentando, se for preciso. Só não morra em vão.",
            2: "Perguntas também servem... Desde que venham manchadas de verdades.",
            3: "O silêncio nunca é seguro, garoto. Só muda o que o provoca.",
            4: "Sem palavras? Melhor assim. Palavras não salvam ninguém, mas aço e coragem talvez salvem... Cuide-se."
        }
        
        result_dialog = tk.Toplevel(self.root)
        result_dialog.title("Resposta do Líder")
        result_dialog.geometry("400x200")
        
        tk.Label(result_dialog, text="Líder da Guilda:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(result_dialog, text=responses_dict[response], wraplength=350, justify="center").pack(pady=20)
        
        tk.Button(result_dialog, text="Continuar", 
                 command=lambda: [result_dialog.destroy(), self.transition_to_scene2()]).pack(pady=20)
        
    def transition_to_scene2(self):
        self.show_loading()
        self.root.after(1500, self.setup_scene2)
        
    def setup_scene2(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 50, text="Cenário 2 - Caminho", fill="white", font=("Arial", 16))
        self.player.x = 50
        self.canvas.create_rectangle(0, 250, 800, 350, fill="gray")
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.bind("<Key>", self.move_player_scene2)
        self.root.focus_set()
        
    def move_player_scene2(self, event):
        if event.keysym == "Right" and self.player.x < 750:
            self.player.move(10, 0)
            self.canvas.coords(self.player_sprite, self.player.x-15, self.player.y-15, 
                             self.player.x+15, self.player.y+15)
            if self.player.x >= 750:
                self.root.unbind("<Key>")
                self.transition_to_scene3()
                
    def transition_to_scene3(self):
        self.show_loading()
        self.root.after(1500, self.setup_scene3)
        
    def setup_scene3(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 50, text="Cenário 3 - Cidade", fill="white", font=("Arial", 16))
        # Casa com janela
        self.canvas.create_rectangle(600, 200, 750, 350, fill="brown")
        self.canvas.create_rectangle(650, 220, 700, 270, fill="lightblue", outline="black", width=2)
        
        # Árvore com papel
        self.canvas.create_rectangle(150, 180, 170, 350, fill="brown")  # Tronco
        self.canvas.create_oval(120, 150, 200, 220, fill="green")  # Copa
        self.canvas.create_rectangle(155, 200, 165, 210, fill="white", outline="black")  # Papel
        self.canvas.create_text(160, 230, text="Papel", fill="yellow", font=("Arial", 10))
        
        self.player.x = 50
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        self.steps = 0
        self.paper_collected = False
        
        self.root.bind("<Key>", self.move_player_scene3)
        self.root.focus_set()
        
    def move_player_scene3(self, event):
        if event.keysym == "Right" and self.player.x < 750:
            self.player.move(10, 0)
            self.steps += 1
            self.canvas.coords(self.player_sprite, self.player.x-15, self.player.y-15, 
                             self.player.x+15, self.player.y+15)
            
            # Verificar se está perto da árvore para pegar o papel
            if 130 <= self.player.x <= 180 and not self.paper_collected:
                self.show_paper_option()
            
            if self.steps == 2:
                self.root.unbind("<Key>")
                return "spawn_enemy"
            elif self.player.x >= 750:
                self.root.unbind("<Key>")
                return "move_to_scene4"
        return None
        
    def show_paper_option(self):
        paper_dialog = tk.Toplevel(self.root)
        paper_dialog.title("Papel na Árvore")
        paper_dialog.geometry("300x150")
        
        tk.Label(paper_dialog, text="Você encontrou um papel pregado na árvore.", 
                wraplength=250, justify="center").pack(pady=20)
        
        def collect_paper():
            self.player.add_item("Papel Misterioso")
            self.paper_collected = True
            # Remover papel do canvas
            self.canvas.delete("all")
            self.setup_scene3_after_paper()
            paper_dialog.destroy()
            
        def ignore_paper():
            paper_dialog.destroy()
            
        tk.Button(paper_dialog, text="Pegar Papel", command=collect_paper).pack(side="left", padx=20, pady=10)
        tk.Button(paper_dialog, text="Ignorar", command=ignore_paper).pack(side="right", padx=20, pady=10)
        
    def setup_scene3_after_paper(self):
        self.canvas.create_text(400, 50, text="Cenário 3 - Cidade", fill="white", font=("Arial", 16))
        # Casa com janela
        self.canvas.create_rectangle(600, 200, 750, 350, fill="brown")
        self.canvas.create_rectangle(650, 220, 700, 270, fill="lightblue", outline="black", width=2)
        
        # Árvore sem papel
        self.canvas.create_rectangle(150, 180, 170, 350, fill="brown")
        self.canvas.create_oval(120, 150, 200, 220, fill="green")
        
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        
    def continue_scene3(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 50, text="Cenário 3 - Cidade", fill="white", font=("Arial", 16))
        self.canvas.create_rectangle(600, 200, 750, 350, fill="brown")
        
        # Mostrar árvore com ou sem papel
        self.canvas.create_rectangle(150, 180, 170, 350, fill="brown")
        self.canvas.create_oval(120, 150, 200, 220, fill="green")
        
        if not self.paper_collected:
            self.canvas.create_rectangle(155, 200, 165, 210, fill="white", outline="black")
            self.canvas.create_text(160, 230, text="Papel", fill="yellow", font=("Arial", 10))
            
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        
        # Oferecer papel após batalha se não foi coletado
        if not self.paper_collected:
            self.show_post_battle_paper_option()
        else:
            self.root.bind("<Key>", self.move_to_scene4_key)
            self.root.focus_set()
            
    def show_post_battle_paper_option(self):
        paper_dialog = tk.Toplevel(self.root)
        paper_dialog.title("Papel na Árvore")
        paper_dialog.geometry("350x200")
        
        tk.Label(paper_dialog, text="Após a batalha, você nota\no papel ainda pregado na árvore.", 
                wraplength=300, justify="center").pack(pady=20)
        
        def collect_paper():
            self.player.add_item("Papel Misterioso")
            self.paper_collected = True
            # Atualizar canvas removendo papel
            self.canvas.delete("all")
            self.canvas.create_text(400, 50, text="Cenário 3 - Cidade", fill="white", font=("Arial", 16))
            self.canvas.create_rectangle(600, 200, 750, 350, fill="brown")
            self.canvas.create_rectangle(150, 180, 170, 350, fill="brown")
            self.canvas.create_oval(120, 150, 200, 220, fill="green")
            self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                        self.player.x+15, self.player.y+15, fill="blue")
            paper_dialog.destroy()
            self.root.bind("<Key>", self.move_to_scene4_key)
            self.root.focus_set()
            
        def ignore_paper():
            paper_dialog.destroy()
            self.root.bind("<Key>", self.move_to_scene4_key)
            self.root.focus_set()
            
        tk.Button(paper_dialog, text="Pegar Papel", command=collect_paper).pack(side="left", padx=30, pady=20)
        tk.Button(paper_dialog, text="Ignorar", command=ignore_paper).pack(side="right", padx=30, pady=20)
        
    def move_to_scene4_key(self, event):
        if event.keysym == "Right":
            self.root.unbind("<Key>")
            return "move_to_scene4"
        return None
        
    def transition_to_scene4(self):
        self.show_loading()
        self.root.after(1500, self.setup_scene4)
        
    def setup_scene4(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 50, text="Cenário 4 - Praça", fill="white", font=("Arial", 16))
        
        self.player.x = 50
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.bind("<Key>", self.move_player_scene4)
        self.root.focus_set()
        
    def move_player_scene4(self, event):
        if event.keysym == "Right" and self.player.x < 700:
            self.player.move(10, 0)
            self.canvas.coords(self.player_sprite, self.player.x-15, self.player.y-15, 
                             self.player.x+15, self.player.y+15)
            if self.player.x >= 700:
                self.root.unbind("<Key>")
                return "show_npc_dialog"
        return None
        
    def show_npc_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("NPC Misterioso")
        dialog.geometry("500x400")
        tk.Label(dialog, text="NPC:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Ei!! Estranho... Você aí! Se tem coragem,\nmate a criatura que se esconde no cemitério.\nEla já levou muitos.", 
                wraplength=450, justify="center").pack(pady=10)
        
        tk.Label(dialog, text="Escolha sua resposta:", font=("Arial", 11, "bold")).pack(pady=(20,10))
        
        responses = [
            "Parece que o dia vai ser longo...",
            "Mais um pedido de socorro, mais um peso nas costas.",
            "Se o mal está lá, eu o encontrarei.",
            "..."
        ]
        
        for i, response in enumerate(responses):
            tk.Button(dialog, text=f"{i+1} - {response}", wraplength=400,
                     command=lambda r=i+1: [dialog.destroy(), self.handle_npc_response(r)]).pack(pady=5, fill="x", padx=20)
                     
    def handle_npc_response(self, response):
        responses_dict = {
            1: "Longo para quem fica. Se for encurtar o sofrimento, volte vivo, se puder.",
            2: "Peso ou obrigação, pouco importa. Só peço que não deixe o peso virar mais almas perdidas.",
            3: "Então vá. Começou a se mexer perto do antigo sepultamento. Siga com cuidado.",
            4: "(suspiro) Silêncio é a resposta, que ele fale com seus atos, então. Boa sorte estranho."
        }
        
        result_dialog = tk.Toplevel(self.root)
        result_dialog.title("Resposta do NPC")
        result_dialog.geometry("400x200")
        
        tk.Label(result_dialog, text="NPC:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(result_dialog, text=responses_dict[response], wraplength=350, justify="center").pack(pady=20)
        
        tk.Button(result_dialog, text="Continuar", 
                 command=lambda: [result_dialog.destroy(), self.transition_to_cemetery()]).pack(pady=20)
        
    def transition_to_cemetery(self):
        self.show_loading()
        self.root.after(1500, self.setup_cemetery_entrance)
        
    def setup_cemetery_entrance(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 50, text="Entrada do Cemitério", fill="white", font=("Arial", 16))
        
        # Coveiro
        self.canvas.create_oval(600, 280, 630, 310, fill="gray")
        self.canvas.create_text(615, 250, text="Coveiro", fill="white", font=("Arial", 12))
        
        self.player.x = 100
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        
        self.show_gravedigger_dialog()
        
    def show_gravedigger_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("O Coveiro")
        dialog.geometry("500x400")
        
        tk.Label(dialog, text="Coveiro:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Você não devia seguir em frente.\nAs tumbas estão inquietas... É perigoso demais.", 
                wraplength=400, justify="center").pack(pady=10)
        
        tk.Label(dialog, text="Escolha sua resposta:", font=("Arial", 11, "bold")).pack(pady=(20,10))
        
        responses = [
            "Eu sei que é perigoso, por isso que eu seguirei.",
            "Perigoso? Certeza que já passei por coisa pior.",
            "Se você tem medo, fique. Pois eu devo continuar.",
            "..."
        ]
        
        for i, response in enumerate(responses):
            tk.Button(dialog, text=f"{i+1} - {response}", wraplength=400,
                     command=lambda r=i+1: [dialog.destroy(), self.handle_response(r)]).pack(pady=5, fill="x", padx=20)
                     
    def handle_response(self, response):
        responses_dict = {
            1: "Coragem e loucura andam de mãos dadas... Espero que a sua coragem dure mais do que a vida dos que vieram antes.",
            2: "Todos dizem isso... Até ouvirem o primeiro sussurro vindo do solo. Que a terra tenha piedade de você.",
            3: "Espere... (Ele pega algo do bolso do manto e entrega ao protagonista) Leve isto. Talvez mantenha as sombras afastadas, por um tempo... Proteja aqueles que não podem se proteger.",
            4: "Silêncio, hein? Às vezes é melhor não dizer nada... As paredes daqui escutam."
        }
        
        result_dialog = tk.Toplevel(self.root)
        result_dialog.title("Resposta do Coveiro")
        result_dialog.geometry("500x300")
        
        tk.Label(result_dialog, text="Coveiro:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(result_dialog, text=responses_dict[response], wraplength=450, justify="center").pack(pady=20)
        
        if response == 3:
            self.player.add_item("Vela Funerária do Esquecido")
            tk.Label(result_dialog, text="\nItem recebido: Vela Funerária do Esquecido", 
                    font=("Arial", 10, "bold"), fg="gold").pack(pady=5)
            tk.Label(result_dialog, text="Uma vela de cera branca, com um pavio feito de cabelo humano.\nQuando acesa, seu fogo exala um odor frio e silencioso,\ncapaz de perturbar até os mortos mais inquietos.", 
                    font=("Arial", 9), fg="yellow", wraplength=400, justify="center").pack(pady=5)
            tk.Label(result_dialog, text="Efeito: Todo ataque após a vela ser usada dará +20 de dano à mortos vivos.", 
                    font=("Arial", 9, "bold"), fg="cyan", wraplength=400, justify="center").pack(pady=5)
            
        tk.Button(result_dialog, text="Continuar", 
                 command=lambda: [result_dialog.destroy(), self.enter_cemetery()]).pack(pady=20)
                 
    def enter_cemetery(self):
        self.show_loading()
        self.root.after(1500, self.setup_cemetery_inside)
        
    def setup_cemetery_inside(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 50, text="Dentro do Cemitério", fill="white", font=("Arial", 16))
        
        # Túmulo aberto
        self.canvas.create_rectangle(600, 350, 700, 400, fill="black", outline="gray", width=3)
        self.canvas.create_text(650, 320, text="Túmulo", fill="white", font=("Arial", 12))
        
        self.player.x = 50
        self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                    self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.bind("<Key>", self.move_to_tomb)
        self.root.focus_set()
        
    def move_to_tomb(self, event):
        if event.keysym == "Right" and self.player.x < 550:
            self.player.move(10, 0)
            self.canvas.coords(self.player_sprite, self.player.x-15, self.player.y-15, 
                             self.player.x+15, self.player.y+15)
            if self.player.x >= 550:
                self.root.unbind("<Key>")
                return "spawn_boss"
        return None
        
    def spawn_boss_animation(self):
        # Boss surge do túmulo
        boss = self.canvas.create_oval(650-20, 375-20, 650+20, 375+20, fill="darkred", outline="red", width=3)
        self.canvas.create_text(650, 450, text="BOSS APARECEU!", fill="red", font=("Arial", 16, "bold"))
        
    def show_ending(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="black")
        self.canvas.create_text(400, 250, text="As almas merecem descanso", 
                               fill="white", font=("Arial", 20))
        self.canvas.create_text(400, 300, text="A demo terminou", 
                               fill="gray", font=("Arial", 16))
        self.canvas.create_text(400, 350, text="Obrigado por jogar!", 
                               fill="white", font=("Arial", 14))