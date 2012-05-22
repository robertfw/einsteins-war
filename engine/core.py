import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP
from engine.render import Display, WindowManager
from engine.controls import KeyBoardController
from engine.widgets import WidgetHandler
from engine.gameclock import GameClock


class GameCore(object):

    def __init__(self, resolution=(800, 600)):

        pygame.init()
        self.display = Display(resolution)

        self.keyboard_controller = KeyBoardController()
        self.widgets = WidgetHandler()
        self.windows = WindowManager(display=self.display)

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
        # tell all widgets to update their data
        self._update_widgets(interpolation)
        
        # blank the screen
        self.display.reset_view()

        #call the game specific draw method
        self._draw(interpolation)

        #draw any widgets
        self.display.draw_sprite_map(self.widgets.get_widget_map())

        #update the display
        self.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == KEYUP:
                self.keyboard_controller.evaluate_keystates()

    def _update(self, dt):
        '''abstract, Update the game state'''
        return

    def _draw(self, interpolation):
        '''abstract, Update the display'''
        return

    def _update_widgets(self, interpolation):
        '''Update any widgets'''
        self.widgets.update(interpolation)

    def _update_windows(self, interpolation):
        '''Update any windows'''
        self.windows.render(interpolation)

    def run(self):
        '''Run the game loop'''
        while True:
            self.clock.tick()
