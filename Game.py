"""Interactive castle game driven by the exam automaton configuration."""
import re
import LA


class Game(LA.LA):
    def __init__(self, file_name, *, autoplay=True):
        super().__init__(file_name)
        self.items_per_room = {
            "Entrance_Hall": ["key"],
            "Dining_Room": ["invitation", "chef's_hat"],
            "Kitchen": ["spoon"],
            "Armoury": ["sword", "crown"],
            "Treasury": ["ancient_coin"],
            "Library": ["spell_book"],
            "Pantry": [],
            "Throne_Room": [],
            "Wizard’s_Study": ["magic_wand"],
            "Secret_Exit": []
        }

        self.current_room = self.get_start_state()
        self.inventory = set()
        self.finished = False
        if autoplay:
            self.play()

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

    def execute(self, command):
        command = command.strip()
        if command == "exit":
            self.finished = True
            return "Goodbye!"
        if command == "help":
            return "look | inventory | take[item] | drop[item] | go[room] | exit"
        if command == "inventory":
            return "Inventory: " + (", ".join(sorted(self.inventory)) or "empty")
        if command == "look":
            rooms = sorted({edge[0][0] for edge in self._adjacent_states.get(self.current_room, {})})
            return (self.get_description(self.current_room) + "\nRooms: " + ", ".join(rooms)
                    + "\nItems: " + (", ".join(self.items_per_room[self.current_room]) or "none"))
        match = re.fullmatch(r"(go|take|drop)\[([^\[\]]+)\]", command)
        if not match:
            return "Unknown command. Type help."
        action, target = match.groups()
        if action == "take":
            if target not in self.items_per_room[self.current_room]:
                return f"There is no {target} in this room"
            self.items_per_room[self.current_room].remove(target)
            self.inventory.add(target)
            return f"Taken: {target}"
        if action == "drop":
            if target not in self.inventory:
                return f"There is no {target} in inventory"
            self.inventory.remove(target)
            self.items_per_room[self.current_room].append(target)
            return f"Dropped: {target}"
        matching = [(edge, destinations) for edge, destinations in self._adjacent_states.get(self.current_room, {}).items() if edge[0][0] == target]
        if not matching:
            return f"There is no path from {self.current_room} to {target}"
        for edge, destinations in matching:
            required = edge[0][1]
            if required == "epsilon" or required in self.inventory:
                self.current_room = destinations[0]
                if self.current_room in self.get_end_states():
                    self.finished = True
                    return "You escaped the Castle of Illusions!"
                return f"Entered: {self.current_room}"
        return "Required item: " + ", ".join(sorted({edge[0][1] for edge, _ in matching}))

    def play(self):
        print("Castle of Illusions — type help for commands.")
        print(self.execute("look"))
        while not self.finished:
            try:
                command = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            print(self.execute(command))
