# 🎮 VEILBORN RPG

Um RPG de ação e aventura desenvolvido em Python com duas versões: **Gráfica (Tkinter)** e **Terminal (Text-based)**.

---

## 📖 HISTÓRIA COMPLETA

### **O Mundo de Veilborn**

Em um mundo onde a linha entre vida e morte se tornou tênue, uma força sombria começou a despertar. Aldeias inteiras desapareceram durante a noite, deixando apenas marcas de garras e o eco de gritos silenciados. Os mortos não descansam mais em paz - eles caminham novamente, servindo a uma vontade maligna.

### **O Protagonista: O Carrasco**

Você é conhecido apenas como "Carrasco" - um caçador de reputação sombria, temido tanto por humanos quanto por criaturas das trevas. Sua lâmina já ceifou incontáveis vidas, mas sempre em nome da justiça. Agora, a Guilda dos Caçadores te convoca para a missão mais perigosa: investigar os desaparecimentos e eliminar a fonte da maldição.

### **A Jornada**

**Ato I - O Chamado**
- A Guilda te envia para o leste, onde três aldeias já foram consumidas pela escuridão
- Rumores falam de um necromante que ressuscita os mortos para formar um exército
- Você parte sozinho, como sempre fez

**Ato II - O Caminho das Sombras**
- Na Taverna da Encruzilhada, um bardo conta histórias de terror sobre as terras do leste
- A Floresta Sombria está infestada de criaturas corrompidas
- Lobos selvagens, antes animais comuns, agora atacam com fúria sobrenatural

**Ato III - A Aldeia Perdida**
- Você encontra a primeira aldeia desaparecida - casas vazias, portas abertas, nenhum corpo
- Uma sobrevivente escondida no porão revela a verdade: criaturas mortas-vivas levaram todos
- Ela te guia para o norte, onde fica o Cemitério Antigo

**Ato IV - A Ponte do Troll**
- Um troll bloqueia a única passagem para o cemitério
- Você pode lutar, negociar ou convencê-lo da ameaça que se aproxima
- Cada escolha tem consequências

**Ato V - Aliados Improváveis**
- Mercenários contratados para eliminar o necromante perderam metade do grupo
- Eles oferecem ajuda e suprimentos
- Unidos, vocês marcham para o cemitério

**Ato VI - O Cemitério Antigo**
- O Coveiro, guardião das tumbas, te adverte sobre o perigo
- Ele te entrega uma Vela Sagrada - a única arma efetiva contra a magia negra
- "Ninguém que entrou voltou vivo", ele murmura

**Ato VII - Descida às Trevas**
- Dentro do cemitério, hordas de mortos-vivos emergem do solo
- Na cripta profunda, um espírito aprisionado implora por libertação
- Usar a Vela Sagrada para libertá-lo concede bênçãos poderosas

**Ato VIII - Confronto Final**
- Na câmara do necromante, você enfrenta o responsável pela maldição
- O Necromante Sombrio controla um exército de mortos-vivos
- A batalha final decide o destino das aldeias e de todas as almas aprisionadas

**Epílogo - Redenção**
- Com o necromante derrotado, os mortos-vivos desmoronam
- Os aldeões aprisionados são libertados das jaulas nas sombras
- Você retorna à Guilda como herói, mas sabe que sempre haverá mais escuridão a combater

---

## 🎬 HISTÓRIA DA DEMO (Versão Gráfica)

A demo apresenta uma versão condensada da história:

### **Cena 1 - Guilda dos Caçadores**
O líder da Guilda te convoca para investigar desaparecimentos misteriosos. Você aceita a missão e parte para o leste.

### **Cena 2 - Caminho Sombrio**
Você atravessa uma estrada onde um enforcado balança ao vento. Um **Bandido** (HP: 150, ATK: 35) te embosca! Primeira batalha obrigatória.

### **Cena 3 - Cidade Abandonada**
Após derrotar o bandido, um NPC misterioso aparece e te avisa sobre perigos à frente. Ele te dá uma poção.

### **Cena 4 - Entrada do Cemitério**
O **Coveiro** te adverte sobre o cemitério. Se você escolher a opção certa, ele te dá a **Vela Funerária do Esquecido** (aumenta dano em 20).

