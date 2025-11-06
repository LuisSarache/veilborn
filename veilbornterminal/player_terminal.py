import time

class Player:
    def __init__(self):
        self.name = "Carrasco"
        self.hp = 120
        self.max_hp = 120
        self.attack = 30
        self.defense = 10
        self.level = 1
        self.xp = 0
        self.inventory = []
        self.gold = 50
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    
    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= 100:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.xp = 0
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 3
        print(f"\n🎉 LEVEL UP! Agora você é nível {self.level}!")
        time.sleep(2)
