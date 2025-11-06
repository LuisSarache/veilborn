import random
import time
from utils_terminal import header, stats

ml_adjuster = None
ml_predictor = None

try:
    from ml_terminal import DifficultyAdjuster, BattlePredictor
    ml_adjuster = DifficultyAdjuster()
    ml_predictor = BattlePredictor()
except:
    pass

def battle(player, enemy, can_flee=True):
    battle_start_hp = player.hp
    battle_turns = 0
    header(f"⚔️  BATALHA: {player.name} VS {enemy.name}")
    
    while player.hp > 0 and enemy.hp > 0:
        stats(player)
        print(f"🔴 {enemy.name} | HP: {enemy.hp}/{enemy.max_hp} | ATK: {enemy.attack}\n")
        
        print("1. Atacar")
        print("2. Defender")
        print("3. Usar Item")
        if can_flee:
            print("4. Fugir")
        
        choice = input("\nAção: ").strip()
        
        if choice == "1":
            battle_turns += 1
            damage = player.attack + random.randint(-5, 10)
            enemy.hp -= damage
            print(f"\n⚔️  Você causou {damage} de dano!")
            
            if ml_predictor and enemy.hp > 0:
                chance = ml_predictor.predict_victory_chance(player, enemy)
                print(f"📊 Chance de vitória: {chance:.1f}%")
            
            time.sleep(1)
            
            if enemy.hp > 0:
                enemy_damage = player.take_damage(enemy.attack + random.randint(-3, 5))
                print(f"💥 {enemy.name} causou {enemy_damage} de dano!")
                time.sleep(1)
        
        elif choice == "2":
            battle_turns += 1
            print("\n🛡️  Você se defendeu!")
            enemy_damage = player.take_damage((enemy.attack // 2) + random.randint(0, 3))
            print(f"💥 {enemy.name} causou {enemy_damage} de dano (reduzido)!")
            time.sleep(1)
        
        elif choice == "3":
            if "Poção" in player.inventory:
                player.heal(50)
                player.inventory.remove("Poção")
                print("\n💚 Você usou uma Poção! +50 HP")
                time.sleep(1)
            else:
                print("\n❌ Sem itens!")
                time.sleep(1)
                continue
        
        elif choice == "4" and can_flee:
            print("\n🏃 Você fugiu da batalha!")
            time.sleep(1)
            return "flee"
        
        else:
            print("\n❌ Opção inválida!")
            time.sleep(1)
            continue
    
    if player.hp > 0:
        header("🎉 VITÓRIA!")
        xp = enemy.max_hp // 2
        gold = random.randint(20, 50)
        player.gain_xp(xp)
        player.gold += gold
        print(f"Você derrotou {enemy.name}!")
        print(f"+ {xp} XP | + {gold} Gold")
        
        if ml_adjuster:
            damage_ratio = (battle_start_hp - player.hp) / battle_start_hp if battle_start_hp > 0 else 0
            ml_adjuster.record_battle(True, battle_turns, damage_ratio)
        
        time.sleep(2)
        return True
    else:
        header("💀 DERROTA")
        print(f"{enemy.name} te derrotou...")
        
        if ml_adjuster:
            ml_adjuster.record_battle(False, battle_turns, 1.0)
        
        time.sleep(2)
        return False
