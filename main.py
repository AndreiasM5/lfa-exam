"""Run the original LFA exam examples from any working directory."""
from pathlib import Path
from Game import Game
from LA import LA


def main():
    root = Path(__file__).resolve().parent
    automaton = LA(root / "LA_config.txt")
    print("Automaton accepts empty input:", automaton.check_string(""))
    Game(root / "game_config.txt")


if __name__ == "__main__":
    main()
