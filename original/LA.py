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
        file = open(file_name, "r")
        file = file.readlines()
        for line in file:
            line = line.replace("\n", "")
            line.strip()
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
            if edge_info[0][1] not in self._section["[Gamma]"]:
                raise Exception(f"{edge_info[0][1]} not in Gamma")

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
        asig_list = []
        start_node = (self.__start_state, -1, asig_list)
        recursion_asig_list = [start_node]

        while len(recursion_asig_list) > 0:
            curr_state = recursion_asig_list.pop()
            curr_letter_index = curr_state[1]
            curr_asig_list = curr_state[2]
            curr_state = curr_state[0]

            if curr_letter_index == len(input_string) - 1:
                if curr_state in self.__end_state:
                    return True

            # using a reached dictionary to avoid being stuck in an epsilon loop
            if curr_letter_index not in self.__reached_state.keys():
                self.__reached_state[curr_letter_index] = {}

            # checking whether the current state doesn't have any next states (dead end)
            if curr_state not in self._adjacent_states.keys():
                continue

            # if we've reached the last character in the string and we're not in a final state we abort
            # the current configuration
            if curr_letter_index == len(input_string) - 1:
                continue

            # looking for letter edges
            next_letter = input_string[curr_letter_index + 1]

            # checking if you can go in any direction using the current letter from the input string
            if next_letter not in [x[0][0] for x in self._adjacent_states[curr_state].keys()]:
                continue

            if curr_letter_index + 1 not in self.__reached_state.keys():
                self.__reached_state[curr_letter_index + 1] = {}

            # going through all the next states using the next letter from the input string
            for next_info in self._adjacent_states[curr_state]:
                # looking for edges that have the transition character equal to the next letter from the input string
                if next_info[0][0] == next_letter:
                    # and at the same time looking for the transition symbol to be in the list already or the symbol to
                    # be epsilon (the list to be empty)
                    if next_info[0][1] == "epsilon" or next_info[0][1] in curr_asig_list:
                        # looping through all states that have the transition character equal to the next letter
                        # from the input string
                        for next_state in self._adjacent_states[curr_state][next_info]:
                            if next_state not in self.__reached_state[curr_letter_index + 1].keys():
                                self.__reached_state[curr_letter_index + 1][next_state] = False

                            # goes to the next state only if it wasn't reached before at the current letter index
                            if self.__reached_state[curr_letter_index + 1][next_state] is False:
                                if next_info[1][0] in curr_asig_list or next_info[1][0] == "epsilon":

                                    next_asig_list = curr_asig_list.copy()

                                    # check for next_info[1][0] to be in the list, because we need to know if
                                    # that symbol is in the list or not
                                    if next_info[1][0] in next_asig_list:
                                        if next_info[1][0] != "epsilon" and next_info[1][0] in next_asig_list:
                                            next_asig_list.remove(next_info[1][0])

                                    # check for next_info[1][0] to not be in the list, because we don't need duplicates
                                    # if the symbol from the edge is epsilon we don't add anything on the list
                                    if next_info[1][1] != "epsilon" and next_info[1][1] not in next_asig_list:
                                        next_asig_list.append(next_info[1][1])

                                    # we push the current configuration to the stack
                                    # similar to making a new recursive call
                                    recursion_asig_list.append((next_state, curr_letter_index + 1, next_asig_list))

                                    # we mark the next state as reached, so we will not make any calls to that
                                    # configuration in the future
                                    self.__reached_state[curr_letter_index + 1][next_state] = True

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
