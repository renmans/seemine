# NOTES
# TODO: U can use more flags than there are mines
# TODO: In popular implementations mines are set after opening first block

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
    'dark': (123, 123, 123),
    1: (1, 0, 254),
    2: (0, 128, 1),
    3: (254, 0, 0),
    4: (0, 0, 127),
    5: (128, 0, 0),
    6: (0, 128, 129),
    7: (0, 0, 0),
    8: (128, 128, 128)
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
        self.flags = np.array(
            [[0 for _ in range(self.size)] for _ in range(self.size)])

    def set_mines(self):
        count = 0
        while count < self.mines:
            x, y = randrange(0, self.size), randrange(0, self.size)
            if self.field[y][x] != -1:
                self.field[y][x] = -1
                count += 1

    def set_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] != -1:
                    self.field[i][j] = self.get_neighbours(i, j)

    def get_neighbours(self, i, j):
        counter = 0
        for y in [a for a in [i-1, i, i+1] if a >= 0 and a < self.size]:
            for x in [b for b in [j-1, j, j+1] if b >= 0 and b < self.size]:
                if y == i and x == j:
                    continue
                else:
                    counter += 1 if self.field[y][x] == -1 else 0
        return counter

    def empty_neighbours(self, i, j):
        if self.field[i][j] != -1:
            self.overlay[i][j] = 1
        for y in [a for a in [i-1, i, i+1] if a >= 0 and a < self.size]:
            for x in [b for b in [j-1, j, j+1] if b >= 0 and b < self.size]:
                if self.overlay[y][x] != 1 and self.field[y][x] == 0:
                    self.empty_neighbours(y, x)
                if self.field[y][x] > 0:
                    self.overlay[y][x] = 1

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

    def draw_colored_bg(self, x, y, color='red'):
        pygame.draw.rect(self.screen, pygame.Color(color),
                         Rect(11+(16*x), 53+(16*y), 15, 15))

    def draw_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] not in [-1, 0]:
                    self.draw_number(11+(16*j), 53+(16*i), self.field[i][j],
                                     COLORS[self.field[i][j]])
                    if self.field[i][j] not in [1, 2, 3]:
                        self.draw_colored_bg(j, i, COLORS[self.field[i][j]])

    def update_overlay(self, x, y):
        if self.flags[y][x] == -1:
            return
        field = self.field[y][x]
        if field == -1:
            self.gameover = True
            self.gameover_pos = (x, y)
            for i in range(self.size):
                for j in range(self.size):
                    if self.field[i][j] == -1:
                        self.overlay[i][j] = 1
        else:
            self.empty_neighbours(y, x)

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

    def draw_number(self, x, y, number, color):
        if number == 1:
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+6, y+3), (x+6, y+10))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+7, y+2), (x+7, y+10))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+8, y+2), (x+8, y+10))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+4, y+10), (x+10, y+10))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+4, y+11), (x+10, y+11))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+5, y+4), (x+5, y+4))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+4, y+5), (x+5, y+5))
        elif number == 2:
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+3, y+2), (x+10, y+2))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+2, y+3), (x+11, y+3))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+2, y+4), (x+4, y+4))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+9, y+4), (x+11, y+4))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+9, y+5), (x+11, y+5))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+7, y+6), (x+10, y+6))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+5, y+7), (x+9, y+7))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+3, y+8), (x+7, y+8))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+2, y+9), (x+5, y+9))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+2, y+10), (x+11, y+10))
            pygame.draw.line(self.screen, pygame.Color(color),
                             (x+2, y+11), (x+11, y+11))
        elif number == 3:
            pygame.draw.rect(self.screen, pygame.Color(color),
                             Rect(x+2, y+2, 9, 2))
            pygame.draw.rect(self.screen, pygame.Color(color),
                             Rect(x+9, y+3, 3, 3))
            pygame.draw.rect(self.screen, pygame.Color(color),
                             Rect(x+5, y+6, 6, 2))
            pygame.draw.rect(self.screen, pygame.Color(color),
                             Rect(x+9, y+8, 3, 3))
            pygame.draw.rect(self.screen, pygame.Color(color),
                             Rect(x+2, y+10, 9, 2))
        elif number == 4:
            pass
        elif number == 5:
            pass
        elif number == 6:
            pass
        elif number == 7:
            pass
        elif number == 8:
            pass

    def draw_counter():
        pass

    def set_flag(self, x, y):
        # 0 / -1
        self.flags[y][x] = ~self.flags[y][x]

    def draw_flag(self, x, y):
        color = 'black'
        pygame.draw.line(self.screen, pygame.Color('red'),
                         (x+6, y+3), (x+6, y+10))
        pygame.draw.rect(self.screen, pygame.Color(color),
                         Rect(x+2, y+2, 9, 2))
        pygame.draw.rect(self.screen, pygame.Color(color),
                         Rect(x+9, y+3, 3, 3))
        pygame.draw.rect(self.screen, pygame.Color(color),
                         Rect(x+5, y+6, 6, 2))
        pygame.draw.rect(self.screen, pygame.Color(color),
                         Rect(x+9, y+8, 3, 3))
        pygame.draw.rect(self.screen, pygame.Color(color),
                         Rect(x+2, y+10, 9, 2))

    def draw_flags(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.flags[i][j] == -1:
                    self.draw_flag(11+(16*j), 53+(16*i))

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
            x, y = self.get_mouse_pos()
            if x in r and y in r:
                self.set_flag(x, y)

    def win_cond(self):
        if np.sum(self.overlay) == (self.size * self.size - self.mines):
            return True
        return False

    def prep(self):
        self.create_field()
        self.set_mines()
        self.set_numbers()

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
                self.draw_numbers()
                self.draw_mines()
                self.draw_field_overlay()
                self.draw_flags()
                if self.win_cond():
                    self.gameover = True
                    print("You Win!")  # TODO: Remove
            else:
                if self.gameover_pos:
                    self.draw_colored_bg(*self.gameover_pos)
                self.draw_mines()
            self.draw_borders()  # should be last step
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()


if __name__ == '__main__':
    # seemine = Seemine()
    seemine = Seemine('intermediate')
    # seemine = Seemine('expert')

    seemine.run()
