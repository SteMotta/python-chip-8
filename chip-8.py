from os.path import exists

import pygame

from keyboard import Keyboard
from monitor import Monitor
from cpu import Cpu
import sys

def main():

    rom = sys.argv[1]

    monitor = Monitor(10)
    keyboard = Keyboard()
    cpu = Cpu(monitor, keyboard)

    clock = pygame.time.Clock()

    if exists(rom):
        cpu.load_rom(rom)
    else:
        print("ROM not found")
        sys.exit()

    while True:
        clock.tick(60)
        cpu.pygame_event_handle()