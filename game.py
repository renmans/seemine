# NOTES
# U can use more flags than there are mines

import pygame
import numpy as np
from random import randrange
from pygame.locals import Rect, QUIT


MINE_SIZE = 16
SETTINGS = {
    'begginer':     {'size':  9, 'mines': 10, 'screen': (164, 206)},
    'intermediate': {'size': 16, 'mines': 40, 'screen': (276, 318)},
    'expert':       {'size': 24, 'mines': 99, 'screen': (404, 446)}
}
COLORS = {
    'gray': (189, 189, 189),
    'dark': (123, 123, 123)
}


class Seemine:
    def __init__(self, difficulty='begginer'):
        self.size = SETTINGS[difficulty]['size']
        self.mines = SETTINGS[difficulty]['mines']
        self.flags = SETTINGS[difficulty]['mines']
        self.screen_size = SETTINGS[difficulty]['screen']
        self.screen = pygame.display.set_mode(self.screen_size)
        self.borders = (
            ((0, self.screen_size[1]-1),
             (self.screen_size[0], self.screen_size[1]-1)),
            ((0, 0),
             (0, self.screen_size[1])),
            ((self.screen_size[0]-1, 0),
             (self.screen_size[0]-1, self.screen_size[1])),
            ((0, 0),
             (self.screen_size[0], 0)),
            ((8, 8),
             (self.screen_size[0]-9, 8)),
            ((8, 42),
             (self.screen_size[0]-9, 42)),
            ((8, 8),
             (8, 42)),
            ((self.screen_size[0]-9, 8),
             (self.screen_size[0]-9, 42)),
            ((8, 50),
             (8, self.screen_size[1]-9)),
            ((self.screen_size[0]-9, 50),
             (self.screen_size[0]-9, self.screen_size[1]-9)),
            ((8, 50),
             (self.screen_size[0]-9, 50)),
            ((8, self.screen_size[1]-9),
             (self.screen_size[0]-9, self.screen_size[1]-9))
        )

    def create_field(self):
        self.field = np.array(
            [[0 for _ in range(self.size)] for _ in range(self.size)])
        print(self.field)  # TODO: Remove

    def set_mines(self):
        count = 0
        while count < self.mines:
            x, y = randrange(0, self.size), randrange(0, self.size)
            if self.field[y][x] != -1:
                self.field[y][x] = -1
                count += 1
        print(self.field)  # TODO: Remove

    def set_values():
        pass

    def neighbours():
        pass

    def change_difficulty():
        pass

    def draw_borders(self):
        for i, border in enumerate(self.borders):
            color = COLORS['dark'] if i % 2 == 0 else 'white'
            pygame.draw.line(self.screen, pygame.Color(color),
                             border[0], border[1], width=2)

    def draw_grid(self):
        for i in range(self.size):
            pygame.draw.line(self.screen, pygame.Color(COLORS['dark']),
                             (10+(16*i), 50),
                             (10+(16*i), self.screen_size[1]-10), width=1)
            pygame.draw.line(self.screen, pygame.Color(COLORS['dark']),
                             (8, 52+(16*i)),
                             (self.screen_size[0]-10, 52+(16*i)), width=1)

    # depends on current state of field
    def draw_field_overlay():
        pass

    def draw_counter():
        pass

    def draw_dropdown_menu():
        pass

    def prep(self):
        self.create_field()
        self.set_mines()

    # TODO: refactoring of this spaghetti
    def run(self):
        pygame.init()
        pygame.display.set_caption('Seemine')
        self.screen.fill(pygame.Color(COLORS['gray']))

        self.prep()
        self.draw_borders()  # should be last step
        self.draw_grid()

        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()


if __name__ == '__main__':
    # seemine = Seemine()
    seemine = Seemine('intermediate')
    # seemine = Seemine('expert')

    seemine.run()
