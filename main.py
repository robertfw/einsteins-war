from engine.core import GameCore
from engine.widgets import TextWidget
from engine.utils import quit
from pygame.locals import K_ESCAPE

from game.system import System
from game.renderers import render_system


class Game(GameCore):

    def __init__(self):
        super(Game, self).__init__()

        fps_display = TextWidget(binding=lambda: round(self.clock.fps, 2), font_size=20, color=(0, 255, 0))
        ups_display = TextWidget(binding=lambda: round(self.clock.ups, 2), font_size=20, color=(50, 50, 255))
        self.widgets.add_widget('fps_display', fps_display, (20, 20))
        self.widgets.add_widget('ups_display', ups_display, (100, 20))

        self.keyboard_controller.bindings = {
            K_ESCAPE: quit
        }

        self.system = System()

    def _update(self, dt):
        render_system(self.renderer, self.system)

    def _draw(self, interpolation):
        pass

Game().run()
