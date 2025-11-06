import time
from utils_terminal import header, slow_print
from enemy_terminal import Enemy
from battle_terminal import battle

try:
    from ml_terminal import DifficultyAdjuster
    ml_adjuster = DifficultyAdjuster()
except:
    ml_adjuster = None

def scene1_guilda(player):
    header("🏰 CENA 1 - GUILDA DOS CAÇADORES")
    slow_print("Você está na Guilda, cercado por outros caçadores.")
    slow_print("O líder, um homem de cicatrizes profundas, se aproxima.\n")
    time.sleep(1)
    
    slow_print("Líder: 'Carrasco... Sua reputação te precede.'")
    slow_print("'Temos uma missão crítica. Aldeias inteiras estão desaparecendo.'")
    slow_print("'Siga para o leste. Investigue. E volte vivo.'\n")
    time.sleep(1)
    
    print("1. Desaparecimentos... Isso cheira a morte.")
    print("2. Quantas aldeias já foram perdidas?")
    print("3. Partirei imediatamente.")
    print("4. ...")
    
    choice = input("\nResposta: ").strip()
    
    responses = {
        "1": "Morte é o que você conhece melhor. Use isso a seu favor.",
        "2": "Três até agora. Não deixe que seja quatro.",
        "3": "Boa sorte, Carrasco. Que os deuses te protejam.",
        "4": "Silêncio... Típico de você. Vá."
    }
    
    print(f"\nLíder: '{responses.get(choice, responses['4'])}'\n")
    time.sleep(2)
    input("Pressione ENTER...")

def scene2_taverna(player):
    header("🍺 CENA 2 - TAVERNA DA ENCRUZILHADA")
    slow_print("Você para em uma taverna antes de seguir viagem.")
    slow_print("O lugar está quase vazio. Um bardo toca uma melodia sombria.\n")
    time.sleep(1)
    
    slow_print("Taverneiro: 'Bem-vindo, viajante. O que deseja?'\n")
    time.sleep(1)
    
    while True:
        print("1. Comprar Poção (30 gold)")
        print("2. Conversar com o Bardo")
        print("3. Partir")
        
        choice = input("\nEscolha: ").strip()
        
        if choice == "1":
            if player.gold >= 30:
                player.gold -= 30
                player.inventory.append("Poção")
                print("\n💚 Você comprou uma Poção!")
                time.sleep(1)
            else:
                print("\n❌ Gold insuficiente!")
                time.sleep(1)
        
        elif choice == "2":
            print("\nBardo: 'Ouvi rumores... Dizem que um necromante")
            print("está ressuscitando os mortos nas terras do leste.'")
            print("'Cuidado, viajante. A morte não descansa mais.'\n")
            time.sleep(2)
            input("Pressione ENTER...")
            break
        
        elif choice == "3":
            break

def scene3_floresta(player):
    header("🌲 CENA 3 - FLORESTA SOMBRIA")
    slow_print("Você entra em uma floresta densa e escura.")
    slow_print("O silêncio é perturbador. Nenhum pássaro canta.")
    slow_print("De repente, lobos selvagens aparecem!\n")
    time.sleep(1)
    
    if ml_adjuster:
        stats = ml_adjuster.get_adjusted_enemy_stats(100, 25)
        enemy = Enemy("Matilha de Lobos", stats["hp"], stats["attack"])
    else:
        enemy = Enemy("Matilha de Lobos", 100, 25)
    result = battle(player, enemy)
    
    if result == "flee":
        print("\nVocê conseguiu escapar, mas perdeu tempo...")
        time.sleep(2)
    elif result:
        print("\nVocê encontra um baú escondido!")
        player.inventory.append("Poção")
        print("💚 Você ganhou uma Poção!")
        time.sleep(2)
    
    return result

def scene4_aldeia(player):
    header("🏘️  CENA 4 - ALDEIA ABANDONADA")
    slow_print("Você chega à primeira aldeia desaparecida.")
    slow_print("Casas vazias. Portas abertas. Nenhum corpo.")
    slow_print("Apenas marcas de garras nas paredes...\n")
    time.sleep(1)
    
    slow_print("Uma sobrevivente surge de um porão!\n")
    time.sleep(1)
    
    slow_print("Sobrevivente: 'Você... você é humano?'")
    slow_print("'Eles vieram à noite... Criaturas mortas-vivas!'")
    slow_print("'Levaram todos para o cemitério antigo!'\n")
    time.sleep(1)
    
    print("1. Onde fica esse cemitério?")
    print("2. Você está ferida. Tome isso. [Dar Poção]")
    print("3. Fique aqui. Eu vou resolver isso.")
    print("4. ...")
    
    choice = input("\nResposta: ").strip()
    
    if choice == "2" and "Poção" in player.inventory:
        player.inventory.remove("Poção")
        print("\nVocê deu sua poção para a sobrevivente.")
        print("Ela te entrega um amuleto antigo.")
        player.inventory.append("Amuleto Protetor")
        player.defense += 5
        print("🛡️  Defesa +5!")
        time.sleep(2)
    
    print("\nSobrevivente: 'Siga para o norte... O cemitério fica lá.'")
    print("'Por favor... salve-os se ainda houver tempo...'\n")
    time.sleep(2)
    input("Pressione ENTER...")

