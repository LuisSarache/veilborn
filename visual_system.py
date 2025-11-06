import pygame
from .asset_manager import AssetManager
from .ml_system import BattleDifficultyClassifier, VictoryPredictor, WeaponRecommender

class VisualBattleSystem:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Veilborn - Sistema de Batalha")
        
        self.asset_manager = AssetManager()
        self.difficulty_classifier = BattleDifficultyClassifier()
        self.victory_predictor = VictoryPredictor()
        self.weapon_recommender = WeaponRecommender()
        
        self.clock = pygame.time.Clock()
        
    def render_battle_scene(self, player_stats, enemy_stats, recommended_weapon=None):
        """Renderiza a cena de batalha com assets visuais"""
        self.screen.fill((50, 50, 50))  # Fundo escuro
        
        # Renderizar personagem do jogador
        player_asset = self.asset_manager.get_character_asset("player")
        if player_asset:
            self._render_asset(player_asset, (150, 300))
        
        # Renderizar inimigo
        enemy_asset = self.asset_manager.get_enemy_asset("monster")
        if enemy_asset:
            self._render_asset(enemy_asset, (550, 300))
        
        # Renderizar arma recomendada
        if recommended_weapon and recommended_weapon.get("asset"):
            self._render_asset(recommended_weapon["asset"], (100, 400))
        
        # Renderizar informações de batalha
        self._render_battle_info(player_stats, enemy_stats)
        
        pygame.display.flip()
    
    def _render_asset(self, asset, position):
        """Renderiza um asset na posição especificada"""
        try:
            if asset["type"] == "image":
                image = pygame.image.load(asset["path"])
                image = pygame.transform.scale(image, (100, 100))
                self.screen.blit(image, position)
            elif asset["type"] == "gif":
                # Para GIFs, renderizar o primeiro frame
                image = pygame.image.load(asset["path"])
                image = pygame.transform.scale(image, (100, 100))
                self.screen.blit(image, position)
        except:
            # Renderizar placeholder se asset não carregar
            pygame.draw.rect(self.screen, (100, 100, 100), (*position, 100, 100))
    
    def _render_battle_info(self, player_stats, enemy_stats):
        """Renderiza informações da batalha"""
        font = pygame.font.Font(None, 24)
        
        # Predições do ML
        difficulty = self.difficulty_classifier.predict_difficulty(player_stats, enemy_stats)
        victory_chance = self.victory_predictor.predict_victory(player_stats, enemy_stats)
        
        # Textos informativos
        texts = [
            f"Dificuldade: {difficulty}",
            f"Chance de Vitória: {victory_chance:.1%}",
            f"Player HP: {player_stats['hp']}",
            f"Player ATK: {player_stats['attack']}",
            f"Enemy HP: {enemy_stats['hp']}",
            f"Enemy ATK: {enemy_stats['attack']}"
        ]
        
        for i, text in enumerate(texts):
            color = (255, 255, 255)
            if "Dificuldade" in text:
                if "Fácil" in text:
                    color = (0, 255, 0)
                elif "Difícil" in text:
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 0)
            
            surface = font.render(text, True, color)
            self.screen.blit(surface, (10, 10 + i * 30))
    
    def run_battle_demo(self):
        """Executa uma demonstração do sistema de batalha"""
        running = True
        
        # Stats de exemplo
        player_stats = {"level": 3, "hp": 120, "attack": 25, "defense": 8, "magic": 15}
        enemy_stats = {"hp": 80, "attack": 20}
        
        # Recomendar arma
        recommended_weapon = self.weapon_recommender.recommend_weapon(player_stats, enemy_stats)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Gerar novos stats aleatórios
                        import random
                        player_stats["hp"] = random.randint(80, 150)
                        player_stats["attack"] = random.randint(20, 40)
                        enemy_stats["hp"] = random.randint(60, 120)
                        enemy_stats["attack"] = random.randint(15, 35)
                        recommended_weapon = self.weapon_recommender.recommend_weapon(player_stats, enemy_stats)
            
            self.render_battle_scene(player_stats, enemy_stats, recommended_weapon)
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    battle_system = VisualBattleSystem()
    battle_system.run_battle_demo()