import os
from pathlib import Path
from .asset_manager import AssetManager

def scan_and_categorize_assets():
    """Escaneia e categoriza todos os assets disponíveis"""
    asset_manager = AssetManager()
    
    print("=== SCANNER DE ASSETS VEILBORN ===\n")
    
    # Verificar pastas
    images_path = Path("c:/Users/sghsb/Downloads/images")
    gifs_path = Path("c:/Users/sghsb/Downloads/gifs")
    
    print(f"Pasta de imagens: {images_path}")
    print(f"Existe: {images_path.exists()}")
    
    print(f"Pasta de GIFs: {gifs_path}")
    print(f"Existe: {gifs_path.exists()}")
    
    # Listar arquivos encontrados
    total_files = 0
    
    if images_path.exists():
        image_files = list(images_path.glob("*"))
        image_files = [f for f in image_files if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']]
        print(f"\nImagens encontradas ({len(image_files)}):")
        for img in image_files:
            print(f"  - {img.name}")
            total_files += 1
    
    if gifs_path.exists():
        gif_files = list(gifs_path.glob("*.gif"))
        print(f"\nGIFs encontrados ({len(gif_files)}):")
        for gif in gif_files:
            print(f"  - {gif.name}")
            total_files += 1
    
    print(f"\nTotal de arquivos: {total_files}")
    
    # Mostrar categorização
    if total_files > 0:
        print("\n=== CATEGORIZAÇÃO AUTOMÁTICA ===")
        asset_manager.list_assets()
        
        # Sugestões de nomes para assets faltantes
        print("\n=== SUGESTÕES DE NOMES ===")
        print("Para armas:")
        print("  - espada_ferro.png, espada_elfica.png")
        print("  - cajado_magico.png, adaga_venenosa.png")
        print("  - martelo_guerra.png")
        
        print("\nPara personagens:")
        print("  - player_idle.gif, player_attack.gif")
        print("  - hero_walk.gif")
        
        print("\nPara inimigos:")
        print("  - orc_idle.gif, dragon_attack.gif")
        print("  - monster_death.gif")
        
        print("\nPara efeitos:")
        print("  - explosion.gif, fire_magic.gif")
        print("  - healing_effect.gif")
    else:
        print("\nNenhum asset encontrado!")
        print("Adicione imagens (.png, .jpg, .jpeg, .bmp) na pasta 'images'")
        print("Adicione GIFs (.gif) na pasta 'gifs'")
    
    return asset_manager

def generate_asset_integration_code():
    """Gera código para integrar assets encontrados"""
    asset_manager = scan_and_categorize_assets()
    
    print("\n=== CÓDIGO DE INTEGRAÇÃO ===")
    
    # Código para armas
    if asset_manager.assets["weapons"]:
        print("\n# Atualização para WeaponRecommender:")
        for filename, asset in asset_manager.assets["weapons"].items():
            weapon_name = filename.replace('.png', '').replace('.jpg', '').replace('_', ' ').title()
            print(f'# {weapon_name}: "{filename}"')
    
    # Código para personagens
    if asset_manager.assets["characters"]:
        print("\n# Assets de personagens disponíveis:")
        for filename in asset_manager.assets["characters"].keys():
            print(f'# {filename}')
    
    # Código para inimigos
    if asset_manager.assets["enemies"]:
        print("\n# Assets de inimigos disponíveis:")
        for filename in asset_manager.assets["enemies"].keys():
            print(f'# {filename}')

if __name__ == "__main__":
    generate_asset_integration_code()