def scene5_ponte(player):
    header("🌉 CENA 5 - PONTE QUEBRADA")
    slow_print("Você chega a uma ponte sobre um rio turbulento.")
    slow_print("A ponte está parcialmente destruída.")
    slow_print("Um troll enorme bloqueia a passagem!\n")
    time.sleep(1)
    
    slow_print("Troll: 'NINGUÉM PASSA! ESTA É MINHA PONTE!'\n")
    time.sleep(1)
    
    print("1. Lutar contra o Troll")
    print("2. Oferecer Gold (50g)")
    print("3. Tentar convencê-lo")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == "2" and player.gold >= 50:
        player.gold -= 50
        print("\nTroll: 'GOLD! TROLL GOSTA DE GOLD! PODE PASSAR!'")
        time.sleep(2)
        return True
    
    elif choice == "3":
        print("\nVocê: 'Um necromante está ressuscitando mortos.'")
        print("'Se ele não for parado, até você será escravizado.'\n")
        print("Troll: '...TROLL NÃO QUER SER ESCRAVO. PODE PASSAR!'")
        time.sleep(2)
        return True
    
    else:
        print("\nO Troll ataca!")
        time.sleep(1)
        if ml_adjuster:
            stats = ml_adjuster.get_adjusted_enemy_stats(150, 35)
            enemy = Enemy("Troll da Ponte", stats["hp"], stats["attack"])
        else:
            enemy = Enemy("Troll da Ponte", 150, 35)
        return battle(player, enemy, can_flee=False)

def scene6_acampamento(player):
    header("⛺ CENA 6 - ACAMPAMENTO DE MERCENÁRIOS")
    slow_print("Você encontra um acampamento de mercenários.")
    slow_print("Eles estão se preparando para algo grande.\n")
    time.sleep(1)
    
    slow_print("Líder Mercenário: 'Você também vai para o cemitério?'")
    slow_print("'Fomos contratados para eliminar o necromante.'")
    slow_print("'Mas perdemos metade do grupo... Quer se juntar?'\n")
    time.sleep(1)
    
    print("1. Aceitar ajuda")
    print("2. Recusar e seguir sozinho")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == "1":
        print("\nLíder: 'Ótimo! Tome isso. Vai precisar.'")
        player.inventory.append("Poção")
        player.inventory.append("Poção")
        print("💚 Você ganhou 2 Poções!")
        player.attack += 5
        print("⚔️  Ataque +5 (Moral elevado)!")
        time.sleep(2)
    else:
        print("\nLíder: 'Corajoso... ou tolo. Boa sorte.'")
        time.sleep(2)
    
    input("\nPressione ENTER...")

def scene7_cemiterio_entrada(player):
    header("⚰️  CENA 7 - ENTRADA DO CEMITÉRIO")
    slow_print("Você chega ao cemitério antigo.")
    slow_print("Névoa densa cobre o chão. Lápides quebradas por toda parte.")
    slow_print("Um coveiro está cavando uma sepultura fresca.\n")
    time.sleep(1)
    
    slow_print("Coveiro: 'Mais um que vem morrer...'")
    slow_print("'O necromante está lá dentro. Ele controla os mortos.'")
    slow_print("'Ninguém que entrou voltou vivo.'\n")
    time.sleep(1)
    
    print("1. Eu serei o primeiro a voltar.")
    print("2. Me dê informações sobre ele.")
    print("3. Você não tenta impedi-lo?")
    print("4. ...")
    
    choice = input("\nResposta: ").strip()
    
    responses = {
        "1": "Confiança... Espero que não seja arrogância.",
        "2": "Ele usa magia negra. Fogo e luz sagrada são suas fraquezas.",
        "3": "Eu sou apenas um coveiro. Cavo tumbas, não heróis.",
        "4": "Silêncio... A morte também é silenciosa."
    }
    
    print(f"\nCoveiro: '{responses.get(choice, responses['4'])}'")
    
    if choice == "2":
        player.attack += 3
        print("\n🔥 Você aprendeu a fraqueza do inimigo! Ataque +3!")
        time.sleep(2)
    
    print("\nCoveiro: 'Leve isto. Pode ajudar.'")
    player.inventory.append("Vela Sagrada")
    print("🕯️  Você recebeu: Vela Sagrada")
    time.sleep(2)
    input("\nPressione ENTER...")

