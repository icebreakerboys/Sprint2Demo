# Imports
import keyboard
import sys
import time
import threading
import random
import pygame

# Helpper Functions

def start_audio():
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

# Initialize pygame mixer
pygame.mixer.init()

def clear_console():
    # Clears Console to make the easily readible
    print("\033[H\033[J", end="")

def key_listener():
    # Waits for the SpaceBar to be Pressed Used in Slow Typing Animation 
    global stop_animation
    while not stop_animation:
        if keyboard.is_pressed('space'):
            stop_animation = True
            break

def slow_type(text, delay=0.05):
    # Slowly Types Text to the Console can be skipped by pressing Space
    global stop_animation
    stop_animation = False
    listener_thread = threading.Thread(target=key_listener, daemon=True)
    listener_thread.start()
    for index, char in enumerate(text):
        if stop_animation:
            sys.stdout.write(text[index:])
            sys.stdout.flush()
            break
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    stop_animation = True

def choose(numOfOptions):
    # Gets an input from the player that qualifies as a valid option 
    choice = input("Selection: ").strip()
    checking = True
    while checking: 
        if not choice.isdigit() or (int(choice) < 1 or int(choice) > numOfOptions):
            print(f"Please enter a digit 1 - {numOfOptions}")
            choice = input("Selection: ").strip()
        else:
            checking = False
    return choice

def pick_option(prompt, choices):
    # Sets up the prompt and options to be picked from by the player
    print("\nPress the Space Bar to Skip Animation\n", end="")
    text = prompt + "\n"
    i = 1
    for choice in choices:
        text += f"{i}. {choice}\n"
        i+=1
    slow_type(text)

    choice = int(choose(len(choices))) - 1

    clear_console()
    return choice

def read_lines_from_file(file_path, start_line, end_line):
    # Returns a specified range of lines from file 
    selected_lines = []
    with open(file_path, 'r') as file:
        for current_line_num, line_content in enumerate(file, start=1):
            if start_line <= current_line_num <= end_line:
                selected_lines.append(line_content.strip())
            elif current_line_num > end_line:
                break
    return selected_lines

def dialog_selection(lines, text):
    # Used when there are multiple dialog options
    # Prepares and displays the dialog selection screen
    prompt = "What do you do?\n"
    options = []
    numOfOptions = 0
    for line in lines:
        if line == "#0":
            break
        options.append(line + "\n")
    
    return pick_option(prompt, options)

def dialog_direction(lines, text, choice):
    # Used when there are multiple dialog options
    # Directs dialog to fit choosen option 
    skipNum = 0
    printOption = False
    for line in lines:
        skipNum += 1
        if line == "#Dialog":
            break
        elif line == "#Done" and printOption:
            printOption = False
        elif printOption:
            text += line + "\n"
        elif line == f"#{choice}":
            printOption = True
        
    return skipNum, text


def dialog(line_start, end_line):
    # Controls displaying dialog
    global player
    print("\nPress the Space Bar to Skip Animation\n")
    text = ""
    skipNum = 0
    lines = read_lines_from_file("dialog.txt", line_start, end_line)
    for index, line in enumerate(lines):
        if skipNum > 0:
            skipNum -= 1
        elif line == "#Options":
            choice = dialog_selection(lines[index+1:], text)
            skipNum, text = dialog_direction(lines[index+1:], text, choice)
        else:     
            text += line + "\n"
    text = text.replace("Player", player.name)
    slow_type(text)
    print("Press the Space Bar to continue")
    keyboard.wait('Space')
    clear_console()
    time.sleep(0.2)

class Character:
    # Class used to manage and keep track stats for both the Player and Enemies
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.special_counter = 3 # only used for player 
        self.health_potion_count = 10 # only used for player
        self.maxHealth = health # only used for player

    def take_damage(self, damage):
        # Used to deal Damage to Character
        raw_damage = damage - self.defense
        self.defense = max(0, self.defense - damage)
        self.health = max(0, self.health - raw_damage)

    def is_alive(self):
        # Used to Determine if Character is Alive
        return self.health > 0 

    def drink_health_potion(self):
        # Used whenever the Player heals
        self.health = min(self.maxHealth, self.health + 50)
        self.special_counter = 3
        self.health_potion_count -= 1

    def is_special_ready(self, inc):
        # Used whenever we need to check to see if the player's special is ready
        if self.special_counter == 3:
            return True
        elif inc:
            self.special_counter += 1
            return False
        else:
            return False


