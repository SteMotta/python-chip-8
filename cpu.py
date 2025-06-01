import random
import pygame
import sys

class Cpu:

    def __init__(self, monitor, keyboard):
        self.monitor = monitor
        self.keyboard = keyboard
        self.speed = 5

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
                self.keyboard.key_down(event.key)
            elif event.type == pygame.KEYUP:
                self.keyboard.key_up(event.key)

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
        if self.delay_timer >= 0:
            self.delay_timer -= 1
        elif self.sound_timer >= 0:
            self.sound_timer -= 1

    def cycle(self):
        for _ in range(self.speed):
            opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]
            '''
            Si fa questa cosa perchè un'istruzione è formata da 16bit
            ma vengono salvate nella memoria in blocchi di 8bit
            quindi bisogna unire Program Counter corrente con quello successivo
            il bitwise >> 8 permette di far diventare la prima parte in un int da 16bit
            es. 1100 0011 >>8 = 1100 0011 0000 0000 | 0011 1100 = 1100 0011 0011 1100 (opcode finale)
            '''
            self.execute_opcode(opcode)
        self.update_timer()
        self.monitor.render_display()


    def execute_opcode(self, opcode):
        self.pc += 2
        print(hex(opcode))
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
                self.reg_v[x] = (self.reg_v[x] + kk) & 0xFF # & 0xFF perché deve essere sempre massimo un byte quindi 255
            case 0x8000:
                match nibble:
                    case 0x0:
                        self.reg_v[x] = self.reg_v[y]
                    case 0x1:
                        self.reg_v[x] = self.reg_v[x] | self.reg_v[y]
                    case 0x2:
                        self.reg_v[x] = self.reg_v[x] & self.reg_v[y]
                    case 0x3:
                        self.reg_v[x] = self.reg_v[x] ^ self.reg_v[y]
                    case 0x4:
                        addition = self.reg_v[x] + self.reg_v[y]
                        self.reg_v[x] = addition & 0xFF
                        if addition > 255:
                            self.reg_v[0xF] = 1
                        else:
                            self.reg_v[0xF] = 0
                    case 0x5:
                        vx = self.reg_v[x]
                        vy = self.reg_v[y]
                        self.reg_v[0xF] = 1 if vx >= vy else 0
                        self.reg_v[x] = (vx - vy) & 0xFF
                    case 0x6:
                        self.reg_v[0xF] = int(self.reg_v[x]) & 0x1
                        self.reg_v[x] >>= 1
                    case 0x7:
                        self.reg_v[x] = (self.reg_v[y] - self.reg_v[x]) & 0xFF
                        if self.reg_v[y] >= self.reg_v[x]:
                            self.reg_v[0xF] = 1
                        else:
                            self.reg_v[0xF] = 0
                    case 0xE:
                        self.reg_v[0xF] = (self.reg_v[x] >> 7) & 0x1
                        self.reg_v[x] = (self.reg_v[x] << 1) & 0xFF
            case 0x9000:
                if self.reg_v[x] != self.reg_v[y]:
                    self.pc += 2
            case 0xA000:
                self.index_reg = addr
            case 0xB000:
                self.pc = addr + self.reg_v[0x0]
            case 0xC000:
                self.reg_v[x] = random.randint(0, 255) & kk
            case 0xD000:
                self.reg_v[0xF] = 0

                for i in range(nibble): # Il nibble segna il numero di pixel in verticale/il numero di sprite
                    sprite = self.memory[self.index_reg + i] # Ogni sprite é formato da 8 bit che se 0 o 1 indicano se il pixel é accesso o spento

                    for j in range(8): # Loop per ciclare ogni bit dello sprite
                        if sprite & 0x80: # prendialo il bit piú sinistra
                            if self.monitor.set_pixel(self.reg_v[x] + j, self.reg_v[y] + i):
                                self.reg_v[0xF] = 1 # C'é stata una collisione
                        sprite = sprite << 1
            case 0xE000:
                match kk:
                    case 0x9E:
                        if self.keyboard.is_key_pressed(self.reg_v[x]):
                            self.pc += 2
                    case 0xA1:
                        if not self.keyboard.is_key_pressed(self.reg_v[x]):
                            self.pc += 2
            case 0xF000:
                match kk:
                    case 0x07:
                        self.reg_v[x] = self.delay_timer
                    case 0x0A:
                        is_key_pressed = True
                        self.pygame_event_handle()
                        while is_key_pressed:
                            for i, is_pressed in enumerate(self.keyboard.key_pressed):
                                if is_pressed:
                                    self.reg_v[x] = i
                                    is_key_pressed = False
                                    break
                    case 0x15:
                        self.delay_timer = self.reg_v[x]
                    case 0x18:
                        self.sound_timer = self.reg_v[x]
                    case 0x1E:
                        self.index_reg += self.reg_v[x]
                    case 0x29:
                        self.index_reg = self.reg_v[x]*5
                    case 0x33:
                        '''
                        L’operatore // fa una divisione intera, 
                        cioè elimina la parte decimale e ti dà solo il quoziente intero. 
                        È molto utile quando lavori con valori interi
                        '''
                        self.memory[self.index_reg] = self.reg_v[x] // 100 # Centinaia
                        self.memory[self.index_reg + 1] = self.reg_v[x] % 100 // 10 # Decine
                        self.memory[self.index_reg + 2] = self.reg_v[x] % 10 # Unità
                    case 0x55:
                        for i in range(x + 1):
                            self.memory[self.index_reg + i] = self.reg_v[i]
                    case 0x65:
                        for i in range(x + 1):
                            self.reg_v[i] = self.memory[self.index_reg + i]