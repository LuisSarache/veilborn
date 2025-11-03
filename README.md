# Veilborn RPG

Um jogo RPG desenvolvido em Python usando tkinter.

## Como Jogar

1. Execute o arquivo `rpg_game.py`:
```bash
python rpg_game.py
```

2. **Controles:**
   - Use as setas direcionais (→) para mover o personagem
   - Clique nos botões durante diálogos e batalhas
   - Siga as instruções na tela

## Fluxo do Jogo

### Cenário 1 - Guilda
- Personagem sai da porta
- Líder da guilda dá a missão
- Transição para próximo cenário

### Cenário 2 - Caminho
- Mova o personagem para a direita
- Transição automática ao chegar no final

### Cenário 3 - Cidade
- Após 2 passos, inimigo aparece da janela
- Sistema de batalha com 4 opções:
  - **Atacar**: 4 tipos de ataques diferentes
  - **Item**: Mostra inventário (vazio inicialmente)
  - **Persuadir**: Tentativa de diálogo (sempre falha)
  - **Fugir**: 25% de chance de sucesso

### Cenário 4 - Praça
- NPC pede para matar monstro no cemitério
- Protagonista aceita a missão

### Entrada do Cemitério
- Diálogo com o Coveiro
- 4 opções de resposta diferentes
- Escolhendo opção 3, ganha item especial: **Vela Funerária do Esquecido**

### Cemitério
- Boss aparece do túmulo
- Batalha final (não é possível fugir)
- Se tiver a Vela Funerária, dano aumenta em 20 pontos
- Vitória encerra o jogo

## Recursos Implementados

- ✅ Sistema de cenários com transições
- ✅ Animações de carregamento (1.5s)
- ✅ Sistema de batalha completo
- ✅ Inventário funcional
- ✅ Diálogos interativos
- ✅ Sistema de itens especiais
- ✅ Boss battle final
- ✅ Múltiplas opções de resposta

## Requisitos

- Python 3.x
- tkinter (incluído no Python padrão)
- scikit-learn (para IA com machine learning)
- numpy

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Execute o jogo:
```bash
python rpg_game.py
```

## Recursos de IA

- **IA com Machine Learning**: Os inimigos usam Random Forest para aprender com as ações do jogador
- **Aprendizado Adaptativo**: A IA ajusta sua estratégia baseada no histórico de batalhas
- **Fallback Inteligente**: Sistema de IA simples como backup caso o ML falhe