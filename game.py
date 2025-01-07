print("Helloworld")
# Ask for the user's name
user_name = input("What is your name? ")

# Ask the user to choose a weapon by typing its name
weapon_choice = input("Choose your weapon (Sword, Bow and Arrow, or Staff): ").strip().lower()

# Map the choice to a weapon
if weapon_choice == 'sword':
    weapon = "Sword"
elif weapon_choice == 'bow and arrow':
    weapon = "Bow and Arrow"
elif weapon_choice == 'staff':
    weapon = "Staff"
else:
    print("Invalid choice, defaulting to Sword.")
    weapon = "Sword"

# Ask the user to choose a pet by typing its name
pet_choice = input("Choose your pet (Tiger, Dragon, or Grizzly Bear): ").strip().lower()

# Map the choice to a pet
if pet_choice == 'tiger':
    pet = "Tiger"
elif pet_choice == 'dragon':
    pet = "Dragon"
elif pet_choice == 'grizzly bear':
    pet = "Grizzly Bear"
else:
    print("Invalid choice, defaulting to Tiger.")
    pet = "Tiger"

# Display the chosen details
print(f"\nWelcome {user_name}!")
print(f"Your chosen weapon is: {weapon}")
print(f"Your chosen pet is: {pet}")
