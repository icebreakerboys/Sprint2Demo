# Imports
import keyboard
import sys
import time
import threading

# Helpper Functions

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

def dialog_options(lines, text):
    # Used when there are multiple dialog options
    # Displays Options and directs dialog lines to fit choosen option 
    skipNum = 0
    text += "What do you do?\n"
    numOfOptions = 0
    for line in lines:
        if line == "#1":
            break
        numOfOptions += 1
        text += line + "\n"
    slow_type(text)
    text = ""

    choice = choose(numOfOptions)

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
    text = ""
    skipNum = 0
    lines = read_lines_from_file("dialog.txt", line_start, end_line)
    for index, line in enumerate(lines):
        if skipNum > 0:
            skipNum -= 1
        elif line == "#Options":
            skipNum, text = dialog_options(lines[index+1:], text)
        else:     
            text += line + "\n"
    slow_type(text)
    print("\nPress the Space Bar to continue")
    keyboard.wait('Space')
    clear_console()
    time.sleep(0.2)

# Start Of Game

clear_console()
player_name = input("What is your name?\n")
clear_console()
sex = pick_option("What Sex would you like to play as?", ["Male", "Female", "Other"])
#Wake up
breakfast = pick_option("What do you eat for breakfast?", ["Cereal","Cooked eggs","Raw onion"])
clothes = pick_option("What clothes are you wearing for work?", ["Suit","Casual","Bathing suit","Bath robe"])
#Your running late
no_brush_teeth = pick_option("Do you brush your teeth?", ["Yes, (Costs 2 mins)", "No"])
no_shower = pick_option(f"Do you take a shower?", ["Yes (Costs 10 mins)","No"])
#Quickly get to work!
#Wake up in world
#Meet wizard

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


