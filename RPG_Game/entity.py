from objects import Object


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


class Player(Entity):
    def __init__(self, name, HP=50, HPMAX=50, ATK=3, DEF=2, level=1, xp=0, xp_needed=10, gold=0, x=0, y=0, inventory={
        "potion": Object("potion", 1),
        "elixir": Object("elixir", 0),
        "atk_boost": Object("atk_boost", 0),
        "def_boost": Object("def_boost", 0),
        "key": Object("key", 0),
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
