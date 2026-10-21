import tempfile
import unittest
from pathlib import Path
from Game import Game
from LA import LA

ROOT = Path(__file__).resolve().parent


class ExamTests(unittest.TestCase):
    def game(self):
        return Game(ROOT / 'game_config.txt', autoplay=False)

    def test_look_and_inventory(self):
        game = self.game()
        self.assertIn('key', game.execute('look'))
        self.assertIn('empty', game.execute('inventory'))

    def test_invalid_commands(self):
        for command in ('', 'hello', 'take', 'go[]', 'go[a][b]'):
            self.assertIn('Unknown', self.game().execute(command))

    def test_required_item(self):
        game = self.game()
        self.assertIn('key', game.execute('go[Armoury]'))
        self.assertEqual(game.current_room, 'Entrance_Hall')

    def test_take_drop(self):
        game = self.game()
        game.execute('take[key]')
        game.execute('drop[key]')
        self.assertNotIn('key', game.inventory)
        self.assertIn('key', game.items_per_room['Entrance_Hall'])

    def test_complete_escape(self):
        game = self.game()
        for command in ('take[key]', 'go[Armoury]', 'take[sword]', 'go[Treasury]',
                        'take[ancient_coin]', 'go[Library]', 'go[Secret_Exit]'):
            result = game.execute(command)
        self.assertIn('escaped', result)
        self.assertTrue(game.finished)

    def test_hat_name(self):
        game = self.game()
        for command in ('go[Dining_Room]', "take[chef's_hat]", 'go[Kitchen]'):
            game.execute(command)
        self.assertEqual(game.current_room, 'Kitchen')

    def test_spell_book_name(self):
        game = self.game()
        self.assertIn('spell_book', game.items_per_room['Library'])

    def test_no_path(self):
        self.assertIn('no path', self.game().execute('go[Secret_Exit]'))

    def test_original_config(self):
        automaton = LA(ROOT / 'LA_config.txt')
        self.assertFalse(automaton.check_string(''))
        self.assertFalse(automaton.check_string('xy'))
        with self.assertRaisesRegex(Exception, 'Sigma'):
            automaton.check_string('z')

    def test_epsilon_and_memory_branches(self):
        config = '''[Sigma]
x
epsilon
[Gamma]
a
b
epsilon
[State]
s, 0
t, 1
f, 2
[Delta]
s, epsilon, epsilon, -> (s, epsilon, epsilon)
s, x, epsilon, -> (t, epsilon, a)
s, x, epsilon, -> (t, epsilon, b)
t, epsilon, b, -> (f, b, epsilon)
'''
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            path = Path(directory) / 'config.txt'
            path.write_text(config, encoding='utf-8')
            automaton = LA(path)
            for _ in range(2):
                self.assertTrue(automaton.check_string('x'))
                self.assertFalse(automaton.check_string(''))
                self.assertFalse(automaton.check_string('xx'))


if __name__ == '__main__':
    unittest.main()
