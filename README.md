# 🎮 VEILBORN RPG

Um RPG de ação e aventura desenvolvido em Python com duas versões: **Gráfica (Tkinter)** e **Terminal (Text-based)**.

---

## 🗂️ ESTRUTURA DO PROJETO

```
veilborn/
├── 📁 src/
│   ├── 📁 graphic/              # Versão Gráfica (Tkinter)
│   │   ├── game_with_menu.py   # Arquivo principal
│   │   ├── player.py           # Classe do jogador
│   │   ├── enemy.py            # Classe dos inimigos
│   │   ├── battle_system_fixed.py  # Sistema de batalha
│   │   ├── scenes_with_images.py   # Gerenciador de cenas
│   │   ├── ml_system.py        # Sistema de Machine Learning
│   │   ├── visualization.py    # Gráficos de estatísticas
│   │   └── asset_manager.py    # Gerenciador de assets
│   │
│   └── 📁 terminal/             # Versão Terminal
│       ├── main_terminal.py    # Arquivo principal
│       ├── player_terminal.py  # Classe do jogador
│       ├── enemy_terminal.py   # Classe dos inimigos
│       ├── battle_terminal.py  # Sistema de batalha
│       ├── scenes_terminal.py  # 10 cenas completas
│       ├── ml_terminal.py      # Sistema de Machine Learning
│       └── utils_terminal.py   # Funções utilitárias
│
├── 📁 assets_game/              # Assets do jogo
│   ├── 📁 images/              # Imagens (PNG/JPG)
│   │   ├── cena1.png, cena2.png, cena3.png, cena4.png
│   │   ├── cemiterio.png
│   │   ├── menumorte.jpg
│   │   ├── vela.png
│   │   └── balões de diálogo...
│   │
│   └── 📁 gifs/                # Animações (GIF)
│       ├── carrasco-parado.gif
│       ├── coveiro.gif
│       ├── finalboss.gif
│       ├── loading.gif
│       └── menu.gif
│
├── JOGAR_GRAFICO.bat           # Executável (Versão Gráfica)
├── JOGAR_TERMINAL.bat          # Executável (Versão Terminal)
├── requirements.txt            # Dependências
└── README.md                   # Este arquivo
```

---

## 🎮 COMO JOGAR

### **Versão Gráfica (Tkinter)**

#### Executar:
```bash
# Windows
JOGAR_GRAFICO.bat

# Ou diretamente
cd src\graphic
python game_with_menu.py
```

#### Controles:
- **Setas Direcionais (← →)**: Mover personagem
- **Mouse**: Clicar em botões de diálogo e batalha
- **Menu Superior**: Acessar estatísticas e inventário

---

### **Versão Terminal (Text-based)**

#### Executar:
```bash
# Windows
JOGAR_TERMINAL.bat

# Ou diretamente
cd src\terminal
python main_terminal.py
```

#### Controles:
- **Digite números**: Escolher opções
- **ENTER**: Avançar diálogos

---

## 🛠️ INSTALAÇÃO

### **Requisitos:**
- Python 3.8+
- tkinter (incluído no Python padrão)
- Pillow (PIL)
- scikit-learn
- numpy
- matplotlib

### **Instalação:**

```bash
# 1. Clone o repositório
git clone https://github.com/LuisSarache/veilborn.git
cd veilborn

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o jogo
# Versão Gráfica:
JOGAR_GRAFICO.bat

# Versão Terminal:
JOGAR_TERMINAL.bat
```

---

## 📖 HISTÓRIA

### **O Mundo de Veilborn**

Em um mundo onde a linha entre vida e morte se tornou tênue, uma força sombria começou a despertar. Aldeias inteiras desapareceram durante a noite, deixando apenas marcas de garras e o eco de gritos silenciados. O véu que separa os vivos dos mortos está se rasgando, e criaturas ancestrais emergem das sombras.

### **O Protagonista: O Carrasco**

Você é conhecido apenas como "Carrasco" - um caçador de reputação sombria, temido tanto por humanos quanto por criaturas das trevas. Sua lâmina já ceifou incontáveis ameaças, mas nenhuma missão foi tão perigosa quanto esta. A Guilda dos Caçadores te convoca para investigar os desaparecimentos e eliminar a fonte da maldição antes que o mundo seja consumido pela escuridão.

---

## 🎬 HISTÓRIA DA VERSÃO GRÁFICA (DEMO)

### **Cena 1 - A Guilda dos Caçadores**
Na sede da Guilda, o Líder te convoca para uma missão urgente:

> *"Sua missão é simples: siga pelas estradas ao leste e investigue os desaparecimentos. Não volte sem respostas."*

**Suas opções de resposta:**
1. *"Missão simples... Isso sempre acaba em morte."*
2. *"Entendido... Voltarei, com respostas ou talvez com ainda mais perguntas."*
3. *"Voltarei quando o silêncio for seguro novamente."*
4. *"..."* (silêncio)

Cada escolha revela um aspecto diferente do Carrasco e gera uma resposta única do Líder, estabelecendo o tom sombrio da jornada.

