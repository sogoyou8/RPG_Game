from objects import Object
import random


class Entity:
    def __init__(self, name, level, HP, ATK, DEF, gold):
        self.name = name
        self.HP = HP
        self.level = level
        self.ATK = ATK
        self.DEF = DEF
        self.gold = gold


class Mob(Entity):
    def __init__(self, name, level, HP, ATK, DEF, gold, XP):
        super().__init__(name, level, HP, ATK, DEF, gold)
        self.XP = XP
        self.base_HP = HP

    def loot(self):
        # Définir les objets possibles à looter
        possible_loot = [
            ("potion", 0.5),  # 50% de chance de looter une potion
            ("elixir", 0.3),  # 30% de chance de looter un elixir
            ("atk_boost", 0.1),  # 10% de chance de looter un boost d'attaque
            ("def_boost", 0.1),  # 10% de chance de looter un boost de défense
            ("magic_scroll", 0.05),  # 5% de chance de looter un magic scroll
            ("shield", 0.05),  # 5% de chance de looter un shield
            ("sword", 0.05)  # 5% de chance de looter un sword
        ]

        # Choisir un objet aléatoire en fonction des probabilités
        loot = random.choices(
            [item[0] for item in possible_loot],
            [item[1] for item in possible_loot],
            k=1
        )[0]

        return loot

class Player(Entity):
    def __init__(self, name, HP=50, HPMAX=50, ATK=3, DEF=2, level=1, xp=0, xp_needed=10, gold=0, x=0, y=0, inventory={
        "potion": Object("potion", 1),
        "elixir": Object("elixir", 0),
        "atk_boost": Object("atk_boost", 0),
        "def_boost": Object("def_boost", 0),
        "key": Object("key", 0),
        "magic_scroll": Object("magic_scroll", 0),
        "shield": Object("shield", 0),  
        "sword": Object("sword", 0), 
    }):
        super().__init__(name, level, HP, ATK, DEF, gold)
        self.HPMAX = HPMAX
        self.xp = xp
        self.xp_needed = xp_needed
        self.gold = gold
        self.x = x
        self.y = y
        self.inventory = inventory
        
    def level_up(self):
        self.level += 1
        self.xp_needed += 5 * self.level
        self.HPMAX += 10
        self.HP = self.HPMAX
        self.ATK += 2
        self.DEF += 1
        print(f"Félicitations! Vous êtes maintenant niveau {self.level}!")
        print(f"HP: {self.HP}, ATK: {self.ATK}, DEF: {self.DEF}")
