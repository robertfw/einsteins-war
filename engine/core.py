import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from engine.render import Display, WindowManager
from engine.controls import KeyBoardController, MouseController
from engine.widgets import WidgetHandler
from engine.gameclock import GameClock


class GameCore(object):
    display = None
    keyboard = None
    widgets = None
    windows = None
    clock = None
    update_callbacks = []
    pre_render_callbacks = []
    post_render_callbacks = []

    def __init__(self, *args, **kwargs):

        pygame.init()
        
        self.display = Display(*args)
        self.keyboard = KeyBoardController()
        self.mouse = MouseController()
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

    def unregister_update_callback(self, callback):
        self.update_callbacks.remove(callback)

    def register_pre_render_callback(self, callback):
        self.pre_render_callbacks.append(callback)

    def unregister_pre_render_callback(self, callback):
        self.pre_render_callbacks.remove(callback)

    def register_post_render_callback(self, callback):
        self.post_render_callbacks.append(callback)

    def unregister_post_render_callback(self, callback):
        self.post_render_callbacks.remove(callback)

    def _update(self, dt):
        self._handle_events()

        for callback in self.update_callbacks:
            callback(dt)

    def _draw(self, interpolation):
        # blank the screen
        self.display.reset_view()

        #run any pre-render callbacks
        for callback in self.pre_render_callbacks:
            callback(self.display)

        # tell all windows to render
        #TODO: should we denote that get_window_layers returns a generator?
        map(lambda layer: self.display.draw_sprite_map(layer), self.windows.get_window_layers(interpolation))

        #draw any widgets
        self.widgets.update(interpolation)
        self.display.draw_sprite_map(self.widgets.get_widget_map())

        #run any post-render callbacks
        for callback in self.post_render_callbacks:
            callback(self.display)

        #update the display
        self.display.update()

    def _handle_events(self):
        keyboard_events = [KEYDOWN, KEYUP]
        mouse_events = [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]

        for event in pygame.event.get():
            if event.type in keyboard_events:
                self.keyboard.handle(event)
            elif event.type in mouse_events:
                self.mouse.handle(event)

    def run(self):
        '''Run the game loop'''
        while True:
            self.clock.tick()