### **Cena 2 - Caminho Sombrio**
Você atravessa uma estrada desolada sob um céu cinzento. O vento carrega sussurros de morte. Ao longe, uma silhueta balança pendurada em uma árvore - um enforcado, testemunha silenciosa dos horrores que assolam a região.

### **Cena 3 - Cidade Abandonada**
Ao chegar na cidade, você é emboscado por um **Bandido** corrompido pela escuridão (HP: 150, ATK: 35). Durante a batalha, você tenta persuadi-lo:

> *"A gente não precisa lutar... Ainda há algo humano dentro de você!"*

Mas ele responde apenas com grunhidos distorcidos. Não há mais humanidade nele.

> *"Acho que não há mais volta para você..."*

Após derrotá-lo, um **NPC misterioso** surge das sombras:

> *"Ei!! Estranho... Você aí! Se tem coragem, mate a criatura que se esconde no cemitério. Ela já levou muitos."*

**Suas opções:**
1. *"Parece que o dia vai ser longo..."*
2. *"Mais um pedido de socorro, mais um peso nas costas."*
3. *"Se o mal está lá, eu o encontrarei."*
4. *"..."*

### **Cena 4 - Entrada do Cemitério**
Você chega ao cemitério sob um crepúsculo vermelho-sangue. O **Coveiro**, uma figura encapuzada, te adverte:

> *"Você não devia seguir em frente. As tumbas estão inquietas... É perigoso demais."*

**Suas opções:**
1. *"Eu sei que é perigoso, por isso que eu seguirei."*
2. *"Perigoso? Certeza que já passei por coisa pior."*
3. *"Se você tem medo, fique. Pois eu devo continuar."* ⭐
4. *"..."*

**⭐ ESCOLHA IMPORTANTE:** Se você escolher a opção 3, o Coveiro te entrega um item lendário:

> *"Espere... (Ele pega algo do bolso do manto) Leve isto. Talvez mantenha as sombras afastadas, por um tempo... Proteja aqueles que não podem se proteger."*

**Item Recebido: Vela Funerária do Esquecido**
- *Uma vela de cera branca com pavio feito de cabelo humano. Quando acesa, seu fogo exala um odor frio e silencioso, capaz de perturbar até os mortos mais inquietos.*
- **Efeito:** +20 de dano contra mortos-vivos

### **Cena 5 - Dentro do Cemitério (BOSS FINAL)**
Você adentra o cemitério. Lápides quebradas, névoa densa, e um silêncio mortal. Ao se aproximar de uma tumba antiga, a terra começa a tremer...

**🎬 CUTSCENE:** Um vídeo cinemático mostra a tumba se abrindo e o boss emergindo das profundezas.

**O BOSS DO CEMITÉRIO emerge!** (HP: 220, ATK: 45)

Uma criatura grotesca, fusão de múltiplos cadáveres, com olhos vazios que brilham em vermelho. Não há fuga possível. É matar ou morrer.

**Vitória:** As almas aprisionadas são libertadas. A demo termina com a mensagem:
> *"As almas merecem descanso. A demo terminou. Obrigado por jogar!"*

**Derrota:** Você é consumido pelas sombras. Game Over.

---

## 🎬 HISTÓRIA DA VERSÃO TERMINAL (COMPLETA)

### **Cena 1 - A Guilda dos Caçadores**
Mesmo início da versão gráfica, mas com mais detalhes narrativos e descrições atmosféricas.

### **Cena 2 - Taverna do Viajante**
Antes de partir, você visita a taverna local. Um **Bardo** canta canções sobre heróis caídos. Você pode:
- Comprar poções de cura (30 gold cada)
- Conversar com NPCs sobre rumores
- Descansar para recuperar HP

### **Cena 3 - Floresta Sombria**
Ao atravessar a floresta, você é atacado por uma **Matilha de Lobos** corrompidos (HP: 100, ATK: 25). Seus olhos brilham com uma luz antinatural. Primeira batalha real.

### **Cena 4 - Aldeia Abandonada**
Você encontra uma aldeia completamente vazia. Portas abertas, comida ainda na mesa, mas nenhum corpo. Apenas marcas de garras nas paredes e sangue seco no chão.

Um **sobrevivente** surge, traumatizado:
> *"Eles... eles vieram à noite. Levaram todos. Eu me escondi... sou um covarde..."*

Você pode consolá-lo ou seguir em frente.

### **Cena 5 - Ponte do Troll**
Uma ponte antiga sobre um desfiladeiro. Um **Troll** (HP: 150, ATK: 35) bloqueia a passagem:
> *"Ninguém passa sem pagar o preço... em sangue ou ouro!"*

**Escolhas:**
- Lutar contra o Troll
- Pagar 100 gold (se tiver)
- Tentar negociar (teste de persuasão)

### **Cena 6 - Acampamento de Mercenários**
Você encontra mercenários acampados. Eles oferecem:
- Vender equipamentos
- Informações sobre o cemitério (50 gold)
- Descanso ao redor da fogueira