### **Cena 5 - Cemitério**
O **Boss do Cemitério** (HP: 220, ATK: 45) emerge de uma tumba. Batalha final sem possibilidade de fuga. Vitória encerra a demo.

---

## 🎮 COMO JOGAR

### **Versão Gráfica (Tkinter)**

#### Executar:
```bash
# Windows
JOGAR.bat

# Ou diretamente
cd veilborn
python game_with_menu.py
```

#### Controles:
- **Setas Direcionais (→)**: Mover personagem
- **Mouse**: Clicar em botões de diálogo e batalha
- **Menu Superior**: Acessar estatísticas e inventário

#### Sistema de Batalha:
1. **Atacar**: 4 tipos de ataques diferentes
2. **Item**: Usar itens do inventário
3. **Persuadir**: Tentar negociar (geralmente falha)
4. **Fugir**: 25% de chance (não disponível contra boss)

---

### **Versão Terminal (Text-based)**

#### Executar:
```bash
# Windows
cd veilbornterminal
JOGAR_TERMINAL.bat

# Ou diretamente
python main_terminal.py
```

#### Controles:
- **Digite números**: Escolher opções
- **ENTER**: Avançar diálogos
- **Texto**: Responder prompts

#### Sistema de Batalha:
1. **Atacar**: Dano baseado em ATK + variação aleatória
2. **Defender**: Reduz dano pela metade
3. **Usar Item**: Consumir poções (cura 50 HP)
4. **Fugir**: Escapar da batalha (quando permitido)

#### Recursos Exclusivos:
- **Sistema de Gold**: Compre poções na taverna (30g)
- **Escolhas Múltiplas**: Diferentes caminhos e consequências
- **10 Cenas Completas**: História expandida
- **NPCs Únicos**: Bardo, Troll, Mercenários, Espírito

---

## 🧠 SISTEMA DE IA COM MACHINE LEARNING

Ambas as versões incluem IA adaptativa usando **Random Forest** e **Logistic Regression**.

### **Funcionalidades:**

#### 1. **Ajuste Dinâmico de Dificuldade**
- Monitora últimas 10 batalhas
- **Win rate > 80%**: Aumenta HP/ATK dos inimigos em até 50%
- **Win rate < 30%**: Diminui HP/ATK dos inimigos em até 50%
- Mantém o jogo desafiador mas justo

#### 2. **Predição de Vitória**
- Usa Random Forest treinado com 1000 cenários simulados
- Mostra probabilidade de vitória durante batalhas
- Considera: Level, HP, ATK, DEF do jogador vs HP/ATK do inimigo

#### 3. **Aprendizado Adaptativo**
- Registra duração de batalhas e dano recebido
- Ajusta estratégia baseado em performance
- Sistema de fallback se sklearn não estiver disponível

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

## 🗂️ ESTRUTURA DO PROJETO

```
veilborn/
├── 📁 veilborn/                    # Versão Gráfica
│   ├── game_with_menu.py          # Arquivo principal
│   ├── player.py                  # Classe do jogador
│   ├── enemy.py                   # Classe dos inimigos
│   ├── battle_system_fixed.py     # Sistema de batalha
│   ├── scenes_with_images.py      # Gerenciador de cenas
│   ├── ml_system.py               # Sistema de Machine Learning
│   ├── visualization.py           # Gráficos de estatísticas
│   └── asset_manager.py           # Gerenciador de assets
│
├── 📁 veilbornterminal/            # Versão Terminal
│   ├── main_terminal.py           # Arquivo principal
│   ├── player_terminal.py         # Classe do jogador
│   ├── enemy_terminal.py          # Classe dos inimigos
│   ├── battle_terminal.py         # Sistema de batalha
│   ├── scenes_terminal.py         # 10 cenas completas
│   ├── ml_terminal.py             # Sistema de Machine Learning
│   ├── utils_terminal.py          # Funções utilitárias
│   └── JOGAR_TERMINAL.bat         # Executável
│
├── 📁 images/                      # Assets gráficos
│   ├── cena1.png, cena2.png...    # Cenários
│   ├── cemiterio.png              # Cemitério
│   ├── menumorte.jpg              # Tela de derrota
│   └── vela.png                   # Itens
│
├── 📁 gifs/                        # Animações
│   ├── carrasco-parado.gif        # Personagem animado
│   ├── coveiro.gif                # NPC animado
│   ├── loading.gif                # Tela de carregamento
│   └── menu.gif                   # Menu principal
│
├── JOGAR.bat                      # Executável (Gráfico)
├── requirements.txt               # Dependências
└── README.md                      # Este arquivo
```

