import random as rand
from src.classes import *
import src.data
from time import sleep

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
        "\tPhysical Weapons are generally slightly stronger than spells, however Physical Weapons have durability")
    print("\tDurability is simply the amount of times you can use it")
    print("\tDebuff Spells debuff the enemy in some way. They have limited uses!")
    print("\tYou can only use 7 debuff potions per chamber.")
    print("Armor: This type of gear will increase your defense temporarily. Also has durability.")
    print("1 armor durability is subtracted every time you take damage.")

    print("Your objective is to get through all 50 rounds of trial chambers. ")
    print("After defeating an enemy in the chamber, you will be rewarded with items. ")
    print("After defeating a boss, a Restoration Tower will restore your health to maximum.")
    print("This game is a turn based game, you always start with the first turn.")

    print("Good luck, and have fun!\n\n")


def pick_mob(chamber_num) -> Enemy:
    if (picked_mob := data.bosses.get(chamber_num)) is None:
        return rand.choice(data.regular_mobs)
    else:
        return picked_mob

inventory: list[tuple[str, int]] = [] # int being amount of uses

def spell_take_damage(index):
    inventory[index] = (inventory[index][0], inventory[index][1]-1)
    if inventory[index][1] <= 0:
        inventory.pop(index)

def battle(player: Player, enemy: Enemy):
    global inventory
    muted = False
    potions = 0
    while player.is_alive() and enemy.is_alive():
        sleep(0.5)
        print("\n")
        enemy.print_ascii_art()
        print(enemy.name)
        enemy.print_stats()
        print('\n\n')

        sleep(0.25)
        print(f"Player: {player.name}")
        player.print_ascii_art()
        player.print_stats()
        if not muted:
            println(30)

            while True:
                for weapon_num, weapon in enumerate(player.weapons_list()):
                    print(f"{weapon_num + 1}: {weapon}")

                print(f"5. Open Inventory")

                prev_spell_count = potions
                action = _input()

                if 1 <= action <= 4 and player.weapons_list()[action - 1]:
                    break
                elif action == 5:
                    pass
                else:
                    print("Not a valid choice. ")

                while action == 5:
                    if potions >= 7:
                        print("You cannot use any more potions in this chamber!")
                        break
                    if len(inventory) == 0:
                        print("You have no items in your inventory.")
                    for index, item in enumerate(inventory):
                        print(f"{index + 1}: {item[0]} - {item[1]} uses remaining")
                    print(f"{(exit_num := len(inventory)+1)}: Exit")

                    while True:
                        inv_input = _input()-1
                        if 0 <= inv_input <= exit_num-1:
                            break
                        else:
                            print("Invalid!")

                    exit_num -= 1
                    if inv_input == exit_num:
                        break

                    match inventory[inv_input][0]:
                        case "Shield Depletor":
                            print("Enemy's both type of defense reduced by 10%!")
                            enemy.defense.reduce_multiplicative("Both", 10)

                            potions += 1
                            break
                        case "Sword Dull'r":
                            print("Enemy attack reduced by 3!")
                            enemy.attack -= 2
                            potions += 1
                            break
                        case "Carcinogenic Potion":
                            print("Enemy attack reduced by 1, Enemy physical defense reduced by 7%!")
                            enemy.defense.reduce_multiplicative("Phys", 7)
                            potions +=1
                            break
                        case "Steel Melter":
                            print("Enemy attack reduced by 2, Enemy Physical Defense reduced by 4%!")
                            enemy.defense.reduce_multiplicative("Phys", 4)
                            enemy.attack += 2
                            potions +=1
                            break
                        case "Magic Res. Shredder":
                            print("Enemy Magic Defense reduced by 25%!")
                            enemy.defense.reduce_multiplicative("Magic", 25)
                            potions += 1
                            break
                        case _:
                            print("Invalid!")

                if action == 5 and potions > prev_spell_count:
                    spell_take_damage(inv_input)


            weapon_selected = player.weapons_list()[action - 1]
            damage_dealt = DamageType.calc_dmg(weapon_selected.damage + player.attack,
                                               eval(f"enemy.defense.{weapon_selected.damage_type}"))

            enemy.take_damage(damage_dealt)

            if weapon_selected.name == 'Life Steal Dagger':
                print(f"Your Life Steal dagger healed you for {(healing := damage_dealt)}!")
                player.heal(healing)

            player.weapons_list()[action - 1].take_dur_damage()
            if enemy.is_alive():
                player_take_dmg = DamageType.calc_dmg(enemy.attack, eval(f"player.defense.{data.mob_type[enemy.name]}"))
                player.take_damage(player_take_dmg)

        else:
            print("You were silenced! You cannot take a turn!")

        if not player.is_alive() or not enemy.is_alive():
            break

        if not muted and rand.randint(1, 3) == 3 and enemy.name != 'Xareth, the Void Emperor':
            if enemy.special:
                if enemy.name != "Wizard":
                    # this is because spilling a spell by accident is not a special ability
                    print(f"{enemy.name} has a SPECIAL ability! ")
                sleep(0.25)
                match enemy.name:
                    case "Healer":
                        print('The healer healed herself for 1 health!')
                        enemy.heal(1)
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
                        print("The Golem Fortifies itself! (+ 2 Physical Defense)")
                        enemy.defense += Defense(2, 0)
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
            if rand.randint(1, 4) == 2:
                print("Xareth buffs himself!")
                print("Xareth gains +1 attack, +2 defense, +2 hp")
                enemy.attack += 1
                enemy.defense += Defense(2,2)
                enemy.heal(2)
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
        options.append(rand.choice(data.Debuff_Spells))

    print("Weapons: ")
    for index, option in enumerate(options):
        if index == 2:
            print("Debuff Spells: ")
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
    if 2 <= enc_choice <= 3:
        inventory.append((chosen, 5))
        print("Successfully added to inventory!")
        return
    print("Which weapon would you like to replace? ")
    for weapon_num, weapon in enumerate(player.weapons_list()):
        print(f"{weapon_num + 1}: {weapon}")
    print(f"5. I changed my mind - exit")

    while True:
        replace = _input()
        if replace == 5:
            return
        elif 1 <= replace <= 4:
            player.weapons[replace-1] = chosen
            break
        else:
            print("Invalid! ")

    print("Weapon replaced successfully.")


