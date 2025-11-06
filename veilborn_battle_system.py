from .asset_manager import AssetManager
from .ml_system import BattleDifficultyClassifier, VictoryPredictor, WeaponRecommender, DifficultyAdjuster

class VeilbornBattleSystem:
    def __init__(self):
        self.asset_manager = AssetManager()
        self.difficulty_classifier = BattleDifficultyClassifier()
        self.victory_predictor = VictoryPredictor()
        self.weapon_recommender = WeaponRecommender()
        self.difficulty_adjuster = DifficultyAdjuster()
        
        # Personagens disponíveis com seus assets
        self.characters = {
            "carrasco": {
                "name": "Carrasco",
                "hp": 120,
                "attack": 25,
                "defense": 8,
                "magic": 5,
                "level": 3,
                "asset": self.asset_manager.get_character_asset("carrasco"),
                "balloon": self.asset_manager.get_ui_asset("balao-carrasco")
            },
            "arcano": {
                "name": "Arcano",
                "hp": 80,
                "attack": 15,
                "defense": 5,
                "magic": 30,
                "level": 4,
                "asset": self.asset_manager.get_character_asset("arcano"),
                "balloon": self.asset_manager.get_ui_asset("balao-arcano")
            },
            "assaltante": {
                "name": "Assaltante",
                "hp": 100,
                "attack": 30,
                "defense": 6,
                "magic": 8,
                "level": 2,
                "asset": self.asset_manager.get_character_asset("assaltante"),
                "balloon": self.asset_manager.get_ui_asset("balao-assaltante")
            },
            "coveiro": {
                "name": "Coveiro",
                "hp": 90,
                "attack": 20,
                "defense": 10,
                "magic": 25,
                "level": 3,
                "asset": self.asset_manager.get_character_asset("coveiro"),
                "balloon": None
            },
            "renascido": {
                "name": "Renascido",
                "hp": 150,
                "attack": 35,
                "defense": 12,
                "magic": 20,
                "level": 5,
                "asset": self.asset_manager.get_character_asset("renascido"),
                "balloon": self.asset_manager.get_ui_asset("balao-renascido")
            }
        }
        
        # Cenários disponíveis
        self.scenes = {
            1: {"name": "Cemitério", "asset": self.asset_manager.get_scene_asset(1)},
            2: {"name": "Floresta Sombria", "asset": self.asset_manager.get_scene_asset(2)},
            3: {"name": "Castelo Abandonado", "asset": self.asset_manager.get_scene_asset(3)},
            4: {"name": "Portal Dimensional", "asset": self.asset_manager.get_scene_asset(4)}
        }
    
    def analyze_battle(self, player_character, enemy_character, scene_id=1):
        """Analisa uma batalha usando ML e retorna informações completas"""
        player_stats = self.characters[player_character]
        enemy_stats = self.characters[enemy_character]
        
        # Predições do ML
        difficulty = self.difficulty_classifier.predict_difficulty(player_stats, enemy_stats)
        victory_chance = self.victory_predictor.predict_victory(player_stats, enemy_stats)
        recommended_weapon = self.weapon_recommender.recommend_weapon(player_stats, enemy_stats)
        
        # Ajustar stats do inimigo baseado no histórico
        adjusted_enemy = self.difficulty_adjuster.get_adjusted_enemy_stats(
            enemy_stats["hp"], 
            enemy_stats["attack"]
        )
        
        battle_info = {
            "player": {
                "character": player_character,
                "stats": player_stats,
                "asset": player_stats["asset"],
                "balloon": player_stats["balloon"]
            },
            "enemy": {
                "character": enemy_character,
                "stats": enemy_stats,
                "adjusted_stats": adjusted_enemy,
                "asset": enemy_stats["asset"],
                "balloon": enemy_stats["balloon"]
            },
            "scene": self.scenes[scene_id],
            "predictions": {
                "difficulty": difficulty,
                "victory_chance": victory_chance,
                "recommended_weapon": recommended_weapon
            },
            "ui_assets": {
                "menu_battle": self.asset_manager.get_ui_asset("menu-batalha"),
                "inventory": self.asset_manager.get_ui_asset("inventario"),
                "attack_selection": self.asset_manager.get_ui_asset("selecao-ataque"),
                "loading": self.asset_manager.get_ui_asset("loading")
            },
            "effects": {
                "candle": self.asset_manager.assets["effects"].get("vela.png"),
                "cemetery": self.asset_manager.assets["backgrounds"].get("cemiterio.png"),
                "paper": self.asset_manager.assets["backgrounds"].get("papel.png")
            }
        }
        
        return battle_info
    
    def simulate_battle(self, player_character, enemy_character, scene_id=1):
        """Simula uma batalha completa"""
        battle_info = self.analyze_battle(player_character, enemy_character, scene_id)
        
        print(f"=== BATALHA NO {battle_info['scene']['name'].upper()} ===")
        print(f"🗡️  {battle_info['player']['stats']['name']} VS {battle_info['enemy']['stats']['name']} ⚔️")
        print(f"📊 Dificuldade: {battle_info['predictions']['difficulty']}")
        print(f"🎯 Chance de Vitória: {battle_info['predictions']['victory_chance']:.1%}")
        
        if battle_info['predictions']['recommended_weapon']:
            weapon = battle_info['predictions']['recommended_weapon']
            print(f"⚔️  Arma Recomendada: {weapon['name']} (Dano: {weapon['damage']})")
        
        # Simular resultado
        import random
        victory = random.random() < battle_info['predictions']['victory_chance']
        battle_duration = random.randint(30, 120)
        damage_ratio = random.uniform(0.6, 1.4)
        
        # Registrar resultado para ajuste de dificuldade
        self.difficulty_adjuster.record_battle(victory, battle_duration, damage_ratio)
        
        print(f"🏆 Resultado: {'VITÓRIA!' if victory else 'DERROTA!'}")
        print(f"⏱️  Duração: {battle_duration}s")
        
        return {
            "victory": victory,
            "duration": battle_duration,
            "battle_info": battle_info
        }
    
    def list_available_content(self):
        """Lista todo o conteúdo disponível"""
        print("=== CONTEÚDO VEILBORN DISPONÍVEL ===\n")
        
        print("PERSONAGENS:")
        for char_id, char_data in self.characters.items():
            asset_status = "✅" if char_data["asset"] else "❌"
            balloon_status = "✅" if char_data["balloon"] else "❌"
            print(f"  {asset_status} {char_data['name']} (Nível {char_data['level']}) - Balão: {balloon_status}")
        
        print("\nCENÁRIOS:")
        for scene_id, scene_data in self.scenes.items():
            asset_status = "✅" if scene_data["asset"] else "❌"
            print(f"  {asset_status} Cena {scene_id}: {scene_data['name']}")
        
        print("\nASSETS DE INTERFACE:")
        ui_assets = ["menu-batalha", "inventario", "selecao-ataque", "loading", "menu"]
        for ui in ui_assets:
            asset = self.asset_manager.get_ui_asset(ui)
            status = "✅" if asset else "❌"
            print(f"  {status} {ui}")
        
        print("\nEFEITOS E OBJETOS:")
        for filename in self.asset_manager.assets["effects"].keys():
            print(f"  ✅ {filename}")

if __name__ == "__main__":
    battle_system = VeilbornBattleSystem()
    battle_system.list_available_content()
    
    print("\n" + "="*50)
    print("SIMULAÇÃO DE BATALHA")
    print("="*50)
    
    # Simular algumas batalhas
    battle_system.simulate_battle("carrasco", "arcano", 1)
    print()
    battle_system.simulate_battle("assaltante", "renascido", 2)