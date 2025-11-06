import os
from pathlib import Path

def scan_assets():
    """Escaneia assets nas pastas especificadas"""
    images_path = Path("c:/Users/sghsb/OneDrive/Documentos/GitHub/veilborn/images")
    gifs_path = Path("c:/Users/sghsb/OneDrive/Documentos/GitHub/veilborn/gifs")
    
    print("=== SCANNER DE ASSETS VEILBORN ===\n")
    
    assets = {
        "weapons": [],
        "characters": [],
        "enemies": [],
        "backgrounds": [],
        "effects": [],
        "ui": []
    }
    
    total_files = 0
    
    # Escanear imagens
    if images_path.exists():
        for file in images_path.iterdir():
            if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                categorize_asset(file.name, assets)
                total_files += 1
                print(f"Imagem encontrada: {file.name}")
    
    # Escanear GIFs
    if gifs_path.exists():
        for file in gifs_path.iterdir():
            if file.suffix.lower() == '.gif':
                categorize_asset(file.name, assets)
                total_files += 1
                print(f"GIF encontrado: {file.name}")
    
    print(f"\nTotal de arquivos: {total_files}")
    
    if total_files > 0:
        print("\n=== CATEGORIZAÇÃO ===")
        for category, files in assets.items():
            if files:
                print(f"\n{category.upper()}:")
                for filename in files:
                    print(f"  - {filename}")
        
        generate_integration_code(assets)
    else:
        print("\nNenhum asset encontrado!")
        print("Adicione arquivos nas pastas:")
        print(f"  - Imagens: {images_path}")
        print(f"  - GIFs: {gifs_path}")

def categorize_asset(filename, assets):
    """Categoriza asset baseado no nome"""
    name_lower = filename.lower()
    
    # Personagens específicos do jogo
    if any(char in name_lower for char in ['carrasco', 'coveiro', 'arcano', 'assaltante', 'renascido']):
        assets["characters"].append(filename)
    
    # Cenários e fundos
    elif any(bg in name_lower for bg in ['cemiterio', 'cena', 'papel']):
        assets["backgrounds"].append(filename)
    
    # Interface e menus
    elif any(ui in name_lower for ui in ['menu', 'inventario', 'selecao', 'balao', 'loading']):
        assets["ui"].append(filename)
    
    # Efeitos e objetos
    elif any(effect in name_lower for effect in ['vela']):
        assets["effects"].append(filename)
    
    # Armas (caso adicione depois)
    elif any(weapon in name_lower for weapon in ['sword', 'espada', 'staff', 'cajado', 'dagger', 'adaga', 'hammer', 'martelo']):
        assets["weapons"].append(filename)
    
    # Inimigos (caso adicione depois)
    elif any(enemy in name_lower for enemy in ['enemy', 'inimigo', 'monster', 'monstro', 'boss', 'dragon', 'orc']):
        assets["enemies"].append(filename)

def generate_integration_code(assets):
    """Gera código de integração para os assets"""
    print("\n=== CÓDIGO DE INTEGRAÇÃO ===")
    
    if assets["weapons"]:
        print("\n# Atualizar WeaponRecommender com assets:")
        for weapon in assets["weapons"]:
            weapon_name = weapon.replace('.png', '').replace('.jpg', '').replace('.gif', '').replace('_', ' ').title()
            print(f'# {weapon_name} -> "{weapon}"')
    
    if assets["characters"]:
        print("\n# Assets de personagens:")
        for char in assets["characters"]:
            print(f'# {char}')
    
    if assets["enemies"]:
        print("\n# Assets de inimigos:")
        for enemy in assets["enemies"]:
            print(f'# {enemy}')

if __name__ == "__main__":
    scan_assets()