import pygame

OFF = (0, 0, 0)
ON = (255, 255, 255)

WIDTH, HEIGHT = 64, 32

class Monitor:

    def __init__(self, scale):
        pygame.display.set_caption('Emulatore Chip-8')

        self.scale = scale

        pygame.init()

        self.display = [[0 for x in range (WIDTH)] for y in range(HEIGHT)] # Indica la griglia di pixel da disegnare (draw) display[WIDTH][HEIGHT]

        self.win = pygame.display.set_mode((WIDTH*scale, HEIGHT*scale))
        self.win.fill(OFF)

        pygame.display.flip()

    def clear(self):
        self.display = [[0 for x in range (WIDTH)] for y in range(HEIGHT)]
        pygame.display.flip()

    def get_win(self):
        return self.win

    def get_resolution(self):
        return WIDTH*self.scale, HEIGHT*self.scale

    def set_scale(self, scale):
        self.scale = scale
        self.win = pygame.display.set_mode((WIDTH * scale, HEIGHT * scale))


    def set_pixel(self, x:int, y:int):

        # Necessario nel caso la posizone sia fuori dallo schermo, il pixel verrà settato dal lato opposto dello schermo
        x %= WIDTH
        y %= HEIGHT

        self.display[y][x] ^= 1

        return not self.display[y][x] # Ritorna True se il pixel é 0, quindi significa che c'é stata una collisione.
        # Una collisione avviene quando si setta un pixel già settato

    def render_display(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                colour = ON if self.display[y][x] else OFF
                pygame.draw.rect(self.win, colour, (x * self.scale, y * self.scale, self.scale, self.scale), 0)
                # rect: [Posizione x del rettangolo, posizione y del rettangolo, larghezza del rettangolo, altezza del rettangolo]
        pygame.display.flip() # Per disegnare a schermo le modifiche