---

## 🛠️ REQUISITOS E INSTALAÇÃO

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
git clone https://github.com/seu-usuario/veilborn.git
cd veilborn

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o jogo
# Versão Gráfica:
JOGAR.bat
# ou
cd veilborn
python game_with_menu.py

# Versão Terminal:
cd veilbornterminal
python main_terminal.py
```

### **requirements.txt:**
```
pillow>=10.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
matplotlib>=3.7.0
```

---

## 🎨 RECURSOS VISUAIS

### **Versão Gráfica:**
- ✅ Resolução: 1280x720
- ✅ Personagem animado (GIF 150x150)
- ✅ Cenários em alta resolução
- ✅ Menu de morte customizado
- ✅ Sprites de NPCs (Coveiro 150x150)
- ✅ Animações de transição
- ✅ Interface gráfica completa

### **Versão Terminal:**
- ✅ Texto animado (efeito de digitação)
- ✅ Emojis para melhor visualização
- ✅ Cores e formatação
- ✅ Cabeçalhos estilizados
- ✅ Barra de estatísticas

---

## 🎯 CARACTERÍSTICAS PRINCIPAIS

### **Sistema de Progressão:**
- Level Up automático ao ganhar XP
- Aumento de atributos por nível
- Sistema de inventário
- Gold e loja (terminal)

### **Sistema de Escolhas:**
- Múltiplas opções de diálogo
- Consequências baseadas em escolhas
- Itens especiais por decisões corretas
- Caminhos alternativos (terminal)

### **Sistema de Combate:**
- Dano variável e críticos
- Defesa reduz dano recebido
- Itens consumíveis
- Fuga estratégica

### **Inteligência Artificial:**
- Dificuldade adaptativa
- Predição de vitória em tempo real
- Aprendizado baseado em performance
- Balanceamento automático

---

## 🏆 CONQUISTAS E DESAFIOS

### **Versão Gráfica (Demo):**
- 🎯 Derrotar o Bandido
- 🎯 Obter a Vela Funerária
- 🎯 Derrotar o Boss do Cemitério
- 🎯 Completar sem morrer

### **Versão Terminal (História Completa):**
- 🎯 Sobreviver à Floresta Sombria
- 🎯 Negociar com o Troll
- 🎯 Libertar o Espírito Aprisionado
- 🎯 Derrotar o Necromante Sombrio
- 🎯 Salvar todos os aldeões
- 🎯 Completar sem usar poções

---

## 🐛 TROUBLESHOOTING

### **Erro: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

### **Erro: tkinter não encontrado**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### **Jogo não inicia (Windows)**
- Certifique-se de estar na pasta correta
- Execute como Administrador
- Verifique se Python está no PATH

### **IA não funciona**
- Instale scikit-learn: `pip install scikit-learn`
- O jogo funciona sem IA (fallback automático)

---

## 👥 CRÉDITOS

**Desenvolvimento:** Equipe Veilborn
**Engine:** Python + Tkinter
**IA:** scikit-learn (Random Forest)
**Arte:** Assets customizados
**História:** Narrativa original

---

## 📜 LICENÇA

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## 🔮 FUTURAS ATUALIZAÇÕES

- [ ] Mais classes de personagens
- [ ] Sistema de crafting
- [ ] Multiplayer local
- [ ] Mais cenários e inimigos
- [ ] Sistema de save/load
- [ ] Trilha sonora original
- [ ] Modo hardcore
- [ ] Conquistas e rankings

---

## 📞 CONTATO E SUPORTE

Para bugs, sugestões ou dúvidas:
- **Issues:** GitHub Issues
- **Email:** veilborn@example.com
- **Discord:** [Link do servidor]

---

**Que sua jornada seja lendária, Carrasco. As sombras aguardam.** ⚔️💀
