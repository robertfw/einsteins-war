import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP
from engine.render import Display, WindowManager
from engine.controls import KeyBoardController
from engine.widgets import WidgetHandler
from engine.gameclock import GameClock


class GameCore(object):
    display = None
    keyboard = None
    widgets = None
    windows = None
    clock = None
    update_callbacks = []

    def __init__(self, resolution=(800, 600)):

        pygame.init()
        
        self.display = Display(resolution)
        self.keyboard = KeyBoardController()
        self.widgets = WidgetHandler()
        self.windows = WindowManager()

        if sys.platform in('win32', 'cygwin'):
            time_source = None
        else:
            time_source = lambda: pygame.time.get_ticks() / 1000.

        self.clock = GameClock(max_ups=30,
                  max_fps=0,
                  use_wait=False,
                  update_callback=self._update,
                  frame_callback=self._draw,
                  paused_callback=None,
                  time_source=time_source
                  )

    def register_update_callback(self, callback):
        self.update_callbacks.append(callback)

    def _update(self, dt):
        self._handle_events()

        for callback in self.update_callbacks:
            callback(dt)

    def _draw(self, interpolation):
        # blank the screen
        self.display.reset_view()

        # tell all windows to render
        window_layers = self.windows.get_window_layers(interpolation)
        for layer in window_layers:
            self.display.draw_sprite_map(layer)

        #draw any widgets
        self.widgets.update(interpolation)
        self.display.draw_sprite_map(self.widgets.get_widget_map())

        #update the display
        self.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == KEYUP:
                self.keyboard.evaluate_keystates()

    def run(self):
        '''Run the game loop'''
        while True:
            self.clock.tick()
