import pygame
from pygame.locals import *
from render import Renderer
from controls import KeyBoardController
from widgets import WidgetHandler, TextWidget
from utils import quit
from pygame.time import Clock

#config settings
KEY_REPEAT_DELAY = 250  # how long to wait before resending held down keys
KEY_REPEAT_INTERVAL = 100  # how often to resend held down keys

VIEWPORT_SIZE = (800, 600)
TARGET_FPS = 30

#initialize pygame
pygame.init()

#create a new renderer
renderer = Renderer(VIEWPORT_SIZE)

#create a new controller
#TODO: refactor player controls to abstract actions from implementation
keyboard_controller = KeyBoardController({
    K_ESCAPE: quit
})

keyboard_controller.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

#create a widget handler
widget_handler = WidgetHandler()

#simple widget to show tick
fps_display = TextWidget(font_size=40)
widget_handler.add_widget('fps_display', fps_display, (20, 20))

#create our fps clock
fps_clock = Clock()

while True:
    fps_display.set_text(round(fps_clock.get_fps(), 2))

    #TODO: decouple physics tick from renderer tick
    renderer.reset_view()
    widgets = widget_handler.get_widget_map()
    renderer.draw_sprite_map(widgets)
    renderer.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN or event.type == KEYUP:
            keystates = pygame.key.get_pressed()
            keyboard_controller.evaluate_keystates(keystates)

    fps_clock.tick_busy_loop(30)