def scene8_cemiterio_interno(player):
    header("💀 CENA 8 - DENTRO DO CEMITÉRIO")
    slow_print("Você entra no cemitério.")
    slow_print("Mãos esqueléticas emergem do solo!")
    slow_print("Mortos-vivos atacam!\n")
    time.sleep(1)
    
    if ml_adjuster:
        stats = ml_adjuster.get_adjusted_enemy_stats(180, 40)
        enemy = Enemy("Horda de Mortos-Vivos", stats["hp"], stats["attack"])
    else:
        enemy = Enemy("Horda de Mortos-Vivos", 180, 40)
    return battle(player, enemy, can_flee=False)

def scene9_cripta(player):
    header("🏛️  CENA 9 - CRIPTA PROFUNDA")
    slow_print("Você desce para a cripta.")
    slow_print("Velas negras iluminam o caminho.")
    slow_print("Você ouve cânticos macabros ecoando...\n")
    time.sleep(1)
    
    slow_print("Um espírito aparece!\n")
    time.sleep(1)
    
    slow_print("Espírito: 'Viajante... você busca o necromante?'")
    slow_print("'Ele me aprisionou aqui. Liberte-me e eu te ajudarei.'\n")
    time.sleep(1)
    
    print("1. Como posso te libertar?")
    print("2. Usar Vela Sagrada")
    print("3. Ignorar e seguir")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == "2" and "Vela Sagrada" in player.inventory:
        player.inventory.remove("Vela Sagrada")
        print("\nVocê acende a Vela Sagrada.")
        print("O espírito é libertado em uma luz brilhante!")
        print("\nEspírito: 'Obrigado... Tome minha bênção!'")
        player.max_hp += 30
        player.hp = player.max_hp
        player.defense += 5
        print("✨ HP Máximo +30 | Defesa +5 | HP Restaurado!")
        time.sleep(2)
    else:
        print("\nO espírito desaparece tristemente...")
        time.sleep(2)
    
    input("\nPressione ENTER...")

def scene10_boss(player):
    header("🔥 CENA 10 - CÂMARA DO NECROMANTE")
    slow_print("Você entra na câmara final.")
    slow_print("Um círculo de runas brilha no chão.")
    slow_print("O necromante está no centro, invocando os mortos!\n")
    time.sleep(1)
    
    slow_print("Necromante: 'Mais um tolo que ousa me desafiar?'")
    slow_print("'Você será meu próximo servo morto-vivo!'")
    slow_print("'LEVANTE-SE, MEUS SERVOS!'\n")
    time.sleep(2)
    
    slow_print("🔥 BATALHA FINAL! 🔥\n")
    time.sleep(1)
    
    if ml_adjuster:
        stats = ml_adjuster.get_adjusted_enemy_stats(250, 50)
        boss = Enemy("Necromante Sombrio", stats["hp"], stats["attack"])
    else:
        boss = Enemy("Necromante Sombrio", 250, 50)
    return battle(player, boss, can_flee=False)

def ending_victory(player):
    header("🎉 FINAL - VITÓRIA")
    slow_print("O necromante cai derrotado.")
    slow_print("As runas no chão se apagam.")
    slow_print("Os mortos-vivos desmoronam, finalmente em paz.\n")
    time.sleep(2)
    
    slow_print("Você ouve vozes... Os aldeões aprisionados!")
    slow_print("Eles estavam presos em jaulas nas sombras.")
    slow_print("Você os liberta. Eles estão salvos!\n")
    time.sleep(2)
    
    slow_print("Aldeão: 'Você nos salvou! Obrigado, Carrasco!'")
    slow_print("'Você é um verdadeiro herói!'\n")
    time.sleep(2)
    
    slow_print("Você retorna à Guilda.")
    slow_print("O líder te recebe com um sorriso raro.\n")
    time.sleep(2)
    
    slow_print("Líder: 'Você conseguiu. As aldeias estão seguras.'")
    slow_print("'Sua reputação crescerá ainda mais, Carrasco.'")
    slow_print("'Mas lembre-se... Sempre há mais escuridão a combater.'\n")
    time.sleep(2)
    
    print("=" * 70)
    print("  FIM DA HISTÓRIA".center(70))
    print("  Obrigado por jogar VEILBORN!".center(70))
    print("=" * 70)
    time.sleep(3)

def game_over():
    header("💀 GAME OVER")
    slow_print("Você falhou em sua missão.")
    slow_print("As sombras consumiram sua alma...")
    slow_print("Os aldeões nunca serão salvos.\n")
    time.sleep(2)
    
    print("1. Tentar Novamente")
    print("2. Sair")
    
    choice = input("\nEscolha: ").strip()
    return choice == "1"
