import os
from pathlib import Path

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class AssetManager:
    def __init__(self, base_path=None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        else:
            base_path = Path(base_path)
        
        self.images_path = base_path / "images"
        self.gifs_path = base_path / "gifs"
        self.assets = {
            "weapons": {},
            "characters": {},
            "enemies": {},
            "backgrounds": {},
            "effects": {},
            "ui": {}
        }
        self.load_assets()
    
    def load_assets(self):
        """Carrega todos os assets das pastas"""
        self._load_images()
        self._load_gifs()
    
    def _load_images(self):
        """Carrega imagens estáticas"""
        if self.images_path.exists():
            for file in self.images_path.glob("*"):
                if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                    self._categorize_asset(file.name, str(file), "image")
    
    def _load_gifs(self):
        """Carrega GIFs animados"""
        if self.gifs_path.exists():
            for file in self.gifs_path.glob("*.gif"):
                self._categorize_asset(file.name, str(file), "gif")
    
    def _categorize_asset(self, filename, filepath, asset_type):
        """Categoriza assets baseado no nome do arquivo"""
        name_lower = filename.lower()
        
        # Personagens específicos do Veilborn
        if any(char in name_lower for char in ['carrasco', 'coveiro', 'arcano', 'assaltante', 'renascido']):
            self.assets["characters"][filename] = {"path": filepath, "type": asset_type}
        
        # Cenários e fundos
        elif any(bg in name_lower for bg in ['cemiterio', 'cena', 'papel']):
            self.assets["backgrounds"][filename] = {"path": filepath, "type": asset_type}
        
        # Interface e menus
        elif any(ui in name_lower for ui in ['menu', 'inventario', 'selecao', 'balao', 'loading']):
            self.assets["ui"][filename] = {"path": filepath, "type": asset_type}
        
        # Efeitos e objetos
        elif any(effect in name_lower for effect in ['vela']):
            self.assets["effects"][filename] = {"path": filepath, "type": asset_type}
        
        # Armas (para futuras adições)
        elif any(weapon in name_lower for weapon in ['sword', 'espada', 'staff', 'cajado', 'dagger', 'adaga', 'hammer', 'martelo']):
            self.assets["weapons"][filename] = {"path": filepath, "type": asset_type}
        
        # Inimigos (para futuras adições)
        elif any(enemy in name_lower for enemy in ['enemy', 'inimigo', 'monster', 'monstro', 'boss', 'dragon', 'orc']):
            self.assets["enemies"][filename] = {"path": filepath, "type": asset_type}
    
    def get_weapon_asset(self, weapon_name):
        """Retorna asset de arma baseado no nome"""
        for filename, asset in self.assets["weapons"].items():
            if weapon_name.lower() in filename.lower():
                return asset
        return None
    
    def get_character_asset(self, character_type="carrasco"):
        """Retorna asset de personagem"""
        for filename, asset in self.assets["characters"].items():
            if character_type.lower() in filename.lower():
                return asset
        return list(self.assets["characters"].values())[0] if self.assets["characters"] else None
    
    def get_scene_asset(self, scene_number):
        """Retorna asset de cena específica"""
        scene_name = f"cena{scene_number}"
        for filename, asset in self.assets["backgrounds"].items():
            if scene_name in filename.lower():
                return asset
        return None
    
    def get_ui_asset(self, ui_type):
        """Retorna asset de interface específico"""
        for filename, asset in self.assets["ui"].items():
            if ui_type.lower() in filename.lower():
                return asset
        return None
    
    def get_enemy_asset(self, enemy_type):
        """Retorna asset de inimigo baseado no tipo"""
        for filename, asset in self.assets["enemies"].items():
            if enemy_type.lower() in filename.lower():
                return asset
        return list(self.assets["enemies"].values())[0] if self.assets["enemies"] else None
    
    def list_assets(self):
        """Lista todos os assets carregados"""
        for category, assets in self.assets.items():
            if assets:
                print(f"\n{category.upper()}:")
                for filename in assets.keys():
                    print(f"  - {filename}")