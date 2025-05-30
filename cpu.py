import sys

import pygame

class Cpu:

    def __init__(self, monitor, keyboard):
        self.monitor = monitor
        self.keyboard = keyboard

        self.memory = [0] * 4096

        self.reg_v = [0] * 16
        self.index_reg = 0

        self.delay_timer = 0
        self.sound_timer = 0

        self.pc = 0x200 # Program counter, viene inizializzato a 0x200 perchè nella memoria la prima istruzione della rom si trova a 0x200

        self.stack= [] # We don't need the stack pointer, because in python we can append and pop

    def pygame_event_handle(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                pass
            elif event.type == pygame.KEYUP:
                pass

    def load_sprite(self):
        sprite = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,   # 0
            0x20, 0x60, 0x20, 0x20, 0x70,   # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,   # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,   # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,   # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,   # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,   # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,   # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,   # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,   # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,   # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,   # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,   # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,   # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,   # E
            0xF0, 0x80, 0xF0, 0x80, 0x80    # F
        ]

        for i, sprite in enumerate(sprite):
            self.memory[i] = sprite

    def load_rom(self, rom):
        rom_bin = open(rom, "rb")

        for i, binary in enumerate(rom_bin.read()):
            self.memory[0x200+i] = binary


    def update_timer(self):
        if self.delay_timer != 0:
            self.delay_timer -= 1
        elif self.sound_timer != 0:
            self.sound_timer -= 1

    def cycle(self):
        opcode = self.memory[self.pc] >> 8 | self.memory[self.pc+1]
        '''
        Si fa questa cosa perchè un'istruzione è formata da 16bit
        ma vengono salvate nella memoria in blocchi di 8bit
        quindi bisogna unire Program Counter corrente con quello successivo
        il bitwise >> 8 permette di far diventare la prima parte in un int da 16bit
        es. 1100 0011 >>8 = 1100 0011 0000 0000 | 0011 1100 = 1100 0011 0011 1100 (opcode finale)
        '''

        self.update_timer()


    def execute_opcode(self, opcode):
        addr = opcode & 0x0FFF
        nibble = opcode & 0x000F
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        kk = opcode & 0x00FF
        op = opcode & 0xF000
        match opcode:
            case 0x00E0: #CLS
                self.monitor.clear()
            case 0x00EE: #RET
                self.pc = self.stack.pop()

        match op:
            case 0x1000: # Program counter = addr
                self.pc = addr
            case 0x2000:
                self.stack.append(self.pc)
                self.pc = addr
            case 0x3000:
                if self.reg_v[x] == kk:
                    self.pc += 2
            case 0x4000:
                if self.reg_v[x] != kk:
                    self.pc += 2
            case 0x5000:
                if self.reg_v[x] == self.reg_v[y]:
                    self.pc += 2
            case 0x6000:
                self.reg_v[x] = kk
            case 0x7000:
                self.reg_v[x] = self.reg_v[x] + kk
