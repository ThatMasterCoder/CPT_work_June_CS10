from classes import *
from random import randint
"name, hp, max_hp, attack, defense"

Phys = "Phys"
Magic = "Magic"

bosses = {}
regular_mobs = []
mob_type = {}
Weapons = []
Debuff_Spells = []

def init_defs():
    global bosses, regular_mobs, mob_type, Weapons, Debuff_Spells
    bosses = {
        10: Enemy("Snake", hp := randint(20, 30), hp, randint(7, 10),
                  Defense(30, randint(10, 20))),
        15: Enemy("Phoenix", hp := 25, hp, randint(7, 16),
                  Defense(20, randint(40,70))),
        21: Enemy("Minotaur", hp := 35, hp, 30, Defense(10, 15)),
        25: Enemy("Skeleton Giant", hp := randint(35, 45), hp, randint(7, 10),
                  Defense(20, randint(10, 20))),
        30: Enemy("Grim Reaper", hp := randint(35, 50), hp, 50, # does a crazy amount of damage but low health
                  Defense(40, 20), special=True),
        35: Enemy("Medusa", hp := randint(50,75), hp, randint(40,50),
                  Defense(10, 40)),
        40: Enemy("Dragon", 100, 100, 15, Defense(10, 30)),
        42: Enemy("Golem", 125, 125, 20, Defense(55, 10), special=True),
        45: Enemy("Valkyrie", 120, 120, 30, Defense(10, 10)),
        48: Enemy("Cerberus",150, 150, 40, Defense(30,50)),
        50: Enemy("Xareth, the Void Emperor", 200, 200, 60,
                  Defense(50, 50)) # special boss
    }

    regular_mobs = [
        Enemy("Wyvern", 9, 9, randint(3,5), Defense(5,5)),
        Enemy("Wizard", 8,8,randint(5,7), Defense(0, 40), special=True),
        Enemy("Knight", 10,10, randint(2,5), Defense(10, 0)),
        Enemy("Prince", hp := randint(7,15), hp, randint(5,10), Defense(30, 0)),
        Enemy("Healer", 15, 15, randint(1,3), Defense(10,10), special=True),
        Enemy("Jason", 6,6, randint(3,5), Defense(50, 50), special=True),
        Enemy("Tiger", 8,8, randint(3,6), Defense(5,0)),
        Enemy("Black Cat", 3, 3, 30, Defense(0,0))
    ]

    mob_type = {
        "Snake": Phys,
        "Phoenix": Magic,
        "Minotaur": Phys,
        "Skeleton Giant": Phys,
        "Grim Reaper": Magic,
        "Medusa": Magic,
        "Dragon": Magic,
        "Golem": Phys,
        "Valkyrie": Phys,
        "Cerberus": Magic,  # Xareth has his own thing going

        "Wyvern": Phys,
        "Wizard": Magic,
        "Knight": Phys,
        "Prince": Phys,
        "Healer": Magic,
        "Jason": Phys,
        "Tiger": Phys,
        "Black Cat": Magic
    }
    """name, durability, damage, damage_type: DamageType"""

    Weapons = [
        Weapon('Iron Sword', 15, 5, DamageType(Phys)),
        Weapon('Spike-Infused Potion', 15, 4, DamageType(Magic)),
        Weapon("Medora's Staff", 5, 23, DamageType(Magic)),
        Weapon("Maxor's Dagger", 20, 4, DamageType(Phys)),
        Weapon("Scylla's Wand", 20, 4, DamageType(Magic)),
        Weapon("Seymour's Whip", 8, 12, DamageType(Phys)),
        Weapon("Fire Wand", 15, 5, DamageType(Magic)),
        Weapon("Alexander's Blade", 15, 10, DamageType(Phys)),
        Weapon("Lava Spray Wand", 10, 8, DamageType(Magic)),
        Weapon('Life Steal Dagger', 10, 9, DamageType(Phys))
    ]
    Debuff_Spells = [
        "Shield Depletor",
        "Sword Dull'r",
        "Carcinogenic Potion",
        "Steel Melter",
        "Magic Res. Shredder"
    ]


    return bosses, regular_mobs, mob_type, Weapons, Debuff_Spells
