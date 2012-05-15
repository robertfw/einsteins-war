import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP, K_ESCAPE
from engine.render import Renderer
from engine.controls import KeyBoardController
from engine.widgets import WidgetHandler, TextWidget
from engine.utils import quit
from engine.gameclock import GameClock


class GameCore(object):

    def __init__(self,
                 key_repeat_delay=250,
                 key_repeat_interval=100,
                 viewport_size=(800, 600)):

        #initialize pygame
        pygame.init()

        #create a new renderer
        self.renderer = Renderer(viewport_size)

        #create a new controller
        #TODO: refactor controls to be more abstract
        self.keyboard_controller = KeyBoardController({
            K_ESCAPE: quit
        })

        self.keyboard_controller.set_repeat(key_repeat_delay, key_repeat_interval)

        #create a widget handler
        self.widgets = WidgetHandler()

        #simple widget to show tick
        fps_display = TextWidget(font_size=40)
        ups_display = TextWidget(font_size=40)
        self.widgets.add_widget('fps_display', fps_display, (20, 20))
        self.widgets.add_widget('ups_display', ups_display, (20, 100))

        if sys.platform in('win32', 'cygwin'):
            time_source = None
        else:
            time_source = lambda: pygame.time.get_ticks() / 1000.

        self.clock = GameClock(max_ups=30,
                  max_fps=0,
                  use_wait=False,
                  update_callback=self._master_update,
                  frame_callback=self._master_draw,
                  paused_callback=None,
                  time_source=time_source
                  )

    def _update(self, dt):
        '''Update the game state'''
        return

    def _master_update(self, dt):
        self._handle_events()
        self._update(dt)

    def _draw(self, interpolation):
        '''Update the display'''
        return

    def _master_draw(self, interpolation):
        self.renderer.reset_view()
        self._draw(interpolation)
        self.renderer.draw_sprite_map(self.widgets.get_widget_map())
        self.renderer.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == KEYUP:
                keystates = pygame.key.get_pressed()
                self.keyboard_controller.evaluate_keystates(keystates)

    def run(self):
        while True:
            self.clock.tick()
