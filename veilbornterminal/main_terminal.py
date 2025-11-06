#!/usr/bin/env python3
from player_terminal import Player
from utils_terminal import header
from scenes_terminal import *

def main():
    while True:
        player = Player()
        
        header("⚔️  VEILBORN - A MALDIÇÃO DO NECROMANTE")
        print("Uma aventura de texto épica\n")
        print("1. Novo Jogo")
        print("2. Sair")
        
        choice = input("\nEscolha: ").strip()
        
        if choice != "1":
            print("\nAté logo, Carrasco!")
            break
        
        # História completa
        scene1_guilda(player)
        scene2_taverna(player)
        
        result = scene3_floresta(player)
        if not result:
            if not game_over():
                break
            continue
        
        scene4_aldeia(player)
        
        result = scene5_ponte(player)
        if not result:
            if not game_over():
                break
            continue
        
        scene6_acampamento(player)
        scene7_cemiterio_entrada(player)
        
        result = scene8_cemiterio_interno(player)
        if not result:
            if not game_over():
                break
            continue
        
        scene9_cripta(player)
        
        result = scene10_boss(player)
        if not result:
            if not game_over():
                break
            continue
        
        ending_victory(player)
        
        print("\n1. Jogar Novamente")
        print("2. Sair")
        choice = input("\nEscolha: ").strip()
        
        if choice != "1":
            print("\nAté logo, Carrasco!")
            break

if __name__ == "__main__":
    main()
