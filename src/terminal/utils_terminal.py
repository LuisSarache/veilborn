import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def header(title):
    clear()
    print("=" * 70)
    print(f"  {title.center(66)}")
    print("=" * 70)
    print()

def stats(player):
    print(f"\n📊 {player.name} | HP: {player.hp}/{player.max_hp} | ATK: {player.attack} | DEF: {player.defense} | LVL: {player.level} | 💰 {player.gold}g")
    print("-" * 70)
