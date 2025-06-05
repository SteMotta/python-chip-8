from os.path import exists
import pygame
import pygame_gui
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
        ('All files', '*.*')
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

    slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((200, 200), (400, 40)), start_value=1., value_range=(1, (get_monitors()[0].width/WIDTH_CHIP)), manager=manager)
    text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 150), (400, 40)), html_text="", manager=manager, anchors={'left': 'left',
                   'right': 'right',
                   'top': 'top',
                   'bottom': 'bottom'})
    file_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((620, 150), (400, 40)), text="Apri File", manager=manager)
    load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 260), (420, 40)), text="Load", manager=manager)
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
                if event.ui_element == load_button:
                    monitor.set_scale(int(slider.get_current_value()))
                    running_gui = False
            manager.process_events(event)

        manager.update(time_delta)

        current_scale = int(slider.get_current_value())
        text_box.set_text("Scale = " + str(current_scale) +  " Width = " + str(WIDTH_CHIP*current_scale) + "px Height = " + str(HEIGHT_CHIP*current_scale) + "px")
        manager.draw_ui(monitor.get_win())

        pygame.display.flip()

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