def enemy_turn(enemy):
    global player
    enemy_action = random.choice(["Attack", "Defend"])
    text = ""
    if enemy_action == "Attack":
        #attack
        if player.defense <= 0:
            text += f"{enemy.name} Attacks you for {enemy.attack} Damage\n\n"
        elif enemy.defense < player.attack:
            text += f"{enemy.name} Attacks you for {enemy.attack} Damage\nYou have {player.defense} defense so they will deal a total of {enemy.attack - player.defense} damage.\n\n"
        else:
            text += f"{enemy.name} Attacks you for {enemy.attack} Damage\nYou have {player.defense} defense so they will thankfully deal 0 damage.\n\n"     
        player.take_damage(enemy.attack)
    elif enemy_action == "Defend":
        #defend
        enemy.defense += 3
        text += f"{enemy.name} defends for an attack!\nThey have perpared a total of {enemy.defense} block to negate incoming damage\n\n"
    return text

def excute_player_action(action, enemy):
    global player, weapon, special_attack
    text = ""
    if action == 0:
        #attack
        if enemy.defense <= 0:
            text += f"You {weapon} for {player.attack} damage!\n\n"
        elif enemy.defense < player.attack:
            text += f"You {weapon} for {player.attack} damage!\n{enemy.name} has {enemy.defense} defense so you will deal a total of {player.attack - enemy.defense} damage.\n\n"
        else:
            text += f"You {weapon} for {player.attack} damage!\n{enemy.name} has {enemy.defense} defense so you will sadly deal 0 damage.\n\n"
        enemy.take_damage(player.attack)
    elif action == 1:
        #defend
        player.defense += 5
        text += f"You defend for an attack!\nYou have perpared a total of {player.defense} block to negate incoming damage\n\n"
    elif action == 2 and player.health_potion_count > 0:
        #heal
        if player.is_special_ready(False): 
            text += f"You drink a Health Potion and heal for {min(player.maxHealth - player.health, 50)} HP\nYou feel replenished! Your special is back up\n\n"
        else: 
            text += f"You drink a Health Potion and heal for {min(player.maxHealth - player.health, 50)} HP\n\n"
        player.drink_health_potion()
    elif action == 3 or (action == 2 and not player.health_potion_count > 0):
        #special
        if enemy.defense <= 0:
            text += f"You {special_attack} for {2*player.attack} damage!\nYour Exhausted! You won't be able to do that again for a while.\n\n"
        elif enemy.defense < player.attack:
            text += f"You {special_attack} for {2*player.attack} damage!\nYour Exhausted! You won't be able to do that again for a while.\n{enemy.name} has {enemy.defense} defense so you will deal a total of {2*player.attack - enemy.defense} damage.\n\n"
        else:
            text += f"You {special_attack} for {2*player.attack} damage!\nYour Exhausted! You won't be able to do that again for a while.\n{enemy.name} has {enemy.defense} defense so you will sadly deal 0 damage.\n\n"
        enemy.take_damage(2*player.attack)
        player.special_counter = 0
    return text

def combat(enemy):
    # Conducts Combat
    global player, weapon, special_attack
    player.defense = 5
    inCombat = True
    print(f"You have encountered a {enemy.name} prepare to fight")
    while inCombat:
        print(f"\nYour HP: {player.health} | {enemy.name} HP {enemy.health}")

        # Player's Turn

        # Determining Player's Availible Actions and their action choice
        options = [weapon, "Prepare to Defend"]
        if player.health_potion_count > 0:
            options.append(f"Drink Health Potion 50 HP ({player.health_potion_count} left)")
        if player.is_special_ready(True):
            options.append(f"{special_attack}")
        action = pick_option("Pick an Action:", options) #clears console 

        print(f"\nYour HP: {player.health} | {enemy.name} HP {enemy.health}")
        print("\nPress the Space Bar to Skip Animation\n")

        # Execute Player's Action
        text = excute_player_action(action, enemy) # adds players turn to text 

        if enemy.is_alive():
            # Enemies Turn
            text += enemy_turn(enemy) # adds Enemies turn to text
        else:
            text += f"\nYou've Beaten {enemy.name}\n"
            inCombat = False
        
        slow_type(text) # Prints Text to Screen and prepare for next turn 
        print("Press the Space Bar to continue")
        keyboard.wait('Space')
        clear_console()
        time.sleep(0.2)

        # Check if player is dead and if enemies won
        if not player.is_alive():
            slow_type(f"\n\n Game Over")
            if not input("Enter Q to quit or anything else to Restart: ").strip() == "Q":
                play()
            else:
                exit()
            
