class Player:
    def __init__(self, x=100, y=300, player_class="Guerreiro"):
        self.x = x
        self.y = y
        self.player_class = player_class
        
        # Atributos base
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        
        # Atributos de combate
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack_power = 20
        self.defense = 5
        self.magic_power = 10
        
        # Estatísticas
        self.battles_won = 0
        self.battles_lost = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        
        # Inventário e equipamentos
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        
        # Aplicar bônus da classe
        self._apply_class_bonuses()
        
    def _apply_class_bonuses(self):
        class_bonuses = {
            "Guerreiro": {"hp": 20, "attack": 10, "defense": 5},
            "Mago": {"hp": -10, "attack": 5, "magic": 15},
            "Ladino": {"hp": 0, "attack": 8, "defense": 3}
        }
        
        bonus = class_bonuses.get(self.player_class, {})
        self.max_hp += bonus.get("hp", 0)
        self.hp = self.max_hp
        self.attack_power += bonus.get("attack", 0)
        self.defense += bonus.get("defense", 0)
        self.magic_power += bonus.get("magic", 0)
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def add_item(self, item):
        self.inventory.append(item)
        
    def has_item(self, item_name):
        return item_name in self.inventory
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        self.total_damage_taken += actual_damage
        return actual_damage
        
    def deal_damage(self, base_damage):
        total_damage = base_damage + self.attack_power
        if self.equipped_weapon:
            total_damage += self.equipped_weapon.get("damage", 0)
        self.total_damage_dealt += total_damage
        return total_damage
        
    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.level_up()
            
    def level_up(self):
        self.xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        
        # Aumentar atributos
        self.max_hp += 15
        self.hp = self.max_hp  # Cura completa ao subir de nível
        self.attack_power += 3
        self.defense += 2
        self.magic_power += 2
        
    def win_battle(self, xp_reward=50):
        self.battles_won += 1
        self.gain_xp(xp_reward)
        
    def lose_battle(self):
        self.battles_lost += 1
        
    def is_alive(self):
        return self.hp > 0
        
    def get_stats(self):
        return {
            "level": self.level,
            "xp": self.xp,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack_power,
            "defense": self.defense,
            "magic": self.magic_power,
            "battles_won": self.battles_won,
            "battles_lost": self.battles_lost,
            "total_damage_dealt": self.total_damage_dealt,
            "total_damage_taken": self.total_damage_taken
        }