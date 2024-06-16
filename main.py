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
    print(
        "\tPhysical Weapons are generally slightly stronger than offensive spells, however Physical Weapons have durability")
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
                print(f"{weapon_num + 1}: {weapon}")

            print(f"5. Open Inventory")

            while True:
                action = _input()
                if 1 <= action <= 4 and player.weapons_list()[action - 1]:
                    break
                else:
                    print("Not a valid choice. ")

            weapon_selected = player.weapons_list()[action - 1]
            damage_dealt = DamageType.calc_dmg(weapon_selected.damage + player.attack,
                                               eval(f"enemy.defense.{weapon_selected.damage_type}"))
            enemy.take_damage(damage_dealt)
            player_take_dmg = DamageType.calc_dmg(enemy.attack, eval(f"player.defense.{data.mob_type[enemy.name]}"))
            player.take_damage(player_take_dmg)

        else:
            print("You were silenced! You cannot take a turn!")

        if not player.is_alive() or not enemy.is_alive():
            break

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
                        if rand.randint(1, 2) == 1:
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
                        raise IndexError(f"battle special ability not existed, given: {enemy.name}")


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


def encounter(player: Player):
    println()
    print("You have passed the chamber trial. Its rewards shall be bestowed upon thee.")

    options = [rand.choice(data.Weapons) for _ in range(2)]
    for spell in range(2):
        options.append(rand.choice(data.Offensive_Spells))

    for index, option in enumerate(options):
        print(f"{index + 1}. {option}")

    print("5. Leave with nothing")

    while True:
        enc_choice = _input()
        if enc_choice == 5:
            return
        elif 1 <= enc_choice <= 4:
            break
        else:
            print("Invalid! ")

    enc_choice -= 1  # for 0-index
    chosen = options[enc_choice]
    print("Which weapon would you like to replace? ")
    for weapon_num, weapon in enumerate(player.weapons_list()):
        print(f"{weapon_num + 1}: {weapon}")
    print(f"5. I changed my mind - exit")

    while True:
        replace = _input()
        if replace == 5:
            return
        elif 1 <= replace <= 4:
            player.weapons[replace] = chosen
            break
        else:
            print("Invalid! ")

    print("Weapon replaced successfully.")


def blessing(player: Player, jason_counter: int, forced_blessing: str | None = None):
    blessings = {
        'Gift of Medora': "Grants +20 permanent max hp",
        'Blessing of Goldor': "Grants +7 defense of both types",
        "A Fraction of Zeus' Strength": "Grants +5 permanent attack",
        "Devil's Exchange": "Consumes 30% of your current health to grant a permanent +10 max hp, and +5 attack. This blessing cannot kill you.",
        "Josh's Blessing": "Grants +10 permanent max hp and +5 magic defense",
        "0.01% of Jason's True Strength": "Grants +3 Attack per Jasons fought this session",
        "Maxor's Courtesy": "Grants +15 permanent max hp",
        "The Great Defender's Protection": "Grants +10 Physical Defense",
        'The Joker Card': "Picks another blessing at random",
        "Sealing Wax of Destruction": "Grants +3 attack and +5 max hp",
        "The Protector's Grace": "Heals you to max hp instantly and restores 2 durability to all current weapons."
    }
    if not forced_blessing:
        println()
        print('You come across an altar of worship. ')
        print("You see an ancient script, giving you instructions on how to gain the favour of the gods...")
        sleep(0.25)
        print("You perform the instructions, and writing appears on the wall: ")

        choices = [rand.choice(list(blessings.keys())), rand.choice(list(blessings.keys())),
                   rand.choice(list(blessings.keys()))]

        while True:
            for index, choice in enumerate(choices):
                print(f"{index + 1}: {choice}: {blessings[choice]}")
            print("4. Leave without a blessing (why?)")
            chosen_blessing_index = _input()
            if chosen_blessing_index == 4:
                print("You left without any blessing...")
                return
            elif 1 <= chosen_blessing_index <= 3:
                break
            else:
                print("Invalid option!\n")

        chosen_blessing_index -= 1  # 0-index list
        chosen_blessing = choices[chosen_blessing_index]
    else:
        chosen_blessing = forced_blessing
    match chosen_blessing:
        case "Gift of Medora":
            print(f"{player.max_hp} max hp increased to {player.max_hp+20}")
            player.max_hp += 20
        case 'Blessing of Goldor':
            print("Defense Buff Granted Successfully")
            player.defense = player.defense + Defense(7,7)
        case "A Fraction of Zeus' Strength":
            print(f"{player.attack} attack increased to {player.attack + 5}")
            player.attack += 5
        case "Devil's Exchange":
            player.hp *= 0.7
            if player.hp <= 1:
                player.hp = 1
            player.max_hp += 10
            player.attack += 5

            print(f"{player.max_hp-10} max hp increased to {player.max_hp}")
            print(f"{player.attack-10} attack increased to {player.attack}")
            print(f"Consuming your health lowered your health to {player.hp}!")
        case "Josh's Blessing":
            player.max_hp += 10
            player.defense = player.defense + Defense(0,5)
            print(f"{player.max_hp-10} max hp increased to {player.max_hp}")
            print(f"Defense Buff Granted Successfully")
        case "0.01% of Jason's True Strength":
            prev_atk = player.attack
            player.attack += (jason_counter*3)
            print(f"{prev_atk} atk increased to {player.attack}")
        case "Maxor's Courtesy":
            player.max_hp += 15
            print(f"{player.max_hp-15} max hp increased to {player.max_hp}")
        case "The Great Defender's Protection":
            player.defense = player.defense + Defense(15, 0)
            print("Defense Buff Granted Successfully")
        case "The Joker Card":
            print("You got the joker card!")
            blessing(player, jason_counter, rand.choice(list(blessings.keys())))
        case "Sealing Wax of Destruction":
            player.attack += 3
            player.max_hp += 5
            print(f"{player.attack-3} attack increased to {player.attack}")
            print(f"{player.max_hp -5} max hp increased to {player.max_hp}")
        case "The Protector's Grace":
            "Heals you to max hp instantly and restores 2 durability to all current weapons."
            player.heal(99999)
            for weapon in player.weapons:
                weapon.durability += 2
        case _:
            raise IndexError("Blessing Does Not Exist")


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
        data.init_defs()
        player.weapons[0] = (data.Weapons[0])  # fist
        jason_counter = 0
        for chamber in range(1, 51):
            println(40)
            print(f"CHAMBER {chamber}")
            data.init_defs()
            picked_mob = pick_mob(chamber)
            picked_mob.buff_all_stats(enemy_buff)
            if picked_mob.name == 'Jason':
                jason_counter += 1
            battle(player, picked_mob)
            if chamber in data.bosses.keys():  # is a boss
                print("You defeated a boss! A Restoration Tower has restored your health to max.")
                player.heal(9999)  # overflow healing means nothing

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

            encounter(player)
            if chamber % 5 == 0:
                blessing(player, jason_counter)

        if player.is_alive():
            raise NotImplementedError("MISSING SOME KIND OF WINNING MESSAGE")


if __name__ == '__main__':
    main()
