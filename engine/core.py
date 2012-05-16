import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP
from engine.render import Renderer
from engine.controls import KeyBoardController
from engine.widgets import WidgetHandler
from engine.gameclock import GameClock


class GameCore(object):

    def __init__(self, viewport_size=(800, 600)):

        pygame.init()
        self.renderer = Renderer(viewport_size)

        self.keyboard_controller = KeyBoardController()
        self.widgets = WidgetHandler()

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

    def _master_update(self, dt):
        self._handle_events()
        self._update(dt)

    def _master_draw(self, interpolation):
        self._update_widgets(interpolation)
        self.renderer.reset_view()
        self._draw(interpolation)
        self.renderer.draw_sprite_map(self.widgets.get_widget_map())
        self.renderer.update()

    def _handle_events(self):

        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == KEYUP:
                keystates = pygame.key.get_pressed()
                self.keyboard_controller.evaluate_keystates(keystates)

    def _update(self, dt):
        '''Update the game state'''
        return

    def _draw(self, interpolation):
        '''Update the display'''
        return

    def _update_widgets(self, interpolation):
        '''Update any widgets'''
        self.widgets.update(interpolation)

    def run(self):
        while True:
            self.clock.tick()
