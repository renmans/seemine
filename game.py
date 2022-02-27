# NOTES
# TODO: U can use more flags than there are mines
# TODO: Fix bug with a red background after losing

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
        self.gameover = False
        self.gameover_pos = None
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
        self.overlay = np.array(
            [[0 for _ in range(self.size)] for _ in range(self.size)])

    def set_mines(self):
        count = 0
        while count < self.mines:
            x, y = randrange(0, self.size), randrange(0, self.size)
            if self.field[y][x] != -1:
                self.field[y][x] = -1
                count += 1

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
        # hotfix
        pygame.draw.line(self.screen, pygame.Color('white'),
                         (self.screen_size[0]-10, 52),
                         (self.screen_size[0]-10, self.screen_size[1]-9))
        pygame.draw.line(self.screen, pygame.Color('white'),
                         (8, self.screen_size[1]-10),
                         (self.screen_size[0]-9, self.screen_size[1]-10))

    def draw_grid(self):
        pygame.draw.rect(self.screen, pygame.Color(COLORS['gray']),
                         Rect(10, 52, self.size * 16, self.size * 16))
        for i in range(self.size):
            pygame.draw.line(self.screen, pygame.Color(COLORS['dark']),
                             (10+(16*i), 50),
                             (10+(16*i), self.screen_size[1]-10), width=1)
            pygame.draw.line(self.screen, pygame.Color(COLORS['dark']),
                             (8, 52+(16*i)),
                             (self.screen_size[0]-10, 52+(16*i)), width=1)

    def draw_overlay_block(self, x, y):
        pygame.draw.rect(self.screen, pygame.Color(COLORS['gray']),
                         Rect(x, y, 16, 16))
        pygame.draw.line(self.screen, pygame.Color('white'),
                         (x, y), (x+15, y), width=2)
        pygame.draw.line(self.screen, pygame.Color('white'),
                         (x, y), (x, y+15), width=2)
        pygame.draw.line(self.screen, pygame.Color(COLORS['dark']),
                         (x+14, y), (x+14, y+15), width=2)
        pygame.draw.line(self.screen, pygame.Color(COLORS['dark']),
                         (x, y+14), (x+15, y+14), width=2)

    def draw_field_overlay(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.overlay[i][j]:
                    self.draw_overlay_block(10+(16*j), 52+(16*i))

    def draw_exploded_block(self, x, y):
        pygame.draw.rect(self.screen, pygame.Color('red'),
                         Rect(11+(16*x), 53+(16*y), 15, 15))

    def update_overlay(self, x, y):
        if self.field[y][x] == -1:
            self.gameover = True
            self.gameover_pos = (x, y)
            for i in range(self.size):
                for j in range(self.size):
                    if self.field[i][j] == -1:
                        self.overlay[i][j] = 1
        else:
            self.overlay[y][x] = 1

    def draw_mine(self, x, y):
        pygame.draw.line(self.screen, pygame.Color('black'),
                         (x+7, y+1), (x+7, y+13))
        pygame.draw.line(self.screen, pygame.Color('black'),
                         (x+1, y+7), (x+13, y+7))
        pygame.draw.line(self.screen, pygame.Color('black'),
                         (x+3, y+3), (x+11, y+11))
        pygame.draw.line(self.screen, pygame.Color('black'),
                         (x+11, y+3), (x+3, y+11))
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         Rect(x+5, y+3, 5, 9))
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         Rect(x+3, y+5, 9, 5))
        pygame.draw.rect(self.screen, pygame.Color('white'),
                         Rect(x+5, y+5, 2, 2))

    def draw_mines(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == -1:
                    self.draw_mine(11+(16*j), 53+(16*i))

    def draw_counter():
        pass

    def draw_dropdown_menu():
        pass

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        x = (x - 11) // 16
        y = (y - 53) // 16
        return (x, y)

    def get_button_pressed(self):
        r = [*range(self.size)]
        lmb, _, rmb = pygame.mouse.get_pressed()
        if lmb:
            x, y = self.get_mouse_pos()
            if x in r and y in r:
                self.update_overlay(x, y)
        elif rmb:
            print(f"RMB: {self.get_mouse_pos()}")

    def prep(self):
        self.create_field()
        self.set_mines()

    # TODO: refactoring of this spaghetti
    def run(self):
        pygame.init()
        pygame.display.set_caption('Seemine')
        self.screen.fill(pygame.Color(COLORS['gray']))

        self.prep()

        while True:
            pygame.display.flip()
            if not self.gameover:
                self.draw_grid()
                self.get_button_pressed()
                self.draw_field_overlay()
            else:
                self.draw_exploded_block(*self.gameover_pos)
                self.draw_mines()
            self.draw_borders()  # should be last step
            for event in pygame.event.get():
                if event.type == QUIT:
                    print(self.overlay)
                    pygame.quit()


if __name__ == '__main__':
    # seemine = Seemine()
    # seemine = Seemine('intermediate')
    seemine = Seemine('expert')

    seemine.run()
