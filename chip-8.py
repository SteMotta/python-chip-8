from os.path import exists
import pygame
from keyboard import Keyboard
from monitor import Monitor
from cpu import Cpu
import sys

def main():
    print(sys.argv)

    rom = sys.argv[1]

    monitor = Monitor(20)
    keyboard = Keyboard()
    cpu = Cpu(monitor, keyboard)
    clock = pygame.time.Clock()

    cpu.load_sprite()

    if exists(rom):
        cpu.load_rom(rom)
    else:
        print("ROM not found")
        sys.exit()

    while True:
        clock.tick(60)
        cpu.pygame_event_handle() # Event handle per la chiusura del gioco
        cpu.cycle()

if __name__ == "__main__": main()