def blessing(player: Player, jason_counter: int, forced_blessing: str | None = None) -> bool:
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
                return False
            elif 1 <= chosen_blessing_index <= 3:
                break
            else:
                print("Invalid option!\n")

        chosen_blessing_index -= 1  # 0-index list
        chosen_blessing = choices[chosen_blessing_index]
    else:
        chosen_blessing = forced_blessing
        print(f"You received the {chosen_blessing} blessing.")
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
            print(f"Consuming your health lowered your health to {player.hp} hp!")
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
            print("Heals you to max hp instantly and restores 2 durability to all current weapons.")
            player.heal(99999)
            for weapon in player.weapons:
                if weapon is not None:
                    weapon.durability += 2
        case _:
            raise IndexError(f"Blessing Does Not Exist: blessing given: {blessings} -> {chosen_blessing}")

    if not forced_blessing:
        print("Press Enter to continue...")
    return True

def main():
    global inventory
    replay = True
    while replay:
        data.init_defs()
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
        inventory = []

        print(f"Hello {player.name}. We have been expecting you. The first trial chamber is already open.")

        enemy_buff = 0

        player.weapons[0] = Weapon('Fist', 1000, 2, DamageType("Phys"))  # fist
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
                if not blessing(player, jason_counter):  # returns true if blessing is given else false
                    print("Your blessing has caused the mobs to become stronger...")
                    enemy_buff += 1

        if player.is_alive():
            print("You have successfully conquered Xareth's Dungeon. You win!")
            print("Would you like to play again?")

            replay = (input()[0].lower() == 'y')
            if not replay:
                exit("See you again, Prisoner...")
            print("\n\n")
            break


if __name__ == '__main__':
    main()
