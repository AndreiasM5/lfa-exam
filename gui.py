"""Minimal clickable map. All game rules remain in Game.py."""
from pathlib import Path

import pygame

from Game import Game

ROOT = Path(__file__).resolve().parent
ROOMS = {
    'Entrance_Hall': (35, 85),
    'Dining_Room': (225, 85),
    'Kitchen': (415, 85),
    'Pantry': (605, 85),
    'Armoury': (35, 255),
    'Treasury': (225, 255),
    'Library': (415, 255),
    'Throne_Room': (35, 425),
    'Wizard’s_Study': (225, 425),
    'Secret_Exit': (605, 425),
}
BG = (240, 239, 232)
INK = (40, 44, 44)
GREEN = (132, 197, 151)


def label(name):
    return name.replace('_', ' ').replace('’', "'")


class MapWindow:
    def __init__(self):
        pygame.font.init()
        self.surface = pygame.display.set_mode((800, 700))
        pygame.display.set_caption('Castle of Illusions')
        self.font = pygame.font.Font(None, 23)
        self.small = pygame.font.Font(None, 20)
        self.rooms = {room: pygame.Rect(x, y, 155, 62) for room, (x, y) in ROOMS.items()}
        self.reset_button = pygame.Rect(674, 18, 105, 32)
        self.reset()

    def reset(self):
        self.game = Game(ROOT / 'game_config.txt', autoplay=False)
        self.message = 'Click a room to move.'
        self.actions = []

    def text(self, value, position, *, small=False, color=INK):
        self.surface.blit((self.small if small else self.font).render(value, True, color), position)

    def draw(self):
        self.surface.fill(BG)
        self.text('Castle of Illusions', (24, 25))
        pygame.draw.rect(self.surface, (215, 215, 207), self.reset_button, border_radius=5)
        self.text('Restart', (695, 26))
        # One line per physical connection; direction and keys are enforced by Game.
        connections = set()
        for origin, edges in self.game.get_adjacency_list().items():
            for destinations in edges.values():
                for destination in destinations:
                    connections.add(tuple(sorted((origin, destination))))
        for origin, destination in sorted(connections):
            pygame.draw.line(self.surface, (184, 184, 175), self.rooms[origin].center, self.rooms[destination].center, 2)
        for room, rect in self.rooms.items():
            current = room == self.game.current_room
            color = GREEN if current else (255, 255, 250)
            pygame.draw.rect(self.surface, color, rect, border_radius=6)
            pygame.draw.rect(self.surface, INK, rect, 2 if current else 1, border_radius=6)
            self.text(label(room), (rect.x + 9, rect.y + 12), small=True)
            if current:
                pygame.draw.circle(self.surface, INK, (rect.centerx, rect.y + 45), 5)
        pygame.draw.rect(self.surface, (225, 224, 216), (0, 520, 800, 180))
        self.actions = []
        if self.game.finished:
            self.text('You escaped!', (24, 544), color=(35, 110, 55))
        else:
            self.text('Room: click to take', (24, 538), small=True)
            self.buttons(self.game.items_per_room[self.game.current_room], 561, 'take')
            self.text('Bag: click to drop', (24, 600), small=True)
            self.buttons(sorted(self.game.inventory), 623, 'drop')
        self.text(self.message, (24, 677), small=True)

    def buttons(self, items, y, action):
        x = 24
        if not items:
            self.text('-', (x, y + 5), small=True)
        for item in items:
            width = self.small.size(label(item))[0] + 18
            if x + width > 780:
                x, y = 24, y + 27
            rect = pygame.Rect(x, y, width, 25)
            pygame.draw.rect(self.surface, (255, 255, 250), rect, border_radius=4)
            self.text(label(item), (x + 9, y + 5), small=True)
            self.actions.append((rect, f'{action}[{item}]'))
            x += width + 7

    def click(self, position):
        if self.reset_button.collidepoint(position):
            self.reset()
            return
        if self.game.finished:
            return
        for rect, command in self.actions:
            if rect.collidepoint(position):
                self.message = self.game.execute(command)
                return
        for room, rect in self.rooms.items():
            if rect.collidepoint(position) and room != self.game.current_room:
                self.message = self.game.execute(f'go[{room}]')
                return

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click(event.pos)
            clock.tick(30)


if __name__ == '__main__':
    try:
        MapWindow().run()
    finally:
        pygame.quit()