def combat_set(enemies):
    global player
    player.health_potion_count = 10
    player.special_counter = 3
    pygame.mixer.music.load('11-Fighting.mp3')
    start_audio()
    ran_num = random.randint(1, 2)
    i = 2
    while ran_num >= 0:
        ran_enemy = random.randint(0,i)
        combat(enemies[ran_enemy])
        enemies.pop(ran_enemy)
        ran_num -= 1
        i -= 1
    stop_audio()
    pygame.mixer.music.load('12-Fanfare.mp3')
    start_audio()

def play():
    # Start Of Game
    pygame.mixer.music.load('01-The Prelude.mp3')
    start_audio()

    clear_console()
    player_name = input("\nWhat is your name?\n")

    global player
    player = Character(player_name, 100, 30, 5)
    
    clear_console()
    #sex = pick_option("What Sex would you like to play as?", ["Male", "Female", "Other"])
    dialog(64, 65)
    breakfast = pick_option("What do you eat for breakfast?", ["Cereal","Cooked eggs","Raw onion"])
    clothes = pick_option("What clothes are you wearing for work?", ["Suit","Casual","Bathing suit","Bath robe"])
    dialog(68, 68)
    no_brush_teeth = pick_option("Do you brush your teeth?", ["Yes", "No"])
    no_shower = pick_option(f"Do you take a shower?", ["Yes","No"])
    dialog(71, 73)
    dialog(76, 80)

    if clothes == 0:
        dialog(2, 5)
    elif clothes == 1:
        dialog(8, 12)
    elif clothes == 2:
        dialog(15, 24)
    elif clothes == 3:
        dialog(27, 31)

    if no_shower and no_brush_teeth and breakfast == 2:
        dialog(34, 49)
    elif no_brush_teeth and breakfast == 2:
        dialog(52, 54)
    elif no_shower:
        dialog(57, 61)
        
    #story of world
    dialog(83, 86)
    clear_console()
    dialog(89, 97)
    clear_console()
    dialog(100, 110)
    clear_console()
    dialog(113, 119)
    clear_console()
    stop_audio()
    pygame.mixer.music.load('28-On That Day, 5 Years Ago.mp3')
    start_audio()
    dialog(122,131)
    clear_console()
    dialog(134,134)
    clear_console()    
    dialog(137,137)
    clear_console()
    
    global weapon, special_attack

    weapons = pick_option("Weapon?", ["Sword", "Bow", "Staff"])

    dialog(138,139)
    clear_console()
    dialog(140,140)
    print()

    special_attack = ""
    if weapons == 0:
        special_attack = "Perform a Jump Attack"
        weapon = "Attack with your Sword"
        dialog(141,141)
        clear_console()
    elif weapons == 1:
        special_attack = "Perform a Charge Shot"
        weapon = "Attack with your Bow"
        dialog(142,142)
        clear_console()
    elif weapons == 2:
        special_attack = "Cast a Greater Fireball"
        weapon = "Cast a Minor Fireball"
        dialog(143,143)
        clear_console()

    dialog(146,151)
    clear_console()

    #Battles for the Valley
    
    valley_enemy = [Character("Flowering Cactoid", 50, 10, 3), Character("Mandragora",80,10,3), Character("Treant",100,20,5)]
    combat_set(valley_enemy)

    dialog(154,154)
    clear_console()
    stop_audio()
    pygame.mixer.music.load('86-The Birth of God.mp3')
    start_audio()
    dialog(157,163)    
    clear_console()

    #Batles for the Stormspire

    mountain_enemy = [Character("Golem", 100, 20, 25), Character("Troll",60,30,10), Character("Goblin",40,15,1)]
    combat_set(mountain_enemy)

    dialog(166,166)
    clear_console()
    stop_audio()
    pygame.mixer.music.load('52-The Nightmare\'s Beginning.mp3')
    start_audio()
    dialog(169,176)
    clear_console()
    
    #Battle for the Marsh

    marsh_enemy = [Character("Wild Onion", 50, 10, 5), Character("Deadly Nightshade",60,15,3), Character("Dark Wisp",40,15,1)]
    combat_set(marsh_enemy)

    dialog(179,179)
    stop_audio()
    pygame.mixer.music.load('52-The Nightmare\'s Beginning.mp3')
    start_audio()
    dialog(182,188)
    clear_console()
    dialog(191,203)
    stop_audio()

    player = Character(player_name,100,30,30)
    gorlath = Character("Gorlath",300,30,30)
    pygame.mixer.music.load('21-Still More Fighting.mp3')
    start_audio()
    combat(gorlath)
    stop_audio()
    pygame.mixer.music.load('12-Fanfare.mp3')
    start_audio()
    dialog(202,202)
    stop_audio()
    pygame.mixer.music.load('62-Interrupted by Fireworks.mp3')
    start_audio()
    dialog(205,224)
    clear_console()
    dialog(226,226)

play()