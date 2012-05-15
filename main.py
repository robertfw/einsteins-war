import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP, K_ESCAPE
from engine.render import Renderer
from engine.controls import KeyBoardController
from engine.widgets import WidgetHandler, TextWidget
from engine.utils import quit
from engine.gameclock import GameClock


class Game(object):
    clock = None
    renderer = None

    def __init__(self):
        #config settings
        KEY_REPEAT_DELAY = 250  # how long to wait before resending held down keys
        KEY_REPEAT_INTERVAL = 100  # how often to resend held down keys

        VIEWPORT_SIZE = (800, 600)

        #initialize pygame
        pygame.init()

        #create a new renderer
        self.renderer = Renderer(VIEWPORT_SIZE)

        #create a new controller
        #TODO: refactor player controls to abstract actions from implementation
        self.keyboard_controller = KeyBoardController({
            K_ESCAPE: quit
        })

        self.keyboard_controller.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

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
                  update_callback=self._update,
                  frame_callback=self._draw,
                  paused_callback=None,
                  time_source=time_source
                  )

    def run(self):
        while True:
            self.clock.tick()

    def _update(self, interpolation):
        self._handle_events()

    def _draw(self, dt):
        self.widgets.get_widget('fps_display').set_text('fps: {fps}'.format(fps=round(self.clock.fps, 2)))
        self.widgets.get_widget('ups_display').set_text('ups: {ups}'.format(ups=round(self.clock.ups, 2)))

        self.renderer.reset_view()
        self.renderer.draw_sprite_map(self.widgets.get_widget_map())
        self.renderer.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == KEYUP:
                keystates = pygame.key.get_pressed()
                self.keyboard_controller.evaluate_keystates(keystates)

Game().run()
