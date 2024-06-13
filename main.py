import random as rand
from classes import *
import mobs
import data
from time import sleep
from warnings import warn

"""
TODO: 
1. Finish working on game logic
1.5. Missing end of game...
2. ADD THE WEAPONS TO THE GAME 
2.5. add spells
3. Finish Ascii mobs 
3. ADD MORE SPELLS JLKASJFKA:SFLKJ:SEOGIJSDLKF
99. Add coloured text
"""


def _input(_prompt: str = '') -> int:
    while True:
        try:
            if _prompt == '':
                return int(input(">>> "))
            else:
                print(_prompt)
                return int(input(">>> "))
        except ValueError:
            print("Invalid input. Try again.")


def welcome_screen():
    print(r"""
 _    _      _                            _                
| |  | |    | |                          | |               
| |  | | ___| | ___ ___  _ __ ___   ___  | |_ ___          
| |/\| |/ _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \         
\  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |        
 \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/         


) (`-.       ('-.     _  .-')     ('-.   .-') _    ('-. .-.      .-')                      ('-.             _  .-')   
 ( OO ).    ( OO ).-.( \( -O )  _(  OO) (  OO) )  ( OO )  /,--. ( OO ).                   ( OO ).-.        ( \( -O )  
(_/.  \_)-. / . --. / ,------. (,------./     '._ ,--. ,--.\  |(_)---\_)       ,--.       / . --. /  ,-.-') ,------.  
 \  `.'  /  | \-.  \  |   /`. ' |  .---'|'--...__)|  | |  | `-'/    _ |        |  |.-')   | \-.  \   |  |OO)|   /`. ' 
  \     /\.-'-'  |  | |  /  | | |  |    '--.  .--'|   .|  |    \  :` `.        |  | OO ).-'-'  |  |  |  |  \|  /  | | 
   \   \ | \| |_.'  | |  |_.' |(|  '--.    |  |   |       |     '..`''.)       |  |`-' | \| |_.'  |  |  |(_/|  |_.' | 
  .'    \_) |  .-.  | |  .  '.' |  .--'    |  |   |  .-.  |    .-._)   \      (|  '---.'  |  .-.  | ,|  |_.'|  .  '.' 
 /  .'.  \  |  | |  | |  |\  \  |  `---.   |  |   |  | |  |    \       /       |      |   |  | |  |(_|  |   |  |\  \  
'--'   '--' `--' `--' `--' '--' `------'   `--'   `--' `--'     `-----'        `------'   `--' `--'  `--'   `--' '--' 


""")


def help_screen():
    print("Stats: ")
    print("HP: This is how health something has.")
    print("Attack: This is how much damage something will deal.")
    print("Defense: This stat reduces damage taken from attacks. ")
    print("\tThis stat is calculated as such: floor(damage_value * (100 - (damage_defense / 100)))")
    print("\tThere are two types of defense: Physical Resistance and Magic Resistance.")
    print("\tEach of these types of defense reduces its respective type of damage taken.")

    print("\nPlayer Exclusive Gear:")
    print("Weapon: Increases damage dealt")
    print("\tComes in two types: Physical Weapon and Offensive Spell")
    print("\tYou can only hold 4 weapons at a time")
    print("\tPhysical Weapons are generally slightly stronger than offensive spells, however Physical Weapons have durability")
    print("\tDurability is simply the amount of rounds you can use it in")
    print("\t\tNote: if you do not use the weapon in the round, durability damage will not be taken")
    print("\tOffensive Spells either deal damage or debuff the enemy in some way. They have limited uses!")
    print("Buffing Spell: This type of spell temporarily boosts one of your stats")
    print("Healing Spell: This type of spell heals you for a certain amount")
    print("Armor: This type of gear will increase your defense temporarily. Also has durability.")

    print("Your objective is to get through all 50 rounds of trial chambers. ")
    print("After defeating an enemy in the chamber, you will be rewarded with items. ")
    print("This game is a turn based game, you always start with the first turn.")

    print("Good luck, and have fun!\n\n")


def pick_mob(chamber_num) -> Enemy:
    if (picked_mob := data.bosses.get(chamber_num)) is None:
        return rand.choice(data.regular_mobs)
    else:
        return picked_mob


