from os.path import exists
import pygame
import pygame_gui
from pygame import Color

from keyboard import Keyboard
from monitor import Monitor
from cpu import Cpu
import sys
from tkinter import filedialog
from screeninfo import get_monitors

WIDTH_CHIP, HEIGHT_CHIP = 64, 32

def select_file():
    filetypes = (
        ('CHIP-8 Rom', '*.ch8'),
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    return filename

def main():
    print(sys.argv)

    monitor = Monitor(20)
    keyboard = Keyboard()
    cpu = Cpu(monitor, keyboard)
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager(monitor.get_resolution())

    background = pygame.Surface(monitor.get_resolution())

    background.fill(pygame.Color('#000000'))

    slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((200, 200), (400, 40)), start_value=1., value_range=(1, (get_monitors()[0].width/WIDTH_CHIP)), manager=manager)
    resolution_text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 150), (400, 40)), html_text="", manager=manager, anchors={'left': 'left',
                   'right': 'right',
                   'top': 'top',
                   'bottom': 'bottom'})
    file_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((620, 150), (400, 40)), text="Apri File", manager=manager)

    load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 260), (420, 40)), text="Load", manager=manager)

    color_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 320), (360, 40)), text="Pick Primary Color", manager=manager)

    rgb_color = pygame_gui.windows.UIColourPickerDialog(rect=(780, 220, 390, 390), manager=manager,
                                                        initial_colour=Color(255, 255, 255))
    rgb_color.hide()

    file_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((620, 200), (400, 40)), html_text="", manager=manager)
    load_button.disable()


    running_gui = True
    while running_gui:
        time_delta = clock.tick(60) / 1000.0



        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == file_button:
                    pass
                    try:
                        file_box.set_text(select_file())
                        load_button.enable()
                    except:
                        pass
                    file_box.disable()
                elif event.ui_element == load_button:
                    monitor.set_scale(int(slider.get_current_value()))
                    running_gui = False
                elif event.ui_element == color_button:
                    rgb_color = pygame_gui.windows.UIColourPickerDialog(rect=(780, 220, 390, 390), manager=manager,
                                                                        initial_colour=rgb_color.get_colour())
                    rgb_color.show()
            manager.process_events(event)

        manager.update(time_delta)

        monitor.get_win().blit(background, (0, 0))
        current_scale = int(slider.get_current_value())
        resolution_text_box.set_text("Scale = " + str(current_scale) + " Width = " + str(WIDTH_CHIP * current_scale) + "px Height = " + str(HEIGHT_CHIP * current_scale) + "px")

        pygame.draw.rect(monitor.get_win(), rgb_color.get_colour(), ((780, 320), (40, 40)), 0) # Currect colour
        manager.draw_ui(monitor.get_win())

        pygame.display.flip()

    monitor.set_colour(rgb_color.get_colour())
    manager.clear_and_reset()
    pygame.display.flip()

    cpu.load_sprite()

    if exists(file_box.html_text):
        cpu.load_rom(file_box.html_text)
    else:
        print("ROM not found")
        sys.exit()

    while True:
        clock.tick(60)
        cpu.cycle()

if __name__ == "__main__": main()