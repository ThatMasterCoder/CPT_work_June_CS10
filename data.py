from classes import *
from random import randint
"name, hp, max_hp, attack, defense"
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
    Enemy("Wyvern", 12, 12, randint(3,5), Defense(5,5)),
    Enemy("Wizard", 8,8,randint(5,8), Defense(0, 40), special=True),
    Enemy("Knight", 14,14, randint(2,5), Defense(10, 0)),
    Enemy("Prince", hp := randint(7,15), hp, randint(5,10), Defense(30, 0)),
    Enemy("Healer", 15, 15, randint(1,3), Defense(10,10), special=True),
    Enemy("Jason", 6,6, randint(3,5), Defense(50, 50), special=True),
    Enemy("Tiger", 8,8, randint(5,8), Defense(5,0)),
    Enemy("Black Cat", 3, 3, 50, Defense(0,0))
]

"""name, durability, damage, damage_type: DamageType"""
Phys = "Phys"
Magic = "Magic"
Weapons = [
    Weapon('Fist', 100, 2, DamageType(Phys)),

]

Spells = []