def battle(player: Player, enemy: Enemy):
    muted = False
    while player.is_alive() and enemy.is_alive():
        sleep(0.5)
        print("\n")
        # enemy.print_ascii_art()
        print('ascii art goes here lol')
        print(enemy.name)
        enemy.print_stats()
        print('\n\n')

        print(f"Player: {player.name}")
        player.print_ascii_art()
        player.print_stats()
        if not muted:
            println(30)
            for weapon_num, weapon in enumerate(player.weapons_list()):
                print(f"{weapon_num+1}: {weapon}")

            while True:
                action = _input()
                if 1 <= action <= 4 and player.weapons_list()[action-1]:
                    break
                else:
                    print("Not a valid choice. ")

            weapon_selected = player.weapons_list()[action-1]
            damage_dealt = DamageType.calc_dmg(weapon_selected.damage, eval(f"enemy.defense.{weapon_selected.damage_type}"))
            print(damage_dealt)

        else:
            print("You were silenced! You cannot take a turn!")


        if not muted and rand.randint(1, 3) == 3:
            if enemy.special:
                if enemy.name != "Wizard":
                    # this is because spilling a spell by accident is not a special ability
                    print(f"{enemy.name} has a SPECIAL ability! ")
                sleep(0.25)
                match enemy.name:
                    case "Healer":
                        print('The healer healed herself for 3 health!')
                        enemy.heal(3)
                    case "Wizard":
                        if rand.randint(1, 2) == 3:
                            print("The wizard spilled his healing spell on you! (player +5 hp)")
                            player.heal(5)

                    case "Jason":
                        print("Jason nerfed himself and reduced his defenses by 10!")
                        enemy.defense.reduce_additive("Both", 10)
                    case "Grim Reaper":
                        print("The Grim Reaper used Super Drain!")
                        print("The Grim Reaper stole 5 health from you!")
                        prev_user_hp = player.hp
                        prev_grim_hp = enemy.hp
                        player.take_damage(5)
                        enemy.heal(5)
                        print(f"Your health: {prev_user_hp}/{player.max_hp} --> {player.hp}/{player.max_hp}")
                        print(f"Grim Reaper health: {prev_grim_hp}/{enemy.max_hp} --> {enemy.hp}/{enemy.max_hp}")
                    case "Golem":
                        print("The Golem Fortifies itself! (+ 5 Physical Defense)")
                        enemy.defense += Defense(5, 0)
                    case "Medusa":
                        roll = (rand.randint(1, 2) == 2)  # make it harder
                        if roll:
                            print("Medusa silenced you! You cannot take the next turn. ")
                            muted = True
                        else:
                            print("Medusa tried to silence you, but failed!")
                    case _:
                        raise IndexError("battle special ability not existed")
                sleep(0.25)

        elif enemy.name == 'Xareth, the Void Emperor':
            raise NotImplementedError('yea idk ill figure something out for this')
        # maybe it could summon something?
        else:
            muted = False

    if not player.is_alive():
        print("You DIED!")
        return
    else:
        print(f"You have defeated the {enemy.name}.")


def println(length: int = 20) -> None:
    print('-' * length)


def main():
    replay = True
    while replay:
        welcome_screen()
        player_input = _input("Enter 1 to play the game, enter 2 for help, enter anything else to quit")

        match player_input:
            case 1:
                pass
            case 2:
                help_screen()
            case _:
                exit()
        player = Player(input("Prisoner, declare your name at once: "))

        if player.name == "debug":
            player.hp = _input("hp: ")
            player.max_hp = player.hp
            player.attack = _input('atk: ')
            player.name = 'CHEATS ENABLED'


        print(f"Hello {player.name}. We have been expecting you. The first trial chamber is already open.")

        enemy_buff = 0
        player.weapons[0] = (data.Weapons[0])  # fist
        for chamber in range(1, 51):
            println(40)
            print(f"CHAMBER {chamber}")
            if chamber == 50:
                picked_mob = 'Xareth, the Void Emperor'
            picked_mob = pick_mob(chamber)
            battle(player, picked_mob)

            if not player.is_alive():
                print(f"You made it {chamber} chambers in.")
                print(f"You died to a {picked_mob.name}.")
                print("You have failed! Xareth prevails once again.")
                print("Would you like to play again?")

                replay = (input()[0].lower() == 'y')
                if not replay:
                    exit("See you again, Prisoner...")
                print("\n\n")
                break

        if player.is_alive():
            raise NotImplementedError("MISSING SOME KIND OF WINNING MESSAGE")


if __name__ == '__main__':
    main()
