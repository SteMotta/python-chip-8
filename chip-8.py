from os.path import exists
import pygame
import pygame_gui
from keyboard import Keyboard
from monitor import Monitor
from cpu import Cpu
import sys
from tkinter import filedialog


def select_file():
    filetypes = (
        ('CHIP-8 Rom', '*.ch8'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    return filename

def main():
    print(sys.argv)

    rom = sys.argv[1]

    monitor = Monitor(20)
    keyboard = Keyboard()
    cpu = Cpu(monitor, keyboard)
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager(monitor.get_resolution())

    slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((350, 275), (500, 50)), start_value=0., value_range=(0, 30), manager=manager)
    text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 150), (200, 30)), html_text="<p>" + "C:/" + "</p>", manager=manager, anchors={'left': 'left',
                   'right': 'right',
                   'top': 'top',
                   'bottom': 'bottom'})
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 150), (200, 30)), text="Apri File", manager=manager)

    file_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((400, 350), (200, 30)), html_text="", manager=manager, )


    running_gui = True
    while running_gui:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    file_box.set_text(select_file())
                    file_box.disable()
            manager.process_events(event)

        manager.update(time_delta)
        text_box.set_text(str(int(slider.get_current_value())))
        manager.draw_ui(monitor.get_win())

        pygame.display.flip()

    manager.clear_and_reset()
    pygame.display.flip()

    cpu.load_sprite()

    if exists(rom):
        cpu.load_rom(rom)
    else:
        print("ROM not found")
        sys.exit()

    while True:
        clock.tick(60)
        cpu.cycle()

if __name__ == "__main__": main()