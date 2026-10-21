# Ivascu_Ioan-Andrei_143
import LA


class Game(LA.LA):
    def __init__(self, file_name):
        super().__init__(file_name)
        self.__play_game()

    def get_description(self, name):
        # dict with description of every room
        descriptions = {
            "Entrance_Hall": "The grand foyer of the Castle of Illusions.",
            "Dining_Room": "A room with a large table filled with an everlasting feast.",
            "Kitchen": "A room packed with peculiar ingredients.",
            "Armoury": "A chamber filled with antiquated weapons and armour.",
            "Treasury": "A glittering room overflowing with gold and gemstones.",
            "Library": "A vast repository of ancient and enchanted texts.",
            "Pantry": "A storage area for the Kitchen",
            "Throne_Room": "The command center of the castle.",
            "Wizard’s_Study": "A room teeming with mystical artifacts.",
            "Secret_Exit": "The hidden passage that leads out of the Castle of Illusions."
        }

        return descriptions[name]

    def __play_game(self):
        play_game = 1
        sigma = super().get_section("[Sigma]")
        states = super().get_section("[State]")
        adjacent_states = super().get_adjacency_list()
        delta = super().get_section("[Delta]")
        game_input = ""

        # keeping track of every item in evey room
        items_per_room = {
            "Entrance_Hall": ["key"],
            "Dining_Room": ["invitation", "chef’s_hat"],
            "Kitchen": ["spoon"],
            "Armoury": ["sword", "crown"],
            "Treasury": ["ancient_coin"],
            "Library": ["spell book"],
            "Pantry": [],
            "Throne_Room": [],
            "Wizard’s_Study": ["magic_wand"],
            "Secret_Exit": []
        }

        # we start in Entrance_Hall
        current_room = "Entrance_Hall"
        # create an inventory as a set
        inventory = set()

        while play_game:
            # Commands : look, take[item], drop[item], inventory, go[room_name]

            game_input = input()

            if game_input == "look":
                # print the room description
                print(self.get_description(current_room))
                # print the adjacent rooms
                print([x[0][0] for x in self._adjacent_states[current_room].keys() if x[0][0] != current_room])

            if game_input == "exit":
                # the game is over when it reads exit
                play_game = 0
                break

            # if the input is not look or exit it will be go[], take[] or drop[]
            game_input = game_input.split("[")
            game_input[1] = game_input[1].strip("]")

            if game_input[0] == "go":
                adjacent = 0
                inv = 0
                # checking for the next room to be adjacent to the current room
                # and checking if I have the necessary item to enter that room
                for i in self._adjacent_states[current_room].keys():
                    if i[0][0] == game_input[1]:
                        adjacent = 1
                    else:
                        print(f"There is no path from {current_room} to {game_input[1]}")
                    if i[0][1] in inventory or i[0][1] == "epsilon":
                        inv = 1
                    else:
                        print(f"You don't have the {i[0][1]} to be able to enter the {game_input[1]}")
                if adjacent == 1 and inv == 1:
                    current_room = game_input[1]

            # checking if the certain item is in the current room and removing it from the room after i take it
            if game_input[0] == "take":
                if game_input[1] in items_per_room[current_room]:
                    inventory.add(game_input[1])
                    items_per_room[current_room].remove(game_input[1])
                else:
                    print(f"There is no {game_input[1]} in this room")

            # checking if the item is in the inventory and dropping it in
            # current room and removing it from the inventory
            if game_input[0] == "drop":
                if game_input[1] in inventory:
                    inventory.remove(game_input[1])
                    items_per_room[current_room].append(game_input[1])
                else:
                    print(f"There is no {game_input[1]} in inventory")


