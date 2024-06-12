"""
This file's purpose is to define custom classes for the game
For example, it contains classes such as armor, player, enemy etc.
Used in the main game code.
"""
from math import floor
import mobs

def underscoreify(string: str) -> str:
    return string.replace(' ', '_')

class DamageException(BaseException):
    def __init__(self, message):
        self.message = message

class DefenseException(BaseException):
    def __init__(self, message):
        self.message = message
class Defense:
    """
    Defense is calculated in terms of % of damage reduced, times 100.
    For example, 4 Physical Defense reduces all Physical Damage by 4%.
    100 Defense of a type reduces all damage by 100%
    Anything above 100 Defense is useless
    This class also has static methods that calculate damage.
    """
    def __init__(self, Phys, Magic):
        self.Phys = Phys
        self.Magic = Magic

    def __repr__(self):  # debugging
        return f'{self.Phys = }, {self.Magic = }'

    def __str__(self):
        return f'Physical Defense: {self.Phys}, Magic Defense: {self.Magic}'

    def print_def(self) -> None:
        print(f"This enemy has {self.Phys} physical defense and {self.Magic} magic defense.")

    """
        def valid_def(self) -> bool:
            return 0 <= self.Phys <= 100 and 0 <= self.Magic <= 100
    """
    def __add__(self, other):
        return Defense(self.Phys + other.Phys, self.Magic + other.Magic)

    def reduce_additive(self, reduced_type: str, reduced_value: int | float):
        if reduced_type == 'Phys':
            self.Phys -= reduced_value

            return self
        elif reduced_type == 'Magic':
            self.Magic -= reduced_value
            return self
        elif reduced_type == 'Both':
            self.Phys -= reduced_value
            self.Magic -= reduced_value
            return self
        else:
            raise DefenseException(f"Invalid type of Defense. Defense given: {reduced_type}")

    def reduce_multiplicative(self, reduced_type: str, reduce_by_factor: int | float):
        """
        :param reduced_type: Type being reduced
        :param reduce_by_factor: Factor of which by the defense is reduced.
            I.E. Factor of 5 reduction is -5%. (*.95%)
        :return:
        """
        if reduced_type == 'Phys':
            self.reduce_additive("Phys", self.Phys * (100 - reduce_by_factor))
        elif reduced_type == 'Magic':
            self.reduce_additive("Magic", self.Magic * (100 - reduce_by_factor))
        elif reduced_type == 'Both':
            self.reduce_additive("Phys", self.Phys * (100 - reduce_by_factor))
            self.reduce_additive("Magic", self.Magic * (100 - reduce_by_factor))
        else:
            raise DefenseException(f"Invalid Type of defense. Defense given: {reduced_type}")



class DamageType:
    def __init__(self, damage_type):
        if DamageType.check(damage_type):
            self.damage_type = damage_type
        else:
            raise DamageException('Invalid Type of damage')

    @staticmethod
    def check(damage_type):
        return damage_type in ['Phys', 'Magic']

    @staticmethod
    def calc_dmg(damage_type, damage_value, damage_defense):
        if not DamageType.check(damage_type):  # damage invalid
            raise DamageException('Invalid type of damage')
        else:
            if damage_defense > 100:
                raise DamageException(f'Defense cannot be greater than 100. Defense is {damage_defense}')
            elif damage_defense < 0:
                raise DamageException(f'Defense cannot be negative. Defense is {damage_defense}')
            return floor(damage_value * (100 - (damage_defense / 100)))

class Gear:
    def __init__(self, name, durability):
        self.name = name
        self.durability = durability

    def take_dur_damage(self):  # returns remaining durability
        self.durability -= 1
        if self.durability < 0:
            self.durability = 0
        return self.durability

class Buff:
    def __init__(self, name, healing, attack_buff):
        self.name = name
        self.healing = healing
        self.attack_buff = attack_buff

class Armor(Gear):
    """
    This has durability
    Durability based on how many rounds it will last

    """
    def __init__(self, name, durability, defense_value: Defense):
        super().__init__(name, durability)
        self.defense_value = defense_value





class Weapon(Gear):
    """
    For Player to use
    """
    def __init__(self, name, durability, damage, damage_type: DamageType):
        super().__init__(name, durability)
        self.damage = damage
        self.damage_type = damage_type


class Character:
    def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: Defense):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense

    def __repr__(self):
        return f'name: {self.name}, hp: {self.hp}, max_hp: {self.max_hp}, atk: {self.attack}, def: {self.defense}'

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage_take) -> int | float:
        """Returns current health"""
        self.hp -= damage_take
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, healing) -> int | float:
        self.hp += healing
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self.hp

    def print_stats(self):
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attack: {self.attack}")
        print(f"{self.defense}")


