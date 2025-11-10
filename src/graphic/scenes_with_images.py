import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class SceneManagerWithImages:
    def __init__(self, canvas, root, player):
        self.canvas = canvas
        self.root = root
        self.player = player
        self.current_scene = 1
        
        # Paths para assets
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.images_path = os.path.join(base_path, "assets_game", "images")
        self.gifs_path = os.path.join(base_path, "assets_game", "gifs")
        
        # Cache de imagens
        self.images = {}
        self.load_images()
        
    def load_images(self):
        """Carrega todas as imagens"""
        try:
            # Cenários
            for i in range(1, 5):
                img_path = os.path.join(self.images_path, f"cena{i}.png")
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                    self.images[f"cena{i}"] = ImageTk.PhotoImage(img)
            
            # Cemitério
            cem_path = os.path.join(self.images_path, "cemiterio.png")
            if os.path.exists(cem_path):
                img = Image.open(cem_path)
                img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                self.images["cemiterio"] = ImageTk.PhotoImage(img)
            
            # GIFs
            coveiro_path = os.path.join(self.gifs_path, "coveiro.gif")
            if os.path.exists(coveiro_path):
                img = Image.open(coveiro_path)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                self.images["coveiro"] = ImageTk.PhotoImage(img)
            
            loading_path = os.path.join(self.gifs_path, "loading.gif")
            if os.path.exists(loading_path):
                self.loading_gif = Image.open(loading_path)
                self.loading_frames = []
                try:
                    while True:
                        frame = self.loading_gif.copy().resize((1280, 720), Image.Resampling.LANCZOS)
                        self.loading_frames.append(ImageTk.PhotoImage(frame))
                        self.loading_gif.seek(len(self.loading_frames))
                except EOFError:
                    pass
            
            # GIF do Boss animado
            boss_path = os.path.join(self.gifs_path, "finalboss.gif")
            if os.path.exists(boss_path):
                self.boss_gif = Image.open(boss_path)
                self.boss_frames = []
                try:
                    while True:
                        frame = self.boss_gif.copy().resize((200, 200), Image.Resampling.LANCZOS)
                        self.boss_frames.append(ImageTk.PhotoImage(frame))
                        self.boss_gif.seek(len(self.boss_frames))
                except EOFError:
                    pass
            
            # Carregar GIF animado do carrasco parado
            self.player_gif_path = os.path.join(self.gifs_path, "carrasco-parado.gif")
            if os.path.exists(self.player_gif_path):
                self.player_gif = Image.open(self.player_gif_path)
                self.player_frames = []
                try:
                    while True:
                        frame = self.player_gif.copy().resize((300, 300), Image.Resampling.LANCZOS)
                        self.player_frames.append(ImageTk.PhotoImage(frame))
                        self.player_gif.seek(len(self.player_frames))
                except EOFError:
                    pass
                self.current_frame = 0
            
            # Carregar GIF animado do carrasco andando
            self.player_walking_path = os.path.join(self.gifs_path, "spriteandando.gif")
            if os.path.exists(self.player_walking_path):
                self.player_walking_gif = Image.open(self.player_walking_path)
                self.player_walking_frames = []
                self.player_walking_frames_left = []
                try:
                    while True:
                        frame = self.player_walking_gif.copy().resize((300, 300), Image.Resampling.LANCZOS)
                        self.player_walking_frames.append(ImageTk.PhotoImage(frame))
                        frame_left = frame.transpose(Image.FLIP_LEFT_RIGHT)
                        self.player_walking_frames_left.append(ImageTk.PhotoImage(frame_left))
                        self.player_walking_gif.seek(len(self.player_walking_frames))
                except EOFError:
                    pass
                    
        except Exception as e:
            print(f"Erro ao carregar imagens: {e}")
    
    def animate_player(self):
        frames = self.player_frames
        if hasattr(self, 'walking_direction') and self.walking_direction:
            if self.walking_direction == 'right' and hasattr(self, 'player_walking_frames') and len(self.player_walking_frames) > 0:
                frames = self.player_walking_frames
            elif self.walking_direction == 'left' and hasattr(self, 'player_walking_frames_left') and len(self.player_walking_frames_left) > 0:
                frames = self.player_walking_frames_left
        
        if frames and len(frames) > 0:
            if self.current_frame >= len(frames):
                self.current_frame = 0
            self.canvas.itemconfig(self.player_sprite, image=frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.animation_id = self.root.after(100, self.animate_player)
    
    def animate_boss(self):
        if hasattr(self, 'boss_frames') and len(self.boss_frames) > 0:
            self.canvas.itemconfig(self.boss_id, image=self.boss_frames[self.boss_frame_index])
            self.boss_frame_index = (self.boss_frame_index + 1) % len(self.boss_frames)
            self.boss_animation_id = self.root.after(100, self.animate_boss)
    
    def show_loading(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="black")
        if hasattr(self, 'loading_frames') and len(self.loading_frames) > 0:
            self.loading_frame_index = 0
            self.loading_sprite = self.canvas.create_image(640, 360, image=self.loading_frames[0])
            self.animate_loading()
        else:
            self.canvas.create_text(640, 360, text="Carregando...", fill="white", font=("Arial", 20))
    
    def animate_loading(self):
        if hasattr(self, 'loading_frames') and len(self.loading_frames) > 0 and hasattr(self, 'loading_sprite'):
            self.canvas.itemconfig(self.loading_sprite, image=self.loading_frames[self.loading_frame_index])
            self.loading_frame_index = (self.loading_frame_index + 1) % len(self.loading_frames)
            self.loading_anim_id = self.root.after(100, self.animate_loading)
        
    def setup_scene1(self):
        if hasattr(self, 'loading_anim_id'):
            self.root.after_cancel(self.loading_anim_id)
        self.canvas.delete("all")
        
        # Fundo da cena 1
        if "cena1" in self.images:
            self.canvas.create_image(640, 360, image=self.images["cena1"])
        else:
            self.canvas.configure(bg="darkgreen")
            self.canvas.create_rectangle(560, 240, 720, 480, fill="brown", outline="black", width=3)
        
        self.canvas.create_text(640, 60, text="Cenário 1 - Guilda", fill="white", font=("Arial", 16), tags="ui")
        
        # Protagonista
        if hasattr(self, 'player_frames') and len(self.player_frames) > 0:
            self.player_sprite = self.canvas.create_image(self.player.x, self.player.y, image=self.player_frames[0])
            self.animate_player()
        else:
            self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                        self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.after(1000, self.show_guild_dialog)
        
    def show_guild_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Líder da Guilda")
        dialog.geometry("500x400")
        tk.Label(dialog, text="Líder da Guilda:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Sua missão é simples: siga pelas estradas ao leste\\ne investigue os desaparecimentos.\\nNão volte sem respostas.", 
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
        if hasattr(self, 'loading_anim_id'):
            self.root.after_cancel(self.loading_anim_id)
        self.canvas.delete("all")
        
        if "cena2" in self.images:
            self.canvas.create_image(640, 360, image=self.images["cena2"])
        else:
            self.canvas.configure(bg="lightblue")
            self.canvas.create_rectangle(0, 300, 1280, 420, fill="gray")
        
        self.canvas.create_text(640, 60, text="Cenário 2 - Caminho Sombrio", fill="white", font=("Arial", 16), tags="ui")
        
        self.player.x = 50
        self.walking_direction = None
        if hasattr(self, 'player_frames') and len(self.player_frames) > 0:
            self.player_sprite = self.canvas.create_image(self.player.x, self.player.y, image=self.player_frames[0])
            self.current_frame = 0
            self.animate_player()
        else:
            self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                        self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.bind("<KeyPress>", self.move_player_scene2)
        self.root.bind("<KeyRelease>", self.move_player_scene2)
        self.root.focus_set()
        
    def move_player_scene2(self, event):
        if event.type == '2':  # KeyPress
            if event.keysym == "Right" and self.player.x < 1200:
                self.walking_direction = 'right'
                self.player.move(10, 0)
                self.canvas.coords(self.player_sprite, self.player.x, self.player.y)
                if self.player.x >= 600:
                    self.root.unbind("<KeyPress>")
                    self.root.unbind("<KeyRelease>")
                    if hasattr(self, 'animation_id'):
                        self.root.after_cancel(self.animation_id)
                    self.walking_direction = None
                    return "spawn_enemy"
            elif event.keysym == "Left" and self.player.x > 50:
                self.walking_direction = 'left'
                self.player.move(-10, 0)
                self.canvas.coords(self.player_sprite, self.player.x, self.player.y)
        elif event.type == '3':  # KeyRelease
            self.walking_direction = None
        return None
                
    def transition_to_scene3(self):
        self.show_loading()
        self.root.after(1500, self.setup_scene3)
        
    def setup_scene3(self):
        if hasattr(self, 'loading_anim_id'):
            self.root.after_cancel(self.loading_anim_id)
        self.canvas.delete("all")
        
        if "cena3" in self.images:
            self.canvas.create_image(640, 360, image=self.images["cena3"])
        else:
            self.canvas.configure(bg="gray")
        
        self.canvas.create_text(640, 60, text="Cenário 3 - Cidade Abandonada", fill="white", font=("Arial", 16), tags="ui")
        
        self.player.x = 50
        self.walking_direction = None
        if hasattr(self, 'player_frames') and len(self.player_frames) > 0:
            self.player_sprite = self.canvas.create_image(self.player.x, self.player.y, image=self.player_frames[0])
            self.current_frame = 0
            self.animate_player()
        else:
            self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                        self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.bind("<KeyPress>", self.move_player_scene3)
        self.root.bind("<KeyRelease>", self.move_player_scene3)
        self.root.focus_set()
        
    def move_player_scene3(self, event):
        if event.type == '2':  # KeyPress
            if event.keysym == "Right" and self.player.x < 1120:
                self.walking_direction = 'right'
                self.player.move(10, 0)
                self.canvas.coords(self.player_sprite, self.player.x, self.player.y)
                if self.player.x >= 1120:
                    self.root.unbind("<KeyPress>")
                    self.root.unbind("<KeyRelease>")
                    if hasattr(self, 'animation_id'):
                        self.root.after_cancel(self.animation_id)
                    self.walking_direction = None
                    return "show_npc_dialog"
            elif event.keysym == "Left" and self.player.x > 50:
                self.walking_direction = 'left'
                self.player.move(-10, 0)
                self.canvas.coords(self.player_sprite, self.player.x, self.player.y)
        elif event.type == '3':  # KeyRelease
            self.walking_direction = None
        return None
        
    def continue_scene3(self):
        self.transition_to_scene3()
        
    def move_to_scene4_key(self, event):
        return None
        
    def transition_to_scene4(self):
        self.show_loading()
        self.root.after(1500, self.setup_scene4)
        
    def setup_scene4(self):
        if hasattr(self, 'loading_anim_id'):
            self.root.after_cancel(self.loading_anim_id)
        self.canvas.delete("all")
        
        if "cemiterio" in self.images:
            self.canvas.create_image(640, 360, image=self.images["cemiterio"])
        
        self.canvas.create_text(640, 60, text="Cenário 4 - Entrada do Cemitério", fill="white", font=("Arial", 16), tags="ui")
        
        if "coveiro" in self.images:
            self.canvas.create_image(984, 420, image=self.images["coveiro"])
        else:
            self.canvas.create_oval(960, 336, 1008, 372, fill="gray")
        
        self.canvas.create_text(984, 340, text="Coveiro", fill="white", font=("Arial", 12), tags="ui")
        
        self.player.x = 100
        if hasattr(self, 'player_frames') and len(self.player_frames) > 0:
            self.player_sprite = self.canvas.create_image(self.player.x, self.player.y, image=self.player_frames[0])
            self.animate_player()
        else:
            self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                        self.player.x+15, self.player.y+15, fill="blue")
        
        self.show_gravedigger_dialog()
        
    def move_player_scene4(self, event):
        return None
        
    def show_npc_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("NPC Misterioso")
        dialog.geometry("500x400")
        tk.Label(dialog, text="NPC:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Ei!! Estranho... Você aí! Se tem coragem,\\nmate a criatura que se esconde no cemitério.\\nEla já levou muitos.", 
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
                 command=lambda: [result_dialog.destroy(), self.transition_to_scene4()]).pack(pady=20)
        
    def show_gravedigger_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("O Coveiro")
        dialog.geometry("500x400")
        
        tk.Label(dialog, text="Coveiro:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Você não devia seguir em frente.\\nAs tumbas estão inquietas... É perigoso demais.", 
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
            tk.Label(result_dialog, text="\\nItem recebido: Vela Funerária do Esquecido", 
                    font=("Arial", 10, "bold"), fg="gold").pack(pady=5)
            
        tk.Button(result_dialog, text="Continuar", 
                 command=lambda: [result_dialog.destroy(), self.enter_cemetery()]).pack(pady=20)
                 
    def enter_cemetery(self):
        self.show_loading()
        self.root.after(1500, self.setup_cemetery_inside)
        
    def setup_cemetery_inside(self):
        if hasattr(self, 'loading_anim_id'):
            self.root.after_cancel(self.loading_anim_id)
        self.canvas.delete("all")
        
        if "cemiterio" in self.images:
            self.canvas.create_image(640, 360, image=self.images["cemiterio"])
        
        self.canvas.create_text(640, 60, text="Dentro do Cemitério", fill="white", font=("Arial", 16), tags="ui")
        self.canvas.create_rectangle(960, 420, 1120, 480, fill="black", outline="gray", width=3)
        self.canvas.create_text(1040, 384, text="Túmulo", fill="white", font=("Arial", 12), tags="ui")
        
        self.player.x = 50
        self.walking_direction = None
        if hasattr(self, 'player_frames') and len(self.player_frames) > 0:
            self.player_sprite = self.canvas.create_image(self.player.x, self.player.y, image=self.player_frames[0])
            self.current_frame = 0
            self.animate_player()
        else:
            self.player_sprite = self.canvas.create_oval(self.player.x-15, self.player.y-15, 
                                                        self.player.x+15, self.player.y+15, fill="blue")
        
        self.root.bind("<KeyPress>", self.move_to_tomb)
        self.root.bind("<KeyRelease>", self.move_to_tomb)
        self.root.focus_set()
        
    def move_to_tomb(self, event):
        if event.type == '2':  # KeyPress
            if event.keysym == "Right" and self.player.x < 880:
                self.walking_direction = 'right'
                self.player.move(10, 0)
                self.canvas.coords(self.player_sprite, self.player.x, self.player.y)
                if self.player.x >= 880:
                    self.root.unbind("<KeyPress>")
                    self.root.unbind("<KeyRelease>")
                    if hasattr(self, 'animation_id'):
                        self.root.after_cancel(self.animation_id)
                    self.walking_direction = None
                    return "spawn_boss"
            elif event.keysym == "Left" and self.player.x > 50:
                self.walking_direction = 'left'
                self.player.move(-10, 0)
                self.canvas.coords(self.player_sprite, self.player.x, self.player.y)
        elif event.type == '3':  # KeyRelease
            self.walking_direction = None
        return None
        
    def spawn_boss_animation(self):
        if hasattr(self, 'boss_frames') and len(self.boss_frames) > 0:
            self.boss_id = self.canvas.create_image(1040, 450, image=self.boss_frames[0])
            self.boss_frame_index = 0
            self.animate_boss()
        else:
            self.canvas.create_oval(1040-20, 450-20, 1040+20, 450+20, fill="darkred", outline="red", width=3)
        self.canvas.create_text(1040, 560, text="BOSS APARECEU!", fill="red", font=("Arial", 20, "bold"), tags="ui")
        
    def show_ending(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="black")
        self.canvas.create_text(640, 300, text="As almas merecem descanso", 
                               fill="white", font=("Arial", 20))
        self.canvas.create_text(640, 360, text="A demo terminou", 
                               fill="gray", font=("Arial", 16))
        self.canvas.create_text(640, 420, text="Obrigado por jogar!", 
                               fill="white", font=("Arial", 14))
    
    def show_defeat(self):
        for widget in self.root.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        
        self.canvas.delete("all")
        self.canvas.configure(bg="#1a0000")
        
        self.canvas.create_text(640, 200, text="VOCÊ FOI DERROTADO", 
                               fill="#ff0000", font=("Arial", 48, "bold"))
        self.canvas.create_text(640, 280, text="As sombras consumiram sua alma...", 
                               fill="#cc0000", font=("Arial", 20))
        
        btn_frame = tk.Frame(self.root, bg="#1a0000")
        btn_frame.place(relx=0.5, rely=0.6, anchor="center")
        
        tk.Button(btn_frame, text="TENTAR NOVAMENTE", command=lambda: self.retry_game(), 
                 font=("Arial", 14, "bold"), width=20, bg="#8b0000", fg="white").pack(pady=10)
        tk.Button(btn_frame, text="SAIR", command=self.root.quit, 
                 font=("Arial", 14, "bold"), width=20, bg="#4a0000", fg="white").pack(pady=10)
    
    def retry_game(self):
        for widget in self.root.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        self.player.hp = self.player.max_hp
        self.setup_scene1()
