# Configurações do jogo
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Configurações do jogador
PLAYER_INITIAL_HP = 100
PLAYER_SPEED = 10

# Configurações de batalha
FLEE_CHANCE = 0.25
LOADING_TIME = 1500

# Configurações de inimigos
ENEMIES = {
    "bandido": {
        "name": "Bandido",
        "hp": 60,
        "attack": 15
    },
    "boss": {
        "name": "Boss do Cemitério", 
        "hp": 120,
        "attack": 25
    }
}

# Ataques do jogador
ATTACKS = {
    "golpe_rapido": {"name": "Golpe Rápido", "damage": 15},
    "ataque_forte": {"name": "Ataque Forte", "damage": 25},
    "combo": {"name": "Combo", "damage": 20},
    "ataque_especial": {"name": "Ataque Especial", "damage": 30}
}

# Item especial
SPECIAL_ITEM = {
    "name": "Vela Funerária do Esquecido",
    "damage_bonus": 20,
    "description": "Uma vela feita de cera negra, com um pavio trançado de cabelo humano."
}