# import random
import pygame
from pygame.locals import Rect, QUIT


# globals
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
        # borders are permanent
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
            ((0, 0), (0, 0)),  # dark
            ((0, 0), (0, 0)),  # white
            ((0, 0), (0, 0)),  # dark
            ((0, 0), (0, 0))   # white
        )

    def create_field():
        pass

    def set_mines():
        pass

    def set_values():
        pass

    def neighbours():
        pass

    def draw_screen(self):
        pass

    def draw_border(self):
        for i, border in enumerate(self.borders):
            color = COLORS['dark'] if i % 2 == 0 else 'white'
            pygame.draw.line(self.screen, pygame.Color(color),
                             border[0], border[1], width=2)

    def draw_field():
        pass

    # TODO: refactoring of this spaghetti
    def run(self):
        pygame.init()
        pygame.display.set_caption('Seemine')
        self.screen.fill(pygame.Color(COLORS['gray']))

        # TODO: Remove
        temp_margin = 8
        temp_size = MINE_SIZE * self.size + 4
        # game rect
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         Rect(temp_margin, temp_margin+42, temp_size,
                              temp_size))

        self.draw_screen()
        self.draw_border()

        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()


if __name__ == '__main__':
    # seemine = Seemine()
    # seemine = Seemine('intermediate')
    seemine = Seemine('expert')
    seemine.run()
