# Ivascu_Ioan-Andrei_143
class LA:
    def __init__(self, file_name):
        self._section = {}
        self.__end_state = []
        self.__file = []
        self.__start_state = -1
        self.__reached_state = {}
        self._adjacent_states = {}
        self.__parse_file(file_name)

    def __parse_file(self, file_name):
        with open(file_name, "r", encoding="utf-8") as stream:
            file = stream.readlines()
        for line in file:
            line = line.replace("\n", "")
            line = line.strip()
            if line != "" and line[0] != '#':
                self.__file.append(line)

        self.__load_sections()

    # goes through the parsed file and adds each section into the section dictionary
    def __load_sections(self):
        curr_section = ""
        for line in self.__file:
            if line[0] == '[':
                curr_section = line
            else:
                if curr_section not in self._section.keys():
                    self._section[curr_section] = set()
                self._section[curr_section].add(line)

        self._validate_states()
        self._validate_delta()

    def _validate_states(self):

        states = self.get_section("[State]")
        new_states_section = set()
        for line in states:
            tokens = line.split(', ')
            tokens = [token.replace("\n", "") for token in tokens]
            new_states_section.add(tokens[0])
            for state_type in range(1, len(tokens)):
                if tokens[state_type] == "0":
                    if self.__start_state != -1:
                        raise Exception("There is already a start state")
                    else:
                        self.__start_state = tokens[0]
                if tokens[state_type] == "2":
                    self.__end_state.append(tokens[0])

        self._section["[State]"] = new_states_section

    # checks the delta function from the file
    # creates the graph of the Automaton
    def _validate_delta(self):
        for steps in self._section["[Delta]"]:
            line = steps.split('>')
            tokens = line[0].split(', ')
            tokens.pop()

            # file manipulation
            line[1] = line[1].split(', ')
            line[1] = [lin.replace("\n", "") for lin in line[1]]
            line[1] = [lin.replace(" (", "") for lin in line[1]]
            line[1] = [lin.replace(")", "") for lin in line[1]]

            origin_state = tokens[0]
            edge_info = ((tokens[1], tokens[2]), (line[1][1], line[1][2]))
            destination_state = line[1][0]

            if origin_state not in self._section["[State]"]:
                raise Exception(f"{origin_state} not in States")
            if destination_state not in self._section["[State]"]:
                raise Exception(f"{destination_state} not in States")
            if edge_info[0][0] not in self._section["[Sigma]"]:
                raise Exception(f"{edge_info[0][0]} not in Sigma")
            if edge_info[0][1] not in self._section["[Gamma]"]:
                raise Exception(f"{edge_info[0][1]} not in Gamma")
            if edge_info[1][0] not in self._section["[Gamma]"]:
                raise Exception(f"{edge_info[1][0]} not in Gamma")
            if edge_info[1][1] not in self._section["[Gamma]"]:
                raise ValueError(f"{edge_info[1][1]} not in Gamma")

            if origin_state not in self._adjacent_states.keys():
                self._adjacent_states[origin_state] = {}

            if edge_info not in self._adjacent_states[origin_state].keys():
                self._adjacent_states[origin_state][edge_info] = []
            self._adjacent_states[origin_state][edge_info].append(destination_state)

    def print_sections(self):
        print(self._section)
        print(f"Start state: {self.__start_state}\nEnd state: {self.__end_state}")

    def get_section(self, section_name):
        if section_name in self._section.keys():
            return self._section[section_name]
        else:
            raise Exception(f"There is no {section_name}")

    def get_end_states(self):
        return self.__end_state

    def get_start_state(self):
        return self.__start_state

    def get_adjacency_list(self):
        return self._adjacent_states

    # checks if there's any path in the graph that ends in a final state
    # it's a basically a dfs, but made with a stack instead of recursion in order to bypass stack overflow
    def __exists_path(self, input_string):
        # A configuration includes memory: equal states can have different futures.
        pending = [(self.__start_state, 0, frozenset())]
        visited = set()
        while pending:
            state, index, memory = pending.pop()
            configuration = (state, index, memory)
            if configuration in visited:
                continue
            visited.add(configuration)
            if index == len(input_string) and state in self.__end_state:
                return True
            for ((symbol, required), (remove, add)), destinations in self._adjacent_states.get(state, {}).items():
                if symbol != "epsilon" and (index == len(input_string) or input_string[index] != symbol):
                    continue
                if required != "epsilon" and required not in memory:
                    continue
                if remove != "epsilon" and remove not in memory:
                    continue
                next_memory = set(memory)
                next_memory.discard(remove)
                if add != "epsilon":
                    next_memory.add(add)
                for destination in destinations:
                    pending.append((destination, index + (symbol != "epsilon"), frozenset(next_memory)))
        return False

    # checks the validity of the string and verifies whether the string is accepted by the automata
    # returns True if the string is accepted and False otherwise
    def check_string(self, input_string):
        alphabet = self.get_section("[Sigma]")
        for curr_char in input_string:
            if curr_char not in alphabet:
                raise Exception(f"Invalid string\n{curr_char} -> not in Sigma")

        path = self.__exists_path(input_string)
        self.__reached_state = {}

        return path

    def reset(self):
        self._section = {}
        self.__end_state = []
        self.__file = []
        self.__start_state = -1
        self.__reached_state = {}
        self._adjacent_states = {}
