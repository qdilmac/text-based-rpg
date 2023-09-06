# Simple text-based RPG game
# that I wrote to sharpen my python skills
# Author: Mustafa Osman Dilmaç

import time
import os
import random
import sys

class Player:
    def __init__(self,name,health,attack,defence):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defence
        self.inventory = []

class Enemy(Player):
    def __init__(self, name, health, attack, defence):
        super().__init__(name, health, attack, defence)

def title_screen():
    print("""
          ########################################################################
                \||/
                |  @___oo
      /\  /\   / (__,,,,|
     ) /^\) ^\/ _)
     )   /^\/   _)                  Welcome to The Lands Not Between
     )   _ /  / _)
 /\  )/\/ ||  | )_)                    "Definitely NOT Elden Ring"
<  >      |(,,) )__)
 ||      /    \)___)\\              Text-Based "Souls-Like" Python Game
 | \____(      )___) )___                         v0.1
  \______(_______;;; __;;;
          ########################################################################
          """)
    time.sleep(1)
    opening_lines = ["You found yourself in mysterious cave",
             "All you remember is someone called you 'You get no maidens haha lol'",
             "You feel the rage in you. You tell yourself:",
             "> I'll not called maidenless ever again! I should hit the gym at Altus Pilates!",
             "Can you reach to the GYM without being obliterated on the way?"]
    for line in opening_lines:
        for l in line:
            print(l,end="")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")
    input("Press ENTER to continue...\n")

rand_room = random.randint(0,8) # we cant allow player to randomly teleport to rooms 9,10 and 11
rooms_list = ["r0","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10","r11"]

rooms = {
    "r0": {"desc":"You're in the cave. If you don't come out you'll be eaten by hungry rats.\nThere is 4 exits that are named pretty strangely.",
           "connects_to":["r1","r3","r6","r7"]},
    "r1": {"desc":"You wandered in to some huge forest in the middle of Mimgravel.\nAnd you stumbled upon some random dude.",
           "npc":{"name": "Viriel the Dog"},
           "connects_to":["r0","r2"]},
    "r2": {"desc":"After that inspiring talk with that dude you decided to \nfollow the shallow path that leads to a chest. And there is something guarding it!",
           "npc":{"name": "Dead Man with Loot","items":["Big Sword","Shiny Armor"]},
           "connects_to":["r1"]},
    "r3": {"desc":"O-oh traveller. I think your dreams to get shredded ends here.\nThere is a Stick Looking Man with a mighty sword! And he respawns every time you kill him too???",
           "enemy": {"name": "Stick Looking Man","health": 30, "attack": 10, "defence": 2},
           "connects_to":["r0","r4"]},
    "r4": {"desc":"While fighting Stick Looking Man he smashed his mighty sword on to a wall and cracked open some hidden room.\nAnd there is an old wizard who wants to talk to you.",
           "npc":{"name": "Lore Giver Fiji"},
           "connects_to":["r5"]},
    "r5": {"desc":"HAHA you've been bamboozled. Hippity hoppity, your room selection right now my property!",
           "connects_to":[rooms_list[rand_room]]},
    "r6": {"desc":"You saw a hut in the big lake that's named 'Big Lake'.\nYou're not sure but you think there is someone waving at you.\nThat must be Definitely Not Scammer Trader Joe!",
           "npc":{"name": "Definitely Not Scammer Trader Joe","items":["Bandage Wrapped Stick","Literally Just a Stick"]},
           "connects_to":["r0","r8"]},
    "r7": {"desc":"After some time on the road you saw a huge tower and decided to climb to it for some loot.\nThere is a mysterious lady that wants to hug you.",
           "npc":{"name": "Fifa the Huggiver"},
           "connects_to":["r0","r8"]},
    "r8": {"desc":"You've been on the road for quite some time.\nFor some much needed rest you decided to take shelter in nearest hut-like thing.\nTo your luck, there is another adventurer with interesting and definitely not boring and incredible long stories.",
           "connects_to":["r6","r7","r9"]},
    "r9": {"desc":"You listened that adventurer's 'inspiring' tales for so long that you had to leave.\nYou've seen some light coming from a crack on the mountain's wall.\nYou crawled into it and suddenly the cracked closed!\nThere is a old man with a thousand meter long beard waiting for you to get up.",
           "npc":{"name": "Spammer Gideon"},
           "connects_to":["r10"]},
    "r10": {"desc":"You walked through that mist wall. You know what to expect now.\nThis is the boss room! Epic orchestral music kicks in and the boss made his epic entry to the scene!.\nHis name is... 'Margaret the Risen Luck'! Yes his name is Margaret. Deal with it.",
            "boss":{"name": "Fat Rolling Man","health": 100, "attack": 20, "defence": 20},
            "connects_to":["r11"]},
    "r11": {"desc":"WELCOME TO THE ALTUS PILATES!",
            "connects_to":[]}
    }