Se você comprar as informações, eles revelam:
> *"O Necromante... ele está ressuscitando os mortos. Dizem que ele busca algo... uma relíquia antiga enterrada no cemitério."*

### **Cena 7 - Entrada do Cemitério**
Mesma cena da versão gráfica, com o Coveiro e a Vela Funerária.

### **Cena 8 - Cemitério - Área Externa**
Você explora o cemitério. Pode:
- Investigar tumbas (encontrar itens)
- Ler lápides (lore do mundo)
- Seguir sons estranhos

Eventualmente, você é atacado por uma **Horda de Mortos-Vivos** (HP: 180, ATK: 40).

### **Cena 9 - Cripta Profunda**
Você desce para a cripta subterrânea. Paredes cobertas de runas antigas. Um altar no centro com um livro negro aberto.

Um **Espírito Aprisionado** aparece:
> *"Liberte-me... e eu te ajudarei contra ele... o Necromante..."*

**Escolha crucial:**
- Libertar o espírito (ele te ajuda na batalha final)
- Ignorar e seguir sozinho
- Destruir o espírito (ganha XP extra)

### **Cena 10 - Confronto Final - O Necromante Sombrio**
No coração da cripta, você encontra o **Necromante Sombrio** (HP: 250, ATK: 50):

> *"Finalmente... um sacrifício digno. Sua alma fortalecerá meu exército!"*

**Batalha épica final:**
- Se você libertou o espírito, ele enfraquece o Necromante (-50 HP)
- Se você tem a Vela Funerária, causa +20 de dano por turno
- Não há fuga possível

**Vitória:** Você destrói o Necromante e o livro negro. As almas são libertadas. A aldeia está salva.

**Ending:**
> *"A escuridão foi banida... por enquanto. Mas você sabe que outras ameaças virão. O Carrasco nunca descansa. As sombras sempre retornam."*

**Derrota:** Sua alma é absorvida pelo Necromante. Você se torna parte de seu exército morto-vivo.

---

## 🎭 TEMAS E ATMOSFERA

- **Tom Sombrio:** Narrativa dark fantasy com horror gótico
- **Escolhas Morais:** Suas decisões afetam diálogos e recompensas
- **Solidão:** Você está sozinho contra forças sobrenaturais
- **Sacrifício:** Nem todos podem ser salvos
- **Mistério:** O que realmente causou a maldição?

---

## 🧠 SISTEMA DE IA COM MACHINE LEARNING

Ambas as versões incluem IA adaptativa usando **Random Forest** e **Logistic Regression**.

### **Funcionalidades:**

#### 1. **Ajuste Dinâmico de Dificuldade**
- Monitora últimas 10 batalhas
- **Win rate > 80%**: Aumenta HP/ATK dos inimigos em até 50%
- **Win rate < 30%**: Diminui HP/ATK dos inimigos em até 50%

#### 2. **Predição de Vitória**
- Usa Random Forest treinado com 1000 cenários simulados
- Mostra probabilidade de vitória durante batalhas

---

## 📊 ESTATÍSTICAS DO JOGO

### **Personagem: Carrasco**
- **HP Inicial**: 120
- **Ataque**: 30
- **Defesa**: 10
- **Gold Inicial**: 50 (apenas terminal)

### **Inimigos (Versão Gráfica)**
| Inimigo | HP | Ataque | Pode Fugir? |
|---------|-----|--------|-------------|
| Bandido | 150 | 35 | ✅ Sim |
| Boss do Cemitério | 220 | 45 | ❌ Não |

### **Inimigos (Versão Terminal)**
| Inimigo | HP | Ataque | Pode Fugir? |
|---------|-----|--------|-------------|
| Matilha de Lobos | 100 | 25 | ✅ Sim |
| Troll da Ponte | 150 | 35 | ❌ Não |
| Horda de Mortos-Vivos | 180 | 40 | ❌ Não |
| Necromante Sombrio | 250 | 50 | ❌ Não |

*Valores ajustados dinamicamente pela IA*

---

## 🎨 RECURSOS VISUAIS

### **Versão Gráfica:**
- ✅ Resolução: 1280x720
- ✅ Personagem animado (GIF 180x180)
- ✅ Cenários em alta resolução
- ✅ Menu de morte customizado
- ✅ Sprites de NPCs animados
- ✅ Boss animado (GIF 200x200)
- ✅ Cutscene em vídeo (MP4) antes do boss
- ✅ Interface gráfica completa

### **Versão Terminal:**
- ✅ Texto animado (efeito de digitação)
- ✅ Emojis para melhor visualização
- ✅ Cores e formatação
- ✅ 10 Cenas Completas

---

## 👥 CRÉDITOS

**Desenvolvimento:** Equipe Veilborn  
**Engine:** Python + Tkinter  
**IA:** scikit-learn (Random Forest)  
**História:** Narrativa original

---

## 📜 LICENÇA

Este projeto é distribuído sob a licença MIT.

---

**Que sua jornada seja lendária, Carrasco. As sombras aguardam.** ⚔️💀
