import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP, K_ESCAPE
from engine.render import Renderer
from engine.controls import KeyBoardController
from engine.widgets import WidgetHandler, TextWidget
from engine.utils import quit
from engine.gameclock import GameClock

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

#create our game clock
if sys.platform in('win32', 'cygwin'):
    time_source = None
else:
    time_source = lambda: pygame.time.get_ticks() / 1000.

clock = GameClock(ticks_per_second=30,
                  max_fps=0,
                  use_wait=False,
                  max_frame_skip=5,
                  update_callback=None,
                  frame_callback=None,
                  time_source=time_source
                  )

while True:
    fps_display.set_text(round(clock.get_fps(), 2))

    clock.tick()

    #TODO: convert this to use callbacks
    if clock.update_ready:
        pass
    elif clock.frame_ready:
        renderer.reset_view()
        widgets = widget_handler.get_widget_map()
        renderer.draw_sprite_map(widgets)
        renderer.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN or event.type == KEYUP:
            keystates = pygame.key.get_pressed()
            keyboard_controller.evaluate_keystates(keystates)