starting_room = "r0"
current_room = starting_room
player = None # this little thing solved a lot of problems for me :d Can now access created player (character) data across all functions
npcs_without_items = []

def create_character():
    global player
    print("\nWhat's your character's name?")
    c_name = input(">")
    print("\nYour health, attack and defense stats will be randomly assigned.\nDon't ask why its probably because of game's lore or smthn.\n")
    c_health = random.randint(80,120)
    c_attack = random.randint(5,25)
    c_defence = random.randint(1,10)
    player = Player(c_name,c_health,c_attack,c_defence)
    time.sleep(1)
    print(f"Your final stats >> Name: {player.name}, Health: {player.health}, Attack: {player.attack}, Defence: {player.defense}") # this line tought me the F-string insted of .format()

def load_room(room_name):
    global current_room
    room = rooms[room_name]
    print("\n"+room["desc"])

    if "npc" in room:
       load_npc(room["npc"])
    if "enemy" in room:
       load_enemy(room["enemy"])

def load_npc(npc_data):
    npc_name = npc_data["name"]
    print(f"You've encountered {npc_name}")

    if npc_name in npcs_without_items:
        print(f"{npc_name} doesn't have anything more to offer right now.")
    elif "items" in npc_data:
        items = npc_data["items"]
        if items:
            print(f"{npc_name} has the following items:")
            for index, item in enumerate(items, start=1):
                print(f"{index}. {item}")

            choice = input("Choose an item number: ")
            try:
                chosen_index = int(choice) - 1
                if 0 <= chosen_index < len(items):
                    chosen_item = items[chosen_index]
                    print(f"You chose: {chosen_item}")
                    player.inventory.append(chosen_item)
                    apply_item_effects(chosen_item, player)
                    npcs_without_items.append(npc_name)  # Mark the NPC as having given an item
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
        else:
            print(f"{npc_name} doesn't have any items right now.")
    
def load_enemy(enemy_data):
    enemy_name = enemy_data["name"]
    print(f"You've encountered {enemy_name}")

    if "health" in enemy_data:
        enemy_health = enemy_data["health"]
        print(f"{enemy_name} has {enemy_health} health points.")

    if "attack" in enemy_data:
        enemy_attack = enemy_data["attack"]
        print(f"{enemy_name} has {enemy_attack} attack points.")

    if "defence" in enemy_data:
        enemy_defence = enemy_data["defence"]
        print(f"{enemy_name} has {enemy_defence} defence points.")

def apply_item_effects(item, player):
    # Define item effects on player's stats
    if item == "Bandage Wrapped Stick":
        player.health += 10  # Example: Increase player's health
    elif item == "Literally Just a Stick":
        player.attack += 2   # Example: Increase player's attack

def main_game():
    global current_room
    player = Player("Player", 100, 10, 5)

    while True:
        room = rooms[current_room]
        print("\n" + room["desc"])

        if not room["connects_to"]:
            time.sleep(1)
            print("Congrats! You somehow finished the game! Here have some cookie :]")
            input("Press ENTER to quit the game...")
            break

        connected_rooms = room["connects_to"]
        print("Roads to follow to: ", ", ".join(connected_rooms))
        room_choice = input("Which road do you want to go to? ").lower()

        if room_choice in connected_rooms:
            current_room = room_choice
            load_room(current_room)  # Load the chosen room
        else:
            print("Please provide a correct road name.\n")
            time.sleep(0.5)

if __name__ == "__main__":
    title_screen()
    create_character( )
    main_game()
