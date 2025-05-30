import pygame

OFF = (0, 0, 0)
ON = (255, 255, 255)

WIDTH, HEIGHT = 64, 32

class Monitor:

    def __init__(self, scale):
        pygame.display.set_caption('Chip-8 Emulator')

        self.scale = scale

        pygame.init()

        self.display = [0]*HEIGHT*64*WIDTH

        self.win = pygame.display.set_mode((WIDTH*scale, HEIGHT*scale))
        self.win.fill(OFF)

        pygame.display.flip()

    def clear(self):
        self.win.fill(OFF)
        pygame.display.flip()