class Player(Character):
    # starts with 100 hp, 0 defense of all types
    # starts with 1 attack (fist)
    def __init__(self, name, hp=100, max_hp=100, attack=1, defense: Defense = Defense(0,0), armor: Armor | None = None,
                 weapons: list[Weapon] | None = None):
        super().__init__(name, hp, max_hp, attack, defense)
        self.armor = armor
        self.weapons = weapons

    def weapons_list(self) -> list[Weapon]:
        return self.weapons
    def print_ascii_art(self):
        print(r"""
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⠒⠒⠒⠒⠒⠢⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠋⠀⠀⠀⢀⡵⣄⠀⠀⠀⠈⢢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⢹⡤⣸⠁⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⣀⠤⠤⣀⡀⠀⠀⣀⠠⠤⢀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⢾⣿⡯⢤⣀⣀⢹⠏⣿⣁⣀⣠⢤⣿⣿⠾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡟⠁⠀⣷⣿⡋⠀⠈⣿⣿⠃⠀⢹⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣈⣧⡀⠀⠀⣰⠀⠀⠀⢹⡀⠀⠀⣸⣇⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⠖⣺⣍⣽⣵⣾⠏⢟⠛⠉⠈⠓⣤⡔⠋⠈⠑⢛⠟⣿⣤⣹⢍⣷⡒⢤⣤⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣤⡖⢹⣣⠘⣿⣧⠿⠿⠛⢻⠸⡄⠈⠳⠤⠤⠔⠉⠓⠤⠤⠴⠊⠀⡇⢹⠛⠲⠿⢄⣿⡇⢠⣿⠓⢢⡄⠀⠀⠀
⠀⠀⢠⣾⡉⠑⠔⠛⠉⠁⠀⠀⠀⠀⢸⠀⠑⠤⢄⣀⣀⣀⣀⣀⣀⣀⣀⡤⠞⠁⢸⠀⠀⠀⠀⠀⠉⠙⠃⠖⠁⣹⣆⠀⠀
⠀⠀⣸⠀⠈⠢⡀⠀⠀⠀⠀⠀⠀⠀⠘⣄⡤⢤⠀⠈⢟⠳⣄⡔⢹⠏⠀⢠⠤⣄⡏⠀⠀⠀⠀⠀⠀⠀⣀⡤⠊⠀⢸⠀⠀
⠀⠀⡇⠀⠀⠀⠈⢇⠀⠀⣤⠤⠤⠤⠤⠤⣤⣼⠀⠀⠈⣞⠀⢸⠏⠀⠀⢨⣾⠽⠯⠿⠿⠿⢯⡇⠀⢠⠏⠀⠀⠀⠘⡇⠀
⠀⠀⡇⠀⠀⠀⠀⠈⢦⠀⠧⣀⠀⠀⠀⣀⠼⠉⠉⠒⠦⢼⣆⣎⠤⠖⠊⠁⠸⢄⡀⠀⠀⢀⡠⠇⢠⠏⠀⠀⠀⠀⠀⡇⠀
⠀⠀⠁⠀⠀⠀⠀⠀⢸⡷⣄⠀⠉⠉⠉⠀⠀⠀⠀⠀⢀⣀⣿⡇⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⢀⠴⣟⡀⠀⠀⠀⠀⠀⡇⠀
⠀⠀⣆⠀⠀⠀⠀⠀⣸⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢹⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⢸⡃⠀⠀⠀⠀⢀⡇⠀
⠀⣰⠋⠉⠉⠉⠉⠉⠉⠳⡄⠈⢧⡀⠀⠀⠀⠀⠀⠀⠰⣶⢾⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠏⢀⡴⠋⠉⠉⠉⠉⠉⠉⢳⡀
⢀⡇⠀⠀⠀⠀⠀⠀⠀⢡⣸⠆⠀⠉⣹⠷⢶⣶⣶⣤⣤⡤⢼⣤⣤⣤⣤⣶⣶⠶⢿⡉⠁⠀⣎⣠⠂⠀⠀⠀⠀⠀⠀⠀⡇
⠈⡇⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀⠧⡀⠀⠀⠀⠀⠉⠉⠛⠛⠉⠀⠀⠀⠀⢀⡴⠇⠀⠀⢸⢿⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⢱⣄⢀⠀⠀⢠⡀⠀⢀⡞⠀⠀⠀⠀⡇⠀⠀⠀⠀⠐⢢⠦⢴⠒⠀⠀⠀⠀⢈⡇⠀⠀⠀⠘⣆⠀⠀⡀⠀⠀⢀⣀⣼⠃
⠀⠀⠈⠉⠓⠤⠔⠛⠊⠉⠀⠀⠀⠀⠀⠙⢄⣀⠀⢀⣀⠜⠀⠘⢄⡀⠀⢀⣀⠜⠀⠀⠀⠀⠀⠈⠉⠚⠓⠠⠴⠋⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣶⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⣷⣶⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠛⠛⠛⠛⠛⠋⠙⠛⠃⠀⠀⠀⠀⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀""")
    def print_def(self):
        if self.armor:
            print(f"You have {self.armor.name} equipped, giving you {self.armor.defense_value}")
        else:
            print(f"You do not have armor")

        print(f"You have a total defense value of {self.defense}")

    def print_hp(self):
        super().print_stats()
        self.print_def()



class Enemy(Character):
    def __init__(self, name, hp, max_hp, attack, defense, special=False):
        super().__init__(name, hp, max_hp, attack, defense)
        self.special = special



    def buff_all_stats(self, stat_increase):
        self.hp += stat_increase
        self.max_hp += stat_increase
        self.attack += stat_increase
        self.defense += Defense(stat_increase, stat_increase)

    def print_ascii_art(self):
        try:
            print(eval('mobs.' + underscoreify(self.name).capitalize()))
        except AttributeError as e:
            raise AttributeError(str(e) + f'Mob tried: {self.name}')


