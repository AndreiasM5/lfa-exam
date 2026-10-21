# Ivascu_Ioan-Andrei_143

import sys
import LA as LA
import Game
import time
import random


def main():

    # load a config for LA
    la = LA.LA("LA_config.txt")
    # test a string for LA
    print(la.check_string(""))

    # run the game with the specific config
    game = Game.Game("game_config.txt")


main()
